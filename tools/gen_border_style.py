#!/usr/bin/env python3
"""Generate/check a restrained location-border texture from installed EU5."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dds import convert, identify

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/local_paths.json"
OUT = ROOT / "in_game/gfx/map/borders/border_location.dds"
WORK = ROOT / ".tmp/endore_border_location.png"
ALPHA_SCALE = 0.18


def installed_source() -> Path:
    config = json.loads(CONFIG.read_text(encoding="utf-8-sig"))
    return (
        Path(str(config["game_dir"]))
        / "game/in_game/gfx/map/borders/border_location.dds"
    )


def styled_rgba() -> np.ndarray:
    source = installed_source()
    if not source.is_file():
        raise FileNotFoundError(f"missing installed EU5 location border: {source}")
    with Image.open(source) as image:
        rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8).copy()
    if rgba.shape != (32, 64, 4):
        raise ValueError(f"installed location border has unexpected shape {rgba.shape}")
    # Retain the exact installed stroke, antialiasing, cadence, and format.
    # ENDÓRË only reduces its alpha because 12,104 compact locations make the
    # vanilla-strength stroke overwhelm physical relief at close zoom.
    rgba[:, :, 3] = np.rint(
        rgba[:, :, 3].astype(np.float64) * ALPHA_SCALE
    ).astype(np.uint8)
    return rgba


def write() -> None:
    rgba = styled_rgba()
    WORK.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(WORK, compress_level=9)
    convert(WORK, OUT, "dxt5", mipmaps=True)
    print(
        "gen_border_style: wrote installed-style 64x32 DXT5 location border "
        f"at {ALPHA_SCALE:.0%} alpha"
    )


def check() -> list[str]:
    failures: list[str] = []
    if not OUT.is_file():
        return ["missing in_game/gfx/map/borders/border_location.dds"]
    details = identify(OUT)
    if (
        details["format"] != "DDS"
        or details["width"] != "64"
        or details["height"] != "32"
        or "a" not in details["channels"].casefold()
    ):
        failures.append(f"location border has unexpected DDS contract: {details}")
        return failures
    expected = styled_rgba()
    with Image.open(OUT) as image:
        actual = np.asarray(image.convert("RGBA"), dtype=np.uint8)
    if actual.shape != expected.shape:
        failures.append("location border decoded dimensions differ from installed source")
        return failures
    alpha = actual[:, :, 3]
    if int(alpha.max()) > 64 or float(alpha.mean()) > 8.0:
        failures.append(
            "location border alpha is too strong for the physical-map contract "
            f"(max={int(alpha.max())}, mean={float(alpha.mean()):.3f})"
        )
    if int(alpha.max()) < 24 or float(alpha.mean()) < 1.0:
        failures.append(
            "location border became unreadably faint "
            f"(max={int(alpha.max())}, mean={float(alpha.mean()):.3f})"
        )
    if np.any(actual[:, :, :3] != 0):
        failures.append("location border no longer preserves the installed black stroke")
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
            print(f"gen_border_style: FAIL {failure}")
        return 1
    print("gen_border_style: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
