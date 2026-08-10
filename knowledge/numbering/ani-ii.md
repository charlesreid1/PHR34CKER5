# ANI II — the "info digits"

Every call on a Feature Group D (FGD) trunk arrives with a two-digit
**info-digit prefix** that describes the *class* of line the call
originated on — separate from the calling number itself. This is the
"ANI II" (or "II digits") the terminating switch sees before it sees the
ANI proper.

The full 100-code table is stored as typed records in
[`knowledge/records/operator_service_codes.json`](../records/operator_service_codes.json).
Look them up via `lookup_tone`-style tools (any `search_records` with
`category=operator_and_service_code`) or query a specific code
(`ani_ii_27_coin`, `ani_ii_61_cellular_type1`, etc.).

## The classes a CTF assistant actually cares about

- **00** — Ordinary POTS. Default; anything that isn't below.
- **02** — ANI failure. The switch couldn't produce a calling number.
- **06** — Hotel/motel guest room without CDR.
- **10** — Test call from a network test facility.
- **20** — AIOD PBX extension (per-station billing).
- **23** — *Pre-1988* combined coin/coinless payphone. Split into 27/70.
- **24 / 25** — Inbound to 8YY (toll-free) / 900 (premium).
- **27** — Coin payphone (ACTS-equipped). Post-1988 split-child of 23.
  This is the class that used to hand the assistant "you are being
  called from a real payphone" for free.
- **29** — Inmate telephone system.
- **30 / 31 / 32** — Intercept: blank / trouble / regular.
- **60 / 66 / 67** — TRS (relay-service). Added 1993 per ADA. 66 = TRS
  from a hotel; 67 = TRS from a restricted (prison) line.
- **61 / 62 / 63** — Cellular / wireless (Type 1 / Type 2 / Type 2
  alternate).
- **70** — Private paystation (coinless). Post-1988 split-child of 23.
- **93** — Private virtual network / enterprise VPN off-net access.

Everything else in the 00-99 range is Reserved on a period-authoritative
NANPA letter (see the `ani_ii_reserved_range` record for the full list).
Some reserved codes have been assigned by post-2003 letters; when
answering, cite the letter version by date.

## How the digits actually reach the far end

On MF FGD trunks the format is:

```
KP  +  II  +  KP  +  ANI (10 digits)  +  ST
```

Two `KP`s: the first delimits the II prefix, the second delimits from
the 10-digit ANI. On SS7 ISUP, delivered as the OLI (Originating Line
Information) parameter — one octet, hex 00-63, mapping to decimal
00-99. The record `ani_ii_delivery_note` carries this in typed form.

## Why phreaks cared

Two reasons:

1. **Enumeration.** An early-90s PC-based scanner sitting on an 800
   line logged the II byte for every inbound call — building a map of
   which lines in the wild were payphones, hotels, cellular, etc. This
   is where "how do you tell it's a COCOT vs. a Bell payphone from a
   distance" became a *tractable* question.
2. **Bypass tests.** A caller who could inject their own II bits at the
   right point in an FGD MF spill could impersonate a class — most
   famously, faking `20` (AIOD) to get billing routed to a specific
   listed DN, or `00` to hide that a call was from a payphone.

## Sources

- Bellcore GR-317-CORE (FGD signaling)
- Bellcore SR-TSV-002275 (BOC Notes on LATA Switching Systems)
- NANPA "ANI II Digits Assignments" letter (living document at
  nationalnanpa.com/number_resource_info/ani_ii_assignments.html)

## See also

- [[operator-services/README]] — the wider operator + test surface.
- [[redboxing/README]] — code 27 is the class of the phones this
  targets.
- [[cna/README]] — CN/A depended on the calling-number spill; ANI-II
  is the *class* delivered alongside that number.
