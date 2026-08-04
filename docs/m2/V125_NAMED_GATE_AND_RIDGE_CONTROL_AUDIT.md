# v125 named gate and ridge control audit

This bounded M2 review re-checks the source-pinned political controls in the theatres
where a coarse nearest-seat allocation is most likely to produce a misleading political
shape: Dunland/Isengard, Lothlorien, Dale/Erebor, Mordor, and the represented East.
The coast, height, forest, river, location, and claim-polygon controls are untouched.

## Exact changes

| Named witness | Before | After | Basis |
| --- | --- | --- |
| Cirith Gorgor | wild | MOR | LOTR, Book IV, Ch. 3 places the Haunted Pass at the guarded Black Gate between its Towers. |
| Morgai | wild | MOR | LOTR, Book IV, Ch. 8 identifies the Morgai as the inner ridge of the Mountains of Shadow within Mordor. |
| Methedras and its two detached unnamed north-spur cells | ISE | wild | LOTR, Book III, Ch. 9 places Isengard at Methedras' foot; the source-oriented compact Nan Curunir vale cannot retain a detached mountain-side island. |

Cirith Gorgor and Morgai are not a redraw of Mordor. They are two exact
`FRONTIER_LANDMARK_CLAIM_EXCEPTIONS`, source-cited and cross-validated against a matching
required-owner contract. This preserves the frozen source-derived Ered Lithui/Ephel Duath
lowland enclosure while removing an implausible wild gap at the Black Gate and on the
inner Mordor ridge.

## Cross-theatre findings retained

| Theatre | Source witnesses checked | Result |
| --- | --- | --- |
| Dunland / Isengard | Dunland Moot, Fords of Isen, Isengard, Methedras | Dunland stays a compact lowland polity; the Fords stay Rohan; Isengard stays Nan Curunir; Methedras is wild. |
| Lothlorien | Caras Galadhon, Cerin Amroth, Redhorn Gate, Field of Celebrant | Golden Wood remains within its source forest/Naith mask; Moria controls its immediate gate approach; the Celebrant field remains wild. |
| Dale / Erebor | Dale, Esgaroth, Erebor, Iron Hills, Withered Heath, Grey Mountain holds | The three distinct northern centres retain their compact source roles; abandoned and dragon-haunted ground remains wild. |
| Mordor approaches | Cirith Gorgor, Narchost, Carchost, Udun, Gorgoroth, Nurn, Lithlad, Dead Marshes, Dagorlad, Shelob's Lair | Occupied gateworks and the interior are Mordor; the marshes, battle plain, and Shelob's independent pass remain wild. |
| East and South | Dorwinion, Burh Gath, Wainhold, Eastern March, Khazan, Harnenhold, Qarsad, Mumak Gate | Each existing canonical or explicitly marked invented seat resolves to its documented realm; no broad eastern or southern border is inferred from a point. |

## Guardrail

The M3 checker rejects an orphaned exception or one whose required owner differs from
its exception tag. The generated ownership audit exposes the exact required-owner verdict
for all three changed witnesses. This is an ownership-quality regression suite, not a
licence to fill uncertain wilderness.

## Verification

- `gmake validate`: PASS in 477.5 seconds; the complete M2 world gate passed in 405.6
  seconds, including political connectivity, people, census, runtime, and terrain-template
  joins.
- `gmake smoke`: PASS in 201.7 seconds. Vanilla control and ENDÃ“RÃ‹ both reached menu-ready
  with zero mod-unique error-log lines on game-visible fingerprint
  `3606db87877e7d37523b02989b6650db9549190a6ac7cf6c34e977de17bd0d33`.
