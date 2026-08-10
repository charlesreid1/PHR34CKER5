# IVR MAZES

> Every "press 1 for sales" is a corridor. At a con, some corridors have
> doors that were never announced.

An **IVR maze** is an Interactive Voice Response tree used as a puzzle: a
recorded menu, a DTMF-driven set of branches, and — this is the point —
options the menu never tells you about.

## First 15 seconds

- Pickup is near-instant, no ringback pause. Often a jingle or a canned
  "Thank you for calling."
- A **spoken menu**: "For X press 1, for Y press 2…" delivered at an even,
  narrated cadence. No live-human hesitation.
- Frequently a short **inter-digit timeout** (5–10s of silence) after the
  menu, then it re-reads the menu or dumps you to a default branch.

If you hear a menu, you are in recipe #3 territory. See
`docs/ctf_playbook.md` triage tree ("IVR menu → recipe #3").

## How to probe it

1. Record from the first ring (`start_recording`). Let the full menu play
   at least twice so you have the announced options verbatim.
2. **Enumerate every key**, not just the announced ones: press each of
   `0 1 2 3 4 5 6 7 8 9 * #` from the top level and note where each lands.
   `0` and `*` often reach an operator/back; `#` often submits or skips.
3. Map the tree breadth-first: note which branches loop back, which dead-end,
   which ask for more digits (that smells like `[[ctf/disa-prompts]]`).
4. If the system **reads digits back at you** (echoes an account number,
   confirmation code, or "you entered…"), run `dtmf_decode(call_sid)` to
   recover them — the readback may itself be the flag.
5. Watch the **timeout behavior**: a deliberate no-input drop can route you
   to a hidden branch that keypresses never reach.

## Tools to reach for

- `dial`, `start_recording`, `stop_recording`, `get_recording_url`
- `play_dtmf_into_call` for single presses; `dtmf_decode` for readback audio
- `transcribe` to get the menu wording as text for cipher work
- `play_sequence` to walk a known-good path atomically:

```python
play_sequence(call_sid, [
    {"action": "wait_for_answer"},
    {"action": "listen", "s": 12},        # hear the full menu
    {"action": "dtmf", "digits": "4"},    # take a branch
    {"action": "listen", "s": 6},
    {"action": "dtmf", "digits": "7"},
    {"action": "dtmf_decode", "seconds": 5},  # grab any readback
])
```

## What it means as a puzzle

- **Options are a cipher.** The keypad maps to letters (2=ABC … 9=WXYZ), so a
  sequence of "correct" menu choices can spell a word, or option N stands for
  the Nth letter of the alphabet (4 = D). Log the path, not just the endpoint.
- **The undocumented option is the flag.** The announced menu is decoy; a key
  the recording never mentions opens the real branch.
- **The tree shape is the message** — number of branches at each level, or
  the depth of the correct path, can encode digits.

## See also
- [[ctf/disa-prompts]] — when a menu turns into a PIN prompt
- [[ctf/voicemail-riddles]] — the greeting-as-puzzle cousin
- [[dtmf/README]] — keypad frequencies and keypad-to-letter mapping
- [[war-dialing/README]] — how these numbers get found in the first place

## Sources
- ITU-T Q.23 / Q.24 (DTMF, "Multifrequency push-button signal reception")
- Telecom Digest and comp.dcom.telecom archives on IVR/VRU design (1990s)
- 2600 Magazine (various issues, 1990s) on voice-mail and PBX menu mazes
