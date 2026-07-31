#!/usr/bin/env python3
"""Deterministic shared model for the M2 Middle-earth map generators.

The authored 4096x2048 controls are the single source of truth.  This module
turns them into a labelled raster model; individual generators package that
model into EU5 files.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, deque
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "docs/world/control"
DERIVED = ROOT / "docs/world/derived"
MAP_OUT = ROOT / "in_game/map_data"
TERRAIN_OUT = ROOT / "in_game/gfx/terrain2"

CONTROL_W, CONTROL_H = 4096, 2048
WORLD_W, WORLD_H = 16384, 8192
HEIGHT_W, HEIGHT_H = 8192, 4096
BIOME_W, BIOME_H = HEIGHT_W - 1, HEIGHT_H - 1
SEED = 3018

# The installed native 16384x8192 map registers 28,490 locations. Both the
# exact-count tree and progressively smaller 14,245- and 12,104-cell trees
# reached the target machine's fresh-game renderer memory cliff. The latter
# loaded twice, but later byte-exact repeats exhausted 32.4 GB of private
# memory after cached-data completion and never rendered country selection.
# Keep a release-safe margin with roughly half that political tessellation.
# Cartographic precision lives in the independent authored coast, height,
# river, forest, biome, and q64 terrain controls; none is rescaled here.
TARGETS = {
    "land": 5_200,
    "mountain": 600,
    "lake": 60,
    "sea": 144,
}

KIND_ORDER = ("land", "mountain", "lake", "sea")
KIND_CODE = {"sea": 0, "land": 1, "lake": 2, "mountain": 3}
LOCALIZATION_COLLISION_RENAMES = {
    # Live EU5 localization-table evidence from the first M2 smoke.
    "me_land_2436": "me_land_2436_endore",
    "me_land_5457": "me_land_5457_endore",
    "me_land_16368": "me_land_16368_endore",
    "me_sea_0241": "me_sea_0241_endore",
}
CONTROL_BIOMES = {
    0: "ocean",
    1: "temperate",
    2: "forest",
    3: "dense_forest",
    4: "mountain",
    5: "tundra",
    6: "marsh",
    7: "lake",
    8: "ash",
    9: "steppe",
    10: "arid",
}
FOREST_TEMPLATE_MIN_FRACTION = 0.72


@dataclass(frozen=True)
class Anchor:
    key: str
    name: str
    x: float
    y: float
    rank: str
    language: str
    realm_hint: str
    source: str


@dataclass(frozen=True)
class Location:
    index: int
    key: str
    display_name: str
    kind: str
    x: int
    y: int
    biome_id: int
    continent: str
    region: str
    color: tuple[int, int, int]
    anchor: bool = False

    @property
    def normalized(self) -> tuple[float, float]:
        return self.x / (CONTROL_W - 1), self.y / (CONTROL_H - 1)


@dataclass
class WorldModel:
    labels: np.ndarray
    kind_map: np.ndarray
    biomes: np.ndarray
    density: np.ndarray
    locations: list[Location]
    areas: np.ndarray

    @property
    def by_key(self) -> dict[str, Location]:
        return {location.key: location for location in self.locations}


def location_biome_counts(model: WorldModel) -> np.ndarray:
    """Count authored control-biome cells owned by every generated location."""
    return np.bincount(
        (model.labels.ravel() * 11 + model.biomes.ravel()).astype(np.int64),
        minlength=len(model.locations) * 11,
    ).reshape((len(model.locations), 11))


def effective_template_biomes(
    model: WorldModel,
    counts: np.ndarray | None = None,
) -> np.ndarray:
    """Return the biome actually exposed by location-scoped terrain templates.

    Continuous object transforms render porous woodland margins.  A location-wide
    woods/forest template is therefore reserved for cells whose authored woodland
    coverage is unambiguous; fringe cells fall back to temperate terrain.  Consumers
    such as raw-material generation must use this same classification because engine
    potentials evaluate the final template, not the raw control-layer majority.
    """
    if counts is None:
        counts = location_biome_counts(model)
    effective = np.argmax(counts, axis=1)
    forest_fraction = (counts[:, 2] + counts[:, 3]) / model.areas
    land = np.fromiter(
        (location.kind == "land" for location in model.locations),
        dtype=np.bool_,
        count=len(model.locations),
    )
    forest = np.isin(effective, (2, 3))
    effective[land & forest & (forest_fraction < FOREST_TEMPLATE_MIN_FRACTION)] = 1
    return effective


def load_anchors() -> list[Anchor]:
    path = CONTROL / "settlements.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [
        Anchor(
            key=row["key"],
            name=row["name"],
            x=float(row["x"]),
            y=float(row["y"]),
            rank=row["rank"],
            language=row["language"],
            realm_hint=row["realm_hint"],
            source=row["source"],
        )
        for row in rows
    ]


def control_array(name: str) -> np.ndarray:
    with Image.open(CONTROL / name) as image:
        if image.size != (CONTROL_W, CONTROL_H):
            raise ValueError(f"{name} is {image.size}, expected {(CONTROL_W, CONTROL_H)}")
        return np.asarray(image).copy()


def source_sha256() -> str:
    digest = hashlib.sha256()
    for name in ("projection.json", "settlements.csv"):
        digest.update((CONTROL / name).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def game_map() -> Path:
    config = json.loads((ROOT / "config/local_paths.json").read_text(encoding="utf-8-sig"))
    return Path(config["game_dir"]) / "game/in_game/map_data"


@lru_cache(maxsize=1)
def installed_named_registry() -> tuple[str, set[str], set[tuple[int, int, int]]]:
    text = (game_map() / "named_locations/00_default.txt").read_text(
        encoding="utf-8-sig"
    )
    names: set[str] = set()
    colors: set[tuple[int, int, int]] = set()
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if "=" not in line:
            continue
        key, raw_value = (part.strip() for part in line.split("=", 1))
        if not key or not raw_value:
            continue
        try:
            value = int(raw_value, 16)
        except ValueError:
            continue
        names.add(key)
        colors.add(((value >> 16) & 255, (value >> 8) & 255, value & 255))
    return text, names, colors


def location_colors(count: int) -> list[tuple[int, int, int]]:
    """Return colors unique against both vanilla and earlier ENDÓRË colors."""
    used = set(installed_named_registry()[2])
    result: list[tuple[int, int, int]] = []
    for index in range(1, count + 1):
        value = ((index + 37) * 0x9E3779 + 0x5A17C3) & 0xFFFFFF
        while True:
            color = (value >> 16) & 255, (value >> 8) & 255, value & 255
            if color not in used and color not in ((0, 0, 0), (255, 255, 255)):
                break
            value = (value + 0x9E3779) & 0xFFFFFF
        used.add(color)
        result.append(color)
    return result


def spatial_group(x: float, y: float) -> tuple[str, str]:
    """Assign strategic regions in the equal-scale ArdaCraft projection.

    These boundaries follow the source-audited physical frame.  They are
    deliberately resolved from the most geographically constrained realms
    outward so the broad wilderness bins cannot swallow narrow countries.
    """
    if y < 0.12:
        if x < 0.40:
            return "me_forodwaith", "me_forochel_region"
        if x < 0.49:
            return "me_forodwaith", "me_angmar_region"
        return "me_forodwaith", "me_northern_wastes_region"

    # Harad and Khand use the actual southern/eastern extents rather than the
    # old vertically stretched sketch.
    if y > 0.76:
        if x < 0.56 and y > 0.86:
            return "me_harad", "me_umbar_region"
        if x > 0.69 and y < 0.88:
            return "me_mordor_and_rhun", "me_khand_region"
        if y < 0.91:
            return "me_harad", "me_near_harad_region"
        return "me_harad", "me_far_harad_region"

    # Rhûn lies east of Rhovanion and north/east of Mordor; the diagonal keeps
    # Dorwinion west of the Sea of Rhûn in its intended frontier region.
    if x > max(0.62, 0.645 + (y - 0.30) * 0.10):
        if y < 0.52:
            return "me_mordor_and_rhun", "me_rhun_region"
        if y < 0.72:
            return "me_mordor_and_rhun", "me_mordor_region"
        return "me_mordor_and_rhun", "me_khand_region"

    # Calenardhon is the strip between Fangorn/Anduin and the White Mountains.
    if 0.455 <= x < 0.565 and 0.43 <= y < 0.57:
        return "me_rhovanion", "me_rohan_region"

    # Gondor follows the White Mountains, Anduin, and Ephel Dúath.
    if y >= 0.56:
        if x < 0.525:
            return "me_gondor", "me_belfalas_region"
        if x < 0.575 and y > 0.63:
            return "me_gondor", "me_lebennin_region"
        if x >= 0.585 and y < 0.70:
            return "me_gondor", "me_ithilien_region"
        if y < 0.635:
            return "me_gondor", "me_anorien_region"
        return "me_gondor", "me_south_gondor_region"

    # Rhovanion is split around the Anduin and the source forest footprints.
    if x >= 0.485:
        if y < 0.15:
            return "me_rhovanion", "me_grey_mountains_region"
        if x > 0.585 and y < 0.22:
            return "me_rhovanion", "me_dale_region"
        if x > 0.545 and y < 0.38:
            return "me_rhovanion", "me_mirkwood_region"
        if x < 0.55 and y < 0.43:
            return "me_rhovanion", "me_anduin_vale_region"
        return "me_rhovanion", "me_brown_lands_region"

    # Eriador: Lindon is west of Ered Luin, the Shire/Bree belt sits around
    # the East Road, and Enedwaith begins south of the Glanduin/Gwathló system.
    if x < 0.315:
        return "me_eriador", "me_lindon_region"
    if y < 0.205 or (x >= 0.405 and y < 0.30):
        return "me_eriador", "me_north_arnor_region"
    if x < 0.415 and y < 0.295:
        return "me_eriador", "me_shire_breeland_region"
    return "me_eriador", "me_enedwaith_region"


def kind_masks(biomes: np.ndarray, anchors: list[Anchor]) -> tuple[np.ndarray, dict[str, tuple[int, int]]]:
    kind_map = np.full(biomes.shape, KIND_CODE["land"], dtype=np.uint8)
    kind_map[biomes == 0] = KIND_CODE["sea"]
    kind_map[biomes == 7] = KIND_CODE["lake"]
    kind_map[biomes == 4] = KIND_CODE["mountain"]

    pinned: dict[str, tuple[int, int]] = {}
    for anchor in anchors:
        x = round(anchor.x * (CONTROL_W - 1))
        y = round(anchor.y * (CONTROL_H - 1))
        if kind_map[y, x] in (KIND_CODE["sea"], KIND_CODE["lake"]):
            raise ValueError(f"anchor {anchor.key} is not on authored land")
        pinned[anchor.key] = (y, x)
        # A pinned stronghold or pass is playable even where its exact point
        # intersects a ridge. Connect it to nearby authored land instead of
        # creating an isolated 3x3 passable island inside the mountains.
        carve_anchor_access(kind_map, y, x)
    # Passes are authored movement contracts, not merely low-elevation paint.
    # The blurred ridge control can otherwise leave a two-pixel mountain seam
    # across a visually open gap. Hard-cut every pass disk into playable land
    # before component cleanup and seed placement.
    projection = json.loads((CONTROL / "projection.json").read_text(encoding="utf-8"))
    yy, xx = np.ogrid[:CONTROL_H, :CONTROL_W]
    for pass_data in projection["passes"]:
        px = round(float(pass_data["center"][0]) * (CONTROL_W - 1))
        py = round(float(pass_data["center"][1]) * (CONTROL_H - 1))
        radius = max(2, round(float(pass_data["radius"]) * CONTROL_H))
        disk = (xx - px) ** 2 + (yy - py) ** 2 <= radius**2
        kind_map[disk & (kind_map == KIND_CODE["mountain"])] = KIND_CODE["land"]
    clean_small_components(
        kind_map,
        minimum=4,
        protected_land=set(pinned.values()),
    )
    return kind_map, pinned


def carve_anchor_access(kind_map: np.ndarray, y: int, x: int) -> None:
    """Cut a narrow deterministic connection from a ridge anchor to land."""
    if kind_map[y, x] == KIND_CODE["land"]:
        return
    search_radius = 96
    y0, y1 = max(0, y - search_radius), min(CONTROL_H, y + search_radius + 1)
    x0, x1 = max(0, x - search_radius), min(CONTROL_W, x + search_radius + 1)
    candidates = np.argwhere(
        kind_map[y0:y1, x0:x1] == KIND_CODE["land"]
    )
    if not len(candidates):
        raise ValueError(f"anchor {(y, x)} has no land within {search_radius} cells")
    candidates[:, 0] += y0
    candidates[:, 1] += x0
    distances = np.square(candidates[:, 0] - y) + np.square(candidates[:, 1] - x)
    target_y, target_x = (
        int(value) for value in candidates[int(np.argmin(distances))]
    )
    steps = max(abs(target_y - y), abs(target_x - x), 1)
    for line_y, line_x in zip(
        np.rint(np.linspace(y, target_y, steps + 1)).astype(int),
        np.rint(np.linspace(x, target_x, steps + 1)).astype(int),
    ):
        for ny in range(max(0, line_y - 2), min(CONTROL_H, line_y + 3)):
            for nx in range(max(0, line_x - 2), min(CONTROL_W, line_x + 3)):
                if kind_map[ny, nx] == KIND_CODE["mountain"]:
                    kind_map[ny, nx] = KIND_CODE["land"]


def clean_small_components(
    kind_map: np.ndarray,
    minimum: int,
    protected_land: set[tuple[int, int]] | None = None,
) -> None:
    """Absorb raster artifacts and unplayable mountain-enclosed land pockets."""
    protected_land = protected_land or set()
    for class_id in KIND_CODE.values():
        mask = kind_map == class_id
        seen = np.zeros(mask.shape, dtype=bool)
        for start_y, start_x in np.argwhere(mask):
            start = (int(start_y), int(start_x))
            if seen[start]:
                continue
            queue: deque[tuple[int, int]] = deque([start])
            seen[start] = True
            cells: list[tuple[int, int]] = []
            neighbours: Counter[int] = Counter()
            while queue:
                y, x = queue.popleft()
                cells.append((y, x))
                for ny, nx in ((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)):
                    if not (0 <= ny < kind_map.shape[0] and 0 <= nx < kind_map.shape[1]):
                        continue
                    if kind_map[ny, nx] == class_id:
                        if not seen[ny, nx]:
                            seen[ny, nx] = True
                            queue.append((ny, nx))
                    else:
                        neighbours[int(kind_map[ny, nx])] += 1
            protected = class_id == KIND_CODE["land"] and any(
                cell in protected_land for cell in cells
            )
            enclosed_land = (
                class_id == KIND_CODE["land"]
                and neighbours[KIND_CODE["sea"]] == 0
                and not protected
            )
            # Never absorb a source-coast water inlet merely because it is
            # sub-location-sized. Doing so creates passable political pixels
            # at the 420-unit water datum and visibly blunts the audited coast.
            too_small = len(cells) < minimum and class_id != KIND_CODE["sea"]
            if (too_small or enclosed_land) and neighbours:
                replacement = neighbours.most_common(1)[0][0]
                for y, x in cells:
                    kind_map[y, x] = replacement


def choose_seeds(
    mask: np.ndarray,
    count: int,
    weight: np.ndarray,
    rng: np.random.Generator,
    pinned: list[tuple[int, int]],
    radius: int,
) -> list[tuple[int, int]]:
    if int(mask.sum()) < count:
        raise ValueError(f"only {int(mask.sum())} cells exist for {count} seeds")
    chosen = list(dict.fromkeys(pinned))
    occupied = np.zeros(mask.shape, dtype=bool)

    def block(y: int, x: int, distance: int) -> None:
        occupied[
            max(0, y - distance) : min(mask.shape[0], y + distance + 1),
            max(0, x - distance) : min(mask.shape[1], x + distance + 1),
        ] = True

    for y, x in chosen:
        if not mask[y, x]:
            raise ValueError(f"pinned seed {(y, x)} lies outside its class")
        block(y, x, radius)

    coords = np.argwhere(mask)
    local_weight = np.maximum(weight[mask].astype(np.float64), 1.0)
    scores = rng.random(len(coords)) / np.square(local_weight / 255.0 + 0.22)
    for candidate_index in np.argsort(scores, kind="stable"):
        if len(chosen) >= count:
            break
        y, x = (int(value) for value in coords[candidate_index])
        if occupied[y, x]:
            continue
        chosen.append((y, x))
        block(y, x, radius)

    # Highly fragmented masks can exhaust a conservative exclusion radius.
    # Relax one pixel at a time while retaining all already accepted seeds.
    for relaxed in range(radius - 1, -1, -1):
        if len(chosen) >= count:
            break
        occupied.fill(False)
        for y, x in chosen:
            block(y, x, relaxed)
        for candidate_index in np.argsort(scores, kind="stable"):
            if len(chosen) >= count:
                break
            y, x = (int(value) for value in coords[candidate_index])
            if occupied[y, x] or (y, x) in chosen:
                continue
            chosen.append((y, x))
            block(y, x, relaxed)
    if len(chosen) != count:
        raise ValueError(f"selected {len(chosen)} of {count} requested seeds")
    return chosen


def cover_components(
    mask: np.ndarray,
    pinned: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """Guarantee at least one seed in every four-connected class component."""
    required = list(dict.fromkeys(pinned))
    pinned_set = set(required)
    seen = np.zeros(mask.shape, dtype=bool)
    for start_y, start_x in np.argwhere(mask):
        start = (int(start_y), int(start_x))
        if seen[start]:
            continue
        queue: deque[tuple[int, int]] = deque([start])
        seen[start] = True
        representative = start
        covered = start in pinned_set
        while queue:
            y, x = queue.popleft()
            if (y, x) in pinned_set:
                covered = True
            for ny, nx in ((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)):
                if (
                    0 <= ny < mask.shape[0]
                    and 0 <= nx < mask.shape[1]
                    and mask[ny, nx]
                    and not seen[ny, nx]
                ):
                    seen[ny, nx] = True
                    queue.append((ny, nx))
        if not covered:
            required.append(representative)
    return required


def grow_labels(
    kind_map: np.ndarray,
    seeds_by_kind: dict[str, list[tuple[int, int]]],
    offsets: dict[str, int],
) -> np.ndarray:
    """Grow connected, organic location cells inside each authored map class.

    A four-neighbour flood produces a Manhattan-distance Voronoi diagram.  At
    ENDÓRË's density those diamond wavefronts become long parallel bands when
    EU5 renders location borders.  Cardinal edges remain universally available
    for connectivity, while a deterministic half of the diagonal graph is
    opened and the visit order rotates spatially.  The result retains the
    linear-time flood and connected seed ownership, but breaks the axis-aligned
    wavefronts into compact, irregular cells.
    """
    labels = np.full(kind_map.shape, -1, dtype=np.int32)
    queue: deque[tuple[int, int]] = deque()
    neighbour_orders = (
        (
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
        ),
        (
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
        ),
        (
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
        ),
        (
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
        ),
    )
    for kind in KIND_ORDER:
        expected = KIND_CODE[kind]
        for local_index, (y, x) in enumerate(seeds_by_kind[kind]):
            if kind_map[y, x] != expected:
                raise ValueError(f"{kind} seed {(y, x)} has class {kind_map[y, x]}")
            labels[y, x] = offsets[kind] + local_index
            queue.append((y, x))
    while queue:
        y, x = queue.popleft()
        label = labels[y, x]
        expected = kind_map[y, x]
        phase = ((x * 73) ^ (y * 151) ^ SEED) & 3
        for dy, dx in neighbour_orders[phase]:
            ny, nx = y + dy, x + dx
            if dy and dx:
                edge_y, edge_x = min(y, ny), min(x, nx)
                edge_hash = (
                    (edge_x * 73_856_093)
                    ^ (edge_y * 19_349_663)
                    ^ SEED
                )
                if (edge_hash & 3) >= 2:
                    continue
            if (
                0 <= ny < CONTROL_H
                and 0 <= nx < CONTROL_W
                and labels[ny, nx] < 0
                and kind_map[ny, nx] == expected
            ):
                labels[ny, nx] = label
                queue.append((ny, nx))
    if np.any(labels < 0):
        counts = Counter(int(value) for value in kind_map[labels < 0])
        raise ValueError(f"unfilled control cells by class: {dict(counts)}")
    return labels


@lru_cache(maxsize=1)
def build_model() -> WorldModel:
    biomes = control_array("biomes.png").astype(np.uint8)
    density = control_array("density.png").astype(np.uint8)
    anchors = load_anchors()
    kind_map, pinned = kind_masks(biomes, anchors)
    rng = np.random.default_rng(SEED)

    masks = {
        kind: kind_map == KIND_CODE[kind]
        for kind in KIND_ORDER
    }
    seeds_by_kind: dict[str, list[tuple[int, int]]] = {}
    land_pins = cover_components(
        masks["land"],
        [pinned[anchor.key] for anchor in anchors],
    )
    seeds_by_kind["land"] = choose_seeds(
        masks["land"],
        TARGETS["land"],
        density,
        rng,
        land_pins,
        radius=10,
    )
    seeds_by_kind["mountain"] = choose_seeds(
        masks["mountain"],
        TARGETS["mountain"],
        np.full_like(density, 128),
        rng,
        cover_components(masks["mountain"], []),
        radius=10,
    )
    seeds_by_kind["lake"] = choose_seeds(
        masks["lake"],
        TARGETS["lake"],
        np.full_like(density, 128),
        rng,
        cover_components(masks["lake"], []),
        radius=20,
    )
    seeds_by_kind["sea"] = choose_seeds(
        masks["sea"],
        TARGETS["sea"],
        np.full_like(density, 128),
        rng,
        cover_components(masks["sea"], []),
        radius=40,
    )

    offsets: dict[str, int] = {}
    running = 0
    for kind in KIND_ORDER:
        offsets[kind] = running
        running += len(seeds_by_kind[kind])
    labels = grow_labels(kind_map, seeds_by_kind, offsets)
    areas = np.bincount(labels.ravel(), minlength=running)

    anchor_by_cell = {
        pinned[anchor.key]: anchor
        for anchor in anchors
    }
    generated_numbers = Counter()
    colors = location_colors(running)
    vanilla_names = installed_named_registry()[1]
    locations: list[Location] = []
    for kind in KIND_ORDER:
        for y, x in seeds_by_kind[kind]:
            index = len(locations)
            anchor = anchor_by_cell.get((y, x)) if kind == "land" else None
            if anchor:
                key = (
                    f"me_{anchor.key}"
                    if anchor.key in vanilla_names
                    else anchor.key
                )
                display_name = anchor.name
            else:
                generated_numbers[kind] += 1
                key = f"me_{kind}_{generated_numbers[kind]:04d}"
                key = LOCALIZATION_COLLISION_RENAMES.get(key, key)
                display_name = f"{kind.title()} {generated_numbers[kind]:04d}"
            nx, ny = x / (CONTROL_W - 1), y / (CONTROL_H - 1)
            continent, region = spatial_group(nx, ny)
            locations.append(
                Location(
                    index=index,
                    key=key,
                    display_name=display_name,
                    kind=kind,
                    x=x,
                    y=y,
                    biome_id=int(biomes[y, x]),
                    continent=continent,
                    region=region,
                    color=colors[index],
                    anchor=anchor is not None,
                )
            )

    if len({location.key for location in locations}) != len(locations):
        raise ValueError("duplicate generated location key")
    if len({location.color for location in locations}) != len(locations):
        raise ValueError("duplicate generated location color")
    if np.any(areas == 0):
        raise ValueError("one or more generated locations owns no control cells")
    return WorldModel(labels, kind_map, biomes, density, locations, areas)


def model_manifest(model: WorldModel) -> dict:
    counts = Counter(location.kind for location in model.locations)
    by_continent = Counter(location.continent for location in model.locations)
    model_digest = hashlib.sha256()
    model_digest.update(model.labels.astype("<i4", copy=False).tobytes())
    for location in model.locations:
        model_digest.update(
            (
                f"{location.index}|{location.key}|{location.kind}|{location.x}|"
                f"{location.y}|{location.biome_id}|{location.continent}|"
                f"{location.region}|{location.color}\n"
            ).encode("utf-8")
        )
    return {
        "schema": 1,
        "seed": SEED,
        "control_resolution": [CONTROL_W, CONTROL_H],
        "world_resolution": [WORLD_W, WORLD_H],
        "height_resolution": [HEIGHT_W, HEIGHT_H],
        "biome_resolution": [BIOME_W, BIOME_H],
        "location_count": len(model.locations),
        "kind_counts": dict(sorted(counts.items())),
        "passable_land_locations": counts["land"],
        "anchor_locations": sum(location.anchor for location in model.locations),
        "continent_counts": dict(sorted(by_continent.items())),
        "minimum_control_area": int(model.areas.min()),
        "median_control_area": float(np.median(model.areas)),
        "maximum_control_area": int(model.areas.max()),
        "control_source_sha256": source_sha256(),
        "model_sha256": model_digest.hexdigest(),
    }


def coastal_edges(
    model: WorldModel,
    water_kinds: tuple[str, ...] = ("sea",),
) -> dict[int, dict[int, tuple[int, int, int, int]]]:
    """Return land -> water -> representative control-grid boundary edge."""
    result: dict[int, dict[int, tuple[int, int, int, int]]] = {}
    kind_by_label = [location.kind for location in model.locations]
    for y in range(CONTROL_H):
        for x in range(CONTROL_W):
            land_label = int(model.labels[y, x])
            if kind_by_label[land_label] != "land":
                continue
            for wy, wx in ((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)):
                if not (0 <= wy < CONTROL_H and 0 <= wx < CONTROL_W):
                    continue
                water_label = int(model.labels[wy, wx])
                if kind_by_label[water_label] not in water_kinds:
                    continue
                result.setdefault(land_label, {}).setdefault(
                    water_label,
                    (y, x, wy, wx),
                )
    return result


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
