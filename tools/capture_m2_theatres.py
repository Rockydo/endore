#!/usr/bin/env python3
"""Capture the binding M2 nine-theatre evidence with deterministic cameras."""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "tools" / "gamedriver.py"
INDEX = ROOT / "docs" / "world" / "derived" / "location_index.csv"
LOCALIZATION = ROOT / "in_game" / "localization" / "english" / "m2_map_l_english.yml"
EX_TEMPFAIL = 75


@dataclass(frozen=True)
class Theatre:
    slug: str
    regional_query: str
    close_query: str
    regional_zoom: int = 8
    close_zoom: int = 12


# Queries deliberately resolve to one generated display name.  This avoids the
# ambiguous Dol Amroth/Edhellond finder evidence that previously centred either
# open sea or an inland cell and therefore proved nothing about Belfalas.
THEATRES = (
    Theatre("01_shire_old_forest", "The Old Forest", "The Old Forest"),
    Theatre("02_forochel", "Forochel Camp", "Forochel Camp"),
    Theatre("03_misty_anduin", "Caras Galadhon", "Khazad"),
    Theatre("04_mirkwood", "Woodmen's Hall", "Woodmen's Hall"),
    Theatre("05_rohan_white", "Edoras", "Dunharrow"),
    Theatre("06_gondor_belfalas", "Dol Amroth", "Dol Amroth", 7, 10),
    Theatre("07_mordor", "Morannon", "Barad"),
    Theatre("08_rhun", "Burh Gath", "Burh Gath"),
    Theatre("09_harad", "Qarsad", "Qarsad"),
)

# The nine-theatre gate proves continental coverage; these two additional
# deterministic pairs bind the owner's river acceptance criterion to the
# upper and lower reaches of the Great River.
HYDROLOGY_VIEWS = (
    Theatre("10_anduin_upper", "Caras Galadhon", "Caras Galadhon", 8, 12),
    Theatre("11_anduin_lower", "Osgiliath", "Osgiliath", 8, 12),
    # Current localized locations nearest the hash-pinned middle reaches of
    # Celebrant and Entwash; coordinate contracts below prevent name drift
    # from silently moving either camera to another theatre.
    Theatre("12_celebrant", "Field of Celebrant", "Field of Celebrant", 8, 12),
    Theatre("13_entwash", "odgar", "odgar", 8, 12),
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
    "Field of Celebrant": (0.539941, 0.413770, "me_anduin_vale_region"),
    "odgar": (0.517055, 0.480938, "me_rohan_region"),
    "Caras Galadhon": (0.519414, 0.356131, "me_anduin_vale_region"),
    "Khazad": (0.490110, 0.335613, "me_anduin_vale_region"),
    "Edoras": (0.498657, 0.538349, "me_rohan_region"),
    "Dunharrow": (0.496703, 0.553004, "me_rohan_region"),
    "Dol Amroth": (0.489133, 0.672692, "me_belfalas_region"),
    "Morannon": (0.609768, 0.529555, "me_brown_lands_region"),
    "Barad": (0.643956, 0.573522, "me_mordor_region"),
    "Osgiliath": (0.592430, 0.603811, "me_ithilien_region"),
}
MAX_TARGET_DISTANCE = 0.012


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


def check_manifest() -> list[str]:
    failures: list[str] = []
    with INDEX.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    localized_by_key = localization_names()
    localized_rows = [
        (row, localized_by_key.get(row["key"], row["display_name"])) for row in rows
    ]
    for theatre in THEATRES + HYDROLOGY_VIEWS:
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
        if not 1 <= theatre.regional_zoom < theatre.close_zoom <= 16:
            failures.append(f"{theatre.slug} has invalid zoom pair")
    if len({item.slug for item in THEATRES}) != 9:
        failures.append("the binding audit must contain nine unique theatres")
    if len({item.slug for item in THEATRES + HYDROLOGY_VIEWS}) != 13:
        failures.append("the theatre and hydrology audit slugs must be unique")
    return failures


def reset_and_capture(query: str, zoom: int, name: str, session: str) -> int:
    commands = (
        ("scroll", "-32", "--settle", "2"),
        ("focus-location", query, "--settle", "4"),
        ("scroll", str(zoom), "--settle", "4"),
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


def capture(session: str, playback: float, *, hydrology_only: bool) -> int:
    result = driver("new-observer", "--visual-map", "--session", session)
    if result:
        return result
    try:
        if not hydrology_only:
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
        targets = HYDROLOGY_VIEWS if hydrology_only else THEATRES + HYDROLOGY_VIEWS
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
    parser.add_argument("--hydrology-only", action="store_true")
    args = parser.parse_args()
    failures = check_manifest()
    if failures:
        for failure in failures:
            print(f"capture_m2_theatres: FAIL {failure}", file=sys.stderr)
        return 1
    if args.check:
        print("capture_m2_theatres: PASS (source-bound localized camera targets)")
        return 0
    return capture(
        args.session,
        args.playback,
        hydrology_only=args.hydrology_only,
    )


if __name__ == "__main__":
    raise SystemExit(main())
