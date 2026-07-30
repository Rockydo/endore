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
  source-to-water channels using installed width indices 4â€“6; 23 axes remain in the
  height/biome drainage control.
- Every independent channel must reach palette-index-254 water. After the west coast
  rewrite, the Baranduin control endpoint remained inland and produced one isolated
  `River source not found`; an engine-only continuation across the coastal plain to open
  water plus a monotonic source at Lake Evendim's southern outlet fixes the contract
  without changing its valley-incision axis. Paired smoke then produced zero mod-unique
  lines.
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
