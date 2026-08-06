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
