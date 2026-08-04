# v123 active settlement control audit

Every non-ruined entry in `docs/world/control/settlements.csv` is now an exact TA 3018
ownership witness. The contract derives its required realm from the source-controlled
realm hint, with Dol Amroth correctly mapped to its separate starting realm. It covers 39
active named sites across Lindon, the Shire, Bree-land, Imladris, the mountain holds,
Wilderland, Rohan, Gondor, Mordor, and Umbar.

The three explicit Arnor ruins (Annúminas, Fornost, and Amon Sûl) are intentionally
excluded and remain wild. This audit moves no current location or boundary; it makes a
future allocator fail if an active canonical settlement drifts from its documented owner.
