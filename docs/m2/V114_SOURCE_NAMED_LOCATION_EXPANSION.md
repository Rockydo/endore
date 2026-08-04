# v114 source-named location expansion

## Purpose

The physical map has dense generated political locations, but generic regional
compounds can obscure landmark recognition at close and regional zoom. v114
promotes 27 additional, exact-source Middle-earth sites to named EU5 locations.
This is a cartographic readability pass: it changes no coastline, terrain,
river, realm claim, capital, or generated-location geometry.

## Method

Each new row in `docs/world/control/m3_landmarks.csv` comes from a named point
in the current, hash-pinned Arda Maps Third Age topology. Its coordinate was
projected through the same committed Arda Maps-to-ArdaCraft calibration used by
the map-control generator, then resolved against the current 6,004-location
land mesh. All 27 resolve to distinct passable locations; no established
settlement, realm capital, canonical ruin, or source landmark is displaced.
Each post-baseline location also reserves its displaced generic-name stream
slot. This keeps unrelated generated labels and source-bound evidence cameras
stable as the gazetteer grows.

The batch covers:

- Four named Shire settlements: Bywater, Frogmorton, Stock, and Haysend.
- Framsburg; Eagles' Eyrie; Beorn's Hall; Redhorn Gate; Cerin Amroth; and the
  Glittering Caves.
- Tarlang's Neck, Cirith Gorgor, and Morgai.
- The seven Gondor beacon peaks: Amon Dîn, Eilenach, Nardol, Erelas,
  Min-Rimmon, Calenhad, and Amon Anwar.
- Caradhras, Celebdil, Fanuidhol, Mindolluin, Irensaga, Dwimorberg, and
  Starkhorn.

Book citations are included row-by-row where the site is named in Tolkien;
the precise placement is attributed to the source point. Framsburg remains a
ruin. The four source-city entries remain villages; every other non-settlement
site is a `landmark`, so the naming improvement does not invent a city,
population, or political claim.

## Deterministic result

The M3 allocator resolves the complete enlarged ledger over the unchanged
6,004-location mesh and preserves all 38 realm totals: 3,030 assigned land
locations and 2,974 deliberate wildland locations. The downstream M5 census
regeneration confirms that Framsburg has no starting population; the world has
5,178 populated locations and 12 markets. The complete validation suite passes,
including source-bound camera resolution and all map/census layers. The paired
real-game vanilla/ENDÓRË smoke also passes with zero new mod-attributable
`error.log` lines.
