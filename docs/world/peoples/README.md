# Peoples source ledgers

This directory is the authored source of truth for M4 peoples, languages, faiths, and
realm/region profiles.

- `cultures.csv` defines 33 cultures in 10 culture groups.
- `language_families.csv` maps eight semantic Middle-earth language families onto the
  installed engine-family adapters required by this EU5 build.
- `languages.csv` defines 10 language roots and 33 culture dialects.
- `faiths.csv` defines 10 faiths in three gameplay groups.
- `name_pools.json` records canon seeds and explicitly constructed name components.
- `realm_profiles.csv` and `region_profiles.csv` drive deterministic placement.

`tools/m4_peoples.py` compiles these ledgers into game definitions, localization, and
`docs/world/derived/m4_people_assignments.csv`. Generated files must not be hand-edited;
change a source ledger and regenerate the world instead.
