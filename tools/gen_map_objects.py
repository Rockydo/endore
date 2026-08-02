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
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))

from m2_controls import (
    draw_shape,
    land_mask,
    load_projection,
    naturalize_forest_mask,
)
from worldgen import CONTROL, CONTROL_H, CONTROL_W, ROOT, WORLD_H, WORLD_W

OUT = ROOT / "in_game/gfx/map/map_objects"
GENERATED = OUT / "generated"
RECORD = struct.Struct("<10f")
GENERATOR_VERSION = 12


@dataclass(frozen=True)
class Family:
    key: str
    biome_ids: tuple[int, ...]
    y_max: float
    meshes: tuple[str, ...]
    counts: tuple[int, int, int]
    scale: tuple[float, float]
    variant_weights: tuple[float, ...] | None = None


FAMILIES = (
    Family(
        "forest",
        (3,),
        1.0,
        (
            # Installed full-canopy, light-trunk oceanic meshes are the
            # closest retail analogue for Lothlórien's birch-dominant read.
            # Variant assignment below reserves these two for that source
            # forest; no new mesh or texture asset is invented.
            "environment_oceanic_wt_tree_01_mesh",
            "environment_oceanic_wt_tree_02_mesh",
            "vegetation_diorama_tree_single2_mesh",
            "vegetation_diorama_tree_single3_mesh",
        ),
        (300_421, 209_645, 208_750),
        (0.765, 0.935),
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
        (111_130, 78_432, 83_044),
        (0.70, 0.92),
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
        (864_055, 604_616, 597_292),
        (0.72, 0.86),
    ),
    Family(
        "generic_rock",
        (8, 9, 10),
        1.0,
        ("sm_rock_a_01_mesh",),
        (16_000, 10_000, 10_000),
        (0.58, 1.24),
    ),
)
LODS = ("high", "medium", "low")
# The release-safe 6,004-location topology leaves materially more headroom
# than the rejected 12,104-location/4.08m-object pair. Use a bounded 3.06m
# vegetation budget: high detail rises 25%, while medium/low rise 75% so named
# forests no longer collapse as the camera crosses an LOD boundary. This is
# still only 30% of the installed transform population and remains far below
# the rejected pair's object count.
EXPECTED_RECORDS = 3_093_385
REJECTED_EXPERIMENTAL_PREFIXES = ("palms_generator_", "grass_generator_")
FOREST_ZONE_MINIMUM_DETAIL = {
    # Floors are checked independently for every renderer LOD. They are
    # tightened after generation from the deterministic zone census below.
    "fangorn": {"high": 50_000, "medium": 25_000, "low": 25_000},
    "old_forest": {"high": 8_000, "medium": 8_000, "low": 8_000},
    "lothlorien": {"high": 52_000, "medium": 40_000, "low": 40_000},
    "ithilien": {"high": 700, "medium": 500, "low": 500},
    "mirkwood": {"high": 740_000, "medium": 550_000, "low": 550_000},
}
FOREST_ZONE_LOD_BOOST = {
    # Apply named-forest protection at every LOD. The former high-only field
    # made dense woods visibly evaporate at the normal regional camera.
    "fangorn": {"high": 26.0, "medium": 26.0, "low": 26.0},
    "old_forest": {"high": 16.0, "medium": 28.0, "low": 28.0},
    "lothlorien": {"high": 110.0, "medium": 140.0, "low": 140.0},
    "ithilien": {"high": 2.0, "medium": 2.0, "low": 2.0},
    "mirkwood": {"high": 5.8, "medium": 7.5, "low": 7.5},
}
TUNDRA_VEGETATION_BOUNDS = {
    # The Forodwaith is open tundra with only sparse, stunted conifer pockets.
    # The v73 live audit found ordinary forest density here because pine
    # eligibility treated biome 5 exactly like dense woodland.
    "high": (1_000, 30_000),
    "medium": (700, 24_000),
    "low": (700, 24_000),
}


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
    land = ~np.isin(biomes, (0, 4, 7))
    if family.key in {"forest", "woods", "pine"}:
        land &= ~np.isin(biomes, (8, 10))
    if family.y_max < 1.0:
        land[round(family.y_max * CONTROL_H) :, :] = False
    radius = {
        "forest": 18,
        "woods": 28,
        "pine": 22,
        "generic_rock": 14,
    }[family.key]
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
    if family.key == "generic_rock":
        # Climate scenery must never smear across a source-zone boundary.
        # Porosity comes from deterministic modulation and clearings inside
        # the exact polygon, not from broad binary terrain-material islands.
        suitability[~core] = 0.0
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
    pre_river_suitability = suitability.copy()
    major_pixels = rivers >= 192
    minor_pixels = (rivers > 0) & (rivers < 192)
    major_corridor = np.asarray(
        Image.fromarray(major_pixels.astype(np.uint8) * 255, "L").filter(
            ImageFilter.MaxFilter(15)
        ),
        dtype=np.uint8,
    ) > 0
    minor_corridor = np.asarray(
        Image.fromarray(minor_pixels.astype(np.uint8) * 255, "L").filter(
            ImageFilter.MaxFilter(5)
        ),
        dtype=np.uint8,
    ) > 0
    river_corridor = major_corridor | minor_corridor
    suitability[river_corridor] = 0.0
    # A seven-pixel blanket clearance consumed a disproportionate share of
    # narrow canonical forests. Preserve a smaller three-pixel bank corridor
    # inside the large dense woods, and only the authored channel itself in
    # Ithilien's river-following strips. The water remains continuously clear
    # while the canopy no longer vanishes from both sides of it.
    dense_named = np.zeros((CONTROL_H, CONTROL_W), dtype=bool)
    for key in ("fangorn", "old_forest", "lothlorien", "mirkwood"):
        dense_named |= named_forest_mask(key)
    narrow_major = np.asarray(
        Image.fromarray(major_pixels.astype(np.uint8) * 255, "L").filter(
            ImageFilter.MaxFilter(7)
        ),
        dtype=np.uint8,
    ) > 0
    narrow_minor = np.asarray(
        Image.fromarray(minor_pixels.astype(np.uint8) * 255, "L").filter(
            ImageFilter.MaxFilter(3)
        ),
        dtype=np.uint8,
    ) > 0
    dense_restore = dense_named & ~(narrow_major | narrow_minor)
    suitability[dense_restore] = pre_river_suitability[dense_restore]
    ithilien_restore = named_forest_mask("ithilien") & (rivers == 0)
    suitability[ithilien_restore] = pre_river_suitability[ithilien_restore]
    # The Gaussian placement field is useful for porous natural margins, but
    # it attenuates very narrow source polygons almost to zero. Guarantee a
    # continuous interior suitability floor only where the authored biome is
    # already eligible for this family. Rare deterministic glades and the
    # narrowed river corridors remain excluded.
    dense_interior = dense_named & core & (glade_values >= 14)
    dense_interior &= ~(narrow_major | narrow_minor)
    suitability[dense_interior] = np.maximum(suitability[dense_interior], 0.62)
    ithilien_interior = ithilien_restore & core & (glade_values >= 14)
    suitability[ithilien_interior] = np.maximum(
        suitability[ithilien_interior],
        0.45,
    )
    if family.key == "pine":
        # Preserve a few deterministic arctic groves without rendering the
        # entire Forodwaith as temperate woodland. Fixed global transform
        # counts redistribute the removed instances into genuinely forested
        # source zones, especially Mirkwood, rather than reducing detail.
        suitability[biomes == 5] *= 0.05
        # Lothlórien's renderer identity is a dense light-trunk deciduous wood,
        # not the generic dense-forest pine mixture used across Mirkwood. The
        # exact source boundary remains unchanged; only species eligibility is
        # specialized inside it.
        suitability[named_forest_mask("lothlorien")] = 0.0
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


@lru_cache(maxsize=None)
def named_forest_mask(key: str) -> np.ndarray:
    """Return one exact naturalized source-forest mask on physical land."""
    projection = load_projection()
    land = np.asarray(
        land_mask(projection, (CONTROL_W, CONTROL_H)),
        dtype=np.uint8,
    ) > 0
    for zone in projection["biome_zones"]:
        if str(zone["key"]) != key:
            continue
        mask = Image.new("L", (CONTROL_W, CONTROL_H), 0)
        draw_shape(
            mask,
            str(zone["shape"]),
            zone["coords"],
            (CONTROL_W, CONTROL_H),
            255,
            key=f"biome:{key}",
        )
        mask = naturalize_forest_mask(mask, key=key)
        return (np.asarray(mask, dtype=np.uint8) > 0) & land
    raise ValueError(f"missing named forest zone {key!r}")


@lru_cache(maxsize=3)
def detail_boost_field(lod: str) -> np.ndarray:
    """Return named-source-zone weights for one renderer LOD."""

    if lod not in LODS:
        raise ValueError(f"unsupported vegetation LOD {lod!r}")
    result = np.ones((CONTROL_H, CONTROL_W), dtype=np.float32)
    for key, lod_weights in FOREST_ZONE_LOD_BOOST.items():
        boost = lod_weights[lod]
        active = named_forest_mask(key)
        result[active] = np.maximum(result[active], boost)
    return result


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
    boost = detail_boost_field(lod)
    weights *= boost[cells[:, 0], cells[:, 1]]
    choices = rng.choice(len(cells), size=count, replace=True, p=weights / weights.sum())
    selected = cells[choices]
    # Random position inside its authored control cell; source Y is inverted
    # to EU5's world-space Z, matching generated locators.
    x = (selected[:, 1] + rng.random(count)) * WORLD_W / CONTROL_W
    z = WORLD_H - (selected[:, 0] + rng.random(count)) * WORLD_H / CONTROL_H
    yaw = rng.uniform(0.0, 2.0 * math.pi, count)
    scale = rng.uniform(family.scale[0], family.scale[1], count)
    if family.variant_weights is None:
        variants = rng.integers(0, len(family.meshes), count)
    else:
        weights = np.asarray(family.variant_weights, dtype=np.float64)
        if len(weights) != len(family.meshes) or np.any(weights < 0.0):
            raise ValueError(f"{family.key} has invalid mesh-variant weights")
        variants = rng.choice(
            len(family.meshes),
            size=count,
            p=weights / weights.sum(),
        )
    if family.key == "forest":
        lothlorien = named_forest_mask("lothlorien")[selected[:, 0], selected[:, 1]]
        # Reserve the two installed light-trunk full-canopy variants for
        # Lothlórien and the two retail billboard variants for other deciduous
        # forests. This makes species identity spatial rather than a global
        # random tint and preserves the four-object renderer ABI.
        variants[lothlorien] = rng.integers(0, 2, int(lothlorien.sum()))
        variants[~lothlorien] = rng.integers(2, 4, int((~lothlorien).sum()))
        scale[lothlorien] = rng.uniform(0.88, 1.08, int(lothlorien.sum()))
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


def detail_zone_counts(expected: dict[Path, bytes]) -> dict[str, dict[str, int]]:
    """Count transforms in every protected source forest at every LOD."""

    result: dict[str, dict[str, int]] = {
        key: {} for key in FOREST_ZONE_MINIMUM_DETAIL
    }
    for lod in LODS:
        points: list[np.ndarray] = []
        for path, data in expected.items():
            if path.suffix != ".bin" or f"_{lod}_" not in path.name:
                continue
            records = np.frombuffer(data, dtype="<f4").reshape(-1, 10)
            points.append(records[:, (0, 2)])
        if not points:
            continue
        world_points = np.concatenate(points)
        control_x = np.clip(
            (world_points[:, 0] / WORLD_W * CONTROL_W).astype(np.int32),
            0,
            CONTROL_W - 1,
        )
        control_y = np.clip(
            ((WORLD_H - world_points[:, 1]) / WORLD_H * CONTROL_H).astype(np.int32),
            0,
            CONTROL_H - 1,
        )
        for key in FOREST_ZONE_MINIMUM_DETAIL:
            active = named_forest_mask(key)
            result[key][lod] = int(active[control_y, control_x].sum())
    return result


def count_records_in_mask(data: bytes, mask: np.ndarray) -> int:
    """Count one transform payload inside a control-resolution mask."""

    records = np.frombuffer(data, dtype="<f4").reshape(-1, 10)
    control_x = np.clip(
        (records[:, 0] / WORLD_W * CONTROL_W).astype(np.int32),
        0,
        CONTROL_W - 1,
    )
    control_y = np.clip(
        ((WORLD_H - records[:, 2]) / WORLD_H * CONTROL_H).astype(np.int32),
        0,
        CONTROL_H - 1,
    )
    return int(mask[control_y, control_x].sum())


def family_lod_records(
    expected: dict[Path, bytes],
    family: Family,
    lod: str,
) -> np.ndarray:
    """Return every transform for one exact retail family/LOD definition."""

    arrays = [
        np.frombuffer(
            expected[OUT / f"{family.key}_generator_{lod}_{variant}.bin"],
            dtype="<f4",
        ).reshape(-1, 10)
        for variant in range(len(family.meshes))
    ]
    return np.concatenate(arrays) if arrays else np.empty((0, 10), dtype="<f4")


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
    for prefix in REJECTED_EXPERIMENTAL_PREFIXES:
        for path in OUT.glob(f"{prefix}*.bin"):
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
    stale.extend(
        path.name
        for prefix in REJECTED_EXPERIMENTAL_PREFIXES
        for path in OUT.glob(f"{prefix}*.bin")
        if path.name not in expected_names
    )
    if stale:
        failures.append(f"stale ENDÓRË vegetation outputs: {', '.join(sorted(stale))}")
    definition_count = sum(path.suffix == ".txt" for path in expected)
    bin_count = sum(path.suffix == ".bin" for path in expected)
    if definition_count != 12 or bin_count != 39:
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
    biomes, _, rivers = controls()
    for family in FAMILIES:
        for lod_index, lod in enumerate(LODS):
            rows = family_lod_records(expected, family, lod)
            if len(rows) != family.counts[lod_index]:
                failures.append(
                    f"{family.key} {lod} count differs from its authored budget"
                )
                continue
            control_x = np.clip(
                (rows[:, 0] / WORLD_W * CONTROL_W).astype(np.int32),
                0,
                CONTROL_W - 1,
            )
            control_y = np.clip(
                ((WORLD_H - rows[:, 2]) / WORLD_H * CONTROL_H).astype(np.int32),
                0,
                CONTROL_H - 1,
            )
            sampled_biomes = biomes[control_y, control_x]
            if family.key == "generic_rock" and np.any(
                ~np.isin(sampled_biomes, family.biome_ids)
            ):
                failures.append(
                    f"{family.key} {lod} scenery escaped its source climate"
                )
            if family.key == "generic_rock":
                for biome_id in family.biome_ids:
                    fraction = float((sampled_biomes == biome_id).mean())
                    if fraction < 0.05:
                        failures.append(
                            f"generic_rock {lod} lost biome {biome_id} coverage"
                        )
    zone_counts = detail_zone_counts(expected)
    for key, lod_minimums in FOREST_ZONE_MINIMUM_DETAIL.items():
        for lod, minimum in lod_minimums.items():
            count = zone_counts.get(key, {}).get(lod, 0)
            if count < minimum:
                failures.append(
                    f"{key} {lod}-detail vegetation regressed "
                    f"({count:,} < {minimum:,})"
                )
    lothlorien = named_forest_mask("lothlorien")
    for lod in LODS:
        light_trunk = sum(
            count_records_in_mask(
                expected[OUT / f"forest_generator_{lod}_{variant}.bin"],
                lothlorien,
            )
            for variant in (0, 1)
        )
        generic = sum(
            count_records_in_mask(
                expected[OUT / f"forest_generator_{lod}_{variant}.bin"],
                lothlorien,
            )
            for variant in (2, 3)
        )
        pine = sum(
            count_records_in_mask(
                expected[OUT / f"pine_generator_{lod}_{variant}.bin"],
                lothlorien,
            )
            for variant in range(4)
        )
        lothlorien_total = zone_counts["lothlorien"][lod]
        if light_trunk != lothlorien_total or generic or pine:
            failures.append(
                f"lothlorien {lod} species contract regressed "
                f"(light={light_trunk:,}, generic={generic:,}, pine={pine:,}, "
                f"total={lothlorien_total:,})"
            )
    tundra = biomes == 5
    for lod, (minimum, maximum) in TUNDRA_VEGETATION_BOUNDS.items():
        tundra_count = sum(
            count_records_in_mask(data, tundra)
            for path, data in expected.items()
            if path.suffix == ".bin" and f"_{lod}_" in path.name
        )
        if not minimum <= tundra_count <= maximum:
            failures.append(
                f"{lod}-detail tundra vegetation left sparse-arctic bounds "
                f"({tundra_count:,}, expected {minimum:,}..{maximum:,})"
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
