# M1 — Proof of Arda

Gate date: 2026-07-29
Binding physical re-gate: 2026-07-29

## Result

PASS, after explicit visual invalidation and correction.

The initial 300-location spike proved that custom location geometry, dates, Observer mode,
and runtime assertions work, but its political-map screenshots were not sufficient proof
of a custom physical world. Owner close-zoom review correctly rejected the later production
view: authored political land was physically underwater and retail Earth-authored map
objects still survived underneath.

The binding proof now loads the native-resolution production world with a recognizable
Middle-earth silhouette, dry authored land, authored water, a custom close-zoom cache, and
no retail Earth relief or generated object placement. It starts on 3018.1.1, declares
3200.1.1 as its end, does not wrap horizontally, enters live Observer, and advances time.
The sole installed tag remains technical setup scaffolding, not faction content.

## Binding map manifest

- Location/rivers canvas: 16384x8192
- Height/flat-map canvas: 8192x4096
- Biome canvas: 8191x4095
- Authored controls: 1024x512
- Locations: 5,812
- Classes: 5,200 passable land, 260 impassable mountains, 32 lakes, 320 sea zones
- Canon settlement anchors: 41
- Installed raw-height waterline: 5466
- Generated minimum land / maximum water: 10477 / 420
- Virtual terrain surface: 65536x32768, 174,763 indexed tiles
- Retail decal layers retained: zero
- Earth map-object definitions suppressed: 41 generated + 9 static

## Real-game evidence

The first three frames preserve the original engineering spike. Frames 04–08 supersede
its visual evidence:

- [Original spike world map](screenshots/01_world_map_ta3018.png)
- [Original live Observer entry](screenshots/02_observer_live_ta3018.png)
- [Original Observer time advance](screenshots/03_observer_running.png)
- [Corrected native full-map silhouette](screenshots/04_native_full_map_corrected.png)
- [Corrected close physical land, with Earth objects removed](screenshots/05_native_close_land_corrected.png)
- [Corrected close open sea](screenshots/06_native_close_open_sea.png)
- [Corrected close authored shoreline](screenshots/07_native_close_shoreline.png)
- [Corrected live Observer on 4 January 3018](screenshots/08_observer_corrected_3018_01_04.png)
- [Parseable runtime test results](evidence/runtime_test_results.txt)

The corrected shoreline frame demonstrates the political/physical transition directly.
The Observer frame advanced from 08:00 on 1 January to 18:00 on 4 January 3018. The
runtime assertions separately prove that the live `test_log` sink executes and that
native `is_immortal = yes` satisfies the conditional immortality probe.

## Gate checks

- `gmake validate`: PASS
- Paired vanilla/mod `gmake smoke`: PASS, zero mod-only normalized `error.log` lines
- Complete custom virtual terrain cache: PASS
- Retail Earth generated/static map-object quarantine: PASS
- Full-map, inland, open-sea, and shoreline non-debug renderer series: PASS
- Live Observer entry and time advance: PASS
- Parseable live-engine assertion: PASS

## Reproduction

```text
.\.venv\Scripts\python.exe tools\m2_controls.py --write
.\.venv\Scripts\python.exe tools\m2_world.py --write
gmake validate
gmake smoke
.\.venv\Scripts\python.exe tools\gamedriver.py start-observer
```

No realm, mechanic, narrative, or art milestone may use the earlier political-only
screenshots as map acceptance evidence.
