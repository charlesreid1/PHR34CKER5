# PLAN — organize PHR34CKER5 for the DEF CON phreaking CTF

> Status: **plan only, nothing executed yet.** This file exists so we can
> argue with it before touching the repo.

## The problem in one paragraph

The repo shipped a real telephony toolkit in its last four commits (tone
synthesis + Twilio live-call injection + recording), but the README still
opens by insisting PHR34CKER5 is "a font of phreaking knowledge — not a
'generate DTMF tones' utility" (`README.md:33`). Meanwhile `docs/twilio_setup.md`
(342 lines, excellent) is untracked and unlinked, and `scripts/` sits next
to `src/` with no explanation of the difference. The result: a user
opening this repo can't tell that it's a co-pilot that *does things*,
not just a corpus that *knows things*.

## What we're building toward

A CTF phreaking co-pilot: an MCP server that (a) knows the history and
jargon deeply enough to advise, (b) synthesizes any tone we'd want to
inject, and (c) drives live PSTN calls end-to-end so the assistant can
execute scripted sequences ("dial X, wait for answer, wait 10s, deposit
75¢, listen for 5s, hang up") without a human in the loop for every step.

---

## Phase 1 — Re-frame and reorganize (docs + layout)

Fast, no code risk, biggest clarity payoff. Do this first.

### 1a. Rewrite the README lede

Replace the current "font of knowledge — not a DTMF utility" framing with
a three-tier identity:

> PHR34CKER5 is a CTF phreaking co-pilot: a corpus of lore *and* a
> live-telephony toolbox exposed over MCP. It knows the history
> (blueboxing, red-boxing, ACTS, ESS, CN/A, T.30) and can act on it —
> synthesize tones, place PSTN calls via Twilio, script sequences, and
> record.

Immediately below, a "What can it do?" section with three tiers:

- **Know** — corpus tools (`list_topics`, `search_lore`, `read_lore`, `random_lore`)
- **Synthesize** — tone generators (DTMF, MF, red box, fax CNG/CED, 2600 Hz)
- **Act** — live-call tools (`dial`, `wait_for_answer`, `play_*_into_call`, `listen`, `record`)

Then promote the canonical scripted example (currently at `README.md:124`)
to sit right under those three tiers.

### 1b. Add a "Repo map" section to the README

One paragraph, ~7 lines:

```
src/phr34cker5_mcp/    the MCP server (installable Python package)
knowledge/             the lore corpus (markdown, one topic per dir)
skills/phreaking/      the SKILL.md that tells assistants to use the MCP
scripts/               user-facing shell helpers (credential setup, etc.)
docs/                  long-form guides that don't fit in the README
```

### 1c. Add `scripts/README.md`

One short paragraph clarifying: *these are shell helpers you run once as
a human (`setup-twilio.sh` for credential setup). Runtime code — the MCP
server itself — lives in `src/`. `scripts/` and `src/` are deliberately
separate because they have different audiences (human-once vs.
runtime-always).*

### 1d. Commit the existing `docs/twilio_setup.md`

Currently untracked (per `git status`). Commit it and link it from the
README's Twilio section: *"see [docs/twilio_setup.md](docs/twilio_setup.md)
for the full CTF-focused Twilio playbook."*

### 1e. Add placeholder `docs/call_recipes.md`

**Purpose:** a cookbook of scripted call sequences the assistant (or a
human) can adapt at the con. Reading this file should teach both "what
sequences are common" and "how to compose the MCP tools to do them."

**Placeholder skeleton to author later:**

```
# CALL RECIPES

Reusable sequences of MCP tool calls for common CTF phone tasks. Each
recipe has: intent, when to reach for it, the sequence, and what to
watch for.

## 1. "Just dial it and see what happens"
## 2. Deposit exact change at an ACTS prompt
## 3. IVR walk — enumerate a menu tree via DTMF
## 4. DISA probe — try a PIN list, back off on lockout
## 5. Modem carrier — detect and hand off to minicom
## 6. Fax send — replay a canned page
## 7. Fax receive — capture + decode a flag page
## 8. Voicemail poke — press 0 / *, listen for greeting variants
## 9. Conference bridge — join, listen, announce
## 10. Loop-around — dial both ends of a test pair, cross-connect
## 11. Blueboxing simulation (against a Village-owned MF trunk)
## 12. Red-box simulation (against a Village-owned ACTS PBX)
```

Each recipe should include: the exact MCP tool sequence as pseudocode,
what the audio should *sound like* at each step, and the failure modes
(what it means if you don't hear that). Cross-link to the relevant
`knowledge/` files.

### 1f. Add placeholder `docs/ctf_playbook.md`

**Purpose:** the assistant's mental model for "you've been handed a
mystery phone number at DEF CON, now what." Complements
`docs/twilio_setup.md` (which is pre-con setup) — this one is *at the
con, in the moment.*

**Placeholder skeleton to author later:**

```
# CTF PLAYBOOK

What to do when handed an unknown number at a phreaking CTF. Optimized
for the first 60 seconds of a puzzle.

## Before you dial
- Confirm it's PSTN, not SIP-only (see docs/twilio_setup.md).
- Confirm the CTF sanctions the target (village-owned vs. real infra).
- Set MAX_CALL_MINUTES so a stuck call can't burn Twilio budget.

## The triage dial
- Place the call with recording enabled.
- Listen for 15-30s. Classify what you hear:
    - Ringback → nobody home (or they're screening — retry, or move on)
    - IVR menu → recipe #3 (IVR walk)
    - Silence with periodic prompts → likely DISA — recipe #4
    - Voice greeting → likely voicemail — recipe #8
    - CED (2100 Hz) → fax — recipe #7
    - Carrier tones → modem — recipe #5
    - Multiple voices/hold music → conference bridge — recipe #9
    - Milliwatt (1004 Hz test tone) → CTF humor — try 2600-adjacent puzzles
    - ANAC-like "your number is …" → identify what ANI the CTF sees

## Common puzzle patterns
- The greeting IS the puzzle (voicemail, IVR intro)
- The hold music IS the puzzle (steganography, morse)
- The IVR menu options are a cipher (option 4 = D, etc.)
- The fax page IS the flag (image with QR/text)
- The DISA PIN comes from another puzzle
- The number itself is a cipher (letters on the keypad)

## What to write down
- Full recording (Twilio-side)
- Transcript of any voice prompts (once transcribe tool exists)
- DTMF you heard (once dtmf_decode exists)
- Timing of prompts and pauses (for later diffing)

## When to stop
- Budget cap reached
- You've extracted the flag
- You've confirmed the puzzle needs an out-of-band input you don't have yet
```

Both placeholder files should be short at first (they're stubs the
assistant fills in as we play). They exist so the *structure* is in the
repo and so the README can link to them from day one.

### 1g. Update `knowledge/MANIFEST.md`

One-paragraph edit: acknowledge that the corpus is the *reference* half
of the assistant and the MCP tools (in `src/`) are the *acting* half.
Currently the MANIFEST reads as if lore is all there is.

### 1h. Keep `scripts/` and `src/` separate

They serve different audiences (human-once vs. runtime-always). Don't
consolidate. Document the distinction (1c handles that) and move on.

---

## Phase 2 — Fill knowledge gaps

Assessment first, then the fill plan.

### Why the current corpus reads as *shallow*

The 12 topics are broad (they cover the whole classic canon) but each
file is 20-77 lines and follows the same template: 1-paragraph intro,
one or two bulleted lists, a "why it doesn't work anymore" section, a
"see also" block. That template produces excellent **encyclopedia
stubs** — dense enough to orient someone, thin enough that anyone who
already knows what a red box is learns nothing new. Concrete evidence
from the corpus as it stands:

- **`redboxing/README.md`** (32 lines): gives the tone frequencies and
  the burst table, but does not cover — *why* those specific durations,
  what a real COCOT does to reject them, why quarter-in-nickel-slot
  works or doesn't, how ACTS detection tolerated timing slop, how the
  1996 payphone deregulation changed detection, or a single worked
  example of an actual red-boxing session with prompts and pauses.
- **`blueboxing/README.md`** (36 lines): mentions KP and ST, but the
  full R1 MF digit table isn't here — the MANIFEST explicitly promises
  `mf-tones.md` "to be written." No worked seizure example. No
  discussion of the ~1s 2600 duration vs. carrier flash detection,
  no operator-position numbers to route to, no `KP2` / `STP` / `ST2P`
  / `ST3P` variants, no international routing codes.
- **`ess/README.md`** (35 lines): a switch lineage table with dates.
  Nothing about *how you'd tell what switch you were on* from audible
  behavior (5ESS reorder cadence vs. DMS-100, dial tone timbre, ring
  cadence quirks), which is exactly the kind of thing the assistant
  needs when triaging an unknown number at a con.
- **`cna/README.md`** (30 lines): the pretext script and why it worked,
  but no example pretext dialogue, no list of historical CN/A bureau
  numbers by region (public-domain, in every issue of TAP), no
  discussion of what the modern equivalent lookups (LIDB/CNAM) actually
  return.
- **`tandem-stacking/README.md`** (27 lines): explains the concept in
  the abstract. No trunk route code examples. No description of what
  the audio sounded like at each hop (that's the debugging skill).
- **`fax/README.md`** (77 lines, the deepest file): actually gets to
  worked examples — the T.30 handshake diagram, tone parameters, war-
  dialing angle. This is the shape the other files should grow toward.

So "shallow" = **encyclopedic, not operational.** The corpus tells you
*what a thing is*; it rarely tells you *what it sounds like, what it
looks like on the wire, or how to recognize it in the wild.* For a CTF
co-pilot, the operational layer is the load-bearing one.

### What "deeper" looks like, concretely

Adopt a per-topic pattern of splitting one README into several files:

```
knowledge/<topic>/
    README.md              orient — what is this, why care (keep short)
    reference.md           the technical spec — frequencies, timings, tables
    walkthrough.md         one or more worked examples with real audio hints
    recognition.md         how to identify it from audio / behavior at a CTF
    history.md             optional — the full story, sources, incidents
```

Each file stays short (that's the corpus convention), but the *set*
adds up to something operational instead of encyclopedic. `fax/` is
already 2/3 of the way there in a single file — split it or leave it,
but use its depth as the bar.

### The specific fills

**Flesh out existing topics** (write the files the MANIFEST already
promises, plus operational companions):

- `blueboxing/mf-tones.md` — the full R1 MF digit table with frequencies,
  KP/ST/STP/ST2P/ST3P variants, tone durations, a worked
  `KP-1-800-555-1212-ST` example with what each step sounds like.
- `blueboxing/seizure-walkthrough.md` — 2600 Hz duration tolerances,
  what the far-end trunk did in response, what the audio sequence
  sounded like from the caller's end.
- `redboxing/acts-timing.md` — burst tolerance windows, why quarters
  are five 33 ms bursts (spec history), COCOT vs. LEC-owned payphone
  detection differences.
- `redboxing/walkthrough.md` — a full "long-distance from a fortress
  phone, deposit $1.25" session as it would have sounded in 1993.
- `ess/audible-tells.md` — how to tell what switch you're on from dial
  tone, ring cadence, reorder, busy signal timbre.
- `ess/no-4-ess.md` — the toll switch that mattered for blueboxing.
- `tandem-stacking/international.md` — trunk route codes, what each
  hop sounded like, a worked overseas-loop example.
- `cna/pretext-scripts.md` — worked example dialogues (period-accurate),
  what would blow the pretext.
- `2600hz/whistle-tolerances.md` — how forgiving the SF detector was
  (frequency drift, duration), the actual detector implementation.
- `war-dialing/toneloc-tuning.md` — how the classifier worked, what
  carrier/VMB/dialtone results actually meant, false-positive patterns.

**New topics** (the CTF-facing ones the corpus is missing):

- `knowledge/ctf/` — one file per subgenre of village puzzle:
  - `ivr-mazes.md`
  - `disa-prompts.md`
  - `voicemail-riddles.md`
  - `modem-carriers.md`
  - `fax-flags.md`
  - `conference-bridges.md`
  - `simulated-anac-cna.md`
  - `milliwatt-testlines.md`
  Each: what it sounds like on the first 15 seconds of a call, how to
  probe it, which MCP tools to reach for. This is `docs/ctf_playbook.md`
  cross-referenced into the corpus so the assistant finds it via
  `search_lore`.

- `knowledge/dtmf/` — the DTMF frequency chart, ABCD / autovon tones,
  common misconceptions (why # ≠ * on all systems, what happens at 4-digit
  post-dialing on legacy PBXs).

- `knowledge/modems/` — V.21/V.22/V.32/V.34 handshake audio, what "the
  whistle" sounds like at each rate, why modem carriers show up as CTF
  puzzles, what handshake stage fails first when audio is stripped.

- `knowledge/operator-services/` — 0, 00, 611, 411, 950 dialing;
  historical vs. modern behavior; what a CTF "operator" IVR is
  probably parodying.

Target: ~2 hours of writing. Format is already established (short,
cite sources at bottom, `[[topic/name]]` links).

---

## Phase 3 — Missing MCP capabilities

The tool set today is strong on *primitives* (generate a tone, inject
audio, listen for N seconds) and thin on *composition* and *perception*.
That's the gap.

### High value

1. **`play_sequence(call_sid, steps=[...])`** — atomic scripted-action
   tool. Right now "dial, wait, tone, listen, hangup" is 5+ separate
   MCP tool calls with the assistant in the loop for each one. A single
   tool taking `[{"action":"wait","s":10},{"action":"dtmf","digits":"1234"},{"action":"listen","s":5}]`
   is more reliable and matches how a user actually thinks about a call
   plan. Also gives us a single place to add timeouts and cleanup.

2. **`detect_tone(call_sid, seconds, targets=["dial-tone","busy","ringback","2600","cng","ced","modem","milliwatt"])`**
   — Goertzel-based detector on inbound audio. Right now `listen()`
   gives you a WAV and the assistant has to guess what's in it. A native
   detector unlocks "wait until dial tone, then send digits."

3. **`dtmf_decode(call_sid, seconds)` / `dtmf_decode_wav(path)`** — pull
   DTMF digits out of inbound audio. Critical for IVR/DISA puzzles
   where the far end plays back digits.

4. **`transcribe(call_sid_or_wav, seconds)`** — speech-to-text on
   captured audio. Twilio has this built in; add a thin wrapper. Huge
   lift for "listen to the IVR menu and tell me the options."

5. **`send_dtmf_via_twilio(call_sid, digits)`** — use Twilio's
   `<Play digits="...">` TwiML instead of injecting synthesized audio,
   for IVRs that need clean digits.

### Medium value

6. **`answer_inbound(call_sid, script=[...])`** — the `/twiml/inbound`
   endpoint exists but no MCP tool lets the assistant *do* anything
   with an incoming call. Add one that scripts the answer.

7. **`generate_modem_carrier(rate="v21"|"v22"|"v32")`** — synthetic
   modem carrier for testing / matching a CTF flag.

8. **`generate_busy()`, `generate_ringback()`, `generate_reorder()`**
   — the ambient tones of the network. Useful for detector tests and
   for authoring puzzles.

9. **`generate_milliwatt(ms=10000)`** — 1004 Hz at −16 dBm0. Every CO
   had one; CTF authors love them.

10. **`call_log(call_sid)`** — full timeline (twiml_hit, ws_connect,
    tones sent, bytes captured, marks acked) for post-mortem.

### Lower priority

11. Green box (operator coin collect / return) to round out the box zoo.
12. `play_recording_into_call(call_sid, recording_sid)` — replay a
    captured recording into a new call (great for reverse-engineering
    an IVR).
13. `multi_call_bridge(sids=[...])` — conference bridge across two live
    calls (Twilio-native).

### Operational polish

14. **Cost guardrail:** `MAX_CALL_MINUTES` env var; auto-hangup after
    that. The Twilio doc (`docs/twilio_setup.md`) already flags the
    1-hour stuck-call footgun. Belt and suspenders.

15. **Structured call events** streamed via an MCP resource
    (`phr34cker5://calls/<sid>/events`) so the assistant can subscribe
    instead of polling `call_status`.

---

## Phase 4 — Skill update

Update `skills/phreaking/SKILL.md` to:

1. Mention the new MCP tools as they land (each new tool needs a
   one-line description in the SKILL, or the assistant won't reach for
   it).
2. Add a "playbook" section that mirrors `docs/ctf_playbook.md` — when
   handed a mystery number, do X, Y, Z. The SKILL is what actually
   shapes assistant behavior mid-CTF, so its density matters more than
   the README's.
3. Add "corpus depth cues" — remind the assistant that the corpus now
   has walkthroughs / recognition / reference splits per topic, and to
   prefer `walkthrough.md` when the user is doing rather than reading.

---

## Suggested execution order

1. **Phase 1 (docs pass)** — README rewrite, `scripts/README.md`,
   commit `docs/twilio_setup.md`, create `docs/call_recipes.md` and
   `docs/ctf_playbook.md` stubs, update `knowledge/MANIFEST.md`. Fast,
   no code risk, biggest clarity payoff. Check in before proceeding.
2. **Phase 3 top 4 tools** — `play_sequence`, `detect_tone`,
   `dtmf_decode`, `transcribe`. These are the leverage tools.
3. **Phase 2 knowledge fills** — start with `ctf/`, `modems/`,
   `dtmf/`, plus the specific stubs the MANIFEST already promises.
   Fill `docs/call_recipes.md` and `docs/ctf_playbook.md` for real as
   we accumulate real recipes.
4. **Phase 3 remaining tools + cost guardrails**.
5. **Phase 4 skill update** to teach the assistant to use the new
   surface.

Each phase is independently valuable; stopping between phases leaves
the repo in a coherent state.
