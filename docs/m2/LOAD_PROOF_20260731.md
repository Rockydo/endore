# M2 load proof — 2026-07-31

Status: the current detailed map loads and ticks. M2 visual acceptance remains red.

## Exact tree

- Game build: Steam 24187685.
- Game-visible fingerprint:
  `8ca808d78c535292a60f2439130797c6e28514a3e063310253e2ca703369b0a4`.
- Runtime topology: 6,004 locations (5,200 passable land, 600 impassable mountain,
  60 lake, 144 sea) and 2,038,645 Arda-native vegetation transforms.
- Terrain cache: 174,763 indexed tiles, q64 height, 79,922 unique height tiles,
  63,501 unique material tiles, zero Earth decal layers.

## Gates

- `make validate`: PASS in 285.3 seconds, including the live-Observer false-positive
  regression, map bijection, height/material cache, rivers, transforms, quarantine,
  setup, and lint.
- `make smoke`: PASS. Paired vanilla and ENDÓRË launches reached menu-ready with zero new
  lines and zero mod-unique diagnostics.
- Cold full-visual New Game attempt 1: country selection and HUD-proven live Observer in
  116.8 seconds.
- Cold full-visual New Game attempt 2: country selection and HUD-proven live Observer in
  114.8 seconds. The live HUD measured dark=0.951/light=0.021; the pause banner measured
  red=0.293.
- Playback: the monitor resumed exactly once, the banner disappeared, and the date
  advanced from 3018.1.1 to 3018.1.15 in 45 seconds. The error log stayed at 1,486 bytes.
- Native location focus: the same session continued to 3018.2.1 while centering
  Khazad-dum. Mirrormere no longer excavates a rectangular host-cell quarry.

## Root cause of the apparent failure

The detailed world had completed the MainMenu-to-Game transition and reached country
selection. The old automation accepted a centered red-pixel crop as proof of the pause
banner even when that red came from political-map paint, then clicked controls belonging
to the wrong UI state. The driver now requires the independent top-left Observer HUD for
both live-state success and any pause/resume action. A synthetic red lobby frame is a
permanent regression test.

## Evidence captures

The gitignored runtime evidence directory is
`docs/screens/20260731_m2_loadproof_v28_tick/`:

- `fresh_country_select.png` — interactive country-selection state.
- `fresh_live.png` — live Observer HUD and real pause banner.
- `observer_0003.png` — running Observer at 3018.1.15.
- `khazad_after_pond.png` — physical terrain at 3018.2.1; former Mirrormere quarry gone.

The close capture still shows a plain wet-material patch and a rock fringe that need
substantial visual refinement. This evidence greens loadability only, not the reopened
M2 nine-theatre quality gate.
