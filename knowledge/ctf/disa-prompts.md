# DISA PROMPTS

> The PBX that answers with a second dial tone is asking a question. The
> question is "do you have the PIN?" — and the con expects you to *earn* it,
> not hammer it.

**DISA** = Direct Inward System Access: a PBX feature that answers an inbound
call and hands you an *outbound* dial tone (historically for employees to
place company-billed calls from the road). At a CTF, a DISA-style target is a
gated prompt: get past the PIN and you reach the flag (an outdial, a code, a
next stage).

## First 15 seconds

- Pickup, then **silence** — no menu, no greeting. This dead air is the tell.
- Often a short **stutter dial tone** (interrupted dial tone) or a plain
  **second dial tone** inviting digits, sometimes a single terse beep.
- Occasionally one clipped prompt: "Enter authorization code" then silence.
- No "press 1 for…" narration — that would be an IVR (`[[ctf/ivr-mazes]]`).

Silence-with-a-prompt is the recipe #4 signature. See `docs/ctf_playbook.md`
triage tree ("Silence with periodic prompts → likely DISA — recipe #4").

## How to probe it

1. `detect_tone(call_sid, targets=["dial-tone"])` right after answer. A clean
   dial-tone (350+440 Hz) confirms it wants digits; `reorder`/`busy` means a
   wrong turn.
2. Note the **digit length** it expects: many DISA codes are a fixed 4–8
   digits, then a delimiter (`#`) or an automatic timeout.
3. Try a small **sanctioned** PIN/dictionary list — con-provided lists, obvious
   defaults, a code from another puzzle. This framing is a village-owned
   exercise, not an attack on live infrastructure.
4. **Back off on lockout.** If you hear reorder/fast-busy or the line drops
   after a few tries, stop. Space attempts with `wait`, cap total attempts,
   and treat a lockout as "the PIN comes from elsewhere," not "try faster."
5. A correct PIN typically yields a *fresh* dial tone or a confirmation tone —
   listen for the state change.

## Tools to reach for

- `detect_tone` (dial-tone / reorder / busy) to read line state between tries
- `play_dtmf_into_call` for a single attempt; `wait` to pace them
- `play_sequence` to script one paced attempt with a listen and a tone check:

```python
play_sequence(call_sid, [
    {"action": "wait_for_answer"},
    {"action": "detect_tone", "seconds": 3, "targets": ["dial-tone"]},
    {"action": "dtmf", "digits": "1234#"},   # one candidate
    {"action": "wait", "s": 2},
    {"action": "detect_tone", "seconds": 3},  # new dial tone == success
])
```

Run one attempt per `play_sequence`, inspect the result, then decide — never
loop blindly.

## What it means as a puzzle

- **The PIN is the whole game.** It almost always comes from another stage
  (an ANAC readback, a fax page, a menu cipher). DISA is the lock; the key is
  elsewhere.
- **The expected digit length leaks the format** of a code you find later.
- **Success = a new dial tone** you can then use — the con may score the digits
  you dial *after* the PIN.

## See also
- [[ctf/ivr-mazes]] — when the gate is a menu instead of a bare prompt
- [[war-dialing/README]] — "DIALTONE" hits are exactly this class of target
- [[blueboxing/README]] — the outdial you reach is the historical prize
- [[ess/README]] — the switches these PBXs hang off of

## Sources
- Telecommunications: DISA fraud advisories, FCC/telco bulletins (1990s)
- 2600 Magazine (various issues, early 1990s) on PBX and DISA abuse
- ITU-T Q.24 (DTMF signal reception) for the digit-collection side
