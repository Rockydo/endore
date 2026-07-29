#!/usr/bin/env python3
"""Generate/check the throwaway M1 Proof-of-Arda map.

The spike keeps exactly 300 installed location keys and colors, reassigning
their geometry on a coarse grid into an Arda-shaped landmass. M2 replaces this
entire layer with the real generator chain and Middle-earth hierarchy.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import shutil
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "in_game/map_data"
START_OUT = ROOT / "main_menu/setup/start"
SCENARIO_OUT = ROOT / "main_menu/common/scenarios"
TEST_OUT = ROOT / "in_game/common/tests"
TRAIT_OUT = ROOT / "in_game/common/traits"
LOC_OUT = ROOT / "in_game/localization/english"
GRID_W, GRID_H = 512, 256
WORLD_W, WORLD_H = 16384, 8192
SEED = 3018
TARGET_COUNTS = {0: 50, 1: 190, 2: 10, 3: 20, 4: 30}


def game_map() -> Path:
    config = json.loads((ROOT / "config/local_paths.json").read_text(encoding="utf-8-sig"))
    return Path(config["game_dir"]) / "game/in_game/map_data"


def strip_comments(text: str) -> str:
    return re.sub(r"#.*", "", text)


def hierarchy_keys(text: str) -> list[list[str]]:
    """Return definition keys by continent/subcontinent/region/area/province depth."""
    levels: list[list[str]] = [[] for _ in range(5)]
    depth = 0
    token_re = re.compile(r"([A-Za-z0-9_]+)\s*=\s*\{|\}")
    for match in token_re.finditer(strip_comments(text)):
        key = match.group(1)
        if key is not None:
            if depth < len(levels):
                levels[depth].append(key)
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                raise ValueError("installed definitions close before opening")
    if depth:
        raise ValueError(f"installed definitions end at brace depth {depth}")
    return levels


OVERLAY_MARKER = "# Generated M1 geography compatibility overlay; replaced wholesale by M2.\n"


def write_generated_script_overlays(
    installed_game: Path,
    installed_definitions: str,
) -> list[str]:
    """Retarget installed geography references onto the temporary Arda hierarchy.

    M1 deliberately has only 300 raster locations. Retail EU5 still parses hundreds
    of otherwise useful vanilla definitions that mention Earth geography, so exact
    file overlays preserve those definitions while replacing only geography tokens.
    M2 removes this compatibility layer as it quarantines each system deliberately.
    """
    manifest_path = OUT / "m1_script_overlay_manifest.json"
    previous: set[str] = set()
    if manifest_path.is_file():
        previous = set(json.loads(manifest_path.read_text(encoding="utf-8-sig")))

    for relative in previous:
        target = (
            ROOT / relative
            if relative.startswith(("in_game/", "main_menu/", "loading_screen/"))
            else ROOT / "in_game" / relative
        )
        if target.is_file() and target.read_text(
            encoding="utf-8-sig", errors="replace"
        ).startswith(OVERLAY_MARKER):
            target.unlink()

    replacements: dict[str, str] = {}
    standins = (
        "middle_earth",
        "endore_subcontinent",
        "endore_region",
        "endore_area",
        "endore_province_001",
    )
    installed_locations = {
        name
        for name, _ in named_colors(
            installed_game
            / "in_game/map_data/named_locations/00_default.txt"
        )
    }
    for depth, keys in enumerate(hierarchy_keys(installed_definitions)):
        for key in keys:
            # Geography keys occasionally collide across hierarchy levels or
            # with a location key. Prefer the broadest valid geography object,
            # and leave genuine location tokens untouched.
            if key not in installed_locations:
                replacements.setdefault(key, standins[depth])
    # Two installed keys are legal at more than one hierarchy depth.
    replacements["eastern_baltic_sea"] = "endore_area"
    replacements["limousin_province"] = "endore_province_001"
    token_re = re.compile(r"\b[A-Za-z0-9_]+\b")

    written: list[str] = []
    for tree in ("in_game", "main_menu", "loading_screen"):
        installed_tree = installed_game / tree
        for source_path in sorted(installed_tree.rglob("*.txt")):
            relative_in_tree = source_path.relative_to(installed_tree).as_posix()
            if tree == "in_game" and relative_in_tree.startswith("map_data/"):
                continue
            if tree == "loading_screen" and relative_in_tree.startswith("sound/"):
                # Sound-bank text indexes contain coincidental identifier words;
                # they are not scripts and the project adds no audio.
                continue
            source_text = source_path.read_text(encoding="utf-8-sig", errors="strict")
            rewritten = token_re.sub(
                lambda match: replacements.get(match.group(0), match.group(0)),
                source_text,
            )
            if (
                tree == "in_game"
                and relative_in_tree.startswith("common/scripted_geography/")
            ):
                for block_name, standin in (
                    ("location", "liljendal"),
                    ("province_definition", "endore_province_001"),
                    ("area", "endore_area"),
                    ("region", "endore_region"),
                    ("subcontinent", "endore_subcontinent"),
                    ("continent", "middle_earth"),
                ):
                    rewritten = re.sub(
                        rf"(?ms)(^\s*{block_name}\s*=\s*\{{\s*$).*?(^\s*\}}\s*$)",
                        rf"\1\n\t\t{standin}\n\2",
                        rewritten,
                    )
            if rewritten == source_text:
                continue
            relative = f"{tree}/{relative_in_tree}"
            target = ROOT / relative
            if target.is_file() and not target.read_text(
                encoding="utf-8-sig", errors="replace"
            ).startswith(OVERLAY_MARKER):
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(OVERLAY_MARKER + rewritten, encoding="utf-8-sig")
            written.append(relative)

    manifest_path.write_text(
        json.dumps(written, indent=2) + "\n",
        encoding="utf-8",
    )
    return written


def section(text: str, name: str) -> set[str]:
    clean = strip_comments(text)
    match = re.search(rf"\b{re.escape(name)}\s*=\s*\{{", clean)
    if not match:
        return set()
    start = match.end()
    depth = 1
    index = start
    while index < len(clean) and depth:
        if clean[index] == "{":
            depth += 1
        elif clean[index] == "}":
            depth -= 1
        index += 1
    if depth:
        raise ValueError(f"unterminated {name} section")
    return set(re.findall(r"\b[A-Za-z0-9_]+\b", clean[start : index - 1]))


def empty_section(text: str, name: str) -> str:
    """Replace one top-level braced map classification with an empty block."""
    match = re.search(rf"(?m)^\s*{re.escape(name)}\s*=\s*\{{", text)
    if not match:
        raise ValueError(f"missing {name} section")
    depth = 1
    index = match.end()
    while index < len(text) and depth:
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
        index += 1
    if depth:
        raise ValueError(f"unterminated {name} section")
    return text[: match.start()] + f"{name} = {{\n}}\n" + text[index:]


def replace_section(text: str, name: str, keys: list[str]) -> str:
    """Replace one top-level braced map classification with selected keys."""
    match = re.search(rf"(?m)^\s*{re.escape(name)}\s*=\s*\{{", text)
    if not match:
        raise ValueError(f"missing {name} section")
    depth = 1
    index = match.end()
    while index < len(text) and depth:
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
        index += 1
    if depth:
        raise ValueError(f"unterminated {name} section")
    body = "\n\t" + " ".join(keys) + "\n" if keys else "\n"
    return text[: match.start()] + f"{name} = {{{body}}}\n" + text[index:]


def named_colors(path: Path) -> list[tuple[str, tuple[int, int, int]]]:
    result: list[tuple[str, tuple[int, int, int]]] = []
    pattern = re.compile(r"^\s*([A-Za-z0-9_]+)\s*=\s*([0-9a-fA-F]{1,6})\s*(?:#.*)?$")
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = pattern.match(line)
        if not match:
            continue
        value = int(match.group(2), 16)
        result.append((match.group(1), ((value >> 16) & 255, (value >> 8) & 255, value & 255)))
    if len(result) < 25_000:
        raise ValueError(f"unexpected named-location count: {len(result)}")
    if len({name for name, _ in result}) != len(result):
        raise ValueError("duplicate named-location key")
    if len({color for _, color in result}) != len(result):
        raise ValueError("duplicate named-location color")
    return result


def proof_classes() -> np.ndarray:
    image = Image.new("L", (GRID_W, GRID_H), 0)
    draw = ImageDraw.Draw(image)
    p = lambda x, y: (round(x * (GRID_W - 1)), round(y * (GRID_H - 1)))

    # Belegaer-facing north-western Middle-earth, deliberately schematic.
    coast = [
        p(.24, .06), p(.45, .03), p(.66, .08), p(.83, .20), p(.88, .42),
        p(.86, .72), p(.80, .92), p(.62, .98), p(.42, .96), p(.34, .90),
        p(.36, .82), p(.32, .76), p(.39, .69), p(.33, .64), p(.25, .60),
        p(.28, .52), p(.21, .46), p(.26, .39), p(.20, .32), p(.23, .22),
        p(.20, .13),
    ]
    draw.polygon(coast, fill=1)

    # Icebay of Forochel and the deep Bay of Belfalas.
    draw.polygon([p(.20, .13), p(.31, .12), p(.27, .22), p(.20, .24)], fill=0)
    draw.polygon([p(.25, .64), p(.46, .72), p(.37, .79), p(.31, .76)], fill=0)

    # Inland seas: Rhûn, Núrnen, Evendim.
    for box in ((.69, .40, .79, .50), (.65, .74, .72, .79), (.29, .28, .315, .32)):
        draw.ellipse([p(box[0], box[1]), p(box[2], box[3])], fill=2)

    # Mountain systems: Grey/Misty/White Mountains and Mordor's enclosing walls.
    mountain_lines = [
        ([p(.43, .10), p(.47, .28), p(.46, .47), p(.48, .61)], 11),
        ([p(.43, .13), p(.61, .15), p(.73, .19)], 10),
        ([p(.39, .66), p(.53, .69), p(.65, .72)], 11),
        ([p(.65, .61), p(.77, .61), p(.79, .76), p(.70, .82), p(.65, .72), p(.65, .61)], 10),
    ]
    for points, width in mountain_lines:
        draw.line(points, fill=3, width=width, joint="curve")
    # Keep explicit strategic gaps through the temporary impassable ranges.
    for box in (
        (.445, .31, .475, .35),
        (.455, .52, .485, .56),
        (.485, .675, .525, .705),
        (.635, .625, .675, .655),
        (.765, .685, .795, .725),
    ):
        draw.ellipse([p(box[0], box[1]), p(box[2], box[3])], fill=1)

    # Mirkwood, Fangorn, the Old Forest and the forests of Ithilien.
    for box in ((.54, .27, .66, .51), (.46, .56, .52, .65), (.30, .39, .36, .47), (.59, .63, .64, .73)):
        draw.ellipse([p(box[0], box[1]), p(box[2], box[3])], fill=4)

    return np.asarray(image, dtype=np.uint8)


def components(mask: np.ndarray) -> list[tuple[int, int]]:
    seen = np.zeros(mask.shape, dtype=bool)
    starts: list[tuple[int, int]] = []
    for y, x in zip(*np.where(mask)):
        if seen[y, x]:
            continue
        starts.append((int(y), int(x)))
        queue = deque([(int(y), int(x))])
        seen[y, x] = True
        while queue:
            cy, cx = queue.popleft()
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < GRID_H and 0 <= nx < GRID_W and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    queue.append((ny, nx))
    return starts


def partition(grid: np.ndarray, class_id: int, keys: list[str], rng: random.Random) -> dict[str, list[tuple[int, int]]]:
    mask = grid == class_id
    cells = [(int(y), int(x)) for y, x in zip(*np.where(mask))]
    if len(cells) < len(keys):
        raise ValueError(f"class {class_id} has {len(cells)} cells for {len(keys)} keys")
    starts = components(mask)
    if len(starts) > len(keys):
        raise ValueError(f"class {class_id} has more components than keys")
    pool = [cell for cell in cells if cell not in set(starts)]
    rng.shuffle(pool)
    seeds = starts + pool[: len(keys) - len(starts)]

    labels = np.full(grid.shape, -1, dtype=np.int32)
    queue: deque[tuple[int, int]] = deque()
    for label, (y, x) in enumerate(seeds):
        labels[y, x] = label
        queue.append((y, x))
    while queue:
        y, x = queue.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < GRID_H and 0 <= nx < GRID_W and mask[ny, nx] and labels[ny, nx] < 0:
                labels[ny, nx] = labels[y, x]
                queue.append((ny, nx))
    result = {key: [] for key in keys}
    for y, x in cells:
        result[keys[int(labels[y, x])]].append((y, x))
    return result


def write() -> None:
    source = game_map()
    OUT.mkdir(parents=True, exist_ok=True)
    names = named_colors(source / "named_locations/00_default.txt")
    # The named-color registry contains nine dormant entries which vanilla does
    # not paint or place in definitions. Painting them creates hard map-index
    # failures, so derive the active registry from the installed raster.
    source_colors = {
        color
        for _, color in (Image.open(source / "locations.png").getcolors(maxcolors=30_000) or [])
    }
    source_order = [name for name, color in names if color in source_colors]
    colors = dict(names)
    default_text = (source / "default.map").read_text(encoding="utf-8-sig")
    sea = section(default_text, "sea_zones")
    lakes = section(default_text, "lakes")
    mountains = section(default_text, "impassable_mountains")
    all_names = set(source_order)
    mountains &= all_names
    sea &= all_names
    lakes &= all_names
    mountains -= sea | lakes
    regular = all_names - sea - lakes - mountains

    grid = proof_classes()
    source_groups = {
        0: [name for name in source_order if name in sea],
        2: [name for name in source_order if name in lakes],
        3: [name for name in source_order if name in mountains],
    }
    regular_order = [name for name in source_order if name in regular]
    source_groups[4] = regular_order[: TARGET_COUNTS[4]]
    source_groups[1] = regular_order[
        TARGET_COUNTS[4] : TARGET_COUNTS[4] + TARGET_COUNTS[1]
    ]
    groups = {
        class_id: source_groups[class_id][: TARGET_COUNTS[class_id]]
        for class_id in range(5)
    }
    selected = {name for keys in groups.values() for name in keys}
    order = [name for name in source_order if name in selected]
    if len(order) != sum(TARGET_COUNTS.values()):
        raise ValueError(f"could not select {sum(TARGET_COUNTS.values())} proof locations")
    rng = random.Random(SEED)
    assignments: dict[str, list[tuple[int, int]]] = {}
    for class_id, keys in groups.items():
        assignments.update(partition(grid, class_id, keys, rng))

    coarse = np.zeros((GRID_H, GRID_W, 3), dtype=np.uint8)
    key_grid = np.empty((GRID_H, GRID_W), dtype=object)
    key_class: dict[str, int] = {}
    for class_id, keys in groups.items():
        for key in keys:
            key_class[key] = class_id
            color = colors[key]
            for y, x in assignments[key]:
                coarse[y, x] = color
                key_grid[y, x] = key

    # The temporary proof retains thousands of vanilla sea keys. Randomly
    # partitioning them along a short Middle-earth coastline can create more
    # coastal sea zones than unique land endpoints, while EU5 permits only one
    # port per land location. Consolidate the shoreline under one sea key and
    # keep every displaced key alive on an interior ocean cell. M2 replaces this
    # deliberately crude device with authored sea zones.
    coastal_cells: set[tuple[int, int]] = set()
    for y in range(GRID_H):
        for x in range(GRID_W):
            if grid[y, x] != 0:
                continue
            if any(
                0 <= sy < GRID_H
                and 0 <= sx < GRID_W
                and grid[sy, sx] not in (0, 2, 3)
                for sy, sx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1))
            ):
                coastal_cells.add((y, x))
    coast_key = groups[0][0]
    for cell in coastal_cells:
        old_key = str(key_grid[cell])
        if old_key == coast_key:
            continue
        assignments[old_key].remove(cell)
        assignments[coast_key].append(cell)
        key_grid[cell] = coast_key
    for empty_key in (key for key in groups[0] if not assignments[key]):
        donor_key = next(
            key
            for key in groups[0]
            if any(cell not in coastal_cells for cell in assignments[key])
            and len(assignments[key]) > 1
        )
        donor_cell = next(cell for cell in assignments[donor_key] if cell not in coastal_cells)
        assignments[donor_key].remove(donor_cell)
        assignments[empty_key].append(donor_cell)
        key_grid[donor_cell] = empty_key
    for y in range(GRID_H):
        for x in range(GRID_W):
            coarse[y, x] = colors[str(key_grid[y, x])]

    locations = Image.fromarray(coarse, "RGB").resize((WORLD_W, WORLD_H), Image.Resampling.NEAREST)
    locations.save(OUT / "locations.png", compress_level=6)

    named_dir = OUT / "named_locations"
    named_dir.mkdir(parents=True, exist_ok=True)
    installed_definitions = (source / "definitions.txt").read_text(
        encoding="utf-8-sig"
    )
    definition_lines = [
        "middle_earth = {",
        "\tendore_subcontinent = {",
        "\t\tendore_region = {",
        "\t\t\tendore_area = {",
    ]
    for index in range(0, len(order), 10):
        definition_lines.append(
            f"\t\t\t\tendore_province_{index // 10 + 1:03d} = "
            f"{{ {' '.join(order[index:index + 10])} }}"
        )
    definition_lines.extend(("\t\t\t}", "\t\t}", "\t}", "}", ""))
    (OUT / "definitions.txt").write_text("\n".join(definition_lines), encoding="utf-8-sig")
    # nodes.dat is derived from geometry. A stale installed cache neither
    # prevents nor advances the reduced-world transition, so omit it.
    stale_nodes = OUT / "nodes.dat"
    if stale_nodes.exists():
        stale_nodes.unlink()
    # M1 needs the ranges to read as mountains without splitting the temporary
    # vanilla geography into hundreds of unreachable components. M2 restores
    # deliberate non-ownable/impassable classifications around authored passes.
    proof_default = default_text
    for section_name in (
        "sound_toll",
        "volcanoes",
        "earthquakes",
        "non_ownable",
    ):
        proof_default = empty_section(proof_default, section_name)
    proof_default = replace_section(proof_default, "sea_zones", groups[0])
    proof_default = replace_section(proof_default, "lakes", groups[2])
    proof_default = replace_section(proof_default, "impassable_mountains", groups[3])
    proof_default = re.sub(r"(?m)^(\s*wrap_x\s*=\s*)yes\b", r"\1no", proof_default)
    proof_default = "\n".join(line.split("#", 1)[0].rstrip() for line in proof_default.splitlines())
    (OUT / "default.map").write_text(proof_default, encoding="utf-8-sig")
    shutil.copy2(source / "named_locations/00_default.txt", named_dir / "00_default.txt")
    (OUT / "adjacencies.csv").write_text("", encoding="utf-8")
    (OUT / "generated_locators_port.txt").write_text(
        'game_object_locator={\n\tname="port"\n\tclamp_to_water_level=no\n'
        '\trender_under_water=no\n\tgenerated_content=no\n\tlayer=""\n\tinstances={\n\t}\n}\n',
        encoding="utf-8",
    )

    # Every raster-adjacent coastal land and sea location needs a connector.
    # Determine the coastline before emitting templates so harbor suitability is
    # assigned only to actual coastal land locations.
    coastal_land: dict[str, tuple[int, int, int, int]] = {}
    coastal_sea: dict[str, tuple[int, int, int, int]] = {}
    coast_edges_by_land: dict[str, dict[str, tuple[int, int, int, int]]] = {}
    coast_edges_by_sea: dict[str, dict[str, tuple[int, int, int, int]]] = {}
    for y in range(GRID_H):
        for x in range(GRID_W):
            if grid[y, x] in (0, 2, 3):
                continue
            for sy, sx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if 0 <= sy < GRID_H and 0 <= sx < GRID_W and grid[sy, sx] == 0:
                    land_key = str(key_grid[y, x])
                    sea_key = str(key_grid[sy, sx])
                    edge = (y, x, sy, sx)
                    coastal_land.setdefault(land_key, edge)
                    coastal_sea.setdefault(sea_key, edge)
                    coast_edges_by_land.setdefault(land_key, {}).setdefault(sea_key, edge)
                    coast_edges_by_sea.setdefault(sea_key, {}).setdefault(land_key, edge)

    lines = ["# Generated by tools/m1_proof_map.py --write; throwaway M1 terrain scaffold."]
    templates = {
        0: "topography = ocean climate = oceanic",
        1: "topography = flatland vegetation = grasslands climate = continental religion = catholic culture = swedish raw_material = wheat",
        2: "topography = lakes climate = continental",
        3: "topography = mountains vegetation = grasslands climate = continental",
        4: "topography = flatland vegetation = forest climate = continental religion = catholic culture = swedish raw_material = lumber",
    }
    for name in order:
        harbor = " natural_harbor_suitability = 0.50" if name in coastal_land else ""
        lines.append(f"{name} = {{ {templates[key_class[name]]}{harbor} }}")
    (OUT / "location_templates.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    scale_x, scale_y = WORLD_W // GRID_W, WORLD_H // GRID_H

    def port_line(edge: tuple[int, int, int, int]) -> str:
        y, x, sy, sx = edge
        land_key, sea_key = str(key_grid[y, x]), str(key_grid[sy, sx])
        if sy == y:
            px = sx * scale_x if sx > x else (sx + 1) * scale_x - 1
            py = y * scale_y + scale_y // 2
        else:
            px = x * scale_x + scale_x // 2
            py = sy * scale_y if sy > y else (sy + 1) * scale_y - 1
        return f"{land_key};{sea_key};{px};{WORLD_H - py};x"

    # EU5 accepts many land ports into one sea zone, but only one port per land
    # location. Match every coastal sea to a unique adjacent land first, then
    # attach each remaining coastal land to any adjacent sea.
    land_match: dict[str, str] = {}

    def match_sea(sea_key: str, visited: set[str]) -> bool:
        for land_key in sorted(coast_edges_by_sea[sea_key]):
            if land_key in visited:
                continue
            visited.add(land_key)
            previous = land_match.get(land_key)
            if previous is None or match_sea(previous, visited):
                land_match[land_key] = sea_key
                return True
        return False

    unmatched_seas = [
        sea_key
        for sea_key in sorted(coast_edges_by_sea)
        if not match_sea(sea_key, set())
    ]
    if unmatched_seas:
        raise ValueError(f"could not assign unique land ports for {unmatched_seas[:5]}")

    port_edges: list[tuple[int, int, int, int]] = []
    for land_key in coastal_land:
        sea_key = land_match.get(land_key)
        if sea_key is None:
            sea_key = next(iter(coast_edges_by_land[land_key]))
        port_edges.append(coast_edges_by_land[land_key][sea_key])
    (OUT / "ports.csv").write_text(
        "\n".join(["LandProvince;SeaZone;x;y;", *(port_line(edge) for edge in port_edges)]),
        encoding="utf-8",
    )

    # Indexed river image: 254 sea, 255 land. M2 adds the proper river graph.
    vanilla_rivers = Image.open(source / "rivers.png")
    palette = vanilla_rivers.getpalette()
    full_class = Image.fromarray(grid, "L").resize((WORLD_W, WORLD_H), Image.Resampling.NEAREST)
    rivers = Image.new("P", (WORLD_W, WORLD_H), 255)
    rivers.putpalette(palette)
    water = np.isin(np.asarray(full_class), (0, 2))
    river_array = np.asarray(rivers).copy()
    river_array[water] = 254
    rivers = Image.fromarray(river_array, "P")
    rivers.putpalette(palette)
    rivers.save(OUT / "rivers.png", compress_level=6)

    # Vanilla locators become spatially stale when colors move. Centroids are
    # sufficient for the proof and can be emitted without the interactive editor.
    locator_dir = ROOT / "in_game/gfx/map/map_objects"
    locator_dir.mkdir(parents=True, exist_ok=True)
    def locator_text(kind: str, keys: list[str]) -> str:
        body = [
            "game_object_locator={",
            f'\tname="{kind}"',
            "\tclamp_to_water_level=no",
            "\trender_under_water=no",
            "\tgenerated_content=no",
            '\tlayer=""',
            "\tinstances={",
        ]
        for key in keys:
            cells = assignments[key]
            # A region centroid can fall outside a concave or disconnected
            # location and is then rejected as missing. A real member cell is a
            # guaranteed-valid proof locator.
            cy, cx = cells[0]
            x = (cx + 0.5) * WORLD_W / GRID_W
            z = WORLD_H - (cy + 0.5) * WORLD_H / GRID_H
            body.extend(
                (
                    "\t\t{",
                    f"\t\t\tid={key}",
                    f"\t\t\tposition={{ {x:.6f} 0.000000 {z:.6f} }}",
                    "\t\t\trotation={ 0.000000 0.000000 0.000000 1.000000 }",
                    "\t\t\tscale={ 1.000000 1.000000 1.000000 }",
                    "\t\t}",
                )
            )
        body.extend(("\t}", "}", ""))
        return "\n".join(body)

    vanilla_locator_dir = source.parent / "gfx/map/map_objects"

    def installed_locator_ids(kind: str) -> list[str]:
        text = (vanilla_locator_dir / f"generated_map_object_locators_{kind}.txt").read_text(
            encoding="utf-8-sig"
        )
        return [
            key
            for key in re.findall(r"(?m)^\s*id=([A-Za-z0-9_]+)\s*$", text)
            if key in assignments
        ]

    locator_keys = {
        "city": installed_locator_ids("city"),
        # The engine generator requires all locations except impassable
        # mountains. This deliberately includes the one key reclassified from
        # installed wasteland to M1 open sea.
        "combat": [key for key in order if key not in groups[3]],
        "unit_stack": [key for key in order if key not in groups[3]],
        "vfx": installed_locator_ids("vfx"),
        "dock": list(coastal_land),
    }
    for kind in ("city", "combat", "unit_stack", "vfx", "dock"):
        (locator_dir / f"generated_map_object_locators_{kind}.txt").write_text(
            locator_text(kind, locator_keys[kind]), encoding="utf-8"
        )
    (locator_dir / "generated_map_object_locators_volcano_eruption.txt").write_text(
        locator_text("volcano_eruption", []), encoding="utf-8"
    )
    dynamic_source = (vanilla_locator_dir / "dynamic_game_objects.txt").read_text(
        encoding="utf-8-sig"
    )
    dynamic_without_volcanoes = dynamic_source.split(
        'dynamic_game_object = {\n\tname = "volcano_eruption"'
    )[0]
    (locator_dir / "dynamic_game_objects.txt").write_text(
        dynamic_without_volcanoes, encoding="utf-8-sig"
    )
    override_dir = ROOT / "in_game/gfx/map/locators_override"
    override_dir.mkdir(parents=True, exist_ok=True)
    (override_dir / "locators_override.txt").write_text(
        "# M1 proof map: vanilla coordinate overrides are intentionally neutralized.\n",
        encoding="utf-8-sig",
    )
    holy_site_out = ROOT / "in_game/common/holy_sites"
    holy_site_out.mkdir(parents=True, exist_ok=True)
    installed_holy_sites = source.parent / "common/holy_sites"
    for installed_file in installed_holy_sites.glob("*.txt"):
        (holy_site_out / installed_file.name).write_text(
            "# M1 proof map: vanilla location-bound holy sites are quarantined.\n",
            encoding="utf-8-sig",
        )

    # The reshaped geometry invalidates vanilla roads, buildings, ownership and
    # other bookmark payload. Mirror the installed numbered start files with
    # neutral managers, then seed one inherited vanilla country at a passable
    # proof location. This is intentionally throwaway M1 scaffolding: it exists
    # only to enter the live map before M2 builds the real geography quarantine.
    target_y, target_x = round(GRID_H * 0.55), round(GRID_W * 0.55)
    anchor = min(
        (key for key in order if key_class[key] in (1, 4)),
        key=lambda key: min(
            (y - target_y) ** 2 + (x - target_x) ** 2 for y, x in assignments[key]
        ),
    )
    owned_locations = [key for key in order if key_class[key] in (1, 4)]
    START_OUT.mkdir(parents=True, exist_ok=True)
    start_files = {
        "02_core.txt": "institution_manager = {\n\tinstitutions = {\n\t}\n}\nreligion_manager = {\n}\n",
        "03_markets.txt": f"market_manager = {{\n\tadd_market = {anchor}\n}}\n",
        "04_dynasties.txt": "dynasty_manager = {\n}\n",
        "05_characters.txt": "character_db = {\n}\n",
        "06_pops.txt": (
            "locations = {\n"
            + "".join(
                f"\t{key} = {{ define_pop = "
                "{ type = peasants size = 1 culture = swedish religion = catholic } }\n"
                for key in owned_locations
            )
            + "}\n"
        ),
        "07_cities_and_buildings.txt": (
            "locations = {\n"
            f"\t{anchor} = {{ rank = town }}\n"
            "}\n"
            "building_manager = {\n}\n"
        ),
        "08_institutions.txt": "locations = {\n}\n",
        "09_roads.txt": "road_network = {\n}\n",
        "10_countries.txt": (
            "current_age = age_1_traditions\n"
            "countries = {\n"
            "\tcountries = {\n"
            "\t\tSWE = {\n"
            f"\t\t\town_control_core = {{ {' '.join(owned_locations)} }}\n"
            '\t\t\tinclude = "catholic_monarchy"\n'
            "\t\t\tcountry_rank = rank_county\n"
            f"\t\t\tcapital = {anchor}\n"
            "\t\t}\n"
            "\t}\n"
            "}\n"
        ),
        "11_art.txt": "work_of_art_manager = {\n}\n",
        "12_diplomacy.txt": "diplomacy_manager = {\n}\n",
        "13_religion.txt": "building_manager = {\n}\nreligion_manager = {\n}\n",
        "14_development.txt": "development = {\n\tbase = 0\n}\n",
        "15_international_organizations.txt": (
            "international_organization_manager = {\n"
            "\tadd_international_organization = {\n"
            "\t\ttype = hre\n"
            "\t\tcreation_date = 3018.1.1\n"
            "\t\tmap_color = hsv360 { 40 50 70 }\n"
            "\t\tmembers = { SWE }\n"
            "\t\tleader = SWE\n"
            "\t\temperor = { SWE }\n"
            "\t}\n"
            "}\n"
        ),
        "16_wars.txt": "war_manager = {\n}\n",
        "18_opinions.txt": "diplomacy_manager = {\n}\n",
        "19_diseases.txt": "disease_outbreak_manager = {\n}\n",
        "20_rivals.txt": "diplomacy_manager = {\n}\n",
        "21_locations.txt": "locations = {\n}\n",
        "22_situations.txt": "situation_manager = {\n}\n",
        "23_colonies.txt": "colony_manager = {\n}\n",
        "24_town_rights.txt": "townrights_manager = {\n}\n",
        "25_area_preferences.txt": "countries = {\n\tcountries = {\n\t}\n}\n",
        "26_ai_personalities.txt": "countries = {\n\tcountries = {\n\t}\n}\n",
        "27_armies.txt": "unit_manager = {\n}\n",
    }
    for name, text in start_files.items():
        (START_OUT / name).write_text(
            "# Generated by tools/m1_proof_map.py --write; throwaway M1 start scaffold.\n"
            + text,
            encoding="utf-8",
        )
    SCENARIO_OUT.mkdir(parents=True, exist_ok=True)
    (SCENARIO_OUT / "00_scenarios.txt").write_text(
        "# Generated by tools/m1_proof_map.py --write; throwaway M1 scenario.\n"
        "me_m1_proof_scenario = {\n"
        "\tcountry = SWE\n"
        "\tplayer_playstyle = ADMINISTRATIVE\n"
        "\tplayer_proficiency = NOVICE\n"
        "}\n",
        encoding="utf-8-sig",
    )
    TEST_OUT.mkdir(parents=True, exist_ok=True)
    installed_tests = source.parent / "common/tests"
    for installed_file in installed_tests.glob("*.txt"):
        if installed_file.name == "readme.txt":
            continue
        (TEST_OUT / installed_file.name).write_text(
            "# M1 proof map: vanilla geography-dependent runtime tests are quarantined.\n",
            encoding="utf-8-sig",
        )
    (TEST_OUT / "me_m1_proof.txt").write_text(
        "# Generated by tools/m1_proof_map.py --write; M1 runtime probe.\n"
        "me_m1_proof_map_test = {\n"
        # Tests are sampled on New Year's Day. The bookmark starts at 08:00 on
        # 1 January 3018, so the first complete annual sample is 3019.
        "\tyear = 3019\n"
        "\tsuccess = { always = yes }\n"
        "\tend_year = 3020\n"
        "\tfail_on_end_year = yes\n"
        "\tsuccess_effect = {\n"
        "\t\ttest_log = {\n"
        "\t\t\tname = me_m1_proof_map_test\n"
        '\t\t\ttext = "M1 Proof of Arda runtime test passed"\n'
        "\t\t}\n"
        "\t}\n"
        "}\n",
        encoding="utf-8-sig",
    )
    scripted_effect_out = ROOT / "in_game/common/scripted_effects"
    scripted_effect_out.mkdir(parents=True, exist_ok=True)
    (scripted_effect_out / "___test_effects.txt").write_text(
        "# M1 proof map: vanilla debug effects reference quarantined databases.\n",
        encoding="utf-8-sig",
    )
    debug_event_out = ROOT / "in_game/events/debug"
    debug_event_out.mkdir(parents=True, exist_ok=True)
    (debug_event_out / "000_johan_debug.txt").write_text(
        "# M1 proof map: retail developer-only events use unavailable debug effects.\n",
        encoding="utf-8-sig",
    )
    succession_source = (
        source.parent
        / "common/disasters/byzantine_succession_crisis.txt"
    ).read_text(encoding="utf-8-sig")
    succession_out = ROOT / "in_game/common/disasters"
    succession_out.mkdir(parents=True, exist_ok=True)
    (succession_out / "byzantine_succession_crisis.txt").write_text(
        succession_source.replace(
            "\t\tset_variable = succession_crisis_disaster_counter\n",
            "",
        ),
        encoding="utf-8-sig",
    )
    TRAIT_OUT.mkdir(parents=True, exist_ok=True)
    (TRAIT_OUT / "me_m1_immortality_probe.txt").write_text(
        "# Generated by tools/m1_proof_map.py --write; M1 engine-support probe.\n"
        "me_m1_immortality_probe = {\n"
        "\tallow = { }\n"
        "\tcategory = ruler\n"
        "\tmodifier = {\n"
        "\t\tis_immortal = yes\n"
        "\t}\n"
        "}\n",
        encoding="utf-8-sig",
    )
    LOC_OUT.mkdir(parents=True, exist_ok=True)
    localization_lines = [
        "l_english:",
        ' middle_earth: "Middle-earth"',
        ' endore_subcontinent: "Middle-earth"',
        ' endore_region: "Middle-earth"',
        ' endore_area: "Proof of Arda"',
        ' me_m1_immortality_probe: "Undying"',
        ' desc_me_m1_immortality_probe: "This M1 probe verifies native immortality support."',
        ' me_m1_immortality_probe_die_desc: "An immortal character cannot die naturally."',
    ]
    localization_lines.extend(
        f' endore_province_{index:03d}: "Proof Province {index}"'
        for index in range(1, 31)
    )
    (LOC_OUT / "m1_proof_l_english.yml").write_text(
        "\n".join(localization_lines) + "\n",
        encoding="utf-8-sig",
    )
    overlay_files = write_generated_script_overlays(source.parents[1], installed_definitions)

    manifest = {
        "world_size": [WORLD_W, WORLD_H],
        "grid_size": [GRID_W, GRID_H],
        "location_count": len(order),
        "classes": {str(class_id): len(keys) for class_id, keys in groups.items()},
        "ports": len(port_edges),
        "legacy_geography_keys": sum(
            len(level) for level in hierarchy_keys(installed_definitions)
        ),
        "compatibility_overlay_files": len(overlay_files),
        "anchor": anchor,
        "seed": SEED,
    }
    (OUT / "m1_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


def check() -> list[str]:
    failures: list[str] = []
    required = (
        "locations.png", "rivers.png", "definitions.txt", "default.map",
        "location_templates.txt", "ports.csv", "adjacencies.csv",
        "named_locations/00_default.txt", "m1_manifest.json",
    )
    for relative in required:
        if not (OUT / relative).is_file():
            failures.append(f"missing in_game/map_data/{relative}")
    if failures:
        return failures
    start_names = {
        "02_core.txt", "03_markets.txt", "04_dynasties.txt", "05_characters.txt",
        "06_pops.txt", "07_cities_and_buildings.txt", "08_institutions.txt",
        "09_roads.txt", "10_countries.txt", "11_art.txt", "12_diplomacy.txt",
        "13_religion.txt", "14_development.txt", "15_international_organizations.txt",
        "16_wars.txt", "18_opinions.txt", "19_diseases.txt", "20_rivals.txt",
        "21_locations.txt", "22_situations.txt", "23_colonies.txt",
        "24_town_rights.txt", "25_area_preferences.txt", "26_ai_personalities.txt",
        "27_armies.txt",
    }
    missing_start = sorted(name for name in start_names if not (START_OUT / name).is_file())
    if missing_start:
        failures.append(f"missing M1 start override(s): {', '.join(missing_start)}")
    if not (SCENARIO_OUT / "00_scenarios.txt").is_file():
        failures.append("missing M1 scenario override")
    if not (TEST_OUT / "me_m1_proof.txt").is_file():
        failures.append("missing M1 in-game test")
    if not (TRAIT_OUT / "me_m1_immortality_probe.txt").is_file():
        failures.append("missing M1 immortality trait probe")
    locator_dir = ROOT / "in_game/gfx/map/map_objects"
    for kind in ("city", "combat", "unit_stack", "vfx", "dock"):
        if not (locator_dir / f"generated_map_object_locators_{kind}.txt").is_file():
            failures.append(f"missing generated {kind} locator")
    if not (locator_dir / "generated_map_object_locators_volcano_eruption.txt").is_file():
        failures.append("missing generated volcano_eruption locator")
    if not (locator_dir / "dynamic_game_objects.txt").is_file():
        failures.append("missing dynamic game-object quarantine")
    holy_site_dir = ROOT / "in_game/common/holy_sites"
    if not holy_site_dir.is_dir() or not any(holy_site_dir.glob("*.txt")):
        failures.append("missing vanilla holy-site quarantine")
    installed_tests = game_map().parent / "common/tests"
    missing_test_quarantines = [
        path.name
        for path in installed_tests.glob("*.txt")
        if path.name != "readme.txt" and not (TEST_OUT / path.name).is_file()
    ]
    if missing_test_quarantines:
        failures.append(
            "missing vanilla test quarantines: " + ", ".join(missing_test_quarantines)
        )
    names = named_colors(OUT / "named_locations/00_default.txt")
    color_to_name = {color: name for name, color in names}
    present: set[tuple[int, int, int]] = set()
    with Image.open(OUT / "locations.png") as image:
        if image.mode != "RGB" or image.size != (WORLD_W, WORLD_H):
            failures.append(f"locations.png contract mismatch: {image.mode} {image.size}")
        sampled = np.asarray(image.resize((GRID_W, GRID_H), Image.Resampling.NEAREST))
        present = {tuple(int(v) for v in color) for row in sampled for color in row}
        unknown = present - set(color_to_name)
        if unknown:
            failures.append(f"locations.png contains {len(unknown)} unregistered color(s)")
        manifest = json.loads((OUT / "m1_manifest.json").read_text(encoding="utf-8"))
        if len(present) != manifest["location_count"]:
            failures.append(
                f"location-color count mismatch: present={len(present)} "
                f"manifest={manifest['location_count']}"
            )
    with Image.open(OUT / "rivers.png") as image:
        if image.mode != "P" or image.size != (WORLD_W, WORLD_H):
            failures.append(f"rivers.png contract mismatch: {image.mode} {image.size}")
    template_keys = set(
        re.findall(r"(?m)^([A-Za-z0-9_]+)\s*=", (OUT / "location_templates.txt").read_text(encoding="utf-8-sig"))
    )
    expected_keys = {color_to_name[color] for color in present if color in color_to_name}
    if template_keys != expected_keys:
        failures.append(f"location-template coverage mismatch: {len(template_keys)} != {len(expected_keys)}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        write()
    failures = check()
    if failures:
        print("m1_proof_map: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("m1_proof_map: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
