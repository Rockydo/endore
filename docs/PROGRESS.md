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
- The first alternate small-water representation generated coherently but failed its
  runtime gate. The three exact Arda Maps pools east of Hobbiton were tested as
  lake-biome polygons over continuous dry terrain with wet pond and transition material.
  Both permitted fresh New Games completed setup/cache work and then missed the
  600-second post-cache interactivity bound without a diagnostic. Generator v27 is
  rejected and removed; the runtime returns to the v25 engine-water baseline.
- Cartographic validation now hash-pins the complete reviewed projection geometry in
  addition to its feature counts and landmark tolerances. Any future movement of a coast,
  island, lake, mountain, summit, pass, woodland, river, or density envelope must be an
  explicit source-review event rather than an unnoticed generator drift.
- A fresh in-memory rebuild against the quarantined, hash-verified Arda Maps payload
  reproduced the committed projection exactly: 1,251 mainland vertices, 15 lakes, 43
  mountain footprints, 18 named peaks, all 15 named forests, and 24 rivers with 816
  retained vertices. This verifies source reproducibility without copying the raw map
  payload into the repository.
- The final cached v27 decorative-pond repeat independently completed menu and
  setup/cache transition but remained nonresponsive for 600 seconds and shut down
  cleanly. Together with the first actual attempt this exhausts the route's two-strike
  allowance. The intervening Antiquitas lock deferrals never launched EU5 and remain
  correctly excluded from the strike count. No renderer verdict exists for v27.
- The Harnen no longer uses an eight-point manual diagonal. An unnamed 216-vertex Arda
  Maps channel in the exact Harnen corridor now supplies 49 retained bends, followed by
  only two reconciled points to its source-coast mouth. The obsolete farther-west mouth
  was rejected after the native river gate proved that it crossed sea and re-entered
  land. The formerly four-point Morgulduin now follows the matching unnamed 40-vertex
  source channel as well. The coherent 12,104-location world rebuilt with 816 total river
  vertices, 79,924 unique height tiles, 63,583 material tiles, and a parser-green indexed
  river raster.
- After v27's second runtime strike, the complete world was regenerated with v25
  engine-water and material semantics while retaining the source-pinned projection,
  Harnen, Morgulduin, equal-scale safeguards, and all 24 source-derived river axes. The
  clean restoration produced the same 12,104-location topology, 79,924 unique height
  tiles, 63,583 unique material tiles, and zero Earth-authored map objects or decals.
- The first validation after restoration correctly caught pond-era generated controls
  that `m2_world --write` consumes but does not author. No mixed tree was accepted:
  `m2_controls.py --write` regenerated the binding water masks first, then a second full
  world build regenerated every downstream asset. Repository-wide validation passed on
  that consistent tree. Paired vanilla/mod smoke then passed on exact game-visible
  fingerprint `b838a130d24989fdf86d77212f3b5cf4e21fc66fa2553091eb55b84572e4a64d`
  with zero new error lines and zero mod-unique diagnostics. This greens the source-river
  integration and v25 restoration batch only; M2 remains red pending physical-map visual
  acceptance.
- Two subsequent deep Observer attempts on that exact restored fingerprint still missed
  the 600-second map-transition bound, so `b838a130` is now a two-strike blocker and may
  not be launched again. The first attempt exposed an actionable contract gap absent from
  menu smoke: `endore_dynamic_land_biome` had no entry in EU5's independent
  `gfx/city_materials` registry. The material generator now authors a separate
  `99_endore.txt` entry inheriting the installed `default_biome` road/decal stack, and its
  checker requires the exact mapping before another materially different runtime test.
- The first generated city-material file used plain UTF-8; paired smoke correctly
  rejected EU5's BOM warning. The generator now emits and verifies UTF-8 BOM. Full
  validation and paired smoke passed on corrected fingerprint `be6864eb` with zero new
  or mod-unique diagnostics, and the former missing-city-material line no longer appears
  during map transition. Two fresh Observer attempts still timed out after setup/cache
  with roughly 24 GB free RAM, so that fingerprint is blocked after two strikes. Retain
  the clean registry fix, but do not claim that it resolved the independent deep-load
  failure or greens M2.
- A controlled worktree A/B then combined commit `789d2d1`'s last live-proven v25
  terrain/cache/river/flatmap/vegetation bytes with only the corrected city-material
  registry. One Chrome foreground-lock run never entered the transition and was
  discarded. Two subsequent PID-verified runs both completed setup/cache and timed out
  at country selection on fingerprint `86972304`. This disproves the current
  source-backed Harnen/Morgulduin raster, its local height/material changes, flatmap, or
  12 cleared woods bins as the distinguishing cause. The source river integration stays;
  the temporary worktree was removed after its evidence was copied into `docs/screens`.
- The shared ENDÓRË user directory still held 2.88 GB of derived July renderer state,
  including a 350 MB navmesh created before the current Arda map. `gfx` and
  `shadercache` were moved recoverably to
  `G:\endore_runtime\quarantine\20260731_pre_fresh_map_cache`. A cold run regenerated
  333 MB of shaders and a fresh 128 MB Arda flatmap but did not finish transition state 4
  within 600 seconds; a warm repeat completed setup/cache and then missed the post-cache
  bound. The stale navmesh was neither restored nor regenerated. This fresh-cache route
  is exhausted after two strikes; renderer evidence moves to the compatible saved
  Observer route while fresh country selection stays red.
- Corrected automation proved that build 24187685 starts MainMenu-to-Game during menu
  initialization and a single New Game click can join that active transaction. The
  driver now parses the latest transition state, requires state 4 plus cache completion,
  and distinguishes the actual country-selection top bar from responsive menu/loading
  frames. Its regression test is part of `make validate`. Repository text is also pinned
  to LF so fresh worktrees cannot silently differ under global `core.autocrlf=true`.
- A final controlled run on the 12,104-location tree issued exactly one valid click,
  completed setup and all cache recalculations, then remained nonresponsive for the full
  900-second country-frame bound at 32.42 GB private memory. Together with the exact-byte
  A/B, this identifies an unreliable renderer memory envelope rather than a river,
  terrain-cache, city-material, or launcher regression.
- The runtime-only topology was reduced to 6,004 cells (5,200 land, 600 mountain, 60
  lake, 144 sea) and 2,038,645 vegetation transforms. The full source projection,
  coastlines, 8192x4096 heightfield, q64 cache, 43 mountain footprints, 24 rivers, 15
  forests, 18 peaks, and 10 passes did not change. All 38 realms, 5,179 populated
  locations, 283 ports, and canonical-forest density floors remain coherent. Forochel
  Camp, an invented seasonal seat, was moved from an offshore judgment point to the
  nearest unchanged source coastline.
- Full validation passed in 286.8 seconds. Paired vanilla/mod smoke passed on fingerprint
  `f0cff53ee8fafc337e0fa4b6c634a8447e2dbfc135490e1ccafaa6f183fafc8e` with zero new
  lines and zero mod-unique diagnostics. A fresh full-visual New Game then reached an
  actual country-selection frame and live Observer in 135 seconds at roughly 8.62 GB
  private memory; an in-game speed-control test advanced from 3018.1.1 to 3018.1.7.
  Evidence: `docs/screens/20260731_runtime_budget_6004/`. Fresh start-game loading is
  green again; M2 remains red only for the required physical-map visual acceptance.
- The first refinement on the release-safe 6,004-location tree separates movement
  topology from renderer presentation. All 600 mountain cells remain listed under
  `impassable_mountains`, but now use the same neutral surface template as ordinary land;
  continuous q64 height and material controls alone paint the ranges. The three exact
  Arda Maps pools east of Hobbiton remain 43 source-control pixels at height
  12,422–12,445, but use wet material over physical land instead of converting whole
  runtime cells into engine water. The other 12 source lakes retain true water.
- Validation passed with 174,763 Arda-owned cache tiles and zero Earth decals/transforms.
  Paired smoke passed on fingerprint
  `e9d3a5f08c529fdede1e9f2d0a6bb4f55b0bd90c38da0c011832d0261f13693b` with zero
  new lines and no mod-unique diagnostics. A fresh non-debug full-visual New Game reached
  country selection and live Observer in 115 seconds, then advanced through 3018.1.10.
  Evidence under `docs/screens/20260731_m2_neutral_mountains_ponds/` proves that the giant
  grey/white mountain-location slabs and Hobbiton water quarries are gone. It also keeps
  M2 honestly red: exposed rock remains patchy/geometric at regional zoom, several ranges
  need stronger physical readability, and the full nine-theatre refresh is outstanding.

- Generator v28 replaces hard altitude/slope rock cuts with a continuous material field
  derived from all nine source ridge axes, their branches, all 18 named peaks, smoothed
  physical slope, altitude, and deterministic organic noise. The heightfield, passes,
  600-cell impassability topology, q64 cache budget, and source geometry remain unchanged.
  Fresh Khazad-dum evidence shows a more coherent crest-following massif rather than the
  former disconnected grey islands, but M2 remains red pending softer material fringes
  and the full nine-theatre review.
- The lake policy is now systematic at the release-safe political scale. Exactly ten
  source lakes occupy at most 64 pixels each in the 4096x2048 atlas (189 pixels total):
  Mirrormere and minor lakes 04-07/10-14 remain exact wet-material polygons over physical
  land. Long Lake, Lake Evendim, Nen Hithoel, Nurnen, and Rhun remain engine water. The
  complete world regenerated coherently at 6,004 locations and 2,038,645 Arda-native
  vegetation transforms; fresh Mirrormere evidence proves the deep host-cell quarry is
  gone, while the replacement surface still needs later scenery polish.
- The apparent fresh-start failure was an automation false positive, not a map-load
  regression. Country-selection political paint could satisfy the centered red-banner
  heuristic before Observer started. The driver now requires the independent top-left
  Observer HUD for both live-state and pause actions, with regression coverage for a red
  lobby frame. Full validation passed in 285.3 seconds; paired smoke passed on exact
  game-visible fingerprint
  `8ca808d78c535292a60f2439130797c6e28514a3e063310253e2ca703369b0a4`
  with zero new and zero mod-unique lines. Two cold full-visual New Games independently
  reached HUD-proven live Observer in 115-117 seconds. The corrected monitor resumed the
  second game exactly once, advanced from 3018.1.1 to 3018.1.15 in 45 seconds, and the
  location-focus evidence continued to 3018.2.1 without error-log growth. Evidence:
  `docs/m2/LOAD_PROOF_20260731.md` and
  `docs/screens/20260731_m2_loadproof_v28_tick/`.

- Source-terrain v29 imports 190 renderable Arda Maps highland footprints (10,805
  simplified vertices) and all eight moor footprints (369 vertices). The new highlands
  provide low continuous relief; the Dead Marshes now use their exact 111-vertex source
  shape; all named forests render above broad climate paint. Mordor's proof-era
  fifteen-point ash oval is replaced by a continuous field bound to source mountain
  footprints 8-11, the Ered Lithui/Ephel Dúath/Mountains of Shadow axes, and Mount Doom.
  Sub-location ponds gain shallow physical bowls, while crest material thresholds and
  Ithilien's fixed-budget high-detail allocation were tightened.
- The complete world remains at 6,004 locations and 2,038,645 Arda-native vegetation
  transforms. Full validation passed in 281.9 seconds. Paired smoke passed in 200.8
  seconds on fingerprint
  `e453742c7d20aaaf3b68567ffb6c98855df41b8b40695bd5899b9100c60e25d4`
  with zero new and zero mod-unique lines. A fresh full-visual world loaded to responsive
  country selection, continued into HUD-proven Observer, resumed exactly once, and
  visibly ticked for 45 seconds. One non-repeating coat-of-arms tooltip line appeared
  before playback and is carried explicitly to the final gate; the error log stayed fixed
  during playback. Evidence: `docs/m2/SOURCE_TERRAIN_PROOF_20260731.md` and
  `docs/screens/20260731_m2_source_terrain_v29/`. M2 remains red for macro-biome cleanup
  and the full nine-theatre physical review.
- The v29 fresh-world command's apparent 600-second load failure was isolated to the
  driver, not the generated world: its first transition stage waited exclusively for two
  debug-log suffix markers even after the responsive country-selection screen existed.
  The transition gate now accepts five stable seconds of the calibrated country-selection
  bar when those markers are unavailable, then reconfirms the same interactive state in
  the existing second gate before sending input. Pure regression coverage rejects state
  4 alone, cache completion without its quiet period, incomplete visual stability, and
  generic quiet logs while accepting both complete-log and stable-country-selection
  proofs.
- A repeat exposed two further automation-only ambiguities without changing the v29 game
  tree: the first Observer click could be consumed foregrounding EU5 and then cascade into
  a map-country selection, while another topmost application could occlude EU5 from a
  desktop-pixel probe. Evidence capture and transition probes now foreground the exact
  tokenized EU5 PID, process exit terminates the wait immediately, and Observer automation
  requires the warning-dialog and start-button signatures before clicking onward.
- Owner visual review accepts the greatly improved coasts provisionally and keeps M2 red
  for inland fidelity: relief must become taller, narrower, and jagged rather than broad
  plateaus; Mordor and northern ranges require exact source review; Erebor must be a lone
  peak; and the river system needs wider trunks plus many more source-derived tributaries.
  A complete Arda Maps/Ardacraft audit follows those fixes, with political assignment and
  blocky Dunland repair deliberately after final physical terrain.
- Terrain candidate v30 replaces sparse high hand-axis relief with a checksum-locked,
  640×513, 4-bit numeric reduction of Ardacraft Heightmap V2. Arda Maps retains the outer
  range envelopes; all 18 named peaks and ten passes remain pinned. The former axes now
  contribute only 18% continuity, residual kernels are narrower, Erebor's generic
  shoulder is smaller, and continuous soft ceilings remove all final-height clipping
  (0 samples at 65535, maximum 63885). Offline previews now reproduce the detailed Grey,
  Misty, White, Ered Luin, and Mordor range branches and keep Erebor visibly isolated.
- The same candidate expands source-backed physical drainage from 24 to 100 controls.
  Seventy-six additional Arda Maps parts—including seventeen omitted named systems—are
  terrain/material-only because the installed affluent parser remains restrictive. Major
  independent trunks now widen earlier through palette indices 4/5/11/15. Control and
  full-resolution height/river outputs regenerated deterministically; real-game smoke and
  nine-theatre close review remain required before acceptance.
- The first non-debug live source-field review entered fresh Observer on fingerprint
  `d033c396de73ab92f67874c6665a2d0f0490418fd2b95b31a09ce4517792a332` with
  paired smoke at zero new lines. It accepted exact branching/placement and an isolated
  Erebor footprint but rejected the 0.82 relief exponent: Gundabad, Morannon, and
  Dunharrow still read as broad high hills. Evidence is retained under
  `docs/screens/20260801_m2_ardacraft_relief_v30/`; it is comparison evidence, not M2
  acceptance.
- The replacement contracts source relief with exponent 1.38, compresses low shoulders,
  lifts upper crests, increases crest-only ruggedness, and gives Erebor a dedicated
  compact isolated-peak profile. Its 8192×4096 height source spans 0–64,323 with zero
  clipped samples. The synchronized 6,004-location / 174,763-tile / 2,038,645-object tree
  regenerated and full validation passed. Paired smoke then correctly deferred without
  launching because Antiquitas held the shared EU5 slot; retry and live comparison remain
  pending rather than failed.
- v31 subsequently passed paired vanilla/mod smoke on exact fingerprint
  `0eac3a5dcaab65613deba6fae82436e1ee7bb465bf9b1faf96131fde5f3acf8f` with zero
  mod-attributable lines and entered fresh live Observer in 126 seconds. The live evidence
  under `docs/screens/20260801_m2_ardacraft_relief_v31/` rejects the profile: Orodruin's
  dedicated cone reads strongly, but the long ranges remain broad hills. The same evidence
  identified two precise control errors: the Gundabad saddle was carved at the canonical
  summit, and Erebor's settlement/control camera lay about 40 final-height pixels from the
  exact Lonely Mountain peak.
- v32 contracts the Ardacraft response from exponent 1.38 to 1.90, replaces the final
  shoulder-amplifying curve with a convex 1.72-power cross-range profile, and reduces the
  low Arda Maps polygon-footprint lift. The Gundabad saddle now occupies the previously
  reviewed north-east approach at `[0.506471, 0.097215]` rather than the summit. Erebor's
  anchor, cartography target, and realm seat now coincide with exact Arda Maps
  `point_mount LonelyMountain` `[0.603783, 0.145042]`.
- The complete v32 world regenerated in 637.3 seconds: 6,004 locations, 600 mountain
  locations, 299 ports, 174,763 terrain tiles, 2,038,645 vegetation transforms, and a
  0–63,678 height field with no clipped samples. Full validation passed in 325.2 seconds,
  including new steep-gradient regression floors. Permanent source-conformance checks
  measure 93.3855% coverage of Ardacraft's strong crest core and 99.5973% source support
  for generated high ridges. Smoke is pending, not failed: Antiquitas
  held the shared EU5 session slot and the coordination layer recorded ENDÓRË fingerprint
  `d749842a575870a209f4abfd45b57990cdd24d09c3396f126c9ebf82f5ee600b` for retry.
- v32 subsequently passed paired vanilla/mod smoke on exact fingerprint `d749842a` with
  zero mod-attributable error lines and entered a fresh HUD-proven Observer in 116.2
  seconds. Live views accepted the broadened Anduin at Caras Galadhon/Osgiliath and
  retained Erebor/Orodruin as materially improved components. The first correctly framed
  Gundabad view still showed the generic size-class summit stamp as an oversized
  mesa-like cap. Later Morannon and Dunharrow captures inherited cumulative close zoom;
  they are retained as camera evidence but explicitly excluded from placement verdicts.
- v33 changes only Gundabad's named-peak overlay: exact Arda Maps point and both underlying
  source ranges remain fixed, while the generic 0.0071 range-sized envelope becomes a
  compact 0.0045 `chain_peak` crown. The projection rebuild and static audit bind that
  profile. The coherent 6,004-location world regenerated in 657.0 seconds with 298 ports,
  174,763 terrain tiles, and 2,038,645 vegetation transforms. Source relief retains
  93.3773% strong-core coverage and 99.5965% high-ridge source support. Full validation
  passed in 332.7 seconds. Paired smoke then passed on exact v33 fingerprint `810a2f1f`
  with zero mod-attributable lines, and a fresh game reached HUD-proven Observer in 126.3
  seconds. Independent hard-reset regional views accept Gundabad's compact crown, Erebor's
  isolated massif, and Orodruin's cratered cone as components. They reject the still-low,
  green Ered Lithui/Ephel Duath around Morannon and White Mountains near Dunharrow. The
  attempted close frames drifted off their targets and are explicitly excluded from the
  verdict.
- v34 preserves Ardacraft's exact relief placement and Arda Maps' range envelopes but
  replaces the underpowered blanket 18% residual axes with reviewed continuity weights:
  40% Misty Mountains, 38% Grey Mountains, 34% Ered Luin, 48% White Mountains, 50% Ephel
  Duath, 50% Ered Lithui, 46% southern Mountains of Shadow, 32% Iron Hills, and 28%
  Mountains of Mirkwood. Residual broad/body/spine widths contract to 1.50/0.82/0.20 and
  concentrate 56% of the response on the narrow spine. Control conformance records
  93.5712% strong-core coverage and 99.2840% high-ridge source support. A new independent
  theatre guard prevents that global average from hiding local regressions: northern
  ranges record 93.2500%/99.7365% core/support, Erebor 88.4884%/99.0044%, White Mountains
  95.0116%/98.0522%, and Mordor 91.7496%/97.6886%. A parallel regional drainage guard
  binds northern, Anduin, White Mountains, and Mordor/Gondor systems to independent
  control-count, vertex, and source-path-length floors. The full world
  regenerated in 695.8 seconds with 6,004 locations, 279 ports, 174,763 terrain tiles,
  2,038,645 vegetation transforms, and height range 0–63,678. Full validation passed in
  326.5 seconds. Paired smoke is pending rather than failed on exact fingerprint
  `e4cd6cd55640cde8cff297a918420c71c95f0a03cb5661183ff86778eccfcaa4` while Antiquitas
  owns the shared EU5 lease.
- v34 subsequently passed paired vanilla/mod smoke on that exact fingerprint with zero
  new and zero mod-unique lines, then entered a fresh non-debug HUD-proven Observer in
  126.4 seconds. Independent hard-reset regional/target-relative close pairs retain
  Gundabad's compact chain crown, Erebor's isolated snowy massif, and Orodruin's cratered
  cone as accepted components. They reject v34 as the range fix: the Morannon remains a
  shallow green saddle without visibly high Ered Lithui/Ephel Duath flanks, and Dunharrow
  remains low green relief without a visibly tall White Mountains wall. Attempted
  Carachost/Starkhorn control searches returned the full political overview and are
  explicitly excluded. The game stopped cleanly and released the shared slot.
- v35 diagnoses the two valid v34 failures as renderer-pipeline defects rather than
  cartographic placement errors. The former circular pass blur is now an anisotropic
  saddle at Paths of the Dead and Morannon: it is narrow along the reviewed range tangent
  and elongated across the crossing. Every source coordinate remains fixed. A 1.28 gain
  applies only to the exact hash-pinned Ardacraft crest field, not to the secondary hand
  axes; all four independent source-support theatres remain green. Material generator v30
  exposes earlier dark-rock/rock transitions only on the White Mountains, Ephel Duath,
  Ered Lithui, and southern Mountains of Shadow axes.
- Deterministic flank contracts quantify the actual live failures. Dunharrow retains a
  low 21,188 route cell while its 0.01 equal-scale window reaches 61,889 and carries
  21.566% terrain at or above 43,000. Morannon retains a low 24,257 route cell while its
  0.005 window reaches 55,000 with 6.169% at or above 43,000. Material windows require
  exposed-rock coverage independently at both theatres. Strong Ardacraft core coverage is
  99.8509% globally with 99.4203% high-ridge source support; northern, Erebor, White
  Mountains, and Mordor theatre guards all pass.
- The first v35 production write used the system Pillow and exposed a legitimate
  toolchain-reproducibility issue: the pinned validator differed by one unit at 1,894
  resampled height pixels. The authoritative `.venv` toolchain was therefore used for the
  complete rewrite. Stronger northern relief also exposed that Gundabad's playable anchor
  had connected to a 180-cell internal green pocket. Anchor access now rejects small or
  enclosed candidate components and connects to land proven to contain at least 2,048
  control cells, preserving the accepted summit while restoring route topology.
  `m2_world.py` now refuses writes/checks unless Pillow 12.3.0 and numpy 2.4.6 match the
  pinned `requirements.txt`; the system Pillow 12.0.0 path fails before touching outputs.
- The authoritative v35 world regenerated in 637.0 seconds with 6,004 locations, 289
  ports, 174,763 terrain tiles, 2,038,645 Arda-native vegetation transforms, and model
  SHA `8d31aa479efb2b4cae69e0cd9724f5a39f2bb87c23af0aa207dda97d0505eff8`.
  Full validation passed in 337.5 seconds, including deterministic height, terrain cache,
  source relief/drainage, Gundabad/realm reachability, and census. Exact game-visible
  fingerprint `7b1e09179985873da81495ffb8ad53cce531aaa7e19b5273eeb67b31c6cc5cc2`
  awaits smoke/live proof because Antiquitas currently owns the shared EU5 slot; this is
  pending, not failed, and v35 is not yet visually accepted.
- v35 subsequently passed paired smoke in 200.6 seconds with zero new and zero mod-unique
  error lines, then entered a fresh non-debug HUD-proven Observer in 124 seconds. Ten
  valid captures used independent hard reset, named focus, regional capture, and exactly
  +3 target-relative zoom for Gundabad, Erebor, Morannon, Orodruin, and Dunharrow. The
  live verdict rejects v35: Erebor remains an isolated snowy massif and Orodruin a strong
  cratered cone, but Morannon and Dunharrow still read as broad green uplands. Their high
  samples are scattered at frame edges instead of forming continuous enclosing walls.
  Evidence is retained under `docs/screens/20260801_m2_ardacraft_relief_v35/`.
- v36 does not raise unbounded hand axes. It adds audited continuity gains of 1.65 for the
  White Mountains/southern Mountains of Shadow and 1.75 for Ephel Duath/Ered Lithui, then
  multiplies every gained axis/branch sample by a soft dilation of the exact Ardacraft
  support mask before relief composition. This resolves the source-drift failure of the
  earlier blanket-axis experiment. Global high-ridge source support rises to 99.6845%; the
  White Mountains record 98.7299% and Mordor 99.5990%, both above unchanged theatre floors.
- v36 raises Dunharrow's 0.01-window >=43,000 fraction from 21.566% to 24.652% and
  Morannon's 0.005 fraction from 6.169% to 16.756%; corresponding regression floors are
  now 24% and 15%. Tightened material contracts require 21% exposed/10% rock at
  Dunharrow and 54% exposed/8% rock at Morannon. The pinned world regenerated in 662.5
  seconds with model SHA `e03c16e1ecd2da5a6c3dfefcf56fb82834348e5f1cf0d2323ed80983e475bcfe`,
  6,004 locations, 306 ports, and 174,763 terrain tiles. Full validation passed in 334.3
  seconds on exact fingerprint `a9de05d5baced55be3b59a884bb89a43232e7c1ad4a1c43c54f6f9531c41274b`.
  Corrected paired smoke later passed in 249.1 seconds with zero new and zero mod-unique
  lines. A fresh world reached HUD-proven Observer in 110.8 seconds. Five independently
  reset regional/+3 close pairs reject v36 despite that technical proof: Gundabad,
  Morannon, and Dunharrow still present broad or displaced green/grey uplands. Erebor and
  Orodruin remain accepted components. The first automation attempt clicked Continue and
  is excluded; the captured incompatible-save/Continue-as-Observer modal proves a UI-
  coordinate defect, not a load failure.
- The New Game driver now targets the measured y `0.420` button centre and classifies both
  the retained main menu and Load Game panel after the click. The excluded first attempt
  had actually activated Continue's lower edge and its incompatible-save modal, not Load
  Game; retained-menu retries now press Escape to restore a clean menu. Regression tests
  cover neutral, main-menu, and save-list frames.
- v37 replaces the low-precision plateau-producing profile with a 1280×1026 five-bit
  Ardacraft numeric field. Exact source response is convex and crest-dominant; supported
  named axes use narrow 2/12/86% broad/body/spine composition; final height normalizes at
  the actual 40,800 control maximum and reaches 63,983 without hard-clipped samples.
  Dunharrow's honest 0.0125 window records 19.75% >=43,000 and gradient p90 4,467;
  Morannon's 0.015 window records only 1.10% >=43,000 with gradient p90 2,851, satisfying
  bounded-area anti-upland contracts rather than rewarding broad lift.
- Terrain material contracts now have upper as well as lower bounds at Dunharrow,
  Morannon, Gundabad, and Erebor. Mordor's former radial ash/slab presentation was caught
  in offline preview and replaced by a source-range-enclosed dark basin with lighter rock
  restricted to high exposed crests. Terrain-cache generator v33 forces algorithm changes
  to invalidate stale material payloads while reusing only verified compatible height.
  The coherent 6,004-location model `14a8466848db92925280889bdefdb9ef132510f688b1dd5755aae11b51491436`
  regenerated in 325.0 seconds with 284 ports, 174,763 terrain tiles, and 2,038,645
  vegetation transforms. Full validation passed in 367.2 seconds. Exact fingerprint
  `97e271fbcdb68203b30a731f62037899c7e4b28658113160a721892aaa3c7337` is queued behind
  Antiquitas's shared lease; smoke/live proof is pending, not failed.
- v37 subsequently passed paired smoke on that exact fingerprint with zero new and zero
  mod-unique lines. After correcting the menu target from Continue's lower edge to the
  measured New Game centre, one click entered a genuinely fresh HUD-proven Observer in
  201.2 seconds. Five independent reset/regional/+3 pairs are valid but reject v37:
  Gundabad remains a broad tableland, Morannon and Dunharrow do not form convincing walls,
  and Orodruin is an oversized flat-topped mesa. This is a visual rejection, not a load
  failure; the custom world is independently proven to start.
- v38 removes redundant hand axes, Gaussian pass flanks, and source-backed summit lobes
  from physical relief. The pinned 1280×1026 Ardacraft numeric field now owns range
  branches and jagged crests directly; only compact source-gap peaks remain at Mindolluin
  and Irensaga. Erebor moves from the displaced Arda point to Ardacraft's direct mountain
  marker `(0.599699, 0.137606)`, and the Morannon pass moves to its direct fortification
  marker `(0.609732, 0.529449)`. A 68,000-unit cubic final response preserves narrow upper
  arêtes while reaching 64,493 without hard clipping; Orodruin is a compact 63k cone.
  Source support is 99.9672% globally, 100% in the northern/Erebor theatres, 99.7956% in
  the White Mountains, and 99.9296% in Mordor. The unified generator now authors controls
  before all downstream stages, closing the stale-control pipeline gap. Mordor's material
  biome now flood-fills the exact source U-wall with a bounded irregular east transition,
  replacing v37's rounded two-lobed proximity blob. Model `fefa695d` regenerated with
  6,004 locations, 292 ports, 174,763 terrain tiles, and a 199.9 MB self-contained cache.
  The pre-enclosure candidate passed validation in 385.8 seconds; the final source-
  enclosure tree requires a fresh full validation, including control
  regeneration and complete cache verification. Smoke deferred with exit 75 while
  Antiquitas owns the shared EU5 session; live verdict remains pending and no visual pass
  is claimed.
- Final v38 validation passed in 372.7 seconds. Exact paired smoke passed in 202.9 seconds
  on fingerprint `f5d6fd22` with zero new and zero mod-unique diagnostics, and a genuinely
  fresh New Game entered HUD-proven Observer in 124.3 seconds. Five independently reset
  regional/+3 pairs reject the visuals: the quantized source and saturated response make
  sheer flat-topped mesas. This is definitive visual rejection, not a load failure.
- v39 replaces the half-resolution five-bit relief with a losslessly compressed native
  2500x2003 eight-bit numeric field, removes relief-modulation saturation, and authors
  compact canonical summits only at final 8192x4096 resolution. Orodruin likewise leaves
  the generic range normalizer for an independent irregular cone, rim, and crater.
  Morannon expands only nonzero exact source relief around its direct marker; the pass
  floor and all zero-source cells remain fixed.
- Anti-mesa contracts now require 30,000-80,000 samples above 45k and cap low-gradient
  high relief below 10%. v39 records 39,672 and 8.94%. Erebor, Gundabad, Dunharrow, and
  Orodruin reach compact 60-61k summits; Morannon's exact arms reach 50.9k around its
  12.7k gate. Only sub-eight-cell gameplay mountain-class flecks are absorbed; all
  physical source relief remains, with 485 substantive mountain components covered.
- The unified v39 world write passed in 360.5 seconds with model
  `9f022ce30e64d2127476cb452007d4429fae2781e94b6bdede367d34dfe4052e`,
  6,004 locations, 298 ports, 235 authored route edges, 2,038,645 vegetation transforms,
  and a 171.7 MB cache (25,053 unique height / 63,647 unique material tiles). Full
  validation passed in 381.8 seconds. Exact paired smoke passed in 201.5 seconds on
  fingerprint `f8e557faca68a8d5204fab6c305fa32a96f42569a7ea72dfd288248bb9781759`
  with zero new and zero mod-unique diagnostics, and a genuinely fresh New Game reached
  HUD-proven Observer in 126.4 seconds.
- Five independently reset regional/+3 pairs under
  `docs/screens/20260801_m2_ardacraft_relief_v39/` reject v39 at the live visual gate.
  The native source removed most giant tablelands, but its current final-height response
  still turns painted relief bands into cliff shelves. Gundabad retains a rounded summit,
  Morannon shows one displaced southern massif instead of the Ered Lithui/Ephel Duath
  hinge enclosing the gate, Orodruin reads as several lobes rather than one dominant
  volcano, and the White Mountains around Dunharrow do not read as a continuous jagged
  chain. Erebor is correctly isolated at the direct Ardacraft marker, but its crown is
  still too smooth. This is another visual rejection, not a load or cache failure; M2
  remains red and v40 must correct source-to-EU5 relief morphology before rivers.
- v40 replaces raw warm-rock shelves with a source-native 4/12/18-pixel continuous
  body/shoulder reconstruction while retaining 22% of the exact jagged core. The final
  response is single-stage and vanilla-calibrated: terrain above 45k has median/p75/p90
  gradients 342/538/772 rather than v39's 3,263/5,428/7,561, while major range crests
  reach 52-55k and Erebor/Orodruin reach 61.4k. Validation now rejects both featureless
  hills and excessive cliff shelves instead of imposing the former non-vanilla 10%
  low-gradient ceiling.
- Morannon retains its direct marker and receives two narrow drawing-confirmed hinge arms
  to the nearest exact Ered Lithui and Ephel Duath source crests. The oriented carve keeps
  the gate floor at 18.6k while adjacent relief reaches 44.0k. Source-backed named points
  receive only tiny final-resolution teeth; Gundabad uses its source junction, Erebor its
  isolated asymmetric massif, and Mindolluin/Irensaga retain source-gap profiles.
- The complete v40 world regenerated in 644.0 seconds with model
  `7f48ab78fac25a9c3b134152ff94c23f29282789103e79e2b581c508cb9942ec`,
  6,004 locations, 282 ports, 225 authored route edges, and 2,038,645 vegetation
  transforms. Its 180.1 MB self-contained cache contains 32,675 unique height tiles and
  63,531 unique material tiles. Severe rock follows narrow reconstructed source crests,
  not legacy hand-axis slabs. Full validation, exact smoke, and the fresh five-pair live
  visual verdict remain pending; no v40 visual pass is claimed.
- v40 then passed full validation, exact paired smoke on fingerprint `3b425cca`, and two
  fresh HUD-proven Observer starts. Correctly targeted live frames reject it: Erebor is
  an isolated but broad stump at close zoom and a weak hill regionally; Gundabad is a
  green basin surrounded by flat rock carpet; and Morannon is a low grassy V rather than
  the Ered Lithui/Ephel Duath gate. The first capture batch was discarded after proving
  Finder had retained focus on Snowpoint; `focus-location` now explicitly focuses and
  clears the search box before typing, and exact-target captures provide the verdict.
- v41 keeps every horizontal source coordinate and tightens only vertical/material
  translation. Ardacraft relief now uses a 3/8/15-pixel reconstruction dominated by its
  three-pixel folded body, one moderate control gamma, and a 55k convex upper response.
  Terrain above 45k has 307,474 samples with median/p75/p90 gradients
  720/1,270/1,895: materially sharper than v40 without approaching v39 shelves. Erebor's
  summit radius is reduced 43%, Gundabad receives a compact exact-point crown, Morannon's
  two hinge spines are narrower and taller, and Orodruin's harmonics are halved.
- The complete v41 world regenerated in 669.6 seconds with model
  `35fc4a7ce429826b1e83a81e8cd75f72782025c502d6df9117498a141e6d201b`,
  6,004 locations, 292 ports, 232 authored route edges, and 2,038,645 vegetation
  transforms. Its 172.3 MB self-contained cache contains 26,160 unique height tiles and
  64,046 unique material tiles. Static source/height/material gates pass; full validation,
  exact smoke, and fresh live five-theatre judgment remain mandatory. No visual pass is
  claimed and rivers/politics remain blocked.
- v41 passed full validation in 366.0 seconds, exact paired smoke in 200.5 seconds on
  fingerprint `ba936c9e`, and a genuinely fresh HUD-proven Observer in 121.0 seconds.
  Exact-target live frames reject it. Erebor is substantially improved into an isolated
  steep cone and Orodruin is a single pointed volcano, but Gundabad remains a green basin
  inside rock carpet, Morannon is a broad southwest wall plus a ruler-straight eastern
  trace, and Dunharrow is two isolated spikes rather than a continuous White Mountains
  chain. The gate remains red.
- v42's offline source preflight decodes Ardacraft's pale neutral summit pixels as well as
  warm-rock shoulders. This restores the raster's existing snow-spine structure that all
  earlier red-minus-green reductions discarded. It removes v41's synthetic Morannon
  lines and ordinary source-backed named-point teeth while retaining specialized Erebor,
  Gundabad, Mindolluin, and Irensaga profiles. Height/source/material preflights pass;
  330,014 samples exceed 45k with median/p75/p90 gradients 744/1,355/2,045. Full world
  regeneration, validation, smoke, and live judgment remain pending.
- The complete v42 world regenerated in 697.0 seconds with model
  `987245ab43496bd171dbe2cd11901c0fd195ef4de42cf40ff2ad934f43e57a90`,
  6,004 locations, 293 ports, 242 authored route edges, and 2,038,645 vegetation
  transforms. Its 173.8 MB self-contained cache contains 26,306 unique height tiles and
  64,068 unique material tiles. Full validation, exact smoke, and fresh live judgment
  remain pending; no visual pass is claimed.
- v42 then passed full validation in 410.2 seconds, exact paired smoke in 202.7 seconds
  on fingerprint `5b9b078e`, and a genuinely fresh HUD-proven Observer start in 124.0
  seconds. Exact close/regional frames under
  `docs/screens/20260801_m2_ardacraft_relief_v42/` reject it: Gundabad still sits inside
  a broad exposed-rock carpet, Erebor is two adjacent oversized mounds, Morannon is a low
  rounded berm, Orodruin remains too broad, and Dunharrow is surrounded by smooth green
  ridges rather than a continuous jagged White Mountains spine. This is visual rejection
  evidence, not a load failure; rivers and political reassignment remain blocked.
- v43 is the current offline candidate. It leaves every source coordinate unchanged but
  compresses warm upper shoulders beneath the true top 8% arête field, reducing terrain
  above 45k from 330,014 to 224,227 samples. Those samples retain varied
  median/p75/p90 gradients of 869/1,718/2,641 with only 37.2% below 512. Erebor's duplicate
  raster/marker bodies are locally collapsed into one direct-marker summit; Gundabad gains
  a compact exposed crown; Orodruin's apron/cone are smaller; and Morannon receives a
  source-shaped upper-wall lift that cannot create synthetic lines or raise the gate.
  The complete 6,004-location model
  `16e5d5492da39c3ba88d67ff6a6c110f5d02393c47cb2128bf8fd7f34db8833c`
  regenerated in 590.8 seconds with 300 ports, 239 route edges, 2,038,645 vegetation
  transforms, 25,276 unique height tiles, and 63,897 unique material tiles. Static height
  and material preflights pass; full validation, exact smoke, and fresh five-target live
  judgment remain mandatory.
- v43 passed full validation in 354.0 seconds, exact paired smoke in 199.8 seconds on
  fingerprint `74a774b1`, and a genuinely fresh Observer start in 126.0 seconds. The ten
  exact-target frames reject the long-range presentation: Erebor is finally one isolated
  massif and Orodruin is a compact pointed cone, but Gundabad remains dominated by broad
  exposed material, Morannon's eastern/northern wall remains a low uplift, and the White
  Mountains around Dunharrow still read as smooth green ridges. v43 is retained as proof
  of those two local improvements, not accepted as the terrain gate.
- v44 preserved v43's source footprints, coordinate set, pass floors, Erebor
  de-duplication, and Orodruin cone while increasing only final-resolution signed folds
  and sparse positive summits inside the existing mountain-strength envelope. The
  complete world regenerated in 581.0 seconds with model `16e5d549`, 6,004 locations,
  300 ports, 239 route edges, 2,038,645 vegetation transforms, 25,332 unique height
  tiles, 63,900 unique material tiles, and a 170.6 MB self-contained cache. Full
  validation passed in 350.3 seconds; exact paired smoke passed in 200.0 seconds on
  fingerprint `312aa575` with zero new and zero mod-unique diagnostics; and a genuinely
  fresh Observer started in 126.2 seconds. Exact-target live views nevertheless reject
  v44: some extra exposed crest patches appear around Gundabad, but the long ranges remain
  broad and low; Morannon and Dunharrow are not materially improved. Erebor remains one
  isolated massif and Orodruin remains a compact pointed cone. The next candidate must be
  calibrated from matched installed-vanilla mountain captures rather than another
  arbitrary amplitude increase.
- Installed-vanilla v45 calibration captured matched close/regional views around Chur,
  Shey, and Kathmandu under `docs/screens/20260801_vanilla_mountain_calibration/` and
  added `tools/mountain_calibration.py`. Equal 8192x4096 windows prove that v44 was not
  globally too low: its upper gradients were already two to three times vanilla's. The
  measurable defects were morphology and material placement: Gundabad occupied 35.7% of
  the radius-96 upper half and 20.2% of its upper quarter, while Dunharrow and Morannon
  had only 11 and 3 upper-quarter maxima respectively. Vanilla Shey occupied 23.2% and
  7.5% with 427 quantized maxima; those counts are comparative morphology evidence, not
  literal elevation targets.
- v45 contracted Gundabad's source shoulder, redistributed part of the broad ruggedness
  budget into a bounded high-frequency signed field, widened source-aligned material
  response, and bound Morannon rock to source relief plus physical wall height. Its
  coherent pinned-toolchain world regenerated in 600.9 seconds with model `16e5d549`,
  6,004 locations, 100 rivers, 300 ports, 239 route edges, 2,038,645 vegetation
  transforms, 25,920 unique height tiles, 64,049 unique material tiles, and a 192.3 MB
  cache. Full validation passed in 381.3 seconds; paired smoke passed in 209.9 seconds on
  fingerprint `3d769297` with zero new lines; and a fresh Observer reached the live HUD
  in 126.1 seconds.
- The fresh live evidence under
  `docs/screens/docs/screens/20260801_v45_mountain_review/` rejects v45. Gundabad's
  upper-quarter area improved to 8.2%, but its regional view is an enormous pale cap and
  its close view remains broad. Dunharrow shows regular terrace/facet bands and blocky
  exposed-rock patches introduced by the high-frequency field/material thresholds.
  Morannon keeps its saddle open but still fails to present the enclosing Ered Lithui and
  Ephel DÃºath walls at close view. Erebor and Orodruin retain their accepted isolated
  forms. v45 is load proof and calibration evidence only; it must not be committed or
  accepted as the terrain gate.

## 2026-08-02 — v70 relief retention and all-LOD forest-density candidate

- The retained v62-v70 mountain sequence narrowed Mordor's two walls, moved the old
  off-source hand axes onto sampled Ardacraft relief maxima, made their cross-sections
  pointed, de-duplicated the broad source junction body, and rebuilt the Morannon hinge
  as two arms that rise away from the exact low Cirith Gorgor gate. Cache-only serration
  was proven insufficient; authoritative 8192×4096 height morphology controls the
  renderer-scale silhouette. Static source, height, material, cache, and mountain
  calibration gates pass. Owner review now finds the mountain system recognizably
  mountainous and the overall map increasingly accurate; no final nine-theatre terrain
  acceptance is claimed.
- A v70 fresh New Game reached a fully rendered country-selection map, proving the map
  bytes load, but a missed Observe toggle was misclassified as the similarly painted
  `Select a Country` control. The driver now requires the independent country-change-rule
  dialog before authorizing Observer start and clicks the actual centre of the accepted
  control; its regression test passes. Two runs ended with engine-logged OS quit events,
  no crash dump, and no fatal map diagnostic, so the repeated external test interruption
  is recorded in `BLOCKERS.md` and will be retried at the forest checkpoint.
- The current offline forest candidate increases derived vegetation from 2,038,645 to
  3,057,385 transforms without changing any source woodland polygon or political cell.
  Deterministic all-LOD contracts require at least 550k/420k/420k transforms in Mirkwood
  and 25k/18k/18k in Lothlórien. The generated census provides roughly
  580k/443k/439k and 29k/21k/22k respectively. Lothlórien contains zero pine/generic
  variants and uses only two installed light-trunk full-canopy meshes. Exact written-bin
  validation and the Observer-driver regression pass; full validation, fresh close views,
  and paired smoke remain pending.

## 2026-08-02 — v71 dense-forest live proof

- The accepted cartographic projection hash is now bound to explicit Ered Lithui and
  Ephel Dúath coordinate, width, sharp-profile, and Morannon-endpoint contracts rather
  than a hash-only review. A coherent full regeneration produced 6,004 locations,
  287 ports, 100 river controls, 3,057,385 vegetation transforms, and deterministic world
  model `6048d0cc97170670688e2d8259517242efffc1482bf14d0a141745f90735ed34`.
  Full `gmake validate` then passed every control, world, cache, object, runtime, realm,
  people, census, template, and lint check in 364.8 seconds.
- A genuinely fresh player-facing New Game on exact tree fingerprint
  `06e7c07eba15006020da9d498a7811270f9e3f359d50c93839fd037b865d8b2f`
  reached country selection, independently accepted the Observer rule, and entered the
  paused live HUD in 171.1 seconds. Evidence is under
  `docs/screens/20260802_v71_dense_forests/`.
- Caras Galadhon regional/close views prove Lothlórien as a continuous closed broadleaf
  canopy with the installed light-trunk meshes resolving at close zoom; the deterministic
  species contract retains zero pine and zero generic forest variants in its source
  polygon. Woodmen's Hall regional/close views prove Mirkwood as a theatre-scale mixed
  ancient canopy rather than sparse dots, with deliberately irregular clearings and a
  visibly denser interior at every rendered LOD.
- A 45-second live playback resumed once, advanced from TA 3018.1.1 to 3018.1.10, remained
  responsive at approximately 5.8 GB working set, and added no map, terrain, vegetation,
  mesh, location, or gameplay diagnostic. The only post-launch lines were the two known
  Steam store-backend lookups and inherited `AudioArena` warning. The shared EU5 lease
  was released cleanly afterward. Paired commit-gate smoke remains mandatory.

## 2026-08-02 — v72 source-constrained political assignment

- Replaced unrestricted nearest-seat political spread with 30 explicit equal-scale claim
  envelopes for well-attested western/northern realms. Capitals, canon anchors, and eight
  occupied operational sites remain pinned; lower-confidence East/South realms retain
  region claims under a 0.32 anti-sprawl ceiling rather than invented precise borders.
  Ordinary Ithilien is now deliberately wild while its attested refuges, crossings,
  towers, and gateworks keep their controllers.
- Added complete generated audits at `docs/world/derived/m3_ownership_audit.csv` and
  `.json`. They cover all 5,200 land locations with source contract, normalized position,
  distance, forced-anchor status, verdict, final bounding boxes, and political connected
  components. Validation rejects every envelope violation and fragmentation of 15 compact
  source-side realms. The final audit has zero violations: Lothlórien is one 44-location
  Naith claim, Dunland one 47-location lowland claim, and Iron Hills one 45-location
  cluster; 200 ordinary Ithilien locations are `wild_ithilien`.
- A coherent regeneration rebuilt 6,004 locations, 38 realms, 5,179 populated locations,
  100 rivers, 287 ports, and 3,057,385 forest transforms on unchanged world model
  `6048d0cc97170670688e2d8259517242efffc1482bf14d0a141745f90735ed34`.
  Full `gmake validate` passed in 387.4 seconds.
- Fresh live evidence under `docs/screens/20260802_v72_political_boundaries/` reached the
  Observer HUD in 129.5 seconds on exact fingerprint
  `d595e311ec4ce6174747091865c87e279f73f6f2fe7d4ee488021cb1580773f9`.
  Regional frames prove Lothlórien east of and separate from Moria, and Dunland west of
  Isengard/north-west of Rohan instead of its former block. A 45-second run advanced from
  TA 3018.1.1 to TA 3018.1.10 while responsive at about 5.9 GB. Repeated evidence UI
  interactions reproduced the already tracked coat-of-arms tooltip/input-context lines;
  no map, ownership, setup, or simulation error appeared.
- Mandatory paired `gmake smoke` then launched vanilla and ENDÓRË back-to-back under one
  transaction lease and passed in 202.2 seconds with exactly zero new error-log lines.

## 2026-08-02 — v73 source-drainage hierarchy candidate

- Rebuilt the hash-pinned Arda Maps drainage as 102 non-duplicated physical controls.
  Lefnui and Serni are now independent indexed channels; Lhûn is a strong source-derived
  main stem plus southern branch; Sirith and all eleven Ethir Anduin distributaries remain
  visible parser-safe physical drainage. Duplicate Harnen, Morgulduin, and lower-Anduin
  source parts were removed rather than double-incised.
- Added six bounded hydrology classes with reviewed incision/material response, nearly
  uniform minor-bank growth, complete provenance, twelve independent-channel and basin
  coverage contracts, exact Ethir retention, and duplicate-source rejection. Major rivers
  keep the installed downstream 4→5→11→15 widening grammar; dense-forest bank clearance
  remains below the major threshold, preserving the accepted Lothlórien/Mirkwood canopy.
- One coherent 834.2-second regeneration produced 6,004 locations, 102 river controls,
  287 ports, 25,247 unique height tiles, 63,979 unique material tiles, and 3,057,385 forest
  transforms on unchanged world model
  `6048d0cc97170670688e2d8259517242efffc1482bf14d0a141745f90735ed34`.
  Full `gmake validate` passed every gate in 373.6 seconds.
- A genuinely fresh visual New Game reached HUD-proven Observer in 147 seconds on exact
  tree fingerprint `c9b21485f3d78d7f11874c4f48ae706b33ad02146953008f9956c66a5c5eee1b`.
  Evidence under `docs/screens/docs/screens/20260802_v73_river_hierarchy/` proves the broad
  Anduin beside dense light-trunk Lothlórien, the broad Osgiliath reach, and multiple
  narrower Gondor/Lindon source channels at regional and close zoom. A 45-second playback
  advanced from TA 3018.1.1 to TA 3018.1.10 without pause recovery. The sole appended
  95-byte diagnostic was the inherited machine `AudioArena size is too small` warning;
  no map, river, terrain, ownership, setup, or simulation line appeared.
- The first paired-smoke attempt correctly deferred while Antiquitas owned the shared
  lease. At the next natural checkpoint, the exact pending fingerprint acquired the slot
  and `gmake smoke` passed in 201.5 seconds: vanilla and ENDÓRË both reached menu-ready,
  the mod added exactly zero error-log lines, and the transaction lease released cleanly.

## 2026-08-02 - v74 dense canonical forests and source-shaped realm claims

- Owner review reopened Mirkwood/Lothlorien density and political silhouettes. A direct
  audit proved that only 5 of Lothlorien's former 44 location centres lay inside the
  physical Golden Wood source mask; the other 39 were admitted by a rectangular search
  envelope. Rectangles are now search bounds only, never sufficient woodland evidence.
- The political generator raster-overlaps complete EU5 locations against the hash-pinned,
  naturalized Arda Maps polygons for Lothlorien, Fangorn, Druadan, and the three Mirkwood
  controllers. Dunland uses a reviewed seven-vertex lowland polygon. A detected four-cell
  detached Woodmen island exposed an artificial region seam and was correctly transferred
  to Dol Guldur's southern-Mirkwood claim. The final audit covers all 5,200 land locations,
  has zero violations, and makes every affected compact realm contiguous: LOR 21, DUN 32,
  WOO 59, WDM 40, DOL 36, FAN 31, DRU 3.
- The fixed 3,057,385-object runtime budget was redistributed without reducing the accepted
  Fangorn, Old Forest, or Ithilien floors. Final high/medium/low counts are Mirkwood
  760,747/567,263/561,115 and Lothlorien 70,991/50,758/50,250. Every Lothlorien transform
  remains one of the two installed light-trunk full-canopy meshes, with zero pine/generic
  variants. Generator version 11 makes the placement deterministic.
- One coherent 394.6-second regeneration rebuilt 6,004 locations, 38 realms, 5,200 land
  profiles, 5,179 populated locations, 242 route edges, and all three vegetation LODs on
  unchanged world model `6048d0cc97170670688e2d8259517242efffc1482bf14d0a141745f90735ed34`.
  Full `gmake validate` passed every gate in 415.0 seconds.
- A genuinely fresh New Game reached HUD-proven Observer in 147.8 seconds on exact tree
  fingerprint `98c795b54ca828d998f81ed2e3548cc61087dc6955fce28aab6ba8410b26962a`.
  Evidence under `docs/screens/20260802_v74_dense_forests_source_claims/` proves the smaller
  irregular Lothlorien silhouette outside the Misty Mountains, dense light-trunk interior
  canopy, near-continuous Mirkwood canopy, and corrected Dunland silhouette. A 45-second
  maximum-speed playback advanced from TA 3018.1.1 to TA 3018.1.15 without pause recovery;
  `error.log` remained exactly 1,486 bytes. The EU5 lease was released cleanly. Paired
  commit-gate smoke remains pending.

## 2026-08-02 - v75 sparse tundra and varied Harad renderer candidate

- The v73 nine-theatre evidence exposed two independent renderer defects while the v74
  commit gate was lease-deferred: biome 5 tundra had been omitted from material climate
  handling, and the pine family treated tundra as ordinary conifer country. Vegetation
  generator v12 now retains only 14,589/8,171/7,921 transforms across the complete tundra
  at high/medium/low LOD. The unchanged 3,057,385-object budget redistributes those trees
  into true forests, raising Mirkwood to 950,729/677,500/670,517 and Lothlorien to
  75,643/54,871/54,459 while preserving its light-trunk-only species contract.
- Terrain material generator v44 was rejected in real EU5 evidence under
  `docs/screens/20260802_v75_climate_forests/`: the installed renderer resolved its
  earth/sand combination as green ground with pale sand islands. The evidence is retained
  as a failed calibration and is not an accepted visual checkpoint.
- Terrain material generator v45 was also rejected in real EU5 evidence under
  `docs/screens/20260802_v75b_climate_forests/`: its binary rock/sand channels formed
  enormous dark blotches across Harad. Both speculative climate branches were removed.
  `gen_terrain_cache.py`, its preview, and all 174,763 cache tiles were regenerated from
  and verified against the last proven v43 source; all three now have zero Git diff.
- The complete v45 source tree had passed full validation in 461.8 seconds, proving the
  failure was visual rather than structural. That result does not accept the rejected
  palette. The remaining combined candidate is narrowly scoped to vegetation v12 and
  source-shaped political ownership. Post-rollback full validation passed in 405.4
  seconds with the proven v43 material source/cache at zero diff.
- Fresh v75c evidence under
  `docs/screens/20260802_v75c_dense_forests_source_claims/` reached HUD-proven Observer on
  exact fingerprint `fb07a2150e6aa439efb5c1cad6f9c3d52f22cfdf496fa7b698a8a20008791283`.
  Regional/close frames prove theatre-scale continuous Mirkwood and a closed
  light-canopy Lothlorien interior; the clean political overview retains the compact
  source-shaped woodland controllers and smaller Dunland. Finder/country-panel evidence
  interactions produced only a reproducible GUI data-model loop, with no map, terrain,
  setup, ownership, or simulation diagnostic, so that playback was not used as the clean
  runtime proof.
- A second untouched fresh session under `docs/screens/20260802_v75d_clean_playback/`
  immediately ran maximum-speed Observer for 45 seconds with zero pause recovery and
  ended at the exact 1,486-byte baseline `error.log`. Paired vanilla plus ENDÓRË smoke
  then passed in 201.8 seconds with zero new mod lines. `eu5_slot.py assert-smoked`
  confirms that the smoke covers exact fingerprint `fb07a215`. This accepts the focused
  dense-forest/source-shaped-ownership checkpoint; the wider nine-theatre physical gate
  remains red.

## 2026-08-02 - v76/v77 bounded water and climate-scenery probes

- Two fresh live lake-object variants proved that the installed `lake_mesh` ABI loads on
  Arda but exposes a rectangular carrier around small authored basins. The complete
  experiment was removed after the second strike; all ten material ponds and the exact
  Earth-object quarantine remain unchanged. Rejected evidence is retained under
  `docs/screens/docs/screens/20260802_v76_native_ponds/` and
  `docs/screens/20260802_v76b_native_ponds/`.
- Audited the installed exact generated-object families for palms, grass, and generic
  rocks as a materially different alternative to rejected broad material masks. Palm
  populations of 26,000, 4,000, and 1,600 records did not yield a defensible localized
  improvement. A fresh zero-palm A/B left the southern green rosettes unchanged; a fresh
  zero-grass A/B removed them. Palm and grass definitions are now quarantined, their bins
  removed, and stale-output validation prevents either route from silently returning.
- Retained only 16,000/10,000/10,000 high/medium/low generic-rock transforms. Static
  contracts clip every record to source climate biomes 8/9/10, preserve all three biome
  populations, and enforce spatial serialization. Fresh evidence under
  `docs/screens/20260802_v77e_no_generic_green/` proves clean Qarsad and Umbar views while
  the accepted dense Lothlórien canopy remains intact. The deterministic corpus now has
  3,093,385 records: the unchanged 3,057,385-tree v75 baseline plus 36,000 sparse rocks.
- The permanent quarantine/stale-output implementation passed full `gmake validate` in
  405.9 seconds. Paired vanilla/ENDÓRË `gmake smoke` then passed in 200.4 seconds with
  zero new mod error lines; `eu5_slot.py assert-smoked` binds that result to exact
  game-visible fingerprint `f97befaa204df096c0877aa0d48f7de7f274060fd664598187a45e6de9d74366`.
  This accepts the narrow rock/quarantine renderer batch only. M2's complete physical
  nine-theatre owner gate remains red and no gameplay milestone is resumed.

## 2026-08-02 - v78 full political-component review candidate

- Rebuilt the edge-sharing graph for all 5,200 land locations and reviewed every
  component beyond each realm's primary body. The previous audit reported components but
  only failed fragmentation for fifteen compact realms; it could still admit tiny
  unforced color islands elsewhere. Schema 3 now records complete detached member lists,
  forced-anchor status, and one exact physical disposition per surviving split. Any
  unclassified future component is a validation failure.
- Applied sixteen bounded source-side repairs. Two Shire specks outside the reviewed
  Brandywine claim and one unattested far Lindon island become wild. Three Lindon cells
  beyond its coast join the Blue Mountain holds; two Rohan cells south of the White
  Mountains join Gondor; one Belfalas coast cell joins Dol Amroth; one Long Lake cell
  joins Esgaroth; reciprocal Beorning/Goblin specks move to the vale/mountain sides; and
  three southwest Rhûn cells join contiguous Dorwinion. The two-location Tolfalas island,
  Westfold, divided coasts, mountain fastnesses, crop-edge claims, and all forced
  strongholds/refuges remain with explicit dispositions.
- The regenerated audit has 3,430 owned and 1,770 deliberately wild land locations,
  zero claim violations, and zero unreviewed detached components. Lothlórien remains a
  single 21-location Golden Wood overlap and Dunland a single 32-location reviewed
  lowland polygon. The roster remains 38 realms: no subfaction was invented merely to
  hide a border defect. M3, M4 people assignments, the deterministic location
  localization/templates, and the 5,179-location census were regenerated coherently.
- Full `gmake validate` passed in 536.8 seconds. A genuinely fresh player-facing New Game
  reached HUD-proven Observer on exact game-visible fingerprint
  `e2c57c6edf7cde11a71f944732a1c597efc7830f170270b33b0cada5995f12f8`; evidence under
  `docs/screens/20260802_v78_component_audit/` includes the complete political overview,
  dense source-side Lothlórien, bounded Dunland, and corrected Esgaroth/Long Lake view.
  A 45-second maximum-speed playback required zero pause recovery and ended at the exact
  1,486-byte `error.log` baseline. Paired vanilla/ENDÓRË smoke passed in 265.3 seconds
  with zero new mod lines, and `eu5_slot.py assert-smoked` binds the result to the same
  fingerprint. This accepts the focused component audit; M2's full physical nine-theatre
  owner gate remains red.

## 2026-08-02 - v79 source-biome and topology-reseed candidate

- Replaced the proof-era Brown Lands, Rhûn, and Harad climate polygons with an exact,
  hash-pinned reduction of Ardacraft's 197-feature biome atlas. The production controls
  now contain one detailed Brown Lands component, 41 Rhûn steppe components, 37 Near
  Harad scrub/woodland components, and seven Far Harad arid components. Only explicitly
  logged organic continuations reach the authored east/south crop edges; Mordor's
  source-enclosed ash field retains final precedence.
- Regenerated the complete 174,763-tile terrain cache. It now contains 68,178 unique
  material records in a 204.0 MB self-contained cache while retaining the accepted
  heightfield, coast, rivers, mountain geometry, and 3,093,385-object renderer budget.
  The coherent world remains 6,004 locations: 5,200 land, 600 impassable mountain, 60
  lake, and 144 sea locations.
- Climate-weighted density legitimately reseeded generated location IDs. The schema-3
  political gate rejected the stale v78 component repairs before a game launch; the
  stale mapping would otherwise have painted Gondor in Rhûn, Blue Mountain holdings in
  Far Harad, and Dorwinion in Angmar. Replaced it with ten physically witnessed local
  repairs. Every repair now binds an expected region, a tight coordinate window, and the
  destination realm's source-side claim contract, so a future reseed fails immediately.
- The renewed audit has 3,467 owned and 2,537 wild land locations, zero contract
  violations, and zero unreviewed political components. Lothlórien remains one compact
  20-location source-overlap claim east of the Misty crest; Dunland remains one compact
  32-location lowland polygon. M3, M4, M5, and all 6,004 engine templates pass their
  independent static checks. Full validation, live nine-theatre renderer evidence,
  playback, paired smoke, and exact-fingerprint assertion are still pending, so v79 is a
  candidate and M2 remains red.

## 2026-08-02 - v80 dense ancient forests and complete frontier contracts

- Before changing the proven tree, completed v79's fresh-game baseline. New Game reached
  HUD-proven Observer on exact game-visible fingerprint
  `1f899f223fe4b5a389530523c21f1453023bdf2644edc23d689134b8bb13b425`;
  an untouched 45-second maximum-speed playback required zero recovery and retained the
  exact 1,486-byte `error.log` baseline. Evidence is under
  `docs/screens/20260802_v79_source_biomes/`. This proves v79 loadability, not its complete
  nine-theatre acceptance. The preceding v79 summary's `2,537 wild` figure included 804
  mountain/lake/sea entries; its land-only count was 1,733.
- Fresh Caras Galadhon and Woodmen's Hall close views reproduced the owner report. The
  source forest shapes were present, but Mirkwood exposed broad park-like openings.
  Vegetation generator v13 therefore increases the bounded total from 3,093,385 to
  3,493,385 transforms, broadens tree canopies, and raises continuous-interior
  suitability without changing any source woodland polygon or river corridor.
- The deterministic high/medium/low census is Mirkwood
  1,112,756/796,168/788,083; Lothlorien 87,564/69,865/69,863; Fangorn
  57,974/26,658/26,881; Old Forest 13,186/12,968/13,078; and Ithilien
  1,757/1,313/1,356. Every Lothlorien transform remains an installed light-trunk
  full-canopy variant, with zero pine/generic intrusion. The complete 3.49m transform
  corpus passes deterministic, locality, climate-escape, tundra, named-zone, and species
  checks.
- Audited all realm extents after the v79 reseed. Harnendor had reached the far-south
  crop, Khand had reached Far Harad, and Rhunic allocations had spilled into the Brown
  Lands. Every one of the 38 realms now has an explicit physical geography contract.
  Lothlorien and all three Mirkwood powers intersect source-forest overlap with irregular
  theatre partitions; seven East/South states use irregular bounded spheres and leave
  wilderness between unattested controllers. The result has 3,044 owned and 2,156 wild
  land locations, zero violations, zero unreviewed components, and zero uncontracted
  realms. No new realm was invented to absorb neutral cells.
- Regenerated M3/M4/M5, definitions, localization, census, and all 6,004 location
  templates coherently. The tagged political QA raster makes every realm directly
  identifiable. Targeted `gen_map_objects.py --check` and `m3_realms.py --check` pass.
  Full validation, fresh v80 renderer evidence, playback, paired smoke, and exact
  fingerprint assertion remain pending; M2's complete nine-theatre gate stays red.

### v80b live focused verification

- The first v80 launch on fingerprint `fabdcff9` loaded and proved the denser Mirkwood,
  but close Caras Galadhon views rejected the original wide-canopy Lothlorien variants as
  too dark and generic. This negative calibration is retained under
  `docs/screens/20260802_v80_dense_forests_frontiers/`.
- Replaced only Lothlorien's two renderer mesh references with the installed slimmer,
  light-trunk `environment_oceanic_tree_01/02` meshes. Counts, positions, source masks,
  political cells, and Mirkwood remained byte-identical. Deterministic map-object checks
  passed before launch.
- A genuinely fresh v80b New Game reached HUD-proven Observer in 113.6 seconds on exact
  fingerprint `2df4b63d9be5180089d9d74fa4b61fb4c22f4c94020d481c394b3b02d0140e63`.
  Evidence under `docs/screens/20260802_v80b_birch_meshes/` includes a wide live
  Wilderland political view, Caras Galadhon and interior Lothlorien regional/close,
  Mirkwood regional/close, and playback frames. The tagged generated QA raster supplies
  the corresponding full-world political coverage. Lothlorien now exposes pale trunks
  and a separate broadleaf silhouette;
  Mirkwood reads as a darker near-continuous ancient canopy.
- Maximum-speed Observer playback ran 45 seconds with zero pause recovery and retained
  the exact 1,486-byte `error.log` baseline. Final full validation passed in 430.5 seconds,
  including the complete 174,763-tile terrain cache, 3,493,385 map-object corpus, all
  realm/people/census/template outputs, and lint. After Antiquitas released its healthy
  session, paired vanilla/ENDORE smoke passed at the next natural checkpoint in 200.8
  seconds with zero mod-unique error lines. `eu5_slot.py assert-smoked` binds the pass to
  exact fingerprint `2df4b63d9be5180089d9d74fa4b61fb4c22f4c94020d481c394b3b02d0140e63`.
  This accepts the focused v80b forest/frontier checkpoint; the complete nine-theatre
  owner gate is still red.

## 2026-08-02 - v81 nine-theatre audit and v82 climate/Old Forest correction

- Launched an exact fresh v80b Observer and captured all nine physical theatres under
  `docs/screens/20260802_v81_nine_theatre_audit/`. The audit accepted Mirkwood's
  near-continuous close canopy and the retained rugged mountain renderer, while proving
  three presentation defects: Forochel still read as temperate green, Rhûn/Near Harad
  were nearly uniform green plains, and the Old Forest's old roughly 13k-per-LOD budget
  read as isolated clumps. Far Harad was a single pale sand surface. A 45-second playback
  retained the 1,486-byte error-log baseline. Dol Amroth's ocean-only capture was marked
  inconclusive rather than misclassified as a coast defect.
- Implemented a materially different climate renderer instead of repeating rejected
  v44/v45 noise masks. The single seamless ENDÓRË biome now exposes installed native
  tundra, steppe, and stony-sand materials as dedicated palette channels. Generator v46
  paints source-smoothed climate interiors deterministically and enforces lowland coverage
  floors. It reused the verified v43 height cache and regenerated all 174,763 material
  tiles; the self-contained cache remains 193.3 MB and contains zero Earth decal layers.
- Generator v14 preserves the v13 per-family random seed while redistributing the fixed
  3,493,385-transform corpus into the unchanged Old Forest mask. Final named-zone counts
  are Old Forest 75,027/56,507/55,995, Mirkwood 1,060,221/759,520/752,336, Lothlórien
  85,157/67,671/67,930, Fangorn 56,299/25,896/26,082, and Ithilien
  1,735/1,282/1,324 at high/medium/low. Lothlórien remains pine-free and uses only the
  installed light-trunk oceanic variants.
- A genuinely fresh v82 New Game reached HUD-proven Observer in 124.2 seconds on exact
  fingerprint `9edf9d2da385ca1c3a619ea8c213226f851c7a2f8e969070836beed31cd073eb`.
  Evidence under `docs/screens/20260802_v82_climate_old_forest/` proves cold stony
  Forochel, ochre Rhûn/Near Harad, stony Far Harad, retained dense Mirkwood/Lothlórien,
  and the compact closed Old Forest source core. A unique Edhellond retest proves
  Belfalas land is intact. Maximum-speed Observer playback ran 45 seconds with no recovery
  and no error-log growth. Full validation passed in 462.6 seconds, including all 174,763
  cache tiles, 3,493,385 object transforms, downstream world outputs, and lint. After
  several correct lease deferrals behind Antiquitas, paired vanilla/ENDÓRË smoke acquired
  the slot and passed in 202.7 seconds with zero new lines. Exact-fingerprint assertion
  binds the pass to `9edf9d2da385ca1c3a619ea8c213226f851c7a2f8e969070836beed31cd073eb`;
  the complete nine-theatre M2 gate remains red regardless.
- Used the lease interval for a read-only drainage audit. The pinned controls retain 102
  non-duplicated Arda Maps courses and 1,736 vertices, but the installed-safe writer emits
  only 12 independent source-to-water channels: 28,512 non-background width-marker pixels
  versus vanilla's 741,652. Fourteen named tributaries are skipped because they join a
  parent; 76 additional courses remain height/material drainage. Vanilla uses green
  source endpoints, red/yellow degree-two junction markers, and 4/5/11/15 width channels,
  but earlier exact red-endpoint tests still failed in build 24187685. This isolates the
  next physical-map task without contaminating the accepted v82 candidate.

## 2026-08-02 - v83 hierarchy-aware physical drainage visibility

- Generator v47 reused the verified Arda height payload and regenerated only the terrain
  material cache. It leaves the accepted 12-channel engine river raster and every source
  course untouched, while increasing named terrain-only drainage presentation by roughly
  32% and unnamed physical feeders by roughly 16%. Class validation rejects any physical
  course lacking one of the six authored hydrology classes. The complete 174,763-tile
  cache check passes and still reports zero Earth decal layers.
- A genuinely fresh player-facing New Game entered HUD-proven Observer in 162.4 seconds on
  exact candidate fingerprint
  `b299dedc65704ba3b3c8c408274fb8dd7b20d088776a7e7cbb96313546d1eeed`.
  Evidence under `docs/screens/20260802_v83_river_visibility/` includes independently
  reset Brandywine Bridge, Field of Celebrant, Pelargir, and Hills of Evendim views at
  calibrated +12/+14 zoom. The indexed Brandywine and Anduin-family channels remain blue
  water; parser-unsafe tributaries read as wider incised drainage following their exact
  Arda Maps courses. No broad road-like material corridor appeared.
- Maximum-speed Observer playback ran 45 seconds with zero pause recovery and retained
  the accepted 1,486-byte error-log baseline. Paired vanilla/ENDÓRË smoke passed in 226.4
  seconds with zero new lines and no mod-unique diagnostics; `eu5_slot.py assert-smoked`
  binds that pass to exact fingerprint
  `b299dedc65704ba3b3c8c408274fb8dd7b20d088776a7e7cbb96313546d1eeed`. Full validation
  passed in 415.2 seconds, including all cartography controls, 174,763 cache tiles,
  downstream world outputs, and lint. This accepts only the narrow visibility mechanism;
  the complete river presentation and M2 nine-theatre gate remain red.

## 2026-08-02 - v84 terrain-native sub-location water checkpoint

- Re-audited all fifteen source lakes and the installed lake-object/material contracts.
  Five large lakes remain engine water. Mirrormere and minor lakes 04-07/10-14 occupy
  only 189 pixels in the 4096x2048 source atlas and remain continuous physical land to
  avoid the already proven whole-location quarry. The prior retail `lake_mesh` variants
  remain rejected because their unit-square carriers render as visible blue rectangles.
- Removed an uncommitted exact-outline mesh experiment after the session-start master-plan
  review reaffirmed the explicit ban on generating new 3D meshes. No experimental mesh,
  locator, transform, or quarantine change survives in the tree.
- Built a materially different supported A/B: `endore_still_water` derives its diffuse
  deterministically from the hash-pinned installed vanilla `dirt_ponds_01` texture,
  using vanilla's flatter unmasked normal and glossy properties contract.
  Only the existing wetland-coast channel changes identity. Each exact material-pond core
  now uses that one channel instead of the former grass/earth/pond/transition/river blend;
  the feathered rim remains, and source geometry, height, coast, river raster, forests,
  relief, locations, and ownership are byte-identical.
- Generator write/check, byte-for-byte DDS derivation, terrain-cache regeneration,
  `pdxlint`, and a pre-precedence full `gmake validate` passed. A final audit found 115
  high-resolution pond/shore samples crossed by the later river pass; generator v48 now
  restores water-channel precedence after that pass and regenerated the full material
  payload. Targeted checks pass on final candidate fingerprint
  `bfecb37264d46f9f08c6762cff1b732e9ca3f65c69887fa20906a4effaecd5de`.
  The first fresh live colour/relief calibration was rejected: exact Nindalf outlines
  appeared, but their mottled brown-green cores read as craters rather than water. A
  second genuinely fresh New Game on the pre-manifest fingerprint
  `9f4f323905de8b47587a296ec41b08fb3b3202a0b8590e01119b8bae3e086ccc`
  accepted a cooler blue range plus vanilla's level unmasked normal. Calibrated Nindalf,
  Mirrormere, and Shire evidence under `docs/screens/20260802_v84b_terrain_water/` shows
  level blue irregular water and no square carrier, hard rim, or polygon spill. A
  45-second maximum-speed Observer interval required zero recovery and retained the
  1,486-byte baseline. The first full gate then correctly rejected stale cache provenance;
  coherent regeneration retained byte-identical material payload hashes while updating
  the source manifest. Paired vanilla/ENDÓRË smoke passed in 201.0 seconds with zero new
  lines on final exact fingerprint
  `9fff7077743c1f78248aa48ab5a3342d5ae3917c328803878698b6b43973ed4e`.
  Commit remains conditioned on repository-wide static green; M2 remains red regardless.

## 2026-08-02 - v85 deterministic nine-theatre evidence candidate

- Re-audited the invalid Belfalas evidence path. The v81 result centred a sea location
  and showed only open water; the later Edhellond finder result centred an inland cell and
  showed only grass. Neither is shoreline evidence, and neither justifies redrawing the
  hash-pinned 2,043-vertex Belfalas source window.
- Added a single autonomous nine-theatre capture driver. It starts one fresh visual-map
  Observer, captures a centred full-map silhouette, hard-resets zoom before every theatre view, uses unique generated-location queries,
  captures regional and close pairs for all nine binding theatres, runs 45 seconds of
  maximum-speed playback, and releases the lease. Belfalas uses `Dol Amroth` at calibrated
  zoom; source-interior targets replace fuzzy labels in Old Forest, Forochel, Mirkwood,
  Rhûn, and Harad. Its static target-resolution and compile checks pass.
- Full validation passed in 472.8 seconds, including the new unique-camera contract and
  complete 174,763-tile map pipeline. Repeated invocations correctly deferred before
  launch because unmanaged EU5 PID 29448
  owns the shared machine. Per the cross-project protocol this is neither a failure nor a
  blocker and is not polled. The tool remains an uncommitted candidate until the fresh
  evidence exists and can drive a source-backed physical correction or an honest no-change
  verdict. M2 remains red.

## 2026-08-02 - v86 physical-frontier hierarchy and player-profile correction

- A named-anchor audit found that the realm repair layer had hidden wrong strategic
  hierarchy: Barad-dur, Orodruin, and Nurn reported as Ithilien; Dale and Erebor as Grey
  Mountains; Rivendell as Anduin Vale; and Erech as Rohan. Mordor now follows an
  irregular source-aligned mountain enclosure, the Misty boundary bends around
  Rivendell, the Dale theatre resolves before the Grey Mountains, and Rohan stops north
  of Erech. Ten named anchor-region contracts make these distinctions permanent.
- Rebuilt only hierarchy-dependent outputs. Terrain geometry, coasts, height, rivers,
  vegetation transforms, and terrain cache remain unchanged. The 38-realm audit now has
  3,198 owned and 2,002 deliberately wild land locations, zero claim violations, and no
  undispositioned component. Mordor owns its full enclosed interior; Rivendell is compact
  in Eriador; Erebor is a compact 13-location Lonely Mountain realm and no longer claims
  the Grey Mountains; a detached one-cell Goblin-town island is deliberately wild.
- Confirmed the owner's flat manual view was configuration leakage, not missing map data:
  the shared `pdx_settings.json` retained smoke's `3d_terrain_disable=true`. Added a
  player visual-profile command and made smoke snapshot/restore the complete prior
  settings payload. Unit and isolated round-trip checks pass, and the visual profile was
  restored after the owner's EU5 process closed.
- The full nine-theatre audit is still pending and M2 remains red. Repository-wide
  validation, exact smoke, fresh physical/political evidence, and owner acceptance remain
  mandatory before this candidate can be committed or the gate can advance.
- Repository-wide `gmake validate` passed in 569.8 seconds on the regenerated candidate:
  all seven top-level commands, the 174,763-tile Arda-only cache, 38-realm graph,
  downstream setup, capture manifest, and lint are green. Exact smoke remains pending
  behind the owner's responsive manual visual session.

## 2026-08-02 - v87 complete drainage-water hierarchy

- Reworked the visible river system around all 102 non-duplicated source courses without
  changing their lore-pinned geometry or the installed-safe twelve-channel parser graph.
  Upper and lower Anduin now reach the installed maximum river width earlier. Every
  affluent also receives a class-aware nested terrain-water core, while exact valleys,
  tributary hierarchy, distributaries, and confluences remain source-controlled.
- Rejected three genuinely fresh live calibrations. v49 and v50 painted the full broad
  bank mask and produced inland-sea bands; v51 proved that OR-blending a narrow core with
  an outer material band still renders the entire band as water. Generator v52 paints
  only the nested core: ordinary drainage is roughly two to three source pixels and the
  Great River grows to roughly five or six, leaving readable dry banks.
- Fresh New Game evidence on exact fingerprint
  `f75e17f804a716537ec2b5acd9ca126bbae05b5d7338ca3f640ce8159e4151c9`
  is under `docs/screens/20260802_v87d_hydrology/` and
  `docs/screens/20260802_v87e_hydrology/`. Upper Anduin at Caras Galadhon and lower Anduin
  at Osgiliath read as the dominant watercourse; Celebrant and Entwash remain continuous,
  visibly narrower source-aligned branches. Maximum-speed playback ran 45 seconds with
  zero pause recovery and retained the exact 1,486-byte error-log baseline.
- Extended the deterministic evidence driver with upper/lower Anduin plus Celebrant and
  Entwash regional/close captures and fixed full-map ordering so Caras focus cannot leak
  into the silhouette frame. Repository-wide validation passed in 421.8 seconds. Paired
  vanilla/ENDÓRË smoke passed in 201.3 seconds with zero new mod lines, and
  `eu5_slot.py assert-smoked` binds it to the exact v52 fingerprint. This is an accepted
  focused hydrology mechanism, not M2 completion; the nine-theatre owner gate remains red.

## 2026-08-03 - v88 source-bound full-atlas evidence

- The first technically clean v88 full-atlas run was rejected on inspection: stale raw
  `Land ####` queries could silently land around Moria or Mordor after localization. Its
  full-map and genuinely named frames remain mechanically useful, but no affected raw-
  query frame is accepted as evidence.
- The capture manifest now parses the committed localization and requires one localized
  result, a matching strategic region, and a normalized source-coordinate distance no
  greater than 0.012 for all thirteen theatre and hydrology targets.
- Corrected v88b completed in 809.5 seconds on exact fingerprint
  `f75e17f804a716537ec2b5acd9ca126bbae05b5d7338ca3f640ce8159e4151c9`, from fresh New
  Game to Observer, followed by 45 seconds of maximum-speed playback with zero recovery
  and the unchanged 1,486-byte error log. Every finder target resolved to its intended
  source-bound location.
- The corrected atlas supports only the focused mechanisms it visibly proves: dense
  source-shaped forests, source-derived climates, a dominant upper/lower Anduin, and
  visible narrower Limlight and Entwash courses. Its frame labelled Celebrant was later
  rejected because Field of Celebrant is physically on the Limlight. It does not close M2.
  Full feature-level
  source comparison, political review after physical acceptance, and explicit owner
  acceptance remain open. Mordor camera framing was improved for the next atlas; terrain
  was not changed merely because a close camera looked into the canonical Morannon saddle.

## 2026-08-03 - v89 source-bound drainage atlas and camera calibration

- Expanded the focused hydrology manifest from four views to seventeen. Brandywine,
  Lhûn, Greyflood, Isen, Celduin, Carnen, Harnen, Poros, Lefnui, Serni, Morgulduin,
  Gladden, and Limlight now have unique ASCII finder anchors, exact localized
  coordinate/region contracts, and a maximum 0.010 distance to their named source course.
  The default nine-theatre run is unchanged; `--drainage-only` and selective exact
  `--targets` runs avoid repeating unrelated cameras.
- v89 completed all thirteen new drainage pairs in 812.8 seconds on exact fingerprint
  `f75e17f804a716537ec2b5acd9ca126bbae05b5d7338ca3f640ce8159e4151c9`, then ran 45
  seconds at maximum speed with zero recovery and the unchanged 1,486-byte error log.
  Its frames prove that the major courses are present and substantial, but its nominal
  regional/close pairs were rejected as scale evidence because finder focus saturated
  both at effectively the same close camera.
- v89b reversed the operation order and completed an eight-course sample in 551.4 seconds
  with the same clean playback/log result. It proved source centers and distinct political
  scales, but absolute +8/+12 detents from full-map state did not preserve 3D terrain, so
  those frames are not accepted as physical-map evidence.
- v89c used finder-relative -6/-1 zoom-outs and completed in 305.1 seconds with the same
  exact fingerprint, clean 45-second playback, and 1,486-byte log. The regional frame now
  supplies political orientation and the close frame retains 3D terrain. Close evidence
  proves the upper Anduin is already massive, the true Celebrant is visible on its
  mountain-to-Anduin course, and the narrower Morgulduin runs west from Minas Morgul.
  No river was widened from the rejected intermediate frames. M2 remains red.

## 2026-08-03 - v90 native-resolution river banks

- Traced the remaining tooth-like river banks to the material-cache scale mismatch:
  Endórë's general material source is 8,192×4,096, while the installed cache contract is
  65,536×32,768 and nearest sampling expands every binary edge pixel eightfold.
- Generator v53 retains the complete 8K material stack and all v52 source paths, widths,
  height incision, pond precedence, climate, relief, forests, and ownership. Only a
  one-bit river core is rendered at the full virtual resolution and substituted for the
  coarse channel-6 bit in close/medium mips. The verified height cache was reused.
- The material bake completed in 244.2 seconds with 174,763 tiles, 45,083 unique material
  tiles, and a 24.0 MB payload (about 0.5 MB larger than v52). The complete cache remains
  193.8 MB.
- Fresh v90 New Game evidence on fingerprint
  `0ef39c3b6c40a8dcc2f224b204a542e38f6432982e2477ba41199ebafd84c69d`
  compares the same source-bound Anduin, Celebrant, Brandywine, Harnen, and Morgulduin
  cameras. Banks are continuous rather than 8×8 stair-steps; Anduin remains dominant,
  major trunks remain substantial, and Morgulduin remains narrower. The session completed
  45 seconds at maximum speed with zero recovery and the unchanged 1,486-byte error log.
  Repository-wide validation passed in 405.1 seconds. Paired vanilla/Endórë smoke passed
  in 202.1 seconds with zero new lines. Final living-document validation and exact smoke
  binding are being repeated before commit; M2 remains red regardless.

## 2026-08-03 - v91 full atlas and feature-specific camera correction

- Sealed v90 after a final 422.6-second repository validation, exact 202.1-second paired
  smoke with zero new lines, and `assert-smoked` on fingerprint
  `0ef39c3b6c40a8dcc2f224b204a542e38f6432982e2477ba41199ebafd84c69d`.
  Commit `5e32785` is pushed to `origin/main`.
- Captured the complete nine-theatre plus four-course hydrology atlas on that exact tree
  in 721 seconds. Fresh New Game reached HUD-proven Observer and completed 45 seconds at
  maximum speed with zero recovery and the unchanged 1,486-byte error log.
- Rejected three misleading v91 camera conclusions rather than changing terrain from
  them. A one-detent zoom-out hides forest objects; Dol Amroth centered its sea cell; and
  Barad-dur did not frame Mount Doom. The renderer data itself remained intact.
- Updated the source-bound manifest to use maximum-close forest cameras, unique Edhellond
  land for Belfalas, and exact Orodruin for Mordor close evidence. A focused v91b fresh
  run completed in 345.4 seconds with the same clean 45-second playback. It proves dense
  Mirkwood, a dense source-shaped Old Forest core with porous surroundings, Belfalas land
  and drainage at Edhellond, and compact cratered Orodruin. All localization, coordinate,
  region, and river-camera contracts pass.
- The current Anduin views remain visibly dominant over their affluents; the lower reach
  at Osgiliath is especially broad. Do not globally widen the v53 hierarchy. Continue the
  remaining course-by-course source-edge review and change only a demonstrated local
  width, confluence, or coverage defect. M2 remains red pending the complete visual audit
  and explicit owner acceptance.

## 2026-08-03 - v92 complete native-bank drainage review

- Completed the remaining twelve source-bound regional/close pairs under
  `docs/screens/20260803_v92_remaining_drainage/`: lower Anduin, Entwash, Lhûn,
  Greyflood, Isen, Celduin, Carnen, Poros, Lefnui, Serni, Gladden, and Limlight. The
  fresh New Game reached HUD-proven Observer on exact fingerprint
  `0ef39c3b6c40a8dcc2f224b204a542e38f6432982e2477ba41199ebafd84c69d` and completed
  45 seconds at maximum speed with zero recovery and the unchanged 1,486-byte error log.
- The close physical views show the lower Anduin as the dominant massive trunk, broad
  named rivers beneath it, and progressively narrower affluents. Greyflood has multiple
  fine headwaters; Lhûn forms its source-backed three-way system; Celduin and Carnen keep
  readable subordinate drainage; and the Gondor, Vale, and Rohan tributaries meet their
  intended receiving waters.
- Audited the only apparent discontinuity directly against projected controls. `lhun`
  and `source_lhun_84_02` share endpoint `[0.316589, 0.114628]`, with a computed minimum
  separation of exactly zero. The apparent gap is finder-marker/camera presentation, not
  absent source geometry.
- This completes live coverage of the 102-course Arda Maps drainage control on v53's
  native-resolution banks. There is no source-backed basis for global widening or for
  inventing additional decorative watercourses. Freeze the present hierarchy and change
  only a specifically named course with a demonstrated source mismatch. M2 remains red
  for explicit owner acceptance.

## 2026-08-03 - v93 owner-calibrated Great River scale

- Direct owner review superseded v92's conservative visual-width conclusion for the
  Anduin while leaving its source-completeness conclusion intact. Generator v54 changes
  only the native-resolution water-core scales for upper_anduin (0.22→0.46) and
  anduin (0.22→0.44). All 102 axes, control widths, confluences, incision paths,
  parser-safe channels, bank envelopes, height data, and non-Anduin materials remain
  unchanged.
- The regenerated material cache reused the verified height payload and completed in
  248.2 seconds: 174,763 tiles, 45,088 unique material tiles, 24.0 MB material payload,
  and 193.8 MB complete cache. Its direct checker passes with zero Earth decal layers.
- Fresh same-camera evidence under docs/screens/20260803_v93_anduin_scale/ proves a
  visibly massive upper Anduin at Caras Galadhon and a roughly doubled lower reach through
  Osgiliath, while the tributaries remain narrow and readable. The water stays inside the
  existing source-incised valley and does not recreate the rejected inland-water bands.
- The exact candidate fingerprint is
  9d1357d8bff04560a847c1ce9b0dab3f56e5da248be5c49f1365b25b2d64dd80.
  Fresh HUD-proven Observer playback ran 45 seconds at maximum speed with zero recovery
  and the unchanged 1,486-byte error log. Paired vanilla/Endórë smoke passed in 201.7
  seconds with zero new lines and no mod-unique diagnostic. Full validation and exact
  smoke assertion remain before commit; M2 remains red for owner acceptance.

## 2026-08-03 - v94 compact Nan Curunir political correction

- Direct full-map/raster review isolated Isengard's 38-location rectangular strip as a
  concrete ownership defect. It extended south across the Gap almost to Helm's Deep and
  included the source-bound Fords of Isen despite Saruman's attested domain being the
  compact ring and vale of Nan Curunir.
- Added an eight-vertex normalized polygon around the Isengard anchor and north of the
  Fords. A permanent silhouette contract requires 8..18 locations inside a tight physical
  bbox, one connected component, and an explicit `fords_of_isen != ISE` rule. Schema 4
  now records eligible-location counts and fill fractions for all contracted realms.
- The coherent result assigns 13 connected locations to Isengard, 193 to one connected
  Rohan, 36 to one connected Dunland, and 31 to one connected Fangorn. Relative to v93,
  16 cells return to Rohan, four to Dunland, one to Fangorn, and seven become deliberate
  wilderness. All 38 realm contracts have zero violations and every detached component
  has a physical disposition.
- Regenerated M3 ownership/gazetteer/setup, all 5,200 M4 people profiles, the 5,179-location
  M5 census, all 6,004 templates, and hierarchy localization. Focused M3/M4/M5/template
  checks pass. Full validation correctly caught the initially stale hierarchy localization;
  regenerating its owned payload resolved that deterministic cascade omission.
- Fresh source-bound evidence under `docs/screens/20260803_v94b_gap_political/` entered
  HUD-proven Observer on final fingerprint
  `6572f6400849e103c54fdf526f0dbc8325713d38ad64b98451da38e25a46ba1b`.
  The regional frame proves compact Isengard between Dunland, Fangorn, and Rohan with the
  Fords inside Rohan; the close frame retains physical terrain and Isen. Playback ran 45
  seconds at maximum speed with zero recovery and the unchanged 1,486-byte error log.
  Paired vanilla/mod smoke passed in 221.8 seconds with zero new lines. Full repository
  validation passed in 446.0 seconds and exact smoke assertion covers the same final
  fingerprint. Commit/push this focused checkpoint; M2 stays red.

## 2026-08-03 - owner hydrology review after v93

- Direct player review rejects v93 as a final visual scale despite its technical/runtime
  success: Anduin still reads too small and the visible network needs more rivers,
  affluents, and feeder branches.
- Reopened the hydrology TODO and owner gate. Preserve v54 as the minimum non-regression
  baseline, but re-audit rendered Great River width and source-extraction completeness
  against both accepted online maps. Every added course remains source-traced or otherwise
  lore-attested; no decorative drainage is authorized.

## 2026-08-03 - v94 deterministic cascade closure

- The first full validation rejected stale hierarchy localization after the political
  regeneration. Rewrote only `gen_definitions`' owned hierarchy/localization payload.
- The regenerated lexicon moved two generated-name evidence queries. Static source
  contracts rejected the stale Entwash `odgar`/Léodgar and Greyflood `Blackdown End`
  matches; rebound them to current `Framham` and exact-coordinate `Cedardown End` without
  moving either camera, course, coordinate, or strategic-region contract.
- Final validation passes in 446.0 seconds. Final-fingerprint Fords evidence completes in
  215.6 seconds with clean 45-second playback. Paired smoke passes in 221.8 seconds with
  zero new lines, and exact assertion covers
  `6572f6400849e103c54fdf526f0dbc8325713d38ad64b98451da38e25a46ba1b`.

## 2026-08-03 - v95-v97 rejected dense-drainage experiments

- Reduced the already quarantined, hash-pinned Ardacraft V2 drainage payload to a numeric
  binary field around the complete 102-course Arda Maps atlas. Raw published imagery
  remains outside Git.
- v95 used native nearest-neighbour enlargement. A fresh New Game loaded and ticked cleanly
  and Anduin's 0.72/0.68 native core scale finally read as massive, but the feeder layer
  became giant square blocks. Reject it.
- v96 replaced material enlargement with thresholded bilinear cores. It loaded and ticked
  cleanly but left short right-angle stubs. Reject it.
- v97 added a 24-pixel connected reach, source-thickness opening, component filtering,
  thinning, and terminal pruning. Its 25,475-sample field loaded and ticked cleanly but
  still presented combs/lattices because too much of the raw rill network survived.
  Reject it. None of v95-v97 was committed.

## 2026-08-03 - v98 curated source-connected affluents

- Replaced broad raster presentation with a direct-affluent graph filter. A retained path
  must start within four source pixels of a reviewed river, extend at least twenty pixels
  away, contain at least sixteen samples, and reconnect to the exact reviewed axis. This
  yields 61 source paths and 2,060 binary samples across all four bound drainage theatres.
- Reconstructs those paths as corner-safe graph edges, removes source-pixel stair steps,
  applies two endpoint-preserving curve passes, and uses the same geometry for shallow
  incision, narrow tree clearance, wet banks, and full-resolution water cores. The 102
  reviewed courses and twelve parser-safe channels remain unchanged.
- The complete 6,004-location v56 bake passed in 833.8 seconds: height 0..64,310, 174,763
  height tiles/25,246 unique, 174,763 material tiles/45,133 unique, 193.9 MB total cache,
  and 3,493,385 vegetation transforms. Cartography, control, height, zero-Earth cache, and
  indexed-river checks all pass. Full repository validation passes in 428.6 seconds.
- Fresh source-bound evidence under
  `docs/screens/20260803_v98_curated_affluents/` entered live Observer on fingerprint
  `696cfc31bacb10bf238fa91becbff9e6678281d808d17bf99145fc56ea007f18`.
  Eight regional/close pairs prove upper/lower Anduin, Celebrant, Entwash, Baranduin,
  Greyflood, Isen, and Celduin. Playback ran 45 seconds at maximum speed with zero
  recovery and the unchanged 1,486-byte error log. M2 remains red for direct owner review.

## 2026-08-03 - v99 complete current-fingerprint visual gate

- Expanded the default M2 atlas with focused pairs for Lothlorien canopy density,
  Gundabad, isolated Erebor, Mirrormere, and the Nindalf wetland cluster. Every finder
  query resolves to committed localization and is bound to an exact normalized source
  coordinate and strategic region. The ambiguous literal Gundabad query is deliberately
  replaced by unique Coldpoint Heights, the closest localized mountain cell to the
  audited summit.
- A fresh no-debug New Game entered HUD-proven Observer on unchanged fingerprint
  `696cfc31bacb10bf238fa91becbff9e6678281d808d17bf99145fc56ea007f18` and captured the
  full map, all nine regional/close theatres, four core hydrology pairs, and all five
  focused physical pairs under `docs/screens/20260803_v99_full_atlas/`.
- Native-resolution review confirms that the current payload retains dense Mirkwood and
  Lothlorien canopies, visible 3D relief across the audited ranges, isolated Erebor,
  source-shaped small-water material, and a dominant upper/lower Anduin. Playback then
  ran 45 seconds at maximum speed with zero recovery and no change to the 1,486-byte
  baseline error log. No game-visible correction is justified by this pass; M2 remains
  red solely for explicit owner acceptance.

## 2026-08-03 - v100 compact Erebor political correction

- Replaced Erebor's source-inconsistent east-west strip with a compact nine-vertex claim
  around the exact Lonely Mountain coordinate. ERE now owns nine connected locations
  inside `x=0.588523..0.612454`, `y=0.123107..0.139228`; the four released locations
  (`me_land_1935`, `me_land_4163`, `me_land_4241`, `me_land_4950`) return to deliberate
  wild land. Dale and the Iron Hills are unchanged, all 38 realms remain present, and all
  political silhouette contracts pass.
- Regenerated the downstream M3-M5 ownership, people, census, localization, templates,
  and setup layers. Deterministic naming changed the Celduin/Carnen camera labels from
  Dalestrand/Gundgathol to Lakestrand/Gatholgathol without moving either source coordinate,
  strategic region, or river geometry.
- A fresh no-debug New Game entered HUD-proven Observer on fingerprint
  `24b205efa0a037f7ae37b40cd15294d86fbbd32eac88749b97dd0005e854ab78` and captured
  regional and close Erebor evidence under
  `docs/screens/20260803_v100_compact_erebor/`. The regional frame proves the compact
  political holding; the close frame retains the isolated physical summit. Playback ran
  45 seconds at maximum speed with zero recovery and no change to the 1,486-byte log.
- The first paired smoke attempt suffered a vanilla-control `nvtt.dll` access violation
  while two orphaned ENDÓRË audit interpreters consumed roughly 17 GB of private memory.
  Their exact PIDs and command lines matched the two earlier timed-out read-only probes.
  After terminating only those owned orphans, free memory recovered to about 19.7 GB and
  the unchanged candidate passed paired vanilla/mod smoke with zero new error lines. This
  was a host-resource failure, not a candidate regression. M2 remains red pending direct
  owner acceptance.
