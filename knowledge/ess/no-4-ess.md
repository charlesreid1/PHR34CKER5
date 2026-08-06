# NO. 4 ESS — THE TOLL SWITCH THE BLUE BOX TALKED TO

> Every free long-distance call in the 1970s was a conversation with a
> 4ESS. It was the blue box's favorite audience — and, a decade later,
> its executioner.

The **No. 4 ESS** (Western Electric / AT&T, first cutover **1976**,
Chicago) was the digital **toll/tandem** switch that carried
long-distance traffic across the AT&T Long Lines network. Unlike a
local switch, a 4ESS had no subscriber loops — it terminated
**inter-office trunks** and routed calls between distant cities. That
role is exactly why it mattered to phreaks: when you placed a
long-distance call, your local office handed you up to a toll switch,
and on an SF/MF route that toll switch was very often a 4ESS.

## Why it was the blue box's target

Blue-boxing (`[[blueboxing/README]]`) works by talking **in-band** to
the trunk-side signaling equipment — the equipment that lived on the
toll switch. The attack sequence:

1. Seize a real long-distance trunk by dialing a distant number.
2. Play **2600 Hz** into the path. The 4ESS's trunk hears the
   supervision tone as "far end hung up" and drops the billing side
   while the trunk stays up.
3. The trunk winks and enters MF-register mode, expecting an
   originating toll office to key-pulse a destination.
4. Send `KP + digits + ST` in R1 MF and the 4ESS routes you — as if you
   were the network itself.

The 4ESS believed in-band signaling because that is how toll switches
talked to each other. See `[[blueboxing/seizure-walkthrough]]` for the
step-by-step audio.

## Role in the toll network

- **Class 4 tandem:** aggregated and routed interoffice/interLATA
  traffic; a single 4ESS could handle over 100,000 trunks.
- Among the **first switches to carry CCIS (Common Channel Interoffice
  Signaling, CCITT No. 6)** — the out-of-band signaling ancestor of
  SS7. Early 4ESS routes still ran SF/MF in-band, but the migration
  path was built in from the start.
- Handled operator (TSPS) and international gateway traffic on many
  routes.

## How the 4ESS also killed blueboxing

The toll switch was not just the victim — it hosted the **detection**
that ended the game:

- **2600 Hz hold-time alarms.** Generic loads on 4ESS (and 1AESS)
  flagged a supervision tone held past a plausible window — a human
  never sends a clean 700–1000 ms 2600 Hz burst mid-conversation.
- **AT&T's "greenstar" program** logged suspicious 2600/MF patterns on
  toll trunks through the 1970s–80s, building traffic-study evidence
  that fed prosecutions.
- The decisive kill was **architectural, not legal:** as toll routes
  migrated from SF/MF to **CCIS and then SS7**, call-control signaling
  moved to a separate data channel. A 2600 Hz tone in the voice path
  became just *audio* — the far end no longer listened to it for call
  state. AT&T completed CCIS on major routes through the early-to-mid
  1980s; by **~1990 a blue-box call on a major US route was already
  impractical**, and it was fully dead as SS7 became ubiquitous on
  interoffice trunks by ~1992.

Independents, small tandems, and some international gateways ran in-band
signaling later — into the mid-1990s — which is why blueboxing lore
persisted after it had died on the AT&T backbone.

## See also
- [[ess/README]] — where the 4ESS sits in the switch lineage
- [[ess/audible-tells]] — why a toll switch gives you no dial tone
- [[blueboxing/README]] — the attack the 4ESS enabled
- [[blueboxing/seizure-walkthrough]] — the seizure, tone by tone
- [[2600hz/README]] — the supervision tone at the center of it all

## Sources
- BSTJ, "No. 4 ESS: Long Distance Switching for the Future" (1977)
- Bell Labs Record, 1976–1977 (4ESS cutover, CCIS deployment)
- Phrack #25.7 "The Blue Box and Ma Bell" — The Noid
- Ronald Rosenbaum, "Secrets of the Little Blue Box," Esquire, Oct 1971
  (historical framing)
- Bruce Sterling, *The Hacker Crackdown* (1992) — enforcement-era context
