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
- M3 now paints 38 first-class realms over the binding physical world, assigns 4,189
  passable locations, keeps 1,011 desolate land locations deliberately wild, and leaves
  every sea, lake, and impassable mountain unowned.
- The realm generator emits the complete 5,812-location gazetteer, ownership ledger,
  script-only first-pass arms, setup files, localization, and an exact political/physical
  QA raster. Validation proves zero below-water owned pixels and dry-land capitals.
- The M3 real-game gate passed in northern and central/southern political views: labels
  sit on their colored territories rather than the ocean. Observer advanced from
  3018.1.1 to 3018.1.25, paired smoke remained zero-new, and the deep runtime log had no
  mod-caused error.
- M3 is complete. Installed culture, faith, census, government-title, and ruler values
  remain explicitly technical bridges for M4–M6, not accepted final content.

- M4 now owns 33 cultures in 10 groups and 10 faiths in three gameplay groups across all
  5,200 passable land locations and every realm primary.
- Ten language roots, 33 culture dialects, and deterministic name pools emit 1,105
  localized male, female, and house names from documented canon seeds and constructed
  conventions.
- Exact overlays gate all 29 installed Earth religion files to 3200.1.2 while preserving
  the parser ABI required by inherited scripts.
- The actual Culture and Religion location map modes render the authored terms across
  representative northern, eastern, western, and southern theatres.
- Paired smoke is green. A fresh non-debug Observer run advanced from 3018.1.1 to
  3018.1.20 without recovery, while `error.log` remained byte-identical at 1,486 bytes.
- M4 is complete. M5 census, settlements, markets, infrastructure, economy, and military
  setup is the next active milestone.
- The first M5 slice now replaces the technical census with 9.029 million authored
  inhabitants across 5,179 populated locations while leaving all 21 canonical ruins
  empty. Every authored culture and faith appears, minorities are explicit, and the
  installed culture ABI presences remain separately measured technical entries.
- The same deterministic model seeds 12 markets, 58 towns/cities/holds, regional and
  location development, timeless raw materials for every passable land location, modest
  starting buildings, and one provisional army per first-class realm. Pop-type names are
  relocalized in all 11 supported clients.
- Nine canonical road corridors remain source-authored as 302 validated adjacent edges,
  but the runtime road graph is deliberately empty until an Arda-native
  `spline_network.splnet` exists. This removes every missing-strip diagnostic without
  retaining Earth splines; the bounded editor blocker remains open.
- Full validation and the paired vanilla/mod smoke are green for this slice. The terrain
  regression gate still proves 174,763 custom-indexed tiles and zero Earth decal layers,
  while the smoke produced zero mod-unique error lines on fingerprint `ee4afc6a`.
- M5 remains active: a fresh five-year Observer economy run and native road-spline
  serialization are still required before its milestone gate can be declared.
- Fresh M5 initialization exposed 23 inherited culture-ABI populations placed in
  0.063k–0.095k Lossoth locations. Reducing entry count did not alter the failures;
  assigning all 2,086 ABI populations after census allocation to hosts with at least
  1.0k authored inhabitants eliminated every missing-culture line.
- The repaired non-debug selection screen loaded the custom map with the accepted
  1,486-byte baseline, and live Observer advanced to 3018.2.17. The census remained
  clean; a separate late vanilla boat-model `waves_vfx` state-machine diagnostic is
  recorded as an open M5 deep-test blocker rather than being hidden or misclassified.
- Owner close-zoom review has reopened M2 and superseded M5 as the active priority. The
  current world remains a valid technical proof but fails the production visual bar:
  geometric internal waters/forest masks, crude coasts, weak rivers, and missing
  close-zoom relief, vegetation, and terrain texture. New gameplay work is paused until
  `docs/m2/VISUAL_REOPEN_GATE.md` passes in the real non-debug renderer.
- The first reopened-M2 production slice replaces every ellipse/box natural region with
  explicit authored polygons plus deterministic sub-macro edge detail. It expands the
  drainage model from 9 to 23 rivers, the relief model to nine branched massif systems
  with nine deliberate crossings/valleys, and adds the permanent Fields of Nurn anchor.
- The native height source now separates rolling lowlands from rugged mountain-local
  octaves. The full 174,763-tile terrain cache was rebuilt and still contains zero Earth
  decal layers.
- Close-zoom vegetation no longer depends on quarantined Earth definitions: 420,000
  deterministic Arda-native transforms reuse exact installed forest, woods, and pine
  meshes across EU5's high/medium/low vegetation layers.
- The installed river parser rejected both naturalized paths and every tested custom
  affluent junction. The corrected engine raster ships 12 complete major channels;
  all 23 axes still drive valley incision and the authored drainage control.
- Full static validation is green. Paired smoke remains pending only because Antiquitas
  owned the shared EU5 slot at the first retry; no visual acceptance is claimed yet.
- The major-channel smoke isolated one remaining error to the Baranduin ending inland
  after the west-coast rewrite. Its parser-visible channel now continues to open water;
  static validation is green again and the confirming smoke deferred behind a new
  Antiquitas lease.
- The Baranduin engine path now begins monotonically at Lake Evendim's southern outlet and
  reaches unambiguous open ocean. Paired smoke passed with zero mod-unique lines on
  fingerprint `d24cf138`; all 12 major channels and the native vegetation definitions
  load cleanly.
- The repository-safe 512-unit terrain-cache rebuild reduced `heightmap.bin` from 116 MB
  to 82.2 MB while preserving the full-precision source. Paired smoke passed again with
  zero mod-unique lines on fingerprint `fa9123dc`.
