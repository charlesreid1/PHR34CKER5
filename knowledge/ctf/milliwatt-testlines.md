# MILLIWATT TEST LINES

> A number that just hums one note forever. Boring — until the note twitches.

A **milliwatt test line** answers with a single steady test tone at a defined
level, used by telco techs to measure loss on a circuit. The canonical one is
**1004 Hz** (older lines use 1000 Hz) held at **0 dBm0 — one milliwatt** — the
"milliwatt" reference. At a CTF it's usually a wink at the audience, and
sometimes a steady tone that isn't quite steady.

## First 15 seconds

- Instant pickup, then a **pure, continuous tone** — a single held note, no
  cadence, no on/off pulsing. 1004 Hz (or 1000 Hz) is the classic.
- It just *sustains*. No menu, no voice, no handshake, no ringback pauses.
- Related **100-type test lines** may instead give a **quiet termination**
  (near silence, for noise measurement) or a **sweep** (a tone that glides
  across frequencies). A loopback line echoes your own audio back.

Milliwatt (1004 Hz test tone) → CTF humor / 2600-adjacent puzzles. See
`docs/ctf_playbook.md` triage tree ("Milliwatt (1004 Hz test tone) → CTF
humor").

## How to probe it

1. `detect_tone(call_sid, targets=["milliwatt"])` — confirms a ~1004 Hz steady
   tone and reports the dominant frequency and a cadence estimate. A flat
   cadence with one dominant freq is the signature.
2. Don't stop at "it's a test tone." **Record a long sample** and watch for the
   note to *move*: brief frequency steps, amplitude dips, or on/off gaps that a
   truly steady milliwatt would never have.
3. Check for **level/loss encoding** — if multiple test numbers each answer at
   different dB levels, the levels themselves may spell digits.
4. Compare against **2600 Hz** and other single-frequency tones nearby — a CTF
   loves to swap the expected 1004 Hz for a meaningful frequency
   (`[[2600hz/README]]`).

## Tools to reach for

- `detect_tone` (target `milliwatt`) — identify and get dominant-freq/cadence
- `start_recording` + `get_recording_url` — capture a long steady sample for
  spectral analysis (amplitude/frequency shifts over time)
- `generate_tone` — synthesize a reference 1004 Hz tone to A/B against what you
  hear and spot the deviation

```python
play_sequence(call_sid, [
    {"action": "wait_for_answer"},
    {"action": "detect_tone", "seconds": 3, "targets": ["milliwatt"]},
    {"action": "listen", "s": 20},   # long sample: watch for the tone to twitch
])
```

## What it means as a puzzle

- **A pattern hides in the "steady" tone** — amplitude shift-keying, small
  frequency steps, or timed gaps encode Morse or bits over an otherwise
  featureless hum. The steadiness is the misdirection.
- **The frequency is the message** — 2600 Hz where you expected 1004 Hz is a
  pointer to `[[2600hz/README]]` and blue-box lore.
- **Level = data** — a bank of test lines at graded dB levels reads out digits.
- Often it's simply **CTF humor**: a nod to phreaking heritage with no deeper
  flag. Confirm before spending budget.

## See also
- [[2600hz/README]] — single-frequency tones and the whistle that named it all
- [[ctf/conference-bridges]] — the other "steady audio hides a pattern" genre
- [[ess/README]] — where test lines and 100-type terminations live in the plant
- [[blueboxing/README]] — in-band tones as signaling

## Sources
- Bell System Technical Reference / Telcordia on 100-type test lines and the
  1004 Hz / 0 dBm0 milliwatt reference
- ITU-T O-series (transmission measuring equipment) — the 1020 Hz reference
  generator and level-measurement practice
- 2600 Magazine (various issues) on test numbers and milliwatt lines
