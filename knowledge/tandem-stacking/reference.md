# Tandem stacking — reference

Trunk-route addressing on an in-band MF R1 network. Everything below
assumes you're already on a seized trunk (see
[[blueboxing/seizure-walkthrough]]) and can pulse MF.

## Trunk route codes

An MF-signaled tandem accepts addresses in one of two forms:

1. **Ordinary destination:** `KP + [7-digit or 10-digit destination] + ST`.
   The tandem routes to the called number by NPA-NXX lookup.
2. **Explicit trunk-route:** `KP + [3-digit route code + destination] + ST`,
   or on some toll switches `KP + 0 + [route code] + destination + ST`.
   The `0` (or `1`) prefix digit signals "nature of address = explicit
   routing," followed by a route number that identifies a specific
   outbound trunk group.

The exact route-code space is switch- and translation-table-dependent.
Route numbers are 3-digit CLLI-mapped groups (e.g., `010` = a specific
outbound group, `023` = another). To learn a switch's route codes you
had to either read leaked translation-table dumps (a Phrack staple —
see 27.5 "COSMOS Part Two") or map by trial.

## Special route codes worth knowing

| Route | Meaning (era-typical) |
|---|---|
| 0 | Nature-of-address = operator | Reaches an operator on the far tandem — sometimes an out-of-scope TSPS position. |
| 00 | Nature-of-address = international operator | If the far tandem was a gateway (4ESS/DMS-250 with international routing), 00 could land you on an international operator position. |
| 01 | International direct dial | On a gateway tandem, `KP + 01 + CC + national_number + ST` was the international-dialing form. Domestic tandems reject this. |
| 010 / 020 / 030 / … | Named outbound trunk groups | Actual codes vary per switch. Learned by reading the switch's translation tables (see COSMOS phile family, Phrack 26.5 / 27.5 / 31.6). |
| 950-XXXX (as tail digits) | Feature Group B carrier access | On a tandem that routed FGB, KP + 950 + 4-digit CIC + ST reached an alternate long-distance carrier's POP. |
| 1-700-555-4141 | Carrier ID | AT&T's "you have reached AT&T" verification line. Reached this from a stacked hop to confirm which IXC you were on. |

## Internal test numbers reachable via stacked hops

Once you were on a distant tandem, its local test numbers were
reachable as if you were a local customer of that CO.

- **Loop-arounds (LP1/LP2):** matched pair of numbers that terminate on
  the CO's milliwatt individually; when both are seized (one from each
  side) audio bridges. Historic use: anonymous meet-ups pre-BBS.
  Numbers vary per CO — canonically prefix `95X` or `96X` with a `99XX`
  suffix. Do NOT hardcode "the" loop-around number; per-NPA discovery
  applies.
- **Milliwatt (1004 Hz 0 dBm0):** commonly `959-1111` or `NPA-XXX-1111`
  in DMS regions.
- **Ringback:** commonly `660 + last 4 of your own number`, `571-XXXX`,
  or `260-XXXX`. Highly office-dependent.
- **ANAC (calling-number readback):** `958`, `958-XXXX`, `200-222-2222`,
  `311-1111` — per-CO / per-NPA (see the ANI-II and numbering records
  in the KR).

## Audio texture per hop

Each seizure + reroute produced a distinct sequence:

1. **Own-side seizure:** you play 2600 Hz for ~700 ms into an
   established call. You hear a brief pop / silence as the near-end
   tandem drops to wink/idle.
2. **Wink:** the far-end tandem returns a ~150-200 ms off-hook /
   on-hook pattern. On some carriers you hear this as a very short
   click-click cadence in the audio.
3. **MF pulse:** you send `KP + address + ST` at 60-75 ms per digit,
   100 ms for KP. The tones are clearly audible — sub-second bursts of
   the six R1 frequencies.
4. **Routing:** silence (or very light hiss) as the tandem selects an
   outbound trunk group and forwards.
5. **Second hop:** if you're stacking, you may hear a second wink from
   the next tandem, or you may hear ringback of the final destination.

## Billing-record misalignment

The reason phreaks stacked hops rather than just called direct: each
tandem generated a separate AMA (Automatic Message Accounting) record.
On an in-band SF/MF network, the AMA record from the *originating* CO
recorded the destination the phreak first dialed — not the seized-and-
rerouted destination. Downstream tandems' AMA didn't tie back to any
paying customer. Once a call reached its actual destination through 3
or 4 stacked hops, no single AMA record described the whole path.
Reconciliation was a manual, after-the-fact process — which is why
Bell's SPC-based billing systems, and eventually SS7's answer-message
ANM, exist.

## Sources

- BSTJ Nov 1960 — the R1 MF spec
- Phrack 4.4 (Phantom Phreaker, MAX Long Distance profile) — trunk
  routing terminology
- Phrack 27.5 (King Arthur, COSMOS Part Two) — translation tables
- Phrack 11.10 / 12.8 (Phantom Phreaker, Busy Line Verification) — the
  operator platform on the receiving end of stacked calls
