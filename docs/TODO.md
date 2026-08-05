# ENDORE backlog

This is the authoritative forward backlog, not a changelog. Every bullet uses `[ ]` or
`[X]`. Work always starts with the first unblocked unchecked task. Completed evidence
belongs in `docs/PROGRESS.md` and `docs/m*/`; do not turn this file into a revision log.
No milestone after M2 may start while the M2 gate remains unchecked.

## Always in force

- [ ] At each session start, read the master plan, both `AGENTS.md` files, the ANTIQVITAS
  master plan, and `docs/ENGINE_FACTS.md`; then read this file and take the first
  unblocked task.
- [ ] Keep `TODO.md`, `PROGRESS.md`, `DECISIONS.md`, `ASSUMPTIONS.md`, and `BLOCKERS.md`
  current. Record canon judgements and source limitations when they are made.
- [ ] Before every commit, pass `gmake validate`. For every game-visible commit, acquire
  the shared EU5 lease without waiting, pass `gmake smoke`, assert the exact fingerprint,
  commit one coherent green batch, and push it. A busy lease defers only that runtime gate.

## M2 - Map v1 (current hard gate)

- [X] Publish the v132 source-marker orientation batch with its green paired real-game
  smoke assertion and final validation. Evidence: `docs/m2/V132_SOURCE_MARKER_ORIENTATION.md`.
- [X] Continue the political fidelity audit from direct Arda Maps Third Age and ArdaCraft
  controls. Address one demonstrated mismatch at a time; each ownership change requires a
  precise source, canon rationale, exact control/contract, and topology proof. Keep
  uncertain land deliberately wild; never invent broad borders.
  - [X] Complete the source-backed Eregion/Moria batch: restore Eregion as its own
    geographic region north of the Glanduin and west of Moria, correct Warg Hill from an
    inferred Moria extension to deliberate wilderness, then verify the complete generated
    hierarchy, topology, and runtime once.
  - [X] Complete the Eregion exterior reconciliation: keep the Angle in North Arnor,
    confine Moria to the Anduin-side mountain interior, and enforce the empty TA 3018
    Eregion land as deliberate wilderness with one complete generated and runtime proof.
  - [X] Complete the direct-source location-granularity batch: add only separated,
    TA 3018-valid point locations with exact Arda Maps/ArdaCraft controls and a complete
    owner-or-wilderness contract; do not turn aliases or uncertain reconstructions into
    duplicate locations. Evidence: `docs/m2/V135_SOURCE_LOCATION_GRANULARITY.md`.
  - [X] Complete the Buckland anchor-density batch: turn only exact, separate Tolkien-map
    settlements into pinned land cells so local source positions do not displace generic or
    neighbouring canonical locations. Keep Buckland's political treatment unchanged until
    the M3 realm roster is unlocked. Evidence: `docs/m2/V136_BUCKLAND_ANCHOR_DENSITY.md`.
  - [X] Complete the geographic-witness anchor batch: pin the Slag-hills, Haudh in Gwanur,
    and Forsaken Inn to their separate exact source cells without converting physical
    landmarks into settlements or moving surviving locations. Evidence:
    `docs/m2/V137_GEOGRAPHIC_WITNESS_ANCHORS.md`.
- [X] Audit all named locations and realm placement in the enforced theatres: Gap of
  Rohan; Lothlorien/Moria; Dale/Lonely Mountain; Mordor/Ithilien; represented East/South;
  and the Far Harad fringe. Correct only source-proven errors, including compact
  sub-realms where TA 3018 control actually warrants them. Evidence:
  `docs/m2/V134_EREGION_EXTERIOR_RECONCILIATION.md`.
- [ ] Correct physical geography only when a specific source-backed defect is identified:
  coasts and inland waters; jagged range axes and isolated Erebor; dense shaped forests
  including birch Lothlorien and Mirkwood; native rivers and tributaries; and close-zoom
  terrain, material, vegetation, and relief visibility. No vanilla-Earth residue,
  placeholder geography, or decorative painted water is acceptable.
- [ ] Preserve the native-river contract: `in_game/map_data/rivers.png` is the sole water
  and width authority. Add an engine river only with the installed vanilla raster grammar,
  a source-exact course, and live proof. Never simulate river width with blue terrain;
  retain unsupported drainage as dry source-shaped valleys.
- [ ] Run the M2 acceptance gate only after the audits above are clean: actual-game
  screenshots and an in-game test must prove recognizable full Middle-earth extent,
  close terrain, forest density, mountains, major rivers, and political placement. Keep
  M2 unchecked until the owner-fidelity review and all required evidence are green.
  - [X] Prove the materially different exact-key console camera route in a fresh Observer
    session. It must center the source-bound Old Forest and a second separated theatre
    with a measured camera transition; do not reopen or weaken the blocked Finder route.
    Evidence: `docs/screens/20260805_m2_exact_key_probe_v5/` and the matching
    `console_history.txt` transforms/engine marker.
  - [X] Prove the fresh deep-load log has no coat-of-arms or Finder data-model diagnostics
    after the collision-free `me_coa_*` realm-arm and exact-key camera batch. Evidence:
    `docs/screens/20260806_m2_nondebug_deep_log_v1/` (fresh non-debug 45-second Observer;
    only installed DX12/store/audio diagnostics remain).

## Completed gates

- [X] M0 minimum bootstrap: repository, GitHub remote, ported ANTIQVITAS toolchain,
  isolated user data, shared EU5 lease, vanilla baseline, and empty-mod smoke.
- [X] M1 Proof of Arda: a custom Middle-earth-shaped world loads in EU5 at TA 3018.1.1
  without reliance on vanilla Earth.

## Locked until M2 is accepted

- [ ] M3 Realms: finalize the playable realm roster, ownership, named locations, ruins,
  and first-pass heraldry; prove every location is assigned or deliberately wild.
- [ ] M4 Peoples and faiths: cultures, languages, name pools, faiths, templates, and
  complete localization.
- [ ] M5 Census: populations, markets, roads, ranks, buildings, armies, and the required
  five-year economy soak.
- [ ] M6 Power and people: governments, laws, estates, diplomacy, international bodies,
  characters, and traits.
- [ ] M7 Military: setting-appropriate units, forts, navies, balance, and a verified
  gunpowder-free ten-year soak.
- [ ] M8 Knowledge: Middle-earth ages, advances, and institution replacements.
- [ ] M9 Economy finish: goods, production, markets, buildings, prices, and a 25-year
  no-collapse soak.
- [ ] M10 Narrative: War of the Ring, Ring quest, Saruman arc, set pieces, missions,
  flavor, and in-game tests.
- [ ] M11 Art and language: bespoke 2D art generated four-up using exact vanilla EU5
  asset references and Peter Jackson trilogy art-direction references; terminology,
  localization, palette review, and zero placeholders. Do not add audio.
- [ ] M12 Hardening and release: performance, canon-plausibility runs, soak to TA 3200,
  issue triage, v0.1.0 tag, GitHub release, and the complete definition of done.
