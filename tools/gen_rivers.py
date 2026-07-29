#!/usr/bin/env python3
"""Generate/check M2 rivers using the installed EU5 indexed palette contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worldgen import CONTROL, DERIVED, MAP_OUT, ROOT, WORLD_H, WORLD_W

RIVERS_OUT = MAP_OUT / "rivers.png"
PREVIEW_OUT = DERIVED / "river_preview.png"


def game_rivers_path():
    config = json.loads((ROOT / "config/local_paths.json").read_text(encoding="utf-8-sig"))
    return (
        __import__("pathlib").Path(config["game_dir"])
        / "game/in_game/map_data/rivers.png"
    )


def point(value: list[float]) -> tuple[int, int]:
    return (
        round(float(value[0]) * (WORLD_W - 1)),
        round(float(value[1]) * (WORLD_H - 1)),
    )


def orthogonal_path(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Rasterize a polyline as a strictly four-connected, one-pixel path."""
    result = [points[0]]
    for target_x, target_y in points[1:]:
        x, y = result[-1]
        delta_x, delta_y = target_x - x, target_y - y
        steps_x, steps_y = abs(delta_x), abs(delta_y)
        sign_x = 1 if delta_x > 0 else -1
        sign_y = 1 if delta_y > 0 else -1
        moved_x = moved_y = 0
        while moved_x < steps_x or moved_y < steps_y:
            next_x = (
                (moved_x + 0.5) / steps_x
                if moved_x < steps_x
                else float("inf")
            )
            next_y = (
                (moved_y + 0.5) / steps_y
                if moved_y < steps_y
                else float("inf")
            )
            if next_x <= next_y:
                x += sign_x
                moved_x += 1
            else:
                y += sign_y
                moved_y += 1
            if (x, y) != result[-1]:
                result.append((x, y))
    return result


def render() -> Image.Image:
    projection = json.loads(
        (CONTROL / "projection.json").read_text(encoding="utf-8")
    )
    with Image.open(CONTROL / "biomes.png") as control:
        biomes = np.asarray(
            control.resize((WORLD_W, WORLD_H), Image.Resampling.NEAREST),
            dtype=np.uint8,
        )
    water = np.isin(biomes, (0, 7))
    pixels = np.full((WORLD_H, WORLD_W), 255, dtype=np.uint8)
    pixels[water] = 254
    with Image.open(game_rivers_path()) as vanilla:
        palette = vanilla.getpalette()
    if palette is None or len(palette) != 768:
        raise ValueError("installed rivers.png lacks the expected 256-color palette")
    expected_head = [
        0, 255, 0,
        255, 0, 0,
        255, 252, 0,
        0, 225, 255,
        0, 200, 255,
    ]
    if palette[:15] != expected_head:
        raise ValueError("installed river marker palette changed; re-investigate contract")
    paths: list[tuple[list[tuple[int, int]], int]] = []
    for river in projection["rivers"]:
        nominal_width = float(river["width"]) * WORLD_H
        palette_index = 4 if nominal_width >= 16 else 5 if nominal_width >= 9 else 6
        paths.append(
            (
                orthogonal_path([point(item) for item in river["points"]]),
                palette_index,
            )
        )

    result = pixels
    occupied: set[tuple[int, int]] = set()
    sources: list[tuple[int, int]] = []
    for path, palette_index in paths:
        land_path = [(x, y) for x, y in path if not water[y, x]]
        if not land_path:
            continue
        sources.append(land_path[0])
        for x, y in land_path:
            if (x, y) in occupied:
                result[y, x] = 1  # vanilla red confluence marker
            else:
                result[y, x] = palette_index
                occupied.add((x, y))
    for x, y in sources:
        if result[y, x] != 1:
            result[y, x] = 0
    active = result < 16
    neighbours = np.zeros(result.shape, dtype=np.uint8)
    neighbours[1:, :] += active[:-1, :]
    neighbours[:-1, :] += active[1:, :]
    neighbours[:, 1:] += active[:, :-1]
    neighbours[:, :-1] += active[:, 1:]
    # Stair-stepped polylines can touch at an intended confluence one pixel
    # before their exact duplicate coordinate. Mark every graph branch with
    # vanilla's red join index so the flow parser has an explicit contract.
    result[active & (neighbours > 2)] = 1
    output = Image.fromarray(result, "P")
    output.putpalette(palette)
    return output


def preview(image: Image.Image) -> Image.Image:
    return image.convert("RGB").resize((1024, 512), Image.Resampling.NEAREST)


def write() -> None:
    image = render()
    MAP_OUT.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)
    image.save(RIVERS_OUT, compress_level=9)
    preview(image).save(PREVIEW_OUT, compress_level=9)
    values, counts = np.unique(np.asarray(image), return_counts=True)
    print(
        "gen_rivers: wrote indexed river raster "
        + ", ".join(f"{int(value)}={int(count)}" for value, count in zip(values, counts))
    )


def check() -> list[str]:
    failures: list[str] = []
    expected = render()
    expected_preview = preview(expected)
    if not RIVERS_OUT.is_file():
        failures.append("missing in_game/map_data/rivers.png")
    else:
        with Image.open(RIVERS_OUT) as actual:
            if actual.mode != "P" or actual.size != (WORLD_W, WORLD_H):
                failures.append(
                    f"rivers.png is {actual.mode} {actual.size}, expected P {(WORLD_W, WORLD_H)}"
                )
            elif actual.getpalette() != expected.getpalette():
                failures.append("rivers.png palette differs from installed EU5 reference")
            elif not np.array_equal(np.asarray(actual), np.asarray(expected)):
                failures.append("rivers.png differs from deterministic river model")
    if not PREVIEW_OUT.is_file():
        failures.append("missing docs/world/derived/river_preview.png")
    else:
        with Image.open(PREVIEW_OUT) as actual_preview:
            if not np.array_equal(
                np.asarray(actual_preview),
                np.asarray(expected_preview),
            ):
                failures.append("river_preview.png differs from deterministic river model")
    used = set(int(value) for value in np.unique(np.asarray(expected)))
    if (
        not {0, 1, 254, 255}.issubset(used)
        or not used.intersection({4, 5, 6})
    ):
        failures.append(f"river raster lacks expected source/flow/background indices: {used}")
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
    failures = check()
    if failures:
        for failure in failures:
            print(f"gen_rivers: FAIL {failure}")
        return 1
    print("gen_rivers: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
