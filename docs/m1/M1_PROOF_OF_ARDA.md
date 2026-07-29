# M1 — Proof of Arda

Gate date: 2026-07-29

## Result

PASS. EU5 loads a new, recognizable Middle-earth-shaped world with exactly 300 live
locations. The scenario starts on 3018.1.1, declares 3200.1.1 as its end, does not wrap
horizontally, enters live Observer mode, and advances time. The proof is intentionally
crude and contains no final factions, mechanics, art, or lore content.

## Map manifest

- Canvas: 16384×8192 RGB
- Coarse authored grid: 512×256
- Locations: 300
- Classes: 50 sea, 190 plains, 10 lakes, 20 impassable mountains, 30 forest
- Provinces: 30
- Coast/port relations: 56
- Placeholder setup: one temporary installed tag, one market/town, 220 owned land cells
- Derived graph cache: no committed `nodes.dat`
- Compatibility layer: generated, manifest-tracked, M1-only; mandatory removal in M2

## Real-game evidence

- [World map at TA 3018](screenshots/01_world_map_ta3018.png)
- [Live Observer entry](screenshots/02_observer_live_ta3018.png)
- [Observer running on 5 January 3018](screenshots/03_observer_running.png)
- [Parseable runtime test results](evidence/runtime_test_results.txt)

The runtime assertions prove that the live `test_log` sink executes and that a character
with the native `is_immortal = yes` trait satisfies the conditional immortality probe.

## Gate checks

- `gmake validate`: PASS
- Paired vanilla/mod `gmake smoke`: PASS, zero mod-only normalized `error.log` lines
- Real-game map-screen series: PASS
- Live Observer entry and time advance: PASS
- Parseable live-engine assertion: PASS

## Reproduction

```text
gmake validate
gmake smoke
.\.venv\Scripts\python.exe tools\gamedriver.py observer
```

The generator entry point is:

```text
.\.venv\Scripts\python.exe tools\m1_proof_map.py --write
.\.venv\Scripts\python.exe tools\m1_proof_map.py --check
```

M2 replaces the proof raster, hierarchy, placeholder setup, and all compatibility
overlays with the production map pipeline before any realm or lore content is added.
