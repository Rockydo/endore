# Verified Engine Facts

Build examined: Steam app 3450310, build ID 24187685. The proven reference runtime reports
Europa Universalis V 1.3.1.1 (Pavia), checksum 7917; metadata uses comparator `1.3.11`.

## Runtime

- Game directory: `G:\SteamLibrary\steamapps\common\Europa Universalis V` (read-only).
- Content roots: `game/in_game`, `game/main_menu`, and `game/loading_screen`.
- `--user_dir=<absolute path>` and playset JSON automation are proven on this machine.
- The French-keyboard console scan code is `0x29`.
- Renderer must be pinned to `DX12` in `pdx_settings.json`, matching the proven
  ANTIQVITAS runtime on this machine. An unset renderer selected Vulkan and
  crashed after custom-map game generation on two bounded M1 attempts.
- A fresh empty-mod paired smoke on 2026-07-28 reached the menu in both control and mod
  modes. The mod introduced zero normalized `error.log` lines.
- Vanilla baseline notices are limited to unavailable store item IDs 3865300 and 3699010
  plus the expected no-mounted-mods diagnostic.

## M1 Proof of Arda

- A custom 16384×8192 RGB location map with exactly 300 live location colors loads into
  the country-selection map and live observer play. The proof classification is 50 sea,
  190 plains, 10 lakes, 20 impassable mountains, and 30 forest locations.
- `wrap_x = no` is accepted. The new-game screen and live session display 3018.1.1; the
  scenario parser accepts an end date of 3200.1.1.
- `nodes.dat` is not required for this reduced custom world. EU5 derives its geometry
  graph during load.
- The minimum functional map also needs valid `definitions.txt`, `default.map`,
  `location_templates.txt`, `ports.csv`, `adjacencies.csv`, named colors, rivers, and
  game-object locators. The proof has 30 provinces and 56 generated coast/port relations.
- Hierarchy membership is unique. Reusing one location under several provinces or areas
  empties every earlier owner and emits `Empty Geography` diagnostics.
- Retail scripts parse geography references even when their content is not active. M1
  therefore generates marked, temporary token-level compatibility overlays for all three
  content roots; M2 removes them through the deliberate quarantine sweep.
- `rivers.png` must be indexed with 255 land, 254 water, and a valid directed source/flow
  graph. A neutral no-river raster loads without river diagnostics.
- Every coastal land location and coastal sea zone requires a `ports.csv` relation; an
  empty file is explicitly crash-unsafe.
- Relocated geometry invalidates city/combat/unit-stack/VFX/dock locators. The engine
  command `MapObjects.GenerateGameLocators <type>` is automatable. For combat and unit
  stacks, completeness means exactly every live location except those listed as
  `impassable_mountains`; M1 therefore emits 280 anchors for each.
- A holy-site definition that points at a removed location can terminate new-game load;
  reduced custom worlds must quarantine or replace all dangling location databases.
- Native trait data supports `is_immortal = yes`. A live conditional test on the
  placeholder ruler emitted `me_m1_immortality_probe_pass` in year 3040.
- `test_log` writes parseable `[TEST_NAME]`, `[CUSTOM_MESSAGE]`, and `[DATE]` records from
  a live observer session. The retail automatic `common/tests` scheduler did not activate
  under the tested command-line combinations; see `BLOCKERS.md`.
- The final 2026-07-29 paired smoke found four fresh vanilla-control line types, zero
  mod-only line types, and one archived baseline type absent. The M1 world is therefore
  zero-new at the menu gate.

## M2 production-map contract

- The real game reaches the menu with an 8192×4096 custom location raster containing
  5,812 live Middle-earth locations: 5,200 passable land, 260 impassable mountains,
  32 lakes, and 320 sea zones.
- The installed parser requires five braced geography levels below the top-level
  continent: subcontinent, region, area, province, and location. ENDÓRË therefore emits
  a continent → subcontinent → region → area → province → location hierarchy even
  though the planning shorthand omits the subcontinent layer.
- A 4096×2048 unsigned 16-bit `heightmap.png` is accepted. The corresponding manual
  `biomes.png` override is one pixel smaller on each axis (4095×2047), matching the
  installed contract; location templates remain the source of gameplay terrain.
- River channels must be one-pixel-wide, four-connected directed paths. Palette index 0
  denotes sources, index 1 explicit joins, indices 4–6 encode channel widths, 254 water,
  and 255 land. Thick antialiased strokes are interpreted as malformed flow graphs.
- Locator completeness is type-specific: city covers passable land; combat and unit
  stacks cover every location except impassable mountains; VFX covers every live
  location, including mountains; dock covers exactly the sea-zone port endpoints.
- Naval ports may terminate only in locations classified under `sea_zones`. A lake
  endpoint caused the dock database to request regeneration, so Esgaroth remains a
  lakeshore settlement without a naval-port edge.
- `ports.csv` must be UTF-8 without a BOM and without a terminal blank record. A trailing
  newline is parsed as an empty location lookup in this build.
- Any non-empty `adjacencies.csv` tested on the production custom canvas—including a
  header-only file and valid authored rows—caused one empty-location lookup. The proven
  safe fallback is an exact zero-byte file; authored Himling and Tolfalas candidates
  remain in generator source for a later map-editor investigation.
- Every passable land location requires a raw material during setup validation. M2 uses
  an explicit temporary `wheat` placeholder alongside safe installed culture and
  religion placeholders; the world-content milestones replace all three.
- Localization keys share an internal hash namespace: two otherwise distinct generated
  keys collided with installed strings and were rejected. Deterministic collision
  detection and suffixing is therefore part of production location generation.
- Retail content still parses named-location references outside the active setup. The
  installed named-color registry can remain defined but unpainted while ENDÓRË colors
  stay disjoint, allowing inherited references to parse without adding Earth geometry.
- The final M2 production-stack paired smoke on 2026-07-29 passed with zero mod-unique
  `error.log` lines.
- One installed `area` cannot contain both sea-zone and non-sea locations. M2 gives sea
  areas a distinct `_sea` domain suffix and generator-checks the invariant.
- A mod file under `main_menu/setup/templates` replaces the corresponding installed
  template directory rather than merging one file. M2 embeds its sanitized technical
  monarchy in the setup country and does not shadow the template directory.
- Country setup definitions load from `in_game/setup/countries`. The M2 gate exact-file
  quarantine keeps one technical `SWE` definition and blanks the remaining Earth country
  setup files; the flag registry alone cannot restrict the country database.
- Retained dynamic-historical-event blocks must remain registered even when disabled.
  Replacing each schedule with an unreachable `SWE` schedule avoids both absent-tag and
  orphan-event diagnostics.
- The deep M2 load requires a technical census covering every retained active culture and
  enabled religion database entry. Pop sizes below `0.01` round to zero in setup.
- The neutral setup needs a sanitized full government, a valid market capital, and
  discovery of all 24 generated regions. A capital alone is not implicitly discovered.
- Retail building potentials can evaluate before every custom location has a market link
  on the first daily tick. Optional `market ?= { ... }` scopes preserve valid behavior and
  prevent invalid-link errors; absent Earth dynasty comparisons in formable triggers must
  likewise be disabled against the neutral no-dynasty setup.
- Final deep verification entered Observer, resolved Minas Tirith, Rivendell, and Orodruin
  through `goto`, and advanced cleanly from 3018.1.1 to 3018.1.9. The only deep-load line
  beyond the paired menu baseline is the machine `AudioArena` allocation notice.

## Binding native physical-map correction

- The earlier reduced-resolution M2 visual gate is superseded. The binding production
  contract uses the installed native raster dimensions: 16384x8192 locations and rivers,
  8192x4096 unsigned 16-bit height and flat map, and 8191x4095 biomes.
- The renderer's sea threshold is explicit installed evidence:
  `NJominiMap.WATERLEVEL = 32 * 0.08340625`, corresponding to raw 16-bit height sample
  5466. Political land classification does not prevent a lower physical height from being
  rendered as water. The generator now requires minimum land >5466 and maximum water
  <5466.
- `gfx/terrain2/terrain_cache` is a 65536x32768 virtual surface with 174,763 indexed
  128-pixel tiles across its mip pyramid. If the mod does not own the complete cache,
  retail Earth relief survives at close zoom. ENDÓRË emits all cache metadata and payloads
  itself and leaves retail index/intensity decal layers explicitly empty.
- Retail `gfx/map/map_objects/generated/*.txt` files reference hundreds of megabytes of
  Earth-authored transform bins. Owning height, flat map, locations, and locators does not
  suppress those objects. Exact overlays for all 41 generated definitions and nine static
  instance definitions remove the Earth placement layer without copying the bins.
- The corrected physical-map re-gate proved separate inland, open-sea, and shoreline
  points in the non-debug renderer. Live Observer advanced the corrected shoreline from
  3018.1.1 to 3018.1.4 with only the established machine baseline lines.

## M3 political-map contract

- The installed setup accepts 38 custom country tags owning 4,189 of the 5,200 passable
  land locations. The remaining 1,011 land locations are deliberately wild; all 260
  impassable mountains, 32 lakes, and 320 sea zones remain unowned.
- The political lookup and 16-bit physical control agree at every owned control pixel:
  200,167 owned pixels, zero at or below raw water sample 5466. Every realm capital is a
  passable-land location; the maximum authored-seat snap distance is 0.021535 normalized
  map units.
- Country-selection and live-Observer labels render over the corresponding colored land
  in both the northern and central/southern theatres. No realm label or capital resolves
  into the sea.
- A non-debug live Observer session advanced from 3018.1.1 through 3018.1.25. The runtime
  `error.log` contained no country, ownership, location, geography, terrain, cache,
  locator, script, culture, religion, pop, or market error.

## M4 peoples-and-faiths contract

- The accepted setup contains 33 cultures in 10 culture groups, 10 language roots with
  33 required dialects, and 10 faiths in three gameplay groups.
- Language-family keys come from a fixed installed registry. ENDÓRË maps eight semantic
  families to those engine adapters and owns their visible localization.
- Culture colors are unique and the deterministic ledgers emit 1,105 localized male,
  female, and house names.
- All 5,200 passable land locations and all 38 country primaries resolve to custom
  Middle-earth cultures and faiths.
- The engine continues to require 2,086 installed culture ABI keys to have populations.
  Size `0.001` rounds away in this build; distributed size `0.01` presences are accepted
  and remain subordinate to size `1.0` custom populations.
- Fresh M5 bookmark initialization rejected 23 size `0.01` inherited-culture ABI pops
  hosted in very small Lossoth locations (0.063k–0.095k authored population), while the
  two larger Lossoth ABI hosts and all hosts elsewhere were accepted. Reducing the same
  locations from eight entries to seven did not change the rejection set, disproving an
  entry-count explanation. ABI hosts are therefore selected only after census allocation
  and must contain at least 1.0k authored population.
- The robust-host census then passed fresh non-debug bookmark initialization with the
  accepted 1,486-byte baseline and zero missing-culture lines. Live Observer advanced to
  3018.2.17 without a census or economy diagnostic.
- Exact overlays for all 29 installed religion files retain their parser symbols but gate
  availability to 3200.1.2, beyond the campaign.
- The actual Culture (Location) and Religion (Location) map modes visibly render custom
  Middle-earth terms across representative northern, eastern, western, and southern land.
- The final non-debug Observer gate advanced from 3018.1.1 to 3018.1.20. Its 1,486-byte
  `error.log` was byte-identical before and after the run.

## Reopened-M2 renderer contracts

- Installed vegetation transform bins are headerless 40-byte records containing ten
  little-endian floats: position xyz, quaternion xyzw, and scale xyz. Installed
  forest/woods/pine definitions use `generated_content=yes` and the exact layers
  `vegetation_high`, `vegetation_medium`, and `vegetation_low`.
- Generated vegetation definitions parse arbitrary mod-owned transform paths without
  diagnostics, but the live renderer did not draw them. Exact retail definition
  filenames, exact retail object names, and exact retail transform-bin path overrides
  also rendered no trees at maximum zoom. These paths are not a proven custom-map
  vegetation mechanism in build 24187685.
- The detailed full-precision height source produced a 116 MB virtual-cache payload at
  256-unit quantization, exceeding GitHub's single-file limit. A 512-unit cache quantum is
  0.78% of the 16-bit engine range and yields an 82.2 MB `heightmap.bin`; the committed
  `heightmap.png` remains full precision.
- In non-debug Observer with the explicit 3D map mode, the custom height and cache produce
  genuinely raised mountain masses visible from a tilted horizon camera. The same live
  evidence shows that current terrain-material transitions follow coarse location-shaped
  patches, while custom trees and major river channels remain visually absent.
- Build 24187685 emits `map.cpp:2698` for every passable land location whose four-connected
  land component contains no legal port. Capital-only connectivity validation is
  insufficient; ENDÓRË now checks every passable location against port components.
- The river parser rejects self-touching meanders. It also rejected every tested custom
  affluent layout, including single red index-1 endpoints orthogonally adjacent to a
  clean parent channel. The green engine raster therefore contains 12 independent major
  source-to-water channels; 23 axes remain in the height/biome drainage control.
- Installed `rivers.png` uses index 4 for the overwhelming majority of upstream flow,
  then transitions through 5 and 11 to 15 on the widest downstream reaches. Sources are
  overwhelmingly adjacent to index 4, while red/yellow junction markers touch all four
  widths. Index 6 is absent from the installed raster and is not a valid basis for the
  previous width heuristic.
- A complete installed-raster graph census gives 693 green index-0 degree-one sources,
  1,286 red index-1 degree-two markers, 129 yellow index-2 degree-two markers, and 1,414
  ordinary river pixels of graph degree three. The installed raster contains 741,652
  4/5/11/15 width-marker pixels; ENDÓRË's proven independent-channel raster contains
  28,512. These counts explain the regional density gap but do not supersede the live
  finding that a single red endpoint beside a clean parent still fails the custom affluent
  parser. A future junction experiment must reproduce a complete retail local grammar,
  not infer safety from marker colors alone.
- Naturalized independent channels are parser-safe when a static graph proof forbids
  repeated pixels, diagonal gaps, non-consecutive orthogonal neighbours, and contact
  between channels. The exact current tree loaded in no-debug Observer with downstream
  4/5/11/15 transitions and zero river diagnostics. This does not change the separate
  finding that custom affluent junctions remain rejected.
- Every independent channel must reach palette-index-254 water. After the west coast
  rewrite, the Baranduin control endpoint remained inland and produced one isolated
  `River source not found`; an engine-only continuation across the coastal plain to open
  water plus a monotonic source at Lake Evendim's southern outlet fixes the contract.
  Equivalent current-coast extensions now complete the Anduin, Ringló, Gilrain, Poros,
  and Harnen without changing their valley-incision axes.
- Installed `materials.bin` payloads are deduplicated 132x132 PNG tiles in unsigned
  16-bit mode. Each pixel is a bitmask over the 16 entries in installed
  `gfx/terrain2/materials.txt`: bits 0-4 coast topography, 5 coast transition, 6
  rivers/lakes, 7 water transition, 8 vegetation transition, 9 climate transition, and
  10-15 material-variation slots.
- ENDÓRË may safely use variation slots 10-12 because every retained gameplay biome
  supplies those material-array positions. Adjacent variation bits can overlap to avoid
  hard threshold bands; the material source must remain continuous and independent of
  location polygons.
- `index_map.bin` is the 16-bit terrain-decal index payload and `intensity_map.bin` is its
  RGBA intensity companion. Empty payloads with complete `.info` indexes are the correct
  no-Earth-decal contract; they are not missing biome or terrain paint.
- A non-debug explicit 3D-map run proved that a populated custom material cache affects
  the real renderer: continuous within-location variation, mountain snow/rock material,
  and shoreline transition bands all appeared where the former shared zero tile did not.
  The exact final refinement still requires a stable multi-theatre visual acceptance run.
- The custom canvas may terminate land at its east and south edges with `wrap_x = no`;
  those borders do not require a surrounding sea ring. A 70.13% land / 29.87% water
  height source reaches menu-ready with 200 sea zones and 495 unique legal ports.
- Build 24187685 reports 32-bit localization hash collisions even for textually distinct
  generated hierarchy keys. `me_belfalas_sea_area_30_21` collides with installed
  `indian_southcurrent23`; the deterministic `_arda` suffix is accepted with zero new
  smoke diagnostics.
- The installed vanilla location raster contains exactly 28,490 locations on the same
  16384×8192 canvas used by ENDÓRË. Matching that count is engine-safe under static
  validation; the current split is 22,000 passable land, 6,000 mountain, 90 lake, and
  400 sea locations.
- Full-precision terrain-cache height tiles (`height_quantum = 1`) produce a
  699,999,471-byte `heightmap.bin` with 123,963 unique height tiles. Generator v18 can
  reuse the verified v17 height payload while independently rebuilding material tiles;
  the cache still has 174,763 indexed entries and empty Earth decal payloads.
- Installed `mountain_wasteland sparse` material slots are ordered snow at bit 10,
  `base_rock_03` at bit 11, and `dirt_dark_transition_01` at bit 12. A generic
  increasing-slot altitude selector therefore inverted high crests into dark rubble;
  explicit physical-height selection is required.
- Vanilla country setup accepts `accepted_cultures = { key }` directly inside a country
  block in `main_menu/setup/start/10_countries.txt`. ENDÓRË uses this ABI for Umbar's
  Black Númenórean noble stratum while retaining Umbarite as the primary culture.
- Logged `MainMenu->Game` state 4 and `ClearAndRecalculateCachedData` completion can
  precede an unresponsive `Loading Savegame — 98%` frame. They are not sufficient
  evidence that country selection is interactive; build 24187685 must keep a responsive,
  rendered game window stable for a bounded interval after those log markers.
- On the exact 28,490-location tree, the 699,999,471-byte q1 height cache exited at that
  98% boundary under both the full visual and lightweight profiles. Retaining the same
  full-precision 65,536×32,768 source while quantizing only the derived cache to q64
  produces 120,118 unique height tiles in 172,161,411 bytes. q64 is 0.098% of the 16-bit
  range and eight times finer than the already live-proven q512 cache. Generator v19
  statically validates all 174,763 indexed entries, 124,205 material tiles, and empty
  Earth decal payloads; retail acceptance remains a separate evidence requirement.
- On source-frame fingerprint `dbd52c52`, a 14,245-location q64 tree passed paired smoke
  with zero mod-unique lines but did not cross the post-cache renderer boundary under
  either the full-visual or lightweight fresh-game profile. Both attempts completed
  setup serialization and `ClearAndRecalculateCachedData`, stayed nonresponsive for the
  full 600-second interactivity bound, and peaked near 23.5 GB working memory without a
  map/terrain/river/locator diagnostic. Build 24187685 therefore requires a lower
  fresh-game runtime envelope even when the map's physical controls are valid.
- Reducing the same source-frame map to 12,104 locations does not materially lower the
  fresh-game renderer peak: no-debug lightweight and debug checkpoint profiles both
  completed setup/cache work, approached 23.5 GB, and missed the same 600-second
  interactivity bound. Location count is not the dominant residency driver for this
  tree; derived map-object population must be tested independently before any further
  political-granularity cut.
- Scaling the exact retail vegetation population from 10,193,212 to 4,077,285 transforms
  lowers the observed debug-checkpoint peak only modestly, to roughly 22 GB, and does not
  produce an interactive post-cache frame within 600 seconds. The object payload is a
  contributor rather than a sufficient explanation. The source-frame tree's 2,700
  impassable mountain locations remain the largest structural difference from the last
  live 12,104 topology, which used 520.
- A priority-9000 biome definition keyed only to the custom `me_arda_surface` climate
  selects one appended 16-channel material array across ordinary and impassable land
  without a parser diagnostic. Fresh no-debug evidence shows that cache variation bits
  then render continuous sand in Harad, ash/rock in Mordor, dense green Mirkwood, and
  mixed Rhûn/Dorwinion ground without the earlier location-shaped transition islands.
- Changing the 1,200 impassable locations from `mountain_wasteland` to neutral `flatland`
  in a fresh New Game did not alter the grey massif shapes. The shapes therefore came
  from the physical height/material source, not from the renderer-facing location
  template. Passability remains independently controlled by `default.map`'s
  `impassable_mountains` section, but template substitution is not a useful repair for
  this visual defect.
- Small engine-water locations can render a cell-shaped terrain bowl even when their
  shoreline material is reduced to the water-transition channel. Neither neutral
  flatland climate nor a lake bed raised immediately below the local dry datum changed
  that bowl; the latter merely removed the visible water surface.
- Build 24187685 renders source-pinned summit relief from the custom q64 height cache:
  fresh close views at Khazad-dûm, Dunharrow, and Goblin-town show physical slopes and
  crests after mountain polygons are reduced to foothill envelopes. The remaining broad
  grey/white failure was materially reduced by requiring local height gradient for
  exposed rock and snow, proving that it was material selection over valid relief rather
  than an inability to mod EU5's physical terrain.
- A centred two-pixel height difference is stable enough to select steep highland
  surfaces at the 8192×4096 material-source resolution without changing the height
  payload. Hard slope thresholds still render as coarse rock ribbons at close zoom;
  acceptance requires feathered ridge-aligned selection rather than a return to
  altitude-only or location-polygon paint.
- Build 24187685 requires appended files under `common/climates` and
  `gfx/map/biome_definitions` to carry a physical UTF-8 BOM even when it can otherwise
  parse them. A custom climate also needs a color distinct from every installed climate
  and both `<key>` and `<key>_desc` localization entries.
- `me_khand_area_33_36_province_02` collides with installed
  `name_milano.serbo_croatian_language` at localization hash 2602704833. Remapping the
  deterministic area stem to `me_khand_area_33_36_arda` removes the generated province
  collision without changing any location key, coordinate, or hierarchy membership.
- In the fixed 1936×1119 release-layout window, the ENDÓRË main-menu controls are centred
  near normalized x `0.14`: Continue y `0.362`, New Game y `0.420`, and Load Game y
  `0.475`. The former y `0.383` target can activate Continue's lower edge and open its
  incompatible-save confirmation. Pixel classification plus Escape cleanup of a retained
  menu is required before waiting on `MainMenu->Game`; log preload alone cannot prove the
  intended click.
- `pathlib.Path("")` resolves to the current working directory and therefore reports that
  it exists. Smoke bootstrap must treat an empty `mod_dir` as invalid explicitly and must
  restore the configured runtime to `G:\endore_user_data` before launching build 24187685.
- `m2_world.py` must author/check `m2_controls.py` before locations and every downstream
  raster. Its former stage list began at locations, so changing control-renderer code and
  invoking a full write could silently reuse committed elevation/biome controls.
- Build 24187685's vanilla Observer start button uses a brighter skin than ENDÃ“RÃ‹: the
  live detector measured dark/gold ratios 0.480/0.152 in vanilla. A valid detector floor
  of dark >=0.38 plus gold >=0.08 accepts both skins. During a fresh transition, logged
  MainMenu-to-Game evidence must be checked before visually classifying a Load Game panel;
  blue loading art can otherwise resemble that panel and abort a healthy new game.
- Equal native-pixel height windows are useful morphology evidence but not literal
  elevation equivalence. At radius 96, installed Shey has upper-half/quarter fractions
  0.232/0.075 and p90 gradient 782; v44 Gundabad had 0.357/0.202 and p90 2,971. ENDÃ“RÃ‹
  therefore did not need a global height escalation. Its renderer defects were broad cap
  area, low along-range crest frequency, and material placement. Conversely, v45 proves
  that high-frequency signed detail which passes 3,175/4,226 p75/p90 global bounds can
  still render as regular terraces in the q64 cache; live spatial-frequency evidence is
  mandatory.
- Build 24187685 loads and plays the 6,004-location custom world with 3,057,385 generated
  vegetation transforms. On fingerprint `06e7c07e`, fresh player-facing New Game reached
  the live Observer HUD in 171.1 seconds; a 45-second playback advanced nine in-game days,
  remained responsive, and used approximately 5.8 GB working set. Full-canopy installed
  `environment_oceanic_wt_tree_01_mesh` and `_02_mesh` references resolve correctly in
  Lothlórien at close zoom, so they are a viable light-trunk deciduous proxy in this build.
- The exact installed `lakes_locators.txt` definition and headerless 40-byte transform ABI
  activate `lake_mesh` on the custom map, but its unit-square carrier remains visibly
  rectangular over shallow sub-location basins at both 0.42 and 0.10 terrain-relative Y
  offsets. Build 24187685 does not depth-clip that carrier tightly enough to reproduce an
  authored pond polygon; the layer must remain quarantined pending a different mechanism.
- The exact installed `generic_rock_generator_high.txt`, `_medium.txt`, and `_low.txt`
  definition filenames activate custom headerless 40-byte transforms on the Arda world.
  A 36,000-record source-clipped population loads cleanly and remains visually sparse.
  The same mechanism is not sufficient evidence of suitability for every retail mesh:
  `vegetation_grass_test_mesh` renders as repeated green shrub-like rosettes at normal
  camera scales, and removing its transforms removes those clumps in a fresh-game A/B.
  Palm/grass exact definitions therefore remain quarantined and their bins absent.
- Build 24187685 safely loads the accepted 12 independent ENDÓRË river channels while 90
  additional source-backed courses remain physical height/material drainage. Increasing
  only those terrain-only masks from 0.62/two pixels to class-aware 0.82/four pixels for
  named drainage and 0.72/three pixels for unnamed drainage does not require a change to
  `rivers.png`. Fresh +12/+14 Observer views show the Brandywine, Celebrant/Anduin,
  lower-Anduin tributaries, and upper Lhûn without broad material corridors.
- At close zoom, independently serialized courses render as blue engine water, whereas
  joined physical courses render as incised rocky/material drainage. This is a useful and
  load-safe visibility distinction, not proof that build 24187685 supports arbitrary
  affluent water graphs; the earlier exact red degree-two endpoint candidate remains
  rejected.
- Build 24187685 resolves an appended terrain material that combines a mod-owned diffuse
  with vanilla's packed `unmasked/ice_normal.dds` and `unmasked/ice_properties.dds` without
  a missing-asset diagnostic. Assigning that material as the sole variation bit over an
  exact land-surface mask preserves irregular sub-location lake outlines. The first
  dirt-normal/muted-teal probe read as mottled ground; a darker blue diffuse plus the
  level unmasked normal reads as water in a fresh calibrated Nindalf A/B. It remains
  terrain, not navigable engine water, and cannot inherit water-location simulation.
- Build 24187685 treats any slot-6 water-material presence as visually dominant rather
  than softly blending it with neighboring terrain bits. A broad mixed mask therefore
  becomes a full blue water band. The accepted presentation uses only a narrow nested
  core; height incision and the surrounding dry terrain provide the wider valley and
  banks.
- The build loads 102 source-aligned material-water cores while `rivers.png` retains only
  twelve independent parser-safe channels. The other joined and terrain-only cores are
  visual terrain and must not be documented as navigable engine river graph edges.
- Build 24187685's F11 finder can accept a query absent from localized location names,
  center an unrelated first result, and leave automation with no error. Generated
  `Land ####` display names are therefore not finder-safe once localization overrides
  their keys. Evidence tooling must validate the actual localized text together with the
  intended source coordinate and strategic region before launching the game.
- Finder focus also selects its own maximum-close camera. Zooming out before a focus and
  then applying positive detents makes nominal regional/close pairs saturate at effectively
  the same close view. Hard-resetting after focus and applying +8/+12 detents produces
  distinct political-map scales but not binding 3D terrain evidence. In build 24187685,
  finder-relative -6 detents provide useful political/regional orientation while -1
  retains a close 3D terrain view.
- Build 24187685's material cache advertises a 65,536×32,768 virtual surface. Feeding its
  close mips from an 8,192×4,096 binary river mask with nearest sampling visibly expands
  each edge pixel into an 8×8 staircase. A full-virtual-resolution one-bit river source
  can replace only channel 6 in mips 0–3 while the general material source remains 8K.
  Fresh v90 evidence shows smooth continuous banks at unchanged normalized widths, and the
  resulting 45,083-unique-tile material cache loads and plays without a new diagnostic.
- Build 24187685 drops ENDÓRË's physical forest objects between the finder-created
  maximum-close camera and a one-detent zoom-out, even though the forest ground response,
  height relief, and river material remain visible. A one-detent forest frame can
  therefore falsely appear treeless. Forest-object evidence must use the finder maximum;
  the independently reset regional frame supplies orientation rather than object-density
  proof.
