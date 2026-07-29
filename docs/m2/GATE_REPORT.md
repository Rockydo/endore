# M2 Gate Report

Milestone M2 was script/runtime-green on 2026-07-29, then returned to red when owner
close-zoom review exposed a physical-map mismatch. This report records the binding
same-day correction against Europa Universalis V 1.3.1.1 (Pavia), Steam build 24187685.

## Defect and disposition

The custom political raster showed a recognizable Middle-earth silhouette, but most
ordinary land heights were below the installed renderer's waterline. Close zoom therefore
showed water beneath political land. Retail generated vegetation/static object definitions
also fell through the VFS and placed Earth-authored transforms on the custom surface.

Both defects are closed:

- generated lowland is now at least raw height 10477 versus installed waterline 5466;
- generated water is at most 420;
- the complete 65536x32768 terrain virtual surface is owned by the mod;
- retail decal index/intensity layers are explicitly empty;
- all 41 retail generated map-object definitions and nine static Earth definitions have
  exact comment-only overlays, leaving their transform bins unreachable.

## Generated world

- Location/rivers raster: 16384x8192
- Height/flat-map raster: 8192x4096
- Biome raster: 8191x4095
- Total locations: 5,812
- Passable land: 5,200
- Impassable mountains: 260
- Lakes: 32
- Sea zones: 320
- Canon settlement anchors: 41
- Continents / subcontinents / regions: 6 / 6 / 24
- Sea-zone ports: 407
- Model SHA-256:
  `e38937c1a653696f099411fbd7e6a4b577bbca2a80d41492a219da7b1bb17822`

## Real-game verification

The automated non-debug visual-map driver proved the same generated world at four scales:
full political silhouette, close physical land, close physical open sea, and the exact
shoreline transition. Unlike the rejected evidence, the close frames also ran with all
retail Earth map-object transforms suppressed.

The corrected shoreline entered live Observer and advanced from 08:00, 1 January 3018 to
18:00, 4 January 3018. The runtime log contained only established machine/control lines:
DX12 feature-query failure, unavailable DLC store entries, and the `AudioArena` allocation
notice. It contained no script, geography, terrain-cache, locator, country, culture,
religion, pop, market, building, or dangling-reference diagnostic.

The earlier named-location deep test remains valid: the engine resolved Minas Tirith,
Rivendell, and Orodruin and advanced to 3018.1.9. The corrected visual re-gate adds the
physical evidence that test lacked.

## Binding evidence

- [Corrected native full-map silhouette](../m1/screenshots/04_native_full_map_corrected.png)
- [Corrected close physical land](../m1/screenshots/05_native_close_land_corrected.png)
- [Corrected close open sea](../m1/screenshots/06_native_close_open_sea.png)
- [Corrected close authored shoreline](../m1/screenshots/07_native_close_shoreline.png)
- [Corrected live Observer on 4 January 3018](../m1/screenshots/08_observer_corrected_3018_01_04.png)

The earlier `world_map_in_game.png`, `observer_live.png`, and `time_advanced.png` remain
historical deep-load evidence but are not sufficient physical-map acceptance evidence.

## Gate checks

- `gmake validate`: PASS
- Paired vanilla/mod `gmake smoke`: PASS, zero mod-only normalized `error.log` lines
- Non-debug physical renderer series: PASS
- Live Observer time advance: PASS
- No retail Earth terrain/cache/object placement: PASS
