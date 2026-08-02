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

## 2026-07-30 — Arbitrary generated vegetation definitions are not renderer-discovered

Status: resolved by spatial serialization; quality refinement remains under reopened M2.

Two non-debug live-Observer attempts reached maximum close zoom over Mirkwood with zero
tree objects. The first used new `endore_forest_*`, `endore_woods_*`, and
`endore_pine_*` definition siblings under the installed `generated/` directory. The
second moved the same Arda-native transforms onto exact overrides of all nine retail
`forest_generator_*`, `woods_generator_*`, and `pine_generator_*` filenames. Both
variants parsed without a diagnostic and both rendered no vegetation.

Binary comparison rules out transform elevation: installed and ENDÓRË records are the
same headerless 40-byte position/quaternion/scale layout, and both store world-space Y as
zero. The exact-object-name test and the final override of all 36 exact
`{forest,woods,pine}_generator_{high,medium,low}_N.bin` paths also rendered no vegetation,
including after 30 additional close-zoom detents. A direct vanilla visual control was
inconclusive because the shared user directory still loaded ENDÓRË. Do not repeat these
generated-layer variants; pursue another renderer mechanism or a truly isolated vanilla
control.

New installed evidence changed the next experiment without invalidating those results:
retail generated bins keep contiguous records spatially local, whereas the prior ENDÓRË
writer randomized each 32-record batch across most of the continent. The new writer
Hilbert-orders Arda-only transforms and lint-enforces retail-like locality. This is a
format/batching change, not a fourth filename variant.

Resolution: a fresh no-debug full-3D Observer rendered dense physical tree objects over
Mirkwood from those Hilbert-ordered bins. The same session used no Earth transform or
decal. The renderer-discovery blocker is closed. Reopened M2 now treats forest margin,
glade, density, and theatre coverage as ordinary quality work rather than a missing
engine capability.

## 2026-07-30 — Final native-material visual pass exhausts the interactive renderer

Status: renderer bootstrap resolved; the broader reopened-M2 quality gate remains red.

Two non-debug `--visual-map` attempts reached the custom-map transition on fingerprint
`f004fab1`. The first completed `ClearAndRecalculateCachedData` and save serialization,
but the screenshot helper exceeded its bound before a stable country-selection capture.
The second completed the same cache transaction, then remained Windows-unresponsive while
CPU time advanced and working memory cycled between roughly 12 and 24 GB. The process was
stopped cleanly after two additional bounded monitoring intervals. Neither attempt added
a mod-specific `error.log` line.

The immediately preceding material-cache iteration did reach live 3D Map mode and proved
continuous ground variation, snow/rock mountain material, shoreline transitions, and
physical relief. That evidence proves the custom material mechanism, but it does not
accept the final refined tree. Do not repeat the same timed country-selection route.
Pursue a materially different bounded renderer route, reduce first-render pressure, or
obtain a fresh current-tree Observer save before repeating the multi-theatre gate.

Resolution: a lightweight debug Observer now writes a named `autosave_*` checkpoint.
The driver then cold-loads that checkpoint with no debug mode and full 3D terrain,
avoiding the resource-heavy new-game renderer during country selection. The current tree
reached live 3D Map in 122 seconds at about 5.6 GB working memory. Use this two-stage
route for all remaining M2 captures; do not return to the exhausted direct visual-map
country-selection path.

## 2026-07-30 — Windows foreground lock during native-density country selection

Status: bounded automation blocker; map transition completes, alternate capture contract
implemented.

Four exact-tree no-debug attempts completed `MainMenu->Game`, cached-data recalculation,
and setup serialization, then failed when the screenshot helper tried to force the
country-selection window into the foreground. Windows retained VS Code as foreground.
The engine also recreates its DirectX top-level HWND during this transition, invalidating
one handle between enumeration and rectangle lookup. PID-aware child-window acceptance,
ALT/`SwitchToThisWindow`, a verified title-bar click, and per-attempt HWND refresh did not
make foreground ownership reliable. The resulting forced session termination produced
identical abnormal-shutdown crash packs; no map parser crash preceded it.

Bounded fallback: capture only the fixed, topmost 1920×1080 rectangle whose HWND is tied
to the tokenized EU5 PID, without requiring keyboard foreground. Physical clicks on that
topmost rectangle acquire focus naturally; keyboard-only actions retain the stricter
foreground proof. Evidence screenshots remain subject to visual inspection. Do not
repeat the exhausted foreground-lock variants.

## 2026-07-30 — q1 cache exceeds the native-density first-load envelope

Status: q1 and q64 exact-count routes exhausted; half-vanilla topology authorized.

After the foreground-independent capture path exposed the actual screen, the alleged
country-selection success was still `Loading Savegame — 98%` with an unresponsive EU5
window. A PID-aware post-cache stability wait then observed the process exit before
becoming interactive. Repeating the launch with the lightweight debug profile and 3D
terrain disabled failed at the same boundary, so the failure is not specific to the
visual settings. Both attempts used the exact 28,490-location tree and the
699,999,471-byte q1 height cache.

Do not repeat q1 first-load attempts on this machine. Preserve the full-precision source
and test the verified generator-v19 q64 derived cache through the established lightweight-
checkpoint/cold-visual-resume route.

Resolution update: two q64 lightweight-checkpoint attempts reached healthy menus, accepted
New Game, completed setup/cache work, and then remained nonresponsive at 98% for the full
600-second post-cache bound. Both oscillated between roughly 14 and 23.5 GB working set;
the second drove free physical memory below 0.5 GB. Neither added a mod-unique error line.
The driver stopped only its tokenized process and released the shared lease after each
bound. The owner explicitly authorized approximately 50% fewer locations because Middle-
earth covers a smaller world, while making cartographic precision and lore accuracy
non-negotiable. Do not repeat exact-28,490 launches; proceed with 14,245 locations, retain
the full-resolution physical source, and spend topology preferentially on mountain chains.

## 2026-07-31 — Source-frame 14,245-location first-load envelope

Status: two-strike runtime blocker; static scale reduction in progress.

Paired vanilla/mod smoke passed on fingerprint `dbd52c52` with zero mod-unique error
lines. Two fresh, no-debug New Game routes then exercised that identical game-visible
tree. The full visual profile completed setup serialization and both cached-data
recalculations, but stayed Windows-unresponsive for the complete 600-second post-cache
interactivity bound. Working memory rose to about 23.5 GB before falling while CPU time
continued to advance. The lightweight checkpoint profile repeated the same measured
failure, cycling from roughly 12.9 to 23.2 GB and back down. Neither attempt emitted a
map, terrain, river, locator, setup, or renderer diagnostic; both were stopped through
their tokenized ENDÓRË lease. Evidence is in
`docs/screens/20260731_m2_sourceframe/` and
`docs/screens/20260731_m2_sourceframe_light/`.

Do not repeat the 14,245-cell fresh-game route unchanged. Preserve the equal-scale
ArdaCraft projection, all source-derived coast/height/river/forest geometry, all 42
anchors, and all 38 realm seats. Reduce only the runtime political tessellation to the
last proven 12,104-location aggregate, preferentially retaining 2,700 mountain cells.
If that materially different tree still misses the same bound twice, profile and reduce
derived renderer payloads independently of the binding cartographic controls.

Resolution update: the 12,104-cell tree passed full static validation in 315.3 seconds
and paired smoke on fingerprint `152d7798`, but both a no-debug lightweight checkpoint
and the historically proven debug-checkpoint profile repeated the same 600-second
post-cache timeout. The no-debug route peaked at 23.57 GB; the debug route started near
13.3 GB, remained CPU-active, and never produced a responsive rendered frame. Neither
added a map diagnostic. Location count is therefore not the dominant fresh-render
constraint. Keep the 12,104-cell source-frame topology and reduce the 407.7 MB,
10,193,212-transform vegetation set independently before another launch.

Resolution update: a 4,077,285-transform candidate reduced the object payload from
407.7 MB to 163.1 MB while retaining every named-forest floor, passed full validation
and paired smoke on fingerprint `8b088c92`, but its debug checkpoint still missed the
same bound and reached about 22 GB. Vegetation contributes to residency but is not the
dominant blocker. The remaining structural delta from the last live 12,104 tree is the
impassable split: 2,700 mountain locations now versus 520 then. Keep the total count,
4.08-million transform candidate, and all physical relief controls; test a 1,200-mountain
/ 10,700-land allocation before sacrificing q64 height precision.

Resolution: the 10,700-land / 1,200-mountain candidate completed a fresh debug New Game,
entered live Observer, and advanced through 3018.2.04. A second cold non-debug
`--visual-map` New Game independently entered live Observer on the same bytes. The first
debug attempt was already live but exposed a pause-banner detector false negative; the
driver now also recognizes the fixed Observer HUD, and both repeats passed. Retain q64
and close this resource-envelope blocker. The separate nine-theatre physical-quality gate
remains red.

## 2026-07-31 — Sub-location inland-water bowl renderer

Status: two-strike visual blocker; exact source outline retained, alternate
representation required.

The small source pool east of Hobbiton renders as a deep, cell-shaped quarry despite the
correct bottom-up terrain-cache orientation and a physically dry shoreline shelf. Two
fresh no-debug experiments on the same source geometry exhausted the direct engine-water
route:

1. Assigning the lake cells `flatland` plus the continuous ENDÓRË surface climate did not
   alter the bowl.
2. Raising the lake bed to 5,146, immediately below the measured local dry datum, removed
   the blue water surface but left the same dry bowl.

Both experiments were rejected and fully reverted. Do not repeat them. Keep the audited
lake outline in the binding cartographic controls; pursue either a non-engine-water
scenery representation or topology-aware handling for source waters smaller than one
runtime location after the broader theatre audit. Evidence:
`docs/screens/20260731_m2_lake_adapter_probe/`,
`docs/screens/20260731_m2_lake_floor_probe/`, and
`docs/screens/20260731_m2_height_material_probe/hobbiton_restored.png`.

## 2026-07-31 — Location-template and compact-ellipse mountain repairs

Status: two-strike visual route exhausted; physical height-envelope route in progress.

The correctly targeted Khazad-dûm, Dunharrow, and Goblin-town views showed broad grey
plateaus with hard pass cuts. Two materially different renderer-facing repairs failed:

1. Narrower, higher-amplitude off-axis peak ellipses changed source statistics but did
   not make the live ranges read as peaks.
2. A fresh New Game with every impassable cell rendered as neutral `flatland` instead of
   `mountain_wasteland` produced the same grey shapes.

Both experiments were rejected and reverted. Do not repeat template substitution or
compact-ellipse tuning against the old polygon lift. The neutral-template result proves
that the defect lives in the physical height/material source, not in political
impassability. The next route keeps every audited polygon border but treats it as a low
foothill envelope, with source ridge axes carrying the summit relief. Evidence:
`docs/screens/20260731_m2_compact_peaks_probe/` and
`docs/screens/20260731_m2_neutral_mountain_probe/`.

Resolution update: the physical height-envelope route is viable. Eighteen exact named
source peaks, narrow high saddles, low polygon foothills, and slope-aware exposed
materials produced visible 3D massifs in fresh Observer at all three target ranges while
preserving Mount Doom's crater. Do not return to the two exhausted routes. The remaining
defect is a new material-feathering task: hard slope thresholds form coarse rock ribbons
and islands at close zoom. Evidence:
`docs/screens/20260731_m2_slope_material_probe/`. M2 remains red.

## 2026-07-31 — Ridge-feather material v26 fresh-load envelope

Status: two-strike runtime blocker; candidate rejected and baseline restoration required.

Generator v26 replaced hard slope-only rock thresholds with a feathered field around the
nine audited ridge axes, their branches, and 18 exact named peaks. Its q64 height payload
was unchanged and its material cache remained approximately 28.1 MB with 63,596 unique
tiles. Two fresh debug visual New Games on identical runtime fingerprint
`0f65a5e5bcdbbb695b9366bbc88b54f673a7cb8183470ffbe070115c61e9e2b4` reached healthy
menus, accepted New Game, completed setup/cache work, and then remained nonresponsive
for the full 600-second post-cache bound. The second began with 23 GB free RAM. Neither
attempt emitted a map, material, cache, river, or locator diagnostic.

Do not launch this exact v26 cache a third time. It has no renderer evidence and is not
eligible to replace the smoke-green v25 slope-aware baseline. Restore v25, then revisit
ridge feathering only through a materially different cache representation or after an
independent runtime cause is identified. Evidence:
`docs/screens/20260731_m2_ridge_feather_probe/` and
`docs/screens/20260731_m2_ridge_feather_probe_repeat/`.

## 2026-07-31 — Decorative Shire-pond material v27 fresh-load envelope

Status: two-strike runtime blocker; candidate rejected and v25 restoration required.

Generator v27 kept `minor_lake_10`, `minor_lake_11`, and `minor_lake_12` as exact
lake-biome footprints over continuous dry terrain and selected wet river/transition
material instead of engine water. Two actual fresh visual New Games completed the menu,
accepted New Game, and completed setup/cache work, then remained nonresponsive for the
full 600-second post-cache interactivity bound without a rendered country-selection
window. Neither emitted a map, material, terrain-cache, river, or locator diagnostic.
Several intervening attempts deferred before launch because Antiquitas owned the shared
EU5 lease and do not count as runtime strikes.

Do not launch this exact v27 representation again. It has no renderer evidence and may
not replace the live- and smoke-proven v25 engine-water baseline. Preserve the
hash-pinned source pool outlines, but pursue only a materially different runtime route.
Evidence: `docs/screens/20260731_m2_decorative_pond_probe_live/` and
`docs/screens/20260731_m2_source_rivers_pond_final/`.

## 2026-07-31 — Restored-v25 source-river deep-load envelope

Status: two-strike runtime blocker; exact fingerprint must not be relaunched.

After source-backed Harnen/Morgulduin integration and full v25 lake/material restoration,
two fresh debug visual New Games on fingerprint
`b838a130d24989fdf86d77212f3b5cf4e21fc66fa2553091eb55b84572e4a64d`
reached responsive menus and began the MainMenu-to-Game transition but did not reach an
interactive country-selection or Observer window within the 600-second bound. The first
completed setup/cache detection; the second timed out during the same transition and the
configured process had stopped by cleanup. The paired vanilla/mod menu smoke on these
exact bytes remained green with zero mod-unique lines.

Do not launch this fingerprint a third time. The first attempt exposed one actionable
map-transition diagnostic—missing `gfx/city_materials` data for
`endore_dynamic_land_biome`—which was not covered by menu smoke. Repair and statically
validate that independent renderer registry before a materially different fresh load.
Evidence: `docs/screens/20260731_m2_v25_source_river_theatres/` and
`docs/screens/20260731_m2_v25_source_river_theatres_repeat/`.

## 2026-07-31 — City-material-corrected deep-load envelope

Status: two-strike runtime blocker; component fix retained, deep-load route exhausted.

The materially different fingerprint
`be6864eb31619101a62eb7fcdefb5f5bdb0070ca685a7d742a57c880d077c24c`
added a BOM-correct `gfx/city_materials` entry for `endore_dynamic_land_biome`. Full
validation and paired vanilla/mod smoke passed, and the earlier missing-city-material
diagnostic disappeared. Two fresh debug visual New Games nevertheless completed
setup/cache detection and remained nonresponsive for the entire 600-second post-cache
interactivity bound. Both started with roughly 24 GB free physical memory and emitted no
map, terrain, material, cache, river, or locator diagnostic.

Do not launch this exact fingerprint a third time. Retain the city-material registry
repair because it closes a proven renderer contract and has clean smoke evidence, but do
not describe it as resolving fresh Observer. The next route must change an independent
map-transition input or isolate the country-selection renderer workload without reducing
the binding source geometry or q64 physical precision. Evidence:
`docs/screens/20260731_m2_city_material_contract/` and
`docs/screens/20260731_m2_city_material_contract_repeat/`.

## 2026-07-31 — Live-proven-v25 byte A/B at country selection

Status: two-strike diagnostic blocker; source-river payload exonerated.

An isolated G:-only worktree combined the last live-proven v25 terrain/cache/river/
flatmap/vegetation bytes from `789d2d1` with only the retained BOM-correct city-material
registry. After one foreground-lock run was discarded before transition, two
PID-verified attempts on fingerprint
`86972304735a2d53ed3eebcd003dbe5f0e5ec25867a73ae2b8d8343e65abeace`
both started MainMenu-to-Game, completed setup/cache detection, and then remained
nonresponsive for the full 600-second post-cache bound.

Do not launch this diagnostic fingerprint again. Because the failure reproduces before
the source-derived Harnen/Morgulduin river raster, local incision/material tiles,
flatmap, and 12 altered woods bins are present, none of those changes is the
discriminating cause. Preserve the source-backed rivers. Treat the current issue as a
broader country-selection/runtime-environment blocker and change an independent load
input before further deep testing. Evidence:
`docs/screens/20260731_diag_baseline_v25_city_focus/` and
`docs/screens/20260731_diag_baseline_v25_city_focus_repeat/`.

## 2026-07-31 — Fresh user-cache country-selection route

Status: two-strike runtime blocker; stale cache removed but fresh New Game still blocked.

The ENDÓRË user directory contained a 2.4 GB shader cache dated 28 July and a 479 MB
generated `gfx` tree whose 350 MB `navmesh2.cache` dated from 29 July, before the current
Arda map. Both derived directories were moved recoverably to
`G:\endore_runtime\quarantine\20260731_pre_fresh_map_cache`; saves, logs, settings, and
playsets were untouched. The first cold run rebuilt 333 MB of shaders and a fresh 128 MB
Arda flatmap, reached MainMenu-to-Game state 2 in 127 seconds, but did not complete state
4 within the 600-second transition bound. A warm repeat completed setup/cache detection
but remained nonresponsive for the complete 600-second post-cache bound. No stale
navmesh was regenerated or inherited.

Do not repeat this exact fresh-cache New Game route. Keep the new Arda-derived cache and
the quarantined old copy; do not restore the July navmesh. Switch to the compatible
live-proven Observer save route for renderer evidence while investigating fresh country
selection separately. Evidence: `docs/screens/20260731_m2_fresh_user_cache/` and
`docs/screens/20260731_m2_fresh_user_cache_repeat/`.

## 2026-07-31 — Fresh country-selection renderer memory envelope

Status: resolved by a geometry-preserving runtime budget.

A corrected one-click/state-aware 900-second run on the 12,104-location,
4,077,285-object fingerprint completed MainMenu-to-Game state 4 and every cached-data
recalculation, then remained nonresponsive without a country-selection frame. EU5 held
32.42 GB private memory and continuously paged. Earlier exact-byte worktree repeats prove
that later source rivers and relief are not the discriminating cause: the formerly
successful tree was operating at an unreliable memory cliff.

The replacement keeps every binding physical source and the 174,763-entry q64 cache, but
uses 6,004 runtime locations and 2,038,645 derived vegetation transforms. Full validation
and paired smoke passed. Fresh New Game reached a calibrated country-selection frame,
entered live Observer in 135 seconds at about 8.62 GB private memory, and advanced through
3018.1.7. Fresh start-game loading is no longer blocked. Do not restore the quarantined
July navmesh or relaunch the superseded 12,104-location fingerprints. Evidence:
`docs/screens/20260731_current_joined_transition_fix/` and
`docs/screens/20260731_runtime_budget_6004/`.

## 2026-08-02 — External OS quit during v70 fresh-world proof

Status: two-strike external runtime blocker; continue static forest work and retry at the
next natural game checkpoint.

Two fresh `new-observer` attempts on identical game-visible fingerprint
`ffb9947c2035d78a0fe96f845380fabef5d12c2ba48580eabb268f2368ab1e17` were terminated by
an OS-requested quit at different stages. The first reached a fully rendered country
selection and then exposed an independent Observer-button false positive in the driver;
the second began `MainMenu->Game` and was closed before transition completion. In both
cases EU5 logged `Quit: Quit event from OS`, unwound through LoadingScreen/SplashScreen,
produced no new crash directory, and emitted no fatal map/height/terrain/cache diagnostic.
Antiquitas had no active test process or current lease, and the shared slot returned clean
and available after each exit. This is not evidence that v70 map bytes failed to load.

Retain the driver correction that requires the independently observed game-rule dialog
before accepting the ambiguous gold start control and clicks the true centre of `Start
Observing the game`. Do not spend a third immediate launch on the same checkpoint. Continue
the owner-requested static forest-density/species batch and retry fresh Observer plus
paired smoke after that fingerprint changes. Evidence:
`docs/screens/20260802_v70_morannon_ramped_hinge/` and
`docs/screens/20260802_v70b_morannon_ramped_hinge/`.

## 2026-08-02 - v74 paired smoke deferred behind Antiquitas

Status: two-strike external coordination blocker; pending gate retained, continue the next
static atlas correction and retry only at a natural checkpoint.

Two `gmake smoke` attempts for exact game-visible fingerprint
`98c795b54ca828d998f81ed2e3548cc61087dc6955fce28aab6ba8410b26962a` correctly returned
exit 75 while Antiquitas owned the shared EU5 session lease (PID 8848, fingerprint
`ad4bd264`). Neither attempt launched, waited on, or interfered with the other project.
ENDORE's pending smoke gate remains recorded at
`G:\endore_runtime\state\pending_eu5_gate.json`. This is not a game or content failure:
the same ENDORË candidate already completed a fresh HUD-proven Observer start, dense-forest
and political-map captures, and 14 days of playback with no `error.log` growth.

Do not poll the lease or attempt a third immediate smoke. Continue the static correction
of the nine-theatre Forochel/Belfalas/Rhun/Harad defects and retry the exact pending gate
at the next coherent checkpoint. Do not commit the game-visible v74 batch until paired
smoke and `tools/eu5_slot.py assert-smoked` pass.

Resolution: the lease became available at later natural checkpoints. Two speculative
climate-material candidates were live-rejected and fully rolled back; the narrowed
vegetation/source-ownership tree then passed fresh Observer, untouched 45-second playback,
paired smoke, and exact `assert-smoked` on fingerprint `fb07a215`. This coordination
blocker is resolved for the v75 focused checkpoint.
