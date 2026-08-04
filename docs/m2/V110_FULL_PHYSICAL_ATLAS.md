# v110 full physical atlas

## Candidate

- Published commit: `222e295` (`feat(map): add nested Ethir river mouth`)
- Game build: `24187685` (`1.3.11`, Pavia)
- Game-visible fingerprint:
  `57db5107df395adb1b1a1bf4b0d0f52c8b223392e1ad2f957cc58609763eea21`
- River graph: 16 source-to-water systems, 38 incoming red confluences, two outgoing
  yellow distributaries, 56 genuine engine courses, zero cycles
- Material-water contract: 61,432 indexed pixels and an exact 982,912-pixel four-times
  nearest-neighbour terrain footprint; no terrain-only blue proxy

## Runtime atlas

Fresh Observer loaded normally and captured the full map plus paired regional/close views
for Shire/Old Forest, Forochel, Misty Mountains/Anduin, Mirkwood, Rohan/White Mountains,
Gondor/Belfalas, Mordor, Rhûn, and Harad. It then captured upper Anduin, lower Anduin,
Celebrant, Entwash, Lothlórien canopy, Gundabad, Erebor, Mirrormere, Nindalf, and Mount
Gram. Evidence is intentionally ignored working material at
`docs/screens/20260804_v110_full_atlas/`.

The session completed the fixed 45-second maximum-speed Observer playback. The process
exited cleanly and released the shared EU5 lease; `error.log` remained the normal
1,486-byte log with no recovery record.

## Visual findings

- The current terrain is entirely custom Middle-earth terrain at close zoom: no vanilla
  Earth surface, coast, vegetation, or decal underlay was observed.
- Mirkwood and Lothlórien show dense, distinct canopy; the Misty, White, northern, and
  Mordor systems have physical relief rather than flat political-map substitutes.
- The Old Forest confluences, upper/lower Anduin, Celebrant, and Entwash views show real
  indexed river cores and joins. No broad blue shoulders or parallel painted channels are
  present. The Anduin remains the visibly dominant trunk.
- The exact Ardacraft Erebor marker remains a 61,926-unit isolated source peak. The
  location/army overlay makes that compact crown hard to see in its direct-name capture;
  this is a camera-composition limitation, not evidence that the Lonely Mountain is absent.

## Consequence

This is a reproducible physical-review baseline, not M2 acceptance. The next M2 work is a
source-anchored political ownership review, beginning with the user-identified sensitive
frontiers, while preserving the accepted physical controls.
