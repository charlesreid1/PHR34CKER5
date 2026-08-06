# CTF PLAYBOOK

What to do when handed an unknown number at a phreaking CTF. Optimized
for the first 60 seconds of a puzzle. Complements
[`twilio_setup.md`](twilio_setup.md) (which is *pre-con* setup) — this
one is *at the con, in the moment.*

> **Status: stub.** Short on purpose; it fills in as we play. The
> triage tree below is the load-bearing part — keep it accurate.

## Before you dial

- Confirm it's PSTN, not SIP-only (see [`twilio_setup.md`](twilio_setup.md)).
- Confirm the CTF sanctions the target (village-owned vs. real infra).
- Set `MAX_CALL_MINUTES` so a stuck call can't burn Twilio budget.

## The triage dial

- Place the call with recording enabled.
- Listen for 15–30s. Classify what you hear:
    - Ringback → nobody home (or they're screening — retry, or move on)
    - IVR menu → recipe #3 (IVR walk)
    - Silence with periodic prompts → likely DISA — recipe #4
    - Voice greeting → likely voicemail — recipe #8
    - CED (2100 Hz) → fax — recipe #7
    - Carrier tones → modem — recipe #5
    - Multiple voices / hold music → conference bridge — recipe #9
    - Milliwatt (1004 Hz test tone) → CTF humor — try 2600-adjacent puzzles
    - ANAC-like "your number is …" → identify what ANI the CTF sees

(Recipe numbers cross-reference [`call_recipes.md`](call_recipes.md).)

## Common puzzle patterns

- The greeting IS the puzzle (voicemail, IVR intro)
- The hold music IS the puzzle (steganography, morse)
- The IVR menu options are a cipher (option 4 = D, etc.)
- The fax page IS the flag (image with QR / text)
- The DISA PIN comes from another puzzle
- The number itself is a cipher (letters on the keypad)

## What to write down

- Full recording (Twilio-side)
- Transcript of any voice prompts (once `transcribe` tool exists)
- DTMF you heard (once `dtmf_decode` exists)
- Timing of prompts and pauses (for later diffing)

## When to stop

- Budget cap reached
- You've extracted the flag
- You've confirmed the puzzle needs an out-of-band input you don't have yet
