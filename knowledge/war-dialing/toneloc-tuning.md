# TONELOC / THC-SCAN TUNING — HOW THE CLASSIFIER ACTUALLY WORKED

> A war dialer is a classifier with a modem for a sensor. Every result
> category is a guess the tool made from a few seconds of audio and
> carrier-detect state — and every false positive is that guess going
> wrong in a way worth knowing.

`[[war-dialing/README]]` lists the tools and result categories. This
file is the operational layer: *how* ToneLoc and THC-Scan decided
CARRIER vs FAX vs VOICE vs DIALTONE vs RINGOUT, where they were wrong,
and what the knobs cost you.

## The decision, per number

The dialer dialed, then watched two things: the modem's **carrier-detect
(DCD)** line / result codes, and, failing a carrier, the **timing** of
what came back.

| Result | How it was decided |
|---|---|
| **CARRIER** | modem returned `CONNECT` — it trained up with the far end. Strongest, most reliable classification. |
| **FAX** | `CONNECT` from a fax, or the tool heard the **CED (2100 Hz)** answer / detected fax framing. THC-Scan split fax out better than early ToneLoc. |
| **VOICE** | `NO CARRIER` after answer supervision, but the line answered — someone (or an announcement) picked up and no carrier trained. Often inferred, not measured. |
| **DIALTONE / second dial tone** | after connect, the far end presented a dial tone (a PBX outdial / diverter). Detected by tone, or by the tool successfully dialing again. |
| **RINGOUT / TIMEOUT / NO ANSWER** | rang past the ring-count limit, or the modem returned `NO ANSWER`. Noise. |
| **BUSY** | modem `BUSY` result. Skipped, sometimes requeued. |

## The false-positive patterns

The classifier only sees `CONNECT`/`NO CARRIER`/`NO ANSWER` plus crude
tone timing, so it mislabels predictably:

- **Voice → CARRIER.** A "Hello? Hello?" or answering-machine beep could
  make some 2400-baud modems briefly assert DCD or false-`CONNECT`,
  especially with aggressive guard tones. Eyeball CARRIER hits.
- **FAX ↔ CARRIER.** Both answer near 2100 Hz; a tool that didn't wait
  for fax framing lumped them together.
- **CARRIER → RINGOUT.** Too-short **carrier wait** hangs up before a
  slow far-end modem answers — a real carrier logged as nothing.
- **DIALTONE → VOICE/TIMEOUT.** A diverter that answers silently then
  presents dial tone after a pause is missed if the listen window is short.
- **BUSY vs reorder.** Line-busy and fast-busy (all-trunks-busy) differ
  only by cadence; a dialer that only knew `BUSY` conflated them (see
  `[[ess/audible-tells]]` — 500/500 vs 250/250 ms).

Rule of thumb: **CARRIER and FAX hits were trustworthy; VOICE and
TIMEOUT needed a human callback.**

## The `.dat` file format (why it matters at a CTF)

ToneLoc stored scan state in a binary **`.dat`** file per exchange (e.g.
`555-.DAT`) — a compact per-number status map plus a header:

- A **header** with the mask/range, counts, and config.
- A **status byte/nibble per number** encoding one of: unscanned / busy
  / no-answer / ringout / carrier / voice / tone / aborted / blacklisted.
- Companion **`.log`** / `FOUND.LOG` / `TONE.LOG` held the readable
  carrier list with timestamps.

Why a CTF hands you one: the `.dat` *is the puzzle state*. Decode the
status bytes and you recover which numbers answered as what without
re-dialing — render it with `TONELOC /S` (or `tlreport`), or parse the
byte-per-number map directly. The flag is usually the lone CARRIER (or
an oddball status) in a sea of no-answers.

## Tuning params and what each costs

| Param | What it does | Cost of raising | Cost of lowering |
|---|---|---|---|
| **Dial timing / inter-call delay** | pause between attempts | slower scan | overruns the modem / trips telco fraud heuristics; missed answers |
| **Ring count** (rings before hangup) | how long to wait for answer | more time per dead number | hangs up on slow-answering PBXs (missed hits) |
| **Carrier wait** (`CARRIERTIME`) | seconds to wait for training after answer | catches slow far-end modems | misses real carriers as RINGOUT |
| **Nudge / connect string** | text sent after CONNECT to provoke a banner | — | too aggressive can drop a fragile login |
| **Blacklist / exclude** | numbers never to dial | safety | miss something in-range |
| **Randomize order** | dial the range out of sequence | — | (mostly a detection-avoidance choice) |

Faster scans skip slow answerers; patient scans take all night. The scan
is a time-vs-completeness trade the whole way down.

## Login-banner fingerprints (from what the nudge string pulls back)

Once connected, the **banner** dates and names the far end. A short field
guide (see `plan-knowledge.md` D.6 for the full list):

| Banner seen | Likely system |
|---|---|
| `Username:` then `Password:` (capitals) | VAX/VMS |
| `login:` / `login: incorrect` | Unix (VAX/Ultrix, SunOS, BSD) |
| `Welcome to the ROLM PhoneMail system` | Rolm PhoneMail |
| `Enter Terminal Type:` / blob then `HELLO,` | HP3000 MPE/iX |
| `CI:` | Nortel DMS (MAPCI) |
| bare `<` prompt | AT&T 5ESS (RCV) |
| `[Ctrl-C to abort, Enter to continue]` | Nortel SL-1 SDI port |
| `@` bare prompt / `Enter your NUI:` | Sprintnet PAD / Tymnet |
| `AT` / `OK` echo | another modem |

Cross-check against `[[ctf/modem-carriers]]` (name-the-stall-stage) and
`[[modems/README]]` (standards).

## Modern: WarVOX vs SIP

WarVOX (H. D. Moore, 2009) dropped the carrier obsession and recorded
**audio**, then classified by signal-processing (voice/fax/modem/
silence/dialtone) offline — a scan finds *voicemail, IVRs, and humans*,
not just modems. Against **SIP/VoIP** today the "dial" is an INVITE and
"answer" is a 200 OK with an RTP stream; you classify the RTP audio the
same way WarVOX did a WAV. Fax pass-through is the fragile part — G.711
usually survives, G.729 mangles the handshake (`[[fax/README]]`).

## See also
- [[war-dialing/README]] — tools, result categories, modern relevance
- [[modems/README]] — the standards a CARRIER hit trains to
- [[ctf/modem-carriers]] — naming the modem by where the handshake stalls
- [[fax/README]] — the FAX category and codec pass-through caveats
- [[ess/audible-tells]] — busy vs reorder, dial-tone timbre

## Sources
- ToneLoc documentation (Minor Threat & Mucho Maas, 1994) — `.dat`/`.log`
  formats and config parameters
- THC-Scan documentation (van Hauser / THC, 1996)
- H. D. Moore, WarVOX release notes and talks (2009)
- Phrack and 2600 Magazine (various) on war-dialing practice and banners
- plan-knowledge.md Appendix D.6 (war-dial banner fingerprints)
