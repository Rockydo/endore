#!/usr/bin/env python3
"""Capture the binding M2 nine-theatre evidence with deterministic cameras."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "tools" / "gamedriver.py"
INDEX = ROOT / "docs" / "world" / "derived" / "location_index.csv"
LOCALIZATION = ROOT / "in_game" / "localization" / "english" / "m2_map_l_english.yml"
PROJECTION = ROOT / "docs" / "world" / "control" / "projection.json"
EX_TEMPFAIL = 75


@dataclass(frozen=True)
class Theatre:
    slug: str
    regional_query: str
    close_query: str
    # Finder focus establishes a stable maximum-close 3D camera. These are
    # zoom-out detents from that camera, not absolute zoom-ins from full map.
    regional_zoom: int = 6
    close_zoom: int = 1


# Physical-theatre cameras are feature-specific. Forest objects disappear one
# detent before the finder's maximum-close camera in build 24187685, while
# relief and material remain readable there. Regional frames deliberately
# retain map orientation; close frames are the binding 3D evidence. Keep the
# hydrology defaults above for river pairs, but bind forests to maximum close.
# Queries deliberately resolve to one generated display name.
THEATRES = (
    Theatre("01_shire_old_forest", "The Old Forest", "The Old Forest", 2, 0),
    Theatre("02_forochel", "Forochel Camp", "Forochel Camp", 4, 1),
    Theatre("03_misty_anduin", "Caras Galadhon", "Khazad", 4, 1),
    Theatre("04_mirkwood", "Woodmen's Hall", "Woodmen's Hall", 2, 0),
    Theatre("05_rohan_white", "Edoras", "Dunharrow", 4, 1),
    Theatre("06_gondor_belfalas", "Edhellond", "Edhellond", 4, 1),
    Theatre("07_mordor", "Morannon", "Orodruin", 4, 1),
    Theatre("08_rhun", "Burh Gath", "Burh Gath", 4, 1),
    Theatre("09_harad", "Qarsad", "Qarsad", 4, 1),
)

# The nine-theatre gate proves continental coverage; these two additional
# deterministic pairs bind the owner's river acceptance criterion to the
# upper and lower reaches of the Great River.
HYDROLOGY_VIEWS = (
    Theatre("10_anduin_upper", "Caras Galadhon", "Caras Galadhon"),
    Theatre("11_anduin_lower", "Osgiliath", "Osgiliath"),
    # Current localized locations nearest the hash-pinned middle reaches of
    # Celebrant and Entwash; coordinate contracts below prevent name drift
    # from silently moving either camera to another theatre.
    Theatre("12_celebrant", "Westbank Heights", "Westbank Heights"),
    Theatre("13_entwash", "Framham", "Framham"),
)

# The nine theatres prove continental coverage, but several owner-sensitive
# mechanisms can fall between their camera centres. Keep them in the same
# fresh renderer session so canopy density, isolated summits, and terrain-
# native small water are never accepted from stale or incomparable captures.
# Forest and sub-location-water close frames use finder maximum-close because
# both object density and tiny irregular water outlines disappear rapidly one
# detent farther out in build 24187685.
FOCUSED_PHYSICAL_VIEWS = (
    Theatre("27_lothlorien_canopy", "Caras Galadhon", "Caras Galadhon", 2, 0),
    # The literal settlement name also matches a generated "Gundabad
    # Heights" far to the south. Coldpoint Heights is the unique closest
    # localized mountain cell to the audited summit and keeps the camera on
    # the intended northern junction without renaming game content.
    Theatre("28_gundabad", "Coldpoint Heights", "Coldpoint Heights", 4, 1),
    Theatre("29_erebor", "Erebor", "Erebor", 4, 1),
    Theatre("30_mirrormere", "Lake Alderbank", "Lake Alderbank", 2, 0),
    Theatre("31_nindalf", "Nen Emyn adarath", "Nen Emyn adarath", 2, 0),
    Theatre("32_mount_gram", "Mount Gram", "Mount Gram", 4, 1),
)

# A separate focused run covers the other binding major trunks and named
# affluents without making the established nine-theatre default audit slower.
# Anchors are deliberately ASCII finder queries and uniquely localized below.
DRAINAGE_VIEWS = (
    Theatre("14_baranduin", "Brandywine Bridge", "Brandywine Bridge"),
    Theatre("15_lhun", "Winterhaven Waste", "Winterhaven Waste"),
    Theatre("16_greyflood", "Cedardown End", "Cedardown End"),
    Theatre("17_isen", "Fords of Isen", "Fords of Isen"),
    Theatre("18_celduin", "Lakestrand", "Lakestrand"),
    Theatre("19_carnen", "Gatholgathol", "Gatholgathol"),
    Theatre("20_harnen", "Qasahir Oasis", "Qasahir Oasis"),
    Theatre("21_poros", "Bar bornlad", "Bar bornlad"),
    Theatre("22_lefnui", "Celon gondeth", "Celon gondeth"),
    Theatre("23_serni", "Eithel duinlad", "Eithel duinlad"),
    Theatre("24_morgulduin", "Minas Morgul", "Minas Morgul"),
    Theatre("25_gladden", "Goldenhall", "Goldenhall"),
    Theatre("26_limlight", "Field of Celebrant", "Field of Celebrant"),
    # v105 junction proof: these pairs sit on newly promoted red-ended
    # tributaries rather than merely revisiting their established trunks.
    Theatre("33_sirith_confluence", "Minas Tirith", "Minas Tirith"),
    Theatre("34_shire_confluences", "Bucklebury", "Bucklebury"),
    Theatre("35_forest_river_feeder", "Esgaroth", "Esgaroth"),
)

# Finder success proves only that a string exists. Bind every formerly raw
# generated target to its intended equal-scale source coordinate and strategic
# region as well, so a localization or regeneration change fails statically
# instead of producing a confidently mislabeled screenshot.
SOURCE_TARGETS = {
    "The Old Forest": (0.387750, 0.240760, "me_shire_breeland_region"),
    "Forochel Camp": (0.341880, 0.065462, "me_forochel_region"),
    "Woodmen's Hall": (0.562000, 0.300000, "me_mirkwood_region"),
    "Burh Gath": (0.770000, 0.250000, "me_rhun_region"),
    "Qarsad": (0.675000, 0.870000, "me_near_harad_region"),
    "Westbank Heights": (0.500366, 0.339521, "me_anduin_vale_region"),
    "Framham": (0.517055, 0.480938, "me_rohan_region"),
    "Caras Galadhon": (0.519414, 0.356131, "me_anduin_vale_region"),
    "Khazad": (0.490110, 0.335613, "me_anduin_vale_region"),
    "Edoras": (0.498657, 0.538349, "me_rohan_region"),
    "Dunharrow": (0.496703, 0.553004, "me_rohan_region"),
    "Edhellond": (0.501832, 0.646800, "me_belfalas_region"),
    "Morannon": (0.609768, 0.529555, "me_brown_lands_region"),
    "Orodruin": (0.628571, 0.576942, "me_mordor_region"),
    "Osgiliath": (0.592430, 0.603811, "me_ithilien_region"),
    "Brandywine Bridge": (0.381197, 0.227162, "me_shire_breeland_region"),
    "Winterhaven Waste": (0.316728, 0.115779, "me_forochel_region"),
    "Cedardown End": (0.415629, 0.346849, "me_enedwaith_region"),
    "Fords of Isen": (0.467888, 0.488520, "me_rohan_region"),
    "Lakestrand": (0.607082, 0.211040, "me_dale_region"),
    "Gatholgathol": (0.671307, 0.181729, "me_rhun_region"),
    "Qasahir Oasis": (0.586081, 0.827553, "me_near_harad_region"),
    "Bar bornlad": (0.592918, 0.711773, "me_south_gondor_region"),
    "Celon gondeth": (0.432234, 0.579384, "me_belfalas_region"),
    "Eithel duinlad": (0.558974, 0.658525, "me_lebennin_region"),
    "Minas Morgul": (0.607326, 0.595506, "me_ithilien_region"),
    "Goldenhall": (0.522100, 0.269174, "me_anduin_vale_region"),
    "Field of Celebrant": (0.539194, 0.417196, "me_anduin_vale_region"),
    "Minas Tirith": (0.578266, 0.611138, "me_anorien_region"),
    "Bucklebury": (0.376801, 0.232535, "me_shire_breeland_region"),
    "Esgaroth": (0.599756, 0.162677, "me_dale_region"),
    "Coldpoint Heights": (0.502345, 0.102487, "me_northern_wastes_region"),
    "Erebor": (0.599699, 0.137606, "me_dale_region"),
    "Lake Alderbank": (0.496887, 0.330666, "me_anduin_vale_region"),
    "Nen Emyn adarath": (0.580500, 0.511200, "me_brown_lands_region"),
    "Mount Gram": (0.449084, 0.141671, "me_north_arnor_region"),
}
MAX_TARGET_DISTANCE = 0.012

# Every hydrology camera must also lie near the exact source-backed course it
# claims to show. This catches semantically wrong but geographically stable
# labels such as the former Field-of-Celebrant camera on the Limlight.
RIVER_TARGETS = {
    "Caras Galadhon": "upper_anduin",
    "Osgiliath": "anduin",
    "Westbank Heights": "celebrant",
    "Framham": "entwash",
    "Brandywine Bridge": "baranduin",
    "Winterhaven Waste": "lhun",
    "Cedardown End": "greyflood",
    "Fords of Isen": "isen",
    "Lakestrand": "celduin",
    "Gatholgathol": "carnen",
    "Qasahir Oasis": "harnen",
    "Bar bornlad": "poros",
    "Celon gondeth": "lefnui",
    "Eithel duinlad": "serni",
    "Minas Morgul": "morgulduin",
    "Goldenhall": "gladden",
    "Field of Celebrant": "limlight",
    "Minas Tirith": "source_sirith_75_00",
    "Bucklebury": "source_stockbrook_61_00",
    "Esgaroth": "source_unnamed_73_00",
}
MAX_RIVER_DISTANCE = 0.010


def localization_names() -> dict[str, str]:
    result: dict[str, str] = {}
    pattern = re.compile(r'^\s*([a-zA-Z0-9_]+):\s*"(.*)"\s*$')
    for line in LOCALIZATION.read_text(encoding="utf-8-sig").splitlines():
        match = pattern.match(line)
        if match:
            result[match.group(1)] = match.group(2)
    return result


def driver(*args: str) -> int:
    command = [sys.executable, str(DRIVER), *args]
    print("+", " ".join(command), flush=True)
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def point_segment_distance(
    point: tuple[float, float],
    start: list[float],
    end: list[float],
) -> float:
    delta_x = float(end[0]) - float(start[0])
    delta_y = float(end[1]) - float(start[1])
    length_squared = delta_x * delta_x + delta_y * delta_y
    if length_squared == 0.0:
        return math.dist(point, (float(start[0]), float(start[1])))
    progress = (
        (point[0] - float(start[0])) * delta_x
        + (point[1] - float(start[1])) * delta_y
    ) / length_squared
    progress = min(1.0, max(0.0, progress))
    nearest = (
        float(start[0]) + progress * delta_x,
        float(start[1]) + progress * delta_y,
    )
    return math.dist(point, nearest)


def check_manifest() -> list[str]:
    failures: list[str] = []
    with INDEX.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    localized_by_key = localization_names()
    localized_rows = [
        (row, localized_by_key.get(row["key"], row["display_name"])) for row in rows
    ]
    projection = json.loads(PROJECTION.read_text(encoding="utf-8"))
    rivers = {item["key"]: item for item in projection["rivers"]}
    all_views = (
        THEATRES
        + HYDROLOGY_VIEWS
        + DRAINAGE_VIEWS
        + FOCUSED_PHYSICAL_VIEWS
    )
    for theatre in all_views:
        for role, query in (
            ("regional", theatre.regional_query),
            ("close", theatre.close_query),
        ):
            matches = [
                (row, name)
                for row, name in localized_rows
                if query.casefold() in name.casefold()
            ]
            if len(matches) != 1:
                failures.append(
                    f"{theatre.slug} {role} query {query!r} resolves to "
                    f"{len(matches)} localized locations: "
                    f"{[name for _, name in matches[:5]]}"
                )
            elif query in SOURCE_TARGETS:
                row, name = matches[0]
                expected_x, expected_y, expected_region = SOURCE_TARGETS[query]
                actual_x = float(row["normalized_x"])
                actual_y = float(row["normalized_y"])
                distance = ((actual_x - expected_x) ** 2 + (actual_y - expected_y) ** 2) ** 0.5
                if distance > MAX_TARGET_DISTANCE:
                    failures.append(
                        f"{theatre.slug} {role} target {name!r} is {distance:.5f} "
                        "from its source coordinate"
                    )
                if row["region"] != expected_region:
                    failures.append(
                        f"{theatre.slug} {role} target {name!r} is in "
                        f"{row['region']}, expected {expected_region}"
                    )
                river_key = RIVER_TARGETS.get(query)
                if river_key:
                    river = rivers.get(river_key)
                    if river is None:
                        failures.append(
                            f"{theatre.slug} {role} references unknown river {river_key}"
                        )
                    else:
                        point = (actual_x, actual_y)
                        distance_to_river = min(
                            point_segment_distance(point, start, end)
                            for start, end in zip(
                                river["points"], river["points"][1:], strict=False
                            )
                        )
                        if distance_to_river > MAX_RIVER_DISTANCE:
                            failures.append(
                                f"{theatre.slug} {role} target {name!r} is "
                                f"{distance_to_river:.5f} from river {river_key}"
                            )
        if not 0 <= theatre.close_zoom < theatre.regional_zoom <= 16:
            failures.append(f"{theatre.slug} has invalid zoom pair")
    if len({item.slug for item in THEATRES}) != 9:
        failures.append("the binding audit must contain nine unique theatres")
    if len({item.slug for item in all_views}) != len(all_views):
        failures.append("the theatre and hydrology audit slugs must be unique")
    used_river_queries = {
        query
        for theatre in HYDROLOGY_VIEWS + DRAINAGE_VIEWS
        for query in (theatre.regional_query, theatre.close_query)
    }
    if used_river_queries != set(RIVER_TARGETS):
        failures.append("river camera/course bindings do not cover every drainage view")
    return failures


def reset_and_capture(query: str, zoom: int, name: str, session: str) -> int:
    commands = (
        ("focus-location", query, "--settle", "4"),
        # Finder focus establishes both the correct centre and a maximum-close
        # 3D camera. Apply a bounded zoom-out from that known state: a larger
        # value gives the regional frame and a smaller value the close frame.
        ("scroll", str(-zoom), "--settle", "4"),
        (
            "move",
            "0.95",
            "0.10",
            "--settle",
            "3",
            "--capture",
            name,
            "--session",
            session,
        ),
    )
    for command in commands:
        result = driver(*command)
        if result:
            return result
    return 0


def capture(
    session: str,
    playback: float,
    *,
    hydrology_only: bool,
    drainage_only: bool,
    target_slugs: tuple[str, ...],
) -> int:
    result = driver("new-observer", "--visual-map", "--session", session)
    if result:
        return result
    try:
        if not hydrology_only and not drainage_only and not target_slugs:
            # Bind the full-map silhouette gate to the same fresh renderer
            # state as the theatre pairs. Focus first because the location
            # finder can retain or restore a close camera; the hard zoom-out
            # must be the final camera operation before capture.
            for command in (
                ("focus-location", "Caras Galadhon", "--settle", "4"),
                ("scroll", "-32", "--settle", "4"),
                (
                    "move",
                    "0.95",
                    "0.10",
                    "--settle",
                    "3",
                    "--capture",
                    "00_full_map",
                    "--session",
                    session,
                ),
            ):
                result = driver(*command)
                if result:
                    return result
        if target_slugs:
            all_views = (
                THEATRES
                + HYDROLOGY_VIEWS
                + DRAINAGE_VIEWS
                + FOCUSED_PHYSICAL_VIEWS
            )
            by_slug = {item.slug: item for item in all_views}
            targets = tuple(by_slug[slug] for slug in target_slugs)
        elif drainage_only:
            targets = DRAINAGE_VIEWS
        elif hydrology_only:
            targets = HYDROLOGY_VIEWS
        else:
            targets = THEATRES + HYDROLOGY_VIEWS + FOCUSED_PHYSICAL_VIEWS
        for theatre in targets:
            result = reset_and_capture(
                theatre.regional_query,
                theatre.regional_zoom,
                f"{theatre.slug}_regional",
                session,
            )
            if result:
                return result
            result = reset_and_capture(
                theatre.close_query,
                theatre.close_zoom,
                f"{theatre.slug}_close",
                session,
            )
            if result:
                return result
        if playback > 0:
            result = driver(
                "observer",
                "--seconds",
                str(playback),
                "--maximum-speed",
                "--capture-interval",
                "20",
                "--status-interval",
                "10",
                "--session",
                session,
            )
            if result:
                return result
        return 0
    finally:
        driver("stop")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--session", default="m2_nine_theatre_audit")
    parser.add_argument("--playback", type=float, default=45)
    focus = parser.add_mutually_exclusive_group()
    focus.add_argument("--hydrology-only", action="store_true")
    focus.add_argument("--drainage-only", action="store_true")
    focus.add_argument(
        "--targets",
        help="comma-separated exact theatre slugs for a selective live rerun",
    )
    args = parser.parse_args()
    failures = check_manifest()
    if failures:
        for failure in failures:
            print(f"capture_m2_theatres: FAIL {failure}", file=sys.stderr)
        return 1
    if args.check:
        print(
            "capture_m2_theatres: PASS "
            "(source- and course-bound localized camera targets)"
        )
        return 0
    target_slugs: tuple[str, ...] = ()
    if args.targets:
        target_slugs = tuple(
            slug.strip() for slug in args.targets.split(",") if slug.strip()
        )
        known_slugs = {
            item.slug
            for item in (
                THEATRES
                + HYDROLOGY_VIEWS
                + DRAINAGE_VIEWS
                + FOCUSED_PHYSICAL_VIEWS
            )
        }
        unknown_slugs = sorted(set(target_slugs) - known_slugs)
        if unknown_slugs:
            parser.error(f"unknown target slugs: {', '.join(unknown_slugs)}")
        if len(target_slugs) != len(set(target_slugs)):
            parser.error("--targets repeats a slug")
    return capture(
        args.session,
        args.playback,
        hydrology_only=args.hydrology_only,
        drainage_only=args.drainage_only,
        target_slugs=target_slugs,
    )


if __name__ == "__main__":
    raise SystemExit(main())
