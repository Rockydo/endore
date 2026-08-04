# v108 outgoing distributary gate

## Candidate

- Game build: `24187685` (`1.3.11`, Pavia)
- Game-visible fingerprint:
  `f4193469621a29e6028b02f984f3b17d86f74329560c368921269d8f5ce9123a`
- Graph: 16 source-to-water systems, 38 red confluences, one yellow distributary,
  55 genuine engine courses
- Indexed footprint: 61,344 source pixels; exact 981,504-pixel 4x material footprint
- Painted proxy width: none

## Static gates

- Full validation: PASS, 494.4 seconds
- Deterministic M2 world gate: PASS, 415.8 seconds
- Terrain cache: PASS, 174,763 tiles, 45,053 unique material tiles, zero Earth decals
- Graph invariants: PASS, one source per system, degree-two yellow marker adjacent to a
  degree-three split, cycle rank zero, real engine-water mouth

## Live gates

- Paired vanilla/ENDÓRË smoke: PASS, 203.8 seconds, zero new/mod-unique lines
- Exact-fingerprint smoke assertion: PASS
- Fresh no-debug Observer at `37_ethir_distributary`: PASS
- Maximum-speed playback: PASS, 45 seconds, zero recovery, normal 1,486-byte log

The source candidate combines Arda Maps `line_river` 71 parts 6 and 4 through their exact
shared delta junction. Part 0 was rejected because it reconnects to Anduin and would form
a cycle absent from every installed vanilla river component.

Local evidence is under `docs/screens/20260804_v108_ethir/`. The maximum-close Ost galenen
frame shows the source-exact Y split and outgoing arm as continuous engine-rendered river
splines reaching the sea. The surrounding terrain retains its normal material texture;
there is no broad or parallel blue proxy. The 40-second playback frame shows TA 3018.1.13
at 16:00, and the complete interval ends with no recovery or log growth. This clears the
v108 technical river gate. It does not declare the complete M2 map accepted; the owner
remains the final visual authority.
