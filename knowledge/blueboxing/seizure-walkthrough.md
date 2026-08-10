# SEIZING A TRUNK — A TIME-ANNOTATED WALKTHROUGH

> "You don't shout at the trunk. You wait for it to answer, then you
>  tell it a lie it was built to believe."

A step-by-step domestic seizure as it sounded from the caller's end on a
~1975 outbound toll trunk. Operational companion to [[blueboxing/README]]
(the concept) and [[blueboxing/mf-tones]] (the full R1 MF digit table +
the KP2 / ST-prime dispute — not repeated here).

**The premise:** play 2600 Hz over an answered long-distance call, the near
tandem hears "far end hung up," drops billing, and hands you a fresh
register — you then MF-pulse a new destination as if you were the
originating office.

## The timeline

| t (approx) | You do | You hear |
|---|---|---|
| 0.0 s | Dial a long-distance number you legitimately reach | ringback |
| ~4 s | (far end answers) | answer + far party's "hello", room tone |
| +0 ms | Apply **2600 Hz** | far audio cuts to silence under the tone |
| ~700 ms | Stop 2600 Hz | the **wink** (see below) |
| +~100 ms | Send **KP** (1100+1700) | short chirp, register now open |
| then | Send digits | rapid MF chatter, ~68 ms/tone |
| then | Send **ST** (1500+1700) | last chirp — tandem cuts through |
| after | (routing) | ringback on the *new* leg |

## The 700 ms is switch-dependent — do not treat it as one number

The seizure hold time is a dispute the record carries, not a constant
(`sf_2600` in `records/tones.json`): **4ESS wanted >=400 ms**, some **1ESS
installations needed ~650 ms**, community canon cites **750-1000 ms "safe."**
~700 ms is a reasonable domestic default; if it fails, go longer before
concluding the trunk isn't SF at all. Level: 2600 sits at -20 dBm0 idle
guard, ~-8 dBm0 while pulsing.

## What the wink sounds like

Not a tone — an *event*. When the near tandem accepts the "disconnect" it
throws the trunk back to a signaling-ready state: a brief **ka-chirp / blip
of silence**, sometimes a faint reorder-like stutter, then a hollow,
dead-sounding open trunk. That hollow openness *is* the "come ahead." You
KP into it.

## MCP tools — two ways to drive it

Step-at-a-time (`K` = KP, `S` = ST per [[blueboxing/mf-tones]]; MF defaults
`tone_ms=68, gap_ms=68, kp_ms=100`):

```
play_2600_into_call(sid, ms=700)          # seize
play_mf_into_call(sid, "K18005551212S")   # KP 1-800-555-1212 ST
```

Or as one atomic scripted sequence (timing handled between steps):

```
play_sequence(sid, [
    {"action": "wait_for_answer"},
    {"action": "2600", "ms": 700},
    {"action": "detect_tone", "s": 3},          # listen for the wink
    {"action": "mf", "digits": "K18005551212S"},
    {"action": "listen", "s": 5},               # ringback on the new leg?
])
```

## Failure modes — and what each one tells you

- **No wink came back.** The far side likely never spoke SF — the route
  migrated out-of-band (CCIS, later SS7); your 2600 is just audio and call
  state never changed. This is what killed the trick on major US routes by
  ~1990.
- **Nothing happened; audio just resumed.** 2600 was **too short** for that
  switch — bump toward 1000 ms and retry.
- **The call dropped / you got flagged.** 2600 held **too long** trips the
  "hold-time exceeded" alarms (1AESS generic 1AE7+, 4ESS) and AT&T's
  *greenstar* logging. Overlong tone is the loud way to get noticed.
- **Wink, then reorder after ST.** Register opened but rejected the address
  — wrong digit count / nature-of-address, or that tandem won't route there.

## See also
- [[blueboxing/README]] — the attack in caricature
- [[blueboxing/mf-tones]] — full R1 MF table, KP/ST, the KP2 dispute
- [[2600hz/whistle-tolerances]] — why the detector accepted a crude whistle
- [[tandem-stacking/international]] — after the seize, chaining hops
- [[ess/README]] — the switches (1ESS/4ESS) whose hold times differ above

## Sources
- Bell System Technical Journal, Vol. 39 No. 6 (Nov 1960), pp. 1319-1408
  — SF supervision + MF pulsing format and levels.
- Ron Rosenbaum, "Secrets of the Little Blue Box," Esquire, Oct 1971
  — historical framing, not a technical primary source.
- 2600 Magazine (various issues) — community seizure walkthroughs and the
  switch-dependent hold-time lore.
