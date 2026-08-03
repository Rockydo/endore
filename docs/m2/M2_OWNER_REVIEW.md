# M2 owner review — current physical map

Status: rejected by direct owner review; the gate remains red.

## Exact candidate

- Game-visible fingerprint:
  `6572f6400849e103c54fdf526f0dbc8325713d38ad64b98451da38e25a46ba1b`
- Generator: v54 native-resolution river banks plus the rejected-as-final Great River
  scale, with v94's compact Nan Curunir political correction.
- Runtime proof: fresh HUD-proven Observer, repeated 45-second maximum-speed playback,
  zero recovery, unchanged 1,486-byte baseline error log, 446.0-second full validation,
  221.8-second paired zero-new-line smoke, and exact smoke assertion.

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
| `docs/screens/20260803_v93_anduin_scale/` | Same-camera owner-calibrated upper/lower Anduin scale and clean 45-second playback. |
| `docs/screens/20260803_v94b_gap_political/` | Final-fingerprint source-bound Fords regional/close pair proving compact Isengard, separate Dunland/Fangorn/Rohan, live terrain, and clean playback. |

Screenshots are reproducible, ignored working evidence rather than shipped mod payload.
Regional frames establish position and political context; the corresponding close frames
are binding for terrain, relief, forest objects, coast, and river presentation.

## Review standard

Compare the live close physical map against the pinned Third Age Arda Maps control and
the equal-scale Ardacraft placement already recorded in the source ledger. Report a defect
with a named landmark, coast, ridge, forest, realm boundary, or river and its approximate
screen position. That gives the next iteration a falsifiable source comparison.

The current technical review supports these statements, but not visual acceptance:

- no vanilla Earth terrain remains beneath the political map;
- the coast, ridges, passes, forests, climate materials, small water, and 102-course
  drainage system come from the committed Middle-earth controls;
- the 102 committed courses are source-backed and connected, but direct player review
  still finds Anduin visibly too narrow and the overall tributary/affluent network too
  sparse at ordinary close play zoom;
- all 38 realm assignments satisfy their source/anchor contracts with no unreviewed
  political component; Isengard is a compact 13-location Nan Curunir claim and the Fords
  resolve outside it.

The next hydrology pass must compare rendered width and visible network density—not only
control-raster completeness—against both accepted map sources. Additional courses must be
source-traced or lore-attested; no decorative drainage is permitted. Explicit owner
acceptance is still required. Until then, M2 is red and gameplay, faction expansion,
mechanics, bespoke art, and lore-content production remain prohibited.
