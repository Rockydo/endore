#!/usr/bin/env python3
"""Generate/check the neutral runtime scaffold used to verify the M2 map."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worldgen import MAP_OUT, ROOT, build_model, game_map

START_OUT = ROOT / "main_menu/setup/start"
SCENARIO_OUT = ROOT / "main_menu/common/scenarios"
TEST_OUT = ROOT / "in_game/common/tests"
TRAIT_OUT = ROOT / "in_game/common/traits"
LOC_OUT = ROOT / "in_game/localization/english"
M2_DATE = (3018, 1, 1)


def _script_line(text: str) -> str:
    """Remove comments and quoted contents without disturbing script braces."""
    result: list[str] = []
    quoted = False
    escaped = False
    for character in text:
        if escaped:
            escaped = False
            result.append(" ")
        elif quoted and character == "\\":
            escaped = True
            result.append(" ")
        elif character == '"':
            quoted = not quoted
            result.append(" ")
        elif character == "#" and not quoted:
            break
        else:
            result.append(" " if quoted else character)
    return "".join(result)


def _installed_definitions(
    folder: str,
    *,
    enabled_at: tuple[int, int, int] | None = None,
    exclude_inactive: bool = False,
) -> list[str]:
    """Return top-level database keys, optionally excluding future entries."""
    source = game_map().parent / "common" / folder
    definitions: list[str] = []
    for path in sorted(source.glob("*.txt")):
        depth = 0
        current: str | None = None
        enable: tuple[int, int, int] | None = None
        active = True
        for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
            line = _script_line(raw_line)
            if depth == 0:
                match = re.match(r"\s*([A-Za-z0-9_]+)\s*=\s*\{", line)
                if match:
                    current = match.group(1)
                    enable = None
                    active = True
            elif depth == 1 and current is not None:
                match = re.match(
                    r"\s*enable\s*=\s*(\d+)\.(\d+)\.(\d+)",
                    line,
                )
                if match:
                    enable = tuple(int(part) for part in match.groups())
                match = re.match(r"\s*active\s*=\s*(?:no|false)\b", line)
                if match:
                    active = False
            depth += line.count("{") - line.count("}")
            if depth < 0:
                raise ValueError(f"{path} closes before opening")
            if depth == 0 and current is not None:
                enabled = (
                    enabled_at is None or enable is None or enable <= enabled_at
                )
                if enabled and (active or not exclude_inactive):
                    definitions.append(current)
                current = None
        if depth:
            raise ValueError(f"{path} ends at brace depth {depth}")
    if len(definitions) != len(set(definitions)):
        raise ValueError(f"duplicate top-level definitions in common/{folder}")
    return sorted(definitions)


def technical_census(owned: list[str]) -> dict[str, list[str]]:
    """Cover retained vanilla demographic registries during the M2 map gate."""
    cultures = _installed_definitions("cultures", exclude_inactive=True)
    religions = _installed_definitions("religions", enabled_at=M2_DATE)
    if not cultures or not religions:
        raise ValueError("installed culture/religion registry is empty")
    census: dict[str, list[str]] = defaultdict(list)
    for index, culture in enumerate(cultures):
        religion = religions[index % len(religions)]
        location = owned[index % len(owned)]
        census[location].append(
            "\tdefine_pop = { type = peasants size = 0.01 "
            f"culture = {culture} religion = {religion} }}"
        )
    return census


def pops_payload(owned: list[str]) -> str:
    census = technical_census(owned)
    lines = ["locations = {"]
    for key in owned:
        lines.append(f"\t{key} = {{")
        lines.append(
            "\t\tdefine_pop = { type = peasants size = 1 "
            "culture = swedish religion = catholic }"
        )
        if key == "minas_tirith":
            for pop_type in ("nobles", "clergy", "burghers"):
                lines.append(
                    "\t\tdefine_pop = { "
                    f"type = {pop_type} size = 0.1 "
                    "culture = swedish religion = catholic }"
                )
        lines.extend(f"\t{entry}" for entry in census.get(key, ()))
        lines.append("\t}")
    lines.append("}")
    return "\n".join(lines) + "\n"


def sanitized_monarchy_template() -> str:
    source = (
        game_map().parents[1]
        / "main_menu/setup/templates/catholic_monarchy.txt"
    ).read_text(encoding="utf-8-sig")
    sanitized = source.replace(
        "\t\tauxilium_et_consilium\n",
        "",
    ).replace(
        "\t\tnoble_fortification_licenses\n",
        "",
    ).replace(
        "royal_court_customs_law = aristocratic_court_policy",
        "royal_court_customs_law = balanced_court_policy",
    ).replace(
        "legal_code_law = civil_law_policy",
        "legal_code_law = traditional_law_policy",
    ).replace(
        "\t\tfeudal_de_jure_law = by_tradition\n",
        "",
    ).replace(
        "\their_selection = cognatic_primogeniture\n",
        "\their_selection = cognatic_primogeniture\n\truler = random\n",
    )
    return "\n".join(line.rstrip() for line in sanitized.splitlines()) + "\n"


def start_payloads() -> dict[Path, str]:
    model = build_model()
    owned = [
        location.key
        for location in model.locations
        if location.kind == "land"
    ]
    discovered_regions = sorted(
        {
            location.region
            for location in model.locations
        }
    )
    dummy_capital = "mithlond"
    monarchy = "".join(
        f"\t\t\t{line}\n" if line else "\n"
        for line in sanitized_monarchy_template().splitlines()
    )
    prefix = "# Generated by tools/m2_runtime.py --write; neutral M2 gate scaffold.\n"
    files = {
        "02_core.txt": "institution_manager = {\n\tinstitutions = {\n\t}\n}\nreligion_manager = {\n}\n",
        "03_markets.txt": "market_manager = {\n\tadd_market = mithlond\n}\n",
        "04_dynasties.txt": "dynasty_manager = {\n}\n",
        "05_characters.txt": "character_db = {\n}\n",
        "06_pops.txt": pops_payload(owned),
        "07_cities_and_buildings.txt": (
            "locations = {\n}\n"
            "building_manager = {\n}\n"
        ),
        "08_institutions.txt": "locations = {\n}\n",
        "09_roads.txt": "road_network = {\n}\n",
        "10_countries.txt": (
            "current_age = age_1_traditions\n"
            "countries = {\n"
            "\tcountries = {\n"
            "\t\tSWE = {\n"
            f"\t\t\town_control_core = {{ {' '.join(owned)} }}\n"
            f"{monarchy}"
            "\t\t\tcountry_rank = rank_county\n"
            "\t\t\tdiscovered_regions = { "
            f"{' '.join(discovered_regions)}"
            " }\n"
            f"\t\t\tcapital = {dummy_capital}\n"
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
    return {START_OUT / name: prefix + text for name, text in files.items()}


def other_payloads() -> dict[Path, str]:
    payloads: dict[Path, str] = {}
    payloads[
        ROOT / "main_menu/common/flag_definitions/00_flag_definitions.txt"
    ] = (
        "\ufeff# Generated M2 gate registry: one technical country only.\n"
        "DEFAULT = {\n"
        "\tflag_definition = {\n"
        "\t\tcoa = SWE\n"
        "\t\tpriority = -100\n"
        "\t\ttrigger = {\n"
        "\t\t\talways = no\n"
        "\t\t\thas_variable = has_had_war_of_the_roses_disaster\n"
        "\t\t\thas_variable = hab_imperial_flag\n"
        "\t\t}\n"
        "\t}\n"
        "}\n"
        "SWE = {\n"
        "\tflag_definition = {\n"
        "\t\tcoa = SWE\n"
        "\t\tpriority = 1\n"
        "\t}\n"
        "}\n"
    )
    installed_country_setup = game_map().parent / "setup/countries"
    for path in sorted(installed_country_setup.glob("*.txt")):
        target = ROOT / "in_game/setup/countries" / path.name
        if path.name == "_scandinavia.txt":
            payloads[target] = (
                "\ufeff# Generated M2 gate country database: technical SWE only.\n"
                "SWE = {\n"
                "\tcolor = map_swedish\n"
                "\tcolor2 = rgb { 208 9 9 }\n"
                "\tunit_color0 = hsv360 { 216 89 54 }\n"
                "\tunit_color1 = hsv360 { 47 91 78 }\n"
                "\tunit_color2 = hsv360 { 0 0 50 }\n"
                "\tculture_definition = swedish\n"
                "\treligion_definition = catholic\n"
                "\tdescription_category = diplomatic\n"
                "\tdifficulty = 2\n"
                "}\n"
            )
        else:
            payloads[target] = (
                "\ufeff# Generated M2 gate quarantine: Earth country database.\n"
            )
    payloads[SCENARIO_OUT / "00_scenarios.txt"] = (
        "\ufeff# Generated by tools/m2_runtime.py --write; neutral M2 scenario.\n"
        "me_m2_map_scenario = {\n"
        "\tcountry = SWE\n"
        "\tplayer_playstyle = ADMINISTRATIVE\n"
        "\tplayer_proficiency = NOVICE\n"
        "}\n"
    )
    payloads[TEST_OUT / "me_m2_map.txt"] = (
        "\ufeff# Generated by tools/m2_runtime.py --write; M2 runtime probe.\n"
        "me_m2_map_test = {\n"
        "\tyear = 3019\n"
        "\tsuccess = { always = yes }\n"
        "\tend_year = 3020\n"
        "\tfail_on_end_year = yes\n"
        "\tsuccess_effect = {\n"
        "\t\ttest_log = {\n"
        "\t\t\tname = me_m2_map_test\n"
        '\t\t\ttext = "M2 production map runtime test passed"\n'
        "\t\t}\n"
        "\t}\n"
        "}\n"
    )
    payloads[TRAIT_OUT / "me_m2_immortality_probe.txt"] = (
        "\ufeff# Native immortality remains a proven ENDÓRË engine contract.\n"
        "me_m2_immortality_probe = {\n"
        "\tallow = { }\n"
        "\tcategory = ruler\n"
        "\tmodifier = {\n"
        "\t\tis_immortal = yes\n"
        "\t}\n"
        "}\n"
    )
    payloads[LOC_OUT / "m2_runtime_l_english.yml"] = (
        '\ufeffl_english:\n'
        ' me_m2_immortality_probe: "Undying"\n'
        ' desc_me_m2_immortality_probe: "This probe preserves the native immortality contract."\n'
        ' me_m2_immortality_probe_die_desc: "An immortal character cannot die naturally."\n'
    )

    installed_tests = game_map().parent / "common/tests"
    for path in installed_tests.glob("*.txt"):
        if path.name == "readme.txt":
            continue
        payloads[TEST_OUT / path.name] = (
            "\ufeff# Generated M2 quarantine: vanilla geography-dependent runtime test.\n"
        )
    installed_holy_sites = game_map().parent / "common/holy_sites"
    for path in installed_holy_sites.glob("*.txt"):
        payloads[ROOT / "in_game/common/holy_sites" / path.name] = (
            "\ufeff# Generated M2 quarantine: vanilla Earth holy sites.\n"
        )
    payloads[ROOT / "in_game/common/scripted_effects/___test_effects.txt"] = (
        "\ufeff# Generated M2 quarantine: retail debug effects reference Earth databases.\n"
    )
    payloads[ROOT / "in_game/events/debug/000_johan_debug.txt"] = (
        "\ufeff# Generated M2 quarantine: retail developer-only event payload.\n"
    )
    succession_source = (
        game_map().parent / "common/disasters/byzantine_succession_crisis.txt"
    ).read_text(encoding="utf-8-sig")
    payloads[
        ROOT / "in_game/common/disasters/byzantine_succession_crisis.txt"
    ] = "\ufeff" + succession_source.replace(
        "\t\tset_variable = succession_crisis_disaster_counter\n",
        "",
    )
    return payloads


def payloads() -> dict[Path, str]:
    result = start_payloads()
    result.update(other_payloads())
    return result


def stale_generated_paths() -> tuple[Path, ...]:
    return (
        MAP_OUT / "m1_manifest.json",
        TEST_OUT / "me_m1_proof.txt",
        TRAIT_OUT / "me_m1_immortality_probe.txt",
        LOC_OUT / "m1_proof_l_english.yml",
        ROOT / "main_menu/setup/templates/catholic_monarchy.txt",
    )


def write() -> None:
    data = payloads()
    for path, text in data.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    for path in stale_generated_paths():
        if path.is_file():
            path.unlink()
    print(f"m2_runtime: wrote {len(data)} neutral scaffold/quarantine files")


def check() -> list[str]:
    failures: list[str] = []
    for path, expected in payloads().items():
        if not path.is_file():
            failures.append(f"missing {path.relative_to(ROOT)}")
        elif path.read_text(encoding="utf-8") != expected:
            failures.append(f"{path.relative_to(ROOT)} differs from M2 runtime model")
    stale = [
        path.relative_to(ROOT).as_posix()
        for path in stale_generated_paths()
        if path.exists()
    ]
    if stale:
        failures.append("stale generated runtime files remain: " + ", ".join(stale))
    owned = [
        location.key
        for location in build_model().locations
        if location.kind == "land"
    ]
    countries = start_payloads()[START_OUT / "10_countries.txt"]
    if any(key not in countries for key in owned):
        failures.append("dummy M2 country does not cover every passable land location")
    pops = start_payloads()[START_OUT / "06_pops.txt"]
    pop_cultures = set(
        re.findall(r"\bculture\s*=\s*([A-Za-z0-9_]+)", pops)
    )
    pop_religions = set(
        re.findall(r"\breligion\s*=\s*([A-Za-z0-9_]+)", pops)
    )
    missing_cultures = (
        set(_installed_definitions("cultures", exclude_inactive=True))
        - pop_cultures
    )
    if missing_cultures:
        failures.append(
            f"technical census omits {len(missing_cultures)} retained cultures"
        )
    missing_religions = (
        set(_installed_definitions("religions", enabled_at=M2_DATE))
        - pop_religions
    )
    if missing_religions:
        failures.append(
            f"technical census omits {len(missing_religions)} enabled religions"
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
            print(f"m2_runtime: FAIL {failure}")
        return 1
    print("m2_runtime: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
