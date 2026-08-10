# BBS — recognition

How to tell you've hit a BBS on a scanned modem line, and what rate it
answered at, from the handshake audio and first-screen bytes.

## The 15-second triage

**If in the first 15 seconds you hear:**

1. **A short 2100 Hz answer tone (~3 seconds), then a "whistle" that
   climbs or warbles → this is a modem handshake.** You've hit either
   a BBS, a mainframe/UNIX dial-in, a fax, or a router console. The
   *rate* is knowable from what happens next; the *system* is knowable
   from the banner after CONNECT (see [[war-dialing/toneloc-tuning]]).

2. **Continuous 1100 Hz tone bursts (0.5 s on / 3 s off) → fax CNG.**
   Not a BBS. See [[fax/README]].

3. **Voice, or a voicemail greeting → not a BBS.**

4. **Silence, then a very brief single tone → a data line waiting for
   the caller to send an origination handshake first (V.25 originate
   mode).** Rare — usually means a modem configured for `AT&D2` or
   similar.

## Handshake audio by baud rate

Each speed had a distinctive audio signature. What a listener on the
line heard, in the first ~5 seconds after answer:

### 300 baud (Bell 103 / V.21)

- **Answer tone:** none in the modern sense. Bell 103 originate sends
  1270 Hz mark / 1070 Hz space; answer sends 2225 Hz mark / 2025 Hz
  space. Both sides transmit simultaneously.
- **Sound:** a low warbly whistle from each direction, overlapping.
  You can tell "someone is definitely there" but the two carriers
  don't obviously converge on any single tone.
- **After CONNECT:** slow, painful character-by-character text. A
  typing speed you can *watch*. 30 characters/sec is the ceiling.

### 1200 baud (Bell 212A / V.22)

- **Answer tone:** ~600 ms of 2100 Hz (V.25 answer tone).
- **Sound:** clear 2100 Hz whistle, then a rapid buzzing that
  settles into a static-ish carrier. Bell 212A used PSK at 1200 Hz
  with 600 baud symbols carrying 2 bits each.
- **Post-CONNECT:** text arrives in visible chunks a few characters
  wide. Feels fast compared to 300; slow compared to anything after.

### 2400 baud (V.22bis)

- **Answer tone:** same 2100 Hz for ~3 seconds.
- **Sound:** after the 2100 Hz answer, a longer negotiation phase
  with alternating pilot tones. The character of the carrier after
  training is a busier hiss than 1200.
- **Post-CONNECT:** feels smooth for a person typing on the other
  end; still visibly incremental for a large text dump.

### 9600 baud (V.32) and 14.4 k (V.32bis)

- **Answer tone:** 2100 Hz for ~3 seconds, then a distinctive
  amplitude-modulated training sequence. On some phones the 2100 Hz
  is followed by a brief phase-reversal chirp intended to disable
  echo cancellers on the network.
- **Sound:** longer, more complex handshake. QAM modulation gives a
  busier, more textured carrier than V.22bis.
- **Post-CONNECT:** essentially instant for text; visibly progressive
  for large file transfers.

### 28.8 k (V.34) and higher

- **Answer tone:** 2100 Hz with phase-reversal (breaks echo cancellers).
- **Sound:** very long handshake — 15-30 seconds of complex training
  including line-probing tones sweeping across the voice band. V.34
  literally measured the line's frequency response and picked a
  constellation to match.
- **Post-CONNECT:** as-fast-as-serial-can-render. Landline modem
  ceiling.

## What a BBS logon looked like after CONNECT

The bytes that came right after CONNECT told you the platform and
often the specific BBS software.

- **Garbage / ANSI escape codes → BBS.** A stream starting with `ESC[`
  sequences (or their visible form `←[`) is ANSI art. Very few
  non-BBS systems replied with ANSI as their first bytes.
- **`CONNECT 2400` from your own modem, then a red/blue ASCII banner
  reading "Welcome to <BBS Name>" → classic amateur BBS.**
- **`Ymodem Ready` / `sz -b` → the far end is a Unix system running
  uucico or a similar batch transfer.** Not a BBS in the interactive
  sense.
- **`login:` (lowercase) → Unix.** Might be a BBS if it's a public-
  access Unix (a "PubNix" — see grex, m-net, cyberspace.org).
- **`Username:` `Password:` (capitals) → VAX/VMS.** Not a BBS.
- **`Welcome to the ROLM PhoneMail system` → voicemail, not a BBS.**

Full banner list in [[war-dialing/toneloc-tuning]] and typed records
in `records/fingerprints.json`.

## Known-BBS software fingerprints

The first-line banner after login usually named the BBS software:

- **`Renegade BBS`** — the DOS-based Renegade BBS software (1990s
  hobbyist favorite)
- **`WWIV`** — WWIV software (Wayne Bell), extensible, prone to trojan
  door-game infections
- **`PCBoard v15.x`** — Clark Development's commercial-ish PCBoard
- **`RemoteAccess`** — RA, often used in Fidonet nodes
- **`Citadel`** — an unusual room-based BBS metaphor
- **`Wildcat!`** — another commercial one, big in the shareware scene
- **`Synchronet`** — one of the few that survived into the internet era

## FidoNet giveaways

If a BBS ran a Fido node, you'd sometimes hit it during **mail hour**
(01:00-02:00 local nightly by treaty) — it wouldn't answer with the
normal BBS banner but with `Ymodem` or a Zmodem handshake.

## Sources

- Bell System Technical Journal, various modem-standard articles
- ITU-T V.21, V.22, V.22bis, V.32, V.32bis, V.34
- Phrack 8.5 (Mad Hacker of 616, The Art of Junction Box Modeming)
- Phrack 3.11 (community treatments of BBS software)

## See also

- [[bbs/README]] — the BBS culture layer
- [[modems/README]] — the modem-standard reference
- [[war-dialing/toneloc-tuning]] — banner fingerprints and false-positive
  patterns
