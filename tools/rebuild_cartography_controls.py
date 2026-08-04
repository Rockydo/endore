#!/usr/bin/env python3
"""Rebuild original ENDÓRË controls from quarantined reference measurements.

This is a development-only authoring tool. Normal validation consumes the
committed, simplified projection.json and never requires downloaded source
data. Raw reference payloads remain under G:\endore_runtime and are not copied
into the repository.
"""

from __future__ import annotations

import argparse
import base64
from collections import deque
import hashlib
import json
import math
import sys
import zlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_rivers import river_control_points

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/world/control/projection.json"
RELIEF_OUTPUT = ROOT / "docs/world/control/ardacraft_relief.json"
DRAINAGE_OUTPUT = ROOT / "docs/world/control/ardacraft_drainage.json"
DEFAULT_REFERENCE_ROOT = Path(r"G:\endore_runtime\cartography_references")
ARDA_MAPS_SHA256 = (
    "147a2d0ff3e36e2b675afb40dd4a74f634006bc6350a6a7c31639019fd2bd4ab"
)
ARDACRAFT_HEIGHTMAP_SHA256 = (
    "a1b05874cd447b9868c0d56a4fad523e5fc94053fa239dc5df7e0b31068144be"
)
ARDACRAFT_BIOMES_SHA256 = (
    "2070d5577d768b2d418fd06e61d2fbafb5b55599340540fd9308ead213037997"
)
ARDACRAFT_DRAINAGE_SHA256 = (
    "d8ec6f22c0e3c87097145f2c3f3b831c778e4df8b705595d335e5c4d7be74871"
)

# Ardacraft's biome GeoJSON uses a projected vegetation-atlas coordinate
# system. Its own map client maps that atlas onto the same 53,888 x 43,008
# equal-scale image used by the height and drainage layers. Keep the complete
# transform here so the reduced climate controls cannot drift independently.
ARDACRAFT_BIOME_BOUNDS = {
    "min_x": -1_432_090.0,
    "max_x": 3_488_504.0,
    "min_z": 3_755_586.0,
    "max_z": 7_796_957.0,
    "horizontal_scale": 1.029,
}

# Least-squares calibration from 64 shared named points in Arda Maps to the
# ArdaCraft equal-scale world grid. It is used for continuous Arda Maps
# linework; committed landmark targets use direct ArdaCraft coordinates where
# available.
ARDA_MAPS_TO_ARDACRAFT = np.asarray(
    [
        [2_199_934.33978042, -22_818.18013716],
        [-47_257.93141998, -2_166_746.78061422],
        [-68_387.71356712, -22_242.85147676],
    ],
    dtype=np.float64,
)

PROJECTION_CONTRACT = {
    "source": "ardacraft_equal_scale_grid",
    "x_center": 10651.5,
    "z_min": -10240.0,
    "z_max": 32767.0,
    "world_span": 43007.0,
    "canvas_aspect": 2.0,
}

# The Ardacraft overlay covers its complete 53,888 x 43,008 equal-scale grid.
# ENDÓRË deliberately retains the surrounding 2:1 canvas rather than stretching
# that source horizontally; these are therefore binding normalized bounds.
ARDACRAFT_IMAGE_BOUNDS = [
    round(0.5 + (-19584.0 - 10651.5) / 86014.0, 9),
    0.0,
    round(0.5 + (34303.0 - 10651.5) / 86014.0, 9),
    1.0,
]
RELIEF_GRID_SIZE = (2500, 2003)
RELIEF_QUANTIZATION_MAX = 255
DRAINAGE_ALPHA_THRESHOLD = 160
DRAINAGE_SEED_WIDTH = 5
DRAINAGE_SEED_RADIUS = 8
DRAINAGE_REACH = 24
DRAINAGE_OPENING_RADIUS = 1
DRAINAGE_PRUNE_STEPS = 8
DRAINAGE_AFFLUENT_NEAR_DISTANCE = 4
DRAINAGE_AFFLUENT_FAR_DISTANCE = 16
DRAINAGE_AFFLUENT_MIN_PATH = 12

# Reviewed Arda Maps watercourses whose receiving channel is unambiguous in
# both the source topology and Tolkien's geography.  These are engine rivers,
# not decorative material paint: gen_rivers serializes each one as a red-ended
# tributary in its parent's indexed drainage network.
SUPPLEMENTARY_ENGINE_PARENTS: dict[str, str] = {
    # Source-unlabelled feeders are still precise Arda Maps geometry. Promote
    # only lines whose receiving endpoint is unambiguous and whose opposite
    # endpoint remains a distinct headwater; braids and deltas stay dry until
    # the yellow-distributary grammar is implemented.
    "source_unnamed_04_00": "upper_anduin",
    "source_enchantedriver_06_00": "forest_river",
    "source_unnamed_12_00": "serni",
    "source_erui_13_00": "anduin",
    "source_fenmark_15_00": "entwash",
    "source_nimrodelriver_22_00": "celebrant",
    "source_unnamed_24_00": "gladden",
    "source_unnamed_31_00": "baranduin",
    "source_unnamed_33_00": "source_lhun_84_02",
    # Arda Maps 35/37/38/39 are source-faithful but too short and parallel at
    # EU5 scale; keep their valley incision dry instead of rendering a comb.
    "source_adorn_48_00": "isen",
    "source_ciril_51_00": "ringlo",
    "source_unnamed_53_00": "ringlo",
    "source_unnamed_55_00": "gilrain",
    "source_unnamed_56_00": "serni",
    "source_shirebourn_59_00": "source_thistlebrook_60_00",
    "source_thistlebrook_60_00": "baranduin",
    "source_stockbrook_61_00": "baranduin",
    "source_unnamed_62_00": "celduin",
    "source_unnamed_65_00": "snowbourn",
    "source_unnamed_67_00": "anduin",
    "source_withywindle_68_00": "baranduin",
    "source_unnamed_73_00": "forest_river",
    "source_sirith_75_00": "anduin",
    "source_unnamed_78_00": "greylin",
    "source_sirannon_82_00": "glanduin",
    "source_lhun_84_02": "lhun",
}

# Complete source-backed courses whose mouths already terminate in a real
# engine-water lake.  These are independent one-source networks, not red-ended
# tributaries of another river.  Keep this contract separate from the parent
# map so the generated indexed grammar cannot silently reverse their meaning.
SUPPLEMENTARY_ENGINE_ROOTS = {
    "source_unnamed_02_00",
    "source_unnamed_09_00",
    "source_unnamed_10_00",
    "source_unnamed_11_00",
}

# Outgoing branches use vanilla's yellow marker immediately after the split.
# Start with the one Ethir arm whose source path directly connects the Anduin
# trunk to engine water; the remaining delta graph stays dry until each nested
# split is represented without loops or cosmetic connectors.
SUPPLEMENTARY_ENGINE_SPLITS = {
    "source_unnamed_71_04": "anduin",
    "source_unnamed_71_05": "source_unnamed_71_04",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ardacraft_relief_payload(reference_root: Path) -> dict:
    """Reduce the Ardacraft terrain overlay to an auditable relief response.

    The quarantined raster is never copied into Git. Its warm-rock response is
    reduced to an 8-bit native-resolution numeric field. Live v38 evidence
    proved that the former 1280x1026/5-bit reduction broadened individual
    source samples into renderer-scale mesa caps. The compressed numeric
    payload preserves exact branching and jagged crest structure while still
    discarding colour, water, labels, and political information.
    """

    source_path = reference_root / "ardacraft_heightmap_v2.webp"
    if sha256(source_path) != ARDACRAFT_HEIGHTMAP_SHA256:
        raise ValueError("Ardacraft height overlay changed; re-audit before rebuilding")
    with Image.open(source_path) as image:
        rgb = np.asarray(image.convert("RGB"), dtype=np.float32)
    red, green, blue = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    warm_rock = np.clip((red - green - 2.0) / 48.0, 0.0, 1.0)
    minimum = np.minimum(np.minimum(red, green), blue)
    chroma = np.maximum(np.maximum(red, green), blue) - minimum
    pale_crest = (
        np.clip((minimum - 142.0) / 78.0, 0.0, 1.0)
        * np.clip(1.0 - chroma / 62.0, 0.0, 1.0)
        * np.clip((red - green + 18.0) / 30.0, 0.0, 1.0)
        * np.clip((red - 145.0) / 55.0, 0.0, 1.0)
    )
    crest_locator = np.maximum(warm_rock, pale_crest)
    warm_image = Image.fromarray(
        np.round(crest_locator * 255.0).astype(np.uint8), "L"
    )

    def blurred(radius: float) -> np.ndarray:
        return np.asarray(
            warm_image.filter(ImageFilter.GaussianBlur(radius=radius)),
            dtype=np.float32,
        ) / 255.0

    # Raw warm-rock colour is a crest locator, not a height field. Using it as
    # the dominant value left nearly uniform high interiors with abrupt edges,
    # which v39 rendered as shelves. Reconstruct a continuous cross-range form
    # at three source-native scales: retain a restrained exact jagged core, then
    # derive a dominant tight body and two shoulder bands from the pinned pixels.
    # No range can move because every term is a convolution of that source.
    response = (
        crest_locator * 0.22
        + blurred(3.0) * 0.50
        + blurred(8.0) * 0.19
        + blurred(15.0) * 0.09
    )
    quantized = np.rint(
        np.clip((response - 0.018) / 0.64, 0.0, 1.0)
        * RELIEF_QUANTIZATION_MAX
    ).astype(np.uint8)
    compressed = zlib.compress(quantized.tobytes(), level=9)
    return {
        "schema": 2,
        "source": "Ardacraft Heightmap layer Middle-earth V2",
        "source_sha256": ARDACRAFT_HEIGHTMAP_SHA256,
        "derivation": (
            "warm-rock plus pale-summit response; source-native 3/8/15-pixel continuous "
            "body and shoulder reconstruction; native-resolution 8-bit numeric reduction"
        ),
        "bounds": ARDACRAFT_IMAGE_BOUNDS,
        "resolution": list(RELIEF_GRID_SIZE),
        "quantization_max": RELIEF_QUANTIZATION_MAX,
        "encoding": "zlib_base85_u8",
        "field_sha256": hashlib.sha256(quantized.tobytes()).hexdigest(),
        "nonzero_samples": int(np.count_nonzero(quantized)),
        "data": base64.b85encode(compressed).decode("ascii"),
    }


def _dilate_binary(values: np.ndarray) -> np.ndarray:
    result = values.copy()
    result[1:, :] |= values[:-1, :]
    result[:-1, :] |= values[1:, :]
    result[:, 1:] |= values[:, :-1]
    result[:, :-1] |= values[:, 1:]
    result[1:, 1:] |= values[:-1, :-1]
    result[1:, :-1] |= values[:-1, 1:]
    result[:-1, 1:] |= values[1:, :-1]
    result[:-1, :-1] |= values[1:, 1:]
    return result


def _erode_binary(values: np.ndarray) -> np.ndarray:
    result = np.zeros_like(values)
    center = result[1:-1, 1:-1]
    center[:] = True
    height, width = values.shape
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            center &= values[1 + dy : height - 1 + dy, 1 + dx : width - 1 + dx]
    return result


def _connected_to_seed(values: np.ndarray, seed: np.ndarray) -> tuple[np.ndarray, int]:
    """Keep complete eight-connected components that touch reviewed axes."""

    height, width = values.shape
    visited = np.zeros_like(values)
    result = np.zeros_like(values)
    kept_components = 0
    for start_y, start_x in zip(*np.where(values), strict=True):
        if visited[start_y, start_x]:
            continue
        queue = deque([(int(start_y), int(start_x))])
        visited[start_y, start_x] = True
        component: list[tuple[int, int]] = []
        touches_seed = False
        while queue:
            y, x = queue.popleft()
            component.append((y, x))
            touches_seed |= bool(seed[y, x])
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if not (dx or dy):
                        continue
                    next_y, next_x = y + dy, x + dx
                    if (
                        0 <= next_y < height
                        and 0 <= next_x < width
                        and values[next_y, next_x]
                        and not visited[next_y, next_x]
                    ):
                        visited[next_y, next_x] = True
                        queue.append((next_y, next_x))
        if touches_seed:
            kept_components += 1
            for y, x in component:
                result[y, x] = True
    return result, kept_components


def _prune_binary_endpoints(values: np.ndarray, steps: int) -> np.ndarray:
    """Remove short terminal rills while retaining confluences and trunks."""

    result = values.copy()
    for _ in range(steps):
        neighbours = np.zeros(result.shape, dtype=np.uint8)
        neighbours[1:, :] += result[:-1, :]
        neighbours[:-1, :] += result[1:, :]
        neighbours[:, 1:] += result[:, :-1]
        neighbours[:, :-1] += result[:, 1:]
        neighbours[1:, 1:] += result[:-1, :-1]
        neighbours[1:, :-1] += result[:-1, 1:]
        neighbours[:-1, 1:] += result[1:, :-1]
        neighbours[:-1, :-1] += result[1:, 1:]
        result &= neighbours > 1
    return result


def _thin_binary(values: np.ndarray) -> tuple[np.ndarray, int]:
    """Return a deterministic one-pixel Zhang-Suen centreline field."""

    image = values.copy()
    iterations = 0
    while True:
        changed = 0
        for phase in (0, 1):
            center = image[1:-1, 1:-1]
            north = image[:-2, 1:-1]
            north_east = image[:-2, 2:]
            east = image[1:-1, 2:]
            south_east = image[2:, 2:]
            south = image[2:, 1:-1]
            south_west = image[2:, :-2]
            west = image[1:-1, :-2]
            north_west = image[:-2, :-2]
            neighbours = (
                north.astype(np.uint8)
                + north_east
                + east
                + south_east
                + south
                + south_west
                + west
                + north_west
            )
            transitions = (
                ((~north) & north_east).astype(np.uint8)
                + ((~north_east) & east)
                + ((~east) & south_east)
                + ((~south_east) & south)
                + ((~south) & south_west)
                + ((~south_west) & west)
                + ((~west) & north_west)
                + ((~north_west) & north)
            )
            remove = (
                center
                & (neighbours >= 2)
                & (neighbours <= 6)
                & (transitions == 1)
            )
            if phase == 0:
                remove &= ~(north & east & south)
                remove &= ~(east & south & west)
            else:
                remove &= ~(north & east & west)
                remove &= ~(north & south & west)
            removed = int(remove.sum())
            if removed:
                updated = center.copy()
                updated[remove] = False
                image[1:-1, 1:-1] = updated
            changed += removed
        iterations += 1
        if changed == 0:
            return image, iterations
        if iterations > 64:
            raise ValueError("Ardacraft drainage thinning failed to converge")


def _corner_safe_neighbours(
    pixel: tuple[int, int],
    pixels: set[tuple[int, int]],
) -> list[tuple[int, int]]:
    """Connect a raster graph without diagonal stair-step shortcuts."""

    y, x = pixel
    neighbours: list[tuple[int, int]] = []
    for dy, dx in ((-1, 0), (0, 1), (1, 0), (0, -1)):
        candidate = (y + dy, x + dx)
        if candidate in pixels:
            neighbours.append(candidate)
    for dy, dx in ((-1, -1), (-1, 1), (1, 1), (1, -1)):
        candidate = (y + dy, x + dx)
        if (
            candidate in pixels
            and (y + dy, x) not in pixels
            and (y, x + dx) not in pixels
        ):
            neighbours.append(candidate)
    return neighbours


def _trace_binary_paths(values: np.ndarray) -> list[list[tuple[int, int]]]:
    """Split a one-pixel network into junction-to-junction paths."""

    pixels = {(int(y), int(x)) for y, x in np.argwhere(values)}
    adjacency = {
        pixel: _corner_safe_neighbours(pixel, pixels) for pixel in pixels
    }
    nodes = {
        pixel for pixel, neighbours in adjacency.items() if len(neighbours) != 2
    }
    visited: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    paths: list[list[tuple[int, int]]] = []

    def edge_key(
        first: tuple[int, int], second: tuple[int, int]
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        return (first, second) if first < second else (second, first)

    def trace(
        start: tuple[int, int], neighbour: tuple[int, int]
    ) -> list[tuple[int, int]]:
        path = [start, neighbour]
        visited.add(edge_key(start, neighbour))
        previous, current = start, neighbour
        while current not in nodes:
            onward = [candidate for candidate in adjacency[current] if candidate != previous]
            if not onward:
                break
            following = onward[0]
            edge = edge_key(current, following)
            if edge in visited:
                break
            visited.add(edge)
            path.append(following)
            previous, current = current, following
        return path

    for node in sorted(nodes):
        for neighbour in adjacency[node]:
            if edge_key(node, neighbour) not in visited:
                paths.append(trace(node, neighbour))
    for pixel in sorted(pixels):
        for neighbour in adjacency[pixel]:
            if edge_key(pixel, neighbour) not in visited:
                paths.append(trace(pixel, neighbour))
    return paths


def _manhattan_distance(values: np.ndarray) -> np.ndarray:
    """Return an integer city-block distance field without SciPy."""

    height, width = values.shape
    infinity = width + height + 5
    columns = np.arange(width, dtype=np.int32)
    left_index = np.maximum.accumulate(
        np.where(values, columns[None, :], -infinity), axis=1
    )
    left_distance = columns[None, :] - left_index
    right_index = np.minimum.accumulate(
        np.where(values, columns[None, :], infinity)[:, ::-1], axis=1
    )[:, ::-1]
    right_distance = right_index - columns[None, :]
    distance = np.minimum(left_distance, right_distance).astype(np.int32)
    for y in range(1, height):
        distance[y] = np.minimum(distance[y], distance[y - 1] + 1)
    for y in range(height - 2, -1, -1):
        distance[y] = np.minimum(distance[y], distance[y + 1] + 1)
    return distance


def _direct_affluents(
    centreline: np.ndarray,
    axes: np.ndarray,
) -> tuple[np.ndarray, int]:
    """Keep source branches that flow directly into a reviewed river axis."""

    axis_distance = _manhattan_distance(axes)
    candidates: list[list[tuple[int, int]]] = []
    for raw_path in _trace_binary_paths(centreline):
        distances = [int(axis_distance[pixel]) for pixel in raw_path]
        nearest_index = int(np.argmin(distances))
        # A graph edge can cross a reviewed course. Split it at that course so
        # each retained object is one affluent, not a basin-to-basin bridge.
        halves = (
            list(reversed(raw_path[: nearest_index + 1])),
            raw_path[nearest_index:],
        )
        for path in halves:
            if len(path) < DRAINAGE_AFFLUENT_MIN_PATH:
                continue
            path_distances = [int(axis_distance[pixel]) for pixel in path]
            if (
                path_distances[0] <= DRAINAGE_AFFLUENT_NEAR_DISTANCE
                and max(path_distances) >= DRAINAGE_AFFLUENT_FAR_DISTANCE
            ):
                candidates.append(path)

    selected = np.zeros_like(centreline, dtype=bool)
    height, width = selected.shape
    for path in candidates:
        for pixel in path:
            selected[pixel] = True
        # Close the at-most-four-pixel gap to the exact reviewed axis.
        y, x = path[0]
        while axis_distance[y, x] > 0:
            neighbours = [
                (next_y, next_x)
                for next_y, next_x in (
                    (y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)
                )
                if 0 <= next_y < height and 0 <= next_x < width
            ]
            next_y, next_x = min(
                neighbours,
                key=lambda value: (int(axis_distance[value]), value),
            )
            if axis_distance[next_y, next_x] >= axis_distance[y, x]:
                raise ValueError("source affluent could not reach its reviewed axis")
            y, x = next_y, next_x
            selected[y, x] = True
    return selected, len(candidates)


def ardacraft_drainage_payload(reference_root: Path, projection: dict) -> dict:
    """Reduce Ardacraft drainage to source-connected physical feeder axes.

    The raw overlay contains every hillside rill. The reviewed 102-course Arda
    Maps atlas therefore seeds a bounded geodesic reconstruction inside the
    hash-pinned Ardacraft network. A 3x3 source-thickness opening rejects the
    thinnest rill field. After thinning and spur pruning, only graph paths that
    run materially away from and return directly to a reviewed river survive.
    """

    source_path = reference_root / "ardacraft_drainage_v2.webp"
    if sha256(source_path) != ARDACRAFT_DRAINAGE_SHA256:
        raise ValueError("Ardacraft drainage overlay changed; re-audit before rebuilding")
    with Image.open(source_path) as opened:
        alpha = np.asarray(opened.convert("RGBA"), dtype=np.uint8)[..., 3]
    height, width = alpha.shape
    if (width, height) != RELIEF_GRID_SIZE:
        raise ValueError("Ardacraft drainage overlay has an unexpected resolution")
    left, _, right, _ = ARDACRAFT_IMAGE_BOUNDS

    def source_pixel(point: list[float]) -> tuple[int, int]:
        x, y = (float(value) for value in point)
        return (
            round((x - left) / (right - left) * (width - 1)),
            round(y * (height - 1)),
        )

    axes = Image.new("L", (width, height), 0)
    axis_draw = ImageDraw.Draw(axes)
    for river in projection["rivers"]:
        points = [source_pixel(point) for point in river_control_points(river)]
        if len(points) >= 2:
            axis_draw.line(
                points,
                fill=255,
                width=DRAINAGE_SEED_WIDTH,
                joint="curve",
            )
    seed_neighbourhood = np.asarray(
        axes.filter(ImageFilter.MaxFilter(DRAINAGE_SEED_RADIUS * 2 + 1)),
        dtype=np.uint8,
    ) > 0

    lake_mask = Image.new("L", (width, height), 0)
    lake_draw = ImageDraw.Draw(lake_mask)
    for lake in projection["lakes"]:
        points = [source_pixel(point) for point in lake["coords"]]
        if len(points) >= 3:
            lake_draw.polygon(points, fill=255)
    lake_neighbourhood = np.asarray(
        lake_mask.filter(ImageFilter.MaxFilter(9)), dtype=np.uint8
    ) > 0

    source_network = (alpha >= DRAINAGE_ALPHA_THRESHOLD) & ~lake_neighbourhood
    selected = source_network & seed_neighbourhood
    seeded_samples = int(selected.sum())
    for _ in range(DRAINAGE_REACH):
        selected = _dilate_binary(selected) & source_network
    geodesic_samples = int(selected.sum())
    opened = source_network.copy()
    for _ in range(DRAINAGE_OPENING_RADIUS):
        opened = _erode_binary(opened)
    for _ in range(DRAINAGE_OPENING_RADIUS):
        opened = _dilate_binary(opened)
    selected, kept_components = _connected_to_seed(
        selected & opened, seed_neighbourhood
    )
    selected_samples = int(selected.sum())
    centreline, thinning_iterations = _thin_binary(selected)
    unpruned_centreline_samples = int(centreline.sum())
    centreline = _prune_binary_endpoints(centreline, DRAINAGE_PRUNE_STEPS)
    pruned_centreline_samples = int(centreline.sum())
    direct_affluents, affluent_paths = _direct_affluents(
        centreline,
        np.asarray(axes, dtype=bool),
    )
    quantized = direct_affluents.astype(np.uint8)
    compressed = zlib.compress(quantized.tobytes(), level=9)
    return {
        "schema": 2,
        "source": "Ardacraft Drainage layer Middle-earth V2",
        "source_sha256": ARDACRAFT_DRAINAGE_SHA256,
        "derivation": (
            "alpha>=160; reviewed 102-course Arda Maps seed; 24-pixel connected "
            "geodesic reach; source-lake exclusion; 3x3 source-thickness opening; "
            "axis-connected components; Zhang-Suen centrelines; 8-step terminal "
            f"pruning; direct-affluent graph filter (near<={DRAINAGE_AFFLUENT_NEAR_DISTANCE}, "
            f"far>={DRAINAGE_AFFLUENT_FAR_DISTANCE}, "
            f"length>={DRAINAGE_AFFLUENT_MIN_PATH}); "
            "exact reviewed-axis reconnection"
        ),
        "bounds": ARDACRAFT_IMAGE_BOUNDS,
        "resolution": [width, height],
        "alpha_threshold": DRAINAGE_ALPHA_THRESHOLD,
        "seed_width": DRAINAGE_SEED_WIDTH,
        "seed_radius": DRAINAGE_SEED_RADIUS,
        "geodesic_reach": DRAINAGE_REACH,
        "opening_radius": DRAINAGE_OPENING_RADIUS,
        "terminal_prune_steps": DRAINAGE_PRUNE_STEPS,
        "affluent_near_distance": DRAINAGE_AFFLUENT_NEAR_DISTANCE,
        "affluent_far_distance": DRAINAGE_AFFLUENT_FAR_DISTANCE,
        "affluent_min_path": DRAINAGE_AFFLUENT_MIN_PATH,
        "encoding": "zlib_base85_u8",
        "field_sha256": hashlib.sha256(quantized.tobytes()).hexdigest(),
        "source_network_samples": int(source_network.sum()),
        "seeded_samples": seeded_samples,
        "geodesic_samples": geodesic_samples,
        "opened_samples": int(opened.sum()),
        "kept_components": kept_components,
        "selected_samples": selected_samples,
        "unpruned_centreline_samples": unpruned_centreline_samples,
        "pruned_centreline_samples": pruned_centreline_samples,
        "affluent_paths": affluent_paths,
        "centreline_samples": int(direct_affluents.sum()),
        "thinning_iterations": thinning_iterations,
        "data": base64.b85encode(compressed).decode("ascii"),
    }


def endore_from_world(x: float, z: float) -> list[float]:
    return [
        round(0.5 + (x - 10651.5) / 86014.0, 6),
        round((z + 10240.0) / 43007.0, 6),
    ]


def endore_from_ardacraft_biome(x: float, z: float) -> list[float]:
    """Project one Ardacraft biome-atlas coordinate onto ENDÓRË."""

    bounds = ARDACRAFT_BIOME_BOUNDS
    source_span = (
        (bounds["max_x"] - bounds["min_x"])
        * bounds["horizontal_scale"]
    )
    source_x = 1.0 - (bounds["max_x"] - x) / source_span
    source_y = 1.0 - (
        (z - bounds["min_z"]) / (bounds["max_z"] - bounds["min_z"])
    )
    left, _, right, _ = ARDACRAFT_IMAGE_BOUNDS
    return [
        round(left + source_x * (right - left), 6),
        round(source_y, 6),
    ]


def endore_from_arda_maps(x: float, y: float) -> list[float]:
    world_x, world_z = (
        np.asarray([x, y, 1.0], dtype=np.float64)
        @ ARDA_MAPS_TO_ARDACRAFT
    )
    return endore_from_world(float(world_x), float(world_z))


def perpendicular_distance(
    point: list[float],
    start: list[float],
    end: list[float],
) -> float:
    px, py = point
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    if dx == 0.0 and dy == 0.0:
        return math.hypot(px - x1, py - y1)
    return abs(dy * px - dx * py + x2 * y1 - y2 * x1) / math.hypot(dx, dy)


def rdp(points: list[list[float]], epsilon: float) -> list[list[float]]:
    if len(points) <= 2:
        return points
    maximum = 0.0
    split = 0
    for index in range(1, len(points) - 1):
        distance = perpendicular_distance(points[index], points[0], points[-1])
        if distance > maximum:
            maximum = distance
            split = index
    if maximum <= epsilon:
        return [points[0], points[-1]]
    left = rdp(points[: split + 1], epsilon)
    right = rdp(points[split:], epsilon)
    return left[:-1] + right


def simplify_ring(points: list[list[float]], epsilon: float) -> list[list[float]]:
    if points and points[0] == points[-1]:
        points = points[:-1]
    if len(points) < 4:
        return points
    # Rotate the closed ring to a stable extreme and split it at the most
    # distant vertex so RDP cannot erase detail around the artificial seam.
    start = min(range(len(points)), key=lambda i: (points[i][0], points[i][1]))
    rotated = points[start:] + points[:start]
    farthest = max(
        range(1, len(rotated)),
        key=lambda i: math.dist(rotated[0], rotated[i]),
    )
    first = rdp(rotated[: farthest + 1], epsilon)
    second = rdp(rotated[farthest:] + [rotated[0]], epsilon)
    result = first[:-1] + second[:-1]
    return [[round(x, 6), round(y, 6)] for x, y in result]


def ardacraft_biome_polygons(
    reference_root: Path,
    *,
    labels: set[str],
    component_filter=None,
) -> list[list[list[float]]]:
    """Reduce reviewed Ardacraft vegetation polygons to climate envelopes.

    This deliberately keeps only simplified outer rings and broad ENDÓRË
    climate classes. Source colour, prose, labels, and imagery never enter the
    repository. Exact named forests remain governed independently by Arda Maps.
    """

    source_path = reference_root / "ardacraft_biomes_v3.json"
    if sha256(source_path) != ARDACRAFT_BIOMES_SHA256:
        raise ValueError(
            "Ardacraft biome atlas changed; re-audit before rebuilding controls"
        )
    source = json.loads(source_path.read_text(encoding="utf-8"))
    if source.get("type") != "FeatureCollection":
        raise ValueError("Ardacraft biome atlas lost its FeatureCollection contract")
    available = {
        (feature.get("properties") or {}).get("Label")
        for feature in source.get("features", [])
    }
    missing = sorted(labels - available)
    if missing:
        raise ValueError(f"Ardacraft biome labels disappeared: {missing}")

    polygons: list[list[list[float]]] = []
    for feature in source["features"]:
        properties = feature.get("properties") or {}
        if properties.get("Label") not in labels:
            continue
        geometry = feature.get("geometry") or {}
        if geometry.get("type") == "Polygon":
            source_polygons = [geometry.get("coordinates", [])]
        elif geometry.get("type") == "MultiPolygon":
            source_polygons = geometry.get("coordinates", [])
        else:
            raise ValueError("Ardacraft biome source gained unsupported geometry")
        for source_polygon in source_polygons:
            if not source_polygon or len(source_polygon[0]) < 4:
                continue
            outer = [
                endore_from_ardacraft_biome(float(x), float(z))
                for x, z in source_polygon[0]
            ]
            xs = [point[0] for point in outer]
            ys = [point[1] for point in outer]
            bbox = (min(xs), min(ys), max(xs), max(ys))
            centroid = (
                sum(xs) / len(xs),
                sum(ys) / len(ys),
            )
            if component_filter is not None and not component_filter(
                properties.get("Label"), bbox, centroid
            ):
                continue
            simplified = simplify_ring(outer, 0.00020)
            if len(simplified) >= 4 and in_view(simplified):
                polygons.append(simplified)
    if not polygons:
        raise ValueError(f"Ardacraft biome reduction became empty: {sorted(labels)}")
    return polygons


class Topology:
    def __init__(self, data: dict):
        self.data = data
        self.scale_x, self.scale_y = data["transform"]["scale"]
        self.translate_x, self.translate_y = data["transform"]["translate"]

    def arc(self, encoded_index: int) -> list[list[float]]:
        reverse = encoded_index < 0
        index = ~encoded_index if reverse else encoded_index
        x = y = 0
        result: list[list[float]] = []
        for dx, dy in self.data["arcs"][index]:
            x += dx
            y += dy
            result.append(
                endore_from_arda_maps(
                    x * self.scale_x + self.translate_x,
                    y * self.scale_y + self.translate_y,
                )
            )
        return list(reversed(result)) if reverse else result

    def line(self, arc_indexes: list[int]) -> list[list[float]]:
        result: list[list[float]] = []
        for index in arc_indexes:
            current = self.arc(index)
            result.extend(current if not result else current[1:])
        return result

    def polygon_rings(self, geometry: dict) -> list[list[list[float]]]:
        if geometry["type"] == "Polygon":
            return [self.line(ring) for ring in geometry["arcs"]]
        if geometry["type"] == "MultiPolygon":
            return [
                self.line(ring)
                for polygon in geometry["arcs"]
                for ring in polygon
            ]
        raise ValueError(f"unsupported polygon geometry {geometry['type']}")

    def line_parts(self, geometry: dict) -> list[list[list[float]]]:
        if geometry["type"] == "LineString":
            return [self.line(geometry["arcs"])]
        if geometry["type"] == "MultiLineString":
            return [self.line(part) for part in geometry["arcs"]]
        raise ValueError(f"unsupported line geometry {geometry['type']}")

    def point(self, geometry: dict) -> list[float]:
        if geometry["type"] != "Point":
            raise ValueError(f"unsupported point geometry {geometry['type']}")
        x, y = geometry["coordinates"]
        return endore_from_arda_maps(
            x * self.scale_x + self.translate_x,
            y * self.scale_y + self.translate_y,
        )

    def largest_ring(self, collection: str, index: int) -> list[list[float]]:
        geometry = self.data["objects"][collection]["geometries"][index]
        rings = self.polygon_rings(geometry)
        return max(rings, key=len)


def join_line_parts(parts: list[list[list[float]]]) -> list[list[float]]:
    """Join TopoJSON river parts by their nearest available endpoints."""

    remaining = [part[:] for part in parts if len(part) >= 2]
    if not remaining:
        return []
    result = remaining.pop(0)
    while remaining:
        choices: list[tuple[float, int, bool, bool]] = []
        for index, part in enumerate(remaining):
            choices.extend(
                (
                    (math.dist(result[-1], part[0]), index, False, False),
                    (math.dist(result[-1], part[-1]), index, True, False),
                    (math.dist(result[0], part[-1]), index, False, True),
                    (math.dist(result[0], part[0]), index, True, True),
                )
            )
        _, index, reverse, prepend = min(choices)
        part = remaining.pop(index)
        if reverse:
            part.reverse()
        if prepend:
            result = part[:-1] + result
        else:
            result.extend(part[1:])
    return result


def in_view(points: list[list[float]]) -> bool:
    return any(-0.05 <= x <= 1.05 and -0.05 <= y <= 1.05 for x, y in points)


def source_polygon(
    topology: Topology,
    collection: str,
    index: int,
    *,
    epsilon: float = 0.00022,
) -> list[list[float]]:
    return simplify_ring(topology.largest_ring(collection, index), epsilon)


def source_multi_polygon(
    topology: Topology,
    collection: str,
    indexes: list[int],
) -> list[list[list[float]]]:
    return [
        source_polygon(topology, collection, index, epsilon=0.00018)
        for index in indexes
    ]


def source_polygon_collection(
    topology: Topology,
    collection: str,
    *,
    key_prefix: str,
    epsilon: float,
) -> list[dict]:
    """Return every production-view source polygon with stable provenance.

    Arda Maps' highland and moor layers contain the fine, irregular terrain
    envelopes that the original proof map omitted.  Keep the source indexes
    in their keys so a future payload audit can identify an altered footprint
    without relying on its position in a generated list.
    """

    result: list[dict] = []
    geometries = topology.data["objects"][collection]["geometries"]
    for index, geometry in enumerate(geometries):
        ring = max(topology.polygon_rings(geometry), key=len)
        if not in_view(ring) or len(ring) < 4:
            continue
        coords = simplify_ring(ring, epsilon)
        if len(coords) < 4:
            continue
        result.append(
            {
                "key": f"{key_prefix}_{index:03d}",
                "shape": "source_polygon",
                "coords": coords,
                "source": f"Arda Maps {collection}",
            }
        )
    return result


def river_geometry(topology: Topology, event_name: str) -> list[list[float]]:
    matches = [
        geometry
        for geometry in topology.data["objects"]["line_river"]["geometries"]
        if (geometry.get("properties") or {}).get("eventname") == event_name
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one Arda Maps river named {event_name}, got {len(matches)}")
    path = join_line_parts(topology.line_parts(matches[0]))
    return rdp(path, 0.00020)


def lhun_main_geometry(topology: Topology) -> list[list[float]]:
    """Recover the northern Lhûn main stem without serializing its branch.

    Arda Maps stores Lhûn as a three-part Y. Parts 1 and 0 are the continuous
    northern headwater-to-sea trunk; part 2 is the southern tributary and stays
    in the parser-safe terrain-only drainage layer.
    """

    geometry = topology.data["objects"]["line_river"]["geometries"][84]
    if (
        (geometry.get("properties") or {}).get("eventname") != "Lhun"
        or geometry["type"] != "MultiLineString"
    ):
        raise ValueError("Arda Maps Lhûn source contract changed")
    parts = topology.line_parts(geometry)
    if len(parts) != 3:
        raise ValueError("Arda Maps Lhûn branch count changed")
    path = list(reversed(parts[1]))
    append_path(path, parts[0])
    if math.dist(path[0], [0.304246, 0.044596]) > 0.001:
        raise ValueError("Arda Maps Lhûn headwater moved")
    if math.dist(path[-1], [0.286711, 0.114941]) > 0.001:
        raise ValueError("Arda Maps Lhûn mouth moved")
    return rdp(path, 0.00020)


def harnen_geometry(topology: Topology) -> list[list[float]]:
    """Recover Arda Maps' unnamed Harnen channel and reconcile its mouth.

    The hash-pinned payload's line_river geometry 8 is the only substantial
    unnamed channel in the Harnen corridor. It ends before reaching the
    represented coast, so preserve its complete source course and append only
    the short downstream continuation already reconciled to the macro map.
    """

    geometry = topology.data["objects"]["line_river"]["geometries"][8]
    properties = geometry.get("properties") or {}
    if properties.get("eventname") is not None or geometry["type"] != "LineString":
        raise ValueError("Arda Maps unnamed Harnen source contract changed")
    source = topology.line_parts(geometry)[0]
    if len(source) < 200:
        raise ValueError("Arda Maps unnamed Harnen source lost detail")
    # Source storage runs mouthward-to-headward; production rivers flow from
    # their headwaters toward the sea.
    path = rdp(list(reversed(source)), 0.00020)
    if math.dist(path[0], [0.657525, 0.745977]) > 0.001:
        raise ValueError("Arda Maps unnamed Harnen headwater moved")
    if math.dist(path[-1], [0.546302, 0.833765]) > 0.001:
        raise ValueError("Arda Maps unnamed Harnen downstream endpoint moved")
    path.extend(
        [
            [0.535000, 0.846000],
            [0.516000, 0.858000],
        ]
    )
    return [[round(x, 6), round(y, 6)] for x, y in path]


def morgulduin_geometry(topology: Topology) -> list[list[float]]:
    """Recover Arda Maps' unnamed Morgulduin channel."""

    geometry = topology.data["objects"]["line_river"]["geometries"][14]
    properties = geometry.get("properties") or {}
    if properties.get("eventname") is not None or geometry["type"] != "LineString":
        raise ValueError("Arda Maps unnamed Morgulduin source contract changed")
    source = topology.line_parts(geometry)[0]
    if len(source) < 35:
        raise ValueError("Arda Maps unnamed Morgulduin source lost detail")
    # Source storage runs Anduin-ward-to-Morgul-ward; production rivers flow
    # toward their receiving channel.
    path = rdp(list(reversed(source)), 0.00020)
    if math.dist(path[0], [0.603831, 0.594698]) > 0.001:
        raise ValueError("Arda Maps unnamed Morgulduin headwater moved")
    if math.dist(path[-1], [0.594108, 0.605029]) > 0.001:
        raise ValueError("Arda Maps unnamed Morgulduin confluence moved")
    return [[round(x, 6), round(y, 6)] for x, y in path]


def append_path(
    destination: list[list[float]],
    source: list[list[float]],
) -> None:
    """Append a source path without duplicating its shared endpoint."""

    destination.extend(source if not destination else source[1:])


def anduin_geometries(topology: Topology) -> tuple[list[list[float]], list[list[float]]]:
    """Extract the main Anduin channels without its mapped distributary loops.

    Arda Maps models the upper Anduin as one branched MultiLineString and the
    lower Anduin/ethir as an unnamed second MultiLineString. Joining every part
    produces backtracking channels that EU5 correctly rejects. The selected
    parts are the continuous main stem in the hash-pinned source payload.
    """

    upper_geometry = next(
        geometry
        for geometry in topology.data["objects"]["line_river"]["geometries"]
        if (geometry.get("properties") or {}).get("eventname") == "Anduin"
    )
    upper_parts = topology.line_parts(upper_geometry)
    upper: list[list[float]] = []
    for part in (
        list(reversed(upper_parts[0])),
        upper_parts[2],
        upper_parts[3],
        list(reversed(upper_parts[5])),
        list(reversed(upper_parts[7])),
    ):
        append_path(upper, part)

    lower_geometry = topology.data["objects"]["line_river"]["geometries"][71]
    lower_parts = topology.line_parts(lower_geometry)
    lower: list[list[float]] = []
    for part in (
        # Part 12 is stored mouthward-to-headward.  Reversing it is required
        # before appending part 13 and the reversed downstream trunk; the old
        # order doubled back from the Entwash confluence to Nen Hithoel and
        # then jumped downstream again.  gen_rivers quite correctly erased
        # that loop, but the result silently lost the real Rauros-to-Entwash
        # reach of the Great River.
        list(reversed(lower_parts[12])),
        lower_parts[13],
        list(reversed(lower_parts[11])),
    ):
        append_path(lower, part)
    # The source's Ethir is a distributary graph. Preserve its central approach
    # and terminate at the source coastline instead of serializing every fork.
    lower.append([0.535188, 0.716594])
    return rdp(upper, 0.00020), rdp(lower, 0.00020)


def orient(points: list[list[float]], mouth: tuple[float, float]) -> list[list[float]]:
    if math.dist(points[0], mouth) < math.dist(points[-1], mouth):
        points = list(reversed(points))
    return [[round(x, 6), round(y, 6)] for x, y in points]


def stable_key(value: str) -> str:
    result = "".join(character.lower() if character.isalnum() else "_" for character in value)
    while "__" in result:
        result = result.replace("__", "_")
    return result.strip("_") or "unnamed"


def supplementary_river_controls(topology: Topology) -> list[dict]:
    """Retain every additional source watercourse as physical terrain detail.

    Reviewed named affluents use the installed red-junction river grammar;
    unreviewed minor lines remain height controls until their receiving course
    is proved. Keep explicitly modelled trunks out of this collection to avoid
    incising them twice; import every other named channel plus every substantial
    unnamed source part independently.
    """

    modelled_names = {
        "Anduin", "Langwell", "Greylin", "GladdenRiver", "Celebrant",
        "Limlight", "Entwash", "Snowbourn", "Brandywine", "Hoarwell",
        "Bruinen", "Gwathlo", "Glanduin", "Isen", "Morthond", "Ringlo",
        "Gilrain", "RiverRunning", "ForestRiver", "Carnen", "Poros",
        "Lefnui", "Serni",
    }
    broad_named = {
        "Adorn", "Celos", "Ciril", "Erui", "Lefnui", "Lhun", "Serni",
        "Sirannon", "Sirith",
    }
    controls: list[dict] = []
    geometries = topology.data["objects"]["line_river"]["geometries"]
    for geometry_index, geometry in enumerate(geometries):
        properties = geometry.get("properties") or {}
        source_name = properties.get("eventname")
        if source_name in modelled_names:
            continue
        for part_index, source_part in enumerate(topology.line_parts(geometry)):
            # These exact lines already back the reviewed Harnen and
            # Morgulduin controls. Drawing them again creates artificial
            # double-width valleys.
            if geometry_index in {8, 14}:
                continue
            # The lower Anduin control owns parts 11-14. Parts 0-10 are the
            # real Ethir distributaries and remain visible physical drainage,
            # including their sub-threshold connector segments.
            if geometry_index == 71 and part_index >= 11:
                continue
            # Lhûn parts 1 and 0 form the reviewed terrain-only trunk; part 2
            # remains its separate source-derived southern tributary.
            if geometry_index == 84 and part_index in {0, 1}:
                continue
            if len(source_part) < 2 or not in_view(source_part):
                continue
            path = rdp(source_part, 0.00014)
            path_length = sum(
                math.dist(start, end)
                for start, end in zip(path, path[1:], strict=False)
            )
            # Discard only genuinely sub-location scratches. Short named
            # tributaries remain binding because several are lore landmarks.
            if (
                path_length < (0.0018 if source_name else 0.0012)
                and geometry_index != 71
            ):
                continue
            if source_name in broad_named:
                hydrology_class = "named_branch"
                width = 0.0021
                incision_strength = 176
                material_scale = 1.00
            elif source_name:
                hydrology_class = "named_tributary"
                width = 0.0016
                incision_strength = 150
                material_scale = 0.86
            elif path_length >= 0.040:
                hydrology_class = "unnamed_trunk"
                width = 0.00155
                incision_strength = 138
                material_scale = 0.82
            elif path_length >= 0.015:
                hydrology_class = "unnamed_branch"
                width = 0.00140
                incision_strength = 124
                material_scale = 0.74
            else:
                hydrology_class = "unnamed_feeder"
                width = 0.00125
                incision_strength = 108
                material_scale = 0.68
            label = stable_key(str(source_name)) if source_name else "unnamed"
            key = f"source_{label}_{geometry_index:02d}_{part_index:02d}"
            item = {
                    "key": key,
                    "label": source_name,
                    "width": width,
                    "wander": 0.0,
                    "engine_raster": False,
                    "terrain_only": True,
                    "hydrology_class": hydrology_class,
                    "incision_strength": incision_strength,
                    "material_scale": material_scale,
                    # Source storage direction is not uniformly head-to-mouth;
                    # keep minor bank paint nearly uniform instead of applying
                    # the engine-raster downstream taper backwards.
                    "material_growth": 0.20,
                    "points": [
                        [round(x, 6), round(y, 6)] for x, y in path
                    ],
                    "source": (
                        f"Arda Maps line_river {geometry_index} part {part_index}"
                    ),
                }
            parent = SUPPLEMENTARY_ENGINE_PARENTS.get(key)
            if parent is not None:
                item["engine_raster"] = True
                item["terrain_only"] = False
                item["joins"] = parent
            elif key in SUPPLEMENTARY_ENGINE_ROOTS:
                item["engine_raster"] = True
                item["terrain_only"] = False
                item["engine_root"] = True
            elif key in SUPPLEMENTARY_ENGINE_SPLITS:
                item["engine_raster"] = True
                item["terrain_only"] = False
                item["splits"] = SUPPLEMENTARY_ENGINE_SPLITS[key]
            controls.append(item)

    # Arda parts 6 and 4 form one acyclic southern Ethir arm: part 6 runs from
    # its internal junction to Anduin, while part 4 runs from sea to that same
    # junction.  Preserve every source point and combine them parent-to-water;
    # part 6 remains as its dry audit control, so no source evidence is lost.
    controls_by_key = {item["key"]: item for item in controls}
    ethir_inner = controls_by_key["source_unnamed_71_06"]
    ethir_mouth = controls_by_key["source_unnamed_71_04"]
    inner_points = list(reversed(ethir_inner["points"]))
    mouth_points = list(reversed(ethir_mouth["points"]))
    if math.dist(inner_points[-1], mouth_points[0]) > 0.0005:
        raise ValueError("Ethir parts 6 and 4 lost their shared source junction")
    ethir_mouth["points"] = inner_points + mouth_points[1:]
    ethir_mouth["source"] = "Arda Maps line_river 71 parts 6+4"
    return controls


def build(reference_root: Path) -> tuple[dict, dict, dict]:
    source_path = reference_root / "arda_maps_third_age.json"
    if sha256(source_path) != ARDA_MAPS_SHA256:
        raise ValueError("Arda Maps payload changed; re-audit before rebuilding controls")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    topology = Topology(source)
    previous = json.loads(OUTPUT.read_text(encoding="utf-8"))
    relief_payload = ardacraft_relief_payload(reference_root)

    brown_lands_polygons = ardacraft_biome_polygons(
        reference_root,
        labels={"M6"},
    )
    rhun_steppe_labels = {
        "L3", "L5", "L7", "M2", "M7", "M11", "M18", "M20",
        "Z2", "Z3", "Z4", "Z5",
    }
    rhun_steppe_polygons = ardacraft_biome_polygons(
        reference_root,
        labels=rhun_steppe_labels,
        component_filter=lambda _label, bbox, centroid: (
            bbox[2] >= 0.56 and centroid[0] >= 0.54 and centroid[1] <= 0.76
        ),
    )
    harad_steppe_labels = {
        "H1", "H2", "H6", "H7", "J22", "J48", "J49",
        "K23", "K31", "N4",
    }
    harad_steppe_polygons = ardacraft_biome_polygons(
        reference_root,
        labels=harad_steppe_labels,
        component_filter=lambda _label, bbox, centroid: (
            bbox[3] >= 0.65 and centroid[1] >= 0.64
        ),
    )
    harad_arid_labels = {"H3", "H4", "H5"}
    harad_arid_polygons = ardacraft_biome_polygons(
        reference_root,
        labels=harad_arid_labels,
        component_filter=lambda _label, bbox, centroid: (
            bbox[3] >= 0.79 and centroid[1] >= 0.79
        ),
    )

    outline_geometries = source["objects"]["poly_outline"]["geometries"]
    islands: dict[str, list[list[float]]] = {}
    island_number = 0
    for index, geometry in enumerate(outline_geometries):
        if index in {2, 13}:
            continue
        ring = max(topology.polygon_rings(geometry), key=len)
        if not in_view(ring):
            continue
        key = "himling" if index == 0 else "tolfalas" if index == 6 else f"island_{island_number:02d}"
        islands[key] = simplify_ring(ring, 0.00016)
        island_number += 1

    lake_names = {
        0: "long_lake",
        1: "mirrormere",
        2: "lake_evendim",
        3: "nen_hithoel",
        8: "sea_of_nurnen",
        9: "sea_of_rhun",
    }
    lakes = []
    for index, geometry in enumerate(source["objects"]["poly_lake"]["geometries"]):
        ring = max(topology.polygon_rings(geometry), key=len)
        if not in_view(ring):
            continue
        lakes.append(
            {
                "key": lake_names.get(index, f"minor_lake_{index:02d}"),
                "shape": "source_polygon",
                # Several named ponds and tarns are only a few control pixels
                # wide; preserve their source vertices instead of simplifying
                # them into triangles.
                "coords": simplify_ring(ring, 0.000025),
            }
        )

    mountain_zones = []
    for collection, strength in (
        ("poly_mountainlow", 0.58),
        ("poly_mountainhigh", 1.0),
    ):
        tier = "low" if strength < 1.0 else "high"
        for index, geometry in enumerate(source["objects"][collection]["geometries"]):
            ring = max(topology.polygon_rings(geometry), key=len)
            if not in_view(ring) or len(ring) < 4:
                continue
            mountain_zones.append(
                {
                    "key": f"{tier}_{index:02d}",
                    "shape": "source_polygon",
                    "coords": simplify_ring(ring, 0.00024),
                    "strength": strength,
                }
            )

    # These two audited layers were absent from the proof map even though the
    # hash-pinned source contains them.  Highlands provide 190 renderable
    # upland/foothill envelopes in the production view; moors provide eight
    # exact wet-ground footprints, including the Dead Marshes and Nindalf.
    # They remain separate from gameplay topography and political locations.
    highland_zones = source_polygon_collection(
        topology,
        "poly_highland",
        key_prefix="highland",
        epsilon=0.00008,
    )
    moor_zones = source_polygon_collection(
        topology,
        "poly_moor",
        key_prefix="moor",
        epsilon=0.00010,
    )

    # Named summits are exact Arda Maps point controls, not generic scenery.
    # The polygon layers bind each range footprint and the axes below bind its
    # overall direction; these points ensure that the most lore-sensitive
    # local maxima fall at the source positions within those ranges.
    named_peak_keys = {
        "Weathertop": "weathertop",
        "Methedras": "methedras",
        "Celebdil": "celebdil",
        "Fanuidhol": "fanuidhol",
        "Caradhras": "caradhras",
        "Mindolluin": "mindolluin",
        "Erech": "erech_hill",
        "Thrihyrne": "thrihyrne",
        "DolBaran": "dol_baran",
        "Irensaga": "irensaga",
        "Dwimorberg": "dwimorberg",
        "Starkhorn": "starkhorn",
        "RasMorthil": "ras_morthil",
        "Carrock": "carrock_height",
        "Gundabad": "mount_gundabad",
        "LonelyMountain": "erebor_peak",
        "Ravenhill": "ravenhill",
        "AmonHen": "amon_hen",
    }
    subdued_peaks = {
        "Weathertop": 0.55,
        "Erech": 0.55,
        "DolBaran": 0.55,
        "RasMorthil": 0.60,
        "Carrock": 0.48,
        "Ravenhill": 0.58,
        "AmonHen": 0.45,
    }
    named_peaks = []
    for geometry in source["objects"]["point_mount"]["geometries"]:
        properties = geometry.get("properties") or {}
        source_name = properties.get("eventname")
        key = named_peak_keys.get(source_name)
        if key is None:
            # Mount Doom has its own asymmetric cratered relief control.
            if source_name == "MountDoom":
                continue
            raise ValueError(f"unreviewed Arda Maps mountain point {source_name!r}")
        size_class = int(properties.get("size", 1))
        radius = 0.0035 + 0.0012 * size_class
        if source_name == "LonelyMountain":
            # Erebor is a single isolated massif. The old generic size-class
            # radius spread its shoulders into the surrounding upland and made
            # it read as part of a range at regional zoom.
            radius = 0.0042
        elif source_name == "Gundabad":
            # Gundabad is a summit at the junction of the Misty and Grey
            # Mountains, not an isolated massif and not a second range-sized
            # envelope. The generic size-3 point radius produced a broad cap
            # over terrain that already carries both source ranges. Reserve
            # this control for the exact source-pinned crown.
            radius = 0.0045
        peak_center = (
            endore_from_world(19_227.0, -4_322.0)
            if source_name == "LonelyMountain"
            else topology.point(geometry)
        )
        named_peaks.append(
            {
                "key": key,
                "label": source_name,
                "center": peak_center,
                "radius": round(radius, 6),
                "strength": round(
                    subdued_peaks.get(
                        source_name,
                        min(1.0, 0.63 + 0.18 * size_class),
                    ),
                    3,
                ),
                **(
                    {"profile": "isolated_peak"}
                    if source_name == "LonelyMountain"
                    else (
                        {"profile": "chain_peak"}
                        if source_name == "Gundabad"
                        else {}
                    )
                ),
                "source": (
                    "Ardacraft direct Erebor marker"
                    if source_name == "LonelyMountain"
                    else "Arda Maps point_mount"
                ),
            }
        )

    # Mount Gram is attested in LOTR but does not appear in Arda Maps'
    # point_mount layer. The v102 exact-camera review showed that leaving the
    # reviewed landmark to low regional source relief makes the namesake
    # stronghold read as flat woodland. Add one deliberately tiny source-gap
    # summit at the existing M3 coordinate; the strict audit below prevents
    # this exception from becoming a generic synthetic-peak route.
    named_peaks.append(
        {
            "key": "mount_gram",
            "label": "MountGram",
            "center": [0.448, 0.145],
            "radius": 0.0038,
            "strength": 0.92,
            "profile": "source_gap_peak",
            "synthetic_peak_required": True,
            "source": "LOTR Book I, Ch. 1; reviewed Mount Gram landmark",
        }
    )

    ridges = [
        {
            "key": "misty_mountains",
            "width": 0.012,
            "height": 0.98,
            "wander": 0.0012,
            "points": [
                [0.501, 0.072], [0.502, 0.105], [0.506, 0.145],
                [0.510, 0.192], [0.507, 0.238], [0.501, 0.282],
                [0.496, 0.318], [0.490, 0.355], [0.481, 0.401],
                [0.467, 0.447], [0.463, 0.478],
            ],
        },
        {
            "key": "grey_mountains",
            "width": 0.010,
            "height": 0.84,
            "wander": 0.0012,
            "points": [
                [0.499, 0.070], [0.530, 0.066], [0.563, 0.071],
                [0.596, 0.070], [0.630, 0.078], [0.661, 0.091],
                [0.688, 0.106],
            ],
        },
        {
            "key": "ered_luin",
            "width": 0.009,
            "height": 0.79,
            "wander": 0.0010,
            "points": [
                [0.302, 0.035], [0.303, 0.075], [0.306, 0.118],
                [0.309, 0.164], [0.311, 0.207], [0.300, 0.250],
                [0.287, 0.290],
            ],
        },
        {
            "key": "white_mountains",
            "width": 0.012,
            "height": 0.96,
            "wander": 0.0012,
            "points": [
                [0.426, 0.600], [0.451, 0.582], [0.475, 0.568],
                [0.500, 0.566], [0.526, 0.575], [0.552, 0.592],
                [0.578, 0.610],
            ],
            # Arda Maps places the Dunharrow peaks on a short northern spur
            # and Mindolluin just beyond the eastern end of the Ardacraft
            # numeric crest. Connect those exact audited points to the main
            # chain as narrow paths; the previous circular source-gap stamps
            # rendered as isolated mesas in v47.
            "branches": [
                [
                    [0.500, 0.566],
                    [0.500845, 0.547265],
                    [0.497545, 0.541502],
                    [0.502831, 0.535253],
                ],
                [
                    [0.578, 0.610],
                    [0.585423, 0.607818],
                ],
            ],
            "source_audited_branches": True,
            # The long Dunharrow spur and very short terminal Mindolluin link
            # need different gains to reach the same renderer-scale crest
            # without broadening either path.
            "source_audited_branch_gains": [0.45, 0.65],
        },
        {
            "key": "ephel_duath",
            "width": 0.0085,
            "height": 1.00,
            "wander": 0.0010,
            "sharp_cross_section": True,
            "points": [
                # Direct hinge endpoint, then local maxima sampled from the
                # hash-pinned Ardacraft relief at the listed latitudes. The
                # former hand guide drifted up to 0.067 canvas-width east of
                # the actual western wall in southern Mordor.
                [0.605128, 0.549585], [0.610012, 0.558000],
                [0.611477, 0.578000], [0.614652, 0.596000],
                [0.612454, 0.615000], [0.613187, 0.632000],
                [0.610745, 0.650000], [0.615385, 0.665000],
                [0.619780, 0.680000], [0.616117, 0.690000],
                [0.613675, 0.703000],
            ],
        },
        {
            "key": "ered_lithui",
            "width": 0.0085,
            "height": 1.00,
            "wander": 0.0010,
            "sharp_cross_section": True,
            "points": [
                # Direct hinge endpoint, then local maxima sampled from the
                # hash-pinned Ardacraft relief at the listed longitudes. The
                # former guide ran north of the visible Ered Lithui by as much
                # as 0.034 canvas-height and was therefore support-clipped.
                [0.621978, 0.531998], [0.625000, 0.544211],
                [0.637000, 0.545188], [0.650000, 0.543723],
                [0.666000, 0.544211], [0.680000, 0.545677],
                [0.694000, 0.544700], [0.707000, 0.542745],
                [0.719000, 0.533464], [0.730000, 0.530044],
                [0.740000, 0.529555],
            ],
        },
        {
            "key": "mountains_of_shadow_south",
            "width": 0.011,
            "height": 0.94,
            "wander": 0.0010,
            "points": [
                [0.681, 0.703], [0.661, 0.720], [0.636, 0.728],
                [0.611, 0.724], [0.590, 0.708],
            ],
        },
        {
            "key": "iron_hills",
            "width": 0.008,
            "height": 0.74,
            "wander": 0.0010,
            "points": [
                [0.602, 0.098], [0.628, 0.091], [0.653, 0.094],
                [0.676, 0.106],
            ],
        },
        {
            "key": "mountains_of_mirkwood",
            "width": 0.007,
            "height": 0.66,
            "wander": 0.0010,
            "points": [
                [0.550, 0.208], [0.558, 0.240], [0.561, 0.273],
                [0.557, 0.307],
            ],
        },
    ]
    # The hash-pinned Ardacraft relief field owns exact crest placement and
    # branching. Live v33 evidence nevertheless proved that a blanket 18%
    # residual made the White Mountains and Mordor walls read as green hills.
    # Retain source-aligned narrow axes as range-specific vertical continuity:
    # the enclosing Mordor walls and White Mountains need the strongest lift,
    # while the smaller Iron/Mirkwood chains stay subordinate.
    relief_weights = {
        "misty_mountains": 0.40,
        "grey_mountains": 0.38,
        "ered_luin": 0.34,
        "white_mountains": 0.48,
        "ephel_duath": 0.50,
        "ered_lithui": 0.50,
        "mountains_of_shadow_south": 0.46,
        "iron_hills": 0.32,
        "mountains_of_mirkwood": 0.28,
    }
    if {ridge["key"] for ridge in ridges} != set(relief_weights):
        raise ValueError("range-specific relief-weight review is incomplete")
    for ridge in ridges:
        ridge["relief_weight"] = relief_weights[ridge["key"]]
    # v35 proved that exact source crests alone still leave renderer-scale gaps
    # in the two live-rejected walls.  These gains apply only after the axis is
    # multiplied by a soft dilation of the Ardacraft support field; unlike the
    # rejected blanket weight increase, they cannot create high terrain away
    # from the source range footprint.
    source_supported_gains = {
        "white_mountains": 1.65,
        "ephel_duath": 1.75,
        "ered_lithui": 1.75,
        "mountains_of_shadow_south": 1.65,
    }
    for ridge in ridges:
        if ridge["key"] in source_supported_gains:
            ridge["source_supported_gain"] = source_supported_gains[ridge["key"]]

    def named_source_point(collection: str, event_name: str) -> list[float]:
        matches = [
            geometry
            for geometry in source["objects"][collection]["geometries"]
            if (geometry.get("properties") or {}).get("eventname") == event_name
        ]
        if len(matches) != 1:
            raise ValueError(
                f"expected one {collection} point named {event_name}, got {len(matches)}"
            )
        return topology.point(matches[0])

    # Pass masks are intentionally narrow. The previous 0.012-0.015 radii
    # carved round lowland holes through whole source massifs and even erased
    # Caradhras. Named controls use exact Arda Maps points where available;
    # the remaining three are hand-reconciled corridor centres.
    passes = [
        {
            "key": "lindon_road",
            "center": [0.309, 0.225],
            "radius": 0.0055,
            "source": "Arda Maps/ArdaCraft reconciled",
        },
        {
            "key": "gundabad_gate",
            # The v31 live audit proved that carving the pass at the exact
            # point_mount coordinate erased Mount Gundabad itself. This is the
            # already reviewed main-land approach immediately north-east of
            # the summit; the peak remains exact and the saddle remains open.
            "center": [0.506471, 0.097215],
            "radius": 0.0040,
            "source": "Arda Maps/ArdaCraft reconciled",
        },
        {
            "key": "high_pass",
            "center": named_source_point("point_place", "GoblinGate"),
            "radius": 0.0055,
            "source": "Arda Maps point_place",
        },
        {
            "key": "imladris_valley",
            "center": named_source_point("point_ford", "FordOfBruinen"),
            "radius": 0.0045,
            "source": "Arda Maps point_ford",
        },
        {
            "key": "redhorn_gate",
            "center": named_source_point("point_place", "RedhornGate"),
            "radius": 0.0040,
            "source": "Arda Maps point_place",
        },
        {
            "key": "gap_of_rohan",
            "center": [0.466, 0.462],
            "radius": 0.0060,
            "source": "Arda Maps/ArdaCraft reconciled",
        },
        {
            "key": "paths_of_the_dead",
            "center": named_source_point("point_place", "PathsOfTheDead"),
            "radius": 0.0040,
            # The road crosses the east-west White Mountains.  Keep the
            # saddle long north-south but very narrow along the range so the
            # Starkhorn/Dunharrow flanks survive immediately beside it.
            "range_tangent": [1.0, 0.0],
            "source": "Arda Maps point_place",
        },
        {
            "key": "mindolluin_road",
            "center": [0.582, 0.610],
            "radius": 0.0030,
            "source": "Arda Maps/ArdaCraft reconciled",
        },
        {
            "key": "morannon",
            "center": endore_from_world(20_090.0, 12_530.0),
            "radius": 0.0055,
            # Cirith Gorgor opens north-west/south-east at the corner where
            # Ered Lithui and Ephel Duath meet.  The perpendicular tangent
            # preserves both arms of that L-shaped wall instead of erasing a
            # circular green bowl around the Black Gate.
            "range_tangent": [1.0, -1.0],
            # Heightmap V2's colour-derived relief drops the last few pixels
            # of both walls at the low gate. These endpoints are the nearest
            # unambiguous Ered Lithui and Ephel Duath crests in that exact
            # layer; the Ardacraft drawing confirms the two connections.
            "hinge_arms": [
                endore_from_world(21_143.315692, 12_639.637986),
                endore_from_world(19_693.979792, 13_396.002095),
            ],
            "hinge_source": "Ardacraft Heightmap V2 + drawing-layer reconciliation",
            "source": "Ardacraft direct Morannon marker",
        },
        {
            "key": "cirith_ungol",
            "center": named_source_point("point_place", "ShelobsLair"),
            "radius": 0.0035,
            "source": "Arda Maps point_place",
        },
    ]

    forests = {
        "lothlorien": ("dense_forest", [0, 1, 2, 3, 4]),
        "rhun_woodlands": ("forest", [5]),
        "ithilien": (
            "forest",
            [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23],
        ),
        "druadan": ("forest", [19]),
        "blackroot_woods": ("forest", [24, 25]),
        "fangorn": ("dense_forest", [26]),
        "minhiriath_woods": ("forest", [27]),
        "eryn_vorn": ("forest", [28, 29, 30]),
        "mirkwood": ("dense_forest", [31, 32]),
        "trollshaws": ("forest", [33]),
        "chetwood": ("forest", [34]),
        "old_forest": ("dense_forest", [35]),
        "shire_woods": (
            "forest",
            list(range(36, 54)),
        ),
        "lindon_woods": ("forest", [54, 55]),
        "lossarnach_woods": ("forest", [56]),
    }
    biome_zones = [
        {
            "key": "forodwaith",
            "biome": "tundra",
            "shape": "organic_polygon",
            "coords": [
                [0.220, 0.000], [0.760, 0.000], [0.730, 0.105],
                [0.680, 0.125], [0.610, 0.110], [0.540, 0.120],
                [0.470, 0.105], [0.400, 0.125], [0.330, 0.105],
                [0.270, 0.115],
            ],
        }
    ]
    for key, (biome, indexes) in forests.items():
        polygons = source_multi_polygon(topology, "poly_forest", indexes)
        biome_zones.append(
            {
                "key": key,
                "biome": biome,
                "shape": "source_polygon" if len(polygons) == 1 else "multi_polygon",
                "coords": polygons[0] if len(polygons) == 1 else polygons,
            }
        )
    biome_zones.extend(
        [
            {
                "key": "dead_marshes",
                "biome": "marsh",
                "shape": "source_polygon",
                "coords": source_polygon(
                    topology, "poly_moor", 0, epsilon=0.00010
                ),
                "source": "Arda Maps poly_moor 0",
            },
            {
                "key": "brown_lands",
                "biome": "steppe",
                "shape": "multi_polygon",
                "coords": brown_lands_polygons,
                "source_labels": ["M6"],
                "source": "Ardacraft Biome layer Middle-earth V3",
            },
            {
                "key": "rhun_steppe",
                "biome": "steppe",
                "shape": "multi_polygon",
                "coords": rhun_steppe_polygons,
                "source_labels": sorted(rhun_steppe_labels),
                "source": "Ardacraft Biome layer Middle-earth V3",
            },
            {
                "key": "rhun_source_edge_continuation",
                "biome": "steppe",
                "shape": "organic_polygon",
                "coords": [
                    [0.744, 0.205], [0.783, 0.195], [0.824, 0.211],
                    [0.861, 0.196], [0.879, 0.278], [0.872, 0.376],
                    [0.883, 0.468], [0.868, 0.573], [0.842, 0.657],
                    [0.798, 0.701], [0.756, 0.679], [0.738, 0.604],
                    [0.751, 0.527], [0.743, 0.438], [0.756, 0.346],
                ],
                "source": (
                    "Judgment: continuous east-edge extension from Ardacraft "
                    "L/M/Z steppe polygons beyond its equal-scale image bound"
                ),
            },
            {
                "key": "near_harad_scrub",
                "biome": "steppe",
                "shape": "multi_polygon",
                "coords": harad_steppe_polygons,
                "source_labels": sorted(harad_steppe_labels),
                "source": "Ardacraft Biome layer Middle-earth V3",
            },
            {
                "key": "harad_source_edge_scrub",
                "biome": "steppe",
                "shape": "organic_polygon",
                "coords": [
                    [0.724, 0.653], [0.771, 0.642], [0.815, 0.666],
                    [0.861, 0.650], [0.879, 0.721], [0.867, 0.789],
                    [0.828, 0.834], [0.778, 0.820], [0.739, 0.786],
                ],
                "source": (
                    "Judgment: continuous east-edge extension from Ardacraft "
                    "Near Harad scrub polygons beyond its equal-scale image bound"
                ),
            },
            {
                "key": "far_harad_arid",
                "biome": "arid",
                "shape": "multi_polygon",
                "coords": harad_arid_polygons,
                "source_labels": sorted(harad_arid_labels),
                "source": "Ardacraft Biome layer Middle-earth V3",
            },
            {
                "key": "harad_source_edge_arid",
                "biome": "arid",
                "shape": "organic_polygon",
                "coords": [
                    [0.723, 0.792], [0.770, 0.783], [0.817, 0.804],
                    [0.864, 0.786], [0.883, 0.872], [0.875, 1.000],
                    [0.724, 1.000], [0.735, 0.913],
                ],
                "source": (
                    "Judgment: continuous east-edge extension from Ardacraft "
                    "H3/H4/H5 arid polygons beyond its equal-scale image bound"
                ),
            },
            # Paint Mordor after eastern climate controls so its exact source
            # enclosure remains ash rather than being overwritten by Z-steppe.
            {
                "key": "mordor",
                "biome": "ash",
                "shape": "source_proximity_field",
                "source_zone_keys": [
                    "low_08", "low_09", "low_10", "low_11"
                ],
                "anchor": named_source_point("point_mount", "MountDoom"),
                "bounds": [0.592, 0.495, 0.758, 0.710],
                "seal_radius": 0.003,
                "edge_feather": 0.004,
                "east_closure_wander": 0.006,
                "threshold": 0.120,
                "source": (
                    "Arda Maps poly_mountainlow 8-11 and "
                    "point_mount MountDoom"
                ),
            },
        ]
    )

    density_zones = [
        {"key": "eriador_settled", "shape": "organic_polygon", "coords": [[0.30,0.15],[0.50,0.15],[0.51,0.34],[0.31,0.35]], "value": 205},
        {"key": "anduin_vale", "shape": "organic_polygon", "coords": [[0.49,0.12],[0.57,0.12],[0.57,0.43],[0.49,0.43]], "value": 190},
        {"key": "rohan", "shape": "organic_polygon", "coords": [[0.44,0.47],[0.57,0.46],[0.58,0.58],[0.45,0.59]], "value": 210},
        {"key": "gondor", "shape": "organic_polygon", "coords": [[0.45,0.56],[0.61,0.56],[0.61,0.72],[0.44,0.72]], "value": 220},
        {"key": "dale_erebor", "shape": "organic_polygon", "coords": [[0.57,0.11],[0.63,0.11],[0.63,0.19],[0.57,0.19]], "value": 220},
        {"key": "mordor", "shape": "organic_polygon", "coords": [[0.60,0.51],[0.75,0.51],[0.72,0.72],[0.60,0.72]], "value": 195},
        {"key": "umbar_coast", "shape": "organic_polygon", "coords": [[0.45,0.84],[0.58,0.84],[0.58,0.98],[0.44,0.98]], "value": 190},
    ]

    upper_anduin, lower_anduin = anduin_geometries(topology)
    river_specs = [
        ("langwell", "Langwell", "anduin", 0.0018, (0.515, 0.105)),
        ("greylin", "Greylin", "anduin", 0.0018, (0.515, 0.105)),
        ("gladden", "GladdenRiver", "anduin", 0.0020, (0.520, 0.285)),
        ("celebrant", "Celebrant", "anduin", 0.0022, (0.540, 0.355)),
        ("limlight", "Limlight", "anduin", 0.0020, (0.545, 0.410)),
        ("entwash", "Entwash", "anduin", 0.0025, (0.565, 0.505)),
        ("snowbourn", "Snowbourn", "entwash", 0.0017, (0.515, 0.535)),
        ("baranduin", "Brandywine", None, 0.0040, (0.295, 0.390)),
        ("mitheithel", "Hoarwell", "greyflood", 0.0022, (0.385, 0.430)),
        ("bruinen", "Bruinen", "mitheithel", 0.0019, (0.430, 0.290)),
        ("greyflood", "Gwathlo", None, 0.0042, (0.335, 0.455)),
        ("glanduin", "Glanduin", "greyflood", 0.0019, (0.410, 0.390)),
        ("isen", "Isen", None, 0.0038, (0.390, 0.590)),
        ("morthond", "Morthond", "ringlo", 0.0020, (0.470, 0.680)),
        ("ringlo", "Ringlo", None, 0.0019, (0.505, 0.690)),
        ("gilrain", "Gilrain", None, 0.0018, (0.545, 0.700)),
        ("celduin", "RiverRunning", None, 0.0042, (0.715, 0.345)),
        ("forest_river", "ForestRiver", None, 0.0018, (0.600, 0.165)),
        ("carnen", "Carnen", "celduin", 0.0033, (0.715, 0.345)),
        ("poros", "Poros", "anduin", 0.0030, (0.620, 0.725)),
        ("lefnui", "Lefnui", None, 0.0028, (0.408670, 0.657678)),
        ("serni", "Serni", None, 0.0024, (0.540569, 0.696225)),
    ]
    rivers = [
        {
            "key": "upper_anduin",
            "width": 0.0056,
            "wander": 0.0,
            "points": orient(upper_anduin, (0.553, 0.509)),
            "source": "Arda Maps line_river 70 and 71 main stem",
        },
        {
            "key": "anduin",
            "width": 0.0068,
            "wander": 0.0,
            "points": orient(lower_anduin, (0.535, 0.717)),
            "source": "Arda Maps line_river 71 lower main stem",
        },
    ]
    for key, source_name, joins, width, mouth in river_specs:
        points = orient(river_geometry(topology, source_name), mouth)
        item = {
            "key": key,
            "width": width,
            "wander": 0.00035,
            "points": points,
            "source": f"Arda Maps line_river named {source_name}",
        }
        if joins:
            if joins == "anduin" and key in {
                "langwell",
                "greylin",
                "gladden",
                "celebrant",
                "limlight",
                "entwash",
            }:
                joins = "upper_anduin"
            item["joins"] = joins
        rivers.append(item)
    # Arda Maps does not name these two channels, but both have detailed
    # unnamed source lines in their exact corridors. Only Harnen's final
    # coastward reach requires a two-point reconciliation.
    rivers.extend(
        [
            {
                "key": "lhun",
                "width": 0.0031,
                "wander": 0.00035,
                "engine_raster": True,
                "terrain_only": False,
                "hydrology_class": "named_trunk",
                "incision_strength": 176,
                "material_scale": 1.0,
                "material_growth": 0.20,
                "points": lhun_main_geometry(topology),
                "source": "Arda Maps line_river 84 parts 1+0",
            },
            {
                "key": "morgulduin",
                "width": 0.0018,
                "wander": 0.00035,
                "joins": "anduin",
                "points": morgulduin_geometry(topology),
                "source": "Arda Maps line_river 14",
            },
            {
                "key": "harnen",
                "width": 0.0032,
                "wander": 0.00035,
                "points": harnen_geometry(topology),
                "source": "Arda Maps line_river 8 plus reconciled coastward reach",
            },
        ]
    )
    rivers.extend(supplementary_river_controls(topology))

    projection = {
        "schema": 4,
        "canvas": [16384, 8192],
        "control_resolution": [4096, 2048],
        "reference_projection": PROJECTION_CONTRACT,
        "source_relief": {
            "file": RELIEF_OUTPUT.name,
            "source": relief_payload["source"],
            "source_sha256": relief_payload["source_sha256"],
            "field_sha256": relief_payload["field_sha256"],
            "bounds": relief_payload["bounds"],
            "resolution": relief_payload["resolution"],
            "quantization_max": relief_payload["quantization_max"],
        },
        "source_biomes": {
            "source": "Ardacraft Biome layer Middle-earth V3",
            "source_sha256": ARDACRAFT_BIOMES_SHA256,
            "source_bounds": ARDACRAFT_BIOME_BOUNDS,
            "endore_bounds": ARDACRAFT_IMAGE_BOUNDS,
            "classification": {
                "brown_lands": ["M6"],
                "rhun_steppe": sorted(rhun_steppe_labels),
                "near_harad_scrub": sorted(harad_steppe_labels),
                "far_harad_arid": sorted(harad_arid_labels),
            },
        },
        "extent": previous["extent"],
        "land_polygons": {
            "mainland": source_polygon(
                topology, "poly_outline", 2, epsilon=0.00018
            ),
            **islands,
        },
        "sea_cutouts": {},
        "lakes": lakes,
        "mountain_zones": mountain_zones,
        "highland_zones": highland_zones,
        "moor_zones": moor_zones,
        "named_peaks": named_peaks,
        "ridges": ridges,
        "passes": passes,
        "biome_zones": biome_zones,
        "density_zones": density_zones,
        "rivers": rivers,
    }
    drainage_payload = ardacraft_drainage_payload(reference_root, projection)
    projection["source_drainage"] = {
        "file": DRAINAGE_OUTPUT.name,
        "source": drainage_payload["source"],
        "source_sha256": drainage_payload["source_sha256"],
        "field_sha256": drainage_payload["field_sha256"],
        "bounds": drainage_payload["bounds"],
        "resolution": drainage_payload["resolution"],
        "alpha_threshold": drainage_payload["alpha_threshold"],
        "geodesic_reach": drainage_payload["geodesic_reach"],
        "opening_radius": drainage_payload["opening_radius"],
        "terminal_prune_steps": drainage_payload["terminal_prune_steps"],
        "affluent_near_distance": drainage_payload["affluent_near_distance"],
        "affluent_far_distance": drainage_payload["affluent_far_distance"],
        "affluent_min_path": drainage_payload["affluent_min_path"],
        "affluent_paths": drainage_payload["affluent_paths"],
    }
    return projection, relief_payload, drainage_payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reference-root",
        type=Path,
        default=DEFAULT_REFERENCE_ROOT,
    )
    parser.add_argument("--write", action="store_true", required=True)
    args = parser.parse_args()
    projection, relief_payload, drainage_payload = build(args.reference_root)
    OUTPUT.write_text(
        json.dumps(projection, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    RELIEF_OUTPUT.write_text(
        json.dumps(relief_payload, separators=(",", ":"), ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    DRAINAGE_OUTPUT.write_text(
        json.dumps(drainage_payload, separators=(",", ":"), ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    print(
        "rebuild_cartography_controls: wrote "
        f"{len(projection['land_polygons']['mainland'])} mainland vertices, "
        f"{len(projection['mountain_zones'])} mountain zones, "
        f"{len(projection['highland_zones'])} highland zones, "
        f"{len(projection['moor_zones'])} moor zones, "
        f"{len(projection['biome_zones'])} biome zones, "
        f"{len(projection['rivers'])} rivers, "
        f"{drainage_payload['centreline_samples']} Ardacraft feeder samples"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
