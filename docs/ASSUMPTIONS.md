# Assumptions

No lore assumptions were made in M1. The proof realm, installed location identities, and
all Earth-named compatibility keys are temporary engineering scaffolds rather than claims
about Middle-earth.

## M2 map controls

- † The exact 8192×4096 normalized coordinates of coastlines, ridges, rivers, lakes, and
  all 41 settlement anchors are gameplay extrapolations from relative placement in the
  cited chapters and the books' schematic map. They preserve canonical ordering and major
  travel corridors but do not claim survey accuracy.
- † The production extent clips deep Rhûn and deep Harad at the eastern and southern
  borders while retaining western Rhûn and a northern Far Harad fringe, providing useful
  playable margins where canon is sparse.
- † Rohan is grouped under Rhovanion for strategic map hierarchy, while Gondor forms its
  own top-level geography. This is a UI and gameplay classification, not an in-world claim.
- † The 41 canon anchors retain their cited names, but all generated fill locations use
  deterministic engineering keys and generic display names. M3 replaces those names with
  a curated gazetteer before any realm is considered first-class.
- † Terrain relief and the flat-map texture are generator-v1 representations intended to
  prove navigability, barriers, and map readability. Their authored ridge/pass alignment
  is binding for gameplay, but their surface detail is not final visual art.
- † Passable locations temporarily use installed culture, religion, and raw-material
  defaults solely because the setup validator requires populated fields. They are not
  claims about the peoples, faiths, or economy of Middle-earth.

## M3 realms and gazetteer

- † Political borders are deterministic strategic extrapolations from the canon anchors,
  mountain barriers, river corridors, and the plan's realm roster. Sparse Forodwaith,
  Enedwaith, the Brown Lands, and emptied Ithilien retain deliberately wild land rather
  than being painted into the nearest realm.
- † The exact seats named The Angle, Halls of Ered Luin, Woodmen's Hall, Ghân's Glade,
  Forochel Camp, Harnenhold, Qarsad, Mûmak Gate, Khazân, Burh Gath, Wainhold, Eastern
  March, and Dunland Moot are gameplay seats invented where binding canon supplies no
  administrative capital. Each remains individually marked in the control ledger.
- † Harnendor, Qarsad of Harad, the western Kingdom of Rhûn, Karmach, and the Sagath
  March are on-map political extrapolations used to make the canon-sparse South and East
  playable without pretending to define all off-map Harad or Rhûn.
- † Generated fill names use documented regional phonotactic impressions and ordinary
  English compounds. They are deterministic Tolkien-register inventions, not claims to
  reconstruct Sindarin, Khuzdul, Black Speech, or any unattested Mannish language.
- † Realm colors and first-pass arms are readability scaffolds. The arms reuse generic
  installed heraldic components as permitted by the M3 gate; M11 replaces them through
  the reference-driven bespoke-art pipeline.

## M4 peoples, languages, and faiths

- Eriadoran is a deliberate gameplay umbrella for the remaining settled Middle Men of
  Eriador; it does not imply a single historical polity or self-identity.
- Karmachi and Sagath identities are documented inventions for canon-sparse eastern
  populations attached to the already logged gameplay realms.
- Constructed name components are Tolkien-register tools, not linguistic reconstructions
  of unattested Sindarin, Khuzdul, Black Speech, or Mannish forms.
- The spiritual “Ways” are gameplay adapters for outlook, allegiance, and custom. They do
  not imply organized churches, universal creeds, or modern religious institutions.
- Entish Memory of the First Music is a gameplay representation of the Ents' remembered
  place in creation, not an assertion of formal Entish worship.
- Firebeards and Broadbeams share one culture; Lake-folk are folded into Dalish culture;
  and Galadhrim remain distinct from other Silvan communities for playable regional
  identity.
- M4 assigns a dominant people and faith profile to each land location. It is not the
  final M5 census: minorities, depopulated ruins, settlement types, and exact population
  weights remain M5 work.

## M5 census and opening economy

- † The represented world begins with 9.029 million people. Gondor has 2.0 million,
  Rohan 0.5 million, the Shire 0.22 million, and Mordor 1.5 million including 0.35
  million Mannish thralls in Nurn; exact totals and social shares are gameplay estimates
  bounded by the master plan and the books' relative military and settlement evidence.
- † On-map Harad, Khand, and Rhûn collectively exceed Gondor in population without
  claiming to represent their much larger off-map peoples. Sparse wild non-ruin land has
  only 22 thousand inhabitants in total, while all 21 canonical ruins begin empty.
- † Twelve opening markets, 58 urban or fortified settlement seeds, regional development
  values, and raw-material placement extrapolate exchange corridors, terrain, and named
  centres into EU5's economic model. They are balance inputs rather than canonical
  administrative statistics.
- † Starting armies use one provisional installed foot-unit type and scale only by broad
  population bands. They establish a loadable M5 economy and do not pre-empt M7's
  canonical unit rosters or final military balance.

## Reopened M2 physical production

- â€  The control atlas now contains 42 stable anchors. Fields of Nurn represents the
  canon-described slave-worked farmlands by NÃºrnen; its exact coordinate and town rank
  are gameplay extrapolations. The anchor prevents Mordor's 350k Mannish field population
  from depending on an unstable generated location key.
- â€  Coast, lake, forest, ridge, valley, and tributary micro-geometry is deterministic
  cartographic interpretation beneath the cited macro ordering, not survey accuracy.
- â€  Umbarite remains Umbar's broad primary culture, while the surviving Black
  Númenórean houses are an accepted culture represented disproportionately among its
  nobles. This is a gameplay interpretation of Umbar's Númenórean lineage and later
  mixed population, not a canonical demographic statistic.

## Reopened M2 source-audited cartography

- † The old statement that all physical coordinates were broad gameplay
  extrapolations is superseded. Large- and medium-scale positions now follow
  the equal-scale ArdaCraft grid and Arda Maps continuous linework under
  `docs/world/CARTOGRAPHY_REFERENCE_LEDGER.md`.
- † Where the two community references differ locally, a point marker uses
  ArdaCraft while coast, river, forest, lake, and mountain linework uses Arda
  Maps. Tolkien's published evidence remains superior to either
  interpretation.
- † Khazad-dûm is placed between the source controls for the Doors of Durin
  and Dimrill Dale. Fields of Nurn uses the centre of the mapped Nurn area,
  Dorwinion uses its mapped area-label centre, and Pelennor lies immediately
  east of Minas Tirith; these are strategic anchor choices rather than claims
  of surveyed city coordinates.
- † The 2:1 EU5 canvas does not horizontally stretch the approximately
  1.1:1 represented source extent. Extra width is honest ocean and eastern
  margin, preserving relative distances and the recognizable proportions of
  Middle-earth.
- † Twelve of the 62 secondary landmark controls remain reconciled or
  gameplay judgments because binding canon does not provide surveyed points:
  the Angle, the composite surviving Blue Mountain halls, the Woodmen's seat,
  the Lossoth camp, three invented Harad seats, three invented Rhûnic seats,
  the Dunland moot, Mount Gram, and the paired Towers of the Teeth. Their
  exact coordinates and cartographic rationale are recorded row-by-row in
  `m3_landmarks.csv`; the Arda Maps/ArdaCraft references constrain the
  surrounding geography.
- † The three invented Rhûnic seats use the represented land around the source
  Rhûn and Sea of Rhûn labels, at x=0.77/0.80/0.82. The previous x=0.875
  Eastern March point was outside the source mainland and is rejected.
- † The Mount Gundabad location represents its usable gate/approach as well as
  the underground stronghold. A narrow pass centred on the canonical marker is
  therefore necessary for gameplay connectivity and does not imply a broad
  break in the surrounding mountains.
- † The Harlond below Minas Tirith is an operational Gondorian port on
  TA 3018.1.1. It remains owned even while most nearby Ithilien locations are
  deliberately wilderness; the wilderness mask cannot override its port rank.
- † Forochel Camp is an invented seasonal Lossoth seat, not a canonical capital. Its
  earlier x=0.340000/y=0.035000 control lay offshore and became unstable when political
  tessellation was reduced. The retained x=0.341880/y=0.065462 point is the nearest
  playable shore on the unchanged source-pinned Forochel coastline.
- † Arda Maps supplies named source polylines for 22 of the 24 production
  river controls. Its unnamed `line_river` geometry 8 is the only substantial
  channel in the Harnen corridor and is used for that river's detailed upper
  and middle course; only its short final reach to the coast is reconciled
  against the owner-approved macro map. Unnamed geometry 14 occupies the exact
  Morgulduin corridor and supplies that channel from the Morgul Vale to its
  Anduin confluence. These identifications are cartographic reconciliations,
  not claims that the source itself labels either river.
