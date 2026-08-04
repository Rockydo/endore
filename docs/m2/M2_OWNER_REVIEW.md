# M2 map review — current handoff

Status: M2 remains the sole active content gate. The physical map loads, ticks, and has
passed the complete deterministic and real-game checks; the remaining work is deliberate
source-anchored fidelity iteration, not an unresolved load or vanilla-Earth problem. Do
not begin gameplay, faction-mechanic, or art content until this review is explicitly
closed.

## Current published baseline

- Current commit: `2b6e9ea` (`test(map): lock Great River width hierarchy`).
- Current game-visible tree fingerprint:
  `d511971af16d7b24784ebdf99f9493d7e039f46795d6333b68fd066a1a5f568e`.
- Game build: `24187685` (`1.3.11`, Pavia).
- World: 6,004 locations; 38 playable realms; 3,029 assigned land locations and 2,975
  deliberately wild locations.
- River raster: 16 source-to-water systems, 38 incoming red confluences, two yellow
  outgoing distributaries, 56 genuine engine courses, and zero graph cycles.
- Water material: 61,432 indexed-river pixels projected by exact nearest-neighbour
  sampling only. There is no independently painted blue shoulder or parallel proxy
  channel.

The physical controls are hash-pinned to the owner-approved Arda Maps Third Age topology
and ArdaCraft coordinate/relief/biome/drainage controls. The repository contains derived
numeric controls, never downloaded reference artwork or map imagery. See
[`CARTOGRAPHY_REFERENCE_LEDGER.md`](../world/CARTOGRAPHY_REFERENCE_LEDGER.md) and
[`V113_SOURCE_PROVENANCE_REAUDIT.md`](V113_SOURCE_PROVENANCE_REAUDIT.md).

## What is proven

| Area | Current evidence |
| --- | --- |
| Map identity | v110's fresh nine-theatre Observer atlas confirms fully custom Middle-earth terrain, coasts, vegetation, and decals at close zoom; no vanilla-Earth underlay. |
| Terrain presentation | v115 proves the player-facing visual profile renders physical ground, relief, materials, and vegetation at close zoom. The far political view is intentionally a strategic overlay. |
| Mountains | Source-pinned Misty, White, northern, and Mordor ranges render as relief; v112 adds a marker-offset proof that Erebor is a compact isolated Lonely Mountain. |
| Forests | v110's Mirkwood/Lothlórien views confirm dense, distinct canopy. Lothlórien stays inside the Golden Wood/Naith source mask rather than crossing the Misty crest. |
| Rivers | v105 replaced the rejected blue-width surrogate with the installed indexed-raster grammar. v109 adds the source-exact Ethir fork; v120 now fails validation if the continuous Langwell–Anduin trunk loses its dominant widest-class segment. |
| Political map | v118 corrects five named frontier witnesses; v119 protects fourteen unclaimed, abandoned, or independent sites and makes Eagles' Eyrie empty of mortal population. Compact Lothlórien, Dunland, Erebor, Isengard, and source-enclosed Mordor contracts remain in force. |
| Runtime | v119 full validation passed in 458.8 seconds. Paired vanilla/ENDÓRË smoke reached menu-ready with zero new mod-unique error-log lines on the current game-visible fingerprint. |

The direct Finder typing route remains blocked by the native edit control and correctly
fails closed; it must not be used to assert a source camera position. This does not affect
the established camera evidence, smoke, or normal player map interaction. See
[`BLOCKERS.md`](../../BLOCKERS.md).

## Reproduce the player-facing physical view

With EU5 closed, from `G:\EUV mods\endore`:

```powershell
.\.venv\Scripts\python.exe tools\gamedriver.py profile visual
.\.venv\Scripts\python.exe tools\gamedriver.py launch --mode mod --visual-map --no-debug-mode
```

The smoke profile deliberately lowers terrain settings for fast automated load checks;
the visual profile restores close 3D terrain and triplanar materials. The stored profile
changes only ENDÓRË's player-facing visual keys and does not replace audio, display, or UI
preferences.

## Evidence index

| Evidence | Binding purpose |
| --- | --- |
| [`V105_RIVER_GATE.md`](V105_RIVER_GATE.md) | First genuine indexed-river proof: connected engine courses, widest Anduin class, no painted proxy. |
| [`V106_TRIBUTARY_GATE.md`](V106_TRIBUTARY_GATE.md) | Source-backed tributary and confluence expansion without decorative drainage. |
| [`V109_NESTED_DISTRIBUTARY_GATE.md`](V109_NESTED_DISTRIBUTARY_GATE.md) | Current Ethir distributary grammar: two source-exact, acyclic outgoing branches. |
| [`V110_FULL_PHYSICAL_ATLAS.md`](V110_FULL_PHYSICAL_ATLAS.md) | Complete fresh continent, hydrology, forest, relief, and playback review. |
| [`V112_EREBOR_RELIEF_EVIDENCE.md`](V112_EREBOR_RELIEF_EVIDENCE.md) | Source-marker-offset Lonely Mountain close view. |
| [`V113_SOURCE_PROVENANCE_REAUDIT.md`](V113_SOURCE_PROVENANCE_REAUDIT.md) | Exact upstream source-byte re-audit. |
| [`V115_RENDER_VISIBILITY_PROBE.md`](V115_RENDER_VISIBILITY_PROBE.md) | Player visual-profile close-render proof. |
| [`V118_POLITICAL_FRONTIER_WITNESSES.md`](V118_POLITICAL_FRONTIER_WITNESSES.md) | Exact settled-frontier ownership corrections. |
| [`V119_UNCLAIMED_SITE_AUDIT.md`](V119_UNCLAIMED_SITE_AUDIT.md) | Exact wilderness/empty-site corrections. |

Screenshots live under ignored `docs/screens/` directories as reproducible development
evidence rather than shipped assets. Static acceptance never replaces a live test; each
new game-visible map batch still requires `gmake validate`, `gmake smoke`, and an exact
fingerprint smoke assertion before publication.

## Review standard and next work

Judge the close physical map against the hash-pinned Third Age Arda Maps control and
equal-scale ArdaCraft placement, with Tolkien's text and map retaining canon precedence.
A valid correction must identify a named landmark, coastline, ridge, forest boundary,
river course, or TA 3018 ownership witness; it must not use a broad cosmetic rectangle or
invent a state merely to tidy colours.

The next source review remains Dunland, Lothlórien, the Dale/Erebor theatre, Mordor, and
the represented East. Preserve the accepted coastline, relief, forest, river, and
location-topology controls. Where sources establish geography but not a cadastral claim,
leave the land wild and record the judgement rather than painting a speculative border.
