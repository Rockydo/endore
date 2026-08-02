#!/usr/bin/env python3
"""Generate/check the M2 16-bit terrain height source and biome override mask."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

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
from m2_controls import (
    land_mask,
    load_settlements,
    natural_path,
    soft_ceiling,
    source_relief_field,
    stable_seed,
)

HEIGHT_OUT = TERRAIN_OUT / "heightmap.png"
BIOME_OUT = TERRAIN_OUT / "biomes.png"
PREVIEW_OUT = DERIVED / "height_preview.png"


def steepen_authored_relief(
    elevation: np.ndarray,
    lowland_reference: np.ndarray,
) -> np.ndarray:
    """Translate authored source relief without manufacturing cliff shelves.

    The control layer already puts every range and pass in the correct place,
    but a nearly linear interpolation from plain to crest spreads that height
    over too much ground. EU5 then reads the result as low rolling ridges even
    though the peak samples are high. This curve leaves the lowland datum
    untouched, slightly compresses foothills, and increasingly lifts the
    upper shoulders and crests. It therefore strengthens physical relief
    without moving a coast, valley, river, pass, or settlement.
    """

    relief = np.maximum(elevation - lowland_reference, 0.0)
    # The authored control can legitimately reach 40,800 units above its
    # latitude datum. Normalizing at 36,000 clipped the upper source levels to
    # one value before the soft ceiling and manufactured flat summit shelves.
    normalized = np.clip(relief / 40_800.0, 0.0, 1.0)
    # v39 applied a second strongly convex transform after an already-convex
    # control response. It produced gradients roughly ten times vanilla's and
    # reduced continuous source bands to sheer shelves. One gentle response
    # retains the native eight-bit shoulders and arêtes while keeping the
    # major crests substantially above the surrounding lowlands.
    sharpened = (
        3_000.0 * normalized
        + 52_000.0 * np.power(normalized, 2.00)
    )
    return np.where(
        relief > 0.0,
        lowland_reference + sharpened,
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


def serrate_mordor_walls(elevation: np.ndarray, projection: dict) -> None:
    """Give Mordor's exact two wall axes an irregular coarse-scale skyline.

    The native terrain cache supplies face detail, but live v63 evidence proves
    that EU5 takes the long-distance silhouette from this 8192x4096 source.
    Vary height only along the projection's source-pinned Ered Lithui and Ephel
    Duath centerlines, while guarding the direct Morannon pass marker.
    """

    ridge_by_key = {ridge["key"]: ridge for ridge in projection["ridges"]}
    phases = (("ephel_duath", 0.37), ("ered_lithui", 1.81))
    margin = 28
    left = max(0, round(0.590 * (HEIGHT_W - 1)) - margin)
    right = min(HEIGHT_W, round(0.748 * (HEIGHT_W - 1)) + margin + 1)
    top = max(0, round(0.500 * (HEIGHT_H - 1)) - margin)
    bottom = min(HEIGHT_H, round(0.710 * (HEIGHT_H - 1)) + margin + 1)
    local = elevation[top:bottom, left:right]
    grid_y, grid_x = np.ogrid[top:bottom, left:right]
    wall_addition = np.zeros(local.shape, dtype=np.float32)
    wall_trough = np.zeros(local.shape, dtype=np.float32)

    for key, phase in phases:
        ridge = ridge_by_key.get(key)
        if ridge is None:
            raise ValueError(f"projection lacks source-pinned Mordor wall {key}")
        points = np.asarray(
            [
                (float(x) * (HEIGHT_W - 1), float(y) * (HEIGHT_H - 1))
                for x, y in ridge["points"]
            ],
            dtype=np.float32,
        )
        vectors = points[1:] - points[:-1]
        lengths = np.hypot(vectors[:, 0], vectors[:, 1])
        cumulative = np.concatenate(
            (np.zeros(1, dtype=np.float32), np.cumsum(lengths)[:-1])
        )
        closest_distance_sq = np.full(local.shape, np.inf, dtype=np.float32)
        closest_arc = np.zeros(local.shape, dtype=np.float32)
        for start, vector, length, arc_start in zip(
            points[:-1], vectors, lengths, cumulative, strict=True
        ):
            length_sq = max(float(length * length), 1.0)
            relative_x = grid_x - float(start[0])
            relative_y = grid_y - float(start[1])
            along = np.clip(
                (relative_x * float(vector[0]) + relative_y * float(vector[1]))
                / length_sq,
                0.0,
                1.0,
            )
            nearest_x = float(start[0]) + along * float(vector[0])
            nearest_y = float(start[1]) + along * float(vector[1])
            distance_sq = np.square(grid_x - nearest_x) + np.square(grid_y - nearest_y)
            nearer = distance_sq < closest_distance_sq
            closest_distance_sq = np.where(nearer, distance_sq, closest_distance_sq)
            closest_arc = np.where(
                nearer,
                float(arc_start) + along * float(length),
                closest_arc,
            )

        distance = np.sqrt(closest_distance_sq)
        longitudinal = (
            0.50
            + 0.24 * np.sin(closest_arc / 22.875 + phase)
            + 0.16 * np.sin(closest_arc / 9.875 + phase * 1.71)
            + 0.10 * np.sin(closest_arc / 4.625 - phase * 0.63)
        )
        summit_chain = np.power(
            np.clip((longitudinal - 0.22) / 0.78, 0.0, 1.0),
            1.55,
        )
        crest = np.exp(-0.5 * np.square(distance / 10.25))
        shoulder = np.exp(-0.5 * np.square(distance / 19.375))
        np.maximum(
            wall_addition,
            crest * summit_chain * 20_000.0,
            out=wall_addition,
        )
        np.maximum(
            wall_trough,
            shoulder
            * np.power(np.clip(0.40 - longitudinal, 0.0, 0.40) / 0.40, 1.25)
            * 5_500.0,
            out=wall_trough,
        )

    gate_x = 0.609732 * (HEIGHT_W - 1)
    gate_y = 0.529449 * (HEIGHT_H - 1)
    gate_distance = np.hypot(grid_x - gate_x, grid_y - gate_y)
    gate_guard = np.clip((gate_distance - 26.25) / 37.50, 0.0, 1.0)
    gate_guard = gate_guard * gate_guard * (3.0 - 2.0 * gate_guard)
    authored_strength = np.clip((local - 17_000.0) / 12_000.0, 0.0, 1.0)
    authored_strength = authored_strength * authored_strength * (
        3.0 - 2.0 * authored_strength
    )
    wall_addition *= gate_guard * authored_strength
    wall_trough *= gate_guard * authored_strength

    local -= wall_trough
    headroom = np.maximum(72_000.0 - local, 1.0)
    fitted_addition = headroom * wall_addition / (
        headroom * 0.58 + wall_addition
    )
    local += fitted_addition


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

    # The Ardacraft raster and its direct marker describe the same Lonely
    # Mountain a few renderer samples apart.  Keeping both responses produced
    # the two adjacent mesa-like mounds rejected in the fresh v42 live frame.
    # Remove only the duplicated local source body, then rebuild one compact
    # canonical summit below from the direct audited Erebor marker.  The
    # surrounding Iron Hills and Grey Mountains lie well outside this mask.
    projection = json.loads(
        (CONTROL / "projection.json").read_text(encoding="utf-8")
    )
    erebor = next(
        item for item in projection.get("named_peaks", [])
        if item["key"] == "erebor_peak"
    )
    isolate_y, isolate_x = np.ogrid[:HEIGHT_H, :HEIGHT_W]
    isolate_dx = (
        isolate_x.astype(np.float32)
        - float(erebor["center"][0]) * (HEIGHT_W - 1)
    )
    isolate_dy = (
        isolate_y.astype(np.float32)
        - float(erebor["center"][1]) * (HEIGHT_H - 1)
    )
    isolate_distance = np.hypot(isolate_dx, isolate_dy)
    isolate_radius = HEIGHT_H * 0.0105
    isolate_weight = np.power(
        np.clip(1.0 - isolate_distance / isolate_radius, 0.0, 1.0),
        1.65,
    )
    local_relief = np.maximum(elevation - lowland_reference, 0.0)
    elevation -= local_relief * isolate_weight * 0.94

    # Native vanilla calibration showed that v44 Gundabad's upper half and
    # upper quarter occupy much more of the review window than even the dense
    # Himalayan reference. Contract only the broad source shoulder here; the
    # exact named summit is rebuilt below, so Gundabad remains a distinct high
    # northern anchor without reading as one oversized tabletop massif.
    gundabad = next(
        item for item in projection.get("named_peaks", [])
        if item["key"] == "mount_gundabad"
    )
    gundabad_dx = (
        isolate_x.astype(np.float32)
        - float(gundabad["center"][0]) * (HEIGHT_W - 1)
    )
    gundabad_dy = (
        isolate_y.astype(np.float32)
        - float(gundabad["center"][1]) * (HEIGHT_H - 1)
    )
    gundabad_distance = np.hypot(gundabad_dx, gundabad_dy)
    gundabad_radius = HEIGHT_H * 0.036
    gundabad_weight = np.power(
        np.clip(1.0 - gundabad_distance / gundabad_radius, 0.0, 1.0),
        1.35,
    )
    local_relief = np.maximum(elevation - lowland_reference, 0.0)
    elevation -= local_relief * gundabad_weight * 0.72

    # The source-native Mordor corner is correctly shaped but the v42 live
    # renderer flattened its upper walls into a low berm.  Lift only relief
    # already present in a small Morannon neighbourhood, and only above the
    # foothill band.  This preserves the irregular Ardacraft V, cannot invent
    # a ruler-straight arm, and leaves Cirith Gorgor itself as a low saddle.
    morannon = next(
        item for item in projection["passes"] if item["key"] == "morannon"
    )
    morannon_dx = (
        isolate_x.astype(np.float32)
        - float(morannon["center"][0]) * (HEIGHT_W - 1)
    )
    morannon_dy = (
        isolate_y.astype(np.float32)
        - float(morannon["center"][1]) * (HEIGHT_H - 1)
    )
    morannon_distance = np.hypot(morannon_dx, morannon_dy)
    morannon_radius = HEIGHT_H * 0.055
    morannon_weight = np.power(
        np.clip(1.0 - morannon_distance / morannon_radius, 0.0, 1.0),
        1.35,
    )
    local_relief = np.maximum(elevation - lowland_reference, 0.0)
    upper_wall = np.power(
        np.clip((local_relief - 5_500.0) / 22_000.0, 0.0, 1.0),
        0.88,
    )
    elevation += morannon_weight * upper_wall * 16_000.0
    mountain_strength = np.clip(
        (elevation - lowland_reference) / 22_000.0,
        0.0,
        1.0,
    )
    # Render the shoreline at the heightmap's native resolution. Nearest
    # enlargement of the 4096x2048 control made every source pixel a visible
    # two-pixel stair in the real renderer. The normalized authored geometry
    # remains the single source of truth.
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
        (2048, 1024, 0.07),
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
        np.clip((rugged_unit - 0.02) / 1.85, 0.0, 1.0),
        1.42,
    )
    # Centre the peak contribution so it changes local form, not the authored
    # theatre-scale range altitude.
    positive_peaks -= float(positive_peaks.mean())
    # v43 proved that correct narrow source footprints can still read as
    # smooth green walls once EU5 applies its shallow terrain projection and
    # political tint.  Increase *local* fold and summit variation without
    # widening the authored massif: both terms remain multiplied by the
    # existing mountain strength, so no ridge, spur, pass, or lowland moves.
    elevation += folded * (
        6_000.0 * np.power(mountain_strength, 0.88)
    )
    elevation += positive_peaks * (
        9_500.0 * np.power(mountain_strength, 1.12)
    )

    # v45 proved that native-frequency signed noise becomes repeated terraces
    # after q64 cache quantization even when aggregate gradients pass. Use the
    # committed Ardacraft numeric relief itself for the missing narrow arÃªte
    # response. Bicubic source reconstruction yields smooth multi-sample
    # crests, and the high threshold cannot create a ridge outside the audited
    # range field. Preserve the accepted isolated Erebor and Orodruin forms.
    native_source_relief = source_relief_field(
        projection, (HEIGHT_W, HEIGHT_H)
    )
    source_arete = np.power(
        np.clip((native_source_relief - 0.72) / 0.28, 0.0, 1.0),
        1.35,
    )
    accepted_guard = 1.0 - np.clip(
        1.0 - isolate_distance / (HEIGHT_H * 0.020), 0.0, 1.0
    )
    mount_doom = next(
        item for item in load_settlements() if item.key == "mount_doom"
    )
    doom_guard_dx = (
        isolate_x.astype(np.float32) - float(mount_doom.x) * (HEIGHT_W - 1)
    )
    doom_guard_dy = (
        isolate_y.astype(np.float32) - float(mount_doom.y) * (HEIGHT_H - 1)
    )
    doom_guard_distance = np.hypot(doom_guard_dx, doom_guard_dy)
    accepted_guard *= 1.0 - np.clip(
        1.0 - doom_guard_distance / (HEIGHT_H * 0.018), 0.0, 1.0
    )
    # The source top band is locally dense at Gundabad; without this reuse of
    # the calibrated contraction mask it simply rebuilds the v44 broad cap
    # after the shoulder has been removed. Retain only a narrow fraction of
    # the extra arÃªte response at the named junction.
    accepted_guard *= 1.0 - gundabad_weight * 0.95
    elevation += (
        source_arete
        * 8_000.0
        * np.power(mountain_strength, 0.92)
        * accepted_guard
    )

    # v48 proved that a single high continuity spine reads as a smooth cliff
    # even when its plan-view width and longitudinal noise are bounded. EU5's
    # vanilla-calibrated ranges instead present a moderate connected body with
    # many distinct high summits. Select those summit centres from local
    # maxima in the hash-pinned Ardacraft relief itself rather than spacing
    # stamps along a line. This preserves real branching and produces
    # irregular multi-row peak groups instead of v49's rejected beads.
    pass_guards = [
        (
            float(item["center"][0]) * (HEIGHT_W - 1),
            float(item["center"][1]) * (HEIGHT_H - 1),
            float(item["radius"]) * HEIGHT_H * 1.55,
        )
        for item in projection["passes"]
    ]

    reduced_relief = np.round(
        native_source_relief[4::8, 4::8] * 255.0
    ).astype(np.uint8)
    local_relief_maximum = np.asarray(
        Image.fromarray(reduced_relief, "L").filter(ImageFilter.MaxFilter(9)),
        dtype=np.uint8,
    )
    candidate_y, candidate_x = np.nonzero(
        (reduced_relief >= 198)
        & (reduced_relief == local_relief_maximum)
    )
    candidate_order = np.lexsort(
        (
            candidate_x,
            candidate_y,
            -reduced_relief[candidate_y, candidate_x].astype(np.int16),
        )
    )
    occupied = np.zeros_like(reduced_relief, dtype=bool)
    separation = 6
    for candidate_index in candidate_order:
        reduced_x = int(candidate_x[candidate_index])
        reduced_y = int(candidate_y[candidate_index])
        if occupied[reduced_y, reduced_x]:
            continue
        occupied[
            max(0, reduced_y - separation) : reduced_y + separation + 1,
            max(0, reduced_x - separation) : reduced_x + separation + 1,
        ] = True
        center_x = reduced_x * 8 + 4
        center_y = reduced_y * 8 + 4
        if water[center_y, center_x] or accepted_guard[center_y, center_x] < 0.50:
            continue
        center = np.array([center_x, center_y], dtype=np.float64)
        if any(
            np.hypot(center_x - guard_x, center_y - guard_y) < guard_radius
            for guard_x, guard_y, guard_radius in pass_guards
        ):
            continue
        rng = np.random.default_rng(
            stable_seed(f"source-summit:{center_x}:{center_y}")
        )
        angle = float(rng.uniform(0.0, np.pi))
        tangent = np.array([np.cos(angle), np.sin(angle)], dtype=np.float64)
        normal = np.array([-tangent[1], tangent[0]], dtype=np.float64)
        along_radius = float(rng.uniform(10.0, 24.0))
        across_radius = float(rng.uniform(7.0, 15.0))
        extent = int(np.ceil(max(along_radius, across_radius) * 1.20))
        left = max(0, center_x - extent)
        right = min(HEIGHT_W, center_x + extent + 1)
        top = max(0, center_y - extent)
        bottom = min(HEIGHT_H, center_y + extent + 1)
        local_y, local_x = np.ogrid[top:bottom, left:right]
        delta_x = local_x.astype(np.float32) - float(center_x)
        delta_y = local_y.astype(np.float32) - float(center_y)
        along = delta_x * tangent[0] + delta_y * tangent[1]
        across = delta_x * normal[0] + delta_y * normal[1]
        distance = np.sqrt(
            (along / along_radius) ** 2
            + (across / across_radius) ** 2
        )
        polar = np.arctan2(across, along)
        distance *= (
            1.0
            + 0.11 * np.sin(polar * 3.0 + rng.uniform(0.0, 6.0))
            + 0.05 * np.sin(polar * 7.0 + rng.uniform(0.0, 6.0))
        )
        tooth = np.power(np.clip(1.0 - distance, 0.0, 1.0), 1.68)
        source_strength = np.clip(
            (float(reduced_relief[reduced_y, reduced_x]) / 255.0 - 0.78)
            / 0.22,
            0.0,
            1.0,
        )
        centre_height = float(elevation[center_y, center_x])
        ceiling_room = np.clip((60_000.0 - centre_height) / 16_000.0, 0.12, 1.0)
        amplitude = (
            (6_000.0 + 14_000.0 * source_strength)
            * float(rng.uniform(0.72, 1.18))
            * ceiling_room
        )
        elevation[top:bottom, left:right] += tooth * amplitude

    def add_path_summits(
        path: list[tuple[int, int]],
        *,
        key: str,
        height_scale: float,
        include_endpoint: bool = False,
    ) -> None:
        rng = np.random.default_rng(stable_seed(f"final-summits:{key}"))
        # Only the two exact Arda Maps branch endpoints need this fallback;
        # all ordinary summits are selected from numeric source maxima above.
        indices = [len(path) - 1] if include_endpoint and path else []
        for index in indices:
            before = np.asarray(path[max(0, index - 2)], dtype=np.float64)
            after = np.asarray(path[min(len(path) - 1, index + 2)], dtype=np.float64)
            tangent = after - before
            tangent_length = float(np.linalg.norm(tangent))
            if tangent_length < 1.0:
                continue
            tangent /= tangent_length
            normal = np.array([-tangent[1], tangent[0]], dtype=np.float64)
            center = np.asarray(path[index], dtype=np.float64)
            if any(
                np.hypot(center[0] - guard_x, center[1] - guard_y) < guard_radius
                for guard_x, guard_y, guard_radius in pass_guards
            ):
                continue
            # Strong overlap along the chain makes one serrated crest rather
            # than a row of circular beads; the narrow across-range radius
            # keeps that crest from broadening into another plateau.
            along_radius = float(rng.uniform(68.0, 126.0))
            across_radius = float(rng.uniform(7.0, 12.0))
            extent = int(np.ceil(along_radius * 1.18))
            left = max(0, int(center[0]) - extent)
            right = min(HEIGHT_W, int(center[0]) + extent + 1)
            top = max(0, int(center[1]) - extent)
            bottom = min(HEIGHT_H, int(center[1]) + extent + 1)
            local_y, local_x = np.ogrid[top:bottom, left:right]
            delta_x = local_x.astype(np.float32) - float(center[0])
            delta_y = local_y.astype(np.float32) - float(center[1])
            along = delta_x * tangent[0] + delta_y * tangent[1]
            across = delta_x * normal[0] + delta_y * normal[1]
            distance = np.sqrt(
                (along / along_radius) ** 2
                + (across / across_radius) ** 2
            )
            angle = np.arctan2(across, along)
            distance *= (
                1.0
                + 0.10 * np.sin(angle * 3.0 + rng.uniform(0.0, 6.0))
                + 0.045 * np.sin(angle * 7.0 + rng.uniform(0.0, 6.0))
            )
            tooth = np.power(np.clip(1.0 - distance, 0.0, 1.0), 1.82)
            endpoint = include_endpoint and index == len(path) - 1
            amplitude = float(
                rng.uniform(12_000.0, 15_000.0)
                if endpoint
                else rng.uniform(1_000.0, 4_000.0)
            ) * height_scale
            local = elevation[top:bottom, left:right]
            local += tooth * amplitude

    for ridge in projection["ridges"]:
        if "source_supported_gain" not in ridge:
            continue
        for branch_index, branch in enumerate(ridge.get("branches", [])):
            add_path_summits(
                natural_path(
                    branch,
                    (HEIGHT_W, HEIGHT_H),
                    key=f"ridge:{ridge['key']}:branch:{branch_index}",
                    closed=False,
                    amplitude=float(ridge.get("wander", 0.0035)),
                    spacing=0.003,
                ),
                key=f"{ridge['key']}:branch:{branch_index}",
                height_scale=0.94,
                include_endpoint=bool(ridge.get("source_audited_branches", False)),
            )

    # Named canonical summits are compact final-resolution peaks, never broad
    # control-layer stamps. They reinforce exact audited anchors (especially
    # the direct Ardacraft Erebor marker) while the source field continues to
    # own every surrounding ridge, spur and pass.
    summit_y, summit_x = np.ogrid[:HEIGHT_H, :HEIGHT_W]
    for peak_index, peak in enumerate(projection.get("named_peaks", [])):
        strength = float(peak["strength"])
        if strength < 0.80:
            continue
        if peak["key"] not in {"erebor_peak", "mount_gundabad"}:
            continue
        peak_x = float(peak["center"][0]) * (HEIGHT_W - 1)
        peak_y = float(peak["center"][1]) * (HEIGHT_H - 1)
        peak_dx = summit_x.astype(np.float32) - peak_x
        peak_dy = summit_y.astype(np.float32) - peak_y
        peak_angle = np.arctan2(peak_dy, peak_dx)
        phase = peak_index * 0.731
        peak_distance = np.hypot(peak_dx, peak_dy) * (
            1.0
            + 0.065 * np.sin(peak_angle * 3.0 + phase)
            + 0.035 * np.sin(peak_angle * 7.0 - phase * 0.7)
            + 0.018 * np.cos(peak_angle * 11.0 + 0.4)
        )
        profile_scale = (
            0.44
            if peak["key"] == "erebor_peak"
            else 0.52
            if peak["key"] == "mount_gundabad"
            else 0.32
        )
        summit_radius = max(
            4.0,
            float(peak["radius"]) * HEIGHT_H * profile_scale,
        )
        apron = np.power(
            np.clip(1.0 - peak_distance / (summit_radius * 1.65), 0.0, 1.0),
            2.0,
        )
        summit = np.power(
            np.clip(1.0 - peak_distance / summit_radius, 0.0, 1.0),
            1.72
            if peak["key"] == "erebor_peak"
            else 1.58
            if peak["key"] == "mount_gundabad"
            else 1.20,
        )
        latitude_height = 10_500.0 + (1.0 - float(peak["center"][1])) * 2_500.0
        if peak["key"] == "erebor_peak":
            apron_height, summit_height = 3_200.0, 54_500.0
        elif peak["key"] == "mount_gundabad":
            apron_height, summit_height = 3_000.0, 58_000.0
        else:
            # Arda Maps peak points sometimes land a few raster pixels off the
            # Ardacraft painted crest. A tiny final-resolution tooth binds the
            # canonical summit without creating another range-sized body.
            apron_height, summit_height = 2_800.0, 47_000.0
        target = latitude_height + strength * (
            apron * apron_height + summit * summit_height
        )
        elevation = np.maximum(elevation, target)

    # Mount Doom is a compact, isolated stratovolcano. Author it after the
    # generic range response so its upper cone is never clipped to the range
    # normalizer's endpoint. The asymmetric profile, broken rim and explicit
    # crater retain source position without manufacturing a flat cap.
    doom_px = float(mount_doom.x) * (HEIGHT_W - 1)
    doom_py = float(mount_doom.y) * (HEIGHT_H - 1)
    doom_y, doom_x = np.ogrid[:HEIGHT_H, :HEIGHT_W]
    doom_dx = doom_x.astype(np.float32) - doom_px
    doom_dy = doom_y.astype(np.float32) - doom_py
    doom_angle = np.arctan2(doom_dy, doom_dx)
    doom_distance = np.hypot(doom_dx, doom_dy)
    irregular_distance = doom_distance * (
        1.0
        + 0.032 * np.sin(doom_angle * 3.0 + 0.8)
        + 0.016 * np.sin(doom_angle * 7.0 - 0.35)
        + 0.008 * np.cos(doom_angle * 11.0 + 0.25)
    )
    apron_radius = max(14.0, HEIGHT_H / 205.0)
    cone_radius = max(7.0, HEIGHT_H / 410.0)
    apron = np.power(
        np.clip(1.0 - irregular_distance / apron_radius, 0.0, 1.0),
        2.45,
    )
    cone = np.power(
        np.clip(1.0 - irregular_distance / cone_radius, 0.0, 1.0),
        1.62,
    )
    rim_radius = cone_radius * 0.24
    rim_width = max(0.80, cone_radius * 0.09)
    rim = np.exp(-0.5 * np.square((doom_distance - rim_radius) / rim_width))
    crater = np.exp(
        -0.5 * np.square(doom_distance / max(0.80, rim_radius * 0.58))
    )
    doom_relief = (
        apron * 4_800.0
        + cone * 62_000.0
        + rim * 7_000.0
        - crater * 12_000.0
    )
    elevation += doom_relief

    # EU5 derives the regional mountain silhouette from this coarse source;
    # native-cache-only serration changed face texture but left the v63 wall
    # visually flat. Apply the exact-axis skyline before shoreline easing and
    # the continuous summit ceiling.
    serrate_mordor_walls(elevation, projection)

    # Ease dry ground down toward EU5's water plane before zeroing submerged
    # terrain. A hard 10.5k-to-zero discontinuity made every tiny source lake
    # look like a quarry at close zoom even though its shoreline was precise.
    shore_field = np.asarray(
        Image.fromarray(water.astype(np.uint8) * 255, "L").filter(
            ImageFilter.GaussianBlur(radius=6.0)
        ),
        dtype=np.float32,
    ) / 255.0
    shore_blend = np.clip((shore_field - 0.015) / 0.43, 0.0, 1.0)
    shore_target = 6_250.0
    elevation = np.where(
        ~water,
        elevation * (1.0 - shore_blend)
        + np.minimum(elevation, shore_target) * shore_blend,
        elevation,
    )
    elevation[~water] = np.maximum(elevation[~water], shore_target)
    elevation[water] = 0.0
    # Preserve summit ordering and fine source-derived crest variation. Hard
    # uint16 clipping was producing thousands of identical 65535 samples,
    # which the close renderer showed as broad flat plateaus.
    elevation = soft_ceiling(elevation, knee=59_000.0, ceiling=65_480.0)
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
    maximum = int(expected_height.max())
    if maximum < 60_000:
        failures.append("heightmap lacks the reviewed sharp summit profile")
    if maximum >= 65_000 or np.count_nonzero(expected_height == 65_535):
        failures.append("heightmap summit profile is hard-clipped into plateaus")
    dry_height = expected_height[expected_height > 0]
    # Broad high-area floors rewarded the rejected v30/v31 models for lifting
    # whole source envelopes into plateaus. Retain enough high terrain for the
    # major chains, but bind the gate to steep upper-massif gradients instead.
    if int(np.percentile(dry_height, 99.0)) < 30_000:
        failures.append("heightmap upper massif relief is too low")
    high_relief_count = int(np.count_nonzero(dry_height >= 45_000))
    if high_relief_count < 80_000:
        failures.append("heightmap high-relief coverage is too sparse")
    if high_relief_count > 350_000:
        failures.append("heightmap high-relief coverage regressed to broad mesas")
    gradient_y, gradient_x = np.gradient(expected_height.astype(np.float32))
    gradient = np.hypot(gradient_x, gradient_y)
    high_cap = expected_height >= 45_000
    flat_cap_fraction = float((gradient[high_cap] < 512.0).mean())
    high_gradient_p90 = float(np.percentile(gradient[high_cap], 90.0))
    # Vanilla's installed height source has a 77% sub-512 fraction above 45k;
    # the old 10% ceiling forced ENDÓRË into gradients nearly ten times larger
    # and directly rewarded cliff shelves. Require meaningful crest variation
    # while accepting the continuous high shoulders used by the real engine.
    if flat_cap_fraction > 0.86 or high_gradient_p90 < 650.0:
        failures.append(
            "heightmap high relief lacks continuous but varied summit structure"
        )
    upper_massif_gradient = gradient[expected_height >= 25_000]
    upper_gradient_p75 = float(np.percentile(upper_massif_gradient, 75.0))
    upper_gradient_p90 = float(np.percentile(upper_massif_gradient, 90.0))
    if upper_gradient_p75 < 900.0 or upper_gradient_p90 < 1_400.0:
        failures.append("heightmap mountain bodies have regressed to broad hills")
    # v43's 2,174 p75 still read as smooth walls in the real half-canvas
    # renderer.  Permit v44's source-scoped serration while retaining a wide
    # safety margin below the rejected v39 shelves (5,428/7,561).
    if upper_gradient_p75 > 3_200.0 or upper_gradient_p90 > 5_200.0:
        failures.append("heightmap mountain bodies regressed to cliff shelves")
    projection = json.loads(
        (CONTROL / "projection.json").read_text(encoding="utf-8")
    )
    pass_by_key = {item["key"]: item for item in projection["passes"]}
    for key in ("paths_of_the_dead", "morannon"):
        center_x, center_y = pass_by_key[key]["center"]
        sample = int(
            expected_height[
                round(float(center_y) * (HEIGHT_H - 1)),
                round(float(center_x) * (HEIGHT_W - 1)),
            ]
        )
        if sample >= 30_000:
            failures.append(f"{key} no longer retains a traversable saddle floor")

    # Bind the two v34-v36 live failures independently. The earlier contracts
    # required 15-24% of a tiny route-centred disc to exceed 43k; that directly
    # rewarded the broad green uplands the camera rejected. The source places
    # both settlements/pass floors below adjacent crests, so use an honest
    # theatre radius and require a tall, steep, *bounded-area* flank instead.
    flank_contracts = {
        "dunharrow": {
            "center": (0.496751, 0.553026),
            "radius": 0.018,
            "minimum_maximum": 48_000,
            "minimum_high_fraction": 0.001,
            "maximum_high_fraction": 0.065,
            "gradient_minimum_height": 25_000,
            "gradient_percentile": 75.0,
            "minimum_gradient": 700,
        },
        "morannon": {
            "center": (0.609732, 0.529449),
            "radius": 0.030,
            "minimum_maximum": 43_000,
            "minimum_high_fraction": 0.001,
            # Source-backed upper arÃªtes occupy about 2% of this honest
            # theatre window. That remains a sparse pair of walls, not an
            # upland, and is necessary for the gate enclosure to render.
            "maximum_high_fraction": 0.040,
            "gradient_minimum_height": 25_000,
            "gradient_percentile": 75.0,
            "minimum_gradient": 900,
        },
    }
    for key, contract in flank_contracts.items():
        center_x = round(contract["center"][0] * (HEIGHT_W - 1))
        center_y = round(contract["center"][1] * (HEIGHT_H - 1))
        radius = max(2, round(contract["radius"] * HEIGHT_H))
        left, right = max(0, center_x - radius), min(HEIGHT_W, center_x + radius + 1)
        top, bottom = max(0, center_y - radius), min(HEIGHT_H, center_y + radius + 1)
        local_y, local_x = np.ogrid[top:bottom, left:right]
        radial = (
            (local_x - center_x) ** 2 + (local_y - center_y) ** 2
        ) <= radius**2
        samples = expected_height[top:bottom, left:right][radial]
        local_height = expected_height[top:bottom, left:right]
        gradient_mask = radial
        if "gradient_minimum_height" in contract:
            gradient_mask = radial & (
                local_height >= int(contract["gradient_minimum_height"])
            )
        gradient_samples = gradient[top:bottom, left:right][gradient_mask]
        if gradient_samples.size == 0:
            failures.append(f"{key} lacks measurable mountain flanks")
            continue
        maximum = int(samples.max())
        high_fraction = float((samples >= 43_000).mean())
        gradient_percentile = float(contract.get("gradient_percentile", 90.0))
        gradient_measure = float(
            np.percentile(gradient_samples, gradient_percentile)
        )
        if maximum < contract["minimum_maximum"]:
            failures.append(f"{key} lacks a high adjacent mountain flank")
        if high_fraction < contract["minimum_high_fraction"]:
            failures.append(f"{key} mountain flanks are too sparse")
        if high_fraction > contract["maximum_high_fraction"]:
            failures.append(f"{key} mountain flanks regressed to a broad upland")
        minimum_gradient = float(
            contract.get("minimum_gradient", contract.get("minimum_gradient_p90", 0.0))
        )
        if gradient_measure < minimum_gradient:
            failures.append(f"{key} adjacent mountain flank is not steep enough")
    for peak in projection.get("named_peaks", []):
        if float(peak["strength"]) < 0.8:
            continue
        x = round(float(peak["center"][0]) * (HEIGHT_W - 1))
        y = round(float(peak["center"][1]) * (HEIGHT_H - 1))
        radius = max(2, round(float(peak["radius"]) * HEIGHT_H * 1.4))
        window = expected_height[
            max(0, y - radius) : min(HEIGHT_H, y + radius + 1),
            max(0, x - radius) : min(HEIGHT_W, x + radius + 1),
        ]
        minimum = (
            58_000
            if peak["key"] == "erebor_peak"
            # Ordinary Arda Maps points are audit anchors within a source-
            # owned chain, not instructions to stamp isolated summit teeth.
            # Starkhorn lies on a lower exact source shoulder, so require a
            # substantial local massif without forcing another v41 spike.
            else 26_000
        )
        if window.size == 0 or int(window.max()) < minimum:
            failures.append(
                f"named source peak {peak['key']} lacks high local relief"
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
            print(f"gen_heightmap: FAIL {failure}")
        return 1
    print("gen_heightmap: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
