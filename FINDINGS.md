# PhreakMe CTF — Findings

**Player:** `ch4zm` (user 145, team 51)
**Target IVR:** `+1 (219) 500-2600`
**CTFd:** https://phreakme.com
**From-number:** `+19289778173` (Twilio, on account `AC_REDACTED`)

## Score

| # | Category | Challenge | Points | Status | Loot |
|---|---|---|---|---|---|
| 74 | Redbox | Call - 212-555-1337 | 100 | ✅ SOLVED | [loot/74-redbox-212-radio-shack.md](loot/74-redbox-212-radio-shack.md) |
| 76 | Trivia | Trivia - Ext 1101 | 10 | ❌ BLOCKED (see [flag-ollama-bell.md](flag-ollama-bell.md)) | — |
| 75 | Redbox | Call - 514-555-1337 | 100 | 🚧 in progress (Montreal, `veuillez déposer vingt-cinq sous`) | — |

**Total: 100 pts**

## ⚠️ BLOCKER: Twilio account on compliance hold

As of 2026-08-08, subsequent outbound calls fail with:

```
HTTP 401 code 20003
"Primary compliance profile is not approved. Please refer to
 documentation and complete the KYC process in Trust Hub to gain access."
```

The 100-pt Radio Shack solve landed just before the hold kicked in. To
unblock:

1. Log into https://console.twilio.com
2. Trust Hub → complete the Primary Compliance Profile
3. Wait for approval (usually minutes; can be hours)
4. Resume dialing

## Infrastructure

### 1. Main IVR (dial `+12195002600`)

```
Welcome to PhreakMe. Abandon all hope ye who dial here.
  1 → Trivia section
  2 → Red box challenges (opens PBX extension prompt)
  3 → Blue box challenges (PBX)
  4 → PhreakTel voicemail system (Nexus Data Solutions)
  5 → Voice BBS
  6 → Multitap Mania
  7 → PhreakTel calling card service
```

### 2. PBX (after pressing `2` or `3`)

- "If you know the extension of the party you wish, dial it now."
- Extension numbers are the challenge target numbers (dial with area code and 7-digit number, no `+1`).
- Example: `2125551337`, `5145551337`, `7135552600` (Erik Bloodaxe, blue-box #71).
- Non-payment on redbox challenges gets you dumped back to the main menu.

### 3. Trivia extensions (menu 1)

- Trivia challenges are named `Trivia - Ext 1101` through `Trivia - Ext 1130` in CTFd (30 total).
- Menu 1 → 1 starts Q1 (Ext 1101). Pressing digits during the question answers.
- Ext 1101: "In the early days of the Bell System, what was the specific resonant frequency in hertz used by phreaks to signal 'all trunks' and bypass toll billing?" — answered `2600#` → *"That is correct."*
- IVR announces a spoken flag ("ollama bell" for Ext 1101) — **but that string is not the CTFd flag** for challenge 76 (see FINDINGS-BLOCKED-1). Real flag delivery likely requires the phone-side "player PIN" auto-claim flow — mechanism unknown.

## Challenge Catalog (from `/api/v1/challenges`)

| Cat | # | Name | Pts | Solves | Notes |
|---|---|---|---|---|---|
| Trivia | 76–105 | Ext 1101…1130 | 10 ea | many | Menu 1, dial 1 to start; answer with DTMF digits |
| Redbox | 74 | 212-555-1337 | 100 | 6 | ✅ SOLVED. 25¢ ACTS quarter, English prompt |
| Redbox | 75 | 514-555-1337 | 100 | 6 | 25¢ ACTS quarter, French prompt: *"Veuillez déposer vingt-cinq sous pour l'appel"* |
| Bluebox | 70 | Bluebox 1 - Seize the Trunk | 50 | 12 | PBX-side blue box; needs 2600 Hz + MF |
| Bluebox | 71 | Bluebox 2 - Call Erik Bloodaxe | 100 | 0 | Call `713-555-2600` via PBX using blue-box KP…ST |
| Voicemail | 21 | Reception | 50 | 5 | Menu 4, Nexus Data Solutions |
| Voicemail | 22 | Emannuel Goldstein | 50 | 7 | Voicemail box, likely PIN needed |
| Voicemail | 23 | Sandra Park | 75 | 0 | Voicemail box |
| Voicemail | 24 | Gary Chen | 100 | 6 | Voicemail box |
| Voice BBS | 59 | Leave a Message After the Beep | 50 | 6 | Menu 5, real board, leave a message |
| Voice BBS | 60 | Appended | 100 | 3 | Listen to all messages |
| Voice BBS | 61 | Number Station | 150 | 2 | Recording is tones, not voice |
| Bluetooth | 62 | Find the Phone | 25 | 6 | **In-person at con** |
| Bluetooth | 63 | What's that info? | 75 | 5 | Short hex ID of BT device |
| Bluetooth | 64 | Contact the Law | 150 | 2 | Send a fax somehow |
| Carding | 10 | Carding 1 - Looping Around | 50 | 4 | Needs physical calling card from con table |
| BBS | 13 | Log On | 50 | 5 | Data BBS, telnet? |
| BBS | 14 | Beat BadgeLife | 100 | 1 | Reach $10M in BadgeLife game on HackStock BBS |
| BBS | 15 | Find the Message | 75 | 5 | CEO left a message on HackStock BBS |
| BBS | 16 | What the SIT | 150 | 3 | Crack encrypted archive (PhoneCardPro) |
| BBS | 17 | Serial Killer | 200 | 2 | Crack software or write keygen |
| BBS | 18 | Hack our Foes | 50 | 10 | Flag on enemy BBS, check private messages |
| BBS | 65 | Something to Prove | 50 | 2 | Look for SECRET file on BBS |
| Wipeout | 106 | Daily Wipeout | 100 | 1 | Physical arcade cabinet at con |

## Tooling notes

### What works
- **CTFd flag submission:** `POST /api/v1/challenges/attempt` with header `CSRF-Token: <csrfNonce from window.init>` and JSON body `{"challenge_id": N, "submission": "flag"}`. Rate limited (~6/min per session). Correct response: `{"data": {"status": "correct"}}`.
- **Twilio outbound calls:** REST API with API-Key auth (`SK…` + `TWILIO_CLIENT_SECRET` + `TWILIO_ACCOUNT_SID`). Working from-number: `+19289778173`.
- **DTMF via `<Play digits>` in TwiML:** confirmed accepted by PhreakMe IVR.
- **Injecting audio via `<Play>URL</Play>`:** hosting the WAV as a Twilio Serverless Asset works cleanly. See `INFRA.md` (below).
- **Red-box tones:** `phr34cker5_mcp.tones.red_box_bytes("q")` produces a valid 0.3s ACTS quarter tone. Deposited via `<Play>` and accepted by PhreakMe.
- **Transcription:** Gemini 2.5 Flash on OpenRouter (`google/gemini-2.5-flash`) with `input_audio` blocks. Good enough for menus/prompts; sometimes mishears specific words (e.g. rendered "ollama bell" as "OLama Bell").

### What's flaky
- **`record=true` + `<Pause length="90"/>`:** intermittently returns a 363-byte empty MP3 (`-1s` duration). Reproduced 3× on the 514 pay attempt. Workaround: use two 30s pauses instead of one 90s, or use `<Record>` verb (but that has its own silence-timeout issues).
- **`<Record>` verb:** silence-detects and terminates the call early. Kill switch — don't use for capturing IVR responses.
- **Rate limits:** CTFd flag submission rate-limits after ~6 attempts/min. Back off 15s and retry.

### What I broke doing this
- Wasted ~30 minutes trying wrong flag spellings for Trivia Ext 1101 before realizing the phone-announced flag isn't the submission string (see `flag-ollama-bell.md`).
- Twilio Serverless setup: two failed API attempts before I passed a valid `DomainSuffix` (must match `^[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*$`).

## Assets

- `.recordings/` — every phone recording, keyed by Twilio Recording SID. Two-channel where available.
- `.tones/` — generated WAVs uploaded to Twilio Serverless.
- Twilio Serverless service: `phreakme-tones-5443.twil.io` (env `live`), hosts `redbox_q.wav` (ACTS quarter).
- Twilio account: `AC_REDACTED`.
