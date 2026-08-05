# v136 Buckland anchor density

## Scope

Newbury, Standelf, and Deephallow are distinct Hobbit settlements shown on Tolkien's map of
the Shire. The authoritative Arda Maps Third Age topology supplies three exact point-city
controls. They are added to `settlements.csv`, not merely to the later landmark allocator,
so each control becomes a pinned land seed in the 6,004-location M2 tessellation.

This corrects a demonstrated precision failure: once the existing named-location reservation
set was applied, resolving these points as post-hoc landmarks would place them 0.013–0.022
equal-scale map units away from their sources. A pinned source anchor creates the necessary
local cell instead of overwriting Brandywine Bridge, Bucklebury, or an unrelated generic cell.
Each locality replaces a nearby, unreviewed generic seed slot (1908, 3335, and 2753); slots
with existing political-repair contracts are deliberately excluded.

## Political scope

The change adds no realm and redraws no border. All three settlements use the existing Shire
scope pending M3's locked realm-roster work. This records geographic and settlement fidelity
without prematurely deciding Buckland's separate constitutional status.

The pre-existing, source-pinned Brandywine Bridge cell remains on the Bree-land side of the
frontier. The exact new local cells separate it from Bree's primary component in the EU5
adjacency graph, so its single-cell crossing is registered in the reviewed physical-component
ledger. No surrounding land is recoloured to conceal that real source/topology consequence.

## Verification

- Full regeneration passed in 463.7 seconds. Newbury, Standelf, and Deephallow resolve as
  passable Shire anchors at the rounded source-grid coordinates `0.382906,0.230581`,
  `0.383150,0.237421`, and `0.382906,0.242306` respectively. The world remains exactly
  6,004 locations and 38 realms.
- Identity comparison against the published baseline proves the intended one-for-one change:
  only `me_land_1908`, `me_land_3335`, and `me_land_2753` are removed; only `newbury`,
  `standelf`, and `deephallow` are added; every surviving location key retains its exact
  former seed coordinate. All three resulting SHI ownership contracts are accepted.
- The full `gmake validate` pass succeeded in 562.5 seconds, including source conformance,
  map controls, terrain/rivers, realm topology, naming lock, setup, census, and lint.
- The mandatory `gmake smoke` attempt deferred in 1.9 seconds because Antiquitas holds the
  shared EU5 lease (`gamedriver session: mod`, PID 35328). The pending gate remains
  mandatory: acquire without waiting, run paired vanilla/ENDÓRË smoke, assert the exact
  fingerprint, and capture a fresh regional map-screen proof before publication.
