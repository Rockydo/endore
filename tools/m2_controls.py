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
    phase = rng.uniform(0.0, 2.0 * math.pi, 4)
    frequency = rng.uniform((0.75, 1.55, 3.2, 6.5), (1.25, 2.45, 5.1, 10.5))
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
                0.50 * math.sin(2 * math.pi * frequency[0] * global_t + phase[0])
                + 0.27 * math.sin(2 * math.pi * frequency[1] * global_t + phase[1])
                + 0.15 * math.sin(2 * math.pi * frequency[2] * global_t + phase[2])
                + 0.08 * math.sin(2 * math.pi * frequency[3] * global_t + phase[3])
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
    elif shape == "organic_polygon":
        draw_organic_polygon(
            image,
            coords,
            size,
            key=key,
            fill=fill,
            amplitude=0.0035,
        )
    else:
        raise ValueError(f"unknown control shape {shape!r}")


def land_mask(projection: dict, size: tuple[int, int]) -> Image.Image:
    image = Image.new("L", size, 0)
    polygons = projection["land_polygons"]
    draw_organic_polygon(
        image,
        polygons["mainland"],
        size,
        key="coast:mainland",
        fill=255,
        amplitude=0.0045,
    )
    for key, polygon in projection["sea_cutouts"].items():
        draw_organic_polygon(
            image,
            polygon,
            size,
            key=f"coast:{key}",
            fill=0,
            amplitude=0.0035,
        )
    # Offshore islands are independent landmasses and must be restored after
    # bays/gulfs carve the mainland; both Himling and Tolfalas sit inside the
    # broad authored water envelopes by design.
    for key, polygon in polygons.items():
        if key == "mainland":
            continue
        draw_organic_polygon(
            image,
            polygon,
            size,
            key=f"island:{key}",
            fill=255,
            amplitude=0.002,
        )
    for lake in projection["lakes"]:
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
    layers = np.zeros((size[1], size[0]), dtype=np.uint8)
    for ridge in projection["ridges"]:
        width = max(3, round(float(ridge["width"]) * size[1]))
        value = round(float(ridge["height"]) * 255)
        path = natural_path(
            ridge["points"],
            size,
            key=f"ridge:{ridge['key']}",
            closed=False,
            amplitude=float(ridge.get("wander", 0.003)),
            spacing=0.003,
        )
        for width_scale, value_scale, blur_scale in (
            (4.8, 0.14, 1.10),
            (3.1, 0.24, 0.68),
            (1.9, 0.37, 0.36),
            (0.85, 0.48, 0.18),
        ):
            band = Image.new("L", size, 0)
            ImageDraw.Draw(band).line(
                path,
                fill=round(value * value_scale),
                width=max(2, round(width * width_scale)),
                joint="curve",
            )
            radius = max(1, round(width * blur_scale))
            band = band.filter(ImageFilter.GaussianBlur(radius=radius))
            layers = np.maximum(layers, np.asarray(band, dtype=np.uint8))
        # A mountain chain is a field of overlapping massifs, not a uniform
        # wall. Scatter deterministic off-axis peaks along the authored spine.
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
            radius_x = rng.uniform(0.72, 1.45) * width
            radius_y = rng.uniform(0.62, 1.30) * width
            peak_draw.ellipse(
                (
                    round(center[0] - radius_x),
                    round(center[1] - radius_y),
                    round(center[0] + radius_x),
                    round(center[1] + radius_y),
                ),
                fill=round(value * rng.uniform(0.58, 0.90)),
            )
        peaks = peaks.filter(
            ImageFilter.GaussianBlur(radius=max(2, round(width * 0.42)))
        )
        layers = np.maximum(layers, np.asarray(peaks, dtype=np.uint8))
        for branch_index, branch in enumerate(ridge.get("branches", [])):
            branch_path = natural_path(
                branch,
                size,
                key=f"ridge:{ridge['key']}:branch:{branch_index}",
                closed=False,
                amplitude=float(ridge.get("wander", 0.0035)),
                spacing=0.003,
            )
            band = Image.new("L", size, 0)
            ImageDraw.Draw(band).line(
                branch_path,
                fill=round(value * 0.62),
                width=max(2, round(width * 1.25)),
                joint="curve",
            )
            band = band.filter(ImageFilter.GaussianBlur(radius=max(1, width // 2)))
            layers = np.maximum(layers, np.asarray(band, dtype=np.uint8))
    image = Image.fromarray(layers, "L")
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
        layers = np.asarray(image, dtype=np.float32) * (1.0 - valley_array * 0.92)
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
    settlements = load_settlements()
    size = tuple(int(value) for value in projection["control_resolution"])
    if len(size) != 2 or min(size) < 128:
        raise ValueError("invalid control resolution")
    canvas = tuple(int(value) for value in projection["canvas"])
    if canvas != (16384, 8192):
        raise ValueError(
            "M2 production canvas must match EU5's installed 16384x8192 contract"
        )

    land = land_mask(projection, size)
    land_array = np.asarray(land) > 0
    ridges = ridge_mask(projection, size)
    ridge_array = np.asarray(ridges, dtype=np.float32) / 255.0
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
        active = (np.asarray(mask) > 0) & land_array
        biome[active] = BIOMES[zone["biome"]]
    biome[(ridge_array > 0.29) & land_array] = BIOMES["mountain"]
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
    mount_doom = next(item for item in settlements if item.key == "mount_doom")
    peak = Image.new("L", size, 0)
    px, py = point((mount_doom.x, mount_doom.y), size)
    radius = max(3, size[1] // 90)
    ImageDraw.Draw(peak).ellipse(
        (px - radius, py - radius, px + radius, py + radius),
        fill=255,
    )
    peak_array = np.asarray(
        peak.filter(ImageFilter.GaussianBlur(radius=max(2, radius // 2))),
        dtype=np.float32,
    ) / 255.0
    elevation += np.where(land_array, peak_array * 22000.0, 0.0)
    elevation = np.clip(elevation, 0, 65535).astype(np.uint16)
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
        "passes": len(projection["passes"]),
        "rivers": len(projection["rivers"]),
        "lakes": len(projection["lakes"]),
        "land_fraction": round(float(land_array.mean()), 6),
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
