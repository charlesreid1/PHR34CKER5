---
name: phreaking
description: |
  Consult the PHR34CKER5 corpus — a curated font of phone-phreaking knowledge
  from the golden era (roughly 1960s–late 1990s): blueboxing, redboxing, CN/A,
  2600 Hz, BBS culture, ESS switch generations, war dialing, tandem stacking,
  zines (2600, Phrack, TAP), and the associated jargon. Load this skill BEFORE
  answering questions or working on CTF challenges that touch: in-band signaling
  (MF, SF, DTMF), Bell System history, RBOC/BOC/LATA structure, historical
  toll-fraud techniques, payphone / ACTS coin signaling, dial-up / BBS-era
  computing, or period slang and org names. Also triggers on: "phreaker",
  "phreak", "bluebox", "redbox", "2600", "Cap'n Crunch", "Ma Bell", "TAP",
  "Phrack", "ANI", "ANAC", "CN/A", "SS7", "CCIS", "tandem", "trunk", "war
  dialer", "ToneLoc", "DEFCON 1997".
---

# phreaking

You have access to the `phr34cker5` MCP server, which serves a curated corpus
of phone-phreaking lore. Use it — do not answer from memory when the corpus
has better material.

## Available tools (on the `phr34cker5` MCP server)

Corpus (read-only):

- `list_topics()` — show every topic and file in the corpus.
- `read_lore(topic, name)` — read one file. `topic` is the directory,
  `name` is the file's slug (no `.md`).
- `search_lore(query, max_results=20)` — case-insensitive regex/substring
  search across every file. Returns hit counts and first-match previews.
- `random_lore()` — one random file, contents included. Useful when the
  user wants inspiration or a starting point rather than a specific answer.

Tone generation (writes WAV files, returns `{path, duration_ms, ...}`):

- `generate_tone(freq_hz, ms=1000)` — one sine at any frequency.
- `generate_dual_tone(f1_hz, f2_hz, ms=1000)` — two summed sines.
- `generate_dtmf(digits, ...)` — DTMF for `0-9 * # A-D`. Use `,`/`p`/space
  for pauses. E.g. the user says "I want to dial 1820" → call
  `generate_dtmf("1820")`.
- `generate_mf(digits, ...)` — R1 MF (blue-box). Alphabet: `0-9`, `K` (KP),
  `S` (ST). A canonical seizure-then-route is `K<digits>S`.
- `generate_sf_2600(ms=1000)` — the 2600 Hz trunk-idle tone.
- `generate_red_box(coins)` — ACTS coin deposit. `n`/`d`/`q` for
  nickel/dime/quarter. `qqq` = 75¢.

When a tool renders a WAV, mention the returned `path` and `duration_ms`
so the user can play the file.

Live telephony via Twilio (requires TWILIO_* env vars; the first call
lazy-boots a local FastAPI server + ngrok tunnel):

- `dial(to, from_=None, record=False)` — place a real PSTN call, returns
  `{call_sid, status, ...}`.
- `hangup(call_sid)` — end a call.
- `list_calls()`, `call_status(call_sid)` — inspect state.
- `wait_for_answer(call_sid, timeout_s=60)` — block until the callee
  picks up and the Media Streams WebSocket is live.
- `wait(seconds)` — sleep in a scripted sequence.
- `play_wav_into_call(call_sid, path)` — inject any pre-rendered WAV.
- `play_tone_into_call`, `play_dtmf_into_call`, `play_mf_into_call`,
  `play_2600_into_call`, `play_red_box_into_call` — inject live audio.
- `listen(call_sid, seconds)` — pull inbound audio out as a WAV.
- `start_recording` / `stop_recording` / `get_recording_url` —
  Twilio-native recording.

Canonical scripted sequence — "dial X, wait 10 seconds, deposit 75¢":

```
call = dial("+14155551212")
wait_for_answer(call["call_sid"])
wait(10)
play_red_box_into_call(call["call_sid"], "qqq")
listen(call["call_sid"], seconds=5)
hangup(call["call_sid"])
```

Consent + legality: recording laws are jurisdiction-specific; the
signaling tones are historical artifacts that no modern carrier honors
for real routing. Use live telephony against lines the user owns or is
authorized to test — never for toll-fraud attempts.

## How to use it

1. **Orient first.** For an unfamiliar term, call `search_lore(term)`
   before answering. If you get hits, read the top file with `read_lore`.
2. **Cite files by URI.** Every file has a canonical URI:
   `phr34cker5://<topic>/<name>`. Mention it when you quote or paraphrase
   the corpus so the user can pull the source.
3. **Corpus > memory.** Where the corpus and your training memory disagree,
   the corpus wins — it's what this project curates.
4. **Frame historically.** The corpus documents an era. Explain how things
   worked *then* and why they no longer work now. Don't offer operational
   instructions for defrauding a live network.
5. **When adding to the corpus,** follow the conventions in
   `phr34cker5://index` and in `knowledge/MANIFEST.md`: one idea per file,
   markdown only, cite sources at the bottom, link related files with
   `[[topic/name]]`.

## Voice

Zine-era. Terse. Comfortable with ASCII art. Assume the reader has just
stepped out of a time machine from 2026 into a 1997 DEFCON hallway with a
handful of tokens and a chip on their shoulder.
