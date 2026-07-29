# Decisions

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
