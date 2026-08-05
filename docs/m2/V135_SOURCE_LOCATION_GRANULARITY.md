# v135 source location granularity

## Scope

This batch adds five separated, exact source controls that improve location density without
inventing borders, copying reference artwork, or displacing existing anchors. Each point is
already present in the hash-pinned local Arda Maps Third Age or ArdaCraft marker archive.
`tools/cartography_reference_audit.py` now binds its coordinate and provenance as a permanent
regression control; `m3_landmark_control.csv` binds its TA 3018 disposition.

| Location | Exact source control | TA 3018 disposition | Contract |
| --- | --- | --- | --- |
| Longbottom | ArdaCraft direct marker | inhabited Southfarthing village | Shire |
| Tuckborough | ArdaCraft direct marker | Took settlement / Thain's seat | Shire |
| Three-Farthing Stone | ArdaCraft direct marker | internal Shire monument | Shire |
| Underharrow | ArdaCraft direct marker | inhabited Rohirric hamlet in Harrowdale | Rohan |
| Goblin-gate | Arda Maps `point_place:GoblinGate` | guarded eastern exit of Goblin-town | Goblin-town |

The source audit rejects close aliases (Amon Sûl/Weathertop, Bag End, and Brandy Hall) rather
than allocating a neighbouring EU5 cell merely for a higher count. It also rejects the
uncertain Third Age reconstruction of Belegost and Mount Dolmed. This preserves the project
rule that map precision outranks quantity.

## Verification

- Complete regeneration passed in 507.8 seconds: the five controls resolve to distinct,
  nearby land cells (`me_land_0867`, `me_land_1667`, `me_land_5125`, `me_land_2282`, and
  `me_land_0449`) in the Shire/Bree-land, Rohan, and Anduin Vale regions respectively.
  The generated ownership ledger accepts their exact SHI, SHI, SHI, ROH, and GOB contracts.
- The complete `gmake validate` pass succeeded in 595.8 seconds: source conformance,
  controls, full map generation, native rivers/materials, realm ownership, setup, and lint
  all passed.
- The mandatory `gmake smoke` attempt deferred in 1.7 seconds because Antiquitas holds the
  cross-repository EU5 lease (`gamedriver session: mod`, PID 34912). This is not a game or
  map failure. The pending gate remains mandatory: acquire without waiting, run paired
  vanilla/ENDORE smoke, assert the fingerprint, and capture a fresh map-screen proof before
  publication.
