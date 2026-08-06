# 2600 Hz — WHISTLE TOLERANCES & THE SF DETECTOR

> "A cereal-box whistle worked because the detector was built to forgive a
>  worn-out relay, not to defeat a teenager."

The recognition/reference layer behind the SF supervision tone. This is
*why* 2600 Hz, *how* the detector decided a tone was really there, and
*how far off* you could be and still trip it. For the attack itself see
[[blueboxing/README]] and the step-by-step [[blueboxing/seizure-walkthrough]].

## Why 2600 Hz specifically

The tone had to live **inside** the ~300-3400 Hz voice channel (so it rode
the same trunk as speech) but **above** most speech energy (so conversation
wouldn't false-trip supervision). 2600 Hz sits near the top of the passband:
high enough that sustained voice rarely parks there, low enough to survive
roll-off, and clear of the ~2100 Hz answer/echo-suppressor-disable band —
which is exactly why fax later put its CED at 2100, not near 2600 (see
[[fax/README]]).

## The detector, in caricature

Two stages in series: a **band-pass filter** centered on 2600 Hz ("is there
energy at the supervision frequency?"), then a **duration / persistence
filter** ("long enough to *mean* something, versus a fricative or a burst of
music?"). Only energy that passes *both* counts as supervision — and that
two-stage design is the whole story of the tolerances below.

## The numbers (per `records/tones.json` — do not contradict)

- **Frequency:** 2600 Hz **+/- 15 Hz** (`sf_2600`). That +/-15 Hz window is
  the generous part — a whistle a few Hz off still lands inside.
- **Level:** **-20 dBm0** idle guard; **~-8 dBm0** while pulsing (some
  carriers -6 to -10).
- **Pull-in vs drop-out:** the detector arms after the tone persists past
  the duration filter (pull-in) and disarms after it's gone for a set
  interval (drop-out), with hysteresis so a momentary dropout doesn't
  chatter the trunk state.
- **Seizure hold time is disputed, bound to the switch:** 4ESS **>=400 ms**,
  some 1ESS **~650 ms**, community canon **750-1000 ms "safe."** Never quote
  a single seizure figure without naming the switch — the record flags this.

## Why the Cap'n Crunch whistle worked

The bosun-whistle from a Cap'n Crunch box put out a crude, drifting tone
*near* 2600 Hz. It worked anyway because the **+/-15 Hz** window forgave the
frequency error, the band-pass didn't demand a pure sinusoid (just enough
in-band energy), and the **duration filter** was the real gate — hold the
note steady past pull-in and the switch was satisfied. The detector was
built to hear a tired relay across a noisy long-haul circuit, not to reject
a teenager: generous bandwidth was a reliability feature and a gift to
phreaks.

## The CCITT No.5 gotcha — 2600 is NOT the international seizer

The single most common trap: on an **international CCITT No.5** trunk,
**2400 Hz** is the *seizure* signal and **2600 Hz** is only
*proceed-to-send* (`ccitt5_line_seize`). A generator emitting *only* 2600 Hz
will **not** seize a C5 trunk. Domestic SF (2600) and international C5 (2400
seize / 2600 proceed) are different systems — see
[[tandem-stacking/international]] for the full sequence.

## Recognition at a CTF — "am I on an SF trunk?"

Be honest about the era: **production SF trunks are gone** (US in-band
supervision migrated to CCIS/SS7, largely complete by the late 1980s). So
in practice a village/CTF is **emulating** one. Treat SF as a puzzle
signal, not a live vulnerability. Tells that an emulated SF trunk *wants*
2600:

- After you connect, a held 2600 Hz produces a **state change** — a wink,
  a drop of the far audio, a "come ahead" — rather than being ignored as
  plain audio.
- The puzzle hands you a register that then expects **MF** (KP + digits +
  ST), not DTMF.
- If 2600 does nothing but **2400** produces a response, you're looking at
  a C5 emulation — reach for the international sequence instead.

## See also
- [[blueboxing/README]] — what the tone was *for*
- [[blueboxing/seizure-walkthrough]] — applying it, step by timed step
- [[blueboxing/mf-tones]] — the MF digits you send after the wink
- [[tandem-stacking/international]] — where 2400 vs 2600 actually bites
- [[ess/README]] — which switches carried the detector alarms

## Sources
- Bell System Technical Journal, Vol. 39 No. 6 (Nov 1960), pp. 1319-1408
  — in-band single-frequency signaling, frequency/level definitions.
- CCITT Blue Book (1988), Recs Q.310-Q.332 — No.5 line signals (2400/2600).
- Ron Rosenbaum, "Secrets of the Little Blue Box," Esquire, Oct 1971
  — the Cap'n Crunch story (journalism, not a technical primary source).
- 2600 Magazine (various issues) — detector-tolerance lore.
