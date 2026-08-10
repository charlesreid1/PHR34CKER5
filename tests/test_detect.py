"""
Tests for the perception layer: Goertzel tone detection and DTMF decode.

Everything here is pure-DSP (no Twilio, no network) — we synthesize with
tones.py and assert that detect.py recovers what we put in.
"""

from __future__ import annotations

from phr34cker5_mcp import detect, tones


def _cadence_tone(f1, f2, on_ms, off_ms, cycles):
    out = bytearray()
    for _ in range(cycles):
        out += tones.dual_tone_bytes(f1, f2, on_ms)
        out += tones.silence_bytes(off_ms)
    return bytes(out)


# --- DTMF decode -------------------------------------------------------------


def test_dtmf_roundtrip_full_alphabet():
    pcm = tones.dtmf_bytes("1234567890*#ABCD", tone_ms=80, gap_ms=60)
    assert detect.decode_dtmf(pcm)["digits"] == "1234567890*#ABCD"


def test_dtmf_roundtrip_phone_number():
    pcm = tones.dtmf_bytes("18005551212", tone_ms=100, gap_ms=80)
    assert detect.decode_dtmf(pcm)["digits"] == "18005551212"


def test_dtmf_repeated_digits_are_separated_by_gaps():
    pcm = tones.dtmf_bytes("111", tone_ms=90, gap_ms=70)
    assert detect.decode_dtmf(pcm)["digits"] == "111"


def test_dtmf_detail_has_timing():
    pcm = tones.dtmf_bytes("55", tone_ms=100, gap_ms=80)
    detail = detect.decode_dtmf(pcm)["detail"]
    assert len(detail) == 2
    assert all(d["digit"] == "5" for d in detail)
    assert detail[1]["start_ms"] > detail[0]["start_ms"]


def test_dtmf_silence_decodes_to_nothing():
    assert detect.decode_dtmf(tones.silence_bytes(500))["digits"] == ""


def test_dtmf_short_blip_is_rejected():
    # A single 10 ms tone is below the 40 ms min-digit floor.
    pcm = tones.dtmf_bytes("7", tone_ms=10, gap_ms=200)
    assert detect.decode_dtmf(pcm)["digits"] == ""


def test_pure_sine_is_not_a_dtmf_digit():
    # One 697 Hz leg alone must not classify as a digit (needs both legs).
    assert detect.decode_dtmf(tones.sine_bytes(697, 300))["digits"] == ""


# --- continuous tone detection ----------------------------------------------


def test_detect_2600():
    d = detect.detect_tones(tones.sf_2600_bytes(500), ["2600", "ced", "dial-tone"])
    assert d["best"] == "2600"


def test_detect_ced_continuous():
    d = detect.detect_tones(tones.ced_bytes(600), ["ced", "2600", "cng"])
    assert d["best"] == "ced"
    assert d["cadence"]["continuous"] is True


def test_detect_dial_tone_dual():
    d = detect.detect_tones(tones.dual_tone_bytes(350, 440, 600), ["dial-tone", "busy", "ringback"])
    assert d["best"] == "dial-tone"


def test_detect_milliwatt():
    d = detect.detect_tones(tones.sine_bytes(1004, 500), ["milliwatt", "2600", "ced"])
    assert d["best"] == "milliwatt"


def test_silence_detects_nothing():
    d = detect.detect_tones(tones.silence_bytes(400), ["2600", "dial-tone", "busy"])
    assert d["best"] is None


def test_offtarget_tone_not_matched():
    # 440 Hz alone (A4) shouldn't match dial-tone (which needs 350 AND 440).
    d = detect.detect_tones(tones.sine_bytes(440, 400), ["dial-tone", "busy"])
    assert d["best"] is None


# --- cadence separates same-frequency tones ---------------------------------


def test_busy_vs_reorder_by_cadence():
    busy = _cadence_tone(480, 620, 500, 500, 3)
    reorder = _cadence_tone(480, 620, 250, 250, 6)
    assert detect.detect_tones(busy, ["busy", "reorder"])["best"] == "busy"
    assert detect.detect_tones(reorder, ["busy", "reorder"])["best"] == "reorder"


# --- helpers -----------------------------------------------------------------


def test_pcm16_to_samples_drops_odd_trailing_byte():
    a = detect.pcm16_to_samples(b"\x01\x02\x03")
    assert len(a) == 1  # 3 bytes -> one 16-bit sample, trailing byte dropped


def test_energy_ratio_single_tone_near_half():
    samples = detect.pcm16_to_samples(tones.sine_bytes(1000, 300))
    assert detect.energy_ratio(samples, 1000) > 0.4
