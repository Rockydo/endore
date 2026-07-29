# Derived M2 world artifacts

This directory contains deterministic QA and audit products from the authored controls in
`docs/world/control`. They are not hand-edited inputs.

- `world_manifest.json` records dimensions, seed, location counts, control-area bounds,
  continent counts, and source/model hashes.
- `location_index.csv` is the complete color, type, hierarchy, terrain, and anchor index
  for all 5,812 live locations.
- `location_preview.png`, `height_preview.png`, `river_preview.png`, and
  `flatmap_preview.png` provide lightweight visual inspection without opening the
  production rasters.
- `flatmap_manifest.json` records the exact installed EU5 style-reference asset and the
  derived texture statistics.

Regenerate the stack with `tools/python tools/m2_world.py --write`; verify it with
`tools/python tools/m2_world.py --check`. The canonical `gmake validate` target runs the
check automatically.
