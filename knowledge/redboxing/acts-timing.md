# ACTS COIN-TONE TIMING

> Two specs, one tolerance window, and the single mistake that gets you
> laughed out of the DEFCON quiz room. This is the reference layer for
> `[[redboxing/README]]`; the worked call lives in `[[redboxing/walkthrough]]`.

Every ACTS coin tone is the **same dual-tone pair — 1700 + 2200 Hz played
together** (not alternated), ±1.5%, at **−7 dBm0** per frequency. The coin
value is encoded *only* in the burst count and cadence. Get the pair wrong
and nothing decodes; get the cadence wrong and a quarter reads as a nickel.

## The two timing tables, side by side

| Coin | GR-506-CORE (Bellcore, primary — telco-side spec) | Phrack 33.9 (community canon — what homebrew boxes emitted) |
|------|---------------------------------------------------|-------------------------------------------------------------|
| Nickel (5¢)  | one 66 ms burst                    | one 60 ms pulse                       |
| Dime (10¢)   | two 66 ms bursts, 66 ms apart       | two 60 ms pulses, 60 ms apart         |
| Quarter (25¢)| **five 33 ms bursts, 33 ms apart**  | **five 35 ms pulses, 35 ms apart**    |
| Dollar ($1)  | one 650 ms burst (rare, not universal) | not documented                     |

**Which is right?** Both. GR-506-CORE is the authoritative Bellcore spec a
compliant ACTS coin-receiver was tuned to detect. Phrack 33.9's 60/35 ms
figures are what a generation of red boxes actually put on the line, and they
worked. Never silently pick one — cite the source with the number: "66/33 ms
per GR-506-CORE" vs. "60/35 ms per Phrack 33.9."

## Why the quarter is 5×33, NOT 5×66

Nickel and dime run on the **66 ms** cadence; the quarter runs on the **33 ms**
cadence — half the burst width and half the gap, five times. A quarter is
*faster and denser* than five nickels, not just "more of them." Conflating
them ("a quarter is five 66 ms bursts") is the classic trap: that's just a
malformed nickel train, and it's the root of the persistent "5×66 ms = a
dollar" myth (the dollar, where implemented at all, is a single 650 ms burst).
Remember one thing: **nickel/dime = 66, quarter = 33.**

## The tolerance window that let both specs work

ACTS coin-signal receivers tolerated roughly **±10–20%** slop on burst width,
so 60 ms and 66 ms both land inside a receiver expecting a "~66 ms nickel" —
Phrack-timed and spec-timed boxes were indistinguishable to the switch. That's
*why* the two number sets coexisted for twenty years without anyone's box
failing: the frequencies (±1.5%, tight) mattered far more than the millisecond
timing (loose).

## COCOT vs. LEC single-slot — where it worked and where it never did

Red-boxing only ever worked against a **LEC-owned "fortress" single-slot**
payphone whose 1700+2200 Hz coin receiver lived on the **toll switch**,
listening to the in-band signal off the 4-wire trunk. **COCOTs**
(Customer-Owned Coin-Operated Telephones) validated coins **locally** in the
phone's own board and post-paid the call — no in-band ACTS tone, nothing for a
red box to spoof. Same for the later Nortel Millennium, which generated ACTS
*inside* its own DSP after an internal sensor confirmed the coin. Playing tones
at a COCOT does nothing — which surprises people who assume every payphone is
the same target.

## The Radio Shack crystal swap (canonical homebrew box)

The famous build: a stock Radio Shack pocket tone dialer with its
**3.579545 MHz** colorburst crystal desoldered and a **6.5536 MHz** crystal
dropped in. The DTMF chip clocks every output frequency off the reference
crystal, so all tones scale by **6.5536 / 3.579545 ≈ 1.831**. The `*` key
(941 + 1209 Hz) therefore emits:

- 941 × 1.831 ≈ **1723 Hz** (target 1700 Hz — inside ±1.5%)
- 1209 × 1.831 ≈ **2213 Hz** (target 2200 Hz — inside ±1.5%)

That single coincidence is the whole reason for the 6.5536 MHz value. Store
five `*` presses in a memory slot and you have a quarter on tap. Two
canonical models: **Cat. No. 43-141** (the one in 2600, Autumn 1990) and its
successor **43-146** after Radio Shack discontinued the 43-141 on 1994-01-01.
Possession of exactly this modified dialer was the crux of the **Bernie S /
Ed Cummings** USSS case (18 USC 1029), a reason the community treats carrying
one as its own hazard.

## When and why it died (1996–2002)

- LEC single-slots migrated to T1/robbed-bit trunks that stripped in-band
  ACTS supervision (retrofits ~1996–2001).
- COCOTs and Millennium-class phones did coin validation locally from the
  start — never vulnerable.
- RBOC payphone divestitures (2000–2007) retired the remaining plant.

By ~2002 red-boxing was inert in North America. It survives as CTF lore and
as a tone-generation exercise — `generate_red_box("q")` still renders a
period-correct quarter for a challenge that's *simulating* 1993.

## See also
- [[redboxing/README]] — the short overview and the coin/burst summary
- [[redboxing/walkthrough]] — a time-annotated 1993 ACTS call, tone by tone
- [[dtmf/README]] — why the crystal swap trades touch-tone for ACTS tones
- [[greenboxing/README]] — the operator side of coin signaling

## Sources
- Bellcore/Telcordia GR-506-CORE (LSSGR: Signaling), coin-service section —
  66/66/33 ms and the 650 ms dollar
- Phrack Vol. 3, Issue 33, File 9, "A REAL Functioning RED BOX Schematic"
  (Sept 1991) — the 60/60/35 ms community figures
- 2600 Magazine, Vol. 7, No. 3 (Autumn 1990), "Converting a Tone Dialer into
  a Red Box" — the 43-141 crystal swap
- 2600 Magazine (various issues) — the 43-146 successor and field practice
