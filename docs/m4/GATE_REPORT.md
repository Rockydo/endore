# M4 Gate Report — Peoples and Faiths

## Result

M4 is green. ENDÓRË now owns 33 cultures in 10 culture groups, 10 language roots with
33 culture dialects, and 10 faiths in three gameplay groups. All 5,200 passable land
locations and all 38 realm primaries resolve to authored Middle-earth definitions.

The deterministic name ledgers provide 1,105 localized male, female, and house names.
Every installed religion file is exact-overlaid with a terminal availability date of
3200.1.2, so inherited Earth faiths cannot enter the 3018 campaign.

## Real-game proof

The actual game rendered the Culture (Location) and Religion (Location) map modes with
authored terms across the northern, eastern, western, and southern theatres. Country
selection also showed the expected primary culture and faith for representative realms.

The first technical-ABI experiment used size `0.001` populations. This build rounded
them away and reported cultures with no populations, so that experiment is rejected and
superseded. The binding setup distributes one size `0.01` installed ABI population per
custom-dominant land location. These compatibility presences never become dominant.

A fresh non-debug Observer session advanced from 3018.1.1 to 3018.1.20 at maximum speed
without recovery. `error.log` remained byte-identical at 1,486 bytes throughout and
contained only the established machine/store/audio baseline.

## Evidence

- [Country selection](country_selection.png)
- [Northern culture map](culture_map_north.png)
- [Eastern and southern culture map](culture_map_east_south.png)
- [Northern faith map](faith_map_north.png)
- [Southern and eastern faith map](faith_map_south_east.png)
- [Observer at 3018.1.20](observer_3018_01_20.png)
- [Final deep error log](deep_error.txt)
- [Evidence hashes and counts](gate_evidence.json)

## Gate checklist

- [x] Culture groups, cultures, language roots, dialects, and name pools generated.
- [x] Light, Shadow, and Old Ways faith surfaces generated and localized.
- [x] Every passable land location and realm primary assigned.
- [x] Installed Earth religions unavailable throughout the campaign.
- [x] Static validation and paired real-game smoke green.
- [x] Culture and faith map modes visually verified.
- [x] Live Observer stable with an unchanged error log.
