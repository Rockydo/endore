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
mainland coast, 15 lakes, 43 mountain footprints, 100 river/valley controls, and forest
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

The current source-frame audit uses exact named-location targeting and a unique
all-land renderer biome. Fresh no-debug evidence accepts continuous Mirkwood canopy,
Harad sand, Mordor ash, Rhûn/Dorwinion ground, and Mount Doom's physical cratered cone.
It rejects the tiny source pool east of Hobbiton, the over-rounded Belfalas inlet, and
the former mountain model's broad grey plateaus. Two lake-template/bed experiments and
two mountain-template/compact-peak experiments were rejected and reverted. The current
mountain route instead interprets all 43 audited source polygons as low foothill
envelopes, makes the nine source-aligned axes and 18 exact named peaks carry high relief,
and makes the 10 passes high saddles. Fresh Observer views at
Khazad-dûm/Dunharrow/Goblin-town/Orodruin prove physical slopes, crests, and the cratered
Mount Doom. Slope-aware material selection removes the former whole-polygon grey plates,
but the same close views reject coarse exposed-rock ribbons/islands and the still-crude
political-cell scale. This is a retained component improvement, not gate acceptance.
The first source-ridge material-feather attempt then exhausted two post-cache fresh-load
attempts without renderer evidence and was reverted to the smoke-green v25 baseline.
The first materially different Shire-pool candidate kept all three source outlines as
wet material over continuous land rather than engine water. It passed static checks but
both permitted fresh New Games missed the post-cache interactivity bound without a
diagnostic. Generator v27 is rejected and restored to the v25 engine-water baseline; do
not relaunch it. The source outlines remain binding, while the visible tiny-water quarry
remains an explicit red defect requiring a genuinely different representation.

The later runtime investigation proved that those v27 misses were evaluations on the
unreliable 12,104-location memory cliff, not renderer verdicts. The same representation
was therefore reintroduced as generator v26 only after reducing runtime topology to the
fresh-load-proven 6,004-location budget. On fingerprint `e9d3a5f0`, paired smoke passed
and a fresh non-debug full-visual New Game reached country selection and live Observer in
115 seconds, then advanced through 3018.1.10. Fresh Hobbiton captures show continuous
ground with no rectangular water quarry. Separately, neutral surface templates for all
600 map-config-impassable mountain cells remove the giant grey/white location slabs in
the Khazad-dûm theatre while retaining the continuous source relief.

This is a retained intermediate correction, not gate acceptance. The new Khazad-dûm
regional capture still rejects patchy/geometric exposed-rock masks, several ranges need
stronger 3D readability, and the complete nine-theatre evidence set remains outstanding.
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

## Current load-safe intermediate — generator v28

Generator v28 retains the source-pinned movement and height model but replaces hard
material bands with a continuous field following all source ridge axes, branches, and
named peaks plus smoothed slope, altitude, and deterministic organic variation. Fresh
Khazad-dum evidence shows a more coherent crest-following massif, although the exposed-
rock fringe still needs softening and the complete nine-theatre review remains
outstanding.

The inland-water correction is systematic: all ten source lakes occupying at most 64
control pixels remain exact wet-material polygons over continuous terrain, while the five
larger lakes remain engine water. Fresh Mirrormere evidence removes the former deep
rectangular quarry but still rejects the flat replacement as final scenery.

The current exact game-visible fingerprint is `8ca808d7`. Paired smoke has zero new and
zero mod-unique lines. Two independent cold full-visual New Games reached country
selection and HUD-proven live Observer in 115-117 seconds. The corrected state-aware
monitor resumed exactly once and advanced from 3018.1.1 through 3018.1.15; the subsequent
Khazad-dum focus continued through 3018.2.1 with no error-log growth. This proves the map
loads and ticks; it does not green the physical-quality gate.

## Current source-relief candidate — v37

The coast remains provisionally frozen. Ardacraft Heightmap V2 now owns exact crest and
secondary-branch placement through a hash-pinned 1280×1026 5-bit numeric reduction; Arda
Maps owns outer mountain footprints, all 18 canonical summit points, and the 100-control
physical drainage atlas. The nine former hand axes retain only 18% continuity influence.
Twenty-four reviewed river trunks enter the parser-safe engine raster, while 76 additional
Arda Maps parts carve terrain/material drainage without creating unsupported affluent
graphs.

v30 and v31 are explicit rejection evidence. v30 expanded lower source response; v31
contracted it but still amplified the middle half of each massif. v31 nevertheless passed
paired smoke and entered fresh HUD-proven Observer, proving the rejection is visual rather
than a load regression. Orodruin's dedicated cone was accepted as a component; Gundabad,
Erebor, Morannon, and Dunharrow remained too broad.

v32 contracts the source response at exponent 1.90 and maps final relief through a convex
1.72-power profile. It also moves the Gundabad saddle off the exact summit and aligns
Erebor's anchor with exact Arda Maps `point_mount LonelyMountain`. The complete
6,004-location world regenerated with 174,763 terrain tiles, 2,038,645 Arda-native
vegetation transforms, and zero clipped height samples. Paired smoke passed with zero
mod-attributable lines and a fresh game entered live Observer in 116 seconds. The Anduin
width is visibly improved, but a correctly framed Gundabad view rejected its broad generic
summit cap. Cumulative close zoom invalidated the later Morannon/Dunharrow framing, so no
negative placement claim is inferred from those images.

v33 preserves every source range and changes only the redundant Gundabad point overlay to
a compact 0.0045 chain crown. It passed paired smoke with zero mod-attributable lines and
entered a fresh HUD-proven Observer in 126.3 seconds. Independent hard-reset regional
views accept Gundabad, isolated Erebor, and Orodruin as components. They reject the still
low, green Ered Lithui/Ephel Duath around Morannon and White Mountains near Dunharrow;
drifted close frames are excluded from that verdict.

v34 responds only to that live failure. It preserves exact source placement while
replacing the underpowered blanket 18% residual continuity with audited per-range weights
from 28% to 50%. Its broad/body/spine kernels are narrower and put 56% of their response
on the fine spine, so long named chains can read as connected rocky ranges without
becoming broad plateaus. Independent source-conformance floors now bind the northern
ranges, Erebor, White Mountains, and Mordor rather than allowing a global average to hide
a broken theatre. The complete 6,004-location, 174,763-tile,
2,038,645-vegetation-transform world regenerated with 279 ports and zero clipped height
samples; full validation is green. Exact-fingerprint paired smoke is pending behind
Antiquitas's shared EU5 session. It subsequently passed with zero new and zero mod-unique
lines, and a fresh game reached HUD-proven Observer in 126.4 seconds. Hard-reset regional
and target-relative close pairs accept Gundabad, isolated Erebor, and Orodruin as
components but reject v34 at Morannon and Dunharrow, whose adjacent source ranges remain
low and green. Invalid Carachost/Starkhorn overview frames are excluded. The gate remains
red pending a v35 final-height/material correction and the complete nine-theatre sweep.

v35 implements that downstream correction without moving cartography. Paths of the Dead
and Morannon use source-oriented anisotropic saddles instead of circular depressions. A
1.28 gain applies only to the exact Ardacraft crest field; an attempted blanket increase
to secondary range axes was rejected by the source-support guard. Earlier exposed-rock
transitions are scoped to the physically high White Mountains and Mordor walls. Static
contracts now require both a low route floor and dense high/exposed adjacent flanks at
Dunharrow and Morannon. The accepted Gundabad summit remains unchanged; its gameplay
access carve now joins a substantial continental land component instead of an enclosed
green pocket.

The pinned-toolchain production world has model SHA `8d31aa47`, 6,004 locations, 289
ports, 174,763 terrain tiles, and exact game-visible fingerprint `7b1e0917`. Full
validation is green. Exact-fingerprint smoke and the same reset five-target live camera
sequence remain pending behind Antiquitas's shared EU5 session. v35 is therefore a
technically green candidate, not visual acceptance, and the nine-theatre gate remains red.

v35 later passed exact-fingerprint paired smoke and reached fresh live Observer in 124
seconds. Its ten independently reset named-location frames are valid, but the visual
verdict is negative: Morannon and Dunharrow remain broad green uplands with scattered
high material patches rather than continuous enclosing walls. Erebor and Orodruin remain
accepted components. v35 is therefore rejection evidence, not the current candidate.

v36 gates stronger continuity through the exact Ardacraft support mask. Added gains apply
only to the White Mountains, Ephel Duath, Ered Lithui, and southern Mountains of Shadow;
unsupported portions of a reviewed hand axis receive no gain. Source conformance improves
to 99.6845% global high-ridge support, 98.7299% in the White Mountains, and 99.5990% in
Mordor. The 6,004-location production model `e03c16e1` regenerated with 306 ports and full
validation passed on exact fingerprint `a9de05d5`. Corrected paired smoke passed with zero
new and zero mod-unique lines, and a fresh world reached HUD-proven Observer in 110.8
seconds. Five independently reset regional/+3 close pairs are valid. They retain Erebor
as isolated and Orodruin as discrete, but reject v36: Gundabad's visible crown is offset
behind a broad green hill, Morannon still reads as a broad uplift with a peripheral slab,
and Dunharrow still lacks a convincing jagged White Mountains wall. The first attempted
fresh run is excluded because automation clicked Continue's lower edge and opened the
incompatible-save/Continue-as-Observer modal; its screenshot proves the UI error, not a
map-load failure.

v37 is the current offline candidate. It doubles the committed numeric relief to
1280×1026 and five-bit precision, separates foothill response from upper arêtes, removes
normalization clipping above 36,000, and concentrates source-supported range axes into
narrow 86%-spine profiles. Bounded flank/material contracts explicitly fail both sparse
green bowls and broad caps/slabs. Mordor no longer derives its surface silhouette from a
Mount Doom-centred ellipse: its ash field fills only the Ered Lithui/Ephel Dúath/southern
Mountains of Shadow enclosure, keeps the basin dark, and exposes lighter rock only on
high steep crests. The complete model `14a84668` regenerated in 325.0 seconds; full
validation passed in 367.2 seconds on fingerprint `97e271fb`. Exact smoke is pending—not
failed—behind Antiquitas's active shared EU5 lease. No v37 visual claim is accepted until
fresh Observer repeats the same Gundabad/Erebor/Morannon/Orodruin/Dunharrow reset pairs.
The gate remains red.

v37 later passed exact paired smoke and entered a corrected, genuinely fresh HUD-proven
Observer in 201.2 seconds. The five reset pairs reject it: broad synthetic tablelands remain
at Gundabad and around the southern walls, while Orodruin reads as a mesa. This evidence
proves loadability but closes v37 as a visual candidate.

v38 is the current offline candidate. Ardacraft's numeric relief owns every source-backed
range without overlaid hand axes, Gaussian pass flanks, or named summit lobes. Erebor and
Morannon use their direct Ardacraft markers; only the raster-empty Mindolluin and Irensaga
receive compact source-gap summits. The cubic 68k upper-arête response reaches 64,493 with
no clipped sample, Orodruin is a compact 63k cone, and all four theatre-support contracts
remain above 99.79%. Mordor's ash field now flood-fills the exact U-shaped source mountain
wall with a bounded irregular eastern transition rather than thresholding a rounded
proximity blob. Model `fefa695d` regenerated with 6,004 locations, 292 ports, and a
complete 199.9 MB Arda-only terrain cache. The pre-enclosure candidate passed validation;
the final tree still requires full validation. Exact smoke deferred cleanly behind
Antiquitas's active shared lease; paired smoke and fresh live comparison remain mandatory.
The gate remains red.

v38 later passed final validation in 372.7 seconds, exact paired smoke with zero new or
mod-unique lines, and a fresh HUD-proven Observer start in 124.3 seconds. Its five reset
pairs reject it: quantized and saturated relief produces flat-topped mesas. Evidence is
retained under `docs/screens/20260801_m2_ardacraft_relief_v38/`.

v39 retains the pinned source response at native
2500x2003/8-bit precision, removes both high-sample saturation paths, and builds named
summits plus Orodruin only at final terrain resolution. Anti-mesa checks bind 39,672
samples above 45k and an 8.94% low-gradient cap fraction. Erebor, Gundabad, Dunharrow,
and Orodruin have compact 60-61k summits; exact Morannon arms reach 50.9k around a 12.7k
gate. Model `9f022ce3` has 6,004 locations, 298 ports, and a 171.7 MB cache. Full
validation, exact paired smoke, and a genuinely fresh Observer load pass. Five independent
reset regional/+3 pairs reject the candidate: Morannon lacks the two source walls at the
camera-visible hinge; Gundabad and Erebor retain smooth radial crowns; Orodruin reads as
several lobes; and Dunharrow's White Mountains remain discontinuous cliff blocks. The
evidence is retained under `docs/screens/20260801_m2_ardacraft_relief_v39/`.

v40 kept the pinned coordinates but replaced raw
warm-rock shelves with a continuous 4/12/18-pixel source-native body/shoulder
reconstruction. Its major range gradients now occupy a vanilla-calibrated interval while
crests remain 52-55k; Erebor and Orodruin reach 61.4k. Source-backed named peaks receive
only tiny exact-coordinate teeth, Gundabad uses its measured junction, and severe rock
follows narrow reconstructed crests rather than legacy hand axes. Morannon retains the
direct gate marker plus two drawing-confirmed short hinge arms to the nearest exact Ered
Lithui and Ephel Duath samples; its oriented saddle remains low. Model `7f48ab78` has
6,004 locations, 282 ports, and a complete 180.1 MB cache. Full validation, exact paired
smoke, and the same fresh five-pair live review remain mandatory. No river or political-
boundary work may begin until those views pass. Full validation, exact smoke, and two
fresh Observer starts subsequently passed, but exact-target live frames reject v40:
Erebor is a broad isolated stump and weak regional hill, Gundabad is a green basin inside
flat rock carpet, and Morannon is a low grassy V. The initially retained Snowpoint frames
are excluded because Finder did not own keyboard focus; the driver now explicitly focuses
and clears its edit box.

v41 is the current offline candidate. It changes no source coordinate, coast, pass floor,
or political cell. A tighter 3/8/15-pixel Ardacraft reconstruction, one moderate control
gamma, and a convex 55k response produce 307,474 samples above 45k with
720/1,270/1,895 median/p75/p90 gradients: between v40 hills and v39 shelves. Erebor is
narrowed, Gundabad gains a compact exact-point crown, the Morannon hinge spines are taller
and narrower, and Orodruin's lobing harmonics are reduced. Model `35fc4a7c` has 6,004
locations, 292 ports, and a 172.3 MB complete cache. Static source/height/material gates
pass. Full validation, exact-fingerprint smoke, and a fresh correctly targeted five-pair
review remain mandatory; the gate remains red.

v41 subsequently passed full validation, exact paired smoke, and a fresh HUD-proven
Observer. Its exact-target frames reject it: Erebor and Orodruin improve, but Gundabad is
still a green basin within rock carpet, Morannon combines a broad wall with a visibly
straight synthetic arm, and Dunharrow is two isolated spikes instead of one chain.

v42 is the current offline candidate. Ardacraft's pale neutral summit spine is now decoded
alongside warm-rock shoulders; the previous reduction had discarded the source raster's
best jagged height signal. Synthetic Morannon arms and ordinary source-backed point teeth
are removed, leaving continuous source-native Mordor and White Mountains geometry.
Static source, height, and material preflights pass. Model `987245ab` regenerated with
6,004 locations, 293 ports, and a 173.8 MB complete cache. Full validation,
exact-fingerprint smoke, and fresh live review remain mandatory; the gate remains red.

v42 subsequently passed full validation, exact paired smoke, and a fresh HUD-proven
Observer load. Its ten exact-target frames reject it: broad exposed-rock mass persists at
Gundabad, Erebor splits into two oversized neighbouring mounds, Morannon remains a low
rounded berm, Orodruin is too broad, and Dunharrow's surrounding chain remains smooth.
Evidence is retained under `docs/screens/20260801_m2_ardacraft_relief_v42/`.

v43 is the current offline candidate. It leaves all audited coordinates fixed and
compresses the warm shoulder field beneath a >=0.92 true-arête band. Terrain above 45k
falls to 224,227 samples while retaining 869/1,718/2,641 median/p75/p90 gradients and a
37.2% low-gradient fraction. Erebor is de-duplicated into one direct-marker summit,
Gundabad receives a compact exposed crown, Orodruin is narrowed, and only pre-existing
high source relief is amplified around Morannon. Model `16e5d549` regenerated with 6,004
locations, 300 ports, and a 168.8 MB complete cache. Offline height/material gates pass;
full validation, exact smoke, and fresh live comparison remain mandatory. The gate stays
red.

v43 subsequently passed full validation, exact paired smoke, and a fresh HUD-proven
Observer. Exact-target views accept one isolated Erebor and the compact pointed Orodruin,
but reject the long ranges: Gundabad remains visually broad, Morannon's northern/eastern
wall stays low, and Dunharrow remains surrounded by smooth green ridges. Evidence is
retained under `docs/screens/20260801_m2_ardacraft_relief_v43/`.

v44 preserved every v43 coordinate and footprint while increasing final-resolution signed
folds and sparse summits only inside the existing mountain-strength envelope. The complete
world regenerated with model `16e5d549`, 6,004 locations, 300 ports, 239 route edges,
2,038,645 vegetation transforms, 25,332 unique height tiles, and 63,900 unique material
tiles. Full validation passed, exact paired smoke passed on fingerprint `312aa575` with
zero new and zero mod-unique diagnostics, and a fresh HUD-proven Observer started. The live
five-target review rejects it: Gundabad gains a few exposed crest patches but remains
broad, Morannon's northern/eastern wall remains low, and Dunharrow remains a smooth green
ridge system. Erebor remains one isolated massif and Orodruin remains a compact pointed
cone. The next pass must begin with matched installed-vanilla mountain captures and derive
renderer-scale width/height/material ratios before changing v45. The gate stays red.

Matched installed-vanilla close/regional captures at Chur, Shey, and Kathmandu then
established that v44's raw relief was already steeper than vanilla. The v45 response
therefore contracted Gundabad's broad upper body and redistributed relief toward finer
facets rather than raising the ceiling. Its pinned coherent world regenerated in 600.9
seconds; full validation passed in 381.3 seconds; exact paired smoke passed in 209.9
seconds on fingerprint `3d769297`; and a genuinely fresh live Observer started in 126.1
seconds. Static morphology improved Gundabad's radius-96 upper-quarter area from 20.2% to
8.2% while preserving Erebor and Orodruin.

The live gate nevertheless rejects v45. Evidence under
`docs/screens/docs/screens/20260801_v45_mountain_review/` shows a theatre-scale pale cap
at Gundabad, repeated terrace/facet bands and disconnected rock blocks at Dunharrow, and
an unreadable northern/eastern Morannon enclosure around the correctly low gate. Erebor
remains one isolated form and Orodruin remains a compact cone. v46 must remove native-
frequency corrugation and globally widened exposure thresholds, retain the accepted
source geometry and local forms, and introduce smooth source-aligned arÃªtes plus feathered
connected material. The terrain gate stays red; rivers and politics remain blocked.

v70 is the retained mountain candidate after source-aligning the Ered Lithui and Ephel
Dúath axes, removing the broad Morannon junction body, and making the exact gate a low
hinge whose two arms rise toward the source walls. Owner review accepts the substantial
mountain improvement as the current direction but has not accepted the complete
nine-theatre terrain gate. Fresh v70 reached country selection; two externally requested
OS quits prevented a new live evidence set and are recorded in `BLOCKERS.md` rather than
misclassified as map crashes.

The following forest checkpoint keeps every woodland boundary fixed and replaces the
2.04m high-only-biased object distribution with a 3.057m all-LOD distribution. Mirkwood
must prove near-continuous canopy at regional and close zoom; Lothlórien must prove dense
light-trunk deciduous coverage with no conifer intrusion. Required evidence is a fresh
HUD-proven Observer plus reset regional/close pairs at Mirkwood and Caras Galadhon, then
the complete nine-theatre refresh. Static transform counts or green biome tint alone do
not pass this gate.

v71 clears the focused forest-density checkpoint. Full validation passed after one
coherent regeneration on model `6048d0cc`; a fresh New Game reached the live Observer HUD
on exact fingerprint `06e7c07e`; and the evidence under
`docs/screens/20260802_v71_dense_forests/` shows closed Lothlórien canopy with light trunks
at close zoom plus theatre-scale mixed Mirkwood canopy at regional and close zoom. A
45-second playback advanced nine days while responsive. No source forest polygon changed,
and no map/terrain/vegetation/mesh diagnostic appeared. This accepts the all-LOD density
and Lothlórien species mechanism, not the complete nine-theatre gate: source-edge,
river-clearance, and remaining physical-theatre review stay open, followed by the
per-location political reassignment audit.

v72 clears the focused political-reassignment checkpoint without claiming the complete
nine-theatre physical gate. The generated audit covers all 5,200 land locations and
reports zero source-envelope violations. Lothlórien, Dunland, Iron Hills, Woodland Realm,
Woodmen, Dol Guldur, Erebor, Fangorn, and Isengard now satisfy hard compact-connectivity
contracts; lower-confidence East/South region claims are separately distance-bounded.
Fresh live frames under `docs/screens/20260802_v72_political_boundaries/` prove the 44-cell
Lothlórien claim east of Moria and the 47-cell Dunland claim west of Isengard in the real
political renderer. Observer advanced nine days, full validation passed, and paired smoke
added zero error-log lines. Physical river/source-edge and remaining nine-theatre review
stay open; future political additions require distinct TA 3018 evidence rather than a
desire to fill neutral land.

v73 is the focused source-drainage candidate. It replaces duplicated/flat supplementary
marks with 102 non-duplicated, classed Arda Maps controls and promotes only Lefnui and
Serni where exact source courses can safely reach engine water. Sirith, Lhûn's true Y,
and the complete Ethir remain strong physical drainage instead of fabricated independent
parser lines. Full validation passed after one coherent regeneration. A fresh visual New
Game reached HUD-proven Observer on fingerprint `c9b21485`; regional and close frames
under `docs/screens/docs/screens/20260802_v73_river_hierarchy/` prove the broad Anduin at
Caras Galadhon/Osgiliath, retained dense Lothlórien canopy, and multiple narrower
Gondor/Lindon channels. Observer advanced nine days with no map/river diagnostic. Paired
smoke initially lease-deferred behind Antiquitas, then passed at the next natural
checkpoint in 201.5 seconds with exactly zero new mod lines. This clears the focused v73
river checkpoint; the complete nine-theatre physical/source-edge review remains red.

v74 clears the reopened focused forest-density and source-shaped political checkpoints.
The fixed 3.057m renderer budget now places 760,747/567,263/561,115 transforms in Mirkwood
and 70,991/50,758/50,250 light-trunk-only transforms in Lothlorien across high/medium/low
LOD while retaining Fangorn, Old Forest, and Ithilien floors. The political generator no
longer treats rectangles as woodland evidence: six woodland polities require complete-cell
overlap with their hash-pinned Arda Maps source mask, and Dunland follows a seven-vertex
lowland polygon. The 5,200-location audit has zero violations and every affected compact
realm is contiguous. Fresh real-game evidence under
`docs/screens/20260802_v74_dense_forests_source_claims/` shows an irregular 21-location
Lothlorien outside the Misty Mountains, dense light-trunk interior canopy, near-continuous
Mirkwood canopy, and the smaller Dunland silhouette. A fresh Observer advanced from
TA 3018.1.1 to 3018.1.15 without recovery or any error-log growth. This does not clear the
complete gate: Forochel, Belfalas, Rhun, Harad, macro materials, small water presentation,
and the full source-edge sweep remain red.

v75 clears the focused vegetation/source-shaped-ownership checkpoint. Static vegetation
contracts now make the complete
tundra sparse while increasing the already accepted Lothlorien and Mirkwood counts. Both
climate-material experiments are rejected: v44 rendered Harad as green earth with pale
sand islands, while v45 rendered enormous dark rock blotches. The complete v43 material
source, preview, and 174,763-tile cache were restored with zero diff. Retain both v75
climate evidence directories as negative calibration evidence. Fresh v75c forest and
political frames, post-rollback full validation, a separate untouched 45-second v75d
playback with baseline-only error log, paired zero-new-line smoke, and exact
`assert-smoked` all pass on fingerprint `fb07a215`. Harad, Forochel, and the wider
nine-theatre material gate remain red.

v79 is the current source-biome/topology candidate. It replaces the remaining proof-era
Brown Lands, Rhûn, Near Harad, and Far Harad climate envelopes with a hash-pinned
classification and simplified-ring reduction of Ardacraft's detailed biome atlas. The
control gate binds 1/41/37/7 components and minimum vertex floors for those four groups;
east/south continuations are explicit judgement controls rather than straight clipping
or invented ocean closure. Mordor ash retains final precedence. The regenerated material
preview shows varied western Rhûn steppe, Near Harad scrub/woodland, and aridity only
farther south instead of uniform green or one pale sand blanket.

The climate-density change reseeded generated location IDs. Schema 3 correctly rejected
v78's now-stale component dispositions before live testing. v79 replaces them with
coordinate-witnessed, contract-checked repairs and exact dispositions for every physical
barrier split; the static political result has zero claim violations and no unreviewed
component. This is not live acceptance. Fresh Rhûn, Brown Lands, Harad, political
overview, 45-second playback, paired smoke, and the complete nine-theatre renderer sweep
remain mandatory; the gate remains red.

v80 is the current dense-forest/complete-frontier candidate. A fresh v79 Observer and
45-second playback first proved the pre-edit world still loads and ticks cleanly on exact
fingerprint `1f899f22`; close views then reproduced the owner's Mirkwood/Lothlorien
density rejection. v80 raises the renderer corpus to a bounded 3,493,385 transforms and
protects continuous ancient-forest interiors at all LODs. Static counts are
1,112,756/796,168/788,083 in Mirkwood and 87,564/69,865/69,863 light-trunk-only in
Lothlorien. These counts are not visual acceptance.

The political audit now binds all 38 realms to explicit physical contracts. Lothlorien
and each Mirkwood controller must satisfy both source woodland overlap and an irregular
theatre partition. Harnendor, Near/Far Harad, Khand, and the three Rhunic controllers no
longer fill their technical regions by unconstrained Voronoi distance; irregular bounded
spheres leave wilderness where TA 3018 control is unattested. The result has 3,044 owned
and 2,156 wild land locations, zero violations, zero unreviewed components, and zero
uncontracted realms. Required acceptance evidence is a fresh v80 HUD-proven Observer,
reset regional/close forest pairs, a wide live Wilderland political view backed by the
tagged full-world QA raster, 45-second playback, paired zero-new-line smoke, and exact-
fingerprint assertion. The full nine-theatre gate remains red regardless.

v80b clears the focused live forest/frontier verification but not the complete M2 gate.
The first v80 wide-canopy Lothlorien calibration is retained as rejected evidence under
`docs/screens/20260802_v80_dense_forests_frontiers/`. v80b uses only the installed slimmer
light-trunk oceanic tree variants for Lothlorien; all counts, source masks, and placements
remain unchanged. A fresh New Game reached HUD-proven Observer on exact fingerprint
`2df4b63d`; the frames under `docs/screens/20260802_v80b_birch_meshes/` show pale trunks,
closed Lothlorien broadleaf canopy, darker near-continuous Mirkwood, and a wide live
Wilderland political view. The tagged generated QA raster supplies full-world coverage
of the contracted East/South realms and wilderness buffers. A 45-second maximum-speed
playback required zero recovery and ended at the exact 1,486-byte baseline error log.
Final full validation passed in 430.5 seconds. After Antiquitas released its healthy
session, paired vanilla/ENDORE smoke passed at the next natural checkpoint in 200.8
seconds with zero mod-unique error lines, and exact-fingerprint assertion binds the pass
to `2df4b63d9be5180089d9d74fa4b61fb4c22f4c94020d481c394b3b02d0140e63`.
The focused v80b forest/frontier checkpoint is accepted; the complete nine-theatre
physical review remains red.
