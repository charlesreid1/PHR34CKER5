# TYPED RECORDS — the KR layer

> The prose corpus (`knowledge/<topic>/*.md`) is the *reference* the
> assistant reads. This directory is the *typed, dated knowledge
> repository* it looks facts up in — numbers, not adjectives.

Everything here is a JSON array of records. The knowledge-retrieval MCP
tools (`lookup_tone`, `verify_claim`, `explain_technique`, `bibliography`,
`cross_reference`) bind to these files, not to free text. The discipline
is specified in `plan-knowledge.md` ("Corpus discipline — a KR, not a
wiki"); this README is the load-time contract.

## Files

| file | category | what's in it |
|---|---|---|
| `tones.json` | `tone_signal` | every discrete tone / tone-pair: exact freqs (Hz), tolerance, level (dBm0), on/off timing (ms), region, era |
| `boxes.json` | `box` | the colored-box catalog: what it emits, what layer it attacks, when/where it worked, why it died |
| `techniques.json` | `technique` | step-by-step compositions of tones + boxes + network elements, with a vulnerability window |
| `bibliography.json` | `bibliography` | canonical sources by `id`; every record cites into this table |

## Record shape

Every record is an object with at least:

```json
{
  "id": "kebab-case-unique",
  "name": "human name",
  "aliases": ["other names"],
  "category": "tone_signal | box | technique | bibliography | ...",
  "region": "NANP | CCITT-No5 | ITU-R2 | AUTOVON | universal | ...",
  "era_bounds": ["1960-01-01", "1990-12-31"],
  "confidence": "primary | secondary | community | folklore",
  "citations": ["bib-id", "..."],
  "see_also": ["other-record-id"],
  "disputed": { "field": "why it's disputed + the competing values" }
}
```

- **`era_bounds`** is `[first_effective, last_effective]`; either end may be
  `null` for open-ended. `explain_technique` refuses when a caller's
  `(year, region)` lands outside these bounds.
- **`citations`** must be non-empty and every entry must resolve to an `id`
  in `bibliography.json`. The loader raises on a violation.
- **`confidence`** weights the answer: `primary` = a Bell/Bellcore/ITU
  document, down to `folklore` = joke boxes and scene lore.
- **`disputed`** is never silently resolved. When Bell docs and community
  canon disagree (the MF KP2/ST-prime naming, the ACTS quarter timing),
  both values are carried with provenance and `verify_claim` returns
  `needs_qualification` rather than picking a side.

## Tone-record body

`tone_signal` records add a `technical_body` with numeric fields:

```json
"technical_body": {
  "frequencies_hz": [1700, 2200],
  "tolerance": "±1.5%",
  "level_dBm0": -7,
  "on_ms": 66, "off_ms": 66,
  "pattern": "human description of the burst structure"
}
```

"About 2600 Hz" is a defect. "2600 Hz ± 15 Hz, ≥ 300 ms continuous, at
−20 dBm0 idle" is a record.

## Sources

The numeric material is transcribed from `plan-knowledge.md` §"Technical
fill material" and §"Explicitly disputed entries", which cite the
primaries (BSTJ Nov 1960, Bellcore GR-506-CORE / TR-NPL-000275, CCITT
Q-series, Phrack 33.9, 2600 Autumn 1990). Tone numeric values are
cross-checked against the synthesis tables in `src/phr34cker5_mcp/tones.py`
and the detector targets in `detect.py`.
