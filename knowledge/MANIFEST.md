# PHR34CKER5 CORPUS — MANIFEST

```
          _____                    _____                    _____                    _____                    _____                    _____
         /\    \                  /\    \                  /\    \                  /\    \                  /\    \                  /\    \
        /::\    \                /::\____\                /::\    \                /::\    \                /::\    \                /::\____\
       /::::\    \              /:::/    /               /::::\    \              /::::\    \              /::::\    \              /:::/    /
      /::::::\    \            /:::/    /               /::::::\    \            /::::::\    \            /::::::\    \            /:::/    /
     /:::/\:::\    \          /:::/    /               /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/    /
    /:::/__\:::\    \        /:::/____/               /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \        /:::/____/
   /::::\   \:::\    \      /::::\    \              /::::\   \:::\    \      /::::\   \:::\    \      /::::\   \:::\    \      /::::\    \
  /::::::\   \:::\    \    /::::::\    \   _____    /::::::\   \:::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \    /::::::\____\________
 /:::/\:::\   \:::\____\  /:::/\:::\    \ /\    \  /:::/\:::\   \:::\____\  /:::/\:::\   \:::\    \  /:::/\:::\   \:::\    \  /:::/\:::::::::::\    \
/:::/  \:::\   \:::|    |/:::/  \:::\    /::\____\/:::/  \:::\   \:::|    |/:::/__\:::\   \:::\____\/:::/  \:::\   \:::\____\/:::/  |:::::::::::\____\
\::/    \:::\  /:::|____|\::/    \:::\  /:::/    /\::/   |::::\  /:::|____|\:::\   \:::\   \::/    /\::/    \:::\  /:::/    /\::/   |::|~~~|~~~~~
 \/_____/\:::\/:::/    /  \/____/ \:::\/:::/    /  \/____|:::::\/:::/    /  \:::\   \:::\   \/____/  \/____/ \:::\/:::/    /  \/____|::|   |
          \::::::/    /            \::::::/    /         |:::::::::/    /    \:::\   \:::\    \               \::::::/    /         |::|   |
           \::::/    /              \::::/    /          |::|\::::/    /      \:::\   \:::\____\               \::::/    /          |::|   |
            \::/____/               /:::/    /           |::| \::/____/        \:::\   \::/    /               /:::/    /           |::|   |
             ~~                    /:::/    /            |::|  ~|               \:::\   \/____/               /:::/    /            |::|   |
                                  /:::/    /             |::|   |                \:::\    \                  /:::/    /             |::|   |
                                 /:::/    /              \::|   |                 \:::\____\                /:::/    /              \::|   |
                                 \::/    /                \:|   |                  \::/    /                \::/    /                \:|   |
                                  \/____/                  \|___|                   \/____/                  \/____/                  \|___|
```

This directory is the **reference half** of PHR34CKER5 — the reservoir of
phreaking knowledge that the assistant consults to advise. The **acting
half** lives in [`src/`](../src/): the MCP tools that synthesize tones,
place live PSTN calls, and record. The corpus tells you *what a thing is*
and *what it sounded like*; the tools *do it*. A good CTF answer usually
draws on both — look up the tone here, then generate and inject it from
`src/`.

Every `.md` file below is exposed as an MCP resource under
`phr34cker5://<topic>/<name>` and is searchable via the `search_lore` tool.

Add files freely. The server picks them up on next startup.

The prose here is the half you *read*. Alongside it, [`records/`](records/)
is a typed, dated, cited knowledge repository — the half you *look facts up
in* (exact frequencies, timings, disputes). The retrieval tools
(`lookup_tone`, `verify_claim`, `explain_technique`, `bibliography`,
`cross_reference`, `search_records`) bind to those JSON records, not to free
text. See [`records/README.md`](records/README.md).

## Topics

- **blueboxing/**   — 2600 Hz, MF signaling, KP/ST, trunk seizure; the full
  R1 MF digit table (`mf-tones.md`) + a time-annotated `seizure-walkthrough.md`
- **redboxing/**   — coin-return simulation, ACTS, quarter/dime/nickel tones;
  `acts-timing.md` (the GR-506 vs Phrack 33.9 dispute) + a `walkthrough.md`
- **greenboxing/** — coin collect/return operator tones
- **cna/**          — Customer Name and Address bureaus; `pretext-scripts.md`
  reconstructs the social-engineering dialogue (historical illustration)
- **2600hz/**       — the whistle, Cap'n Crunch, in-band signaling history;
  `whistle-tolerances.md` on the SF detector
- **dtmf/**         — the touch-tone grid, AUTOVON A/B/C/D, twist, misconceptions
- **modems/**       — carrier handshakes (Bell 103 → V.34), the 2100 Hz answer tone
- **operator-services/** — 0/00/611/411/950 dialing, TSPS/TOPS/OSPS, ANAC,
  milliwatt, ringback, loop-arounds
- **bbs/**          — bulletin board systems, 300/1200/2400 baud culture
- **war-dialing/**  — ToneLoc, THC-Scan, scanning; `toneloc-tuning.md` on the
  classifier and banner fingerprints
- **ess/**          — Electronic Switching Systems (1ESS → 5ESS), CCIS/SS7;
  `audible-tells.md` (identify a switch by ear) + `no-4-ess.md` (the toll switch)
- **tandem-stacking/** — chaining tandems; `international.md` (C5, overseas loops)
- **zines/**        — 2600 Magazine, Phrack, TAP — pointers and history
- **glossary/**     — jargon, acronyms, org names (Ma Bell, CN/A, RBOC…)
- **fax/**          — T.30 handshake, CNG/CED, Group 3, fax war dialing
- **ctf/**          — CTF-facing puzzle genres (IVR mazes, DISA, voicemail,
  modem carriers, fax flags, conference bridges, ANAC/CN·A, milliwatt lines)
  and how to probe each with the MCP tools
- **numbering/**    — NANP structure, N11 codes, dialing plans, ANI-II info
  digits (100-code table lives in `records/operator_service_codes.json`)
- **x25/**          — public packet-switched data networks, DNICs, PADs, and
  scanning; DNIC records live in `records/data_networks.json`
- **pbx/**          — corporate PBX + voicemail; the SL-1 / Meridian LD
  overlay table + voicemail defaults live in `records/pbx_overlays.json`
  and `records/network_elements.json`
- **cellular/**     — AMPS, GSM, CDPD, POCSAG/FLEX paging; the handset NAM
  key sequences live in `records/cellular.json`

## Conventions

- One idea per file. Keep files short and cite sources at the bottom.
- Filename slug is lowercase-with-dashes and becomes the resource name.
- Prefer plain markdown. ASCII art welcome. Do not embed binaries.
- Historical framing only — this corpus documents the era, it does not
  instruct anyone to commit toll fraud on a modern network.
