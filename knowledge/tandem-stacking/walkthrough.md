# Tandem stacking — walkthrough

An era-authentic overseas-loop trick. Historical illustration only — the
in-band trunks this depends on are gone from every mainstream telco.

The goal: place a call from a US phone that appears (from AMA
reconciliation) to originate from somewhere else — canonically, route
into a foreign gateway, back into the US via a stacked tandem, and out
to a domestic destination. Two seizures, two winks, one final ringback.

## Preconditions

- An in-band SF/MF trunk from your local CO to a **US toll switch**
  (4ESS or DMS-200 era-typical). Pre-1990 in Bell territory; into
  mid-90s on some independents.
- The toll switch has a route to an **international gateway** (4ESS
  with international, or a Sprint DMS-250 gateway).
- The gateway spoke **CCITT No.5** to a foreign toll switch (Caribbean,
  West African, or LATAM gateways were era-classic). Post-No.6/No.7,
  the gateway is out-of-band and this doesn't work.
- The foreign toll switch has an outbound US trunk of its own (which,
  in the era, most did — international routes were bidirectional MF).

## The sequence

### t=0.0 s — dial a legitimate long-distance number

Dial `1 + NPA + NXX + XXXX` to a number you have some claim to reach.
The originating CO seizes an outbound trunk to the toll switch. You
hear routing clicks and finally ringback of the destination.

### t=~answer — first seizure

The instant answer supervision returns (audio path is now cut through
and the far party is on the line), you play **2600 Hz for ~700 ms**
into the mouthpiece. The originating tandem interprets this as far-end
on-hook and drops the trunk to wink/idle — but your local loop stays
up. You hear a brief silence, then a **wink** (~150-200 ms click).

### t=~1.0 s — first MF address (to the gateway)

You send `KP + 01 + CC + national_number + ST` in MF. The initial `01`
is nature-of-address = international. The toll switch selects an
international trunk group and forwards.

For an overseas-loop, choose a CC + national_number whose national
network you know accepts a callback into the US. Historic choices:
Caribbean numbers (Anguilla, Antigua, several small island operators),
some West African gateways. **The specific numbers that worked
rotated; the corpus does not publish current ones.**

### t=~1.6 s — second seizure

The foreign switch answers your call (or its ACTS-equivalent voice
prompt asks for something you ignore). As soon as audio path is up,
you play **2400 Hz + 2600 Hz** or the No.5-specific clear-forward pulse
(NOT 2600 alone — that's the trap). On some No.5 gateways this is
2400 Hz seizure alone; on others it's a compound pattern. The foreign
switch's inter-register receiver was less discriminating than a
domestic ACTS receiver, so seizures often worked with modest timing
slop.

### t=~2.5 s — second MF address (back into the US)

You now send `KP + 011 + 1 + NPA + NXX + XXXX + ST` — international
back to a US number. Because you're addressing the foreign switch's
outbound US trunk, the AMA record on the foreign switch will show
"origin: this switch" — the actual chain back to your originating US
CO is not captured on any single billing record.

### t=~3.5 s — routing back to US destination

The foreign switch's outbound US trunk lands on a US gateway (a
different 4ESS or DMS-250 than the one you used going out). The US
gateway routes normally to the destination NPA. You hear ringback.

### t=answer of final destination

The call rings through and the final party answers. From their end it
looks like an international call from wherever the foreign gateway
resolves to. From the AMA side of your US originating CO, only the
first call (to the legitimate long-distance number you started with)
is billed.

## What each hop sounded like

- **Hop 0 (originating CO to US toll):** familiar US ringback cadence
  (2 s on / 4 s off, 440+480 Hz). Answer supervision closes with a
  click and audio cuts through.
- **Hop 1 (US toll → international):** after your 2600 Hz seizure, a
  wink click. MF tones. Then a distinctive **higher-pitched hiss**
  (the international trunk had a different noise floor than domestic).
  Foreign switch answer: often a voice prompt in the local language,
  which you ignore.
- **Hop 2 (foreign → US destination):** after your No.5 seizure, another
  wink but of a slightly different cadence — No.5 winks were on the
  order of 300 ms, longer than R1's ~150-200 ms. MF tones. Then US
  ringback cadence of the final destination.

## Failure modes

- **Foreign switch was CCIS/No.7:** in-band seizure does nothing.
  Modern era — this is why the trick died.
- **US gateway didn't accept your MF nature-of-address prefix:** some
  gateways required specific route codes for international, not a
  bare `01`. Trial-and-error against a given switch.
- **AMA reconciliation eventually caught it:** greenstar/blueflag
  logging on 4ESS could pattern-match unusual 2600-hold-time and MF
  bursts even without decoding the address. Repeated use flagged the
  originating loop.

## Sources

- Phrack 3.4 (Data Line, Signalling Systems Around the World)
- Phrack 11.8 (Doom Prophet, Telephone Signalling Methods)
- Phrack 25.7 (The Noid, The Blue Box And Ma Bell)
- Phrack 33.5 (Infinite Loop, LATA Reference List)
- Phrack 33.6 (The Trunk Terminator, International Toll Free Code List)
- BSTJ Nov 1960 (R1 MF); CCITT Q.140/Q.310-Q.332 (No.5/No.6)

## See also

- [[tandem-stacking/reference]] — route codes + audio texture
- [[tandem-stacking/international]] — the C5 gateway story
- [[blueboxing/seizure-walkthrough]] — the single-hop version
- [[signaling/README]] — why this doesn't work on SS7
