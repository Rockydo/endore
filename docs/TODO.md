# ENDÓRË backlog

This is the live, authoritative backlog—not a changelog. `docs/PROGRESS.md` records
completed work and `docs/m2/` holds technical evidence. An unchecked task means work
continues; no milestone after M2 may begin while the M2 gate is unchecked.

## Operating rules — apply to every unchecked task

- [ ] Read `docs/ENDORE_MASTER_PLAN.md`, `AGENTS.md`, the ANTIQVITAS reference plan, and
  `docs/ENGINE_FACTS.md` at every session start; follow their precedence rules.
- [ ] Keep all work on `G:\`; never edit the installed game. Before each game-visible
  commit, pass `gmake validate`, acquire the shared EU5 lease without contention, pass
  `gmake smoke`, assert the exact fingerprint, commit a coherent batch, and push it.
- [ ] Keep this file, `PROGRESS.md`, `ASSUMPTIONS.md`, `DECISIONS.md`, and `BLOCKERS.md`
  current. Record every canon judgement and source limitation; move completed history out
  of this backlog.

## Current priority: M2 — the Map v1 gate

- [X] Prepare the v130 source-pinned landmark/topology batch: the final 541.0-second
  validation and retained green smoke assertion cover the complete generated dependency
  chain. Evidence: `docs/m2/V130_SOURCE_PINNED_LANDMARK_TOPOLOGY.md`.
- [ ] Continue the source-led political fidelity audit, one demonstrable mismatch at a
  time, against the owner-approved Arda Maps Third Age and ArdaCraft controls. Do not
  invent broad borders: uncertain cells remain wild; every changed owner needs a precise
  source, a canon rationale, an exact control/contract, and topology validation.
  - [X] Restore the source-pinned Archet, Combe, and Staddle cells to contiguous
    Bree-land; see `docs/m2/V131_BREELAND_FOUR_VILLAGES.md`.
- [ ] Recheck every named location and realm position in the six enforced theatres:
  Gap of Rohan; Lothlórien/Moria; Dale/Lonely Mountain; Mordor/Ithilien; represented
  East/South; and the Far Harad fringe. Correct only source-proven defects, including
  compact sub-realms where TA 3018 control warrants one.
- [ ] Preserve and improve the physical map only for a specific source-proven defect:
  natural coastlines and inland waters; jagged mountain axes and isolated Erebor; dense
  source-shaped forests (including birch Lothlórien and Mirkwood); complete lore-backed
  drainage; and close-zoom terrain/material/vegetation visibility. No vanilla-Earth
  terrain, decorative painted rivers, or generic placeholder geography is acceptable.
- [ ] Maintain the native-river contract: `map_data/rivers.png` is the only water-width
  authority; never paint blue terrain shoulders beside thin splines. Extend engine rivers
  only with the installed vanilla raster grammar, an exact source course, and live proof;
  retain non-engine drainage as dry source-shaped valleys rather than misrepresenting it.
- [ ] Perform the M2 milestone verification only after the source audits above are clean:
  actual-game map-screen screenshots and one in-game test covering the recognizable full
  Middle-earth extent, close terrain, forests, mountains, major rivers, and political
  placement. M2 stays unchecked until that evidence and the owner-fidelity gate are green.

## Completed foundations

- [X] M0 minimum bootstrap: repository, remote, ported ANTIQVITAS toolchain, isolated
  user directory, shared EU5 lease, vanilla baseline, and empty-mod smoke.
- [X] M1 Proof of Arda: a custom Middle-earth-shaped world loads in actual EU5 at
  TA 3018.1.1, with the map no longer relying on vanilla Earth.

## Blocked until M2 is accepted

- [ ] M3 realms: finalize the playable realm roster, ownership, named locations, ruins,
  and first-pass heraldry only after M2 is green.
- [ ] M4 peoples and faiths: finalize cultures, languages, names, faiths, and templates
  only after M2 is green.
- [ ] M5 census: finalize populations, markets, roads, ranks, buildings, and armies; run
  the required five-year economy soak only after M2 is green.
- [ ] M6 power and people: governments, laws, estates, diplomacy, international bodies,
  characters, and traits.
- [ ] M7 military: setting-appropriate forces, forts, navies, balance, and a verified
  gunpowder-free ten-year soak.
- [ ] M8 knowledge: Middle-earth ages, advances, and institution replacements.
- [ ] M9 economy finish: goods, production, markets, buildings, prices, and a 25-year
  no-collapse soak.
- [ ] M10 narrative: War of the Ring situation, Ring quest, Saruman arc, set pieces,
  missions, flavor, and in-game tests.
- [ ] M11 art and language: bespoke 2D art generated four-up with exact vanilla EU5 asset
  references and Peter Jackson trilogy art-direction references; terminology, localization,
  palette review, and zero placeholders/forbidden terms. Do not add audio.
- [ ] M12 hardening and release: performance, canon-plausibility runs, soak to TA 3200,
  issue triage, v0.1.0 tag, GitHub release, and the full definition of done.
