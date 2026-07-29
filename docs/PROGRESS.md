# Progress

## 2026-07-28

- M0 complete locally: governing plans read; installed build 24187685 matches the
  reference environment; autonomous toolchain ported; relocated user directory and
  junction configured; fresh vanilla baseline captured; paired vanilla/mod smoke passed
  with zero mod-only error lines.
- M1 remained the only content priority and blocked all broader content.
- M1 spike attempt 1 reached the menu and isolated river/locator diagnostics. Attempt 2
  removed river errors and proved the mandatory coast-port and engine-generated-locator
  contracts; the bounded failures are recorded in `BLOCKERS.md`.

## 2026-07-29

- M1 Proof of Arda is implemented: a recognizable Middle-earth silhouette with exactly
  300 locations, 30 provinces, 56 ports, a 3018.1.1 start, 3200.1.1 end, and `wrap_x = no`.
- The proof map loaded in the real game, entered live Observer mode, and advanced from
  1 January to 5 January 3018. The evidence pack contains the world-map and live-session
  screenshots.
- A live `test_log` sink probe and a conditional native-immortality assertion both
  emitted parseable results. Native `is_immortal = yes` is proven.
- Geography compatibility, coastline, river, hierarchy, dangling-reference, and locator
  contracts are generator-checked. The M1 overlays are explicitly temporary and are the
  first removal target in M2.
- M1 gate is green: `gmake validate` passed, the paired vanilla/mod smoke reported zero
  mod-only `error.log` lines, screenshots are committed, and a live in-game assertion
  executed. Work may now proceed to M2.
- M2 projection controls are authored at 1024×512 for an 8192×4096 production canvas:
  coastline and bays, four lakes, seven ridge systems, five strategic passes, biome and
  density zones, nine river axes, and 41 cited settlement anchors. The deterministic
  renderer produces six committed QA/control rasters and a source-hash manifest.
- The full M2 production stack is generated from those controls: an 8192×4096 raster with
  5,812 locations, 4096×2048 height and flat-map layers, a valid directed river graph,
  six-continent geography, terrain templates, 417 sea-zone ports, and complete
  type-specific locators.
- The 41 canon settlement anchors are pinned in the production mesh. Location allocation,
  colors, definitions, hierarchy, terrain, ports, rivers, flat-map texture, locators, and
  runtime setup are deterministic and validated by `tools/m2_world.py`.
- All M1 runtime artifacts and proof-overlay manifests are removed. A generated M2
  quarantine sweep now isolates still-parsed inherited Earth scripts while preserving
  exact-source traceability.
- The canonical validator and paired real-game menu smoke are green for the production
  stack with zero mod-unique error lines. The deep M2 in-game gate then passed: the engine
  resolved Minas Tirith, Rivendell, and Orodruin, Observer advanced eight days, and the
  deep log retained zero content or dangling-reference diagnostics.
- M2 is complete. Its evidence pack records the 5,812-location model, real-game map and
  Observer screenshots, the 3018.1.9 time-advance result, hashes, and the final diagnostic
  snapshot. The production map is now the binding base for M3.
- Owner close-zoom review correctly invalidated that visual gate: most authored lowlands
  were below EU5's installed raw-height waterline, and retail Earth-authored generated
  vegetation transforms still fell through the VFS. All M3 realm work was quarantined
  without committing it while M1/M2 returned to red.
- The production stack now uses the installed native resolutions throughout: 16384x8192
  locations/rivers, 8192x4096 height/flat map, and 8191x4095 biomes. The complete
  65536x32768 virtual terrain cache has 174,763 custom-indexed tiles and no retail decal
  payloads.
- The waterline mismatch is fixed and linted: installed `NJominiMap.WATERLEVEL` corresponds
  to raw sample 5466; generated ENDÓRË lowland is at least 10477 and all authored water is
  at most 420. Exact-file overlays also disable all 41 retail generated map-object
  definitions and nine static Earth transform definitions.
- The corrected physical map passed a new real-game visual gate at full-map, inland,
  open-sea, and shoreline scales. The shoreline entered live Observer and advanced from
  3018.1.1 to 3018.1.4 with no mod-caused diagnostic. The earlier visual evidence is
  superseded by `docs/m1/screenshots/04` through `08`.
