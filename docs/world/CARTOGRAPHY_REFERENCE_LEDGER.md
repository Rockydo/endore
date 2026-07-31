# Cartography reference ledger

Status: binding for the reopened M2 physical-map gate.

The production map is an original ENDÓRË rendering of north-western
Middle-earth, but its large- and medium-scale geography is measured against
the following two owner-approved cartographic references:

| Reference | Accessed | Binding use |
|---|---:|---|
| [Arda Maps — Third Age](http://arda-maps.org/ages/third) | 2026-07-31 | Coastline, islands, lakes, drainage, mountain and woodland envelopes, roads, and an independent landmark cross-check. |
| [ArdaCraft — interactive Middle-earth map](https://www.ardacraft.me/map/middle-earth-interactive-map) | 2026-07-31 | Equal-scale world grid, precise canon landmark anchors, detailed regional boundaries, biome footprints, and close-scale placement checks. |

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
- The gate also requires real EU5 screenshots in all nine theatres listed in
  `docs/m2/VISUAL_REOPEN_GATE.md`; static agreement never substitutes for
  renderer evidence.

## Reference quarantine

Downloaded TopoJSON, GeoJSON, scripts, tiles, screenshots, film frames, and
other source payloads live only beneath
`G:\endore_runtime\cartography_references`. They are development evidence and
must never ship or enter Git. The repository contains provenance, numeric
control targets, original simplified control geometry, and conformance
results—not source imagery or a redistributable copy of either interactive
map.
