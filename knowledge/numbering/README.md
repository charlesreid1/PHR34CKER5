# NANP + numbering plan

The North American Numbering Plan and its dialing-plan companions —
what the digits *meant*, per era.

## Files here

- [ani-ii.md](ani-ii.md) — the 2-digit info-digit prefix delivered on
  Feature Group D trunks and SS7 OLI. 100-code table lives in the
  typed records ([`records/operator_service_codes.json`](../records/operator_service_codes.json)).

## Structure at a glance (1995-2003 era)

- **NANP number:** NPA-NXX-XXXX.
- **Interchangeable NPA codes** (second digit of NPA can be 2-9) went
  live **1995-01-15**. Pre-1995 area codes were `N0X` / `N1X` only;
  post-1995, codes like 334, 360, 520 appeared.
- **N11 codes:** 211 (community), 311 (non-emergency), 411 (directory
  assist), 511 (traveler info), 611 (repair), 711 (TRS), 811 ("call
  before you dig", 2005), 911 (emergency, nationalized 1968).
- **Feature Group B (950-XXXX):** subscriber-dialable carrier access,
  1984-late-90s; largely obsolete after FGD dialaround generalized.
- **Feature Group D dialaround:** the 3-digit CIC (10-XXX) form was
  replaced by the 4-digit `10-10-XXX` (`101-XXXX`) form on **1998-07-01**
  per FCC Order 97-402.
- **555:** reserved. 555-1212 = directory assistance NPA-wide.
  555-0100 through 555-0199 reserved for fictional use since 1994.
- **NPA 700 / 500 / 600 / 800 / 888 / 877 / 866 / 855 / 844 / 833 / 822**
  — carrier services, personal comm, Canadian non-geographic, and
  toll-free (800 was original; 888 launched 1996, 877 in 1998, 866 in
  2000, 855 in 2010, 844 in 2013, 833 in 2017, 822 reserved).
- **NPA 976:** not an NPA — a legacy per-NPA local premium prefix.

## Test and utility number *classes* — per-NPA, not universal

Every "the ANAC is 958" claim needs a region qualifier. Record entries
are per-CO or per-NPA. Common discovery patterns:

- **ANAC (calling-number readback):** `958`, `958-XXXX`, `200-222-2222`,
  `311-1111`, `1-800-MY-ANI-IS`.
- **Ringback:** `660 + YYYY` (last 4 of your own number), `311-1111`,
  `571-XXXX`, `260-XXXX` — highly office-dependent.
- **Milliwatt (1004 Hz test tone):** `959-1111`, `NPA-XXX-1111` in DMS
  regions.

See the `verify_claim` MCP tool for the DEFCON traps around universal
ANAC.

## Sources

- NANPA numbering-plan letters and INC guidelines.
- FCC Order 97-402 (July 1998 CIC expansion).

## See also

- [[operator-services/README]] — the operator-side surface behind
  these numbers.
- [[records/README]] — typed records for the classes.
