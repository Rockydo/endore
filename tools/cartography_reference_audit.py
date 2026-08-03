#!/usr/bin/env python3
"""Validate the committed Arda Maps/ArdaCraft cartographic crosswalk."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import math
import zlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "docs/world/control"
TARGETS = CONTROL / "cartography_targets.csv"
SETTLEMENTS = CONTROL / "settlements.csv"
LANDMARKS = CONTROL / "m3_landmarks.csv"
REALMS = ROOT / "docs/world/realms.csv"
PROJECTION = CONTROL / "projection.json"
RELIEF = CONTROL / "ardacraft_relief.json"
DRAINAGE = CONTROL / "ardacraft_drainage.json"
REPORT = ROOT / "docs/world/derived/cartography_conformance.json"

EXPECTED_PROJECTION = {
    "source": "ardacraft_equal_scale_grid",
    "x_center": 10651.5,
    "z_min": -10240.0,
    "z_max": 32767.0,
    "world_span": 43007.0,
    "canvas_aspect": 2.0,
}
EXPECTED_PROJECTION_SHA256 = (
    "1d8bd87f373a742b5ed956118f4aedd599fb166963e9d3551db2800a85a3e8b6"
)
EXPECTED_RELIEF_FILE_SHA256 = (
    "666ab17a55a268b801a51dcebeede662ee3f4e840bf497fe61c6300b170505c1"
)
EXPECTED_ARDACRAFT_HEIGHTMAP_SHA256 = (
    "a1b05874cd447b9868c0d56a4fad523e5fc94053fa239dc5df7e0b31068144be"
)
EXPECTED_ARDACRAFT_BIOMES_SHA256 = (
    "2070d5577d768b2d418fd06e61d2fbafb5b55599340540fd9308ead213037997"
)
EXPECTED_DRAINAGE_FILE_SHA256 = (
    "ff625cbb64e4806a031087b4b00a0541f349f1226803771521519625251f4a0f"
)
EXPECTED_ARDACRAFT_DRAINAGE_SHA256 = (
    "d8ec6f22c0e3c87097145f2c3f3b831c778e4df8b705595d335e5c4d7be74871"
)
EXPECTED_SOURCE_BIOME_CLASSES = {
    "brown_lands": ["M6"],
    "rhun_steppe": [
        "L3", "L5", "L7", "M11", "M18", "M2", "M20", "M7",
        "Z2", "Z3", "Z4", "Z5",
    ],
    "near_harad_scrub": [
        "H1", "H2", "H6", "H7", "J22", "J48", "J49", "K23",
        "K31", "N4",
    ],
    "far_harad_arid": ["H3", "H4", "H5"],
}
EXPECTED_FOREST_KEYS = {
    "lothlorien",
    "rhun_woodlands",
    "ithilien",
    "druadan",
    "blackroot_woods",
    "fangorn",
    "minhiriath_woods",
    "eryn_vorn",
    "mirkwood",
    "trollshaws",
    "chetwood",
    "old_forest",
    "shire_woods",
    "lindon_woods",
    "lossarnach_woods",
}
SOURCE_DRAINAGE_THEATRES = {
    "northern_basins": {
        "bbox": (0.35, 0.00, 0.80, 0.32),
        "minimum_controls": 27,
        "minimum_points": 515,
        "minimum_length": 1.54,
    },
    "anduin_system": {
        "bbox": (0.42, 0.12, 0.68, 0.62),
        "minimum_controls": 62,
        "minimum_points": 860,
        "minimum_length": 2.54,
    },
    "white_mountains": {
        "bbox": (0.25, 0.43, 0.63, 0.68),
        "minimum_controls": 35,
        "minimum_points": 560,
        "minimum_length": 1.60,
    },
    "mordor_gondor": {
        "bbox": (0.52, 0.43, 0.80, 0.75),
        "minimum_controls": 46,
        "minimum_points": 565,
        "minimum_length": 1.46,
    },
}
SOURCE_FEEDER_THEATRES = {
    "northern_basins": ((0.35, 0.00, 0.80, 0.32), 750),
    "anduin_system": ((0.42, 0.12, 0.68, 0.62), 1_150),
    "white_mountains": ((0.25, 0.43, 0.63, 0.68), 800),
    "mordor_gondor": ((0.52, 0.43, 0.80, 0.75), 450),
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def render_report() -> dict:
    targets = rows(TARGETS)
    settlements = rows(SETTLEMENTS)
    landmarks = rows(LANDMARKS)
    realms = rows(REALMS)
    if not targets:
        raise ValueError("cartography target ledger is empty")
    target_by_key = {row["key"]: row for row in targets}
    settlement_by_key = {row["key"]: row for row in settlements}
    if len(target_by_key) != len(targets):
        raise ValueError("duplicate cartography target key")
    if set(target_by_key) != set(settlement_by_key):
        missing = sorted(set(target_by_key) - set(settlement_by_key))
        extra = sorted(set(settlement_by_key) - set(target_by_key))
        raise ValueError(
            f"cartography/settlement key mismatch: missing={missing}, extra={extra}"
        )

    projection_bytes = PROJECTION.read_bytes()
    projection_sha256 = hashlib.sha256(projection_bytes).hexdigest()
    if projection_sha256 != EXPECTED_PROJECTION_SHA256:
        raise ValueError(
            "binding source-derived projection geometry changed without "
            "cartographic review"
        )
    projection = json.loads(projection_bytes)
    actual_projection = projection.get("reference_projection")
    if actual_projection != EXPECTED_PROJECTION:
        raise ValueError(
            "projection.json does not declare the binding equal-scale "
            "ArdaCraft projection contract"
        )
    if not RELIEF.is_file():
        raise ValueError("committed Ardacraft-derived numeric relief field is missing")
    relief_bytes = RELIEF.read_bytes()
    if hashlib.sha256(relief_bytes).hexdigest() != EXPECTED_RELIEF_FILE_SHA256:
        raise ValueError("binding Ardacraft-derived relief field changed without review")
    relief = json.loads(relief_bytes)
    descriptor = projection.get("source_relief")
    if (
        not isinstance(descriptor, dict)
        or descriptor.get("file") != RELIEF.name
        or relief.get("source_sha256") != EXPECTED_ARDACRAFT_HEIGHTMAP_SHA256
        or relief.get("source_sha256") != descriptor.get("source_sha256")
        or relief.get("field_sha256") != descriptor.get("field_sha256")
        or relief.get("resolution") != [2500, 2003]
        or relief.get("quantization_max") != 255
        or relief.get("encoding") != "zlib_base85_u8"
        or relief.get("nonzero_samples", 0) < 400_000
    ):
        raise ValueError("Ardacraft-derived relief provenance or detail regressed")
    if not DRAINAGE.is_file():
        raise ValueError("committed Ardacraft-derived numeric drainage field is missing")
    drainage_bytes = DRAINAGE.read_bytes()
    if hashlib.sha256(drainage_bytes).hexdigest() != EXPECTED_DRAINAGE_FILE_SHA256:
        raise ValueError("binding Ardacraft-derived drainage field changed without review")
    drainage = json.loads(drainage_bytes)
    drainage_descriptor = projection.get("source_drainage")
    if (
        not isinstance(drainage_descriptor, dict)
        or drainage_descriptor.get("file") != DRAINAGE.name
        or drainage.get("schema") != 2
        or drainage.get("source_sha256") != EXPECTED_ARDACRAFT_DRAINAGE_SHA256
        or drainage.get("source_sha256") != drainage_descriptor.get("source_sha256")
        or drainage.get("field_sha256") != drainage_descriptor.get("field_sha256")
        or drainage.get("resolution") != [2500, 2003]
        or drainage.get("alpha_threshold") != 160
        or drainage.get("geodesic_reach") != 24
        or drainage.get("opening_radius") != 1
        or drainage.get("terminal_prune_steps") != 8
        or drainage.get("affluent_near_distance") != 4
        or drainage.get("affluent_far_distance") != 20
        or drainage.get("affluent_min_path") != 16
        or drainage.get("affluent_near_distance")
        != drainage_descriptor.get("affluent_near_distance")
        or drainage.get("affluent_far_distance")
        != drainage_descriptor.get("affluent_far_distance")
        or drainage.get("affluent_min_path")
        != drainage_descriptor.get("affluent_min_path")
        or drainage.get("affluent_paths")
        != drainage_descriptor.get("affluent_paths")
        or not (50 <= drainage.get("affluent_paths", 0) <= 75)
        or drainage.get("encoding") != "zlib_base85_u8"
        or not (1_800 <= drainage.get("centreline_samples", 0) <= 2_300)
        or not (160_000 <= drainage.get("selected_samples", 0) <= 180_000)
    ):
        raise ValueError("Ardacraft-derived drainage provenance or detail regressed")
    try:
        drainage_raw = zlib.decompress(
            base64.b85decode(drainage["data"].encode("ascii"))
        )
    except (KeyError, ValueError, zlib.error) as exc:
        raise ValueError("Ardacraft-derived drainage payload is invalid") from exc
    if len(drainage_raw) != 2500 * 2003:
        raise ValueError("Ardacraft-derived drainage payload has the wrong size")
    drainage_field = np.frombuffer(drainage_raw, dtype=np.uint8).reshape((2003, 2500))
    if np.any(drainage_field > 1):
        raise ValueError("Ardacraft-derived drainage payload is not binary")
    if hashlib.sha256(drainage_field.tobytes()).hexdigest() != drainage["field_sha256"]:
        raise ValueError("Ardacraft-derived drainage field checksum changed")
    feeder_y, feeder_x = np.where(drainage_field > 0)
    feeder_x = 0.148481643 + feeder_x / 2499.0 * (0.774972679 - 0.148481643)
    feeder_y = feeder_y / 2002.0
    feeder_theatres = {}
    for key, (bbox, minimum_samples) in SOURCE_FEEDER_THEATRES.items():
        x0, y0, x1, y1 = bbox
        samples = int(
            (
                (feeder_x >= x0)
                & (feeder_x <= x1)
                & (feeder_y >= y0)
                & (feeder_y <= y1)
            ).sum()
        )
        if samples < minimum_samples:
            raise ValueError(f"{key} lost source-connected feeder density")
        feeder_theatres[key] = {
            "bbox": list(bbox),
            "centreline_samples": samples,
            "minimum_samples": minimum_samples,
        }
    biome_descriptor = projection.get("source_biomes")
    if (
        not isinstance(biome_descriptor, dict)
        or biome_descriptor.get("source")
        != "Ardacraft Biome layer Middle-earth V3"
        or biome_descriptor.get("source_sha256")
        != EXPECTED_ARDACRAFT_BIOMES_SHA256
        or biome_descriptor.get("classification")
        != EXPECTED_SOURCE_BIOME_CLASSES
        or biome_descriptor.get("endore_bounds")
        != [0.148481643, 0.0, 0.774972679, 1.0]
    ):
        raise ValueError("Ardacraft-derived biome provenance or classes regressed")
    feature_counts = {
        "mainland_vertices": len(projection["land_polygons"]["mainland"]),
        "offshore_islands": len(projection["land_polygons"]) - 1,
        "lakes": len(projection["lakes"]),
        "mountain_footprints": len(projection["mountain_zones"]),
        "highland_footprints": len(projection.get("highland_zones", [])),
        "moor_footprints": len(projection.get("moor_zones", [])),
        "named_peaks": len(projection.get("named_peaks", [])),
        "ridge_axes": len(projection["ridges"]),
        "passes": len(projection["passes"]),
        "river_valley_controls": len(projection["rivers"]),
        "biome_zones": len(projection["biome_zones"]),
    }
    feature_counts["highland_source_vertices"] = sum(
        len(item["coords"])
        for item in projection.get("highland_zones", [])
    )
    feature_counts["moor_source_vertices"] = sum(
        len(item["coords"])
        for item in projection.get("moor_zones", [])
    )
    forest_zones = [
        item
        for item in projection["biome_zones"]
        if item["biome"] in {"forest", "dense_forest"}
    ]
    forest_components = sum(
        len(item["coords"]) if item["shape"] == "multi_polygon" else 1
        for item in forest_zones
    )
    feature_counts["forest_source_zones"] = len(forest_zones)
    feature_counts["forest_source_components"] = forest_components
    source_climate_zones = [
        item
        for item in projection["biome_zones"]
        if item.get("source") == "Ardacraft Biome layer Middle-earth V3"
    ]
    feature_counts["source_climate_zones"] = len(source_climate_zones)
    feature_counts["source_climate_components"] = sum(
        len(item["coords"]) for item in source_climate_zones
    )
    feature_counts["source_climate_vertices"] = sum(
        len(polygon)
        for item in source_climate_zones
        for polygon in item["coords"]
    )
    feature_counts["river_control_vertices"] = sum(
        len(item["points"]) for item in projection["rivers"]
    )
    minimums = {
        "mainland_vertices": 1_200,
        "offshore_islands": 8,
        "lakes": 15,
        "mountain_footprints": 40,
        "highland_footprints": 190,
        "moor_footprints": 8,
        "highland_source_vertices": 10_000,
        "moor_source_vertices": 200,
        "named_peaks": 18,
        "ridge_axes": 9,
        "passes": 10,
        "river_valley_controls": 24,
        "biome_zones": 25,
        "forest_source_zones": 15,
        "forest_source_components": 57,
        "source_climate_zones": 4,
        "source_climate_components": 86,
        "source_climate_vertices": 7_400,
        "river_control_vertices": 800,
    }
    for key, minimum in minimums.items():
        if feature_counts[key] < minimum:
            raise ValueError(
                f"cartographic feature coverage regressed: {key} "
                f"{feature_counts[key]} < {minimum}"
            )
    if len(forest_zones) != 15 or forest_components != 57:
        raise ValueError(
            "Arda Maps forest coverage changed without cartographic review: "
            f"{len(forest_zones)} zones / {forest_components} components"
        )
    if any(
        item["shape"] not in {"source_polygon", "multi_polygon"}
        for item in forest_zones
    ):
        raise ValueError("one or more named forests lost source-polygon geometry")
    if {item["key"] for item in forest_zones} != EXPECTED_FOREST_KEYS:
        raise ValueError("named forest coverage changed without cartographic review")
    source_climate_by_key = {item["key"]: item for item in source_climate_zones}
    if set(source_climate_by_key) != set(EXPECTED_SOURCE_BIOME_CLASSES):
        raise ValueError("source-derived macro climate coverage changed")
    expected_components = {
        "brown_lands": 1,
        "rhun_steppe": 41,
        "near_harad_scrub": 37,
        "far_harad_arid": 7,
    }
    for key, labels in EXPECTED_SOURCE_BIOME_CLASSES.items():
        zone = source_climate_by_key[key]
        if (
            zone.get("shape") != "multi_polygon"
            or zone.get("source_labels") != labels
            or len(zone.get("coords", [])) != expected_components[key]
        ):
            raise ValueError(f"{key} lost its reviewed source-biome reduction")
    highland_zones = projection.get("highland_zones", [])
    moor_zones = projection.get("moor_zones", [])
    if len(highland_zones) != 190 or len(moor_zones) != 8:
        raise ValueError(
            "Arda Maps upland coverage changed without cartographic review"
        )
    for collection, zones, provenance in (
        ("highland", highland_zones, "Arda Maps poly_highland"),
        ("moor", moor_zones, "Arda Maps poly_moor"),
    ):
        if any(item.get("shape") != "source_polygon" for item in zones):
            raise ValueError(f"one or more {collection}s lost source geometry")
        if any(item.get("source") != provenance for item in zones):
            raise ValueError(f"one or more {collection}s lost source provenance")
    dead_marshes = next(
        item for item in projection["biome_zones"]
        if item["key"] == "dead_marshes"
    )
    if (
        dead_marshes.get("shape") != "source_polygon"
        or dead_marshes.get("source") != "Arda Maps poly_moor 0"
    ):
        raise ValueError("Dead Marshes regressed to hand-authored geometry")
    mordor = next(
        item for item in projection["biome_zones"]
        if item["key"] == "mordor"
    )
    if (
        mordor.get("shape") != "source_proximity_field"
        or mordor.get("source_zone_keys")
        != ["low_08", "low_09", "low_10", "low_11"]
        or "inside_ridges" in mordor
        or not math.isclose(float(mordor.get("seal_radius", 0.0)), 0.003)
        or not math.isclose(float(mordor.get("edge_feather", 0.0)), 0.004)
        or not math.isclose(
            float(mordor.get("east_closure_wander", 0.0)), 0.006
        )
        or mordor.get("source")
        != "Arda Maps poly_mountainlow 8-11 and point_mount MountDoom"
    ):
        raise ValueError("Mordor regressed to a hand-authored oval")
    expected_river_keys = {
        "upper_anduin",
        "anduin",
        "langwell",
        "greylin",
        "gladden",
        "celebrant",
        "limlight",
        "entwash",
        "snowbourn",
        "baranduin",
        "mitheithel",
        "bruinen",
        "greyflood",
        "glanduin",
        "isen",
        "morthond",
        "ringlo",
        "gilrain",
        "celduin",
        "forest_river",
        "carnen",
        "poros",
        "morgulduin",
        "harnen",
        "lhun",
        "lefnui",
        "serni",
    }
    river_by_key = {item["key"]: item for item in projection["rivers"]}
    if not expected_river_keys.issubset(river_by_key):
        raise ValueError("binding named river coverage changed without review")
    terrain_only_rivers = [
        item for item in projection["rivers"] if item.get("terrain_only")
    ]
    if len(projection["rivers"]) != 102 or len(terrain_only_rivers) != 76:
        raise ValueError("source tributary coverage changed without cartographic review")
    named_supplementary_count = sum(
        bool(item.get("label")) for item in terrain_only_rivers
    )
    total_river_points = sum(len(item["points"]) for item in projection["rivers"])
    total_river_length = sum(
        math.dist(start, end)
        for item in projection["rivers"]
        for start, end in zip(item["points"], item["points"][1:], strict=False)
    )
    if named_supplementary_count != 26:
        raise ValueError("named/unnamed supplementary drainage balance changed")
    if total_river_points < 1_700 or total_river_length < 4.85:
        raise ValueError("source river detail was over-simplified")
    if any(
        not str(item.get("source", "")).startswith("Arda Maps")
        for item in projection["rivers"]
    ):
        raise ValueError("a river control lost its hash-pinned source provenance")
    independent_engine_rivers = [
        item
        for item in projection["rivers"]
        if not item.get("terrain_only") and not item.get("joins")
    ]
    if len(independent_engine_rivers) != 12:
        raise ValueError("parser-safe independent river coverage changed")
    drainage_theatres = {}
    for key, contract in SOURCE_DRAINAGE_THEATRES.items():
        x0, y0, x1, y1 = contract["bbox"]
        controls = set()
        points = 0
        length = 0.0
        for river in projection["rivers"]:
            river_points = river["points"]
            inside = [
                x0 <= x <= x1 and y0 <= y <= y1 for x, y in river_points
            ]
            if any(inside):
                controls.add(river["key"])
            points += sum(inside)
            for start, end in zip(river_points, river_points[1:], strict=False):
                midpoint_x = (start[0] + end[0]) / 2.0
                midpoint_y = (start[1] + end[1]) / 2.0
                if x0 <= midpoint_x <= x1 and y0 <= midpoint_y <= y1:
                    length += math.dist(start, end)
        if len(controls) < contract["minimum_controls"]:
            raise ValueError(f"{key} lost source drainage controls")
        if points < contract["minimum_points"]:
            raise ValueError(f"{key} source drainage was over-simplified")
        if length < contract["minimum_length"]:
            raise ValueError(f"{key} source drainage lost too much path length")
        drainage_theatres[key] = {
            "bbox": list(contract["bbox"]),
            "controls": len(controls),
            "points": points,
            "length": round(length, 6),
            "minimum_controls": contract["minimum_controls"],
            "minimum_points": contract["minimum_points"],
            "minimum_length": contract["minimum_length"],
        }
    if any(
        item.get("engine_raster") is not False
        or not str(item.get("source", "")).startswith("Arda Maps line_river ")
        for item in terrain_only_rivers
    ):
        raise ValueError("a source tributary lost its parser-safe terrain-only contract")
    expected_supplementary_names = {
        "Adorn", "Celos", "Ciril", "EnchantedRiver", "Erui", "Fenmark",
        "Lhun", "MouthsOfEntwash", "NimrodelRiver",
        "Shirebourn", "Sirannon", "Sirith", "Stockbrook", "ThistleBrook",
        "Withywindle",
    }
    actual_supplementary_names = {
        item.get("label") for item in terrain_only_rivers if item.get("label")
    }
    if actual_supplementary_names != expected_supplementary_names:
        raise ValueError("named supplementary river coverage changed without review")
    expected_major_widths = {
        "anduin": 0.0068,
        "upper_anduin": 0.0056,
        "greyflood": 0.0042,
        "celduin": 0.0042,
        "baranduin": 0.0040,
        "isen": 0.0038,
        "carnen": 0.0033,
        "harnen": 0.0032,
        "poros": 0.0030,
        "lhun": 0.0031,
        "lefnui": 0.0028,
        "serni": 0.0024,
    }
    for key, expected_width in expected_major_widths.items():
        if not math.isclose(
            float(river_by_key[key]["width"]), expected_width, abs_tol=1e-9
        ):
            raise ValueError(f"{key} lost its reviewed major-river width")
    if len(river_by_key["harnen"]["points"]) < 50:
        raise ValueError("source-backed Harnen detail regressed")
    if len(river_by_key["morgulduin"]["points"]) < 6:
        raise ValueError("source-backed Morgulduin detail regressed")
    expected_hydrology_classes = {
        "named_branch": 7,
        "named_tributary": 19,
        "named_trunk": 1,
        "unnamed_branch": 11,
        "unnamed_feeder": 34,
        "unnamed_trunk": 4,
    }
    actual_hydrology_classes = {
        key: sum(item.get("hydrology_class") == key for item in terrain_only_rivers)
        for key in expected_hydrology_classes
    }
    if actual_hydrology_classes != expected_hydrology_classes:
        raise ValueError("reviewed tributary hierarchy changed")
    if any(
        not (96 < int(item.get("incision_strength", 0)) < 192)
        or not (0.65 <= float(item.get("material_scale", 0.0)) <= 1.0)
        or not math.isclose(
            float(item.get("material_growth", -1.0)), 0.20, abs_tol=1e-9
        )
        for item in terrain_only_rivers
    ):
        raise ValueError("parser-safe drainage presentation contract regressed")
    forbidden_duplicate_keys = {
        "source_unnamed_08_00",
        "source_unnamed_14_00",
        "source_unnamed_71_11",
        "source_unnamed_71_12",
        "source_unnamed_71_13",
        "source_unnamed_71_14",
    }
    if forbidden_duplicate_keys & river_by_key.keys():
        raise ValueError("an already-modelled source channel was duplicated")
    expected_ethir_keys = {
        f"source_unnamed_71_{index:02d}" for index in range(11)
    }
    if not expected_ethir_keys.issubset(river_by_key):
        raise ValueError("the source Ethir Anduin distributaries regressed")
    expected_confluences = {
        "langwell": "upper_anduin",
        "greylin": "upper_anduin",
        "gladden": "upper_anduin",
        "celebrant": "upper_anduin",
        "limlight": "upper_anduin",
        "entwash": "upper_anduin",
        "snowbourn": "entwash",
        "mitheithel": "greyflood",
        "bruinen": "mitheithel",
        "glanduin": "greyflood",
        "morthond": "ringlo",
        "carnen": "celduin",
        "poros": "anduin",
        "morgulduin": "anduin",
    }
    for tributary, receiving_river in expected_confluences.items():
        if river_by_key[tributary].get("joins") != receiving_river:
            raise ValueError(
                f"{tributary} no longer joins lore receiver {receiving_river}"
            )
    for collection in (
        "lakes",
        "mountain_zones",
        "named_peaks",
        "ridges",
        "passes",
        "rivers",
        "biome_zones",
        "highland_zones",
        "moor_zones",
    ):
        keys = [item["key"] for item in projection[collection]]
        if len(keys) != len(set(keys)):
            raise ValueError(f"projection repeats a {collection} key")
    expected_peak_keys = {
        "weathertop",
        "methedras",
        "celebdil",
        "fanuidhol",
        "caradhras",
        "mindolluin",
        "erech_hill",
        "thrihyrne",
        "dol_baran",
        "irensaga",
        "dwimorberg",
        "starkhorn",
        "ras_morthil",
        "carrock_height",
        "mount_gundabad",
        "erebor_peak",
        "ravenhill",
        "amon_hen",
    }
    actual_peak_keys = {item["key"] for item in projection["named_peaks"]}
    if actual_peak_keys != expected_peak_keys:
        raise ValueError("named source-peak coverage changed without cartographic review")
    for peak in projection["named_peaks"]:
        expected_source = (
            "Ardacraft direct Erebor marker"
            if peak["key"] == "erebor_peak"
            else "Arda Maps point_mount"
        )
        if peak.get("source") != expected_source:
            raise ValueError(f"{peak['key']} lost its Arda Maps point provenance")
        x, y = peak["center"]
        if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
            raise ValueError(f"{peak['key']} lies outside the production canvas")
    peak_by_key = {item["key"]: item for item in projection["named_peaks"]}
    erebor = peak_by_key["erebor_peak"]
    if erebor.get("profile") != "isolated_peak" or not math.isclose(
        float(erebor["radius"]), 0.0042, abs_tol=1e-9
    ) or any(
        not math.isclose(float(actual), expected, abs_tol=1e-9)
        for actual, expected in zip(
            erebor["center"], (0.599699, 0.137606), strict=True
        )
    ):
        raise ValueError("Erebor lost its compact isolated-peak profile")
    gundabad = peak_by_key["mount_gundabad"]
    if gundabad.get("profile") != "chain_peak" or not math.isclose(
        float(gundabad["radius"]), 0.0045, abs_tol=1e-9
    ):
        raise ValueError("Gundabad lost its compact chain-summit profile")
    source_gap_peaks = {
        peak["key"]
        for peak in projection["named_peaks"]
        if peak.get("synthetic_peak_required", False)
    }
    # v47 live evidence showed the two old source-gap fallback stamps as
    # isolated mesas. The exact, source-clipped White Mountains continuity
    # axis now covers both anchors, so no synthetic summit is permitted.
    if source_gap_peaks:
        raise ValueError("source-gap summit allowlist changed without review")
    expected_relief_weights = {
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
    for ridge in projection["ridges"]:
        if not math.isclose(
            float(ridge.get("relief_weight", -1.0)),
            expected_relief_weights[ridge["key"]],
            abs_tol=1e-9,
        ):
            raise ValueError(f"{ridge['key']} lost its reviewed continuity weight")
    expected_source_supported_gains = {
        "white_mountains": 1.65,
        "ephel_duath": 1.75,
        "ered_lithui": 1.75,
        "mountains_of_shadow_south": 1.65,
    }
    actual_source_supported_gains = {
        ridge["key"]: ridge["source_supported_gain"]
        for ridge in projection["ridges"]
        if "source_supported_gain" in ridge
    }
    if actual_source_supported_gains != expected_source_supported_gains:
        raise ValueError("source-supported severe-range gains changed")
    ridge_by_key = {ridge["key"]: ridge for ridge in projection["ridges"]}
    expected_mordor_walls = {
        "ephel_duath": {
            "width": 0.0085,
            "points": [
                [0.605128, 0.549585],
                [0.610012, 0.558000],
                [0.611477, 0.578000],
                [0.614652, 0.596000],
                [0.612454, 0.615000],
                [0.613187, 0.632000],
                [0.610745, 0.650000],
                [0.615385, 0.665000],
                [0.619780, 0.680000],
                [0.616117, 0.690000],
                [0.613675, 0.703000],
            ],
        },
        "ered_lithui": {
            "width": 0.0085,
            "points": [
                [0.621978, 0.531998],
                [0.625000, 0.544211],
                [0.637000, 0.545188],
                [0.650000, 0.543723],
                [0.666000, 0.544211],
                [0.680000, 0.545677],
                [0.694000, 0.544700],
                [0.707000, 0.542745],
                [0.719000, 0.533464],
                [0.730000, 0.530044],
                [0.740000, 0.529555],
            ],
        },
    }
    for key, expected in expected_mordor_walls.items():
        ridge = ridge_by_key[key]
        if (
            not math.isclose(
                float(ridge["width"]), expected["width"], abs_tol=1e-9
            )
            or ridge.get("sharp_cross_section") is not True
            or ridge["points"] != expected["points"]
        ):
            raise ValueError(f"{key} lost its source-aligned sharp wall contract")
    white_mountains = next(
        ridge for ridge in projection["ridges"]
        if ridge["key"] == "white_mountains"
    )
    if (
        white_mountains.get("branches") != [
            [
                [0.500, 0.566],
                [0.500845, 0.547265],
                [0.497545, 0.541502],
                [0.502831, 0.535253],
            ],
            [[0.578, 0.610], [0.585423, 0.607818]],
        ]
        or white_mountains.get("source_audited_branches") is not True
        or white_mountains.get("source_audited_branch_gains") != [0.45, 0.65]
    ):
        raise ValueError("White Mountains lost its audited peak continuations")
    expected_pass_keys = {
        "lindon_road",
        "gundabad_gate",
        "high_pass",
        "imladris_valley",
        "redhorn_gate",
        "gap_of_rohan",
        "paths_of_the_dead",
        "mindolluin_road",
        "morannon",
        "cirith_ungol",
    }
    actual_pass_keys = {item["key"] for item in projection["passes"]}
    if actual_pass_keys != expected_pass_keys:
        raise ValueError("named pass coverage changed without cartographic review")
    for pass_control in projection["passes"]:
        if not pass_control.get("source"):
            raise ValueError(f"{pass_control['key']} lacks cartographic provenance")
        if not (0.0025 <= float(pass_control["radius"]) <= 0.0060):
            raise ValueError(f"{pass_control['key']} has a non-saddle-scale radius")
    pass_by_key = {item["key"]: item for item in projection["passes"]}
    expected_oriented_saddles = {
        "paths_of_the_dead": [1.0, 0.0],
        "morannon": [1.0, -1.0],
    }
    actual_oriented_saddles = {
        item["key"]: item["range_tangent"]
        for item in projection["passes"]
        if "range_tangent" in item
    }
    if actual_oriented_saddles != expected_oriented_saddles:
        raise ValueError("source-reviewed pass orientations changed")
    morannon = pass_by_key["morannon"]
    if (
        morannon.get("center") != [0.609732, 0.529449]
        or morannon.get("source") != "Ardacraft direct Morannon marker"
    ):
        raise ValueError("Morannon lost its direct Ardacraft marker")
    if morannon.get("hinge_arms") != [
        [0.621978, 0.531998],
        [0.605128, 0.549585],
    ]:
        raise ValueError("Morannon lost its audited two-wall hinge")
    gundabad_gate = pass_by_key["gundabad_gate"]
    if (
        gundabad_gate.get("center") != [0.506471, 0.097215]
        or "access_to" in gundabad_gate
        or not math.isclose(float(gundabad_gate["radius"]), 0.0040, abs_tol=1e-9)
    ):
        raise ValueError("Gundabad saddle moved back onto the canonical summit")

    entries: list[dict] = []
    failures: list[str] = []
    for key in sorted(target_by_key):
        target = target_by_key[key]
        settlement = settlement_by_key[key]
        expected_x = float(target["target_x"])
        expected_y = float(target["target_y"])
        actual_x = float(settlement["x"])
        actual_y = float(settlement["y"])
        tolerance = float(target["tolerance"])
        deviation = math.hypot(actual_x - expected_x, actual_y - expected_y)
        passed = deviation <= tolerance
        if not passed:
            failures.append(
                f"{key} deviates {deviation:.6f}, tolerance {tolerance:.6f}"
            )
        if not target["primary_reference"].strip():
            failures.append(f"{key} lacks a primary cartographic reference")
        entries.append(
            {
                "key": key,
                "target": [expected_x, expected_y],
                "actual": [actual_x, actual_y],
                "deviation": round(deviation, 8),
                "tolerance": tolerance,
                "passed": passed,
                "primary_reference": target["primary_reference"],
            }
        )

    if failures:
        raise ValueError("; ".join(failures))
    controls = {
        row["key"]: (float(row["x"]), float(row["y"]))
        for row in settlements
    }
    manual_landmarks = 0
    for landmark in landmarks:
        reference = landmark.get("cartography_reference", "").strip()
        if not reference:
            failures.append(f"{landmark['ref']} lacks cartographic provenance")
        if reference.startswith(("Judgment:", "Reconciled:")):
            manual_landmarks += 1
        x, y = float(landmark["x"]), float(landmark["y"])
        if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
            failures.append(f"{landmark['ref']} lies outside the map frame")
        controls[landmark["ref"]] = (x, y)
    for realm in realms:
        capital_ref = realm["capital_ref"]
        if capital_ref not in controls:
            failures.append(
                f"{realm['tag']} has unresolved capital control {capital_ref}"
            )
            continue
        actual = (float(realm["x"]), float(realm["y"]))
        if actual != controls[capital_ref]:
            failures.append(
                f"{realm['tag']} seat differs from capital control {capital_ref}"
            )
    if failures:
        raise ValueError("; ".join(failures))
    return {
        "schema": 6,
        "projection": EXPECTED_PROJECTION,
        "projection_sha256": projection_sha256,
        "feature_counts": feature_counts,
        "drainage_theatres": drainage_theatres,
        "source_feeder_theatres": feeder_theatres,
        "source_feeder_samples": int(drainage_field.sum()),
        "anchor_count": len(entries),
        "landmark_count": len(landmarks),
        "manual_or_reconciled_landmarks": manual_landmarks,
        "synchronized_realm_seats": len(realms),
        "maximum_deviation": max(item["deviation"] for item in entries),
        "mean_deviation": round(
            sum(item["deviation"] for item in entries) / len(entries), 8
        ),
        "all_within_tolerance": True,
        "entries": entries,
    }


def write() -> None:
    report = render_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        "cartography_reference_audit: wrote "
        f"{report['anchor_count']} anchors, "
        f"max deviation {report['maximum_deviation']:.6f}"
    )


def check() -> list[str]:
    try:
        expected = render_report()
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]
    if not REPORT.is_file():
        return ["missing docs/world/derived/cartography_conformance.json"]
    try:
        actual = json.loads(REPORT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid cartography conformance report: {exc}"]
    if actual != expected:
        return ["cartography conformance report differs from current controls"]
    return []


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
            print(f"cartography_reference_audit: FAIL {failure}")
        return 1
    print("cartography_reference_audit: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
