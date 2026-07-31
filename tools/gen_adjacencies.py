#!/usr/bin/env python3
"""Generate/check M2 ports and explicit offshore-island adjacencies."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worldgen import (
    CONTROL_H,
    CONTROL_W,
    MAP_OUT,
    WORLD_H,
    WORLD_W,
    WorldModel,
    build_model,
    coastal_edges,
)

PORTS_OUT = MAP_OUT / "ports.csv"
ADJACENCIES_OUT = MAP_OUT / "adjacencies.csv"


def control_point(x: float, y: float) -> tuple[int, int]:
    return round(y * (CONTROL_H - 1)), round(x * (CONTROL_W - 1))


def label_at(model: WorldModel, x: float, y: float) -> int:
    cy, cx = control_point(x, y)
    return int(model.labels[cy, cx])


def port_coordinate(edge: tuple[int, int, int, int]) -> tuple[int, int]:
    y, x, wy, wx = edge
    scale_x, scale_y = WORLD_W // CONTROL_W, WORLD_H // CONTROL_H
    if wy == y:
        px = wx * scale_x if wx > x else (wx + 1) * scale_x - 1
        py = y * scale_y + scale_y // 2
    else:
        px = x * scale_x + scale_x // 2
        py = wy * scale_y if wy > y else (wy + 1) * scale_y - 1
    return px, WORLD_H - py


def matched_port_edges(
    edges: dict[int, dict[int, tuple[int, int, int, int]]],
) -> list[tuple[int, int, tuple[int, int, int, int]]]:
    water_to_lands: dict[int, dict[int, tuple[int, int, int, int]]] = {}
    for land, waters in edges.items():
        for water, edge in waters.items():
            water_to_lands.setdefault(water, {})[land] = edge

    land_match: dict[int, int] = {}

    def match_water(water: int, visited: set[int]) -> bool:
        for land in sorted(water_to_lands[water]):
            if land in visited:
                continue
            visited.add(land)
            previous = land_match.get(land)
            if previous is None or match_water(previous, visited):
                land_match[land] = water
                return True
        return False

    unmatched = [
        water
        for water in sorted(water_to_lands)
        if not match_water(water, set())
    ]
    if unmatched:
        details = ", ".join(
            f"{water}:{len(water_to_lands[water])}"
            for water in unmatched
        )
        raise ValueError(
            "cannot give coastal water zones unique ports "
            f"(water:candidate-land-count {details})"
        )

    result: list[tuple[int, int, tuple[int, int, int, int]]] = []
    for land in sorted(edges):
        water = land_match.get(land, min(edges[land]))
        result.append((land, water, edges[land][water]))
    return result


def ports_text(model: WorldModel) -> str:
    rows = ["LandProvince;SeaZone;x;y;"]
    for land, water, edge in matched_port_edges(coastal_edges(model)):
        px, py = port_coordinate(edge)
        rows.append(
            f"{model.locations[land].key};{model.locations[water].key};{px};{py};x"
        )

    # Live M2 evidence: EU5's dock validator accepts sea_zones only. Esgaroth
    # remains a lakeshore location, but Long Lake cannot be a naval port.
    # The EU5 CSV parser treats a terminal blank record as an empty location
    # reference on a custom canvas. Match M1/vanilla row termination exactly.
    return "\n".join(rows)


def adjacency_rows(model: WorldModel) -> list[str]:
    authored = (
        (
            "Himling crossing",
            (0.203800, 0.052600),
            (0.246500, 0.085000),
            (0.235900, 0.073800),
        ),
        (
            "Tolfalas crossing",
            (0.522660, 0.744400),
            (0.525500, 0.715000),
            (0.526000, 0.723000),
        ),
    )
    rows: list[str] = []
    for comment, start, stop, through in authored:
        start_index = label_at(model, *start)
        stop_index = label_at(model, *stop)
        through_index = label_at(model, *through)
        start_location = model.locations[start_index]
        stop_location = model.locations[stop_index]
        water_location = model.locations[through_index]
        if start_location.kind != "land" or stop_location.kind != "land":
            raise ValueError(f"{comment} endpoints do not both resolve to land")
        if water_location.kind != "sea":
            raise ValueError(f"{comment} does not resolve through a sea zone")
        sx, sy = (
            round(start[0] * (WORLD_W - 1)),
            WORLD_H - round(start[1] * (WORLD_H - 1)),
        )
        tx, ty = (
            round(stop[0] * (WORLD_W - 1)),
            WORLD_H - round(stop[1] * (WORLD_H - 1)),
        )
        rows.append(
            f"{start_location.key};{stop_location.key};sea;{water_location.key};"
            f"{sx};{sy};{tx};{ty};{comment}"
        )
    return rows


def adjacencies_text(model: WorldModel) -> str:
    # Live A/B evidence: this build emits one empty-location lookup whenever a
    # custom-canvas adjacencies.csv is non-empty, even with vanilla-formatted,
    # fully resolved rows. Preserve the authored candidates in adjacency_rows()
    # but package the proven zero-byte fallback until the editor path is solved.
    return ""


def write() -> None:
    model = build_model()
    MAP_OUT.mkdir(parents=True, exist_ok=True)
    ports = ports_text(model)
    PORTS_OUT.write_text(ports, encoding="utf-8")
    ADJACENCIES_OUT.write_text(adjacencies_text(model), encoding="utf-8")
    print(
        f"gen_adjacencies: wrote {ports.count(chr(10))} ports; "
        f"{len(adjacency_rows(model))} island crossings retained as gated candidates"
    )


def check() -> list[str]:
    model = build_model()
    expected = {
        PORTS_OUT: ports_text(model),
        ADJACENCIES_OUT: adjacencies_text(model),
    }
    failures: list[str] = []
    for path, text in expected.items():
        if not path.is_file():
            failures.append(f"missing in_game/map_data/{path.name}")
        elif path.read_text(encoding="utf-8") != text:
            failures.append(f"{path.name} differs from deterministic coast model")
        elif path.read_bytes().startswith(b"\xef\xbb\xbf"):
            failures.append(f"{path.name} must match vanilla's BOM-free CSV contract")
    if ADJACENCIES_OUT.read_bytes() != b"":
        failures.append("adjacencies.csv must remain the proven zero-byte M2 fallback")
    port_lands = [
        line.split(";", 1)[0]
        for line in expected[PORTS_OUT].splitlines()[1:]
    ]
    if len(port_lands) != len(set(port_lands)):
        failures.append("ports.csv assigns more than one port to a land location")
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
            print(f"gen_adjacencies: FAIL {failure}")
        return 1
    print("gen_adjacencies: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
