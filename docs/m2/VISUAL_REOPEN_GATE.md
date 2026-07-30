# Reopened M2 visual-production gate

Status: blocking. Owner review supersedes the earlier technical M2 acceptance.

The current map is a successful self-contained proof: it loads at the installed native
canvas size, retains no Earth terrain decals, and supports custom locations, realms, and
Observer play. It is not yet a release-quality physical map. Political readability does
not substitute for geographic quality.

Current iteration: the authored control lattice is 4096×2048 and generates 12,104
locations on the proven 16384×8192 engine canvas: 11,320 passable land, 520 mountains,
64 lakes, and 200 seas. Rhûn and Harad now continue through the east/south borders instead
of being enclosed by a false ocean ring. Static validation is green, including all
anchors, realm connectivity, ports, rivers, locators, and terrain-cache quarantine.
Real-game non-debug review proves that ridge systems produce physical 3D relief. A new
Arda-native material cache also proves continuous ground variation, mountain snow/rock
material, and shoreline transition bands instead of the former shared zero tile and
coarse location-shaped patches. A two-stage checkpoint route now reaches the current
tree in stable non-debug 3D Observer, resolving the earlier resource-bound capture
bootstrap. A later exact-state session proves that Hilbert-ordered Arda transforms render
real tree objects and dense canopy in Mirkwood; native `WM_MOUSEWHEEL` delivery also
provides deterministic close zoom. That same close evidence still shows hard woodland
walls and too-continuous snow/rock ridges. The current physical batch therefore adds
porous forest margins, object-only glades, continuously feathered tree placement,
modulated massif relief, isolated mountain cores, and asymmetric Rhûn/Núrnen shores.
Exact-state renderer proof accepted the relief change but rejected transition paint along
generated location-biome seams because it emphasized pale Voronoi patches. The current
vegetation iteration removes that route and matches vanilla's roughly 10.2 million
installed per-family/LOD transforms with wholly Arda-generated positions. This gate
now has live maximum-close proof of continuous physical Mirkwood canopy at that density.
The final batch adds authored river clearances so the canopy cannot obscure the wet
channels. Ground-level evidence now proves those clearances and a parser-safe naturalized
major-channel raster with installed downstream width progression. The exact current tree
entered no-debug Observer without a river or map diagnostic, and paired smoke is green
with zero mod-unique lines. Multi-theatre evidence and explicit owner acceptance remain
outstanding; this gate remains red.

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
