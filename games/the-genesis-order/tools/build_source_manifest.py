#!/usr/bin/env python3
"""Create a content-free inventory of the local TGO source files.

The manifest records paths, sizes, SHA-256 digests and RPG Maker plugin status.
It never emits or copies source strings and never evaluates JavaScript.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = REPO_ROOT / "google_drive" / "the-genesis-order"
DEFAULT_OUT = SOURCE_ROOT / "source_manifest.json"
PLUGIN_ASSIGNMENT = re.compile(r"\bvar\s+\$plugins\s*=\s*", re.MULTILINE)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def plugin_rows(path: Path) -> list[dict[str, Any]]:
    """Decode the JSON array assigned to $plugins without evaluating JS."""
    text = path.read_text(encoding="utf-8-sig")
    match = PLUGIN_ASSIGNMENT.search(text)
    if not match:
        raise ValueError(f"Could not find static $plugins assignment in {path.name}")
    decoder = json.JSONDecoder()
    try:
        rows, _end = decoder.raw_decode(text, match.end())
    except json.JSONDecodeError as error:
        raise ValueError(f"$plugins value is not JSON in {path.name}: {error}") from error
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("$plugins must be a JSON array of plugin records")
    return rows


def source_files(root: Path) -> list[Path]:
    paths = [
        path for path in (root / "data").glob("*")
        if path.is_file() and path.suffix.lower() in {".json", ".txt"}
    ]
    paths.extend(path for path in (root / "www" / "js").rglob("*.js") if path.is_file())
    package = root / "package.json"
    if package.is_file():
        paths.append(package)
    return sorted(set(paths), key=lambda path: path.relative_to(root).as_posix().casefold())


def category_for(rel: str) -> str:
    if rel.startswith("data/"):
        return "rpg_maker_data"
    if rel == "package.json":
        return "project_manifest"
    if rel.startswith("www/js/plugins/"):
        return "plugin_source"
    if rel.startswith("www/js/libs/"):
        return "runtime_library"
    return "rpg_maker_engine_source"


def build_manifest(root: Path) -> dict[str, Any]:
    if not root.is_dir():
        raise FileNotFoundError(f"TGO source directory not found: {root}")
    plugin_config = root / "www" / "js" / "plugins.js"
    plugin_path_status: dict[str, str] = {}
    configured = enabled = 0
    if plugin_config.is_file():
        for row in plugin_rows(plugin_config):
            name = row.get("name")
            if not isinstance(name, str) or not name:
                continue
            configured += 1
            state = "enabled" if row.get("status") else "disabled"
            enabled += state == "enabled"
            plugin_path_status[f"www/js/plugins/{name}.js"] = state

    provenance_path = root / "source_drive_inventory.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8")) if provenance_path.is_file() else {}
    drive_entries = provenance.get("downloaded_files", [])
    drive_by_path = {item["path"]: item for item in drive_entries if isinstance(item, dict) and item.get("path")}
    if len(drive_by_path) != len(drive_entries):
        raise ValueError("Drive inventory has duplicate or invalid downloaded file paths")

    entries = []
    for path in source_files(root):
        rel = path.relative_to(root).as_posix()
        size = path.stat().st_size
        entry: dict[str, Any] = {
            "path": rel,
            "category": category_for(rel),
            "size_bytes": size,
            "sha256": sha256_file(path),
        }
        drive_item = drive_by_path.get(rel)
        if drive_item:
            if int(drive_item.get("size_bytes", -1)) != size:
                raise ValueError(f"Drive/local size mismatch for {rel}")
            entry["drive_file_id"] = drive_item["id"]
            entry["drive_parent_folder_id"] = drive_item["parent_id"]
        if entry["category"] == "plugin_source":
            entry["plugin_status"] = plugin_path_status.get(rel, "not_configured")
        entries.append(entry)

    missing_local = sorted(set(drive_by_path) - {entry["path"] for entry in entries})
    if missing_local:
        raise ValueError(f"Drive inventory lists files missing locally: {missing_local[:5]}")

    digest_input = "".join(
        f"{entry['path']}\0{entry['size_bytes']}\0{entry['sha256']}\n"
        for entry in entries
    ).encode("utf-8")
    return {
        "schema": "tgo-source-manifest-v1",
        "scope": "local text data, project manifest and static JavaScript sources; no media",
        "plugin_config": {
            "configured": configured,
            "enabled": enabled,
            "disabled": configured - enabled,
            "unconfigured_plugin_files": sum(
                entry["category"] == "plugin_source"
                and entry.get("plugin_status") == "not_configured"
                for entry in entries
            ),
        },
        "drive_folders": provenance.get("drive_folders", {}),
        "archive_sources": provenance.get("archive_sources", []),
        "not_downloaded": provenance.get("not_downloaded", []),
        "file_count": len(entries),
        "aggregate_sha256": hashlib.sha256(digest_input).hexdigest(),
        "files": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE_ROOT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    manifest = build_manifest(args.source)
    out = args.out.resolve()
    private_root = (REPO_ROOT / "google_drive").resolve()
    if out != private_root and private_root not in out.parents:
        raise ValueError("Refusing to write a source manifest outside ignored google_drive/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest written: {out.relative_to(private_root).as_posix()}")
    print(f"Files: {manifest['file_count']}; aggregate SHA-256: {manifest['aggregate_sha256']}")
    print("Plugin config: " + json.dumps(manifest["plugin_config"], sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
