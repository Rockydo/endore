# v133 Eregion hierarchy and Warg Hill boundary correction

This M2 map-hierarchy and political batch restores Eregion (Hollin) as a source-bounded
Eriador region and removes one unsupported exterior extension from the current Moria
allocation. It does not create an Eregion realm, redraw a sovereign border, or change
terrain, water, forests, mountains, or location geometry.

## Geographic hierarchy

The prior hierarchy incorrectly divided Eregion's named controls between North Arnor and
Enedwaith. The new compact Eregion polygon follows the source-pinned Glanduin on the south,
the western Misty Mountains / Doors of Durin approach on the east, and conservative joins
between the documented northern foothills and the Glanduin on the remaining sides. It
contains 60 land locations, including Hollin Ridge, Ost-in-Edhil, and Warg Hill, while
Khazad-dum and the Redhorn Gate remain in the Vales of Anduin.

This is geographic hierarchy only: the Eregion land remains a former Elven country and is
not promoted into a TA 3018 political realm. The Moria allocation keeps only its immediate
source-reviewed approach cells, subject to all existing landmark contracts.

## Source and ruling

ArdaCraft's direct marker places Warg Hill at `0.479405, 0.318111`, in Eregion close to
Moria's West-gate. *The Lord of the Rings*, Book II, Chapter 4 locates the Fellowship's
Warg attack at this exposed exterior hill. Its position is not evidence that the ruined,
orc-inhabited Moria hold administers the surrounding Eregion land at TA 3018.

The active tessellation resolves that source point to `me_land_2010` at
`0.4778999, 0.3160723`. Before the correction, nearest-seat allocation assigned it to
Moria. The new exact landmark and ownership contract make it deliberate wilderness with
the `unsettled-eregion` rationale.

## Topology result

Moria changes from 24 to 22 locations, retaining one connected component with no detached
unforced specks. The full world retains 38 realms; 3,023 locations are assigned and 2,981
are deliberate wilderness. The source audit now protects eight direct ArdaCraft point
landmarks, including Warg Hill.

## Verification

- `gmake validate`: PASS in 566.7 seconds, including the 471.3-second full M2 world
  gate, source-coordinate audit, controls, terrain cache, native rivers, topology,
  realm hierarchy, people, census, templates, and lint.
- Paired `gmake smoke`: PASS in 203.4 seconds. Both vanilla and ENDÓRË reached the
  menu-ready state; the mod introduced zero new error-log lines.
- The exact tree fingerprint asserted after smoke is
  `43e55f5fbf240daf2bc040d318b641332eccaac639fa5e9131bd3ac3e13e88df`.
