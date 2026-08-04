# M2 map review — current handoff

Status: M2 remains the sole active content gate. The physical map loads, ticks, and has
passed the complete deterministic and real-game checks; the remaining work is deliberate
source-anchored fidelity iteration, not an unresolved load or vanilla-Earth problem. Do
not begin gameplay, faction-mechanic, or art content until this review is explicitly
closed.

## Current published baseline

- Current published revision: v129 native river surface isolation.
- Current game-visible tree fingerprint:
  `d021a02eea707cf6581f5fc0d730480f852c58720951400998a867941ac6e696`.
- Game build: `24187685` (`1.3.11`, Pavia).
- World: 6,004 locations; 38 playable realms; 3,027 assigned locations and 2,977
  deliberately wild locations.
- River raster: 16 source-to-water systems, 38 incoming red confluences, two yellow
  outgoing distributaries, 56 genuine engine courses, and zero graph cycles.
- River surface: v129 removes the duplicate terrain-cache channel-6 footprint entirely.
  The native indexed renderer is the only water and width authority; source terrain remains
  beneath it and no blue terrain proxy is permitted.

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
| Rivers | v129 makes the installed indexed-raster grammar exclusive: the cache has zero duplicate river-material pixels. v109 adds the source-exact Ethir fork; v120 now fails validation if the continuous Langwell–Anduin trunk loses its dominant widest-class segment. |
| Political map | v127 makes 96 named-landmark ownership dispositions auditable and adds a permanent six-theatre frontier audit. It preserves compact Lothlórien, Dunland, Moria, Erebor, Dale, Esgaroth, Iron Hills, Isengard, and source-enclosed Mordor while retaining canonically uncertain land as wild. |
| Runtime | v129 full validation passed in 539.8 seconds. Paired vanilla/ENDÓRË smoke reached menu-ready with zero new mod-unique error-log lines on the current game-visible fingerprint. |

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
| [`V124_NATIVE_RIVER_SURFACE_FIX.md`](V124_NATIVE_RIVER_SURFACE_FIX.md) | Native water/width versus dry terrain-bank responsibility correction. |
| [`V129_INDEXED_RIVER_SURFACE_ISOLATION.md`](V129_INDEXED_RIVER_SURFACE_ISOLATION.md) | v124 supersession: native indexed raster is the only river surface. |
| [`V125_NAMED_GATE_AND_RIDGE_CONTROL_AUDIT.md`](V125_NAMED_GATE_AND_RIDGE_CONTROL_AUDIT.md) | Exact Black Gate/Morgai control and compact-Isengard ridge correction. |
| [`V126_COMPLETE_LANDMARK_CONTROL_AUDIT.md`](V126_COMPLETE_LANDMARK_CONTROL_AUDIT.md) | Complete 89-landmark control ledger and five corrected exact political cells. |
| [`V127_FRONTIER_GAZETTEER_AND_CONTROL.md`](V127_FRONTIER_GAZETTEER_AND_CONTROL.md) | Seven added exact source landmarks and 96-row control ledger. |
| [`V128_FRONTIER_THEATRE_AUDIT.md`](V128_FRONTIER_THEATRE_AUDIT.md) | Six fail-closed source review scopes for political containment and landmark control. |
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

The named control ledger now covers the immediate frontier evidence. The next source
review remains exact-border reconciliation within Dunland, Lothlórien/Moria,
Dale/Erebor, Mordor/Ithilien, and the represented East and South. Preserve the accepted
coastline, relief, forest, river, and location-topology controls. Where sources establish
geography but not a cadastral claim, leave the land wild and record the judgement rather
than painting a speculative border.
