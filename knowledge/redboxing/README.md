# REDBOXING

A **red box** emulates the ACTS (Automated Coin Toll Service) coin-deposit
tones a payphone sends to the CO when a caller drops change into the slot.

## The tones
Each is a dual-tone burst of **1700 + 2200 Hz**:

| Coin    | Burst pattern                          |
|---------|----------------------------------------|
| Nickel  | one 66 ms burst                         |
| Dime    | two 66 ms bursts, 66 ms apart           |
| Quarter | five 33 ms bursts, 33 ms apart          |

## How it worked (historical)
1. Dial a long-distance number from a fortress phone.
2. ACTS voice prompt: "Please deposit one dollar and twenty-five cents."
3. Instead of coins, play the tone pattern into the mouthpiece.
4. ACTS credits the deposit and cuts the call through.

## Countermeasures that killed it
- COCOTs (Customer-Owned Coin-Operated Telephones) that did their own local
  coin validation.
- Removal of in-band coin signaling.
- Payphones themselves largely disappearing.

## Which payphones — the platform records
The red box worked against one specific platform (ACTS-supervised Bell
1C/1D fortress phones); it never worked against COCOTs and it stopped
working against Nortel Millennium as those rolled out. Typed records
for every platform live in
[`records/payphone_systems.json`](../records/payphone_systems.json):

- `pay_acts` — the coin-toll signaling protocol itself
- `pay_bell_1c_1d` — the fortress phone (the target)
- `pay_millennium` — the smart phone with local validation (immune)
- `pay_cocot` — customer-owned, local validation (immune, but has its
  own admin-mode attack via default 4-digit password)
- `pay_tsps_operator` — the operator platform (green-box surface)
- `pay_three_slot` — the pre-1975 predecessor payphone

## See also
- [[greenboxing/README]] — the operator side of coin signaling
- [[signaling/README]] — SF/MF/ACTS in the systems taxonomy
- [[zines/README]] — 2600 Magazine, Winter 1993, ran the definitive writeup

## Sources
- 2600 Magazine, Vol. 10, No. 4 (Winter 1993–94)
