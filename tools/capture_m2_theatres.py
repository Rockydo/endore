#!/usr/bin/env python3
"""Capture the binding M2 nine-theatre evidence with deterministic cameras."""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "tools" / "gamedriver.py"
INDEX = ROOT / "docs" / "world" / "derived" / "location_index.csv"
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
    Theatre("01_shire_old_forest", "Land 4390", "Land 4390"),
    Theatre("02_forochel", "Land 0513", "Land 0513"),
    Theatre("03_misty_anduin", "Caras Galadhon", "Khazad"),
    Theatre("04_mirkwood", "Land 4278", "Land 4278"),
    Theatre("05_rohan_white", "Edoras", "Dunharrow"),
    Theatre("06_gondor_belfalas", "Dol Amroth", "Dol Amroth", 7, 10),
    Theatre("07_mordor", "Barad", "Morannon"),
    Theatre("08_rhun", "Land 2408", "Land 2408"),
    Theatre("09_harad", "Land 1408", "Land 1408"),
)

# The nine-theatre gate proves continental coverage; these two additional
# deterministic pairs bind the owner's river acceptance criterion to the
# upper and lower reaches of the Great River.
HYDROLOGY_VIEWS = (
    Theatre("10_anduin_upper", "Caras Galadhon", "Caras Galadhon", 8, 12),
    Theatre("11_anduin_lower", "Osgiliath", "Osgiliath", 8, 12),
    # Generated location centres nearest the hash-pinned middle reaches of
    # Celebrant and Entwash; both queries are uniqueness-checked below.
    Theatre("12_celebrant", "Land 1568", "Land 1568", 8, 12),
    Theatre("13_entwash", "Land 2696", "Land 2696", 8, 12),
)


def driver(*args: str) -> int:
    command = [sys.executable, str(DRIVER), *args]
    print("+", " ".join(command), flush=True)
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def check_manifest() -> list[str]:
    failures: list[str] = []
    with INDEX.open(encoding="utf-8-sig", newline="") as handle:
        names = [row["display_name"] for row in csv.DictReader(handle)]
    for theatre in THEATRES + HYDROLOGY_VIEWS:
        for role, query in (
            ("regional", theatre.regional_query),
            ("close", theatre.close_query),
        ):
            matches = [name for name in names if query.casefold() in name.casefold()]
            if len(matches) != 1:
                failures.append(
                    f"{theatre.slug} {role} query {query!r} resolves to "
                    f"{len(matches)} generated locations: {matches[:5]}"
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
        print("capture_m2_theatres: PASS (nine unique generated camera targets)")
        return 0
    return capture(
        args.session,
        args.playback,
        hydrology_only=args.hydrology_only,
    )


if __name__ == "__main__":
    raise SystemExit(main())
