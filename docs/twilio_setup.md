# TWILIO SETUP — PHR34CKER5

Everything you need to make PHR34CKER5 place real PSTN calls at
DEF CON / a phreaking CTF in 2026. Written after a session of
figuring this out the hard way, so future-you doesn't have to.

---

## TL;DR — the executive summary

1. **Upgrade to a paid Twilio account before the con.** Fund $20. Do
   not attempt to use trial mode at a live CTF. See
   [Trial mode is a trap](#trial-mode-is-a-trap) below.
2. **Buy one voice-capable US local number** ($1.15/mo). This becomes
   your `FROM_NUMBER`.
3. **Run `scripts/setup-twilio.sh`** to drop credentials at
   `~/.config/phr34cker5/env` and source that file from your shell rc.
4. **Set `PHR34CKER5_PUBLIC_URL`** to a VPS you control, or leave it
   unset to let PHR34CKER5 launch an ngrok tunnel for you.
5. **Ask the CTF organizers one question up front:** "Is the CTF
   endpoint a real PSTN number I can dial from the outside, or is it a
   con-local SIP address?" This changes everything (see
   [The CTF reality check](#the-ctf-reality-check)).

---

## The CTF reality check

Before you touch Twilio at all, read this. It saves money and dignity.

### DEF CON is at a convention center

DEF CON 2026 is at the **Las Vegas Convention Center (LVCC)**, not a
hotel property. That has several consequences the classic phreaking
mythology doesn't cover:

- **No hotel-room phones** attendees can dial from or to. The
  Bell-era "call the room, get a data drop" trick has no surface.
- **No payphones on the floor.** LVCC does not have working PSTN
  payphones. If you see one at the con, it's a **prop the Phreaking
  Village or TeleChallenge set up on purpose** — usually wired to an
  Asterisk box under a folding table, not to Ma Bell.
- **No usable "internal" phone system** for attendees. Convention
  center house phones are for staff/security and don't route arbitrary
  outbound.
- **The con Wi-Fi is famously hostile.** If you plan to run SIP or
  WebRTC over the con network, expect deep packet inspection, aggressive
  captive portals, and other people actively fucking with your traffic.
  Use LTE hotspot for anything sensitive.

So your **only reliable path onto the CTF's phone infra is the outside
PSTN**, dialed from a service you trust (Twilio) over a network you
trust (your phone's LTE, not con Wi-Fi).

### CTF numbers are almost never a human

Phreaking CTFs at DEF CON (TeleChallenge historically, the Phreaking
Village more recently) are built by people who own **Asterisk PBXs,
hobbyist crossbar switches, vintage step-by-step gear, and simulated
Bell-system fauna** for fun on their weekends. What they hand out as a
"phone number to call" is almost always one of:

- An **Asterisk extension** playing a recorded message or an IVR maze
- A **DISA prompt** waiting for a PIN
- A **voicemail box** with a puzzle in the greeting
- A **modem carrier** you're supposed to dial into
- A **fax machine** with the flag encoded in the transmission
- An **operator IVR** parodying 1970s Ma Bell
- A **simulated CN/A bureau, ANAC, milliwatt tone, or loop-around**
- A **conference bridge** with other players already on it

**A human picking up the phone and reading you a code back is not the
puzzle.** The puzzle *is* the phone network. Do not plan around getting
a person on the line — probably 1 in 10, maybe 0.5. See "human operator
likelihood" in this session for the reasoning.

### The endpoint might not be PSTN at all

Some village CTFs publish endpoints as **SIP URIs on the con's own
Asterisk** (`sip:1234@ctf.village.local` or similar) rather than as
real DIDs. Twilio can't reach those. If the CTF is SIP-only, you want:

- A softphone (Linphone, Zoiper, MicroSIP) on your laptop, or
- An IP phone / ATA with a handset if you want the tactile experience

Ask before the con starts. Organizers usually publish this on their
website or Discord/IRC channel a couple of weeks out.

---

## Getting a Twilio account and number

### Step 1 — sign up

https://www.twilio.com/try-twilio. Real email, real phone (for their
verification of *you*), real name. They will make you verify your
personal cell before doing anything.

You start in **trial mode**. Read the next section before you touch
anything else.

### Step 2 — trial mode is a trap

Twilio trial accounts have three restrictions that will destroy your
CTF weekend:

1. **Outbound calls can only reach numbers you've verified.** You add
   each destination number via Console → Phone Numbers → Verified
   Caller IDs, Twilio calls it, and it reads out a 6-digit code you
   have to enter. That's *inbound to the destination number*, meaning
   whoever is at the CTF number has to pick up and read a robocall code
   back to you. **This will not happen at a CTF.**
2. **Every call plays a trial-account preamble** ("You have a trial
   account, please upgrade…") before your audio is heard. This eats the
   first ~10 seconds of the call, well past the point where a modem or
   fax would have given up, and mangles CNG/CED detection.
3. **You get ~$15 of trial credit** and cannot buy additional numbers
   or top up.

**Fix: upgrade to a paid account before the con.** Fund $20 via credit
card. Restrictions above all go away. Domestic calls are ~$0.014/min
inbound and ~$0.014/min outbound. A full weekend of aggressive
dialing runs you $5–$15 all-in.

### Step 3 — buy a number

Console → Phone Numbers → Buy a Number.

- **Country:** United States (unless the CTF is elsewhere; even then
  a US number is usually fine and cheaper).
- **Capabilities:** check **Voice** (required). SMS / MMS / Fax are
  optional and don't matter for PHR34CKER5.
- **Type:** Local. Toll-free numbers cost more and add nothing here.
- Pick any area code. The first available will do.

Cost: **$1.15/month** for a US local voice number.

The E.164 number Twilio shows you (`+15551234567`) is your
`FROM_NUMBER`.

### Step 4 — you do NOT need to configure the number in the console

For **outbound** calls (PHR34CKER5's primary use case), the number is
just an identity. You don't wire up any webhooks. The TwiML that drives
the call is passed inline when `dial()` runs, pointing at PHR34CKER5's
own `/twiml/outbound` endpoint.

For **inbound** calls (someone dials your Twilio number and PHR34CKER5
answers), you'd point the "A Call Comes In" webhook at
`https://<your-public-url>/twiml/inbound`. Skip this until you actually
want inbound.

### Step 5 — grab credentials

Console home page shows:

- **Account SID** — starts with `AC…`, ~34 hex chars
- **Auth Token** — click to reveal, treat like a password

Copy both. You'll paste them into the setup script next.

---

## Getting PHR34CKER5 wired up

### The one-shot setup script

From the repo root:

```
scripts/setup-twilio.sh
```

It prompts for:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER` — the E.164 number you bought (`+15551234567`)
- `PHR34CKER5_PUBLIC_URL` — optional; the HTTPS URL where Twilio can
  reach PHR34CKER5 (see [Public URL](#public-url-two-topologies))
- `NGROK_AUTHTOKEN` — optional; only if you want the laptop-mode
  ngrok fallback

It writes `~/.config/phr34cker5/env` with `chmod 600`, verifies the
credentials against the Twilio API if the SDK is installed, and prints
the exact `source` line to add to your shell rc (bash / zsh / fish
detected from `$SHELL`).

### Verify

```
python -c "from phr34cker5_mcp.runtime import TwilioRuntime; \
           print(TwilioRuntime().ensure_started())"
```

Should print the public URL PHR34CKER5 will use. If it errors on
missing env vars, you didn't `source` the env file in the current
shell.

---

## Public URL — two topologies

Twilio's Media Streams need to reach a WebSocket endpoint on the public
internet over TLS. PHR34CKER5 supports two ways to give them one.

### Option A — VPS (recommended for the con)

You own a small VPS (Hetzner, DigitalOcean, Linode, whatever) with a
DNS name pointing at it and a valid TLS cert (Caddy makes this
one-line). PHR34CKER5 runs there.

```
PHR34CKER5_PUBLIC_URL=https://phr34cker5.example.com
PHR34CKER5_BIND_HOST=127.0.0.1
PHR34CKER5_BIND_PORT=8787
```

Caddy sits in front on 443 and reverse-proxies to `127.0.0.1:8787`.
Systemd unit keeps PHR34CKER5 running.

Why this is the answer at the con: **you do not want your laptop in
the middle of anything**. Con Wi-Fi is hostile. Your laptop will
suspend, roam, drop, get rebooted. A VPS just sits there answering
Twilio.

### Option B — laptop + ngrok

Fine for local development, not the con.

```
# leave PHR34CKER5_PUBLIC_URL unset
NGROK_AUTHTOKEN=<from ngrok dashboard>
```

PHR34CKER5 launches a pyngrok tunnel on startup and uses that URL.
Requires the `ngrok` extra: `pip install "phr34cker5-mcp[ngrok]"`.

---

## Gotcha checklist — the things that will bite you

Ranked roughly by how often they show up.

- **"The number you dialed is unverified"** → you're still on trial and
  haven't verified the destination number. Upgrade or verify.
- **"The number is not a valid phone number"** → not E.164. Include the
  `+` and country code. `+15551234567`, never `5551234567` or
  `(555) 123-4567`.
- **`FROM_NUMBER` was bought without Voice capability** → the call
  errors before it dials. Buy a Voice-capable number in Console →
  Phone Numbers → Active Numbers → your number → Capabilities.
- **Everything works but the far end hears silence** → your public URL
  is wrong, or Twilio can't reach the WebSocket. Check
  `curl https://<your-public-url>/healthz` from another machine and
  make sure the Twilio debugger (Console → Monitor → Logs → Errors)
  is not showing 12200 / 11200 / 31920.
- **Media Streams work locally but not from the VPS** → your Caddy /
  nginx reverse proxy needs `Upgrade` / `Connection: upgrade` headers
  passed through for the WebSocket. Caddy does this automatically.
  nginx needs an explicit `proxy_set_header Upgrade $http_upgrade;`
  block.
- **CNG plays but no fax handshake comes back** → the far end isn't a
  fax, or is a fax but has ATA/G.729 transcoding stripping the tones.
  Not something you can fix from your side.
- **Twilio's outbound call ends with "an application error occurred"**
  → check the Console → Monitor → Logs. Almost always your
  `/twiml/outbound` endpoint returned an error or a non-XML body.
- **You get charged $$$ for a stuck call** → PHR34CKER5's outbound
  TwiML has a `<Pause length="3600"/>` (one hour) after `<Stream>` so
  the call doesn't hang up mid-stream. If your MCP crashes without
  calling `hangup(call_sid)`, that call runs for up to an hour before
  Twilio bills you the cutoff. **Always** wrap experiments in a
  `try/finally` that calls `hangup()`, or set a shorter `<Pause>` at
  the cost of shorter interactions.

---

## Consent, legality, and the sniff test

- **Two-party consent states** (CA, FL, IL, MD, MA, MT, NH, PA, WA, and
  a couple of others) require *all* parties to consent to a call being
  recorded. PHR34CKER5's `start_recording()` is convenient and legally
  loaded. At a con, the CTF is knowingly on-record — the puzzle assumes
  it. Elsewhere, be careful.
- **Autodialing/blasting** — do not use this for cold outbound to real
  numbers. Twilio will terminate your account fast, and TCPA damages
  are $500–$1500 *per call*.
- **Play tones only into calls you set up.** Injecting red-box tones
  into a real 2026 telco payphone is not going to accomplish anything
  (ACTS died with the ILECs' payphone divestitures) and is illegal in
  spirit if not by statute.
- **The CTF is the sanctioned space.** Play there.

---

## The environment variables, all of them

| Var                       | Required? | What it is                                                       |
|---------------------------|-----------|------------------------------------------------------------------|
| `TWILIO_ACCOUNT_SID`      | yes       | Account SID, `AC…`                                               |
| `TWILIO_AUTH_TOKEN`       | yes       | Account auth token                                               |
| `TWILIO_FROM_NUMBER`      | yes       | E.164 number PHR34CKER5 calls from (`+15551234567`)              |
| `PHR34CKER5_PUBLIC_URL`   | either    | Public HTTPS URL of your PHR34CKER5 (VPS mode)                   |
| `NGROK_AUTHTOKEN`         | either    | ngrok auth token (laptop/dev mode; requires `[ngrok]` extra)     |
| `PHR34CKER5_BIND_HOST`    | no        | Interface to bind uvicorn to (default `127.0.0.1`)               |
| `PHR34CKER5_BIND_PORT`    | no        | Port to bind uvicorn to (default `8787`)                         |

"either" = you need one of `PHR34CKER5_PUBLIC_URL` or `NGROK_AUTHTOKEN`.
VPS mode should always use `PHR34CKER5_PUBLIC_URL`.

---

## A minimal end-to-end smoke test

Before the con, in the safety of your kitchen. Verify your own cell in
the Twilio console first if you're still on trial. From an MCP client:

```
dial("+1YOUR_CELL_HERE")
wait_for_answer(call_sid)          # picks up on your phone
play_fax_cng_into_call(call_sid)   # your cell squawks 1100 Hz at you
wait(15)
hangup(call_sid)
```

If your cell rings, you answer, and you hear the fax squeal — the
whole stack works. If any of those steps fails, the debugger at
Console → Monitor → Logs → Errors will tell you exactly which one.

---

## Sources / further reading

- Twilio Voice REST API: https://www.twilio.com/docs/voice/api/call-resource
- Twilio Media Streams: https://www.twilio.com/docs/voice/twiml/stream
- Twilio pricing: https://www.twilio.com/pricing
- DEF CON Phreaking Village (check for current-year info at
  defcon.org's villages page)
- TeleChallenge (historical): https://www.telechallenge.org
- The ITU-T T.30 spec if you want to go deeper on fax
