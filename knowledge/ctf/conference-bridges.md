# CONFERENCE BRIDGES

> A room you dial into. Sometimes the other callers are the puzzle. Sometimes
> the hold music is.

A **conference bridge** answers by dropping you into a shared audio room:
multiple voices, looping hold music, and often a robotic count of who's
present. At a CTF the flag hides in the mix — in what a looped recording says,
in the structure of the music, or in another caller you're meant to find.

## First 15 seconds

- Pickup, then either **hold music on a loop** or a **hum of multiple voices**
  talking over each other — a texture no single-endpoint puzzle produces.
- A system announcement: **"You are caller number N,"** a join chime, or
  "there are M participants." The count itself may matter.
- The audio does not respond to your DTMF the way a menu would; you've joined
  a room, not a tree.

Multiple voices / hold music → recipe #9. See `docs/ctf_playbook.md` triage
tree ("Multiple voices / hold music → conference bridge — recipe #9").

## How to probe it

1. **Join and listen first, silently.** `start_recording` immediately and let
   the room run — loops repeat on a period, so capture at least two full cycles.
2. Note the **participant count and any join/leave chimes** — a bridge that
   only reveals the flag when N callers are present is a coordination puzzle.
3. Analyze the **hold music offline**: it is a classic steganography carrier.
   Look for Morse in the melody, a spectrogram image, a spoken clue mixed low,
   or DTMF under the loop (`dtmf_decode_wav` on the saved audio).
4. If there are **live voices**, they may be scripted recordings on a loop or
   other players — transcribe to catch a spoken flag or a rendezvous
   instruction.
5. **Announce presence** only when the puzzle calls for it (a challenge/response
   room): inject a WAV or DTMF so the bridge or other players register you.

## Tools to reach for

- `start_recording` + `get_recording_url` — grab the loop for offline analysis
- `transcribe(call_sid, seconds=…)` — pull spoken clues and the participant count
- `dtmf_decode` / `dtmf_decode_wav` — DTMF hidden under the hold music
- `play_wav_into_call` / `play_dtmf_into_call` — announce presence when required

```python
play_sequence(call_sid, [
    {"action": "wait_for_answer"},
    {"action": "listen", "s": 30},          # two loop cycles, stay quiet
    {"action": "dtmf_decode", "seconds": 8}, # tones under the music?
    {"action": "wav", "path": "/tmp/hello.wav"},  # announce, if the puzzle wants it
])
```

## What it means as a puzzle

- **The hold music IS the puzzle** — Morse, a spectrogram picture, backmasking,
  or a low-mixed voice. Save the WAV and look at it, don't just hear it.
- **The caller count is a gate** — the flag drops only with the right number of
  participants, forcing team coordination.
- **A hidden participant** speaks a flag on a schedule; you have to be recording
  when the loop comes around.

## See also
- [[ctf/voicemail-riddles]] — the other "the audio is the payload" genre
- [[ctf/milliwatt-testlines]] — steady-tone steganography, a related trick
- [[ess/README]] — bridging historically lived in the switch
- [[2600hz/README]] — in-band audio as a signaling/side channel

## Sources
- ITU-T H.323 / RFC 3261 (SIP) conferencing models, for how bridges mix audio
- Audio steganography references (spectrogram / LSB / Morse-in-music techniques)
- DEF CON / phreaking-village CTF writeups (various years)
