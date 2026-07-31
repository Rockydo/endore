# M2 source-terrain proof — 2026-07-31

Status: the v29 source-terrain tree loads and ticks. M2 visual acceptance remains red.

## Exact tree

- Game build: Steam 24187685.
- Game-visible fingerprint:
  `e453742c7d20aaaf3b68567ffb6c98855df41b8b40695bd5899b9100c60e25d4`.
- Runtime topology: 6,004 locations (5,200 passable land, 600 impassable mountain,
  60 lake, 144 sea) and exactly 2,038,645 Arda-native vegetation transforms.
- Terrain cache v29: 174,763 indexed tiles, q64 height, 80,217 unique height tiles,
  63,098 unique material tiles, and zero Earth decal layers.
- Binding projection hash:
  `5b585889790c4601c10baa75d07ad0075fa4ff56fa55e053e0499f7e668a4903`.

## Physical-map change

- Imported 190 renderable `poly_highland` source footprints with 10,805 simplified
  vertices. They add low, feathered rolling relief without changing mountain
  impassability or political tessellation.
- Imported all eight `poly_moor` footprints with 369 vertices. The Dead Marshes now use
  the exact 111-vertex source polygon instead of a seven-point hand-authored blob.
- Named forests render after broad climate paint, so Rhûn, Harad, and Mordor envelopes
  cannot erase their source geometry. Ithilien retains its high-detail tree floor within
  the unchanged global object budget.
- Mordor's fifteen-point ash oval is gone. Its volcanic envelope is derived from Arda
  Maps mountain footprints 8–11, the source-aligned Ered Lithui, Ephel Dúath, and
  Mountains of Shadow axes, and the exact Mount Doom point; its open eastern edge fades
  continuously.
- Sub-location material ponds now sit in shallow feathered physical bowls and use a
  wetland/water-transition material stack while remaining safely above the engine water
  plane.
- Rock, snow, and dark-rock thresholds are more selective around physical crests, which
  reduces the hard exposed-rock fringe without moving any ridge, peak, or pass.

## Gates

- `make validate`: PASS in 281.9 seconds after the canonical-forest allocator correction.
- `make smoke`: PASS in 200.8 seconds. Paired vanilla and ENDÓRË launches reached
  menu-ready with zero new lines and zero mod-unique diagnostics.
- The fresh non-debug full-visual New Game loaded the exact v29 world and reached an
  interactive country-selection frame. The outer command wrapper expired after 604
  seconds while the state driver was still waiting, but direct inspection proved the
  owned EU5 process responsive at 5.44 GB working set and already at country selection.
- Continuing that same token-verified session entered HUD-proven live Observer. Attempt
  two measured `red=0.289`, `dark=0.855`, and `light=0.043`.
- The 45-second monitor resumed exactly once and remained unpaused. Lothlórien's visible
  population changed from 25,022 to 25,125 and the age banner advanced from Traditions to
  Renaissance, proving live simulation rather than a static loaded frame.
- The deep session's error log grew once, from 1,486 to 1,616 bytes, when a
  country-selection coat-of-arms tooltip was built. The single
  `NCoatOfArms::SCoatOfArmsSpriteWrapper` line did not recur or grow during live playback
  and is not a map/cache/load diagnostic. It remains an explicit cleanup/provenance item
  before the final M2 gate; paired smoke remains zero-new-lines green.

## Evidence captures

The gitignored runtime evidence directory is
`docs/screens/20260731_m2_source_terrain_v29/`:

- `current_after_outer_timeout.png` — responsive interactive country selection after the
  outer wrapper timeout.
- `manual_selection_live.png` — HUD-proven live Observer.
- `observer_0000.png` through `observer_0002.png` — uninterrupted live playback.
- `source_terrain_zoom.png` — post-playback map frame showing changed live values.

This proof greens loadability only. Brown Lands, Rhûn, and Harad still contain broad
proof-era macro-biome envelopes; close physical presentation and the complete nine-theatre
capture set remain below the reopened M2 acceptance bar.
