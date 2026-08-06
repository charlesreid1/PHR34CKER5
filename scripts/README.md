# PHR34CKER5 SCRIPTS

These are **shell / Python helpers you run once, as a human** — not
runtime code.

- `setup-twilio.sh` — prompts for your Twilio SID / Auth Token / From
  Number, writes them to `~/.config/phr34cker5/env` (chmod 600), and
  verifies them against the Twilio API. Run it once when you set up a
  machine; never again.

- `generate-tone-fixtures.py` — renders one WAV per `tone_signal`
  record from `knowledge/records/tones.json` into
  `tests/fixtures/tones/`. The WAV files themselves are gitignored
  (they're ~200 KB total and trivially reproducible from the
  records), but their SHA-256 checksums are committed at
  `tests/fixtures/tones.sha256` so we can verify determinism across
  regenerations.

  ```
  python scripts/generate-tone-fixtures.py            # render + refresh checksums
  python scripts/generate-tone-fixtures.py --verify   # render + fail on drift
  ```

  Run this once after cloning if you want to hear the tones or run
  detector tests against them. Re-run after editing a `tone_signal`
  record's `technical_body` to pick up the change (and to update
  the committed checksum file).

The MCP server itself — the code that actually runs while an assistant is
driving calls — lives in [`src/`](../src/), not here.

`scripts/` and `src/` are deliberately separate because they have
different audiences: `scripts/` is **human-once** (you, at a terminal,
during setup), while `src/` is **runtime-always** (the server, on every
tool call). Keeping them apart means the setup helpers never get imported
by the server and the server never gets confused for something you run
by hand.
