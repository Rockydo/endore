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
4. REOPENED M2 BELFALAS — preserve the hash-pinned Arda Maps mainland ring: the apparent
   inlet is backed by 2,043 raw Belfalas-window source vertices and the committed
   simplification deviates by at most roughly three location-raster pixels. Treat the
   remaining defect as shoreline/material/location presentation, not permission to
   invent a different bay. Verify regional and maximum-close zoom after the pond probe.
5. REOPENED M2 MACRO BIOMES — Mordor's fifteen-point ash oval is rejected and replaced
   by a source-range/axis/Mount Doom field. Replace the remaining Brown Lands blob and
   broad Rhûn/Harad proof-era envelopes with audited source-native or explicitly logged
   continuous controls; never reintroduce an oval or straight clipped climate edge.
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
