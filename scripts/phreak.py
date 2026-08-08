#!/usr/bin/env python3
"""Thin wrapper around Twilio for the PhreakMe CTF.

Two subcommands:

  dial   TWIML   — place a call with the given TwiML body, poll to completion,
                   download the recording, transcribe it. TwiML may reference
                   %(WAV_BASE)s as the base URL of our Twilio Serverless env.
  submit ID FLAG — submit FLAG to CTFd challenge ID.

Config:
  ~/.twilio_api_key         → TWILIO_SID, TWILIO_CLIENT_SECRET
  ./.env                    → PHREAKME_USER, PHREAKME_PASS, TWILIO_FROM_NUMBER,
                              TWILIO_ACCOUNT_SID, PHREAKME_TARGET
  ~/.openrouter_api_key     → OPENROUTER_API_KEY (for transcription)

Every call writes:
  .recordings/<label>_<recording_sid>.mp3       — the audio
  .recordings/<label>_<recording_sid>.txt       — the transcript
  .recordings/<label>_<recording_sid>.json      — call metadata

Usage:
  scripts/phreak.py dial redbox_514 \\
    '<Response><Pause length="6"/><Play digits="2"/>' \\
    '<Pause length="5"/><Play digits="5145551337"/>' \\
    '<Pause length="8"/><Play>%(WAV_BASE)s/redbox_q.wav</Play>' \\
    '<Pause length="60"/></Response>'

  scripts/phreak.py submit 74 "Radio Shack"
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import pathlib
import re
import sys
import time
from typing import Any

import requests
from requests.auth import HTTPBasicAuth

ROOT = pathlib.Path(__file__).parent.parent
RECS = ROOT / ".recordings"
TONES = ROOT / ".tones"
RECS.mkdir(exist_ok=True)
TONES.mkdir(exist_ok=True)

WAV_BASE = "https://phreakme-tones-5443-live.twil.io"


def _need(name: str) -> str:
    v = os.environ.get(name, "").strip()
    if not v:
        sys.exit(f"missing env: {name}")
    return v


def twilio_auth() -> tuple[HTTPBasicAuth, str, str, str]:
    sid = _need("TWILIO_SID")
    sec = _need("TWILIO_CLIENT_SECRET")
    acct = _need("TWILIO_ACCOUNT_SID")
    frm = _need("TWILIO_FROM_NUMBER")
    return HTTPBasicAuth(sid, sec), sid, acct, frm


def dial(label: str, twiml_parts: list[str], target: str | None = None,
         record_channels: str = "dual") -> dict[str, Any]:
    """Place a call with the given TwiML fragments (joined), record it, download & transcribe."""
    auth, _, acct, frm = twilio_auth()
    target = target or os.environ.get("PHREAKME_TARGET", "+12195002600")
    twiml = "".join(twiml_parts) % {"WAV_BASE": WAV_BASE}
    # Sanity: must have a single <Response> wrapper
    if not twiml.startswith("<Response>") or not twiml.endswith("</Response>"):
        sys.exit(f"bad TwiML: must be wrapped in <Response>…</Response>\n  got: {twiml!r}")

    print(f"[dial] target={target} label={label} twiml_len={len(twiml)}", flush=True)
    # Place the call
    r = requests.post(
        f"https://api.twilio.com/2010-04-01/Accounts/{acct}/Calls.json",
        auth=auth,
        data={"To": target, "From": frm, "Twiml": twiml,
              "Record": "true", "RecordingChannels": record_channels},
        timeout=30,
    )
    r.raise_for_status()
    call_sid = r.json()["sid"]
    print(f"[dial] call_sid={call_sid}", flush=True)

    # Poll
    for i in range(80):
        time.sleep(3)
        c = requests.get(
            f"https://api.twilio.com/2010-04-01/Accounts/{acct}/Calls/{call_sid}.json",
            auth=auth, timeout=30,
        ).json()
        status = c["status"]
        print(f"  t={i*3}s status={status} dur={c.get('duration')}", flush=True)
        if status in ("completed", "failed", "busy", "no-answer", "canceled"):
            break

    # Grab recordings — wait a beat for finalization, retry a few times if empty
    recs: list[dict[str, Any]] = []
    for attempt in range(6):
        time.sleep(3)
        recs = requests.get(
            f"https://api.twilio.com/2010-04-01/Accounts/{acct}/Calls/{call_sid}/Recordings.json",
            auth=auth, timeout=30,
        ).json().get("recordings", [])
        # Skip broken (-1s) recordings
        good = [r for r in recs if int(r.get("duration", "-1")) > 0
                and r.get("status") == "completed"]
        if good:
            recs = good
            break
        print(f"  [wait] recordings not ready yet (attempt {attempt+1}/6): {recs}", flush=True)

    if not recs:
        print("[dial] NO USABLE RECORDINGS — the call itself completed OK but Twilio didn't save audio", flush=True)
        return {"call_sid": call_sid, "status": "no_recording"}

    rec = max(recs, key=lambda r: int(r["duration"]))
    print(f"[dial] using recording {rec['sid']} dur={rec['duration']}s ch={rec['channels']}", flush=True)
    url = f"https://api.twilio.com/2010-04-01/Accounts/{acct}/Recordings/{rec['sid']}.mp3"
    mp3_path = RECS / f"{label}_{rec['sid']}.mp3"
    mp3_path.write_bytes(requests.get(url, auth=auth, timeout=60).content)
    print(f"[dial] saved {mp3_path} ({mp3_path.stat().st_size} bytes)", flush=True)

    # Transcribe
    text = transcribe(mp3_path)
    txt_path = mp3_path.with_suffix(".txt")
    txt_path.write_text(text)
    print(f"[dial] transcript:\n---\n{text}\n---", flush=True)

    # Save metadata
    meta = {
        "call_sid": call_sid, "recording_sid": rec["sid"],
        "duration": rec["duration"], "channels": rec["channels"],
        "twiml": twiml, "target": target,
    }
    mp3_path.with_suffix(".json").write_text(json.dumps(meta, indent=2))
    return {"call_sid": call_sid, "recording": str(mp3_path),
            "transcript": str(txt_path), "text": text}


def transcribe(path: pathlib.Path) -> str:
    """Send an MP3 to Gemini via OpenRouter for verbatim transcription."""
    key = _need("OPENROUTER_API_KEY")
    b64 = base64.b64encode(path.read_bytes()).decode()
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": "google/gemini-2.5-flash",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "input_audio", "input_audio": {"data": b64, "format": "mp3"}},
                    {"type": "text", "text": (
                        "Transcribe every word verbatim, in order. This is a phone-quality "
                        "recording. Note tones, DTMF beeps, ringing, coin-deposit prompts, "
                        "busy signals, silences. If a flag or code is announced, quote it "
                        "exactly. If a menu is presented, list every option with the digit "
                        "to press. Be precise about spelling."
                    )},
                ],
            }],
        },
        timeout=240,
    )
    d = r.json()
    if "choices" not in d:
        return f"[transcription error] {json.dumps(d)[:500]}"
    return d["choices"][0]["message"]["content"]


# ---- CTFd submission ------------------------------------------------------

def _ctfd_session() -> tuple[requests.Session, str]:
    s = requests.Session()
    r = s.get("https://phreakme.com/login", timeout=30)
    m = re.search(r'name="nonce"[^>]*value="([^"]+)"', r.text)
    if not m:
        sys.exit("could not find login nonce")
    s.post("https://phreakme.com/login",
           data={"name": _need("PHREAKME_USER"),
                 "password": _need("PHREAKME_PASS"),
                 "nonce": m.group(1), "_submit": "Submit"},
           timeout=30)
    m = re.search(r"'csrfNonce':\s*\"([^\"]+)\"",
                  s.get("https://phreakme.com/challenges", timeout=30).text)
    if not m:
        sys.exit("could not find CSRF nonce (login failed?)")
    return s, m.group(1)


def submit(challenge_id: int, flag: str) -> dict[str, Any]:
    s, csrf = _ctfd_session()
    while True:
        r = s.post("https://phreakme.com/api/v1/challenges/attempt",
                   headers={"CSRF-Token": csrf, "Content-Type": "application/json"},
                   json={"challenge_id": challenge_id, "submission": flag}, timeout=30)
        d = r.json().get("data", {})
        status = d.get("status", "?")
        if status == "ratelimited":
            print(f"[submit] rate limited on {flag!r} → waiting 15s", flush=True)
            time.sleep(15); continue
        print(f"[submit] challenge {challenge_id} flag {flag!r} → {status}: {d.get('message','')}", flush=True)
        return d


def challenges() -> list[dict[str, Any]]:
    s, _ = _ctfd_session()
    return s.get("https://phreakme.com/api/v1/challenges", timeout=30).json()["data"]


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("dial", help="Place a call with TwiML, record, transcribe")
    d.add_argument("label", help="short filename tag (e.g. redbox_514)")
    d.add_argument("twiml", nargs="+", help="TwiML fragments; %(WAV_BASE)s is substituted")
    d.add_argument("--target", default=None)
    d.add_argument("--channels", default="dual", choices=["dual", "mono"])

    s_ = sub.add_parser("submit", help="Submit a flag to CTFd")
    s_.add_argument("challenge_id", type=int)
    s_.add_argument("flag")

    sub.add_parser("list", help="List CTFd challenges")

    t = sub.add_parser("transcribe", help="(Re-)transcribe an existing recording")
    t.add_argument("path")

    args = p.parse_args()
    if args.cmd == "dial":
        result = dial(args.label, args.twiml, target=args.target,
                      record_channels=args.channels)
        print("\n[result]", json.dumps(result, indent=2)[:400])
    elif args.cmd == "submit":
        submit(args.challenge_id, args.flag)
    elif args.cmd == "list":
        for c in challenges():
            print(f"  #{c['id']:>3} [{c['category']:>10}] {c['name']!r:<40} {c['value']} pts"
                  f"  solved={c['solved_by_me']}")
    elif args.cmd == "transcribe":
        text = transcribe(pathlib.Path(args.path))
        print(text)


if __name__ == "__main__":
    main()
