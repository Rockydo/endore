# v109 nested distributary gate

## Candidate

- Game build: `24187685` (`1.3.11`, Pavia)
- Game-visible fingerprint:
  `57db5107df395adb1b1a1bf4b0d0f52c8b223392e1ad2f957cc58609763eea21`
- Graph: 16 source-to-water systems, 38 red confluences, two yellow distributaries,
  56 genuine engine courses
- Indexed footprint: 61,432 source pixels; exact 982,912-pixel 4x material footprint
- Painted proxy width: none

## Gates

- Coherent world rebuild: PASS, 683.9 seconds
- Terrain cache: PASS, 174,763 tiles, 45,053 unique material tiles, zero Earth decals
- Graph invariants: PASS, one source in the Anduin component, two valid yellow splits,
  19,353 nodes, 19,352 edges, cycle rank zero
- Paired vanilla/ENDÓRË smoke: PASS, 202.4 seconds, zero new/mod-unique lines
- Exact-fingerprint smoke assertion: PASS
- Fresh no-debug Observer at `37_ethir_distributary`: PASS
- Maximum-speed playback: PASS, 45 seconds, zero recovery, normal 1,486-byte log
- Final full validation: PASS, 537.4 seconds (M2 world 445.9 seconds)

## Visual review

Local evidence is under `docs/screens/20260804_v109_nested_ethir/`. The close camera is
identical to v108. The new exact part-5 mouth branches from the existing arm near the coast
as a compact natural Y; both arms are engine splines and neither has a broad or parallel
blue terrain band. The 40-second playback frame shows TA 3018.1.13 at 19:00.

This accepts nested yellow branches as an engine mechanism. It does not authorize the
other source arm at the Anduin junction, which would exceed vanilla's degree-three tree
grammar, and it does not declare the complete M2 map accepted.
