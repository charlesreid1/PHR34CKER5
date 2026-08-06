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

> A time machine to DEFCON 5, 1997.

**PHR34CKER5** is a Model Context Protocol (MCP) server plus a companion
**Skill** that turns any MCP-capable assistant (Claude Desktop, Claude Code,
opencode, …) into a knowledgeable phreaking historian and CTF cohort.

This repo is a **font of phreaking knowledge** — not a "generate DTMF tones"
utility. It curates lore: blueboxing, redboxing, CN/A social engineering,
2600 Hz, BBS culture, ESS switch generations, war dialing, tandem stacking,
the zines (2600, Phrack, TAP), the jargon. The MCP server exposes the corpus
as resources and search tools. The Skill teaches the assistant to consult
the corpus before answering.

## What's in the box

```
phr34cker5/
├── pyproject.toml           # uv/pipx/uvx-installable Python package
├── src/phr34cker5_mcp/      # the MCP server
├── knowledge/               # the corpus — markdown, one idea per file
│   ├── MANIFEST.md
│   ├── blueboxing/  redboxing/  greenboxing/  cna/  2600hz/
│   ├── bbs/  war-dialing/  ess/  tandem-stacking/  zines/  glossary/
├── skills/
│   └── phreaking/SKILL.md   # Claude Code / opencode skill
└── README.md                # you are here
```

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

| tool | what it does |
|---|---|
| `dial(to, from_=None, record=False)` | place outbound PSTN call, returns `CallSid` |
| `hangup(call_sid)` | end call via REST |
| `list_calls()` | every call this MCP instance has seen |
| `call_status(call_sid)` | fresh Twilio status + local WS state |
| `wait_for_answer(call_sid, timeout_s=60)` | block until answered + WS connected |
| `wait(seconds)` | sleep in a scripted sequence |
| `play_wav_into_call(call_sid, path)` | inject any mono 8kHz WAV |
| `play_tone_into_call(call_sid, freq_hz, ms)` | inject a single sine |
| `play_dtmf_into_call(call_sid, digits, ...)` | live DTMF |
| `play_mf_into_call(call_sid, digits, ...)` | live blue-box MF |
| `play_2600_into_call(call_sid, ms=1000)` | live 2600 Hz |
| `play_red_box_into_call(call_sid, coins)` | live ACTS coin tones |
| `listen(call_sid, seconds, save_wav=True)` | pull inbound audio to WAV |
| `start_recording(call_sid)` / `stop_recording` / `get_recording_url` | Twilio-native recording |

Canonical "dial X, wait 10s, deposit 75c" sequence:

```
call = dial("+14155551212")
wait_for_answer(call["call_sid"])
wait(10)
play_red_box_into_call(call["call_sid"], "qqq")
listen(call["call_sid"], seconds=5)
hangup(call["call_sid"])
```

#### Env vars

| var | required | notes |
|---|---|---|
| `TWILIO_ACCOUNT_SID` | yes | from console.twilio.com |
| `TWILIO_AUTH_TOKEN` | yes | keep it secret |
| `TWILIO_FROM_NUMBER` | yes | a Twilio-owned or verified E.164 number |
| `NGROK_AUTHTOKEN` | recommended | free at ngrok.com; without it tunnels are unreliable |
| `PHR34CKER5_PUBLIC_URL` | alternative | skip ngrok, point at your own public HTTPS URL (e.g. Cloudflare Tunnel) |

Add them to your MCP config:

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

## Ethos

This corpus is a **history and CTF resource**, not an operations manual. It
documents how phone signaling *used to work* and why the tricks of the era
don't work on modern networks. Frame everything historically; do not
instruct operating against live production infrastructure.

## License

MIT.
