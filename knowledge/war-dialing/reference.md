# War dialing — reference

The exact result-category semantics, the ToneLoc `.dat` file format,
and the scan-parameter trade-offs. If you're triaging a CTF-supplied
scan output, this file is what you look up first.

For a discussion of *how* the classifier decided its verdicts and the
false-positive patterns, see [[war-dialing/toneloc-tuning]] (which is
the operational companion to this file).

## Result categories — the wire meaning

Every war dialer of the era logged one of a small set of per-number
result codes. Semantics were nearly identical across ToneLoc / THC-Scan
/ PhoneSweep but the code names varied.

| ToneLoc | THC-Scan | PhoneSweep | Wire condition |
|---|---|---|---|
| `CARRIER` | `CARRIER` | `MODEM` | Modem returned `CONNECT` — negotiation succeeded. Follow-up: log the banner. |
| `TONE` | `TONE` | `TONE` | A recognizable tone was heard (fax CED, dial tone). Follow-up: distinguish by frequency + duration. |
| `VOICE` | `VOICE` | `VOICE` | Someone answered but no carrier trained. Human or announcement. |
| `NOTE` | `TIMEOUT` | `RINGOUT` | Rang for `RINGCOUNT` rings without answer. |
| `RINGOUT` | (same) | `NO_ANSWER` | Alternate spelling of the above on some ToneLoc versions. |
| `BUSY` | `BUSY` | `BUSY` | Modem `BUSY` result — line is engaged. |
| `ABORTED` | `ABORT` | `ABORT` | Manual cancel or scan interrupted. |
| `UNSCANNED` | `-` | `PENDING` | Not yet attempted. |
| `BLACKLIST` | `EXCLUDE` | (none) | Explicitly excluded by config. |

Detected-but-not-classified hits landed in a bucket ToneLoc called
`TONES.LOG` (any inband tone the classifier couldn't name) while
carrier hits landed in `FOUND.LOG`.

## The ToneLoc `.dat` file format

ToneLoc stored per-exchange state in a compact binary file:
`<NPA>-<NXX>.DAT` for a full-exchange scan, or `<NPA>-<NXX>-<X>.DAT`
for a partial scan.

### Header (256 bytes)

```
offset  size   field
0x00    2      magic (0x1A 0x0F for ToneLoc 1.10+)
0x02    2      version
0x04    8      config-nickname (ASCII, null-padded)
0x0C    4      timestamp of scan start (DOS date/time)
0x10    4      timestamp of last update
0x14    4      total numbers in range
0x18    4      numbers scanned so far
0x1C    ...    various counters: carriers found, tones found,
               voices found, busies, rings, etc.
0xFF    -      end of header
```

### Body (one nibble per number)

The remaining bytes hold **one nibble (4 bits) per number** in
scan-range order. Each nibble encodes:

| Value | Meaning |
|---|---|
| 0x0 | UNSCANNED |
| 0x1 | BUSY |
| 0x2 | VOICE |
| 0x3 | NOANS / RINGOUT |
| 0x4 | CARRIER (banner logged to FOUND.LOG by timestamp) |
| 0x5 | TONE (dial tone, fax, etc.) |
| 0x6 | ABORTED |
| 0x7 | BLACKLIST |
| 0x8-0xF | reserved / version-specific |

Two nibbles per byte, low nibble = even-indexed number, high nibble =
odd-indexed. For a 10,000-number exchange the body is ~5000 bytes.

### Why a CTF hands you one

The `.dat` is the puzzle state. Recovering the CARRIER positions (or an
oddball status) gives you which numbers answered as what — without
re-dialing, and often without any surviving `FOUND.LOG`. Render with
`TONELOC /S` or `tlreport`; or parse the body directly (offset + nibble
extraction).

Common CTF pattern: a `.dat` where exactly one number is 0x4 (CARRIER)
in a sea of 0x0 (UNSCANNED) — that lone number is the flag or points
to it.

## Scan-parameter dictionary

| Param | Config key | Effect if raised | Effect if lowered |
|---|---|---|---|
| Ring count | `RINGCOUNT` | Catches slow PBXs, big timeouts | Faster scan, misses slow answerers |
| Carrier wait | `CARRIERTIME` | Catches slow far-end modems | Misses real carriers as RINGOUT |
| Inter-call delay | `NUISDELAY` / `NUISANCE` | Fewer fraud-heuristic hits, slower scan | Faster; may trip CO fraud alarms |
| Nudge string | `NUDGE` | Elicits banner from stubborn modems | Bare-CONNECT scan; less info |
| Random order | `RANDOMDIAL` | Detection-resistant | Miss patterns emerge in log order |
| Blacklist | `BLACKLIST` | Skips known-hostile numbers (911, etc.) | Legal risk |

## Modern equivalents

- **WarVOX** (H. D. Moore, 2009) — records audio, classifies offline.
  Finds voicemail and IVRs, not just modems.
- **PhoneSweep** (Sandstorm) — commercial audit tool with a live UI.
- **iaxflood / SIPScan** — SIP-endpoint enumeration analog.

For SIP scans, "dial" is an INVITE and "answer" is a 200 OK with an
RTP stream; classify the RTP the way WarVOX classifies a WAV.

## See also

- [[war-dialing/README]] — tools, result categories, modern relevance
- [[war-dialing/toneloc-tuning]] — classifier internals + false-positive
  patterns + banner-fingerprint quickref
- [[records/README]] — banner fingerprints as typed records
  (`system_fingerprint`)

## Sources

- ToneLoc documentation (Minor Threat & Mucho Maas, 1994) — the `.dat`
  and `.log` formats and config parameters
- THC-Scan documentation (van Hauser / THC, 1996)
- Sandstorm PhoneSweep user manual
- H. D. Moore, WarVOX release notes and talks (2009)
