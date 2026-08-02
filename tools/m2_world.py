#!/usr/bin/env python3
"""Orchestrate the complete deterministic M2 map generator chain."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import PIL
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gen_adjacencies
import gen_arda_materials
import gen_border_style
import gen_definitions
import gen_flatmap
import gen_heightmap
import gen_location_templates
import gen_locations
import gen_locators
import gen_map_objects
import gen_map_config
import gen_rivers
import gen_terrain_cache
import m2_quarantine
import m2_runtime
import m2_controls
import m3_realms
import m4_peoples
import m5_census

STAGES = (
    # Control rasters are generated code too. Keeping this explicit prevents
    # a full rewrite from silently consuming stale elevation after the control
    # renderer changes.
    ("controls", m2_controls),
    ("locations", gen_locations),
    ("definitions", gen_definitions),
    ("heightmap", gen_heightmap),
    ("materials", gen_arda_materials),
    ("terrain_cache", gen_terrain_cache),
    ("rivers", gen_rivers),
    ("adjacencies", gen_adjacencies),
    ("map_config", gen_map_config),
    ("flatmap", gen_flatmap),
    ("border_style", gen_border_style),
    ("map_objects", gen_map_objects),
    ("locators", gen_locators),
    ("runtime", m2_runtime),
    ("quarantine", m2_quarantine),
    ("realms", m3_realms),
    ("peoples", m4_peoples),
    ("census", m5_census),
    # Templates join M3/M4/M5 outputs. Keeping this last prevents an early
    # raw-material lookup from caching a political/census state belonging to
    # the previous control geometry during a full rewrite.
    ("templates", gen_location_templates),
)

PINNED_TOOLCHAIN = {
    "Pillow": "12.3.0",
    "numpy": "2.4.6",
}


def assert_pinned_toolchain() -> None:
    """Refuse byte-different world writes/checks from an unpinned raster stack."""

    actual = {
        "Pillow": PIL.__version__,
        "numpy": np.__version__,
    }
    if actual != PINNED_TOOLCHAIN:
        expected_text = ", ".join(
            f"{name}=={version}" for name, version in PINNED_TOOLCHAIN.items()
        )
        actual_text = ", ".join(
            f"{name}=={version}" for name, version in actual.items()
        )
        raise RuntimeError(
            "M2 deterministic raster toolchain mismatch: expected "
            f"{expected_text}; found {actual_text}. Run through "
            ".venv\\Scripts\\python.exe or gmake."
        )


def write() -> None:
    started = time.monotonic()
    for name, module in STAGES:
        print(f"m2_world: writing {name}")
        module.write()
    print(f"m2_world: WRITE PASS in {time.monotonic() - started:.1f}s")


def check() -> list[str]:
    failures: list[str] = []
    for name, module in STAGES:
        stage_failures = module.check()
        if stage_failures:
            failures.extend(f"{name}: {failure}" for failure in stage_failures)
        else:
            print(f"m2_world: {name} PASS")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    assert_pinned_toolchain()
    if args.write:
        write()
        return 0
    started = time.monotonic()
    failures = check()
    if failures:
        for failure in failures:
            print(f"m2_world: FAIL {failure}")
        return 1
    print(f"m2_world: PASS in {time.monotonic() - started:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
