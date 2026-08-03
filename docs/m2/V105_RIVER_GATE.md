# v105 genuine indexed-river gate

## Candidate

- Game build: `24187685` (`1.3.11`, Pavia)
- Game-visible fingerprint:
  `3381fb36a8a87bd9d541cd153ed9c255fc1abacb4e53648dec1ce731bebd78e9`
- Graph: 12 source-to-water systems, 25 red tributary junctions, 37 engine courses
- Indexed footprint: 54,184 source pixels; exact 866,944-pixel 4x material footprint
- Painted proxy width: none

## Gates

- Full validation: PASS, 566.5 seconds
- Deterministic M2 world gate: PASS, 481.1 seconds
- Paired vanilla/ENDÓRË smoke: PASS, 204.1 seconds, zero new/mod-unique lines
- Exact-fingerprint smoke assertion: PASS
- Fresh live Observer: PASS
- Maximum-speed playback: PASS, 45 seconds, TA 3018.1.1 to 3018.1.15, zero recovery
- Playback error-log growth: zero bytes

The 1,794-byte final log contains two `pdxinput_context` lines emitted before playback by
failed Escape-key evidence cleanup. They account for the 308-byte difference from the
normal 1,486-byte deep baseline; no line was added during playback.

## Visual review

Local evidence is under `docs/screens/20260803_v105_genuine_rivers/` and covers regional
and maximum-close pairs for upper/lower Anduin, Celebrant, Entwash, Baranduin, Lhûn,
Greyflood, the Sirith-Anduin reach, and the Shire tributary network. Review confirms:

- the Anduin is one continuous widest-class indexed spline;
- tributaries visibly connect to their trunks instead of terminating as dry controls;
- trunk and tributary width classes remain distinct;
- no broad blue terrain band runs beside a thin river spline; and
- the world remains responsive throughout playback.

This clears the v105 technical river mechanism. It does not declare the complete M2 map
accepted; the owner remains the final visual authority.
