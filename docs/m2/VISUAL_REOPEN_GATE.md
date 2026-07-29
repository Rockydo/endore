# Reopened M2 visual-production gate

Status: blocking. Owner review supersedes the earlier technical M2 acceptance.

The current map is a successful self-contained proof: it loads at the installed native
canvas size, retains no Earth terrain decals, and supports custom locations, realms, and
Observer play. It is not yet a release-quality physical map. Political readability does
not substitute for geographic quality.

## Binding defects

1. Inland seas, lakes, and forest regions read as geometric ovals rather than natural
   landforms.
2. Coasts are imprecise, overly smooth linework without convincing bays, estuaries,
   headlands, islands, or multi-scale shoreline detail.
3. Mountain systems do not present as physical close-zoom relief.
4. Forests, ground materials, and other terrain character are not visibly comparable to
   vanilla at close zoom.
5. Rivers are weak or invisible and do not read as a coherent drainage system.
6. The world needs substantially more geographic detail and, after the physical controls
   stabilize, finer location granularity.

## Work order

### A. Evidence-led renderer audit

- Capture the current non-debug terrain view at full, regional, and close zoom.
- Trace every visible layer back to its authored input: height topology, visible
  `gfx/terrain2` sibling, terrain virtual-texture cache, biome/topography assignment,
  rivers palette, flat map, map-object definitions, and locators/transforms.
- Compare exact installed vanilla assets and data contracts. Reuse vanilla terrain
  materials, but never retain an Earth-authored transform, decal, coastline, river, or
  height payload.

### B. Natural control geometry

- Replace primitive masks with authored multi-scale coastline, lake, forest, ridge, pass,
  valley, marsh, and drainage controls.
- Preserve the canonical silhouette and relative geography without tracing a published
  map. Add deterministic seeded detail only beneath hand-authored large and medium forms.
- Hand-tune at least the Icebay of Forochel, Gulf of Lune, Bay of Belfalas, Anduin delta,
  Sea of Rhûn, Núrnen, Mirkwood, Old Forest, Fangorn, Misty/White/Grey Mountains, Ephel
  Dúath, Ered Lithui, and Mount Doom.

### C. Physical rendering

- Build mountain masses with foothills, crest variation, valleys, and pass cuts rather
  than thin ridge lines.
- Generate a hydrologically coherent river network with visible major rivers and
  tributaries, valley incision, valid sources, merges, mouths, and installed palette
  semantics.
- Restore forests through Arda-native placement/coverage derived from controls. Do not
  re-enable the quarantined Earth transform files.
- Paint varied installed terrain materials by topography, climate, vegetation, elevation,
  moisture, and landmark masks so close zoom never reads as a flat political board.

### D. Scale and granularity

- Keep the installed-proven 16384×8192 locations raster and 8192×4096 height sibling.
  This is already the full vanilla canvas contract.
- Measure landmass occupancy and enlarge/recenter Middle-earth within that canvas if it
  materially improves close-zoom scale while retaining the full planned extent.
- Only after coast/hydrology/relief controls freeze, regenerate location seeds at
  vanilla-Europe-like settled density, refine strategic passes and crossings, and review
  every named anchor against the new geometry.

## Acceptance evidence

The gate is green only when all of the following are true:

- Full-map silhouette remains unmistakably Middle-earth without geometric primitive
  landforms.
- Regional and close-zoom non-debug screenshots visibly show 3D mountain relief, forest
  coverage, major rivers, varied terrain materials, natural shores, and intended passes.
- Required screenshot theatres: Shire/Old Forest, Forochel, Misty Mountains/Anduin,
  Mirkwood, Rohan/White Mountains, Gondor/Belfalas, Mordor, Rhûn, and Harad.
- Political labels and all named anchors still resolve onto the correct land.
- Terrain-cache validation still proves zero Earth decal layers and quarantine validation
  proves zero Earth-authored transforms.
- Paired smoke has zero mod-unique lines; fresh non-debug Observer loads and advances with
  zero mod-caused map, terrain, river, locator, or renderer diagnostics.
- The map receives explicit owner-quality acceptance before M5 gameplay work resumes.
