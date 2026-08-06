"""
Tests for the call event-log infrastructure and the offline-factorable parts
of the remaining action tools (no live Twilio).
"""

from __future__ import annotations

import pytest

from phr34cker5_mcp import server
from phr34cker5_mcp.twilio_bridge import CallState


class _FakeRT:
    def __init__(self, call: CallState):
        self._call = call
        self.auto_hung_up = {}

    def get_call(self, sid):
        if sid != self._call.call_sid:
            raise KeyError(sid)
        return self._call


# --- CallState event log -----------------------------------------------------


def test_add_and_get_events_are_ordered():
    cs = CallState(call_sid="CA1")
    cs.add_event("registered", direction="outbound")
    cs.add_event("ws_connect", stream_sid="MZ1")
    cs.add_event("inject", label="redbox:qqq", queued_ms=1200)
    events = cs.get_events()
    assert [e["kind"] for e in events] == ["registered", "ws_connect", "inject"]
    assert events[0]["direction"] == "outbound"
    assert events[2]["queued_ms"] == 1200
    assert all("t" in e for e in events)


def test_get_events_returns_a_copy():
    cs = CallState(call_sid="CA1")
    cs.add_event("registered")
    snap = cs.get_events()
    cs.add_event("ws_connect")
    assert len(snap) == 1  # snapshot not mutated by later events


# --- call_log assembly -------------------------------------------------------


def test_call_log_timeline_offsets_and_fields():
    cs = CallState(call_sid="CAlog", direction="outbound", to_number="+1555", from_number="+1444")
    cs.add_event("registered", direction="outbound")
    cs.add_event("inject", label="dtmf:123", queued_ms=300)
    log = server._call_log(_FakeRT(cs), "CAlog")
    assert log["call_sid"] == "CAlog"
    assert log["direction"] == "outbound"
    assert log["event_count"] == 2
    assert log["timeline"][0]["kind"] == "registered"
    assert all("offset_ms" in e for e in log["timeline"])
    assert log["auto_hung_up"] is False


def test_call_log_reports_auto_hung_up():
    cs = CallState(call_sid="CAkill")
    cs.add_event("registered")
    rt = _FakeRT(cs)
    rt.auto_hung_up["CAkill"] = 123.0
    assert server._call_log(rt, "CAkill")["auto_hung_up"] is True


def test_call_log_unknown_call_raises():
    cs = CallState(call_sid="CAknown")
    with pytest.raises(KeyError):
        server._call_log(_FakeRT(cs), "CAnope")


# --- inject records an event -------------------------------------------------


def test_inject_records_event(monkeypatch):
    cs = CallState(call_sid="CAinj")
    cs.ws_connected = True
    monkeypatch.setattr(server, "_rt", lambda: _FakeRT(cs))
    server._inject("CAinj", b"\x00\x00" * 800, "sf_2600")  # 1600 bytes = 100ms @8k
    kinds = [e["kind"] for e in cs.get_events()]
    assert "inject" in kinds
    inj = next(e for e in cs.get_events() if e["kind"] == "inject")
    assert inj["label"] == "sf_2600"
    assert inj["queued_ms"] == 100
