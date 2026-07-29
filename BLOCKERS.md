# ENDÓRË Blockers

## 2026-07-28 — Direct centroid locators are rejected after custom-map geometry

Status: resolved in M1.

Two real-game attempts proved that the custom RGB map reaches the menu, but direct centroid
files still produced `game_object_locators.cpp:1159` incomplete-locator notices and
`manual_locators_database.cpp:213` requested `MapObjects.GenerateGameLocators` output.
The second attempt also proved that an empty `ports.csv` is invalid and enumerated the
coastal-pair signatures.

Resolution: the automated engine command established the exact completeness rule. Combat
and unit-stack locators cover every live location except `impassable_mountains`; city
locators cover ownable land. The deterministic generator now reproduces that contract.
No human editor step is required.

## 2026-07-28 — All-passable proof classifications overflow the in-game renderer

Status: bounded M1 failure; resolved by restoring eligibility classes.

Two full new-game loads reached `InGameInterfaceIdler` and then failed with
`Tried to reallocate a pre-allocated buffer` / `EXCEPTION_ACCESS_VIOLATION`
(`crashes/Europa Universalis V20260728_213234`). The all-passable diagnostic
made every former impassable location city-eligible, growing the city object
set beyond the installed contract. The recovery driver reproduced the failure.

Resolution: the 300-location proof restores explicit impassable classifications and emits
locators from current proof eligibility rather than stale installed eligibility.

## 2026-07-29 — Full installed location count exhausts memory after custom-map caches

Status: bounded M1 failure; resolved by the planned 300-location proof world.

Two DX12 new-game attempts completed both `ClearAndRecalculateCachedData` passes
but then grew beyond safe memory bounds: the one-country scaffold reached roughly
17 GB and terminated abnormally, while the full-government diagnostic crossed
20 GB before the driver stopped it. Both used 28,573 live locations on the
reshaped full-size canvas. Restoring valid governments removed null-scope noise
but did not change the growth, proving the retained installed location count is
not a viable custom-world scaffold.

Resolution: the 300-location proof loads and runs at roughly 5–6 GB.

## 2026-07-29 — Retail automatic scripted-test scheduler does not activate

Status: bounded M1 limitation; manual live-engine test logging is the verified fallback.

The same M1 `common/tests` assertion was attempted with `-test`, `-automated_test`, both
flags together, observer mode, a focused test name, custom log sinks, and same-filename
quarantines for the installed tests. The executable contains the scheduler and result
categories, and the test file parses, but no automatic PASS/FAIL record was emitted.

The live observer console can execute the underlying `test_log` effect. It emitted a
parseable sink probe in year 3029 and a conditional native-immortality PASS in year 3040.
M1 records those results honestly. M2 may revisit scheduler activation only if installed
evidence changes; it does not block the proven runtime assertion path.

## 2026-07-29 — Non-empty production adjacencies create an empty lookup

Status: bounded M2 limitation; zero-byte fallback is green and non-blocking.

Two controlled real-game A/B attempts tested the 8192×4096 custom canvas with valid
Himling/Tolfalas adjacency rows, then with a header-only file. Both non-empty variants
produced the same single empty-location lookup. Removing all bytes from
`adjacencies.csv`, matching the proven M1 fallback, removed the diagnostic without
affecting ordinary coastline navigation.

Resolution: M2 emits an exact zero-byte file and keeps the two intended crossings in
generator source. A later map-editor-backed experiment may activate them if it proves the
runtime serialization contract. This does not block the production map or its ordinary
land/sea graph.

## 2026-07-29 — Arda road splines cannot be rebuilt within the retail map editor

Status: bounded M5 blocker; the authored route ledger is retained, but the M5 gate remains
open until an Arda-native `spline_network.splnet` can be produced.

The gameplay road graph accepts 302 adjacent land edges across nine canonical routes, but
the renderer correctly refuses to draw them through the installed Earth-authored spline
cache. A live load reports one `Could not find spline network strip of type 0` diagnostic
per missing Arda strip. Suppressing the diagnostics or retaining the Earth binary would
violate the native-map contract.

Two supported `-mapeditor` launches attempted the engine's own spline rebuild path. The
first used the milestone visual-map profile; the second used minimum graphics. Both entered
`MapEditorIdler`, loaded the Arda graph, then exhausted machine resources before the editor
UI became interactive. The minimum-graphics attempt reached the 88% savegame phase, grew to
about 30 GB private memory, consumed all 72 GB of swap, and terminated abnormally at
2026-07-29 17:15 with 3.6 GB system memory remaining. Neither run emitted a mod-owned
`.splnet`.

Bounded fallback: keep `docs/world/economy/routes.csv` and the deterministic adjacency
paths as source truth, omit the runtime road graph from any green M5 census slice, and
continue census/economy verification. Revisit native spline serialization only through a
materially different route, such as an editor-safe content-source overlay or a proven
binary writer; do not repeat the two exhausted editor launches.

## 2026-07-29 — Boat foam state event lacks `waves_vfx`

Status: bounded M5 deep-test blocker; census initialization is green, but the five-year
economy gate remains open.

A fresh non-debug Observer run initialized with the accepted 1,486-byte baseline and
advanced cleanly through early February. On 3018.2.17, the installed
`boat_with_oars_unit` state machine emitted:

`Couldn't find an entity at hierarchy place waves_vfx`

`Error on state machine [boat_with_oars_unit] when trying to execute event [foam_stop]`

The repository contains no override for that entity or state machine, and a text search
found no writable source definition in either the mod or installed game. A same-duration
direct “vanilla” control was attempted, but the direct launch still loaded ENDÓRË's map
despite selecting the vanilla playset, so it cannot classify the lines as a vanilla
baseline.

Bounded fallback: retain the green paired menu smoke and the zero-error fresh census
initialization as evidence for the current census repair, but do not claim the M5 deep
gate. Pursue a materially different unit-entity resolver or a truly isolated vanilla
Observer control before the five-year economy run.
