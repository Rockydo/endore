#!/usr/bin/env python3
"""Regression tests for bounded EU5 menu-transition automation."""

from __future__ import annotations

import tempfile
import sys
from pathlib import Path

from PIL import Image, ImageDraw

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from gamedriver import (
    mainmenu_game_transition_state,
    observer_frame_state,
    observer_pause_banner,
)


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

        # A red political-map patch can cover the centered pause-banner crop
        # while country selection is still active. It must never prove that a
        # live Observer game exists without the independent top-left HUD.
        lobby = Image.new("RGB", (1000, 600), (120, 135, 100))
        lobby_draw = ImageDraw.Draw(lobby)
        lobby_draw.rectangle((420, 96, 580, 144), fill=(135, 18, 12))
        paused, _ = observer_pause_banner(lobby)
        require(paused, "synthetic lobby must exercise the red-banner ambiguity")
        live, paused, *_ = observer_frame_state(lobby)
        require(not live, "red lobby paint must not pass the live Observer gate")
        require(not paused, "red lobby paint must not trigger Observer resume")

        live_frame = lobby.copy()
        live_draw = ImageDraw.Draw(live_frame)
        live_draw.rectangle((5, 42, 325, 93), fill=(20, 20, 20))
        live_draw.rectangle((18, 52, 58, 72), fill=(235, 235, 235))
        live, paused, *_ = observer_frame_state(live_frame)
        require(live, "the independent Observer HUD must pass the live-game gate")
        require(paused, "a HUD-backed pause banner must remain resumable")
    print("test_gamedriver: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
