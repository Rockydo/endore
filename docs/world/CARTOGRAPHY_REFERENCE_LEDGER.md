# Cartography reference ledger

Status: binding for the reopened M2 physical-map gate.

The production map is an original ENDÓRË rendering of north-western
Middle-earth, but its large- and medium-scale geography is measured against
the following two owner-approved cartographic references:

| Reference | Accessed | Binding use |
|---|---:|---|
| [Arda Maps — Third Age](http://arda-maps.org/ages/third) | 2026-07-31 | Coastline, islands, lakes, drainage, mountain and woodland envelopes, roads, and an independent landmark cross-check. |
| [ArdaCraft — interactive Middle-earth map](https://www.ardacraft.me/map/middle-earth-interactive-map) | 2026-08-01 | Equal-scale world grid, precise canon landmark anchors, detailed regional boundaries, biome footprints, close-scale placement checks, and the Heightmap V2 crest/branch interpretation. |

Tolkien's published text and map evidence retains the canon precedence stated
in `docs/ENDORE_MASTER_PLAN.md`. Arda Maps and ArdaCraft are precise
cartographic interpretations, not new canon. When they differ, ENDÓRË uses the
book evidence first, then prefers the ArdaCraft equal-scale grid for a point
location and Arda Maps for continuous physical linework. Every substantive
exception is logged in `docs/ASSUMPTIONS.md`.

## Projection contract

ArdaCraft exposes an equal-scale 53,888×43,008 grid with world bounds
`x=-19584..34303`, `z=-10240..32767`. ENDÓRË preserves that scale instead of
stretching the smaller represented world across EU5's 2:1 canvas:

```text
endore_y = (z + 10240) / 43007
endore_x = 0.5 + (x - 10651.5) / 86014
```

This places the owner-requested extent from Forochel to northern Far Harad on
the complete vertical canvas. The classic mapped lands occupy the central
roughly 55% of its width, leaving honest ocean and off-map eastern margin
rather than distorting Middle-earth horizontally. Arda Maps is calibrated to
the same frame through 64 shared named landmarks; local source disagreements
remain visible in the development audit instead of being hidden by hand
tuning.

## Conformance controls

- `docs/world/control/cartography_targets.csv` is the committed landmark
  crosswalk. Every production settlement anchor must remain within its stated
  normalized tolerance.
- `docs/world/control/projection.json` contains only transformed, simplified,
  and hand-reviewed ENDÓRË control geometry. It must identify this projection
  contract and both reference roles.
- `docs/world/control/ardacraft_relief.json` contains only a 2500x2003, 8-bit,
  zlib/base85 numeric warm-rock plus pale-summit response derived from the hash-pinned
  Heightmap V2 overlay. v42 retains a restrained exact crest response and reconstructs a dominant
  tight body plus continuous shoulders at 3/8/15 source pixels; all terms remain
  source samples. It contains no source colours, labels, water, political information,
  or redistributable reference image. Validation binds its source and field hashes.
- `tools/cartography_reference_audit.py --check` is a permanent static gate.
- The gate hash-pins the complete reviewed `projection.json`, not only its
  feature counts. Any coordinate change to a coast, island, lake, mountain,
  summit, pass, woodland, river, or density envelope therefore requires an
  explicit cartographic review and audit-hash update.
- That gate also requires provenance for all 62 secondary landmarks and exact
  coordinate synchronization between every one of the 38 realm seats and its
  settlement/landmark capital control.
  It verifies the projection constants, complete anchor coverage, tolerances,
  and the generated conformance report.
- Coast, lake, forest, mountain, and river controls are reviewed by feature
  envelope, axis, adjacency, and ordering—not merely by landmark count.
- Forest object density, LOD distribution, and species mix are renderer presentation
  layered strictly inside those reviewed envelopes. They may not dilate, simplify, or
  relocate an Arda Maps woodland polygon. Mirkwood and Lothlórien additionally carry
  per-LOD transform floors so a correct source outline cannot pass with sparse physical
  canopy.
- Stronger renderer-scale continuity on the White Mountains and Mordor walls
  is multiplied by a softly dilated mask of the committed Ardacraft numeric
  support field. The added response therefore cannot authorize a high ridge
  outside source-backed relief; global and four-theatre support floors remain
  binding independently.
- Morannon additionally binds two exact short hinge arms from the direct gate marker to
  the nearest source crests at `[0.621978, 0.531998]` and `[0.605128, 0.549585]`.
  Ardacraft's drawing layer confirms these Ered Lithui/Ephel Duath connections; the
  oriented pass carve retains the low Cirith Gorgor saddle between them.
- The gate also requires real EU5 screenshots in all nine theatres listed in
  `docs/m2/VISUAL_REOPEN_GATE.md`; static agreement never substitutes for
  renderer evidence.

- River conformance binds 102 non-duplicated Arda Maps controls: 26 reviewed
  trunks/tributaries and 76 parser-safe physical-drainage controls. Twelve
  complete source-to-water channels are independently serializable in EU5's
  installed indexed raster; the remaining tributaries still own exact valley
  incision and wet-bank material without invented unsupported junctions.
  Lefnui and Serni are independent indexed channels. Sirith, the branched Lhûn
  system, and the complete Ethir Anduin distributaries remain visible physical
  drainage where build 24187685 cannot serialize their true receiving graph.
  Validation rejects duplicated Harnen, Morgulduin, or lower-Anduin source
  parts and binds the hierarchy, provenance, widths, incision, material
  response, and basin-level coverage independently.
- Native terrain also carries 104 direct affluent paths reconstructed from the
  hash-pinned Ardacraft drainage layer. The reduction retains only paths beginning within
  four source pixels of one of the 102 reviewed courses, reaching at least sixteen pixels
  away, spanning at least twelve centreline samples, and reconnecting to the exact axis.
  Its 3,075 samples remain physical incision/material detail only; they do not fabricate
  parser-unsafe EU5 river junctions or claim new Tolkien names.

## Source-biome reduction contract

The quarantined Ardacraft biome atlas is hash-pinned as
`2070d5577d768b2d418fd06e61d2fbafb5b55599340540fd9308ead213037997`. Production
code retains no downloaded image, label text, or source colour. It transforms and
simplifies only the outer numeric rings needed by ENDÓRË, grouped as follows:

- Brown Lands: `M6` (one component).
- Rhûn steppe: `L3`, `L5`, `L7`, `M11`, `M18`, `M2`, `M20`, `M7`, and `Z2`–`Z5`
  (41 components).
- Near Harad scrub/woodland: `H1`, `H2`, `H6`, `H7`, `J22`, `J48`, `J49`, `K23`,
  `K31`, and `N4` (37 components).
- Far Harad arid: `H3`, `H4`, and `H5` (seven components).

The source atlas ends at its own represented edge. ENDÓRË's wider east/south crop needs
explicit organic continuation polygons for Rhûn and Harad; those controls are marked as
judgement calls and may not masquerade as source geometry. Mordor's source-enclosed ash
zone is applied after the reduced atlas so the eastern steppe cannot overwrite it.
Validation binds the source hash, classification, component counts, vertex floors,
continuation provenance, ordering, and the complete resulting projection hash.

## Political source-overlap contract

Political woodland claims are independently raster-overlapped against the same
hash-pinned source masks. Rectangular search bounds cannot authorize ownership by
themselves; the generated audit binds substantial overlap, forced exceptions, final
bounding boxes, and connected components for Lothlorien, Fangorn, Druadan, Woodland
Realm, Woodmen, and Dol Guldur. Dunland instead carries an explicit reviewed lowland
polygon because it is not defined by a woodland mask.

## Reference quarantine

Downloaded TopoJSON, GeoJSON, scripts, tiles, screenshots, film frames, and
other source payloads live only beneath
`G:\endore_runtime\cartography_references`. They are development evidence and
must never ship or enter Git. The repository contains provenance, numeric
control targets, original simplified control geometry, and conformance
results—not source imagery or a redistributable copy of either interactive
map.
