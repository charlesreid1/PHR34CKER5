# Redbox #74 — Call 212-555-1337 → **"Radio Shack"** (100 pts)

- **Challenge:** `Redbox / Call - 212-555-1337` (`challenge_id = 74`, 100 pts, 6 solves before us)
- **Flag:** `Radio Shack`
- **Solved:** 2026-08-08

## Play-by-play

1. Dialed `+12195002600` (PhreakMe main IVR).
2. Pressed **`2`** → landed in the PBX extension prompt: *"If you know the extension of the party you wish, dial it now."*
3. Dialed **`2125551337`** → got: *"Please deposit 25 cents."*
4. Injected a Red Box quarter tone via TwiML `<Play>` pointing at a Twilio-hosted WAV of one ACTS `q` burst (1700+2200 Hz, 33ms on / 33ms off × 5).
5. IVR response:

   > You didn't pay for that call and are stealing from IX. Good. They have enough money already. The flag is **two words**. **Radio Shack**. You may now enter this flag manually on the PhreakMe CTF website to receive your points. Or, for immediate credit, please enter your player PIN now.

## Full TwiML used

```xml
<Response>
  <Pause length="6"/><Play digits="2"/>
  <Pause length="5"/><Play digits="2125551337"/>
  <Pause length="6"/><Play>https://phreakme-tones-5443-live.twil.io/redbox_q.wav</Play>
  <Pause length="60"/>
</Response>
```

## Submission

```
POST https://phreakme.com/api/v1/challenges/attempt
CSRF-Token: <session csrfNonce>
Content-Type: application/json

{"challenge_id": 74, "submission": "Radio Shack"}
```

Response: `{"success": true, "data": {"status": "correct", "message": "Correct"}}`.

## Artifacts

- Recording: `.recordings/redbox_pay_RE87e466995a7650d80cd3c7a4952068f2.mp3`
- Tone WAV: `.tones/redbox_q.wav` (4796 bytes, 8kHz mono PCM, 0.297s)
- Twilio Call SID: `CA3fdd31b3e1beb281b71eb00773f3d6f7`

## Design note

The joke is Radio Shack — they infamously sold the "Pocket Tone Dialer" (part #43-141) that phreakers reprogrammed with a 6.5536 MHz crystal to produce the ACTS coin tones. So the *tool* for redboxing is what the challenge asks for.
