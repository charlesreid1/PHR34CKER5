"""
TwilioRuntime — lazy-initialized singleton owning:

  * Twilio REST client (from TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN).
  * FastAPI app + uvicorn server (in a daemon thread) for TwiML + Media Streams.
  * Public URL, either from PHR34CKER5_PUBLIC_URL or an ngrok tunnel we spawn.
  * Per-call CallState registry, keyed by CallSid.

Nothing here happens at import time; boot only when the first Twilio-flavored
MCP tool is invoked. That keeps the offline corpus/tone tools usable even if
Twilio env vars aren't set.
"""

from __future__ import annotations

import logging
import os
import socket
import threading
import time
from typing import Dict

import uvicorn
from twilio.rest import Client as TwilioClient

from phr34cker5_mcp import twilio_bridge
from phr34cker5_mcp.twilio_bridge import CallState

log = logging.getLogger("phr34cker5.runtime")


class MissingConfig(RuntimeError):
    pass


def _require_env(name: str) -> str:
    v = os.environ.get(name)
    if not v:
        raise MissingConfig(
            f"missing env var {name}. See README > Live telephony > Env vars."
        )
    return v


def _free_port(host: str = "127.0.0.1") -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, 0))
        return s.getsockname()[1]


def _bind_host() -> str:
    """
    Interface uvicorn binds to. Default 127.0.0.1 (safe for laptop+ngrok).
    Set PHR34CKER5_BIND_HOST=0.0.0.0 on a VPS so a reverse proxy on the
    same box (or an external one) can reach us.
    """
    return os.environ.get("PHR34CKER5_BIND_HOST", "127.0.0.1")


def _bind_port() -> int | None:
    """
    Pin the local port with PHR34CKER5_BIND_PORT so the reverse proxy has
    a stable upstream. Default: pick a free ephemeral port.
    """
    v = os.environ.get("PHR34CKER5_BIND_PORT")
    return int(v) if v else None


class TwilioRuntime:
    _instance: "TwilioRuntime | None" = None
    _instance_lock = threading.Lock()

    def __init__(self) -> None:
        self._started = False
        self._start_lock = threading.Lock()

        self._client: TwilioClient | None = None
        self._from_number: str | None = None

        self._app = None
        self._server_thread: threading.Thread | None = None
        self._local_port: int | None = None

        self._public_http_url: str | None = None  # https://...
        self._public_ws_url: str | None = None    # wss://.../media
        self._ngrok_tunnel = None

        self.calls: Dict[str, CallState] = {}
        self._calls_lock = threading.Lock()

    # ---- singleton ----

    @classmethod
    def instance(cls) -> "TwilioRuntime":
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    # ---- lazy start ----

    def ensure_started(self) -> None:
        if self._started:
            return
        with self._start_lock:
            if self._started:
                return
            self._init_twilio_client()
            self._start_http_server()
            self._resolve_public_url()
            self._started = True
            log.info(
                "TwilioRuntime ready — public=%s ws=%s from=%s",
                self._public_http_url, self._public_ws_url, self._from_number,
            )

    def _init_twilio_client(self) -> None:
        sid = _require_env("TWILIO_ACCOUNT_SID")
        tok = _require_env("TWILIO_AUTH_TOKEN")
        self._from_number = _require_env("TWILIO_FROM_NUMBER")
        self._client = TwilioClient(sid, tok)

    def _start_http_server(self) -> None:
        self._app = twilio_bridge.create_app(self)
        host = _bind_host()
        port = _bind_port() or _free_port(host if host != "0.0.0.0" else "127.0.0.1")
        self._local_port = port
        cfg = uvicorn.Config(
            self._app,
            host=host,
            port=port,
            log_level="warning",
            loop="asyncio",
            # Trust X-Forwarded-* from the reverse proxy in front of us
            # (Caddy / nginx / Cloudflare). Safe here because we only
            # deploy behind a proxy in the VPS topology.
            proxy_headers=True,
            forwarded_allow_ips="*",
        )
        server = uvicorn.Server(cfg)

        def _run():
            server.run()

        t = threading.Thread(target=_run, name="phr34cker5-uvicorn", daemon=True)
        t.start()
        self._server_thread = t

        # Wait for the socket to actually accept before returning.
        # Use loopback for the health probe even when bound to 0.0.0.0.
        probe_host = "127.0.0.1" if host in ("0.0.0.0", "127.0.0.1") else host
        deadline = time.time() + 10
        while time.time() < deadline:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect((probe_host, port))
                    return
                except OSError:
                    time.sleep(0.05)
        raise RuntimeError(f"uvicorn failed to come up on {host}:{port} within 10s")

    def _resolve_public_url(self) -> None:
        override = os.environ.get("PHR34CKER5_PUBLIC_URL")
        if override:
            base = override.rstrip("/")
            self._public_http_url = base
            self._public_ws_url = _http_to_ws(base) + "/media"
            return

        # No public URL configured — fall back to spawning ngrok. pyngrok is
        # imported lazily so VPS deployments don't need it installed.
        try:
            from pyngrok import conf, ngrok
        except ImportError as e:
            raise MissingConfig(
                "no PHR34CKER5_PUBLIC_URL set and pyngrok is not installed. "
                "Either set PHR34CKER5_PUBLIC_URL=https://your.domain to "
                "point Twilio at your public ingress, or `pip install "
                "pyngrok` to auto-tunnel from a laptop."
            ) from e

        auth = os.environ.get("NGROK_AUTHTOKEN")
        if auth:
            conf.get_default().auth_token = auth

        tunnel = ngrok.connect(self._local_port, "http", bind_tls=True)
        self._ngrok_tunnel = tunnel
        public = tunnel.public_url
        if not public.startswith("https://"):
            public = "https://" + public.split("://", 1)[1]
        self._public_http_url = public
        self._public_ws_url = _http_to_ws(public) + "/media"

    # ---- accessors for the bridge / tools ----

    @property
    def client(self) -> TwilioClient:
        assert self._client is not None, "call ensure_started() first"
        return self._client

    @property
    def from_number(self) -> str:
        assert self._from_number is not None
        return self._from_number

    def public_http_url(self) -> str:
        assert self._public_http_url is not None
        return self._public_http_url

    def media_ws_url(self) -> str:
        assert self._public_ws_url is not None
        return self._public_ws_url

    def outbound_twiml_url(self) -> str:
        return f"{self.public_http_url()}/twiml/outbound"

    def inbound_twiml_url(self) -> str:
        return f"{self.public_http_url()}/twiml/inbound"

    # ---- call registry ----

    def register_call(self, call_sid: str, **kwargs) -> CallState:
        with self._calls_lock:
            cs = self.calls.get(call_sid)
            if cs is None:
                cs = CallState(call_sid=call_sid, **kwargs)
                self.calls[call_sid] = cs
            else:
                for k, v in kwargs.items():
                    setattr(cs, k, v)
            return cs

    def get_or_create_call(self, call_sid: str) -> CallState:
        return self.register_call(call_sid)

    def get_call(self, call_sid: str) -> CallState:
        with self._calls_lock:
            cs = self.calls.get(call_sid)
        if cs is None:
            raise KeyError(f"unknown call_sid: {call_sid}")
        return cs

    def on_twiml_hit(self, call_sid: str, direction: str, form: dict) -> None:
        cs = self.register_call(call_sid, direction=direction)
        cs.to_number = form.get("To") or cs.to_number
        cs.from_number = form.get("From") or cs.from_number


def _http_to_ws(url: str) -> str:
    if url.startswith("https://"):
        return "wss://" + url[len("https://"):]
    if url.startswith("http://"):
        return "ws://" + url[len("http://"):]
    return url
