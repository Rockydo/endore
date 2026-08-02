#!/usr/bin/env python3
"""Bake/check ENDÓRË's self-contained EU5 terrain virtual-texture cache.

Installed-game evidence shows that the four ``terrain_cache/*.bin`` payloads
are concatenated 132x132 PNG tiles.  Their companion ``.info`` files index a
complete 128-pixel-tile mip pyramid over a 65536x32768 virtual surface.

The retail cache contains Earth's decal-baked relief and material paint.
Letting those paths fall through the VFS therefore leaks Earth back into a
custom map at close zoom.  This generator owns the complete cache contract:

* ``heightmap`` is sampled from ENDÓRË's authored 16-bit height source;
* ``materials`` is an Arda-native 16-bit material-channel mask derived from
  the continuous biome, elevation, coastline, and river controls;
* ``index_map`` and ``intensity_map`` contain no decal references;
* ``quadtree_nodes`` is the engine's geometry-independent full zero tree.

No installed-game payload is copied.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import io
import json
import math
import re
import struct
import sys
import time
import zlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_rivers import river_control_points
from m2_controls import (
    land_mask,
    natural_path,
    source_relief_field,
    source_zone_mask,
)
from worldgen import CONTROL, DERIVED, TERRAIN_OUT

ROOT = Path(__file__).resolve().parents[1]
CACHE_OUT = TERRAIN_OUT / "terrain_cache"
HEIGHT_SOURCE = TERRAIN_OUT / "heightmap.png"
BIOME_CONTROL = CONTROL / "biomes.png"
PROJECTION_CONTROL = CONTROL / "projection.json"
MATERIAL_PREVIEW_OUT = DERIVED / "terrain_material_preview.png"
MANIFEST_OUT = CACHE_OUT / "endore_terrain_cache_manifest.json"
MATERIAL_DEFINITIONS = TERRAIN_OUT / "materials.txt"

SOURCE_W = 65_536
SOURCE_H = 32_768
MATERIAL_W = 8_192
MATERIAL_H = 4_096
TILE_SIZE = 128
BORDER_SIZE = 2
STORED_TILE_SIZE = TILE_SIZE + BORDER_SIZE * 2
# q64 retains 0.098% of the 16-bit range per step—eight times finer than the
# live-proven q512 cache—while avoiding the 700 MB q1 payload that pushes the
# vanilla-count world past this machine's reliable 98%-load memory envelope.
HEIGHT_QUANTUM = 64
GENERATOR_VERSION = 47
# v34-v35 change height payload semantics by adding and thresholding
# native-cache sculpting. v37 replaces the broad high body with a lower body
# plus native-cache summits; v38 de-duplicates Erebor at runtime-cache scale;
# v39 makes both extremes of the global relief field eligible for summit teeth
# and removes Erebor's clipped ceiling. v40-v41 change material eligibility and
# face thresholds only, so their height payload is exactly compatible with v39.
# v42 adds native-cache longitudinal serration to the two source-pinned Mordor
# walls, so no older height payload is compatible with this generator. v43
# changes river-material semantics only. The rejected v44/v45 climate probes
# never survived in source. v46 changes the custom palette and material mask
# only, so it may reuse a verified v42/v43 height payload.
HEIGHT_FORMAT_COMPATIBLE_VERSIONS = frozenset({42, 43, 46, 47})

# Vanilla's 8192x4096 heightmap is only its coarse terrain source. Its shipped
# virtual-texture cache contains a separately sculpted 65536x32768 surface:
# equal-area cache probes around Shey measure roughly three times the native
# gradient and tens of thousands of distinct levels compared with a bilinear
# enlargement. ENDÓRË must provide the same scale of renderer input or even
# correctly placed high ranges collapse into broad plateaus at close zoom.
# These global-coordinate octaves add no new horizontal mountain footprint;
# they are multiplied by relief already present in the audited height source.
MICRORELIEF_OCTAVES = (
    (384.0, 1.00, 771),
    (192.0, 0.70, 991),
    (96.0, 0.55, 1_217),
    (48.0, 0.40, 1_439),
    (24.0, 0.26, 1_699),
    (12.0, 0.15, 1_877),
    (6.0, 0.08, 2_093),
)
MICRORELIEF_WEIGHT_NORM = math.sqrt(
    sum(weight * weight for _, weight, _ in MICRORELIEF_OCTAVES)
)

# The runtime cache is eight times finer than the authored height source.  The
# two paths below are looked up by key from the hash-pinned projection control,
# so this stage changes only vertical crest morphology and can never drift from
# the horizontal source geometry.  They form the canonical northern and
# western walls of Mordor and meet at the low Cirith Gorgor/Morannon saddle.
MORDOR_RUNTIME_WALL_PHASES = (
    ("ephel_duath", 0.37),
    ("ered_lithui", 1.81),
)
MORANNON_RUNTIME_CENTER = (0.609732, 0.529449)

# Installed materials.txt establishes the native mask-channel meanings.  The
# cache stores a bitset rather than a material index: several bits may be set
# where the renderer should blend a transition. ENDÓRË's unique all-land
# rendering biome gives channels 10-15 stable semantic meanings while
# location-scoped gameplay topography remains independent.
MATERIAL_FLAT_COAST = np.uint16(1 << 0)
MATERIAL_HILL_COAST = np.uint16(1 << 1)
MATERIAL_PLATEAU_COAST = np.uint16(1 << 2)
MATERIAL_MOUNTAIN_COAST = np.uint16(1 << 3)
MATERIAL_WETLAND_COAST = np.uint16(1 << 4)
MATERIAL_COAST_TRANSITION = np.uint16(1 << 5)
MATERIAL_RIVER = np.uint16(1 << 6)
MATERIAL_WATER_TRANSITION = np.uint16(1 << 7)
# v44/v45 proved that encoding climate by mixing the six terrain-variation
# channels creates green/pale islands or huge rock blotches. The single
# continuous ENDORË biome instead gives its otherwise-unused transition slots
# dedicated installed-material identities, preserving seamless raster edges.
MATERIAL_TUNDRA = np.uint16(1 << 8)
MATERIAL_STEPPE = np.uint16(1 << 9)
MATERIAL_GRASS = np.uint16(1 << 10)
MATERIAL_EARTH = np.uint16(1 << 11)
MATERIAL_DARK_ROCK = np.uint16(1 << 12)
MATERIAL_ROCK = np.uint16(1 << 13)
MATERIAL_SNOW = np.uint16(1 << 14)
MATERIAL_SAND = np.uint16(1 << 15)

# Physical tributaries cannot enter build 24187685's rejected custom affluent
# graph, but their exact Arda Maps courses still need to read as drainage in
# the native terrain material. Keep independently serialized engine rivers at
# the accepted narrow-bank calibration; widen only source-classed physical
# feeders, well below the rejected former 1.45x blanket.
TERRAIN_ONLY_RIVER_VISIBILITY = {
    "named_trunk": (0.82, 4),
    "named_branch": (0.82, 4),
    "named_tributary": (0.82, 4),
    "unnamed_trunk": (0.72, 3),
    "unnamed_branch": (0.72, 3),
    "unnamed_feeder": (0.72, 3),
}
MATERIAL_VARIATIONS = np.asarray(
    [
        MATERIAL_GRASS,
        MATERIAL_EARTH,
        MATERIAL_DARK_ROCK,
        MATERIAL_ROCK,
        MATERIAL_SNOW,
        MATERIAL_SAND,
    ],
    dtype=np.uint16,
)

# quadtree_nodes.bin is a full 12-level geometry-independent quadtree.  The
# installed file's 20-byte header describes 5,592,405 zeroed 12-byte records.
QUADTREE_DEPTH = 12
QUADTREE_RECORDS = 5_592_405
QUADTREE_LEAF_OFFSET = 1_398_101
QUADTREE_FLAGS = 33
QUADTREE_DIMENSIONS = 65_537
QUADTREE_HEADER_SIZE = 20
QUADTREE_RECORD_SIZE = 12

INFO_HEADER = (
    f"source_resolution={{ {SOURCE_W} {SOURCE_H} }}\n"
    f"tile_size={TILE_SIZE}\n"
    f"border_size={BORDER_SIZE}\n"
)
SCALAR_INFO_FIELDS = (
    "num_channels=1\n"
    "bytes_per_channel=2\n"
    "empty_value={ 0 0 0 0 }\n"
    "raw=no\n"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def material_source_hashes() -> dict[str, str]:
    return {
        str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
        for path in (
            HEIGHT_SOURCE,
            BIOME_CONTROL,
            PROJECTION_CONTROL,
            MATERIAL_DEFINITIONS,
        )
    }


def pyramid_layout() -> list[tuple[int, int, int]]:
    """Return the engine's finest-to-coarsest mip groups."""
    fine_to_coarse: list[tuple[int, int, int]] = []
    mip = 0
    tiles_x = math.ceil(SOURCE_W / TILE_SIZE)
    tiles_y = math.ceil(SOURCE_H / TILE_SIZE)
    while True:
        fine_to_coarse.append((mip, tiles_x, tiles_y))
        if tiles_x == 1 and tiles_y == 1:
            return fine_to_coarse
        tiles_x = max(1, math.ceil(tiles_x / 2))
        tiles_y = max(1, math.ceil(tiles_y / 2))
        mip += 1


def tile_count() -> int:
    return sum(width * height for _, width, height in pyramid_layout())


def morton_coordinates(tiles_x: int, tiles_y: int) -> list[tuple[int, int]]:
    """Return Z-order coordinates for one 2:1 mip group."""
    if tiles_x == tiles_y == 1:
        return [(0, 0)]
    if tiles_x != tiles_y * 2 or tiles_y & (tiles_y - 1):
        raise AssertionError(
            f"unsupported virtual-texture mip dimensions {tiles_x}x{tiles_y}"
        )
    coordinates: list[tuple[int, int]] = []
    bits = tiles_y.bit_length() - 1
    for half in range(2):
        for code in range(tiles_y * tiles_y):
            x = 0
            y = 0
            for bit in range(bits):
                x |= ((code >> (2 * bit)) & 1) << bit
                y |= ((code >> (2 * bit + 1)) & 1) << bit
            coordinates.append((x + half * tiles_y, y))
    return coordinates


def engine_tile_sequence() -> list[tuple[int, int, int]]:
    """Return EU5's fine-first row order with source Y stored bottom-up."""
    return [
        (mip, x, tiles_y - 1 - info_y)
        for mip, tiles_x, tiles_y in pyramid_layout()
        for info_y in range(tiles_y)
        for x in range(tiles_x)
    ]


def morton_tile_sequence() -> list[tuple[int, int, int]]:
    """Return the incorrect v5 traversal solely for lossless migration."""
    return [
        (mip, x, y)
        for mip, tiles_x, tiles_y in pyramid_layout()
        for x, y in morton_coordinates(tiles_x, tiles_y)
    ]


def preorder_tile_sequence() -> list[tuple[int, int, int]]:
    """Return the incorrect v4 traversal solely for lossless migration."""
    layout = {mip: (width, height) for mip, width, height in pyramid_layout()}
    root_mip = max(layout)
    result: list[tuple[int, int, int]] = [(root_mip, 0, 0)]

    def visit(mip: int, x: int, y: int) -> None:
        result.append((mip, x, y))
        if mip == 0:
            return
        child_mip = mip - 1
        for child_x, child_y in (
            (x * 2, y * 2),
            (x * 2 + 1, y * 2),
            (x * 2, y * 2 + 1),
            (x * 2 + 1, y * 2 + 1),
        ):
            visit(child_mip, child_x, child_y)

    # The 65536x32768 surface is one global root above two 32768-square
    # quadtrees. Each square is stored fully depth-first before its sibling.
    visit(root_mip - 1, 0, 0)
    visit(root_mip - 1, 1, 0)
    if len(result) != tile_count():
        raise AssertionError(
            f"virtual-texture traversal has {len(result):,} nodes, "
            f"expected {tile_count():,}"
        )
    return result


def png_bytes(array: np.ndarray) -> bytes:
    image = Image.fromarray(array)
    output = io.BytesIO()
    image.save(output, format="PNG", compress_level=9, optimize=False)
    return output.getvalue()


def write_info(
    path: Path,
    entries: list[tuple[int, int]],
    *,
    scalar_fields: bool,
) -> None:
    lines = [INFO_HEADER]
    if scalar_fields:
        lines.append(SCALAR_INFO_FIELDS)
    lines.append("tile_infos={ ")
    for offset, size in entries:
        lines.append(
            "{\n"
            f"\t\toffset={offset}\n"
            f"\t\tsize={size}\n"
            "\t} "
        )
    lines.append("}\n")
    path.write_text("".join(lines), encoding="utf-8", newline="\n")


def write_sparse_layer(
    stem: str,
    *,
    scalar_fields: bool,
    shared: np.ndarray | None,
) -> None:
    """Write an empty layer, optionally backed by one shared zero PNG."""
    bin_path = CACHE_OUT / f"{stem}.bin"
    info_path = CACHE_OUT / f"{stem}.info"
    count = tile_count()
    if shared is None:
        bin_path.write_bytes(b"")
        entries = [(-1, -1)] * count
    else:
        payload = png_bytes(shared)
        bin_path.write_bytes(payload)
        entries = [(0, len(payload))] * count
    write_info(info_path, entries, scalar_fields=scalar_fields)


def transformed_height_tile(
    source: Image.Image,
    mip: int,
    tile_x: int,
    tile_y: int,
) -> np.ndarray:
    # One output sample covers 2**mip virtual pixels.  The authored heightmap is
    # 1/8 of the virtual cache resolution in both dimensions.
    scale = (2**mip) * source.width / SOURCE_W
    x_offset = (tile_x * TILE_SIZE - BORDER_SIZE) * scale
    y_offset = (tile_y * TILE_SIZE - BORDER_SIZE) * scale
    tile = source.transform(
        (STORED_TILE_SIZE, STORED_TILE_SIZE),
        Image.Transform.AFFINE,
        (scale, 0.0, x_offset, 0.0, scale, y_offset),
        resample=Image.Resampling.BILINEAR,
        fillcolor=0,
    )
    values = np.clip(np.asarray(tile, dtype=np.float32), 0, 65_535)
    values = sculpted_height_tile(
        values,
        mip=mip,
        tile_x=tile_x,
        tile_y=tile_y,
    )
    # Preserve the full-precision authored source, but package its derived
    # runtime tiles at the bounded HEIGHT_QUANTUM. q512 and q256 created
    # unmistakable parallel terraces; q1 pushed the native-density world past
    # this machine's reliable 98%-load envelope. q64 is the current retail
    # candidate and still requires like-for-like close-renderer acceptance.
    values = (
        (values.astype(np.uint32) // HEIGHT_QUANTUM) * HEIGHT_QUANTUM
    ).astype(np.uint16)
    return values


@functools.lru_cache(maxsize=1)
def microrelief_noise_sources() -> dict[tuple[float, int], Image.Image]:
    """Build compact global lattices once; PIL samples them in native code."""

    result: dict[tuple[float, int], Image.Image] = {}
    for cell_size, _, seed in MICRORELIEF_OCTAVES:
        width = math.ceil(SOURCE_W / cell_size) + 2
        height = math.ceil(SOURCE_H / cell_size) + 2
        rng = np.random.default_rng(seed)
        lattice = rng.integers(0, 256, (height, width), dtype=np.uint8)
        result[(cell_size, seed)] = Image.fromarray(lattice, "L")
    return result


@functools.lru_cache(maxsize=1)
def mordor_runtime_walls() -> tuple[tuple[str, np.ndarray, float], ...]:
    projection = json.loads(PROJECTION_CONTROL.read_text(encoding="utf-8"))
    ridges = {ridge["key"]: ridge for ridge in projection["ridges"]}
    result: list[tuple[str, np.ndarray, float]] = []
    for key, phase in MORDOR_RUNTIME_WALL_PHASES:
        ridge = ridges.get(key)
        if ridge is None:
            raise ValueError(f"projection lacks source-pinned Mordor wall {key}")
        result.append(
            (
                key,
                np.asarray(
                    [
                        (float(x) * (SOURCE_W - 1), float(y) * (SOURCE_H - 1))
                        for x, y in ridge["points"]
                    ],
                    dtype=np.float32,
                ),
                phase,
            )
        )
    return tuple(result)


def mordor_wall_serration(
    result: np.ndarray,
    *,
    sample_x: np.ndarray,
    sample_y: np.ndarray,
) -> np.ndarray:
    """Break Mordor's exact range axes into an irregular chain of summits.

    The generic native-cache field gives mountain faces convincing small-scale
    texture, but live v60-v62 evidence showed that the long Ered Lithui crest
    still presents a level silhouette.  Measure distance and cumulative arc
    length only against the two audited wall polylines, then vary height along
    those same centerlines.  A broad guard around the direct Morannon marker
    preserves its low saddle and the two short source-reconciliation arms.
    """

    # Nearly every runtime tile is outside Mordor.  Reject those before
    # allocating a 132x132 coordinate grid or evaluating line segments.
    margin = 420.0
    left = 0.590 * (SOURCE_W - 1) - margin
    right = 0.748 * (SOURCE_W - 1) + margin
    top = 0.500 * (SOURCE_H - 1) - margin
    bottom = 0.710 * (SOURCE_H - 1) + margin
    if (
        float(sample_x[-1]) < left
        or float(sample_x[0]) > right
        or float(sample_y[-1]) < top
        or float(sample_y[0]) > bottom
    ):
        return result

    grid_x = sample_x[None, :]
    grid_y = sample_y[:, None]
    wall_addition = np.zeros(result.shape, dtype=np.float32)
    wall_trough = np.zeros(result.shape, dtype=np.float32)

    for _, points, phase in mordor_runtime_walls():
        segment_vectors = points[1:] - points[:-1]
        segment_lengths = np.hypot(
            segment_vectors[:, 0], segment_vectors[:, 1]
        )
        cumulative = np.concatenate(
            (np.zeros(1, dtype=np.float32), np.cumsum(segment_lengths)[:-1])
        )
        closest_distance_sq = np.full(result.shape, np.inf, dtype=np.float32)
        closest_arc = np.zeros(result.shape, dtype=np.float32)
        for start, vector, length, arc_start in zip(
            points[:-1],
            segment_vectors,
            segment_lengths,
            cumulative,
            strict=True,
        ):
            length_sq = max(float(length * length), 1.0)
            relative_x = grid_x - float(start[0])
            relative_y = grid_y - float(start[1])
            along = np.clip(
                (relative_x * float(vector[0]) + relative_y * float(vector[1]))
                / length_sq,
                0.0,
                1.0,
            )
            nearest_x = float(start[0]) + along * float(vector[0])
            nearest_y = float(start[1]) + along * float(vector[1])
            distance_sq = np.square(grid_x - nearest_x) + np.square(grid_y - nearest_y)
            nearer = distance_sq < closest_distance_sq
            closest_distance_sq = np.where(nearer, distance_sq, closest_distance_sq)
            closest_arc = np.where(
                nearer,
                float(arc_start) + along * float(length),
                closest_arc,
            )

        distance = np.sqrt(closest_distance_sq)
        # Overlapping incommensurate bands make irregular peak groups rather
        # than evenly spaced beads.  The 0.22 floor is removed below so long
        # troughs remain visibly lower than their neighbouring summits.
        longitudinal = (
            0.50
            + 0.24 * np.sin(closest_arc / 183.0 + phase)
            + 0.16 * np.sin(closest_arc / 79.0 + phase * 1.71)
            + 0.10 * np.sin(closest_arc / 37.0 - phase * 0.63)
        )
        summit_chain = np.power(
            np.clip((longitudinal - 0.22) / 0.78, 0.0, 1.0),
            1.55,
        )
        crest = np.exp(-0.5 * np.square(distance / 82.0))
        shoulder = np.exp(-0.5 * np.square(distance / 155.0))
        np.maximum(
            wall_addition,
            crest * summit_chain * 18_000.0,
            out=wall_addition,
        )
        np.maximum(
            wall_trough,
            shoulder
            * np.power(np.clip(0.40 - longitudinal, 0.0, 0.40) / 0.40, 1.25)
            * 4_500.0,
            out=wall_trough,
        )

    gate_x = MORANNON_RUNTIME_CENTER[0] * (SOURCE_W - 1)
    gate_y = MORANNON_RUNTIME_CENTER[1] * (SOURCE_H - 1)
    gate_distance = np.hypot(grid_x - gate_x, grid_y - gate_y)
    gate_guard = np.clip((gate_distance - 210.0) / 300.0, 0.0, 1.0)
    gate_guard = gate_guard * gate_guard * (3.0 - 2.0 * gate_guard)
    authored_strength = np.clip((result - 17_000.0) / 12_000.0, 0.0, 1.0)
    authored_strength = authored_strength * authored_strength * (
        3.0 - 2.0 * authored_strength
    )
    wall_addition *= gate_guard * authored_strength
    wall_trough *= gate_guard * authored_strength

    # Preserve ordering without creating a hard 64.4k cap.  The rational fit
    # retains a distinct height for every peak even where the existing massif
    # is already high, while bounded troughs cut the formerly level skyline.
    result = np.maximum(result - wall_trough, 0.0)
    headroom = np.maximum(64_400.0 - result, 1.0)
    fitted_addition = headroom * wall_addition / (
        headroom * 0.62 + wall_addition
    )
    return result + fitted_addition


def sculpted_height_tile(
    base: np.ndarray,
    *,
    mip: int,
    tile_x: int,
    tile_y: int,
) -> np.ndarray:
    """Add seamless native-cache relief only inside authored high terrain.

    The 8192-wide source remains the geography contract. This stage supplies
    the sub-source folds that vanilla bakes into its 65536-wide terrain cache.
    Detail fades naturally in coarser mips so distant LODs retain the authored
    silhouette and close LODs gain irregular faces, gullies, and summit teeth.
    """

    if float(np.max(base)) <= 15_000.0:
        return base

    virtual_step = float(2**mip)
    virtual_x = float(tile_x * TILE_SIZE - BORDER_SIZE) * virtual_step
    virtual_y = float(tile_y * TILE_SIZE - BORDER_SIZE) * virtual_step
    rugged = np.zeros(base.shape, dtype=np.float32)
    effective_weight_square = 0.0
    noise_sources = microrelief_noise_sources()
    for cell_size, weight, seed in MICRORELIEF_OCTAVES:
        # Suppress frequencies smaller than four samples in this mip. This is
        # a deterministic low-pass response, not a tile-local normalization,
        # so adjacent tiles and LOD transitions cannot acquire seams.
        lod_weight = min(1.0, cell_size / (virtual_step * 4.0))
        effective_weight = weight * lod_weight
        if effective_weight < 0.005:
            continue
        noise_tile = noise_sources[(cell_size, seed)].transform(
            (STORED_TILE_SIZE, STORED_TILE_SIZE),
            Image.Transform.AFFINE,
            (
                virtual_step / cell_size,
                0.0,
                virtual_x / cell_size,
                0.0,
                virtual_step / cell_size,
                virtual_y / cell_size,
            ),
            resample=Image.Resampling.BILINEAR,
            fillcolor=127,
        )
        rugged += (
            np.asarray(noise_tile, dtype=np.float32) / 127.5 - 1.0
        ) * effective_weight
        effective_weight_square += effective_weight * effective_weight

    if effective_weight_square <= 0.0:
        return base
    # Empirical global calibration of the lattice stack. Scaling by the
    # effective octave norm keeps the response stable as fine octaves fade.
    rugged /= max(
        0.535
        * math.sqrt(effective_weight_square)
        / MICRORELIEF_WEIGHT_NORM,
        1.0e-6,
    )
    folded = np.tanh(rugged * 0.82)
    positive_teeth = np.power(
        np.clip((rugged - 0.12) / 1.65, 0.0, 1.0),
        1.50,
    )
    negative_teeth = 0.72 * np.power(
        np.clip((-rugged - 0.18) / 1.65, 0.0, 1.0),
        1.50,
    )
    # A one-sided crest response left whole source-backed arms smooth whenever
    # their deterministic noise field happened to be negative. Both extrema
    # now raise compact teeth; the calibrated subtraction preserves the global
    # zero mean, so this changes morphology rather than inflating the ranges.
    summit_teeth = np.maximum(positive_teeth, negative_teeth) - 0.257
    detail = folded * 10_500.0 + summit_teeth * 30_000.0

    # The normal dry datum is about 12.7k. Treating its harmless broad noise as
    # mountain relief made a qualifying tile differ by one q64 step from an
    # adjacent skipped lowland tile. Begin at the real foothill band instead;
    # this makes ordinary ground bit-identical regardless of tile eligibility.
    authored_relief = np.maximum(base - 15_000.0, 0.0)
    strength = np.clip(authored_relief / 10_000.0, 0.0, 1.0)
    strength = strength * strength * (3.0 - 2.0 * strength)
    # The v53-v54 high-resolution folds sat on top of the full coarse range
    # height, so the renderer still saw one broad high body. Vanilla instead
    # keeps a lower connected massif beneath many native-cache summits. Lower
    # only already-authored mountain relief here; the detail response then
    # restores irregular peaks while its negative half opens real gullies.
    mountain_body = base - authored_relief * strength * 0.42
    # Fit positive relief continuously into the available headroom. A simple
    # multiplier still allowed rare teeth to overshoot into the hard ceiling;
    # this rational response stays strictly below it while retaining ordering
    # between every summit sample. Negative gullies remain uncompressed.
    positive_raw = np.maximum(detail, 0.0) * strength
    headroom = np.maximum(64_400.0 - mountain_body, 1.0)
    positive = headroom * positive_raw / (
        headroom * 0.45 + positive_raw
    )
    negative = np.minimum(detail, 0.0) * strength
    result = np.maximum(
        mountain_body + positive + negative,
        0.0,
    )

    # The 8192 source still retains two nearby responses around the direct
    # Ardacraft Erebor marker: a tiny canonical tooth and a larger painted
    # mound. At close zoom their magnified overlap produced v54's rejected
    # U-shaped mesa. De-duplicate them at the renderer's native scale, then
    # author one asymmetric cone. Ravenhill is about 466 virtual pixels away
    # and therefore remains outside this bounded 400-pixel guard.
    erebor_x = 0.599699 * (SOURCE_W - 1)
    erebor_y = 0.137606 * (SOURCE_H - 1)
    sample_x = virtual_x + np.arange(STORED_TILE_SIZE, dtype=np.float32) * virtual_step
    sample_y = virtual_y + np.arange(STORED_TILE_SIZE, dtype=np.float32) * virtual_step
    erebor_dx = sample_x[None, :] - erebor_x
    erebor_dy = sample_y[:, None] - erebor_y
    erebor_distance = np.hypot(erebor_dx, erebor_dy)
    if float(np.min(erebor_distance)) < 400.0:
        feather = np.clip((erebor_distance - 250.0) / 150.0, 0.0, 1.0)
        feather = feather * feather * (3.0 - 2.0 * feather)
        flatten_weight = 1.0 - feather
        datum = 12_743.0
        result = result * (1.0 - flatten_weight) + datum * flatten_weight
        angle = np.arctan2(erebor_dy, erebor_dx)
        irregular_distance = erebor_distance * (
            1.0
            + 0.045 * np.sin(angle * 3.0 + 0.7)
            + 0.020 * np.sin(angle * 7.0 - 0.4)
        )
        apron = np.power(
            np.clip(1.0 - irregular_distance / 180.0, 0.0, 1.0),
            2.20,
        )
        cone = np.power(
            np.clip(1.0 - irregular_distance / 84.0, 0.0, 1.0),
            1.48,
        )
        # Keep the single peak below the cache ceiling. v38's 70.7k target was
        # clipped to 64.5k across several samples and visibly flattened the
        # Lonely Mountain's crown.
        erebor_target = (
            datum
            + apron * 5_000.0
            + cone * 43_000.0
            + cone * np.tanh(rugged * 0.90) * 2_200.0
        )
        result = np.maximum(result, erebor_target)
    result = mordor_wall_serration(
        result,
        sample_x=sample_x,
        sample_y=sample_y,
    )
    return np.clip(result, 0.0, 64_400.0)


def resized_mask(
    values: np.ndarray,
    *,
    resampling: Image.Resampling = Image.Resampling.NEAREST,
) -> np.ndarray:
    return np.asarray(
        Image.fromarray(values.astype(np.uint8), "L").resize(
            (MATERIAL_W, MATERIAL_H),
            resampling,
        ),
        dtype=np.uint8,
    )


def rounded_expansion(
    values: np.ndarray,
    *,
    radius: float,
    threshold: int = 18,
) -> np.ndarray:
    """Expand a binary mask without the square footprint of MaxFilter."""
    return np.asarray(
        Image.fromarray(values.astype(np.uint8) * 255, "L").filter(
            ImageFilter.GaussianBlur(radius=radius)
        ),
        dtype=np.uint8,
    ) >= threshold


def smoothed_biome_weight(
    biomes: np.ndarray,
    biome_ids: tuple[int, ...],
    *,
    radius: float,
) -> np.ndarray:
    """Return a continuous material weight around an authored biome envelope."""
    mask = np.isin(biomes, biome_ids).astype(np.uint8) * 255
    image = Image.fromarray(mask, "L").resize(
        (MATERIAL_W, MATERIAL_H),
        Image.Resampling.BILINEAR,
    )
    if radius > 0.0:
        image = image.filter(ImageFilter.GaussianBlur(radius=radius))
    return np.asarray(image, dtype=np.float32) / 255.0


def material_noise() -> np.ndarray:
    """Return broad organic variation fields without location-cell geometry."""
    rng = np.random.default_rng(30_181_947)
    broad = Image.fromarray(
        rng.integers(0, 256, (256, 512), dtype=np.uint8),
        "L",
    ).resize((MATERIAL_W, MATERIAL_H), Image.Resampling.BICUBIC)
    medium = Image.fromarray(
        rng.integers(0, 256, (1_024, 2_048), dtype=np.uint8),
        "L",
    ).resize((MATERIAL_W, MATERIAL_H), Image.Resampling.BICUBIC)
    broad_values = np.asarray(broad, dtype=np.uint16)
    medium_values = np.asarray(medium, dtype=np.uint16)
    return ((broad_values * 3 + medium_values * 2) // 5).astype(np.uint8)


def physical_slope(height: np.ndarray) -> np.ndarray:
    """Return the strongest centred one-pixel rise around every source pixel.

    Material paint must describe the rendered relief rather than merely repeat
    broad altitude bands.  A two-pixel centred difference suppresses single
    noisy pixels while preserving the authored flanks of ridges and summits.
    Work in row chunks so deriving the 8192x4096 field does not require two
    full-size signed copies of the 16-bit height source.
    """
    slope = np.zeros(height.shape, dtype=np.uint16)
    chunk_rows = 256

    for start in range(0, height.shape[0], chunk_rows):
        stop = min(height.shape[0], start + chunk_rows)
        delta = np.abs(
            height[start:stop, 2:].astype(np.int32)
            - height[start:stop, :-2].astype(np.int32)
        )
        delta //= 2
        slope[start:stop, 1:-1] = np.maximum(
            slope[start:stop, 1:-1],
            delta.astype(np.uint16),
        )

    for start in range(1, height.shape[0] - 1, chunk_rows):
        stop = min(height.shape[0] - 1, start + chunk_rows)
        delta = np.abs(
            height[start + 1 : stop + 1].astype(np.int32)
            - height[start - 1 : stop - 1].astype(np.int32)
        )
        delta //= 2
        slope[start:stop] = np.maximum(
            slope[start:stop],
            delta.astype(np.uint16),
        )

    return slope


def ridge_material_weight(
    projection: dict,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return organic source-crest exposure without location-cell geometry.

    Height remains the authority for physical relief. This companion field
    only tells the material painter where a source-aligned chain or named
    summit can plausibly expose rock. Broad blurred bodies prevent binary
    height/slope contours from becoming disconnected grey ribbons, while a
    narrower spine retains readable crests at regional zoom.
    """

    result = np.zeros((MATERIAL_H, MATERIAL_W), dtype=np.float32)
    severe_range = np.zeros((MATERIAL_H, MATERIAL_W), dtype=np.float32)

    def path_field(
        points: list[list[float]],
        *,
        key: str,
        width: int,
        strength: float,
        wander: float,
        expose_severe_range: bool,
        sharp_cross_section: bool,
    ) -> None:
        path = natural_path(
            points,
            (MATERIAL_W, MATERIAL_H),
            key=key,
            closed=False,
            amplitude=wander,
            spacing=0.003,
        )
        if sharp_cross_section:
            body = Image.new("L", (MATERIAL_W, MATERIAL_H), 0)
            ImageDraw.Draw(body).line(path, fill=255, width=1, joint="curve")
            body_values = np.asarray(
                body.filter(
                    ImageFilter.GaussianBlur(radius=max(2, round(width * 0.32)))
                ),
                dtype=np.float32,
            )
            spine = Image.new("L", (MATERIAL_W, MATERIAL_H), 0)
            ImageDraw.Draw(spine).line(path, fill=255, width=1, joint="curve")
            spine_values = np.asarray(
                spine.filter(
                    ImageFilter.GaussianBlur(radius=max(1, round(width * 0.075)))
                ),
                dtype=np.float32,
            )
            body_values *= 255.0 / max(float(body_values.max()), 1.0)
            spine_values *= 255.0 / max(float(spine_values.max()), 1.0)
            field = np.maximum(body_values * 0.30, spine_values)
        else:
            body = Image.new("L", (MATERIAL_W, MATERIAL_H), 0)
            ImageDraw.Draw(body).line(
                path,
                fill=255,
                width=max(3, round(width * 1.25)),
                joint="curve",
            )
            body = body.filter(
                ImageFilter.GaussianBlur(radius=max(2, round(width * 0.38)))
            )
            spine = Image.new("L", (MATERIAL_W, MATERIAL_H), 0)
            ImageDraw.Draw(spine).line(
                path,
                fill=255,
                width=max(2, round(width * 0.34)),
                joint="curve",
            )
            spine = spine.filter(
                ImageFilter.GaussianBlur(radius=max(1, round(width * 0.10)))
            )
            field = np.maximum(
                np.asarray(body, dtype=np.float32) * 0.35,
                np.asarray(spine, dtype=np.float32),
            )
        np.maximum(result, field / 255.0 * strength, out=result)
        if expose_severe_range:
            np.maximum(severe_range, field / 255.0 * strength, out=severe_range)

    for ridge in projection["ridges"]:
        width = max(3, round(float(ridge["width"]) * MATERIAL_H))
        strength = float(ridge["height"])
        wander = float(ridge.get("wander", 0.001))
        path_field(
            ridge["points"],
            key=f"ridge:{ridge['key']}",
            width=width,
            strength=strength,
            wander=wander,
            expose_severe_range=False,
            sharp_cross_section=bool(ridge.get("sharp_cross_section", False)),
        )
        for branch_index, branch in enumerate(ridge.get("branches", [])):
            path_field(
                branch,
                key=f"ridge:{ridge['key']}:branch:{branch_index}",
                width=max(3, round(width * 0.72)),
                strength=strength * 0.72,
                wander=wander,
                expose_severe_range=bool(
                    ridge.get("source_audited_branches", False)
                ),
                sharp_cross_section=False,
            )

    for peak in projection.get("named_peaks", []):
        if peak["key"] not in {"erebor_peak", "mount_gundabad"}:
            continue
        x = round(float(peak["center"][0]) * (MATERIAL_W - 1))
        y = round(float(peak["center"][1]) * (MATERIAL_H - 1))
        radius_scale = (
            0.72
            if peak["key"] == "erebor_peak"
            else 0.34
            if peak["key"] == "mount_gundabad"
            else 1.0
        )
        radius = max(
            3,
            round(float(peak["radius"]) * MATERIAL_H * radius_scale),
        )
        image = Image.new("L", (MATERIAL_W, MATERIAL_H), 0)
        ImageDraw.Draw(image).ellipse(
            (
                x - round(radius * 0.92),
                y - round(radius * 0.92),
                x + round(radius * 0.92),
                y + round(radius * 0.92),
            ),
            fill=255,
        )
        image = image.filter(
            ImageFilter.GaussianBlur(radius=max(1, round(radius * 0.28)))
        )
        field = (
            np.asarray(image, dtype=np.float32)
            / 255.0
            * float(peak["strength"])
        )
        np.maximum(result, field, out=result)
        if float(peak["strength"]) >= 0.80:
            np.maximum(severe_range, field, out=severe_range)

    # Paint exposed rock from the exact Ardacraft numeric crest authority.
    # The former material field depended mainly on broad hand axes and turned
    # narrow ranges into grey slabs disconnected from their source arêtes.
    # A convex response keeps foothills quiet while retaining every jagged
    # high branch. The same source response makes all major northern and
    # southern ranges eligible for the severe-height transition without
    # inventing exposure outside the audited footprint.
    source_relief = source_relief_field(
        projection, (MATERIAL_W, MATERIAL_H)
    )
    source_crest = np.clip(
        np.power(source_relief, 3.65) * 1.16,
        0.0,
        1.0,
    )
    np.maximum(result, source_crest, out=result)
    np.maximum(
        severe_range,
        np.clip(np.power(source_relief, 3.05) * 1.10, 0.0, 1.0),
        out=severe_range,
    )

    return (
        np.clip(result, 0.0, 1.0),
        np.clip(severe_range, 0.0, 1.0),
        source_relief,
    )


def river_material_mask(projection: dict) -> np.ndarray:
    image = Image.new("L", (MATERIAL_W, MATERIAL_H), 0)
    draw = ImageDraw.Draw(image)

    for river in projection["rivers"]:
        source_points = river_control_points(river)
        points = natural_path(
            source_points,
            (MATERIAL_W, MATERIAL_H),
            key=f"river:{river['key']}",
            closed=False,
            amplitude=float(river.get("wander", 0.0015)),
            spacing=0.00125,
        )
        if len(points) < 2:
            continue
        # The indexed parser graph supplies the actual water. Material paint
        # only darkens the banks around it. Theatre review showed the former
        # 1.45x mask as broad transport-like corridors at regional zoom.
        if river.get("terrain_only"):
            hydrology_class = str(river.get("hydrology_class", ""))
            if hydrology_class not in TERRAIN_ONLY_RIVER_VISIBILITY:
                raise ValueError(
                    f"river {river['key']} has unsupported physical-drainage class "
                    f"{hydrology_class!r}"
                )
            visibility_scale, minimum_width = TERRAIN_ONLY_RIVER_VISIBILITY[
                hydrology_class
            ]
        else:
            visibility_scale, minimum_width = 0.62, 2
        nominal = max(
            float(minimum_width),
            float(river["width"])
            * MATERIAL_H
            * visibility_scale
            * float(river.get("material_scale", 1.0)),
        )
        growth = float(river.get("material_growth", 0.58))
        if not 0.0 <= growth <= 0.75:
            raise ValueError(f"river {river['key']} has invalid material growth")
        segments = len(points) - 1
        for index, (start, end) in enumerate(zip(points, points[1:])):
            progress = (index + 0.5) / segments
            width = max(2, round(nominal * (1.0 - growth + progress * growth)))
            draw.line((start, end), fill=255, width=width)
            radius = width // 2
            if radius:
                for x, y in (start, end):
                    draw.ellipse(
                        (x - radius, y - radius, x + radius, y + radius),
                        fill=255,
                    )
    return np.asarray(image, dtype=np.uint8) > 0


def render_material_source() -> np.ndarray:
    """Paint the native 16-channel mask from continuous Arda controls."""
    with Image.open(BIOME_CONTROL) as opened:
        control_biomes = np.asarray(opened, dtype=np.uint8)
    if control_biomes.shape != (MATERIAL_H // 2, MATERIAL_W // 2):
        raise ValueError(
            "material control is "
            f"{control_biomes.shape[::-1]}, expected "
            f"{(MATERIAL_W // 2, MATERIAL_H // 2)}"
        )
    biomes = resized_mask(control_biomes)
    projection = json.loads(PROJECTION_CONTROL.read_text(encoding="utf-8"))
    # Match the native-resolution shoreline used by the height source rather
    # than re-enlarging the control biome edge.
    land = np.asarray(
        land_mask(projection, (MATERIAL_W, MATERIAL_H)),
        dtype=np.uint8,
    ) > 0
    water = ~land

    with Image.open(HEIGHT_SOURCE) as opened:
        height = np.asarray(opened, dtype=np.uint16)
    if height.shape != (MATERIAL_H, MATERIAL_W):
        raise ValueError(
            f"material height is {height.shape[::-1]}, expected "
            f"{(MATERIAL_W, MATERIAL_H)}"
        )

    noise = material_noise()
    # Terrain variation must follow geography at theatre scale.  The former
    # equal random mix put the same brown-green stipple on plains, forests,
    # and crests, flattening the otherwise valid 3D height field.  Keep the
    # organic noise, but bias it continuously by altitude and authored biome
    # so high ranges expose rockier variation while woods and wetlands retain
    # a cooler, greener base.  This changes no gameplay terrain template.
    selector = noise.astype(np.float32)
    material = np.zeros(noise.shape, dtype=np.uint16)

    earth = land & (selector >= 142.0)
    earth_blend = land & (selector >= 116.0) & (selector < 142.0)
    material[land & ~earth & ~earth_blend] = MATERIAL_GRASS
    material[earth_blend] = MATERIAL_GRASS | MATERIAL_EARTH
    material[earth] = MATERIAL_EARTH

    cool_ground = np.isin(biomes, (2, 3, 6)) & land
    cool_earth = cool_ground & (selector >= 188.0)
    cool_blend = cool_ground & (selector >= 160.0) & (selector < 188.0)
    material[cool_ground & ~cool_earth & ~cool_blend] = MATERIAL_GRASS
    material[cool_blend] = MATERIAL_GRASS | MATERIAL_EARTH
    material[cool_earth] = MATERIAL_EARTH

    # Climate envelopes use dedicated native-material channels inside the one
    # continuous renderer biome. This is deliberately different from the
    # rejected v44/v45 binary mixtures: source geometry owns the interior and
    # a broad distance weight owns only the edge feather. No location template
    # or high-frequency selector can create cell-shaped climate islands.
    tundra = (biomes == 5) & land
    material[tundra] = MATERIAL_TUNDRA

    steppe_weight = smoothed_biome_weight(
        control_biomes, (9,), radius=44.0
    )
    steppe_fringe = (steppe_weight >= 0.10) & (steppe_weight < 0.62) & land
    steppe_core = (steppe_weight >= 0.62) & land
    material[steppe_fringe] = MATERIAL_GRASS | MATERIAL_STEPPE
    material[steppe_core] = MATERIAL_STEPPE

    arid_weight = smoothed_biome_weight(
        control_biomes, (10,), radius=72.0
    )
    arid_fringe = (arid_weight >= 0.10) & (arid_weight < 0.58) & land
    arid_core = (arid_weight >= 0.58) & land
    material[arid_fringe] = MATERIAL_STEPPE | MATERIAL_SAND
    material[arid_core] = MATERIAL_SAND

    ash_weight = smoothed_biome_weight(
        control_biomes, (8,), radius=42.0
    )
    ash_score = ash_weight * 255.0 + (selector - 127.5) * 0.30
    ash_active = (ash_weight > 0.025) & land
    ash_earth = ash_active & (ash_score < 112.0)
    ash_dark = ash_active & (
        (ash_score >= 112.0) & (ash_score < 286.0)
    )
    # Keep Mordor's basin basaltic. The former 205 cutoff promoted most of the
    # fully weighted ash interior to grey rock, so the basin read as one giant
    # slab while the true enclosing ranges disappeared into it. Sparse ground
    # rock remains organic; physical highland exposure below owns the crests.
    ash_rock = ash_active & (ash_score >= 286.0)
    material[ash_earth] = MATERIAL_EARTH | MATERIAL_DARK_ROCK
    material[ash_dark] = MATERIAL_DARK_ROCK
    material[ash_rock] = MATERIAL_DARK_ROCK | MATERIAL_ROCK

    # Arda Maps supplies 190 renderable upland footprints independently of its
    # mountain atlas. Give those rolling hills a restrained earth bias while
    # preserving forests, wetlands, deserts, and Mordor's volcanic paint.
    # This removes the proof map's visually flat lowlands without promoting
    # every source highland to an impassable or snow-covered range.
    highland_image = source_zone_mask(
        projection, "highland_zones", (MATERIAL_W, MATERIAL_H)
    ).filter(ImageFilter.GaussianBlur(radius=3.0))
    highland_weight = np.asarray(highland_image, dtype=np.uint8)
    upland_active = (
        (highland_weight >= 14)
        & land
        & ~cool_ground
        & (arid_weight < 0.45)
        & (ash_weight < 0.45)
    )
    upland_score = (
        selector
        + highland_weight.astype(np.float32) * 0.30
        + np.clip(
            (height.astype(np.float32) - 13_000.0) / 120.0,
            0.0,
            64.0,
        )
    )
    upland_blend = upland_active & (
        (upland_score >= 132.0) & (upland_score < 188.0)
    )
    upland_earth = upland_active & (upland_score >= 188.0)
    material[upland_blend] = MATERIAL_GRASS | MATERIAL_EARTH
    material[upland_earth] = MATERIAL_EARTH
    del highland_image, highland_weight, upland_score

    # Mordor's high volcanic surfaces must remain basaltic. Everywhere else,
    # blend altitude, a locally smoothed physical slope, the source-aligned
    # crest field, and broad organic noise. The former hard height/slope cuts
    # broke one continuous range into coarse grey ribbons and islands even
    # after location-scoped mountain_wasteland rendering was removed.
    slope = physical_slope(height)
    slope_strength = np.clip(
        slope.astype(np.float32) / 12.0,
        0.0,
        255.0,
    ).astype(np.uint8)
    slope_weight = np.asarray(
        Image.fromarray(slope_strength, "L").filter(
            ImageFilter.GaussianBlur(radius=3.5)
        ),
        dtype=np.float32,
    ) / 255.0
    height_weight = np.clip(
        (height.astype(np.float32) - 28_000.0) / 34_000.0,
        0.0,
        1.0,
    )
    (
        crest_weight,
        severe_range_weight,
        native_source_relief,
    ) = ridge_material_weight(projection)
    organic_weight = (selector - 127.5) / 127.5
    exposure = (
        crest_weight * 0.52
        + height_weight * 0.36
        + slope_weight * 0.34
        + organic_weight * 0.10
    )
    highland = land & (height >= 27_000) & (ash_weight < 0.62)
    # Source-reviewed severe ranges receive earlier rock transitions only on
    # their exact reconstructed crest response. The former hand-axis severe
    # field was wider than the physical reconstructed ranges and recreated grey slabs
    # after their height shelves had been removed. Pass floors remain below
    # the highland gate and therefore stay traversable/green.
    severe_range = highland & (severe_range_weight >= 0.50)
    highland_grass_earth = highland & (height < 38_000)
    highland_earth = highland & (height >= 38_000)
    source_dark = (
        highland & (height >= 33_000) & (native_source_relief >= 0.62)
    )
    source_blend = (
        highland & (height >= 43_000) & (native_source_relief >= 0.74)
    )
    source_rock = (
        highland & (height >= 50_000) & (native_source_relief >= 0.84)
    )
    highland_dark = (
        highland & (height >= 43_000) & (exposure >= 0.66)
    ) | (severe_range & (height >= 38_000) & (exposure >= 0.46)) | source_dark
    highland_blend = (
        highland & (height >= 49_000) & (exposure >= 0.78)
    ) | (severe_range & (height >= 43_000) & (exposure >= 0.56)) | source_blend
    highland_rock = (
        highland & (height >= 54_000) & (exposure >= 0.88)
    ) | (severe_range & (height >= 46_000) & (exposure >= 0.62)) | source_rock
    material[highland_grass_earth] = MATERIAL_GRASS | MATERIAL_EARTH
    material[highland_earth] = MATERIAL_EARTH
    material[highland_dark] = MATERIAL_EARTH | MATERIAL_DARK_ROCK
    material[highland_blend] = MATERIAL_DARK_ROCK | MATERIAL_ROCK
    material[highland_rock] = MATERIAL_ROCK

    # Gundabad's v46 height is deliberately contracted into a compact chain
    # crown. Paint that *physical* body at lower thresholds than ordinary long
    # ranges so it does not return to either v44's green bowl or v45's regional
    # snow carpet. The neighbourhood only selects the canonical theatre; the
    # 32k/35k height contours own the irregular visible boundary.
    surface_y, surface_x = np.ogrid[:MATERIAL_H, :MATERIAL_W]
    gundabad = next(
        item for item in projection.get("named_peaks", [])
        if item["key"] == "mount_gundabad"
    )
    gundabad_dx = (
        surface_x.astype(np.float32)
        - float(gundabad["center"][0]) * (MATERIAL_W - 1)
    )
    gundabad_dy = (
        surface_y.astype(np.float32)
        - float(gundabad["center"][1]) * (MATERIAL_H - 1)
    )
    gundabad_neighbourhood = (
        np.hypot(gundabad_dx, gundabad_dy) <= MATERIAL_H * 0.014
    )
    gundabad_exposed = (
        land & gundabad_neighbourhood & (height >= 32_000)
    )
    gundabad_rock = gundabad_exposed & (height >= 35_000)
    material[gundabad_exposed] = MATERIAL_EARTH | MATERIAL_DARK_ROCK
    material[gundabad_rock] = MATERIAL_DARK_ROCK | MATERIAL_ROCK

    # Snow is the most selective crest material. It follows source-aligned
    # exposure plus actual altitude rather than a mountain-class footprint.
    crest = land & (ash_weight < 0.62)
    rock_snow = crest & (
        (
            (height >= 58_000)
            & (exposure >= 0.84)
            & (native_source_relief >= 0.88)
        )
        | (severe_range & (height >= 54_000) & (exposure >= 0.72))
    )
    snow = crest & (
        (
            (height >= 62_000)
            & (exposure >= 0.91)
            & (native_source_relief >= 0.95)
        )
        | (severe_range & (height >= 59_000) & (exposure >= 0.82))
    )
    material[rock_snow] = MATERIAL_ROCK | MATERIAL_SNOW
    material[snow] = MATERIAL_SNOW

    volcanic_highland = land & (height >= 30_000) & (ash_weight >= 0.62)
    volcanic_exposed = volcanic_highland & (
        (height >= 42_000) & (exposure >= 0.58)
    )
    volcanic_rock = volcanic_highland & (
        (height >= 52_000) & (exposure >= 0.74)
    )
    material[volcanic_highland] = MATERIAL_DARK_ROCK
    material[volcanic_exposed] = MATERIAL_DARK_ROCK | MATERIAL_ROCK
    material[volcanic_rock] = MATERIAL_ROCK

    # Morannon's canonical point is the low Cirith Gorgor saddle, so a broad
    # altitude-only paint either misses its encircling walls or incorrectly
    # rocks over the pass floor. Bind the visible wall transition to all three
    # available authorities: proximity to the audited gate, exact source
    # relief, and physical height. The 23k/30k steps expose the enclosing arms
    # while the 12.7k saddle remains untouched and traversable.
    morannon = next(
        item for item in projection["passes"] if item["key"] == "morannon"
    )
    material_y, material_x = np.ogrid[:MATERIAL_H, :MATERIAL_W]
    morannon_dx = (
        material_x.astype(np.float32)
        - float(morannon["center"][0]) * (MATERIAL_W - 1)
    )
    morannon_dy = (
        material_y.astype(np.float32)
        - float(morannon["center"][1]) * (MATERIAL_H - 1)
    )
    morannon_neighbourhood = (
        np.hypot(morannon_dx, morannon_dy) <= MATERIAL_H * 0.040
    )
    morannon_source_wall = severe_range_weight >= 0.10
    morannon_exposed = (
        land
        & morannon_neighbourhood
        & morannon_source_wall
        & (height >= 23_000)
    )
    morannon_rock = morannon_exposed & (height >= 30_000)
    material[morannon_exposed] = MATERIAL_EARTH | MATERIAL_DARK_ROCK
    material[morannon_rock] = MATERIAL_DARK_ROCK | MATERIAL_ROCK

    # Major coasts receive EU5's complete shore channel stack. Source lakes
    # smaller than one runtime location remain physical land because engine-
    # water classification turns their entire host cells into deep quarries.
    # Their exact lake-biome polygons instead receive wet pond material and a
    # soft margin, preserving the cartography without breaking the heightfield.
    lake_water = (biomes == 7) & water
    material_pond = (biomes == 7) & land
    ocean_water = water & ~lake_water
    coast = rounded_expansion(
        ocean_water, radius=1.35, threshold=60
    ) & land
    lake_coast = rounded_expansion(
        lake_water, radius=1.15, threshold=70
    ) & land
    material_pond_margin = rounded_expansion(
        material_pond, radius=1.45, threshold=52
    ) & land
    outer_coast = rounded_expansion(land, radius=2.0) & water

    coast_kind = np.full(height.shape, MATERIAL_FLAT_COAST, dtype=np.uint16)
    coast_kind[(height >= 16_000) & (height < 27_000)] = MATERIAL_HILL_COAST
    coast_kind[(height >= 27_000) & (height < 39_000)] = MATERIAL_PLATEAU_COAST
    coast_kind[height >= 39_000] = MATERIAL_MOUNTAIN_COAST
    coast_kind[biomes == 4] = MATERIAL_MOUNTAIN_COAST
    coast_kind[biomes == 6] = MATERIAL_WETLAND_COAST
    material[coast] |= (
        coast_kind[coast]
        | MATERIAL_COAST_TRANSITION
        | MATERIAL_WATER_TRANSITION
    )
    material[lake_coast] |= MATERIAL_WATER_TRANSITION
    material[material_pond_margin] |= (
        MATERIAL_WETLAND_COAST | MATERIAL_WATER_TRANSITION
    )
    material[material_pond] = (
        MATERIAL_GRASS
        | MATERIAL_EARTH
        | MATERIAL_WETLAND_COAST
        | MATERIAL_WATER_TRANSITION
        | MATERIAL_RIVER
    )
    material[outer_coast] |= MATERIAL_WATER_TRANSITION

    # Every playable dry cell uses one ENDÓRË renderer biome. Engine
    # channels 8/9 above are terrain variations in that custom palette, not
    # engine vegetation/climate transitions or per-location templates.

    rivers = river_material_mask(projection) & land
    material[rivers] |= MATERIAL_RIVER

    if np.any(material[land] == 0):
        raise AssertionError("material paint leaves land without a variation channel")
    if np.any(material[water & ~outer_coast] != 0):
        raise AssertionError("material paint leaks into open water")

    climate_contracts = (
        ("tundra", (biomes == 5) & land & (height < 27_000), MATERIAL_TUNDRA, 0.96),
        ("steppe", (biomes == 9) & land & (height < 27_000), MATERIAL_STEPPE, 0.90),
        ("arid", (biomes == 10) & land & (height < 27_000), MATERIAL_SAND, 0.90),
    )
    for key, active, channel, minimum in climate_contracts:
        if not np.any(active):
            raise AssertionError(f"{key} material contract has no lowland samples")
        coverage = float(((material[active] & channel) != 0).mean())
        if coverage < minimum:
            raise AssertionError(
                f"{key} dedicated material coverage regressed: "
                f"{coverage:.6f} < {minimum:.6f}"
            )

    # Bind renderer material to the same compact source geometry as the height
    # contracts.  A minimum alone rewarded the rejected v34-v36 solution: it
    # could pass by painting an ever larger grey slab.  These bounded windows
    # require readable exposed crests while refusing range-sized caps.  The
    # Morannon window is intentionally mostly dark rock because it overlaps the
    # source-authored volcanic biome. Its grey-rock ceiling allows the two
    # audited Cirith Gorgor hinge arms while the stricter total-exposure ceiling
    # remains the anti-plateau signal there.
    material_contracts = {
        "dunharrow": {
            "center": (0.496751, 0.553026),
            "radius": 0.018,
            "minimum_exposed": 0.14,
            "maximum_exposed": 0.38,
            "minimum_rock": 0.045,
            "maximum_rock": 0.24,
        },
        "morannon": {
            "center": (0.609732, 0.529449),
            "radius": 0.015,
            "minimum_exposed": 0.06,
            "maximum_exposed": 0.18,
            # v68 removes the duplicated colour-derived body which v66-v67
            # proved as a grey tabletop at Carchost. The pointed hinge is
            # predominantly volcanic dark rock; retain a compact grey crest
            # signal without rewarding the deleted slab's broad coverage.
            "minimum_rock": 0.001,
            "maximum_rock": 0.03,
        },
        "gundabad": {
            "center": (0.502345, 0.102487),
            "radius": 0.008,
            "minimum_exposed": 0.24,
            "maximum_exposed": 0.45,
            "minimum_rock": 0.10,
            "maximum_rock": 0.25,
        },
        "erebor": {
            "center": (0.599699, 0.137606),
            "radius": 0.008,
            "minimum_exposed": 0.007,
            "maximum_exposed": 0.16,
            "minimum_rock": 0.004,
            "maximum_rock": 0.10,
        },
    }
    contract_failures: list[str] = []
    contract_metrics: list[str] = []
    for key, contract in material_contracts.items():
        center_x = round(contract["center"][0] * (MATERIAL_W - 1))
        center_y = round(contract["center"][1] * (MATERIAL_H - 1))
        radius = max(2, round(contract["radius"] * MATERIAL_H))
        left = max(0, center_x - radius)
        right = min(MATERIAL_W, center_x + radius + 1)
        top = max(0, center_y - radius)
        bottom = min(MATERIAL_H, center_y + radius + 1)
        local_y, local_x = np.ogrid[top:bottom, left:right]
        radial = (
            (local_x - center_x) ** 2 + (local_y - center_y) ** 2
        ) <= radius**2
        samples = material[top:bottom, left:right][radial]
        dark = (samples & MATERIAL_DARK_ROCK) != 0
        rock = (samples & MATERIAL_ROCK) != 0
        snow = (samples & MATERIAL_SNOW) != 0
        exposed_fraction = float((dark | rock | snow).mean())
        rock_fraction = float(rock.mean())
        contract_metrics.append(
            f"{key}=exposed:{exposed_fraction:.6f},rock:{rock_fraction:.6f}"
        )
        if exposed_fraction < contract["minimum_exposed"]:
            contract_failures.append(
                f"{key} mountain material remains too green: "
                f"{exposed_fraction:.6f} < {contract['minimum_exposed']:.6f}"
            )
        if exposed_fraction > contract["maximum_exposed"]:
            contract_failures.append(
                f"{key} mountain material regressed to a broad cap: "
                f"{exposed_fraction:.6f} > {contract['maximum_exposed']:.6f}"
            )
        if rock_fraction < contract["minimum_rock"]:
            contract_failures.append(
                f"{key} lacks exposed rock on its high flanks: "
                f"{rock_fraction:.6f} < {contract['minimum_rock']:.6f}"
            )
        if rock_fraction > contract["maximum_rock"]:
            contract_failures.append(
                f"{key} exposed rock regressed to a broad slab: "
                f"{rock_fraction:.6f} > {contract['maximum_rock']:.6f}"
            )
    if contract_failures:
        raise AssertionError(
            "; ".join(contract_failures)
            + "; actual "
            + ", ".join(contract_metrics)
        )
    return material


def transformed_material_tile(
    source: Image.Image,
    height_source: Image.Image,
    mip: int,
    tile_x: int,
    tile_y: int,
) -> np.ndarray:
    scale = (2**mip) * source.width / SOURCE_W
    x_offset = (tile_x * TILE_SIZE - BORDER_SIZE) * scale
    y_offset = (tile_y * TILE_SIZE - BORDER_SIZE) * scale
    tile = source.transform(
        (STORED_TILE_SIZE, STORED_TILE_SIZE),
        Image.Transform.AFFINE,
        (scale, 0.0, x_offset, 0.0, scale, y_offset),
        resample=Image.Resampling.NEAREST,
        fillcolor=0,
    )
    material = np.asarray(tile, dtype=np.uint16).copy()
    # Vanilla's material cache, like its height cache, contains native virtual-
    # texture detail absent from the coarse 8192-wide source. Keep every
    # authored material logic, but let the physical cache relief select
    # connected exposed faces at close and medium LOD. Height and slope are
    # sufficient authorities even where the coarse material source was green;
    # their thresholds cannot paint an ordinary lowland or source gap as a
    # mountain.
    if mip > 3:
        return material

    height = transformed_height_tile(
        height_source,
        mip,
        tile_x,
        tile_y,
    ).astype(np.float32)
    step = float(2**mip)
    rise_x = np.abs(height[:, 2:] - height[:, :-2]) / (2.0 * step)
    rise_y = np.abs(height[2:, :] - height[:-2, :]) / (2.0 * step)
    slope = np.zeros(height.shape, dtype=np.float32)
    slope[:, 1:-1] = np.maximum(slope[:, 1:-1], rise_x)
    slope[1:-1, :] = np.maximum(slope[1:-1, :], rise_y)

    dark_support = (
        material & (MATERIAL_DARK_ROCK | MATERIAL_ROCK | MATERIAL_SNOW)
    ) != 0
    rock_support = (material & (MATERIAL_ROCK | MATERIAL_SNOW)) != 0
    snow_support = (material & MATERIAL_SNOW) != 0
    # Physical height is itself the audited range envelope. Requiring the
    # coarse material bit again left more than 97% of Dunharrow green even on
    # steep faces. Let physical high terrain expose dark rock directly, then
    # reserve lighter rock/snow for the stronger face and source predicates.
    dark_face = (height >= 20_000.0) & (
        (slope >= 90.0) | (height >= 28_000.0)
    )
    volcanic_only = dark_support & ~rock_support
    rock_face = (height >= 26_000.0) & (
        (slope >= 120.0) | (height >= 34_000.0)
    ) & (~volcanic_only | rock_support)
    snow_face = snow_support & (height >= 39_000.0) & (
        (slope >= 155.0) | (height >= 48_000.0)
    )
    snow_core = snow_support & (height >= 52_000.0)
    fixed_channels = material & np.uint16(0x03FF)
    material[dark_face] = (
        fixed_channels[dark_face] | MATERIAL_EARTH | MATERIAL_DARK_ROCK
    )
    material[rock_face] = (
        fixed_channels[rock_face] | MATERIAL_DARK_ROCK | MATERIAL_ROCK
    )
    material[snow_face] = (
        fixed_channels[snow_face] | MATERIAL_ROCK | MATERIAL_SNOW
    )
    material[snow_core] = fixed_channels[snow_core] | MATERIAL_SNOW
    return material


def material_preview(values: np.ndarray) -> Image.Image:
    reduced = np.asarray(
        Image.fromarray(values).resize((1_024, 512), Image.Resampling.NEAREST),
        dtype=np.uint16,
    )
    rgb = np.zeros((512, 1_024, 3), dtype=np.uint8)
    rgb[:] = (26, 47, 58)
    colors = (
        (MATERIAL_GRASS, (86, 119, 65)),
        (MATERIAL_EARTH, (122, 91, 58)),
        (MATERIAL_DARK_ROCK, (55, 51, 49)),
        (MATERIAL_ROCK, (112, 108, 101)),
        (MATERIAL_SNOW, (224, 229, 225)),
        (MATERIAL_SAND, (174, 143, 83)),
        (MATERIAL_TUNDRA, (91, 94, 89)),
        (MATERIAL_STEPPE, (151, 116, 69)),
    )
    for bit, color in colors:
        rgb[(reduced & bit) != 0] = color
    coast = (reduced & MATERIAL_COAST_TRANSITION) != 0
    rgb[coast] = (154, 142, 105)
    rivers = (reduced & MATERIAL_RIVER) != 0
    rgb[rivers] = (55, 104, 127)
    return Image.fromarray(rgb, "RGB")


def write_height_layer() -> dict[str, int]:
    started = time.monotonic()
    bin_path = CACHE_OUT / "heightmap.bin"
    info_path = CACHE_OUT / "heightmap.info"
    temp_bin = bin_path.with_suffix(".bin.tmp")
    entries: list[tuple[int, int]] = []
    dedup: dict[bytes, tuple[int, int]] = {}
    unique_tiles = 0
    written_tiles = 0
    total_tiles = tile_count()

    with Image.open(HEIGHT_SOURCE) as opened:
        # PIL's I;16 affine resampler truncates the high byte.  Float mode is
        # required to preserve the authored 16-bit height range.
        source = opened.convert("F")
        with temp_bin.open("wb") as output:
            for mip, tile_x, tile_y in engine_tile_sequence():
                payload = png_bytes(
                    transformed_height_tile(source, mip, tile_x, tile_y)
                )
                key = hashlib.blake2b(payload, digest_size=16).digest()
                known = dedup.get(key)
                if known is None:
                    offset = output.tell()
                    output.write(payload)
                    known = (offset, len(payload))
                    dedup[key] = known
                    unique_tiles += 1
                entries.append(known)
                written_tiles += 1
                if written_tiles % 8_192 == 0:
                    print(
                        "gen_terrain_cache: height "
                        f"{written_tiles:,}/{total_tiles:,} tiles, "
                        f"{unique_tiles:,} unique",
                        flush=True,
                    )
    temp_bin.replace(bin_path)
    write_info(info_path, entries, scalar_fields=True)
    print(
        "gen_terrain_cache: height complete "
        f"({written_tiles:,} tiles, {unique_tiles:,} unique, "
        f"{bin_path.stat().st_size / 1_000_000:.1f} MB) in "
        f"{time.monotonic() - started:.1f}s",
        flush=True,
    )
    return {"tiles": written_tiles, "unique_tiles": unique_tiles}


def write_material_layer() -> dict[str, int | float]:
    started = time.monotonic()
    bin_path = CACHE_OUT / "materials.bin"
    info_path = CACHE_OUT / "materials.info"
    temp_bin = bin_path.with_suffix(".bin.tmp")
    entries: list[tuple[int, int]] = []
    dedup: dict[bytes, tuple[int, int]] = {}
    unique_tiles = 0
    written_tiles = 0
    total_tiles = tile_count()
    values = render_material_source()
    nonzero_fraction = float(np.count_nonzero(values)) / values.size
    DERIVED.mkdir(parents=True, exist_ok=True)
    material_preview(values).save(MATERIAL_PREVIEW_OUT, compress_level=9)

    source = Image.fromarray(values)
    with Image.open(HEIGHT_SOURCE) as opened_height:
        height_source = opened_height.convert("F")
        with temp_bin.open("wb") as output:
            for mip, tile_x, tile_y in engine_tile_sequence():
                payload = png_bytes(
                    transformed_material_tile(
                        source,
                        height_source,
                        mip,
                        tile_x,
                        tile_y,
                    )
                )
                key = hashlib.blake2b(payload, digest_size=16).digest()
                known = dedup.get(key)
                if known is None:
                    offset = output.tell()
                    output.write(payload)
                    known = (offset, len(payload))
                    dedup[key] = known
                    unique_tiles += 1
                entries.append(known)
                written_tiles += 1
                if written_tiles % 8_192 == 0:
                    print(
                        "gen_terrain_cache: materials "
                        f"{written_tiles:,}/{total_tiles:,} tiles, "
                        f"{unique_tiles:,} unique",
                        flush=True,
                    )
    temp_bin.replace(bin_path)
    write_info(info_path, entries, scalar_fields=True)
    print(
        "gen_terrain_cache: materials complete "
        f"({written_tiles:,} tiles, {unique_tiles:,} unique, "
        f"{bin_path.stat().st_size / 1_000_000:.1f} MB) in "
        f"{time.monotonic() - started:.1f}s",
        flush=True,
    )
    return {
        "tiles": written_tiles,
        "unique_tiles": unique_tiles,
        "nonzero_fraction": nonzero_fraction,
    }


def reusable_height_stats(height_source_hash: str) -> dict[str, int] | None:
    """Keep a verified current-order height bake while replacing materials."""
    try:
        manifest = json.loads(MANIFEST_OUT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if (
        manifest.get("generator_version") not in HEIGHT_FORMAT_COMPATIBLE_VERSIONS
        or manifest.get("source_sha256") != height_source_hash
        or manifest.get("tile_order")
        != "fine_to_coarse_row_major_y_inverted"
        or manifest.get("height_quantum") != HEIGHT_QUANTUM
    ):
        return None
    info_path = CACHE_OUT / "heightmap.info"
    bin_path = CACHE_OUT / "heightmap.bin"
    if not info_path.is_file() or not bin_path.is_file():
        return None
    entries = parse_entries(info_path)
    if len(entries) != tile_count():
        return None
    payload_size = bin_path.stat().st_size
    if any(
        offset < 0 or size <= 0 or offset + size > payload_size
        for offset, size in entries
    ):
        return None
    record = manifest.get("outputs", {}).get("heightmap.bin", {})
    if (
        record.get("bytes") != payload_size
        or record.get("sha256") != sha256(bin_path)
    ):
        return None
    print("gen_terrain_cache: reusing verified Arda height cache")
    return {
        "tiles": len(entries),
        "unique_tiles": len(set(entries)),
    }


def migrate_legacy_height_order(height_source_hash: str) -> dict[str, int] | None:
    """Re-index an already baked payload without recompressing it."""
    try:
        manifest = json.loads(MANIFEST_OUT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    legacy_version = manifest.get("generator_version")
    if legacy_version not in {1, 2, 3, 4, 5} or manifest.get("source_sha256") != height_source_hash:
        return None

    info_path = CACHE_OUT / "heightmap.info"
    bin_path = CACHE_OUT / "heightmap.bin"
    if not info_path.is_file() or not bin_path.is_file():
        return None
    old_entries = parse_entries(info_path)
    if len(old_entries) != tile_count():
        return None

    # v1 emitted fine-first row-major groups; v2 used coarse-first row-major
    # groups; v3 used coarse-first Morton groups; v4 used one global pre-order
    # tree; v5 used fine-first Morton groups. Reassembling retail cache tiles
    # proves the actual contract: fine-first row-major info entries whose
    # source rows run bottom-to-top.
    by_coordinate: dict[tuple[int, int, int], tuple[int, int]] = {}
    if legacy_version == 4:
        by_coordinate.update(
            dict(zip(preorder_tile_sequence(), old_entries, strict=True))
        )
    elif legacy_version == 5:
        by_coordinate.update(
            dict(zip(morton_tile_sequence(), old_entries, strict=True))
        )
    else:
        cursor = 0
        legacy_layout = (
            pyramid_layout()
            if legacy_version == 1
            else list(reversed(pyramid_layout()))
        )
        for mip, tiles_x, tiles_y in legacy_layout:
            count = tiles_x * tiles_y
            group = old_entries[cursor : cursor + count]
            if legacy_version in {1, 2}:
                coordinates = [
                    (x, y)
                    for y in range(tiles_y)
                    for x in range(tiles_x)
                ]
            else:
                coordinates = morton_coordinates(tiles_x, tiles_y)
            by_coordinate.update(
                {
                    (mip, x, y): entry
                    for (x, y), entry in zip(
                        coordinates, group, strict=True
                    )
                }
            )
            cursor += count
    reordered = [
        by_coordinate[(mip, x, y)]
        for mip, x, y in engine_tile_sequence()
    ]
    write_info(info_path, reordered, scalar_fields=True)
    print(
        f"gen_terrain_cache: migrated v{legacy_version} height index to "
        "fine-to-coarse row-major order with inverted source Y",
        flush=True,
    )
    return {
        "tiles": len(reordered),
        "unique_tiles": len(set(reordered)),
    }


def write_quadtree() -> None:
    path = CACHE_OUT / "quadtree_nodes.bin"
    header = struct.pack(
        "<5I",
        QUADTREE_DEPTH,
        QUADTREE_RECORDS,
        QUADTREE_LEAF_OFFSET,
        QUADTREE_FLAGS,
        QUADTREE_DIMENSIONS,
    )
    expected_size = (
        QUADTREE_HEADER_SIZE + QUADTREE_RECORDS * QUADTREE_RECORD_SIZE
    )
    with path.open("wb") as output:
        output.write(header)
        output.seek(expected_size - 1)
        output.write(b"\0")


def output_paths() -> list[Path]:
    return [
        CACHE_OUT / "heightmap.bin",
        CACHE_OUT / "heightmap.info",
        CACHE_OUT / "index_map.bin",
        CACHE_OUT / "index_map.info",
        CACHE_OUT / "intensity_map.bin",
        CACHE_OUT / "intensity_map.info",
        CACHE_OUT / "materials.bin",
        CACHE_OUT / "materials.info",
        CACHE_OUT / "quadtree_nodes.bin",
        CACHE_OUT / "checksum.json",
    ]


def write() -> None:
    CACHE_OUT.mkdir(parents=True, exist_ok=True)
    height_source_hash = sha256(HEIGHT_SOURCE)
    material_sources = material_source_hashes()
    existing_failures = check(quiet=True)
    if not existing_failures:
        print("gen_terrain_cache: current cache already matches its source")
        return

    height_stats = reusable_height_stats(height_source_hash)
    if height_stats is None:
        height_stats = migrate_legacy_height_order(height_source_hash)
    if height_stats is None:
        height_stats = write_height_layer()
    material_stats = write_material_layer()
    write_sparse_layer(
        "index_map", scalar_fields=False, shared=None
    )
    write_sparse_layer(
        "intensity_map", scalar_fields=False, shared=None
    )
    write_quadtree()

    checksum_seed = bytes.fromhex(height_source_hash) + b"".join(
        bytes.fromhex(value)
        for value in material_sources.values()
    )
    checksum = zlib.crc32(checksum_seed) & 0xFFFFFFFF
    (CACHE_OUT / "checksum.json").write_text(
        json.dumps(
            {
                "total": checksum,
                "decals": 0,
                "decal_sets": [],
            },
            indent="\t",
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    manifest = {
        "generator": "gen_terrain_cache.py",
        "generator_version": GENERATOR_VERSION,
        "source": str(HEIGHT_SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": height_source_hash,
        "source_resolution": [SOURCE_W, SOURCE_H],
        "tile_size": TILE_SIZE,
        "border_size": BORDER_SIZE,
        "tile_order": "fine_to_coarse_row_major_y_inverted",
        "height_quantum": HEIGHT_QUANTUM,
        "material_resolution": [MATERIAL_W, MATERIAL_H],
        "material_sources": material_sources,
        "mip_layout": [
            [mip, width, height]
            for mip, width, height in pyramid_layout()
        ],
        "tile_count": tile_count(),
        "height_unique_tiles": height_stats["unique_tiles"],
        "material_unique_tiles": material_stats["unique_tiles"],
        "material_nonzero_fraction": material_stats["nonzero_fraction"],
        "earth_decal_layers": 0,
        "material_preview": {
            "path": str(MATERIAL_PREVIEW_OUT.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "bytes": MATERIAL_PREVIEW_OUT.stat().st_size,
            "sha256": sha256(MATERIAL_PREVIEW_OUT),
        },
        "outputs": {
            path.name: {
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in output_paths()
        },
    }
    MANIFEST_OUT.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        "gen_terrain_cache: wrote self-contained ENDÓRË cache "
        f"({sum(path.stat().st_size for path in output_paths()) / 1_000_000:.1f} MB)"
    )


def parse_entries(path: Path) -> list[tuple[int, int]]:
    text = path.read_text(encoding="utf-8")
    return [
        (int(offset), int(size))
        for offset, size in re.findall(
            r"offset=(-?\d+)\s+size=(-?\d+)", text
        )
    ]


def check_info(
    stem: str,
    *,
    scalar_fields: bool,
    sparse: bool,
    failures: list[str],
) -> None:
    info_path = CACHE_OUT / f"{stem}.info"
    bin_path = CACHE_OUT / f"{stem}.bin"
    if not info_path.is_file() or not bin_path.is_file():
        failures.append(f"missing {stem} cache pair")
        return
    text = info_path.read_text(encoding="utf-8")
    if not text.startswith(INFO_HEADER):
        failures.append(f"{stem}.info has the wrong virtual-texture header")
    if scalar_fields and SCALAR_INFO_FIELDS not in text:
        failures.append(f"{stem}.info lacks scalar layer fields")
    entries = parse_entries(info_path)
    if len(entries) != tile_count():
        failures.append(
            f"{stem}.info has {len(entries):,} tiles, expected {tile_count():,}"
        )
        return
    payload_size = bin_path.stat().st_size
    if sparse:
        if payload_size != 0 or any(entry != (-1, -1) for entry in entries):
            failures.append(f"{stem} is not an explicitly empty decal layer")
        return
    for offset, size in entries:
        if offset < 0 or size <= 0 or offset + size > payload_size:
            failures.append(f"{stem}.info contains an invalid tile span")
            break


def check(*, quiet: bool = False) -> list[str]:
    failures: list[str] = []
    if not HEIGHT_SOURCE.is_file():
        return ["missing authored terrain height source"]
    for path in (BIOME_CONTROL, PROJECTION_CONTROL):
        if not path.is_file():
            return [
                "missing authored material source "
                f"{path.relative_to(ROOT)}"
            ]
    if not MANIFEST_OUT.is_file():
        return ["missing terrain cache manifest"]
    try:
        manifest = json.loads(MANIFEST_OUT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"invalid terrain cache manifest: {error}"]
    if manifest.get("generator_version") != GENERATOR_VERSION:
        failures.append("terrain cache generator version is stale")
    if manifest.get("height_quantum") != HEIGHT_QUANTUM:
        failures.append("terrain cache height quantum is stale")
    if manifest.get("tile_order") != "fine_to_coarse_row_major_y_inverted":
        failures.append("terrain cache manifest has the wrong tile order")
    if manifest.get("source_sha256") != sha256(HEIGHT_SOURCE):
        failures.append("terrain cache does not match the authored height source")
    if manifest.get("material_resolution") != [MATERIAL_W, MATERIAL_H]:
        failures.append("terrain cache has the wrong material source resolution")
    if manifest.get("material_sources") != material_source_hashes():
        failures.append("terrain cache does not match its Arda material sources")
    if manifest.get("tile_count") != tile_count():
        failures.append("terrain cache manifest has the wrong tile count")
    if manifest.get("earth_decal_layers") != 0:
        failures.append("terrain cache manifest permits inherited Earth decals")
    if int(manifest.get("material_unique_tiles", 0)) < 100:
        failures.append("terrain cache lacks varied authored material tiles")
    material_fraction = float(
        manifest.get("material_nonzero_fraction", 0.0)
    )
    if not 0.35 < material_fraction < 0.90:
        failures.append(
            "terrain material coverage is implausible "
            f"({material_fraction:.3f})"
        )

    check_info(
        "heightmap",
        scalar_fields=True,
        sparse=False,
        failures=failures,
    )
    check_info(
        "materials",
        scalar_fields=True,
        sparse=False,
        failures=failures,
    )
    check_info(
        "index_map",
        scalar_fields=False,
        sparse=True,
        failures=failures,
    )
    check_info(
        "intensity_map",
        scalar_fields=False,
        sparse=True,
        failures=failures,
    )

    materials_bin = CACHE_OUT / "materials.bin"
    if materials_bin.is_file():
        if materials_bin.stat().st_size < 1_000_000:
            failures.append("materials.bin is still an empty placeholder layer")
        elif materials_bin.stat().st_size >= 95_000_000:
            failures.append(
                "materials.bin exceeds the repository's 95 MB safety budget"
            )

    preview_record = manifest.get("material_preview", {})
    if not MATERIAL_PREVIEW_OUT.is_file():
        failures.append("missing authored terrain-material preview")
    elif (
        preview_record.get("bytes") != MATERIAL_PREVIEW_OUT.stat().st_size
        or preview_record.get("sha256") != sha256(MATERIAL_PREVIEW_OUT)
    ):
        failures.append("terrain-material preview differs from its manifest")

    outputs = manifest.get("outputs", {})
    for path in output_paths():
        if not path.is_file():
            failures.append(f"missing {path.name}")
            continue
        record = outputs.get(path.name, {})
        if record.get("bytes") != path.stat().st_size:
            failures.append(f"{path.name} size differs from its manifest")
        elif record.get("sha256") != sha256(path):
            failures.append(f"{path.name} hash differs from its manifest")

    quadtree = CACHE_OUT / "quadtree_nodes.bin"
    expected_quadtree_size = (
        QUADTREE_HEADER_SIZE + QUADTREE_RECORDS * QUADTREE_RECORD_SIZE
    )
    if quadtree.is_file():
        with quadtree.open("rb") as stream:
            header = stream.read(QUADTREE_HEADER_SIZE)
        expected_header = struct.pack(
            "<5I",
            QUADTREE_DEPTH,
            QUADTREE_RECORDS,
            QUADTREE_LEAF_OFFSET,
            QUADTREE_FLAGS,
            QUADTREE_DIMENSIONS,
        )
        if quadtree.stat().st_size != expected_quadtree_size:
            failures.append("quadtree_nodes.bin has the wrong size")
        elif header != expected_header:
            failures.append("quadtree_nodes.bin has the wrong generic-tree header")

    if not quiet:
        if failures:
            for failure in failures:
                print(f"gen_terrain_cache: FAIL {failure}")
        else:
            print(
                "gen_terrain_cache: PASS "
                f"({tile_count():,} indexed tiles, Arda material paint, "
                "zero Earth decal layers)"
            )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        write()
        return 0
    return 1 if check() else 0


if __name__ == "__main__":
    raise SystemExit(main())
