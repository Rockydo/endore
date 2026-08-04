# v127 frontier gazetteer and control expansion

This M2 map-detail batch adds seven exact ArdaCraft source markers to the generated
Middle-earth gazetteer and the full political-control ledger. It improves player-facing
readability around the Bruinen, Eregion, Lothlórien, upper Anduin, Rohan, and Moria without
altering coastlines, relief, forests, rivers, source claim polygons, or realm roster.

| Source landmark | Final control | Basis |
| --- | --- | --- |
| Ford of Bruinen | RIV | *The Fellowship of the Ring*, Book I, Ch. 12; protected Imladris crossing. |
| Hollin Ridge | WILD | *The Fellowship of the Ring*, Book II, Ch. 3; abandoned Eregion wilderness. |
| Lone-lands | WILD | *The Fellowship of the Ring*, Book I, Ch. 11; unsettled Eriador. |
| Redhorn Pass | MOA | *The Fellowship of the Ring*, Book II, Ch. 3; immediate Moria mountain approach. |
| Egladil | LOR | *The Fellowship of the Ring*, Book II, Ch. 6; the Golden Wood of Lothlórien. |
| East Wall of Rohan | ROH | *Unfinished Tales*, “Cirion and Eorl”; exact Rohirric frontier-side cell. |
| Old Ford | BEO | *The Fellowship of the Ring*, Book I, Ch. 2; Beorning-held upper-Anduin crossing. |

The source coordinates resolve to unique passable cells. Hollin had previously inherited
the nearest Ranger allocation; it is now an explicit wild Eregion cell. No other ownership
or population policy changes are inferred from the new labels.

## Verification

- `gmake validate`: PASS in 460.0 seconds; the complete M2 world gate passed in 387.7
  seconds, including the updated 96-landmark cartography conformance report.
- `gmake smoke`: PASS in 204.9 seconds. Vanilla control and ENDÓRË both reached
  menu-ready with zero mod-unique error-log lines on game-visible fingerprint
  `580fe4052808c55a15601f170154babfbbc9d866f2671ab021103705c94af9c6`.
- `tools/eu5_slot.py assert-smoked`: PASS on that exact tree.
