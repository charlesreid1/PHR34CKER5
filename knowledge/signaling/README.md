# Signaling systems

The wire-level protocols that carried "who's calling whom, is the line
idle, has the far party answered." This directory orients across the
family; the typed records in
[`records/signaling_systems.json`](../records/signaling_systems.json)
carry the exact frequencies, timings, and standards citations.

Everything below is a *system* — the tones in `records/tones.json` are
the alphabet, and these records are the grammar.

## The taxonomy that matters

A phreaking claim always lives at the intersection of three axes:

| Axis | Values |
|---|---|
| Region | NANP, ITU-R2, CCITT-No5, AUTOVON, universal |
| Layer | subscriber_loop, co_to_co_inband_trunk, co_to_co_outofband_trunk, co_to_co_digital_trunk, co_to_co_inband_trunk_international, subscriber_loop_concentrator, operator_platform |
| Era | 1954-2005 (roughly) |

*Cross-layer confusion is the #1 source of DEFCON-trap wrongness.* A
2600 Hz whistle attacks `sig_sf` at the `co_to_co_inband_trunk` layer;
it does nothing at `subscriber_loop`. AUTOVON precedence keys work at
`subscriber_loop` on `AUTOVON`-region switches; they mean nothing on a
civilian NANP switch. `search_records category=signaling_system
region=NANP year=1998` gives you the systems live on that intersection.

## The families

### Subscriber-loop layer (customer to CO)

- **Loop-start** (`sig_loop_start`) — the default POTS supervision.
  DC loop closure = off-hook. Still effective 2026.
- **Ground-start** (`sig_ground_start`) — reduces glare on PBX trunks;
  one side grounds tip, the other grounds ring.
- **Reverse-battery** (`sig_reverse_battery`) — answer supervision
  signal from far CO. The black-box attack surface.
- **DTMF** (`sig_dtmf`) — Q.23 touch-tone. 697/770/852/941 × 1209/1336/1477/1633.
- **AUTOVON** (`sig_autovon`) — DTMF plus the 1633 Hz column keys for
  precedence preemption on military switches.

### Inter-office trunk, in-band (SF/MF family)

- **SF supervision** (`sig_sf`) — 2600 Hz single-frequency, NANP.
  Trunk-idle / seizure signal. The layer classic blue boxing attacks.
- **MF R1** (`sig_mf_r1`) — 700/900/1100/1300/1500/1700 Hz two-of-six.
  Address signaling that follows SF seizure. KP + digits + ST.
- **CCITT No.5** (`sig_ccitt5`) — international MF. Line signaling on
  **2400 + 2600 Hz** (seizure = 2400, proceed-to-send = 2600). A blue
  box that emits only 2600 Hz does NOT seize a No.5 trunk.
- **MF R2 / MFC** (`sig_r2`) — LATAM/Iberia/parts of Asia. Different
  frequencies (1140–1980 forward, 540–1140 backward), compelled
  signaling, group-dependent semantics.
- **E&M types I-V** (`sig_em_trunk`) — DC-signaled trunk interfaces
  between colocated switches.
- **ANI wink-start / spill** (`sig_ani_wink_spill`) — FGD in-band ANI
  delivery: `KP + II + KP + ANI + ST`.

### Inter-office trunk, out-of-band

- **CCIS / No.6** (`sig_ccis_no6`) — the change that killed classical
  blue boxing. Signaling moved off the voice band.
- **SS7 / No.7** (`sig_ss7_no7`) — the successor. Modern SS7 attacks
  (SCCP/TCAP/MAP abuse) are a separate, post-era research topic.

### Digital trunk

- **T-1 robbed-bit / CAS** (`sig_t1_cas`) — the reason 56 k modems.
  Steals the LSB of every 6th frame for A/B/C/D supervision bits.
- **SLC-96 / SLC-2000** (`sig_slc96`) — the green sidewalk cabinet.
  Concentrator between the subscriber loop and the CO switch. Changes
  which layer your local loop actually talks to.

## Why phreaks needed the systems abstraction

Because a claim like "blueboxing works" is meaningless without the
system. It works against **SF supervision on inter-office trunks
carrying MF R1**, in **NANP**, from **~1954 through mostly 1990**. It
never worked at the subscriber-loop layer. It never worked on out-of-
band signaling. Once you have systems as first-class records, you can
ask `explain_technique blueboxing region=NANP year=1998` and get an
answer that qualifies "still worked on some independents; long dead on
AT&T Long Lines."

## See also

- [[records/README]] — the typed KR contract.
- [[blueboxing/README]] — SF + MF R1 in prose.
- [[2600hz/README]] — the SF carrier tone specifically.
- [[dtmf/README]] — the subscriber-loop touch-tone side.
- [[numbering/README]] — the NANP dial plan that runs on top of MF R1.
