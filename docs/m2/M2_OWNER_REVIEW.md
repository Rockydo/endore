# M2 owner review — current physical map

Status: awaiting explicit owner acceptance. This page does not make the gate green.

## Exact candidate

- Game-visible fingerprint:
  `0ef39c3b6c40a8dcc2f224b204a542e38f6432982e2477ba41199ebafd84c69d`
- Generator: v53 native-resolution river banks over the accepted source-complete physical
  map.
- Runtime proof: fresh HUD-proven Observer, repeated 45-second maximum-speed playback,
  zero recovery, unchanged 1,486-byte baseline error log, full validation, paired smoke,
  and exact smoke assertion.

## Launch with physical terrain enabled

Close EU5 first. From `G:\EUV mods\endore`, restore the player-quality visual profile:

```powershell
.\.venv\Scripts\python.exe tools\gamedriver.py profile visual
```

Then launch the current mod through the shared leased driver:

```powershell
.\.venv\Scripts\python.exe tools\gamedriver.py launch --mode mod --visual-map --no-debug-mode
```

The smoke profile deliberately disables expensive terrain. A manual launch that inherits
those keys can show the political map but no close 3D terrain; that is a configuration
state, not map evidence. The profile command changes only player-facing visual keys and
does not overwrite personal audio, display-mode, or UI choices.

## Evidence index

| Evidence | Binding purpose |
| --- | --- |
| `docs/screens/20260803_v90_native_river_edges/` | Same-camera proof that native-resolution river banks remove 8×8 teeth while preserving widths. |
| `docs/screens/20260803_v91_full_atlas/` | Complete nine-theatre orientation plus core hydrology coverage. Three misleading feature-camera conclusions are superseded by v91b. |
| `docs/screens/20260803_v91b_camera_calibration/` | Maximum-close forests, Edhellond land, and exact Orodruin physical evidence. |
| `docs/screens/20260803_v92_remaining_drainage/` | Remaining twelve source-bound drainage pairs and complete 102-course review. |

Screenshots are reproducible, ignored working evidence rather than shipped mod payload.
Regional frames establish position and political context; the corresponding close frames
are binding for terrain, relief, forest objects, coast, and river presentation.

## Review standard

Compare the live close physical map against the pinned Third Age Arda Maps control and
the equal-scale Ardacraft placement already recorded in the source ledger. Report a defect
with a named landmark, coast, ridge, forest, realm boundary, or river and its approximate
screen position. That gives the next iteration a falsifiable source comparison.

The current technical review supports these statements:

- no vanilla Earth terrain remains beneath the political map;
- the coast, ridges, passes, forests, climate materials, small water, and 102-course
  drainage system come from the committed Middle-earth controls;
- Anduin is the broad dominant river, while named trunks and tributaries retain a readable
  lore-compatible hierarchy;
- all 38 realm assignments satisfy their source/anchor contracts with no unreviewed
  political component.

Explicit owner acceptance is still required by the reopened M2 gate. Until then, M2 is
red and gameplay, faction expansion, mechanics, bespoke art, and lore-content production
remain prohibited.
