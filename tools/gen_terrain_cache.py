#!/usr/bin/env python3
"""Bake/check ENDÓRË's self-contained EU5 terrain virtual-texture cache.

Installed-game evidence shows that the four ``terrain_cache/*.bin`` payloads
are concatenated 132x132 PNG tiles.  Their companion ``.info`` files index a
complete 128-pixel-tile mip pyramid over a 65536x32768 virtual surface.

The retail cache contains Earth's decal-baked relief and materials.  Letting
those paths fall through the VFS therefore leaks Earth back into a custom map
at close zoom.  This generator owns the complete cache contract:

* ``heightmap`` is sampled from ENDÓRË's authored 16-bit height source;
* ``materials`` is an explicit empty 16-bit layer;
* ``index_map`` and ``intensity_map`` contain no decal references;
* ``quadtree_nodes`` is the engine's geometry-independent full zero tree.

No installed-game payload is copied.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import re
import struct
import sys
import time
import zlib
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worldgen import TERRAIN_OUT

ROOT = Path(__file__).resolve().parents[1]
CACHE_OUT = TERRAIN_OUT / "terrain_cache"
HEIGHT_SOURCE = TERRAIN_OUT / "heightmap.png"
MANIFEST_OUT = CACHE_OUT / "endore_terrain_cache_manifest.json"

SOURCE_W = 65_536
SOURCE_H = 32_768
TILE_SIZE = 128
BORDER_SIZE = 2
STORED_TILE_SIZE = TILE_SIZE + BORDER_SIZE * 2
HEIGHT_QUANTUM = 512
GENERATOR_VERSION = 7

# quadtree_nodes.bin is a full 12-level geometry-independent quadtree.  The
# installed file's 20-byte header describes 5,592,405 zeroed 12-byte records.
QUADTREE_DEPTH = 12
QUADTREE_RECORDS = 5_592_405
QUADTREE_LEAF_OFFSET = 1_398_101
QUADTREE_FLAGS = 33
QUADTREE_DIMENSIONS = 65_537
QUADTREE_HEADER_SIZE = 20
QUADTREE_RECORD_SIZE = 12

INFO_HEADER = (
    f"source_resolution={{ {SOURCE_W} {SOURCE_H} }}\n"
    f"tile_size={TILE_SIZE}\n"
    f"border_size={BORDER_SIZE}\n"
)
SCALAR_INFO_FIELDS = (
    "num_channels=1\n"
    "bytes_per_channel=2\n"
    "empty_value={ 0 0 0 0 }\n"
    "raw=no\n"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pyramid_layout() -> list[tuple[int, int, int]]:
    """Return the engine's finest-to-coarsest mip groups."""
    fine_to_coarse: list[tuple[int, int, int]] = []
    mip = 0
    tiles_x = math.ceil(SOURCE_W / TILE_SIZE)
    tiles_y = math.ceil(SOURCE_H / TILE_SIZE)
    while True:
        fine_to_coarse.append((mip, tiles_x, tiles_y))
        if tiles_x == 1 and tiles_y == 1:
            return fine_to_coarse
        tiles_x = max(1, math.ceil(tiles_x / 2))
        tiles_y = max(1, math.ceil(tiles_y / 2))
        mip += 1


def tile_count() -> int:
    return sum(width * height for _, width, height in pyramid_layout())


def morton_coordinates(tiles_x: int, tiles_y: int) -> list[tuple[int, int]]:
    """Return Z-order coordinates for one 2:1 mip group."""
    if tiles_x == tiles_y == 1:
        return [(0, 0)]
    if tiles_x != tiles_y * 2 or tiles_y & (tiles_y - 1):
        raise AssertionError(
            f"unsupported virtual-texture mip dimensions {tiles_x}x{tiles_y}"
        )
    coordinates: list[tuple[int, int]] = []
    bits = tiles_y.bit_length() - 1
    for half in range(2):
        for code in range(tiles_y * tiles_y):
            x = 0
            y = 0
            for bit in range(bits):
                x |= ((code >> (2 * bit)) & 1) << bit
                y |= ((code >> (2 * bit + 1)) & 1) << bit
            coordinates.append((x + half * tiles_y, y))
    return coordinates


def engine_tile_sequence() -> list[tuple[int, int, int]]:
    """Return EU5's fine-first row order with source Y stored bottom-up."""
    return [
        (mip, x, tiles_y - 1 - info_y)
        for mip, tiles_x, tiles_y in pyramid_layout()
        for info_y in range(tiles_y)
        for x in range(tiles_x)
    ]


def morton_tile_sequence() -> list[tuple[int, int, int]]:
    """Return the incorrect v5 traversal solely for lossless migration."""
    return [
        (mip, x, y)
        for mip, tiles_x, tiles_y in pyramid_layout()
        for x, y in morton_coordinates(tiles_x, tiles_y)
    ]


def preorder_tile_sequence() -> list[tuple[int, int, int]]:
    """Return the incorrect v4 traversal solely for lossless migration."""
    layout = {mip: (width, height) for mip, width, height in pyramid_layout()}
    root_mip = max(layout)
    result: list[tuple[int, int, int]] = [(root_mip, 0, 0)]

    def visit(mip: int, x: int, y: int) -> None:
        result.append((mip, x, y))
        if mip == 0:
            return
        child_mip = mip - 1
        for child_x, child_y in (
            (x * 2, y * 2),
            (x * 2 + 1, y * 2),
            (x * 2, y * 2 + 1),
            (x * 2 + 1, y * 2 + 1),
        ):
            visit(child_mip, child_x, child_y)

    # The 65536x32768 surface is one global root above two 32768-square
    # quadtrees. Each square is stored fully depth-first before its sibling.
    visit(root_mip - 1, 0, 0)
    visit(root_mip - 1, 1, 0)
    if len(result) != tile_count():
        raise AssertionError(
            f"virtual-texture traversal has {len(result):,} nodes, "
            f"expected {tile_count():,}"
        )
    return result


def png_bytes(array: np.ndarray) -> bytes:
    image = Image.fromarray(array)
    output = io.BytesIO()
    image.save(output, format="PNG", compress_level=9, optimize=False)
    return output.getvalue()


def write_info(
    path: Path,
    entries: list[tuple[int, int]],
    *,
    scalar_fields: bool,
) -> None:
    lines = [INFO_HEADER]
    if scalar_fields:
        lines.append(SCALAR_INFO_FIELDS)
    lines.append("tile_infos={ ")
    for offset, size in entries:
        lines.append(
            "{\n"
            f"\t\toffset={offset}\n"
            f"\t\tsize={size}\n"
            "\t} "
        )
    lines.append("}\n")
    path.write_text("".join(lines), encoding="utf-8", newline="\n")


def write_sparse_layer(
    stem: str,
    *,
    scalar_fields: bool,
    shared: np.ndarray | None,
) -> None:
    """Write an empty layer, optionally backed by one shared zero PNG."""
    bin_path = CACHE_OUT / f"{stem}.bin"
    info_path = CACHE_OUT / f"{stem}.info"
    count = tile_count()
    if shared is None:
        bin_path.write_bytes(b"")
        entries = [(-1, -1)] * count
    else:
        payload = png_bytes(shared)
        bin_path.write_bytes(payload)
        entries = [(0, len(payload))] * count
    write_info(info_path, entries, scalar_fields=scalar_fields)


def transformed_height_tile(
    source: Image.Image,
    mip: int,
    tile_x: int,
    tile_y: int,
) -> np.ndarray:
    # One output sample covers 2**mip virtual pixels.  The authored heightmap is
    # 1/8 of the virtual cache resolution in both dimensions.
    scale = (2**mip) * source.width / SOURCE_W
    x_offset = (tile_x * TILE_SIZE - BORDER_SIZE) * scale
    y_offset = (tile_y * TILE_SIZE - BORDER_SIZE) * scale
    tile = source.transform(
        (STORED_TILE_SIZE, STORED_TILE_SIZE),
        Image.Transform.AFFINE,
        (scale, 0.0, x_offset, 0.0, scale, y_offset),
        resample=Image.Resampling.BILINEAR,
        fillcolor=0,
    )
    values = np.clip(np.asarray(tile, dtype=np.float32), 0, 65_535).astype(
        np.uint16
    )
    # 512 height units are 0.78% of the engine range. The full-precision
    # authored source remains committed separately; cache quantization keeps
    # the derived virtual texture below GitHub's 100 MiB ordinary-file limit.
    values = (
        (values.astype(np.uint32) // HEIGHT_QUANTUM) * HEIGHT_QUANTUM
    ).astype(np.uint16)
    return values


def write_height_layer() -> dict[str, int]:
    started = time.monotonic()
    bin_path = CACHE_OUT / "heightmap.bin"
    info_path = CACHE_OUT / "heightmap.info"
    temp_bin = bin_path.with_suffix(".bin.tmp")
    entries: list[tuple[int, int]] = []
    dedup: dict[bytes, tuple[int, int]] = {}
    unique_tiles = 0
    written_tiles = 0
    total_tiles = tile_count()

    with Image.open(HEIGHT_SOURCE) as opened:
        # PIL's I;16 affine resampler truncates the high byte.  Float mode is
        # required to preserve the authored 16-bit height range.
        source = opened.convert("F")
        with temp_bin.open("wb") as output:
            for mip, tile_x, tile_y in engine_tile_sequence():
                payload = png_bytes(
                    transformed_height_tile(source, mip, tile_x, tile_y)
                )
                key = hashlib.blake2b(payload, digest_size=16).digest()
                known = dedup.get(key)
                if known is None:
                    offset = output.tell()
                    output.write(payload)
                    known = (offset, len(payload))
                    dedup[key] = known
                    unique_tiles += 1
                entries.append(known)
                written_tiles += 1
                if written_tiles % 8_192 == 0:
                    print(
                        "gen_terrain_cache: height "
                        f"{written_tiles:,}/{total_tiles:,} tiles, "
                        f"{unique_tiles:,} unique",
                        flush=True,
                    )
    temp_bin.replace(bin_path)
    write_info(info_path, entries, scalar_fields=True)
    print(
        "gen_terrain_cache: height complete "
        f"({written_tiles:,} tiles, {unique_tiles:,} unique, "
        f"{bin_path.stat().st_size / 1_000_000:.1f} MB) in "
        f"{time.monotonic() - started:.1f}s",
        flush=True,
    )
    return {"tiles": written_tiles, "unique_tiles": unique_tiles}


def migrate_legacy_height_order(height_source_hash: str) -> dict[str, int] | None:
    """Re-index an already baked payload without recompressing it."""
    try:
        manifest = json.loads(MANIFEST_OUT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    legacy_version = manifest.get("generator_version")
    if legacy_version not in {1, 2, 3, 4, 5} or manifest.get("source_sha256") != height_source_hash:
        return None

    info_path = CACHE_OUT / "heightmap.info"
    bin_path = CACHE_OUT / "heightmap.bin"
    if not info_path.is_file() or not bin_path.is_file():
        return None
    old_entries = parse_entries(info_path)
    if len(old_entries) != tile_count():
        return None

    # v1 emitted fine-first row-major groups; v2 used coarse-first row-major
    # groups; v3 used coarse-first Morton groups; v4 used one global pre-order
    # tree; v5 used fine-first Morton groups. Reassembling retail cache tiles
    # proves the actual contract: fine-first row-major info entries whose
    # source rows run bottom-to-top.
    by_coordinate: dict[tuple[int, int, int], tuple[int, int]] = {}
    if legacy_version == 4:
        by_coordinate.update(
            dict(zip(preorder_tile_sequence(), old_entries, strict=True))
        )
    elif legacy_version == 5:
        by_coordinate.update(
            dict(zip(morton_tile_sequence(), old_entries, strict=True))
        )
    else:
        cursor = 0
        legacy_layout = (
            pyramid_layout()
            if legacy_version == 1
            else list(reversed(pyramid_layout()))
        )
        for mip, tiles_x, tiles_y in legacy_layout:
            count = tiles_x * tiles_y
            group = old_entries[cursor : cursor + count]
            if legacy_version in {1, 2}:
                coordinates = [
                    (x, y)
                    for y in range(tiles_y)
                    for x in range(tiles_x)
                ]
            else:
                coordinates = morton_coordinates(tiles_x, tiles_y)
            by_coordinate.update(
                {
                    (mip, x, y): entry
                    for (x, y), entry in zip(
                        coordinates, group, strict=True
                    )
                }
            )
            cursor += count
    reordered = [
        by_coordinate[(mip, x, y)]
        for mip, x, y in engine_tile_sequence()
    ]
    write_info(info_path, reordered, scalar_fields=True)
    print(
        f"gen_terrain_cache: migrated v{legacy_version} height index to "
        "fine-to-coarse row-major order with inverted source Y",
        flush=True,
    )
    return {
        "tiles": len(reordered),
        "unique_tiles": len(set(reordered)),
    }


def write_quadtree() -> None:
    path = CACHE_OUT / "quadtree_nodes.bin"
    header = struct.pack(
        "<5I",
        QUADTREE_DEPTH,
        QUADTREE_RECORDS,
        QUADTREE_LEAF_OFFSET,
        QUADTREE_FLAGS,
        QUADTREE_DIMENSIONS,
    )
    expected_size = (
        QUADTREE_HEADER_SIZE + QUADTREE_RECORDS * QUADTREE_RECORD_SIZE
    )
    with path.open("wb") as output:
        output.write(header)
        output.seek(expected_size - 1)
        output.write(b"\0")


def output_paths() -> list[Path]:
    return [
        CACHE_OUT / "heightmap.bin",
        CACHE_OUT / "heightmap.info",
        CACHE_OUT / "index_map.bin",
        CACHE_OUT / "index_map.info",
        CACHE_OUT / "intensity_map.bin",
        CACHE_OUT / "intensity_map.info",
        CACHE_OUT / "materials.bin",
        CACHE_OUT / "materials.info",
        CACHE_OUT / "quadtree_nodes.bin",
        CACHE_OUT / "checksum.json",
    ]


def write() -> None:
    CACHE_OUT.mkdir(parents=True, exist_ok=True)
    height_source_hash = sha256(HEIGHT_SOURCE)
    existing_failures = check(quiet=True)
    if not existing_failures:
        print("gen_terrain_cache: current cache already matches its source")
        return

    height_stats = migrate_legacy_height_order(height_source_hash)
    if height_stats is None:
        height_stats = write_height_layer()
    zero_scalar = np.zeros(
        (STORED_TILE_SIZE, STORED_TILE_SIZE), dtype=np.uint16
    )
    write_sparse_layer(
        "materials", scalar_fields=True, shared=zero_scalar
    )
    write_sparse_layer(
        "index_map", scalar_fields=False, shared=None
    )
    write_sparse_layer(
        "intensity_map", scalar_fields=False, shared=None
    )
    write_quadtree()

    checksum_seed = bytes.fromhex(height_source_hash)
    checksum = zlib.crc32(checksum_seed) & 0xFFFFFFFF
    (CACHE_OUT / "checksum.json").write_text(
        json.dumps(
            {
                "total": checksum,
                "decals": 0,
                "decal_sets": [],
            },
            indent="\t",
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    manifest = {
        "generator": "gen_terrain_cache.py",
        "generator_version": GENERATOR_VERSION,
        "source": str(HEIGHT_SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": height_source_hash,
        "source_resolution": [SOURCE_W, SOURCE_H],
        "tile_size": TILE_SIZE,
        "border_size": BORDER_SIZE,
        "tile_order": "fine_to_coarse_row_major_y_inverted",
        "height_quantum": HEIGHT_QUANTUM,
        "mip_layout": [
            [mip, width, height]
            for mip, width, height in pyramid_layout()
        ],
        "tile_count": tile_count(),
        "height_unique_tiles": height_stats["unique_tiles"],
        "earth_decal_layers": 0,
        "outputs": {
            path.name: {
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in output_paths()
        },
    }
    MANIFEST_OUT.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        "gen_terrain_cache: wrote self-contained ENDÓRË cache "
        f"({sum(path.stat().st_size for path in output_paths()) / 1_000_000:.1f} MB)"
    )


def parse_entries(path: Path) -> list[tuple[int, int]]:
    text = path.read_text(encoding="utf-8")
    return [
        (int(offset), int(size))
        for offset, size in re.findall(
            r"offset=(-?\d+)\s+size=(-?\d+)", text
        )
    ]


def check_info(
    stem: str,
    *,
    scalar_fields: bool,
    sparse: bool,
    failures: list[str],
) -> None:
    info_path = CACHE_OUT / f"{stem}.info"
    bin_path = CACHE_OUT / f"{stem}.bin"
    if not info_path.is_file() or not bin_path.is_file():
        failures.append(f"missing {stem} cache pair")
        return
    text = info_path.read_text(encoding="utf-8")
    if not text.startswith(INFO_HEADER):
        failures.append(f"{stem}.info has the wrong virtual-texture header")
    if scalar_fields and SCALAR_INFO_FIELDS not in text:
        failures.append(f"{stem}.info lacks scalar layer fields")
    entries = parse_entries(info_path)
    if len(entries) != tile_count():
        failures.append(
            f"{stem}.info has {len(entries):,} tiles, expected {tile_count():,}"
        )
        return
    payload_size = bin_path.stat().st_size
    if sparse:
        if payload_size != 0 or any(entry != (-1, -1) for entry in entries):
            failures.append(f"{stem} is not an explicitly empty decal layer")
        return
    for offset, size in entries:
        if offset < 0 or size <= 0 or offset + size > payload_size:
            failures.append(f"{stem}.info contains an invalid tile span")
            break


def check(*, quiet: bool = False) -> list[str]:
    failures: list[str] = []
    if not HEIGHT_SOURCE.is_file():
        return ["missing authored terrain height source"]
    if not MANIFEST_OUT.is_file():
        return ["missing terrain cache manifest"]
    try:
        manifest = json.loads(MANIFEST_OUT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"invalid terrain cache manifest: {error}"]
    if manifest.get("generator_version") != GENERATOR_VERSION:
        failures.append("terrain cache generator version is stale")
    if manifest.get("tile_order") != "fine_to_coarse_row_major_y_inverted":
        failures.append("terrain cache manifest has the wrong tile order")
    if manifest.get("source_sha256") != sha256(HEIGHT_SOURCE):
        failures.append("terrain cache does not match the authored height source")
    if manifest.get("tile_count") != tile_count():
        failures.append("terrain cache manifest has the wrong tile count")
    if manifest.get("earth_decal_layers") != 0:
        failures.append("terrain cache manifest permits inherited Earth decals")

    check_info(
        "heightmap",
        scalar_fields=True,
        sparse=False,
        failures=failures,
    )
    check_info(
        "materials",
        scalar_fields=True,
        sparse=False,
        failures=failures,
    )
    check_info(
        "index_map",
        scalar_fields=False,
        sparse=True,
        failures=failures,
    )
    check_info(
        "intensity_map",
        scalar_fields=False,
        sparse=True,
        failures=failures,
    )

    outputs = manifest.get("outputs", {})
    for path in output_paths():
        if not path.is_file():
            failures.append(f"missing {path.name}")
            continue
        record = outputs.get(path.name, {})
        if record.get("bytes") != path.stat().st_size:
            failures.append(f"{path.name} size differs from its manifest")
        elif record.get("sha256") != sha256(path):
            failures.append(f"{path.name} hash differs from its manifest")

    quadtree = CACHE_OUT / "quadtree_nodes.bin"
    expected_quadtree_size = (
        QUADTREE_HEADER_SIZE + QUADTREE_RECORDS * QUADTREE_RECORD_SIZE
    )
    if quadtree.is_file():
        with quadtree.open("rb") as stream:
            header = stream.read(QUADTREE_HEADER_SIZE)
        expected_header = struct.pack(
            "<5I",
            QUADTREE_DEPTH,
            QUADTREE_RECORDS,
            QUADTREE_LEAF_OFFSET,
            QUADTREE_FLAGS,
            QUADTREE_DIMENSIONS,
        )
        if quadtree.stat().st_size != expected_quadtree_size:
            failures.append("quadtree_nodes.bin has the wrong size")
        elif header != expected_header:
            failures.append("quadtree_nodes.bin has the wrong generic-tree header")

    if not quiet:
        if failures:
            for failure in failures:
                print(f"gen_terrain_cache: FAIL {failure}")
        else:
            print(
                "gen_terrain_cache: PASS "
                f"({tile_count():,} indexed tiles, zero Earth decal layers)"
            )
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
    return 1 if check() else 0


if __name__ == "__main__":
    raise SystemExit(main())
