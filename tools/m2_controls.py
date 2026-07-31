#!/usr/bin/env python3
"""Render and validate the authored M2 Middle-earth projection controls."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "docs/world/control"
PROJECTION = CONTROL / "projection.json"
SETTLEMENTS = CONTROL / "settlements.csv"

BIOMES = {
    "ocean": 0,
    "temperate": 1,
    "forest": 2,
    "dense_forest": 3,
    "mountain": 4,
    "tundra": 5,
    "marsh": 6,
    "lake": 7,
    "ash": 8,
    "steppe": 9,
    "arid": 10,
}

PREVIEW_COLORS = {
    0: (39, 75, 97),
    1: (126, 145, 95),
    2: (70, 115, 72),
    3: (38, 83, 55),
    4: (128, 127, 120),
    5: (166, 175, 164),
    6: (83, 111, 91),
    7: (54, 100, 128),
    8: (91, 72, 62),
    9: (147, 139, 84),
    10: (174, 143, 94),
}

# Installed build 24187685 defines NJominiMap.WATERLEVEL as
# 32 * 0.08340625. Heightmap samples span that same normalized 0..32 world
# height, so the corresponding 16-bit shoreline threshold is about 5466.
# Keep ordinary lowlands comfortably above it even after river incision.
ENGINE_WATER_LEVEL_PERCENTAGE = 0.08340625
ENGINE_WATER_LEVEL_SAMPLE = round(65535 * ENGINE_WATER_LEVEL_PERCENTAGE)
LOWLAND_SOUTH_SAMPLE = 10500.0
LOWLAND_NORTH_SAMPLE = 13000.0
WATER_FLOOR_SAMPLE = 420.0
RIVER_INCISION_SAMPLE = 1450.0
# Keep physical foothills broad while reserving the snow/rock mountain
# topography template for isolated massif cores. The earlier 0.29 and 0.45
# thresholds both left continuous pale ridge segments at regional zoom.
# Physical relief extends across the whole authored massif, but the installed
# snow/rock mountain template is visually much louder than its vanilla-Europe
# counterpart. Reserve it for genuinely high crest islands; regional audit
# showed that 0.56 still painted broad white slabs through the White Mountains.
MOUNTAIN_BIOME_THRESHOLD = 0.68
# Source lakes smaller than one runtime location become deep location-shaped
# quarries when classified as engine water. Preserve every such source polygon
# as a wet material control over continuous physical land. The explicit set is
# cross-checked below against the current source-raster area threshold so a
# cartography update cannot silently change the policy.
MATERIAL_POND_MAX_SOURCE_PIXELS = 64
MATERIAL_POND_KEYS = frozenset(
    {
        "mirrormere",
        "minor_lake_04",
        "minor_lake_05",
        "minor_lake_06",
        "minor_lake_07",
        "minor_lake_10",
        "minor_lake_11",
        "minor_lake_12",
        "minor_lake_13",
        "minor_lake_14",
    }
)


@dataclass(frozen=True)
class Settlement:
    key: str
    name: str
    x: float
    y: float
    rank: str
    language: str
    realm_hint: str
    source: str


def load_projection() -> dict:
    return json.loads(PROJECTION.read_text(encoding="utf-8"))


def validate_geometry_contract(projection: dict) -> None:
    """Reject a return to primitive proof-map lakes, forests, or coasts."""

    if projection.get("schema") != 3:
        raise ValueError("projection controls must use cartography schema 3")
    if len(projection["land_polygons"]["mainland"]) < 500:
        raise ValueError("mainland coastline lacks source-audited multi-scale detail")
    for key, coords in projection["sea_cutouts"].items():
        if len(coords) < 12:
            raise ValueError(f"sea cutout {key} lacks bay/headland detail")
    if len(projection.get("mountain_zones", [])) < 30:
        raise ValueError("mountain atlas lacks source-audited range footprints")
    for lake in projection["lakes"]:
        if lake["shape"] not in {"organic_polygon", "source_polygon"}:
            raise ValueError(
                f"lake {lake['key']} regressed to primitive geometry"
            )
        if len(lake["coords"]) < 4:
            raise ValueError(f"lake {lake['key']} lacks shoreline detail")
    lake_keys = {lake["key"] for lake in projection["lakes"]}
    if not MATERIAL_POND_KEYS <= lake_keys:
        missing = sorted(MATERIAL_POND_KEYS - lake_keys)
        raise ValueError(f"material source ponds are missing: {missing}")
    for zone in projection["biome_zones"]:
        if zone["biome"] not in {"forest", "dense_forest"}:
            continue
        if zone["shape"] not in {
            "organic_polygon",
            "source_polygon",
            "multi_polygon",
        }:
            raise ValueError(
                f"forest {zone['key']} regressed to primitive geometry"
            )


def load_settlements() -> list[Settlement]:
    with SETTLEMENTS.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    expected = {
        "key", "name", "x", "y", "rank", "language", "realm_hint", "source"
    }
    if not rows or set(rows[0]) != expected:
        raise ValueError("settlements.csv header does not match the M2 control contract")
    result = [
        Settlement(
            key=row["key"],
            name=row["name"],
            x=float(row["x"]),
            y=float(row["y"]),
            rank=row["rank"],
            language=row["language"],
            realm_hint=row["realm_hint"],
            source=row["source"],
        )
        for row in rows
    ]
    if len({item.key for item in result}) != len(result):
        raise ValueError("duplicate settlement key")
    if len({item.name for item in result}) != len(result):
        raise ValueError("duplicate settlement name")
    return result


def point(value: list[float] | tuple[float, float], size: tuple[int, int]) -> tuple[int, int]:
    width, height = size
    return (
        round(float(value[0]) * (width - 1)),
        round(float(value[1]) * (height - 1)),
    )


def box(value: list[float], size: tuple[int, int]) -> tuple[int, int, int, int]:
    x0, y0 = point(value[:2], size)
    x1, y1 = point(value[2:], size)
    return x0, y0, x1, y1


def stable_seed(key: str) -> int:
    return int.from_bytes(
        hashlib.sha256(f"ENDORE|{key}|3018".encode("utf-8")).digest()[:8],
        "little",
    )


def natural_path(
    coords: list[list[float]],
    size: tuple[int, int],
    *,
    key: str,
    closed: bool,
    amplitude: float,
    spacing: float = 0.004,
) -> list[tuple[int, int]]:
    """Densify hand-authored geometry with deterministic sub-macro variation.

    The source vertices remain the binding large/medium geography. Several
    incommensurate periodic bands perturb only the intervening edge, avoiding
    both random-pixel noise and the primitive straight segments of the proof.
    """
    vertices = [
        np.array(
            [float(item[0]) * (size[0] - 1), float(item[1]) * (size[1] - 1)],
            dtype=np.float64,
        )
        for item in coords
    ]
    if closed:
        vertices.append(vertices[0])
    rng = np.random.default_rng(stable_seed(key))
    phase = rng.uniform(0.0, 2.0 * math.pi, 6)
    frequency = rng.uniform(
        (0.75, 1.55, 3.2, 6.5, 13.0, 27.0),
        (1.25, 2.45, 5.1, 10.5, 21.0, 43.0),
    )
    result: list[tuple[int, int]] = []
    pixel_spacing = max(2.0, spacing * size[1])
    amplitude_px = amplitude * size[1]
    segment_count = len(vertices) - 1
    for segment_index, (start, end) in enumerate(zip(vertices, vertices[1:])):
        delta = end - start
        length = float(np.linalg.norm(delta))
        if length < 0.5:
            continue
        normal = np.array([-delta[1], delta[0]], dtype=np.float64) / length
        steps = max(2, math.ceil(length / pixel_spacing))
        for index in range(steps):
            if segment_index and index == 0:
                continue
            t = index / steps
            global_t = (segment_index + t) / segment_count
            # Pin authored vertices exactly. Variation grows between them.
            envelope = math.sin(math.pi * t)
            wave = (
                0.43 * math.sin(2 * math.pi * frequency[0] * global_t + phase[0])
                + 0.24 * math.sin(2 * math.pi * frequency[1] * global_t + phase[1])
                + 0.14 * math.sin(2 * math.pi * frequency[2] * global_t + phase[2])
                + 0.09 * math.sin(2 * math.pi * frequency[3] * global_t + phase[3])
                + 0.06 * math.sin(2 * math.pi * frequency[4] * global_t + phase[4])
                + 0.04 * math.sin(2 * math.pi * frequency[5] * global_t + phase[5])
            )
            displaced = start + delta * t + normal * amplitude_px * envelope * wave
            result.append((round(displaced[0]), round(displaced[1])))
    result.append((round(vertices[-1][0]), round(vertices[-1][1])))
    return result


def draw_organic_polygon(
    image: Image.Image,
    coords: list[list[float]],
    size: tuple[int, int],
    *,
    key: str,
    fill: int,
    amplitude: float,
) -> None:
    ImageDraw.Draw(image).polygon(
        natural_path(
            coords,
            size,
            key=key,
            closed=True,
            amplitude=amplitude,
        ),
        fill=fill,
    )


def draw_shape(
    image: Image.Image,
    shape: str,
    coords: list,
    size: tuple[int, int],
    fill: int,
    *,
    key: str,
) -> None:
    draw = ImageDraw.Draw(image)
    if shape == "box":
        draw.rectangle(box(coords, size), fill=fill)
    elif shape == "ellipse":
        draw.ellipse(box(coords, size), fill=fill)
    elif shape == "polygon":
        draw.polygon([point(item, size) for item in coords], fill=fill)
    elif shape == "source_polygon":
        draw.polygon([point(item, size) for item in coords], fill=fill)
    elif shape == "multi_polygon":
        for polygon in coords:
            draw.polygon([point(item, size) for item in polygon], fill=fill)
    elif shape == "organic_polygon":
        amplitude = (
            0.0110
            if key.startswith("biome:")
            else 0.0080
            if key.startswith("lake:")
            else 0.0045
        )
        draw_organic_polygon(
            image,
            coords,
            size,
            key=key,
            fill=fill,
            amplitude=amplitude,
        )
    else:
        raise ValueError(f"unknown control shape {shape!r}")


def naturalize_forest_mask(
    image: Image.Image,
    *,
    key: str,
) -> Image.Image:
    """Break a hand-authored forest envelope into a natural, porous margin.

    The polygon remains the binding large form. A deterministic broad field
    feathers its edge, avoiding both an oval wall of trees and a hard vector
    boundary at close zoom. Glades belong to object placement so whole
    gameplay locations do not flip their base terrain.
    """

    size = image.size
    radius = max(5, round(size[1] * 0.006))
    softened = np.asarray(
        image.filter(ImageFilter.GaussianBlur(radius=radius)),
        dtype=np.float32,
    ) / 255.0
    rng = np.random.default_rng(stable_seed(f"forest-field:{key}"))
    broad = Image.fromarray(
        rng.integers(
            0,
            256,
            (max(16, size[1] // 24), max(32, size[0] // 24)),
            dtype=np.uint8,
        ),
        "L",
    ).resize(size, Image.Resampling.BICUBIC)
    broad_values = np.asarray(broad, dtype=np.float32) / 255.0
    active = softened + (broad_values - 0.5) * 0.48 > 0.50
    source = np.asarray(image, dtype=np.uint8) > 0
    # Source forests include narrow Ithilien woods and compact Chetwood/Old
    # Forest polygons. A broad feather alone can erase these legitimate small
    # features. Preserve their interiors and most source-covered cells while
    # leaving the procedural field responsible for porous outer margins.
    interior = np.asarray(
        image.filter(ImageFilter.MinFilter(5)),
        dtype=np.uint8,
    ) > 0
    active |= interior
    active |= source & (broad_values > 0.18)

    return Image.fromarray(active.astype(np.uint8) * 255, "L")


def relief_modulation(size: tuple[int, int]) -> np.ndarray:
    """Return broad and medium rock-mass variation for authored ridges."""

    rng = np.random.default_rng(stable_seed("ridge-relief-field"))
    broad = Image.fromarray(
        rng.integers(0, 256, (128, 256), dtype=np.uint8),
        "L",
    ).resize(size, Image.Resampling.BICUBIC)
    medium = Image.fromarray(
        rng.integers(0, 256, (384, 768), dtype=np.uint8),
        "L",
    ).resize(size, Image.Resampling.BICUBIC)
    values = (
        np.asarray(broad, dtype=np.float32) * 0.62
        + np.asarray(medium, dtype=np.float32) * 0.38
    ) / 255.0
    return 0.66 + values * 0.58


def land_mask(projection: dict, size: tuple[int, int]) -> Image.Image:
    image = Image.new("L", size, 0)
    polygons = projection["land_polygons"]
    # Schema-3 coastline vertices are already a detailed, source-audited
    # original control. Do not add the former large procedural wobble: it
    # displaced capes, estuaries, and the Gulf of Lune by tens of kilometres.
    draw_shape(
        image,
        "source_polygon",
        polygons["mainland"],
        size,
        255,
        key="coast:mainland",
    )
    for key, polygon in projection["sea_cutouts"].items():
        draw_organic_polygon(
            image,
            polygon,
            size,
            key=f"coast:{key}",
            fill=0,
            amplitude=0.0070,
        )
    # Offshore islands are independent landmasses and must be restored after
    # bays/gulfs carve the mainland; both Himling and Tolfalas sit inside the
    # broad authored water envelopes by design.
    for key, polygon in polygons.items():
        if key == "mainland":
            continue
        draw_shape(
            image,
            "source_polygon",
            polygon,
            size,
            255,
            key=f"island:{key}",
        )
    for lake in projection["lakes"]:
        if lake["key"] in MATERIAL_POND_KEYS:
            continue
        draw_shape(
            image,
            lake["shape"],
            lake["coords"],
            size,
            0,
            key=f"lake:{lake['key']}",
        )
    return image


def ridge_mask(projection: dict, size: tuple[int, int]) -> Image.Image:
    layers = np.zeros((size[1], size[0]), dtype=np.float32)

    def smooth_union(current: np.ndarray, addition: np.ndarray) -> np.ndarray:
        """Composite height envelopes without discrete max-band terraces."""

        current_unit = np.clip(current / 255.0, 0.0, 1.0)
        addition_unit = np.clip(addition / 255.0, 0.0, 1.0)
        return (1.0 - (1.0 - current_unit) * (1.0 - addition_unit)) * 255.0

    def blurred_path(
        path: list[tuple[int, int]],
        *,
        width: int,
        blur: int,
    ) -> np.ndarray:
        band = Image.new("L", size, 0)
        ImageDraw.Draw(band).line(
            path,
            fill=255,
            width=max(2, width),
            joint="curve",
        )
        return np.asarray(
            band.filter(ImageFilter.GaussianBlur(radius=max(1, blur))),
            dtype=np.float32,
        )

    # Arda Maps mountain polygons bind the full range footprint, but they are
    # foothill envelopes rather than flat summit plates. Earlier versions
    # lifted almost every polygon interior to 44-100% of the relief range;
    # the real renderer consequently showed broad grey mesas with circular
    # green pass holes. Keep the source footprint as low irregular mass and
    # let the source-aligned axes below carry the high ridges and summits.
    modulation = relief_modulation(size)
    for zone in projection.get("mountain_zones", []):
        mask = Image.new("L", size, 0)
        draw_shape(
            mask,
            zone["shape"],
            zone["coords"],
            size,
            255,
            key=f"mountain:{zone['key']}",
        )
        strength = float(zone["strength"])
        radius = max(2, round(size[1] * (0.0025 if strength > 0.8 else 0.0045)))
        softened = np.asarray(
            mask.filter(ImageFilter.GaussianBlur(radius=radius)),
            dtype=np.float32,
        ) / 255.0
        zone_field = (
            softened
            * strength
            * 255.0
            * (0.10 + 0.22 * modulation)
        )
        layers = smooth_union(layers, np.clip(zone_field, 0.0, 255.0))

    for ridge in projection["ridges"]:
        width = max(3, round(float(ridge["width"]) * size[1]))
        value = float(ridge["height"]) * 255.0
        path = natural_path(
            ridge["points"],
            size,
            key=f"ridge:{ridge['key']}",
            closed=False,
            amplitude=float(ridge.get("wander", 0.003)),
            spacing=0.003,
        )
        # Earlier versions stacked four independently blurred paths with
        # ``maximum``. Their transition shoulders became visible as parallel,
        # terraced contour bands in EU5's close renderer. Three overlapping
        # Gaussian envelopes instead form one continuously sloped massif:
        # low foothills, a steep folded body, and an irregular central spine,
        # with no discrete change in construction method at any radius. Live
        # theatre evidence rejected the former 5.4-width broad envelope: even
        # after polygon plateaus were removed it still read as a flat exposed-
        # rock field. Concentrate height into a visibly steep chain.
        broad = blurred_path(
            path,
            width=round(width * 3.2),
            blur=round(width * 0.95),
        )
        body = blurred_path(
            path,
            width=round(width * 1.6),
            blur=round(width * 0.45),
        )
        spine = blurred_path(
            path,
            width=round(width * 0.45),
            blur=round(width * 0.18),
        )
        massif = value * (
            0.18 * (broad / 255.0)
            + 0.40 * (body / 255.0)
            + 0.42 * (spine / 255.0)
        )
        # A mountain chain is a field of overlapping massifs, not a uniform
        # wall. Scatter low-amplitude off-axis shoulders along the authored
        # spine. Smooth-union composition prevents their blurred ellipses from
        # cutting visible rings into the main envelope.
        rng = np.random.default_rng(stable_seed(f"peaks:{ridge['key']}"))
        peaks = Image.new("L", size, 0)
        peak_draw = ImageDraw.Draw(peaks)
        stride = max(2, round(width * 0.25))
        for path_index in range(stride, len(path) - stride, stride):
            before = np.array(path[path_index - 1], dtype=np.float64)
            after = np.array(path[path_index + 1], dtype=np.float64)
            tangent = after - before
            tangent_length = float(np.linalg.norm(tangent))
            if tangent_length < 0.5:
                continue
            normal = np.array([-tangent[1], tangent[0]]) / tangent_length
            center = np.array(path[path_index], dtype=np.float64)
            center += normal * rng.uniform(-1.15, 1.15) * width
            radius_x = rng.uniform(0.30, 0.66) * width
            radius_y = rng.uniform(0.26, 0.60) * width
            peak_draw.ellipse(
                (
                    round(center[0] - radius_x),
                    round(center[1] - radius_y),
                    round(center[0] + radius_x),
                    round(center[1] + radius_y),
                ),
                fill=round(rng.uniform(150.0, 235.0)),
            )
        peaks = peaks.filter(
            ImageFilter.GaussianBlur(radius=max(2, round(width * 0.18)))
        )
        peak_values = np.asarray(peaks, dtype=np.float32) / 255.0
        massif += value * peak_values * 0.72
        layers = smooth_union(layers, np.clip(massif, 0.0, 255.0))
        for branch_index, branch in enumerate(ridge.get("branches", [])):
            branch_path = natural_path(
                branch,
                size,
                key=f"ridge:{ridge['key']}:branch:{branch_index}",
                closed=False,
                amplitude=float(ridge.get("wander", 0.0035)),
                spacing=0.003,
            )
            branch_body = blurred_path(
                branch_path,
                width=round(width * 1.30),
                blur=round(width * 0.42),
            )
            branch_spine = blurred_path(
                branch_path,
                width=round(width * 0.42),
                blur=round(width * 0.18),
            )
            branch_field = value * 0.58 * (
                0.68 * (branch_body / 255.0)
                + 0.32 * (branch_spine / 255.0)
            )
            layers = smooth_union(layers, branch_field)

    # Place lore-sensitive summits at their hash-pinned Arda Maps point
    # coordinates. Each field is a weighted blend of lumpy outer shoulders,
    # an offset body, and a compact source-centered core. This keeps the
    # canonical coordinate as the local maximum without stamping circular
    # cones or concentric rings into isolated hills.
    for peak in projection.get("named_peaks", []):
        x, y = point(peak["center"], size)
        radius = max(3, round(float(peak["radius"]) * size[1]))
        strength = float(peak["strength"])
        rng = np.random.default_rng(stable_seed(f"named-peak:{peak['key']}"))
        peak_field = np.zeros_like(layers)
        for scale, lobe_count, blur, weight, offset in (
            (1.65, 6, 0.72, 0.22, 0.65),
            (0.95, 5, 0.38, 0.38, 0.34),
            (0.42, 3, 0.18, 0.62, 0.10),
        ):
            lobe_image = Image.new("L", size, 0)
            lobe_draw = ImageDraw.Draw(lobe_image)
            for lobe_index in range(lobe_count):
                # The first core lobe is exactly source-centered. Other
                # shoulders wander locally but cannot move the summit anchor.
                if scale <= 0.42 and lobe_index == 0:
                    center_x, center_y = x, y
                else:
                    angle = rng.uniform(0.0, math.tau)
                    distance = rng.uniform(0.0, offset) * radius
                    center_x = x + math.cos(angle) * distance
                    center_y = y + math.sin(angle) * distance
                radius_x = radius * scale * rng.uniform(0.62, 1.18)
                radius_y = radius * scale * rng.uniform(0.62, 1.18)
                lobe_draw.ellipse(
                    (
                        round(center_x - radius_x),
                        round(center_y - radius_y),
                        round(center_x + radius_x),
                        round(center_y + radius_y),
                    ),
                    fill=255,
                )
            lobe_image = lobe_image.filter(
                ImageFilter.GaussianBlur(
                    radius=max(1, round(radius * blur))
                )
            )
            peak_field += (
                np.asarray(lobe_image, dtype=np.float32)
                * weight
                * strength
            )
        peak_field = np.clip(peak_field, 0.0, 255.0)
        layers = smooth_union(layers, peak_field)

    image = Image.fromarray(np.clip(layers, 0, 255).astype(np.uint8), "L")
    for pass_data in projection["passes"]:
        valley = Image.new("L", size, 0)
        x, y = point(pass_data["center"], size)
        radius = max(2, round(float(pass_data["radius"]) * size[1]))
        ImageDraw.Draw(valley).ellipse(
            (x - radius, y - radius, x + radius, y + radius),
            fill=230,
        )
        valley_array = np.asarray(
            valley.filter(ImageFilter.GaussianBlur(radius=max(2, radius // 2))),
            dtype=np.float32,
        ) / 255.0
        # A pass is a high saddle through a range, not a circular lowland
        # crater. Retain enough relief to keep the mountain mass continuous
        # while making the authored crossing visibly lower than its crests.
        layers = np.asarray(image, dtype=np.float32) * (1.0 - valley_array * 0.58)
        image = Image.fromarray(np.clip(layers, 0, 255).astype(np.uint8), "L")
    return image


def river_mask(projection: dict, size: tuple[int, int]) -> Image.Image:
    image = Image.new("L", size, 0)
    draw = ImageDraw.Draw(image)
    for river in projection["rivers"]:
        width = max(1, round(float(river["width"]) * size[1]))
        draw.line(
            natural_path(
                river["points"],
                size,
                key=f"river:{river['key']}",
                closed=False,
                amplitude=float(river.get("wander", 0.0015)),
                spacing=0.0025,
            ),
            fill=255,
            width=width,
            joint="curve",
        )
    return image


def render() -> tuple[dict[str, Image.Image], dict]:
    projection = load_projection()
    validate_geometry_contract(projection)
    settlements = load_settlements()
    size = tuple(int(value) for value in projection["control_resolution"])
    if len(size) != 2 or min(size) < 128:
        raise ValueError("invalid control resolution")
    canvas = tuple(int(value) for value in projection["canvas"])
    if canvas != (16384, 8192):
        raise ValueError(
            "M2 production canvas must match EU5's installed 16384x8192 contract"
        )

    lake_pixel_areas: dict[str, int] = {}
    for lake in projection["lakes"]:
        lake_mask = Image.new("L", size, 0)
        draw_shape(
            lake_mask,
            lake["shape"],
            lake["coords"],
            size,
            255,
            key=f"lake-area:{lake['key']}",
        )
        lake_pixel_areas[lake["key"]] = int(
            (np.asarray(lake_mask) > 0).sum()
        )
    threshold_pond_keys = {
        key
        for key, area in lake_pixel_areas.items()
        if area <= MATERIAL_POND_MAX_SOURCE_PIXELS
    }
    if threshold_pond_keys != MATERIAL_POND_KEYS:
        raise ValueError(
            "sub-location pond set changed without review: "
            f"source={sorted(threshold_pond_keys)} "
            f"contract={sorted(MATERIAL_POND_KEYS)}"
        )

    land = land_mask(projection, size)
    land_array = np.asarray(land) > 0
    ridges = ridge_mask(projection, size)
    ridge_array = np.clip(
        np.asarray(ridges, dtype=np.float32)
        / 255.0
        * relief_modulation(size),
        0.0,
        1.0,
    )
    ridges = Image.fromarray(np.round(ridge_array * 255.0).astype(np.uint8), "L")
    rivers = river_mask(projection, size)

    biome_image = Image.new("L", size, BIOMES["ocean"])
    biome = np.asarray(biome_image).copy()
    biome[land_array] = BIOMES["temperate"]
    for zone in projection["biome_zones"]:
        mask = Image.new("L", size, 0)
        draw_shape(
            mask,
            zone["shape"],
            zone["coords"],
            size,
            255,
            key=f"biome:{zone['key']}",
        )
        if zone["biome"] in {"forest", "dense_forest"}:
            mask = naturalize_forest_mask(mask, key=zone["key"])
        active = (np.asarray(mask) > 0) & land_array
        biome[active] = BIOMES[zone["biome"]]
    biome[
        (ridge_array > MOUNTAIN_BIOME_THRESHOLD) & land_array
    ] = BIOMES["mountain"]
    for lake in projection["lakes"]:
        mask = Image.new("L", size, 0)
        draw_shape(
            mask,
            lake["shape"],
            lake["coords"],
            size,
            255,
            key=f"lake:{lake['key']}",
        )
        biome[np.asarray(mask) > 0] = BIOMES["lake"]
    biome_image = Image.fromarray(biome.astype(np.uint8), "L")

    yy = np.linspace(0.0, 1.0, size[1], dtype=np.float32)[:, None]
    base_land = LOWLAND_SOUTH_SAMPLE + (
        1.0 - yy
    ) * (LOWLAND_NORTH_SAMPLE - LOWLAND_SOUTH_SAMPLE)
    elevation = np.where(land_array, base_land, WATER_FLOOR_SAMPLE)
    elevation += np.where(land_array, ridge_array * 36000.0, 0.0)
    river_blur = np.asarray(
        rivers.filter(ImageFilter.GaussianBlur(radius=max(1, size[1] // 240))),
        dtype=np.float32,
    ) / 255.0
    elevation = np.where(
        land_array,
        elevation - river_blur * RIVER_INCISION_SAMPLE,
        elevation,
    )
    # Orodruin is an isolated stratovolcano, not another blurred mountain
    # envelope. The former soft ellipse left only a shallow rise in the close
    # renderer. Build an asymmetric apron, a steep cone, and a summit crater
    # enclosed by a broken rim without moving the source-audited anchor.
    mount_doom = next(item for item in settlements if item.key == "mount_doom")
    px, py = point((mount_doom.x, mount_doom.y), size)
    doom_y, doom_x = np.ogrid[: size[1], : size[0]]
    doom_dx = doom_x.astype(np.float32) - float(px)
    doom_dy = doom_y.astype(np.float32) - float(py)
    doom_angle = np.arctan2(doom_dy, doom_dx)
    doom_distance = np.hypot(doom_dx, doom_dy)
    irregular_distance = doom_distance * (
        1.0
        + 0.075 * np.sin(doom_angle * 5.0 + 0.8)
        + 0.040 * np.sin(doom_angle * 11.0 - 0.35)
    )
    apron_radius = max(18.0, size[1] / 105.0)
    cone_radius = max(6.0, size[1] / 300.0)
    apron = np.power(
        np.clip(1.0 - irregular_distance / apron_radius, 0.0, 1.0),
        2.15,
    )
    cone = np.power(
        np.clip(1.0 - irregular_distance / cone_radius, 0.0, 1.0),
        1.32,
    )
    rim_radius = cone_radius * 0.31
    rim_width = max(0.75, cone_radius * 0.11)
    rim = np.exp(
        -np.square((doom_distance - rim_radius) / rim_width) * 0.5
    )
    crater = np.exp(
        -np.square(doom_distance / max(0.85, rim_radius * 0.58)) * 0.5
    )
    doom_relief = (
        apron * 7_500.0
        + cone * 40_000.0
        + rim * 6_000.0
        - crater * 14_000.0
    )
    elevation += np.where(land_array, doom_relief, 0.0)
    elevation = np.clip(elevation, 0, 65535).astype(np.uint16)
    material_pond_mask = (biome == BIOMES["lake"]) & land_array
    material_pond_pixels = int(material_pond_mask.sum())
    expected_material_pond_pixels = sum(
        lake_pixel_areas[key] for key in MATERIAL_POND_KEYS
    )
    if material_pond_pixels != expected_material_pond_pixels:
        raise ValueError(
            "sub-location source pond footprint changed without review: "
            f"{material_pond_pixels} != {expected_material_pond_pixels} pixels"
        )
    material_pond_height = [
        int(elevation[material_pond_mask].min()),
        int(elevation[material_pond_mask].max()),
    ]
    if material_pond_height[0] <= ENGINE_WATER_LEVEL_SAMPLE:
        raise ValueError("material pond terrain fell below the engine water plane")
    minimum_land_height = int(elevation[land_array].min())
    maximum_water_height = int(elevation[~land_array].max())
    if minimum_land_height <= ENGINE_WATER_LEVEL_SAMPLE:
        raise ValueError(
            "authored lowland falls below EU5's installed water level: "
            f"{minimum_land_height} <= {ENGINE_WATER_LEVEL_SAMPLE}"
        )
    if maximum_water_height >= ENGINE_WATER_LEVEL_SAMPLE:
        raise ValueError(
            "authored water rises above EU5's installed water level: "
            f"{maximum_water_height} >= {ENGINE_WATER_LEVEL_SAMPLE}"
        )
    elevation_image = Image.fromarray(elevation)

    density = np.full((size[1], size[0]), 18, dtype=np.uint8)
    density[land_array] = 135
    density[(biome == BIOMES["mountain"]) & land_array] = 28
    density[np.isin(biome, [BIOMES["forest"], BIOMES["dense_forest"]])] = 82
    density[biome == BIOMES["tundra"]] = 58
    density[biome == BIOMES["marsh"]] = 45
    density[biome == BIOMES["ash"]] = 70
    density[biome == BIOMES["arid"]] = 92
    for zone in projection["density_zones"]:
        mask = Image.new("L", size, 0)
        draw_shape(
            mask,
            zone["shape"],
            zone["coords"],
            size,
            255,
            key=f"density:{zone['key']}",
        )
        active = (np.asarray(mask) > 0) & land_array
        density[active] = np.maximum(density[active], int(zone["value"]))
    density_image = Image.fromarray(density, "L")

    for item in settlements:
        if not (0.0 <= item.x <= 1.0 and 0.0 <= item.y <= 1.0):
            raise ValueError(f"settlement {item.key} lies outside normalized canvas")
        sx, sy = point((item.x, item.y), size)
        if not land_array[sy, sx]:
            raise ValueError(f"settlement {item.key} lies outside authored land")
        if not item.source.strip():
            raise ValueError(f"settlement {item.key} lacks a canon source")

    preview_array = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    for biome_id, color in PREVIEW_COLORS.items():
        preview_array[biome == biome_id] = color
    preview = Image.fromarray(preview_array, "RGB")
    preview_draw = ImageDraw.Draw(preview)
    for river in projection["rivers"]:
        width = max(1, round(float(river["width"]) * size[1]))
        preview_draw.line(
            natural_path(
                river["points"],
                size,
                key=f"river:{river['key']}",
                closed=False,
                amplitude=float(river.get("wander", 0.0015)),
                spacing=0.0025,
            ),
            fill=(68, 132, 167),
            width=width,
            joint="curve",
        )
    for item in settlements:
        sx, sy = point((item.x, item.y), size)
        radius = 3 if item.rank in {"capital", "city", "fortress", "hold"} else 2
        color = (199, 164, 79) if item.rank != "ruin" else (128, 102, 75)
        preview_draw.ellipse(
            (sx - radius, sy - radius, sx + radius, sy + radius),
            fill=color,
            outline=(42, 34, 28),
        )

    source_hash = hashlib.sha256(
        PROJECTION.read_bytes() + b"\0" + SETTLEMENTS.read_bytes()
    ).hexdigest()
    land_y, land_x = np.where(land_array)
    land_bbox = [
        int(land_x.min()),
        int(land_y.min()),
        int(land_x.max()),
        int(land_y.max()),
    ]
    land_bbox_occupancy = [
        round((land_bbox[2] - land_bbox[0] + 1) / size[0], 6),
        round((land_bbox[3] - land_bbox[1] + 1) / size[1], 6),
    ]
    land_edge_contact = {
        "west": int(land_array[:, 0].sum()),
        "east": int(land_array[:, -1].sum()),
        "north": int(land_array[0, :].sum()),
        "south": int(land_array[-1, :].sum()),
    }
    # The equal-scale projection deliberately fills the north/south extent
    # while retaining honest western ocean and eastern margin. Stretching or
    # recentering it to make the playable land appear larger would either clip
    # Forochel/Far Harad or falsify physical distances.
    if land_bbox_occupancy[1] != 1.0:
        raise ValueError("equal-scale source no longer fills the vertical extent")
    if not 0.69 <= land_bbox_occupancy[0] <= 0.72:
        raise ValueError("equal-scale source width occupancy changed without review")
    if land_edge_contact["north"] < 1_500 or land_edge_contact["south"] < 1_400:
        raise ValueError("binding north/south source extent was clipped")
    if land_edge_contact["west"] or land_edge_contact["east"]:
        raise ValueError("binding western ocean/eastern margin was lost")
    images = {
        "coastline.png": land,
        "elevation.png": elevation_image,
        "biomes.png": biome_image,
        "density.png": density_image,
        "rivers.png": rivers,
        "projection_preview.png": preview,
    }
    manifest = {
        "schema": 1,
        "canvas": list(canvas),
        "control_resolution": list(size),
        "settlements": len(settlements),
        "ridges": len(projection["ridges"]),
        "mountain_zones": len(projection.get("mountain_zones", [])),
        "named_peaks": len(projection.get("named_peaks", [])),
        "passes": len(projection["passes"]),
        "rivers": len(projection["rivers"]),
        "lakes": len(projection["lakes"]),
        "engine_water_lakes": len(projection["lakes"]) - len(MATERIAL_POND_KEYS),
        "material_pond_keys": sorted(MATERIAL_POND_KEYS),
        "material_pond_max_source_pixels": MATERIAL_POND_MAX_SOURCE_PIXELS,
        "source_lake_pixel_areas": lake_pixel_areas,
        "material_pond_pixels": material_pond_pixels,
        "material_pond_height": material_pond_height,
        "land_fraction": round(float(land_array.mean()), 6),
        "land_bbox_pixels": land_bbox,
        "land_bbox_occupancy": land_bbox_occupancy,
        "land_edge_contact": land_edge_contact,
        "engine_water_level_sample": ENGINE_WATER_LEVEL_SAMPLE,
        "minimum_land_height": minimum_land_height,
        "maximum_water_height": maximum_water_height,
        "biome_ids": BIOMES,
        "source_sha256": source_hash,
    }
    return images, manifest


def write() -> None:
    CONTROL.mkdir(parents=True, exist_ok=True)
    images, manifest = render()
    for name, image in images.items():
        image.save(CONTROL / name, compress_level=9)
    (CONTROL / "control_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


def check() -> list[str]:
    failures: list[str] = []
    try:
        images, manifest = render()
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]
    for name, expected in images.items():
        path = CONTROL / name
        if not path.is_file():
            failures.append(f"missing docs/world/control/{name}")
            continue
        with Image.open(path) as actual:
            if actual.mode != expected.mode or actual.size != expected.size:
                failures.append(
                    f"{name}: expected {expected.mode} {expected.size}, "
                    f"got {actual.mode} {actual.size}"
                )
                continue
            if not np.array_equal(np.asarray(actual), np.asarray(expected)):
                failures.append(f"{name}: pixels differ from authored controls")
    manifest_path = CONTROL / "control_manifest.json"
    if not manifest_path.is_file():
        failures.append("missing docs/world/control/control_manifest.json")
    else:
        actual_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if actual_manifest != manifest:
            failures.append("control_manifest.json differs from authored controls")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        write()
    failures = check()
    if failures:
        print("m2_controls: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("m2_controls: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
