#!/usr/bin/env bash
# One-shot Twilio credential setup for PHR34CKER5.
#
# Prompts for SID / Auth Token / From Number (once), writes them to
# ~/.config/phr34cker5/env, and prints the export lines you can paste
# into a shell rc file if you want them global.
#
# Re-running overwrites. That's the point.

set -euo pipefail

CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/phr34cker5"
ENV_FILE="$CONFIG_DIR/env"

mkdir -p "$CONFIG_DIR"
chmod 700 "$CONFIG_DIR"

echo "==> PHR34CKER5 Twilio setup"
echo "    Writes: $ENV_FILE (chmod 600)"
echo

read -r -p "TWILIO_ACCOUNT_SID   (ACxxxx…): " SID
read -r -s -p "TWILIO_AUTH_TOKEN    (hidden):    " TOK; echo
read -r -p "TWILIO_FROM_NUMBER   (+15551234567): " FROM

read -r -p "PHR34CKER5_PUBLIC_URL (blank = laptop+ngrok): " PUBLIC_URL
NGROK_TOKEN=""
if [[ -z "$PUBLIC_URL" ]]; then
    read -r -s -p "NGROK_AUTHTOKEN      (hidden, blank OK): " NGROK_TOKEN; echo
fi

umask 077
{
    echo "# PHR34CKER5 Twilio credentials — generated $(date -u +%FT%TZ)"
    echo "export TWILIO_ACCOUNT_SID=\"$SID\""
    echo "export TWILIO_AUTH_TOKEN=\"$TOK\""
    echo "export TWILIO_FROM_NUMBER=\"$FROM\""
    [[ -n "$PUBLIC_URL"   ]] && echo "export PHR34CKER5_PUBLIC_URL=\"$PUBLIC_URL\""
    [[ -n "$NGROK_TOKEN"  ]] && echo "export NGROK_AUTHTOKEN=\"$NGROK_TOKEN\""
} > "$ENV_FILE"
chmod 600 "$ENV_FILE"

echo
echo "==> Wrote $ENV_FILE"
echo
echo "Two ways to use it:"
echo
echo "  A) Load it in your shell (recommended):"
echo "       echo '[ -f $ENV_FILE ] && . $ENV_FILE' >> ~/.zshrc"
echo "       . $ENV_FILE"
echo
echo "  B) Point your MCP client at it. In claude_desktop_config.json:"
echo "       \"phr34cker5\": {"
echo "         \"command\": \"bash\","
echo "         \"args\": [\"-lc\", \". $ENV_FILE && exec phr34cker5-mcp\"]"
echo "       }"
echo
echo "==> Verifying credentials against Twilio API…"
if command -v python3 >/dev/null 2>&1 && python3 -c 'import twilio' >/dev/null 2>&1; then
    python3 - <<PY
import os
os.environ["TWILIO_ACCOUNT_SID"] = "$SID"
os.environ["TWILIO_AUTH_TOKEN"]  = "$TOK"
from twilio.rest import Client
c = Client("$SID", "$TOK")
acct = c.api.accounts("$SID").fetch()
print(f"    OK — account: {acct.friendly_name} ({acct.status})")
nums = list(c.incoming_phone_numbers.list(phone_number="$FROM", limit=1))
if nums:
    n = nums[0]
    print(f"    OK — number:  {n.phone_number}  voice_url={n.voice_url or '(unset)'}")
else:
    print(f"    !! number $FROM not found on this account (typo? wrong subaccount?)")
PY
else
    echo "    (skipped — twilio SDK not importable in this python; run \`pip install twilio\` to verify)"
fi

echo
echo "Done. Never do this again."
