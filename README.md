# PHR34CKER5

```
          _____                    _____                    _____                    _____                    _____                    _____
         /\    \                  /\    \                  /\    \                  /\    \                  /\    \                  /\    \
        /::\    \                /::\____\                /::\    \                /::\    \                /::\    \                /::\____\
       /::::\    \              /:::/    /               /::::\    \              /::::\    \              /::::\    \              /:::/    /
      /::::::\    \            /:::/    /               /::::::\    \            /::::::\    \            /::::::\    \            /:::/    /
     /:::/\:::\    \          /:::/    /               /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/    /
    /:::/__\:::\    \        /:::/____/               /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \        /:::/____/
   /::::\   \:::\    \      /::::\    \              /::::\   \:::\    \      /::::\   \:::\    \      /::::\   \:::\    \      /::::\    \
  /::::::\   \:::\    \    /::::::\    \   _____    /::::::\   \:::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \    /::::::\____\________
 /:::/\:::\   \:::\____\  /:::/\:::\    \ /\    \  /:::/\:::\   \:::\____\  /:::/\:::\   \:::\    \  /:::/\:::\   \:::\    \  /:::/\:::::::::::\    \
/:::/  \:::\   \:::|    |/:::/  \:::\    /::\____\/:::/  \:::\   \:::|    |/:::/__\:::\   \:::\____\/:::/  \:::\   \:::\____\/:::/  |:::::::::::\____\
\::/    \:::\  /:::|____|\::/    \:::\  /:::/    /\::/   |::::\  /:::|____|\:::\   \:::\   \::/    /\::/    \:::\  /:::/    /\::/   |::|~~~|~~~~~
 \/_____/\:::\/:::/    /  \/____/ \:::\/:::/    /  \/____|:::::\/:::/    /  \:::\   \:::\   \/____/  \/____/ \:::\/:::/    /  \/____|::|   |
          \::::::/    /            \::::::/    /         |:::::::::/    /    \:::\   \:::\    \               \::::::/    /         |::|   |
           \::::/    /              \::::/    /          |::|\::::/    /      \:::\   \:::\____\               \::::/    /          |::|   |
            \::/____/               /:::/    /           |::| \::/____/        \:::\   \::/    /               /:::/    /           |::|   |
             ~~                    /:::/    /            |::|  ~|               \:::\   \/____/               /:::/    /            |::|   |
                                  /:::/    /             |::|   |                \:::\    \                  /:::/    /             |::|   |
                                 /:::/    /              \::|   |                 \:::\____\                /:::/    /              \::|   |
                                 \::/    /                \:|   |                  \::/    /                \::/    /                \:|   |
                                  \/____/                  \|___|                   \/____/                  \/____/                  \|___|
```

> A time machine to 1997.

**PHR34CKER5** is a CTF phreaking co-pilot: a corpus of lore *and* a
live-telephony toolbox exposed over the Model Context Protocol (MCP), plus
a companion **Skill** that teaches any MCP-capable assistant (Claude Desktop,
Claude Code, opencode) to use it. It knows the history — blueboxing,
red-boxing, ACTS, ESS, CN/A, T.30 — and it can act on it: synthesize tones,
place PSTN calls via Twilio, script sequences, and record.

## What can it do?

Three tiers, from knowing to acting:

- **Know** — corpus tools: `list_topics`, `search_lore`, `read_lore`, `random_lore`, plus typed-record lookups (`lookup_tone`, `verify_claim`, `explain_technique`)
- **Synthesize** — tone generators: DTMF, R1 MF, red box, fax CNG/CED, 2600 Hz
- **Act** — live-call tools: `dial`, `wait_for_answer`, `play_*_into_call`, `listen`, `record`
- **Perceive** — read the line back: `detect_tone`, `dtmf_decode`, `transcribe`, and `play_sequence` to script a whole call plan

The canonical move is to script all three together — "dial X, wait for
answer, wait 10s, deposit 75¢, listen for 5s, hang up":

```
call = dial("+14155551212")
wait_for_answer(call["call_sid"])
wait(10)
play_red_box_into_call(call["call_sid"], "qqq")
listen(call["call_sid"], seconds=5)
hangup(call["call_sid"])
```

## Repo map

```
src/phr34cker5_mcp/    the MCP server (installable Python package)
knowledge/             prose corpus (one topic per dir) + records/ (typed, cited facts)
skills/phreaking/      the SKILL.md that tells assistants to use the MCP
scripts/               user-facing shell helpers (credential setup, etc.)
docs/                  long-form guides that don't fit in the README
tests/                 pytest suite (pure-DSP + fake-runtime; no network)
```

See [`scripts/README.md`](scripts/README.md) for why `scripts/` and `src/`
are separate, and [`docs/`](docs/) for the long-form guides.

## MCP tools

### Corpus (read-only)

| tool | what it does |
|---|---|
| `list_topics()` | every topic and file in the corpus |
| `read_lore(topic, name)` | one file's contents |
| `search_lore(query, max_results=20)` | case-insensitive regex/substring search |
| `random_lore()` | one random file — for inspiration |

Every markdown file is also exposed as an MCP **resource** at
`phr34cker5://<topic>/<name>`, plus a `phr34cker5://index` resource with a
human-readable table of contents.

### Knowledge retrieval (typed records)

The prose corpus is what the assistant *reads*; the typed records under
[`knowledge/records/`](knowledge/records/) are what it *looks facts up in* —
numbers, not adjectives, each dated and cited. These are the tools a DEFCON
judge's precision question should hit.

| tool | what it does |
|---|---|
| `lookup_tone(name)` | exact spec for a named tone/code — `frequencies_hz`, `tolerance`, `level_dBm0`, `on_ms/off_ms`, plus `disputed{}` and the citation envelope. Resolves aliases (`2600`, `KP`, `red box quarter`, `the whistle`) |
| `verify_claim(text)` | grades a claim `true / false / needs_qualification / unverified` against the trap catalog (e.g. "2600 Hz seizes an international trunk" → **false**; No.5 seizure is 2400 Hz). Won't bluff an unmatched claim |
| `explain_technique(name, year?, region?)` | step-by-step composition with vulnerability window; **always returns the steps** (old-school techniques are the point at a CTF). `year`/`region` add a non-blocking historical note, never a refusal |
| `bibliography(cite_id?)` | resolve a source id, or list all |
| `cross_reference(record_id)` | traverse a record's `see_also` links |
| `search_records(query?, category?, region?, year?)` | filter the KR — e.g. NANP `tone_signal`s effective in 1998 |

Every response carries the envelope `{citations[], era_bounds, region,
confidence ∈ {primary, secondary, community, folklore}}`. See
[`knowledge/records/README.md`](knowledge/records/README.md) for the schema.

### Tones (actionable)

Pure Python (stdlib `wave` + `math`, no numpy). Every tool writes a mono
8 kHz signed-16 WAV and returns `{path, duration_ms, sample_rate, …}`. If
`path` is omitted, the file lands in `$PHR34CKER5_TONE_DIR` (defaults to
`$TMPDIR/phr34cker5-tones/`).

| tool | what it does |
|---|---|
| `generate_tone(freq_hz, ms=1000, ...)` | one sine wave at any frequency |
| `generate_dual_tone(f1_hz, f2_hz, ms=1000, ...)` | two summed sines |
| `generate_dtmf(digits, tone_ms=100, gap_ms=80, ...)` | 0-9, `*`, `#`, A-D; `,`/`p`/space = pause |
| `generate_mf(digits, tone_ms=68, gap_ms=68, kp_ms=100, ...)` | R1 MF: 0-9, K (KP), S (ST) |
| `generate_sf_2600(ms=1000, ...)` | the 2600 Hz supervision tone |
| `generate_red_box(coins, ...)` | ACTS coin bursts: n / d / q |
| `generate_green_box(signal="collect", ...)` | operator coin control: collect / return / ringback |
| `generate_fax_cng(cycles=4, ...)` | T.30 CNG (1100 Hz, 0.5s on / 3s off) |
| `generate_fax_ced(ms=3000, ...)` | T.30 CED (2100 Hz continuous) |
| `generate_busy(cycles=4, ...)` | line-busy tone (480+620 Hz, 500/500 ms) |
| `generate_reorder(cycles=8, ...)` | reorder / fast-busy (480+620 Hz, 250/250 ms) |
| `generate_ringback(cycles=2, ...)` | audible ringback (440+480 Hz, 2s on / 4s off) |
| `generate_milliwatt(ms=10000, ...)` | 1004 Hz test tone — every CO had one |
| `generate_modem_carrier(rate="v22", ...)` | synthetic modem answer+carrier (bell103/v21/v22/v32/v34) |

The call-progress tones (`busy`, `reorder`, `ringback`, `milliwatt`,
`modem`) round-trip through `detect_tone` to the same classification, so
they double as detector fixtures. Each also has a `play_*_into_call`
injector and a `play_sequence` action.

Example — dial 1-820 as DTMF, then blue-box a `KP 1 800 555 1212 ST`
sequence:

```
generate_dtmf("1,820")
generate_mf("K18005551212S")
```

### Live telephony — Twilio

Real PSTN calls. Origination, live audio injection, live audio capture,
recording. The first call to any tool below lazy-boots a local FastAPI
server (TwiML webhooks + a bidirectional Media Streams WebSocket) and
opens an ngrok tunnel so Twilio can reach it.

**Requires Python 3.10–3.12** (uses stdlib `audioop` for μ-law).

> See [docs/twilio_setup.md](docs/twilio_setup.md) for the full CTF-focused
> Twilio playbook — buying a number, verifying credentials, VPS vs. laptop
> topologies, and the stuck-call budget footgun.

| tool | what it does |
|---|---|
| `dial(to, from_=None, record=False)` | place outbound PSTN call, returns `CallSid` |
| `hangup(call_sid)` | end call via REST |
| `list_calls()` | every call this MCP instance has seen |
| `call_status(call_sid)` | fresh Twilio status + local WS state |
| `call_log(call_sid)` | full local timeline (injects, marks, auto-hangup) with ms offsets — post-mortem |
| `wait_for_answer(call_sid, timeout_s=60)` | block until answered + WS connected |
| `wait_for_inbound(timeout_s=120, since_sid=None)` | block for an incoming call (target dials *you*; point the number's inbound webhook at `/twiml/inbound`) |
| `wait(seconds)` | sleep in a scripted sequence |
| `play_wav_into_call(call_sid, path)` | inject any mono 8kHz WAV |
| `play_tone_into_call(call_sid, freq_hz, ms)` | inject a single sine |
| `play_dtmf_into_call(call_sid, digits, ...)` | live DTMF (synthesized audio) |
| `send_dtmf_via_twilio(call_sid, digits)` | clean Twilio-generated DTMF for picky IVRs (ends the media stream) |
| `play_mf_into_call(call_sid, digits, ...)` | live blue-box MF |
| `play_2600_into_call(call_sid, ms=1000)` | live 2600 Hz |
| `play_red_box_into_call(call_sid, coins)` | live ACTS coin tones |
| `play_green_box_into_call(call_sid, signal="collect")` | live operator coin-control tones |
| `play_fax_cng_into_call(call_sid, cycles=4)` | live fax CNG |
| `play_fax_ced_into_call(call_sid, ms=3000)` | live fax CED |
| `play_busy_into_call` / `play_reorder_into_call` / `play_ringback_into_call` | live call-progress tones |
| `play_milliwatt_into_call(call_sid, ms=10000)` | live 1004 Hz test tone |
| `play_modem_carrier_into_call(call_sid, rate="v22", ...)` | live synthetic modem answer+carrier |
| `play_recording_into_call(call_sid, recording_url)` | replay a captured recording / any audio URL |
| `multi_call_bridge(call_sids, announce=None)` | bridge live calls into a Twilio conference |
| `listen(call_sid, seconds, save_wav=True)` | pull inbound audio to WAV |
| `start_recording(call_sid)` / `stop_recording` / `get_recording_url` | Twilio-native recording |

#### Perceive & orchestrate

The tools above are primitives. These compose and interpret them — script a
whole call plan, or figure out what's on the line.

| tool | what it does |
|---|---|
| `play_sequence(call_sid, steps)` | run a scripted call plan atomically; injection steps block until played out, so "send digits then listen" listens *after* the digits |
| `detect_tone(call_sid, seconds=3, targets=None)` | Goertzel classifier: dial-tone, busy, reorder, ringback, 2600, cng, ced, modem, milliwatt — with a cadence estimate to split busy from reorder |
| `dtmf_decode(call_sid, seconds=5)` | pull DTMF digits out of inbound audio (IVR / DISA playback) |
| `dtmf_decode_wav(path)` | same decoder, on a WAV file |
| `transcribe(call_sid, seconds=10)` | capture audio + start a Twilio recording/transcription for speech-to-text |

`play_sequence` steps are dicts keyed by `action` — `dtmf`, `mf`, `tone`,
`2600`, `redbox`, `cng`, `ced`, `wav`, `wait`, `wait_for_answer`, `hangup`,
`listen`, `detect_tone`, `dtmf_decode`, `transcribe`. The canonical
"deposit 75¢" flow as one call:

```
play_sequence(sid, [
    {"action": "wait_for_answer"},
    {"action": "wait", "s": 10},
    {"action": "redbox", "coins": "qqq"},
    {"action": "listen", "s": 5},
    {"action": "hangup"},
])
```

(For the primitive-by-primitive version of that sequence, see
[What can it do?](#what-can-it-do) at the top.)

#### Env vars

| var | required | notes |
|---|---|---|
| `TWILIO_ACCOUNT_SID` | yes | from console.twilio.com |
| `TWILIO_AUTH_TOKEN` | yes | keep it secret |
| `TWILIO_FROM_NUMBER` | yes | a Twilio-owned or verified E.164 number |
| `PHR34CKER5_PUBLIC_URL` | VPS mode | the public HTTPS URL Twilio will hit (e.g. `https://phreak.example.com`). When set, ngrok is not used. |
| `PHR34CKER5_BIND_HOST` | VPS mode | interface uvicorn binds to. Default `127.0.0.1`. Set `0.0.0.0` on a VPS. |
| `PHR34CKER5_BIND_PORT` | VPS mode | pin the local port so your reverse proxy has a stable upstream. Default: random ephemeral. |
| `NGROK_AUTHTOKEN` | laptop mode | free at ngrok.com. Only used when `PHR34CKER5_PUBLIC_URL` is unset. Requires `pip install "phr34cker5-mcp[ngrok]"`. |
| `MAX_CALL_MINUTES` | no | cost guardrail. Any call older than this is auto-hung-up by a watchdog — belt-and-suspenders on the 1-hour `<Pause>`. Unset/0 disables. Fractional OK. `call_status` reports `auto_hung_up`. |

Two deployment topologies:

##### A. VPS mode (recommended — no laptop in the middle)

The MCP runs on your server. Twilio talks directly to your domain over
TLS. Steps below use Caddy + systemd on a Debian/Ubuntu box; adapt to
your stack.

**1. Install:**

```sh
# on the VPS
sudo useradd -r -m -s /bin/bash phr34cker5
sudo -u phr34cker5 bash -lc '
  cd ~
  python3 -m venv .venv
  .venv/bin/pip install -U pip
  .venv/bin/pip install phr34cker5-mcp   # or: pip install -e /path/to/checkout
'
```

**2. `/etc/systemd/system/phr34cker5-mcp.service`:**

```ini
[Unit]
Description=PHR34CKER5 MCP (Twilio bridge)
After=network-online.target
Wants=network-online.target

[Service]
User=phr34cker5
WorkingDirectory=/home/phr34cker5
Environment=TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Environment=TWILIO_AUTH_TOKEN=your_auth_token
Environment=TWILIO_FROM_NUMBER=+15555550123
Environment=PHR34CKER5_PUBLIC_URL=https://phreak.example.com
Environment=PHR34CKER5_BIND_HOST=127.0.0.1
Environment=PHR34CKER5_BIND_PORT=8787
# Note: MCP servers typically talk stdio; on a VPS you'd usually run this
# under an MCP transport like SSE. For now, use --transport sse.
ExecStart=/home/phr34cker5/.venv/bin/phr34cker5-mcp --transport sse
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
```

Enable:

```sh
sudo systemctl daemon-reload
sudo systemctl enable --now phr34cker5-mcp
sudo systemctl status phr34cker5-mcp
```

**3. `/etc/caddy/Caddyfile`:**

```caddy
phreak.example.com {
    encode zstd gzip

    # Twilio Media Streams uses WebSocket; Caddy auto-upgrades.
    reverse_proxy 127.0.0.1:8787
}
```

```sh
sudo systemctl reload caddy
```

Caddy will provision a Let's Encrypt cert automatically. Confirm:

```sh
curl -sS https://phreak.example.com/healthz
# {"ok": true, "calls": 0}
```

**4. Point Twilio at your domain** — in the Twilio console, on the phone
number you're using: set **A Call Comes In** → Webhook →
`https://phreak.example.com/twiml/inbound` (for inbound calls). Outbound
calls use the URL the MCP passes to `dial()` at call time; no console
config needed.

##### B. Laptop mode (ngrok)

For local dev only. Install with the ngrok extra:

```sh
pip install "phr34cker5-mcp[ngrok]"
```

Add to your MCP config:

```json
{
  "mcpServers": {
    "phr34cker5": {
      "command": "uvx",
      "args": ["phr34cker5-mcp"],
      "env": {
        "TWILIO_ACCOUNT_SID": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "TWILIO_AUTH_TOKEN":  "your_auth_token",
        "TWILIO_FROM_NUMBER": "+15555550123",
        "NGROK_AUTHTOKEN":    "your_ngrok_token"
      }
    }
  }
}
```

The first live tool call spawns an ngrok tunnel; the URL is logged and
used for the lifetime of the process. Restart = new URL.

#### Legal & consent

Recording laws vary by jurisdiction — many US states are one-party consent,
others (CA, FL, IL, MA, MD, MT, NH, PA, WA) require all-party consent. The
`play_2600_into_call` / `play_mf_into_call` / `play_red_box_into_call`
tools reproduce historical tones that had operational meaning on the
pre-CCIS PSTN; modern carriers (Twilio included) will not honor them for
signaling, and using them to attempt toll fraud is illegal. This project
treats live telephony as a **CTF / research capability**: use it against
lines you own, test numbers you're authorized to hit (Twilio provides some),
or your own conference bridges.

## Install the MCP server

### Option A — run from source (recommended while iterating)

```sh
git clone <this repo> phr34cker5
cd phr34cker5
uv venv && source .venv/bin/activate
uv pip install -e .
phr34cker5-mcp --help
```

### Option B — one-shot via uvx (no clone required, once published)

```sh
uvx phr34cker5-mcp
```

## Wire it up

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
or the equivalent on your OS, and add under `mcpServers`:

```json
{
  "mcpServers": {
    "phr34cker5": {
      "command": "uvx",
      "args": ["phr34cker5-mcp"]
    }
  }
}
```

If you're running from source, point at the local install instead:

```json
{
  "mcpServers": {
    "phr34cker5": {
      "command": "/absolute/path/to/phr34cker5/.venv/bin/phr34cker5-mcp",
      "env": {
        "PHR34CKER5_KNOWLEDGE": "/absolute/path/to/phr34cker5/knowledge"
      }
    }
  }
}
```

Restart Claude Desktop. Ask: "What tools do you have from phr34cker5?"

### Claude Code

Add to `~/.claude/settings.json` (or the project's `.claude/settings.json`):

```json
{
  "mcpServers": {
    "phr34cker5": {
      "command": "uvx",
      "args": ["phr34cker5-mcp"]
    }
  }
}
```

### opencode

opencode reads MCP servers from `~/.config/opencode/config.json` (or the
equivalent under `$XDG_CONFIG_HOME`). Add:

```json
{
  "mcp": {
    "servers": {
      "phr34cker5": {
        "command": "uvx",
        "args": ["phr34cker5-mcp"]
      }
    }
  }
}
```

## Install the Skill

See [`skills/README.md`](skills/README.md). Short version:

```sh
# Claude Code
ln -s "$PWD/skills/phreaking" ~/.claude/skills/phreaking

# opencode
mkdir -p ~/.config/opencode/skills
ln -s "$PWD/skills/phreaking" ~/.config/opencode/skills/phreaking
```

## Add to the corpus

Drop a markdown file under `knowledge/<topic>/<slug>.md`. Follow the
conventions in [`knowledge/MANIFEST.md`](knowledge/MANIFEST.md). Restart the
server; the file becomes readable, searchable, and available as a resource
under `phr34cker5://<topic>/<slug>`.

For precise, dated facts (frequencies, timings, disputes), add a typed
record under `knowledge/records/` instead — the `lookup_tone` /
`verify_claim` / `explain_technique` tools bind to those. See
[`knowledge/records/README.md`](knowledge/records/README.md) for the schema
(every record needs `era_bounds` and a `citations[]` that resolves into the
bibliography, or the server won't load it).

## Ethos

This is a **CTF and history resource**. At a phreaking village the target is
built to replay the golden-era network, so old-school techniques — blue box,
red box, the 2600 Hz whistle — are exactly what you reach for, and the tools
never refuse one for being "obsolete." The corpus records *when and where*
each trick worked (and why it left the production PSTN) as context, not as a
gate. The one hard line: use it against CTF/Village gear and lines you own or
are authorized to test — not to defraud live production infrastructure.

## License

MIT.
