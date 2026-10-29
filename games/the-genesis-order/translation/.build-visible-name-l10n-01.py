#!/usr/bin/env python3
"""Build a small contextual LLM draft for the remaining localizable proper-name UI."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "tools"))
from apply_translation import validate_record  # noqa: E402

OUTPUT = ROOT / "drafts" / "visible-name-l10n-01.jsonl"
TRANSLATIONS = {
    "system.gameTitle": {
        "The Genesis Order": "Zakon Genesis",
    },
    "database.actors.name": {
        "Arianna as Erica": "Arianna jako Erica",
    },
    "map_label": {
        # Keep the unclear in-world proper-name prefix; translate the clear noun.
        "WoNoChurch": "WoNo — kościół",
    },
}
EXPECTED = 3


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f"Refusing to overwrite existing draft: {OUTPUT}")
    known: set[str] = set()
    for path in (ROOT / "drafts").rglob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                if isinstance(row.get("translation"), str) and row["translation"].strip():
                    known.add(row["id"])

    rows: list[dict] = []
    for path in sorted((ROOT / "export-v1").glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            by_category = TRANSLATIONS.get(row.get("category"), {})
            translated = by_category.get(row.get("source_text"))
            if translated is None or row["id"] in known:
                continue
            if (row.get("context") or {}).get("translation_policy") == "keep_source_value":
                raise SystemExit(f"Refusing protected source: {row['id']}")
            if row["category"] == "map_label" and not (
                row.get("context", {}).get("map_id") == 154
                and row.get("context", {}).get("map_name") == "WoNoChurch"
            ):
                raise SystemExit(f"Unexpected map-label context: {row['id']}")
            if row["category"] == "database.actors.name" and not (
                row.get("context", {}).get("database_record_id") == 24
            ):
                raise SystemExit(f"Unexpected actor-alias context: {row['id']}")
            if row["category"] == "system.gameTitle" and row.get("structure", {}).get("json_path") != "/gameTitle":
                raise SystemExit(f"Unexpected game-title locator: {row['id']}")
            row["translation"] = translated
            validate_record(row, require_complete=True)
            rows.append(row)
    if len(rows) != EXPECTED:
        raise SystemExit(f"Expected exactly {EXPECTED} contextual translations, got {len(rows)}")
    if len({row["id"] for row in rows}) != len(rows):
        raise SystemExit("Duplicate stable IDs in batch")
    OUTPUT.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {len(rows)} contextual UI/name translations.")


if __name__ == "__main__":
    main()
