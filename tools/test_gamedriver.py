#!/usr/bin/env python3
"""Regression tests for bounded EU5 menu-transition automation."""

from __future__ import annotations

import tempfile
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from gamedriver import mainmenu_game_transition_state


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def write(path: Path, *lines: str) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(dir="G:\\") as directory:
        debug = Path(directory) / "debug.log"
        require(
            mainmenu_game_transition_state(debug) == "not-started",
            "missing log must not pass menu initialization",
        )
        write(
            debug,
            "[00:00:01] Transition LoadingScreen->MainMenu started",
            "[00:00:02] Transition MainMenu->Game started",
        )
        require(
            mainmenu_game_transition_state(debug) == "active",
            "startup MainMenu->Game state 1 must be recognized for a joined load",
        )
        write(
            debug,
            "[00:00:02] Transition MainMenu->Game started",
            "[00:00:30] Running OnTransitionStateChanged callback for state 4, "
            "transition: MainMenu->Game",
            "[00:00:30] Setting Task state 4",
        )
        require(
            mainmenu_game_transition_state(debug) == "complete",
            "state-4 callback must release the menu gate",
        )
        write(
            debug,
            "[00:00:02] Transition MainMenu->Game started",
            "[00:00:30] Running OnTransitionStateChanged callback for state 4, "
            "transition: MainMenu->Game",
            "[00:01:00] Transition MainMenu->Game started",
        )
        require(
            mainmenu_game_transition_state(debug) == "active",
            "a later transaction must supersede an earlier completion",
        )
    print("test_gamedriver: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
