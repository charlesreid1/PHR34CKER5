# Cellular — AMPS through early GSM/CDMA

The wireless era that overlapped with classic phreaking. Between roughly
1983 and 2008 (US), the phone in someone's pocket was interesting because
its identity was on the air *in the clear* — and its keypad hid a
service menu that could reprogram it.

Typed records live in [`records/cellular.json`](../records/cellular.json)
under two categories:

- `cellular_system` — the technology itself (AMPS, GSM, CDPD, FLEX/POCSAG
  pagers)
- `handset_service_menu` — the actual key sequences to enter test/NAM
  mode on specific handset families

## AMPS — the reason phreaks cared

**AMPS** (Advanced Mobile Phone System) was analog cellular on 850 MHz.
On every registration and origination, the handset broadcast its
identity — **MIN + ESN, in the clear** — on the RECC (Reverse Control
Channel) at 10 kbps Manchester-encoded. Anyone with a scanner and a
decoder box could log every phone that registered in a cell.

- **MIN** = Mobile ID Number (34 bits, derived from the 10-digit MDN).
- **ESN** = Electronic Serial Number (32 bits, meant to be immutable).

Cloning: reprogram MIN/ESN into a second handset via **NAM** (Number
Assignment Module) programming mode. Every AMPS phone had one; the
entry sequence varied by manufacturer. The corpus has records for
Motorola (MicroTAC, StarTAC, bag phones), OKI (the 900/1150 was the
scanner platform of choice), Nokia, Ericsson, Qualcomm, Audiovox, Sony.

Cloning died as **A-Key authentication** rolled out on IS-54B / IS-136
TDMA (1996-1998), and legally died with the FCC-authorized **AMPS
sunset on 2008-02-18**.

## GSM — the second-generation surface

GSM in North America landed on PCS 1900 MHz starting 1996. Identity
moved onto the **SIM** (IMSI + Ki-128), authenticated by A3/A8
(commonly **COMP128-1**, broken by Wagner/Goldberg/Briceno in 1998).
Encryption over the air was **A5/1** (Western Europe, US) and
**A5/2** (weakened export).

A common DEFCON-style claim trap: "A5/1 was practically broken by
2003." No. Practical rainbow-table attacks (Karsten Nohl et al.)
landed **2008-2010**. Pre-2004 A5/1 required precomputation few had.

## CDPD — packet data over unused AMPS channels

**CDPD** (Cellular Digital Packet Data) put 19.2 kbps IP over unused
AMPS voice channels via channel-hopping. Used by PocketNet, early
wireless credit-card readers, dispatch data, Palm VII on OmniSky.
Encrypted with **RC4** from a shared secret; MDBS spoofing attacks
were documented.

## Pagers — POCSAG and FLEX

Two-way paging on the 900 MHz band. Both **POCSAG** (512/1200/2400
bps FSK) and **FLEX** (1600-6400 bps, 4-level FSK) broadcast
messages **unencrypted**. A phreak in the mid-90s with an ICOM
PCR-1000 (or a Radio Shack Pro-2006) plus **PDW** or **POC32** on a
PC could passively log tens of thousands of messages per day in a
metro.

Traffic that went out unencrypted for a decade:
- Hospital pages (with patient info)
- On-call SRE / NOC alerts with server hostnames and sometimes
  credentials
- Bank alarm-panel notifications
- White House Communications Agency (WHCA) traffic (published in the
  2009 WikiLeaks 9/11 pager release)

## Handset service menus

Every entry has the exact key sequence + what it exposes. The classics:

- **Motorola MicroTAC / StarTAC (AMPS):** `FCN + 0 0 * * 8 3 7 8 6 6 + STO`
  (the digits spell TEST-MOTO on a keypad)
- **OKI 900 / 1150:** `# 6 2 3 8 8 8` — the platform of choice for
  building AMPS scanners with custom firmware
- **Nokia 100/232/636 (AMPS):** `Menu 3-1-4-1-4-1 Menu`
- **Nokia 51xx/61xx (GSM/TDMA):** `*#3001#12345#`, plus `*#06#` for IMEI
- **Ericsson 788:** `> * < < * < *` on the joystick
- **Qualcomm QCP-800/860:** `Fcn 0`, then `111111` at the NAM prompt

**Legal note.** Entering a phone's test mode without ownership was an
18 USC 1029 issue even in the 90s. These records are historical
education, not an operational recipe.

## Sources

- EIA/TIA IS-553 (AMPS spec)
- Phrack 38.9, 40.6 "Cellular Telephony" (Brian Oblivion) — foundational
- Phrack 45.26 "Cellular Debug Mode Commands" — canonical NAM-sequences
  catalog
- Phrack 48.6-48.7 (Motorola, Tandy/Radio Shack)
- Phrack 46.8 "The Wonderful World of Pagers" (Erik Bloodaxe)

## See also

- [[modems/README]] — the wired-modem side of the same era
- [[records/README]] — the typed KR
