#!/usr/bin/env python3
"""Regression tests for bounded EU5 menu-transition automation."""

from __future__ import annotations

import json
import tempfile
import sys
from pathlib import Path

from PIL import Image, ImageDraw

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from gamedriver import (
    camera_delta_ratio,
    load_game_panel_state,
    main_menu_new_game_button_state,
    mainmenu_game_transition_state,
    observer_confirmation_dialog_state,
    observer_frame_state,
    observer_pause_banner,
    observer_start_button_state,
    observer_toggle_ready,
    set_player_visual_settings,
    transition_completion_signal,
)
from smoketest import restore_settings, runtime_link_needs_repair, settings_snapshot


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def write(path: Path, *lines: str) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    require(
        runtime_link_needs_repair(
            {
                "mod_dir": "",
                "user_dir": r"G:\endore_user_data",
                "candidate_relocated_user_dir": r"G:\endore_user_data",
            }
        ),
        "an empty mod path must never resolve to the repository as configured",
    )
    require(
        runtime_link_needs_repair(
            {
                "mod_dir": ".",
                "user_dir": r"C:\Users\Alvin\Documents\Paradox Interactive\Europa Universalis V",
                "candidate_relocated_user_dir": r"G:\endore_user_data",
            }
        ),
        "a valid mod path must not excuse the default C: user directory",
    )
    require(
        not runtime_link_needs_repair(
            {
                "mod_dir": ".",
                "user_dir": r"G:\endore_user_data",
                "candidate_relocated_user_dir": r"G:\endore_user_data",
            }
        ),
        "an existing mod path and matching relocated user directory must pass",
    )
    with tempfile.TemporaryDirectory(dir="G:\\") as directory:
        settings = Path(directory) / "pdx_settings.json"
        original_settings = {
            "Audio": {"personal_volume": 0.37},
            "Graphics": {"display_mode": "fullscreen"},
            "Terrain": {
                "3d_terrain_disable": True,
                "triplanar_uv_quality": "disabled",
            },
        }
        settings.write_text(json.dumps(original_settings), encoding="utf-8")
        snapshot = settings_snapshot(settings)
        set_player_visual_settings(settings.parent)
        visual_settings = json.loads(settings.read_text(encoding="utf-8"))
        require(
            visual_settings["Terrain"]["3d_terrain_disable"] is False,
            "the player visual profile must enable physical terrain",
        )
        require(
            visual_settings["Terrain"]["triplanar_uv_quality"] == "medium",
            "the player visual profile must enable terrain material projection",
        )
        require(
            visual_settings["Audio"] == original_settings["Audio"],
            "the player visual profile must preserve personal audio settings",
        )
        require(
            visual_settings["Graphics"]["display_mode"] == "fullscreen",
            "the player visual profile must preserve personal display mode",
        )
        restore_settings(settings, snapshot)
        require(
            json.loads(settings.read_text(encoding="utf-8")) == original_settings,
            "smoke settings restoration must reproduce the exact player payload",
        )

        unchanged = Image.new("RGB", (1000, 600), (42, 80, 36))
        require(
            camera_delta_ratio(unchanged, unchanged.copy()) == 0.0,
            "an unchanged Finder frame must never prove a camera transition",
        )
        moved = unchanged.copy()
        moved_draw = ImageDraw.Draw(moved)
        moved_draw.rectangle((350, 200, 650, 400), fill=(130, 90, 30))
        require(
            camera_delta_ratio(unchanged, moved) > 0.002,
            "a material map-camera change must exceed the Finder delta floor",
        )

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

        require(
            transition_completion_signal(False, False, 60, 15, 0) is None,
            "quiet logs without completion markers must not pass",
        )
        require(
            transition_completion_signal(True, False, 60, 15, 0) is None,
            "state 4 alone must not pass the logged completion route",
        )
        require(
            transition_completion_signal(True, True, 14.9, 15, 0) is None,
            "cache completion must remain quiet for the configured settle time",
        )
        require(
            transition_completion_signal(True, True, 15, 15, 0) == "log",
            "state 4, cache completion, and log quiet must pass",
        )
        require(
            transition_completion_signal(False, False, 0, 15, 4.9) is None,
            "an unstable country-selection frame must not pass",
        )
        require(
            transition_completion_signal(False, False, 0, 15, 5)
            == "country-selection",
            "a stable country-selection frame must recover missed log markers",
        )

        neutral_menu = Image.new("RGB", (1000, 600), (70, 75, 72))
        still_menu, *_ = main_menu_new_game_button_state(neutral_menu)
        load_panel, *_ = load_game_panel_state(neutral_menu)
        require(not still_menu, "neutral paint must not mimic the New Game button")
        require(not load_panel, "neutral paint must not mimic the Load Game panel")

        ready_menu = neutral_menu.copy()
        ready_menu_draw = ImageDraw.Draw(ready_menu)
        ready_menu_draw.rectangle((55, 213, 200, 249), fill=(125, 78, 18))
        still_menu, *_ = main_menu_new_game_button_state(ready_menu)
        load_panel, *_ = load_game_panel_state(ready_menu)
        require(still_menu, "the warm New Game button must prove a retained menu")
        require(not load_panel, "the ready menu must not mimic the save-list page")

        save_list = neutral_menu.copy()
        save_list_draw = ImageDraw.Draw(save_list)
        save_list_draw.rectangle((50, 504, 210, 534), fill=(32, 68, 118))
        still_menu, *_ = main_menu_new_game_button_state(save_list)
        load_panel, *_ = load_game_panel_state(save_list)
        require(not still_menu, "the save-list page must not mimic New Game")
        require(load_panel, "the blue Back control must identify Load Game")

        neutral_ui = Image.new("RGB", (1000, 600), (110, 120, 95))
        confirmation, *_ = observer_confirmation_dialog_state(neutral_ui)
        require(not confirmation, "plain political-map paint must not mimic a dialog")
        start_visible, *_ = observer_start_button_state(neutral_ui)
        require(not start_visible, "plain political-map paint must not mimic Start")

        confirmation_ui = neutral_ui.copy()
        confirmation_draw = ImageDraw.Draw(confirmation_ui)
        confirmation_draw.rectangle((320, 324, 680, 372), fill=(35, 35, 35))
        confirmation_draw.rectangle((340, 333, 500, 350), fill=(52, 76, 112))
        confirmation, *_ = observer_confirmation_dialog_state(confirmation_ui)
        require(confirmation, "the Observer confirmation button row must be detected")

        start_ui = neutral_ui.copy()
        start_draw = ImageDraw.Draw(start_ui)
        start_draw.rectangle((400, 480, 600, 546), fill=(45, 40, 30))
        start_draw.rectangle((410, 490, 590, 536), fill=(145, 105, 45))
        start_draw.rectangle((420, 498, 580, 528), fill=(55, 45, 30))
        start_visible, *_ = observer_start_button_state(start_ui)
        require(start_visible, "the gold Observer start control must be detected")

        vanilla_start_ui = neutral_ui.copy()
        vanilla_start_draw = ImageDraw.Draw(vanilla_start_ui)
        vanilla_start_draw.rectangle((400, 480, 600, 546), fill=(42, 36, 28))
        vanilla_start_draw.rectangle((410, 490, 590, 526), fill=(166, 122, 48))
        vanilla_start_draw.rectangle((420, 497, 580, 519), fill=(72, 53, 31))
        start_visible, *_ = observer_start_button_state(vanilla_start_ui)
        require(start_visible, "the brighter vanilla Observer start control must be detected")
        require(
            not observer_toggle_ready(False, True),
            "a gold country-selection button must not authorize Observer start",
        )
        require(
            observer_toggle_ready(True, True),
            "an accepted Observer confirmation plus start control must authorize start",
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
