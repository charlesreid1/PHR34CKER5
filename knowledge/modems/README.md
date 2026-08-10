# MODEMS — THE CARRIER HANDSHAKE

> The whistle-then-hiss you heard when a call answered with a data set on
> the far end. Every stage of that noise is a negotiation you can read.

A modem call opens with a scripted courtship: an **answer tone**, then a
back-and-forth of probes as the two ends agree on the fastest scheme both
support, then the steady "hiss" of scrambled data (the *carrier*). When a
war dialer or a CTF triage dial lands on a modem, that opening is the tell.

## What you hear, in order

```
  (ring, answer)
  ANSWER TONE      2100 Hz, ~3 s     "a data set answered"   <-- detect_tone target: ced/modem
  probes / trill   rate-dependent    the two ends feel out V.8 / fallback
  CARRIER          scrambled hiss    training + data; broadband, no pitch
```

The **answer tone is 2100 Hz** — the *same frequency as fax CED*. That
overlap is not a coincidence: both are "I am a machine, proceed" answers,
and both sit clear of the 2600 Hz supervision band (see [[fax/README]] and
[[2600hz/README]]). This is why `detect_tone` reports `ced` and `modem` as
sharing 2100 Hz: on the first ~3 seconds you often *can't* tell fax from
modem by frequency alone — you wait for what comes next (fax → V.21
preamble and CNG/CED cadence; modem → wideband training).

## The rate zoo

| Scheme      | Rate            | Era    | Audible signature                    |
|-------------|-----------------|--------|--------------------------------------|
| Bell 103    | 300 bps         | 1962   | two soft FSK tones, almost musical   |
| Bell 212A   | 1200 bps        | 1970s  | 300-style origin + PSK carrier       |
| V.21        | 300 bps         | —      | FSK; also the fax control channel    |
| V.22 / bis  | 1200 / 2400 bps | 1980s  | steady PSK carrier                   |
| V.32 / bis  | 9600 / 14.4k    | 1984–91| echo-cancelled; louder "roar"        |
| V.34        | up to 33.6k     | 1994   | long line-probing sweep up front     |
| V.90 / V.92 | 56k down        | 1998   | digital-side asymmetry               |

Lower rates sound *tonal* (you can almost hum 300 baud); higher rates
sound like *broadband noise* because the data fills the whole voice band.
The longer the up-front probing/sweep, the newer the standard (V.34's line
probe is a distinctive rising warble).

## Reaching for it at a CTF

1. `detect_tone(sid, targets=["ced","modem","2600"])` on answer. A strong
   2100 Hz that then turns to hiss (not the CNG/CED fax cadence) = modem.
2. `start_recording` / `listen` to capture the carrier for offline analysis.
3. Hand off to a real data stack — `minicom`, `ATDT`, `pppd`, or a soft
   modem — because this repo synthesizes/*detects* audio but does not
   demodulate a carrier. The MCP gets you to the point of "yes, that's a
   modem at roughly rate X"; a terminal program takes it from there.

```
play_sequence(sid, [
    {"action": "wait_for_answer"},
    {"action": "detect_tone", "s": 3, "targets": ["ced", "modem"]},
    {"action": "listen", "s": 8},   # capture the training for offline demod
])
```

## Why modems are CTF puzzles

- The **login banner** behind the carrier is the flag (old BBS, a Unix
  `login:`, a Telebit/PEP prompt).
- The **handshake stage that fails first** when audio is stripped or
  transcoded is itself a clue — G.711 μ-law over VoIP mangles high-rate
  training, so a V.34 line may only fall back to V.22 through Twilio. If a
  connection won't train past 2400, suspect the codec, not the puzzle.
- A **fake carrier** (recorded hiss with no real data) is a troll; a real
  one will actually train against a soft modem.

## See also
- [[war-dialing/README]] — how carriers were found in the first place
- [[ctf/modem-carriers]] — the CTF-facing probe recipe
- [[fax/README]] — the 2100 Hz answer-tone cousin
- [[bbs/README]] — what usually lived behind the carrier

## Sources
- ITU-T V.8 (call setup), V.21, V.22bis, V.32bis, V.34, V.90
- ITU-T V.25 — the 2100 Hz answer tone and its echo-suppressor-disabling
  phase reversals
- Bell System Technical Journal — Bell 103 / 212A data set descriptions
