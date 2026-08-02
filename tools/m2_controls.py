#!/usr/bin/env python3
"""Render and validate the authored M2 Middle-earth projection controls."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import math
import zlib
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
# Global source-conformance averages can conceal a locally broken theatre.
# These normalized equal-scale windows bind the four relief zones called out
# in live owner review. Thresholds retain deliberate named-axis continuity
# outside the reduced raster while requiring the strong Ardacraft core to
# survive independently in every window.
SOURCE_RELIEF_THEATRES = {
    "northern_ranges": {
        "bbox": (0.42, 0.02, 0.78, 0.25),
        "min_core_coverage": 0.925,
        "min_high_support": 0.995,
    },
    "erebor": {
        "bbox": (0.56, 0.10, 0.65, 0.20),
        "min_core_coverage": 0.875,
        "min_high_support": 0.985,
    },
    "white_mountains": {
        "bbox": (0.31, 0.45, 0.60, 0.65),
        "min_core_coverage": 0.940,
        "min_high_support": 0.970,
    },
    "mordor": {
        "bbox": (0.56, 0.45, 0.76, 0.72),
        "min_core_coverage": 0.910,
        "min_high_support": 0.970,
    },
}
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


def source_relief_field(projection: dict, size: tuple[int, int]) -> np.ndarray:
    """Decode the committed Ardacraft-derived numeric relief control."""

    descriptor = projection.get("source_relief")
    if not isinstance(descriptor, dict):
        raise ValueError("projection lacks the source-derived relief descriptor")
    path = CONTROL / str(descriptor.get("file", ""))
    if path.parent != CONTROL or not path.is_file():
        raise ValueError("source-derived relief control is missing")
    payload = json.loads(path.read_text(encoding="utf-8"))
    for key in (
        "source", "source_sha256", "field_sha256", "bounds", "resolution",
        "quantization_max",
    ):
        if payload.get(key) != descriptor.get(key):
            raise ValueError(f"source-relief descriptor mismatch: {key}")
    if payload.get("schema") != 2 or payload.get("encoding") != "zlib_base85_u8":
        raise ValueError("unsupported source-relief numeric encoding")
    width, height = (int(value) for value in payload["resolution"])
    quantization_max = int(payload["quantization_max"])
    encoded = payload.get("data")
    if width < 128 or height < 128 or quantization_max < 2 or not isinstance(encoded, str):
        raise ValueError("source-relief numeric field lacks production detail")
    try:
        raw = zlib.decompress(base64.b85decode(encoded.encode("ascii")))
    except (ValueError, zlib.error) as exc:
        raise ValueError("source-relief compressed payload is invalid") from exc
    if len(raw) != width * height:
        raise ValueError("source-relief compressed payload has the wrong size")
    decoded = np.frombuffer(raw, dtype=np.uint8).reshape((height, width))
    if np.any(decoded > quantization_max):
        raise ValueError("source-relief numeric field exceeds its quantization")
    if hashlib.sha256(decoded.tobytes()).hexdigest() != payload["field_sha256"]:
        raise ValueError("source-relief numeric field checksum changed")
    bounds = [float(value) for value in payload["bounds"]]
    if len(bounds) != 4 or bounds[1] != 0.0 or bounds[3] != 1.0:
        raise ValueError("source-relief field lost its equal-scale full-height bounds")
    left = round(bounds[0] * (size[0] - 1))
    right = round(bounds[2] * (size[0] - 1))
    if not (0 <= left < right < size[0]):
        raise ValueError("source-relief field lies outside the production canvas")
    mapped = Image.fromarray(
        np.round(decoded.astype(np.float32) / quantization_max * 255.0).astype(np.uint8),
        "L",
    ).resize((right - left + 1, size[1]), Image.Resampling.BICUBIC)
    result = np.zeros((size[1], size[0]), dtype=np.float32)
    result[:, left : right + 1] = np.asarray(mapped, dtype=np.float32) / 255.0
    return np.clip(result, 0.0, 1.0)


def soft_ceiling(values: np.ndarray, *, knee: float, ceiling: float) -> np.ndarray:
    """Compress extreme relief continuously instead of clipping flat summits."""

    span = ceiling - knee
    if span <= 0.0:
        raise ValueError("terrain soft ceiling must exceed its knee")
    above = np.maximum(values - knee, 0.0)
    compressed = knee + above / (1.0 + above / span)
    return np.where(values > knee, compressed, values)


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
    descriptor = projection.get("source_relief", {})
    if (
        descriptor.get("file") != "ardacraft_relief.json"
        or descriptor.get("resolution") != [2500, 2003]
        or descriptor.get("quantization_max") != 255
    ):
        raise ValueError("mountain atlas lacks the audited Ardacraft relief field")
    highlands = projection.get("highland_zones", [])
    if len(highlands) != 190:
        raise ValueError(
            "Arda Maps highland coverage changed without cartographic review"
        )
    moors = projection.get("moor_zones", [])
    if len(moors) != 8:
        raise ValueError(
            "Arda Maps moor coverage changed without cartographic review"
        )
    for collection_name, zones, source_name in (
        ("highland", highlands, "Arda Maps poly_highland"),
        ("moor", moors, "Arda Maps poly_moor"),
    ):
        for zone in zones:
            if zone.get("shape") != "source_polygon":
                raise ValueError(
                    f"{collection_name} {zone.get('key')} lost source geometry"
                )
            if len(zone.get("coords", [])) < 4:
                raise ValueError(
                    f"{collection_name} {zone.get('key')} lacks terrain detail"
                )
            if zone.get("source") != source_name:
                raise ValueError(
                    f"{collection_name} {zone.get('key')} lost source provenance"
                )
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
    dead_marshes = next(
        zone for zone in projection["biome_zones"]
        if zone["key"] == "dead_marshes"
    )
    if (
        dead_marshes["shape"] != "source_polygon"
        or dead_marshes.get("source") != "Arda Maps poly_moor 0"
    ):
        raise ValueError("Dead Marshes regressed to a hand-authored blob")
    mordor = next(
        zone for zone in projection["biome_zones"]
        if zone["key"] == "mordor"
    )
    if (
        mordor.get("shape") != "source_proximity_field"
        or mordor.get("source_zone_keys")
        != ["low_08", "low_09", "low_10", "low_11"]
        or "inside_ridges" in mordor
        or mordor.get("source")
        != "Arda Maps poly_mountainlow 8-11 and point_mount MountDoom"
    ):
        raise ValueError("Mordor regressed to a hand-authored oval")


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


def source_zone_mask(
    projection: dict,
    collection: str,
    size: tuple[int, int],
) -> Image.Image:
    """Rasterize one audited source-polygon collection without wobble."""

    image = Image.new("L", size, 0)
    for zone in projection.get(collection, []):
        draw_shape(
            image,
            zone["shape"],
            zone["coords"],
            size,
            255,
            key=f"{collection}:{zone['key']}",
        )
    return image


def highland_relief_field(
    projection: dict,
    size: tuple[int, int],
) -> np.ndarray:
    """Return low, continuously feathered relief from Arda Maps highlands.

    These shapes describe rolling upland rather than mountain summits.  Two
    overlapping soft envelopes preserve their intricate source outlines while
    avoiding a flat raised plate at the polygon edge; deterministic rock-mass
    modulation supplies the smaller folds visible at close zoom.
    """

    source = source_zone_mask(projection, "highland_zones", size)
    inner = np.asarray(
        source.filter(ImageFilter.GaussianBlur(radius=max(1, size[1] // 1365))),
        dtype=np.float32,
    ) / 255.0
    shoulder = np.asarray(
        source.filter(ImageFilter.GaussianBlur(radius=max(3, size[1] // 256))),
        dtype=np.float32,
    ) / 255.0
    envelope = inner * 0.76 + shoulder * 0.24
    modulation = relief_modulation(size)
    return np.clip(envelope * (0.72 + modulation * 0.26), 0.0, 1.0)


def source_proximity_field(
    projection: dict,
    zone: dict,
    size: tuple[int, int],
) -> np.ndarray:
    """Derive a soft region from exact source ranges and a source anchor.

    Mordor's old fifteen-point ash oval ignored the detailed Ered Lithui,
    Ephel Duath, and Mountains of Shadow footprints already present in the
    audited atlas.  This field grows inward from those footprints, closes at
    the exact Mount Doom point, and uses only a soft production-view window to
    prevent the influence leaking into Gondor, Harad, or Rhun.
    """

    by_key = {
        item["key"]: item
        for item in projection.get("mountain_zones", [])
    }
    boundary = Image.new("L", size, 0)
    for key in zone["source_zone_keys"]:
        source_zone = by_key[key]
        draw_shape(
            boundary,
            source_zone["shape"],
            source_zone["coords"],
            size,
            255,
            key=f"source-field:{zone['key']}:{key}",
        )
    # Seal pixel-scale breaks in the exact source U-shaped mountain wall. The
    # source is open to the east, so derive its two eastern endpoints from the
    # raster itself and join them with one narrow, deterministic transition.
    # Flood filling from Mount Doom then yields the enclosed interior whose
    # north/west/south silhouette is the measured mountain footprint—not a
    # blurred axis envelope or an anchor-centred oval.
    seal_radius = max(1, round(float(zone["seal_radius"]) * size[1]))
    seal_kernel = seal_radius * 2 + 1
    boundary = boundary.filter(ImageFilter.MaxFilter(seal_kernel))
    boundary_array = np.asarray(boundary, dtype=np.uint8)
    anchor_x, anchor_y = point(zone["anchor"], size)
    x0, y0, x1, y1 = (float(value) for value in zone["bounds"])
    wall_y, wall_x = np.where(boundary_array > 0)
    upper = (
        (wall_x >= anchor_x)
        & (wall_x <= round(x1 * (size[0] - 1)))
        & (wall_y >= round(y0 * (size[1] - 1)))
        & (wall_y <= anchor_y)
    )
    lower = (
        (wall_x >= anchor_x)
        & (wall_x <= round(x1 * (size[0] - 1)))
        & (wall_y >= anchor_y)
        & (wall_y <= round(y1 * (size[1] - 1)))
    )
    if not upper.any() or not lower.any():
        raise ValueError("Mordor source wall lacks an eastern endpoint")

    def rightmost(mask: np.ndarray) -> tuple[int, int]:
        candidate_x = wall_x[mask]
        candidate_y = wall_y[mask]
        index = int(np.argmax(candidate_x))
        return int(candidate_x[index]), int(candidate_y[index])

    upper_x, upper_y = rightmost(upper)
    lower_x, lower_y = rightmost(lower)
    closure = natural_path(
        [
            (upper_x / (size[0] - 1), upper_y / (size[1] - 1)),
            (lower_x / (size[0] - 1), lower_y / (size[1] - 1)),
        ],
        size,
        key="mordor:east-transition",
        closed=False,
        amplitude=float(zone["east_closure_wander"]),
        spacing=0.003,
    )
    ImageDraw.Draw(boundary).line(
        closure,
        fill=255,
        width=max(3, seal_kernel),
        joint="curve",
    )
    filled = boundary.copy()
    ImageDraw.floodfill(filled, (anchor_x, anchor_y), 128, thresh=0)
    interior = np.asarray(filled, dtype=np.uint8) == 128
    if (
        not interior[anchor_y, anchor_x]
        or interior[0].any()
        or interior[-1].any()
        or interior[:, 0].any()
        or interior[:, -1].any()
    ):
        raise ValueError("Mordor source enclosure leaked outside its mountain wall")
    interior_fraction = float(interior.mean())
    if not 0.010 <= interior_fraction <= 0.030:
        raise ValueError(
            f"Mordor source enclosure has implausible area {interior_fraction:.6f}"
        )
    edge_radius = max(1.0, float(zone["edge_feather"]) * size[1])
    edge = np.asarray(
        Image.fromarray(interior.astype(np.uint8) * 255, "L").filter(
            ImageFilter.GaussianBlur(radius=edge_radius)
        ),
        dtype=np.float32,
    ) / 255.0
    interior_floor = 0.20 + relief_modulation(size) * 0.10
    return np.clip(np.maximum(interior * interior_floor, edge * 0.18), 0.0, 1.0)


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

    def normalized_gaussian_path(
        path: list[tuple[int, int]],
        *,
        blur: int,
    ) -> np.ndarray:
        """Return a pointed one-pixel crest with a normalized Gaussian falloff."""

        values = blurred_path(path, width=1, blur=blur)
        maximum = float(values.max())
        if maximum <= 0.0:
            return values
        return values * (255.0 / maximum)

    # This numeric field is the exact-placement authority for range branches
    # and jagged footprints. It is a severe reduction of the pinned
    # Ardacraft terrain overlay, not reference artwork, and contains no colour,
    # labels, water, terrain texture, or political information.
    source_relief = source_relief_field(projection, size)
    support_radius = max(1, round(size[1] * 0.0050))
    support_kernel = support_radius * 2 + 1
    source_axis_support = np.asarray(
        Image.fromarray(
            (source_relief >= 0.15).astype(np.uint8) * 255,
            "L",
        )
        .filter(ImageFilter.MaxFilter(support_kernel))
        .filter(
            ImageFilter.GaussianBlur(
                radius=max(1, round(size[1] * 0.0018))
            )
        ),
        dtype=np.float32,
    ) / 255.0
    # Native eight-bit relief already contains continuous shoulders, spurs and
    # crest variation. The v39 double-convex response discarded most of those
    # levels and converted the remaining upper bands into renderer-scale cliff
    # shelves. Retain the source morphology through one restrained gamma; the
    # final terrain stage now supplies only a gentle altitude response.
    # Fresh v42 Observer evidence showed that retaining the source morphology
    # was necessary but not sufficient: the warm shoulder field still lifted
    # entire range footprints into broad rock carpets.  Preserve the audited
    # upper arêtes while compressing mid-level shoulders into steep flanks.
    # The stronger exponent makes half-strength painted foothills less than
    # one quarter as tall as the crest, while leaving the true source maxima
    # untouched.  This is deliberately a narrow arête response: v42 proved
    # that a compensating gain simply converted too much upper shoulder into
    # another broad high field.
    source_form = np.power(source_relief, 2.25)
    # Mordor's numeric overlay has unusually broad, high shoulders along the
    # Ered Lithui and Ephel Duath. v60 proved that the global response turns
    # those shoulders into a table-like cap even after native-cache sculpting.
    # Compress only the source-defined Mordor bounds more strongly; exact
    # maxima, the audited range axes, and every footprint coordinate remain.
    mordor_zone = next(
        zone for zone in projection["biome_zones"] if zone["key"] == "mordor"
    )
    mordor_left, mordor_top, mordor_right, mordor_bottom = (
        float(value) for value in mordor_zone["bounds"]
    )
    mordor_x0 = max(0, round(mordor_left * (size[0] - 1)))
    mordor_x1 = min(size[0], round(mordor_right * (size[0] - 1)) + 1)
    mordor_y0 = max(0, round(mordor_top * (size[1] - 1)))
    mordor_y1 = min(size[1], round(mordor_bottom * (size[1] - 1)) + 1)
    mordor_relief = source_relief[mordor_y0:mordor_y1, mordor_x0:mordor_x1]
    source_form[mordor_y0:mordor_y1, mordor_x0:mordor_x1] = np.power(
        mordor_relief,
        3.10,
    )

    # The colour-derived relief contains a broad high body across the direct
    # Morannon/Carchost marker. Once the drawing-confirmed hinge was restored
    # below, that old body and the new bridge stacked into the rounded grey
    # tabletop proven at medium and maximum-close zoom in v66-v67. De-duplicate
    # only this bounded source body, then rebuild both exact hinge arms and the
    # source-aligned walls below. This is the same evidence-led operation used
    # for Ardacraft's duplicate Erebor body; no pass or endpoint moves.
    morannon = next(item for item in projection["passes"] if item["key"] == "morannon")
    suppress_y, suppress_x = np.ogrid[: size[1], : size[0]]
    # The v68 renderer locates the surviving table body south-east of the
    # direct gate marker, at the painted junction of the two source walls.
    # Centre this de-duplication on that body rather than enlarging a circular
    # hole around the traversable pass itself.
    morannon_x = 0.615 * (size[0] - 1)
    morannon_y = 0.545 * (size[1] - 1)
    duplicate_body = np.exp(
        -0.5
        * (
            np.square((suppress_x - morannon_x) / (size[1] * 0.038))
            + np.square((suppress_y - morannon_y) / (size[1] * 0.040))
        )
    )
    source_form *= 1.0 - duplicate_body * 0.985

    # Ardacraft's painted height overlay loses the few low-colour pixels at
    # Cirith Gorgor, although its drawing layer clearly joins Ered Lithui and
    # Ephel Duath at the Morannon hinge. Two narrow audited traces reconcile
    # that raster gap with the drawing without creating broad Gaussian flanks.
    # The pass carve below keeps the direct Black Gate marker as the low saddle.
    layers = smooth_union(layers, source_form * 255.0)
    hinge_arms = morannon.get("hinge_arms", [])
    if len(hinge_arms) != 2:
        raise ValueError("Morannon requires two audited source-reconciliation arms")
    # v41 proved literal straight strokes were visible as artificial walls,
    # but v59's native-cache review proved the source raster alone leaves both
    # range ends detached from Cirith Gorgor. Reconcile only the two audited
    # source gaps with short naturally wandering arms. The general pass carve
    # below then lowers their shared centre into the Black Gate saddle.
    hinge_center = morannon["center"]
    hinge_width = max(3, round(size[1] * 0.0050))
    hinge_y, hinge_x = np.ogrid[: size[1], : size[0]]
    hinge_center_x = float(hinge_center[0]) * (size[0] - 1)
    hinge_center_y = float(hinge_center[1]) * (size[1] - 1)
    for arm_index, endpoint in enumerate(hinge_arms):
        hinge_path = natural_path(
            [hinge_center, endpoint],
            size,
            key=f"morannon-hinge:{arm_index}",
            closed=False,
            amplitude=0.0022,
            spacing=0.0012,
        )
        # v66's exact Carchost close-up proved that finite-width bridge lines
        # enlarge into a sheer flat tabletop even when the adjoining source
        # ranges are pointed. Use the same normalized one-pixel Gaussian
        # section as the corrected Mordor walls; the pass carve below still
        # owns the low centre and both audited endpoints remain unchanged.
        hinge_body = normalized_gaussian_path(
            hinge_path,
            blur=max(1, round(hinge_width * 0.32)),
        )
        hinge_spine = normalized_gaussian_path(
            hinge_path,
            blur=max(1, round(hinge_width * 0.08)),
        )
        hinge_field = 255.0 * (
            0.24 * (hinge_body / 255.0)
            + 0.76 * (hinge_spine / 255.0)
        )
        endpoint_x = float(endpoint[0]) * (size[0] - 1)
        endpoint_y = float(endpoint[1]) * (size[1] - 1)
        arm_length = max(
            math.hypot(endpoint_x - hinge_center_x, endpoint_y - hinge_center_y),
            1.0,
        )
        distance_from_gate = np.hypot(
            hinge_x - hinge_center_x,
            hinge_y - hinge_center_y,
        )
        # Cirith Gorgor is a low cleft between two walls, not a high bridge.
        # Rise steeply but continuously from zero at the gate to full pointed
        # relief at the two audited source endpoints. This removes v69's
        # uniform high tabletop while retaining an unbroken physical approach.
        rise = np.clip(
            (distance_from_gate - hinge_width * 0.30)
            / max(arm_length - hinge_width * 0.30, 1.0),
            0.0,
            1.0,
        )
        rise = rise * rise * (3.0 - 2.0 * rise)
        hinge_field *= rise
        layers = smooth_union(layers, hinge_field)

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
            * (0.06 + 0.13 * modulation)
        )
        layers = smooth_union(layers, np.clip(zone_field, 0.0, 255.0))

    # Ardacraft supplies source-native relief across every covered range. v46
    # live evidence nevertheless proved that its sparse upper samples leave
    # disconnected cliff blocks where the drawing and continuous Arda Maps
    # linework show one chain. Re-enable only the four projection axes carrying
    # an explicit source_supported_gain: every added sample is multiplied by a
    # soft dilation of the numeric source immediately below. Ordinary hand
    # axes remain disabled; this cannot relocate or invent a mountain.
    for ridge in (
        item
        for item in projection["ridges"]
        if item.get("synthetic_axis_required", False)
        or "source_supported_gain" in item
    ):
        width = max(3, round(float(ridge["width"]) * size[1]))
        value = (
            float(ridge["height"])
            * float(ridge.get("relief_weight", 1.0))
            * float(ridge.get("source_supported_gain", 1.0))
            * 255.0
        )
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
        # Gaussian envelopes instead form one continuously sloped massif.
        # v48 proved that concentrating the full height into a very narrow
        # spine merely exchanged a broad mesa for a vertical wall. Vanilla's
        # calibrated ranges use a moderate connected body with separate high
        # summits. Keep this control envelope lower and smoothly shouldered;
        # gen_heightmap adds compact source-aligned summit teeth downstream.
        source_supported = "source_supported_gain" in ridge
        sharp_cross_section = bool(ridge.get("sharp_cross_section", False))
        if sharp_cross_section:
            # Live v60-v64 evidence isolated Mordor's remaining plateau to the
            # finite-width line cores below. A normalized one-pixel Gaussian
            # retains the same centre height and audited outer width while
            # giving both enclosing walls a pointed, non-tabletop section.
            broad = normalized_gaussian_path(
                path,
                blur=round(width * 0.30),
            )
            body = normalized_gaussian_path(
                path,
                blur=round(width * 0.13),
            )
            spine = normalized_gaussian_path(
                path,
                blur=round(width * 0.050),
            )
        else:
            broad = blurred_path(
                path,
                width=round(width * (0.78 if source_supported else 1.20)),
                blur=round(width * (0.24 if source_supported else 0.36)),
            )
            body = blurred_path(
                path,
                width=round(width * (0.46 if source_supported else 0.68)),
                blur=round(width * (0.14 if source_supported else 0.19)),
            )
            spine = blurred_path(
                path,
                width=round(width * (0.14 if source_supported else 0.17)),
                blur=round(width * (0.045 if source_supported else 0.045)),
            )
        if source_supported:
            massif = value * (
                0.10 * (broad / 255.0)
                + 0.32 * (body / 255.0)
                + 0.58 * (spine / 255.0)
            )
            longitudinal = np.clip((modulation - 0.66) / 0.58, 0.0, 1.0)
            massif *= 0.56 * (0.78 + 0.22 * longitudinal)
        else:
            massif = value * (
                0.06 * (broad / 255.0)
                + 0.24 * (body / 255.0)
                + 0.70 * (spine / 255.0)
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
            offset_limit = 0.30 if source_supported else 1.15
            center += normal * rng.uniform(-offset_limit, offset_limit) * width
            radius_x = rng.uniform(
                0.12 if source_supported else 0.30,
                0.30 if source_supported else 0.66,
            ) * width
            radius_y = rng.uniform(
                0.10 if source_supported else 0.26,
                0.27 if source_supported else 0.60,
            ) * width
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
            ImageFilter.GaussianBlur(
                radius=max(1, round(width * (0.08 if source_supported else 0.18)))
            )
        )
        peak_values = np.asarray(peaks, dtype=np.float32) / 255.0
        massif += value * peak_values * (0.07 if source_supported else 0.40)
        if source_supported:
            # The stronger continuity is legal only inside a soft dilation of
            # the measured Ardacraft range footprint.  This produces a tall,
            # connected renderer-scale wall without relocating a crest or
            # allowing the hand axis to invent high terrain in a source gap.
            massif *= source_axis_support
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
                width=round(width * (0.48 if source_supported else 0.95)),
                blur=round(width * (0.14 if source_supported else 0.30)),
            )
            branch_spine = blurred_path(
                branch_path,
                width=round(width * (0.15 if source_supported else 0.30)),
                blur=round(width * (0.050 if source_supported else 0.12)),
            )
            audited_branch_gains = ridge.get("source_audited_branch_gains")
            branch_gain = float(
                audited_branch_gains[branch_index]
                if audited_branch_gains is not None
                else 0.50 if source_supported else 0.55
            )
            branch_field = value * branch_gain * (
                (0.16 if source_supported else 0.48) * (branch_body / 255.0)
                + (0.84 if source_supported else 0.52) * (branch_spine / 255.0)
            )
            if source_supported:
                branch_field *= 0.78 + 0.22 * longitudinal
                # White Mountain continuations are exact Arda Maps summit
                # chains across two small holes in Ardacraft's numeric paint.
                # They replace the rejected circular peak stamps, so retain
                # their narrow connected geometry rather than fading them out
                # at the second source's raster boundary.
                if not ridge.get("source_audited_branches", False):
                    branch_field *= source_axis_support
            layers = smooth_union(layers, branch_field)

    # Synthetic pass shoulders are likewise opt-in fallbacks. Ardacraft's
    # measured relief owns both flanks wherever it is present; adding Gaussian
    # shoulder stamps on top manufactured the rejected Morannon/Dunharrow
    # uplands even though their centres remained correctly low.
    flank_y, flank_x = np.ogrid[: size[1], : size[0]]
    for pass_data in projection["passes"]:
        range_tangent = pass_data.get("range_tangent")
        if range_tangent is None or not pass_data.get(
            "synthetic_flanks_required", False
        ):
            continue
        tangent_x = float(range_tangent[0])
        tangent_y = float(range_tangent[1])
        tangent_length = math.hypot(tangent_x, tangent_y)
        if tangent_length <= 0.0:
            raise ValueError(f"{pass_data['key']} has a zero pass tangent")
        tangent_x /= tangent_length
        tangent_y /= tangent_length
        center_x = float(pass_data["center"][0]) * (size[0] - 1)
        center_y = float(pass_data["center"][1]) * (size[1] - 1)
        radius_pixels = float(pass_data["radius"]) * size[1]
        flank_field = np.zeros_like(layers)
        for direction in (-1.0, 1.0):
            peak_x = center_x + direction * tangent_x * radius_pixels
            peak_y = center_y + direction * tangent_y * radius_pixels
            delta_x = flank_x.astype(np.float32) - peak_x
            delta_y = flank_y.astype(np.float32) - peak_y
            along = delta_x * tangent_x + delta_y * tangent_y
            across = -delta_x * tangent_y + delta_y * tangent_x
            peak = np.exp(
                -0.5
                * (
                    (along / max(1.0, radius_pixels * 0.45)) ** 2
                    + (across / max(1.0, radius_pixels * 0.30)) ** 2
                )
            )
            np.maximum(flank_field, peak * 242.0, out=flank_field)
        flank_field *= source_axis_support
        layers = smooth_union(layers, flank_field)

    # Named summit coordinates remain audit anchors, not automatic relief
    # stamps. Source-native Ardacraft relief and the clipped continuity axes
    # now cover the formerly sparse Irensaga/Mindolluin samples. No production
    # peak currently opts into this fallback; retaining the explicit gate
    # prevents an audit marker from silently becoming a circular cap.
    for peak in (
        item
        for item in projection.get("named_peaks", [])
        if item.get("synthetic_peak_required", False)
    ):
        x, y = point(peak["center"], size)
        radius = max(3, round(float(peak["radius"]) * size[1]))
        strength = float(peak["strength"])
        rng = np.random.default_rng(stable_seed(f"named-peak:{peak['key']}"))
        peak_field = np.zeros_like(layers)
        profile = (
            (
                (0.55, 3, 0.12, 0.35, 0.18),
                (0.25, 3, 0.06, 0.70, 0.08),
                (0.08, 2, 0.03, 1.00, 0.02),
            )
            if peak.get("profile") == "source_gap_peak"
            else
            (
                (1.05, 5, 0.42, 0.18, 0.42),
                (0.58, 4, 0.22, 0.42, 0.20),
                (0.24, 3, 0.09, 0.86, 0.05),
            )
            if peak.get("profile") == "isolated_peak"
            else (
                (
                    (0.82, 5, 0.30, 0.14, 0.28),
                    (0.42, 4, 0.16, 0.40, 0.14),
                    (0.16, 3, 0.05, 0.94, 0.035),
                )
                if peak.get("profile") == "chain_peak"
                else (
                    (1.65, 6, 0.72, 0.22, 0.65),
                    (0.95, 5, 0.38, 0.38, 0.34),
                    (0.42, 3, 0.18, 0.62, 0.10),
                )
            )
        )
        for scale, lobe_count, blur, weight, offset in profile:
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
        range_tangent = pass_data.get("range_tangent")
        if range_tangent is not None:
            # A pass is a corridor across a range, not a circular crater.
            # Work in equal-scale normalized map coordinates so the field is
            # independent of the 2:1 control-raster aspect ratio.  It is
            # narrow along the range tangent (retaining both adjacent flanks)
            # and elongated along the crossing normal (opening the route).
            center_x = float(pass_data["center"][0]) * (size[0] - 1)
            center_y = float(pass_data["center"][1]) * (size[1] - 1)
            radius_norm = float(pass_data["radius"])
            tangent_x = float(range_tangent[0])
            tangent_y = float(range_tangent[1])
            tangent_length = math.hypot(tangent_x, tangent_y)
            if tangent_length <= 0.0:
                raise ValueError(f"{pass_data['key']} has a zero pass tangent")
            tangent_x /= tangent_length
            tangent_y /= tangent_length
            extent = radius_norm * 3.25
            left = max(0, math.floor(center_x - extent * size[1]))
            right = min(size[0], math.ceil(center_x + extent * size[1]) + 1)
            top = max(0, math.floor(center_y - extent * size[1]))
            bottom = min(size[1], math.ceil(center_y + extent * size[1]) + 1)
            pixel_x = np.arange(left, right, dtype=np.float32)
            pixel_y = np.arange(top, bottom, dtype=np.float32)
            delta_x = (pixel_x[None, :] - center_x) / float(size[1])
            delta_y = (pixel_y[:, None] - center_y) / float(size[1])
            along = delta_x * tangent_x + delta_y * tangent_y
            across = -delta_x * tangent_y + delta_y * tangent_x
            valley = np.exp(
                -0.5
                * (
                    (along / (radius_norm * 0.32)) ** 2
                    + (across / (radius_norm * 0.92)) ** 2
                )
            ).astype(np.float32)
            layers = np.asarray(image, dtype=np.float32)
            layers[top:bottom, left:right] *= 1.0 - valley * 0.58
            image = Image.fromarray(
                np.clip(layers, 0, 255).astype(np.uint8), "L"
            )
            continue

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
            # Major reviewed trunks own the full incision/clearance response.
            # Supplementary catchment detail remains visible but must not cut
            # the same broad valley or tree-free bank as the Anduin.
            fill=int(
                river.get(
                    "incision_strength",
                    96 if river.get("terrain_only") else 255,
                )
            ),
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
    ridge_base = np.asarray(ridges, dtype=np.float32) / 255.0
    ridge_variation = np.clip(
        (relief_modulation(size) - 0.66) / 0.58,
        0.0,
        1.0,
    )
    # Modulation may lower individual shoulders, but must never multiply an
    # already-high source sample past 1.0. That saturation made v38's long,
    # identical summit caps.
    ridge_array = ridge_base * (
        1.0 - (1.0 - ridge_base) * 0.22 * (1.0 - ridge_variation)
    )
    # Bind the generated crests to the reduced Ardacraft authority, not just
    # to a checksum that a later renderer could accidentally ignore. Strong
    # source cores must survive as high relief, while generated high relief may
    # stray only within a narrow support envelope for named peaks and legacy
    # continuity axes.
    source_relief = source_relief_field(projection, size)
    # Fresh v42 evidence shows that even 0.82 includes too much warm upper
    # shoulder.  At native eight-bit precision, 0.92 isolates the actual
    # pale/dark arête pixels which must remain visibly high after compression.
    source_core = source_relief >= 0.92
    source_core_coverage = float((ridge_array[source_core] >= 0.50).mean())
    source_support_image = Image.fromarray(
        (source_relief >= 0.15).astype(np.uint8) * 255,
        "L",
    ).filter(ImageFilter.MaxFilter(21))
    # The two White Mountain continuation paths are themselves audited Arda
    # Maps source geometry. Include their narrow corridors in the provenance
    # support metric so the cross-source reconciliation is explicit rather
    # than being misreported as invented relief.
    source_support_draw = ImageDraw.Draw(source_support_image)
    for ridge in projection["ridges"]:
        if not ridge.get("source_audited_branches", False):
            continue
        for branch_index, branch in enumerate(ridge.get("branches", [])):
            source_support_draw.line(
                natural_path(
                    branch,
                    size,
                    key=f"ridge:{ridge['key']}:branch:{branch_index}",
                    closed=False,
                    amplitude=float(ridge.get("wander", 0.0035)),
                    spacing=0.003,
                ),
                fill=255,
                width=21,
                joint="curve",
            )
    source_support = np.asarray(source_support_image, dtype=np.uint8) > 0
    high_ridge = ridge_array >= 0.50
    high_ridge_source_support = float(source_support[high_ridge].mean())
    if source_core_coverage < 0.93:
        raise ValueError("generated relief dropped too much Ardacraft crest structure")
    if high_ridge_source_support < 0.99:
        raise ValueError("generated high relief drifted outside Ardacraft support")
    theatre_conformance = {}
    for key, contract in SOURCE_RELIEF_THEATRES.items():
        x0, y0, x1, y1 = contract["bbox"]
        left = round(x0 * size[0])
        top = round(y0 * size[1])
        right = round(x1 * size[0])
        bottom = round(y1 * size[1])
        theatre_core = source_core[top:bottom, left:right]
        theatre_high = high_ridge[top:bottom, left:right]
        if not theatre_core.any() or not theatre_high.any():
            raise ValueError(f"{key} source-relief theatre became empty")
        theatre_ridge = ridge_array[top:bottom, left:right]
        theatre_support = source_support[top:bottom, left:right]
        core_coverage = float((theatre_ridge[theatre_core] >= 0.50).mean())
        high_support = float(theatre_support[theatre_high].mean())
        if core_coverage < contract["min_core_coverage"]:
            raise ValueError(
                f"{key} dropped too much Ardacraft crest structure: "
                f"{core_coverage:.6f} < {contract['min_core_coverage']:.6f}"
            )
        if high_support < contract["min_high_support"]:
            raise ValueError(
                f"{key} high relief drifted outside Ardacraft support: "
                f"{high_support:.6f} < {contract['min_high_support']:.6f}"
            )
        theatre_conformance[key] = {
            "bbox": list(contract["bbox"]),
            "source_core_pixels": int(theatre_core.sum()),
            "source_core_coverage": round(core_coverage, 6),
            "high_ridge_pixels": int(theatre_high.sum()),
            "high_ridge_source_support": round(high_support, 6),
            "minimum_source_core_coverage": contract["min_core_coverage"],
            "minimum_high_ridge_source_support": contract["min_high_support"],
        }
    ridges = Image.fromarray(np.round(ridge_array * 255.0).astype(np.uint8), "L")
    rivers = river_mask(projection, size)

    biome_image = Image.new("L", size, BIOMES["ocean"])
    biome = np.asarray(biome_image).copy()
    biome[land_array] = BIOMES["temperate"]
    # Broad climate envelopes go down first. Exact source moors and named
    # forests then retain their identity instead of being overwritten by the
    # old Rhun/Harad/Mordor proof-map paint.
    climate_zones = [
        zone
        for zone in projection["biome_zones"]
        if zone["biome"] not in {"forest", "dense_forest"}
    ]
    forest_zones = [
        zone
        for zone in projection["biome_zones"]
        if zone["biome"] in {"forest", "dense_forest"}
    ]
    for zone in climate_zones:
        if zone["shape"] == "source_proximity_field":
            field = source_proximity_field(projection, zone, size)
            active = (field >= float(zone["threshold"])) & land_array
        else:
            mask = Image.new("L", size, 0)
            draw_shape(
                mask,
                zone["shape"],
                zone["coords"],
                size,
                255,
                key=f"biome:{zone['key']}",
            )
            active = (np.asarray(mask) > 0) & land_array
        biome[active] = BIOMES[zone["biome"]]
    moor_mask = source_zone_mask(projection, "moor_zones", size)
    biome[(np.asarray(moor_mask) > 0) & land_array] = BIOMES["marsh"]
    for zone in forest_zones:
        mask = Image.new("L", size, 0)
        draw_shape(
            mask,
            zone["shape"],
            zone["coords"],
            size,
            255,
            key=f"biome:{zone['key']}",
        )
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
    material_pond_mask = (biome == BIOMES["lake"]) & land_array

    highland_relief = highland_relief_field(projection, size)

    yy = np.linspace(0.0, 1.0, size[1], dtype=np.float32)[:, None]
    base_land = LOWLAND_SOUTH_SAMPLE + (
        1.0 - yy
    ) * (LOWLAND_NORTH_SAMPLE - LOWLAND_SOUTH_SAMPLE)
    elevation = np.where(land_array, base_land, WATER_FLOOR_SAMPLE)
    elevation += np.where(land_array, highland_relief * 4_800.0, 0.0)
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
    # Sub-location source lakes remain above the engine water plane, but they
    # still need physical bowls. A shallow feathered depression plus a deeper
    # exact centre prevents their wet material from reading as a flat decal.
    pond_basin = np.asarray(
        Image.fromarray(material_pond_mask.astype(np.uint8) * 255, "L").filter(
            ImageFilter.GaussianBlur(radius=max(1, size[1] // 1024))
        ),
        dtype=np.float32,
    ) / 255.0
    elevation -= np.where(
        land_array,
        pond_basin * 900.0 + material_pond_mask * 450.0,
        0.0,
    )
    # Orodruin's final cratered cone is authored at native terrain resolution
    # in gen_heightmap.py. Keep only its low irregular apron here; feeding a
    # 50k control cone through the generic range normalizer directly caused
    # v38's flat-topped tower.
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
    apron_radius = max(10.0, size[1] / 180.0)
    apron = np.power(
        np.clip(1.0 - irregular_distance / apron_radius, 0.0, 1.0),
        2.35,
    )
    doom_relief = apron * 3_800.0
    elevation += np.where(land_array, doom_relief, 0.0)
    elevation = soft_ceiling(elevation, knee=59_000.0, ceiling=65_300.0)
    elevation = np.clip(elevation, 0, 65535).astype(np.uint16)
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
    upland_alpha = np.clip(highland_relief * 0.24, 0.0, 0.24)[..., None]
    upland_tint = np.asarray((116, 105, 78), dtype=np.float32)
    preview_array = np.where(
        land_array[..., None],
        np.round(
            preview_array.astype(np.float32) * (1.0 - upland_alpha)
            + upland_tint * upland_alpha
        ).astype(np.uint8),
        preview_array,
    )
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
        "highland_zones": len(projection.get("highland_zones", [])),
        "moor_zones": len(projection.get("moor_zones", [])),
        "highland_source_pixels": int((highland_relief > 0.08).sum()),
        "moor_source_pixels": int((np.asarray(moor_mask) > 0).sum()),
        "named_peaks": len(projection.get("named_peaks", [])),
        "source_relief_core_pixels": int(source_core.sum()),
        "source_relief_core_coverage": round(source_core_coverage, 6),
        "high_ridge_source_support": round(high_ridge_source_support, 6),
        "source_relief_theatres": theatre_conformance,
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
