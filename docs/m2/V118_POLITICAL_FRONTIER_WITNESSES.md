# v118 political frontier witnesses

## Scope

This is a narrow TA 3018 ownership correction within reopened M2. It changes no coastline,
height, material, river, forest, location coordinate, capital, or realm roster. The audit
uses exact named locations from the Arda Maps control ledger as durable witnesses rather
than reshaping broad nearest-seat borders.

## Corrected witnesses

| Witness | Previous owner | TA 3018 owner | Basis |
|---|---:|---:|---|
| Frogmorton | wild | Shire | *The Fellowship of the Ring*, Book I, Ch. 3; named East Road village |
| Stock | wild | Shire | *The Fellowship of the Ring*, Book I, Ch. 3; eastern Shire village |
| Haysend | Bree-land | Shire | *The Fellowship of the Ring*, Book I, Ch. 5; Buckland settlement |
| Old Forest | Bree-land | wild | *The Fellowship of the Ring*, Book I, Ch. 6; beyond the settled Shire and not a Bree village |
| Nardol | Drúadan Forest | Gondor | *The Return of the King*, Book V, Ch. 1; Gondor's beacon chain |

The audit deliberately leaves the empty Ithilien belt, the Dead Marshes, Barrow-downs,
and uncertain edge claims wild. Cirith Gorgor and Shelob's Lair remain wild because their
exact pass cells fall outside the source-reviewed Mordor enclosure; the adjacent Narchost,
Carchost, Cirith Ungol, and Durthang cells remain Mordor-controlled. It also leaves Amon
Hen, Rauros, and the Argonath to the existing reviewed Rohan/Gondor border contract: the
cited source maps are geographic and do not warrant a speculative broad frontier redraw.

## Regression contract

`FRONTIER_LANDMARK_REQUIRED_OWNERS` forces these exact localized anchors after normal
allocation and validates their physical claim envelopes. The derived ownership audit must
report them as `accepted_forced_anchor`; any terrain reseed that changes their identity,
passability, or admissible frontier fails generation rather than silently moving a realm.
