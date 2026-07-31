#!/usr/bin/env python3
"""Generate/check the M2 16-bit terrain height source and biome override mask."""

from __future__ import annotations

import argparse
import json
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
from m2_controls import land_mask

HEIGHT_OUT = TERRAIN_OUT / "heightmap.png"
BIOME_OUT = TERRAIN_OUT / "biomes.png"
PREVIEW_OUT = DERIVED / "height_preview.png"


def steepen_authored_relief(
    elevation: np.ndarray,
    lowland_reference: np.ndarray,
) -> np.ndarray:
    """Turn broad authored range envelopes into steep, readable massifs.

    The control layer already puts every range and pass in the correct place,
    but a nearly linear interpolation from plain to crest spreads that height
    over too much ground. EU5 then reads the result as low rolling ridges even
    though the peak samples are high. This curve leaves the lowland datum
    untouched, slightly compresses foothills, and increasingly lifts the
    upper shoulders and crests. It therefore strengthens physical relief
    without moving a coast, valley, river, pass, or settlement.
    """

    relief = np.maximum(elevation - lowland_reference, 0.0)
    normalized = np.sqrt(np.clip(relief / 40_000.0, 0.0, 1.0))
    factor = 0.72 + 0.72 * normalized
    return np.where(
        relief > 0.0,
        lowland_reference + relief * factor,
        elevation,
    )


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
    latitude = np.linspace(0.0, 1.0, HEIGHT_H, dtype=np.float32)[:, None]
    lowland_reference = 10_500.0 + (
        1.0 - latitude
    ) * (13_000.0 - 10_500.0)
    elevation = steepen_authored_relief(elevation, lowland_reference)
    mountain_strength = np.clip(
        (elevation - lowland_reference) / 22_000.0,
        0.0,
        1.0,
    )
    # Render the shoreline at the heightmap's native resolution. Nearest
    # enlargement of the 4096x2048 control made every source pixel a visible
    # two-pixel stair in the real renderer. The normalized authored geometry
    # remains the single source of truth.
    projection = json.loads(
        (CONTROL / "projection.json").read_text(encoding="utf-8")
    )
    water = np.asarray(
        land_mask(projection, (HEIGHT_W, HEIGHT_H)),
        dtype=np.uint8,
    ) == 0

    # Keep lowlands gently varied without injecting high-frequency entropy
    # across the whole continent. Coarse cache quantization turned the former
    # ~1,000-unit noise stack into visible topographic contour bands; broad,
    # low-amplitude undulation preserves natural ground while compressing far
    # better at full height precision.
    rng = np.random.default_rng(SEED + 41)
    noise = np.zeros((HEIGHT_H, HEIGHT_W), dtype=np.float32)
    for width, height, amplitude in (
        (96, 48, 110.0),
        (192, 96, 60.0),
        (384, 192, 28.0),
        (768, 384, 12.0),
    ):
        octave = rng.normal(0.0, 1.0, (height, width)).astype(np.float32)
        octave -= float(octave.mean())
        noise += resize_array(
            octave,
            (HEIGHT_W, HEIGHT_H),
            Image.Resampling.BICUBIC,
        ) * amplitude
    elevation += noise

    # Mountain surfaces need substantially more local relief than lowlands.
    # Modulate several tighter octaves by the authored massif envelope so
    # broad ranges retain coherent shoulders but break into slopes and peaks.
    # Do not use an absolute-value "ridged" transform here: at EU5's close
    # camera its high-amplitude zero-crossing crests read as repeated contour
    # terraces. A bounded signed multifractal instead yields asymmetric peaks,
    # gullies, and folded shoulders without moving any authored range, pass,
    # coast, river, or settlement.
    rugged = np.zeros((HEIGHT_H, HEIGHT_W), dtype=np.float32)
    for width, height, amplitude in (
        (128, 64, 1.00),
        (256, 128, 0.62),
        (512, 256, 0.32),
        (1024, 512, 0.14),
    ):
        octave = rng.normal(0.0, 1.0, (height, width)).astype(np.float32)
        octave -= float(octave.mean())
        rugged += resize_array(
            octave,
            (HEIGHT_W, HEIGHT_H),
            Image.Resampling.BICUBIC,
        ) * amplitude
    rugged_scale = max(float(rugged.std()), 1.0e-6)
    rugged_unit = rugged / rugged_scale
    folded = np.tanh(rugged_unit * 0.78)
    positive_peaks = np.power(
        np.clip((rugged_unit - 0.18) / 2.35, 0.0, 1.0),
        1.55,
    )
    # Centre the peak contribution so it changes local form, not the authored
    # theatre-scale range altitude.
    positive_peaks -= float(positive_peaks.mean())
    elevation += folded * (
        4_600.0 * np.sqrt(mountain_strength)
    )
    elevation += positive_peaks * (
        4_500.0 * np.power(mountain_strength, 0.82)
    )
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
    gradient_y, gradient_x = np.gradient(values)
    normal_x = -gradient_x / 720.0
    normal_y = -gradient_y / 720.0
    normal_z = np.ones_like(values)
    length = np.sqrt(normal_x**2 + normal_y**2 + normal_z**2)
    light = (-0.46, -0.38, 0.80)
    shade = np.clip(
        (
            normal_x * light[0]
            + normal_y * light[1]
            + normal_z * light[2]
        )
        / length,
        -0.15,
        1.0,
    )
    altitude = np.sqrt(np.clip(values / 65535.0, 0.0, 1.0))
    scaled = np.clip((0.20 + 0.66 * shade + 0.22 * altitude) * 235.0, 0, 255)
    scaled[values < 1.0] = 0.0
    return Image.fromarray(scaled.astype(np.uint8), "L")


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
    # ENDÓRË is a cropped continental theatre: Rhûn and Harad deliberately
    # continue through the east/south map borders instead of being enclosed by
    # a false ocean ring. Retain a hard 25% water floor to catch accidental
    # all-land generation while accepting the authored 29.87% western seas.
    if np.count_nonzero(expected_height == 0) < expected_height.size // 4:
        failures.append("heightmap water coverage is implausibly small")
    if int(expected_height.max()) < 45000:
        failures.append("heightmap lacks authored high mountain masses")
    dry_height = expected_height[expected_height > 0]
    if int(np.percentile(dry_height, 99.0)) < 50000:
        failures.append("heightmap upper massif shoulders are too low")
    if np.count_nonzero(dry_height >= 45000) < 250_000:
        failures.append("heightmap high-relief coverage is too sparse")
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
