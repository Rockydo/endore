# V137 - Geographic witness anchors

Status: published candidate; the complete three-place batch passed the full static and
runtime gates on 2026-08-05.

## Scope

This batch makes three well-separated direct source controls exact EU5
land cells without perturbing the established 6,004-location topology:

| Place | Exact source control | TA 3018 disposition |
| --- | --- | --- |
| Slag-hills | `SlagHills`, `0.602143, 0.531198` | desolate exterior of the Black Gate, deliberately wild |
| Haudh in Gwanûr | `HaudhInGwanur`, `0.595579, 0.705673` | historic Gondorian memorial in South Gondor |
| The Forsaken Inn | ArdaCraft marker, `0.412567, 0.232195` | abandoned East Road inn, deliberately wild |

The source files remain hash-pinned outside the repository. No reference imagery, film
frame, or traced map geometry is committed.

## Mechanism and safety contract

`geographic_anchors.csv` reuses the proven slot-preserving anchor design while declaring
these rows inactive. Inactive anchors receive exact names and a complete owner/wilderness
contract, but are excluded from the active-settlement ownership and population path. Their
reserved generic slots are `0432`, `0878`, and `2915`; the name lock replaces only those
three generic
keys. The generator consumes each former ordinal, so every surviving location
retains its key and seed coordinate.

The separate Arda Maps `DoorsOfDurin` point remains a terrain/relief gate control. Its exact
pixel is impassable mountain terrain, so a passable EU5 political cell there would be less
accurate than the existing Moria-side approach representation. It is explicitly rejected as
a location addition rather than relocated into a misleading neighbouring cell.

## Required evidence before publication

- complete world write: PASS in 495.3 seconds;
- complete static validation: PASS in 542.3 seconds, including the source audit, full M2
  generator chain, political topology, and lint;
- slot-preserving generator contract: each exact source seed consumes its former generic
  ordinal, retaining all subsequent generated keys and seed order;
- shared-lease smoke: PASS with zero mod-specific new error lines; the tree remained fixed
  throughout launch and `eu5_slot.py assert-smoked` passed on fingerprint
  `975d5651a0e013f40e5b8975aa6cfa8d4aac8a7e46296bc7f9f48c425e7d4b3c`.
