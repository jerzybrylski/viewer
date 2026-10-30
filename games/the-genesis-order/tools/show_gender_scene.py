#!/usr/bin/env python3
"""Podgląd sceny z inwentarza audytu rodzaju — wyłącznie odczyt, zero zapisów.

Narzędzie nie ocenia tłumaczenia i nie zmienia korpusu. Pokazuje kwestie jednej
sceny (mapa/event/strona lub common event) w kolejności poleceń, z nagłówkiem,
nazwą mówcy z mapy kodów, oryginałem i przekładem, żeby decyzję o rodzaju
podejmować na pełnym kontekście, a nie na jednym zdaniu.

Ostrzeżenia (te same co w kolejce): nagłówek może wskazywać ciało, nie faktyczną
tożsamość (sceny opętania), a sąsiednia kwestia nie dowodzi adresata ani gałęzi.

Przykłady:

    python3 tools/inventory_gender_review.py --output /tmp/tgo-inventory.jsonl
    python3 tools/show_gender_scene.py --inventory /tmp/tgo-inventory.jsonl \\
        --id tgo:custom_dialogue:0523d4464428d26ef567
    python3 tools/show_gender_scene.py --inventory /tmp/tgo-inventory.jsonl \\
        --locator map:144:40:3 --only-scene
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from fix_grammatical_gender import gender_of, speaker_of


def load(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def locator(row: dict) -> str:
    context = row.get("context") or {}
    kind = context.get("source_kind")
    if kind == "common_event":
        return f"ce:{context.get('event_id')}"
    if kind == "map":
        return f"map:{context.get('map_id')}:{context.get('event_id')}:{context.get('page_number')}"
    return f"{row.get('category')}"


def describe(row: dict) -> str:
    context = row.get("context") or {}
    header = context.get("custom_header") or "-"
    name = speaker_of(row)
    if name:
        return f"{header} ({name}/{gender_of(name) or '?'})"
    return f"{header} ({context.get('speaker_status') or 'brak mapowania'})"


def render(rows: list[dict], target: dict, window: int = 12, only_scene: bool = False) -> list[str]:
    """Zwraca linie sceny z zaznaczoną kwestią; nie modyfikuje wejścia."""
    key = locator(target)
    context = target.get("context") or {}
    lines = [f"# scena {key}  event={context.get('event_name')} mapa={context.get('map_name')} "
             f"warunki={(json.dumps(context.get('page_conditions'), ensure_ascii=False))}"]
    scene = [row for row in rows
             if locator(row) == key and isinstance((row.get('context') or {}).get('command_index'), int)]
    scene.sort(key=lambda row: row['context']['command_index'])
    try:
        center = next(index for index, row in enumerate(scene) if row['id'] == target['id'])
    except StopIteration:
        center = 0
    low = 0 if only_scene else max(0, center - window // 2)
    high = len(scene) if only_scene else min(len(scene), center + window // 2)
    for index in range(low, high):
        row = scene[index]
        mark = ">>" if row["id"] == target["id"] else "  "
        lines.append(f"{mark} #{row['context']['command_index']:>4} [{describe(row)}]")
        lines.append(f"     EN: {row.get('source_text')}")
        lines.append(f"     PL: {row.get('translation')}")
    lines.append(f"# kwestii w scenie: {len(scene)}; zaznaczona na pozycji {center + 1}")
    return lines


def find(rows: list[dict], *, target_id: str | None, locator_key: str | None) -> dict | None:
    if target_id:
        return next((row for row in rows if row['id'] == target_id), None)
    if locator_key:
        return next((row for row in rows if locator(row) == locator_key), None)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Podgląd sceny z inwentarza audytu rodzaju (tylko odczyt).")
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--id")
    parser.add_argument("--locator", help="map:<id>:<event>:<strona> albo ce:<event>")
    parser.add_argument("--window", type=int, default=12)
    parser.add_argument("--only-scene", action="store_true")
    args = parser.parse_args()

    rows = load(Path(args.inventory))
    target = find(rows, target_id=args.id, locator_key=args.locator)
    if target is None:
        print("Nie znaleziono rekordu w inwentarzu.", file=sys.stderr)
        return 1
    print("\n".join(render(rows, target, window=args.window, only_scene=args.only_scene)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
