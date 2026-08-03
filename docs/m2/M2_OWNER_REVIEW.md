# M2 owner review — current physical map

Status: the v101 map payload awaits direct owner re-review. v99 is the complete physical
atlas; v100 adds compact Erebor; v101 contracts Mordor to the shared mountain enclosure.
The previous v93 rejection keeps the gate red until the owner explicitly accepts the
current result.

## Exact candidate

- Game-visible fingerprint:
  `3dbe7354260c77ea57bcdacfc4df62ec0a7a7ef07c2a930db5a7db94b879fd63`
- Generator: v56 native-resolution river cores, enlarged Great River hierarchy, 102
  reviewed Arda Maps courses, and 61 curated source-connected Ardacraft affluents, with
  v94's compact Nan Curunir, v100's compact Erebor, and v101's source-enclosed Mordor
  political corrections.
- Runtime proof: v98 supplied eight source-bound river camera pairs; v99 independently
  supplied the full map, all nine regional/close theatre pairs, four core hydrology pairs,
  and focused close pairs for Lothlorien, Gundabad, Erebor, Mirrormere, and Nindalf.
  v100 supplied a fresh regional/close Erebor pair; v101 supplied a fresh regional/close
  Mordor pair after binding its politics to the shared mountain ring. All HUD-proven
  Observer sessions completed 45-second maximum-speed playback with zero recovery and the
  normal 1,486-byte log. The final v101 candidate passes paired vanilla/mod smoke with
  zero new error lines.

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
| `docs/screens/20260803_v98_curated_affluents/` | Current upper/lower Anduin and six other course pairs after rejecting blocky v95-v97 feeder mechanisms. |
| `docs/screens/20260803_v99_full_atlas/` | Current-fingerprint full map, all nine theatre pairs, four core hydrology pairs, and focused Lothlorien/Gundabad/Erebor/Mirrormere/Nindalf physical pairs; clean 45-second playback. |
| `docs/screens/20260803_v100_compact_erebor/` | Fresh regional/close proof that Erebor is a compact nine-cell holding around its unchanged isolated summit; clean 45-second playback. |
| `docs/screens/20260803_v101_mordor_enclosure/` | Fresh regional/close proof that Mordor follows its mountain-enclosed basin with separate canonical western outposts; Orodruin retained; clean 45-second playback. |

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
- the 102 committed courses remain source-backed and connected; v98 makes Anduin visibly
  dominant and adds only 61 directly source-connected, unnamed affluents after rejecting
  three denser but artificial-looking mechanisms;
- v99 close frames independently show dense Mirkwood and Lothlorien canopies, fully 3D
  Misty/White/northern relief, isolated Erebor, exact small-water material at Mirrormere
  and Nindalf, and dominant upper/lower Anduin width on the unchanged candidate;
- all 38 realm assignments satisfy their source/anchor contracts with no unreviewed
  political component; Isengard is a compact 13-location Nan Curunir claim and the Fords
  resolve outside it; Erebor is a compact nine-location Lonely Mountain claim, while Dale
  and the Iron Hills remain separate and unchanged; Mordor's 296-location main body shares
  the accepted Ered Lithui/Ephel Dúath ring and retains only source-bound western outposts.

Review v98's rendered width and visible network density against both accepted map sources.
Additional courses remain prohibited unless source-traced or lore-attested; no decorative
drainage is permitted. Explicit owner acceptance is still required. Until then, M2 is red
and gameplay, faction expansion, mechanics, bespoke art, and lore-content production
remain prohibited.
