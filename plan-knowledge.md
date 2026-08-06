# PLAN — deepen the PHR34CKER5 knowledge corpus

> Status: **plan only, nothing executed yet.** Sibling to `plan-organize.md`;
> this file zooms in on `knowledge/`. Read that one first for the wider repo
> context.

## The problem in one sentence

The corpus is **broad but encyclopedic** — every file explains *what a
thing is*, few explain *what it sounds like, what it looks like on the
wire, or how to recognize it in the wild* — and that operational layer
is exactly what a CTF co-pilot loads on.

## The problem in more than one sentence

There are 12 topics under `knowledge/`, each a single `README.md`,
each 20-77 lines, all following the same template:

1. One-paragraph intro
2. One or two bulleted lists (tones, dates, actors)
3. A "why it doesn't work anymore" paragraph
4. A `## See also` cross-link block
5. A `## Sources` bibliography

That template produces excellent orient-me stubs — dense enough that a
newcomer knows what a red box is, thin enough that anyone who already
knows learns nothing new. It works as a table of contents *plus a few
paragraphs*, not as a working reference.

The load-bearing missing layer is **operational knowledge**: the kind
of thing you need not to explain phreaking, but to *do* it at a con
with a live line and a puzzle you've never seen before.

---

## Concrete evidence, per file

Every point below is a specific thing the corpus *does not currently
say* but should, cross-checked against the file it belongs in.

### `redboxing/README.md` (32 lines)

Present: the 1700+2200 Hz frequencies, the burst pattern per coin,
countermeasures that killed it.

Missing:
- Why the specific durations (66 ms nickel/dime, 33 ms quarter). Spec
  history matters because CTF authors love to test the edges.
- ACTS detector tolerance windows — how far off timing could be and
  still credit.
- COCOT vs. LEC-owned payphone detection differences (COCOTs did local
  validation; that's why cassette-recorder red-boxes stopped working in
  some places before others).
- A worked example: full "call long-distance, hear ACTS prompt, deposit
  $1.25 with tones, get cut through" session as it sounded in 1993.
- The Radio Shack tone dialer + crystal swap mod that everyone
  actually used.

### `blueboxing/README.md` (36 lines)

Present: the KP/ST concept, the seizure sequence in caricature, why
it's history.

Missing:
- The full R1 MF digit table. The MANIFEST literally names
  `mf-tones.md` as "to be written."
- KP2 / STP / ST2P / ST3P variants and when each was used.
- 2600 Hz duration tolerance (~1s nominal, but detectors varied).
- Operator position codes ("dialing" internal AT&T positions).
- International route codes — what `KP+011+…+ST` looked like vs.
  domestic.
- A worked seizure: 2600 Hz for N ms → wink → KP → digits → ST →
  what happens at each stage on the audio.
- Failure modes: what "the trunk didn't wink back" sounded like.

### `2600hz/README.md` (27 lines)

Present: what SF supervision meant, Cap'n Crunch story, in-band vs.
out-of-band framing.

Missing:
- SF detector implementation sketch (band-pass + duration filter).
- The actual pull-in / drop-out timings different detectors used.
- Why 2600 Hz specifically (voice-band selection, avoiding fricative
  overlap).
- The 3700 Hz variant used on some carriers.
- Why the Cap'n Crunch whistle worked despite being crude — detector
  bandwidth was generous.

### `ess/README.md` (35 lines)

Present: a lineage table (1ESS through 5ESS + DMS-100) with dates and
one-line descriptions.

Missing — this is the file with the biggest operational gap:
- **How to tell what switch you're on from audible cues.** Dial tone
  timbre, ring cadence, reorder tone cadence, busy signal characteristics,
  "your call cannot be completed" recording style. This is *the* skill
  when triaging an unknown number at a CTF.
- What signaling each switch spoke on trunks (1ESS → MF, 4ESS →
  CCIS/SS7, 5ESS → SS7 native).
- Which switches were most common in what regions and eras.
- What each switch's characteristic bug or misfeature was.

### `cna/README.md` (30 lines)

Present: the pretext concept, why it worked, modern equivalents (LIDB,
CNAM).

Missing:
- **Example pretext dialogue** — a full, period-accurate script with
  what the operator asked, how the phreaker responded, what would blow
  the pretext.
- Historical CN/A bureau numbers by region. These were in every issue
  of TAP; public-domain by decades.
- What LIDB / CNAM lookups actually return today, and how that differs
  from a CN/A lookup.
- The overlap with CBCS (Calling-Card Bureau) and the parallel social
  engineering game against it.

### `tandem-stacking/README.md` (27 lines)

Present: the concept — chain tandems via in-band signaling.

Missing:
- Trunk route codes — what `KP+7-digit-route+ST` actually meant.
- A worked stack: hop 1 sounds like X, hop 2 sounds like Y.
- The billing-record misalignment mechanic in real detail (why one
  hop's AMA record didn't tie to the next).
- Internal test numbers reachable via stacking (loop-arounds, milliwatt,
  ANAC).
- The famous overseas-loop trick (route back into the US via a foreign
  tandem to disguise origination).

### `war-dialing/README.md` (31 lines)

Present: tool list (ToneLoc, THC-Scan, PhoneSweep, WarVOX), result
categories (CARRIER, VMB, DIALTONE, RINGOUT).

Missing:
- What the classifier *actually did* — how ToneLoc distinguished a
  carrier from a fax from a voice greeting.
- The false-positive patterns (why some voice lines got tagged as
  carriers).
- The `.dat` file format (this matters because CTF puzzles occasionally
  hand you one).
- Tuning: dial timing, ring count, carrier wait, what each parameter
  costs you.
- Modern equivalents: what a WarVOX-style scan looks like against
  SIP/VoIP endpoints today.

### `bbs/README.md` (29 lines)

Present: BBS culture overview, baud lineage, sysop role.

Missing:
- The actual handshake sounds at 300 / 1200 / 2400 / 9600 / V.34, and
  what a listener could tell about the connection from the audio alone.
- What a BBS logon sequence *sounded* and *looked* like — CONNECT
  message, garbage, ANSI, login prompt.
- FidoNet / mail-hour mechanics — why BBSes went dead at specific
  hours.
- The transition to public-internet gateways (UUCP dial-ups) which
  bridged the BBS world to Usenet.

### `zines/README.md` (35 lines)

Present: the three big zines (2600, Phrack, TAP), founding dates,
one-line descriptions.

Missing:
- Table of contents highlights — the two or three landmark articles
  in each zine that everyone references (e.g. Phrack 47 "Smashing the
  Stack" as the *out-of-scope-but-canonical* reference; the specific
  2600 Winter '93 red-box article the corpus already cites).
- Where to actually read them today (archive.org, textfiles.com, the
  Phrack site).
- Zine-adjacent BBS scenes (LOD, MOD, cDc release channels).

### `fax/README.md` (77 lines) — the exception

This is already the deepest file. It has the T.30 handshake diagram,
concrete tone parameters, the war-dialing angle, and a bibliography
that names the ITU-T specs and SpanDSP. **This is the depth bar the
other files should hit.**

Even here, gaps remain:
- What the *rest* of the handshake sounds like after CED (V.21 300-baud
  FSK preamble is very distinctive).
- How Twilio's transcoding affects fax pass-through (G.729 mangles it
  entirely; G.711 usually works but isn't guaranteed).
- How to author a fax page whose *image* encodes a flag.

### `greenboxing/README.md` (20 lines) and `glossary/README.md` (49 lines)

These are honest one-file references and largely fine as-is. Glossary
should keep growing as new terms enter the corpus. Green box could
gain a worked example (COIN COLLECT vs. COIN RETURN operator tone
pairs and what they did).

---

## Why "shallow" ≠ "table of contents"

Worth being precise about the diagnosis: the files are not empty and
they're not link farms. They have real content — Cap'n Crunch, RBOC
divestiture, KP/ST, ACTS burst counts, the ESS lineage. They read like
a well-edited pocket encyclopedia.

The shallowness is one level down: **encyclopedic content is not
operational content.** An encyclopedia tells you red boxes emit
1700+2200 Hz bursts. An operational reference tells you the ACTS
detector had a ~±10 ms tolerance on burst width, that a Radio Shack
tone dialer with a 6.5536 MHz crystal produced tones within that
window, and here is what the resulting call sounded like on a 1993
Chicago fortress phone. The corpus today is at level one and needs to
grow toward level two — while keeping level one intact for
orientation.

---

## The proposed shape — split-per-topic

Adopt this pattern for the fat topics (all of them except `glossary/`
and `greenboxing/`):

```
knowledge/<topic>/
    README.md          Orient — what is this, why care. Short.
                       Links to the files below. This is the entry
                       point for search_lore hits.
    reference.md       The technical spec — frequencies, timings,
                       tables, protocol diagrams, standards citations.
                       Dry, complete, load-bearing.
    walkthrough.md     One or more worked examples. Real audio hints
                       at each step ("you hear a wink, then silence").
                       Time-annotated. Failure modes called out.
    recognition.md     How to identify this thing in the wild from
                       audio and behavior. The CTF triage layer.
                       "If you hear X within the first 15 seconds,
                       it's probably Y."
    history.md         Optional. The full story — landmark incidents,
                       who did what when, the sources that go deeper.
```

Each file stays short (the corpus convention holds); the *set* is
operational. `fax/README.md` is 2/3 of the way there already inside a
single file — split it if that helps, but its density is the target.

### Why this split works for a CTF co-pilot

The four file types map to the four questions the assistant asks
during a challenge:

| Assistant question | File it opens |
|---|---|
| "What am I looking at?" | `README.md` |
| "What are the exact parameters?" | `reference.md` |
| "What does this look like end-to-end?" | `walkthrough.md` |
| "Is *this call* an example of it?" | `recognition.md` |
| "Where did this come from?" | `history.md` |

`search_lore` finds the hit; the assistant then chooses the follow-up
file by intent. That's a much better ergonomic than one file that has
a little of everything.

### What stays in the top-level README

Only orientation. If a `README.md` starts trying to be its own
`reference.md` and `walkthrough.md`, it defeats the split. Rule of
thumb: if the section has a table, it belongs in `reference.md`; if
it has "step 1 / step 2 / step 3", it belongs in `walkthrough.md`.

---

## The specific fills, prioritized

Priority tiers reflect *CTF utility per hour of writing*. High-tier
items should be written first because they unblock actual play.

### Tier 1 — operational must-haves

These are the files that let the assistant *do* things at a con.

1. `blueboxing/reference.md` — full R1 MF digit table, KP variants,
   ST variants, tone durations, amplitude norms. Absorb the current
   README's tone section, expand.
2. `blueboxing/walkthrough.md` — `K18005551212S` end-to-end. What each
   sub-step sounded like on a 1975 outbound trunk.
3. `redboxing/reference.md` — ACTS burst-width tolerance windows,
   coin-value math, the Radio Shack crystal mod.
4. `redboxing/walkthrough.md` — full fortress-phone → ACTS → deposit
   session with prompts and pauses.
5. `ess/recognition.md` — audible tells per switch generation. **This
   is arguably the single most valuable file the corpus is missing.**
6. `2600hz/reference.md` — SF detector timings, pull-in/drop-out,
   Cap'n Crunch tolerances, why 2600 specifically.
7. `cna/walkthrough.md` — one full pretext dialogue, annotated with
   what could have gone wrong at each turn.

### Tier 2 — new topics the corpus doesn't have at all

The CTF-facing corpus. `plan-organize.md` §Phase 2 also lists these;
they belong here operationally because they're the corpus mirror of
`docs/ctf_playbook.md`.

- `knowledge/ctf/` — one file per village-puzzle subgenre:
  - `ivr-mazes.md`
  - `disa-prompts.md`
  - `voicemail-riddles.md`
  - `modem-carriers.md`
  - `fax-flags.md`
  - `conference-bridges.md`
  - `simulated-anac-cna.md`
  - `milliwatt-testlines.md`
  Each: what it sounds like in the first 15 seconds, how to probe it,
  which MCP tools to reach for, common flag-hiding patterns.
- `knowledge/dtmf/` — DTMF frequency chart, ABCD/autovon tones,
  post-dialing behavior, the twist quirk.
- `knowledge/modems/` — V.21/V.22/V.32/V.34 handshake audio, what fails
  first when audio is stripped, how to identify carrier rate from the
  handshake.
- `knowledge/operator-services/` — 0, 00, 611, 411, 950 dialing; what a
  CTF operator IVR is probably parodying.

### Tier 3 — depth on existing topics

Nice-to-haves that turn the corpus from good to definitive.

- `ess/reference.md` — trunk signaling per generation, what CCIS
  variant each spoke.
- `tandem-stacking/reference.md` — trunk route codes, real examples.
- `tandem-stacking/walkthrough.md` — overseas loop.
- `war-dialing/reference.md` — result categories, false-positive
  patterns, `.dat` format.
- `war-dialing/walkthrough.md` — tuning a scan.
- `bbs/recognition.md` — connection-audio characteristics per baud
  rate.
- `zines/reference.md` — landmark article table with URLs.

### Tier 4 — history depth

The `history.md` files. Lowest priority because they're for after-the-con
reading, not for playing. Do these when momentum permits.

---

## Conventions to enforce as the corpus grows

Small things, but they'll matter at N=100 files.

- **One idea per file.** The MANIFEST already says this; the split
  above operationalizes it.
- **Cite sources at the bottom of every file.** `fax/README.md`'s
  bibliography style is the model.
- **`[[topic/name]]` cross-links liberally.** Especially between the
  four file types within a topic — `README.md` should link to its own
  `reference.md` and `walkthrough.md`.
- **Every walkthrough includes timing.** "Wait ~200 ms. Now you hear
  X." A walkthrough without timing is a story, not a reference.
- **Every recognition file leads with the 15-second triage.** "If in
  the first 15 seconds you hear …" — matches how the assistant will
  actually use it.
- **No operational-fraud framing.** The MANIFEST's ethos rule stands:
  historical/CTF framing only. A `walkthrough.md` for red-boxing
  describes 1993, not last Tuesday.
- **Filename slugs stay lowercase-with-dashes.** Filename becomes the
  MCP resource name; drift here breaks tool paths.

---

## Estimated effort

Rough, assuming the writer already knows the material:

| Tier | Files | Hours |
|---|---|---|
| 1 (operational must-haves) | 7 | 4-6 |
| 2 (new topics) | ~12 | 6-8 |
| 3 (depth on existing) | 7 | 3-4 |
| 4 (history) | up to 10 | 4-6 |

Total ~20 hours to bring the whole corpus to `fax/`-level depth across
the board. Tier 1 alone (~5 hours) closes the biggest CTF-utility gap.

---

## Suggested execution order

1. **Write Tier 1 first.** Those seven files unblock the co-pilot for
   the con.
2. **Publish Tier 2 next.** New topics are additive, low-risk, and
   pair naturally with `docs/ctf_playbook.md` and `docs/call_recipes.md`
   (see `plan-organize.md`).
3. **Backfill Tier 3.** Rounds out the existing topics.
4. **Tier 4 is optional.** History files are for after-hours reading.

Between tiers, run `list_topics` and `search_lore` against realistic
CTF prompts and watch what the assistant reaches for. Anywhere it
falls back to memory instead of the corpus is a signal about what to
write next.
