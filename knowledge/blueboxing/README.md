# BLUEBOXING

> "The phone company built a network that trusted its own signaling. That
>  trust was the vulnerability."

A **blue box** generates in-band Multi-Frequency (MF) tones over an active
voice call to talk to the far-end trunk equipment directly — seizing trunks,
routing calls, and (historically) bypassing billing.

## Core tones
- **2600 Hz** — trunk idle / supervision. A held 2600 Hz tone would drop the
  billing side of the call while leaving the trunk seized.
- **KP** (700+1100 Hz) — Key Pulse. Start-of-address signal.
- **ST** (1500+1700 Hz) — Start. End-of-address signal.
- Digit pairs (MF 1–0) — see `mf-tones.md` (to be written).

## Sequence, in caricature
1. Dial a long-distance number you legitimately have access to.
2. When the far end answers (or during ringback), send 2600 Hz for ~1s.
3. The near-end trunk hears "idle" and hands you off to signaling.
4. Send `KP <digits> ST` to route wherever the tandem will take you.

## Why this is history
Modern networks moved signaling **out of band** (SS7, and later SIP/Diameter)
specifically to close this class of attack. In-band MF is gone from the PSTN
in almost every jurisdiction. This file is preserved as an artifact of how
signaling used to work.

## See also
- [[2600hz/README]]
- [[ess/README]] — the switches that MF talked to
- [[tandem-stacking/README]]

## Sources
- BSTJ, "No. 4 ESS: Long Distance Switching for the Future" (1977)
- Rosenbaum, "Secrets of the Little Blue Box", Esquire, Oct 1971
