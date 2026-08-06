# PHR34CKER5 SCRIPTS

These are **shell helpers you run once, as a human** — not runtime code.

- `setup-twilio.sh` — prompts for your Twilio SID / Auth Token / From
  Number, writes them to `~/.config/phr34cker5/env` (chmod 600), and
  verifies them against the Twilio API. Run it once when you set up a
  machine; never again.

The MCP server itself — the code that actually runs while an assistant is
driving calls — lives in [`src/`](../src/), not here.

`scripts/` and `src/` are deliberately separate because they have
different audiences: `scripts/` is **human-once** (you, at a terminal,
during setup), while `src/` is **runtime-always** (the server, on every
tool call). Keeping them apart means the setup helpers never get imported
by the server and the server never gets confused for something you run
by hand.
