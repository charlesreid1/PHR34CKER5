# PhreakMe CTF — Trivia Ext 1101 flag rejection report

**Date:** 2026-08-08
**Player:** `ch4zm` (user id `145`, team id `51`)
**Target number:** (219) 500-2600
**Challenge:** `Trivia - Ext 1101` (`challenge_id = 76`, category `Trivia`, value 10)

## TL;DR

The IVR clearly announces **"The flag is ollama bell"** after we correctly
answer the Ext 1101 trivia question with `2600#`. Every reasonable spelling
of that flag — plain, cased, hyphenated, underscored, wrapped in
`flag{...}` / `phreakme{...}` — is rejected as **incorrect** by
`POST /api/v1/challenges/attempt` with status `200 {success: true, data:
{status: "incorrect", message: "Incorrect"}}`. Please clarify:

1. Is the flag we hear on the phone the actual submission string, or a
   decoy?
2. If it's real, what's the exact canonical form (casing / separator /
   wrapper)?
3. What is the "player PIN" the recording asks for, and where in the CTFd
   UI is it exposed?

## Reproduction

### 1. Dialed the number and pressed `1`, `1`, then `2600#`

Using Twilio, TwiML:

```xml
<Response>
  <Pause length="6"/><Play digits="1"/>        <!-- main menu → trivia -->
  <Pause length="7"/><Play digits="1"/>        <!-- trivia sub-menu → start Q1 -->
  <Pause length="10"/><Play digits="2600#"/>   <!-- answer -->
  <Pause length="30"/>
</Response>
```

### 2. Transcript of the response (dual-channel Twilio recording)

Recording: `.recordings/trivia_ans_RE8df9b89c08a2742ca9d386da877bd0d5.mp3`

Verbatim (Gemini 2.5 Flash / Pro on OpenRouter, verified by the user
listening at their machine):

> Welcome to PhreakMe. Abandon all hope, ye who dial here.
> *[DTMF `1`]*
> You've reached the trivia section. If you would like to go back to the
> previous section, dial zero. You can also start with the first question
> by dialing one.
> *[DTMF `1`]*
> In the early days of the Bell System, what was the specific resonant
> frequency in hertz used by phreaks to signal all trunks and bypass toll
> billing?
> *[DTMF `2 6 0 0 #`]*
> **That is correct. You entered two six zero zero.**
> **The flag is `ollama bell`.**
> Manual submission is available at the PhreakMe CTF website. Enter
> player PIN now to process auto claim.

Two independent runs of ASR produced `"OLama Bell"` (Flash) and
`"Ola Ma Belle"` (Pro); the user identified the actual spoken flag as
**`ollama bell`** when playing the recording locally.

### 3. Every reasonable submission is `incorrect`

`POST https://phreakme.com/api/v1/challenges/attempt`
with `Content-Type: application/json`, `CSRF-Token: <session csrf>`,
body `{"challenge_id": 76, "submission": "<flag>"}`.

All 21 of the following returned `{"success": true, "data": {"status":
"incorrect", "message": "Incorrect"}}`:

| # | Submission |
|---|---|
| 1 | `OLama Bell` |
| 2 | `Olama Bell` |
| 3 | `flag{OLama Bell}` |
| 4 | `phreakme{OLama Bell}` |
| 5 | `OLamaBell` |
| 6 | `Alexander Bell` |
| 7 | `Alexander Graham Bell` |
| 8 | `Ma Bell` |
| 9 | `AT&T` |
| 10 | `Bell System` |
| 11 | `Ada Bell` |
| 12 | `Ola Ma Belle` |
| 13 | `Olama Belle` |
| 14 | `Olamabelle` |
| 15 | `Ola Ma Bell` |
| 16 | `Aloha Ma Belle` |
| 17 | `ollama bell` ← the spoken flag |
| 18 | `Ollama Bell` |
| 19 | `ollamabell` |
| 20 | `Ollama bell` |
| 21 | `OllamaBell` |
| 22 | `OLLAMA BELL` |
| 23 | `ollama_bell` |
| 24 | `ollama-bell` |
| 25 | `flag{ollama_bell}` |
| 26 | `phreakme{ollama_bell}` |
| 27 | `PhreakMe{ollama_bell}` |
| 28 | `PHREAKME{ollama_bell}` |
| 29 | `flag{OllamaBell}` |
| 30 | `flag{ollama bell}` |
| 31 | `2600` |
| 32 | `flag{2600}` |

Rate limiting kicks in around ~6 attempts per minute per session (`{"status":
"ratelimited"}`), which the harness respects with a 15 s backoff.

## The "player PIN" mystery

The IVR ends with:

> *Manual submission is available at the PhreakMe CTF website. Enter
> player PIN now to process auto claim.*

We can't find any "PIN" or "Player PIN" field in the CTFd UI:

- `/settings` HTML inputs: `name`, `email`, `confirm`, `password`,
  `affiliation`, `website`, plus a `token` (CTFd API access token) generator
  with `expiration`. **No `pin` field.**
- `/api/v1/users/me` returns `country`, `email`, `fields`, `id`,
  `team_id`, `oauth_id`, `affiliation`, `bracket_id`, `name`, `language`,
  `website`, `place`, `score` — **no `pin` field**.
- `/api/v1/teams/me` — same, no `pin`.
- Grep for `PIN` across `/`, `/challenges`, `/settings`, `/profile`,
  `/team`, `/scoreboard`, `/notifications`, `/PhreakTel` returns only
  incidental hits (`pin-nav.js` asset, the string `pines` in `pipelines`).

So either:

- The PIN is generated somewhere non-obvious (a hidden challenge? a
  registration email we missed? profile field we haven't unlocked?).
- The PIN feature is not yet wired, and manual submission is the only
  path — in which case the flag string above should just… work.

## What we've verified end-to-end

- ✅ We can place PSTN calls to `+12195002600` from
  `+19289778173` (Twilio SID `AC_REDACTED`).
- ✅ DTMF via `<Play digits>` is accepted by the IVR (it acknowledges
  `1 → trivia`, `1 → start Q1`, `2600# → correct`).
- ✅ Two-channel recording captures the announced flag consistently.
- ✅ CTFd login for `ch4zm` succeeds (redirects to `/challenges`).
- ✅ CSRF-Token from `window.init.csrfNonce` is accepted by
  `/api/v1/challenges/attempt`.
- ❌ Every attempted flag string for challenge id 76 is rejected.

## Ask

- **What is the exact canonical flag for `Trivia - Ext 1101`?** Casing,
  separator, wrapper (`flag{...}` vs bare)?
- **Where do we get / configure our player PIN** for the phone
  auto-claim flow?
- If the phone answer routes to a *different* challenge than the CTFd
  entry we're submitting to, please confirm the mapping between
  extension numbers and `challenge_id`s.

Everything else on the box works — just this last mile between "the IVR
says correct" and "CTFd accepts the string" is broken for us.
