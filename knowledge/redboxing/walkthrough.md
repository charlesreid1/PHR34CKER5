# RED BOX WALKTHROUGH — A 1993 ACTS CALL

> This is 1993, not last Tuesday. The fortress phone is a Bell single-slot,
> the switch is a 1AESS, and the coin receiver is still listening in-band.
> A time-annotated tour of one long-distance call. Timing math in
> `[[redboxing/acts-timing]]`; the summary tables in `[[redboxing/README]]`.

## The coin math first

ACTS asks for **$1.25**. There is no "dollar tone" to lean on (rare, often
unimplemented — see `[[redboxing/acts-timing]]`), so you pay it in quarters:

```
$1.25 ÷ $0.25 = 5 quarters  →  coin string "qqqqq"
```

Five quarters, each rendered as five 33 ms bursts of 1700+2200 Hz. Not to be
confused with the *nickel/dime* 66 ms cadence — five quarters is 25 fast
bursts total, in five groups of five.

## The call, step by step (what you hear at each beat)

| t (approx) | You do | You hear |
|-----------|--------|----------|
| 0:00 | Lift handset off-hook | Dial tone |
| 0:02 | Dial `1 + NPA + NXX-XXXX` (long distance) | Touch-tones, then a pause as the toll switch routes |
| 0:06 | (wait) | A soft click / cut-through, then the **ACTS voice**: *"Please deposit one dollar and twenty-five cents."* |
| 0:10 | **Do nothing for ~1 s** — let ACTS finish and open its coin receiver | Brief silence; ACTS is now listening for 1700+2200 Hz |
| 0:11 | Play `qqqqq` into the mouthpiece | Twenty-five fast dual-tone chirps, in five bursts-of-five, ~250 ms between coins |
| 0:15 | (wait) | ACTS tallies. On success: *"Thank you"* (or just silence) and the call **cuts through** — you hear ringing at the far end |
| 0:18 | — | Distant phone rings; conversation begins |

The felt rhythm: a machine asks, you answer in a burst of chirps, and the
line goes quiet-then-ringing. The pause at 0:10 matters — fire tones before
ACTS opens the receiver and the leading coins get clipped.

## Doing it with the MCP tools

Dialing is handled elsewhere; assume you hold a live `call_sid` sitting at
the ACTS prompt. Simplest form — render and inject the five quarters:

```python
generate_red_box("qqqqq")            # render the PCM (25 bursts, 1700+2200 Hz)
play_red_box_into_call(call_sid, coins="qqqqq")   # inject into the live call
```

The scripted form is better here because it handles the *timing* — it waits
for answer, pauses so ACTS can finish talking and open its receiver, deposits,
then listens for the result in one atomic call:

```python
play_sequence(call_sid, [
    {"action": "wait_for_answer"},                 # ACTS picks up
    {"action": "listen", "s": 4},                  # capture "deposit $1.25"
    {"action": "wait", "s": 1},                    # let the receiver open
    {"action": "redbox", "coins": "qqqqq"},        # five quarters
    {"action": "listen", "s": 5},                  # success? re-prompt? intercept?
])
```

`redbox` blocks until all 25 bursts have played out, so the trailing
`listen` captures ACTS's *reaction*, not your own tones bleeding over.

## Failure modes — what rejection sounds like

- **Re-prompt.** ACTS didn't tally enough: *"Please deposit twenty-five
  cents"* (the remaining balance) or a repeat of the full amount. Usually a
  clipped leading coin, tones too quiet (level off from −7 dBm0), or an
  off-hook receiver that hadn't opened yet. Pause longer, re-send the
  shortfall (`{"action": "redbox", "coins": "q"}`).
- **Timeout.** No valid coins detected in the window: dead air, then a
  reorder / fast-busy, then the switch tears the call down. Your `listen`
  returns a cadence, not a voice.
- **Operator intercept.** ACTS bails to a live TSPS operator: *"This is the
  operator, how can I help you?"* On a COCOT you'd get nothing at all — it
  never spoke ACTS and validated coins locally
  (`[[redboxing/acts-timing]]`). At a CTF the "operator" is a scripted IVR —
  probe it as one (`[[ctf/milliwatt-testlines]]` and the operator-services
  notes).

## See also
- [[redboxing/acts-timing]] — the burst tables, the tolerance window, the math
- [[redboxing/README]] — the short reference and coin/burst summary
- [[ctf/milliwatt-testlines]] — the sibling "listen to a test line" pattern

## Sources
- 2600 Magazine, Vol. 7, No. 3 (Autumn 1990) and later issues — ACTS call
  flow and red-box practice
- Phrack Vol. 3, Issue 33, File 9 (Sept 1991) — coin-tone timing
- Bellcore/Telcordia GR-506-CORE (LSSGR: Signaling) — ACTS coin service
