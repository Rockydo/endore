# V138 — renderer and atlas calibration

## Scope

This evidence batch corrects the M2 review camera after the owner reported a flat-looking
map. It changes no terrain, ownership, rivers, or content data.

## Installed-engine findings

- The retail native Terrain map is the pinned first map-mode slot (`Ctrl+Q` in the
  installed default input profile). The debug-console text `mapmode terrain` is not a
  substitute for that GUI route.
- `Map.flatmap_mode = "never"` in ENDÓRË's isolated visual profile is required for the
  engine to expose the custom 3D relief, material ground, water, and vegetation below the
  native Terrain map presentation.
- The source-bound `Camera.SetTransform` at distance 1800 is an orientation baseline.
  Sixteen wheel-in detents prove maximum physical foliage detail at the exact Old Forest,
  but crop broad landforms too aggressively for a review atlas.

## Evidence

- `docs/screens/20260806_m2_flatmap_never_probe/`: fresh native-Terrain 3D renderer probe.
- `docs/screens/20260806_m2_max_close_calibration/`: exact Old Forest maximum-detail
  canopy proof (`me_land_4390`).
- `docs/screens/20260806_m2_context_close_calibration/`: exact eight-detent Old Forest,
  Erebor, and Caras Galadhon context probes.
- `docs/screens/20260806_m2_physical_atlas_v1/`: one fresh debug Observer captures nine
  continental theatres, four Anduin/tributary views, and focused canopy/relief views,
  then completes 45 seconds of maximum-speed playback with the normal 1,486-byte log.
- `docs/screens/20260806_m2_nondebug_deep_log_v1/`: fresh normal Observer, native Terrain
  slot, 45 seconds at maximum speed; the strict deep-log parser reports zero unexpected
  lines, including zero coat-of-arms collision or Finder data-model diagnostics.

## Capture contract

The evidence runner now uses eight wheel-in detents as its close-review baseline and a
zero/one-detent contextual backoff per feature. Sixteen detents remain an explicit
maximum-detail capability probe only. This makes visual review faithful to the actual
rendered world without confusing an overly cropped detail frame for geographic evidence.

## Gate status

This closes only the deep-load diagnostic sub-gate. M2 remains open: source-backed physical
geography and native-river audits, then the complete owner acceptance gate, are still
required.
