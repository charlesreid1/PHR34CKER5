# CN/A PRETEXT SCRIPTS — A HISTORICAL ILLUSTRATION

> **Framing:** this file reconstructs how CN/A social engineering
> *sounded* in the 1980s–90s, as history and as a CTF prop. It is NOT a
> playbook against any live bureau. The real bureaus described here are
> gone; their numbers are deliberately omitted. Use it to score a parody
> CN/A operator at a con — see `[[ctf/simulated-anac-cna]]`.

A **CN/A (Customer Name and Address)** bureau was the telco-internal
office that turned a phone number into a subscriber's name and billing
address. Each RBOC ran **its own regional bureaus** after divestiture,
each with its own hours and ANI-restricted access number, and each
expected callers to *sound like telco*. The security model was "you
dialed in on a line only insiders reach, and you talk like an insider."
Blue-boxing and tandem tricks (`[[blueboxing/README]]`) let outsiders
originate calls that looked internal — the rest was voice.

## What "sounding internal" meant

Three things gated a request, none of them real authentication:

- **The right access path** — the call came from telco-internal ANI.
- **A plausible company code / office reference** — a short identifier
  tying you to a business office or repair group in that region. (We do
  **not** print real codes; the *concept* is that it had to match the
  region's format.)
- **The right jargon and cadence** — "I need a CN/A on…," "for a repair
  ticket," delivered flat and bored, like someone on their fiftieth of
  the shift.

## An illustrative exchange (period-accurate, reconstructed)

```
OPERATOR:  CN/A, [region].
PHREAK:    Yeah, hi, this is Dave over in the business office, I need a
           CN/A on 212-555-0100.                       [flat, unhurried]
OPERATOR:  What's your company code?
PHREAK:    [regional-format code, said quickly, no pause]
OPERATOR:  ...one moment.  [keys it]  That's listing to a J. MERCER,
           410 East 9th Street.
PHREAK:    Great, thanks.                               [hang up, don't linger]
```

Annotated:

- **"business office," not "the phone company."** Insiders name the
  *group* they work in. Vagueness is the first tell of an outsider.
- **The company-code demand is the gate.** A confident, correctly
  *formatted* answer usually passed; the operator was checking that you
  sounded like you belonged, not verifying you against a roster.
- **Never linger, never over-explain.** A real clerk reads it back and
  moves on.

## What would BLOW the pretext

| Failure | Why it tanks |
|---|---|
| Wrong / mis-formatted **company code** | the one thing they actually asked for; a bad format flags you instantly |
| Wrong **jargon** ("can you look up who owns…") | civilians say "look up who owns"; insiders say "I need a CN/A on" |
| Asking the operator to **explain the process** | insiders already know it |
| Requesting a **callback** or giving a callback number | inverts the trust model — now *they* verify *you* |
| Hesitation, "um," reading from a script audibly | cadence is half the credential |
| Calling **outside bureau hours** or from an obviously external path | breaks the access-path assumption |

The parallel game ran against the **CBCS (Calling-Card Bureau)** with
the same social dynamics — different jargon, same "sound like staff"
gate.

## How the modern descendants differ

CN/A-as-a-phone-service is dead. Its function moved into **databases you
dip, not operators you sweet-talk**:

- **LIDB (Line Information Database)** — per-LEC store queried by
  switches for billing/validation; returns line class, calling-card
  validation, billing name for operator services.
- **CNAM** — the Caller-ID *name*. Crucially it is **not sent by the
  originating switch**; the *terminating* switch performs a dip against
  the number's LIDB/CNAM record. Whoever controls that record controls
  the displayed name — which is why CNAM has always been spoofable at
  the record level, a database-integrity problem rather than a
  voice-pretext one.

The pretext moved with it: instead of talking a bureau operator into a
listing, the modern analog is obtaining *access to the dip* (contracted,
paid, logged). The corpus does not cover live access; see the
non-goals in `plan-knowledge.md`.

## See also
- [[cna/README]] — what CN/A bureaus were and why they worked
- [[ctf/simulated-anac-cna]] — scoring a parody CN/A operator IVR
- [[glossary/README]] — CN/A, LIDB, CNAM, RBOC, ANI
- [[blueboxing/README]] — how outsiders faked "internal" origination

## Sources
- 2600 Magazine and TAP (various, 1984–1999) — CN/A concept and
  rotating bureau listings (historical)
- Kevin Mitnick, *The Art of Deception* (2002) — pretexting case studies
- Bellcore SR-TSV-000030 / GR-30-CORE — CLASS / Caller-ID (CNAM) delivery
- Telcordia GR-446 and LIDB service descriptions
- comp.dcom.telecom archives on CN/A and operator-services practice
