# VOICEMAIL RIDDLES

> "Leave a message after the tone." The message you should be reading is the
> one already playing.

A **voicemail riddle** is a puzzle where the outgoing **greeting is the
payload**. The box may never take a message at all — the flag is in what the
greeting says, how it's said, or what's hidden under it.

## First 15 seconds

- A **personal or system greeting**, human-sounding, then the classic
  **record beep** (a short ~1 kHz tone) followed by open line / silence.
- Variants that tell you the platform: "…is not available" (generic), a name
  spoken by a synthesized voice, or a mailbox number read back.
- No DTMF menu up front — but the system is *listening* for DTMF the whole
  time. That's your way in.

Voice greeting → recipe #8. See `docs/ctf_playbook.md` triage tree ("Voice
greeting → likely voicemail — recipe #8").

## How to probe it

1. `start_recording`, then let the greeting play **to completion at least
   twice** — riddles often gate a clue on the second half after most callers
   have hung up.
2. Interrupt to reach the system: press `*`, `#`, or `0` during the greeting.
   Historically `*` or `#` jumps to the login/main menu; `0` seeks an operator.
3. If you reach a login, note whether it wants a **mailbox + PIN** — old
   platforms shipped defaults (mailbox number, `0000`, `1234`, last-4). Try
   only con-sanctioned defaults.
4. **Enumerate greeting variants**: some boxes rotate greetings by time of
   day, by caller-ID, or after N calls. Re-dial and diff.
5. Suspect **hidden DTMF under the speech** — a low-level tone burst mixed
   into the audio. Run `dtmf_decode(call_sid)` across the greeting, or
   `dtmf_decode_wav` on the saved recording, to pull digits a human ear misses.

## Tools to reach for

- `transcribe(call_sid, seconds=…)` — turn the greeting into text; spoken
  flags, spelled words, and phonetic-alphabet clues fall out here
- `dtmf_decode` / `dtmf_decode_wav` — recover DTMF buried in the greeting
- `play_dtmf_into_call` — send `*` / `#` / `0` to reach the system
- `start_recording` + `get_recording_url` — keep the raw audio for spectral
  and steganographic analysis later

```python
play_sequence(call_sid, [
    {"action": "wait_for_answer"},
    {"action": "listen", "s": 15},              # full greeting
    {"action": "dtmf_decode", "seconds": 5},    # hidden digits under speech?
    {"action": "dtmf", "digits": "*"},          # try to reach the system
    {"action": "listen", "s": 8},
])
```

## What it means as a puzzle

- **Spoken flag.** The greeting literally recites the answer — often spelled
  with the NATO phonetic alphabet ("Foxtrot, one, one…"). `transcribe` it.
- **DTMF under speech.** A code is mixed low into the audio; only a decoder
  hears it.
- **Steganographic greeting.** The clue is in the audio itself — a spectrogram
  image, backmasking, or a tone pattern — not the words. Save the WAV.
- **Default-PIN gate.** Getting into the mailbox reveals saved messages that
  hold the flag.

## See also
- [[ctf/ivr-mazes]] — the menu-driven sibling
- [[ctf/conference-bridges]] — another "the audio is the puzzle" genre
- [[dtmf/README]] — decoding tones hidden in the greeting
- [[war-dialing/README]] — "VMB" hits are voice-mail boxes

## Sources
- Telecom Digest / comp.dcom.telecom archives on VMB systems (1990s)
- 2600 Magazine (various issues, late 1980s–1990s) on voice-mail hacking
- ITU-T Q.23/Q.24 (DTMF) for the in-band digit detection under audio
