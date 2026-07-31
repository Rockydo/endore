# TODO

1. REOPENED M2 remains the sole content priority. Follow
   `docs/m2/VISUAL_REOPEN_GATE.md`; do not resume gameplay work until the physical map
   receives explicit owner acceptance. The current source-audited runtime tree loads,
   but the nine-theatre visual gate remains red.
2. REOPENED M2 MOUNTAINS — retain the source-pinned foothill/axis/peak/saddle height
   model, neutral renderer template for all 600 separately impassable mountain cells, and
   v28 continuous source-crest material weight. Fresh Khazad-dum evidence proves that this
   removes giant location-shaped slabs and joins the former exposed-rock islands into a
   more coherent massif without opening the ranges. Next soften the remaining hard rock
   fringe, improve regional ridge readability, and verify all named passes without moving
   binding axes, peaks, or saddles.
3. REOPENED M2 INLAND WATER — retain the scale-enforced material-pond representation for
   all ten source lakes occupying at most 64 pixels in the 4096x2048 control atlas
   (189 pixels total). Mirrormere and minor lakes 04-07/10-14 remain exact lake-biome
   polygons over continuous physical land; the five larger lakes remain engine water.
   Fresh Mirrormere evidence proves the deep rectangular quarry is gone. Improve the
   flat wet-material patch into a subtle close-zoom water/scenery read later without
   restoring engine-water host cells or changing any source outline.
4. REOPENED M2 BELFALAS — preserve the hash-pinned Arda Maps mainland ring: the apparent
   inlet is backed by 2,043 raw Belfalas-window source vertices and the committed
   simplification deviates by at most roughly three location-raster pixels. Treat the
   remaining defect as shoreline/material/location presentation, not permission to
   invent a different bay. Verify regional and maximum-close zoom after the pond probe.
5. REOPENED M2 RIVERS/FORESTS — verify readable Anduin, Baranduin, Greyflood, Isen,
   Celduin, Carnen, Poros, and Harnen channels plus Fangorn, Old Forest, Lórien, and
   Ithilien canopy. Preserve source axes, downstream width grammar, porous margins,
   river clearances, and zero Earth transforms/decals. Harnen now uses the matching
   unnamed Arda Maps source channel plus only a two-point coast continuation; do not
   restore the rejected straight diagonal or farther-west mouth. Morgulduin likewise
   uses its matching unnamed source line. All 24 production river axes are now
   source-derived.
6. REOPENED M2 SCALE/GRANULARITY — the measured source frame already occupies 100% of
   canvas height and 70.3% of width, with substantial land contact at both north and
   south crop edges. Do not enlarge uniformly: it would clip Forochel or Far Harad.
   Preserve equal physical scale and improve close precision through physical controls
   and later tessellation. Up to roughly 50% fewer locations than vanilla is acceptable;
   source geometry and lore anchors are not.
7. REOPENED M2 NINE-THEATRE GATE — refresh full/regional/close evidence for Shire/Old
   Forest, Forochel, Misty Mountains/Anduin, Mirkwood, Rohan/White Mountains,
   Gondor/Belfalas, Mordor, Rhûn, and Harad after each accepted physical batch. Run fresh
   Observer and paired smoke with zero mod-caused diagnostics. Do not reduce q64 or any
   source geometry to improve runtime. Fresh New Game is green on fingerprint
   `8ca808d7`: the 6,004-location / 2.04M-object v28 tree reached country selection and
   HUD-proven live Observer in 115 seconds, resumed exactly once, and advanced from
   3018.1.1 through 3018.2.1 with no error-log growth. Preserve this
   release-safe runtime budget, all canonical-forest detail floors,
   and the independent full-resolution physical controls while capturing the nine
   required terrain theatres. Do not restore the quarantined July navmesh or relaunch
   the superseded 12,104-location fingerprints.
8. PAUSED M5 renderer: isolate or replace the inherited `boat_with_oars_unit` path that
   emitted a missing `waves_vfx` / `foam_stop` pair on 3018.2.17. The attempted direct
   vanilla control was inconclusive because it still loaded the active ENDÓRË map.
9. PAUSED M5 evidence: run a fresh non-debug five-year Observer economy session and
   capture population, market, settlement, raw-material, and development map modes.
10. PAUSED M5 roads: pursue a materially different Arda-native `spline_network.splnet` route
   (binary-format writer or editor-safe source overlay); do not repeat the two exhausted
   retail map-editor launches.
11. PAUSED M5 gate: install the validated 302-edge route graph only with matching native splines,
   then repeat paired smoke and the five-year economy evidence run.
12. Later map tooling: revisit Himling/Tolfalas adjacency candidates only through a bounded
   editor-backed experiment; the zero-byte fallback remains the proven safe contract.
