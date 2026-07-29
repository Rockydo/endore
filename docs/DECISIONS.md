# Decisions

## 2026-07-29 — M5 census slice and road-source contract

Treat the authored nine-route ledger and its 302 adjacent land edges as source data, not
as permission to install a runtime road graph. EU5 requires a matching Arda-native strip
inside `spline_network.splnet` for every starting road edge. The two bounded map-editor
attempts could not produce that binary, and the installed Earth cache may not survive.
Therefore M5 emits an explicitly empty `road_network` while continuing to validate every
route waypoint and edge. Markets, settlements, development, census, raw materials, town
setups, and provisional pre-M7 armies remain independently shippable.

The M5 demographic total is 9.029 million for the represented map extent. This is a
gameplay census, not an assertion that Tolkien supplied numerical totals. Installed
culture presences remain parser ABI only and are excluded from all authored totals.

## 2026-07-29 — Physical-map gate precedence

Treat political-shape screenshots as insufficient evidence for any custom-map milestone.
M1/M2 is green only when the same authored coordinates agree across the political raster,
16-bit height source, complete virtual terrain cache, and close physical renderer. The
owner's close-zoom report superseded the earlier gate immediately; unfinished M3 realm
work was isolated until the physical world was corrected.

Use the installed raw-height waterline as an enforced generator contract. Keep every
authored water sample below it and every ordinary land sample safely above it after river
incision. Own the complete terrain cache and suppress every installed Earth-authored
generated/static transform definition through deterministic exact-file overlays.

## 2026-07-29 — Later generated-art reference direction

For every later generated bitmap family, use precise real EU5 assets as the primary style
and format references and actual images from Peter Jackson's three *Lord of the Rings*
films as additional art-direction references. Film material guides mood, production
design, costume, landscape, and lighting only; Tolkien canon remains authoritative for
content. Reference images stay in a gitignored G:-drive cache and are not redistributed.
Icons are generated four distinct designs per sheet, split locally, and individually QA'd.

## 2026-07-29 — M3 political contract

Ship 38 first-class realm tags in the first political partition. Fold Minas Morgul into
Mordor as a fortress-location rather than a separate country; use the plan's micro-tag
allowance for Qarsad of Harad and a third Rhûnic confederation so the sparse South and
East have playable texture.

Political ownership is generated only for passable-land locations. Sea zones, lakes, and
impassable mountains are always unowned, and selected desolations remain deliberately
wild. The M3 validator projects the exact realm lookup onto the authored elevation control
and fails if any owned pixel lies at or below the installed waterline, if any non-land
location receives an owner, or if a capital snaps materially away from its authored seat.
This makes the owner's reported “labels/colors in the ocean” failure mechanically
non-regressible.

Keep the installed monarchy, culture, faith, and demographic registries only as
parser-safe technical bridges. M4 replaces culture and faith, M5 replaces the census, and
M6 replaces government titles and rulers; none of those visible placeholders is accepted
as final Middle-earth content.

## 2026-07-29 — M2 deep-load quarantine

Keep the M2 inherited-content quarantine exact, generated, and milestone-scoped. The
production world retains one installed technical country only to satisfy the setup
contract. Installed cultures and religions receive a tiny technical census so their
retained registries validate; Earth country setup, unsafe hardcoded on-actions, flag
predicates, historical schedules, and unreferenced Earth-only static modifiers are
neutralized by deterministic exact-file overlays.

Guard retail building `market` scopes during the neutral world's first tick and disable
Earth dynasty comparisons where the corresponding historical database is deliberately
absent. These are parser/runtime isolation measures, not ENDÓRË content. M3 and later
replace the scaffolds as bespoke databases become authoritative.

## 2026-07-28 — Workspace path precedence

The explicit task path `G:\EUV mods\endore` supersedes the older `G:\endore` path embedded
inside the master plan. Runtime user data remains at `G:\endore_user_data`.

## 2026-07-28 — Installed DLC playset

Use the same four installed content entries as the proven ANTIQVITAS environment:
`D000_shared`, `D008_fate_of_the_phoenix`, `D015_ancient_monuments_pack`, and
`D017_sacred_sites_pack`. This maximizes reproducibility on this machine and preserves
the monuments framework for later Middle-earth landmarks.

## 2026-07-28 — Bootstrap thumbnail

Use a temporary 512×512 recomposition of the installed EU5 paper-map table texture for the
M0 metadata contract. It is explicitly tracked for replacement through the reference-driven
art pipeline before M11 and is not treated as bespoke final art.

## 2026-07-29 — M1 proof-world scope

Use exactly 300 installed location identities and colors on a new Middle-earth-shaped
geometry: 50 sea, 190 plains, 10 lakes, 20 impassable mountains, and 30 forests. Group
them into 30 temporary provinces and one temporary owned realm using the installed `SWE`
identity solely to satisfy the start contract. These are engineering scaffolds, not world
content; M2 replaces the hierarchy and M3 replaces ownership.

The accepted proof canvas is 16384×8192 because it matches the installed renderer contract
and remained stable at roughly 5–6 GB. M2 will still study and target the plan's 8192×4096
production canvas before committing the final projection.

## 2026-07-29 — Temporary geography compatibility overlays

Generate token-level overlays for retained retail scripts that name removed Earth
geography. They preserve the engine definitions required to reach a playable 300-location
world while redirecting only geography symbols to the proof hierarchy. Every file is
marked as M1-only, generated from the read-only install, and listed in a manifest. M2 must
remove the entire layer during its quarantine sweep; none of these overlays are final
Middle-earth content.

## 2026-07-29 — Locator source of truth

Use the automated engine command `MapObjects.GenerateGameLocators <type>` to establish
eligibility, then encode the resulting rule in the generator. Combat and unit-stack
locators cover all live locations except impassable mountains (280 of 300); deterministic
member-cell positions are valid and avoid any manual map-editor step.

## 2026-07-29 — M2 projection and hierarchy split

Use an original 2:1 normalized projection covering Lindon to western Rhûn and Forochel to
northern Far Harad. It is authored from textual relative geography and travel logic, not
traced from a published map. The production location canvas is 8192×4096, with 1024×512
committed controls and a 4096×2048 terrain heightmap target.

Use six top-level strategic geography groups in the production hierarchy: Eriador,
Forodwaith, Rhovanion, Gondor, Mordor-and-Rhûn, and Harad. Rohan belongs to Rhovanion
because its strategic ties and movement corridors run through the Gap of Rohan and Anduin
system; Gondor remains a distinct group for useful map-mode scale. Mordor and western Rhûn
share a top-level group because each is too narrow for balanced UI regions alone and their
eastward strategic theatre is tightly linked.

## 2026-07-29 — M2 production location model

Generate 5,812 deterministic locations from the authored controls: 5,200 passable land,
260 impassable mountains, 32 lakes, and 320 sea zones. The density-weighted seed model
pins all 41 cited settlement anchors and uses a minimum control-cell area of eight. This
stays within the plan's intended land-location range while leaving explicit tactical
classes for mountain barriers and inland water.

Follow the installed parser's six-level hierarchy contract rather than the plan's
five-name shorthand: continent, subcontinent, region, area, province, location. ENDÓRË
uses six continents, six corresponding subcontinents, and 24 authored strategic regions.

## 2026-07-29 — M2 inherited-reference compatibility

Retain the installed named-location color registry as unpainted definitions and allocate
all ENDÓRË colors from a disjoint set. This is not retained Earth content: it is a parser
compatibility measure for inherited files that still resolve location tokens during the
quarantine phase. No installed location occupies a pixel in the production world.

The generated M2 quarantine overlays replace the M1 proof overlays and redirect remaining
installed geography references to one valid Middle-earth hierarchy path. They are exact,
marked, deterministic source transformations and remain milestone-scoped scaffolding to
be deleted as inherited Earth scripts are retired.

## 2026-07-29 — M2 setup placeholders

Use installed `catholic`, `swedish`, and `wheat` values as explicit temporary parser-safe
religion, culture, and raw-material defaults for the 5,200 passable locations. Real-game
evidence requires a raw material on every passable land location. These values make no
lore claim and M4–M5 must replace them completely with bespoke Middle-earth systems.

## 2026-07-29 — M2 ports and authored crossings

Restrict naval ports to sea zones. Esgaroth is deliberately represented as a lakeshore
settlement without a naval-port edge because the installed dock validator rejects lake
endpoints.

Ship M2 with the proven zero-byte `adjacencies.csv` fallback. Two bounded A/B attempts
showed that any non-empty file on the custom canvas causes an empty-location lookup even
when its rows are valid. Keep the intended Himling and Tolfalas crossings in generator
source, but do not activate them until a later editor-backed contract is proven.

## 2026-07-29 — M4 people model

Model the playable world with 33 cultures in 10 broad culture groups. Rangers remain a
social and military identity inside the Dúnedain rather than a separate ethnicity.
Trolls remain units or special populations rather than a first-class culture. Orcs are
split by sustained regional communities where gameplay and lore support the distinction.

The installed engine rejects arbitrary language-family keys, so eight semantic
Middle-earth families map onto fixed installed family adapters whose visible names are
fully relocalized. Ten language roots and 33 culture dialects drive name pools. Major
roots target at least 60 male, 40 female, and 30 house names; minor roots target
30/20/15. The generated localization contains 1,105 name entries.

Model spiritual allegiance with 10 faiths in three gameplay groups: Light, Shadow, and
Old Ways. These are not organized-church claims. Every inherited religion file is
exact-overlaid with `enable = 3200.1.2`, keeping its parser symbol available while making
it unavailable throughout the ENDÓRË campaign.

## 2026-07-29 — M4 installed culture ABI

Installed culture keys behave as a compile-time ABI in this build: removing or disabling
them produces widespread invalid-key failures. Keep one distributed size `0.01`
compatibility presence per custom-dominant land location while assigning all visible
dominant populations and realm primaries to authored Middle-earth cultures. These ABI
presences never dominate and make no worldbuilding claim.

A size `0.001` experiment is rejected because the engine rounded it away and reported
2,086 cultures without populations. The narrow Sinicization compatibility overlay keeps
the installed script structure and variable reads intact while replacing only its
country-base lookup with zero, preventing a selection-screen type error.
