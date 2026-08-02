#!/usr/bin/env python3
"""Measure installed-vanilla and ENDÓRË mountain morphology at native scale.

This is an evidence tool, not a world generator.  It compares equal-sized
heightmap windows around live-reviewed locations so renderer tuning can target
vanilla proportions without moving any Arda source geometry.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
Image.MAX_IMAGE_PIXELS = None
OUT = ROOT / "docs/world/derived/mountain_renderer_calibration.json"
VANILLA_KEYS = ("chur", "shey", "kathmandu")
ENDORE_KEYS = ("gundabad", "erebor", "dunharrow", "morannon", "mount_doom")
RADII = (48, 96, 160)


def config() -> dict[str, object]:
    return json.loads((ROOT / "config/local_paths.json").read_text(encoding="utf-8-sig"))


def run_lengths(mask: np.ndarray) -> np.ndarray:
    lengths: list[int] = []
    for line in (*mask, *mask.T):
        padded = np.pad(line.astype(np.int8), (1, 1))
        changes = np.flatnonzero(np.diff(padded))
        lengths.extend((changes[1::2] - changes[::2]).tolist())
    return np.asarray(lengths or [0], dtype=np.float32)


def sample_metrics(height: np.ndarray, x: float, y: float, radius: int) -> dict[str, object]:
    center_x = round(x * (height.shape[1] - 1))
    center_y = round(y * (height.shape[0] - 1))
    left, right = max(0, center_x - radius), min(height.shape[1], center_x + radius + 1)
    top, bottom = max(0, center_y - radius), min(height.shape[0], center_y + radius + 1)
    window = height[top:bottom, left:right].astype(np.float32)
    percentiles = np.percentile(window, (10, 25, 50, 75, 90, 95, 99))
    base = float(percentiles[0])
    peak = float(window.max())
    relief = max(1.0, peak - base)
    gy, gx = np.gradient(window)
    gradient = np.hypot(gx, gy)
    upper_half = window >= base + relief * 0.50
    upper_quarter = window >= base + relief * 0.75
    lengths_half = run_lengths(upper_half)
    lengths_quarter = run_lengths(upper_quarter)
    local_max = upper_quarter.copy()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx or dy:
                local_max &= window >= np.roll(np.roll(window, dy, axis=0), dx, axis=1)
    local_max[[0, -1], :] = False
    local_max[:, [0, -1]] = False

    def pct(values: np.ndarray, levels: tuple[int, ...]) -> list[float]:
        if not values.size:
            return [0.0 for _ in levels]
        return [round(float(value), 3) for value in np.percentile(values, levels)]

    return {
        "center_height_pixel": [center_x, center_y],
        "radius_pixels": radius,
        "height_percentiles_10_25_50_75_90_95_99": [round(float(v), 3) for v in percentiles],
        "maximum": round(peak, 3),
        "relief_above_p10": round(relief, 3),
        "upper_half_fraction": round(float(upper_half.mean()), 6),
        "upper_quarter_fraction": round(float(upper_quarter.mean()), 6),
        "gradient_percentiles_50_75_90_95": pct(gradient, (50, 75, 90, 95)),
        "upper_half_gradient_percentiles_50_75_90_95": pct(
            gradient[upper_half], (50, 75, 90, 95)
        ),
        "upper_half_run_percentiles_50_75_90_max": pct(
            lengths_half, (50, 75, 90, 100)
        ),
        "upper_quarter_run_percentiles_50_75_90_max": pct(
            lengths_quarter, (50, 75, 90, 100)
        ),
        "upper_quarter_local_maxima": int(local_max.sum()),
    }


def vanilla_centers(game_dir: Path) -> dict[str, tuple[float, float]]:
    map_dir = game_dir / "game/in_game/map_data"
    registry = (map_dir / "named_locations/00_default.txt").read_text(
        encoding="utf-8-sig"
    )
    colors: dict[str, tuple[int, int, int]] = {}
    for key in VANILLA_KEYS:
        match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*([0-9a-fA-F]{{6}})", registry)
        if not match:
            raise RuntimeError(f"installed named-location color missing for {key}")
        value = match.group(1)
        colors[key] = tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))
    locations = np.asarray(Image.open(map_dir / "locations.png").convert("RGB"))
    centers: dict[str, tuple[float, float]] = {}
    for key, color in colors.items():
        ys, xs = np.where(np.all(locations == color, axis=2))
        if not xs.size:
            raise RuntimeError(f"installed locations.png has no pixels for {key}={color}")
        centers[key] = (
            float(np.median(xs)) / (locations.shape[1] - 1),
            float(np.median(ys)) / (locations.shape[0] - 1),
        )
    return centers


def endore_centers() -> dict[str, tuple[float, float]]:
    with (ROOT / "docs/world/control/settlements.csv").open(
        encoding="utf-8-sig", newline=""
    ) as handle:
        rows = {row["key"]: row for row in csv.DictReader(handle)}
    return {key: (float(rows[key]["x"]), float(rows[key]["y"])) for key in ENDORE_KEYS}


def build() -> dict[str, object]:
    cfg = config()
    game_dir = Path(str(cfg["game_dir"]))
    vanilla_height = np.asarray(
        Image.open(game_dir / "game/in_game/gfx/terrain2/heightmap.png"), dtype=np.uint16
    )
    endore_height = np.asarray(
        Image.open(ROOT / "in_game/gfx/terrain2/heightmap.png"), dtype=np.uint16
    )
    if vanilla_height.shape != endore_height.shape:
        raise RuntimeError(
            f"heightmap shapes differ: vanilla={vanilla_height.shape} endore={endore_height.shape}"
        )
    samples: dict[str, object] = {"vanilla": {}, "endore_current": {}}
    for key, center in vanilla_centers(game_dir).items():
        samples["vanilla"][key] = {
            "normalized_center": [round(center[0], 9), round(center[1], 9)],
            "windows": [sample_metrics(vanilla_height, *center, radius) for radius in RADII],
        }
    for key, center in endore_centers().items():
        samples["endore_current"][key] = {
            "normalized_center": [round(center[0], 9), round(center[1], 9)],
            "windows": [sample_metrics(endore_height, *center, radius) for radius in RADII],
        }
    return {
        "schema": 1,
        "installed_build_id": str(cfg["game_build_id"]),
        "heightmap_shape": list(vanilla_height.shape[::-1]),
        "window_radii_pixels": list(RADII),
        "live_evidence": "docs/screens/20260801_vanilla_mountain_calibration",
        "notes": [
            "Equal native-pixel windows compare morphology, not geographic elevation.",
            "Arda Maps and Ardacraft remain authoritative for ENDÓRË horizontal geometry.",
            "The v44 isolated Erebor and Orodruin profiles are retained as accepted components.",
        ],
        "samples": samples,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = build()
    text = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(text, encoding="utf-8")
        print(f"mountain_calibration: wrote {OUT.relative_to(ROOT)}")
        return 0
    if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
        print("mountain_calibration: derived evidence is stale", flush=True)
        return 1
    print("mountain_calibration: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
