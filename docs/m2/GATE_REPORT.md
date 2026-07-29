# M2 Gate Report

Milestone M2, the production Middle-earth world, passed its deep real-game gate on
2026-07-29 against Europa Universalis V 1.3.1.1 (Pavia), Steam build 24187685.

## Generated world

- Location raster: 8192×4096
- Total locations: 5,812
- Passable land: 5,200
- Impassable mountains: 260
- Lakes: 32
- Sea zones: 320
- Canon settlement anchors: 41
- Continents / subcontinents / regions: 6 / 6 / 24
- Sea-zone ports: 417
- Model SHA-256:
  `ffa5374bd9d080f2fc53db32144df2ee61c609d79825b74748138bff4d684818`

## Real-game verification

The automated driver launched the enabled mod, reached the country-selection map,
entered Observer mode, and loaded the complete production world. The debug console then
resolved and navigated to these authored anchors:

- location 3246 — Minas Tirith
- location 2095 — Rivendell
- location 4008 — Orodruin (`mount_doom`)

The live simulation advanced from 08:00, 1 January 3018 to 13:00, 9 January 3018.
No line was added to `error.log` during those eight days. The only post-menu diagnostic
in the deep-load snapshot is the machine/engine `AudioArena` allocation notice; there are
no script, dangling-reference, geography, locator, country, culture, religion, pop,
market, building, town, capital-discovery, or unused-database diagnostics.

The direct live `test_log` effect parsed without an error when sent through the
clipboard-preserving console path. Named navigation and eight clean simulated days are
the required in-game map test.

## Evidence

- `world_map_in_game.png` — production-world map view in live Observer
- `observer_live.png` — final Observer session at the 3018.1.1 gate
- `time_advanced.png` — paused live session on 3018.1.9
- `deep_error.log` — final deep-load/tick diagnostic snapshot

SHA-256:

- `deep_error.log`:
  `bacf647bd82cea504863158d3a72c042a406c8d0ea953b084a2ddcdf2abfa103`
- `observer_live.png`:
  `87544f2ad1f5fef524394a07231846f00ebb289aeca5e8806dce9de17c914391`
- `time_advanced.png`:
  `34298fff331af06b446a036b8c7613413209d9bf34c9ef1e8db3910aef0cba20`
- `world_map_in_game.png`:
  `678d329d46621f68ac756ccd3089efa14847849817e3da5582fb3acf08d33153`

The canonical `gmake validate` and paired `gmake smoke` results are recorded in the
milestone commit and `docs/PROGRESS.md`.
