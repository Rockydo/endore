# Assumptions

No lore assumptions were made in M1. The proof realm, installed location identities, and
all Earth-named compatibility keys are temporary engineering scaffolds rather than claims
about Middle-earth.

## M2 map controls

- † The exact 8192×4096 normalized coordinates of coastlines, ridges, rivers, lakes, and
  all 41 settlement anchors are gameplay extrapolations from relative placement in the
  cited chapters and the books' schematic map. They preserve canonical ordering and major
  travel corridors but do not claim survey accuracy.
- † The production extent clips deep Rhûn and deep Harad at the eastern and southern
  borders while retaining western Rhûn and a northern Far Harad fringe, providing useful
  playable margins where canon is sparse.
- † Rohan is grouped under Rhovanion for strategic map hierarchy, while Gondor forms its
  own top-level geography. This is a UI and gameplay classification, not an in-world claim.
- † The 41 canon anchors retain their cited names, but all generated fill locations use
  deterministic engineering keys and generic display names. M3 replaces those names with
  a curated gazetteer before any realm is considered first-class.
- † Terrain relief and the flat-map texture are generator-v1 representations intended to
  prove navigability, barriers, and map readability. Their authored ridge/pass alignment
  is binding for gameplay, but their surface detail is not final visual art.
- † Passable locations temporarily use installed culture, religion, and raw-material
  defaults solely because the setup validator requires populated fields. They are not
  claims about the peoples, faiths, or economy of Middle-earth.

## M3 realms and gazetteer

- † Political borders are deterministic strategic extrapolations from the canon anchors,
  mountain barriers, river corridors, and the plan's realm roster. Sparse Forodwaith,
  Enedwaith, the Brown Lands, and emptied Ithilien retain deliberately wild land rather
  than being painted into the nearest realm.
- † The exact seats named The Angle, Halls of Ered Luin, Woodmen's Hall, Ghân's Glade,
  Forochel Camp, Harnenhold, Qarsad, Mûmak Gate, Khazân, Burh Gath, Wainhold, Eastern
  March, and Dunland Moot are gameplay seats invented where binding canon supplies no
  administrative capital. Each remains individually marked in the control ledger.
- † Harnendor, Qarsad of Harad, the western Kingdom of Rhûn, Karmach, and the Sagath
  March are on-map political extrapolations used to make the canon-sparse South and East
  playable without pretending to define all off-map Harad or Rhûn.
- † Generated fill names use documented regional phonotactic impressions and ordinary
  English compounds. They are deterministic Tolkien-register inventions, not claims to
  reconstruct Sindarin, Khuzdul, Black Speech, or any unattested Mannish language.
- † Realm colors and first-pass arms are readability scaffolds. The arms reuse generic
  installed heraldic components as permitted by the M3 gate; M11 replaces them through
  the reference-driven bespoke-art pipeline.

## M4 peoples, languages, and faiths

- Eriadoran is a deliberate gameplay umbrella for the remaining settled Middle Men of
  Eriador; it does not imply a single historical polity or self-identity.
- Karmachi and Sagath identities are documented inventions for canon-sparse eastern
  populations attached to the already logged gameplay realms.
- Constructed name components are Tolkien-register tools, not linguistic reconstructions
  of unattested Sindarin, Khuzdul, Black Speech, or Mannish forms.
- The spiritual “Ways” are gameplay adapters for outlook, allegiance, and custom. They do
  not imply organized churches, universal creeds, or modern religious institutions.
- Entish Memory of the First Music is a gameplay representation of the Ents' remembered
  place in creation, not an assertion of formal Entish worship.
- Firebeards and Broadbeams share one culture; Lake-folk are folded into Dalish culture;
  and Galadhrim remain distinct from other Silvan communities for playable regional
  identity.
- M4 assigns a dominant people and faith profile to each land location. It is not the
  final M5 census: minorities, depopulated ruins, settlement types, and exact population
  weights remain M5 work.

## M5 census and opening economy

- † The represented world begins with 9.029 million people. Gondor has 2.0 million,
  Rohan 0.5 million, the Shire 0.22 million, and Mordor 1.5 million including 0.35
  million Mannish thralls in Nurn; exact totals and social shares are gameplay estimates
  bounded by the master plan and the books' relative military and settlement evidence.
- † On-map Harad, Khand, and Rhûn collectively exceed Gondor in population without
  claiming to represent their much larger off-map peoples. Sparse wild non-ruin land has
  only 22 thousand inhabitants in total, while all 21 canonical ruins begin empty.
- † Twelve opening markets, 58 urban or fortified settlement seeds, regional development
  values, and raw-material placement extrapolate exchange corridors, terrain, and named
  centres into EU5's economic model. They are balance inputs rather than canonical
  administrative statistics.
- † Starting armies use one provisional installed foot-unit type and scale only by broad
  population bands. They establish a loadable M5 economy and do not pre-empt M7's
  canonical unit rosters or final military balance.

## Reopened M2 physical production

- â€  The control atlas now contains 42 stable anchors. Fields of Nurn represents the
  canon-described slave-worked farmlands by NÃºrnen; its exact coordinate and town rank
  are gameplay extrapolations. The anchor prevents Mordor's 350k Mannish field population
  from depending on an unstable generated location key.
- â€  Coast, lake, forest, ridge, valley, and tributary micro-geometry is deterministic
  cartographic interpretation beneath the cited macro ordering, not survey accuracy.
- â€  Umbarite remains Umbar's broad primary culture, while the surviving Black
  Númenórean houses are an accepted culture represented disproportionately among its
  nobles. This is a gameplay interpretation of Umbar's Númenórean lineage and later
  mixed population, not a canonical demographic statistic.

## Reopened M2 source-audited cartography

- † The old statement that all physical coordinates were broad gameplay
  extrapolations is superseded. Large- and medium-scale positions now follow
  the equal-scale ArdaCraft grid and Arda Maps continuous linework under
  `docs/world/CARTOGRAPHY_REFERENCE_LEDGER.md`.
- † Where the two community references differ locally, a point marker uses
  ArdaCraft while coast, river, forest, lake, and mountain linework uses Arda
  Maps. Tolkien's published evidence remains superior to either
  interpretation.
- † Khazad-dûm is placed between the source controls for the Doors of Durin
  and Dimrill Dale. Fields of Nurn uses the centre of the mapped Nurn area,
  Dorwinion uses its mapped area-label centre, and Pelennor lies immediately
  east of Minas Tirith; these are strategic anchor choices rather than claims
  of surveyed city coordinates.
- † The 2:1 EU5 canvas does not horizontally stretch the approximately
  1.1:1 represented source extent. Extra width is honest ocean and eastern
  margin, preserving relative distances and the recognizable proportions of
  Middle-earth.
- † Twelve of the 62 secondary landmark controls remain reconciled or
  gameplay judgments because binding canon does not provide surveyed points:
  the Angle, the composite surviving Blue Mountain halls, the Woodmen's seat,
  the Lossoth camp, three invented Harad seats, three invented Rhûnic seats,
  the Dunland moot, Mount Gram, and the paired Towers of the Teeth. Their
  exact coordinates and cartographic rationale are recorded row-by-row in
  `m3_landmarks.csv`; the Arda Maps/ArdaCraft references constrain the
  surrounding geography.
- † The three invented Rhûnic seats use the represented land around the source
  Rhûn and Sea of Rhûn labels, at x=0.77/0.80/0.82. The previous x=0.875
  Eastern March point was outside the source mainland and is rejected.
- † The Arda Maps Gundabad point is interpreted as the summit/stronghold, not
  the gameplay saddle. The usable gate/approach is represented by a separate
  narrow pass immediately north-east at `[0.506471, 0.097215]`; this preserves
  connectivity without lowering the canonical summit. Because the point lies
  at a junction already represented by two source ranges, its named-peak field
  is interpreted as a compact chain crown rather than a third range-sized
  envelope or an Erebor-style isolated mountain.
- † The Harlond below Minas Tirith is an operational Gondorian port on
  TA 3018.1.1. It remains owned even while most nearby Ithilien locations are
  deliberately wilderness; the wilderness mask cannot override its port rank.
- † Forochel Camp is an invented seasonal Lossoth seat, not a canonical capital. Its
  earlier x=0.340000/y=0.035000 control lay offshore and became unstable when political
  tessellation was reduced. The retained x=0.341880/y=0.065462 point is the nearest
  playable shore on the unchanged source-pinned Forochel coastline.
- † Arda Maps supplies named source polylines for 22 of the 24 production
  river controls. Its unnamed `line_river` geometry 8 is the only substantial
  channel in the Harnen corridor and is used for that river's detailed upper
  and middle course; only its short final reach to the coast is reconciled
  against the owner-approved macro map. Unnamed geometry 14 occupies the exact
  Morgulduin corridor and supplies that channel from the Morgul Vale to its
  Anduin confluence. These identifications are cartographic reconciliations,
  not claims that the source itself labels either river.
- † Mirrormere and minor lakes 04-07/10-14 are valid cartographic features but each
  occupies at most 64 pixels in the 4096x2048 source-control atlas, too small to justify
  an independent EU5 water location at the current release-safe political tessellation.
  Their exact source shapes are represented as wet surface material rather than
  navigable engine water; this is a scale conversion, not a claim that they are dry
  in-world. Long Lake, Lake Evendim, Nen Hithoel, Nurnen, and Rhun remain true water.
- † Arda Maps `poly_highland` footprints are interpreted as rolling upland and foothill
  envelopes, not as surveyed elevation contours or permission to create additional
  impassable mountain cells. Their exact horizontal shapes bind the v29 low-relief field;
  their 4,800-sample maximum lift is a renderer calibration.
- † Arda Maps `poly_moor` footprints are interpreted as wet or moorland surface controls.
  Geometry 0 binds the Dead Marshes and geometry 6 covers the broad Nindalf/Anduin-mouth
  wet ground; the remaining small footprints retain source keys until individual lore
  labels are established. This does not claim that every moor polygon is navigable water.
- † Canon and the two binding community maps define Mordor through its enclosing ranges
  and named internal features, not a surveyed ash-soil boundary. The v29 Gorgoroth field
  therefore interpolates inward from Arda Maps mountain polygons 8-11, the three enclosing
  ridge axes, and Mount Doom, then fades toward the open east. It is a renderer
  reconciliation and must not be reused as a political frontier.

## v30 source-relief and drainage interpretation

- † Detailed crest and branch placement now uses the Ardacraft Heightmap V2
  interpretation inside the audited Arda Maps outer mountain envelopes. This
  supersedes the earlier blanket assumption that all mountain linework came
  from Arda Maps. Exact named points still constrain canonical summits, and
  Tolkien's published evidence remains superior to either community source.
- † The committed Ardacraft relief field is an 8-bit native-resolution numeric
  measurement, not a reusable heightmap or copy of the reference artwork. Its
  losslessly compressed warm-rock response
  contains no colour, labels, water, terrain texture, or political information.
- † Arda Maps supplies named source polylines for 22 of the 24 parser-modelled
  river controls and 30 of the 76 additional terrain-only source parts. The 76
  additions are physical drainage controls, not 76 additional navigable EU5
  rivers: build 24187685 rejects custom affluent junction graphs, so they carve
  valleys and inform wet terrain while remaining absent from `rivers.png`.
- † Ardacraft's direct Erebor marker supersedes the displaced least-squares Arda
  point for Erebor's map anchor. The city/hold is represented
  at the mountain point because EU5 requires one location anchor; this does not
  claim that every Dale settlement or entrance occupied the summit itself.

## v35 pass and surface interpretation

- † The Arda Maps Paths of the Dead and Cirith Gorgor points identify route centres, not
  circular lowland basins. Their gameplay saddles may be anisotropic according to the
  surrounding source range structure while their coordinates remain exact.
- † A passable stronghold location on a physical massif does not imply that its summit is
  flat or low. Gundabad's location topology may use a narrow connection to the continental
  land component while the canonical point retains its accepted high chain-crown relief.
- † Earlier exposed-rock transitions on the White Mountains and Mordor's enclosing walls
  are renderer calibration, not a claim of uniform bare stone. They apply only where a
  reviewed named-range axis overlaps genuinely high physical terrain.

## v40 relief reconstruction

- † Ardacraft Heightmap V2's warm-rock colour identifies mountain placement and crest
  structure but is not itself literal elevation. Continuous 4/12/18-pixel convolutions
  of that exact numeric response are a renderer-scale height interpretation; they do not
  move a range or import the reference image.
- † The two Morannon hinge endpoints are the nearest unambiguous source-relief samples on
  Ered Lithui and Ephel Duath. Ardacraft's drawing layer confirms both arms meet at Cirith
  Gorgor, so restoring those short missing raster connections is preferable to leaving a
  lore-inaccurate open basin.
- † Small exact-coordinate teeth at strong Arda Maps peak points represent named summits
  where the calibrated point and painted Ardacraft crest differ by a few pixels. Their
  compact scale is not evidence for a separate massif or political boundary.

## v41 half-canvas vertical calibration

- † Installed vanilla gradient statistics are a useful lower reference but not a literal
  visual target for ENDORË's half-sized terrain canvas. The accepted static interval is an
  engine-scale interpretation: materially steeper than vanilla/v40, materially gentler
  than v39, with unchanged source coordinates.
- † A compact crown at Mount Gundabad's exact source junction represents the named peak's
  required prominence; it does not alter the surrounding Grey/Misty Mountain geometry or
  imply a separate massif.

## v42 summit-colour interpretation

- † Pale neutral pixels embedded in Ardacraft's warm mountain bodies represent the
  highest snow/stone summit spines rather than lowland light. The numeric reduction may
  decode them only when red, brightness, neutrality, and red/green-balance guards all
  agree; it remains a derived height signal, not copied source artwork.

## v43 renderer-scale arête interpretation

- † The >=0.92 band of the committed Ardacraft numeric response represents the true
  upper arête signal for EU5 height translation. Lower warm bands remain source-authored
  foothills and shoulders, but may be vertically compressed because the reference's
  painted colour width is not literal terrain width.
- † Ardacraft's painted Erebor spot and its direct Erebor marker describe one physical
  Lonely Mountain. Collapsing their few-sample overlap into one marker-centred summit is
  a de-duplication of the same source feature, not an invented relocation.
- † Raising only already-high source samples within the Morannon theatre represents
  renderer-scale vertical exaggeration of Ered Lithui and Ephel Dúath. The exact source
  shape and low Cirith Gorgor saddle remain authoritative.

## v44 range serration

- † Source-pinned mountain placement and renderer-scale summit variation are separate
  concerns. Deterministic fold/peak variation may alter local altitude inside an existing
  audited massif to make a long range physically readable, but it may not widen, move,
  connect, or invent a range or close a named pass.

## v45 installed-renderer calibration

- † A visually convincing EU5 mountain is governed by the rendered relationship among
  physical width, height contrast, crest frequency, camera scale, and material exposure;
  raw height-gradient percentiles alone are not a sufficient proxy. Matched captures of
  installed vanilla ranges may therefore define renderer-scale ratios for ENDÓRË while
  Arda Maps and Ardacraft continue to define every horizontal placement and footprint.

## v46 renderer-frequency interpretation

- The installed q64 terrain renderer cannot be assumed to preserve arbitrary native-
  sample signed detail even when its gradients pass static bounds. Repeated regular bands
  in a fresh live frame are authoritative rejection evidence; a usable arÃªte signal must
  vary smoothly over several cache samples and remain tied to the source range axis.
- Exposed-material fraction is not sufficient evidence of convincing mountain surface.
  Material must also be spatially connected to the physical crest/flank, feathered rather
  than blocky, and bounded against theatre-scale caps. Live connectivity/regularity checks
  may therefore supersede a numerically passing fraction window without changing any lore
  geometry.

## Canonical forest species and renderer density

- † Owner direction treats TA 3018 Lothlórien as birch-dominant for map presentation.
  Installed EU5 has no dedicated birch generated-object family. Its two full-canopy
  `environment_oceanic_wt_tree` meshes use light wood and are therefore the closest
  vanilla-format approximation. Reserving them for Lothlórien is a visual species proxy,
  not a claim that every tree in the Golden Wood was botanically identical.
- † Transform density and LOD continuity are renderer-scale interpretations of a source
  woodland polygon, not cartographic evidence for a larger forest. Mirkwood and
  Lothlórien keep their exact hash-pinned source boundaries while receiving more and
  better-distributed physical trees inside those boundaries.

## TA 3018 political-boundary interpretation

- † Tolkien and the two accepted cartographic references identify named lands, seats,
  forests, rivers, mountain walls, and spheres of control, but do not provide a complete
  cadastral border for every 6,004-location cell. For well-attested western and northern
  realms, equal-scale claim envelopes therefore follow those named physical limits and
  are recorded per location in `m3_ownership_audit.csv`; the envelopes may constrain the
  allocator but may never move terrain to make the political paint fit.
- † Impassable mountain locations and water can divide the location-adjacency graph of a
  canonically coherent realm. Such components are retained only when the generated audit
  exposes them for review (for example Lindon's separated coasts or Mordor's occupied
  gates). Compact realms including Lothlórien, Dunland, Woodmen, Woodland Realm, Dol
  Guldur, Iron Hills, Erebor, Fangorn, and Isengard are required to remain contiguous.
- † Rhûn, Khand, and Far Harad are much less precisely bounded in the accepted sources.
  They remain explicitly lower-confidence region claims with a hard anti-sprawl distance
  instead of receiving invented precise borders. The roster may gain a smaller realm only
  where TA 3018 evidence supports distinct control; unclaimed or depopulated land is
  preferable to decorative fragmentation.
- † Ithilien is depopulated contested country on TA 3018.1.1, not ordinary Mordor
  heartland. Its non-anchor locations therefore remain `wild_ithilien`; the occupied
  refuges, crossings, towers, and gateworks at Henneth Annûn, Cair Andros, Cirith Ungol,
  Durthang, Narchost, and Carchost stay explicitly pinned to their attested controllers.

## Source-drainage hierarchy interpretation

- † Arda Maps' `line_river` storage order is not a reliable flow-direction claim for
  every minor part. A terrain-only channel may therefore use nearly uniform wet-bank
  material width while retaining its exact path; this avoids depicting a tributary as
  widening toward its headwaters. Independently indexed major rivers keep EU5's proven
  downstream 4→5→11→15 palette progression.
- † Lhûn's three source parts encode a Y-shaped system: parts 1 and 0 form the northern
  main stem and part 2 is the southern branch. Preserving that physical Y is more faithful
  than inventing an independent coastward parser channel. Sirith likewise remains a
  physical receiving-channel control until the installed engine accepts a source-faithful
  junction graph. Neither choice means the watercourse is absent from the terrain.
- † A sub-control-pixel endpoint extension for Lefnui or Serni is a raster contact
  correction at the already authored coastline, not new cartographic linework. Longer
  manually drawn extensions are forbidden.

## v74 forest-edge and political-overlap interpretation

- Caras Galadhon lies near Lothlorien's eastern edge and the Anduin/Celebrant approach.
  A visibly more open riverward margin around its locator is therefore not evidence that
  the whole Golden Wood is sparse. Acceptance requires separate interior regional/close
  evidence, a dense all-LOD source-zone census, and light-trunk-only species checks.
- Generated political locations are larger than many source-forest details. A location
  may therefore qualify when at least 16 control pixels overlap a small, softly contacted
  source mask even if its seed/label centre lies outside the polygon. This is a whole-cell
  raster assignment tolerance, not authorization to enlarge the physical woodland.
- `me_anduin_vale_region` is a technical setup partition that cuts across southern
  Mirkwood. Including that region in Dol Guldur's candidate roster asserts no claim west
  of the forest: the independent Mirkwood source-overlap mask and southern bounds remain
  mandatory and prevent political spill.

## v75 climate-renderer interpretation

- Forodwaith and Forochel are open cold country at TA 3018, not continuous northern
  conifer forest. Sparse installed arctic-tree pockets are a renderer approximation for
  stunted vegetation; their bounded count does not assert a woodland boundary.
- The accepted cartographic sources define Harad's broad arid envelope and source-backed
  uplands but not a cadastral distribution of individual sand and stone textures. No new
  texture distribution is accepted: both v44 and v45 live calibrations were rejected and
  the proven v43 cache was restored. A future presentation pass may reveal source
  highlands but may not change the climate outline, coast, rivers, or elevation.
