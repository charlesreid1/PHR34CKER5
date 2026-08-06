# WAR DIALING

Named after the 1983 film *WarGames*. A war dialer sweeps a range of phone
numbers, logging which ones answer with a modem carrier, a fax, a voice
prompt, or a dial tone.

## The classics
- **ToneLoc** (Minor Threat & Mucho Maas, 1994) — DOS, screen-based grid of
  numbers, iconic UI. Named for the rapper Tone Loc.
- **THC-Scan** (van Hauser / THC, 1996) — DOS, more configurable, better
  carrier detection.
- **PhoneSweep** (Sandstorm, late 1990s) — commercial, for auditors.
- **WarVOX** (H. D. Moore, 2009) — VoIP-era rewrite; classified *audio*
  rather than just carriers.

## What you found
- **CARRIER** — a modem. Sometimes a router console, sometimes a mainframe
  dial-in, sometimes just another BBS.
- **VMB** — a voice-mail system. Sometimes hackable.
- **DIALTONE** — a PBX with an outdial. Enter magic digits, get a fresh
  dial tone to place your own calls.
- **RINGOUT / TIMEOUT** — noise.

## Modern relevance
Between mobile numbers, VoIP, and the near-total elimination of dial-in
modems on production infra, war dialing is now a niche audit activity — but
it still finds things: legacy alarm panels, fax servers, HVAC controllers.

## Fingerprinting what you found

Once a scanner hit answers with a CARRIER, the *banner* it produces
tells you what system it is. Typed records for every classic
fingerprint live in
[`records/fingerprints.json`](../records/fingerprints.json) —
category `system_fingerprint`.

Quick reference (see the records for full detail + login next-steps):

- `Welcome to the ROLM PhoneMail system` → Rolm voicemail
- `Username:` then `Password:` (both capital-first) → DEC VAX/VMS
- `login:` lowercase + `login: incorrect` on retry → SunOS/BSD
- Blank blob then `HELLO,` → HP3000 MPE/iX
- `HP-UX <ver> login:` → HP 9000 running HP-UX
- `IBM AIX Version` → RS/6000
- `[Ctrl-C to abort, Enter to continue]` → SL-1 SDI craft port
- `NT-1 MSDL v2.0` → Nortel MSDL card
- `CI:` → Nortel DMS MAPCI
- Bare `<` prompt → AT&T 5ESS RCV
- `TOPS-20 Monitor` → DEC-20 (rare by mid-90s)
- `Enter class:` → PICK OS variant
- Bare `%` prompt → GTE Telemail (early era)
- `Enter your NUI:` → Tymnet PAD
- Bare `@` after `<CR><CR>` → Sprintnet PAD

## See also
- [[bbs/README]]
- [[ess/README]]
- [[x25/README]] — the PADs behind Sprintnet/Tymnet fingerprints
- [[pbx/README]] — post-login next-steps for SL-1 / DMS / 5ESS hits
