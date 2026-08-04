# v113 cartographic-source provenance re-audit

## Scope

This audit rechecked the exact source bytes behind the reopened M2 map rather
than relying on an old download or a visual resemblance. It does not copy,
redistribute, or ship any source artwork. The existing G:-drive research cache
remains outside the repository; ENDÓRË ships only its original transformed
controls and generated map data.

## Results — 2026-08-04

| Source control | Upstream location | SHA-256 | Result |
|---|---|---|---|
| Arda Maps Third Age topology | `kwoxer/Arda-Maps`, `htdocs/maps/arda_third_age.json` | `147a2d0ff3e36e2b675afb40dd4a74f634006bc6350a6a7c31639019fd2bd4ab` | Exact cache match |
| ArdaCraft Heightmap V2 | `cdn.ardacraft.me/Heightmap-layer-Middle-earth-V2.webp` | `a1b05874cd447b9868c0d56a4fad523e5fc94053fa239dc5df7e0b31068144be` | Exact cache match |
| ArdaCraft Drainage V2 | `cdn.ardacraft.me/Drainage-layer-Middle-earth-V2.webp` | `d8ec6f22c0e3c87097145f2c3f3b831c778e4df8b705595d335e5c4d7be74871` | Exact cache match |
| ArdaCraft Biome V3 | `cdn.ardacraft.me/Biome-layer-Middle-earth-V3.json` | `2070d5577d768b2d418fd06e61d2fbafb5b55599340540fd9308ead213037997` | Exact cache match |
| ArdaCraft paths | `cdn.ardacraft.me/arda_paths.json` | `bf23a5781b2034b4ddcf45ca551d878469f39e99b4d8f48e9ad30249b905508f` | Exact cache match |

The current Arda Maps hosted interactive route falls back to its HTML shell for
direct JSON requests, but its published open-source repository supplies the
same named Third Age topology that ENDÓRË has hash-pinned. The complete
ArdaCraft CDN assets were fetched directly and each matched the cache.

## Political interpretation boundary

These two sources are authoritative here for geography, landmarks, terrain,
drainage, forest envelopes, and the equal-scale placement frame. Their Third
Age geographic data does not provide a surveyed TA 3018 sovereignty polygon
for every playable realm. Therefore it cannot be used to justify filling gaps
with speculative political land. Existing hard realm contracts may be revised
only where Tolkien evidence, a named strategic anchor, or an explicit physical
frontier supports the change; otherwise land remains deliberately wild.

## Consequence

No coast, mountain, forest, biome, river, settlement coordinate, or political
cell changed in v113. The re-audit confirms that the current detailed physical
map is derived from the precise owner-approved source revisions, not a stale or
approximate substitute. Continue the political review against this frozen
baseline.
