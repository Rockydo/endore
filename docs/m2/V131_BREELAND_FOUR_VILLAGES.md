# v131 Bree-land four-village source correction

This M2 political-fidelity batch corrects a compact, source-proven error east of Bree.
Archet, Combe, and Staddle were resolving to wild cells in the North Arnor hierarchy
region even though all three are part of Bree-land on TA 3018. No coast, relief, forest,
river, location geometry, realm roster, or broad claim envelope is changed.

## Evidence and exact controls

*The Lord of the Rings*, Book I, Chapter 9 names Bree as the chief village and explicitly
names Archet, Combe, and Staddle as the other villages of Bree-land. The direct
equal-scale Ardacraft markers supply their rendering controls.

| Village | Marker coordinate | Generated land cell | TA 3018 owner |
| --- | --- | --- | --- |
| Archet | `0.409637, 0.227916` | `me_land_1898` | Bree-land |
| Combe | `0.406637, 0.226521` | `me_land_4583` | Bree-land |
| Staddle | `0.406370, 0.232311` | `me_land_2798` | Bree-land |

The cells remain in `me_north_arnor_region` because regional hierarchy is geographic,
not a political assertion. The existing Bree-land source envelope already covers their
actual generated centroids. After regeneration, all 24 Bree-land locations form one
connected component, with zero contract violations and a final physical bounding box of
`0.3811966–0.4129426` by `0.2056668–0.2755252`.

`tools/cartography_reference_audit.py` now fail-closes if any of the three exact markers,
their coordinates, or their Ardacraft provenance are removed. The complete validation and
paired runtime smoke are required before publication.

## Repository and runtime verification

- Final `gmake validate`: PASS in 504.5 seconds, including the complete 428.2-second `m2_world`
  gate, source-marker audit, ownership topology, people, census, templates, and lint.
- `gmake smoke`: PASS in 211.9 seconds. Paired vanilla and ENDÓRË launches both reached
  menu-ready through the shared EU5 lease; ENDÓRË added zero new error-log lines.
- The final exact-tree smoke assertion remains required immediately before commit.
