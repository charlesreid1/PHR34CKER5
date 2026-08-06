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
