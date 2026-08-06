# R1 MF — THE FULL DIGIT TABLE

> The MANIFEST promised this file. Here it is: the multi-frequency
> signaling alphabet a blue box actually spoke to the trunk. Do not
> confuse it with DTMF — different frequencies, different purpose.

MF (Multi-Frequency) was the **inter-office** signaling of the pre-CCIS
North American network (R1 signaling). Where DTMF is what your *handset*
sends to your *local* switch, MF is what one *switch* sent to *another*
over a trunk — and a blue box impersonated the near switch. Each signal is
a pair of tones drawn from six frequencies: **700, 900, 1100, 1300, 1500,
1700 Hz.**

## The table

This is exactly the table `generate_mf` / `play_mf_into_call` emit:

| Signal | Tones (Hz)   | Notes                         |
|--------|--------------|-------------------------------|
| 1      | 700 + 900    |                               |
| 2      | 700 + 1100   |                               |
| 3      | 900 + 1100   |                               |
| 4      | 700 + 1300   |                               |
| 5      | 900 + 1300   |                               |
| 6      | 1100 + 1300  |                               |
| 7      | 700 + 1500   |                               |
| 8      | 900 + 1500   |                               |
| 9      | 1100 + 1500  |                               |
| 0      | 1300 + 1500  |                               |
| KP     | 1100 + 1700  | Key Pulse — start of address  |
| ST     | 1500 + 1700  | Start — end of address        |

Tone digits are ~**68 ms** on with ~68 ms between; **KP is longer (~100
ms)** because it primes the far register. Those are the defaults in the
generator (`tone_ms=68, gap_ms=68, kp_ms=100`).

In the code's alphabet: `K` = KP, `S` = ST. So a routing burst is written
`K<digits>S`.

## The ST-prime variants (KP2, STP, ST2P, ST3P) — read this carefully

Later/expanded MF used additional "start" signals to carry call-completion
and class-of-call information (e.g. coin vs. non-coin, or which digit field
just ended). You will see tables online listing STP / ST2P / ST3P and a
KP2 (inbound/international key pulse). **Their exact frequency assignments
are reported inconsistently across sources**, and this repo deliberately
does **not** synthesize them yet (see the comment in `tones.py`: "STP/ST2P/
ST3P variants omitted here; add when needed"). Treat any single online
table of these as *community-grade* until cross-checked against a Bell
System Technical Journal or Bellcore/Telcordia signaling reference. If a
CTF asks for one, verify the value before you trust it — this is exactly
the kind of detail DEF CON judges plant traps in.

## Worked example — `KP 1 800 555 1212 ST`

```
generate_mf("K18005551212S")
```

What the sequence is, tone by tone (all pairs from the table above):

```
KP     1100+1700   ~100 ms   "address follows"
1      700+900     ~68 ms
8      900+1500
0      1300+1500
0      1300+1500
5      900+1300
5      900+1300
5      900+1300
1      700+900
2      700+1100
1      700+900
2      700+1100
ST     1500+1700   ~68 ms    "address complete, route it"
```

To the far register this reads as: *"key pulse — route to 1-800-555-1212 —
start."* On the historical network, KP opened the register, the digits
filled it, and ST told the tandem the address was complete and to cut
through. Into a live call: seize with 2600 first (see
[[blueboxing/README]]), then `play_mf_into_call(sid, "K18005551212S")`.

## Why the frequencies don't collide with DTMF

MF uses 700–1700 Hz in 200 Hz steps; DTMF's high group reaches 1633 and
its low group starts at 697. The overlap is deliberate-adjacent but the
*pairs* never coincide, so a switch listening for MF wouldn't trip on a
subscriber's touch-tones leaking down a trunk.

## See also
- [[blueboxing/README]] — seizure, 2600 Hz, the attack in caricature
- [[dtmf/README]] — the *other* multi-frequency scheme
- [[2600hz/README]] — the supervision tone that opened the trunk
- [[tandem-stacking/README]] — chaining MF routes hop to hop

## Sources
- Bell System Technical Journal, "Signaling Systems for Control of
  Telephone Switching" (Nov 1960) — R1 MF frequencies and format
- Telcordia/Bellcore GR-506-CORE — signaling for LSSGR (MF timing)
- ITU-T Q.320-series — R1 MF register signaling
