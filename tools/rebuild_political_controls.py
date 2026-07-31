#!/usr/bin/env python3
"""Reproject M3 landmarks and realm seats into the source-audited map frame.

Raw Arda Maps and ArdaCraft payloads remain quarantined under G:\endore_runtime.
This development-only authoring tool records only point measurements and their
provenance in the committed CSV controls.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rebuild_cartography_controls import Topology, endore_from_arda_maps

ROOT = Path(__file__).resolve().parents[1]
LANDMARKS = ROOT / "docs/world/control/m3_landmarks.csv"
SETTLEMENTS = ROOT / "docs/world/control/settlements.csv"
REALMS = ROOT / "docs/world/realms.csv"
DEFAULT_REFERENCE_ROOT = Path(r"G:\endore_runtime\cartography_references")
ARDA_MAPS_SHA256 = (
    "147a2d0ff3e36e2b675afb40dd4a74f634006bc6350a6a7c31639019fd2bd4ab"
)
ARDACRAFT_MARKERS_SHA256 = (
    "310d3cabb98fb48a54e3ae62f5d575d8e25ef07641e2b824d5834a569e45547a"
)


def normalized(value: str) -> str:
    folded = unicodedata.normalize("NFKD", value)
    return "".join(character for character in folded.lower() if character.isalnum())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def marker_index(markers: list[dict]) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for marker in markers:
        key = normalized(marker["title"])
        if key in result:
            raise ValueError(f"duplicate normalized ArdaCraft marker {key}")
        result[key] = marker
    return result


def endore_from_marker(marker: dict) -> list[float]:
    return [
        round(0.5 + (float(marker["x"]) - 10651.5) / 86014.0, 6),
        round((float(marker["z"]) + 10240.0) / 43007.0, 6),
    ]


def arda_maps_indexes(source: dict) -> tuple[dict[str, list[float]], dict[str, list[float]]]:
    scale_x, scale_y = source["transform"]["scale"]
    translate_x, translate_y = source["transform"]["translate"]
    points: dict[str, list[float]] = {}
    for collection in (
        "point_city",
        "point_place",
        "point_waterfall",
        "point_bridge",
        "point_mount",
        "point_ford",
        "point_castletower",
    ):
        for geometry in source["objects"][collection]["geometries"]:
            name = (geometry.get("properties") or {}).get("eventname")
            if not name:
                continue
            x, y = geometry["coordinates"]
            points[normalized(name)] = endore_from_arda_maps(
                x * scale_x + translate_x,
                y * scale_y + translate_y,
            )

    topology = Topology(source)
    text: dict[str, list[float]] = {}
    for geometry in source["objects"]["line_text"]["geometries"]:
        properties = geometry.get("properties") or {}
        name = properties.get("eventname") or properties.get("name_EN")
        if not name:
            continue
        line = [point for part in topology.line_parts(geometry) for point in part]
        if not line:
            continue
        text[normalized(name)] = [
            round(sum(point[0] for point in line) / len(line), 6),
            round(sum(point[1] for point in line) / len(line), 6),
        ]
    return points, text


# Exact source features are preferred. "manual" entries exist only where canon
# names no fixed seat or where two adjacent source controls define a feature.
SPECS: dict[str, tuple[str, str | tuple[float, float], str]] = {
    "the_angle": ("manual", (0.475000, 0.270000), "Reconciled: Angle between Mitheithel and Bruinen"),
    "blue_halls": ("craft", "Thorin's Hall", "ArdaCraft: Thorin's Hall proxy for surviving Ered Luin halls"),
    "iron_hills": ("text", "IronMountains", "Arda Maps: Iron Mountains / Iron Hills label"),
    "woodmen_hall": ("manual", (0.562000, 0.300000), "Judgment: western Mirkwood Woodmen seat"),
    "wellinghall": ("craft", "Derndingle", "ArdaCraft: Derndingle"),
    "ghans_glade": ("craft", "Drúadan Forest", "ArdaCraft: Drúadan Forest"),
    "forochel_camp": ("manual", (0.340000, 0.035000), "Judgment: playable Icebay shore within source Forochel"),
    "rhosgobel": ("craft", "Rhosgobel", "ArdaCraft: Rhosgobel"),
    "harnenhold": ("text", "Harnen", "Arda Maps: River Harnen"),
    "qarsad": ("manual", (0.675000, 0.870000), "Judgment: unnamed inland Harad seat"),
    "mumak_gate": ("manual", (0.585000, 0.955000), "Judgment: on-map Far Harad fringe"),
    "khazan": ("text", "Khand", "Arda Maps: Khand label"),
    "burh_gath": ("manual", (0.770000, 0.250000), "Judgment: western Rhûn at the source Rhûn label"),
    "wainhold": ("manual", (0.800000, 0.350000), "Judgment: southeastern Rhûn beyond the Sea of Rhûn"),
    "eastern_march": ("manual", (0.820000, 0.200000), "Judgment: eastern edge of represented Rhûn"),
    "dunland_moot": ("text", "Dunland", "Arda Maps: Dunland label"),
    "mount_gram": ("manual", (0.448000, 0.145000), "Judgment: Mount Gram within northern Eriador"),
    "tharbad": ("craft", "Tharbad", "ArdaCraft: Tharbad"),
    "ost_in_edhil": ("craft", "Ost-in-Edhil", "ArdaCraft: Ost-in-Edhil"),
    "lond_daer": ("craft", "Lond Daer", "ArdaCraft: Lond Daer"),
    "methedras": ("point", "Methedras", "Arda Maps: Methedras"),
    "derndingle": ("craft", "Derndingle", "ArdaCraft: Derndingle"),
    "celebrant": ("craft", "Parth Celebrant", "ArdaCraft: Parth Celebrant"),
    "rauros": ("craft", "Falls of Rauros", "ArdaCraft: Falls of Rauros"),
    "amon_hen": ("craft", "Amon Hen", "ArdaCraft: Amon Hen"),
    "amon_lhaw": ("craft", "Amon Lhaw", "ArdaCraft: Amon Lhaw"),
    "argonauth": ("craft", "Argonath", "ArdaCraft: Argonath"),
    "cair_andros": ("craft", "Cair Andros", "ArdaCraft: Cair Andros"),
    "henneth_annun": ("craft", "Henneth Annűn", "ArdaCraft: Henneth Annûn"),
    "emyn_arnen": ("text", "EmynArnen", "Arda Maps: Emyn Arnen label"),
    "cross_roads": ("manual", (0.600000, 0.605000), "Reconciled: Osgiliath–Minas Morgul road junction"),
    "cirith_ungol": ("craft", "Cirith Ungol", "ArdaCraft: Cirith Ungol"),
    "shelobs_lair": ("point", "ShelobsLair", "Arda Maps: Shelob's Lair"),
    "durthang": ("point", "Durthang", "Arda Maps: Durthang"),
    "narchost": ("manual", (0.606500, 0.529500), "Reconciled: western Tower of the Teeth at Morannon"),
    "carchost": ("manual", (0.613000, 0.529500), "Reconciled: eastern Tower of the Teeth at Morannon"),
    "udun": ("craft", "Udűn", "ArdaCraft: Udûn"),
    "gorgoroth": ("text", "PlateauOfGorgoroth", "Arda Maps: Plateau of Gorgoroth"),
    "nurn": ("text", "Nurn", "Arda Maps: Nurn label"),
    "lithlad": ("text", "Lithlad", "Arda Maps: Lithlad label"),
    "dead_marshes": ("text", "DeadMarshes", "Arda Maps: Dead Marshes"),
    "dagorlad": ("text", "Dagorlad", "Arda Maps: Dagorlad"),
    "tolfalas": ("text", "Tolfalas", "Arda Maps: Tolfalas"),
    "edhellond": ("point", "Edhellond", "Arda Maps: Edhellond"),
    "pinnath_gelin": ("text", "PinnathGelin", "Arda Maps: Pinnath Gelin"),
    "lamedon": ("text", "Lamedon", "Arda Maps: Lamedon"),
    "lossarnach": ("craft", "Imloth Melui", "ArdaCraft: Imloth Melui in Lossarnach"),
    "harlond_gondor": ("craft", "Harlond (Gondor)", "ArdaCraft: Harlond of Gondor"),
    "rammas_echor": ("craft", "Rammas Echor", "ArdaCraft: Rammas Echor"),
    "stonewain_valley": ("craft", "Stonewain Road", "ArdaCraft: Stonewain Road"),
    "paths_of_dead": ("point", "PathsOfTheDead", "Arda Maps: Paths of the Dead"),
    "halifirien": ("craft", "Halifirien (Amon Anwar)", "ArdaCraft: Halifirien"),
    "fords_of_isen": ("craft", "Fords of Isen", "ArdaCraft: Fords of Isen"),
    "firien_wood": ("text", "Firienholt", "Arda Maps: Firienholt"),
    "gladden_fields": ("text", "GladdenFields", "Arda Maps: Gladden Fields"),
    "old_forest": ("text", "OldForest", "Arda Maps: Old Forest"),
    "barrow_downs": ("text", "BarrowDowns", "Arda Maps: Barrow-downs"),
    "sarn_ford": ("craft", "Sarn Ford", "ArdaCraft: Sarn Ford"),
    "brandywine_bridge": ("point", "BrandywineBridge", "Arda Maps: Brandywine Bridge"),
    "mountains_of_mirkwood": ("text", "MountainsOfMirkwood", "Arda Maps: Mountains of Mirkwood"),
    "withered_heath": ("text", "WitheredHeath", "Arda Maps: Withered Heath"),
    "grey_mountain_holds": ("text", "GreyMountains", "Arda Maps: Grey Mountains"),
}


def resolve(
    spec: tuple[str, str | tuple[float, float], str],
    craft: dict[str, dict],
    points: dict[str, list[float]],
    text: dict[str, list[float]],
) -> tuple[list[float], str]:
    kind, value, provenance = spec
    if kind == "manual":
        x, y = value
        return [float(x), float(y)], provenance
    key = normalized(str(value))
    if kind == "craft":
        return endore_from_marker(craft[key]), provenance
    if kind == "point":
        return points[key], provenance
    if kind == "text":
        return text[key], provenance
    raise ValueError(f"unknown cartography source kind {kind}")


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rebuild(reference_root: Path) -> tuple[int, int]:
    arda_maps_path = reference_root / "arda_maps_third_age.json"
    markers_path = reference_root / "ardacraft_canon_markers.json"
    if sha256(arda_maps_path) != ARDA_MAPS_SHA256:
        raise ValueError("Arda Maps source hash changed")
    if sha256(markers_path) != ARDACRAFT_MARKERS_SHA256:
        raise ValueError("ArdaCraft marker source hash changed")

    source = json.loads(arda_maps_path.read_text(encoding="utf-8"))
    craft = marker_index(json.loads(markers_path.read_text(encoding="utf-8")))
    points, text = arda_maps_indexes(source)

    with LANDMARKS.open("r", encoding="utf-8-sig", newline="") as handle:
        landmark_rows = list(csv.DictReader(handle))
    refs = {row["ref"] for row in landmark_rows}
    if refs != set(SPECS):
        raise ValueError(
            f"landmark specification mismatch: missing={sorted(refs - set(SPECS))}, "
            f"extra={sorted(set(SPECS) - refs)}"
        )
    for row in landmark_rows:
        coordinate, provenance = resolve(SPECS[row["ref"]], craft, points, text)
        row["x"], row["y"] = (f"{value:.6f}" for value in coordinate)
        row["cartography_reference"] = provenance
    write_csv(
        LANDMARKS,
        landmark_rows,
        ["ref", "name", "x", "y", "rank", "source", "cartography_reference"],
    )

    controls: dict[str, tuple[str, str]] = {
        row["ref"]: (row["x"], row["y"]) for row in landmark_rows
    }
    with SETTLEMENTS.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            controls[row["key"]] = (row["x"], row["y"])
    with REALMS.open("r", encoding="utf-8-sig", newline="") as handle:
        realm_reader = csv.DictReader(handle)
        realm_fields = list(realm_reader.fieldnames or [])
        realm_rows = list(realm_reader)
    for row in realm_rows:
        try:
            row["x"], row["y"] = controls[row["capital_ref"]]
        except KeyError as exc:
            raise ValueError(f"unresolved realm capital {row['capital_ref']}") from exc
    write_csv(REALMS, realm_rows, realm_fields)
    return len(landmark_rows), len(realm_rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", required=True)
    parser.add_argument(
        "--reference-root",
        type=Path,
        default=DEFAULT_REFERENCE_ROOT,
    )
    args = parser.parse_args()
    landmarks, realms = rebuild(args.reference_root)
    print(
        "rebuild_political_controls: wrote "
        f"{landmarks} landmarks and synchronized {realms} realm seats"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
