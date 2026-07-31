# Decisions

## 2026-07-29 — M5 census slice and road-source contract

Treat the authored nine-route ledger and its 302 adjacent land edges as source data, not
as permission to install a runtime road graph. EU5 requires a matching Arda-native strip
inside `spline_network.splnet` for every starting road edge. The two bounded map-editor
attempts could not produce that binary, and the installed Earth cache may not survive.
Therefore M5 emits an explicitly empty `road_network` while continuing to validate every
route waypoint and edge. Markets, settlements, development, census, raw materials, town
setups, and provisional pre-M7 armies remain independently shippable.

The M5 demographic total is 9.029 million for the represented map extent. This is a
gameplay census, not an assertion that Tolkien supplied numerical totals. Installed
culture presences remain parser ABI only and are excluded from all authored totals.

## 2026-07-29 — Physical-map gate precedence

Treat political-shape screenshots as insufficient evidence for any custom-map milestone.
M1/M2 is green only when the same authored coordinates agree across the political raster,
16-bit height source, complete virtual terrain cache, and close physical renderer. The
owner's close-zoom report superseded the earlier gate immediately; unfinished M3 realm
work was isolated until the physical world was corrected.

Use the installed raw-height waterline as an enforced generator contract. Keep every
authored water sample below it and every ordinary land sample safely above it after river
incision. Own the complete terrain cache and suppress every installed Earth-authored
generated/static transform definition through deterministic exact-file overlays.

## 2026-07-29 — Later generated-art reference direction

For every later generated bitmap family, use precise real EU5 assets as the primary style
and format references and actual images from Peter Jackson's three *Lord of the Rings*
films as additional art-direction references. Film material guides mood, production
design, costume, landscape, and lighting only; Tolkien canon remains authoritative for
content. Reference images stay in a gitignored G:-drive cache and are not redistributed.
Icons are generated four distinct designs per sheet, split locally, and individually QA'd.

## 2026-07-29 — M3 political contract

Ship 38 first-class realm tags in the first political partition. Fold Minas Morgul into
Mordor as a fortress-location rather than a separate country; use the plan's micro-tag
allowance for Qarsad of Harad and a third Rhûnic confederation so the sparse South and
East have playable texture.

Political ownership is generated only for passable-land locations. Sea zones, lakes, and
impassable mountains are always unowned, and selected desolations remain deliberately
wild. The M3 validator projects the exact realm lookup onto the authored elevation control
and fails if any owned pixel lies at or below the installed waterline, if any non-land
location receives an owner, or if a capital snaps materially away from its authored seat.
This makes the owner's reported “labels/colors in the ocean” failure mechanically
non-regressible.

Keep the installed monarchy, culture, faith, and demographic registries only as
parser-safe technical bridges. M4 replaces culture and faith, M5 replaces the census, and
M6 replaces government titles and rulers; none of those visible placeholders is accepted
as final Middle-earth content.

## 2026-07-29 — M2 deep-load quarantine

Keep the M2 inherited-content quarantine exact, generated, and milestone-scoped. The
production world retains one installed technical country only to satisfy the setup
contract. Installed cultures and religions receive a tiny technical census so their
retained registries validate; Earth country setup, unsafe hardcoded on-actions, flag
predicates, historical schedules, and unreferenced Earth-only static modifiers are
neutralized by deterministic exact-file overlays.

Guard retail building `market` scopes during the neutral world's first tick and disable
Earth dynasty comparisons where the corresponding historical database is deliberately
absent. These are parser/runtime isolation measures, not ENDÓRË content. M3 and later
replace the scaffolds as bespoke databases become authoritative.

## 2026-07-28 — Workspace path precedence

The explicit task path `G:\EUV mods\endore` supersedes the older `G:\endore` path embedded
inside the master plan. Runtime user data remains at `G:\endore_user_data`.

## 2026-07-28 — Installed DLC playset

Use the same four installed content entries as the proven ANTIQVITAS environment:
`D000_shared`, `D008_fate_of_the_phoenix`, `D015_ancient_monuments_pack`, and
`D017_sacred_sites_pack`. This maximizes reproducibility on this machine and preserves
the monuments framework for later Middle-earth landmarks.

## 2026-07-28 — Bootstrap thumbnail

Use a temporary 512×512 recomposition of the installed EU5 paper-map table texture for the
M0 metadata contract. It is explicitly tracked for replacement through the reference-driven
art pipeline before M11 and is not treated as bespoke final art.

## 2026-07-29 — M1 proof-world scope

Use exactly 300 installed location identities and colors on a new Middle-earth-shaped
geometry: 50 sea, 190 plains, 10 lakes, 20 impassable mountains, and 30 forests. Group
them into 30 temporary provinces and one temporary owned realm using the installed `SWE`
identity solely to satisfy the start contract. These are engineering scaffolds, not world
content; M2 replaces the hierarchy and M3 replaces ownership.

The accepted proof canvas is 16384×8192 because it matches the installed renderer contract
and remained stable at roughly 5–6 GB. M2 will still study and target the plan's 8192×4096
production canvas before committing the final projection.

## 2026-07-29 — Temporary geography compatibility overlays

Generate token-level overlays for retained retail scripts that name removed Earth
geography. They preserve the engine definitions required to reach a playable 300-location
world while redirecting only geography symbols to the proof hierarchy. Every file is
marked as M1-only, generated from the read-only install, and listed in a manifest. M2 must
remove the entire layer during its quarantine sweep; none of these overlays are final
Middle-earth content.

## 2026-07-29 — Locator source of truth

Use the automated engine command `MapObjects.GenerateGameLocators <type>` to establish
eligibility, then encode the resulting rule in the generator. Combat and unit-stack
locators cover all live locations except impassable mountains (280 of 300); deterministic
member-cell positions are valid and avoid any manual map-editor step.

## 2026-07-29 — M2 projection and hierarchy split

Use an original 2:1 normalized projection covering Lindon to western Rhûn and Forochel to
northern Far Harad. It is authored from textual relative geography and travel logic, not
traced from a published map. The production location canvas is 8192×4096, with 1024×512
committed controls and a 4096×2048 terrain heightmap target.

Use six top-level strategic geography groups in the production hierarchy: Eriador,
Forodwaith, Rhovanion, Gondor, Mordor-and-Rhûn, and Harad. Rohan belongs to Rhovanion
because its strategic ties and movement corridors run through the Gap of Rohan and Anduin
system; Gondor remains a distinct group for useful map-mode scale. Mordor and western Rhûn
share a top-level group because each is too narrow for balanced UI regions alone and their
eastward strategic theatre is tightly linked.

## 2026-07-29 — M2 production location model

Generate 5,812 deterministic locations from the authored controls: 5,200 passable land,
260 impassable mountains, 32 lakes, and 320 sea zones. The density-weighted seed model
pins all 41 cited settlement anchors and uses a minimum control-cell area of eight. This
stays within the plan's intended land-location range while leaving explicit tactical
classes for mountain barriers and inland water.

Follow the installed parser's six-level hierarchy contract rather than the plan's
five-name shorthand: continent, subcontinent, region, area, province, location. ENDÓRË
uses six continents, six corresponding subcontinents, and 24 authored strategic regions.

## 2026-07-29 — M2 inherited-reference compatibility

Retain the installed named-location color registry as unpainted definitions and allocate
all ENDÓRË colors from a disjoint set. This is not retained Earth content: it is a parser
compatibility measure for inherited files that still resolve location tokens during the
quarantine phase. No installed location occupies a pixel in the production world.

The generated M2 quarantine overlays replace the M1 proof overlays and redirect remaining
installed geography references to one valid Middle-earth hierarchy path. They are exact,
marked, deterministic source transformations and remain milestone-scoped scaffolding to
be deleted as inherited Earth scripts are retired.

## 2026-07-29 — M2 setup placeholders

Use installed `catholic`, `swedish`, and `wheat` values as explicit temporary parser-safe
religion, culture, and raw-material defaults for the 5,200 passable locations. Real-game
evidence requires a raw material on every passable land location. These values make no
lore claim and M4–M5 must replace them completely with bespoke Middle-earth systems.

## 2026-07-29 — M2 ports and authored crossings

Restrict naval ports to sea zones. Esgaroth is deliberately represented as a lakeshore
settlement without a naval-port edge because the installed dock validator rejects lake
endpoints.

Ship M2 with the proven zero-byte `adjacencies.csv` fallback. Two bounded A/B attempts
showed that any non-empty file on the custom canvas causes an empty-location lookup even
when its rows are valid. Keep the intended Himling and Tolfalas crossings in generator
source, but do not activate them until a later editor-backed contract is proven.

## 2026-07-29 — M4 people model

Model the playable world with 33 cultures in 10 broad culture groups. Rangers remain a
social and military identity inside the Dúnedain rather than a separate ethnicity.
Trolls remain units or special populations rather than a first-class culture. Orcs are
split by sustained regional communities where gameplay and lore support the distinction.

The installed engine rejects arbitrary language-family keys, so eight semantic
Middle-earth families map onto fixed installed family adapters whose visible names are
fully relocalized. Ten language roots and 33 culture dialects drive name pools. Major
roots target at least 60 male, 40 female, and 30 house names; minor roots target
30/20/15. The generated localization contains 1,105 name entries.

Model spiritual allegiance with 10 faiths in three gameplay groups: Light, Shadow, and
Old Ways. These are not organized-church claims. Every inherited religion file is
exact-overlaid with `enable = 3200.1.2`, keeping its parser symbol available while making
it unavailable throughout the ENDÓRË campaign.

## 2026-07-29 — M4 installed culture ABI

Installed culture keys behave as a compile-time ABI in this build: removing or disabling
them produces widespread invalid-key failures. Keep one distributed size `0.01`
compatibility presence per custom-dominant land location while assigning all visible
dominant populations and realm primaries to authored Middle-earth cultures. These ABI
presences never dominate and make no worldbuilding claim.

A size `0.001` experiment is rejected because the engine rounded it away and reported
2,086 cultures without populations. The narrow Sinicization compatibility overlay keeps
the installed script structure and variable reads intact while replacing only its
country-base lookup with zero, preventing a selection-screen type error.

## 2026-07-29 — M5 robust population-ABI hosts

Assign the 2,086 size `0.01` compatibility populations only after the authored census has
been allocated, selecting the 2,086 largest custom-dominant locations and enforcing at
least 1.0k authored population per host. Fresh-game evidence rejected 23 ABI populations
placed in 0.063k–0.095k Lossoth locations even after reducing their setup entry count,
while larger Lossoth hosts were accepted. The robust-host policy keeps compatibility
populations non-dominant without inflating them or encoding inherited cultures as lore.

## 2026-07-29 — Owner visual review reopens M2 as the blocking gate

The current map proves that a self-contained Arda canvas loads, but it is not an accepted
production map. Owner close-zoom review found geometric oval inland waters and forests,
imprecise line-like coasts, absent visible mountain relief, absent forest and terrain
detail, weak or invisible rivers, and insufficient geographic polish/granularity.

Suspend new M5–M12 gameplay, faction, mechanic, lore, and art expansion. Preserve already
green work, but return active development to Part 5 and require a vanilla-detail
player-facing physical map before resuming later milestones. The full native 16384×8192
locations canvas is already in use; “larger” therefore means improving Middle-earth's
footprint on that canvas and its locations-per-region density, not inventing an
unsupported larger raster contract.

## 2026-07-30 â€” Reopened-M2 natural geometry and native vegetation

Keep the proven 1024Ã—512 control/location ABI for the first physical-production slice so
all 5,812 downstream locations remain mechanically regenerable while relief and hydrology
stabilize. Replace source primitives with hand-authored polygon vertices and apply
deterministic multi-frequency perturbation only between those vertices.

Model mountain systems as broad shoulders, irregular overlapping massifs, local rugged
height octaves, and explicit valley/pass cuts. Impassable classification follows authored
cores; foothill relief is physical rather than an impassable wall. The White Mountains
are shifted south of Edoras and Minas Tirith.

Reuse installed EU5 vegetation meshes and exact LOD layers, but generate every transform
from ENDÃ“RÃ‹ biome controls. Never re-enable retail Earth transform bins. River previews
may retain smooth interpolation, but the engine raster uses four-connected authored
polylines for 12 independent major channels. All 23 axes remain height/valley controls,
but custom affluent junctions are omitted because neither naturalized nor retail-style
red-endpoint variants were parser-safe.

Quantize only the derived terrain-cache height tiles to 512 units so the single payload
stays below GitHub's 100 MiB hard limit. Preserve the authored 8192Ã—4096 16-bit heightmap
at full precision and keep all generator/check manifests explicit about the cache quantum.

## 2026-07-30 — Reopened-M2 native-detail lattice

Raise the authored physical-control lattice from 1024×512 to 4096×2048 while retaining
the installed-proven 16384×8192 locations canvas. This reduces source-derived coastline
steps from 16 engine pixels to four and supports 11,200 passable land locations without
changing the engine raster contract.

Use 520 impassable mountain locations, 64 lake locations, and the proven 320 sea-zone
count, for 12,104 locations total. Attempts at 520, 480, and 440 sea zones over-partitioned
a narrow coastal pocket whose two zones shared only one eligible land port; 320 preserves
the complete 605-port one-to-one contract while shoreline precision remains controlled by
the higher-resolution source mask.

Scale location-seed spacing with the new lattice and pin infrastructure routes only to
named anchors. Tharbad and Fields of Nurn replace obsolete generated-number waypoints.
Widen the High Pass cut around Goblin-town so the hold remains connected through the
Misty Mountains rather than becoming an isolated passable island.

Treat every passable location as requiring a land path to a legal port component. Ridge
anchors now carve narrow access paths rather than isolated 3×3 cells, and unprotected
mountain-enclosed land pockets are absorbed before seeding. The first live smoke exposed
14 such locations that the former capital-only static check missed; the generator now
checks all 11,200 passable locations.

Assign raw materials from each location's dominant biome, matching the terrain-template
emitter, rather than from its seed pixel. A seed-pixel mismatch assigned lumber to two
grassland locations during the live Observer gate; dominant-biome allocation and a
lumber/forest compatibility invariant prevent recurrence after map regeneration.

## 2026-07-30 — Arda-native continuous terrain materials

Generate the terrain-cache material layer directly from ENDÓRË's continuous biome,
height, river, and projection controls. Use the installed 16-bit bitmask ABI and only the
universally populated material-variation slots 10-12. Blend neighboring variation bits
instead of assigning hard location-sized patches.

Keep `index_map.bin` and `intensity_map.bin` empty because they are Earth-authored decal
layers, not required material paint. Never copy installed Earth cache payloads. Record
source hashes, coverage, tile diversity, preview hash, and output sizes in the manifest,
and fail validation if the material layer regresses to a shared placeholder tile.

## 2026-07-30 — Crop beyond-edge Rhûn and Harad as land

Supersede the rounded-island outline and the earlier 320-sea-zone density. The plan says
beyond-edge lands are handled by the map border: western Rhûn therefore continues through
the east edge and Far Harad through the south edge. Only actual western and internal
waters remain water. A 25% heightmap-water floor replaces the old one-third heuristic;
the authored crop is 29.87% water and still cannot regress to an accidental all-land map.

The reduced true-ocean footprint cannot sustain 320 unique sea-zone ports. Use 200 sea
zones and transfer the 120 cells to passable land, preserving exactly 12,104 locations:
11,320 land, 520 impassable mountains, 64 lakes, and 200 seas. Keep the strict one-port
per coastal water-zone matching invariant.

Engine-reported localization hash collisions are never baselined. Remap the specific
`me_belfalas_sea_area_30_21` runtime key to a deterministic `_arda` suffix while retaining
its generated display label and geography.

## 2026-07-30 — Spatial vegetation batches and high mountain cores

Treat generated map-object transform order as part of EU5's renderer ABI. The installed
bins keep contiguous instance records spatially local, consistent with range-based
generated-instance batching and culling. Serialize each ENDÓRË mesh/LOD payload on a
16-bit Hilbert curve and reject bins whose median consecutive distance exceeds 250 world
units or whose median 32-record span exceeds 800. This changes only disk order: all
positions, rotations, scales, and meshes remain deterministic Arda-derived placements.

Separate physical mountain relief from the gameplay mountain material/classification.
Broad massif shoulders and foothills remain in the height field, but only modulated ridge
values above 0.56 receive the mountain topography template. This preserves physical
barriers and passes while preventing whole ranges from becoming uniform snow/rock
ribbons.

The terrain-cache river channel is a visible wet-corridor material, not the parser's
one-pixel directed graph. It therefore follows naturalized control paths, shares the
Baranduin source/mouth corrections, and uses a stronger downstream taper. The parser
raster remains unchanged and authoritative for river topology.

## 2026-07-30 — Porous margins and vanilla-density Arda vegetation

Keep forest polygons as binding large forms, but never serialize or render their vector
boundaries as a wall. Deterministic broad fields feather each woodland, and Arda-native
transforms are weighted continuously across its margin. Internal glades suppress only
object placement; they do not cut holes in the discrete gameplay biome.

Reject transition paint along every generated location-biome boundary. A live close
probe showed that this makes the renderer emphasize pale Voronoi patches rather than
hide them. Terrain transition bits remain tied to the authored continuous atlas, while
dense, feathered physical tree coverage carries the forest margin across location seams.

Match vanilla's installed transform counts per forest, woods, and pine LOD: about 10.2
million deterministic Arda placements rather than the proof batch of 420,000. All bins
remain Hilbert-ordered and every position remains generated from ENDÓRË controls.

Exclude a narrow dilation of the 23 authored river controls from every vegetation
placement field. This is a renderer clearance, not a second hydrology model: it keeps
the visible wet material and banks legible through vanilla-density canopy while the
indexed river raster remains authoritative for topology.

Keep the installed 16384×8192 canvas and 12,104-location target. The current map already
uses the full vanilla raster contract; perceived scale and quality must be solved through
physical detail, coherent terrain layers, and close-view density rather than inventing a
larger unsupported canvas.

## 2026-07-30 — Parser-safe natural major rivers

Supersede the constant-width straight engine raster without reopening the rejected custom
affluent topology. Keep exactly 12 independent major channels, but densify the
hand-authored axes with the same deterministic natural-path phase used by the terrain
material. Statically prove that each result is four-connected, has no duplicate or
self-touching pixel, never touches another independent channel, and terminates against
palette-index-254 water. Any failure aborts generation before EU5 can parse the raster.

Follow the installed downstream width grammar rather than assigning one width per river:
index 4 at sources, then 5 and 11 downstream, with index 15 reserved for the final Anduin
reach. Extend the Anduin, Ringló, Gilrain, Poros, and Harnen through their coastal plains
to the current authored coast, just as the proven Baranduin override already does.
Tributaries remain physical valley/material controls until a genuinely editor-proven
affluent contract exists.

## 2026-07-30 — Entire covered extent is north of the equator

Place `equator_y` beyond the 8192-pixel southern map edge. The covered north-western
Middle-earth extent runs from Forochel to northern Far Harad and contains no southern-
hemisphere land. The previous value 4600 crossed Rohan: Fangorn at canvas y=4984
consequently received full southern winter on 4 August while Mirkwood remained green.
Encode this as a generator invariant rather than compensating with weaker climates,
because `continental = { winter = normal }` is an installed gameplay contract and
temperate Middle-earth should retain real northern seasons.

## 2026-07-30 — Named woodland coverage is a generated-content invariant

Do not accept the global vanilla-density transform count as sufficient vegetation proof.
It could remain numerically green while a control change redistributed trees away from a
binding forest. The map-object validator therefore requires at least 50,000 high-detail
transforms inside Fangorn, 50,000 inside the Old Forest, 25,000 inside Lórien, and 50,000
inside Ithilien. The current exact tree is comfortably above every floor; the thresholds
protect theatre coverage without freezing each forest's precise future boundary.

## 2026-07-30 — Vanilla-count topology and altitude-correct mountain material

Supersede the 12,104-location target with the installed world's exact 28,490-location
count on the same proven 16384×8192 canvas: 22,000 passable land, 6,000 impassable
mountain, 90 lake, and 400 sea locations. The rejected close probe occupied 497 control
pixels; the refined mountain distribution has a 37-pixel median. Count parity is a
granularity control, not visual acceptance, and M2 remains red until the real renderer
passes all required theatres.

Keep the complete full-precision (`height_quantum = 1`) Arda cache despite its large
derived binary, using Git LFS only for `heightmap.bin`. Visible mountain terraces are a
more serious production defect than repository convenience, and installed-game evidence
has already proved that the retail renderer consumes this payload.

Treat installed `mountain_wasteland` material-array order as binding: slot 10 snow,
slot 11 base rock, slot 12 dark dirt transition. Paint by continuous physical height and
organic noise, reserving dirt for low shoulders, rock for the body, and snow for the
highest crests. Never infer altitude semantics from generic slot order.

Occupied operational landmarks override broad wilderness masks before realm allocation.
Henneth Annûn and Cair Andros remain Gondorian; Derndingle belongs to Fangorn; Cirith
Ungol, Durthang, Narchost, and Carchost belong to Mordor. This prevents canonically active
forts/refuges from receiving ownerless town setup after topology regeneration.

## 2026-07-30 — q64 runtime height cache after native-density q1 load failure

Supersede only the earlier decision to ship the q1 *derived cache*. Preserve the exact
28,490-location topology and the complete 65,536×32,768 authored height source, but
serialize the runtime height tiles at q64. The corrected interactive-window observer
showed both full-visual and lightweight q1 sessions exiting at the retail 98% load
boundary after setup/cache completion; repeating the 700 MB payload is therefore an
exhausted route on the target machine.

q64 is 0.098% of the unsigned 16-bit engine range, eight times finer than the q512 cache
already proven in the live renderer. Generator v19 yields 120,118 unique height tiles in
172,161,411 bytes while retaining all 174,763 virtual entries. Continue tracking the
height payload through Git LFS. This memory-envelope decision does not waive visual
acceptance: if q64 produces perceptible terraces in the exact target/theatre captures,
reject it and pursue a different cache mechanism rather than silently accepting them.

## 2026-07-31 — Half-vanilla topology and reference-led cartographic reauthoring

Supersede installed-location-count parity after two independently bounded q64 lightweight
launches reproduced the same 98% hang and 14–23.5 GB working-set oscillation. The owner
explicitly authorizes approximately 50% fewer locations because the represented Middle-
earth extent is smaller than vanilla Earth. Target exactly 14,245 locations—half the
installed 28,490—while keeping the native engine canvas, the 65,536×32,768 authored
height source, q64 cache precision, vegetation density, rivers, materials, and physical
detail. Spend a disproportionate share of cells on narrow mountain systems rather than
using count parity as a proxy for quality.

Treat the owner-approved Arda Maps Third Age map and ArdaCraft interactive map as primary
cartographic references alongside Tolkien's published map evidence. Use them heavily for
relative position, coastline, hydrology, mountain, woodland, lake, road, settlement, and
regional-boundary checks. Downloaded vectors, tiles, and images are transient development
references under `G:\endore_runtime` and never enter the repository. Commit only original
ENDÓRË controls, a provenance/crosswalk ledger, and measured conformance results. This
amends the earlier no-tracing caution only to the extent necessary for the owner's
near-perfect positional-fidelity requirement; it does not authorize redistributing a
source map or its raw data.

## 2026-07-31 — Equal-scale projection and split Anduin engine channels

Preserve the ArdaCraft grid's physical scale with
`x = 0.5 + (world_x - 10651.5) / 86014` and
`y = (world_z + 10240) / 43007`. The unused width of EU5's 2:1 canvas is honest ocean
and eastern margin, not permission to stretch Middle-earth. ArdaCraft point markers take
precedence for named sites; Arda Maps linework takes precedence for continuous coast,
river, forest, lake, and mountain geometry. The permanent audit must cover all 42
settlement anchors, require cartographic provenance on all 62 additional landmarks, and
keep all 38 realm-seat coordinates identical to their capital controls.

Represent the Anduin as separate upper and lower engine channels divided by Nen Hithoel.
The physical controls still show one continuous source-aligned river system, but EU5's
independent-channel parser cannot serialize a river that leaves land for a large internal
lake and later re-enters land. Select the main source stem rather than every mapped
distributary, erase only sub-pixel raster backtracks, and retain exact source axes.
Carnen joins Celduin, Poros joins the lower Anduin, and Morthond joins Ringló; these
tributaries remain height/material controls until the affluent parser contract is proven.

## 2026-07-31 — Preserve source-coast micro-water and open Gundabad's gate

Do not let generic component cleanup absorb even a one-pixel source-coast sea inlet.
The initial reduced-topology validation found two Lindon sea pixels assigned to a land
location at the 420-unit water datum. Sea micro-components now remain water, even when
they are smaller than a gameplay location; the fixed 180 sea seeds partition them
without changing the location target.

Gundabad is a playable fortress, not an impassable mountain location. Add a narrow
authored pass at the canonical stronghold coordinate so its land component reaches the
Anduin/northern road network. Preserve all 3,200 mountain locations and the surrounding
source mountain footprint; connectivity is solved by the gate, not by reducing the
range.

## 2026-07-31 — Return runtime tessellation to the proven 12,104-cell envelope

Supersede only the 14,245-location runtime allocation after paired smoke passed but both
full-visual and lightweight fresh-game routes remained noninteractive for the complete
600-second post-cache bound. Use the last live-proven aggregate of 12,104 locations:
9,200 passable land, 2,700 impassable mountain, 60 lake, and 144 sea. This is still more
than twice the master plan's original 4,500–6,000 land-location scale and preserves over
five times the mountain granularity of the rejected 520-cell proof.

Do not change the equal-scale projection, 1,251-vertex source coast, 15 lake outlines,
43 mountain footprints, 9 ridge axes, 10 pass controls, 24 river/valley controls, 21
biome zones, full-resolution physical source, 42 settlement anchors, 62 landmarks, or
38 realm seats for this reduction. Runtime political cells are not a substitute for
cartographic precision. The 12,104-cell tree must independently pass static validation,
paired smoke, fresh checkpoint creation, cold full-render resume, nine-theatre review,
and explicit owner acceptance.

## 2026-07-31 — Ratio-preserving vegetation residency budget

Supersede the decision to ship the installed world's exact 10,193,212 vegetation-transform
population. That set is valid and rendered densely in an earlier cold-resume proof, but
on the source-frame tree it makes every fresh-game checkpoint profile peak near 23.5 GB
and miss the bounded interactive transition. Reducing political locations from 14,245 to
12,104 did not change that behavior, so further cartographic granularity cuts are not
justified.

Scale every installed forest/woods/pine high/medium/low count to 40%, preserving all nine
family/LOD ratios and exact renderer-discovered filenames. The resulting 4,077,285
Arda-native transforms remain roughly ten times denser than the visibly sparse 420,000
proof. Preserve Hilbert spatial locality, river clearances, porous authored placement,
and explicit high-detail coverage floors for Fangorn, the Old Forest, Lórien, and
Ithilien. This is a bounded renderer candidate, not automatic visual acceptance; only
the nine-theatre close/regional review can decide whether density remains sufficient.

## 2026-07-31 — Rebalance impassable political cells before height degradation

Keep the 12,104-location aggregate and the 4,077,285-transform stratified vegetation
candidate, but supersede its 9,200 land / 2,700 mountain split with 10,700 land / 1,200
mountain. The smaller object set still reached roughly 22 GB and missed the same fresh
checkpoint bound. The last live 12,104 topology had 520 mountain locations, making the
2,700 impassable cells—not total location count—the strongest remaining structural
difference not already isolated.

This decision changes only political tessellation classification. Preserve all 43 source
mountain footprints, 9 ridge axes, 10 pass cuts, full-resolution height/material sources,
mountain topography thresholds, and physical massif relief. A 1,200-cell mountain budget
is still over twice the live baseline and averages substantial granularity across every
source range. Test it before moving the derived height cache from q64 toward a visibly
coarser quantum.

## 2026-07-31 — Smoke fingerprints hash runtime bytes, not Git state

Replace the v1 `HEAD + dirty paths` shortcut with a complete hash of the bytes EU5 can
actually read under the four game-visible roots. A successful smoke must remain valid
when identical bytes are staged, committed, and pushed; those operations do not change
the game. Conversely, any tracked, untracked, ignored, or LFS-smudged runtime byte under
those roots must affect the fingerprint.

The current tree hashes in about 1.7 seconds, far cheaper than a redundant paired game
launch. The permanent slot test creates a temporary G:-resident repository and proves
that a byte edit changes the fingerprint while staging and committing the identical
edited bytes do not.

## 2026-07-31 — Keep q64 after the 1,200-mountain runtime breakthrough

The 12,104-location, 10,700-land / 1,200-mountain topology reached fresh live Observer
under both the debug checkpoint profile and a cold non-debug full visual-map profile.
It also advanced through 3018.2.04 without a mod-caused diagnostic. The fresh-load
constraint was therefore structural enough to resolve through impassable political-cell
rebalancing; it does not justify degrading the physical height cache.

Keep the full-resolution authored source and q64 runtime height cache. Do not test q128,
q256, or q512 unless a future, materially different renderer failure proves q64 itself is
the limiting payload. Continue with physical terrain-mode selection and the nine-theatre
review. Runtime success does not green M2; only visible physical quality and explicit
owner acceptance can do that.

## 2026-07-31 — Recognize the live Observer HUD as a start transition

The fresh-game driver previously recognized only the centered red `Game is Paused`
banner. On the current debug path, the first Start click completed successfully and
rendered the fixed `You are currently in Observer Mode` HUD, but no red banner appeared
within the bounded wait. The driver then clicked a live game again and reported a false
failure.

Accept the stable top-left Observer HUD as an equivalent success signal, requiring both
its near-black panel field and its bright eye/text glyphs. The country-selection map and
white transition veil satisfy neither condition. A repeat debug checkpoint and a cold
non-debug visual-map launch both proved this route.

## 2026-07-31 — One continuous renderer biome across dry Middle-earth

Use a unique `me_arda_surface` climate solely as the highest-priority biome-selection
adapter for every land and impassable-mountain location. Its gameplay modifiers and
seasonality match the retained continental contract, while
`endore_dynamic_land_biome` assigns cache channels 10–15 to grass, earth, volcanic rock,
exposed rock, snow, and sand. Paint those channels from continuous height, moisture,
source-biome, coastline, river, and landmark fields. Do not use location-scoped climate,
vegetation, or topography transition bits for physical colour: fresh renderer evidence
shows that they expose generated Voronoi cells as ochre, green, or pale islands.

Keep Mordor, Rhûn, and Harad as broad source-aligned environmental envelopes, but feather
their weights with organic deterministic fields. Their macro borders follow the audited
cartographic sources; the renderer transition must never be a ruler-straight mask or a
hard gameplay-location boundary.

## 2026-07-31 — Mountain polygons are foothill envelopes, not summit plates

Interpret all 43 Arda Maps mountain polygons as the outer physical footprint of their
ranges. They contribute low, irregular foothill mass. The nine source-aligned axes,
branches, deterministic folds, and landmark relief carry the high crests. Authored pass
coordinates lower those crests into high saddles rather than cutting circular lowland
holes.

This supersedes the nearly full-strength polygon lift that made the retail renderer show
flat grey mesas. It changes only vertical interpretation: source polygon borders, ridge
axes, named passes, political impassability, and the equal-scale projection remain
unchanged. The candidate must still pass fresh non-debug close views at Khazad-dûm,
Dunharrow, Goblin-town, and Orodruin before M2 can advance.

## 2026-07-31 — Pin named summits and make exposed material slope-aware

Retain 18 exact hash-pinned Arda Maps `point_mount` controls as named relief constraints:
Weathertop, Methedras, Celebdil, Fanuidhol, Caradhras, Mindolluin, Erech, Thrihyrne,
Dol Baran, Irensaga, Dwimorberg, Starkhorn, Ras Morthil, Carrock, Gundabad, the Lonely
Mountain, Ravenhill, and Amon Hen. Mount Doom remains its separate cratered landmark.
Retain all 10 passes as narrow source or reconciled saddles rather than broad circular
cuts.

Paint generic highland earth by altitude, but require measured local physical slope for
dark rock, exposed rock, and snow. The old height-only material bands visually expanded
high shoulders into flat grey and white slabs even after the height polygons became low
foothill envelopes. Fresh Observer evidence proves the new route exposes the actual
ridge geometry. It does not accept the current hard threshold edges: source-ridge-aligned
feathering remains required before M2 can pass.

## 2026-07-31 — Preserve equal scale; the vertical extent forbids enlargement

Keep the ArdaCraft equal-scale projection unchanged. At 4096×2048 control resolution,
physical land occupies 46.46% of the canvas; its bounding box spans 70.29% of canvas
width and exactly 100% of canvas height. The source land has 1,846 pixels touching the
north edge and 1,672 touching the south edge. A uniform enlargement cannot improve
close scale without clipping the owner-required Forochel-to-Far-Harad extent, while an
x-only stretch would falsify relative distances and shapes.

Do not trade cartographic fidelity for canvas occupancy. Keep the honest western ocean
and eastern margin. Improve close detail through source geometry, height/material
precision, and later political tessellation within the runtime envelope.

## 2026-07-31 — Rejected experiment: sub-location Shire material ponds

Retain the exact Arda Maps polygons for `minor_lake_10`, `minor_lake_11`, and
`minor_lake_12`, but exclude only those three from the physical-water land cut. They
cover 11, 6, and 26 control pixels and are substantially smaller than one runtime
location. Their lake-biome masks now sit on the surrounding dry datum and select wet
pond plus feathered water-transition material. Every larger lake, including Long Lake,
Mirrormere, Lake Evendim, Nen Hithoel, Núrnen, and the Sea of Rhûn, remains real engine
water.

This was the materially different route required after template substitution and a
near-water bed both left the cell-shaped quarry. It preserved source existence, outline,
and placement while refusing an engine topology that cannot represent the feature at
the current political scale.

Runtime decision: reject this implementation. Two fresh New Games completed cache/setup
work and then remained noninteractive for the full post-cache bound. Remove generator
v27 and restore v25 engine-water semantics without weakening the exact source geometry
or the audit. A later attempt must use a materially different runtime representation.

## 2026-07-31 — Belfalas source geometry outranks an unaudited visual redraw

Do not redraw the apparent inlet near Dol Amroth from visual intuition. The production
coast is the hash-pinned Arda Maps mainland ring; its Belfalas window contains 2,043 raw
source vertices, and the committed simplification tolerance is 0.00018 normalized units
(about three pixels on the 16384-wide location raster). Dol Amroth itself remains pinned
to the ArdaCraft equal-scale anchor.

The close-view defect is therefore shoreline/material/location presentation unless a
second binding source demonstrates a specific geometric contradiction. Preserve the
source coast and repair the renderer layer rather than making the map less faithful.

## 2026-07-31 — Recover the unnamed Arda Maps Harnen and Morgulduin channels

Replace the former eight-point manual Harnen diagonal with the hash-pinned Arda Maps
`line_river` geometry 8. It is the only substantial unnamed channel in the Harnen
corridor and provides 216 raw source vertices from the Harad-facing uplands toward the
canonical western drainage. Retain 49 meaningful bends after the same bounded
simplification used by named rivers, then add only two reconciled points to enter the
source coastline.

The earlier manually chosen mouth at x=0.445/y=0.880 is rejected: native land/water
analysis proves that continuing there crosses the sea and can re-enter land. The
corrected x=0.516/y=0.858 mouth stays on land until its final eight parser pixels enter
open water. The strict river writer accepts the resulting 51-point control with no
self-touch, land re-entry, or palette error.

Likewise replace the four-point manual Morgulduin with unnamed `line_river` geometry 14.
Its 40 raw vertices occupy the exact Morgul Vale-to-Anduin corridor and retain six
meaningful bends after bounded simplification. The source endpoints match the prior
canonical reconciliation, but the intervening course now comes from the same
hash-verified payload as every other production river.

## 2026-07-31 — Register the dynamic terrain biome in EU5's city-material database

EU5 resolves terrain surface materials and city-ground road/decal materials through
separate registries. Defining `endore_dynamic_land_biome` only in
`gfx/terrain2/materials.txt` therefore leaves the renderer with no city material during
the map transition. Add the same key under `gfx/city_materials` and inherit the installed
`default_biome` road/decal stack. This is an installed-contract repair, not bespoke art:
it introduces no texture and preserves the vanilla style/format until the physical map
gate is accepted.
