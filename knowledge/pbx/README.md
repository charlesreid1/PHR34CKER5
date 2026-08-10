# PBX + voicemail

Corporate PBXs — and the voicemail systems bolted onto them — were the
most-abused non-payphone target of the 1990s. Two attack shapes:

1. **Signaling / config abuse.** Get admin access to the PBX's craft
   interface, add a permissive DISA authorization code + FRL-0 route,
   and turn the box into a personal international dial-out. Estimated
   at ~$4B/yr in fraud losses (ITU, 1996).
2. **Voicemail abuse.** Compromise the system administrator's mailbox,
   record system prompts, enable outcall notification with a target
   number = free calling card. Or brute-force user mailboxes with
   default passwords = mailbox number.

## Nortel SL-1 / Meridian 1 / CS1000

The [`records/network_elements.json`](../records/network_elements.json)
entry `netel_sl1` carries the system-level metadata (access channels,
default admin logins, OS lineage). The full LD (overlay) table lives in
[`records/pbx_overlays.json`](../records/pbx_overlays.json) — ~65
records covering LD 02 through LD 143.

**The six load-bearing overlays for DISA abuse:**

| LD | Purpose | Why it matters |
|---|---|---|
| 22 | Package inventory | Confirm DISA (26) enabled and MCT (107) *not* running |
| 15 | Customer data | Enable DISA + set the DISA DN + auth-code length |
| 88 | Auth codes | Add your own code (`NEW` → `CODE` → `COS` → `NCOS`) |
| 70 | CoS / NCOS | Point your NCOS at an FRL-0 route |
| 91 | FRL tables | Verify FRL 0 (no restriction) on the target routes |
| 16 | Route data | Ensure a liberal outbound route to your target country exists |
| 40 | CDR | Turn off / redirect call-detail recording before you use it |

Full end-to-end recipe in the `technique_meridian_disa_abuse` record.

## Voicemail defaults

Every one of these was documented in vendor manuals; publishing them is
a historical/educational act, not a live-attack manual.

- **Meridian Mail**: system admin mailbox `0` or `999999`, password
  `0000` or the mailbox number.
- **Octel Overture**: system-manager mailbox `9999`, password `9999`.
- **AT&T Audix / Lucent Intuity**: admin `9999` or `0`, password
  `12345` (older) or the mailbox number.
- **Rolm PhoneMail**: mailbox `0` / password `1234`, mailbox `88` /
  password `8756`.
- **Panasonic KX-TVS / KX-TD**: system password `1234`, admin mailbox
  `998`.
- **Toshiba Stratagy**: sysadmin mailbox `983`, password `983`.

Full records in [`records/pbx_overlays.json`](../records/pbx_overlays.json)
(category `pbx_and_voicemail`, subclass `voicemail`).

## Access channels — where the modem is

The phreak-relevant entry point is almost always a **maintenance modem
on the PBX's serial port** (SDI on old SL-1, MSDL on Meridian, USB/IP
on CS1000+). Typical rates: 300, 1200, 2400, sometimes 9600 bps. The
modem is often on:

- An unpublished DID within the corporate range (war-dialing finds it).
- A dedicated POTS line tucked in a wire closet ("vendor maintenance
  line") — sometimes on a completely different NPA/NXX than the main
  corporate range.
- (Post-2005) An SSH port at the CS1000 PDT (Problem Determination
  Tool). Out of era.

## The pattern that survived

Even in 2026, an abandoned Meridian 1 with default admin credentials
and DISA enabled is a working DISA gateway. What killed the *class* of
attack in the mainstream was:

1. Enterprise IT enforcing password rotation on the PBX SDI port.
2. CDR feeding into automated fraud-detection at the LEC.
3. Migration off TDM PBXs entirely (IP-PBX, hosted VoIP).

## Sources

- Nortel NTP 553-3001-311 (X11 Input/Output Reference).
- Nortel NTP 553-3001-365 (Features and Services).
- Phrack 40 File 6 "The Nortel SL-1 Overview" (community).
- Phrack 44 File 19 "Northern Telecom's SL-1" (Iceman).
- Phrack 47 File 15 "Complete Guide to Hacking Meridian Voice Mail"
  (Substance).
- 2600 Autumn 1997 "Inside a Meridian".

## See also

- [[operator-services/README]] — the operator surface behind DISA and
  attendant transfers.
- [[war-dialing/toneloc-tuning]] — how the maintenance modem gets
  found in the first place.
- [[records/README]] — the typed KR.
