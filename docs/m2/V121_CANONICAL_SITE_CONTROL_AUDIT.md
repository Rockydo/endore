# v121 canonical-site control audit

## Purpose

This M2 political-fidelity pass locks exact, canon-clear TA 3018 sites that were already
correctly allocated by the current map. It does not move a general frontier, change a
coast, alter terrain or rivers, add a realm, or turn unclaimed land into a state. The
contracts are location-level witnesses: a future reseed or allocator change must fail
instead of silently displacing a named site.

## Locked site witnesses

| Theatre | Required owner | Exact sites | Basis |
| --- | --- | --- | --- |
| Fangorn / Anduin Vale | Fangorn, Beornings | Wellinghall; Beorn's Hall | *The Two Towers*, Book III Ch. 4; *The Hobbit*, Ch. 7. |
| Lothlórien / northern Mirkwood | Lothlórien, Woodland Realm | Cerin Amroth; Mountains of Mirkwood | *The Fellowship of the Ring*, Book II Ch. 6; *The Lord of the Rings* map. |
| Inner Mordor | Mordor | Udûn; Gorgoroth; Nurn; Lithlad | *The Lord of the Rings* map; Book IV Chs. 2–3. |
| Southern Gondor | Gondor | Tolfalas; Pinnath Gelin; Lamedon; Lossarnach; Tarlang's Neck | *The Return of the King*, Book V Ch. 1; *The Lord of the Rings* map. |
| Gondor beacon chain | Gondor | Amon Dîn; Eilenach; Erelas; Min-Rimmon; Calenhad; Amon Anwar | *The Return of the King*, Book V Ch. 1; Appendix A. Nardol was already locked in v118. |
| Rohirric White Mountains | Rohan | Glittering Caves; Paths of the Dead; Irensaga; Dwimorberg; Starkhorn | *The Two Towers*, Book III Ch. 8; *The Return of the King*, Book V Chs. 2–3. |

These sites were all already allocated to the listed owners. This batch records their
existing correct result as a deterministic assertion, rather than fabricating a new
political shape. The old unclaimed-site contracts remain intact: the Dead Marshes,
Dagorlad, outer Ithilien, Grey Mountain ruins, Eagles' Eyrie, and the exact Black Gate and
Shelob pass cells stay `WILD`.

## Mechanism

`FRONTIER_LANDMARK_REQUIRED_OWNERS` now applies and validates the witness owner after
normal allocation. The ownership audit records `accepted_required_frontier_owner` and
includes the exact rationale. All positive contracts must still satisfy their realm's
source-zone, source-polygon, or source-side envelope, so a site witness cannot punch
through the accepted physical claim boundary.
