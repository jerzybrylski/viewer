#!/usr/bin/env python3
"""Statically count TGO's custom text channels and enrich the source CSVs.

The uploaded, text-only RPG Maker data is expected at:
  <repo>/google_drive/the-genesis-order/data/

No game code is executed and no source strings are written to stdout or CSV.
"""
from __future__ import annotations

import argparse
import ast
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "google_drive" / "the-genesis-order" / "data"
DOCS_DIR = REPO_ROOT / "games" / "the-genesis-order" / "docs"

ASSIGNMENT_RE = re.compile(
    r"\$gameVariables\s*\.\s*setValue\s*\(\s*(\d+)\s*,\s*"
    r"(\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')",
    re.IGNORECASE,
)

HEADER_RENAMES = {
    "dialogue_lines": "native_401_nonempty_lines",
    "unique_dialogue_lines": "unique_native_401_texts",
    "ks_page_calls": "ce224_cache_calls",
}

METRICS = {
    "custom_dialogue_entries": "custom_dialogue",
    "unique_custom_dialogue_texts": "custom_dialogue",
    "arianna_hint_entries": "arianna_hint",
    "unique_arianna_hints": "arianna_hint",
    "phone_text_entries": "phone_text",
    "unique_phone_texts": "phone_text",
    "item_found_label_entries": "item_found_label",
    "unique_item_found_labels": "item_found_label",
    "ce224_cache_calls": "ce224_cache_call",
}


def event_lists(obj: object, source: tuple[str, int]):
    """Yield RPG Maker command lists and a stable source key."""
    if source[0] == "map":
        if not isinstance(obj, dict):
            return
        for event in obj.get("events", []):
            if not isinstance(event, dict):
                continue
            for page_number, page in enumerate(event.get("pages", []), start=1):
                if isinstance(page, dict):
                    yield page.get("list", []), ("map", source[1])
    else:
        if not isinstance(obj, list):
            return
        for event in obj:
            if isinstance(event, dict) and isinstance(event.get("id"), int):
                yield event.get("list", []), ("ce", event["id"])


def find_separator(common_events: list[dict]) -> str:
    event = next((e for e in common_events if e and e.get("id") == 60), None)
    if not event:
        raise ValueError("Common Event 60 (MESSAGE) was not found")
    for command in event.get("list", []):
        if not isinstance(command, dict) or command.get("code") not in (355, 655):
            continue
        params = command.get("parameters") or []
        line = params[0] if params and isinstance(params[0], str) else ""
        match = re.search(
            r"\.indexOf\((\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')\)",
            line,
        )
        if match:
            return ast.literal_eval(match.group(1))
    raise ValueError("Could not identify Common Event 60's message separator")


def routed_assignments(command_list: list[dict]):
    """Yield (variable, literal, next common event) before a same-variable overwrite."""
    for index, command in enumerate(command_list):
        if not isinstance(command, dict) or command.get("code") not in (355, 655):
            continue
        params = command.get("parameters") or []
        script = params[0] if params and isinstance(params[0], str) else ""
        assignments = [(int(m.group(1)), ast.literal_eval(m.group(2)))
                       for m in ASSIGNMENT_RE.finditer(script)]
        for variable_id, value in assignments:
            target = None
            for later in command_list[index + 1:]:
                if not isinstance(later, dict):
                    continue
                if later.get("code") in (355, 655):
                    later_params = later.get("parameters") or []
                    later_script = (later_params[0]
                                    if later_params and isinstance(later_params[0], str)
                                    else "")
                    if any(int(m.group(1)) == variable_id
                           for m in ASSIGNMENT_RE.finditer(later_script)):
                        break
                if later.get("code") == 117:
                    call_params = later.get("parameters") or []
                    target = call_params[0] if call_params else None
                    break
            yield variable_id, value, target


def load_source_lists():
    if not DATA_DIR.is_dir():
        raise FileNotFoundError(
            f"Text-only source data not found: {DATA_DIR}. "
            "Restore the user's uploaded www/data JSON files first."
        )
    source_lists = []
    map_files = sorted(DATA_DIR.glob("Map[0-9][0-9][0-9].json"))
    if not map_files:
        raise FileNotFoundError(f"No Map###.json files found in {DATA_DIR}")
    for path in map_files:
        map_id = int(path.stem[-3:])
        data = json.loads(path.read_text(encoding="utf-8"))
        source_lists.extend(event_lists(data, ("map", map_id)))
    common_path = DATA_DIR / "CommonEvents.json"
    common_events = json.loads(common_path.read_text(encoding="utf-8"))
    source_lists.extend(event_lists(common_events, ("ce", 0)))
    return source_lists, common_events


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="verify totals and report counts without updating the CSV files",
    )
    args = parser.parse_args()

    source_lists, common_events = load_source_lists()
    separator = find_separator(common_events)
    if separator != ".":
        raise ValueError("Unexpected MESSAGE parser separator; review before counting")

    by_source: dict[tuple[str, int], dict[str, list[str] | int]] = defaultdict(
        lambda: defaultdict(list)
    )
    global_values: dict[str, list[str]] = defaultdict(list)
    common_event_calls: Counter[tuple[str, int]] = Counter()
    for command_list, source in source_lists:
        for command in command_list:
            if (isinstance(command, dict) and command.get("code") == 117
                    and (command.get("parameters") or [None])[0] == 224):
                common_event_calls[source] += 1
                by_source[source]["ce224_cache_call"].append("call")
        for variable_id, value, target in routed_assignments(command_list):
            category = None
            output = value
            if variable_id == 21 and target == 60:
                if separator not in value:
                    raise ValueError("A MESSAGE payload lacks the parser separator")
                output = value.split(separator, 1)[1]
                if not output.strip():
                    raise ValueError("A MESSAGE payload is empty after parsing")
                category = "custom_dialogue"
            elif variable_id == 21 and target == 222:
                category = "arianna_hint"
            elif variable_id == 25 and target == 53:
                category = "phone_text"
            elif variable_id == 107 and target == 223:
                category = "item_found_label"
            if category:
                by_source[source][category].append(output)
                global_values[category].append(output)

    expected = {
        "custom_dialogue": 38638,
        "arianna_hint": 705,
        "phone_text": 17,
        "item_found_label": 649,
        "ce224_cache_call": 67,
    }
    totals = {key: len(values) for key, values in global_values.items()}
    totals["ce224_cache_call"] = sum(common_event_calls.values())
    if totals != expected:
        raise ValueError(f"Count validation failed: expected {expected}, got {totals}")

    # Verify both source CSVs before modifying either.
    csv_specs = [
        (DOCS_DIR / "COUNT_BY_MAP.csv", "map_id", "map"),
        (DOCS_DIR / "COUNT_BY_COMMON_EVENT.csv", "common_event_id", "ce"),
    ]
    loaded = []
    for path, key_column, source_type in csv_specs:
        with path.open(newline="", encoding="utf-8") as stream:
            original_rows = list(csv.DictReader(stream))
            original_fields = list(original_rows[0].keys()) if original_rows else []
        fieldnames = [HEADER_RENAMES.get(name, name) for name in original_fields]
        rows = [
            {HEADER_RENAMES.get(name, name): value for name, value in row.items()}
            for row in original_rows
        ]
        if not rows or key_column not in fieldnames:
            raise ValueError(f"Unexpected CSV layout: {path}")
        loaded.append((path, key_column, source_type, fieldnames, rows))

    for path, key_column, source_type, fieldnames, rows in loaded:
        for column, category in METRICS.items():
            if column not in fieldnames:
                fieldnames.append(column)
        for row in rows:
            source = (source_type, int(row[key_column]))
            values = by_source.get(source, {})
            for column, category in METRICS.items():
                if column.endswith("_entries") or column.endswith("_calls"):
                    row[column] = str(len(values.get(category, [])))
                else:
                    row[column] = str(len(set(values.get(category, []))))
        if not args.check:
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)

    print("Custom text-channel static counts (source strings are not emitted):")
    for category in ("custom_dialogue", "arianna_hint", "phone_text", "item_found_label"):
        values = global_values[category]
        print(f"  {category}: {len(values)} entries, {len(set(values))} unique")
    print(f"  CE224 image-cache calls: {totals['ce224_cache_call']}")
    for category in ("custom_dialogue", "arianna_hint", "phone_text", "item_found_label"):
        c = Counter()
        for source, metrics in by_source.items():
            count = len(metrics.get(category, []))
            if count:
                c[source[0]] += count
        print(f"  {category} by source type: {dict(c)}")
    if args.check:
        print("CSV files checked; no files changed.")
    else:
        print("Updated COUNT_BY_MAP.csv and COUNT_BY_COMMON_EVENT.csv.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
