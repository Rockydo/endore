# v128 source-led frontier theatre audit

This M2 political-map batch makes the requested whole-map review repeatable without
turning broad rectangles into invented countries. It adds six source-led review envelopes
to `tools/m3_realms.py`. The envelopes are validation-only: the existing narrow source
zones, claim polygons, and exact landmark contracts remain the sole ownership allocation
authority.

## Covered review scopes

| Theatre | Required local controls | Evidence basis |
| --- | --- | --- |
| Gap of Rohan | Dunland, Fangorn, Isengard, Rohan; Dunland Moot, Derndingle, Methedras, Fords of Isen, Glittering Caves | Arda Maps Dunland/Methedras/Fangorn/Fords controls; *The Lord of the Rings*, Book III, Chapters 7-9. |
| Lothlorien and Moria | Lothlorien, Moria; Ost-in-Edhil, Redhorn Gate/Pass, Caradhras, Celebdil, Fanuidhol, Cerin Amroth, Egladil | Arda Maps Golden Wood and Misty Mountain controls; *The Lord of the Rings*, Book II, Chapters 3, 4, 6. |
| Dale and Lonely Mountain | Dale, Erebor, Esgaroth, Iron Hills; northern Mirkwood, Withered Heath, Iron Hills | Arda Maps Erebor/Iron Hills/Long Lake/northern Mirkwood controls; *The Hobbit*, Chapters 10, 14, 17. |
| Mordor and Ithilien approaches | Gondor, Mordor; Argonath, Amon Hen/Lhaw, Cair Andros, Henneth Annun, Cirith Ungol/Gorgor, Udun, Gorgoroth, Nurn, Lithlad, Morgai | Arda Maps Ered Lithui/Ephel Duath/Mordor controls; *The Lord of the Rings*, Books II, IV-V. |
| Represented East and South | Dorwinion, Rhun, Wainriders, eastern Rhun, Khand, Near/South Harad; Iron Hills, Burh Gath, Wainhold, Eastern March, Khazan, Harnenhold, Qarsad | Arda Maps Sea of Rhun, Khand, Harnen controls; sparse borders remain logged extrapolations. |
| Far Harad fringe | Far Harad; Mumak Gate | Arda Maps southern source extent; represented fringe remains a documented extrapolation. |

## Enforced invariants

For each theatre, validation fails when a land cell has an unreviewed owner, a required
local realm disappears, a required landmark has no ownership contract, a witness escapes
its review scope, or its contracted owner is not admitted by that scope. Additional
silhouette contracts keep Dunland, Lothlorien, Moria, Dale, Esgaroth, Iron Hills, Erebor,
Isengard, and Mordor compact and geographically distinct.

The first audit exposed that Mumak Gate is in the represented Far Harad fringe, not in the
East/South envelope. The correction was to add a separate bounded Far Harad review scope;
no location ownership, terrain, coast, forest, river, realm roster, or landmark coordinate
was changed.

## Deterministic result

`tools/m3_realms.py --write` regenerated the manifest binding for the theatre source
ledger. `tools/m3_realms.py --check` passes in 154.5 seconds with 38 realms, 3,027
assigned land cells, and 2,977 deliberately wild cells. The retained wilderness is
intentional: neither source maps nor Tolkien provide a cadastral border for every empty
cell, so no speculative fill is introduced.

## Repository and runtime verification

- `gmake validate`: PASS in 509.0 seconds, including the complete `m2_world` gate in
  436.5 seconds, the native indexed-river checks, terrain-cache checks, and the new
  theatre containment audit.
- `gmake smoke`: PASS in 201.3 seconds. The paired vanilla and ENDÓRË launches both
  reached menu-ready through the shared EU5 lease; ENDÓRË added zero error-log lines.
- `tools/eu5_slot.py assert-smoked`: PASS for game-visible fingerprint
  `580fe4052808c55a15601f170154babfbbc9d866f2671ab021103705c94af9c6`.

This establishes the permanent political-review baseline. M2 remains red pending the
complete owner fidelity decision; no gameplay, mechanics, faction, art, or lore milestone
is unblocked by this static control audit.
