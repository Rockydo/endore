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

from m2_controls import natural_path
from worldgen import CONTROL, DERIVED, MAP_OUT, ROOT, WORLD_H, WORLD_W

RIVERS_OUT = MAP_OUT / "rivers.png"
PREVIEW_OUT = DERIVED / "river_preview.png"
ENGINE_MOUTHS = {
    # The revised western coastline lies beyond the original Baranduin control
    # endpoint. Keep its full valley axis in the physical controls and extend
    # only the parser-visible channel across the coastal plain to open water.
    "baranduin": [[0.270, 0.565], [0.240, 0.570], [0.190, 0.570]],
    # Several southern controls intentionally stopped at their named delta
    # anchors. Continue their wet corridors through the delta/coastal plain so
    # every parser-visible channel actually terminates in the current coast.
    "anduin": [[0.548, 0.806], [0.540, 0.805], [0.536, 0.805]],
    "ringlo": [[0.508, 0.790]],
    "gilrain": [[0.536, 0.802], [0.533, 0.802]],
    "poros": [[0.570, 0.814], [0.560, 0.814], [0.554, 0.814]],
    "harnen": [
        [0.500, 0.892],
        [0.470, 0.890],
        [0.440, 0.886],
        [0.405, 0.884],
        [0.370, 0.886],
        [0.345, 0.887],
    ],
}
ENGINE_SOURCES = {
    # The control axis begins inside Lake Evendim; the engine river begins at
    # its southern outlet so the green source belongs to a land component.
    "baranduin": [0.325, 0.335],
}


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


def river_control_points(river: dict) -> list[list[float]]:
    """Return the parser/material axis including proven source/mouth fixes."""

    points = (
        [ENGINE_SOURCES[river["key"]]] + river["points"][2:]
        if river["key"] in ENGINE_SOURCES
        else river["points"]
    )
    return points + ENGINE_MOUTHS.get(river["key"], [])


def validate_simple_path(key: str, path: list[tuple[int, int]]) -> None:
    """Enforce the retail parser's non-self-touching channel contract."""

    if len(path) < 3:
        raise ValueError(f"river {key} has fewer than three parser pixels")
    positions: dict[tuple[int, int], int] = {}
    for index, current in enumerate(path):
        if current in positions:
            raise ValueError(
                f"river {key} revisits parser pixel {current} at "
                f"{positions[current]} and {index}"
            )
        positions[current] = index
        if index:
            previous = path[index - 1]
            if abs(current[0] - previous[0]) + abs(current[1] - previous[1]) != 1:
                raise ValueError(f"river {key} is not strictly four-connected")
    for index, (x, y) in enumerate(path):
        for neighbour in (
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ):
            other = positions.get(neighbour)
            if other is not None and abs(other - index) > 1:
                raise ValueError(
                    f"river {key} self-touches between parser pixels "
                    f"{index} and {other}"
                )


def parser_safe_path(
    river: dict,
    size: tuple[int, int] = (WORLD_W, WORLD_H),
) -> list[tuple[int, int]]:
    """Naturalize a channel while mechanically forbidding parser-unsafe loops.

    The first reopened-M2 experiment sent unconstrained naturalized tributary
    graphs to the engine and was rejected. This route is deliberately narrower:
    independent major channels only, exact proven endpoints, and a static graph
    proof that every pixel has only its predecessor and successor as neighbours.
    """

    controls = river_control_points(river)
    dense = natural_path(
        controls,
        size,
        key=f"river:{river['key']}",
        closed=False,
        amplitude=float(river.get("wander", 0.0015)),
        spacing=0.00075,
    )
    path = orthogonal_path(dense)
    validate_simple_path(river["key"], path)
    expected_start = (
        round(float(controls[0][0]) * (size[0] - 1)),
        round(float(controls[0][1]) * (size[1] - 1)),
    )
    expected_end = (
        round(float(controls[-1][0]) * (size[0] - 1)),
        round(float(controls[-1][1]) * (size[1] - 1)),
    )
    if path[0] != expected_start or path[-1] != expected_end:
        raise ValueError(f"river {river['key']} lost an authored endpoint")
    return path


def flow_palette_index(river: dict, progress: float) -> int:
    """Approximate vanilla's downstream 4 -> 5 -> 11 -> 15 widening."""

    nominal_width = float(river["width"]) * WORLD_H
    if nominal_width < 18:
        return 4 if progress < 0.78 else 5
    if progress < 0.68:
        return 4
    if progress < 0.90:
        return 5
    if river["key"] != "anduin" or progress < 0.975:
        return 11
    return 15


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
    rivers = {item["key"]: item for item in projection["rivers"]}
    paths: dict[str, list[tuple[int, int]]] = {}
    for river in projection["rivers"]:
        parent = river.get("joins")
        if parent and parent not in rivers:
            raise ValueError(f"river {river['key']} joins unknown parent {parent}")
        # Installed build 24187685 rejects every tested custom affluent
        # junction topology at load. Tributaries remain binding height/valley
        # controls, while the engine raster ships only complete source-to-water
        # major channels until an editor-authored junction contract is proven.
        if parent:
            continue
        paths[river["key"]] = parser_safe_path(river)

    result = pixels
    occupied: set[tuple[int, int]] = set()
    for key, path in paths.items():
        land_runs: list[list[tuple[int, int]]] = []
        current_run: list[tuple[int, int]] = []
        for x, y in path:
            if water[y, x]:
                if current_run:
                    land_runs.append(current_run)
                    current_run = []
            else:
                current_run.append((x, y))
        if current_run:
            land_runs.append(current_run)
        if not land_runs:
            raise ValueError(f"river {key} never crosses land")
        land_path = max(land_runs, key=len)
        if any(len(run) > 8 for run in land_runs if run is not land_path):
            raise ValueError(f"river {key} leaves and re-enters land before its mouth")
        mouth_x, mouth_y = land_path[-1]
        if not any(
            0 <= neighbour_y < WORLD_H
            and 0 <= neighbour_x < WORLD_W
            and water[neighbour_y, neighbour_x]
            for neighbour_x, neighbour_y in (
                (mouth_x - 1, mouth_y),
                (mouth_x + 1, mouth_y),
                (mouth_x, mouth_y - 1),
                (mouth_x, mouth_y + 1),
            )
        ):
            raise ValueError(
                f"river {key} does not terminate orthogonally against "
                "palette-index-254 water"
            )
        validate_simple_path(key, land_path)
        if any(
            (x, y) in occupied
            or any(
                neighbour in occupied
                for neighbour in (
                    (x - 1, y),
                    (x + 1, y),
                    (x, y - 1),
                    (x, y + 1),
                )
            )
            for x, y in land_path
        ):
            raise ValueError(f"independent river {key} touches another channel")
        for index, (x, y) in enumerate(land_path):
            progress = index / max(1, len(land_path) - 1)
            result[y, x] = flow_palette_index(rivers[key], progress)
            occupied.add((x, y))
        source_x, source_y = land_path[0]
        result[source_y, source_x] = 0
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
        not {0, 4, 5, 11, 15, 254, 255}.issubset(used)
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
