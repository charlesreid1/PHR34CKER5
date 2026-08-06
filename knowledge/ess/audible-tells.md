# AUDIBLE TELLS — FINGERPRINTING A SWITCH BY EAR

> Before you probe a number, listen to it. The switch on the far end
> announces itself in the timbre of its dial tone, the crispness of its
> reorder, and the voice that tells you the call failed.

You rarely get told what switch you reached. But the network's own
**call-progress tones** and **intercept recordings** are switch-family
tells. The center frequencies are standardized (350+440 dial tone,
480+620 busy/reorder, 440+480 ringback) — what varies is *timbre*,
*cadence*, *onset speed*, *DTMF acceptance*, and the *recorded-voice
style*. Those variations are the fingerprint.

## The three tones that matter most

| Tone | Freqs (Hz) | Cadence | Meaning |
|---|---|---|---|
| Dial tone | 350 + 440 | continuous | switch ready |
| Busy (line) | 480 + 620 | **500 on / 500 off** (60 IPM) | called party off-hook |
| Reorder (fast busy) | 480 + 620 | **250 on / 250 off** (120 IPM) | no path / all-trunks-busy |
| Ringback | 440 + 480 | 2 s on / 4 s off | far end ringing |

Busy and reorder share the *same frequency pair* — only the cadence
separates them. This is exactly what `detect_tone` keys on: its cadence
estimate splits `busy` (500/500) from `reorder` (250/250). If you can't
tell them apart by ear at a con, run `detect_tone(call_sid, targets=
["busy","reorder"])` and read the `cadence.on_ms`. Reorder means "the
network could not build the call" — a very different clue than a plain
busy.

## Per-family tells

| Switch | Dial-tone timbre & onset | Reorder cadence | "Cannot be completed" style | Tone/pulse |
|---|---|---|---|---|
| **Step-by-step (SxS)** | rough, buzzy; older offices a single ~600 Hz "growl" or howler, with faint relay clatter behind it; noticeable delay before it appears | present but sometimes irregular | often no SIT; a plain tape loop or just reorder | **pulse native**; DTMF frequently ignored |
| **Crossbar (No.1/No.5 XB)** | precise 350+440, cleaner than SxS, mild hum | standard 120 IPM | tape / Audichron announcer | pulse; DTMF only if retrofitted |
| **1ESS / 1AESS** | precise, dead-clean, near-instant | crisp 250/250 | **SIT triplet** then classic Bell voice (Jane Barbe / Pat Fleet) | DTMF native, instant register |
| **4ESS (toll/tandem)** | *no subscriber dial tone* — you meet it mid-call, on a long-distance route | "all circuits busy" reorder / SIT on toll failures | toll intercept + SIT | trunk MF/CCIS, no local loop |
| **5ESS** | precise, instant, digitally clean onset | crisp 250/250 | SIT then digital recorded voice | DTMF native |
| **DMS-100** | precise, instant; some report a subtly "warmer" tone | crisp 250/250 | SIT then Nortel announcer style | DTMF native |

## The SIT triplet — the loudest tell of all

An intercept recording is almost always preceded by a **Special
Information Tone**: three rising tones whose exact frequencies encode
*why* the call failed. Hearing SIT at all means a switch-generated
intercept, not a human. The reason-code variants (approximate):

- **Intercept (IC):** 913.8 / 1370.6 / 1776.7 Hz
- **Vacant code (VC):** 985.2 / 1370.6 / 1776.7 Hz
- **Reorder (RO):** 913.8 / 1428.5 / 1776.7 Hz
- **No circuit (NC):** 985.2 / 1428.5 / 1776.7 Hz

The *voice* after the SIT is a secondary tell: pre-divestiture Bell
offices used a small stable of recorded-announcement talents; GTE and
independents used different voices and phrasings ("We're sorry…" vs.
"Your call cannot be completed as dialed…").

## The pulse-vs-tone probe

The fastest active discriminator: dial one digit as DTMF and see if it
registers. If DTMF is ignored but pulse works, you are on step-by-step
or un-retrofitted crossbar. Instant DTMF cut-through = ESS or DMS.
See `[[dtmf/README]]`.

## At a CTF

A Village can *emulate any of these on purpose* — a challenge that plays
a rough SxS growl and refuses DTMF is telling you "think 1960s
electromechanical," and one that answers with a pristine SIT+reorder is
pointing at a specific failure code. Treat the tone as content, not
noise: `start_recording` from first ring, then `detect_tone` to pin the
cadence, then `transcribe` the intercept voice for wording that may
itself be the flag.

## See also
- [[ess/README]] — the switch lineage these tells map onto
- [[ess/no-4-ess]] — why the toll switch has no subscriber dial tone
- [[ctf/modem-carriers]] — the other "what am I hearing" triage layer
- [[dtmf/README]] — the pulse-vs-tone acceptance probe
- [[glossary/README]] — SIT, reorder, intercept, IPM

## Sources
- BSTJ, "No. 1 ESS" (Sept 1964) and "No. 4 ESS" (1977)
- Bellcore/Telcordia GR-506-CORE (call-progress tone frequencies and
  cadences); precise-tone plan (350+440 / 480+620 / 440+480)
- Telcordia SR-2275 (BOC Notes) — Special Information Tones and
  intercept treatment
- Phrack #25.3 "Bell Network Switching Systems" — Taran King
- 2600 Magazine (various) on identifying switches by call-progress audio
