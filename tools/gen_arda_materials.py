#!/usr/bin/env python3
"""Generate/check ENDÓRË's continuous all-land terrain material palette."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "local_paths.json"
OUT = ROOT / "in_game" / "gfx" / "terrain2" / "materials.txt"

BIOME_BLOCK = r"""

	# ENDÓRË: one rendering palette across every land topography. Gameplay
	# topography remains location-scoped, while cache bits 10-15 select these
	# Arda-native continuous surface families without exposing cell borders.
	{
		name = endore_dynamic_land_biome
		materials = {
			sand_beach_variation_02	# 0 flat coast
			base_rock_02			# 1 hill coast
			base_rock				# 2 plateau coast
			base_rock_dark			# 3 mountain coast
			dirt_ponds_01			# 4 wetland coast
			sand_transition			# 5 coast transition
			dirt_ponds_01			# 6 rivers/lakes
			dirt_transition_02		# 7 water transition
			grass_scatter_variation_01	# 8 vegetation transition
			dirt_grass_transition_01	# 9 climate transition
			grass_dense_variation_01	# 10 grass
			base_dirt				# 11 earth
			base_rock_dark			# 12 dark/volcanic rock
			base_rock				# 13 exposed rock
			Snow					# 14 snow
			base_sand				# 15 sand
		}
	}
"""


def installed_source() -> Path:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    return (
        Path(config["game_dir"])
        / "game"
        / "in_game"
        / "gfx"
        / "terrain2"
        / "materials.txt"
    )


def expected_text() -> str:
    source = installed_source()
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    if "name = endore_dynamic_land_biome" in text:
        raise ValueError("installed materials unexpectedly contain ENDÓRË biome")
    closing = text.rfind("\n}")
    if closing < 0:
        raise ValueError("installed materials file lacks its final biomes closure")
    return text[:closing] + BIOME_BLOCK + text[closing:]


def write() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(expected_text(), encoding="utf-8-sig", newline="\n")
    print("gen_arda_materials: wrote installed-compatible dynamic land palette")


def check() -> list[str]:
    if not OUT.is_file():
        return ["missing in_game/gfx/terrain2/materials.txt"]
    expected = expected_text()
    actual = OUT.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    failures: list[str] = []
    if actual != expected:
        failures.append("materials.txt differs from installed-compatible palette")
    if actual.count("name = endore_dynamic_land_biome") != 1:
        failures.append("dynamic land biome is not unique")
    block = actual[actual.index("name = endore_dynamic_land_biome") :]
    if block.split("}", 2)[0].count("# ") != 16:
        failures.append("dynamic land biome does not expose exactly 16 channels")
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
            print(f"gen_arda_materials: FAIL {failure}")
        return 1
    print("gen_arda_materials: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
