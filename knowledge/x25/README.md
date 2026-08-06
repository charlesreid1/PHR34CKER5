# X.25 — public packet-switched data networks

The pre-Internet corporate remote-access backbone. Between roughly 1976
and 2004 the way you reached "someone else's computer" from your
computer was: dial your local packet PAD, get an `@` (Sprintnet) or a
`please log in:` (Tymnet), then `C <NUA>` to a host somewhere on the
planet. Every phreak-relevant scan of the era eventually walked an X.25
NUA space.

Full DNIC (Data Network Identification Code) records live in the typed
records at [`records/data_networks.json`](../records/data_networks.json).
Query with `search_records category=data_network`.

## The addressing

An NUA (Network User Address) is a **14-digit** address:

```
DNIC (4)  +  NTN (up to 10)
```

The DNIC is assigned per CCITT X.121. Its first digit is the world
"zone" (2 = Europe, 3 = North America, 4 = Asia + Oceania, 5 = Asia +
Oceania, 6 = Africa, 7 = South America). The next three identify the
network. Examples the corpus has records for:

- **3020** Datapac (Canada)
- **3106** Tymnet (US)
- **3110** Sprintnet / Telenet (US)
- **3125** AT&T Accunet Packet
- **3126** FedEx Zapmail *(defunct 1986; DNIC lingered in ITU tables)*
- **2342** BT PSS (UK)
- **2624** Datex-P (Germany)
- **2080** Transpac (France — Minitel's spine)
- **4400** NTT DDX-P (Japan)
- **5052** Austpac (Australia)
- **7220** Interdata (Brazil)
- **7241** RENPAC (Argentina)

## The dial-in surface

- **Sprintnet:** 1-800-546-1000 (voice-band), 1-800-877-5045 (v.32bis).
  Post-CONNECT: `<CR><CR>` → `@` prompt. `TERM=D1` = VT100. `C <NUA>`
  to connect. Local address format: `AAAB-CCC` where AAA = area code,
  B = 0-9 area suffix, CCC = host index.
- **Tymnet:** 1-800-937-2862, 1-800-336-0149. Post-CONNECT: send a
  single lowercase `a` (no CR) to trigger the banner, followed by
  `please log in:` — respond with the NUI.
- **CompuServe Packet Network:** 1-800-848-4480. Post-CONNECT prompt:
  `User ID:`.

## What the fingerprints told you (from the war-dial layer)

Different login banners on a scanned modem line said different things:

- `Enter your NUI:` → Tymnet
- `@` prompt bare → Sprintnet PAD
- `Enter Terminal Type:` → likely HP3000 MPE/iX
- `Username:` then `Password:` (both capitalized) → DEC VAX/VMS
- Blank line then `HELLO,` → HP3000 MPE

More in [`war-dialing/toneloc-tuning.md`](../war-dialing/toneloc-tuning.md).

## The scanning game

X.25 NUAs were dense. Scanners like **Ranger** and **Scan-o-matic**
walked entire area-code / DNIC ranges via PAD-to-PAD `C <NUA>`
commands, logging which responded with what banner. Successful hits
included:

- DEC VAX/VMS clusters (universities, gov)
- IBM VM/CMS, MVS/TSO
- TOPS-20 (rare by mid-90s)
- HP3000 MPE/iX
- SunOS / BSD Unix mail servers
- Specialty PICK OS (INFORMATION, Ultimate)

## Why it died

Frame relay (mid-90s) and IP dial-up (SLIP/PPP, then always-on
broadband) supplanted X.25 for corporate remote access. Most public
PADs were decommissioned 2001-2004. Transpac hung on until **2011-06-30**
(the last big public X.25 to shut down in Europe).

## Sources

- CCITT Recommendation X.121 (international numbering plan for public
  data networks; 1980, revised in the 1988 Blue Book and 1996).
- Phrack 18 File 3 "An Introduction to Packet Switched Networks"
  (Epsilon); Phrack 27 File 4 "NUA List for Datex-P and X.25 Networks"
  (Oberdaemon); Phrack 35 File 4 (Sprintnet PC Pursuit); Phrack 40
  Files 8-10 (BT Tymnet, Toucan Jones); Phrack 42 Files 8-10
  (Sprintnet Directory, Skylar).

## See also

- [[war-dialing/toneloc-tuning]] — banner fingerprints for scanned
  modem lines.
- [[bbs/README]] — X.25 outdials were how BBSes reached long-distance
  callers pre-Internet.
