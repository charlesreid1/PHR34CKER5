# ESS — trunk signaling reference

Per-generation trunk signaling. What each Bell/Nortel switch family
*spoke* on its outbound trunks — and therefore, what a phreaker could
attack.

## Quick lookup

| Switch | Deploy | Trunk in-band | Trunk out-of-band | Notes |
|---|---|---|---|---|
| 1ESS | 1965 | SF + MF R1 | none (v1.x) → CCIS 6 (later 1AE loads) | Reed-relay fabric. Phrack-classic. |
| 1AESS | 1976 | SF + MF R1 | CCIS 6, later SS7 | 1AE7+ generic added 2600-hold-time alarms. |
| 2ESS | 1970 | SF + MF R1 | rare CCIS 6 | Small/suburban office. |
| 3ESS | 1976 | SF + MF R1 | rare | Very small offices. |
| 4ESS | 1976 | MF R1 (toll addressing) | **CCIS 6 native, then SS7** | The toll switch. First widespread out-of-band deployment; the switch that killed classical blueboxing on major routes. |
| 5ESS | 1982 | E&M / MF R1 as gateway | **SS7 native** | Fully digital, fully out-of-band from day one on interoffice. Local subscriber loops still loop-start. |
| DMS-10 | 1979 | E&M / MF R1 | SS7 (later loads) | Small-office DMS. |
| DMS-100 | 1979 | E&M / MF R1 as gateway | **SS7 native** by mid-80s | Canadian answer to 5ESS; widely used in US. |
| DMS-200 | 1979 | R1 (toll addressing) | SS7 native | Toll/access-tandem variant. |
| DMS-250 | 1983 | R1 as gateway | SS7 native | IXC toll switch — Sprint's backbone. |
| EWSD (Siemens) | 1981 | MF R1 (US) / R2 (int'l) | CCS7 / SS7 | Used by GTE/Sprint. German-origin, R2-capable. |
| GTD-5 EAX (AGCS) | 1982 | SF + MF R1 (long-lived) | later SS7 | GTE local switch. Kept SF/MF interoperability longer than Bell offices — a phreak-relevant quirk. |

Every entry in the table maps to a typed record in
[`records/network_elements.json`](../records/network_elements.json) or
to a signaling-system record in
[`records/signaling_systems.json`](../records/signaling_systems.json).
Fields: `signaling_system` → `region`, `era_bounds`,
`retirement_cause`.

## The transitions that mattered

- **CCIS deployment (1976-early 80s):** 4ESS on AT&T Long Lines first,
  then 1AESS locals. Once a route was CCIS, in-band supervision was
  gone — 2600 Hz became just audio on that trunk.
- **SS7 rollout (1980-1992):** the CCIS successor. ANSI SS7
  standardized 1988; ubiquitous on North American interoffice trunks
  by ~1992.
- **Independents lag:** GTE (later Verizon) and small independent
  telcos ran SF/MF trunks in-band into the mid-1990s. GTD-5 EAX
  specifically kept the SF/MF interworking longer than Bell.

## What a phreaker on a fortress phone actually saw

The fortress payphone talked to whatever local Class-5 switch owned
its POTS loop — usually 1ESS/1AESS/5ESS in Bell territory, DMS-100 in
Nortel territory, GTD-5 in GTE. Coin signaling (ACTS 1700+2200 Hz)
went to the local switch's coin-signal receiver, which was in-band up
the toll trunk to the 4ESS/DMS-200. Once T-1 with robbed-bit CAS
replaced analog toll trunks (mid-90s onward), the in-band ACTS path
disappeared — one of the reasons red-boxing died even before smart
payphones took over.

## See also

- [[ess/audible-tells]] — how to *hear* which switch you're on
- [[ess/no-4-ess]] — the toll switch specifically
- [[signaling/README]] — the systems taxonomy
- [[blueboxing/seizure-walkthrough]] — the attack that runs on top

## Sources

- BSTJ "No. 1 ESS" (Sept 1964)
- BSTJ "No. 4 ESS" (1977)
- Bell Labs Record, various 1970-1985
- Phrack 5.5 (Knight Lightning, DMS-100)
- Phrack 25.3 (Taran King, Bell Network Switching Systems)
- Phrack 43.16 (Firm G.R.A.S.P., Guide to the 5ESS)
- Notes on the History of the Bell System, AT&T archives
