# GREENBOXING

A **green box** generates the *operator-side* coin control tones — the ones
the CO sends to a payphone to instruct it to **collect** or **return** coins.

## Tones (1700 + 2200 Hz family, longer durations)
- **Coin Collect** — 900 ms tone. Tells the phone to drop the escrowed coins
  into the vault.
- **Coin Return** — 900 ms tone at different frequency pairing. Releases the
  coins back to the caller.
- **Ringback** — used by ops to ring a payphone from the CO side.

## Why "green"?
Colors in the phreaking taxonomy were arbitrary but sticky. Blue for trunk
signaling, red for coin deposit, green for coin control. The naming outlived
most of the boxes themselves.

## See also
- [[redboxing/README]]
- [[glossary/README]] — for the full color-box zoo (black, beige, cheese…)
