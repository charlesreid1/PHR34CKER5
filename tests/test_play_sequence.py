"""
Tests for play_sequence orchestration.

We don't touch Twilio: a fake runtime hands out a real CallState, and a
background thread plays the "outbound pump" role by draining the outbound
buffer so _wait_for_playout observes the backlog reach zero.
"""

from __future__ import annotations

import threading
import time

import pytest

from phr34cker5_mcp import server
from phr34cker5_mcp.twilio_bridge import CallState


class _FakeRuntime:
    def __init__(self, call: CallState):
        self._call = call

    def get_call(self, sid):
        return self._call


@pytest.fixture
def piped_call(monkeypatch):
    """A connected CallState with a background pump draining outbound audio."""
    cs = CallState(call_sid="CAtest")
    cs.ws_connected = True

    monkeypatch.setattr(server, "_rt", lambda: _FakeRuntime(cs))

    stop = threading.Event()

    def pump():
        while not stop.is_set():
            if cs.take_outbound_frame() is None:
                time.sleep(0.001)

    t = threading.Thread(target=pump, daemon=True)
    t.start()
    yield cs
    stop.set()
    t.join(timeout=1)


def test_sequence_runs_all_steps(piped_call):
    r = server.play_sequence(
        "CAtest",
        [
            {"action": "dtmf", "digits": "123", "tone_ms": 50, "gap_ms": 40},
            {"action": "wait", "s": 0.05},
            {"action": "2600", "ms": 150},
        ],
    )
    assert r["ok"] is True
    assert r["steps_run"] == 3 == r["steps_total"]
    assert all(step["ok"] for step in r["results"])


def test_inject_step_reports_playout(piped_call):
    r = server.play_sequence("CAtest", [{"action": "redbox", "coins": "q"}])
    step = r["results"][0]
    assert step["action"] == "redbox"
    assert step["played_out"] is True
    assert step["queued_ms"] > 0


def test_unknown_action_stops_by_default(piped_call):
    r = server.play_sequence(
        "CAtest",
        [{"action": "wait", "s": 0.01}, {"action": "bogus"}, {"action": "wait", "s": 0.01}],
    )
    assert r["ok"] is False
    assert r["steps_run"] == 2  # stopped at the bad step
    assert "unknown action" in r["results"][-1]["error"]


def test_continue_on_error(piped_call):
    r = server.play_sequence(
        "CAtest",
        [{"action": "bogus"}, {"action": "wait", "s": 0.01}],
        stop_on_error=False,
    )
    assert r["ok"] is False
    assert r["steps_run"] == 2  # ran past the bad step
    assert r["results"][0]["ok"] is False
    assert r["results"][1]["ok"] is True


def test_wav_step_injects_file(piped_call, tmp_path):
    from phr34cker5_mcp import tones

    p = tmp_path / "seq.wav"
    tones.write_wav(str(p), tones.dtmf_bytes("9", tone_ms=60, gap_ms=40))
    r = server.play_sequence("CAtest", [{"action": "wav", "path": str(p)}])
    assert r["ok"] is True
    assert r["results"][0]["queued_ms"] > 0
