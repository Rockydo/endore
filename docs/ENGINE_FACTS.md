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
