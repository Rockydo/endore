# M3 realm gate

Gate date: 2026-07-29

M3 is complete on the corrected native physical map. This evidence supersedes every
quarantined M3 screenshot made before the owner's close-zoom rejection.

## Generated world

- 38 first-class realms
- 5,812 named locations in the gazetteer
- 4,189 owned passable-land locations
- 1,011 deliberately wild passable-land locations
- 260 unowned impassable mountains
- 32 unowned lakes
- 320 unowned sea zones
- 21 canonical ruins, all without placeholder census pops

The generator derives political color from the same location labels used by the physical
world. It then checks the exact authored elevation beneath every owned control pixel:
200,167 owned pixels, zero at or below the installed raw waterline sample 5466. All 38
capitals resolve to passable land and the maximum capital-to-authored-seat snap is
0.021535 normalized map units.

## Real-game verification

The non-debug visual renderer loaded the 38-realm country-selection map. Northern and
central/southern captures show realm labels over their corresponding colored land; ocean
and inland water remain blue and contain no realm ownership. This directly closes the
reported failure where names and political colors appeared displaced into the ocean.

Observer entered live play and advanced from 1 January through 25 January 3018. The
captured runtime error log contains only the established local DX12 feature-query,
unavailable store-item, AudioArena, and automated-input-context lines. It contains no
mod-caused country, ownership, location, geography, terrain, cache, locator, script,
culture, religion, pop, or market diagnostic.

M3 still uses parser-safe installed culture, faith, census, government-title, and ruler
values. Those are explicitly scheduled for M4–M6 and are not final content. They do not
alter the accepted political/physical placement result.

## Evidence

- [Exact generated political/physical control](../world/derived/m3_political_control.png)
- [Northern political placement](political_north.png)
- [Central and southern political placement](political_central_south.png)
- [Live Observer entry](observer_live.png)
- [Observer advanced to 10 January](observer_3018_01_10.png)
- [Deep runtime error log](deep_error.txt)
- [Corrected close physical land](../m1/screenshots/05_native_close_land_corrected.png)
- [Corrected close open sea](../m1/screenshots/06_native_close_open_sea.png)
- [Corrected authored shoreline](../m1/screenshots/07_native_close_shoreline.png)

## Gate checks

- `gmake validate`: PASS
- paired vanilla/mod `gmake smoke`: PASS, zero mod-only normalized error lines
- political/physical ownership projection: PASS, zero wet-owned pixels
- every capital on passable land: PASS
- country-selection north and central/south review: PASS
- live Observer time advance: PASS
- mod-caused deep `error.log` lines: zero
