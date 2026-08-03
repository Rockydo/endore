#!/usr/bin/env python3
"""Generate/check M2 rivers using the installed EU5 indexed palette contract."""

from __future__ import annotations

import argparse
from collections import deque
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
# These sub-control-pixel extensions cross the final source coastline raster
# cell. They do not alter a valley or delta axis; they make the last land pixel
# orthogonally touch EU5's palette-index-254 water after 16K quantization.
ENGINE_MOUTHS: dict[str, list[list[float]]] = {
    "anduin": [[0.535043, 0.716659]],
    "baranduin": [[0.329426, 0.349292]],
    "greyflood": [[0.373138, 0.441622]],
    "isen": [[0.379976, 0.521739]],
    # Arda Maps' Lhûn line stops inland of the Ardacraft-derived Gulf of Lune
    # coast after projection.  Continue its exact terminal bearing through the
    # shortest four reviewed control points to the nearest gulf water cell.
    "lhun": [
        [0.279000, 0.113000],
        [0.271000, 0.108000],
        [0.264000, 0.101000],
        [0.261900, 0.098300],
    ],
    "ringlo": [[0.496459, 0.649243]],
    "lefnui": [[0.408655, 0.657795]],
    "serni": [[0.540255, 0.696374]],
}
ENGINE_SOURCES: dict[str, list[float]] = {}
WIDEST_RIVERS = {
    "anduin",
    "upper_anduin",
    "baranduin",
    "greyflood",
    "isen",
    "celduin",
    "carnen",
    "poros",
    "harnen",
    "lefnui",
}

# A Jomini river network has one green source and may contain any number of
# red-ended tributary segments.  These source controls are stored as separate
# named reaches for cartographic auditing, but form one uninterrupted engine
# trunk.  The first listed reach supplies the real headwater and the last one
# reaches palette-index-254 water.
COMPOSITE_TRUNKS: dict[str, tuple[str, ...]] = {
    "anduin": ("langwell", "upper_anduin", "anduin"),
    "greyflood": ("mitheithel", "greyflood"),
}
COMPOSITE_MEMBERS = {
    member
    for members in COMPOSITE_TRUNKS.values()
    for member in members
    if member != members[-1]
}
PARENT_ALIASES = {
    "upper_anduin": "anduin",
    "langwell": "anduin",
    "mitheithel": "greyflood",
}
# Entwash belongs to the lower Anduin below Rauros.  It was previously pointed
# at the separately authored upper reach only because the engine raster did
# not support joins at all.
PARENT_OVERRIDES = {"entwash": "anduin"}


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


def loop_erase_path(path: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Remove sub-pixel source backtracks while retaining the mapped channel.

    Detailed source polylines occasionally double back by one raster pixel.
    EU5 forbids both revisits and non-consecutive orthogonal self-touching, so
    truncate only the tiny closed branch whenever the advancing path reaches
    or touches an already emitted pixel.
    """

    result: list[tuple[int, int]] = []
    positions: dict[tuple[int, int], int] = {}

    def truncate(index: int) -> None:
        for removed in result[index + 1 :]:
            positions.pop(removed, None)
        del result[index + 1 :]

    for current in path:
        existing = positions.get(current)
        if existing is not None:
            truncate(existing)
            continue
        neighbours = [
            positions[neighbour]
            for neighbour in (
                (current[0] - 1, current[1]),
                (current[0] + 1, current[1]),
                (current[0], current[1] - 1),
                (current[0], current[1] + 1),
            )
            if neighbour in positions
        ]
        if neighbours:
            non_predecessors = [
                index for index in neighbours if index != len(result) - 1
            ]
            if non_predecessors:
                truncate(min(non_predecessors))
        positions[current] = len(result)
        result.append(current)
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
    path = loop_erase_path(orthogonal_path(dense))
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


def orthogonal_neighbours(point_: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    x, y = point_
    return ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))


def merge_trunk_paths(
    key: str,
    segments: list[list[tuple[int, int]]],
) -> list[tuple[int, int]]:
    """Join audited reaches into one simple source-to-mouth engine trunk."""

    result = list(segments[0])
    for segment in segments[1:]:
        if result[-1] == segment[0]:
            result.extend(segment[1:])
        else:
            connector = orthogonal_path([result[-1], segment[0]])
            result.extend(connector[1:-1])
            result.extend(segment)
        result = loop_erase_path(result)
    validate_simple_path(key, result)
    return result


def main_river_path(
    key: str,
    rivers: dict[str, dict],
    paths: dict[str, list[tuple[int, int]]],
) -> list[tuple[int, int]]:
    members = COMPOSITE_TRUNKS.get(key)
    if members is None:
        return paths[key]
    segments = [list(paths[member]) for member in members]
    # Source payload direction varies by named feature.  Orient the headwater
    # so the endpoint nearest the following reach is downstream, then orient
    # every later reach from the preceding endpoint toward the sea.
    first, second = segments[0], segments[1]
    first_start_distance = min(
        abs(first[0][0] - point_[0]) + abs(first[0][1] - point_[1])
        for point_ in (second[0], second[-1])
    )
    first_end_distance = min(
        abs(first[-1][0] - point_[0]) + abs(first[-1][1] - point_[1])
        for point_ in (second[0], second[-1])
    )
    if first_start_distance < first_end_distance:
        first.reverse()
    for index in range(1, len(segments)):
        segment = segments[index]
        previous_end = segments[index - 1][-1]
        if (
            abs(previous_end[0] - segment[-1][0])
            + abs(previous_end[1] - segment[-1][1])
            < abs(previous_end[0] - segment[0][0])
            + abs(previous_end[1] - segment[0][1])
        ):
            segment.reverse()
    return merge_trunk_paths(key, segments)


def clip_main_to_mouth(
    key: str,
    path: list[tuple[int, int]],
    water: np.ndarray,
) -> list[tuple[int, int]]:
    """Keep internal lake crossings and a short invisible ocean continuation."""

    land_indices = [index for index, (x, y) in enumerate(path) if not water[y, x]]
    if not land_indices:
        raise ValueError(f"river {key} never crosses land")
    start = land_indices[0]
    final_land = land_indices[-1]
    result = path[start : min(len(path), final_land + 4)]
    if final_land == len(path) - 1:
        mouth_x, mouth_y = result[-1]
        if not any(
            0 <= neighbour_y < WORLD_H
            and 0 <= neighbour_x < WORLD_W
            and water[neighbour_y, neighbour_x]
            for neighbour_x, neighbour_y in orthogonal_neighbours((mouth_x, mouth_y))
        ):
            raise ValueError(
                f"river {key} does not terminate orthogonally against "
                "palette-index-254 water"
            )
    validate_simple_path(key, result)
    return result


def interaction_kind(
    point_: tuple[int, int],
    parent: set[tuple[int, int]],
    occupied: set[tuple[int, int]],
) -> tuple[bool, int, int]:
    neighbours = orthogonal_neighbours(point_)
    return (
        point_ in occupied,
        sum(neighbour in parent for neighbour in neighbours),
        sum(neighbour in occupied and neighbour not in parent for neighbour in neighbours),
    )


def route_to_parent(
    key: str,
    path: list[tuple[int, int]],
    parent: set[tuple[int, int]],
    occupied: set[tuple[int, int]],
) -> list[tuple[int, int]]:
    """Terminate an incoming segment with one vanilla red confluence pixel."""

    # Stop at the first clean orthogonal contact.  If the authored endpoint
    # lands directly on its parent, the preceding pixel is normally the clean
    # red terminus.
    for index, current in enumerate(path):
        overlaps, parent_neighbours, foreign_neighbours = interaction_kind(
            current, parent, occupied
        )
        if not overlaps and parent_neighbours == 1 and foreign_neighbours == 0:
            result = path[: index + 1]
            validate_simple_path(key, result)
            return result
        if overlaps:
            if current not in parent:
                raise ValueError(
                    f"river {key} intersects an unrelated river at {current}"
                )
            if index:
                candidate = path[index - 1]
                candidate_state = interaction_kind(candidate, parent, occupied)
                if candidate_state == (False, 1, 0):
                    result = path[:index]
                    validate_simple_path(key, result)
                    return result
            # A shared endpoint on the inside of a parent bend can have two
            # parent neighbours and is therefore not a valid vanilla red
            # marker.  Back off two pixels and reconcile to a straight bank.
            path = path[: max(2, index - 1)]
            break
        if parent_neighbours > 1:
            path = path[: max(2, index - 1)]
            break
        if foreign_neighbours:
            raise ValueError(
                f"river {key} touches {foreign_neighbours} unrelated river "
                f"pixel(s) at {current}"
            )

    # Source linework can end a few dozen raster cells short of its receiving
    # course.  Route only that small final reconciliation through a one-cell
    # exclusion halo, preserving every authored pixel before it.
    if len(path) > 4:
        # Leave enough clearance for the connector to turn away from the
        # final authored stair-step without immediately self-touching it.
        path = path[:-2]
    start = path[-1]
    parent_order = sorted(
        parent,
        key=lambda item: (abs(item[0] - start[0]) + abs(item[1] - start[1]), item),
    )
    candidates: list[tuple[int, int]] = []
    for parent_pixel in parent_order[:256]:
        for candidate in orthogonal_neighbours(parent_pixel):
            x, y = candidate
            if not (0 <= x < WORLD_W and 0 <= y < WORLD_H):
                continue
            if interaction_kind(candidate, parent, occupied) != (False, 1, 0):
                continue
            candidates.append(candidate)

    branch = set(path[:-1])
    blocked = set(occupied)
    for pixel in occupied:
        blocked.update(orthogonal_neighbours(pixel))
    for pixel in branch:
        blocked.add(pixel)
        blocked.update(orthogonal_neighbours(pixel))
    blocked.discard(start)

    for target in sorted(
        set(candidates),
        key=lambda item: (abs(item[0] - start[0]) + abs(item[1] - start[1]), item),
    ):
        target_distance = abs(target[0] - start[0]) + abs(target[1] - start[1])
        if target_distance > 192:
            break
        blocked.discard(target)
        minimum_x = max(0, min(start[0], target[0]) - 24)
        maximum_x = min(WORLD_W - 1, max(start[0], target[0]) + 24)
        minimum_y = max(0, min(start[1], target[1]) - 24)
        maximum_y = min(WORLD_H - 1, max(start[1], target[1]) + 24)
        queue = deque([start])
        previous: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        while queue and target not in previous:
            current = queue.popleft()
            ordered = sorted(
                orthogonal_neighbours(current),
                key=lambda item: abs(item[0] - target[0]) + abs(item[1] - target[1]),
            )
            for neighbour in ordered:
                if neighbour in previous or neighbour in blocked:
                    continue
                x, y = neighbour
                if not (minimum_x <= x <= maximum_x and minimum_y <= y <= maximum_y):
                    continue
                previous[neighbour] = current
                queue.append(neighbour)
        if target not in previous:
            blocked.add(target)
            continue
        connector: list[tuple[int, int]] = []
        cursor: tuple[int, int] | None = target
        while cursor is not None:
            connector.append(cursor)
            cursor = previous[cursor]
        connector.reverse()
        result = loop_erase_path(path + connector[1:])
        validate_simple_path(key, result)
        if interaction_kind(result[-1], parent, occupied) != (False, 1, 0):
            raise ValueError(f"river {key} produced an invalid red confluence")
        return result
    raise ValueError(f"river {key} cannot reach parent within 192 raster cells")


def validate_network_raster(result: np.ndarray) -> None:
    """Enforce the installed vanilla source/junction/mouth graph invariants."""

    river_pixels = {
        (int(x), int(y)): int(result[y, x])
        for y, x in zip(*np.where(~np.isin(result, (254, 255))), strict=True)
    }
    for current, value in river_pixels.items():
        degree = sum(neighbour in river_pixels for neighbour in orthogonal_neighbours(current))
        maximum = 3 if value in {1, 2, 4, 5, 11, 15} else 2
        if degree > maximum:
            raise ValueError(f"river pixel {current} index {value} has degree {degree}")
        if value == 0 and degree != 1:
            raise ValueError(f"river source {current} has degree {degree}, expected 1")
        if value == 1 and degree != 2:
            raise ValueError(f"river confluence {current} has degree {degree}, expected 2")

    unseen = set(river_pixels)
    while unseen:
        seed = unseen.pop()
        stack = [seed]
        component = [seed]
        while stack:
            current = stack.pop()
            for neighbour in orthogonal_neighbours(current):
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    stack.append(neighbour)
                    component.append(neighbour)
        sources = sum(river_pixels[pixel] == 0 for pixel in component)
        if sources != 1:
            raise ValueError(
                f"river component at {seed} has {sources} green sources, expected 1"
            )
        if not any(
            0 <= neighbour_y < WORLD_H
            and 0 <= neighbour_x < WORLD_W
            and result[neighbour_y, neighbour_x] == 254
            for pixel in component
            for neighbour_x, neighbour_y in orthogonal_neighbours(pixel)
        ):
            raise ValueError(f"river component at {seed} does not reach water")


def flow_palette_index(river: dict, progress: float) -> int:
    """Approximate vanilla's downstream 4 -> 5 -> 11 -> 15 widening."""

    nominal_width = float(river["width"]) * WORLD_H
    if nominal_width < 18:
        return 4 if progress < 0.78 else 5
    if river["key"] in {"upper_anduin", "anduin"}:
        # The Anduin is Middle-earth's Great River, not merely one member of
        # the broad-river class. Preserve the installed marker vocabulary but
        # reach its broadest downstream channel substantially earlier.
        if progress < 0.08:
            return 4
        if progress < 0.20:
            return 5
        if progress < 0.45:
            return 11
        return 15
    if river["key"] in WIDEST_RIVERS:
        if progress < 0.20:
            return 4
        if progress < 0.48:
            return 5
        if progress < 0.80:
            return 11
        return 15
    if progress < 0.45:
        return 4
    if progress < 0.80:
        return 5
    return 11


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
        if river.get("engine_raster") is False:
            continue
        paths[river["key"]] = parser_safe_path(river)

    result = pixels
    occupied: set[tuple[int, int]] = set()
    drawn_paths: dict[str, list[tuple[int, int]]] = {}
    roots = [
        key
        for key, river in rivers.items()
        if key in paths and not river.get("joins") and key not in COMPOSITE_MEMBERS
    ]
    for key in roots:
        main_path = clip_main_to_mouth(
            key,
            main_river_path(key, rivers, paths),
            water,
        )
        if any(
            pixel in occupied
            or any(neighbour in occupied for neighbour in orthogonal_neighbours(pixel))
            for pixel in main_path
        ):
            raise ValueError(f"independent river {key} touches another channel")
        for index, (x, y) in enumerate(main_path):
            progress = index / max(1, len(main_path) - 1)
            result[y, x] = flow_palette_index(rivers[key], progress)
            occupied.add((x, y))
        source_x, source_y = main_path[0]
        result[source_y, source_x] = 0
        drawn_paths[key] = main_path
        for member in COMPOSITE_TRUNKS.get(key, ()):
            drawn_paths[member] = main_path

    pending = {
        key
        for key, river in rivers.items()
        if key in paths and river.get("joins") and key not in COMPOSITE_MEMBERS
    }
    while pending:
        progressed = False
        for key in sorted(pending):
            river = rivers[key]
            parent_key = PARENT_OVERRIDES.get(key, river["joins"])
            parent_key = PARENT_ALIASES.get(parent_key, parent_key)
            parent_path = drawn_paths.get(parent_key)
            if parent_path is None:
                continue
            branch = list(paths[key])
            parent = set(parent_path)
            first_distance = min(
                abs(branch[0][0] - x) + abs(branch[0][1] - y)
                for x, y in parent
            )
            last_distance = min(
                abs(branch[-1][0] - x) + abs(branch[-1][1] - y)
                for x, y in parent
            )
            if first_distance < last_distance:
                branch.reverse()
            branch = route_to_parent(key, branch, parent, occupied)
            for index, (x, y) in enumerate(branch):
                progress = index / max(1, len(branch) - 1)
                result[y, x] = flow_palette_index(river, progress)
                occupied.add((x, y))
            confluence_x, confluence_y = branch[-1]
            result[confluence_y, confluence_x] = 1
            drawn_paths[key] = branch
            pending.remove(key)
            progressed = True
        if not progressed:
            unresolved = ", ".join(sorted(pending))
            raise ValueError(f"river parent cycle or missing engine parent: {unresolved}")

    validate_network_raster(result)
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
    if not {0, 1, 4, 5, 11, 15, 254, 255}.issubset(used):
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
