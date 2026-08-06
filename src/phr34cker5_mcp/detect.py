"""
Tone & DTMF detection — the *perception* half of the audio pipeline.

Pure Python (stdlib only). Consumes the same mono 8 kHz signed-16 LE PCM that
`tones.py` produces and that the Twilio bridge captures inbound, and answers
two questions:

  * "what tone is this?"   -> Goertzel power at named target frequencies
                              (dial tone, busy, ringback, 2600, CNG, CED,
                              milliwatt, modem), plus a coarse cadence estimate
                              so busy (~0.5s) can be told from reorder (~0.25s).
  * "what digits are these?" -> frame-by-frame DTMF decode with twist and
                              relative-power validation, debounced into a
                              digit string.

The Goertzel algorithm computes the power in a single DFT bin without a full
FFT — cheap, exact for a known frequency, and easy to reason about. That's the
right tool when you already know which frequencies matter (and in telephony you
always do).
"""

from __future__ import annotations

import array
import math
import sys
from dataclasses import dataclass

SAMPLE_RATE = 8000


# --- PCM unpacking -----------------------------------------------------------


def pcm16_to_samples(pcm: bytes) -> array.array:
    """Decode mono signed-16 LE PCM bytes into an array of ints."""
    a = array.array("h")
    # Drop a trailing odd byte if the buffer isn't frame-aligned.
    usable = len(pcm) - (len(pcm) % 2)
    a.frombytes(pcm[:usable])
    if sys.byteorder == "big":  # our PCM is little-endian on the wire
        a.byteswap()
    return a


# --- Goertzel ----------------------------------------------------------------


def goertzel_power(samples, freq_hz: float, sample_rate: int = SAMPLE_RATE) -> float:
    """
    Power in the DFT bin nearest `freq_hz` for the given samples.

    Returns |X_k|^2 (unnormalized). Compare bins to each other, or normalize
    against total energy via `energy_ratio`.
    """
    n = len(samples)
    if n == 0:
        return 0.0
    w = 2.0 * math.pi * (freq_hz / sample_rate)
    coeff = 2.0 * math.cos(w)
    s1 = 0.0
    s2 = 0.0
    for x in samples:
        s0 = x + coeff * s1 - s2
        s2 = s1
        s1 = s0
    return s1 * s1 + s2 * s2 - coeff * s1 * s2


def _total_energy(samples) -> float:
    return float(sum(x * x for x in samples))


def energy_ratio(samples, freq_hz: float, sample_rate: int = SAMPLE_RATE) -> float:
    """
    Fraction of the window's energy sitting in `freq_hz`, in [0, ~0.5].

    A clean single tone at the target reads ~0.5; each leg of an equal-amplitude
    dual tone reads ~0.25; broadband noise or an off-target tone reads ~0.
    """
    n = len(samples)
    if n == 0:
        return 0.0
    e = _total_energy(samples)
    if e <= 0.0:
        return 0.0
    return goertzel_power(samples, freq_hz, sample_rate) / (n * e)


# --- named tone targets ------------------------------------------------------
#
# US "precise tone plan" frequencies. Cadence is (on_ms, off_ms); None = the
# tone is continuous. busy and reorder share frequencies and differ only in
# cadence — that's why the detector reports a cadence estimate.


@dataclass(frozen=True)
class ToneTarget:
    name: str
    freqs: tuple[float, ...]
    cadence: tuple[int, int] | None  # (on_ms, off_ms) or None for continuous
    note: str = ""


TONE_TARGETS: dict[str, ToneTarget] = {
    "dial-tone": ToneTarget("dial-tone", (350.0, 440.0), None, "US precise dial tone"),
    "busy":      ToneTarget("busy", (480.0, 620.0), (500, 500), "line busy"),
    "reorder":   ToneTarget("reorder", (480.0, 620.0), (250, 250), "fast busy / all-trunks-busy"),
    "ringback":  ToneTarget("ringback", (440.0, 480.0), (2000, 4000), "audible ring"),
    "2600":      ToneTarget("2600", (2600.0,), None, "SF trunk supervision"),
    "cng":       ToneTarget("cng", (1100.0,), (500, 3000), "T.30 fax calling tone"),
    "ced":       ToneTarget("ced", (2100.0,), None, "T.30 called-station / V.25 answer tone"),
    "milliwatt": ToneTarget("milliwatt", (1004.0,), None, "1004 Hz test tone (also 1000 Hz)"),
    "modem":     ToneTarget("modem", (2100.0,), None, "V.25 answer tone — overlaps CED; see cadence/carrier"),
}

DEFAULT_TARGETS = ("dial-tone", "busy", "ringback", "2600", "cng", "ced", "modem", "milliwatt")

# Per-frequency energy-ratio floor for a leg to count as "present".
_PRESENCE_FLOOR = 0.08


# --- cadence estimation ------------------------------------------------------


def energy_envelope(samples, sample_rate: int = SAMPLE_RATE, window_ms: int = 40) -> list[float]:
    """RMS per non-overlapping window — the on/off envelope of the signal."""
    win = max(1, int(sample_rate * window_ms / 1000))
    env: list[float] = []
    for start in range(0, len(samples), win):
        chunk = samples[start:start + win]
        if not chunk:
            break
        rms = math.sqrt(sum(x * x for x in chunk) / len(chunk))
        env.append(rms)
    return env


@dataclass(frozen=True)
class Cadence:
    continuous: bool
    on_ms: int
    off_ms: int


def estimate_cadence(samples, sample_rate: int = SAMPLE_RATE, window_ms: int = 40) -> Cadence:
    """
    Coarse on/off timing from the energy envelope. Thresholds at half the peak
    RMS; measures the mean length of on-runs and off-runs. `continuous` is True
    when there's essentially no gap (envelope never drops below threshold).
    """
    env = energy_envelope(samples, sample_rate, window_ms)
    if not env:
        return Cadence(continuous=False, on_ms=0, off_ms=0)
    peak = max(env)
    if peak <= 0.0:
        return Cadence(continuous=False, on_ms=0, off_ms=0)
    thresh = peak * 0.5
    states = [e >= thresh for e in env]

    on_runs: list[int] = []
    off_runs: list[int] = []
    run_len = 1
    for i in range(1, len(states)):
        if states[i] == states[i - 1]:
            run_len += 1
        else:
            (on_runs if states[i - 1] else off_runs).append(run_len)
            run_len = 1
    (on_runs if states[-1] else off_runs).append(run_len)

    # No interior off-run reaching threshold-low → treat as continuous.
    continuous = not any(off_runs) or all(s for s in states)
    on_ms = int(round(sum(on_runs) / len(on_runs) * window_ms)) if on_runs else 0
    off_ms = int(round(sum(off_runs) / len(off_runs) * window_ms)) if off_runs else 0
    return Cadence(continuous=continuous, on_ms=on_ms, off_ms=off_ms)


def _cadence_matches(target: ToneTarget, cad: Cadence) -> bool | None:
    """True/False if the cadence corroborates the target; None if untestable."""
    if target.cadence is None:
        return cad.continuous or None
    if cad.continuous:
        return False
    on, off = target.cadence
    # Generous ±60% windows — real audio and our short capture windows are noisy.
    def near(measured: int, expected: int) -> bool:
        return abs(measured - expected) <= max(80, int(expected * 0.6))
    return near(cad.on_ms, on) and near(cad.off_ms, off)


def _cadence_multiplier(target: ToneTarget, cad: Cadence) -> float:
    """
    Scoring multiplier from how well the cadence corroborates the target.

    Graded (not boolean) on the on/off *period* so tones that share frequencies
    and differ only in timing — busy (1000 ms period) vs. reorder (500 ms) —
    separate cleanly instead of both landing inside a loose window.
    """
    if target.cadence is None:
        # Continuous target: reward a continuous capture, penalize a chopped one.
        return 1.3 if cad.continuous else 0.6
    if cad.continuous:
        return 0.4  # cadenced target but the audio never gaps
    expected_period = sum(target.cadence)
    measured_period = cad.on_ms + cad.off_ms
    if expected_period <= 0:
        return 1.0
    rel_err = abs(measured_period - expected_period) / expected_period
    # 1.5 at a perfect match, decaying toward ~0.7 as the period drifts.
    return 0.7 + 0.8 * math.exp(-rel_err)


# --- tone detection ----------------------------------------------------------


def detect_tones(
    pcm: bytes,
    targets: list[str] | tuple[str, ...] | None = None,
    sample_rate: int = SAMPLE_RATE,
) -> dict:
    """
    Score the buffer against named tone targets.

    Returns dominant frequencies, a cadence estimate, and per-target matches
    (frequency presence + whether the cadence corroborates). `best` is the
    highest-scoring target whose frequencies are present.
    """
    samples = pcm16_to_samples(pcm)
    names = list(targets) if targets else list(DEFAULT_TARGETS)
    cad = estimate_cadence(samples, sample_rate)

    # Dominant frequencies: scan the union of all target legs, report the top 3.
    scan_freqs = sorted({f for n in names if n in TONE_TARGETS for f in TONE_TARGETS[n].freqs})
    freq_ratios = {f: energy_ratio(samples, f, sample_rate) for f in scan_freqs}
    dominant = sorted(freq_ratios.items(), key=lambda kv: kv[1], reverse=True)[:3]

    matches = []
    for name in names:
        t = TONE_TARGETS.get(name)
        if t is None:
            continue
        legs = {f: freq_ratios.get(f, energy_ratio(samples, f, sample_rate)) for f in t.freqs}
        min_leg = min(legs.values()) if legs else 0.0
        present = min_leg >= _PRESENCE_FLOOR
        cadence_ok = _cadence_matches(t, cad)
        # Score: frequency strength, scaled by how well the cadence corroborates.
        score = min_leg * _cadence_multiplier(t, cad)
        matches.append({
            "name": name,
            "present": present,
            "energy_ratio": round(min_leg, 4),
            "freqs_hz": list(t.freqs),
            "cadence_ok": cadence_ok,
            "score": round(score, 4),
            "note": t.note,
        })

    matches.sort(key=lambda m: m["score"], reverse=True)
    present_matches = [m for m in matches if m["present"]]
    best = present_matches[0]["name"] if present_matches else None

    return {
        "captured_ms": int(len(samples) * 1000 / sample_rate),
        "dominant_freqs": [{"freq_hz": f, "energy_ratio": round(r, 4)} for f, r in dominant],
        "cadence": {"continuous": cad.continuous, "on_ms": cad.on_ms, "off_ms": cad.off_ms},
        "matches": matches,
        "best": best,
    }


# --- DTMF decode -------------------------------------------------------------

_DTMF_LOW_FREQS = (697.0, 770.0, 852.0, 941.0)
_DTMF_HIGH_FREQS = (1209.0, 1336.0, 1477.0, 1633.0)

# (low_index, high_index) -> digit
_DTMF_GRID = {
    (0, 0): "1", (0, 1): "2", (0, 2): "3", (0, 3): "A",
    (1, 0): "4", (1, 1): "5", (1, 2): "6", (1, 3): "B",
    (2, 0): "7", (2, 1): "8", (2, 2): "9", (2, 3): "C",
    (3, 0): "*", (3, 1): "0", (3, 2): "#", (3, 3): "D",
}


def _classify_frame(samples, sample_rate: int) -> str | None:
    """Return the DTMF digit in this frame, or None if it isn't a clean digit."""
    e = _total_energy(samples)
    if e <= 0.0:
        return None
    lows = [goertzel_power(samples, f, sample_rate) for f in _DTMF_LOW_FREQS]
    highs = [goertzel_power(samples, f, sample_rate) for f in _DTMF_HIGH_FREQS]

    li = max(range(4), key=lambda i: lows[i])
    hi = max(range(4), key=lambda i: highs[i])
    low_p, high_p = lows[li], highs[hi]

    n = len(samples)
    # Each leg must hold a real share of the window energy.
    if low_p / (n * e) < _PRESENCE_FLOOR or high_p / (n * e) < _PRESENCE_FLOOR:
        return None

    # Reject broadband: the winning bin must dominate the runners-up in its group.
    second_low = max(lows[i] for i in range(4) if i != li)
    second_high = max(highs[i] for i in range(4) if i != hi)
    if low_p < 4.0 * (second_low + 1e-9) or high_p < 4.0 * (second_high + 1e-9):
        return None

    # Twist: high/low amplitude ratio in dB. Real DTMF sits within ~±10 dB.
    low_amp = math.sqrt(low_p)
    high_amp = math.sqrt(high_p)
    if low_amp <= 0.0 or high_amp <= 0.0:
        return None
    twist_db = 20.0 * math.log10(high_amp / low_amp)
    if not (-12.0 <= twist_db <= 12.0):
        return None

    return _DTMF_GRID.get((li, hi))


def decode_dtmf(
    pcm: bytes,
    sample_rate: int = SAMPLE_RATE,
    frame_ms: int = 25,
    min_digit_ms: int = 40,
) -> dict:
    """
    Decode a DTMF sequence from PCM16 audio.

    Frames the signal, classifies each frame, then collapses runs of the same
    digit into one press (requiring `min_digit_ms` to reject blips and needing
    a gap or a change to separate repeated digits).

    Returns {"digits": "...", "detail": [{digit,start_ms,duration_ms}, ...]}.
    """
    samples = pcm16_to_samples(pcm)
    frame = max(1, int(sample_rate * frame_ms / 1000))
    per_frame: list[str | None] = []
    for start in range(0, len(samples) - frame + 1, frame):
        per_frame.append(_classify_frame(samples[start:start + frame], sample_rate))

    detail = []
    digits = []
    i = 0
    min_frames = max(1, int(math.ceil(min_digit_ms / frame_ms)))
    while i < len(per_frame):
        d = per_frame[i]
        if d is None:
            i += 1
            continue
        j = i
        while j < len(per_frame) and per_frame[j] == d:
            j += 1
        run = j - i
        if run >= min_frames:
            digits.append(d)
            detail.append({
                "digit": d,
                "start_ms": int(i * frame_ms),
                "duration_ms": int(run * frame_ms),
            })
        i = j

    return {"digits": "".join(digits), "detail": detail}
