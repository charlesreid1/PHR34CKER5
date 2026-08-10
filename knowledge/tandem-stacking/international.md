# STACKING ACROSS THE OCEAN — INTERNATIONAL TANDEM ROUTES

> "Every hop was another switch that trusted the last one. Chain enough of
>  them and the billing side lost the thread entirely."

The international extension of [[tandem-stacking/README]]: what a routing
burst *meant* hop-to-hop, how the CCITT No.5 international seizure differs
from domestic SF, and the overseas-loop trick. Assumes you already know
the R1 MF digit table in [[blueboxing/mf-tones]] and the SF vs C5 tone
distinction in [[2600hz/whistle-tolerances]].

## KP + routing + ST, one hop at a time

A tandem doesn't understand "call London" — it understands *the next leg*.
Each `KP <address> ST` opened one register, filled it, and told that tandem
to grab an outgoing trunk and cut through. On the far trunk you started
over: seize, `KP <next address> ST`, repeat. The address in each burst was
whatever *that* switch's routing plan expected — a trunk-route code, an
office prefix, or the full called number — not necessarily a dialable
consumer number.

## Domestic SF vs CCITT No.5 — the seizure differs

| | Domestic (NANP, SF) | International (CCITT No.5) |
|---|---|---|
| Seize | drop **2600 Hz** (`sf_2600`) | send **2400 Hz** (`ccitt5_line_seize`) |
| Proceed-to-send | (the wink) | **2600 Hz** |
| Clear / answer | 2600 patterns | pulse patterns of **2400 + 2600**, singly & combined |
| Address (inter-register) | R1 MF: KP + digits + ST | **same R1 MF set** (700-1700): KP + digits + ST |

The catch the record flags: on a C5 trunk **2400 Hz seizes** and 2600 is
only proceed-to-send. A generator that emits only 2600 will never seize an
international trunk. After the C5 line handshake, the address stage is
ordinary R1 MF — so the tones you *pulse* are the same ones from
[[blueboxing/mf-tones]]; only the *supervision* differs.

## A worked overseas hop (~1980 era, historical)

```
2400 Hz                 seize the international trunk
  (far end)   2600 Hz   proceed-to-send
KP  011  CC  NN  ST      KP + intl-access + country code + national number + ST
```

`KP 011 <CC> <NN> ST` = the international-format address on an
international-capable trunk. What you *hear* as it stacks: each tandem cuts
through audibly — a wink, a beat of open trunk, then the next leg's
ringback or the next register accepting MF. Stacking means you **hear each
hop** in series; a three-tandem path sounds like three cut-throughs before
the destination rings.

## Why the billing records didn't line up

Each tandem wrote its **own** AMA entry for the leg *it* set up, keyed to
the trunk it *thought* it was serving. Seize a trunk mid-call and re-pulse a
new destination, and the downstream leg is born under a switch that has no
record of your true origination — its AMA ties to the *previous tandem's
trunk*, not your line. Across several hops nothing reconciles end-to-end:
the origin office bills a short domestic call (or nothing, after the 2600
drop) while the real overseas leg lives in a downstream switch's books under
a trunk identity that points nowhere useful.

## The overseas-loop trick

Route *out* to a foreign tandem, then have that tandem route *back into the
US*. The final US leg then appears to **originate overseas**, disguising the
true origination and frustrating trace-back — the inbound-international leg
carried the foreign tandem's identity, not yours. It was equal parts
misdirection and billing-misalignment: the call you actually placed and the
call the records described were different calls.

## Disputed persistence — flag it

Community memory holds that **CCITT No.5 lingered on Caribbean and West
African routes into the mid-1990s**, long after major routes converted to
CCIS (No.6) and SS7 (No.7) in the 1980s. Primary ITU switching-plan
confirmation for those specific late-90s seizures is **spotty** — treat
"C5 still worked on route X in 199x" as **community-provenance**, not
established fact (`ccitt5_line_seize.disputed.persistence`).

## See also
- [[tandem-stacking/README]] — the domestic concept
- [[blueboxing/mf-tones]] — the R1 MF address tones (same set C5 reuses)
- [[blueboxing/seizure-walkthrough]] — a single domestic seizure, timed
- [[2600hz/whistle-tolerances]] — 2400 vs 2600, the international trap
- [[ess/README]] — 4ESS as the US toll tandem

## Sources
- CCITT Blue Book (1988), Recs Q.310-Q.332 — No.5 line + register signals.
- Bell System Technical Journal, Vol. 39 No. 6 (Nov 1960), pp. 1319-1408
  — R1 MF format the international register set reuses.
- Ron Rosenbaum, "Secrets of the Little Blue Box," Esquire, Oct 1971
  — historical framing (journalism, not a technical primary source).
- 2600 Magazine (various issues) — overseas-loop lore and the disputed
  C5-persistence reports (community-provenance).
