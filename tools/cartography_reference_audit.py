#!/usr/bin/env python3
"""Validate the committed Arda Maps/ArdaCraft cartographic crosswalk."""

from __future__ import annotations

import argparse
import csv
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

    projection = json.loads(PROJECTION.read_text(encoding="utf-8"))
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
        "ridge_axes": len(projection["ridges"]),
        "passes": len(projection["passes"]),
        "river_valley_controls": len(projection["rivers"]),
        "biome_zones": len(projection["biome_zones"]),
    }
    minimums = {
        "mainland_vertices": 1_200,
        "offshore_islands": 8,
        "lakes": 15,
        "mountain_footprints": 40,
        "ridge_axes": 9,
        "passes": 10,
        "river_valley_controls": 24,
        "biome_zones": 21,
    }
    for key, minimum in minimums.items():
        if feature_counts[key] < minimum:
            raise ValueError(
                f"cartographic feature coverage regressed: {key} "
                f"{feature_counts[key]} < {minimum}"
            )
    for collection in ("lakes", "mountain_zones", "ridges", "passes", "rivers", "biome_zones"):
        keys = [item["key"] for item in projection[collection]]
        if len(keys) != len(set(keys)):
            raise ValueError(f"projection repeats a {collection} key")

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
        "schema": 2,
        "projection": EXPECTED_PROJECTION,
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
