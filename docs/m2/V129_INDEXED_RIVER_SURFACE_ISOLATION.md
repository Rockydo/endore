# v129 indexed river surface isolation

Direct owner review reported that some ENDÓRË rivers appeared as a thin native water line
beside a blue tiled strip. That is not an acceptable representation of a large river, and
the large strip must never be used as a substitute for native river width.

## Installed-game finding

EU5 reads water courses and their widths from the indexed `map_data/rivers.png` graph. The
installed `NRivers` contract provides palette-index width values from 1.0 through 2.2;
ENDÓRË keeps the installed palette exactly and retains the Great River's dominant index-15
trunk contract. The current graph has 16 source-to-water systems, 38 confluences, two
distributaries, and 56 genuine engine courses.

The previous v124 cache approach still copied each indexed river pixel into terrain channel
6 at virtual-texture resolution. Although that channel was assigned a dry installed
material, a separate cache layer can be sampled differently from the engine spline and was
not needed to render a river. The prior labelled Finder captures are not evidence for the
feature: the supposed Anduin close images visibly show the northern political overview.

## Correction

- Remove every terrain-cache channel-6 river write, including the 65K virtual-resolution
  override and the blue river diagnostic-preview colour.
- Keep the installed palette, every source-pinned course, confluence, distributary, and
  Great River index-15 width contract unchanged.
- Keep source-lake channel-4 material as a separate small-lake mechanism; it is not a
  river-width surrogate.
- Regenerate the complete material cache as generator v60. Its manifest declares
  `native_river_surface = indexed_raster_only`, and validation recomputes the terrain
  source and fails if one channel-6 river pixel returns.

## Static result

The rebuilt 8192x4096 material source has zero channel-6 river pixels. Its 65K virtual
cache has 174,763 tiles, 44,417 unique material tiles, a 23.1 MB material payload, and no
Earth decal layers. The diagnostic material preview also has zero pixels in its former
blue-river colour. `tools/gen_rivers.py --check` and `tools/gen_terrain_cache.py --check`
both pass.

Full repository validation and paired real-game smoke remain mandatory before publication.
M2 remains red: the false camera captures do not replace direct visual acceptance.

## Verification status

- `gmake validate`: PASS in 539.8 seconds, including the complete M2 world gate in 442.4
  seconds and the recomputed zero-channel-6 isolation check.
- `gmake smoke`: PASS in 232.3 seconds. Paired vanilla and ENDÓRË launches both reached
  menu-ready with zero mod-unique error-log lines on fingerprint
  `d021a02eea707cf6581f5fc0d730480f852c58720951400998a867941ac6e696`.
- `tools/eu5_slot.py assert-smoked`: PASS for that exact game-visible tree.
