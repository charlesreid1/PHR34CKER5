# DTMF — TOUCH-TONE

> Dual-Tone Multi-Frequency. The sound of a phone number since 1963. Two
> sine waves, one from a low group and one from a high group, summed — so
> a single tone can't fake a digit and a voice can't accidentally dial one.

## The grid

Each key is one **low** row tone + one **high** column tone (Hz):

|         | 1209 | 1336 | 1477 | 1633 |
|---------|------|------|------|------|
| **697** | 1    | 2    | 3    | A    |
| **770** | 4    | 5    | 6    | B    |
| **852** | 7    | 8    | 9    | C    |
| **941** | *    | 0    | #    | D    |

So `5` = 770 + 1336 Hz; `#` = 941 + 1477 Hz. This is exactly the table the
tone generator uses — `generate_dtmf("5")` emits 770+1336, and
`dtmf_decode` / `dtmf_decode_wav` recover it by Goertzel power in those
eight bins with a twist check (see below).

## The fourth column: A B C D

The 1633 Hz column is real DTMF but absent from consumer phones. It came
from **AUTOVON**, the US military phone network, where the four keys were
precedence signaling — hold down a priority key to preempt lower-priority
calls:

| Key | AUTOVON meaning        |
|-----|------------------------|
| A   | FO — Flash Override    |
| B   | F — Flash              |
| C   | I — Immediate          |
| D   | P — Priority           |

A/B/C/D survive today in some PBX admin, ham radio (repeater control),
and — reliably — CTF puzzles, precisely because most keypads can't send
them. If a village line only answers to a "D", you need a tone generator,
not a handset. `generate_dtmf("ABCD")` and `play_dtmf_into_call` speak the
full 16-symbol alphabet.

## Twist, timing, and why decoders are picky

- **Twist** — the amplitude difference between the high and low tone. Real
  DTMF sits within ~±(3–8) dB; the network rejects tones outside a window.
  The decoder in this repo rejects frames whose high/low ratio exceeds
  ±12 dB, which is what stops speech and music from decoding as digits.
- **Duration** — a valid digit is ~40 ms minimum on; the decoder debounces
  runs shorter than that as noise.
- **Guard time** — a gap (or a change of digit) separates one press from
  the next, which is how `11` reads as two ones and not one long one.

## Common misconceptions

- **`*` and `#` are not universal control keys.** They're just two more
  DTMF symbols; what they *do* is entirely up to the far-end application.
  On one IVR `#` submits, on another it's ignored, on a third it's the
  puzzle input.
- **DTMF is not pulse dialing.** Pulse (loop-disconnect) dialing clicks a
  count of the digit; DTMF is tones. A line that only understands pulse
  won't hear touch-tones at all — a classic "why won't it respond" trap.
- **Overlap/overdial.** Some legacy PBXs act on the first N digits before
  you finish; sending a long string fast can route you somewhere before
  the last digits land. Insert gaps (`generate_dtmf("1,2,3")`) when timing
  matters.

## See also
- [[blueboxing/mf-tones]] — MF is the *other* multi-frequency scheme; don't confuse the two
- [[ctf/ivr-mazes]] — where touch-tones are the puzzle input
- [[fax/README]] — DTMF sometimes hides under a fax/voice prompt

## Sources
- ITU-T Q.23 / Q.24 — DTMF frequency and level specifications
- Bell System Technical Journal, "Signaling Systems for Control of
  Telephone Switching" (Nov 1960) — the MF/DTMF design rationale
- MIL-STD-188-100 — AUTOVON precedence signaling (A/B/C/D)
