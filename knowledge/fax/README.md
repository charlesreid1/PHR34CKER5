# FAX — T.30 / GROUP 3

> The last analog protocol most offices still run. Held together by
> convention, dead ITU committees, and the terrifying inertia of law and
> healthcare.

## The handshake, in caricature

```
  CALLING FAX                              CALLED FAX
  -----------                              ----------
  dial number                              (ring)
                                           pickup, wait 0.75-2.0s
  CNG: 1100 Hz, 0.5s on / 3s off  ---->
                                    <----  CED: 2100 Hz, 2.6-4.0s
                                    <----  V.21 preamble (300 baud FSK)
                                    <----  DIS  (Digital Identification Signal
                                                 — "I can do 14.4k, ECM, A4…")
  V.21 DCS  (Digital Command Signal ----> 
             — "OK, let's go 9.6k, no ECM")
  V.21 TCF  (Training Check)        ---->
                                    <----  CFR (Confirmation)
  V.27ter / V.29 / V.17 image data  ---->  (T.4 or T.6 encoded)
                                    <----  MCF (Message Confirmation)
  DCN (Disconnect)                  ---->
```

Only the two audible tones — **CNG** and **CED** — are what you actually
*hear* when a fax picks up. Everything after is data on the audio band.

## The tones this repo generates

- `generate_fax_cng(cycles=4)` → CNG. 1100 Hz, 0.5s on / 3s off. The
  calling fax repeats this until the called end answers. Four cycles is
  ~14 seconds of "hello, I am a fax."
- `generate_fax_ced(ms=3000)` → CED. 2100 Hz continuous. The answering
  fax's "yes, I am also a fax, please proceed" reply.

Play one into a call with `play_fax_cng_into_call(call_sid)` /
`play_fax_ced_into_call(call_sid)`. Anything past the handshake is a
real fax stack (SpanDSP, or a hosted API — Phaxio, Documo).

## Group 1 through Group 4

| Group | Era      | Notes                                          |
|-------|----------|------------------------------------------------|
| 1     | 1968     | Analog, ~6 min/page. Xerox Magnafax Telecopier |
| 2     | 1976     | Analog, ~3 min/page                            |
| 3     | 1980     | **The one you know.** Digital over PSTN audio, T.30/T.4, ~30s/page |
| 3bis  | mid-90s  | V.34 half-duplex, up to 33.6k                  |
| 4     | 1984     | Digital over ISDN. Never really took over.     |

Group 3 is what "fax" means in 2026 for the tiny remaining fax population.
Every modern fax machine and virtual fax service speaks T.30 over G.711.

## The war-dialing angle

In the era of `[[war-dialing/README]]`, hitting a fax while scanning was a
result: the CED (2100 Hz) squawk was unmistakable. ToneLoc and THC-Scan
both flagged fax lines separately from carriers. A fax line meant a
machine in someone's office — which meant an accessible endpoint. Junk
faxes ("fax spam") became a plague in the '90s specifically because war
dialers made it cheap to enumerate fax numbers.

## The 2600 Hz footnote

CED at 2100 Hz was chosen partly *because* 2600 Hz was the SF supervision
tone: putting the fax answer at 2100 Hz kept it far enough from the
supervision band that the network wouldn't confuse a fax handshake for
trunk signaling. See `[[2600hz/README]]`.

## Sources
- ITU-T T.30 (2005), "Procedures for document facsimile transmission in
  the general switched telephone network"
- ITU-T T.4, T.6 (image coding)
- SpanDSP source (Steve Underwood) — reference open-source T.30 stack
- Comer, "Ubiquitous Fax: A Study of the Fax Protocols", 1998
