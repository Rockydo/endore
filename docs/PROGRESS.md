# Progress

## 2026-07-28

- M0 complete locally: governing plans read; installed build 24187685 matches the
  reference environment; autonomous toolchain ported; relocated user directory and
  junction configured; fresh vanilla baseline captured; paired vanilla/mod smoke passed
  with zero mod-only error lines.
- M1 remained the only content priority and blocked all broader content.
- M1 spike attempt 1 reached the menu and isolated river/locator diagnostics. Attempt 2
  removed river errors and proved the mandatory coast-port and engine-generated-locator
  contracts; the bounded failures are recorded in `BLOCKERS.md`.

## 2026-07-29

- M1 Proof of Arda is implemented: a recognizable Middle-earth silhouette with exactly
  300 locations, 30 provinces, 56 ports, a 3018.1.1 start, 3200.1.1 end, and `wrap_x = no`.
- The proof map loaded in the real game, entered live Observer mode, and advanced from
  1 January to 5 January 3018. The evidence pack contains the world-map and live-session
  screenshots.
- A live `test_log` sink probe and a conditional native-immortality assertion both
  emitted parseable results. Native `is_immortal = yes` is proven.
- Geography compatibility, coastline, river, hierarchy, dangling-reference, and locator
  contracts are generator-checked. The M1 overlays are explicitly temporary and are the
  first removal target in M2.
- M1 gate is green: `gmake validate` passed, the paired vanilla/mod smoke reported zero
  mod-only `error.log` lines, screenshots are committed, and a live in-game assertion
  executed. Work may now proceed to M2.
