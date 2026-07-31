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
- Maximum-close non-debug evidence disproved three generated-vegetation discovery routes:
  arbitrary definition siblings, exact retail definition/object names redirected to
  mod-owned bins, and exact retail transform-bin overrides. All parsed silently and none
  rendered a tree. The bounded blocker is recorded; no Earth transform was re-enabled.
- The physical source lattice is now 4096×2048 rather than 1024×512, reducing engine-raster
  shoreline steps from 16 to four pixels. The production world now contains 12,104
  locations: 11,200 passable land, 520 impassable mountain, 64 lake, and 320 sea zones.
- The finer world regenerates end-to-end with all 42 anchors, 38 realms, 33 cultures,
  11,179 populated locations, 604 unique legal ports, 12 markets, and 524 recalculated
  authored road edges. Generated-key route waypoints were replaced by stable Tharbad and
  Fields of Nurn anchors.
- The High Pass was widened and recentered around Goblin-town after the first finer-world
  validation correctly found the hold isolated inside the Misty Mountain barrier. Full
  validation is green, including realm connectivity and zero Earth decal layers.
- The first 4096×2048 paired smoke correctly rejected 14 passable pockets isolated inside
  ridge masks plus one generated localization hash collision. Anchor access carving,
  enclosed-pocket cleanup, all-land port-component validation, and a collision-safe key
  eliminated both engine-only defect classes. The regenerated world has a minimum
  47-control-cell location and 605 legal ports.
- Paired smoke then passed with zero mod-unique lines, with the final census-compatible
  tree confirmed on fingerprint `ad12be19`. A fresh
  non-debug Observer loaded and advanced to 3018.1.2. Tilted 3D evidence proves that the
  authored mountain systems have physical relief, but it also proves that terrain
  materials still break into coarse location-shaped patches and that trees and major
  rivers remain absent. Reopened M2 remains red.
- The live Observer initialization found two grassland locations assigned lumber because
  the census used their forest seed pixel while the terrain template used their dominant
  biome. Raw materials now use the same dominant-biome contract; both locations resolve
  to wheat and static validation forbids lumber outside woods/forest.
- Installed terrain-cache evidence has now replaced the 114-byte placeholder material
  payload with a fully Arda-authored 16-bit material-mask cache. The 8192x4096 continuous
  source paints coast/topography, shore/water, biome/climate, elevation variation, and
  all 23 river controls independently of political-location polygons.
- The final cache contains 174,763 indexed tiles, 89,777 unique height tiles, 95,028
  unique material tiles, a 55,986,036-byte `materials.bin`, and zero Earth index/intensity
  decals. Generator checks reject placeholder coverage, wrong provenance, low tile
  diversity, oversized payloads, or a missing material preview.
- Natural paths now use six spatial-frequency bands, and Rhûn, Núrnen, Evendim, and Long
  Lake have hand-authored irregular shore outlines. The regenerated world remains 12,104
  locations with 11,200 passable land, 520 mountains, 64 lakes, 320 sea zones, 630 legal
  ports, and 11,179 populated locations.
- The enlarged Sea of Rhûn exposed an honest static defect: Burh Gath's old point had
  fallen into water. Moving the invented seat to its eastern shore reduced its snap to
  0.000377 and the global capital maximum to 0.018362 without weakening the validator.
- Full validation passed. Paired vanilla/mod smoke passed with zero mod-unique lines on
  fingerprint `f004fab1`. An earlier non-debug 3D session proved the material cache
  renders continuous ground variation, snow/rock mountain material, and shore
  transitions; the final refined state did not complete a stable close-zoom capture
  after two resource-bound UI attempts, so the reopened M2 visual gate remains red.
- The map extent now follows the plan's border rule: Rhûn continues through the east
  edge and Harad through the south edge instead of enclosing north-western Middle-earth
  in a false ocean ring. The western seas, Icebay, Gulf of Lune, Bay of Belfalas, and
  Ethir Anduin remain physical coasts; the authored land fraction is 0.701271.
- Sea tessellation dropped from 320 to 200 after the smaller true-ocean footprint made
  two zones compete for one legal coastal land zone. The 120 recovered cells were added
  to land, preserving exactly 12,104 locations while raising passable granularity to
  11,320. The regenerated world has 495 unique ports, 11,299 populated locations, and a
  maximum capital snap of 0.017499.
- The denser continental cache contains 116,189 unique height tiles in 88,822,519 bytes
  and 124,679 unique material tiles in 73,573,766 bytes. Both remain below the repository
  ceiling; all 174,763 virtual entries and zero Earth decal layers remain validated.
- The first paired smoke exposed one changed-hierarchy localization hash collision with
  installed `indian_southcurrent23`. A deterministic `_arda` area-key remap removed it;
  the confirming paired smoke passed with zero mod-unique lines on fingerprint
  `ad2b237d`.
- A fresh current-tree debug checkpoint now separates country selection from the heavy
  renderer. Reopening that 41 MB save with no debug mode and the full visual profile
  reached live Observer in 122 seconds at about 5.6 GB working memory. The selected 3D
  Map proved that the current Arda height/material cache renders physical relief,
  continuous ground variation, and non-Earth waters. It also honestly confirmed broad
  pale mountain tubes, weak rivers, and no visible tree objects; reopened M2 stayed red.
- Installed transform evidence exposed a format-level difference missed by the earlier
  vegetation path tests. Retail forest records are spatially coherent (about 27 world
  units between consecutive records and about 84 units across a typical 32-record
  batch), while randomized ENDÓRË batches spanned roughly 5,700 units. The generator now
  Hilbert-orders each mesh/LOD bin and validates locality; representative high-forest
  output measures 9.7-unit consecutive and 102.5-unit 32-record medians without copying
  an Earth transform.
- Mountain topography now begins at the high massif core (`ridge > 0.45`) instead of the
  broad physical shoulder (`ridge > 0.29`). Broad authored foothill elevation remains,
  while mountain-template coverage drops from 8.81% to 4.65% of land to eliminate the
  continuous snow-tube appearance.
- Player-facing river material now follows the same deterministic organic paths and
  corrected source/mouth extensions as the engine graph. Its downstream-tapered width
  increases from 0.90× to 1.45× the authored control, with a five-pixel material floor,
  so major channels remain legible outside the one-pixel parser graph.
- The complete downstream world regenerated after those physical changes: 12,104
  locations, 38 realms, 33 cultures, 11,299 populated locations, 467 recalculated ports,
  320 recalculated authored road edges, and 12 markets. Deterministic M2 verification
  passed all stages, including 174,763 cache entries, 124,680 unique material tiles, and
  zero Earth decal layers. Smoke and the new close-zoom vegetation/river capture are
  deferred only while Antiquitas owns the shared EU5 lease; no gate is claimed yet.
- The Hilbert-ordered transform route is now live-proven rather than merely static:
  a no-debug, full-3D Observer rendered physical tree objects and dense woodland canopy
  over Mirkwood. Direct `WM_MOUSEWHEEL` delivery also moved the camera deterministically
  from regional view to ground-level terrain after the former synthesized-wheel and
  numpad-binding routes had no effect.
- That close capture honestly exposed the next quality defect: forest coverage ended in
  hard walls and the snow/rock mountain material remained too continuous. Forest controls
  now use deterministic porous margins and internal glades, object placement uses a
  continuous noise-modulated edge field, and terrain transition paint follows the
  dominant biome actually assigned to each gameplay location as well as the source atlas.
  Mountain classification now begins at `ridge > 0.56`, while broad physical foothill
  elevation remains modulated by independent rock-mass fields.
- Rhûn and Núrnen received asymmetric multi-headland shoreline controls, and coast/lake
  sub-macro displacement increased without changing the full-canvas border contract.
  The coherent downstream rebuild remains 12,104 locations with 11,320 passable land,
  520 mountain, 64 lake, and 200 sea zones; 488 ports, 313 authored route edges, 38
  realms, 33 cultures, 11,299 populated locations, and 12 markets were recalculated.
  Independent M2 verification passed 174,763 indexed cache tiles, 115,834 unique height
  tiles, 124,315 unique material tiles, and zero Earth decal layers. Exact-state visual
  proof and smoke are pending the shared EU5 lease; reopened M2 remains red.
- A fresh current-tree game replaced the stale visual checkpoint and entered Observer
  with no disconnected-path diagnostics. Its no-debug full-3D relaunch proved markedly
  better mountain relief: continuous white tubes are gone, with exposed brown massif
  shoulders and isolated snow/rock cores. Direct-window zoom then proved dense base
  canopy and a visible dark channel in Mirkwood, but physical tree clusters remained too
  sparse and the proposed location-biome transition paint visibly emphasized pale
  Voronoi patches. The renderer evidence rejected that transition route; M2 stays red.
- Installed bins contain about 10.2 million vegetation transforms across the same
  forest/woods/pine meshes and three LODs, versus 420,000 in the proof batch. The next
  exact-state iteration therefore matches those installed per-family/LOD counts with
  wholly Arda-generated, Hilbert-ordered positions. Glades now suppress object placement
  only, so they cannot flip an entire generated location's base vegetation.
- The exact-state vanilla-density probe succeeded under the full renderer at the same
  roughly 5.7 GB working-memory scale as the proof batch. Maximum close zoom over
  Mirkwood now shows continuous physical mixed canopy and small irregular clearings,
  rather than sparse clusters over a flat forest template. This is the first live proof
  that ENDÓRË can match vanilla vegetation density with no Earth-authored transform.
- Dense canopy also hid the player-facing river material. All three vegetation families
  now exclude a narrow dilation of the 23 authored river controls before sampling; the
  complete 10,193,212-transform set regenerated and retained its Hilbert locality.
  A no-debug maximum-close renderer pass then proved both the clearance and continuous
  mixed canopy: the wet corridor and banks remain legible without returning any
  Earth-authored transform.
- That same close pass exposed a final engine-raster defect: parser-safe major channels
  still rendered as constant-width canals because every pixel used one palette width and
  sparse authored vertices were joined by straight orthogonal runs. Installed-raster
  analysis proved vanilla widens rivers downstream through indices 4, 5, 11, and 15.
- The replacement raster keeps the already-proven 12 independent major-channel topology
  but naturalizes each centerline between authored vertices, extends every southern mouth
  to the current coast, and varies width downstream. A new graph validator rejects any
  duplicate pixel, diagonal gap, self-touch, inter-channel touch, or non-water mouth.
  The matching player-facing material uses the same deterministic centerline phase.
- The exact current tree loaded into no-debug full 3D Observer on fingerprint `5782310a`
  with no river-source, affluent, self-touch, disconnected-path, or other mod-caused
  error. Ground-level evidence shows an irregular wet corridor through vanilla-density
  woodland rather than the former straight blue ribbon. Required multi-theatre evidence,
  and explicit owner acceptance remain outstanding; M2 stays red.
- Full deterministic validation passed in 243.4 seconds, including 174,763 terrain-cache
  tiles, all 12 naturalized major channels, all 10,193,212 vegetation transforms, and
  every downstream world subsystem. Paired vanilla/mod smoke then passed with zero
  mod-unique error lines on exact game-visible fingerprint `09192b66`.
- The v14 exact-tree close audit confirmed that the new ridged height detail and
  altitude-aware material selection coexist with dense green Mirkwood canopy. Fangorn,
  however, rendered fully snow-white on 4 August. Its location center is y=4984 on the
  8192-pixel map, while the generated equator was incorrectly at y=4600; the engine
  therefore treated Rohan and every southern theatre as southern-hemisphere winter.
  `gen_map_config.py` now places the equator beyond the southern edge and fails if it can
  intersect the canvas. Live proof awaits the next shared EU5 lease; M2 remains red.
- Named-forest transform QA confirms roughly 138,000 high-detail trees in Fangorn,
  113,000 in the Old Forest, 67,000 in Lórien, and 115,000 in Ithilien. These four
  theatres now have explicit minimum-coverage checks in `gen_map_objects.py`, preventing
  a future global-count pass from concealing a regional vegetation regression.
- The location topology now matches the installed vanilla world exactly at 28,490
  locations: 22,000 passable land, 6,000 mountain, 90 lake, and 400 sea cells on the
  unchanged native 16384×8192 canvas. Median mountain area is 37 control pixels instead
  of the rejected 497-pixel close probe, giving crest systems roughly thirteen times
  finer political/topography granularity.
- Full-precision height cache output is restored (`height_quantum = 1`) and tracked
  through Git LFS; its 174,763-entry payload retains 123,963 unique height tiles and zero
  Earth decal layers. Terrain-cache generator v18 reuses that verified height source but
  corrects the installed `mountain_wasteland` material order: high crests are snow
  (slot 10), middle elevations rock (slot 11), and only low shoulders use dark dirt
  (slot 12), with continuous altitude/noise blending rather than location boundaries.
- A first native-density no-debug load reached the country-selection transition but lost
  automation foreground before evidence capture. Its live initialization honestly
  exposed lumber potential errors, an unowned Henneth Annûn town setup, and discriminated
  Black Númenórean nobles in Umbar. The generators now exclude lumber while templates
  remain neutral, pin occupied Ithilien/Shadow landmarks before the wilderness mask, and
  declare Black Númenórean accepted in Umbar. Permanent validation rejects wild urban
  setups and any remaining lumber assignment.
- The complete repaired 28,490-location tree passed `gmake validate` in 436.7 seconds:
  all map, cache, river, border, vegetation, locator, quarantine, realm, people, census,
  template, slot-protocol, and lint stages are green. Fresh no-debug evidence and paired
  smoke remain pending the shared EU5 slot; reopened M2 remains red.
- The driver no longer treats logged cache completion as proof of an interactive country-
  selection window. A PID-verified stability wait now rejects the engine's still-hung
  `Loading Savegame — 98%` frame, and topmost PID-bound capture no longer depends on
  Windows granting foreground ownership.
- Those corrected observations showed that both full visual and lightweight q1 launches
  exited at the 98% boundary after setup/cache completion. The authored 65,536×32,768
  source and exact 28,490-location topology remain unchanged; only the derived runtime
  height cache moved to q64. Generator v19 produced 120,118 unique height tiles in
  172,161,411 bytes (0.098% vertical quantum, eight times finer than live-proven q512)
  plus 124,205 unique material tiles in 71,508,004 bytes. Independent cache verification
  passed all 174,763 virtual entries and confirmed zero Earth decal layers. Fresh retail
  proof remains pending the shared EU5 lease; reopened M2 remains red.
- The complete q64 tree then passed `gmake validate` in 419.3 seconds. Every control,
  location, definition, height/cache, river, adjacency, map-config, flatmap, border,
  vegetation, locator, runtime, quarantine, realm, people, census, template, coordination,
  and lint check is green. The only stderr was Pillow's expected native-raster size
  warning.
- Two q64 lightweight-checkpoint launches then proved that cache-size reduction alone is
  insufficient at 28,490 locations. Both reached healthy menus, accepted New Game, and
  completed logged setup/cache work, but never left the nonresponsive 98% frame during
  the full 600-second post-cache bound. Working set oscillated from roughly 14 to
  23.5 GB and the second run briefly left under 0.5 GB free physical memory. Both were
  stopped through their tokenized driver session and added no mod-unique diagnostic.
- The owner authorized approximately half vanilla's location count while making map
  precision and lore accuracy non-negotiable. Arda Maps' Third Age TopoJSON and
  ArdaCraft's biome/path layers were fetched only into
  `G:\endore_runtime\cartography_references` for analysis. The first 35-landmark cross-
  check confirms that the current atlas requires systemic reprojection—not isolated
  nudges—especially its north/south spacing. The next production target is 14,245
  locations on the unchanged full-resolution physical terrain.
- The systemic source-frame rewrite is now complete statically. ENDÓRË preserves the
  ArdaCraft equal-scale world grid on the 2:1 EU5 canvas rather than stretching
  Middle-earth horizontally. Arda Maps contributes a 1,251-vertex mainland coast, 15
  lake outlines, 43 mountain footprints, 24 river/valley controls, and source forest
  geometry. The committed conformance report covers 42 anchors and 62 additional
  landmarks; all 38 realm seats are mechanically synchronized to those controls.
- The old 28,490-location runtime tree has been replaced with exactly 14,245 locations:
  10,800 passable land, 3,200 mountain, 65 lake, and 180 sea. All 42 anchors survive,
  median control area is 294 pixels, and the model fingerprint is `632c9cf5ab6b`.
- The complete downstream tree now matches that topology: 24 regions, 38 realms, 33
  cultures, 10 languages, 10 faiths, 10,779 populated locations, 12 markets, 14,245
  terrain templates, 470 ports, and 50 locator/quarantine outputs. The corrected Rhûn
  seats now resolve within 0.0161 physical normalized distance at worst, and its three
  eastern realms own 826, 682, and 196 locations instead of leaving the eastern seat in
  the ocean.
- A fresh 65,536×32,768 q64 virtual cache was baked from the new Arda relief/material
  sources: 174,763 indexed tiles, 80,225 unique height tiles, 83,142 unique material
  tiles, 246.5 MB total, and zero inherited Earth decal layers. The corresponding
  8,192×4,096 height source, flatmap, parser-safe major rivers, borders, and 10,193,212
  Arda-native vegetation transforms are regenerated. Static validation and fresh
  lightweight/full-renderer evidence remain pending; reopened M2 stays red.
- The first full validation correctly rejected two sub-pixel water cells absorbed into a
  Lindon land location, Gundabad's isolated massif cell, stale old-projection forest
  coverage floors, a mixed-Python height render, and stale localization ordering. The
  corrected generator preserves every source-coast water pocket, adds an authored
  Gundabad gate, distinguishes Chetwood from the Old Forest, preserves narrow forest
  interiors during edge feathering, and runs every write under the validation
  environment. Targeted height, vegetation, realm connectivity, and definition checks
  are now green; full validation still must be repeated.
- The next full gate cleared every physical, cache, vegetation, connectivity, realm,
  people, and template stage, then found one downstream setup invariant: Harlond of
  Gondor retained its canon port rank while broad emptied-Ithilien logic left it wild.
  Harlond is now pinned to Gondor with Cair Andros and Henneth Annûn; the full
  realm/people/census/localization/template chain is regenerated. Full validation remains
  pending and M2 remains red.
- The corrected source-frame tree then passed the complete static gate in 327.3 seconds,
  including cartographic conformance, all 14,245 definitions, the 174,763-tile q64 cache,
  10,193,212 Arda-native vegetation transforms, all realm/people/census/template stages,
  and lint. Paired vanilla/mod smoke subsequently passed with zero mod-unique error lines
  on exact game-visible fingerprint `dbd52c52`.
- Real-game proof did not pass. A no-debug full-visual New Game and a separate lightweight
  checkpoint New Game both completed setup serialization and cached-data recalculation,
  then remained noninteractive for the full 600-second post-cache bound. Both peaked near
  23.5 GB without emitting a map, terrain, river, locator, setup, or renderer diagnostic.
  Their evidence is under the two `20260731_m2_sourceframe*` screenshot sessions, and the
  bounded failure is recorded in `BLOCKERS.md`.
- The runtime tessellation is therefore being reduced to the last live-proven 12,104-cell
  aggregate: 9,200 land, 2,700 mountain, 60 lake, and 144 sea locations. The equal-scale
  projection, source-derived coast/lakes/ridges/rivers/forests, full-resolution physical
  source, 42 anchors, 62 landmarks, and 38 realm seats remain unchanged. This is a
  renderer-capacity adjustment, not a cartographic simplification; reopened M2 stays red.
- The 12,104-cell replacement regenerated coherently with 415 ports, 9,179 populated
  locations, 311 authored route edges, 38 realms, and 12,104 terrain templates. Full
  validation passed in 315.3 seconds and paired smoke passed with zero mod-unique lines
  on fingerprint `152d7798`.
- Fresh-game interactivity still failed under both no-debug lightweight and debug
  checkpoint profiles. Each completed setup/cache work, remained nonresponsive for the
  full 600-second post-cache bound, and peaked near 23.5 GB without a map diagnostic.
  Location reduction is therefore not the dominant constraint and will not continue.
- The next renderer candidate keeps all 12,104 locations and full source geography while
  scaling each installed vegetation family/LOD count to 40%: 4,077,285 transforms, still
  about ten times the rejected 420,000 proof. Named-forest high-detail floors and Hilbert
  locality remain mandatory. Reopened M2 stays red pending real-game proof.
- A naive global 40% placement failed the permanent regional floors; the generator now
  reallocates a small fixed share of high-LOD samples into the source-defined Fangorn,
  Old Forest, Lórien, and Ithilien masks without increasing the 4,077,285 total. The
  stratified set passes all density, theatre, river-clearance, filename, and locality
  checks and occupies 163.1 MB instead of 407.7 MB.
- Full validation passed in 351 seconds and paired smoke passed with zero mod-unique lines
  on fingerprint `8b088c92`, but the materially smaller object payload still missed the
  debug checkpoint's 600-second interactivity bound and reached roughly 22 GB. Object
  density contributes but is not the dominant constraint.
- The next static candidate keeps the exact 12,104 total and every physical control, but
  rebalances the unproven 2,700 impassable mountain locations to 1,200 while raising land
  cells from 9,200 to 10,700. The last live source tree used only 520 mountain cells;
  1,200 retains more than twice that strategic granularity without weakening any ridge,
  height, massif, or pass geometry. M2 remains red.
- The rebalanced source-frame tree regenerated coherently: 10,700 land, 1,200 mountain,
  60 lake, and 144 sea locations; after the source-peak control refresh it resolves to
  456 ports, 38 realms, 10,679 populated locations, 361 authored route edges, and 12,104
  final terrain templates. All 42 anchors and the full source projection remain
  unchanged.
- Full validation passed in 313.9 seconds, including every cartography, connectivity,
  cache, river, border, vegetation, locator, quarantine, realm, people, census, template,
  and lint stage. Paired vanilla/mod smoke then passed with zero mod-unique lines on
  fingerprint `66f1cd73`.
- The next debug-checkpoint attempt deferred immediately and safely because Antiquitas
  acquired the shared EU5 lease for its own paired smoke. No ENDÓRË process launched and
  no blocker was counted. The static/smoke-green candidate awaits the next free lease;
  reopened M2 and the nine-theatre visual gate remain red.
- The post-push audit exposed a false stale-smoke result: fingerprint v1 mixed `HEAD` with
  dirty paths, so committing identical bytes changed the fingerprint, and the q64 LFS
  pointer amplified the mismatch. Fingerprint v2 hashes the actual game-visible working
  bytes independent of dirty/staged/committed state. Its synthetic repository test proves
  byte changes invalidate the hash while stage+commit do not; the full current tree hashes
  deterministically in about 1.7 seconds.
- The 10,700-land / 1,200-mountain candidate resolved the fresh-game envelope. A debug
  New Game completed both cache stages, reached interactive country selection, enabled
  Observer, entered the live HUD, and advanced without interruption through 3018.2.04.
  The only apparent failure was a gamedriver false negative: this debug path omitted the
  centered red pause banner even though the fixed top-left Observer HUD was present.
- The driver now accepts that release-layout Observer HUD as an independent bounded
  transition signal. An immediate repeat passed, and a cold non-debug `--visual-map`
  New Game then independently reached live Observer on fingerprint `c39cae70` (the v2
  byte-stable hash). Neither run added a map, terrain, river, locator, setup, or renderer
  diagnostic.
- The non-debug full-map tactical view confirms that the active world is the Arda-derived
  coastline, water, ridge, and river footprint rather than vanilla Earth. It is still a
  flat diagnostic overlay, not physical-map acceptance evidence. Deterministic selection
  of the unoverlaid terrain view and all nine full/regional/close theatre captures remain
  blocking; reopened M2 stays red.
- Deterministic named-location targeting now centers exact ASCII keys through the live
  location finder, replacing error-prone free-camera theatre selection. The first
  correctly targeted nine-theatre audit proves that continuous Arda vegetation and
  materials render, but keeps M2 red: the Shire's smallest pool is a cell-shaped bowl,
  Belfalas still has an over-rounded internal inlet, and Misty/White Mountain cores read
  as broad grey plateaus rather than peak systems.
- Every dry location now resolves through the unique `me_arda_surface` rendering adapter
  and one 16-channel ENDÓRË material array. Fresh no-debug close views prove continuous
  Harad sand, Mordor ash/rock, Mirkwood canopy, and Rhûn/Dorwinion ground variation
  without the previous climate/vegetation Voronoi islands. Mount Doom is now an
  asymmetric physical cone with a crater. These are accepted component improvements,
  not acceptance of the full theatre.
- Two bounded small-lake repairs were rejected and reverted: neutral flatland rendering
  did not change the Hobbiton bowl, and a bed raised to 5,146 removed its water but left
  the bowl. The exact source outline remains in the control atlas; `BLOCKERS.md` records
  the alternate-representation requirement.
- The mountain diagnosis rejected both narrow high-amplitude peak ellipses and neutral
  topography substitution because neither changed the live grey plateaus. The underlying
  cause was the height model lifting nearly every Arda Maps mountain-polygon interior to
  crest altitude. A new deterministic candidate preserves all 43 source footprints as
  low foothill envelopes, makes the nine audited ridge axes carry the high relief, and
  turns all 10 passes into saddles. Its 174,763-entry q64 cache passes targeted static
  checks with 80,219 unique height tiles, 64,067 unique material tiles, 220.1 MB total,
  and zero Earth decals. Fresh no-debug mountain evidence is next when the shared EU5
  lease clears; M2 remains red.
- The retained mountain route now pins 18 named Arda Maps summits and all 10 source or
  reconciled passes in the projection audit. Fresh exact-tree Observer views prove that
  Khazad-dûm, Dunharrow, and Goblin-town have physical sloped massifs and that Orodruin
  retains its asymmetric cratered cone. A slope-aware material rebuild reduced exposed
  rock from 153,379 altitude-selected pixels to 62,684 steep highland pixels and reduced
  snow from 33,893 to a 3,970-pixel steep-crest core. It removes the former continuous
  grey polygon plates, but close views still reject coarse rock ribbons/islands and the
  current political-cell scale. This is a retained component improvement only; the
  nine-theatre gate and M2 remain red.
- The first paired smoke on the coherent source-peak tree reached healthy vanilla and
  mod menus, then correctly rejected five integration lines: missing UTF-8 BOMs on the
  new climate/biome files, missing renderer-climate localization, one generated Khand
  province localization hash collision, and a duplicate continental climate color.
  The source files/generator now own all four repairs: verified BOM encoding, bespoke
  climate text, unique color, and deterministic Khand area-stem remapping. Revalidation
  and paired smoke remain mandatory before commit.
- Post-fix full validation passed in 330.4 seconds. Paired vanilla/mod smoke then passed
  on exact runtime-byte fingerprint `07682616689a4d271b2cd3c08de4de4af3020a92b7f484a520225ec0bdcbd763`
  with zero new error lines and zero mod-unique diagnostics. This greens the component
  batch's integration contract only; close-zoom material feathering, the other physical
  defects, the nine-theatre audit, and explicit owner acceptance keep M2 red.
- A source-ridge feathered material candidate was statically valid but missed the
  600-second post-cache interactivity bound twice on identical fingerprint `0f65a5e5`,
  including a repeat begun with 23 GB free RAM. It emitted no map/material diagnostic,
  was logged in `BLOCKERS.md`, and was fully reverted. The working runtime is byte-exact
  to the pushed/smoked v25 cache.
- The scale audit measures a 70.29%-wide by 100%-high land bounding box with land already
  touching both vertical crop edges. Uniform enlargement would clip binding north/south
  geography, so the equal-scale projection is retained. Belfalas likewise remains on
  its hash-pinned source ring: 2,043 raw vertices cover the audited window and the
  committed simplification is already sub-location-pixel precise.
- The first alternate small-water representation is now generated coherently. The three
  exact Arda Maps pools east of Hobbiton remain lake-biome polygons but no longer cut
  engine water or depress their host terrain; wet pond and feathered transition material
  carry their visible identity. The full 12,104-location world and generator-v27 cache
  rebuilt successfully, and targeted control/cache/reference checks pass. Its live
  Hobbiton close probe deferred without launch because Antiquitas owned the shared slot.
- Cartographic validation now hash-pins the complete reviewed projection geometry in
  addition to its feature counts and landmark tolerances. Any future movement of a coast,
  island, lake, mountain, summit, pass, woodland, river, or density envelope must be an
  explicit source-review event rather than an unnoticed generator drift.
- A fresh in-memory rebuild against the quarantined, hash-verified Arda Maps payload
  reproduced the committed projection exactly: 1,251 mainland vertices, 15 lakes, 43
  mountain footprints, 18 named peaks, all 15 named forests, and 24 rivers with 814
  retained vertices. This verifies source reproducibility without copying the raw map
  payload into the repository.
- The first actual v27 decorative-pond New Game completed setup/cache work but remained
  noninteractive through the 600-second country-selection bound, with no map, cache,
  material, river, or locator diagnostic. This is one runtime strike, not a visual
  rejection. Two later attempts correctly deferred before launching when Antiquitas
  reacquired the shared EU5 slot; neither consumes the one remaining cached repeat.
- The Harnen no longer uses an eight-point manual diagonal. An unnamed 216-vertex Arda
  Maps channel in the exact Harnen corridor now supplies 49 retained bends, followed by
  only two reconciled points to its source-coast mouth. The obsolete farther-west mouth
  was rejected after the native river gate proved that it crossed sea and re-entered
  land. The coherent 12,104-location world rebuilt with 814 total river vertices, 79,924
  unique height tiles, 63,584 material tiles, and a parser-green indexed river raster.
