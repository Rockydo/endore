# v112 Erebor relief evidence

## Purpose

The v110 direct-name Erebor frame was valid runtime evidence but its settlement and
army overlays obscured the compact summit. This focused follow-up changes camera
composition only. It does not alter a map raster, relief control, location, or river.

## Bound camera contract

- Canonical peak: `Erebor`, Ardacraft-pinned at `(0.599699, 0.137606)` in
  `me_dale_region`; static source height at the exact point is 61,926.
- Offset focus: exact canonical `Dale` result at `(0.601803, 0.148883)`, in the
  same source-bound region. The finder has several `Dale...` prefix results, so
  `tools/capture_m2_theatres.py --check` now permits precisely one exact canonical
  name while retaining its one-result requirement for prefix-only cameras.
- Close frame: Finder maximum-close (zero zoom-out detents), then the standard
  pointer-clear move. The Dale marker remains away from the peak rather than
  occluding it.

## Runtime result

Fresh real EU5 Observer session `20260804_v112_erebor_maximum_close` loaded the
published game-visible fingerprint
`57db5107df395adb1b1a1bf4b0d0f52c8b223392e1ad2f957cc58609763eea21`, captured
regional and maximum-close frames, advanced for 45 seconds at maximum speed, then
stopped and released the shared runtime lease. `error.log` stayed at its normal
1,486 bytes; no mod-attributable line was introduced.

`docs/screens/20260804_v112_erebor_maximum_close/39_erebor_relief_close.png` now
shows the compact, steep isolated Erebor cone physically rising north of Dale. It
is terrain relief, not a map label or political overlay. The same frame also keeps
the nearby Dale/Esgaroth geography and Celduin drainage visible, making it a useful
anti-regression proof for the Lonely Mountain's intended isolation.

## Consequence

Keep the source-pinned compact peak. Enlarging it merely to dominate a political
camera would make Erebor a range-sized massif and reduce lore fidelity. M2 remains
open for the separately pending source-anchored political-frontier review; this
document closes only the camera-composition ambiguity in the physical atlas.
