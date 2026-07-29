# M5 census notes

All figures are gameplay estimates in thousands, not claims that Tolkien supplied a
complete Third Age census. The books provide relative scale, settlement character, named
centres, military impressions, and explicit depopulation far more often than totals.

The binding choices are:

- Gondor begins at 2.0 million, Rohan at 0.5 million, and the Shire at 0.22 million,
  directly within the master plan's declared ranges.
- Mordor begins at 1.5 million, including 0.35 million Mannish forced-labour households
  concentrated at Nurn. `slaves` is used only where bondage is textually or structurally
  supported, never as a generic southern population label.
- The represented on-map portions of Harad, Khand, and Rhûn collectively outnumber
  Gondor. These totals do not claim to represent their vast off-map populations.
- Rivendell contains 0.8 thousand; Fangorn 0.5 thousand; Rhosgobel 0.3 thousand.
  Lórien, the Woodland Realm, and the Dwarven holds remain in the low tens of thousands.
- Every canonical `ruin` rank is empty. Wild non-ruin land receives only a 22-thousand
  world total, ensuring Hollin, Enedwaith, Ithilien, the Brown Lands, and Forodwaith read
  as desolate rather than as ordinary countryside.
- Population-type distributions are abstractions of households and social capacity.
  “Loremasters & Keepers” is the visible name for the engine's `clergy` stratum; it does
  not create churches. “Wild Folk” is the visible name for `tribesmen`.
- The installed build requires 2,086 inherited culture symbols to retain a population.
  Their distributed size `0.01` presences are parser ABI only, excluded from every
  authored total, and always subordinate to the local Middle-earth population. They are
  assigned after census allocation to the 2,086 largest custom-dominant locations, each
  with at least 1.0 thousand authored inhabitants; low-population hosts proved unreliable
  during fresh bookmark initialization.
- M5 uses only timeless installed raw goods and modest generic workshops. Bespoke
  pipeweed, mithril, athelas, mûmakil logistics, final prices, demand, and signature
  buildings belong to M9; final armies and units belong to M7.
- The route ledger validates 302 adjacent land edges across nine canonical corridors.
  Runtime roads remain empty because the installed renderer requires matching
  Arda-native strips in `spline_network.splnet`; retaining Earth strips or accepting one
  missing-strip diagnostic per edge is forbidden. `condition` records lore state for the
  later upgrade/decay pass once a native spline writer exists.
