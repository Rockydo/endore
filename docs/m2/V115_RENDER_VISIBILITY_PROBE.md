# v115 player-facing terrain visibility probe

## Purpose

Resolve the reported discrepancy between the flat-looking strategic political
overview and the expected close-scale physical map without changing any map
asset, camera target, or game setting outside the dedicated ENDÓRË user profile.

## Fresh runtime result

A fresh real EU5 Observer session launched with `new-observer --visual-map` on
the v114 fingerprint. The initial political overview is deliberately strategic
and reads principally as realm colours and labels. A bounded positive wheel
zoom at the centre of the live map then produced
`docs/screens/20260804_v115_render_visibility/manual_center_close.png`:

- 3D terrain material is visible rather than the political-overlay fill.
- Terrain texture variation, hills, vegetation object clusters, and exposed
  rock material are all present at close scale.
- The session completed a further 45-second maximum-speed Observer interval
  with zero resume recovery and no new error-log bytes.

This is a renderer/configuration probe only. It proves that the current ENDÓRË
profile has physical terrain enabled (`Terrain.3d_terrain_disable = false` and
medium triplanar projection); it does **not** replace the source-bound v110
theatre atlas for feature-specific coast, river, canopy, or relief acceptance.

## Player reproduction

With EU5 closed, run:

```powershell
.\.venv\Scripts\python.exe tools\gamedriver.py profile visual
.\.venv\Scripts\python.exe tools\gamedriver.py launch --mode mod --visual-map --no-debug-mode
```

Start a new game, then zoom in on the map. The profile is persistent in
`G:\endore_user_data`; smoke tests temporarily use a reduced profile but restore
the prior player settings when they finish.
