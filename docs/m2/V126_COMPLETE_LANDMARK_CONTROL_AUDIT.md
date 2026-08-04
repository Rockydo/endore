# v126 complete named-landmark control audit

This M2 political-fidelity batch replaces the scattered frontier-witness subset with
`docs/world/control/m3_landmark_control.csv`: one source-reviewed expected control
disposition for all 89 named landmarks. The generator rejects a missing, duplicate, or
unknown record and publishes every result through the ownership audit.

## Corrected exact cells

| Witness | Before | After | Basis |
| --- | --- | --- | --- |
| Argonath | ROH | GON | *Unfinished Tales*, “Cirion and Eorl”: the Argonath and Emyn Muil remained in Gondor, though deserted. |
| Amon Hen | ROH | GON | Same source: the western Seat of Seeing remained in deserted Gondor. |
| Amon Lhaw | WILD | GON | Same source: the eastern Seat of Hearing remained in deserted Gondor. |
| Mindolluin | WILD | GON | *The Return of the King*, Book V: Minas Tirith stands on Mindolluin’s shoulder. |
| Edhellond | DAM | WILD | *Unfinished Tales*, “Amroth and Nimrodel”: the last ship departed in TA 1981; the haven is abandoned at the start date. |

The paired Argonath/Amon Lhaw cells and the isolated Amon Hen cell retain explicit
topology dispositions because EU5’s passable-location graph separates them from mainland
Gondor with water and impassable Emyn Muil cells. This does not paint a broader Gondorian
strip or alter any physical map control.

## Guardrails

- Source-ledger occupancy, ruins, independent wilderness, shared-frontier sides, and
  invented realm seats are each explicit rather than inferred from a nearest capital.
- A forced occupied seat can override a reduced polygon centroid only for that documented
  exact point; non-seat political witnesses still require an accepted source claim or a
  source-cited exception.
- Coastline, terrain, forests, rivers, location topology, and realm roster are unchanged.

## Verification

- `gmake validate`: PASS in 456.6 seconds; the complete M2 world gate passed in 384.7
  seconds, including terrain, native rivers, political ownership, people, census, and
  templates.
- `gmake smoke`: PASS in 201.4 seconds. Vanilla control and ENDÓRË both reached
  menu-ready with zero mod-unique error-log lines on game-visible fingerprint
  `6fc487603862df1835ba14b30ada609da7c03204a1071640162d295aab424015`.
- `tools/eu5_slot.py assert-smoked`: PASS on that exact tree.
