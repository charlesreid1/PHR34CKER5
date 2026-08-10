#!/usr/bin/env python3
"""Drive the HackStock BBS over SSH.

Usage:
  scripts/bbs.py session KEYS.txt   — execute a series of keystrokes/commands
                                       from KEYS.txt (see format below) and
                                       dump the full raw session to
                                       .recordings/bbs_<ts>.raw and a stripped
                                       ansi-clean text version to .txt

KEYS.txt format — one action per line:
  send <text>      — send literal text (no newline)
  line <text>      — send text + \\r
  hit <n>          — press enter n times to burp through "Hit a key" prompts
  wait <secs>      — sleep secs seconds
  yesno N          — answer a yes/no prompt (N = "N\\r")
  # comment        — ignored
  END              — terminate the session
"""
from __future__ import annotations
import os, pexpect, sys, time, re, pathlib, datetime

ROOT = pathlib.Path(__file__).parent.parent
RECS = ROOT / ".recordings"
RECS.mkdir(exist_ok=True)

def strip_ansi(s: str) -> str:
    return re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]", "", s)

def main() -> None:
    if len(sys.argv) < 3 or sys.argv[1] != "session":
        print(__doc__); sys.exit(1)
    keys_file = pathlib.Path(sys.argv[2])
    if not keys_file.exists(): sys.exit(f"no keys file: {keys_file}")

    user = os.environ["PHREAKME_USER"]
    pw   = os.environ["PHREAKME_PASS"]
    ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    raw  = RECS / f"bbs_{ts}.raw"
    txt  = RECS / f"bbs_{ts}.txt"

    # Write to file only. (Streaming to stdout at the same time via a Tee
    # class silently loses data with pexpect — the pty logfile_read expects
    # a real file-like with .write/.flush that returns the number written.)
    f = raw.open("w")

    c = pexpect.spawn(
        f"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "
        f"-o PubkeyAuthentication=no {user}@phreakme.com",
        encoding="utf-8", timeout=30, dimensions=(24, 80),
    )
    c.logfile_read = f

    try:
        c.expect(["password:", "Password:"])
        c.sendline(pw)

        for lineno, line in enumerate(keys_file.read_text().splitlines(), 1):
            line = line.strip()
            if not line or line.startswith("#"): continue
            if line == "END": break
            cmd, _, rest = line.partition(" ")
            print(f"\n[[[ line {lineno}: {cmd!r} {rest!r} ]]]\n", file=sys.stderr)
            if cmd == "send":
                c.send(rest)
            elif cmd == "line":
                c.send(rest + "\r")
            elif cmd == "hit":
                for _ in range(int(rest or 1)):
                    time.sleep(0.4); c.send("\r")
            elif cmd == "wait":
                time.sleep(float(rest))
            elif cmd == "yesno":
                c.send(rest + "\r")
            else:
                sys.exit(f"unknown cmd {cmd!r} on line {lineno}")

        # Drain remaining output
        for _ in range(20):
            try: c.expect(pexpect.TIMEOUT, timeout=1)
            except Exception: break
    finally:
        c.close(force=True)
        f.close()

    txt.write_text(strip_ansi(raw.read_text()))
    print(f"\n\n[wrote {raw} and {txt}]", file=sys.stderr)


if __name__ == "__main__":
    main()
