# M2 owner review — current physical map

Status: the v103 map payload awaits direct owner re-review. v99 is the complete physical
atlas; v100 adds compact Erebor; v101 contracts Mordor to the shared mountain enclosure;
v102 contracts Mount Gram to a remnant holding and restores its namesake summit; v103
makes Anduin unmistakably dominant and expands only source-connected affluents. The
previous v93 rejection keeps the gate red until the owner explicitly accepts the current
result.

## Exact candidate

- Game-visible fingerprint:
  `76fb6e7e104c9c82d33162ed17e690554e622ace6e335a104eaec94d6be1ff84`
- Generator: v57 native-resolution river cores, enlarged Great River hierarchy, 102
  reviewed Arda Maps courses, and 104 curated source-connected Ardacraft affluents, with
  v94's compact Nan Curunir, v100's compact Erebor, and v101's source-enclosed Mordor
  political corrections. v102 adds an 18-location Mount Gram remnant plus forced Carn Dûm
  and one compact lore-attested, relief-only Mount Gram summit. Upper/lower Anduin cores
  use `1.10/1.15` scale and wet banks use `1.35/1.50`; all other nominal source-course
  widths and the twelve parser channels remain unchanged.
- Runtime proof: v98 supplied eight source-bound river camera pairs; v99 independently
  supplied the full map, all nine regional/close theatre pairs, four core hydrology pairs,
  and focused close pairs for Lothlorien, Gundabad, Erebor, Mirrormere, and Nindalf.
  v100 supplied a fresh regional/close Erebor pair; v101 supplied a fresh regional/close
  Mordor pair after binding its politics to the shared mountain ring. All HUD-proven
  Observer sessions completed 45-second maximum-speed playback with zero recovery and the
  normal 1,486-byte log. v102 supplies a fresh same-camera Mount Gram pair and another
  clean 45-second run on that exact candidate. v103 supplies eight final-fingerprint
  regional/close hydrology pairs after the dependent 3,493,385-transform vegetation layer
  was regenerated around the new water mask. Its 45-second maximum-speed playback had
  zero recovery and the normal 1,486-byte log; full validation passed in 470.4 seconds and
  paired smoke passed in 202.4 seconds with zero new mod error lines. The v102 paired-smoke
  request had first deferred when
  Antiquitas acquired the shared lease immediately after capture; the pending fingerprint
  then ran when the slot cleared and passed in 201 seconds with zero new mod error lines.

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
| `docs/screens/20260803_v102_mount_gram_final/` | Fresh same-camera proof of the compact Mount Gram remnant, separate Carn Dûm, and an isolated physical namesake summit; clean 45-second playback. |
| `docs/screens/20260803_v103_hydrology_final/` | Final-fingerprint upper/lower Anduin plus six independent basin pairs after affluent expansion and vegetation-clearance regeneration; clean 45-second playback. |

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
- the 102 committed courses remain source-backed and connected; v103 makes Anduin visibly
  dominant and adds only 104 directly source-connected, unnamed affluents after rejecting
  three denser but artificial-looking mechanisms;
- v99 close frames independently show dense Mirkwood and Lothlorien canopies, fully 3D
  Misty/White/northern relief, isolated Erebor, exact small-water material at Mirrormere
  and Nindalf; v103 final frames show the enlarged upper/lower Anduin hierarchy and clean
  regenerated vegetation clearance on the current candidate;
- all 38 realm assignments satisfy their source/anchor contracts with no unreviewed
  political component; Isengard is a compact 13-location Nan Curunir claim and the Fords
  resolve outside it; Erebor is a compact nine-location Lonely Mountain claim, while Dale
  and the Iron Hills remain separate and unchanged; Mordor's 296-location main body shares
  the accepted Ered Lithui/Ephel Dúath ring and retains only source-bound western outposts;
  Mount Gram is a compact 17-location main holding plus exact one-location Carn Dûm, with
  the summit changing relief but not passability topology.

Review v103's rendered width and visible network density against both accepted map sources.
Additional courses remain prohibited unless source-traced or lore-attested; no decorative
drainage is permitted. Explicit owner acceptance is still required. Until then, M2 is red
and gameplay, faction expansion, mechanics, bespoke art, and lore-content production
remain prohibited.
