# TODO

1. REOPENED M2 — physical geography: replace the rough control geometry with
   cartographically natural coasts, bays, islands, inland seas, lakes, forest boundaries,
   mountain masses, valleys, and river catchments at several scales. Follow
   `docs/m2/VISUAL_REOPEN_GATE.md`; do not add gameplay content while this gate is open.
2. REOPENED M2 — close-zoom renderer: prove visible 3D relief, terrain materials,
   Arda-native forest objects/coverage, and correctly scaled rivers in the actual
   non-debug game. No Earth-authored transform or decal may return.
3. REOPENED M2 — scale and granularity: the engine already uses the full native
   16384×8192 locations canvas, so enlarge Middle-earth's footprint within that canvas
   where useful, then increase geographic location granularity only after the revised
   coast, relief, hydrology, and biome controls are stable.
4. REOPENED M2 gate: capture full-map, regional, and close-zoom terrain/political
   screenshots at the Shire/Old Forest, Misty Mountains/Anduin, Mirkwood, Rohan/White
   Mountains, Mordor, Belfalas, Forochel, Rhûn, and Harad; run fresh Observer and require
   zero mod-caused diagnostics.
5. PAUSED M5 renderer: isolate or replace the inherited `boat_with_oars_unit` path that
   emitted a missing `waves_vfx` / `foam_stop` pair on 3018.2.17. The attempted direct
   vanilla control was inconclusive because it still loaded the active ENDÓRË map.
6. PAUSED M5 evidence: run a fresh non-debug five-year Observer economy session and
   capture population, market, settlement, raw-material, and development map modes.
7. PAUSED M5 roads: pursue a materially different Arda-native `spline_network.splnet` route
   (binary-format writer or editor-safe source overlay); do not repeat the two exhausted
   retail map-editor launches.
8. PAUSED M5 gate: install the validated 302-edge route graph only with matching native splines,
   then repeat paired smoke and the five-year economy evidence run.
9. Later map tooling: revisit Himling/Tolfalas adjacency candidates only through a bounded
   editor-backed experiment; the zero-byte fallback remains the proven safe contract.
