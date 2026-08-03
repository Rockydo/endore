# v106 source-exact tributary gate

## Candidate

- Game build: `24187685` (`1.3.11`, Pavia)
- Game-visible fingerprint:
  `67b987a30f38e4613f867d4b931e283a5618b1a9546c42c1af72228dc2270ed4`
- Graph: 12 source-to-water systems, 38 red tributary junctions, 50 engine courses
- Indexed footprint: 56,841 source pixels; exact 909,456-pixel 4x material footprint
- Painted proxy width: none

## Gates

- Full validation: PASS, 517.8 seconds
- Deterministic M2 world gate: PASS, 415.9 seconds
- Paired vanilla/ENDÓRË smoke: PASS, 234.5 seconds, zero new/mod-unique lines
- Exact-fingerprint smoke assertion: PASS
- Fresh no-debug Observer: PASS
- Maximum-speed playback: PASS, 45 seconds, zero recovery
- Playback final error log: normal 1,486 bytes

## Visual review

The first 54-course candidate loaded and played cleanly, but its bound Greyflood close
frame exposed four short, near-parallel strokes from source controls 35/37/38/39. That
candidate was rejected despite valid topology. The controls remain in source-backed
height incision but no longer produce engine water.

Local before evidence is under `docs/screens/20260803_v106_source_tributaries/`; the final
same-camera evidence is under `docs/screens/20260803_v106_pruned_tributaries/`. The final
frame preserves the continuous Greyflood/Glanduin drainage and legitimate confluence,
removes the diagrammatic comb, and shows no separate blue terrain shoulder. The
40-second playback frame visibly reaches TA 3018.1.13 at 16:00; the complete 45-second
interval ends without recovery or log growth.

This clears the v106 technical river gate. It does not declare the complete M2 map
accepted; the owner remains the final visual authority.
