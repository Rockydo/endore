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
