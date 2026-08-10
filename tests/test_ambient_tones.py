"""
Ambient / call-progress generators round-trip through the detector, and the
MAX_CALL_MINUTES guardrail helpers behave.
"""

from __future__ import annotations

import pytest

from phr34cker5_mcp import detect, runtime, tones


# --- generator -> detector round-trips --------------------------------------


def _best(pcm, targets):
    return detect.detect_tones(pcm, targets)["best"]


def test_busy_roundtrips():
    assert _best(tones.busy_bytes(4), ["busy", "reorder", "dial-tone"]) == "busy"


def test_reorder_roundtrips():
    assert _best(tones.reorder_bytes(8), ["busy", "reorder"]) == "reorder"


def test_ringback_roundtrips():
    assert _best(tones.ringback_bytes(2), ["ringback", "busy", "dial-tone"]) == "ringback"


def test_milliwatt_roundtrips():
    assert _best(tones.milliwatt_bytes(1000), ["milliwatt", "2600", "ced"]) == "milliwatt"


def test_modem_carrier_roundtrips():
    # First segment is the 2100 Hz answer tone → classifies as modem/ced.
    assert _best(tones.modem_carrier_bytes("v22"), ["modem", "milliwatt", "dial-tone"]) == "modem"


def test_modem_carrier_bad_rate_raises():
    with pytest.raises(ValueError, match="unknown modem rate"):
        tones.modem_carrier_bytes("v99")


def test_green_box_signals():
    for sig, freqs in [("collect", (700, 1100)), ("return", (1100, 1700)), ("ringback", (700, 1700))]:
        pcm = tones.green_box_bytes(sig)
        samples = detect.pcm16_to_samples(pcm)
        for f in freqs:
            assert detect.energy_ratio(samples, f) > 0.15, (sig, f)


def test_green_box_bad_signal_raises():
    with pytest.raises(ValueError, match="unknown green-box signal"):
        tones.green_box_bytes("teal")


def test_busy_and_reorder_share_frequency_but_differ_by_cadence():
    # Both are 480+620; only the cadence distinguishes them.
    busy = tones.busy_bytes(3)
    reorder = tones.reorder_bytes(6)
    assert _best(busy, ["busy", "reorder"]) == "busy"
    assert _best(reorder, ["busy", "reorder"]) == "reorder"


# --- MAX_CALL_MINUTES env parsing -------------------------------------------


@pytest.mark.parametrize("value,expected", [
    (None, None),
    ("10", 600.0),
    ("0.5", 30.0),
    ("0", None),
    ("-5", None),
    ("junk", None),
])
def test_max_call_seconds_parsing(monkeypatch, value, expected):
    if value is None:
        monkeypatch.delenv("MAX_CALL_MINUTES", raising=False)
    else:
        monkeypatch.setenv("MAX_CALL_MINUTES", value)
    assert runtime._max_call_seconds() == expected


# --- overdue_call_sids pure helper ------------------------------------------


class _FakeCS:
    def __init__(self, started_at=None, connected_at=None, ended_at=None):
        self.started_at = started_at
        self.connected_at = connected_at
        self.ended_at = ended_at


def test_overdue_uses_connected_at_when_present():
    now = 1000.0
    calls = {"c": _FakeCS(started_at=0, connected_at=100)}  # 900s since connect
    assert runtime.overdue_call_sids(calls, 600, now) == ["c"]


def test_overdue_falls_back_to_started_at():
    now = 1000.0
    calls = {"c": _FakeCS(started_at=200)}  # 800s, no WS connect
    assert runtime.overdue_call_sids(calls, 600, now) == ["c"]


def test_fresh_call_not_overdue():
    now = 1000.0
    calls = {"c": _FakeCS(started_at=900, connected_at=950)}
    assert runtime.overdue_call_sids(calls, 600, now) == []


def test_ended_call_skipped():
    now = 1000.0
    calls = {"c": _FakeCS(started_at=0, connected_at=0, ended_at=5)}
    assert runtime.overdue_call_sids(calls, 600, now) == []


def test_unregistered_start_skipped():
    now = 1000.0
    calls = {"c": _FakeCS()}  # no timestamps at all
    assert runtime.overdue_call_sids(calls, 600, now) == []
