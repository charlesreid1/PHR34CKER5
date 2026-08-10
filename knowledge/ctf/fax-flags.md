# FAX FLAGS

> The flag isn't in the tones. The flag is the page. The tones just convince
> the far end to send it.

A **fax flag** is a CTF target where the payload is a **facsimile page** — a
QR code, an ASCII banner, or a block of text — that the far end will only
transmit once it believes a fax is calling. Your job: sound like a fax, then
capture and decode the page.

## First 15 seconds

- Pickup, then a continuous **CED** squawk: **2100 Hz** for ~2.6–4.0s (the
  called fax saying "yes, I am a fax, proceed").
- Immediately after, the **V.21 preamble** — a warbling 300-baud FSK tone —
  carrying DIS ("here's what I can do"). This framing is what distinguishes a
  fax from a bare data modem (`[[ctf/modem-carriers]]`).
- No spoken words, no menu. A pulsing 1100 Hz **CNG** instead would mean *you*
  dialed a machine that expects you to be the fax and is itself calling.

CED (2100 Hz) → recipe #7. See `docs/ctf_playbook.md` triage tree ("CED
(2100 Hz) → fax — recipe #7").

## How to probe it

1. `detect_tone(call_sid, targets=["ced","cng"])`. `ced` = the far end
   answered as a fax and wants you to send a page. `cng` (1100 Hz, 0.5s on /
   3s off) = the far end is a *calling* fax expecting you to answer as one.
2. To make a **called** fax train and send its page, present **CNG** so it
   knows a fax is on the line: `play_fax_cng_into_call(call_sid)`. It should
   answer with CED and begin the T.30 handshake (see `[[fax/README]]` for the
   full DIS/DCS/TCF/CFR dance).
3. To answer an **inbound** calling fax, present **CED**:
   `play_fax_ced_into_call(call_sid)` to trigger its training.
4. **Capture requires a real T.30 stack.** The tone synth here produces CNG/CED
   to *start* the conversation, but decoding image data (V.27ter/V.29/V.17 →
   T.4/T.6) needs SpanDSP or a hosted fax API (Phaxio, Documo, Twilio
   Programmable Fax). Route the call there to receive the page.

## Tools to reach for

- `detect_tone` (targets `ced` / `cng`) — which side of the handshake is this?
- `generate_fax_cng` / `play_fax_cng_into_call` — sound like a calling fax
- `generate_fax_ced` / `play_fax_ced_into_call` — answer as a fax
- `start_recording` — keep the raw handshake for timing analysis
- A real T.30 endpoint (SpanDSP / hosted) — the only thing that yields the page

```python
play_sequence(call_sid, [
    {"action": "wait_for_answer"},
    {"action": "detect_tone", "seconds": 4, "targets": ["ced", "cng"]},
    {"action": "cng", "cycles": 4},    # "I am a fax" — make the far end train
    {"action": "listen", "s": 6},      # expect CED + V.21 preamble back
])
# then bridge the call into a SpanDSP / hosted receiver to render the page
```

## What it means as a puzzle

- **The page IS the flag** — a QR code you scan, a text banner, a photo. Render
  the received TIFF/PDF and read it.
- **The handshake parameters can encode data** — an unusual DIS (odd
  resolution, custom subaddress/TSI string) may carry the clue.
- **Two-way fax** — the con may require you to *send* a specific page to get
  one back; replay a canned page (recipe #6) then receive (recipe #7).

## See also
- [[fax/README]] — the full T.30 handshake and CNG/CED reference
- [[ctf/modem-carriers]] — the other 2100 Hz answer tone; disambiguate
- [[2600hz/README]] — why fax answer sits at 2100, not 2600 Hz
- [[war-dialing/README]] — how fax lines were enumerated

## Sources
- ITU-T T.30 (procedures), T.4 / T.6 (image coding)
- SpanDSP (Steve Underwood) — reference open-source T.30 stack
- ITU-T V.27ter / V.29 / V.17 (fax modem carriers)
