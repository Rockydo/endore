# Middle-earth Map Controls

These files are the authored source for M2 and later map derivation. They are original,
normalized geometric statements assembled from relative positions and journeys in the
books; no published map image or film frame was traced or copied.

## Coordinate convention

- `(0, 0)` is the north-west corner; `(1, 1)` is the south-east corner.
- Production canvas: 8192×4096.
- Authored control raster: 1024×512.
- The visible extent runs from Lindon to western Rhûn and from Forochel to northern Far
  Harad. Deep Rhûn and deep Harad end at the map border.
- Settlement rows cite a book chapter or the book's schematic map. Their exact normalized
  coordinates are gameplay judgments recorded with † in `docs/ASSUMPTIONS.md`.

## Files

- `projection.json`: coastline, bays, lakes, ridges, passes, biome and density zones,
  and river centerlines.
- `settlements.csv`: canon anchor names, ranks, language/realm hints, and sources.
- `locality_anchors.csv`: exact, source-pinned local settlement anchors that replace a
  reviewed generic land slot without renumbering the existing world mesh.
- `geographic_anchors.csv`: exact, source-pinned physical places using the same
  slot-preserving mechanism, without implying an inhabited settlement or broad claim.
- `coastline.png`: binary land mask.
- `elevation.png`: authored 16-bit elevation control.
- `biomes.png`: numeric biome zones listed in `control_manifest.json`.
- `density.png`: relative location-seed density.
- `rivers.png`: binary river-centerline control.
- `projection_preview.png`: visual QA composite with settlement points.
- `control_manifest.json`: counts, contracts, and source hash.

Run `tools/m2_controls.py --write` after an authored edit and `--check` to verify that all
committed rasters and the manifest exactly match their sources.
