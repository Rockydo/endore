# v124 native river surface correction

## Finding

The close-zoom owner report caught a real remaining defect in the prior v105-v123 tree:
although its river graph was native and its terrain-mask footprint came exactly from that
graph, ENDÓRË's channel-6 material resolved to custom still water. In the renderer that
made a blue strip beside, or beneath, the actual indexed spline. It was terrain paint, not
a wider engine river.

## Installed-game reference

EU5's `gfx/terrain2/materials.txt` labels material-mask channel 6 `Rivers/Lakes`, but
ordinary vanilla land biomes map it to dry riverbank ground treatments; for example,
`arctic_flatlands_desert_biome` uses `grass_scatter_dark_variation_01`. The water line and
its 1.0-to-2.2 width hierarchy come independently from the one-pixel indexed
`map_data/rivers.png` graph (`NRivers`). The installed file's palette-4/5/11/15 flow pixels
are likewise one-pixel paths, rather than blue terrain bands.

## Correction

- Keep the exact source-pinned 16-system, 38-confluence, two-distributary native graph.
- Keep the Great River's continuous Langwell--Anduin index-15 contract unchanged.
- Keep the subtle source-aligned elevation incision.
- Map ENDÓRË material channel 6 to vanilla-style dry
  `grass_scatter_dark_variation_01`, not `endore_still_water`.
- Preserve `endore_still_water` only for the separately audited sub-location lake cores on
  channel 4.
- Rebuild the terrain-cache provenance as generator v59 and require validation to reject
  any return to an aqueous channel-6 mapping.

This makes the native engine spline the only blue water surface and the only authority for
river width. No canon course, coast, relief, forest, settlement, or political cell changes.

## Results

- Terrain cache rebuilt as generator v59 with 174,763 indexed tiles and zero inherited
  Earth decal layers.
- Full `gmake validate`: PASS in 478.4 seconds (M2 world gate 406.5 seconds).
- Paired `gmake smoke`: PASS in 204.1 seconds on fingerprint
  `9caa9cea5f4a086967b30d62f49c69a767afcff59e0a4beb3f191fc61a6877f7`, with zero new
  mod-unique error-log lines.
- A fresh visual-profile Observer load completed a 45-second maximum-speed playback with
  zero recovery actions.

The one fresh Finder frame is deliberately not accepted as close river evidence: despite a
measurable first focus, it remained a broad strategic political composition. It proves the
new tree loads and ticks but not feature-scale river presentation. Do not substitute that
frame for a close visual review; the existing two-strike camera-state blocker remains in
force.
