#!/usr/bin/env python3
"""Generate/check Arda-native close-zoom vegetation transforms.

EU5 generated map-object bins are headerless arrays of ten little-endian
floats: position xyz, quaternion xyzw, and scale xyz. The installed meshes and
LOD layer names are reused exactly; every placement is generated only from
ENDÓRË's authored biome controls.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import struct
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worldgen import CONTROL, CONTROL_H, CONTROL_W, ROOT, WORLD_H, WORLD_W

OUT = ROOT / "in_game/gfx/map/map_objects"
GENERATED = OUT / "generated"
RECORD = struct.Struct("<10f")
GENERATOR_VERSION = 6


@dataclass(frozen=True)
class Family:
    key: str
    biome_ids: tuple[int, ...]
    y_max: float
    meshes: tuple[str, ...]
    counts: tuple[int, int, int]
    scale: tuple[float, float]


FAMILIES = (
    Family(
        "forest",
        (3,),
        1.0,
        (
            "vegetation_diorama_tree_single_mesh",
            "vegetation_diorama_tree_single1_mesh",
            "vegetation_diorama_tree_single2_mesh",
            "vegetation_diorama_tree_single3_mesh",
        ),
        (1_201_686, 598_983, 596_430),
        (0.72, 0.92),
    ),
    Family(
        "woods",
        (2, 6),
        1.0,
        (
            "vegetation_diorama_tree_single_mesh",
            "vegetation_diorama_tree_single1_mesh",
            "vegetation_diorama_tree_single2_mesh",
            "vegetation_diorama_tree_single3_mesh",
        ),
        (444_518, 224_087, 237_269),
        (0.68, 0.88),
    ),
    Family(
        "pine",
        (2, 3, 5),
        0.36,
        (
            "vegetation_diorama_arctic_tree_mesh",
            "vegetation_diorama_arctic_tree2_mesh",
            "vegetation_diorama_arctic_tree3_mesh",
            "vegetation_diorama_arctic_tree4_mesh",
        ),
        (3_456_217, 1_727_474, 1_706_548),
        (0.70, 0.86),
    ),
)
LODS = ("high", "medium", "low")
EXPECTED_RECORDS = 10_193_212


def seed(*parts: str) -> int:
    payload = "|".join(("ENDORE", str(GENERATOR_VERSION), *parts, "3018"))
    return int.from_bytes(hashlib.sha256(payload.encode("utf-8")).digest()[:8], "little")


def controls() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    with Image.open(CONTROL / "biomes.png") as image:
        biomes = np.asarray(image, dtype=np.uint8)
    with Image.open(CONTROL / "density.png") as image:
        density = np.asarray(image, dtype=np.uint8)
    with Image.open(CONTROL / "rivers.png") as image:
        rivers = np.asarray(image, dtype=np.uint8)
    if biomes.shape != (CONTROL_H, CONTROL_W):
        raise ValueError("vegetation source has the wrong control resolution")
    return biomes, density, rivers


def placement_field(
    family: Family,
    biomes: np.ndarray,
    rivers: np.ndarray,
) -> np.ndarray:
    """Return continuous placement suitability with a feathered forest edge."""

    core = np.isin(biomes, family.biome_ids)
    land = ~np.isin(biomes, (0, 4, 7, 8, 10))
    if family.y_max < 1.0:
        land[round(family.y_max * CONTROL_H) :, :] = False
    radius = {"forest": 18, "woods": 28, "pine": 22}[family.key]
    blurred = np.asarray(
        Image.fromarray(core.astype(np.uint8) * 255, "L").filter(
            ImageFilter.GaussianBlur(radius=radius)
        ),
        dtype=np.float64,
    ) / 255.0
    rng = np.random.default_rng(seed(family.key, "placement-field"))
    noise = Image.fromarray(
        rng.integers(0, 256, (256, 512), dtype=np.uint8),
        "L",
    ).resize((CONTROL_W, CONTROL_H), Image.Resampling.BICUBIC)
    modulation = 0.70 + np.asarray(noise, dtype=np.float64) / 255.0 * 0.60
    suitability = np.power(blurred, 1.18) * modulation
    # Rare broad low-density clearings belong to placement, not the discrete
    # gameplay biome. Cutting holes in the biome made whole Voronoi locations
    # flip to grass and exposed polygon-shaped glades in the renderer.
    glades = Image.fromarray(
        rng.integers(0, 256, (96, 192), dtype=np.uint8),
        "L",
    ).resize((CONTROL_W, CONTROL_H), Image.Resampling.BICUBIC)
    glade_values = np.asarray(glades, dtype=np.uint8)
    suitability[glade_values < 14] *= 0.08
    # Preserve readable water and banks through dense woodland. Rivers are
    # already organic authored controls; this merely prevents millions of
    # valid tree instances from obscuring their terrain material at close zoom.
    river_corridor = np.asarray(
        Image.fromarray((rivers > 0).astype(np.uint8) * 255, "L").filter(
            ImageFilter.MaxFilter(15)
        ),
        dtype=np.uint8,
    ) > 0
    suitability[river_corridor] = 0.0
    suitability[~land] = 0.0
    suitability[suitability < 0.025] = 0.0
    return suitability


def eligible_cells(
    family: Family,
    biomes: np.ndarray,
    rivers: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    suitability = placement_field(family, biomes, rivers)
    cells = np.argwhere(suitability > 0.0)
    if not len(cells):
        raise ValueError(f"{family.key} has no eligible authored cells")
    return cells, suitability


def hilbert_order(x: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Return a locality-preserving order for 2D generated instances.

    EU5's retail transform bins are not arbitrary bags of instances.  Adjacent
    records remain spatially local (the installed forest bins have a median
    consecutive distance of roughly 27 world units), which allows the map
    object renderer to batch and cull generated content by contiguous ranges.
    A random serialization made every small ENDÓRË range span most of Arda.

    Quantize the full engine canvas to a 16-bit Hilbert lattice and serialize
    each mesh variant along that curve.  Positions remain authored and random;
    only their on-disk order changes.
    """

    qx = np.clip(x / WORLD_W * 65_535.0, 0, 65_535).astype(np.int64)
    qz = np.clip(z / WORLD_H * 65_535.0, 0, 65_535).astype(np.int64)
    hx = qx.copy()
    hz = qz.copy()
    distance = np.zeros(len(qx), dtype=np.int64)
    scale = 1 << 15
    while scale:
        rx = (hx & scale) != 0
        rz = (hz & scale) != 0
        distance += scale * scale * ((3 * rx.astype(np.int64)) ^ rz.astype(np.int64))
        rotate = ~rz
        invert = rotate & rx
        hx[invert] = scale - 1 - hx[invert]
        hz[invert] = scale - 1 - hz[invert]
        swap = hx[rotate].copy()
        hx[rotate] = hz[rotate]
        hz[rotate] = swap
        scale >>= 1
    return np.argsort(distance, kind="stable")


def transforms(
    family: Family,
    lod: str,
    count: int,
    biomes: np.ndarray,
    density: np.ndarray,
    rivers: np.ndarray,
) -> tuple[bytes, ...]:
    rng = np.random.default_rng(seed(family.key, lod))
    cells, suitability = eligible_cells(family, biomes, rivers)
    weights = suitability[cells[:, 0], cells[:, 1]]
    weights *= np.clip(
        density[cells[:, 0], cells[:, 1]].astype(np.float64) / 255.0,
        0.35,
        1.0,
    )
    choices = rng.choice(len(cells), size=count, replace=True, p=weights / weights.sum())
    selected = cells[choices]
    # Random position inside its authored control cell; source Y is inverted
    # to EU5's world-space Z, matching generated locators.
    x = (selected[:, 1] + rng.random(count)) * WORLD_W / CONTROL_W
    z = WORLD_H - (selected[:, 0] + rng.random(count)) * WORLD_H / CONTROL_H
    yaw = rng.uniform(0.0, 2.0 * math.pi, count)
    scale = rng.uniform(family.scale[0], family.scale[1], count)
    variants = rng.integers(0, len(family.meshes), count)
    half = yaw * 0.5
    records = np.zeros((count, 10), dtype="<f4")
    records[:, 0] = x
    records[:, 2] = z
    records[:, 4] = np.sin(half)
    records[:, 6] = np.cos(half)
    records[:, 7] = scale
    records[:, 8] = scale
    records[:, 9] = scale
    payloads: list[bytes] = []
    for variant in range(len(family.meshes)):
        selected_records = records[variants == variant]
        order = hilbert_order(selected_records[:, 0], selected_records[:, 2])
        payloads.append(selected_records[order].tobytes(order="C"))
    return tuple(payloads)


def locality_metrics(data: bytes) -> tuple[float, float]:
    """Return consecutive and 32-record spatial locality in world units."""

    records = np.frombuffer(data, dtype="<f4").reshape(-1, 10)
    if len(records) < 2:
        return 0.0, 0.0
    points = records[:, (0, 2)]
    consecutive = np.linalg.norm(np.diff(points, axis=0), axis=1)
    chunk = min(32, len(points))
    complete = len(points) // chunk
    groups = points[: complete * chunk].reshape(complete, chunk, 2)
    spans = np.linalg.norm(groups.max(axis=1) - groups.min(axis=1), axis=1)
    return float(np.median(consecutive)), float(np.median(spans))


def definition_text(family: Family, lod: str) -> str:
    lines = [
        "# Generated by tools/gen_map_objects.py --write.",
        "# Vanilla EU5 meshes and LOD layers; ENDÓRË-authored transforms only.",
    ]
    for index, mesh in enumerate(family.meshes):
        # The renderer keys these generated layers by the installed object
        # name as well as by their exact definition filename. Keep the object
        # ABI exact while redirecting only its transform payload to Arda.
        object_name = f"{family.key}_generator_{lod}_{index}"
        transform_name = object_name
        lines.extend(
            (
                "object={",
                f'\tname="{object_name}"',
                "\tclamp_to_water_level=no",
                "\trender_under_water=no",
                "\tgenerated_content=yes",
                f'\tlayer="vegetation_{lod}"',
                f'\tpdxmesh="{mesh}"',
                f'\ttransform_bin_file="gfx/map/map_objects/{transform_name}.bin"',
                "}",
            )
        )
    return "\n".join(lines) + "\n"


def payloads() -> dict[Path, bytes]:
    biomes, density, rivers = controls()
    result: dict[Path, bytes] = {}
    for family in FAMILIES:
        for lod_index, lod in enumerate(LODS):
            # EU5's renderer discovers these generated layers by the exact
            # retail definition filename. Arbitrary sibling definitions parse
            # without an error but are not activated by the map-object system.
            result[GENERATED / f"{family.key}_generator_{lod}.txt"] = (
                definition_text(family, lod).encode("utf-8")
            )
            bins = transforms(
                family,
                lod,
                family.counts[lod_index],
                biomes,
                density,
                rivers,
            )
            for index, data in enumerate(bins):
                result[
                    OUT / f"{family.key}_generator_{lod}_{index}.bin"
                ] = data
    return result


def write() -> None:
    expected = payloads()
    for path, data in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    expected_names = {path.name for path in expected}
    for directory, pattern in (
        (GENERATED, "endore_*.txt"),
        (OUT, "endore_*.bin"),
    ):
        for path in directory.glob(pattern):
            if path.name not in expected_names:
                path.unlink()
    records = sum(
        len(data) // RECORD.size
        for path, data in expected.items()
        if path.suffix == ".bin"
    )
    total_bytes = sum(len(data) for data in expected.values())
    print(
        "gen_map_objects: wrote "
        f"{records:,} Arda-native vegetation transforms "
        f"({total_bytes / 1_000_000:.1f} MB)"
    )


def check() -> list[str]:
    failures: list[str] = []
    expected = payloads()
    for path, data in expected.items():
        if not path.is_file():
            failures.append(f"missing {path.relative_to(ROOT)}")
        elif path.read_bytes() != data:
            failures.append(f"{path.name} differs from authored vegetation model")
    expected_names = {path.name for path in expected}
    stale = [
        path.name
        for directory in (OUT, GENERATED)
        for path in directory.glob("endore_*")
        if path.name not in expected_names
    ]
    if stale:
        failures.append(f"stale ENDÓRË vegetation outputs: {', '.join(sorted(stale))}")
    definition_count = sum(path.suffix == ".txt" for path in expected)
    bin_count = sum(path.suffix == ".bin" for path in expected)
    if definition_count != 9 or bin_count != 36:
        failures.append("vegetation output family/LOD contract is incomplete")
    records = sum(
        len(data) // RECORD.size
        for path, data in expected.items()
        if path.suffix == ".bin"
    )
    if records != EXPECTED_RECORDS:
        failures.append(
            f"vegetation density regressed ({records:,} != {EXPECTED_RECORDS:,})"
        )
    for path, data in expected.items():
        if path.suffix != ".bin":
            continue
        median_step, median_chunk_span = locality_metrics(data)
        if median_step > 250 or median_chunk_span > 800:
            failures.append(
                f"{path.name} is not spatially serialized "
                f"(median step {median_step:.1f}, 32-record span "
                f"{median_chunk_span:.1f})"
            )
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
            print(f"gen_map_objects: FAIL {failure}")
        return 1
    print("gen_map_objects: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
