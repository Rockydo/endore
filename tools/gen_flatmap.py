#!/usr/bin/env python3
"""Generate/check the M2 paper-map backup from terrain and an exact vanilla reference."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worldgen import CONTROL, DERIVED, ROOT, save_json

OUT_DIR = ROOT / "in_game/gfx/map/flatmap"
OUT = OUT_DIR / "flatmap_staticbackup.dds"
PREVIEW_OUT = DERIVED / "flatmap_preview.png"
MANIFEST_OUT = DERIVED / "flatmap_manifest.json"
WIDTH, HEIGHT = 8192, 4096

BASE_COLORS = {
    0: (55, 81, 96),
    1: (139, 143, 102),
    2: (91, 112, 77),
    3: (65, 91, 62),
    4: (133, 126, 112),
    5: (169, 168, 148),
    6: (91, 112, 88),
    7: (58, 91, 108),
    8: (87, 72, 63),
    9: (148, 135, 88),
    10: (176, 145, 96),
}


def vanilla_reference() -> Path:
    config = json.loads((ROOT / "config/local_paths.json").read_text(encoding="utf-8-sig"))
    return (
        Path(config["game_dir"])
        / "game/in_game/gfx/map/flatmap/flatmap_staticbackup.dds"
    )


def reference_data() -> tuple[float, str]:
    path = vanilla_reference()
    with Image.open(path) as image:
        sample = np.asarray(
            image.convert("RGB").resize((128, 64), Image.Resampling.BOX),
            dtype=np.float32,
        )
    luminance = float(
        (
            sample[..., 0] * 0.2126
            + sample[..., 1] * 0.7152
            + sample[..., 2] * 0.0722
        ).mean()
    )
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return luminance, digest.hexdigest()


def render() -> Image.Image:
    with Image.open(CONTROL / "biomes.png") as image:
        biome = np.asarray(
            image.resize((WIDTH, HEIGHT), Image.Resampling.NEAREST),
            dtype=np.uint8,
        )
    with Image.open(CONTROL / "elevation.png") as image:
        height = np.asarray(
            image.resize((WIDTH, HEIGHT), Image.Resampling.BICUBIC),
            dtype=np.float32,
        )

    rgb = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    for biome_id, color in BASE_COLORS.items():
        rgb[biome == biome_id] = color

    # Compact Lambert-like hillshade from the authored height field.
    dy, dx = np.gradient(height / 65535.0)
    shade = np.clip(1.04 - dx * 5.0 - dy * 3.0, 0.72, 1.25)
    shade[biome == 0] = 1.0
    rgb *= shade[..., None]

    rng = np.random.default_rng(3018 + 73)
    grain_small = rng.normal(0.0, 1.0, (256, 512)).astype(np.float32)
    grain = np.asarray(
        Image.fromarray(grain_small, "F").resize(
            (WIDTH, HEIGHT),
            Image.Resampling.BICUBIC,
        ),
        dtype=np.float32,
    )
    rgb += grain[..., None] * 2.4

    # Tie overall luminance to the exact installed EU5 paper-map asset.
    reference_luminance, _ = reference_data()
    current_luminance = float(
        (
            rgb[..., 0] * 0.2126
            + rgb[..., 1] * 0.7152
            + rgb[..., 2] * 0.0722
        ).mean()
    )
    rgb *= np.clip(reference_luminance / current_luminance, 0.82, 1.18)
    alpha = np.full((HEIGHT, WIDTH, 1), 255, dtype=np.uint8)
    return Image.fromarray(
        np.concatenate((np.clip(rgb, 0, 255).astype(np.uint8), alpha), axis=2),
        "RGBA",
    )


def manifest() -> dict:
    luminance, reference_sha = reference_data()
    return {
        "schema": 1,
        "resolution": [WIDTH, HEIGHT],
        "format": "DDS DXT5",
        "vanilla_reference": "in_game/gfx/map/flatmap/flatmap_staticbackup.dds",
        "vanilla_reference_sha256": reference_sha,
        "vanilla_reference_mean_luminance": round(luminance, 6),
    }


def write() -> None:
    image = render()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)
    image.save(OUT, pixel_format="DXT5")
    image.resize((1024, 512), Image.Resampling.LANCZOS).convert("RGB").save(
        PREVIEW_OUT,
        compress_level=9,
    )
    save_json(MANIFEST_OUT, manifest())
    print(f"gen_flatmap: wrote {WIDTH}x{HEIGHT} DXT5 map calibrated to vanilla asset")


def check() -> list[str]:
    failures: list[str] = []
    expected = render()
    expected_preview = expected.resize(
        (1024, 512),
        Image.Resampling.LANCZOS,
    ).convert("RGB")
    expected_manifest = manifest()
    if not OUT.is_file():
        failures.append("missing in_game/gfx/map/flatmap/flatmap_staticbackup.dds")
    else:
        with Image.open(OUT) as actual:
            if actual.mode != "RGBA" or actual.size != (WIDTH, HEIGHT):
                failures.append(
                    f"flatmap_staticbackup.dds is {actual.mode} {actual.size}, "
                    f"expected RGBA {(WIDTH, HEIGHT)}"
                )
        if OUT.stat().st_size > WIDTH * HEIGHT * 2:
            failures.append("flatmap_staticbackup.dds is not block-compressed")
    if not PREVIEW_OUT.is_file():
        failures.append("missing docs/world/derived/flatmap_preview.png")
    else:
        with Image.open(PREVIEW_OUT) as actual_preview:
            if not np.array_equal(
                np.asarray(actual_preview),
                np.asarray(expected_preview),
            ):
                failures.append("flatmap_preview.png differs from deterministic render")
    if not MANIFEST_OUT.is_file():
        failures.append("missing docs/world/derived/flatmap_manifest.json")
    elif json.loads(MANIFEST_OUT.read_text(encoding="utf-8")) != expected_manifest:
        failures.append("flatmap_manifest.json differs from installed reference")
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
            print(f"gen_flatmap: FAIL {failure}")
        return 1
    print("gen_flatmap: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
