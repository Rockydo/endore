#!/usr/bin/env python3
"""Generate/check the M2 16-bit terrain height source and biome override mask."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worldgen import (
    BIOME_H,
    BIOME_W,
    CONTROL,
    DERIVED,
    HEIGHT_H,
    HEIGHT_W,
    SEED,
    TERRAIN_OUT,
)

HEIGHT_OUT = TERRAIN_OUT / "heightmap.png"
BIOME_OUT = TERRAIN_OUT / "biomes.png"
PREVIEW_OUT = DERIVED / "height_preview.png"


def resize_array(
    array: np.ndarray,
    size: tuple[int, int],
    resampling: Image.Resampling,
) -> np.ndarray:
    mode = "F" if np.issubdtype(array.dtype, np.floating) else None
    image = Image.fromarray(array, mode) if mode else Image.fromarray(array)
    return np.asarray(image.resize(size, resampling), dtype=np.float32)


def render_height() -> np.ndarray:
    with Image.open(CONTROL / "elevation.png") as source:
        control_elevation = np.asarray(source, dtype=np.float32)
    with Image.open(CONTROL / "biomes.png") as source:
        control_biomes = np.asarray(source, dtype=np.uint8)

    elevation = resize_array(
        control_elevation,
        (HEIGHT_W, HEIGHT_H),
        Image.Resampling.BICUBIC,
    ).copy()
    water = np.isin(
        resize_array(
            control_biomes,
            (HEIGHT_W, HEIGHT_H),
            Image.Resampling.NEAREST,
        ).astype(np.uint8),
        (0, 7),
    )

    # Deterministic fractal detail keeps the authored ridges dominant while
    # preventing the terrain surface from reading as a blurred control raster.
    rng = np.random.default_rng(SEED + 41)
    noise = np.zeros((HEIGHT_H, HEIGHT_W), dtype=np.float32)
    for width, height, amplitude in (
        (128, 64, 1250.0),
        (256, 128, 700.0),
        (512, 256, 360.0),
        (1024, 512, 170.0),
    ):
        octave = rng.normal(0.0, 1.0, (height, width)).astype(np.float32)
        octave -= float(octave.mean())
        noise += resize_array(
            octave,
            (HEIGHT_W, HEIGHT_H),
            Image.Resampling.BICUBIC,
        ) * amplitude
    elevation += noise
    elevation[water] = 0.0
    return np.clip(elevation, 0, 65535).astype(np.uint16)


def render_biome_override() -> np.ndarray:
    # Installed evidence shows this is a sparse manual material-override mask,
    # not the gameplay biome map: vanilla uses only 0, 1 and 127 and is >99%
    # zero. ENDÓRË drives terrain through location templates, so zero means no
    # stale Earth override anywhere.
    return np.zeros((BIOME_H, BIOME_W), dtype=np.uint8)


def preview(height: np.ndarray) -> Image.Image:
    reduced = Image.fromarray(height).resize((1024, 512), Image.Resampling.BILINEAR)
    values = np.asarray(reduced, dtype=np.float32)
    scaled = np.clip(np.sqrt(values / 65535.0) * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(scaled, "L")


def write() -> None:
    height = render_height()
    biome = render_biome_override()
    TERRAIN_OUT.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)
    Image.fromarray(height).save(HEIGHT_OUT, compress_level=9)
    Image.fromarray(biome, "L").save(BIOME_OUT, compress_level=9)
    preview(height).save(PREVIEW_OUT, compress_level=9)
    print(
        f"gen_heightmap: wrote {HEIGHT_W}x{HEIGHT_H} uint16 terrain "
        f"({int(height.min())}..{int(height.max())})"
    )


def check() -> list[str]:
    failures: list[str] = []
    expected_height = render_height()
    expected_biome = render_biome_override()
    expected_preview = preview(expected_height)
    expected = (
        (HEIGHT_OUT, "I;16", (HEIGHT_W, HEIGHT_H), expected_height),
        (BIOME_OUT, "L", (BIOME_W, BIOME_H), expected_biome),
        (
            PREVIEW_OUT,
            "L",
            expected_preview.size,
            np.asarray(expected_preview),
        ),
    )
    for path, mode, size, pixels in expected:
        if not path.is_file():
            failures.append(f"missing {path.relative_to(TERRAIN_OUT.parent.parent.parent)}")
            continue
        with Image.open(path) as image:
            normalized_mode = "I;16" if image.mode.startswith("I;16") else image.mode
            if normalized_mode != mode or image.size != size:
                failures.append(
                    f"{path.name} is {image.mode} {image.size}, expected {mode} {size}"
                )
            elif not np.array_equal(np.asarray(image), pixels):
                failures.append(f"{path.name} differs from deterministic terrain model")
    if np.count_nonzero(expected_height == 0) < expected_height.size // 3:
        failures.append("heightmap water coverage is implausibly small")
    if int(expected_height.max()) < 45000:
        failures.append("heightmap lacks authored high mountain masses")
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
            print(f"gen_heightmap: FAIL {failure}")
        return 1
    print("gen_heightmap: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
