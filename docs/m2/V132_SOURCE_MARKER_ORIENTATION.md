# v132 source-marker orientation at the Anduin, Lothlórien, and Rohan

This M2 batch adds four named, map-scale orientation witnesses only where the active
6,004-location tessellation has an available nearby land cell already on the canon-correct
side of the political map. It preserves every coast, relief, forest, river, location
geometry, realm envelope, and broad ownership claim.

| Marker | Exact Ardacraft control | Resolved cell | TA 3018 disposition | Basis |
| --- | --- | --- | --- | --- |
| Frecasburg | `0.461849, 0.539656` | `me_land_0426` | Rohan | *Unfinished Tales*, “Cirion and Eorl” |
| Sarn Gebir | `0.553997, 0.500500` | `me_land_1001` | Rohan | *The Lord of the Rings*, Book II, Ch. 9 |
| Falls of Nimrodel | `0.502610, 0.351896` | `me_land_1568` | Lothlórien | *The Lord of the Rings*, Book II, Ch. 6 |
| Cormallen | `0.592619, 0.580882` | `me_land_0114` | wild Ithilien | *The Lord of the Rings*, Book VI, Ch. 5 |

The result preserves 38 realms, 3,030 assigned land locations, and 2,974 deliberate wild
locations. Cormallen remains an explicit wild witness because Ithilien is depopulated at
the TA 3018 start; it is not a pre-emptive Gondorian expansion. Nearby Parth Galen and
Dimrill Dale remain aliases: all unreserved candidate cells are more than `0.011` from
their source point, so a new marker would be less accurate than the established nearby
landmark context.

`tools/cartography_reference_audit.py` now preserves all seven direct Ardacraft
map-scale point controls, including the earlier Bree-land cluster.

## Runtime verification

The generated world passed final full validation in 541.8 seconds, including the
457.1-second M2 world gate. The paired vanilla/ENDORE real-game smoke passed in 204.1 seconds: both
launches reached the menu-ready state and the comparison found zero new ENDÓRË-unique
error-log lines. `tools/eu5_slot.py assert-smoked` confirms the exact game-visible tree
fingerprint `ff2e0a0876bacdd473ed97af874f9b60e90b23a1f73f3652eabaddd400a5e6da`.
