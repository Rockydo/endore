#!/usr/bin/env python3
"""Validate the committed Arda Maps/ArdaCraft cartographic crosswalk."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "docs/world/control"
TARGETS = CONTROL / "cartography_targets.csv"
SETTLEMENTS = CONTROL / "settlements.csv"
LANDMARKS = CONTROL / "m3_landmarks.csv"
REALMS = ROOT / "docs/world/realms.csv"
PROJECTION = CONTROL / "projection.json"
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
    "04696d43a3d14a6c0774bf339194cf119281f5639b1c48a3b31a2ed44f1399fe"
)
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
    feature_counts = {
        "mainland_vertices": len(projection["land_polygons"]["mainland"]),
        "offshore_islands": len(projection["land_polygons"]) - 1,
        "lakes": len(projection["lakes"]),
        "mountain_footprints": len(projection["mountain_zones"]),
        "named_peaks": len(projection.get("named_peaks", [])),
        "ridge_axes": len(projection["ridges"]),
        "passes": len(projection["passes"]),
        "river_valley_controls": len(projection["rivers"]),
        "biome_zones": len(projection["biome_zones"]),
    }
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
    feature_counts["river_control_vertices"] = sum(
        len(item["points"]) for item in projection["rivers"]
    )
    minimums = {
        "mainland_vertices": 1_200,
        "offshore_islands": 8,
        "lakes": 15,
        "mountain_footprints": 40,
        "named_peaks": 18,
        "ridge_axes": 9,
        "passes": 10,
        "river_valley_controls": 24,
        "biome_zones": 21,
        "forest_source_zones": 15,
        "forest_source_components": 57,
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
    }
    river_by_key = {item["key"]: item for item in projection["rivers"]}
    if set(river_by_key) != expected_river_keys:
        raise ValueError("named river coverage changed without cartographic review")
    if len(river_by_key["harnen"]["points"]) < 50:
        raise ValueError("source-backed Harnen detail regressed")
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
        if peak.get("source") != "Arda Maps point_mount":
            raise ValueError(f"{peak['key']} lost its Arda Maps point provenance")
        x, y = peak["center"]
        if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
            raise ValueError(f"{peak['key']} lies outside the production canvas")
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
        "schema": 3,
        "projection": EXPECTED_PROJECTION,
        "projection_sha256": projection_sha256,
        "feature_counts": feature_counts,
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
