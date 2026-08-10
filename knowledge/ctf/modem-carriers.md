# MODEM CARRIERS

> The hiss is a handshake. If you can name the stage where it stalls, you can
> name the modem.

A **modem carrier** answers your call with tones instead of a voice — the
sound of two machines negotiating a data link. At a CTF, the carrier is a door
to a terminal: get a modem to complete the handshake and you're at a login,
a BBS, or a device console.

## First 15 seconds

- Pickup, then a steady **answer tone** — a pure ~2100 Hz whistle
  (V.25 ANSam, the modem cousin of the fax CED).
- A beat later, the answer side bursts into **scrambled, static-like hiss**:
  the training/handshake sequence (V.8 / V.21 probes, then the fast-modem
  carrier). It sounds like fast digital rain, not speech, not a single tone.
- Cadence is a rush of noise, not the on/off pulsing of fax CNG.

Carrier tones → recipe #5. See `docs/ctf_playbook.md` triage tree ("Carrier
tones → modem — recipe #5").

## How to probe it

1. `detect_tone(call_sid, targets=["ced","modem"])`. A 2100 Hz answer tone
   classifying as `ced`/`modem` confirms a data answer — but you must
   disambiguate from a **fax**, which also answers near 2100 Hz.
2. Fax vs. modem: a fax follows CED with the slow V.21 300-baud preamble and
   expects a page; a data modem launches straight into wideband training and
   never sends a T.30 DIS. If it trains up into continuous wideband hiss with
   no fax framing, treat it as a carrier (`[[ctf/fax-flags]]` for the fax case).
3. Note **where the handshake stalls** — that's the clue to the far end's
   speed/standard (a stall at the low-speed probe vs. full V.34 training tells
   you what to answer with).
4. Hand off to a **real modem stack** to actually connect: `ATDT<number>`,
   then a terminal (minicom, `cu`, or a softmodem like a Twilio/`<Stream>` +
   SpanDSP bridge). Twilio audio alone can carry the sound but cannot *be* the
   modem — you need a DSP endpoint that negotiates.

## Tools to reach for

- `detect_tone` (targets `ced` / `modem`) — is this a data answer at all?
- `start_recording` + `get_recording_url` — capture the handshake to fingerprint
  the standard offline
- `play_tone_into_call` — you can *originate* a matching answer/originate tone
  for testing, but real data needs a modem DSP, not the tone synth

```python
play_sequence(call_sid, [
    {"action": "wait_for_answer"},
    {"action": "detect_tone", "seconds": 4, "targets": ["ced", "modem"]},
    {"action": "listen", "s": 6},   # record the training burst
])
# best == "modem"/"ced" → hand the call off to a modem stack (ATDT / minicom)
```

## What it means as a puzzle

- **The handshake stage is the clue.** Which standard it trains to (Bell 103,
  V.22bis, V.32, V.34) dates the puzzle and tells you what client to bring.
- **The banner is the flag.** Once connected, the login banner / BBS welcome
  screen / device prompt holds the answer — the phone half just gets you there.
- **A raw tone with no training** may be a red herring or a milliwatt
  (`[[ctf/milliwatt-testlines]]`), not a modem at all.

## See also
- [[modems/README]] — modem standards and dial-up client setup
- [[ctf/fax-flags]] — the other 2100 Hz answer; don't confuse them
- [[war-dialing/README]] — "CARRIER" is exactly this find
- [[bbs/README]] — what's usually on the other end of a carrier
- [[2600hz/README]] — why 2100 Hz answer tones sit away from the SF band

## Sources
- ITU-T V.8 (startup), V.25 (ANSam answer tone), V.34, V.32bis
- Bell 103 / 212A modem specifications (AT&T)
- 2600 Magazine and Phrack (various issues) on dial-up carriers and BBSes
