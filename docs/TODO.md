# TODO

1. REOPENED M2 remains the sole content priority. Follow
   `docs/m2/VISUAL_REOPEN_GATE.md`; do not resume gameplay work until the physical map
   receives explicit owner acceptance. The current source-audited runtime tree loads,
   but the nine-theatre visual gate remains red.
2. REOPENED M2 MOUNTAINS — current relief remains too broad, low, rounded, and plateaued.
   Retain source-pinned axes/peaks/saddles and separate impassability, but rebuild the
   cross-range profile for substantially taller, narrower, jagged crests with secondary
   ridges and irregular peak chains rather than flat-topped high hills. Audit Mordor's
   Ered Lithui/Ephel Dúath/Mountains of Shadow structure and every northern range directly
   against `arda-maps.org/ages/third` and Ardacraft before accepting a vertex or axis.
   Erebor must read unmistakably as one isolated Lonely Mountain, not part of a broad
   upland or range. Verify all named passes at close 3D zoom without opening them.
   The first v30 source-field profile was live-rejected because exponent 0.82 widened its
   correct branches into broad high hills. v31 used exponent 1.38 and loaded/ticked cleanly,
   but like-for-like live Gundabad, Erebor, Morannon, Orodruin, and Dunharrow views rejected
   it too: Orodruin read correctly, while the long ranges retained amplified mid-level
   shoulders; Gundabad's saddle suppressed its summit; and Erebor's city camera was offset
   from the exact peak. v32 contracts source relief at exponent 1.90, uses a convex final
   cross-range profile, reduces polygon foothill lift, moves the Gundabad saddle off the
   summit, and aligns Erebor to the exact Arda Maps point. Offline and full validation are
   green with zero clipped samples. v32 then passed paired smoke with zero
   mod-attributable lines and entered fresh live Observer in 116 seconds. Its first
   correctly framed Gundabad view still rejected the generic range-sized summit stamp as
   a mesa-like cap; later Morannon/Dunharrow captures inherited cumulative maximum zoom
   and are not valid placement evidence. v33 kept the source ranges unchanged, gave
   Gundabad a compact 0.0045 chain-crown profile, passed paired smoke with zero
   mod-attributable lines, and entered a fresh Observer in 126.3 seconds. Hard-reset
   regional views accepted Gundabad, isolated Erebor, and Orodruin as components but
   rejected the low, green Ered Lithui/Ephel Duath around Morannon and the White Mountains
   near Dunharrow. v34 replaces the blanket 18% residual continuity with exact reviewed
   per-range weights and narrower body/spine kernels. Its complete regeneration, full
   validation, exact-fingerprint paired smoke, and fresh 126.4-second Observer load are
   green. Hard-reset views retain Gundabad, isolated Erebor, and Orodruin as accepted
   components but reject v34 at Morannon and Dunharrow: both still render as low green
   relief. v35 keeps every source coordinate fixed, replaces the round Paths of the
   Dead/Morannon depressions with source-oriented anisotropic saddles, lifts only the
   exact Ardacraft crest response by 1.28, and gives the White Mountains/Mordor walls a
   range-scoped severe-rock material transition. Independent contracts now require low
   route floors plus high, exposed adjacent flanks. The pinned-toolchain 6,004-location
   world regenerated in 637.0 seconds on model `8d31aa47`; full validation passed in
   337.5 seconds and paired smoke passed on exact fingerprint `7b1e0917`. A fresh
   124-second Observer and valid reset captures nevertheless reject v35: Erebor/Orodruin
   remain strong, but Morannon and Dunharrow still show broad green uplands with only
   scattered high edge patches. v36 multiplies stronger continuity by a soft dilation of
   the exact Ardacraft support field, only for White Mountains/Ephel Duath/Ered Lithui/
   southern Mountains of Shadow. Offline source support improves rather than regresses;
   the 6,004-location model `e03c16e1` regenerated in 662.5 seconds and full validation
   passed in 334.3 seconds on fingerprint `a9de05d5`. Corrected exact-fingerprint smoke
   and a fresh Observer load are green, but valid independently reset views reject v36:
   its height source is still only 640×513/4-bit and its broad axis/material bodies still
   present grey slabs or green uplands around Gundabad, Morannon, and Dunharrow.
   v37 doubles the numeric source field to 1280×1026/5-bit, removes pre-ceiling clipping,
   concentrates source-supported axes into narrow spines, adds compact oriented pass
   flanks, and replaces unbounded high-area/material floors with bounded anti-plateau
   contracts. Mordor's ash material now follows its source-enclosing ranges: the basin is
   dark basalt and exposed grey rock is reserved for steep high crests, not a synthetic
   oval/slab. The coherent 6,004-location model `14a84668` has 284 ports, height maximum
   63,983, terrain-cache generator v33, and full validation green in 367.2 seconds on
   exact fingerprint `97e271fb`. Paired smoke and a corrected one-click fresh Observer
   load are green, but valid reset views reject v37: synthetic axes/flank stamps still
   broaden Gundabad and flatten the Mordor/White Mountains presentation; Orodruin is a
   mesa. v38 removes every redundant synthetic range axis, pass-flank stamp, and source-
   backed named-peak lobe so the 1280×1026 Ardacraft relief owns exact branches directly.
   It moves Erebor to Ardacraft's direct mountain marker, aligns the Morannon pass with
   its direct fortification marker, adds only compact source-gap summits at Mindolluin and
   Irensaga, uses a 68,000-unit cubic upper-arête response, and shrinks Orodruin to a
   compact 63k cone. Mordor's ash biome now flood-fills its exact U-shaped source mountain
   enclosure instead of a rounded proximity blob. Model `fefa695d` has 292 ports and a
   199.9 MB self-contained cache.
   Full validation is green in 385.8 seconds. Exact smoke is deferred—not failed—while
   Antiquitas owns the shared EU5 session; keep this item open pending that smoke and the
   same five live pairs. That deferred work later completed: final validation, exact
   zero-new-line paired smoke, and a fresh Observer load all passed, but the five reset
   pairs visually reject v38 because its quantized/saturated relief still forms mesas.
   v39 retains Ardacraft relief at native 2500x2003/8-bit
   precision, removes both saturation paths, limits 45k+ terrain to 39,672 samples, and
   rejects more than 10% low-gradient summit-cap coverage. Compact final-resolution
   canonical summits put Erebor, Gundabad, Dunharrow, and Orodruin at 60-61k; the exact
   Morannon source arms reach 50.9k while the gate floor remains 12.7k. Model `9f022ce3`
   retains 6,004 locations, has 298 ports, 235 authored route edges, 2,038,645 vegetation
   transforms, and a 171.7 MB self-contained cache. Full validation, exact paired smoke,
   and a fresh Observer load are all green. The five live pairs nevertheless reject it:
   Gundabad and Erebor retain smooth crowns; Morannon does not visually form the exact
   Ered Lithui/Ephel Duath hinge; Orodruin splits into several lobes; and Dunharrow's
   surrounding White Mountains remain discontinuous cliff blocks. v40 preserved every
   source coordinate and replaced raw colour shelves with a
   4/12/18-pixel continuous source reconstruction, calibrates gradient bounds to installed
   vanilla terrain, removes range-sized named-peak stamps, and binds a narrow two-wall
   Morannon hinge confirmed by Ardacraft's drawing layer. Model `7f48ab78` retains 6,004
   locations with 282 ports, 225 route edges, 2,038,645 vegetation transforms, and a
   180.1 MB self-contained cache. Full validation, exact paired smoke, and two fresh
   Observer starts passed, but exact-target live views rejected it: Erebor was a broad
   stump/weak hill, Gundabad a green basin ringed by flat rock carpet, and Morannon a low
   grassy V. v41 is the current candidate. Its source reconstruction is tightened to
   3/8/15 pixels, upper relief occupies an intermediate 720/1,270/1,895 median/p75/p90
   gradient band above 45k, named summits are narrower, and the Morannon hinge is taller
   without moving its saddle. Model `35fc4a7c` retains 6,004 locations, 292 ports, 232
   route edges, 2,038,645 vegetation transforms, and a 172.3 MB cache. Full validation,
   exact smoke, and correctly targeted fresh live views then rejected v41: Erebor and
   Orodruin improved, but Gundabad remained a green basin in rock carpet, Morannon kept a
   broad wall plus straight synthetic arm, and Dunharrow became two isolated spikes.
   v42 decoded Ardacraft's pale snow/summit spine in
   addition to warm shoulders, removes synthetic Morannon lines, and suppresses ordinary
   named-point teeth so the source raster owns continuous chains. Static source, height,
   and material preflights pass. Model `987245ab` regenerated with 6,004 locations, 293
   ports, 242 route edges, 2,038,645 vegetation transforms, and a 173.8 MB cache. Full
   validation and exact smoke passed, but a fresh exact-target review rejected broad rock
   carpet at Gundabad, twin oversized Erebor mounds, a low Morannon berm, an over-broad
   Orodruin, and smooth White Mountains around Dunharrow. v43 is the current offline
   candidate. It retains only the true top-8% source arête response at full height,
   collapses Erebor's duplicate raster/marker bodies into one compact direct-marker cone,
   gives Gundabad a narrow exposed crown, shrinks Orodruin, and raises only existing
   source relief around Morannon while keeping the exact gate low. Model `16e5d549` has
   6,004 locations, 300 ports, 239 route edges, 2,038,645 vegetation transforms, and a
   168.8 MB cache. Full validation and exact smoke passed. Fresh views accept its single
   Erebor and compact Orodruin improvements but reject the long ranges: Gundabad remains
   broad, Morannon's northern/eastern wall remains low, and Dunharrow remains smooth.
   v44 added stronger final-resolution folds and sparse summits only inside v43's exact
   mountain-strength envelope. Its complete regeneration, validation, smoke, and fresh
   Observer were green, but live views rejected it. Matched installed-vanilla Chur/Shey/
   Kathmandu captures and native morphology measurements then informed v45. v45 reduced
   Gundabad's upper-quarter footprint from 20.2% to 8.2%, regenerated coherently, passed
   full validation and exact paired smoke (`3d769297`), and entered a genuinely fresh
   Observer. Reject it visually: its native-frequency field becomes regular terraces at
   Dunharrow, widened material thresholds create blocky rock patches and a huge pale
   Gundabad cap, and Morannon's enclosing walls remain unreadable despite the low saddle
   being correct. For v46 remove the v45 high-frequency field and broad threshold changes;
   keep the accepted Gundabad footprint contraction, Erebor/Orodruin guards, exact source
   geometry, and low passes. Build smooth continuous range-scale arÃªtes and source-backed
   wall-specific material masks whose transitions are feathered at renderer scale. Add
   live-derived gates that reject regular bands, cap area, and disconnected rock blocks.
   Do not advance to rivers or politics until the five exact views pass honestly.
3. REOPENED M2 INLAND WATER — retain the scale-enforced material-pond representation for
   all ten source lakes occupying at most 64 pixels in the 4096x2048 control atlas
   (189 pixels total). Mirrormere and minor lakes 04-07/10-14 remain exact lake-biome
   polygons over continuous physical land; the five larger lakes remain engine water.
   Fresh Mirrormere evidence proves the deep rectangular quarry is gone. v29 adds shallow
   feathered physical bowls and a wetland/water-transition stack. Verify and refine the
   close-zoom water/scenery read without
   restoring engine-water host cells or changing any source outline.
   ACCEPTED v84 TERRAIN-WATER CHECKPOINT — the master-plan ban on new 3D meshes rules out a
   custom-polygon carrier. Instead, reserve the existing wetland-coast material channel
   for a deterministic muted blue-green still-water surface derived from the exact
   hash-pinned vanilla `dirt_ponds_01` diffuse, with vanilla's flatter unmasked normal and
   glossy properties. The exact 189-pixel source cores now use only that channel; their
   feathered margins, shallow above-water bowls, all source outlines, and every
   engine-water lake remain unchanged. Material generation/checks, cache regeneration,
   `pdxlint`, and a pre-precedence full `gmake validate` are green. Generator v48 restores
   pond precedence after the river pass at 115 intersecting high-resolution samples;
   targeted checks pass. The first live colour/relief probe was honestly rejected as a
   mottled crater. A fresh exact-camera A/B then accepted the cooler surface: the Nindalf
   cluster reads as level blue water with its authored irregular islands, while calibrated
   Mirrormere/Shire views show no tile, rectangle, hard rim, or spill. A 45-second maximum-
   speed Observer run required zero recovery and retained the 1,486-byte baseline. The
   first full gate correctly rejected stale cache provenance after the live colour change;
   coherent regeneration kept the material payload hashes unchanged and updated its source
   manifest. Paired smoke then passed in 201.0 seconds with zero mod-unique lines on exact
   game-visible fingerprint `9fff7077`; commit remains conditioned on repository-wide
   static green. Keep this item open: small-lake presentation is improved, not the complete
   nine-theatre M2 terrain gate.
4. REOPENED M2 BELFALAS — preserve the hash-pinned Arda Maps mainland ring: the apparent
   inlet is backed by 2,043 raw Belfalas-window source vertices and the committed
   simplification deviates by at most roughly three location-raster pixels. Treat the
   remaining defect as shoreline/material/location presentation, not permission to
   invent a different bay. Verify regional and maximum-close zoom after the pond probe.
5. REOPENED M2 MACRO BIOMES — Mordor's fifteen-point ash oval is rejected and replaced
   by a source-range/axis/Mount Doom field. Replace the remaining Brown Lands blob and
   broad Rhûn/Harad proof-era envelopes with audited source-native or explicitly logged
   continuous controls; never reintroduce an oval or straight clipped climate edge.
   ACCEPTED FOCUSED v77 SCENERY CHECKPOINT — a source-clipped 36,000-transform retail
   rock layer adds sparse close-zoom stone across only climate biomes 8/9/10. Repeated
   Qarsad/Umbar A/Bs reject and quarantine the palm and grass-test families: the latter
   creates a generic green rosette carpet, while the former adds no distinct readable
   value. Validation removes and rejects every stale palm/grass bin. Full validation and
   exact-fingerprint paired zero-new-line smoke are green. This does not close the still-
   open macro-material/source-envelope audit.
   CURRENT v79 SOURCE-BIOME CANDIDATE — the proof-era Brown Lands, Rhûn, and Harad
   polygons have been replaced by a hash-pinned reduction of Ardacraft's 197-feature
   biome atlas: one detailed Brown Lands component, 41 Rhûn steppe components, 37 Near
   Harad scrub/woodland components, and seven Far Harad arid components. Explicit organic
   continuations exist only where Rhûn and Harad meet the authored east/south crop edges;
   Mordor ash remains last and cannot be overwritten. Static source, control, terrain-
   cache, and complete 6,004-location regeneration are green. Keep this item open until
   fresh real-renderer Rhûn/Brown Lands/Harad views and the complete nine-theatre review
   accept the material read.
6. REOPENED M2 RIVERS/FORESTS — the primary rivers remain too narrow and the network too
   sparse for EU5 close zoom. Re-audit every visible watercourse against both owner-supplied
   online maps; widen the Anduin, Baranduin, Greyflood, Isen, Celduin, Carnen, Poros,
   Harnen, and other major trunks while importing or source-tracing a materially denser
   hierarchy of tributaries and headwaters. Preserve natural downstream width growth,
   irregular banks, confluences, clearances, and zero Earth transforms/decals. Retain the
   source-matching Harnen and Morgulduin routes; do not restore rejected straight lines.
   Then verify Fangorn, Old Forest, Lórien, and Ithilien canopy at close zoom.
   Current live owner review rejects the forest-object layer as far too sparse: make
   Mirkwood read as a near-continuous, deep ancient canopy and Lothlórien as an equally
   unmistakable dense birch-dominant wood rather than scattered generic trees. Audit
   species mix, close-view trunk/crown density, forest-edge fidelity, clearings, river
   corridors, and performance together; a green biome tint without dense physical trees
   does not pass.
   The v30 candidate expands the physical network from 24 to 100 source controls and
   widens nine major trunks through the installed 4→5→11→15 palette progression. The 76
   additions remain parser-safe terrain-only channels. v32 live views visibly proved the
   broadened Anduin at Caras Galadhon and Osgiliath; keep open for systematic tributary,
   bank, confluence, and canopy review across the full nine-theatre evidence set.
   ACCEPTED FOCUSED v73 RIVER CHECKPOINT — 102 non-duplicated source controls now form six reviewed
   hydrology classes; Lefnui and Serni join the indexed raster, while Sirith, the branched
   Lhûn, and all eleven Ethir distributaries retain their exact physical drainage without
   a fabricated engine graph. Fresh close/regional frames prove the broad Anduin and
   multiple narrower Gondor/Lindon channels while preserving dense Lothlórien canopy.
   Full validation, nine-day Observer playback, and exact-fingerprint paired smoke with
   zero new lines pass. The complete nine-theatre physical/source-edge review remains open.
   ACCEPTED FOCUSED v87 HYDROLOGY MECHANISM — preserve all 102 source-backed courses and
   the parser-safe twelve-channel graph. Build 24187685 renders any broad river-material
   mask as full water, so rejected v49-v51 must not return. v52 paints only nested water
   cores: ordinary drainage remains roughly two to three source pixels while upper/lower
   Anduin grow to roughly five or six and reach installed raster width 15 earlier. Fresh
   Caras Galadhon, Osgiliath, Celebrant, and Entwash evidence proves a dominant Great River
   plus narrower continuous affluents with readable banks. Keep this item open for the
   complete source-edge and nine-theatre review; add no uncited decorative watercourse.
   ACCEPTED FOCUSED v75 FOREST CHECKPOINT remains authoritative after v77 A/B: Mirkwood
   stays a near-continuous all-LOD canopy and Lothlórien stays a dense source-shaped,
   light-trunk-only wood. Removing the rejected generic green scenery does not alter any
   accepted forest transform or boundary.
7. REOPENED M2 SCALE/GRANULARITY — the measured source frame already occupies 100% of
   canvas height and 70.3% of width, with substantial land contact at both north and
   south crop edges. Do not enlarge uniformly: it would clip Forochel or Far Harad.
   Preserve equal physical scale and improve close precision through physical controls
   and later tessellation. Up to roughly 50% fewer locations than vanilla is acceptable;
   source geometry and lore anchors are not.
8. REOPENED M2 NINE-THEATRE GATE — refresh full/regional/close evidence for Shire/Old
   Forest, Forochel, Misty Mountains/Anduin, Mirkwood, Rohan/White Mountains,
   Gondor/Belfalas, Mordor, Rhûn, and Harad after each accepted physical batch. Run fresh
   Observer and paired smoke with zero mod-caused diagnostics. Do not reduce q64 or any
   source geometry to improve runtime. Fresh New Game is green on fingerprint
   `e453742c`: the 6,004-location / 2.04M-object v29 tree reached country selection and
   HUD-proven live Observer, resumed exactly once, and visibly advanced simulation during
   a 45-second monitor. Paired smoke has zero new lines. The deep session added one
   non-repeating coat-of-arms tooltip construction line before playback; eliminate it or
   prove it against a like-for-like vanilla deep session before the final M2 gate. Preserve this
   release-safe runtime budget, all canonical-forest detail floors,
   and the independent full-resolution physical controls while capturing the nine
   required terrain theatres. Do not restore the quarantined July navmesh or relaunch
   the superseded 12,104-location fingerprints.
   CURRENT v85 EVIDENCE AUTOMATION — `tools/capture_m2_theatres.py` captures a centred
   full-map silhouette, hard-resets, and captures deterministic regional/close pairs for all nine binding theatres, then runs
   bounded maximum-speed playback and releases EU5. Every finder query is statically
   required to resolve to exactly one generated display name. Belfalas now targets the
   unique `Dol Amroth` land cell at calibrated shore-visible zoom instead of the prior
   ambiguous ocean-only/inland searches. Full validation passed in 472.8 seconds,
   including all 174,763 terrain tiles and the unique-camera contract. The complete
   fresh audit is DEFERRED, not failed, while an unmanaged EU5 PID owns the
   shared machine; do not poll or commit the tool without its resulting evidence.
9. REOPENED M2 FIDELITY AUDIT — after relief, rivers, water, forests, and macro materials
   converge, compare the entire physical atlas theatre-by-theatre and feature-by-feature
   against `http://arda-maps.org/ages/third` and
   `https://www.ardacraft.me/map/middle-earth-interactive-map`. Treat the substantially
   improved coast as accepted unless a specific source mismatch is demonstrated; spend
   the next physical passes on inland fidelity rather than reopening it generically.
10. REOPENED M2 POLITICAL ASSIGNMENT — only after the physical terrain is final, re-audit
   every realm/location assignment and border against the same sources. Correct blocky or
   displaced regions, explicitly including Dunland and Lothlórien's erroneous intrusion
   into the Misty Mountains, without moving physical geography to accommodate political
   paint. Audit every owned location rather than only the large realm silhouette; add
   smaller canon-valid subfactions where TA 3018 evidence supports distinct control and
   where they improve geographic fidelity rather than fragmenting the map arbitrarily.
   The v71 focused forest checkpoint is green and owner review accepts the current
   mountain direction, so begin the static per-location audit now while the remaining
   full-atlas physical gate stays separately open. First hard contracts: Lothlórien may
   not own Misty Mountain crest/pass cells; Moria/Goblin-town/Gundabad mountain holdings
   must remain distinct; Dunland must follow its source-side lowlands rather than a blocky
   grid envelope. Produce a location-level exception report before changing ownership,
   then regenerate all downstream realm/people/census outputs coherently.
   ACCEPTED FOCUSED v72 POLITICAL CHECKPOINT — all 5,200 land locations now have a review row; 30
   well-attested realms use source-side physical envelopes with zero final violations;
   lower-confidence East/South claims have an anti-sprawl ceiling; compact-realm
   connectivity is linted. Lothlórien is a single 44-location Naith claim, Dunland a
   single 47-location lowland claim, Iron Hills a single 45-location cluster, and 200
   ordinary Ithilien locations are deliberately wild. Coherent downstream regeneration,
   full validation, fresh political-map evidence, nine days of Observer advance, and
   paired zero-new-line smoke are green on fingerprint `d595e311`. Keep the complete
   per-location audit active while the separately open nine-theatre physical review
   continues; add a smaller faction only with distinct TA 3018 control evidence.
   ACCEPTED STATIC v78 COMPONENT AUDIT CANDIDATE — schema 3 now records the full member
   list and physical disposition of every non-primary political component and validation
   rejects any unreviewed split. Sixteen reviewed cells remove Shire, White Mountains,
   Belfalas, Long Lake, Misty/Anduin, southwest Dorwinion, and Blue Mountains specks
   without changing a source polygon or major realm silhouette. Lothlórien remains one
   contiguous 21-location source-overlap claim and Dunland one contiguous 32-location
   frontier polygon. No smaller faction was invented without distinct TA 3018 evidence.
   Full validation, fresh political-map evidence, untouched 45-second playback, paired
   zero-new-line smoke, and exact-fingerprint assertion pass on `e2c57c6e`. This accepts
   the focused ownership checkpoint while the separate physical nine-theatre gate stays
   open; keep the schema-3 component audit active for every later topology change.
   CURRENT v79 RESEED AUDIT — climate-weighted density legitimately changed generated
   cell IDs, and schema 3 rejected the stale v78 dispositions before live testing. The
   replacement audit removes every cross-theatre stale repair, records ten local repairs
   with tight region/coordinate witnesses plus destination claim checks, and dispositions
   every surviving barrier split. The regenerated result has 3,467 owned and 2,537 wild
   land locations, zero claim violations, and zero unreviewed components; Lothlórien is a
   single 20-location source-overlap claim and Dunland remains one 32-location polygon.
   Static M3/M4/M5/template checks pass. Fresh political overview, playback, validation,
   smoke, and exact-fingerprint assertion remain required before this supersedes v78 as
   the accepted focused ownership checkpoint.
11. PAUSED M5 renderer: isolate or replace the inherited `boat_with_oars_unit` path that
   emitted a missing `waves_vfx` / `foam_stop` pair on 3018.2.17. The attempted direct
   vanilla control was inconclusive because it still loaded the active ENDÓRË map.
12. PAUSED M5 evidence: run a fresh non-debug five-year Observer economy session and
   capture population, market, settlement, raw-material, and development map modes.
13. PAUSED M5 roads: pursue a materially different Arda-native `spline_network.splnet` route
   (binary-format writer or editor-safe source overlay); do not repeat the two exhausted
   retail map-editor launches.
14. PAUSED M5 gate: install the validated 302-edge route graph only with matching native splines,
   then repeat paired smoke and the five-year economy evidence run.
15. Later map tooling: revisit Himling/Tolfalas adjacency candidates only through a bounded
   editor-backed experiment; the zero-byte fallback remains the proven safe contract.

## Current v74 focused checkpoint

- ACCEPTED FOREST CHECKPOINT: retain the fixed 3,057,385-transform runtime budget, but
  preserve the v74 redistribution in which Mirkwood carries 760,747/567,263/561,115
  transforms and Lothlorien 70,991/50,758/50,250 transforms at high/medium/low LOD.
  Lothlorien remains pine-free and generic-tree-free, using only installed light-trunk
  full-canopy meshes. Fresh interior/regional/close evidence proves a continuous
  birch-dominant visual read with irregular clearings; Caras Galadhon remains at the
  canonical eastern forest edge beside the Anduin. Mirkwood reads as a near-continuous
  deep mixed canopy. Full validation and a fresh 14-day Observer playback with an
  unchanged error log pass on fingerprint `98c795b5`; paired smoke remains mandatory
  before commit. Keep the complete nine-theatre physical review open for the separately
  identified Forochel, Belfalas, Rhun, Harad, macro-material, and water defects.
- ACCEPTED SOURCE-SHAPE CHECKPOINT: rectangular search envelopes are no longer sufficient
  evidence for woodland polities. Lothlorien, Fangorn, Druadan Forest, Woodland Realm,
  Woodmen, and Dol Guldur now require substantial whole-location overlap with their
  hash-pinned Arda Maps woodland polygon; Dunland uses a reviewed seven-vertex lowland
  frontier. Lothlorien is a single 21-location source-overlap Naith and no longer paints
  the Misty Mountains; Dunland is a single 32-location lowland polity. Woodland Realm
  (59), Woodmen (40), Dol Guldur (36), Fangorn (31), and Druadan (3) are all contiguous.
  The complete 5,200-location audit has zero violations. Do not add a new subfaction
  merely to consume wild land: the current Mirkwood controllers already represent the
  distinct TA 3018 powers, and lower-confidence East/South borders remain openly
  approximate pending stronger source evidence.

## ACCEPTED v75 focused checkpoint

- Preserve v74's source-shaped ownership exactly: LOR 21, DUN 32, WOO 59, WDM 40,
  DOL 36, FAN 31, and DRU 3 remain contiguous with zero audit violations. Do not add a
  decorative faction merely to fill wilderness.
- Preserve the fixed 3,057,385-transform budget and v12 redistribution. Current
  high/medium/low counts are Mirkwood 950,729/677,500/670,517 and Lothlorien
  75,643/54,871/54,459; all Lothlorien transforms remain installed light-trunk meshes.
  Complete tundra vegetation must remain within its sparse 1,000..30,000 high,
  700..24,000 medium, and 700..24,000 low bounds.
- REJECTED: never restore terrain-material v44's green earth/sand islands or v45's huge
  dark rock/sand blotches. The negative live evidence is retained under
  `docs/screens/20260802_v75_climate_forests/` and
  `docs/screens/20260802_v75b_climate_forests/`. The complete material source, preview,
  and cache are restored to proven v43 with zero diff. Reopen Harad/Forodwaith materials
  later only through a materially different renderer mechanism.
- ACCEPTED: post-rollback full validation passed in 405.4 seconds. Fresh v75c frames prove
  the denser canonical forests and source-shaped political overview on fingerprint
  `fb07a215`; the separate untouched v75d session ran 45 seconds at maximum speed with
  zero recovery and a baseline-only 1,486-byte error log. Paired smoke passed in 201.8
  seconds with zero new mod lines and exact `assert-smoked`. Commit and push this coherent
  checkpoint, then return to the still-red wider nine-theatre physical/material review.

## Current v80 priority update (supersedes the stale v74/v75 preservation counts above)

- REOPENED M2 remains the only content priority. The full nine-theatre owner gate is red;
  do not resume gameplay work.
- DENSE FORESTS: fresh v79 Caras Galadhon and Woodmen's Hall close views reproduced the
  owner-reported defect. Mirkwood still exposed broad park-like gaps at ordinary play
  zoom, and Lothlorien's riverward view read as a dark generic wall. Generator v13 raises
  the bounded corpus from 3,093,385 to 3,493,385 total transforms, broadens only tree
  canopies, and protects rare-clearance interiors at every LOD. The exact named-zone
  census is Mirkwood 1,112,756/796,168/788,083 and Lothlorien
  87,564/69,865/69,863 at high/medium/low. Lothlorien remains light-trunk-only with zero
  pine or generic variants; Fangorn, Old Forest, and Ithilien retain independent floors.
  Static generation/checks pass. Full validation, fresh regional/close live pairs,
  playback, paired smoke, and exact-fingerprint assertion remain mandatory.
- POLITICAL FRONTIERS: every one of the 38 realms now has an explicit geography contract;
  there are zero free-sprawl realms. Lothlorien and the three Mirkwood controllers must
  satisfy both source-forest overlap and an irregular theatre partition. Irregular
  envelopes replace unconstrained Voronoi expansion for Harnendor, Qarsad, Far Harad,
  Khand, and the three Rhunic polities, leaving neutral buffers where the sources do not
  support centralized TA 3018 control. The coherent result has 3,044 owned and 2,156
  deliberately wild land locations, zero violations, and zero unreviewed components;
  Lothlorien is one compact 15-location Naith claim east of the Misty crest. The
  permanent QA raster labels every capital/tag. No decorative subfaction was added.
- v79 LOAD BASELINE: before these edits, a fresh HUD-proven Observer start and untouched
  45-second maximum-speed playback passed on exact fingerprint `1f899f22` with the
  1,486-byte error-log baseline. This proves the v79 source-biome tree was loadable, not
  that v80 or the full physical gate is accepted.
- v80b LIVE FOCUSED RESULT: retain the slimmer installed
  `environment_oceanic_tree_01/02` meshes for Lothlorien; reject the v80 wide-canopy
  calibration retained under `docs/screens/20260802_v80_dense_forests_frontiers/` as too
  dark/generic. A genuinely fresh v80b New Game reached HUD-proven Observer on exact
  fingerprint `2df4b63d`; regional/close Lothlorien views expose pale trunks and a closed
  broadleaf canopy, while Mirkwood remains a darker near-continuous mixed forest. The
  wide live Wilderland political view shows compact Lothlorien outside Moria/Misty
  Mountain paint; the tagged full-world QA raster proves the new East/South wilderness
  buffers. A 45-second maximum-speed playback required
  zero recovery and retained the exact 1,486-byte error log. Final full validation passed
  in 430.5 seconds. Paired vanilla/ENDORE smoke then passed in 200.8 seconds with zero
  mod-unique error lines, and `eu5_slot.py assert-smoked` binds that result to exact
  fingerprint `2df4b63d`. Commit and push this focused batch, then continue the still-red
  full nine-theatre M2 owner gate.

## Current v82 physical checkpoint

- ACCEPTED LIVE CLIMATE MECHANISM: keep one continuous ENDÓRË renderer biome, but assign
  its previously unused palette channels 8 and 9 to installed `sediment_dark_01` tundra
  and `sediment_orange_01` steppe, with installed `sand_rocks_variation_01` reserved for
  the Far Harad arid core. Source-smoothed edges blend only those dedicated channels;
  never restore v44/v45's broad binary noise mixtures or location-scoped biome templates.
  Fresh close views prove cold stony Forochel, ochre Rhûn/Near Harad, and distinct stony
  Qarsad desert without location-cell seams or pale/dark material islands. Mordor retains
  final ash precedence. Static lowland coverage floors are 96% tundra, 90% steppe, and
  90% arid sand.
- ACCEPTED ANCIENT-FOREST REBALANCE: preserve the fixed 3,493,385-transform corpus and
  unchanged hash-pinned forest boundaries. Old Forest now receives 75,027/56,507/55,995
  high/medium/low transforms instead of roughly 13k per LOD. The exact source core is a
  closed canopy in the regional evidence; Bucklebury and generated `Land 4390` sit on its
  agricultural/roadward edge and must not be used alone as an interior-density verdict.
  Mirkwood remains dense at 1,060,221/759,520/752,336, and Lothlórien remains a dense
  light-trunk-only wood at 85,157/67,671/67,930.
- LIVE SAFETY: a fresh New Game reached HUD-proven Observer on exact candidate fingerprint
  `9edf9d2da385ca1c3a619ea8c213226f851c7a2f8e969070836beed31cd073eb`; 45 seconds of
  maximum-speed playback required one initial unpause, no recovery, and retained the exact
  1,486-byte error-log baseline. Belfalas retesting at unique Edhellond proves that the
  earlier ocean-only Dol Amroth capture was an ambiguous first-result finder target, not a
  coastline regression. Full validation passed in 462.6 seconds. Paired vanilla/ENDÓRË
  smoke passed in 202.7 seconds with zero new lines, and exact-fingerprint assertion binds
  it to `9edf9d2da385ca1c3a619ea8c213226f851c7a2f8e969070836beed31cd073eb`.
- GATE STATUS: M2 remains red. Continue the complete nine-theatre source-edge sweep,
  small-water presentation, regional river visibility, and any theatre whose unique-anchor
  evidence is still inconclusive. Do not reopen accepted coast or mountain relief without
  a specific source mismatch, and do not resume gameplay milestones.
- NEXT DRAINAGE MECHANISM: the source atlas already contains 102 non-duplicated courses,
  but the installed-safe raster currently serializes only 12 independent source-to-water
  channels (28,512 width-marker pixels versus vanilla's 741,652). Fourteen additional
  named controls join parents and 76 feeders remain physical incision/material because
  build 24187685 rejects custom affluent graphs. Do not naively promote them. Either prove
  an exact retail junction-marker grammar in a bounded experiment or strengthen only the
  source-backed physical feeder presentation while retaining the parser-safe 12-channel
  graph.

## Superseded v83 drainage-visibility checkpoint

- ACCEPTED NARROW MECHANISM: retain the parser-safe 12-channel `rivers.png` byte-for-byte
  and strengthen only the terrain material around the 90 source-backed physical courses.
  Named terrain-only trunks/branches/tributaries use a 0.82 visibility scale with a
  four-pixel floor; unnamed trunks/branches/feeders use 0.72 with a three-pixel floor.
  Independently serialized engine rivers retain the accepted 0.62/two-pixel calibration.
  Exact paths, height incision, vegetation clearance, coast, relief, ownership, and the
  102-course control atlas remain unchanged.
- LIVE RESULT: a genuinely fresh visual New Game reached HUD-proven Observer on exact
  candidate fingerprint `b299dedc65704ba3b3c8c408274fb8dd7b20d088776a7e7cbb96313546d1eeed`.
  Standardized +12/+14 evidence under
  `docs/screens/20260802_v83_river_visibility/` proves readable Brandywine,
  Celebrant/Anduin, lower-Anduin tributary, and upper-Lhun drainage without broad
  transport-like bands. Indexed courses remain blue water; build-unsafe affluent courses
  remain visibly incised physical drainage rather than being misrepresented as parser
  water. Maximum-speed Observer playback ran 45 seconds with zero recovery and retained
  the accepted 1,486-byte error-log baseline. Paired vanilla/ENDÓRË smoke passed in 226.4
  seconds with zero new or mod-unique diagnostics, and exact-fingerprint assertion binds
  it to the candidate tree. Full validation passed in 415.2 seconds across the complete
  generated world and lint surface.
- GATE STATUS: this is a regional-visibility improvement, not completion of the river
  system or M2. The full physical gate remains red. Continue source-edge review and seek a
  materially different, retail-proven affluent mechanism only if it can preserve load
  safety; do not repeat the already rejected red-endpoint custom graph or inflate these
  channels into decorative corridors.

## Current v86 hierarchy/profile candidate

- Keep the source-aligned strategic hierarchy correction: Mordor's interior is no longer
  classified as Ithilien/eastern Rhun, Rivendell lies west of the Misty crest, Dale and
  isolated Erebor are distinct from the Grey Mountains, and Erech lies south of Rohan.
  Ten canonical anchor contracts, all 38 realm contracts, and every component disposition
  must remain green. Current ledger: 3,198 owned / 2,002 deliberately wild land cells,
  zero claim violations, no undispositioned political component.
- Preserve the smoke/player graphics separation. Smoke must restore the exact prior
  settings payload; manual testing can run `gamedriver.py profile visual` or a direct
  `launch --visual-map --no-debug-mode`. Never interpret a terrain-disabled manual frame
  as evidence about the generated physical map.
- LIVE STATUS: the hierarchy candidate loaded in a fresh New Game and the deterministic
  theatre audit completed with clean bounded playback. The first full-map frame exposed a
  capture-order bug rather than a map defect; the driver now resets to the full map only
  after establishing its finder context. A corrected complete atlas remains part of the
  still-red M2 owner gate.
- COMMIT GATES: repository-wide validation passed in 421.8 seconds; paired smoke passed
  in 201.3 seconds with zero new mod lines; `eu5_slot.py assert-smoked` covers exact
  fingerprint `f75e17f804a716537ec2b5acd9ca126bbae05b5d7338ca3f640ce8159e4151c9`.
  M2 remains red regardless; do not resume gameplay content.

## Current v87 hydrology checkpoint

- Preserve generator v52's core-only water mechanism and exact fingerprint
  `f75e17f804a716537ec2b5acd9ca126bbae05b5d7338ca3f640ce8159e4151c9` until the final
  validation/smoke pair. The 193.3 MB terrain cache reuses unchanged height and replaces
  only the material payload/provenance needed by the river hierarchy.
- Evidence under `docs/screens/20260802_v87d_hydrology/` and
  `docs/screens/20260802_v87e_hydrology/` shows both Anduin reaches plus Celebrant and
  Entwash. The exact-fingerprint session completed 45 seconds of maximum-speed playback
  with zero recovery and the baseline-only 1,486-byte error log.
- REMAINING M2 WORK: run the corrected full nine-theatre atlas, continue feature-level
  comparison with the accepted online maps, and refine any demonstrable course, bank,
  or confluence mismatch. Jagged material edges may be softened only if both banks stay
  readable and the inland-sea failure does not return. M2 remains red pending explicit
  owner acceptance.
