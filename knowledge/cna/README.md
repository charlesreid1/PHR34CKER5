# CN/A — CUSTOMER NAME AND ADDRESS

CN/A bureaus were the internal telco offices that mapped a phone number to
the subscriber's name and billing address. Each RBOC ran its own; each had
its own hours, its own toll-free ANI-restricted number, and its own
predictable social-engineering script.

## The classic pretext (historical)
> "Hi, this is [name] from the [local BOC] business office, I need a CN/A on
>  212-555-0100 for a repair ticket."

The bureau operator would read back the listing. No callback, no auth beyond
"you sound like you belong on this line."

## Why it worked
- CN/A numbers were only supposed to be dialable from telco-internal ANI.
- Blueboxing/tandem tricks let outsiders originate calls that *looked*
  internal.
- Bureaus were staffed for volume, not for security.

## Modern equivalent
CN/A as a phone-based service is essentially dead. Its descendants are:
- LIDB (Line Information Database) lookups
- CNAM (Caller ID name) services
- LNP (Local Number Portability) dips
All are now paid, contracted, and logged.

## See also
- [[glossary/README]] — RBOC, BOC, LATA, ILEC
- [[zines/README]] — TAP had rotating CN/A number listings for years
