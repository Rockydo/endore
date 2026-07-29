#!/usr/bin/env python3
"""Render and validate the authored M2 Middle-earth projection controls."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
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


def draw_shape(
    draw: ImageDraw.ImageDraw,
    shape: str,
    coords: list,
    size: tuple[int, int],
    fill: int,
) -> None:
    if shape == "box":
        draw.rectangle(box(coords, size), fill=fill)
    elif shape == "ellipse":
        draw.ellipse(box(coords, size), fill=fill)
    elif shape == "polygon":
        draw.polygon([point(item, size) for item in coords], fill=fill)
    else:
        raise ValueError(f"unknown control shape {shape!r}")


def land_mask(projection: dict, size: tuple[int, int]) -> Image.Image:
    image = Image.new("L", size, 0)
    draw = ImageDraw.Draw(image)
    for polygon in projection["land_polygons"].values():
        draw.polygon([point(item, size) for item in polygon], fill=255)
    for polygon in projection["sea_cutouts"].values():
        draw.polygon([point(item, size) for item in polygon], fill=0)
    for lake in projection["lakes"]:
        draw.ellipse(box(lake["box"], size), fill=0)
    return image


def ridge_mask(projection: dict, size: tuple[int, int]) -> Image.Image:
    image = Image.new("L", size, 0)
    draw = ImageDraw.Draw(image)
    for ridge in projection["ridges"]:
        width = max(2, round(float(ridge["width"]) * size[1]))
        value = round(float(ridge["height"]) * 255)
        draw.line(
            [point(item, size) for item in ridge["points"]],
            fill=value,
            width=width,
            joint="curve",
        )
    for pass_data in projection["passes"]:
        x, y = point(pass_data["center"], size)
        radius = max(2, round(float(pass_data["radius"]) * size[1]))
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=18)
    return image.filter(ImageFilter.GaussianBlur(radius=max(1, size[1] // 170)))


def river_mask(projection: dict, size: tuple[int, int]) -> Image.Image:
    image = Image.new("L", size, 0)
    draw = ImageDraw.Draw(image)
    for river in projection["rivers"]:
        width = max(1, round(float(river["width"]) * size[1]))
        draw.line(
            [point(item, size) for item in river["points"]],
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
    if canvas != (8192, 4096):
        raise ValueError("M2 production canvas must remain 8192x4096")

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
            ImageDraw.Draw(mask),
            zone["shape"],
            zone["coords"],
            size,
            255,
        )
        active = (np.asarray(mask) > 0) & land_array
        biome[active] = BIOMES[zone["biome"]]
    biome[(ridge_array > 0.29) & land_array] = BIOMES["mountain"]
    for lake in projection["lakes"]:
        mask = Image.new("L", size, 0)
        ImageDraw.Draw(mask).ellipse(box(lake["box"], size), fill=255)
        biome[np.asarray(mask) > 0] = BIOMES["lake"]
    biome_image = Image.fromarray(biome.astype(np.uint8), "L")

    yy = np.linspace(0.0, 1.0, size[1], dtype=np.float32)[:, None]
    base_land = 3500.0 + (1.0 - yy) * 1300.0
    elevation = np.where(land_array, base_land, 420.0)
    elevation += ridge_array * 51000.0
    river_blur = np.asarray(
        rivers.filter(ImageFilter.GaussianBlur(radius=max(1, size[1] // 240))),
        dtype=np.float32,
    ) / 255.0
    elevation = np.where(land_array, elevation - river_blur * 1450.0, elevation)
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
    elevation += peak_array * 26000.0
    elevation = np.clip(elevation, 0, 65535).astype(np.uint16)
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
            ImageDraw.Draw(mask),
            zone["shape"],
            zone["coords"],
            size,
            255,
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
            [point(item, size) for item in river["points"]],
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
