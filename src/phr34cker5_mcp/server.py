"""
PHR34CKER5 MCP server.

Serves a corpus of phreaking lore — zine-flavored markdown organized by topic
(blueboxing, redboxing, CN/A, 2600Hz, BBS, war dialing, ESS, tandem stacking…)
— as MCP resources with tools to list, read, search, and roll a random file.

The corpus lives on disk under the package (installed copy) or under
`knowledge/` at the repo root (dev mode). Skills are shipped separately under
`skills/` and installed into Claude Code / opencode's skill directories.
"""

from __future__ import annotations

import argparse
import os
import random
import re
import tempfile
import uuid
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from phr34cker5_mcp import detect, tones

URI_SCHEME = "phr34cker5"


# --- corpus location ---------------------------------------------------------


def _candidate_roots() -> list[Path]:
    """Locations where the knowledge corpus may live, in preference order."""
    roots: list[Path] = []

    env = os.environ.get("PHR34CKER5_KNOWLEDGE")
    if env:
        roots.append(Path(env).expanduser().resolve())

    # Installed wheel: force-included at phr34cker5_mcp/_knowledge
    try:
        pkg_root = resources.files("phr34cker5_mcp").joinpath("_knowledge")
        as_path = Path(str(pkg_root))
        if as_path.exists():
            roots.append(as_path)
    except (ModuleNotFoundError, FileNotFoundError):
        pass

    # Dev mode: repo-root/knowledge/ (two parents up from this file:
    # src/phr34cker5_mcp/server.py -> repo root)
    here = Path(__file__).resolve()
    roots.append(here.parents[2] / "knowledge")

    return roots


def _resolve_knowledge_root() -> Path:
    for r in _candidate_roots():
        if r.exists() and r.is_dir():
            return r
    # Fall back to the dev-mode path even if missing — errors surface clearly.
    return _candidate_roots()[-1]


KNOWLEDGE_ROOT = _resolve_knowledge_root()


# --- corpus helpers ----------------------------------------------------------


@dataclass(frozen=True)
class LoreFile:
    topic: str
    name: str  # filename without extension
    path: Path

    @property
    def uri(self) -> str:
        return f"{URI_SCHEME}://{self.topic}/{self.name}"


def _iter_lore(root: Path) -> list[LoreFile]:
    if not root.exists():
        return []
    out: list[LoreFile] = []
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root)
        parts = rel.parts
        if len(parts) == 1:
            topic = "_root"
            name = md.stem
        else:
            topic = parts[0]
            name = "/".join(parts[1:])[:-3]  # strip .md
        out.append(LoreFile(topic=topic, name=name, path=md))
    return out


def _find_lore(root: Path, topic: str, name: str) -> LoreFile | None:
    for lf in _iter_lore(root):
        if lf.topic == topic and lf.name == name:
            return lf
    return None


# --- server ------------------------------------------------------------------


mcp = FastMCP(
    name="phr34cker5",
    instructions=(
        "PHR34CKER5 is a phreaking knowledge server — a zine archive from the "
        "golden era of the phone network. Use `list_topics` to see what's in "
        "the stacks, `read_lore` to pull a specific file, `search_lore` to "
        "grep the corpus, and `random_lore` when you want to be surprised. "
        "Each markdown file is also exposed as a resource under the "
        f"`{URI_SCHEME}://` scheme."
    ),
)


@mcp.tool()
def list_topics() -> dict:
    """List all phreaking topics in the corpus and the files under each."""
    root = _resolve_knowledge_root()
    lore = _iter_lore(root)
    topics: dict[str, list[str]] = {}
    for lf in lore:
        topics.setdefault(lf.topic, []).append(lf.name)
    return {
        "root": str(root),
        "topic_count": len(topics),
        "file_count": len(lore),
        "topics": topics,
    }


@mcp.tool()
def read_lore(topic: str, name: str) -> str:
    """
    Read a single lore file.

    Args:
        topic: topic directory name (e.g. 'blueboxing', 'cna', '2600hz').
        name: file name without the .md extension.
    """
    root = _resolve_knowledge_root()
    lf = _find_lore(root, topic, name)
    if lf is None:
        raise ValueError(
            f"no lore file for topic={topic!r} name={name!r} "
            f"(root={root}). Try list_topics()."
        )
    return lf.path.read_text(encoding="utf-8")


@mcp.tool()
def search_lore(query: str, max_results: int = 20) -> dict:
    """
    Search the corpus for a term (case-insensitive substring / regex).

    Returns per-file hit counts and the first matching line from each file.
    """
    root = _resolve_knowledge_root()
    try:
        pattern = re.compile(query, re.IGNORECASE)
    except re.error:
        pattern = re.compile(re.escape(query), re.IGNORECASE)

    hits = []
    for lf in _iter_lore(root):
        try:
            text = lf.path.read_text(encoding="utf-8")
        except OSError:
            continue
        matching_lines = [ln for ln in text.splitlines() if pattern.search(ln)]
        if not matching_lines:
            continue
        hits.append(
            {
                "topic": lf.topic,
                "name": lf.name,
                "uri": lf.uri,
                "match_count": len(matching_lines),
                "first_match": matching_lines[0].strip()[:240],
            }
        )
    hits.sort(key=lambda h: h["match_count"], reverse=True)
    return {"query": query, "hit_count": len(hits), "results": hits[:max_results]}


@mcp.tool()
def random_lore() -> dict:
    """Return one random lore file — text and metadata. For inspiration."""
    root = _resolve_knowledge_root()
    lore = _iter_lore(root)
    if not lore:
        raise ValueError(f"corpus is empty (root={root})")
    lf = random.choice(lore)
    return {
        "topic": lf.topic,
        "name": lf.name,
        "uri": lf.uri,
        "content": lf.path.read_text(encoding="utf-8"),
    }


# --- tone generation ---------------------------------------------------------


def _tone_out_dir() -> Path:
    """Where rendered WAV files land. Overridable via $PHR34CKER5_TONE_DIR."""
    env = os.environ.get("PHR34CKER5_TONE_DIR")
    if env:
        d = Path(env).expanduser().resolve()
    else:
        d = Path(tempfile.gettempdir()) / "phr34cker5-tones"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _tone_path(label: str, path: str | None) -> str:
    if path:
        p = Path(path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        return str(p)
    return str(_tone_out_dir() / f"{label}-{uuid.uuid4().hex[:8]}.wav")


def _render_result(rt: tones.RenderedTone, extra: dict | None = None) -> dict:
    out = {
        "path": rt.path,
        "sample_rate": rt.sample_rate,
        "duration_ms": rt.duration_ms,
        "channels": rt.channels,
        "sample_width_bytes": rt.sample_width_bytes,
    }
    if extra:
        out.update(extra)
    return out


@mcp.tool()
def generate_tone(
    freq_hz: float,
    ms: int = 1000,
    amplitude: float = tones.AMPLITUDE,
    path: str | None = None,
) -> dict:
    """
    Generate a single-frequency sine tone as a WAV file.

    Args:
        freq_hz: frequency in Hz (e.g. 2600 for SF supervision, 440 for A4).
        ms: duration in milliseconds.
        amplitude: 0.0-1.0. Default leaves headroom.
        path: output WAV path. If omitted, writes to a temp file and returns
              the path. Directories are created as needed.
    """
    pcm = tones.sine_bytes(freq_hz, ms, amplitude)
    out = _tone_path(f"tone-{int(freq_hz)}hz", path)
    return _render_result(
        tones.write_wav(out, pcm),
        {"kind": "sine", "freq_hz": freq_hz},
    )


@mcp.tool()
def generate_dual_tone(
    f1_hz: float,
    f2_hz: float,
    ms: int = 1000,
    amplitude: float = tones.AMPLITUDE,
    path: str | None = None,
) -> dict:
    """Sum of two sine tones — the underlying primitive for DTMF, MF, ACTS."""
    pcm = tones.dual_tone_bytes(f1_hz, f2_hz, ms, amplitude)
    out = _tone_path(f"dual-{int(f1_hz)}-{int(f2_hz)}hz", path)
    return _render_result(
        tones.write_wav(out, pcm),
        {"kind": "dual_tone", "f1_hz": f1_hz, "f2_hz": f2_hz},
    )


@mcp.tool()
def generate_dtmf(
    digits: str,
    tone_ms: int = 100,
    gap_ms: int = 80,
    amplitude: float = tones.AMPLITUDE,
    path: str | None = None,
) -> dict:
    """
    Render a DTMF sequence to a WAV file.

    Args:
        digits: any of `0-9 * # A B C D` (case-insensitive). Use `,` / `p`
                / whitespace for a pause of `gap_ms`.
        tone_ms: per-digit tone duration.
        gap_ms: silence between digits (and duration of pause characters).
        amplitude: 0.0-1.0.
        path: output WAV path (defaults to a temp file).

    Example: `generate_dtmf("1-820", ...)` dials 1, 8, 2, 0 with a pause
    between the 1 and the 820.
    """
    pcm = tones.dtmf_bytes(digits, tone_ms, gap_ms, amplitude)
    out = _tone_path("dtmf", path)
    return _render_result(
        tones.write_wav(out, pcm),
        {"kind": "dtmf", "digits": digits},
    )


@mcp.tool()
def generate_mf(
    digits: str,
    tone_ms: int = 68,
    gap_ms: int = 68,
    kp_ms: int = 100,
    amplitude: float = tones.AMPLITUDE,
    path: str | None = None,
) -> dict:
    """
    Render an R1 MF (blue-box) sequence to a WAV file.

    Alphabet: 0-9, K (KP — Key Pulse, start), S (ST — Start, end). Use `,`
    / `p` / whitespace for a gap. A typical seizure-then-route sequence
    from the era is `K<digits>S`, e.g. `K18005551212S`.

    Historical only — see phr34cker5://blueboxing/README for context.
    """
    pcm = tones.mf_bytes(digits, tone_ms, gap_ms, kp_ms, amplitude)
    out = _tone_path("mf", path)
    return _render_result(
        tones.write_wav(out, pcm),
        {"kind": "mf", "digits": digits},
    )


@mcp.tool()
def generate_sf_2600(
    ms: int = 1000,
    amplitude: float = tones.AMPLITUDE,
    path: str | None = None,
) -> dict:
    """The 2600 Hz trunk-idle supervision tone. See phr34cker5://2600hz/README."""
    pcm = tones.sf_2600_bytes(ms, amplitude)
    out = _tone_path("sf-2600", path)
    return _render_result(
        tones.write_wav(out, pcm),
        {"kind": "sf_2600", "freq_hz": 2600},
    )


@mcp.tool()
def generate_fax_cng(
    cycles: int = 4,
    amplitude: float = tones.AMPLITUDE,
    path: str | None = None,
) -> dict:
    """
    Render the T.30 CNG (fax calling) tone: 1100 Hz, 0.5s on / 3s off.

    `cycles` is the number of on/off periods. See phr34cker5://fax/README.
    """
    pcm = tones.cng_bytes(cycles, amplitude)
    out = _tone_path("fax-cng", path)
    return _render_result(
        tones.write_wav(out, pcm),
        {"kind": "fax_cng", "freq_hz": 1100, "cycles": cycles},
    )


@mcp.tool()
def generate_fax_ced(
    ms: int = 3000,
    amplitude: float = tones.AMPLITUDE,
    path: str | None = None,
) -> dict:
    """
    Render the T.30 CED (called-station ID) tone: 2100 Hz continuous.

    Standard duration is 2.6-4.0 s. See phr34cker5://fax/README.
    """
    pcm = tones.ced_bytes(ms, amplitude)
    out = _tone_path("fax-ced", path)
    return _render_result(
        tones.write_wav(out, pcm),
        {"kind": "fax_ced", "freq_hz": 2100},
    )


@mcp.tool()
def generate_red_box(
    coins: str,
    amplitude: float = tones.AMPLITUDE,
    path: str | None = None,
) -> dict:
    """
    Render an ACTS coin-deposit sequence (red box) to a WAV file.

    `coins` uses n=nickel, d=dime, q=quarter (case-insensitive). Non-alpha
    characters insert an inter-coin gap. Example: `qqq` for 75c.

    Historical only — see phr34cker5://redboxing/README for context.
    """
    pcm = tones.red_box_bytes(coins, amplitude)
    out = _tone_path("redbox", path)
    return _render_result(
        tones.write_wav(out, pcm),
        {"kind": "red_box", "coins": coins},
    )


# --- live telephony (Twilio) -------------------------------------------------
#
# Every tool below requires:
#   TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER
# and either NGROK_AUTHTOKEN (to auto-tunnel) or PHR34CKER5_PUBLIC_URL.
#
# First call boots the FastAPI server + ngrok tunnel; subsequent calls reuse.


def _rt():
    """Lazy import + start of the Twilio runtime."""
    from phr34cker5_mcp.runtime import TwilioRuntime

    rt = TwilioRuntime.instance()
    rt.ensure_started()
    return rt


def _call_summary(rt, call_sid: str) -> dict:
    try:
        cs = rt.get_call(call_sid)
    except KeyError:
        cs = None
    api_call = rt.client.calls(call_sid).fetch()
    return {
        "call_sid": call_sid,
        "twilio_status": api_call.status,          # queued/ringing/in-progress/completed/…
        "to": api_call.to,
        "from": api_call.from_,
        "direction": api_call.direction,
        "duration_s": int(api_call.duration or 0),
        "ws_connected": bool(cs and cs.ws_connected),
        "outbound_backlog_ms": cs.outbound_backlog_ms() if cs else 0,
    }


@mcp.tool()
def dial(to: str, from_: str | None = None, record: bool = False) -> dict:
    """
    Place an outbound PSTN call from your Twilio number to `to`.

    Args:
        to: destination number in E.164 (e.g. '+14155551212').
        from_: override caller-ID (must be a Twilio-owned or verified number).
               Defaults to $TWILIO_FROM_NUMBER.
        record: if True, ask Twilio to record the entire call. The recording
                is fetched via get_recording_url() after hangup.

    Returns a dict with the CallSid and current Twilio status. Once Twilio
    connects the call, our TwiML opens a bidirectional Media Stream back to
    the MCP so play_*_into_call() and listen() work.
    """
    rt = _rt()
    kwargs = dict(
        to=to,
        from_=from_ or rt.from_number,
        url=rt.outbound_twiml_url(),
        method="POST",
    )
    if record:
        kwargs["record"] = True
    call = rt.client.calls.create(**kwargs)
    rt.register_call(call.sid, direction="outbound", to_number=to, from_number=kwargs["from_"])
    return {
        "call_sid": call.sid,
        "status": call.status,
        "to": to,
        "from": kwargs["from_"],
        "twiml_url": rt.outbound_twiml_url(),
        "media_ws": rt.media_ws_url(),
    }


@mcp.tool()
def hangup(call_sid: str) -> dict:
    """End a live call via Twilio's REST API."""
    rt = _rt()
    call = rt.client.calls(call_sid).update(status="completed")
    return {"call_sid": call_sid, "status": call.status}


@mcp.tool()
def list_calls() -> dict:
    """List calls this MCP instance has originated or seen this session."""
    rt = _rt()
    with rt._calls_lock:
        sids = list(rt.calls.keys())
    return {
        "count": len(sids),
        "calls": [_call_summary(rt, sid) for sid in sids],
    }


@mcp.tool()
def call_status(call_sid: str) -> dict:
    """Fetch fresh Twilio status for a call, plus our local WS state."""
    rt = _rt()
    return _call_summary(rt, call_sid)


@mcp.tool()
def wait_for_answer(call_sid: str, timeout_s: int = 60) -> dict:
    """
    Block until the far end picks up (Twilio status 'in-progress') and our
    media WebSocket is connected. Returns as soon as both are true, or the
    final status if it times out / fails.
    """
    import time as _t

    rt = _rt()
    deadline = _t.time() + timeout_s
    last = None
    while _t.time() < deadline:
        summary = _call_summary(rt, call_sid)
        last = summary
        if summary["twilio_status"] == "in-progress" and summary["ws_connected"]:
            return summary
        if summary["twilio_status"] in ("completed", "failed", "busy", "no-answer", "canceled"):
            return summary
        _t.sleep(0.5)
    return last or {"call_sid": call_sid, "error": "timeout"}


@mcp.tool()
def wait(seconds: float) -> dict:
    """Sleep — useful for scripting sequences like 'dial, wait 10s, send tones'."""
    import time as _t

    _t.sleep(max(0.0, seconds))
    return {"waited_s": seconds}


# ---- audio injection ----


def _inject(call_sid: str, pcm: bytes, label: str) -> dict:
    rt = _rt()
    cs = rt.get_call(call_sid)
    cs.enqueue_outbound_pcm(pcm)
    return {
        "call_sid": call_sid,
        "queued_ms": (len(pcm) // 2) * 1000 // tones.SAMPLE_RATE,
        "backlog_ms": cs.outbound_backlog_ms(),
        "kind": label,
    }


def _read_wav_pcm(path: str) -> bytes:
    """
    Read a mono 8kHz signed-16 WAV file into raw PCM bytes.

    Enforces the canonical telephony format shared by tones.py, the Twilio
    bridge, and the detectors — so callers never feed a 44.1kHz stereo file
    into an 8kHz mono pipeline and get garbage.
    """
    import wave

    with wave.open(path, "rb") as w:
        if w.getnchannels() != 1 or w.getsampwidth() != 2 or w.getframerate() != tones.SAMPLE_RATE:
            raise ValueError(
                f"{path}: expected mono, 16-bit, {tones.SAMPLE_RATE}Hz "
                f"(got {w.getnchannels()}ch, {w.getsampwidth()*8}-bit, {w.getframerate()}Hz)"
            )
        return w.readframes(w.getnframes())


@mcp.tool()
def play_wav_into_call(call_sid: str, path: str) -> dict:
    """
    Inject an existing WAV file (mono 8kHz signed-16 PCM) into a live call.

    Use this to replay files produced by any of the generate_* tone tools
    without re-synthesizing.
    """
    return _inject(call_sid, _read_wav_pcm(path), f"wav:{path}")


def _wait_for_playout(cs, timeout_s: float = 30.0) -> bool:
    """
    Block until queued outbound audio has been shipped to Twilio (backlog ~0).

    This is what makes a scripted sequence sequential: an inject step isn't
    "done" until the tones have actually gone out, so the next step (e.g.
    listen) doesn't start mid-tone. Returns False if it timed out.
    """
    import time as _t

    deadline = _t.time() + timeout_s
    while _t.time() < deadline:
        if cs.outbound_backlog_ms() <= 0:
            # Small settle so the pump ships the final partial frame.
            _t.sleep(0.05)
            return cs.outbound_backlog_ms() <= 0
        _t.sleep(0.02)
    return False


# PCM builders for the injectable actions in play_sequence. Each maps a step
# dict to raw PCM bytes; keys are the `action` names callers use.
_SEQUENCE_TONE_BUILDERS = {
    "dtmf":   lambda s: tones.dtmf_bytes(s["digits"], s.get("tone_ms", 100), s.get("gap_ms", 80)),
    "mf":     lambda s: tones.mf_bytes(s["digits"], s.get("tone_ms", 68), s.get("gap_ms", 68), s.get("kp_ms", 100)),
    "tone":   lambda s: tones.sine_bytes(s["freq_hz"], s.get("ms", 1000)),
    "2600":   lambda s: tones.sf_2600_bytes(s.get("ms", 1000)),
    "redbox": lambda s: tones.red_box_bytes(s["coins"]),
    "cng":    lambda s: tones.cng_bytes(s.get("cycles", 4)),
    "ced":    lambda s: tones.ced_bytes(s.get("ms", 3000)),
    "wav":    lambda s: _read_wav_pcm(s["path"]),
}


@mcp.tool()
def play_sequence(call_sid: str, steps: list[dict], stop_on_error: bool = True) -> dict:
    """
    Run a scripted sequence of call actions atomically, in order.

    One tool call instead of five, and the single place timing is handled:
    every audio-injection step blocks until its tones have actually played out
    before the next step runs, so "send digits, then listen" listens *after*
    the digits go out — not during.

    Each step is a dict with an `action`:

      inject audio (blocks until played out):
        {"action": "dtmf",   "digits": "1234", "tone_ms": 100, "gap_ms": 80}
        {"action": "mf",     "digits": "K18005551212S"}
        {"action": "tone",   "freq_hz": 440, "ms": 1000}
        {"action": "2600",   "ms": 1000}
        {"action": "redbox", "coins": "qqq"}
        {"action": "cng",    "cycles": 4}      {"action": "ced", "ms": 3000}
        {"action": "wav",    "path": "/path/to.wav"}
      timing / control:
        {"action": "wait", "s": 10}
        {"action": "wait_for_answer", "timeout_s": 60}
        {"action": "hangup"}
      perception (captures inbound audio):
        {"action": "listen",      "s": 5}          -> WAV path
        {"action": "detect_tone", "s": 3, "targets": ["dial-tone","busy"]}
        {"action": "dtmf_decode", "s": 5}          -> digits

    Example — dial handled elsewhere; here we wait for answer, pause, deposit
    75c, and listen:
        play_sequence(sid, [
            {"action": "wait_for_answer"},
            {"action": "wait", "s": 10},
            {"action": "redbox", "coins": "qqq"},
            {"action": "listen", "s": 5},
        ])

    Returns per-step results and an overall `ok`. With stop_on_error (default),
    the sequence halts at the first failing step and reports which one.
    """
    rt = _rt()
    results: list[dict] = []
    ok = True

    for i, step in enumerate(steps):
        action = (step.get("action") or "").lower()
        entry: dict = {"index": i, "action": action}
        try:
            if action in _SEQUENCE_TONE_BUILDERS:
                cs = rt.get_call(call_sid)
                pcm = _SEQUENCE_TONE_BUILDERS[action](step)
                cs.enqueue_outbound_pcm(pcm)
                queued_ms = (len(pcm) // 2) * 1000 // tones.SAMPLE_RATE
                played = _wait_for_playout(cs, timeout_s=max(30.0, queued_ms / 1000 + 10))
                entry.update({"queued_ms": queued_ms, "played_out": played})
                if not played:
                    raise TimeoutError("audio did not finish playing out")

            elif action == "wait":
                secs = float(step.get("s", step.get("seconds", 1.0)))
                wait(secs)
                entry["waited_s"] = secs

            elif action == "wait_for_answer":
                summary = wait_for_answer(call_sid, int(step.get("timeout_s", 60)))
                entry["status"] = summary.get("twilio_status")
                entry["ws_connected"] = summary.get("ws_connected")
                if not (summary.get("twilio_status") == "in-progress" and summary.get("ws_connected")):
                    raise RuntimeError(f"call not answered/connected: {summary.get('twilio_status')}")

            elif action == "hangup":
                entry.update(hangup(call_sid))

            elif action == "listen":
                secs = float(step.get("s", step.get("seconds", 5.0)))
                entry.update(listen(call_sid, seconds=secs))

            elif action == "detect_tone":
                secs = float(step.get("s", step.get("seconds", 3.0)))
                entry.update(detect_tone(call_sid, seconds=secs, targets=step.get("targets")))

            elif action == "dtmf_decode":
                secs = float(step.get("s", step.get("seconds", 5.0)))
                entry.update(dtmf_decode(call_sid, seconds=secs))

            else:
                raise ValueError(f"unknown action: {action!r}")

            entry["ok"] = True
        except Exception as e:  # noqa: BLE001 — record and optionally stop
            entry["ok"] = False
            entry["error"] = f"{e.__class__.__name__}: {e}"
            ok = False
            results.append(entry)
            if stop_on_error:
                break
            continue

        results.append(entry)

    return {
        "call_sid": call_sid,
        "ok": ok,
        "steps_run": len(results),
        "steps_total": len(steps),
        "results": results,
    }


@mcp.tool()
def play_tone_into_call(call_sid: str, freq_hz: float, ms: int = 1000) -> dict:
    """Inject a single sine tone into a live call."""
    return _inject(call_sid, tones.sine_bytes(freq_hz, ms), f"sine:{freq_hz}hz")


@mcp.tool()
def play_dtmf_into_call(
    call_sid: str,
    digits: str,
    tone_ms: int = 100,
    gap_ms: int = 80,
) -> dict:
    """Inject a DTMF sequence into a live call (same alphabet as generate_dtmf)."""
    return _inject(call_sid, tones.dtmf_bytes(digits, tone_ms, gap_ms), f"dtmf:{digits}")


@mcp.tool()
def play_mf_into_call(
    call_sid: str,
    digits: str,
    tone_ms: int = 68,
    gap_ms: int = 68,
    kp_ms: int = 100,
) -> dict:
    """Inject an R1 MF (blue-box) sequence into a live call."""
    return _inject(
        call_sid,
        tones.mf_bytes(digits, tone_ms, gap_ms, kp_ms),
        f"mf:{digits}",
    )


@mcp.tool()
def play_2600_into_call(call_sid: str, ms: int = 1000) -> dict:
    """Inject the 2600 Hz supervision tone into a live call."""
    return _inject(call_sid, tones.sf_2600_bytes(ms), "sf_2600")


@mcp.tool()
def play_fax_cng_into_call(call_sid: str, cycles: int = 4) -> dict:
    """Inject the T.30 fax CNG tone into a live call."""
    return _inject(call_sid, tones.cng_bytes(cycles), f"fax_cng:{cycles}c")


@mcp.tool()
def play_fax_ced_into_call(call_sid: str, ms: int = 3000) -> dict:
    """Inject the T.30 fax CED tone into a live call."""
    return _inject(call_sid, tones.ced_bytes(ms), f"fax_ced:{ms}ms")


@mcp.tool()
def play_red_box_into_call(call_sid: str, coins: str) -> dict:
    """
    Inject ACTS coin-deposit (red box) tones into a live call.

    coins: n/d/q for nickel/dime/quarter. Example: 'qqq' for 75c.
    """
    return _inject(call_sid, tones.red_box_bytes(coins), f"redbox:{coins}")


# ---- listening ----


@mcp.tool()
def listen(call_sid: str, seconds: float = 5.0, save_wav: bool = True) -> dict:
    """
    Pull up to `seconds` of inbound audio from a live call and save it as a WAV.

    Returns the WAV path plus how much audio was actually captured.
    """
    import time as _t

    rt = _rt()
    cs = rt.get_call(call_sid)
    _t.sleep(max(0.0, seconds))  # let audio accumulate in the ring buffer
    pcm = cs.drain_inbound_pcm(max_ms=int(seconds * 1000) + 500)
    ms = (len(pcm) // 2) * 1000 // tones.SAMPLE_RATE
    if not save_wav:
        return {"call_sid": call_sid, "captured_ms": ms, "bytes": len(pcm)}
    out = _tone_path(f"listen-{call_sid[:8]}", None)
    rt_info = tones.write_wav(out, pcm)
    return _render_result(rt_info, {"call_sid": call_sid, "captured_ms": ms})


def _capture_inbound_pcm(call_sid: str, seconds: float) -> tuple[bytes, int]:
    """Sleep `seconds`, then drain that much inbound audio. Returns (pcm, ms)."""
    import time as _t

    rt = _rt()
    cs = rt.get_call(call_sid)
    _t.sleep(max(0.0, seconds))
    pcm = cs.drain_inbound_pcm(max_ms=int(seconds * 1000) + 500)
    ms = (len(pcm) // 2) * 1000 // tones.SAMPLE_RATE
    return pcm, ms


# ---- perception (detect / decode / transcribe) ----


@mcp.tool()
def detect_tone(
    call_sid: str,
    seconds: float = 3.0,
    targets: list[str] | None = None,
) -> dict:
    """
    Listen to a live call and classify what tone(s) are on the line.

    Goertzel power at named telephony frequencies plus a cadence estimate, so
    you can tell busy (~1s period) from reorder (~0.5s), or spot dial tone,
    ringback, 2600 Hz, fax CNG/CED, a modem answer tone, or a milliwatt test
    tone. Use it to gate a sequence: "wait until dial tone, then send digits."

    Args:
        call_sid: the live call to listen on.
        seconds: how long to sample.
        targets: subset of {dial-tone, busy, reorder, ringback, 2600, cng,
                 ced, modem, milliwatt} to score against. Default: the common
                 set (all but reorder, which overlaps busy).

    Returns dominant frequencies, the cadence estimate, per-target matches,
    and `best` — the highest-scoring present target (or null if the line is
    silent / unrecognized).
    """
    pcm, ms = _capture_inbound_pcm(call_sid, seconds)
    result = detect.detect_tones(pcm, targets)
    result["call_sid"] = call_sid
    return result


@mcp.tool()
def dtmf_decode(call_sid: str, seconds: float = 5.0) -> dict:
    """
    Decode DTMF digits the far end is sending on a live call.

    Frames the inbound audio, classifies each frame with twist and
    relative-power validation, and collapses runs into a digit string.
    Critical for IVR / DISA puzzles where the far end plays digits back.

    Returns {"digits": "...", "detail": [{digit, start_ms, duration_ms}, ...]}.
    """
    pcm, ms = _capture_inbound_pcm(call_sid, seconds)
    result = detect.decode_dtmf(pcm)
    result["call_sid"] = call_sid
    result["captured_ms"] = ms
    return result


@mcp.tool()
def dtmf_decode_wav(path: str) -> dict:
    """
    Decode DTMF digits from a WAV file (mono 8kHz signed-16).

    Same decoder as dtmf_decode(), but on a file — e.g. a WAV produced by
    listen() earlier, or one of the generate_dtmf() outputs.
    """
    pcm = _read_wav_pcm(path)
    result = detect.decode_dtmf(pcm)
    result["path"] = path
    return result


@mcp.tool()
def transcribe(call_sid: str, seconds: float = 10.0) -> dict:
    """
    Speech-to-text on a live call's inbound audio.

    Captures `seconds` of audio and transcribes it. Uses Twilio's transcription
    if the optional dependency for a local recognizer isn't available; either
    way you get text back for "listen to the IVR menu and tell me the options."

    Currently this captures to a WAV and hands off to Twilio's recording +
    transcription pipeline. Returns the captured WAV path, and the transcript
    once available (transcription is async on Twilio's side — poll
    get_recording_url / the returned transcription_sid if pending).
    """
    pcm, ms = _capture_inbound_pcm(call_sid, seconds)
    out = _tone_path(f"transcribe-{call_sid[:8]}", None)
    tones.write_wav(out, pcm)

    rt = _rt()
    # Kick off a Twilio recording+transcription on the live call so we get a
    # server-side transcript. The captured WAV is the local fallback / evidence.
    transcription_sid = None
    status = "captured"
    try:
        rec = rt.client.calls(call_sid).recordings.create()
        transcription_sid = rec.sid
        status = "recording_started"
    except Exception as e:  # noqa: BLE001 — surface the reason, don't crash
        status = f"local_only: {e.__class__.__name__}"

    return {
        "call_sid": call_sid,
        "captured_ms": ms,
        "wav_path": out,
        "status": status,
        "recording_sid": transcription_sid,
        "note": (
            "Twilio transcription is asynchronous; fetch the recording via "
            "get_recording_url() and run STT, or enable Voice Intelligence on "
            "the account for automatic transcripts."
        ),
    }


# ---- Twilio-native recording ----


@mcp.tool()
def start_recording(call_sid: str) -> dict:
    """Ask Twilio to record the whole call. Uses their infra, not our WS."""
    rt = _rt()
    rec = rt.client.calls(call_sid).recordings.create()
    return {"call_sid": call_sid, "recording_sid": rec.sid, "status": rec.status}


@mcp.tool()
def stop_recording(call_sid: str, recording_sid: str) -> dict:
    rt = _rt()
    rec = rt.client.calls(call_sid).recordings(recording_sid).update(status="stopped")
    return {"call_sid": call_sid, "recording_sid": rec.sid, "status": rec.status}


@mcp.tool()
def get_recording_url(recording_sid: str) -> dict:
    """Return the media URL for a Twilio recording (append .wav or .mp3)."""
    rt = _rt()
    rec = rt.client.recordings(recording_sid).fetch()
    media = f"https://api.twilio.com{rec.uri.replace('.json', '.wav')}"
    return {
        "recording_sid": recording_sid,
        "status": rec.status,
        "duration_s": int(rec.duration or 0),
        "media_url_wav": media,
        "media_url_mp3": media.replace(".wav", ".mp3"),
    }


@mcp.resource(f"{URI_SCHEME}://index")
def _index() -> str:
    """Human-readable index of the corpus."""
    root = _resolve_knowledge_root()
    lore = _iter_lore(root)
    lines = [f"# PHR34CKER5 corpus", f"root: {root}", ""]
    by_topic: dict[str, list[LoreFile]] = {}
    for lf in lore:
        by_topic.setdefault(lf.topic, []).append(lf)
    for topic in sorted(by_topic):
        lines.append(f"## {topic}")
        for lf in by_topic[topic]:
            lines.append(f"- [{lf.name}]({lf.uri})")
        lines.append("")
    return "\n".join(lines)


@mcp.resource(URI_SCHEME + "://{topic}/{name}")
def _lore_resource(topic: str, name: str) -> str:
    """Serve a lore file as an MCP resource."""
    root = _resolve_knowledge_root()
    lf = _find_lore(root, topic, name)
    if lf is None:
        raise ValueError(f"no lore file: {topic}/{name}")
    return lf.path.read_text(encoding="utf-8")


# --- entrypoint --------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(prog="phr34cker5-mcp")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="MCP transport (default: stdio, which is what Claude Desktop / opencode use).",
    )
    parser.add_argument(
        "--knowledge",
        help="Override corpus root (also readable from $PHR34CKER5_KNOWLEDGE).",
    )
    args = parser.parse_args()

    if args.knowledge:
        os.environ["PHR34CKER5_KNOWLEDGE"] = args.knowledge
        global KNOWLEDGE_ROOT
        KNOWLEDGE_ROOT = _resolve_knowledge_root()

    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
