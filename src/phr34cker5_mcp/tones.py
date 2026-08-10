"""
Tone synthesis — pure Python (stdlib only).

Primitives:
  sine(freq_hz, ms)          — one frequency
  dual_tone(f1, f2, ms)      — sum of two sines (the phreaking primitive)
  silence(ms)                — flat zeros

Signaling systems:
  dtmf(digits, ...)          — 0-9, *, #, A-D (autovon), with ,/p for pauses
  mf(digits, ...)            — R1 MF: 0-9, KP (K), ST (S), and ST' variants
  sf_2600(ms, ...)           — the 2600 Hz single-frequency supervision tone
  red_box(coin_string, ...)  — ACTS coin-deposit tones (n, d, q)

All *_bytes helpers return raw signed-16-bit little-endian PCM samples.
Public write_wav() wraps them into a canonical WAV file via stdlib `wave`.
"""

from __future__ import annotations

import math
import struct
import wave
from dataclasses import dataclass


SAMPLE_RATE = 8000  # good enough for telephony; matches historical audio
AMPLITUDE = 0.6     # 0..1; leave headroom to avoid clipping on dual tones


# --- primitives --------------------------------------------------------------


def _samples(ms: int) -> int:
    return max(0, int(SAMPLE_RATE * ms / 1000))


def sine_bytes(freq_hz: float, ms: int, amplitude: float = AMPLITUDE) -> bytes:
    n = _samples(ms)
    step = 2 * math.pi * freq_hz / SAMPLE_RATE
    scale = amplitude * 32767
    out = bytearray(n * 2)
    for i in range(n):
        v = int(scale * math.sin(step * i))
        struct.pack_into("<h", out, i * 2, v)
    return bytes(out)


def dual_tone_bytes(
    f1: float, f2: float, ms: int, amplitude: float = AMPLITUDE
) -> bytes:
    n = _samples(ms)
    step1 = 2 * math.pi * f1 / SAMPLE_RATE
    step2 = 2 * math.pi * f2 / SAMPLE_RATE
    # Two summed sines can peak at 2*amp; halve to preserve headroom.
    scale = (amplitude / 2) * 32767
    out = bytearray(n * 2)
    for i in range(n):
        v = int(scale * (math.sin(step1 * i) + math.sin(step2 * i)))
        struct.pack_into("<h", out, i * 2, v)
    return bytes(out)


def silence_bytes(ms: int) -> bytes:
    return b"\x00\x00" * _samples(ms)


# --- DTMF --------------------------------------------------------------------

# Standard DTMF frequency grid (Hz). Rows are low tones, columns are high tones.
_DTMF_LOW = {"1": 697, "2": 697, "3": 697, "A": 697,
             "4": 770, "5": 770, "6": 770, "B": 770,
             "7": 852, "8": 852, "9": 852, "C": 852,
             "*": 941, "0": 941, "#": 941, "D": 941}
_DTMF_HIGH = {"1": 1209, "4": 1209, "7": 1209, "*": 1209,
              "2": 1336, "5": 1336, "8": 1336, "0": 1336,
              "3": 1477, "6": 1477, "9": 1477, "#": 1477,
              "A": 1633, "B": 1633, "C": 1633, "D": 1633}

DTMF_ALPHABET = set(_DTMF_LOW)


def _normalize_dtmf(digit: str) -> str:
    d = digit.upper()
    if d in DTMF_ALPHABET:
        return d
    raise ValueError(f"not a DTMF digit: {digit!r}")


def dtmf_bytes(
    digits: str,
    tone_ms: int = 100,
    gap_ms: int = 80,
    amplitude: float = AMPLITUDE,
) -> bytes:
    """
    Render a DTMF string to PCM bytes.

    `digits` accepts 0-9, *, #, A-D (case-insensitive). Any of
    ',', 'p', 'P', or whitespace inserts a pause of `gap_ms`.
    """
    out = bytearray()
    for ch in digits:
        if ch in (",", "p", "P") or ch.isspace():
            out += silence_bytes(gap_ms)
            continue
        d = _normalize_dtmf(ch)
        out += dual_tone_bytes(_DTMF_LOW[d], _DTMF_HIGH[d], tone_ms, amplitude)
        out += silence_bytes(gap_ms)
    return bytes(out)


# --- R1 MF (blue-box) --------------------------------------------------------

# R1 MF signaling: pairs of tones from {700, 900, 1100, 1300, 1500, 1700} Hz.
_MF = {
    "1": (700, 900),
    "2": (700, 1100),
    "3": (900, 1100),
    "4": (700, 1300),
    "5": (900, 1300),
    "6": (1100, 1300),
    "7": (700, 1500),
    "8": (900, 1500),
    "9": (1100, 1500),
    "0": (1300, 1500),
    # Control tones
    "K": (1100, 1700),  # KP — Key Pulse, start of address
    "S": (1500, 1700),  # ST — Start, end of address
    # (STP/ST2P/ST3P variants omitted here; add when needed.)
}

MF_ALPHABET = set(_MF)


def mf_bytes(
    digits: str,
    tone_ms: int = 68,   # historical R1 MF is ~60-75 ms per digit
    gap_ms: int = 68,
    kp_ms: int = 100,    # KP is longer than a data digit
    amplitude: float = AMPLITUDE,
) -> bytes:
    """
    Render an R1 MF string to PCM bytes.

    `digits` accepts 0-9, K (KP), S (ST), with ',' / 'p' / whitespace as
    a gap. A typical blue-box sequence is `K <digits> S`, e.g. `K18005551212S`.
    """
    out = bytearray()
    for ch in digits:
        if ch in (",", "p", "P") or ch.isspace():
            out += silence_bytes(gap_ms)
            continue
        d = ch.upper()
        if d not in _MF:
            raise ValueError(f"not an MF digit: {ch!r}")
        f1, f2 = _MF[d]
        dur = kp_ms if d == "K" else tone_ms
        out += dual_tone_bytes(f1, f2, dur, amplitude)
        out += silence_bytes(gap_ms)
    return bytes(out)


# --- SF supervision ----------------------------------------------------------


def sf_2600_bytes(ms: int = 1000, amplitude: float = AMPLITUDE) -> bytes:
    """The 2600 Hz trunk-idle supervision tone."""
    return sine_bytes(2600, ms, amplitude)


# --- call-progress / ambient network tones ----------------------------------
#
# The tones the network plays *at* the caller. Frequencies and cadences follow
# the US "precise tone plan" and match the detector targets in detect.py, so a
# generated tone round-trips through detect_tone() to the same classification.


def _cadenced_dual_tone_bytes(
    f1: float, f2: float, on_ms: int, off_ms: int, cycles: int,
    amplitude: float = AMPLITUDE,
) -> bytes:
    """`cycles` repetitions of (dual tone on, silence off) — a call-progress tone."""
    on = dual_tone_bytes(f1, f2, on_ms, amplitude)
    off = silence_bytes(off_ms)
    out = bytearray()
    for _ in range(max(1, cycles)):
        out += on
        out += off
    return bytes(out)


def busy_bytes(cycles: int = 4, amplitude: float = AMPLITUDE) -> bytes:
    """Line-busy tone: 480 + 620 Hz, 500 ms on / 500 ms off (60 IPM)."""
    return _cadenced_dual_tone_bytes(480, 620, 500, 500, cycles, amplitude)


def reorder_bytes(cycles: int = 8, amplitude: float = AMPLITUDE) -> bytes:
    """Reorder / fast-busy (all-trunks-busy): 480 + 620 Hz, 250 ms on / 250 ms off (120 IPM)."""
    return _cadenced_dual_tone_bytes(480, 620, 250, 250, cycles, amplitude)


def ringback_bytes(cycles: int = 2, amplitude: float = AMPLITUDE) -> bytes:
    """Audible ringback: 440 + 480 Hz, 2 s on / 4 s off."""
    return _cadenced_dual_tone_bytes(440, 480, 2000, 4000, cycles, amplitude)


def milliwatt_bytes(ms: int = 10000, amplitude: float = AMPLITUDE) -> bytes:
    """
    1004 Hz milliwatt test tone, continuous. Every CO had one at a known
    number; nominally 0 dBm0 (a true 'milliwatt') but we render at the shared
    AMPLITUDE for headroom. Older lines used 1000 Hz.
    """
    return sine_bytes(1004, ms, amplitude)


# --- modem carrier (synthetic) ----------------------------------------------
#
# NOT a real modem — this synthesizes the *audible signature* of a data answer
# so detect_tone() can be tested and a CTF flag can be matched by ear: the
# V.25 answer tone (2100 Hz, the CED cousin) followed by a rate-appropriate
# origin/carrier tone. It does not demodulate or negotiate anything.

# Representative low-band carrier/origin markers per rate. These are the tones
# a listener could pick out at the start of a connection, not the full spectra.
_MODEM_RATES = {
    "bell103": 1270,   # Bell 103 originate mark (F1) — soft, near-musical FSK
    "v21": 1180,       # V.21 channel-1 mark — also the fax control channel
    "v22": 1200,       # V.22/bis 1200 bps PSK carrier region
    "v32": 1800,       # V.32/bis 9600-14.4k carrier region ("roar")
    "v34": 1959,       # V.34 carrier region (up to 33.6k)
}

MODEM_RATE_ALPHABET = set(_MODEM_RATES)


def modem_carrier_bytes(
    rate: str = "v22",
    answer_ms: int = 3000,
    carrier_ms: int = 2000,
    amplitude: float = AMPLITUDE,
) -> bytes:
    """
    Synthesize a modem-answer signature: 2100 Hz V.25 answer tone, then a
    rate-appropriate carrier tone. `rate` in {bell103, v21, v22, v32, v34}.

    For detector tests and CTF flag-matching only — this is audio that *sounds*
    like a modem, not a modem.
    """
    r = rate.lower()
    if r not in _MODEM_RATES:
        raise ValueError(f"unknown modem rate: {rate!r} (want one of {sorted(_MODEM_RATES)})")
    out = bytearray()
    out += sine_bytes(2100, answer_ms, amplitude)          # V.25 answer tone
    out += sine_bytes(_MODEM_RATES[r], carrier_ms, amplitude)  # rate carrier marker
    return bytes(out)


# --- Red box (ACTS coin deposit) --------------------------------------------

# ACTS coin-deposit tones: 1700 + 2200 Hz, burst patterns per coin.
_ACTS_F = (1700, 2200)
_ACTS_BURSTS = {
    "n": [(66, 0)],                               # nickel:  one 66 ms burst
    "d": [(66, 66), (66, 0)],                     # dime:    two 66 ms bursts
    "q": [(33, 33)] * 4 + [(33, 0)],              # quarter: five 33 ms bursts
}
COIN_ALPHABET = set(_ACTS_BURSTS)


def red_box_bytes(
    coins: str,
    amplitude: float = AMPLITUDE,
    inter_coin_gap_ms: int = 250,
) -> bytes:
    """
    Render an ACTS coin string to PCM.

    `coins` is a sequence of n/d/q characters (case-insensitive). Anything
    non-alphabetic is treated as an inter-coin gap.
    Example: 'qqq' → three quarters (75 cents).
    """
    out = bytearray()
    coins_l = coins.lower()
    for i, ch in enumerate(coins_l):
        if not ch.isalpha():
            out += silence_bytes(inter_coin_gap_ms)
            continue
        if ch not in _ACTS_BURSTS:
            raise ValueError(f"not an ACTS coin: {ch!r} (want n/d/q)")
        for tone_ms, gap_ms in _ACTS_BURSTS[ch]:
            out += dual_tone_bytes(_ACTS_F[0], _ACTS_F[1], tone_ms, amplitude)
            if gap_ms:
                out += silence_bytes(gap_ms)
        # Between coins
        if i != len(coins_l) - 1:
            out += silence_bytes(inter_coin_gap_ms)
    return bytes(out)


# --- Green box (operator coin-control tones) --------------------------------
#
# The operator (TSPS) side of coin signaling — collect/return/ringback tones
# sent toward the payphone. A green box plays these from the caller side.
# Distinct from the red box: red = coin-deposit report (phone->CO), green =
# coin-control command (operator->phone). See knowledge/records/tones.json.

_GREEN = {
    "collect": (700, 1100),   # coin collect
    "return": (1100, 1700),   # coin return
    "ringback": (700, 1700),  # operator ringback / coin-phone ringback
}

GREEN_ALPHABET = set(_GREEN)


def green_box_bytes(signal: str = "collect", ms: int = 900, amplitude: float = AMPLITUDE) -> bytes:
    """
    Render a green-box operator coin-control tone: `signal` in
    {collect, return, ringback}. Each is a ~900 ms dual tone.
    """
    s = signal.lower()
    if s not in _GREEN:
        raise ValueError(f"unknown green-box signal: {signal!r} (want one of {sorted(_GREEN)})")
    f1, f2 = _GREEN[s]
    return dual_tone_bytes(f1, f2, ms, amplitude)


# --- Fax (T.30 handshake tones) ---------------------------------------------
#
# T.30 defines two tones that identify a fax call at handshake time. They're
# the audio you hear when a fax picks up.
#
#   CNG (calling tone):      1100 Hz, 0.5 s on / 3.0 s off, repeated by the
#                            calling fax until the called end responds.
#   CED (called-station ID): 2100 Hz, 2.6-4.0 s continuous, sent by the
#                            answering fax as an "I'm a fax, go ahead" reply.
#
# Everything after CED (V.21 HDLC preamble, DIS/DCS frames, image data)
# belongs to a real fax stack — see knowledge/fax/README.md.


def cng_bytes(cycles: int = 4, amplitude: float = AMPLITUDE) -> bytes:
    """
    T.30 CNG (fax calling tone). 1100 Hz, 500 ms on / 3000 ms off, per cycle.

    A real calling fax repeats this until the far end answers. `cycles` is
    how many on/off periods to render.
    """
    on = sine_bytes(1100, 500, amplitude)
    off = silence_bytes(3000)
    out = bytearray()
    for _ in range(max(1, cycles)):
        out += on
        out += off
    return bytes(out)


def ced_bytes(ms: int = 3000, amplitude: float = AMPLITUDE) -> bytes:
    """
    T.30 CED (called-station identification). 2100 Hz continuous.

    Standard duration is 2.6-4.0 s. Default 3000 ms sits in the middle.
    """
    return sine_bytes(2100, ms, amplitude)


# --- WAV writer --------------------------------------------------------------


@dataclass(frozen=True)
class RenderedTone:
    path: str
    sample_rate: int
    duration_ms: int
    channels: int = 1
    sample_width_bytes: int = 2


def write_wav(path: str, pcm: bytes) -> RenderedTone:
    """Wrap raw signed-16 LE PCM in a canonical mono 8kHz WAV file."""
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm)
    frames = len(pcm) // 2
    return RenderedTone(
        path=path,
        sample_rate=SAMPLE_RATE,
        duration_ms=int(frames * 1000 / SAMPLE_RATE),
    )
