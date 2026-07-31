# Reopened M2 visual-production gate

Status: blocking. Owner review supersedes the earlier technical M2 acceptance.

The current map is a successful self-contained proof: it loads at the installed native
canvas size, retains no Earth terrain decals, and supports custom locations, realms, and
Observer play. It is not yet a release-quality physical map. Political readability does
not substitute for geographic quality.

Current iteration: the authored control lattice is 4096×2048 on the proven 16384×8192
engine canvas, backed by a full-resolution 65,536×32,768 physical source and q64 derived
runtime cache. The equal-scale ArdaCraft projection preserves the source aspect rather
than stretching Middle-earth, while Arda Maps Third Age supplies the audited 1,251-vertex
mainland coast, 15 lakes, 43 mountain footprints, 24 river/valley controls, and forest
geometry. The permanent conformance layer covers 42 settlement anchors, 62 additional
landmarks, and all 38 realm seats. Downloaded reference data remains transient and
unshipped.

The source-frame production tree initially contained exactly 14,245 locations: 10,800
passable land, 3,200 mountains, 65 lakes, and 180 seas. Static validation passed every
map, cache, vegetation, connectivity, realm, people, census, template, quarantine, and
lint stage. Paired vanilla/mod smoke then passed with zero mod-unique lines on fingerprint
`dbd52c52`. A full-visual fresh New Game and a materially different lightweight
checkpoint attempt both completed setup/cache work but remained noninteractive for the
entire 600-second post-cache bound, peaking around 23.5 GB. The two-strike evidence is
recorded in `BLOCKERS.md`; the 14,245-cell route must not be repeated unchanged.

The current runtime tessellation keeps the last proven 12,104-location aggregate:
10,700 passable land, 1,200 mountains, 60 lakes, and 144 seas. The 1,200 mountain cells
remain more than twice the last live source tree's impassable granularity, while the exact
physical mountain footprints, ridge axes, passes, and full-resolution height source remain
unchanged. The stratified renderer candidate uses 4,077,285 Arda-native vegetation
transforms and preserves explicit high-detail floors in Fangorn, the Old Forest, Lórien,
and Ithilien.

This tree passes the complete static gate and paired smoke with zero mod-unique lines on
fingerprint `66f1cd73`. Its first checkpoint attempt deferred because Antiquitas held the
shared EU5 lease; no process launched. Rhûn and Harad still continue through the east/south
borders instead of being enclosed by a false ocean ring. M2 remains red until the current
tree passes the same real-renderer and multi-theatre gates.
The next free-slot attempt resolved the pending runtime question: a fresh debug New Game
entered live Observer and advanced through 3018.2.04, and a separate cold non-debug
`--visual-map` New Game also entered live Observer. The first run exposed only a
gamedriver pause-banner false negative, now fixed by recognizing the stable Observer HUD.
The full-map tactical overlay confirms the Arda-derived footprint is active and vanilla
Earth is absent, but it is not physical terrain evidence. Nine-theatre full/regional/close
captures and explicit owner acceptance remain outstanding; M2 stays blocking.
Real-game non-debug review proves that ridge systems produce physical 3D relief. A new
Arda-native material cache also proves continuous ground variation, mountain snow/rock
material, and shoreline transition bands instead of the former shared zero tile and
coarse location-shaped patches. A two-stage checkpoint route reached the then-current
12,104-location tree in stable non-debug 3D Observer, resolving that iteration's
resource-bound capture bootstrap. A later exact-state session proves that Hilbert-ordered
Arda transforms render
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
channels. Ground-level evidence on the 12,104-location baseline proves those clearances
and a parser-safe naturalized major-channel raster with installed downstream width
progression. That baseline entered no-debug Observer without a river or map diagnostic,
and its paired smoke was green with zero mod-unique lines. The source-frame replacement
must independently repeat both proofs. Multi-theatre evidence and explicit owner
acceptance remain outstanding; this gate remains red.

The first correctly targeted nine-theatre audit is captured under
`docs/screens/20260730_m2_theatres/`. It confirms that physical trees, relief, and custom
waters render, but rejects the regional presentation: location-scoped climate and
topography changes read as rectangular/Voronoi material patches, mountain-template paint
still forms oversized pale slabs, river-bank material reads as broad artificial
corridors, and the height shoreline exposes the 2x enlargement of the control lattice.
The next slice renders shoreline geometry at native height resolution, narrows secondary
river material, confines snow/rock paint to high crests, and makes woodland margins
depend on the continuous transform field rather than marginal whole-location templates.
The subsequent v14 close pass proved green, dense, porous Mirkwood canopy, but rejected
Fangorn because it rendered entirely snow-white on 4 August. This was not a material-cache
failure: the generated equator crossed Rohan at canvas y=4600, placing Fangorn's y=4984
south of it and therefore in southern-hemisphere winter. The map generator now places the
equator beyond the 8192-pixel southern edge and statically rejects any equator inside the
covered Middle-earth extent. Fresh exact-tree renderer proof is pending. The first
native-density retail load reached the country-selection transition but its automation
capture lost foreground. That run also exposed three setup regressions caused by the
density rebuild: lumber on neutral templates, an unowned Henneth Annûn town setup, and
discriminated Black Númenórean nobles in Umbar. All three are generator-fixed and covered
by validation; they must be confirmed absent in the next interactive source-frame
session.
M2 remains blocking.

## Binding defects

1. Inland seas, lakes, and forest regions read as geometric ovals rather than natural
   landforms.
2. Coasts are imprecise, overly smooth linework without convincing bays, estuaries,
   headlands, islands, or multi-scale shoreline detail.
3. Mountain systems do not present as physical close-zoom relief.
4. Forests, ground materials, and other terrain character are not visibly comparable to
   vanilla at close zoom.
5. Rivers are weak or invisible and do not read as a coherent drainage system.
6. The world needs substantially more geographic detail. Source geometry stays at full
   authored resolution while runtime political granularity is reduced only enough to
   enter the renderer; the renderer—not a headline count—must prove that refinement
   reads naturally at close zoom.

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
