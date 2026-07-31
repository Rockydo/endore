#!/usr/bin/env python3
"""Rebuild original ENDÓRË controls from quarantined reference measurements.

This is a development-only authoring tool. Normal validation consumes the
committed, simplified projection.json and never requires downloaded source
data. Raw reference payloads remain under G:\endore_runtime and are not copied
into the repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/world/control/projection.json"
DEFAULT_REFERENCE_ROOT = Path(r"G:\endore_runtime\cartography_references")
ARDA_MAPS_SHA256 = (
    "147a2d0ff3e36e2b675afb40dd4a74f634006bc6350a6a7c31639019fd2bd4ab"
)

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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def endore_from_world(x: float, z: float) -> list[float]:
    return [
        round(0.5 + (x - 10651.5) / 86014.0, 6),
        round((z + 10240.0) / 43007.0, 6),
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
        lower_parts[12],
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


def build(reference_root: Path) -> dict:
    source_path = reference_root / "arda_maps_third_age.json"
    if sha256(source_path) != ARDA_MAPS_SHA256:
        raise ValueError("Arda Maps payload changed; re-audit before rebuilding controls")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    topology = Topology(source)
    previous = json.loads(OUTPUT.read_text(encoding="utf-8"))

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
        named_peaks.append(
            {
                "key": key,
                "label": source_name,
                "center": topology.point(geometry),
                "radius": round(0.0035 + 0.0012 * size_class, 6),
                "strength": round(
                    subdued_peaks.get(
                        source_name,
                        min(1.0, 0.63 + 0.18 * size_class),
                    ),
                    3,
                ),
                "source": "Arda Maps point_mount",
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
        },
        {
            "key": "ephel_duath",
            "width": 0.012,
            "height": 1.00,
            "wander": 0.0010,
            "points": [
                [0.610, 0.526], [0.611, 0.558], [0.607, 0.596],
                [0.617, 0.632], [0.635, 0.665], [0.657, 0.690],
                [0.681, 0.703],
            ],
        },
        {
            "key": "ered_lithui",
            "width": 0.012,
            "height": 1.00,
            "wander": 0.0010,
            "points": [
                [0.610, 0.526], [0.637, 0.512], [0.666, 0.510],
                [0.694, 0.520], [0.719, 0.540], [0.740, 0.565],
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
            "center": named_source_point("point_mount", "Gundabad"),
            "radius": 0.0050,
            "source": "Arda Maps point_mount",
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
            "center": named_source_point("point_place", "CirithGorgor"),
            "radius": 0.0055,
            "source": "Arda Maps point_place",
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
                "shape": "organic_polygon",
                "coords": [
                    [0.590, 0.510], [0.605, 0.500], [0.620, 0.508],
                    [0.625, 0.532], [0.614, 0.552], [0.596, 0.550],
                    [0.586, 0.532],
                ],
            },
            {
                "key": "mordor",
                "biome": "ash",
                "shape": "organic_polygon",
                "coords": [
                    [0.612, 0.530], [0.640, 0.514], [0.675, 0.511],
                    [0.709, 0.525], [0.736, 0.553], [0.744, 0.589],
                    [0.730, 0.625], [0.704, 0.660], [0.681, 0.701],
                    [0.648, 0.720], [0.615, 0.714], [0.598, 0.686],
                    [0.604, 0.650], [0.607, 0.610], [0.604, 0.570],
                ],
            },
            {
                "key": "brown_lands",
                "biome": "steppe",
                "shape": "organic_polygon",
                "coords": [
                    [0.548, 0.382], [0.590, 0.360], [0.632, 0.372],
                    [0.649, 0.414], [0.640, 0.466], [0.615, 0.505],
                    [0.577, 0.500], [0.552, 0.455],
                ],
            },
            {
                "key": "rhun_steppe",
                "biome": "steppe",
                "shape": "organic_polygon",
                "coords": [
                    [0.645, 0.115], [0.790, 0.105], [1.000, 0.130],
                    [1.000, 0.510], [0.820, 0.500], [0.750, 0.455],
                    [0.705, 0.390], [0.670, 0.310],
                ],
            },
            {
                "key": "harad",
                "biome": "arid",
                "shape": "organic_polygon",
                "coords": [
                    [0.385, 0.730], [0.425, 0.708], [0.468, 0.724],
                    [0.512, 0.699], [0.558, 0.729], [0.606, 0.702],
                    [0.654, 0.727], [0.704, 0.694], [0.756, 0.716],
                    [0.810, 0.688], [0.868, 0.711], [0.928, 0.684],
                    [1.000, 0.700], [1.000, 1.000], [0.220, 1.000],
                    [0.250, 0.900], [0.310, 0.820],
                ],
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
        ("baranduin", "Brandywine", None, 0.0030, (0.295, 0.390)),
        ("mitheithel", "Hoarwell", "greyflood", 0.0022, (0.385, 0.430)),
        ("bruinen", "Bruinen", "mitheithel", 0.0019, (0.430, 0.290)),
        ("greyflood", "Gwathlo", None, 0.0031, (0.335, 0.455)),
        ("glanduin", "Glanduin", "greyflood", 0.0019, (0.410, 0.390)),
        ("isen", "Isen", None, 0.0028, (0.390, 0.590)),
        ("morthond", "Morthond", "ringlo", 0.0020, (0.470, 0.680)),
        ("ringlo", "Ringlo", None, 0.0019, (0.505, 0.690)),
        ("gilrain", "Gilrain", None, 0.0018, (0.545, 0.700)),
        ("celduin", "RiverRunning", None, 0.0031, (0.715, 0.345)),
        ("forest_river", "ForestRiver", None, 0.0018, (0.600, 0.165)),
        ("carnen", "Carnen", "celduin", 0.0026, (0.715, 0.345)),
        ("poros", "Poros", "anduin", 0.0022, (0.620, 0.725)),
    ]
    rivers = [
        {
            "key": "upper_anduin",
            "width": 0.0040,
            "wander": 0.0,
            "points": orient(upper_anduin, (0.553, 0.509)),
        },
        {
            "key": "anduin",
            "width": 0.0048,
            "wander": 0.0,
            "points": orient(lower_anduin, (0.535, 0.717)),
        },
    ]
    for key, source_name, joins, width, mouth in river_specs:
        points = orient(river_geometry(topology, source_name), mouth)
        item = {
            "key": key,
            "width": width,
            "wander": 0.00035,
            "points": points,
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
                "key": "morgulduin",
                "width": 0.0018,
                "wander": 0.00035,
                "joins": "anduin",
                "points": morgulduin_geometry(topology),
            },
            {
                "key": "harnen",
                "width": 0.0025,
                "wander": 0.00035,
                "points": harnen_geometry(topology),
            },
        ]
    )

    return {
        "schema": 3,
        "canvas": [16384, 8192],
        "control_resolution": [4096, 2048],
        "reference_projection": PROJECTION_CONTRACT,
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
        "named_peaks": named_peaks,
        "ridges": ridges,
        "passes": passes,
        "biome_zones": biome_zones,
        "density_zones": density_zones,
        "rivers": rivers,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reference-root",
        type=Path,
        default=DEFAULT_REFERENCE_ROOT,
    )
    parser.add_argument("--write", action="store_true", required=True)
    args = parser.parse_args()
    projection = build(args.reference_root)
    OUTPUT.write_text(
        json.dumps(projection, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        "rebuild_cartography_controls: wrote "
        f"{len(projection['land_polygons']['mainland'])} mainland vertices, "
        f"{len(projection['mountain_zones'])} mountain zones, "
        f"{len(projection['biome_zones'])} biome zones, "
        f"{len(projection['rivers'])} rivers"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
