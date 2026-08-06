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
  R1 MF digit table lives in `blueboxing/mf-tones.md`
- **redboxing/**   — coin-return simulation, ACTS, quarter/dime/nickel tones
- **greenboxing/** — coin collect/return operator tones
- **cna/**          — Customer Name and Address bureaus, social engineering
- **2600hz/**       — the whistle, Cap'n Crunch, in-band signaling history
- **dtmf/**         — the touch-tone grid, AUTOVON A/B/C/D, twist, misconceptions
- **modems/**       — carrier handshakes (Bell 103 → V.34), the 2100 Hz answer tone
- **bbs/**          — bulletin board systems, 300/1200/2400 baud culture
- **war-dialing/**  — ToneLoc, THC-Scan, scanning number ranges
- **ess/**          — Electronic Switching Systems (1ESS → 5ESS), CCIS/SS7
- **tandem-stacking/** — chaining tandems, international routing tricks
- **zines/**        — 2600 Magazine, Phrack, TAP — pointers and history
- **glossary/**     — jargon, acronyms, org names (Ma Bell, CN/A, RBOC…)
- **fax/**          — T.30 handshake, CNG/CED, Group 3, fax war dialing
- **ctf/**          — CTF-facing puzzle genres (IVR mazes, DISA, voicemail,
  modem carriers, fax flags, conference bridges, ANAC/CN·A, milliwatt lines)
  and how to probe each with the MCP tools

## Conventions

- One idea per file. Keep files short and cite sources at the bottom.
- Filename slug is lowercase-with-dashes and becomes the resource name.
- Prefer plain markdown. ASCII art welcome. Do not embed binaries.
- Historical framing only — this corpus documents the era, it does not
  instruct anyone to commit toll fraud on a modern network.
