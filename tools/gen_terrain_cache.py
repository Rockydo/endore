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
from m2_controls import land_mask, natural_path, source_zone_mask
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
GENERATOR_VERSION = 29
HEIGHT_FORMAT_COMPATIBLE_VERSIONS = frozenset(
    {17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29}
)

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
MATERIAL_VEGETATION_TRANSITION = np.uint16(1 << 8)
MATERIAL_CLIMATE_TRANSITION = np.uint16(1 << 9)
MATERIAL_GRASS = np.uint16(1 << 10)
MATERIAL_EARTH = np.uint16(1 << 11)
MATERIAL_DARK_ROCK = np.uint16(1 << 12)
MATERIAL_ROCK = np.uint16(1 << 13)
MATERIAL_SNOW = np.uint16(1 << 14)
MATERIAL_SAND = np.uint16(1 << 15)
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
    values = np.clip(np.asarray(tile, dtype=np.float32), 0, 65_535).astype(
        np.uint16
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


def ridge_material_weight(projection: dict) -> np.ndarray:
    """Return organic source-crest exposure without location-cell geometry.

    Height remains the authority for physical relief. This companion field
    only tells the material painter where a source-aligned chain or named
    summit can plausibly expose rock. Broad blurred bodies prevent binary
    height/slope contours from becoming disconnected grey ribbons, while a
    narrower spine retains readable crests at regional zoom.
    """

    result = np.zeros((MATERIAL_H, MATERIAL_W), dtype=np.float32)

    def path_field(
        points: list[list[float]],
        *,
        key: str,
        width: int,
        strength: float,
        wander: float,
    ) -> None:
        path = natural_path(
            points,
            (MATERIAL_W, MATERIAL_H),
            key=key,
            closed=False,
            amplitude=wander,
            spacing=0.003,
        )
        body = Image.new("L", (MATERIAL_W, MATERIAL_H), 0)
        ImageDraw.Draw(body).line(
            path,
            fill=255,
            width=max(3, round(width * 2.15)),
            joint="curve",
        )
        body = body.filter(
            ImageFilter.GaussianBlur(radius=max(2, round(width * 0.72)))
        )
        spine = Image.new("L", (MATERIAL_W, MATERIAL_H), 0)
        ImageDraw.Draw(spine).line(
            path,
            fill=255,
            width=max(2, round(width * 0.58)),
            joint="curve",
        )
        spine = spine.filter(
            ImageFilter.GaussianBlur(radius=max(1, round(width * 0.20)))
        )
        field = np.maximum(
            np.asarray(body, dtype=np.float32) * 0.62,
            np.asarray(spine, dtype=np.float32),
        )
        np.maximum(result, field / 255.0 * strength, out=result)

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
        )
        for branch_index, branch in enumerate(ridge.get("branches", [])):
            path_field(
                branch,
                key=f"ridge:{ridge['key']}:branch:{branch_index}",
                width=max(3, round(width * 0.72)),
                strength=strength * 0.72,
                wander=wander,
            )

    for peak in projection.get("named_peaks", []):
        x = round(float(peak["center"][0]) * (MATERIAL_W - 1))
        y = round(float(peak["center"][1]) * (MATERIAL_H - 1))
        radius = max(3, round(float(peak["radius"]) * MATERIAL_H))
        image = Image.new("L", (MATERIAL_W, MATERIAL_H), 0)
        ImageDraw.Draw(image).ellipse(
            (
                x - round(radius * 1.45),
                y - round(radius * 1.45),
                x + round(radius * 1.45),
                y + round(radius * 1.45),
            ),
            fill=255,
        )
        image = image.filter(
            ImageFilter.GaussianBlur(radius=max(2, round(radius * 0.62)))
        )
        field = (
            np.asarray(image, dtype=np.float32)
            / 255.0
            * float(peak["strength"])
        )
        np.maximum(result, field, out=result)

    return np.clip(result, 0.0, 1.0)


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
        nominal = max(2.0, float(river["width"]) * MATERIAL_H * 0.62)
        segments = len(points) - 1
        for index, (start, end) in enumerate(zip(points, points[1:])):
            progress = (index + 0.5) / segments
            width = max(2, round(nominal * (0.42 + progress * 0.58)))
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

    # Climate envelopes are continuous material weights. Painting their
    # integer control IDs directly produced ruler-straight Harad boundaries
    # and hard green islands in Mordor. Broad feathering preserves the
    # source-aligned macro envelope while noise breaks the transition into
    # natural tongues instead of location-sized patches.
    steppe_weight = smoothed_biome_weight(
        control_biomes, (9,), radius=44.0
    )
    steppe_score = selector + steppe_weight * 82.0
    steppe_active = (steppe_weight > 0.025) & land
    steppe_blend = steppe_active & (
        (steppe_score >= 142.0) & (steppe_score < 174.0)
    )
    steppe_earth = steppe_active & (steppe_score >= 174.0)
    material[steppe_blend] = MATERIAL_GRASS | MATERIAL_EARTH
    material[steppe_earth] = MATERIAL_EARTH

    arid_weight = smoothed_biome_weight(
        control_biomes, (10,), radius=72.0
    )
    arid_score = arid_weight * 255.0 + (selector - 127.5) * 0.34
    arid_active = (arid_weight > 0.025) & land
    arid_earth = arid_active & (arid_score < 108.0)
    arid_blend = arid_active & (
        (arid_score >= 108.0) & (arid_score < 174.0)
    )
    arid_sand = arid_active & (arid_score >= 174.0)
    material[arid_earth] = MATERIAL_EARTH
    material[arid_blend] = MATERIAL_EARTH | MATERIAL_SAND
    material[arid_sand] = MATERIAL_SAND

    ash_weight = smoothed_biome_weight(
        control_biomes, (8,), radius=42.0
    )
    ash_score = ash_weight * 255.0 + (selector - 127.5) * 0.30
    ash_active = (ash_weight > 0.025) & land
    ash_earth = ash_active & (ash_score < 112.0)
    ash_dark = ash_active & (
        (ash_score >= 112.0) & (ash_score < 205.0)
    )
    ash_rock = ash_active & (ash_score >= 205.0)
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
    crest_weight = ridge_material_weight(projection)
    organic_weight = (selector - 127.5) / 127.5
    exposure = (
        crest_weight * 0.52
        + height_weight * 0.36
        + slope_weight * 0.34
        + organic_weight * 0.10
    )
    highland = land & (height >= 30_000) & (ash_weight < 0.62)
    highland_grass_earth = highland & (height < 38_000)
    highland_earth = highland & (height >= 38_000)
    highland_dark = (
        highland & (height >= 43_000) & (exposure >= 0.66)
    )
    highland_blend = (
        highland & (height >= 49_000) & (exposure >= 0.78)
    )
    highland_rock = (
        highland & (height >= 54_000) & (exposure >= 0.88)
    )
    material[highland_grass_earth] = MATERIAL_GRASS | MATERIAL_EARTH
    material[highland_earth] = MATERIAL_EARTH
    material[highland_dark] = MATERIAL_EARTH | MATERIAL_DARK_ROCK
    material[highland_blend] = MATERIAL_DARK_ROCK | MATERIAL_ROCK
    material[highland_rock] = MATERIAL_ROCK

    # Snow is the most selective crest material. It follows source-aligned
    # exposure plus actual altitude rather than a mountain-class footprint.
    crest = land & (ash_weight < 0.62)
    rock_snow = crest & (
        (height >= 58_000) & (exposure >= 0.84)
    )
    snow = crest & (height >= 62_000) & (exposure >= 0.91)
    material[rock_snow] = MATERIAL_ROCK | MATERIAL_SNOW
    material[snow] = MATERIAL_SNOW

    volcanic_highland = (
        land & (height >= 30_000) & (ash_weight >= 0.62)
    )
    material[volcanic_highland] = MATERIAL_DARK_ROCK

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
    # vegetation/climate transition bits are therefore neither necessary nor
    # safe: live evidence showed that they override semantic surface bits with
    # ochre and green islands. Continuous weights above own all dry blends.

    rivers = river_material_mask(projection) & land
    material[rivers] |= MATERIAL_RIVER

    if np.any(material[land] == 0):
        raise AssertionError("material paint leaves land without a variation channel")
    if np.any(material[water & ~outer_coast] != 0):
        raise AssertionError("material paint leaks into open water")
    return material


def transformed_material_tile(
    source: Image.Image,
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
    return np.asarray(tile, dtype=np.uint16)


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
    )
    for bit, color in colors:
        rgb[(reduced & bit) != 0] = color
    coast = (reduced & MATERIAL_COAST_TRANSITION) != 0
    rgb[coast] = (154, 142, 105)
    transition = (reduced & MATERIAL_VEGETATION_TRANSITION) != 0
    rgb[transition] = (
        rgb[transition].astype(np.uint16) * 3 // 4
        + np.asarray((38, 66, 39), dtype=np.uint16) // 4
    ).astype(np.uint8)
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
    with temp_bin.open("wb") as output:
        for mip, tile_x, tile_y in engine_tile_sequence():
            payload = png_bytes(
                transformed_material_tile(source, mip, tile_x, tile_y)
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
