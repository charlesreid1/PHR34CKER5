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

---

## Corpus discipline — a KR, not a wiki

Everything above treats `knowledge/` as prose. That works for the
`README.md` / `walkthrough.md` / `history.md` layer, but the
**`reference.md`** layer needs to be a *typed, dated knowledge
repository* (KR) if the assistant is going to answer DEFCON-grade
questions without hedging. This section spells out the discipline;
Tier 1/2/3 fills above should follow it as they're authored.

### Design principles

1. **Everything is a typed, dated record.** No prose blobs. Each record
   in a `reference.md` file (or an accompanying JSON sidecar) has:
   `id`, `name`, `aliases[]`, `category`, `first_effective`,
   `last_effective`, `regions[]`, `signaling_layer`, `preconditions[]`,
   `citations[]`, `technical_body{}`, `disputed{}`, `see_also[]`.
2. **Frequencies, timings, levels, and codes are numbers, not
   adjectives.** "About 2600 Hz" is a defect. "2600 Hz ± 15 Hz, ≥ 300 ms
   continuous, at −10 dBm0" is a record.
3. **Region matters.** North American in-band signaling (SF/MF R1) is
   not the same system as ITU-T R2 (used in Latin America, parts of
   Asia/Europe), and neither is CCITT No.5. A US blue box does not work
   on a European trunk. A record MUST bind facts to one signaling
   family.
4. **Layer matters.** Subscriber-loop signaling (DTMF, loop-start,
   ANI-II, CPC), CO-to-CO in-band trunk signaling (SF, MF), CO-to-CO
   out-of-band (CCIS/SS6, SS7), and OA&M (E&M, C.O. maintenance ports,
   LMOS, MIZAR, SCCS, COSMOS) are separate namespaces. Cross-layer
   confusion is the #1 source of bullshit.
5. **Vulnerability window is a first-class field.** Every "trick" has a
   date it stopped working somewhere. Blue boxing died in the US as
   trunks migrated from SF/MF to SS7 (mostly 1985–1990 on interoffice,
   straggler independents into the mid-90s). Red boxing died as
   ACTS-equipped payphones were replaced with "smart" (COCOT / post-pay)
   sets by the late 90s but persisted on Bell-owned single-slot phones
   until ~2001–2002. If you tell a DEFCON audience "blue box works"
   without a date and a region, you will be laughed out of the room.
6. **Ambiguity is explicit.** If community lore contradicts a Bell doc,
   both are captured with provenance and the discrepancy is flagged in
   `disputed{}`. Never silently pick a side.
7. **Deprecation ≠ deletion.** The KR keeps deprecated codes; it labels
   them `last_effective` and `retirement_cause`. DEFCON attendees will
   ask "did 10-XXX still work in 1999?" — the answer is "10-XXX was the
   pre-1998 form; PIC dialaround became 10-10-XXX (1010XXX) in the
   July 1998 Carrier Identification Code expansion from 3 to 4 digits
   per FCC 97-402".

**Cutoff era covered:** ~1988 (SS7 rollout starts in earnest in the US)
through ~2005 (last widespread in-band CO trunks in North America gone;
AMPS shutoff mandated Feb 2008). Focus window: **1995–2003**.

### Top-level ontology

Categories the corpus MUST index (each maps to a `knowledge/<topic>/`
directory or a category tag on records):

- `signaling_system` — SF, MF R1, R2 (both variants), CCITT No.5, No.6
  (CCIS), No.7 (SS7/C7), DTMF (Q.23), MFR2, E&M types I–V, loop-start,
  ground-start, reverse-battery, ANI wink/spill.
- `tone_signal` — every discrete tone or tone-pair used, with exact
  freqs (Hz), tolerance, level (dBm0), and on/off timing (ms).
  Cross-referenced to `signaling_system`.
- `box` — the "colored box" catalog. Each has: what it emits, what
  layer it attacks, when/where it worked, and the physical device
  generating it.
- `network_element` — CO switch families (1ESS, 1AESS, 2ESS, 4ESS,
  5ESS, DMS-10/100/200/250, EWSD, GTD-5 EAX, Nortel SL-1/Meridian PBX),
  tandems, TSPS/TOPS operator systems, ACD, OSPS.
- `numbering_plan` — NANP structure, N11 codes, N0X/N1X history, area
  code splits/overlays, LATA structure, ANI-II digits, Feature Group
  A/B/C/D access, 950-XXXX, 10XXX/101XXXX CIC dialaround.
- `operator_and_service_code` — CN/A, LMOS, MIZAR, LOOP-arounds,
  ringback, ANAC per NPA, 200/958/959 test codes, Milliwatt (1004 Hz
  test tones), silent termination.
- `payphone_system` — ACTS coin signaling, red box tones, coin relay
  control, Northern Telcom Millennium vs. Bell 1C/1D single-slot vs.
  COCOT.
- `cellular_system` — AMPS (control channel structure, ESN, MIN, SID,
  RSSI cloning), CDPD, TDMA IS-54/136, GSM (SIM, IMSI, Ki, A5/1, A5/2,
  A3/A8, COMP128 flaw), CDMA IS-95.
- `pbx_and_voicemail` — DISA abuse, default admin codes for Meridian
  Mail, Audix, Octel, VMB, Rolm/Siemens, Toshiba Strata, Panasonic
  KX-TD.
- `data_network` — X.25 PADs, NUAs, Sprintnet/Tymnet/Datapac, ITI
  dial-outs.
- `technique` — "how to accomplish X"; a technique composes signals,
  boxes, and network elements.
- `defense_and_detection` — CAMA, AMA, tone-scan traps, SS7 side-
  channel, blue-box-detect on 1ESS/4ESS, USSS/DoJ "Operation Sundevil"
  era prosecutions (for historical framing).
- `bibliography` — canonical sources with pinpoint cites.

The knowledge-retrieval MCP tools (`lookup_tone`, `explain_technique`,
`verify_claim`, etc., specified in `plan-organize.md` Phase 3) bind to
these categories. Every tool response carries the envelope
`{citations[], era_bounds, region, confidence ∈ {primary, secondary,
community, folklore}}`.

---

## Technical fill material — what each Tier 1/2 file must cover

The tier list above says *which files to write*. This section says
*what to write in them*. All frequencies, timings, and dates are
load-bearing — if the assistant hedges, the KR failed.

### Signaling systems (feeds `2600hz/`, `blueboxing/`, and a new `signaling/` or `international-signaling/` topic)

#### SF (Single-Frequency) supervision — the "blue box" foundation

- **Frequency:** 2600 Hz ± 15 Hz.
- **Function:** Idle/on-hook indication on a 4-wire analog inter-office
  trunk (North American Bell system). Presence of tone = trunk idle.
  Removal of tone by the far-end CO = seizure. Reapplication by the
  near end after answer = disconnect.
- **Level (nominal, per BSTJ Nov 1960, Weaver & Newell "In-Band
  Single-Frequency Signaling"):** −20 dBm0 during idle guard, −8 dBm0
  during pulsing (some carriers −6 to −10).
- **Blue-box attack:** After the called party's CO returned answer
  supervision, the phreak plays 2600 Hz into the audio path for ≥ ~700
  ms (varied by CO: 4ESS wanted ≥ 400 ms, some 1ESS installations
  required ~650 ms, most sources cite 750–1000 ms as safe). The
  originating tandem interprets this as far-end on-hook and drops the
  trunk to a "wink" idle state while the phreak's local loop stays up.
  The phreak then MF-pulses (see below) a new destination as if they
  were an operator/originating tandem.
- **Died when:** Inter-office trunks migrated to CCIS (No.6) and then
  SS7, moving supervision out-of-band. AT&T Long Lines completed CCIS
  deployment on major routes by the early 1980s; independent telcos and
  small tandems ran SF/MF into the mid-1990s. **A properly conditioned
  blue-box call was already impractical on major US routes by 1990.**
- **Detection:** "2600 Hz hold time exceeded" alarms shipped in 1AESS
  generic 1AE7+ and 4ESS. AT&T's "greenstar" (later
  "greenstar/blueflag") program logged suspicious 2600 patterns
  starting 1970s.
- **Sources:** BSTJ Nov 1960 v39 pp. 1319–1408; Bell Labs Record Feb
  1976 "SF Signaling on Toll Trunks"; Ron Rosenbaum "Secrets of the
  Little Blue Box", Esquire Oct 1971 (historical, not technical
  primary); Phrack #4 file 4 (LOD/H technical journal treatment); GTE
  Automatic Electric TP-401 SF signal set docs.

#### MF R1 (Multi-Frequency, North American) — the "blue box" pulsing tones

Two-of-six frequency pairs, distinct from DTMF. **Do not confuse with
DTMF (Q.23) or R2 MF (Q.441/ITU).**

- **Frequency set:** 700, 900, 1100, 1300, 1500, 1700 Hz.
- **Digit pairs (undisputed):**
  - 1: 700 + 900
  - 2: 700 + 1100
  - 3: 900 + 1100
  - 4: 700 + 1300
  - 5: 900 + 1300
  - 6: 1100 + 1300
  - 7: 700 + 1500
  - 8: 900 + 1500
  - 9: 1100 + 1500
  - 0: 1300 + 1500
  - KP (Key Pulse, "start of address"): 1100 + 1700
  - ST (Start, "end of address" terminator): 1500 + 1700
- **Control-code pairs (DISPUTED — three sources, three ways to name
  the same six frequencies).** The corpus records this as a three-column
  table and never resolves it silently:

  | Frequencies | BSTJ 1960 (Weaver & Newell, v39 pp.1319–1408) | Bellcore TR-NPL-000275 / later Bell Labs docs | Community canon (Phrack #4/4, Phrack #16, 2600 catalogs, LOD/H "The Blue Box and Ma Bell") |
  |---|---|---|---|
  | 700 + 1700 | **Code 11** (unnamed control) | **ST3P** (also written "ST3-prime") | Often called **ST''' ("ST three-prime")** or **Code 11** in early phreak files; some 90s tutorials mislabel this as "KP2" |
  | 900 + 1700 | **Code 12** (unnamed control) | **ST2P** ("ST two-prime") | **ST''** or **Code 12**; some phreak files write this as "STP" |
  | 1100 + 1700 | **KP** (single KP, all addresses) | **KP1** (domestic KP) | **KP** (domestic) |
  | 1300 + 1700 | Not used as a control code in BSTJ 1960 | **KP2** (international / special-routing KP) | **KP2** (international); occasionally mislabeled "KP'" |
  | 1500 + 1700 | **ST** (single ST terminator) | **ST** (domestic terminator) | **ST** |
  | 1700 + 1700 | n/a (invalid pair) | n/a | n/a |

  **What actually disagrees:**
  1. **BSTJ 1960 has one KP and one ST.** The two "extra" 1700-Hz
     combinations at 700+1700 and 900+1700 are called Code 11 and Code
     12 without semantic names. The concept of "KP2 for international"
     does not appear in the 1960 paper — international operator MF was
     documented later.
  2. **Bellcore TR-NPL-000275 (and later Bell docs)** promote the
     paired system: KP1 (domestic) and KP2 (international/special) at
     1100+1700 and 1300+1700, plus a family of ST variants (ST, ST2P,
     ST3P) at 1500+1700 / 900+1700 / 700+1700 used to signal call type
     / operator class / charging instructions to the far-end register.
  3. **Community canon in Phrack/2600/LOD-H files** freely mixes the
     two naming schemes: prime-notation (ST', ST'', ST''') is used
     interchangeably with numeric-suffix notation (ST2P, ST3P), and
     some early files call 1300+1700 "KP'" or even reuse "KP2" to mean
     700+1700. This is the most common source of DEFCON-trap wrongness.

  **Rule:** every MF record with a control code MUST specify (a) the
  numeric frequency pair, (b) the source-scheme naming, and (c) which
  of the three columns above the naming is drawn from. Answering "KP2
  is 1300+1700" without qualifying "in Bellcore/later-Bell notation" is
  a defect. Answering "KP2 is 700+1700" is not automatically wrong
  either — it's community-canon wrong-but-widespread and must be
  flagged as such.
- **Tolerance:** ±1.5% of nominal, per Bell Labs TR-NPL-000275.
- **Level:** −7 dBm0 per frequency; total pair power −4 dBm0.
- **Timing:** KP = 100 ms ± 10 ms on; digits = 60–75 ms on, 60–75 ms
  off; ST = 60–75 ms; inter-digit gap 60–75 ms. On 4ESS/CAMA trunks,
  KP was 100 ms; on some CCIS trunks KP was extended to 120 ms.
- **Address format sent by an originating toll office:** `KP +
  [3-digit prefix or 0/1 nature-of-address digit sequence] + 7 or 10
  digit called number + ST`. Blue-boxing internationally: `KP + 011 +
  CC + NN + ST` on international-capable trunks, though most consumer
  2600-attacks used domestic 7- or 10-digit MF.

#### CCITT No.5 (international MF signaling)

- **Line signals ("supervision"):** two tones — **2400 Hz and 2600 Hz**,
  used singly and in combination. Seizure = 2400 Hz; proceed-to-send =
  2600 Hz; answer/clear-back/clear-forward encoded as pulse patterns of
  2400+2600. This is what enabled the "international blue box" ("Chevy
  Chase, Maryland" ops on TAT-6/TAT-7 in the late 70s/early 80s).
- **Inter-register (address) signals:** the No.5 MF register set is the
  **same** as R1 MF (700–1700). Sequence: KP + digits + ST.
- **Died when:** No.5 trunks were converted to CCITT No.6 (CCIS) and
  No.7 in the 80s. Persisted on some third-world routes into the 90s;
  last widely-reported vulnerable No.5 gateway seizures were on
  Caribbean and African routes into the mid-1990s (community reports;
  primary confirmation weak — mark `disputed_persistence`).
- **Distinction to encode:** in No.5, 2400 Hz is used for seizure — a
  blue-box that only produces 2600 Hz will not seize an international
  trunk. This is a common CTF gotcha.

#### R2 (ITU-T Q.400 / Q.441) — Latin America, Iberia, parts of Asia

- **Line signaling (R2 analog):** compelled tones at 3825 Hz (forward)
  and 3825 Hz (backward), OR digital line signaling in R2-D over PCM.
  NOT 2600 Hz — do not confuse.
- **Inter-register:** MFC (Multi-Frequency Compelled). Forward tones:
  1380, 1500, 1620, 1740, 1860, 1980 Hz (two of six). Backward tones:
  1140, 1020, 900, 780, 660, 540 Hz (two of six). Meaning of each
  combo is context-dependent (Group I/II forward, Group A/B backward).
  Any record about R2 MUST specify the group.
- **Where used:** Mexico, Brazil, Argentina, China (variant),
  Philippines, Spain (until digital), Malaysia. R2 vulnerability
  lingered longer than R1 in these regions — into the late 90s in some
  LATAM operators.

#### CCIS (No.6) and SS7 (No.7)

- **Key property that killed in-band phreaking:** signaling moves to a
  separate data channel (56/64 kbps) between STPs. A 2600 Hz tone in
  the voice path is now just audio to the far end; it does not affect
  call state. This transition, more than any legal action, is what
  ended classical blue boxing.
- **Rollout dates:** SS7 in the AT&T network began 1980 (CCIS/No.6),
  transitioned to No.7 in the mid-80s; ANSI SS7 standardized 1988;
  ubiquitous on interoffice trunks in North America by ~1992.
- **Phreak relevance:** SS7 introduces its own class of attacks (SCCP,
  TCAP, MAP, CAMEL, Global Title spoofing) that became public research
  topics ~2008 onward (Tobias Engel, 25C3). These are OUT of scope for
  a "late 90s / early 00s phreaking" repo but SHOULD be flagged as
  `see_also` for era completeness.

#### DTMF (Q.23) — the subscriber tones

- **Frequency pairs:** low 697/770/852/941 Hz, high 1209/1336/1477/1633
  Hz. Digits 0–9, *, #, and A/B/C/D (1633 Hz column, used in
  mil/AUTOVON precedence — "FO", "F", "I", "P" = Flash Override, Flash,
  Immediate, Priority).
- **Timing per Q.24:** minimum on 40 ms, minimum off 40 ms, receiver
  must accept up to 100 ms on. Twist (level difference high vs. low
  pair) ≤ 4 dB.
- **AUTOVON precedence relevance:** the A/B/C/D column is trivia in
  the civilian world but is a real historical footnote — DEFCON
  audiences will ask, and a wrong answer ("D is for hangup") is a red
  flag. The corpus must have precise AUTOVON precedence codes
  (see Appendix D.3 below).

### The "colored boxes" — canonical catalog (feeds `knowledge/<box>/` topics)

Each box record has: `color`, `attacks_layer`, `emits`, `power_source`,
`works_on{region, era}`, `died_because`. Include **at minimum** the
following; historic community lists include 40+ "boxes" but most are
jokes or non-functional. Only the technically load-bearing ones are
must-haves:

- **Blue box** — emits 2600 Hz + MF R1. Attacks CO trunk supervision.
  Died with SS7 rollout.
- **Red box** — emits ACTS coin-deposit tones (see payphones section).
  Attacks payphone coin signaling to CO. Died as ACTS was retired /
  replaced by post-pay smart phones (Bell single-slots: ~2001; COCOTs:
  never had this vuln).
- **Black box** — DC circuit across the called party's loop that
  prevents answer supervision from being returned to the originating
  CO, so the caller is not billed. Attacks loop-current-reversal answer
  signaling. Died with the shift to CCIS/SS7 answer supervision (the
  answer signal is out-of-band, so keeping the local loop off-hook
  doesn't matter). Also fully dead once the far-end office is a digital
  switch reporting answer via SS7 ISUP ANM.
- **Green box** — operator-tones emitted **from the coin phone side**
  (coin collect 700+1100 Hz "KP-style", coin return 1100+1700 Hz,
  ringback ~) to spoof the TSPS operator on the far end into thinking
  coins were collected. Distinct from red box. Worked mostly against
  operator-attended coin-toll routing.
- **Beige box** (aka "bud"/"lineman's mate") — a simple butt set or
  hand set with alligator clips, allowing subscriber-line access at a
  B-box or NID. Not a signaling attack; a physical access tool. Still
  works today on any twisted-pair POTS drop.
- **Cheese box** — a device installed at a residence that bridged two
  lines and repeated audio, historically used to run bookmaking
  operations remotely. Physical/wire, not signaling.
- **Silver box** — DTMF pad with A/B/C/D column (AUTOVON precedence)
  added. Not an attack by itself; useful only if you're already on a
  network that honors those keys (AUTOVON, some old test lines, some
  PBXs).
- **Aqua box** — attempted to defeat FBI "line lock" hold on a dialed
  line by draining voltage. Community-reported; primary technical
  validity **disputed**. Flag as folklore.
- **Chartreuse box** — powers a device off telco 48 V loop battery.
  Not an attack.
- **Gold box** — DTMF relay/loop-through box for extending a call
  through an unattended phone (used with loop-arounds). Combined with
  a black-box function.
- **Rainbow box** — nickname for a portable tone generator that
  produced any of the above.
- **Diverter attack** (not a color) — an "extender" or "diverter" is a
  business-owned device that answers on one line and dials out on
  another; phreaks would call the business after-hours, receive dial
  tone, and place free long-distance calls billed to the business.
  Very common late-80s to mid-90s attack, aided by DISA-enabled PBXs.
  Countered by dial-out CoS restrictions.

**Rejected as folklore** (record them but flag `folklore: true`):
pearl box, plaid box, mauve box, and most other joke colors from
various boxes-list files circulated on BBSes. Their inclusion in a
DEFCON answer without the folklore flag is a credibility hit.

### Numbering plan and dialing sequences (feeds a new `knowledge/numbering/` topic)

NANP-centric, era 1995–2003.

#### Structure

- NANP number: NPA-NXX-XXXX. Pre-1995: N ∈ {2–9}, second digit of NPA
  ∈ {0, 1} (so area codes were N0X/N1X); NXX prefix second digit
  ∈ {2–9}. On **Jan 15, 1995** interchangeable NPA codes were
  introduced (second digit of NPA can be 2–9) — this is why 334, 360,
  520 appear. Corpus must have this exact date.
- N11 codes: 211, 311, 411, 511, 611, 711, 811, 911 all reserved; 911
  nationalized 1968, 311 (non-emergency) allocated 1997, 211
  (community) 2000, 511 (traveler) 2000, 711 (TRS) 2000, 811 ("call
  before you dig") 2005.
- 950-XXXX: Feature Group B carrier access, subscriber-dialable,
  1984–late 90s. Reached alternate long-distance carriers. Largely
  obsolete after 10XXX/1010XXX dialaround (Feature Group D)
  generalized.
- 10-XXX ("equal access dialaround") became **101-XXXX** on July 1,
  1998 per FCC 97-402 to expand CICs from 3 to 4 digits (10-10-XXX
  form). Callers dialed 101-0288 (AT&T), 101-0222 (MCI), 101-0333
  (Sprint), etc., before 1+NPA+NXX+XXXX.

#### ANI-II ("info digits")

Two-digit code sent by the originating office on Feature Group D
trunks (and captured by 800-number ANI delivery). Full table in
Appendix B below. Reference: Bellcore GR-317-CORE (Switching System
Requirements for CCS Call Control, esp. Feature Group D signaling)
and Telcordia SR-2275.

#### CO test and utility numbers (per-NPA/CO — not universal)

- **ANAC (Automatic Number Announcement Circuit)** — reads back the
  calling number. Per-CO. Well-known 90s codes:
  - 958 (most Pacific Bell)
  - 200-222-2222 (many Bell Atlantic offices)
  - 311 (some GTE offices, pre-311-N11 assignment)
  - 311-1111 (some Southwestern Bell)
  - 200-XXXX (varies)
  - 1-800-MY-ANI-IS (958-6480 spelled) — commercial, still works in
    some places
  - The corpus MUST NOT assert a single universal ANAC. Records are
    per-NPA / per-CO family.
- **Milliwatt test tone (1004 Hz at 0 dBm, on continuously)** — used
  to verify line loss. Reachable at NPA-XXX-1111 in many offices
  (e.g., 959-1111 in DMS regions).
- **Loop-around (LP1/LP2)** — a matched pair of numbers that connect
  two callers to each other; often at 99XX suffixes on a 95X or 99X
  prefix (widely varied). Used for anonymous meet-ups pre-Internet.
- **Ringback** — dial a code, hang up briefly, phone rings. In many
  step-by-step and 1ESS offices: dial 660 + last 4 of your own number,
  or NPA-571 / 511 / 320 codes; **highly office-dependent**. Ringback
  disappeared as SS7/5ESS features replaced maintenance shortcuts.
- **CN/A (Customer Name and Address)** — telco-internal lookup
  bureaus. Phreaks obtained CN/A numbers per-region (each RBOC had its
  own set) via social-engineering. Corpus should NOT publish current
  CN/A numbers even historically-known; instead record the *concept*
  and the historical era they were phreak-relevant.

#### Test/reserved prefixes

- **555**: historically reserved by NANPA; 555-1212 = directory
  assistance across all NPAs. 555-0100–555-0199 reserved for fictional
  use (movies/TV) since 1994 (per Industry Numbering Committee).
- **Prefix 958/959**: reserved test in many regions.
- **NPA 700**: carrier-specific services (Feature Group D). 1-700 +
  carrier code reached that carrier's info line. AT&T's was
  1-700-555-4141 which announced "You have reached AT&T" — used to
  verify default long-distance carrier.
- **NPA 500**: personal communication service (follow-me numbers),
  1994.
- **NPA 600**: Canadian non-geographic.
- **NPA 900**: premium.
- **NPA 976**: not an NPA — a legacy per-NPA local premium prefix.
- **NPA 800/888/877/866/855/844/833/822**: toll-free, added over time
  (888 in 1996, 877 in 1998, 866 in 2000, 855 in 2010, 844 in 2013,
  833 in 2017, 822 reserved).

### Payphones and red-boxing — the ACTS canon (feeds `redboxing/`)

#### ACTS (Automated Coin Toll Service, Bellcore, 1978 rollout)

The pre-payment automated system that removed operators from most
coin-toll transactions. The payphone reports coin deposits by sending
a **pair of 1700 Hz + 2200 Hz tones** back to the CO, encoded as pulse
patterns.

- **Frequencies:** 1700 Hz + 2200 Hz simultaneously (played together,
  not alternated), ±1.5% tolerance.
- **Level:** −7 dBm0 per frequency (nominal, per Bellcore/Bell
  payphone-loop docs).

**Timing — TWO SOURCES DISAGREE. Both are in wide use; the corpus
records both.**

| Coin | Bellcore GR-506-CORE (1996, p.249) [PRIMARY] | Phrack 33.9 "A REAL Functioning RED BOX Schematic" — J.R. "Bob" Dobbs, Sept 1991 [COMMUNITY CANON] |
|---|---|---|
| Nickel (5¢) | One 66 ms tone burst | One 60 ms pulse |
| Dime (10¢) | Two 66 ms tone bursts separated by 66 ms | Two 60 ms pulses separated by 60 ms |
| Quarter (25¢) | Five 33 ms tone bursts separated by 33 ms | Five 35 ms pulses separated by 35 ms |
| Dollar ($1) | One 650 ms tone burst (rare — not universally implemented on all ACTS installations) | Not documented |

**Which one is "correct"?** GR-506-CORE is the primary
Bellcore/Telcordia spec and is what a compliant ACTS coin-receiver in
an SxS/1ESS/1AESS/4ESS/DMS local was tuned to detect at the switch
end. **The 66 ms / 33 ms figures are the authoritative telco-side
timing.** Phrack 33.9's 60/35 ms numbers are what an entire generation
of homebrew red boxes actually emitted, and they worked because real
ACTS receivers tolerated ±10–20% timing slop for coin-signal detection.
Both a 60 ms tone and a 66 ms tone would be accepted as "nickel."
Community tutorials from 1985–2005 overwhelmingly repeat 60/35, which
is why the numbers are so widespread despite disagreeing with GR-506.

**DEFCON-answer rule:** if asked "what timing does ACTS spec," answer
66 ms / 33 ms and cite GR-506-CORE. If asked "what did red boxes
actually emit," answer 60 ms / 35 ms and cite Phrack 33.9. Never
conflate them.

A red box is any tone generator emitting the 1700+2200 Hz pair with
the correct pulse timing.

#### The Radio Shack tone-dialer crystal swap — canonical homebrew red box

**What it is.** A stock Radio Shack pocket tone dialer, modified by
desoldering its 3.579545 MHz "colorburst" crystal and soldering in a
**6.5536 MHz** crystal in its place. The dialer's DTMF-generation chip
clocks all its output frequencies as ratios of the reference crystal,
so replacing the crystal scales every generated tone by the same
factor.

**The two canonical dialer models (both work identically):**
- **Radio Shack Cat. No. 43-141** — the original 33-Memory Pocket Tone
  Dialer used in Noah Clayton's article in **2600 Magazine, Vol 7 No 3
  (Autumn 1990)**, the piece that popularized the mod. Retailed for
  $24.95. Uses three AAA batteries.
- **Radio Shack Cat. No. 43-146** — the direct successor after Radio
  Shack discontinued the 43-141 on **1994-01-01**. Same $24.95 price,
  same three-AAA power, same crystal-swap procedure. Documented in
  Atomic Teddybear's June 1994 update file "Converting a Tone Dialer
  into a Red Box" (BGR/HCH/NATAS, mirrored at textfiles.com).

**Why 6.5536 MHz?** The scaling ratio is 6.5536 / 3.579545 ≈ **1.831**.
The DTMF chip's internal divider chain multiplies its output
frequencies by this factor unchanged. The DTMF "*" key (low group 941
Hz, high group 1209 Hz) therefore emits:
- 941 Hz × 1.831 ≈ **1723 Hz** (target: 1700 Hz — inside ±1.5% ACTS
  tolerance)
- 1209 Hz × 1.831 ≈ **2213 Hz** (target: 2200 Hz — inside ±1.5% ACTS
  tolerance)

That is the sole reason the ratio was chosen. Every OTHER key on the
dialer also gets scaled by 1.831 but none of those scaled pairs land on
anything a telco cares about. As a side-effect the modified dialer can
no longer generate normal DTMF — you trade "phone-dialing" for
"ACTS-emulating."

**How to actually use the modified dialer (from 2600 Autumn 1990 /
Atomic Teddybear 1994):**
1. Slide switch to **STORE** mode.
2. Press MEMORY.
3. Press **`*` five times** (this stores five 1700+2200 Hz bursts —
   one quarter).
4. Press MEMORY again, then a memory slot key (P1/P2/P3).
5. Slide switch back to **DIAL** mode.
6. Pressing the stored memory slot plays back the five bursts at the
   dialer's default DTMF timing (roughly 100 ms on, 100 ms off — closer
   to 33 ms than 66 ms after the crystal retune scales the DTMF timing
   generator as well).

Community canon programs P1 = four quarters ($1.00) with PAUSE between
each set of five, P2 = two quarters (50¢), P3 = one quarter (25¢).

**Where it worked:** any ACTS-equipped payphone whose in-band 1700+2200
Hz coin-tone receiver was on the toll switch (i.e., the pre-Millennium,
pre-COCOT Bell single-slot payphone). Died as ACTS trunks were retired
/ replaced by digital coin phones with local coin validation (Bell
single-slots retrofit 1996–2001; Nortel Millennium never had the vuln).

**Sources:**
- 2600 Magazine, Vol 7 No 3, Autumn 1990, "Converting a Tone Dialer
  into a Red Box" — Noah Clayton. Original publication of the 43-141
  crystal-swap procedure.
- "Converting a Tone Dialer into a Red Box" — Atomic Teddybear
  (BGR/HCH/NATAS), 1994-06-14. Documents the transition from 43-141 to
  43-146 after Radio Shack discontinued the original model.
- Phrack 33.9 (Sept 1991) "A REAL Functioning RED BOX Schematic" —
  J.R. "Bob" Dobbs. Independent from-scratch 555/556-based schematic,
  no dialer required.

**Legal-history note.** The **Bernie S / Ed Cummings 1995 USSS case**
turned on possession of a Radio Shack pocket tone dialer with a 6.5536
MHz crystal. USSS argued this constituted a "device...primarily useful
for the purpose of the surreptitious interception of...electronic
communications" and/or a "counterfeit access device" under **18 USC
1029**. Cummings was convicted and imprisoned. This case is a canonical
piece of DEFCON telco-history and a reason to *never* physically carry
a modified dialer through security.

The tones must be played into the payphone's mouthpiece while off-hook
to the ACTS-controlling toll switch in a way that reaches the switch's
coin-signal receiver on the 4-wire toll trunk (not on the local 2-wire
loop).

- **Died because:**
  1. Bell single-slots migrated to **T1/robbed-bit** trunks that
     stripped in-band ACTS supervision.
  2. **COCOTs** (Customer-Owned Coin-Operated Telephones) were never
     ACTS — they collect coins locally and post-pay; red-boxing never
     worked against them.
  3. Bell-owned payphones were retrofitted or replaced with intelligent
     phones (e.g., Millennium in Canada) that generated ACTS locally in
     the phone's own DSP and validated deposits with an internal coin
     optical/mass sensor before signaling — mid-to-late 90s.
  4. RBOC divestitures of payphone operations (2000–2007) accelerated
     retirement.
  5. By 2002 red box attacks were largely inert in North America.

#### Green-box tones (feeds `greenboxing/`)

Operator-side coin control signals from TSPS to the payphone:

- **Coin collect:** 700 + 1100 Hz for 900 ms
- **Coin return:** 1100 + 1700 Hz for 900 ms
- **Ringback:** 700 + 1700 Hz for 900 ms
- **Operator attached:** 700 + 1700 Hz burst pattern
- **Coin totalizer test:** varied

A green box plays these from the caller side to spoof the coin-relay,
which is why it is distinct from a red box. Practical usefulness in the
field was limited because these signals were normally sent from the
toll switch toward the coin phone; injecting them into the calling
loop only worked in specific topologies (four-wire operator trunk with
poor filtering).

#### Common myths to explicitly refute

- "You can red-box a modern payphone." No — post-COCOT and
  post-Millennium coin acceptance is locally validated.
- "Any DTMF dialer is a red box." No — the crystal or DSP tables must
  be reprogrammed to emit 1700+2200; a stock DTMF chip cannot.
- "ACTS quarter tones are 5 pulses of 66 ms." NO — a quarter is FIVE
  pulses at ~33 ms ON / ~33 ms OFF (per Bellcore GR-506-CORE) or ~35
  ms per Phrack 33.9. The 66 ms cadence is the NICKEL/DIME timing;
  conflating the two is the classic DEFCON trap.
- "The dollar coin tone is 5 × 66 ms." NO — per GR-506-CORE the dollar
  is a single 650 ms tone, and it wasn't universally implemented
  anyway.
- "Red boxes work off a modified colorburst crystal." Not quite — the
  modification is REPLACING the 3.579545 MHz colorburst crystal with a
  **6.5536 MHz** crystal in a Radio Shack pocket tone dialer (Cat.
  No. 43-141 through end-of-1993; Cat. No. 43-146 after). See the
  Radio Shack section above.

### Operator, test, and internal-services surface (feeds a new `knowledge/operator-services/`)

#### TSPS / TOPS / OSPS

- **TSPS (Traffic Service Position System, Western Electric, 1969):**
  operator platform for coin/toll/collect. Later replaced by **TOPS
  (Nortel DMS-based)** and **OSPS (5ESS-based)**.
- Key relevance to phreaks: operator consoles had **verify (busy-
  verify)** and **emergency interrupt (EI)** functions, both of which
  allowed operators to bridge into any subscriber's line. Social-
  engineering the operator into performing an EI on a target line was
  a common technique.

#### Loop-arounds

A "loop-around" is a pair of test numbers (LP1/LP2) that terminate on
a milliwatt tone individually but when both are seized (one from each
end) audio is looped between the callers. Historical use: anonymous
meetups pre-BBS. Numbers vary per CO — canonically prefix 95X or 96X
with 99XX suffix. Do NOT hardcode "the" loop-around number; record the
concept and per-NPA discovery method (call the milliwatt at the alleged
LP1; if a second caller shows up, you're on a loop-around).

#### Diverters and extenders

- **Diverter:** a business PBX/answering machine that answers, times
  out, and returns second dial tone from an outbound trunk. Phreaks
  scanned XXX-XXXX ranges in a small city looking for after-hours
  businesses that answered with dial tone.
- **Extender (PBX DISA):** dial an 800 number that fronts a corporate
  PBX; enter authorization code (often 4–6 digits, brute-forceable);
  receive dial tone and dial anywhere. Common attack 1985–1998; drove
  the ~$4B/yr US PBX-fraud figure the ITU cited in 1996.

### PBXs, voicemail, and default credentials (feeds a new `knowledge/pbx/` and `knowledge/voicemail/`)

The corpus carries a table of well-documented default admin passwords
and system-manager mailboxes for the systems that were phreaker-
relevant during 1995–2003. This is public knowledge (vendor manuals,
historical Phrack articles) and load-bearing for CTF authenticity.

Representative entries (author full table + citations):

- **Meridian Mail (Nortel):** default system administrator mailbox
  often mailbox #0 or 999999, default password 0000 or the mailbox
  number.
- **Octel (Overture):** system manager mailbox 9999, default password
  9999.
- **AT&T Audix / Lucent Intuity:** admin mailbox 9999 or 0, default
  password 12345 (older) / mailbox number.
- **Rolm PhoneMail:** admin 0 / password 1234, admin 88 / password
  8756.
- **AVT Rhetorex / Applied Voice Technology CallXpress:** default
  sysadmin credentials in vendor doc.
- **Panasonic KX-TVS / KX-TD:** default 1234 (system) / mailbox 998.
- **Toshiba Stratagy:** default sysadmin mailbox 983, password 983.
- **Comdial / VODAVI Talkpath:** documented defaults.

Every record includes: default box number, default password, admin
capability once inside (record greeting, DISA out-dial, message
forwarding, outcall notification abuse), and CVE/vendor bulletin
references where available.

Additionally: **DISA out-dial**. If a compromised voicemail supports
"outcall paging" or "call sender", the box can be turned into a poor
man's calling-card. This is a common 90s CTF element.

### Cellular (AMPS → GSM → early CDMA) — the phreak-adjacent era (feeds new `knowledge/cellular/`)

#### AMPS (Advanced Mobile Phone System, IS-3/IS-553, analog, 850 MHz)

- **Channels:** 30 kHz FM, 832 channels per operator across A/B bands.
- **Control channel:** the FOCC (Forward Control Channel) and RECC
  (Reverse Control Channel) send Manchester-encoded 10 kbps data
  alongside SAT tones (5970/6000/6030 Hz) and ST (signaling tone 10
  kHz).
- **Identity:** **MIN (Mobile ID Number, 34 bits, derived from the
  phone's 10-digit MDN)** and **ESN (Electronic Serial Number, 32
  bits, 8-bit manufacturer + 24-bit serial)**. On registration the
  phone sent MIN/ESN in cleartext over the RECC. Anyone with a scanner
  and a decoder box (or a hacked OKI 900, Nokia, or Motorola bag phone)
  could capture and clone.
- **Cloning:** re-program MIN/ESN into a second handset via NAM
  (Number Assignment Module) programming mode. Every AMPS phone had a
  service menu. Well-known entry sequences (record each with model +
  firmware constraints) — see Appendix D.5 below.
- **Defenses:** authentication key ("A-Key") added via IS-54B / IS-136
  (TDMA) and PCS carriers required A-Key exchange starting 1996–1998,
  effectively killing pure clone fraud on properly-provisioned lines.
- **Shutoff:** FCC allowed AMPS sunset **Feb 18, 2008** (US). Analog
  was already largely obsolete in urban markets by 2003; rural
  retention longer.

#### GSM (in North America, 1996+ on 1900 MHz PCS)

- **Identity:** IMSI (in SIM), Ki (128-bit secret in SIM, never
  transmitted), IMEI (device).
- **Authentication:** A3/A8 (implementation-defined, most operators
  used **COMP128-1**, broken by Wagner/Goldberg/Briceno 1998 —
  permitted cloning a SIM given ~150k challenges physically). COMP128-2
  and COMP128-3 followed.
- **Encryption:** A5/1 (Western Europe, US), A5/2 (export, weakened),
  A5/0 (off). A5/1 keystream generator: 3 LFSRs of 19/22/23 bits,
  majority-clock. Barkan/Biham/Keller 2003 published a ciphertext-only
  attack against A5/2. A5/1 practical attacks (rainbow tables) landed
  2008–2010 (Karsten Nohl); pre-2004 A5/1 was still considered "hard"
  outside academia.
- **Corpus MUST NOT** claim A5/1 was broken by 2003 in a practical
  sense; the primary published attacks (Biryukov/Shamir/Wagner 2000,
  real-time on 2 min of ciphertext) required precomputation few had
  done in the wild.

#### CDPD (Cellular Digital Packet Data)

- 19.2 kbps packet data overlaid on unused AMPS channels via
  forward/reverse dedicated channels. Used by early wireless data
  terminals, credit-card readers, PocketNet. Encryption via RC4 with a
  session key derived from a shared secret; MDBS spoofing attacks
  documented.

#### Two-way pagers (Motorola FLEX/ReFLEX)

- FLEX 1600/3200/6400 bps forward, ReFLEX up to 9600. Cap codes
  broadcast in the clear on 900 MHz paging bands. Wide-area monitoring
  possible with a $200 scanner + PC + PDW/POCSAG-decoding software.
  Sensitive info (bank, medical, on-call SRE alerts) travelled
  unencrypted for a decade. This is a huge era-authentic phreak topic.

### Data-network side (Sprintnet/Tymnet/X.25) — 1995–2001 (feeds a new `knowledge/x25/`)

- **X.25 NUAs (Network User Addresses):** 14-digit addresses.
  Sprintnet DNIC 3110, Tymnet 3106, Datapac 3020, PSS (UK) 2342.
  Scanned via PAD-to-PAD `C <NUA>` commands. Full DNIC table in
  Appendix D.4.
- **Dial-up PADs:** 1-800-546-1000 (Sprintnet ~1996), 1-800-937-2862
  (Tymnet). ATDT + `@` (Sprintnet CR) or `.` (Tymnet) after CONNECT.
- **Common phreak-relevant hosts:** DEC VAX clusters, TOPS-20, HP3000
  MPE/iX systems, IBM VM/CMS on X.25 gateways.
- **Died when:** frame relay and IP dial-up (SLIP/PPP) supplanted X.25
  for corporate remote access; most public PADs decommissioned
  2001–2004.

### Switch families — enough to be dangerous (feeds `ess/`)

Each `network_element` record has: manufacturer, first deploy, last
supported OS gen, in-service in NANP through year, phreak-relevant
quirks, and canonical **maintenance modem** access channels.

- **Western Electric / AT&T 1ESS (1965) & 1AESS (1976):** analog-reed
  → digital control. Generic program updates identified as "1AE7",
  "1AE8" etc. Trap/trace and blue-box detection matured through the
  1980s.
- **Western Electric / AT&T 4ESS (1976):** the toll switch. Blue box's
  main victim in the early years, its main killer via detection later.
- **AT&T/Lucent 5ESS (1982):** digital local. TOP command language via
  **RC/V (Recent Change / Verify)** terminals. Craft interface = RCV
  master (RCVMENU). Phreaks who got dialup access to a 5ESS RCV port
  had full switch control. See Appendix D.1 for RCV command surface.
- **Nortel DMS-10/100/200/250:** MAP (Maintenance and Administration
  Position) interface, `MAPCI` command tree. DMS-250 was the toll/
  access-tandem variant. See Appendix D.2.
- **Siemens EWSD:** used by GTE/Sprint; German-origin. Documented in
  Motorola/GTE training manuals from the 90s.
- **AG Communication Systems (AGCS) GTD-5 EAX:** GTE's local switch.
  Distinctive because it kept SF/MF interoperability longer than Bell
  offices.
- **Nortel SL-1 / Meridian 1 (PBX):** the most-phreaked corporate PBX
  of the era. `LD` (load) programs (LD 11 = station admin, LD 21 =
  cust-data print, LD 22 = software list). Access via terminal or
  dial-up modem on the TTY port. Full overlay cheat-sheet in Appendix
  C.

---

## Explicitly disputed / ambiguous entries the corpus must flag

- **MF KP2 / ST' / ST'' / ST''' code mappings:** three distinct naming
  schemes exist for the six 1700-Hz-paired control codes: BSTJ 1960
  (Code 11 / Code 12, single KP, single ST), Bellcore TR-NPL-000275
  (KP1/KP2/ST/ST2P/ST3P), and community canon in Phrack/2600
  (prime-notation, occasionally scrambled). See the three-column table
  under "MF R1" above. Never assert a single "correct" name without
  qualifying the scheme.
- **International blue-box on No.5 vs No.5-BIS vs No.4:** the tones
  and pulse patterns differ. Any record must specify variant.
- **Radio Shack tone-dialer crystal swap:** stock 3.579545 MHz
  (colorburst) crystal replaced with **6.5536 MHz** crystal (scaling
  ratio ≈ 1.831) retunes the internal DTMF chip so the "*" key emits
  ~1723+2213 Hz — inside the ±1.5% ACTS tolerance for 1700+2200 Hz.
  Two canonical dialer models: **Radio Shack Cat. No. 43-141** (2600
  Autumn 1990, Noah Clayton — the original) and **Radio Shack Cat.
  No. 43-146** (Atomic Teddybear 1994-06-14 — the successor after
  43-141 was discontinued 1994-01-01). Some third-hand tutorials
  misstate the crystal, the ratio, or which model — always verify
  against the primary 2600 article or the Atomic Teddybear file.
- **ACTS coin-signal timing (nickel/dime/quarter):** Bellcore
  GR-506-CORE (1996 p.249) says 66 ms / 66 ms / 33 ms; Phrack 33.9
  (Sept 1991) says 60 ms / 60 ms / 35 ms. Both are widely-cited; ACTS
  receivers tolerate the delta. See the ACTS section above for the
  three-way disputed table and DEFCON-answer rule.
- **ANAC universality:** there is no universal ANAC. Any record that
  returns "the ANAC is 958" is defective. Records are per-CO / per-NPA
  and are dated.
- **"C5 works internationally" persistence dates:** community memory
  says the Caribbean and West Africa still had C5 signaling in the
  late 90s. Primary confirmation (ITU-T switching-plan reports) is
  spotty. Mark such claims `provenance: community` and refuse to
  assert them as fact.
- **AUTOVON precedence code assignments in the A/B/C/D column:** A =
  Flash Override (highest), B = Flash, C = Immediate, D = Priority is
  the widely-cited mapping. Some sources reverse D and C. Corpus
  records the DoD MIL-STD-187-100 mapping as authoritative and flags
  the community variant.

---

## Historical/legal framing (era-authentic references)

Every DEFCON talk that lands well anchors technique in the era. The
corpus should carry short, sourced entries for the following (belongs
in `knowledge/zines/history.md` or its own `knowledge/history/`):

- **Operation Sundevil (May 8–9, 1990):** USSS/DoJ raids across 15 US
  cities, ~40 computers seized. Motivator for the founding of EFF.
- **Steve Jackson Games raid (Mar 1, 1990):** SJG v. USSS, 1993
  verdict re: ECPA.
- **Kevin Poulsen "Win a Porsche" KIIS-FM (Jun 1990):** takeover of 25
  KIIS-FM trunks to guarantee being the 102nd caller.
- **Phiber Optik / MOD / LOD "Great Hacker War":** 1990–1992 conflict;
  MOD indictments 1992.
- **Bernie S / Ed Cummings (1995):** possession of a Radio Shack tone
  dialer with the 6.5536 crystal — used as USSS proof of "device to
  defraud" intent; imprisoned; foundational 2600-era case.
- **Kevin Mitnick arrest Feb 15, 1995 (Raleigh, NC).**
- **Bell System Technical Journal Nov 1960:** the article that
  inadvertently taught the world MF R1.
- **AT&T Divestiture Jan 1, 1984:** why "RBOC" is a thing and why
  every RBOC has its own quirks.

---

## Bibliography discipline — pinpoint, not vibes

The corpus ships with a bibliography table (a top-level `knowledge/
bibliography/` topic, or a `bibliography.md` sidecar). Every technical
record cites into this table by ID. Non-exhaustive first-cut:

1. Bell System Technical Journal, Vol. 39 No. 6 (Nov 1960), pp.
   1319–1408 — "In-Band Single-Frequency Signaling" and "Multifrequency
   Pulsing Signals." *The* primary source for R1 MF and SF.
2. Bell Labs Record, various 1960–1978.
3. CCITT Blue Book (1988), Recs Q.310–Q.332 (No.5), Q.400–Q.490 (R2),
   Q.140/Q.180 (No.6), Q.700 series (No.7). Red Book (1984) for earlier
   revs.
4. Bellcore/Telcordia GR-506-CORE (LSSGR: Signaling for Analog
   Interfaces), GR-317-CORE (SS7 Call Control), GR-303-CORE (Integrated
   Digital Loop Carrier), TR-NPL-000275 (MF signaling).
5. Ronald Rosenbaum, "Secrets of the Little Blue Box", Esquire, Oct
   1971 — historical framing, not a technical primary source. Flag as
   `type: journalism`.
6. `2600` Magazine 1984–2005 (specific issues cited per-record).
7. Phrack Inc. issues 1–63 (1985–2005). Specific files cited per-record
   — full phreak-relevant index in Appendix E.
8. Motorola/Nokia/Ericsson OEM service manuals for AMPS handsets (NAM
   programming procedures).
9. FCC Order 97-402 (July 1998, CIC expansion), FCC 03-260 (wireless
   sunset).
10. NANPA numbering-plan letters and INC guidelines.
11. Bruce Sterling, *The Hacker Crackdown* (1992) — historical, not a
    technical primary source.
12. `alt.2600` / `alt.dcom.telecom` archives (Usenet), context-only.
13. cDc / LOD/H technical journals.
14. Cauce/Nohl/Paget/Engel research papers 2007–2010 for the SS7/GSM
    aftermath (out-of-era but linked from era records).

**Every `reference.md` file cites at least one primary source at the
bottom.** `fax/README.md`'s bibliography style is the model.

---

## Build/populate plan (the actual work)

1. **Schema.** Author JSON Schemas (or a documented markdown-frontmatter
   convention) for each record type in the ontology. Enforce
   `citations[]` non-empty at load time. Enforce `era_bounds` as
   `[first_effective, last_effective]` with ISO dates or `null` for
   open-ended.
2. **Seed data.** Hand-author the ~200 core records covering the
   technical fill material above from primary sources. No web-scrape
   auto-generation — every record hand-verified.
3. **Test corpus.** ~100 gold-standard Q/A pairs mined from Phrack,
   2600, DEFCON prior talks (e.g., "Trashing the Phone System",
   "Introduction to Phreaking", DEFCON 4–12 telco tracks). The
   assistant + MCP must answer each correctly.
4. **Adversarial corpus.** ~50 trap questions where the "obvious"
   answer is wrong (e.g., "what frequency does the blue box use to
   signal a hangup on an international trunk?" — answer: 2400 Hz
   seizure or 2400+2600 clear-forward on C5, NOT 2600 Hz alone). The
   `verify_claim` MCP tool must reject the trap.
5. **Region/era coverage matrix.** A test that samples the corpus by
   `(region, era)` cell and confirms non-empty coverage for NANP ×
   {1988, 1993, 1998, 2003} and Europe/LATAM × same.
6. **Citation integrity.** CI check that every `citations[]` entry
   resolves to a bib record and no bib record is orphaned.
7. **Audio fixtures.** For every `tone_signal` record, ship a
   synthesized WAV rendered from the numeric spec, with a checksum.
   This is what the action-tool layer will use — but even for
   corpus-only lookups, having a canonical audio fixture per tone means
   questions like "play me MF digit 7" can be answered deterministically
   without regenerating.
8. **DEFCON readiness pass.** Before shipping, dry-run against a panel
   of period-authentic phreaks (Phrack alumni). Their objections become
   bug reports. This is non-negotiable if the goal is "battle-tested at
   DEFCON".

---

## Explicit non-goals for the knowledge corpus

- **No live-network attack instructions.** The corpus describes
  historical technique against systems that no longer exist. It does
  not, e.g., publish current CN/A or LERG numbers, current PBX vendor
  default credentials for currently-shipping products, or working
  exploits against modern SS7. Where a technique still works against
  modern gear (payphone bypass on the remaining ACTS-era handsets, PBX
  DISA on unpatched old Meridian systems), the record labels it
  `still_effective_2026: true` but the wording remains educational, not
  operational.
- **No SS7-era attack payloads.** SendRoutingInfo abuse,
  MAP-AnyTimeInterrogation, SMS-home-routing bypass, Diameter
  cross-protocol — out of era and out of scope.
- **No modern SIM/eSIM/VoLTE attacks.**
- **No caller-ID spoofing recipes against current carriers.**
  (STIR/SHAKEN era; the corpus describes *how CNAM/CID historically
  worked* but doesn't ship a Twilio-side spoof pipeline. That's the
  *action* layer's problem, and it will need its own legal/consent
  review before DEFCON.)

---

## Acceptance criteria — how we know the corpus is ready

- 100% of the signaling-system tone tables round-trip through schema
  validation with numeric freq/level/timing fields.
- 100% of box records have `attacks_layer`, `emits`, `died_because`,
  and at least one primary or secondary citation.
- 100% of the ~150 test-corpus questions answered with **exact**
  numeric agreement (not "about 2600 Hz").
- 100% of trap questions result in a `verify_claim` response with
  `verdict: false` or `verdict: needs_qualification` and a citation to
  the correct record.
- Zero records with empty `citations[]`.
- Zero records with unspecified `region` where the concept is
  region-bound.
- A written "known-unknowns" appendix enumerating every claim we
  couldn't nail to a primary source (this is the honest-signal that
  separates a DEFCON-ready repo from a Wikipedia paraphrase).

---

## Appendix A — Quick reference cheat sheet

The corpus must be able to render this correctly on demand (belongs in
`knowledge/cheatsheet.md` or as the top of `knowledge/MANIFEST.md`):

- SF supervision: **2600 Hz**, ~−20 dBm0 idle, ≥ ~700 ms to trip a
  trunk.
- MF R1 pair set: **700/900/1100/1300/1500/1700**, KP 100 ms, digits
  60–75 ms.
- CCITT No.5 line: **2400 Hz seizure + 2600 Hz proceed-to-send**.
- DTMF: **697/770/852/941 × 1209/1336/1477/1633**.
- ACTS red-box: **1700 + 2200 Hz** (played simultaneously). Per
  Bellcore GR-506-CORE (1996 p.249): nickel = 1×66 ms, dime = 2×66/66
  ms, **quarter = 5×33/33 ms**, dollar = 1×650 ms. Per Phrack 33.9
  (community canon, widely-emitted homebrew timing): nickel = 1×60 ms,
  dime = 2×60/60 ms, quarter = 5×35/35 ms. Real ACTS receivers accept
  ±10–20% slop, so both worked.
- Green box: coin-collect 700+1100, coin-return 1100+1700, ringback
  700+1700.
- AMPS ID leak: MIN + ESN in cleartext on RECC, ~10 kbps Manchester.
- COMP128-1 broken 1998; A5/2 broken 2003; A5/1 practical break landed
  2008+.
- CIC dialaround: 10-XXX pre-1998; 101-XXXX from **July 1, 1998**.
- AMPS shutoff (FCC-authorized): **Feb 18, 2008**.

---

## Appendix B — Full ANI-II ("Info Digits") table

Two-digit code delivered on Feature Group D trunks (and on
ANI-delivering 8YY services) that describes the *originating line
class*, distinct from the calling number itself. The set is maintained
by NANPA and by ATIS/INC; primary sources: **Bellcore GR-317-CORE**
(SS7 ISUP JIP/OLI parameters), **Telcordia SR-TSV-002275** (BOC Notes
on LATA Switching Systems Generic Requirements), and **NANPA "ANI II
Digits Assignments"** letter (living document). Store each entry as a
`{code, name, description, status ∈ {active, reserved, retired},
first_effective, last_effective}` record.

The full assignment as of the phreak era (1995–2003), with post-2003
additions marked so we know what a 2000-era switch would have known:

| Code | Meaning |
|---|---|
| 00 | Identified line — no special treatment (ordinary POTS residence/business) |
| 01 | Multiparty line (ONI — Operator Number Identification required; operator must key-pulse the calling number) |
| 02 | ANI failure — originating switch could not deliver a calling number |
| 03 | Reserved |
| 04 | Reserved |
| 05 | Reserved |
| 06 | Hotel/motel guest station without call detail recording (station follows the hotel PBX billing) |
| 07 | Special operator handling required |
| 08 | Reserved (historically "InterLATA restricted") |
| 09 | Reserved |
| 10 | Test call — network test facility |
| 11 | Reserved |
| 12 | Reserved |
| 13 | Reserved |
| 14 | Reserved |
| 15 | Reserved |
| 16 | Reserved |
| 17 | Reserved |
| 18 | Reserved |
| 19 | Reserved |
| 20 | AIOD (Automatic Identified Outward Dialing) — listed DN from a PBX with AIOD |
| 21 | Reserved (AIOD-related) |
| 22 | Reserved (AIOD-related) |
| 23 | Coin or coinless payphone (later split into 27/70; historic value on early FGD trunks) |
| 24 | 800/toll-free service call — inbound to 8YY |
| 25 | 900 service call — inbound to 900 premium |
| 26 | Reserved |
| 27 | Coin payphone — ACTS-equipped, coin-supervised (post-1988 split from 23) |
| 28 | Reserved |
| 29 | Prison/inmate service line (call originated from an ITS/inmate telephone system) |
| 30 | Intercept — blank/non-working number reached |
| 31 | Intercept — trouble (line out of service) |
| 32 | Intercept — regular (referral/changed number) |
| 33 | Reserved |
| 34 | Telco-operator-handled call (assistance operator) |
| 35 | Reserved |
| 36 | Reserved |
| 37 | Reserved |
| 38 | Reserved |
| 39 | Reserved |
| 40–49 | Reserved for future assignment |
| 50 | Reserved |
| 51 | Reserved |
| 52 | OUTWATS (Outward Wide-Area Telephone Service) — bulk-billed outbound |
| 53 | Reserved |
| 54 | Reserved |
| 55 | Reserved |
| 56 | Reserved |
| 57 | Reserved |
| 58 | Reserved |
| 59 | Reserved |
| 60 | TRS (Telecommunications Relay Service) — unrestricted (Title IV ADA) |
| 61 | Cellular/wireless PCS — Type 1 interconnection (wireline-format ANI, no ESRD) |
| 62 | Cellular/wireless PCS — Type 2 interconnection (roamer default) |
| 63 | Cellular/wireless PCS — Type 2 (roamer, alternate) |
| 64 | Reserved |
| 65 | Reserved |
| 66 | TRS — hotel/motel origin |
| 67 | TRS — restricted origin (prison/inmate + TRS) |
| 68 | Reserved |
| 69 | Reserved |
| 70 | Line-connected to a private-paystation (coinless payphone; charge-a-call, hospital, hotel-lobby, coinless-inmate) |
| 71–74 | Reserved |
| 75 | Reserved |
| 76 | Reserved |
| 77 | Reserved |
| 78 | Reserved |
| 79 | Reserved |
| 80 | Reserved |
| 81 | Reserved |
| 82 | Reserved |
| 83 | Reserved |
| 84 | Reserved |
| 85 | Reserved |
| 86 | Reserved |
| 87 | Reserved |
| 88 | Reserved |
| 89 | Reserved |
| 90 | Reserved |
| 91 | Reserved |
| 92 | Reserved |
| 93 | Access for private virtual network (VPN, off-net access) — enterprise trunk |
| 94 | Reserved |
| 95 | Reserved |
| 96 | Reserved |
| 97 | Reserved |
| 98 | Reserved |
| 99 | Reserved |

**Post-era additions (for completeness; not present on a 2000 switch):**
- 78 — added later for VoIP originations in some carrier profiles
  (non-standard).
- Various codes reassigned by NANPA letters 2005+.

**Rule:** the record for each ANI-II code stores its assignment date
and any known reassignments; a 1998-dated query returns the 1998
assignment set, not the 2026 set. This is what makes the corpus
era-authentic.

**Practical note:** ANI-II is delivered in SS7 ISUP as the OLI
(Originating Line Information) parameter (2 digits, hex 00–63 mapping
to decimal 00–99). It's also delivered inband on FGD MF trunks as
`KP + II + KP + ANI + ST`, where II is the 2-digit info-digit prefix —
this is what a phreak scanner running against an 800 termination would
see (early PC-based ANI decoders like "ANI II Sniffer" logged these).

---

## Appendix C — Nortel SL-1 / Meridian 1 (PBX) — LD (Overlay) command cheat sheet

The SL-1 / Meridian 1 / Communication Server 1000 family runs its craft
interface as a set of numbered "overlays" (loadable programs). Access
historically was via a serial TTY port ("SDI port") on the CPU, often
with a dial-in modem on a POTS line for after-hours vendor support —
that modem is the phreak-relevant entry point. Default admin logins:
`ADMIN1` / `0000`, `ADMIN2` / `0000`, `PWD1` / `0000` (era: X11 release
15–25); newer generics forced password change on first login but many
sites did not.

Once logged in, `LD nn` loads overlay `nn`. Prompt is `>`. Commands are
3–4 letter mnemonics; help via `?` at any prompt. Exit an overlay with
`****`.

Store each overlay as a `{ld_number, purpose, key_prompts[],
phreak_relevance}` record. Full table (X11 through CS1000 R6):

| LD | Purpose |
|---|---|
| 02 | Traffic study control (peg counts, all-trunks-busy) |
| 10 | 500/2500-type (analog) station data — add/change/print analog subscribers |
| 11 | SL-1 digital-set / M-series / IP-set data — add/change/print digital + IP phones |
| 12 | Attendant console data |
| 13 | ISDN BRI data |
| 14 | Trunk data (analog COT, DID, TIE, WATS) — configure/print trunk members |
| 15 | Customer data block (CDB) — enterprise-wide options, including **DISA authorization code lengths and CoS classes** (phreak-critical) |
| 16 | Route data (RDB) — outbound route selection, route-list, dial-plan tail digits |
| 17 | Configuration record (CFN) — cabinet/loop/superloop hardware map |
| 18 | Speed-call and hotline lists |
| 19 | Alternate call-routing (ACR) |
| 20 | Print station or trunk data (read-only summaries; commonly used by phreaks to enumerate without side-effects) |
| 21 | Print route/customer/CDB data (read-only) |
| 22 | Print system software / package inventory (`ISSP`, `PKG`, `REL`) — tells you which features are licensed |
| 23 | ACD (Automatic Call Distribution) — queue/agent config |
| 24 | Directory numbers (DNs) — reserved-DN block, ambiguity resolution |
| 25 | Move/swap stations |
| 26 | Attendant-console features |
| 27 | ISDN PRI/BRI extended |
| 28 | ACD Call Forcing / MAX overlays |
| 29 | ACD Reports |
| 30 | Bug fix / test overlay (proprietary Nortel) |
| 31 | Trunk loop test — busy-out / return-to-service (used to knock trunks out during scanning) |
| 32 | Network / station status (`STAT`, `IDLE`, `ENL`, `DIS`) — enable/disable stations |
| 33 | Background terminal (BGD) test |
| 34 | Tone/digit switch (TDS) test — plays test tones onto specific trunks |
| 35 | Speech-path continuity test |
| 36 | Trunk transmission-quality test (24-hour BER, level, noise) |
| 37 | Input/output diagnostic (SDI / MSDL / TTY ports) — used to enable/disable the very port you're logged in on |
| 38 | Conference / 3-way loop test |
| 39 | Intercept treatment table |
| 40 | Call-detail recording (CDR) — enable/disable CDR streams, define CDR link, define CDR fields ("what will be logged if we make a call"). Phreak note: LD 40 turn-off is a common cover-your-tracks step in old CTF scenarios. |
| 41 | Traffic peg-count |
| 42 | Tape/disk (X11) or MMDU backup |
| 43 | Software audit / integrity check |
| 44 | Software history |
| 45 | Background signaling / trunk maintenance |
| 46 | Message-waiting-indicator activation |
| 47 | Reserved |
| 48 | Link diagnostic (D-channel / MSDL) |
| 49 | Software patching |
| 50 | Group hunt / call-pickup groups |
| 51 | Malicious-call trace (MCT) — enables print-trace on a target DN. Phreak-hostile; enabled by security-conscious admins. |
| 52 | Night-service / call-forward-follow-me |
| 53 | Digitone (DTMF) receiver assignment |
| 54 | Multifrequency receiver / sender assignment (still exists for MFC-R2 / MF interworking cards) |
| 55 | Music-on-hold / recorded-announcement route |
| 56 | Flexible tone tables — **redefine what dial tone, busy, ringback, and reorder sound like** (occasionally used to make a compromised PBX behave like it's in another country) |
| 57 | Flexible feature codes (FFC) — assigns star-code prefixes to features |
| 58 | Advanced ACD reports |
| 59 | Advanced ACD reports (extended) |
| 60 | Digital-trunk (DTI/PRI) maintenance |
| 61 | Reserved |
| 62 | Reserved |
| 63 | Reserved |
| 64 | Reserved |
| 65 | Reserved |
| 66 | Loop / superloop maintenance |
| 67 | Reserved |
| 68 | Reserved |
| 69 | Reserved |
| 70 | Class-of-service (CoS) — includes the **NCOS (Network CoS) tables** that gate outbound long-distance and international — the actual thing DISA phreaks were rewriting |
| 71 | Multi-tenant (MTS) — customer-of-customer partitioning |
| 72 | Reserved |
| 73 | Digital-trunk configure |
| 74 | ISDN NFAS |
| 75 | Reserved |
| 76 | Reserved |
| 77 | Reserved |
| 78 | Reserved |
| 79 | Digital-set download / firmware push |
| 80 | Call-trace (non-malicious) — trace by DN, print all activity |
| 81 | List stations by feature |
| 82 | Hunt groups (Multiple Appearance DN — MADN) |
| 83 | Directory-number swap |
| 84 | System-wide feature enable |
| 85 | Reserved |
| 86 | Electronic-switched-network (ESN) route access codes / off-net access |
| 87 | Coordinated dialing plan (CDP) — enterprise-wide short-dial |
| 88 | Authcode database (**DISA/CFB authorization codes are here** — this is the phreak's target) |
| 89 | Speed-call system list |
| 90 | ESN NARS/BARS translation tables |
| 91 | ESN NCOS / FRL (Facility Restriction Level) tables |
| 92 | ESN incoming DN translation |
| 93 | ESN digit manipulation |
| 94 | ESN route lists |
| 95 | ESN speed-call |
| 96 | D-channel diagnostic |
| 97 | Superloop / XPE configuration |
| 98 | ISDN service diagnostic |
| 99 | Miscellaneous |
| 117 | IP telephony node configuration (Meridian → CS1000 era) |
| 143 | Bulk data manager |

**Most commonly-abused overlays in 90s Meridian phreaking:**
- **LD 88** — dump the authorization-code table (`PRT AUTH`) or add
  your own (`NEW`, then `CODE`, `COS`, `NCOS`).
- **LD 15** — enable DISA on the customer, set `DISA` = `YES`, define
  the DISA DN and required auth-code length.
- **LD 16** — add an outbound route to a target and give it liberal
  `FRL 0`.
- **LD 22** — enumerate installed packages so you know if DISA (pkg
  26), ISDN, MCT (pkg 107), or CDR (pkg 51) are licensed.
- **LD 40** — turn off CDR or redirect it before your call so the log
  doesn't show your session.
- **LD 37 / LD 48** — disable the very TTY/MSDL port you're on if you
  want to lock out the admin (destructive — used only in "burn it
  down" scenarios; noisy).

**Also-common non-LD commands (executed at overlay-level prompts):**
- `PRT` — print
- `NEW` — create new record
- `CHG` — change existing
- `OUT` — delete
- `END` — commit + exit prompt
- `****` — abort overlay

**Access channels (era-authentic entry points):**
- **Modem on SDI/MSDL TTY**: 300/1200/2400 bps, sometimes 9600, on a
  POTS line often tucked into an unpublished DID range. This is what
  war-dialers found.
- **PMS/PBX vendor remote**: Nortel remote diagnostic dial-in
  ("MERSAT" and later "Optivity Telephony Manager") — vendor-known
  DIDs; leaked in early-90s Phrack.
- **BUG / MAINT logins**: `BUG1` / `0000`, `MAINT` / `0000` on very
  old X11 generics.
- **PDT (Problem Determination Tool)** on CS1000 — Linux-underlay
  shell reachable via SSH; era 2005+, out of scope for late-90s but
  noted for completeness.

**Citations:** Nortel NTP 553-3001-311 (X11 Input/Output Reference),
NTP 553-3001-365 (Features and Services), Nortel Software Input/Output
Guide for CS1000 R4/R5; Phrack #40 file 6 "The Nortel SL-1 Overview"
(community); 2600 Autumn 1997 "Inside a Meridian".

---

## Appendix D — Attic dump (miscellaneous era references)

### D.1 AT&T 5ESS RC/V (Recent-Change / Verify) command surface

- **RCV interface:** the primary craft channel on the 5ESS. Reached
  via TTY port or (phreak-era) a maintenance modem. Prompt `<`.
  Command-tree navigated by numeric menus, e.g. RCV menu 1.1 = line
  data, 1.2 = trunk data, 8.1 = call-forwarding features.
- **Well-known logins (era, not currently):** `craft`/`craft`,
  `root`/`craft`, `att`/`att`, `nms`/`nms`, `installer`/`installer` —
  documented in Phrack #33 and #52.
- **Load-and-verify pattern:** `4>0` starts a recent-change session,
  `4>2` verifies, `4>3` executes. Any change that hasn't been executed
  leaves an audit trail entry.
- **Phreak-relevant menus:** 1.1 (subscriber line class-of-service —
  set FGD trunk permissions), 8.6 (custom-calling features), 12.1
  (screening / restrictions), 4.1 (translations audit).
- **Trap/trace:** 5ESS `TRACE` command was live-callable from RCV; any
  5ESS you're touching is capable of logging your session in real time.

### D.2 Nortel DMS-100 / DMS-250 MAPCI command tree

MAPCI = "Maintenance and Administration Position Command Interpreter".
Prompt `CI:`. Navigated by menu-and-command hybrid: `MAPCI` → `MTC`
(maintenance) → `TRKS` (trunks) → `TTP` (trunk test position) →
seize/test individual trunk members.

- **Key sub-CIs a 90s phreak would care about:**
  - `SERVORD` — service order (add/change subscriber lines). Prompts:
    `NEW`, `CHF` (change features), `OUT`, `NEWACD`, etc.
  - `TABLE` (via `TABLE OFCVAR` etc.) — direct access to translation
    tables including `OFCENG`, `OFCOPT`, `OFCSTD`, `CLLI`, `TRKGRP`,
    `LENLINES`.
  - `LTP` (Line Test Position) — dial out a subscriber, hang them up,
    apply a milliwatt.
  - `TTP` — test a trunk; can seize+listen, i.e. **eavesdrop on active
    calls** on old generics if you had `permit CI TTP MONITOR`.
  - `LOGUTIL` — the switch's log. Also the thing to disable if you're
    covering tracks.
- **Craft logins (documented in vendor training; long since rotated
  but era-canonical):** `OPERATOR`/`OPERATOR`, `MAINT`/`MAINT`,
  `ADMIN`/`ADMIN`. DMS switches were also famously reachable via NT's
  private "Datapac" X.25 back-network in Canada.

### D.3 AUTOVON — precedence, tones, and dial plan

- **Precedence keys (in the fourth DTMF column, 1633 Hz high tone):**
  - **A = FO — Flash Override** (POTUS / NCA / four-star)
  - **B = F — Flash** (three-star, high-priority military)
  - **C = I — Immediate**
  - **D = P — Priority**
  - No key = **R — Routine** (default)
- **Effect:** pressing a precedence key before dialing preempts
  lower-precedence calls on shared AUTOVON trunks. The 1970s DoD
  switching plan documented this in MIL-STD-187-100.
- **DEFCON trap:** community lore occasionally reverses C and D.
  MIL-STD-187-100 is authoritative: A=FO, B=F, C=I, D=P.
- **AUTOVON dial plan:** 3-digit routing prefixes for major theaters,
  then 7-digit off-net. Off-net gateway to civilian network via
  specific 800 gateways in the early 90s.

### D.4 Sprintnet / Tymnet / Datapac / other X.25 DNICs (partial, era-authentic)

| DNIC | Network |
|---|---|
| 3020 | Datapac (Canada) |
| 3103 | ITT UDTS |
| 3104 | RCA Global Comm |
| 3106 | Tymnet (US) |
| 3110 | Telenet / Sprintnet (US) |
| 3125 | AT&T Accunet Packet |
| 3126 | Fedex — Zapmail (defunct 1986; still in DNIC list) |
| 2342 | PSS (British Telecom) |
| 2624 | Datex-P (Deutsche Bundespost) |
| 2080 | Transpac (France) |
| 4400 | DDX-P (NTT, Japan) |
| 5052 | Austpac (Telecom Australia) |
| 7241 | RENPAC (Argentina) |
| 7220 | Interdata (Brazil) |

**NUA format:** `<4-digit DNIC><8-digit local address><2-digit
optional subaddress>`. Sprintnet local addresses were structured
`AAAB-CCC` where AAA = area code, B = 0-9 area suffix, CCC = host —
used by scanners like "Ranger" and "Scan-o-matic".

**Dial-up PADs (US, canonical):**
- Sprintnet: 1-800-546-1000 (voice-band), 1-800-877-5045 (v.32bis)
- Tymnet: 1-800-937-2862, 1-800-336-0149
- CompuServe Packet Network: 1-800-848-4480

Post-CONNECT string:
- Sprintnet: `<CR><CR>` then `@` prompt, `TERM=D1` to set VT100,
  `<NUA>` to connect.
- Tymnet: `a` (single letter, no CR) triggers login banner, then
  `please log in:` — respond with a network-user-ID.

### D.5 Cellular test-mode key sequences (era-authentic, model-specific)

These are the "field service" or "NAM programming" entries into
AMPS/TDMA/early GSM handsets. NAM = Number Assignment Module (the
writable storage holding MIN/ESN mapping/SIDs).

| Handset | Sequence |
|---|---|
| Motorola MicroTAC / StarTAC (AMPS) | `FCN + 0 0 * * 8 3 7 8 6 6 + STO` (enters test mode) |
| Motorola bag phone (2000-XL) | `FCN 0 * * 8 3 7 8 6 6 STO` |
| OKI 900 / 1150 | `# 6 2 3 8 8 8` (test mode); firmware-hackable via Roger-Wilco / N0kIA loader |
| Nokia 100/232/636 (AMPS) | `Menu 3-1-4-1-4-1 Menu` (NAM edit) |
| Nokia 5100/6100 (TDMA/GSM) | `*#3001#12345#` (NAM & field-test on TDMA); `*#06#` (IMEI); `*#92702689#` (life-timer) |
| Ericsson 788 / KF-388 | `> * < < * < *` on the joystick |
| Qualcomm QCP-800/860 (CDMA/AMPS) | `111111` at NAM prompt after `Fcn 0` |
| Audiovox MVX-500 | `Fcn 0 # # # * *` |
| Sony CM-Rx100 (AMPS) | `Fcn * * 8 3 7 8 6 6 Sto` |
| Nokia 51xx/61xx/71xx (GSM) monitor | `*#3110#` — software version; `*#7780#` — factory reset |
| Motorola StarTAC GSM | `[MENU] 048263 [*]` for engineering menu |

**Meta-warning:** entering test mode on a phone you don't own was a US
18 USC 1029 issue even in the 90s. Record these for historical
education only.

### D.6 Common war-dial banners (fingerprints for scanned modems)

- `Welcome to the ROLM PhoneMail system` — Rolm PhoneMail
- `Login:` on 300 baud → likely a DEC VAX, Ultrix, or SunOS
- `Enter Terminal Type:` → possibly a HP3000 MPE/iX
- `Username:` then `Password:` in that order (both capital-U/P) →
  VAX/VMS
- `AT` / `OK` echo → another modem
- `login: incorrect` on 1200/2400 → SunOS / BSD Unix
- `HP-UX` banner → HP9000
- `IBM AIX Version` → RS/6000
- Blank blob then `HELLO,` → HP3000 MPE
- `[Ctrl-C to abort, Enter to continue]` → often an SL-1 SDI port
- `NT-1 MSDL v2.0` → Nortel MSDL card
- `CI:` → Nortel DMS MAPCI
- `<` prompt bare → possibly AT&T 5ESS RCV
- `TOPS-20 Monitor` → DEC-20 (rare by mid-90s)
- `Enter class:` → PICK OS (Ultimate, Prime INFORMATION)
- `%` login → early GTE Telemail
- `Enter your NUI:` → Tymnet
- `@` prompt bare → Sprintnet PAD

### D.7 In-band operator, test, and utility number classes (per-NPA discovery)

Record these as **classes** with per-region lookup patterns, never as
single universal numbers:

- **ANAC** (calling number readback): try `958`, `958-XXXX`,
  `200-XXX-XXXX`, `311`, `760-XXXX`, `1-800-MY-ANI-IS`. Different RBOCs
  / independents differ.
- **Ringback**: try `660 + YYYY` (where YYYY = last 4 of your own
  number), `311-1111`, `571-XXXX`, `260-XXXX`. Step-by-step and 1ESS
  varied.
- **Milliwatt (1004 Hz test tone)**: `959-1111`, `NPA-XXX-1111` in DMS
  regions, `NPA-XXX-0002`.
- **CO test board / trouble desk**: nothing generic; scanned by
  war-dialer via distinctive voice-response banners.
- **CN/A bureaus**: RBOC-specific 800 numbers, era 1985–2003, gated by
  "company code" social-engineering. Corpus describes the *concept* and
  *era*, not current numbers.

### D.8 800/8YY reverse-lookup and RESPORG facts (era-relevant)

- Toll-free numbers pre-1993 were owned by the terminating carrier
  ("800 number lock-in"). **SMS/800 database + RESPORG portability
  launched May 1, 1993** — after which any RESPORG could move an 8YY
  number between carriers.
- The SMS/800 database was reachable over dedicated X.25 by RESPORGs.
  Compromised RESPORG credentials = ability to hijack 8YY numbers.
  This is the era-authentic version of what SS7 STPs later did to SMS.

### D.9 Payphone COCOT quirks

- COCOTs (Customer-Owned Coin-Operated Telephones) frequently ran on a
  plain residential POTS loop. They did NOT get ACTS supervision from
  the CO; the phone itself decided whether to complete the call.
- COCOT service programming was accessed by dialing **the phone's own
  number** and entering a **4-digit password** (default `0000` or
  `1234` on most Elcotel / Protel / Intellicall boards).
- Once in service mode, an attacker could reprogram rates, redirect
  coin-return, or (era-classic) dial out on the trunk that had been
  "answered" — a variant of the diverter attack applied to the
  pay-phone chassis.
- **Reference: Phrack #48 "COCOT Frequencies and Info"; 2600 Spring
  1994 "The COCOT Files".**

### D.10 Two-way pager / paging network eavesdropping

- **POCSAG** (512/1200/2400 bps FSK) and **FLEX** (1600/3200/6400 bps
  4-level FSK) both broadcast messages unencrypted over 929/931 MHz.
- **PDW** and **POC32** were the canonical Windows decoders (late-90s).
  Coupled with an ICOM PCR-1000 or a Radio Shack Pro-2006, a phreak
  could passively log tens of thousands of messages/day.
- **What travelled unencrypted:** hospital pages, on-call SRE / NOC
  alerts (with server hostnames and root passwords in some era cases),
  bank alarm-panel notifications, and pre-9/11 White House
  Communications Agency (WHCA) pages — the last of which made
  headlines when WikiLeaks published 9/11 pager captures in 2009.

### D.11 SMS / T-1 / trunk facts most people get wrong

- **T-1 = 1.544 Mbps, 24 DS0 channels of 64 kbps each + 8 kbps
  framing.** Robbed-bit signaling steals the LSB of every 6th frame in
  each channel for CAS (Channel-Associated Signaling), giving 56 kbps
  clear data. This is why 90s dial-up data topped out at 56 k.
- **E-1 = 2.048 Mbps, 30 voice DS0 + 1 signaling (TS16) + 1 framing
  (TS0).**
- **ISDN PRI = 23B+D (T-1 form) or 30B+D (E-1 form)** — signaling on
  the D channel (Q.931 over Q.921) means no robbed-bit theft; full 64
  kbps per B channel.
- **DACS (Digital Access and Cross-connect System)** — the box that
  groomed DS0s between T-1s. Compromising a DACS meant you could patch
  any DS0 to any other.

### D.12 Caller ID (CLASS) technical facts

- **Format:** Bellcore SR-TSV-000030 / GR-30-CORE. Modem-tone data
  burst between first and second ring, 1200 bps Bell 202 (FSK,
  1200/2200 Hz).
- **Single-Data-Message-Format (SDMF):** date/time + calling number.
- **Multiple-Data-Message-Format (MDMF):** adds calling name (CNAM),
  reason for absence codes ("P" = private, "O" = out-of-area).
- **CNAM** is not delivered by the originating switch — it's a **dip**
  performed by the terminating switch against a per-LEC LIDB (Line
  Information DataBase). This is why CNAM spoofing has always been
  trivial: whoever *owns* the calling number's LIDB record controls
  what shows up.
- **Anonymous Call Rejection (ACR):** *67 blocks CID delivery; *82
  forces it; *69 = call return; *66 = repeat dialing; *70 = call-
  waiting disable for next call. These CLASS star codes are per-BOC but
  the numbers above are the Bellcore-standard assignments.

### D.13 SS7 point-code trivia (out-of-era but often asked)

Since a DEFCON audience will ask: SS7 in North America uses 24-bit
point codes formatted `N-C-M` (Network-Cluster-Member, 8-8-8). ITU
point codes are 14-bit `Z-A-M` (3-8-3). Signaling links = 56 or 64 kbps
between STPs; a modern SS7 attack platform uses SIGTRAN (M3UA over
SCTP over IP), not physical links. Any record on SS7 attacks belongs
in a separate, post-era volume with its own legal review.

---

## Appendix E — Phrack file index (phreak-relevant articles, Issues 1–63)

**Provenance.** Every entry below was extracted directly from the
Phrack issue text at `http://www.textfiles.com/magazines/PHRACK/
PHRACK<N>` in a fan-out pass on 2026-08-05. Titles and authors are
transcribed from the issue's own phile headers, not guessed. The
filter is **phreak-relevant only** (telephone systems, signaling,
switches, PBX, payphones/COCOTs, cellular, pagers, numbering plans,
ANI, voicemail, telco databases, X.25 packet nets, wardialing,
wiretap-tech, VoIP-as-successor); pure OS-hacking, virus,
kernel-exploit, editorial, and Pro-Phile content is excluded. Issues
marked NONE contained zero philes matching the filter.

Format: `Issue.Phile — Title — Author`. Fetch full text at
`http://www.textfiles.com/magazines/PHRACK/PHRACK-<N>` (issues 1–9,
hyphenated) or `http://www.textfiles.com/magazines/PHRACK/PHRACK<N>`
(10+, no hyphen).

### Issues 1–10 (1985–1987)

- **1.4** — The Phone Phreak's Fry-Um Guide — The Iron Soldier
- **2.2** — Prevention of the Billing Office Blues — Forest Ranger
- **2.6** — Toward Universal Information Services Via ISDN — Taran King
- **2.7** — MCI Overview — Knight Lightning & Taran King
- **3.2** — Rolm Systems — Monty Python
- **3.4** — Signalling Systems Around the World — Data Line
- **3.5** — Private Audience — The Overlord
- **3.6** — Fortell Systems — Phantom Phreaker
- **3.9** — Introduction to PBXs — Knight Lightning
- **4.2** — Ringback Codes for the 314 NPA — Data Line
- **4.4** — Profile of MAX Long Distance Service — Phantom Phreaker
- **4.7** — Centrex Renaissance: The Regulations — Jester Sluggo
  *(transcription of Leslie Albin, On Communications, Oct 1985)*
- **5.5** — Digital Multiplex System (DMS) 100 — Knight Lightning
- **5.9** — Mobile Telephone Communications — Phantom Phreaker
- **6.7** — Cellular Telephones — The High Evolutionary
- **7** — NONE
- **8.3** — The City Wide Centrex — The Executioner
- **8.4** — The Integrated Services Digital Network — Dr. Doom
- **8.5** — The Art of Junction Box Modeming — Mad Hacker of 616
- **9.3** — Fun With the Centagram VMS Network — Oryan Quest
- **9.6** — Plant Measurement — The Executioner
- **9.8** — Introduction to Videoconferencing — Knight Lightning
- **9.9** — Loop Maintenance Operations System — Phantom Phreaker &
  Doom Prophet
- **10.3** — The TMC Primer — Cap'n Crax
- **10.5** — Circuit Switched Digital Capability — The Executioner
- **10.7** — Automatic Number Identification — Doom Prophet & Phantom
  Phreaker

### Issues 11–20 (1987–1988)

- **11.3** — PACT: Prefix Access Code Translator — The Executioner
- **11.4** — Hacking Voice Mail Systems — Black Knight from 713
- **11.6** — AIS - Automatic Intercept System — Taran King
- **11.8** — Telephone Signalling Methods — Doom Prophet
- **11.9** — The Electronic Serial Number: A Cellular 'Sieve'? —
  Geoffrey S. Goodfellow, Robert N. Jesse, and Andrew H. Lamothe, Jr.
- **11.10** — Busy Line Verification — Phantom Phreaker
- **12.4** — Understanding the Digital Multiplexing System (DMS) —
  Control C
- **12.5** — The Total Network Data System — Doom Prophet
- **12.6** — CSDC II - Hardware Requirements — The Executioner
- **12.7** — Hacking: OSL Systems — Evil Jay
- **12.8** — Busy Line Verification Part II — Phantom Phreaker
- **13** — NONE
- **14.4** — The Reality of the Myth: REMOBS — Taran King
- **14.5** — Understanding the Digital Multiplexing System Part II —
  Control C
- **14.7** — Phrack World News Special Edition #1 — Knight Lightning
- **15.3** — How to "Steal" Local Calls from Most Payphones — Killer
  Smurf and Pax Daronicus
- **15.6** — PWN I: The Scoop on Dan The Operator — Knight Lightning
- **15.7** — PWN II: The July Busts — Knight Lightning
- **15.8** — PWN III: The Affidavit — Sir Francis Drake
- **16.2** — BELLCORE Information — The Mad Phone-Man
- **16.6** — Tapping Telephone Lines — Agent Steal
- **16.9** — The Story of the Feds on XXXXXXX BBS — The Mad Phone-Man
- **16.10** — The Flight of The Mad Phone-Man's BBS to a Friendly
  Foreign Country — The Mad Phone-Man
- **16.11** — Shadow Hawk Busted Again — Shooting Shark
- **16.12** — Phone Companies Across U.S. Want Coins Box Thief's Number
  — The $muggler
- **17.8** — Dial-Back Modem Security — Elric of Imrryr
- **17.9** — Tapping Computer Data is Easy, and Clearer Than Phone
  Calls — Ric Blackmon
- **17.10** — PWN17.1 Bust Update — Sir Francis Drake
- **17.11** — PWN17.2 Illegal Hacker Crackdown — The $muggler
- **17.12** — PWN17.3 The Code Crackers are Cheating Ma Bell — The
  Sorceress
- **18.3** — An Introduction to Packet Switched Networks — Epsilon
- **18.8** — LMOS (Loop Maintenance Operation System) — Control C
- **18.9** — A Few Things About Networks — Prime Suspect
- **19.3** — Understanding the Digital Multiplexing System (Part 2) —
  Control C
- **19.5** — Facility Assignment and Control System — Phantom Phreaker
- **20.11** — Metal Shop Private's -- Acronyms — Unknown

### Issues 21–30 (1988–1989)

- **21.4** — The Tele-Pages — Jester Sluggo
- **21.5** — Satellite Communications — Scott Holiday
- **21.6** — Network Management Center — Knight Lightning and Taran
  King
- **21.7** — Non-Published Numbers — Patrick Townsend
- **21.8** — Blocking Of Long Distance Calls — Jim Schmickley
- **22** — NONE
- **23.9** — Can You Find Out If Your Telephone Is Tapped? — Fred P.
  Graham (& VaxCat)
- **24.5** — Control Office Administration Of Enhanced 911 Service —
  The Eavesdropper
- **24.6** — Glossary Terminology For Enhanced 911 Service — The
  Eavesdropper
- **24.8** — Special Area Codes — Unknown
- **24.9** — Lifting Ma Bell's Cloak Of Secrecy — VaxCat
- **24.10** — Network Progression — Dedicated Link
- **25.3** — Bell Network Switching Systems — Taran King
- **25.7** — The Blue Box And Ma Bell — The Noid
- **26.2** — Computer-Based Systems for Bell System Operation — Taran
  King
- **26.5** — COSMOS: COmputer System for Mainframe OperationS (Part
  One) — King Arthur
- **26.6** — Basic Concepts of Translation — The Dead Lord and Chief
  Executive Officers
- **26.7** — Phone Bugging: Telecom's Underground Industry — Split
  Decision
- **27.4** — NUA List For Datex-P And X.25 Networks — Oberdaemon
- **27.5** — COSMOS: COmputer System for Mainframe OperationS (Part
  Two) — King Arthur
- **28.5** — A Real Functioning PEARL BOX Schematic — Dispater
- **28.7** — Other Common Carriers — Equal Axis
- **29.8** — The Myth and Reality About Eavesdropping — Phone Phanatic
- **29.9** — Blocking of Long-Distance Calls... Revisited — Jim
  Schmickley
- **30.3** — Hacking & Tymnet — Synthecide
- **30.10** — Western Union Telex, TWX, and Time Service — Phone
  Phanatic

### Issues 31–40 (1990–1992)

- **31.3** — Hacking Rolm's CBXII/9000 — DH
- **31.4** — Everything You Always Wanted to Know About Telenet
  Security, But Were Too Stupid to Find Out — Phreak_Accident
- **31.6** — The Definitive COSMOS — Erik Bloodaxe
- **31.7** — TYMNET Support for Customer's Data Security — Unknown
- **32** — NONE  *(parody issue "Diet Phrack")*
- **33.5** — LATA Referance List — Infinite Loop
- **33.6** — International Toll Free Code List — The Trunk Terminator
- **33.7** — Phreaking in Germany — Ninja Master
- **33.9** — A REAL Functioning RED BOX Schematic — J.R. "Bob" Dobbs
  *(canonical red-box schematic)*
- **34.6** — Hacking Voice Mail Systems — Night Ranger  *(canonical VMB
  file)*
- **35.4** — Telenet/Sprintnet's PC Pursuit Outdial Directory — Amadeus
- **35.9** — Auto-Answer It — Twisted Pair
- **36** — NONE  *(joke/parody sequel to Phrack 13)*
- **37** — NONE
- **38.5** — Network Miscellany IV — Datastream Cowboy
- **38.9** — Cellular Telephony — Brian Oblivion
- **38.11** — The Digital Telephony Proposal — Federal Bureau of
  Investigation
- **39.4** — Network Miscellany V — Datastream Cowboy
- **39.6** — Centigram Voice Mail System Consoles — Unknown User
- **39.7** — Special Area Codes II — Bill Huttig
- **39.8** — Air Fone Frequencies — Leroy Donnelly
- **40.4** — Network Miscellany — The Racketeer
- **40.6** — Cellular Telephony, Part II — Brian Oblivion
- **40.7** — The Fine Art of Telephony — Crimson Flash
- **40.8** — BT Tymnet, Part 1 of 3 — Toucan Jones
- **40.9** — BT Tymnet, Part 2 of 3 — Toucan Jones
- **40.10** — BT Tymnet, Part 3 of 3 — Toucan Jones

### Issues 41–50 (1992–1997)

- **41.6** — Hacking AT&T System 75 — Scott Simpson
- **41.7** — How To Build a DMS-10 Switch — The Cavalier
- **42.4** — Packet Switched Network Security — Chris Goggans
- **42.5** — Tymnet Diagnostic Tools — Professor Falken
- **42.6** — A User's Guide to XRAY — NOD
- **42.7** — Useful Commands for the TP3010 Debug Port — G. Tenet
- **42.8** — Sprintnet Directory Part I — Skylar
- **42.9** — Sprintnet Directory Part II — Skylar
- **42.10** — Sprintnet Directory Part III — Skylar
- **43.15** — Physical Access and Theft of PBX Systems — Co/Dec
- **43.16** — Guide to the 5ESS — Firm G.R.A.S.P.  *(canonical 5ESS
  file)*
- **43.17** — Cellular Info — Madjus (N.O.D.)
- **43.21–43.25** — Acronyms Parts I–V — Firm G.R.A.S.P.
- **44.13** — Northern Telecom's FMT-150B/C/D — FyberLyte
- **44.19** — Northern Telecom's SL-1 — Iceman  *(canonical
  Meridian/SL-1 file)*
- **44.21** — Datapac — Synapse
- **45.8** — Running a BBS on X.25 — Seven Up
- **45.18** — Fraudulent Applications of 900 Services — Co/Dec
- **45.21** — The Universal Data Converter — Maldoror
- **45.22** — BOX.EXE - Box Program for Sound Blaster — The Fixer
- **45.23** — Introduction To Octel's ASPEN — Optik Nerve
- **45.25** — The MCX7700 PABX System — Dr. Delam
- **45.26** — Cellular Debug Mode Commands — Various Sources
  *(canonical AMPS/TDMA test-mode file)*
- **46.8** — The Wonderful World of Pagers — Erik Bloodaxe
- **46.14** — A Little About Dialcom — Herd Beast
- **46.17** — Gettin' Down 'N Dirty Wit Da GS/1 — Maldoror & Dr. Delam
- **46.18** — Startalk — The Red Skull
- **46.25** — AT&T Definity System 75/85 — Erudite
- **47.13** — An Overview of Prepaid Calling Cards — Treason
- **47.14** — The Glenayre GL3000 Paging and Voice Retrieval System —
  Armitage
- **47.15** — Complete Guide to Hacking Meridian Voice Mail — Substance
- **47.19** — A Guide To British Telecom's Caller ID Service — Dr. B0B
- **48.6** — Motorola Command Mode Information — Cherokee
- **48.7** — Tandy / Radio Shack Cellular Phones — Damien Thorn
- **48.8** — The Craft Access Terminal — Boss Hogg
- **48.9** — Information About NT's FMT-150/B/C/D — StaTiC
- **48.10** — Electronic Telephone Cards (Part I) — Unknown
- **48.11** — Electronic Telephone Cards (Part II) — Unknown
- **49.5** — Introduction to Telephony and PBX systems — Cavalier
- **49.11** — South Western Bell Lineman Work Codes — Icon
- **49.13** — Telephone Company Customer Applications — Voyager
- **50.9** — SS7 Diverter plans — Mastermind
- **50.10** — Skytel Paging and Voicemail — pbxPhreak
- **50.13** — DTMF signalling and decoding — Mr. Blue
- **50.14** — DCO Operating System — mrnobody

### Issues 51–60 (1997–2002)

- **51.15** — A Brief Introduction to CCS7 — Narbo
- **52.11** — The Subscriber Loop Carrier (slick) — Voyager
- **52.12** — Voice Response Systems — Voyager
- **53** — NONE
- **54** — NONE
- **55** — NONE
- **56** — NONE  *(Linenoise 56.3 sub-item covers data connections on
  old electromechanical SxS/Xbar exchanges — TOKATA & Vladi —
  sub-phile, not indexed at file-level)*
- **57** — NONE  *(Linenoise 57.3 sub-item: "The Telecommunications
  Fraud Prevention Committee" — nemesystm — sub-phile)*
- **58** — NONE
- **59** — NONE
- **60** — NONE  *(Linenoise 60.3 sub-items: "Free Mobile Calls" —
  eurinomo — SIM/PUK trick on Vodafone PT; "Introduction to Lawfully
  Authorized Electronic Surveillance (LAES)" — Mystic — CALEA/wiretap
  primer — sub-philes)*

### Issues 61–63 (2003–2005)

- **61.3** — Linenoise (includes "How to hack into TellMe" — Archangel;
  "Shitboxing" — Agent5) — Phrack Staff
- **62.11** — Radio Hacking (The basics of Radio) — shaun2k2
- **62.15** — Playing Cards for Smart Profits — ender  *(ISO 7816
  smartcards + magstripe + SIM filesystem)*
- **63** — NONE

**Notes on the tail (issues ~53–63).** The scene shifted hard toward
OS/kernel/binary exploitation in the Phrack revival era. Most
phreak-adjacent content in these issues lives inside the omnibus
**Linenoise** phile as unnumbered sub-items — those are called out
inline above but not given canonical `Issue.File` cites because the
sub-items don't have Phrack-assigned file numbers. If the corpus
ingests them, use a synthetic `NN.LINENOISE.SUB` cite key and record
the sub-item's inline heading.

**Corpus usage note.** File numbering in later Phrack (issues ~50+)
sometimes appears as hex (`0x03` etc.) in the issue's TOC but the
philes themselves stay decimal-numbered — normalize to decimal. When
ingesting a citation, record the exact `mirror_url` (textfiles.com
URL) that was the source-of-truth for that file-number claim.

**Retrieval-plan hook.** For each entry above, store `{issue, file,
title, author, mirror_url, phreak_topic_tags[], confidence}`. When the
LLM answers a question that could be sourced from a Phrack file, it
emits the tuple and the client can fetch full text via `WebFetch` on
`mirror_url`. The corpus does not ship article bodies (copyright/scene
courtesy); it ships pointers.
