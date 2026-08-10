# Defense + detection

The Bell/Telcordia side of the arms race. What the network *knew* about
what you were doing, and how.

Typed records under
[`records/defense_and_detection.json`](../records/defense_and_detection.json).
Ten load-bearing entries covering billing, alarms, OSS, trace, and the
modern SS7-analytics layer.

## The billing layer

- **AMA (Automatic Message Accounting)** — the per-call record every
  originating CO writes. This is what blue-boxing and tandem-stacking
  tried to *misalign*.
- **CAMA (Centralized AMA)** — the pre-SPC variant. Small offices sent
  raw call data to a central accounting office. CAMA trunks were
  vulnerable to ANI spoofing.

## The alarm layer

- **AT&T Greenstar / Blueflag** — the toll-fraud detection program
  that logged suspicious 2600 Hz hold-time patterns on 1AESS/4ESS from
  the 1970s onward.
- **2600 Hz hold-time alarm** — the specific alarm shipped in 1AESS
  generic 1AE7+ and 4ESS. Threshold ~400 ms. This is why phreaks
  favored shorter, sharper 2600 bursts by the 1980s.
- **MCT (Malicious Call Trace)** — subscriber-callable via *57; on
  Meridian, LD 51. Defenders enable this on likely-abused DNs.
- **5ESS RCV TRACE** — live-callable call-trace command from the 5ESS
  craft interface. Every 5ESS you're touching can log your session in
  real time.

## The OSS layer

- **LMOS (Loop Maintenance Operations System)** — Bell's trouble-ticket
  system. Also a dial-up-accessible target itself.
- **COSMOS (COmputer System for Mainframe OperationS)** — frame /
  cross-connect / LEN-to-DN mapping. Access to COSMOS = access to
  physical wire assignments.
- **MIZAR** — SPC-switch translation-download tool. Access = live
  translation changes on 1ESS/1AESS.
- **REMOBS (Remote Observation System)** — Bell's remote line-monitor
  capability. The mythical wiretap that was closer to real than most
  conspiracy theories credited.

## The modern layer

- **SS7-era call-completion pattern analytics** — real-time fraud
  detection that ingests SS7 signaling records and CDR streams. A
  DISA-abused PBX making sudden long-duration international calls
  gets flagged within minutes on well-monitored networks.

## Why it matters for CTFs

A CTF puzzle set in the era can hide flags in what the *defensive*
infrastructure recorded: an AMA record, a Greenstar log, an LMOS
ticket. Understanding what defenses existed at each era is half the
job of recognizing what a puzzle is actually asking.

## Sources

- BSTJ Nov 1960 (AMA on magnetic tape)
- Phrack 9.9 (LMOS), 14.4 (REMOBS), 26.5 / 27.5 / 31.6 (COSMOS)
- Phrack 51.15 (Narbo, CCS7 intro — post-era)
- Bell Labs Record trunk-signaling articles 1970-1985 (greenstar
  reference in situ)

## See also

- [[signaling/README]] — the systems these defenses monitored
- [[ess/reference]] — which alarms shipped in which switch generation
- [[pbx/README]] — LD 51 MCT on Meridian, the enterprise equivalent
