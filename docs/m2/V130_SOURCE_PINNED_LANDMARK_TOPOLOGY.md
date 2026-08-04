# v130 source-pinned landmarks without false political fragments

This M2 batch adds nine player-facing, source-pinned landmarks only where the existing
6,004-location tessellation can represent them without inventing a border. It does not
alter coasts, relief, forests, rivers, location geometry, realm roster, or broad claim
envelopes.

## Exact source controls

| Landmark | Arda Maps feature | ENDÓRË normalized coordinate | TA 3018 disposition |
| --- | --- | --- | --- |
| Trollshaws | `point_place: TomBertWilliam` | `0.462368, 0.227164` | wild Eriador |
| Morgul Vale | `point_place: MorgulVale` | `0.599871, 0.596929` | Mordor-held Minas Morgul approach |
| Thrihyrne | `point_mount: Thrihyrne` | `0.468165, 0.507581` | Rohan |
| Dol Baran | `point_mount: DolBaran` | `0.466451, 0.487359` | Rohan |
| Ras Morthil | `point_mount: RasMorthil` | `0.370767, 0.664296` | Gondor |
| Ravenhill | `point_mount: Ravenhill` | `0.602239, 0.151826` | Erebor |
| Ethring | `point_ford: Ethring` | `0.532735, 0.628708` | Gondor |
| White Towers | `point_castletower: WhiteTowers` | `0.320639, 0.234862` | wild Elvish monument |
| Last Bridge | `point_bridge: LastBridge` | `0.458353, 0.224332` | wild Eriador crossing |

`tools/cartography_reference_audit.py` freezes the exact transformed coordinates and
feature types against the owner-approved Arda Maps cache. Raw source material remains in
the runtime quarantine; the repository stores only transformed controls and provenance.

## Topology decisions

Bombadil's House remains a source-derived orientation reference rather than a separate
location. Its exact point resolves into the same small local tessellation neighbourhood
as Brandywine Bridge. Giving that cell to Breeland creates a false detached Breeland
island; giving it to wilderness cuts the real bridge into a false island. The independent
refuge therefore stays represented by the nearby Old Forest context without a fabricated
cadastral cell.

Ravenhill belongs to Erebor after the War of Five Armies. The compact source contour now
includes only Ravenhill and its immediately adjacent southern Lonely Mountain spur. This
removes the artificial one-cell Dale enclave while retaining a bounded `0.585–0.614` by
`0.118–0.160` Erebor silhouette rather than expanding it into the Dale vale.

Morgul Vale is explicitly Mordor-held. Its single witness cell is separated from the
Mordor basin by the source-shaped Ephel Duath impassable enclosure, so its exact member
set is documented as a reviewed physical split. This is not permission to colour the
surrounding Ithilien wilderness.

## Static result

After regeneration, `tools/m3_realms.py --check` passes with 38 realms, 3,027 assigned
land cells, and 2,977 deliberately wild cells.

## Repository and runtime verification

- Final `gmake validate`: PASS in 541.0 seconds, including the complete 464.9-second `m2_world`
  gate, source-coordinate audit, terrain-cache/rivers checks, ownership topology, people,
  census, templates, and lint.
- `gmake smoke`: PASS in 202.2 seconds. Paired vanilla and ENDÓRË launches both reached
  menu-ready through the shared EU5 lease; ENDÓRË added zero new error-log lines.
- `tools/eu5_slot.py assert-smoked`: PASS for current game-visible fingerprint
  `53c79256d565726bd643d77d2b95bd2e027f0dc4f10476ec7f24d8d5f5361bdd`.
