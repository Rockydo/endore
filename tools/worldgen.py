#!/usr/bin/env python3
"""Deterministic shared model for the M2 Middle-earth map generators.

The authored 1024x512 controls are the single source of truth.  This module
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

CONTROL_W, CONTROL_H = 1024, 512
WORLD_W, WORLD_H = 8192, 4096
HEIGHT_W, HEIGHT_H = 4096, 2048
BIOME_W, BIOME_H = HEIGHT_W - 1, HEIGHT_H - 1
SEED = 3018

TARGETS = {
    "land": 5200,
    "mountain": 260,
    "lake": 32,
    "sea": 320,
}

KIND_ORDER = ("land", "mountain", "lake", "sea")
KIND_CODE = {"sea": 0, "land": 1, "lake": 2, "mountain": 3}
LOCALIZATION_COLLISION_RENAMES = {
    # Live EU5 localization-table evidence from the first M2 smoke.
    "me_land_2436": "me_land_2436_endore",
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
    """Assign the logged M2 strategic hierarchy from normalized position."""
    if y < 0.235:
        if x < 0.38:
            return "me_forodwaith", "me_forochel_region"
        if x < 0.53:
            return "me_forodwaith", "me_angmar_region"
        return "me_forodwaith", "me_northern_wastes_region"
    if y > 0.83:
        if x < 0.53:
            return "me_harad", "me_umbar_region"
        if y < 0.94:
            return "me_harad", "me_near_harad_region"
        return "me_harad", "me_far_harad_region"
    if x > 0.665:
        if y < 0.57:
            return "me_mordor_and_rhun", "me_rhun_region"
        if y < 0.82:
            return "me_mordor_and_rhun", "me_mordor_region"
        return "me_mordor_and_rhun", "me_khand_region"
    if y > 0.655:
        if x < 0.46:
            return "me_gondor", "me_belfalas_region"
        if x < 0.58:
            return "me_gondor", "me_lebennin_region"
        if x > 0.62 and y < 0.79:
            return "me_gondor", "me_ithilien_region"
        if y < 0.78:
            return "me_gondor", "me_anorien_region"
        return "me_gondor", "me_south_gondor_region"
    if x >= 0.46:
        if y < 0.27:
            return "me_rhovanion", "me_grey_mountains_region"
        if x > 0.60 and y < 0.43:
            return "me_rhovanion", "me_dale_region"
        if x > 0.54 and y < 0.56:
            return "me_rhovanion", "me_mirkwood_region"
        if y > 0.59:
            return "me_rhovanion", "me_rohan_region"
        if x < 0.58:
            return "me_rhovanion", "me_anduin_vale_region"
        return "me_rhovanion", "me_brown_lands_region"
    if x < 0.32:
        return "me_eriador", "me_lindon_region"
    if y < 0.35:
        return "me_eriador", "me_north_arnor_region"
    if y < 0.49:
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
        # A pinned stronghold or pass is a playable location even where its
        # exact control pixel intersects a ridge.
        for ny in range(max(0, y - 1), min(CONTROL_H, y + 2)):
            for nx in range(max(0, x - 1), min(CONTROL_W, x + 2)):
                if kind_map[ny, nx] == KIND_CODE["mountain"]:
                    kind_map[ny, nx] = KIND_CODE["land"]
    clean_small_components(kind_map, minimum=4)
    return kind_map, pinned


def clean_small_components(kind_map: np.ndarray, minimum: int) -> None:
    """Absorb single-pixel control artifacts into their dominant neighbour."""
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
            if len(cells) < minimum and neighbours:
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
    labels = np.full(kind_map.shape, -1, dtype=np.int32)
    queue: deque[tuple[int, int]] = deque()
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
        for ny, nx in ((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)):
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
        radius=3,
    )
    seeds_by_kind["mountain"] = choose_seeds(
        masks["mountain"],
        TARGETS["mountain"],
        np.full_like(density, 128),
        rng,
        cover_components(masks["mountain"], []),
        radius=3,
    )
    seeds_by_kind["lake"] = choose_seeds(
        masks["lake"],
        TARGETS["lake"],
        np.full_like(density, 128),
        rng,
        cover_components(masks["lake"], []),
        radius=5,
    )
    seeds_by_kind["sea"] = choose_seeds(
        masks["sea"],
        TARGETS["sea"],
        np.full_like(density, 128),
        rng,
        cover_components(masks["sea"], []),
        radius=10,
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
