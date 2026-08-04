# v107 independent source-to-lake river gate

## Candidate

- Game build: `24187685` (`1.3.11`, Pavia)
- Game-visible fingerprint:
  `907a10edae306e185633a51570af39a844c09e3c10c2f6c614924919910c15e0`
- Graph: 16 source-to-water systems, 38 red tributary junctions, 54 engine courses
- Indexed footprint: 61,126 source pixels; exact 978,016-pixel 4x material footprint
- Painted proxy width: none

## Gates

- Full validation: PASS, 514.5 seconds
- Deterministic M2 world gate: PASS, 438.9 seconds
- Paired vanilla/ENDÓRË smoke: PASS, 201.6 seconds, zero new/mod-unique lines
- Exact-fingerprint smoke assertion: PASS
- Fresh no-debug Observer: PASS
- Maximum-speed playback: PASS, 45 seconds, zero recovery
- Playback final error log: normal 1,486 bytes

## Visual review

The first candidate added six independent source-to-lake networks and passed validation,
smoke, fresh-game entry, and playback. Its Hobbiton close frame nevertheless showed the
two Eriador rivers terminating in tiny rectangular material ponds. Those two promotions
were rejected; their source-backed valley incision remains dry.

The final candidate keeps four substantial courses entering the Sea of Núrnen. Local
evidence is under `docs/screens/20260804_v107_pruned_nurn_roots/`. Source-bound close views
at Krimpzagh Camp and Blackgash Cleft show continuous, naturally meandering river splines
across the correct ashland and highland terrain, without detached strokes or parallel
blue material. The 40-second playback frame visibly reaches TA 3018.1.13 at 17:00; the
complete 45-second interval ends without recovery or log growth.

This clears the v107 technical river gate. It does not declare the complete M2 map
accepted; the owner remains the final visual authority.
