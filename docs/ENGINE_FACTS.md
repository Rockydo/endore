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
