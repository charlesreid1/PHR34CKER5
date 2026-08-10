# OPERATOR & TEST SERVICES

> The internal surface of the phone network: the operator you could talk to,
> the numbers that talked back, and the test lines that were never meant for
> you. Half of these have no universal number — the discovery *method* is the
> knowledge, not a magic string.

## The short-dial codes

| Dial | What it reached |
|------|-----------------|
| `0`   | Local operator (TSPS/TOPS/OSPS) — collect, coin-toll, busy-verify, EI |
| `00`  | Long-distance / inward operator (your presubscribed IXC's operator) |
| `411` | Local directory assistance (also `1-411`, `NPA-555-1212`) |
| `611` | Repair service / trouble desk (per-LEC) |
| `950-XXXX` | Feature Group B carrier access — subscriber-dialable path to an alternate long-distance carrier, 1984–late 90s, obsoleted by 101XXXX dialaround |

None of these are guaranteed universal — `611`/`411` behavior is per-LEC and
`950` was carrier-by-carrier. Record the class, not "the number."

## Operator platforms: TSPS / TOPS / OSPS

- **TSPS** (Traffic Service Position System, Western Electric, 1969) — the
  operator console for coin, collect, and toll calls.
- **TOPS** (Nortel, DMS-based) and **OSPS** (5ESS-based) — the successors.

The phreak-relevant part is what the console could *do* to a subscriber line:

- **Busy-verify** — an operator could bridge onto a line to confirm it was
  genuinely in use (vs. off-hook/broken).
- **Emergency interrupt (EI)** — the operator could break into an active
  call. Talking an operator into performing an EI or a verify on a target
  line — pretexting your way to "please check if this line is busy" — was a
  classic **social-engineering** angle, not a tone trick. The tones died with
  the trunks; the operator sat behind a human who could be convinced.

## ANAC — there is NO universal number

The **Automatic Number Announcement Circuit** reads your own calling number
back to you. It is **per-CO / per-NPA** — the corpus must never assert a
single universal ANAC. Historically observed families:

| Region (1990s) | ANAC seen |
|----------------|-----------|
| Much of Pacific Bell | `958` |
| Many Bell Atlantic offices | `200-222-2222` |
| Some GTE / SWBT offices | `311`, `311-1111`, `200-XXXX` |
| Commercial (spelled 958-6480) | `1-800-MY-ANI-IS` |

Discovery method: try the local `958`, `200-XXX-XXXX`, `760-XXXX` family and
listen for a digit readback. If a record ever tells you "the ANAC is 958,"
it's wrong — it was *an* ANAC, in *some* offices.

## Milliwatt, ringback, loop-arounds

- **Milliwatt test line** — answers with a steady **1004 Hz** tone (older
  lines 1000 Hz) at **0 dBm0**, the one-milliwatt loss reference. Reachable
  at `NPA-XXX-1111` in many offices, `959-1111` in DMS regions, `NPA-XXX-0002`
  elsewhere. See `[[ctf/milliwatt-testlines]]`.
- **Ringback** — dial a code, hang up briefly, and your own phone rings; techs
  used it to test the bell. **Office-dependent**: `660 + last-4-of-your-number`
  in many step-by-step/1ESS offices, elsewhere `571-XXXX`, `260-XXXX`,
  `311-1111`. It vanished as SS7/5ESS features replaced maintenance shortcuts.
- **Loop-arounds (LP1/LP2)** — a matched pair of test numbers, often on a 95X
  prefix with a `99XX` suffix. Called individually, each just gives a
  milliwatt tone; when two people seize LP1 and LP2 at the same time, their
  audio is bridged. Pre-BBS, this was the **anonymous meetup**. Discovery: call
  the tone at the suspected LP1; if a stranger's voice shows up, you've found
  the loop.

## What a CTF "operator" is parodying

A CTF "operator" IVR is almost always a costume for one of the above: an
**ANAC** that reads back the ANI the village sees (prove you control your
caller-ID), a **CN/A operator** scoring your social-engineering pretext, or a
**test-line** joke where a "steady" tone hides a pattern. Probe it like the
real thing — listen, transcribe the readback, note which pretext fields it
demands — and expect the flag in the readback or in the listing it releases.

## See also
- [[cna/README]] — Customer Name & Address bureaus and operator pretexting
- [[ctf/simulated-anac-cna]] — the CTF prop versions of ANAC and CN/A
- [[ctf/milliwatt-testlines]] — probing 1004 Hz test lines and their kin
- [[glossary/README]] — ANI, ANAC, CN/A, TSPS, loop-around, EI

## Sources
- Bell System Technical Journal (Nov 1960) — signaling and operator systems
- Bellcore/Telcordia LSSGR (GR-506-CORE and related) — coin/operator services
- ITU-T O-series — the 1004/1020 Hz milliwatt level reference
- 2600 Magazine and TAP (various issues) — rotating ANAC, ringback, and
  loop-around listings; comp.dcom.telecom archives
