#!/usr/bin/env python3
"""Canonical ENDORE validation and smoke command runner."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Command:
    script: str
    args: tuple[str, ...] = ()

    def argv(self) -> list[str]:
        return [sys.executable, str(ROOT / self.script), *self.args]


VALIDATE_COMMANDS = (
    Command("tools/test_eu5_slot.py"),
    Command("tools/test_gamedriver.py"),
    Command("tools/cartography_reference_audit.py", ("--check",)),
    Command("tools/m2_controls.py", ("--check",)),
    Command("tools/m2_world.py", ("--check",)),
    Command("tools/pdxlint.py"),
)
SMOKE_COMMANDS = (Command("tools/smoketest.py"),)


def run(label: str, commands: tuple[Command, ...]) -> int:
    print(f"{label}: {len(commands)} command(s)")
    for index, command in enumerate(commands, 1):
        path = ROOT / command.script
        if not path.is_file():
            print(f"{label}: FAIL missing {command.script}", file=sys.stderr)
            return 2
        print(f"[{index}/{len(commands)}] {command.script}")
        completed = subprocess.run(command.argv(), cwd=ROOT, check=False)
        if completed.returncode:
            if completed.returncode == 75:
                print(
                    f"{label}: DEFERRED — shared EU5 slot is busy",
                    file=sys.stderr,
                )
            else:
                print(f"{label}: FAIL", file=sys.stderr)
            return completed.returncode
    print(f"{label}: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", choices=("validate", "smoke", "full"))
    args = parser.parse_args()
    if args.target == "validate":
        return run("validate", VALIDATE_COMMANDS)
    if args.target == "smoke":
        return run("smoke", SMOKE_COMMANDS)
    result = run("validate", VALIDATE_COMMANDS)
    return result or run("smoke", SMOKE_COMMANDS)


if __name__ == "__main__":
    raise SystemExit(main())
