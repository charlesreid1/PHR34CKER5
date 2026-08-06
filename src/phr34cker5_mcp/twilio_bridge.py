"""
Twilio bridge — FastAPI app that serves TwiML webhooks and a bidirectional
Media Streams WebSocket. Owns per-call audio state (inbound ring buffer +
outbound send queue).

Twilio Media Streams transport, for reference:
  - Frames are JSON messages over WS. Event types: 'connected', 'start',
    'media', 'mark', 'stop'.
  - Media payload is base64-encoded G.711 μ-law, 8 kHz mono, 20 ms per
    frame (160 audio bytes → 160 μ-law samples → 320 PCM16 bytes).
  - Outbound: send the same shape back and Twilio plays it into the call.

We standardize on signed-16 LE PCM at 8 kHz internally (matches tones.py),
converting at the μ-law boundary via stdlib `audioop`.
"""

from __future__ import annotations

import asyncio
import audioop
import base64
import json
import logging
import os
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Deque

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response

log = logging.getLogger("phr34cker5.twilio_bridge")

MU_LAW_FRAME_SAMPLES = 160   # 20ms at 8kHz
PCM16_FRAME_BYTES = 320      # 160 samples * 2 bytes


# --- per-call state ----------------------------------------------------------


@dataclass
class CallState:
    """Live state for one Twilio call. Owned by the runtime, mutated by the WS."""
    call_sid: str
    stream_sid: str | None = None
    direction: str = "outbound"  # or "inbound"
    to_number: str | None = None
    from_number: str | None = None

    started_at: float = field(default_factory=time.time)
    connected_at: float | None = None
    ended_at: float | None = None

    # Inbound PCM16 audio from the far end. Deque of raw frames (320 bytes each).
    # Bounded so we don't OOM if nobody listens.
    inbound_pcm: Deque[bytes] = field(default_factory=lambda: deque(maxlen=8000))
    inbound_lock: threading.Lock = field(default_factory=threading.Lock)

    # Outbound PCM16 audio to inject into the call. Populated by MCP tools,
    # drained by the WS handler which converts to μ-law and ships frames.
    outbound_pcm: bytearray = field(default_factory=bytearray)
    outbound_lock: threading.Lock = field(default_factory=threading.Lock)

    # Marks the WS has sent, for tools that want to wait until audio actually
    # played out to the callee.
    marks_sent: list[str] = field(default_factory=list)
    marks_acked: list[str] = field(default_factory=list)
    marks_lock: threading.Lock = field(default_factory=threading.Lock)

    ws_connected: bool = False

    # ---- inbound API (called by WS, read by tools) ----

    def push_inbound_pcm(self, pcm: bytes) -> None:
        with self.inbound_lock:
            self.inbound_pcm.append(pcm)

    def drain_inbound_pcm(self, max_ms: int) -> bytes:
        """Pull up to max_ms of inbound audio out of the buffer as PCM16."""
        max_frames = max(1, max_ms // 20)
        out = bytearray()
        with self.inbound_lock:
            for _ in range(max_frames):
                if not self.inbound_pcm:
                    break
                out.extend(self.inbound_pcm.popleft())
        return bytes(out)

    # ---- outbound API (called by tools, drained by WS) ----

    def enqueue_outbound_pcm(self, pcm: bytes) -> None:
        with self.outbound_lock:
            self.outbound_pcm.extend(pcm)

    def take_outbound_frame(self) -> bytes | None:
        """Return one PCM16 frame ready to be μ-law encoded + sent to Twilio."""
        with self.outbound_lock:
            if len(self.outbound_pcm) < PCM16_FRAME_BYTES:
                return None
            frame = bytes(self.outbound_pcm[:PCM16_FRAME_BYTES])
            del self.outbound_pcm[:PCM16_FRAME_BYTES]
            return frame

    def outbound_backlog_ms(self) -> int:
        with self.outbound_lock:
            return (len(self.outbound_pcm) // PCM16_FRAME_BYTES) * 20

    def mark(self, name: str) -> None:
        with self.marks_lock:
            self.marks_sent.append(name)

    def ack_mark(self, name: str) -> None:
        with self.marks_lock:
            self.marks_acked.append(name)

    def mark_acked(self, name: str) -> bool:
        with self.marks_lock:
            return name in self.marks_acked


# --- FastAPI factory ---------------------------------------------------------


def create_app(runtime) -> FastAPI:  # runtime: TwilioRuntime, avoids import cycle
    app = FastAPI(title="phr34cker5-twilio-bridge")

    @app.get("/healthz")
    async def healthz():
        return {"ok": True, "calls": len(runtime.calls)}

    @app.api_route("/twiml/outbound", methods=["GET", "POST"])
    async def twiml_outbound(request: Request):
        """
        Twilio hits this URL when an outbound call we placed is answered.
        We return TwiML that opens a bidirectional Media Stream back to us,
        so tone/audio injection tools can drive the call.
        """
        form = await _form_or_query(request)
        call_sid = form.get("CallSid", "")
        runtime.on_twiml_hit(call_sid, direction="outbound", form=form)
        ws_url = runtime.media_ws_url()
        # <Start><Stream> keeps the call running while streaming media in
        # both directions. <Pause length="3600"/> holds the call open for up
        # to an hour unless we hang up via the REST API.
        twiml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Response>'
            f'<Start><Stream url="{ws_url}" track="inbound_track">'
            f'<Parameter name="call_sid" value="{call_sid}"/>'
            '</Stream></Start>'
            '<Pause length="3600"/>'
            '</Response>'
        )
        return Response(content=twiml, media_type="text/xml")

    @app.api_route("/twiml/inbound", methods=["GET", "POST"])
    async def twiml_inbound(request: Request):
        form = await _form_or_query(request)
        call_sid = form.get("CallSid", "")
        runtime.on_twiml_hit(call_sid, direction="inbound", form=form)
        ws_url = runtime.media_ws_url()
        twiml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Response>'
            f'<Start><Stream url="{ws_url}" track="inbound_track">'
            f'<Parameter name="call_sid" value="{call_sid}"/>'
            '</Stream></Start>'
            '<Pause length="3600"/>'
            '</Response>'
        )
        return Response(content=twiml, media_type="text/xml")

    @app.websocket("/media")
    async def media_ws(ws: WebSocket):
        await ws.accept()
        state: CallState | None = None
        try:
            # A ~20 ms tick paces outbound frame delivery.
            send_task = None
            while True:
                msg_text = await ws.receive_text()
                msg = json.loads(msg_text)
                event = msg.get("event")

                if event == "connected":
                    continue

                if event == "start":
                    start = msg.get("start", {})
                    call_sid = start.get("callSid") or _param(start, "call_sid")
                    stream_sid = start.get("streamSid")
                    state = runtime.get_or_create_call(call_sid)
                    state.stream_sid = stream_sid
                    state.ws_connected = True
                    state.connected_at = time.time()
                    log.info("media WS start call_sid=%s stream=%s", call_sid, stream_sid)
                    # Start the outbound pump.
                    send_task = asyncio.create_task(
                        _outbound_pump(ws, state)
                    )
                    continue

                if event == "media" and state is not None:
                    payload_b64 = msg["media"]["payload"]
                    mulaw = base64.b64decode(payload_b64)
                    pcm16 = audioop.ulaw2lin(mulaw, 2)
                    state.push_inbound_pcm(pcm16)
                    continue

                if event == "mark" and state is not None:
                    name = msg.get("mark", {}).get("name", "")
                    if name:
                        state.ack_mark(name)
                    continue

                if event == "stop" and state is not None:
                    state.ws_connected = False
                    state.ended_at = time.time()
                    log.info("media WS stop call_sid=%s", state.call_sid)
                    break

        except WebSocketDisconnect:
            if state:
                state.ws_connected = False
                state.ended_at = time.time()
        except Exception:
            log.exception("media WS error")
        finally:
            if send_task and not send_task.done():
                send_task.cancel()

    return app


# --- helpers -----------------------------------------------------------------


async def _form_or_query(request: Request) -> dict:
    if request.method == "POST":
        try:
            form = await request.form()
            return {k: v for k, v in form.items()}
        except Exception:
            pass
    return dict(request.query_params)


def _param(start: dict, name: str) -> str | None:
    """Twilio custom <Parameter> shows up in start.customParameters."""
    for p in start.get("customParameters", []) or []:
        if p.get("name") == name:
            return p.get("value")
    return None


async def _outbound_pump(ws: WebSocket, state: CallState) -> None:
    """
    Drain state.outbound_pcm, encode to μ-law, and ship 20ms frames on
    real-time cadence. Idle when the buffer is empty.
    """
    frame_period = 0.02
    next_deadline = time.monotonic() + frame_period
    try:
        while state.ws_connected:
            pcm = state.take_outbound_frame()
            if pcm is None:
                # Nothing to play right now. Sleep briefly and try again.
                await asyncio.sleep(frame_period)
                next_deadline = time.monotonic() + frame_period
                continue
            mulaw = audioop.lin2ulaw(pcm, 2)
            payload_b64 = base64.b64encode(mulaw).decode("ascii")
            await ws.send_text(
                json.dumps(
                    {
                        "event": "media",
                        "streamSid": state.stream_sid,
                        "media": {"payload": payload_b64},
                    }
                )
            )
            # Pace at 50 fps to match Twilio's expected cadence.
            sleep_for = next_deadline - time.monotonic()
            if sleep_for > 0:
                await asyncio.sleep(sleep_for)
            next_deadline += frame_period
    except asyncio.CancelledError:
        raise
    except Exception:
        log.exception("outbound pump error")
