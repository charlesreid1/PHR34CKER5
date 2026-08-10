# SIMULATED ANAC / CN-A

> The line that tells you your own number. At a con it tells you what the
> *village* thinks your number is — which is the whole point of spoofing.

Two classic telco services, rebuilt as CTF props:

- **ANAC** (Automatic Number Announcement Circuit): dial it, a recording reads
  back the calling line's number. Historically used by installers to identify a
  pair. A CTF ANAC tells you the **ANI the village sees** — your real or
  spoofed caller-ID.
- **CN/A** (Customer Name & Address): the telco bureau that mapped a number to a
  subscriber. A parody **CN/A operator IVR** is a social-engineering target —
  it scores your pretext script (see `[[cna/README]]`).

## First 15 seconds

- **ANAC:** near-instant pickup, then a synthesized voice reading digits:
  "Your number is five-five-five…" — sometimes twice, sometimes with a beep
  first. No menu, no PIN.
- **CN/A parody:** an "operator" greeting or a menu asking for a number to look
  up, or asking *you* to identify yourself first (that's the SE test).

ANAC-like "your number is…" → identify what ANI the CTF sees. See
`docs/ctf_playbook.md` triage tree ("ANAC-like 'your number is …' → identify
what ANI the CTF sees").

## How to probe it

1. **ANAC:** `start_recording`, let the full readback play, then
   `transcribe(call_sid)` to capture the digits exactly. Compare against the
   caller-ID you *intended* to present — the delta tells you whether your
   spoofing/trunk is doing what you think.
2. Re-dial from different origination paths (different Twilio number,
   different `From`) and diff the readback to map what each path presents.
3. **CN/A parody:** treat it as a script test. Present your pretext, note which
   fields it demands (callback number, ticket ID, authorization phrase) and
   which phrasing it accepts vs. rejects. Log the wording that works.
4. Watch for a **flag embedded in the readback** — extra digits after the ANI,
   or a spoken code appended to the "your number is" line.

## Tools to reach for

- `transcribe(call_sid, seconds=…)` — capture the number/name readback as text
- `start_recording` + `get_recording_url` — keep the audio to re-check digits
- `dtmf_decode` — in case the readback is echoed as DTMF, not speech
- `play_wav_into_call` — deliver a pre-recorded pretext to a CN/A parody IVR

```python
play_sequence(call_sid, [
    {"action": "wait_for_answer"},
    {"action": "listen", "s": 10},        # let ANAC read the number
    {"action": "transcribe", "seconds": 10},  # capture the ANI readback
])
```

## What it means as a puzzle

- **ANAC is a mirror.** The challenge is often "make the ANAC read a specific
  number back" — i.e., prove you can control the ANI the village sees. The
  readback is the scoring oracle for a spoofing task.
- **The CN/A operator scores your social engineering** — the flag is the
  listing it releases when your pretext is convincing enough.
- **A code rides along** with the readback (trailing digits / a spoken word).

## See also
- [[cna/README]] — the real Customer Name & Address bureaus and pretexts
- [[glossary/README]] — ANI, ANAC, CN/A, LIDB, CNAM
- [[ctf/voicemail-riddles]] — another spoken-readback capture pattern
- [[blueboxing/README]] — historically, how outsiders faked "internal" ANI

## Sources
- Telco ANAC number lists and installer practice, comp.dcom.telecom archives
- 2600 Magazine and TAP (various issues) — rotating ANAC and CN/A listings
- Mitnick, "The Art of Deception" — CN/A-style pretexting case studies
