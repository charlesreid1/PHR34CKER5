# Lift & shift to another machine

This branch (`field-test`) is the live CTF working state — code, docs, evidence
audio, everything except secrets. Move it to another machine like this.

## What ships in the repo

| Path | Purpose |
|---|---|
| `scripts/phreak.py` | Twilio call driver + CTFd flag submission + Gemini transcription |
| `scripts/bbs.py` | pexpect wrapper for the HackStock BBS over SSH |
| `scripts/bbs_*.keys` | Keystroke scripts for `bbs.py` |
| `scripts/setup-twilio.sh` | Interactive Twilio credential setup |
| `src/phr34cker5_mcp/` | The MCP server itself (tones, records, Twilio bridge) |
| `.mcp.json` | Claude Code MCP wiring |
| `.env.example` | Template for `.env` — copy + fill in |
| `FINDINGS.md` | The running CTF log — infra, solved flags, blockers |
| `loot/*.md` | One file per flag solved / blocked, with repro |
| `.recordings/*.mp3` | Twilio recordings (evidence for solved flags) |
| `.recordings/*.raw` + `.txt` | Full BBS session transcripts |
| `.recordings/*.json` | Per-call metadata (Call SID, target, TwiML) |
| `flag-ollama-bell.md` | The Trivia 1101 blocker writeup for organizer follow-up |

## What does NOT ship (regenerate per machine)

| Path | How to recreate |
|---|---|
| `.env` | `cp .env.example .env && $EDITOR .env` — fill in Twilio + PhreakMe creds |
| `~/.twilio_api_key` | `source scripts/setup-twilio.sh` OR paste the two lines yourself |
| `~/.openrouter_api_key` | Same shape: `export OPENROUTER_API_KEY=sk-or-...` |
| `.venv/` | See setup steps below |
| `.tones/` | `.venv/bin/python -c "from phr34cker5_mcp.tones import red_box_bytes; ..."` — or just re-run the redbox call which regenerates it |

## First-time setup on the new machine

### 1. Clone

```sh
git clone <the-repo-url> phr34cker5
cd phr34cker5
git checkout field-test          # or whatever branch is live
```

### 2. Secrets

```sh
# ---- Twilio ----
mkdir -p ~/.config
cat > ~/.twilio_api_key <<'EOF'
export TWILIO_SID=SK...
export TWILIO_CLIENT_SECRET=...
EOF
chmod 600 ~/.twilio_api_key

# ---- OpenRouter ----
cat > ~/.openrouter_api_key <<'EOF'
export OPENROUTER_API_KEY=sk-or-...
EOF
chmod 600 ~/.openrouter_api_key

# ---- Project env ----
cp .env.example .env
$EDITOR .env                     # fill TWILIO_ACCOUNT_SID (AC...) and
                                 # TWILIO_FROM_NUMBER (E.164), plus PhreakMe creds
```

Values you need to fill in on the new machine, from the running conversation:

- `TWILIO_ACCOUNT_SID=AC_REDACTED`
- `TWILIO_FROM_NUMBER=+19289778173`
- `PHREAKME_USER=ch4zm`
- `PHREAKME_PASS=Time4phreaking!` (single-quote in the env: `'Time4phreaking!'`)
- `PHREAKME_TARGET=+12195002600`
- The Twilio `SK…` / secret and OpenRouter key go in the two `~/.` files above.

### 3. Python + venv

Requires Python 3.10–3.12 (uses stdlib `audioop` which was removed in 3.13):

```sh
# macOS with pyenv:
pyenv install 3.11.14
~/.pyenv/versions/3.11.14/bin/python -m venv .venv

# or plain python3.11 / python3.12 on the PATH:
python3.11 -m venv .venv

.venv/bin/pip install -U pip
.venv/bin/pip install -e '.[ngrok]'
.venv/bin/pip install pexpect requests
```

### 4. Verify

```sh
# Twilio auth
source ~/.twilio_api_key && source ./.env
.venv/bin/python -c "
from twilio.rest import Client
import os
c = Client(os.environ['TWILIO_SID'], os.environ['TWILIO_CLIENT_SECRET'], os.environ['TWILIO_ACCOUNT_SID'])
n = list(c.incoming_phone_numbers.list(limit=5))
print('numbers:', [x.phone_number for x in n])
"

# PhreakMe login + flag submission (no-op — try a known-bad flag)
.venv/bin/python scripts/phreak.py list | head -20
```

If both work, you're live.

## Reminders / gotchas from this session

- **Twilio KYC hold**: as of 2026-08-08 the account is on a compliance hold and outbound calls return `401 code 20003` — resolve in Twilio Trust Hub before dialing.
- **SBBS concurrent-login lock**: HackStock (over SSH port 22) refuses new logins for several minutes if a prior session died without pressing `G` (goodbye). Always end BBS `.keys` scripts with a clean `G` + `Y`.
- **Ollama Bell / Trivia 1101 blocker**: see `flag-ollama-bell.md` — spoken flag is rejected by CTFd. Ask organizers about the "player PIN" auto-claim mechanism.
- **Gemini transcription flakes on short audio** (< ~3s): can hallucinate/echo the prompt back. If you get garbage on a short clip, re-record with more context.

## Pushing changes back

```sh
git add -A
git commit -m "field: <what you did>"
git push
```

Never `git add .env` — it's in `.gitignore`, but check with `git status` before committing to be sure. The `~/.twilio_api_key` and `~/.openrouter_api_key` live outside the repo and can't accidentally be staged.
