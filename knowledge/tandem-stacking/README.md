# TANDEM STACKING

A **tandem** is a switch whose job is to connect other switches — a
switch-for-switches. **Stacking** them meant chaining tandem hops together
via in-band signaling, so a call ended up routed through a path the billing
side never fully understood.

## The premise
Once you were talking directly to a tandem via 2600 Hz + MF, you could
send `KP <trunk-route-code> ST` and jump to another tandem, then repeat.
Every hop was another set of billing records that might not reconcile.

## Uses in the era
- International routing without international billing.
- Reaching internal telco test numbers (loops, milliwatt tones, ANI
  readbacks) from outside the network.
- Sheer exploration — mapping the topology of Ma Bell one trunk at a time.

## Why it's over
Same reason as all the other in-band tricks: CCIS/SS7 moved signaling out
of the voice path, and the tandems started refusing to take orders from
audio.

## See also
- [[blueboxing/README]]
- [[ess/README]] — 4ESS was the big US toll tandem
- [[glossary/README]] — LATA, IXC, POI
