#!/usr/bin/env python3
"""Validate translated JSONL records and apply them to a new TGO data copy.

No source file is overwritten. The command only reads JSON/JSONL and writes a
new staging directory under ignored google_drive/. It never executes game JS.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from export_translation import EXTRA_CONTROL_RE, canonical_id, tokens, translation_tokens_match
from build_source_manifest import PLUGIN_ASSIGNMENT, plugin_rows
from scan_js_text_candidates import iter_literals

REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = REPO_ROOT / "google_drive" / "the-genesis-order"
DEFAULT_OUT = SOURCE_ROOT / "translation" / "applied-v1"
ASSIGNMENT_RE = re.compile(
    r"\$gameVariables\s*\.\s*setValue\s*\(\s*(\d+)\s*,\s*"
    r"(\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')",
    re.IGNORECASE,
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_jsonl_files(inputs: list[Path]) -> list[dict[str, Any]]:
    paths: list[Path] = []
    for path in inputs:
        if path.is_dir():
            paths.extend(sorted(path.glob("*.jsonl")))
        elif path.is_file():
            paths.append(path)
        else:
            raise FileNotFoundError(f"Translation input not found: {path}")
    records = []
    for path in paths:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f"Invalid JSONL at {path}:{line_number}: {error}") from error
                if not isinstance(row, dict):
                    raise ValueError(f"Expected a JSON object at {path}:{line_number}")
                row["_input_path"] = str(path)
                row["_input_line"] = line_number
                records.append(row)
    if not records:
        raise ValueError("No translation records found")
    return records


def validate_record(row: dict[str, Any], require_complete: bool) -> str | None:
    required = {"schema", "id", "category", "classification", "source_text",
                "translation", "markup_tokens", "source", "context", "structure"}
    missing = required - row.keys()
    if missing:
        raise ValueError(f"Record {row.get('id', '<no id>')} lacks required fields: {sorted(missing)}")
    if row["schema"] != "tgo-translation-record-v1":
        raise ValueError(f"Unsupported record schema for {row['id']}")
    if not isinstance(row["source_text"], str) or not isinstance(row["translation"], str):
        raise ValueError(f"Source/translation must be strings for {row['id']}")
    if ((row.get("context") or {}).get("translation_policy") == "keep_source_value"
            and row["translation"].strip() and row["translation"] != row["source_text"]):
        raise ValueError(f"This source value is protected from translation for {row['id']}")
    if not isinstance(row["source"], dict) or not isinstance(row["source"].get("locator"), dict):
        raise ValueError(f"Missing locator for {row['id']}")
    source = row["source"]
    locator = source["locator"]
    if source.get("file") != locator.get("file"):
        raise ValueError(f"Source file and locator file differ for {row['id']}")
    if "plugin_index" in locator:
        expected_writeback = "plugin_parameter"
    elif "char_offset" in locator:
        expected_writeback = "js_string_literal"
    elif locator.get("expression_kind") == "variable_value":
        expected_writeback = "event_script_expression"
    elif "json_path" in locator:
        expected_writeback = "json_string_leaf"
    elif "line_number" in locator and source["file"].lower().endswith(".txt"):
        expected_writeback = "text_file_line"
    else:
        expected_writeback = "script_string_literal"
    if source.get("writeback") != expected_writeback:
        raise ValueError(f"Write-back kind does not match locator for {row['id']}")
    if not isinstance(source.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
        raise ValueError(f"Invalid source SHA-256 for {row['id']}")
    if not isinstance(row.get("markup_tokens"), list) or any(not isinstance(token, str) for token in row["markup_tokens"]):
        raise ValueError(f"Invalid markup token list for {row['id']}")
    if canonical_id(row["category"], locator) != row["id"]:
        raise ValueError(f"Stable ID does not match category/locator for {row['id']}")
    if row["markup_tokens"] != tokens(row["source_text"]):
        raise ValueError(f"Source markup signature mismatch for {row['id']}")
    if not row["translation"].strip():
        protected = (row.get("context") or {}).get("translation_policy") == "keep_source_value"
        if require_complete and not protected:
            raise ValueError(f"Translation is empty for {row['id']}")
        return None
    if not translation_tokens_match(row["source_text"], row["translation"], row["markup_tokens"]):
        raise ValueError(f"Markup/token mismatch in translation for {row['id']}")
    if EXTRA_CONTROL_RE.findall(row["translation"]) != EXTRA_CONTROL_RE.findall(row["source_text"]):
        raise ValueError(f"Additional control/placeholder mismatch in translation for {row['id']}")
    return row["translation"]


def unescape_pointer(segment: str) -> str:
    return segment.replace("~1", "/").replace("~0", "~")


def event_owner(document: Any, rel: str, locator: dict[str, Any]) -> dict[str, Any]:
    event_id = locator.get("event_id")
    page_number = locator.get("page_number")
    if rel.startswith("data/Map"):
        events = document.get("events", [])
        event = next((item for item in events if isinstance(item, dict) and item.get("id") == event_id), None)
        if event is None:
            raise ValueError(f"Map event not found for {rel}, event {event_id}")
        pages = event.get("pages", [])
        if not isinstance(page_number, int) or not 1 <= page_number <= len(pages):
            raise ValueError(f"Map page not found for {rel}, event {event_id}")
        return pages[page_number - 1]
    if rel == "data/CommonEvents.json":
        event = next((item for item in document if isinstance(item, dict) and item.get("id") == event_id), None)
        if event is None:
            raise ValueError(f"Common Event {event_id} not found")
        return event
    raise ValueError(f"Event locator is not valid for {rel}")


def resolve_json_leaf(document: Any, rel: str, locator: dict[str, Any]) -> tuple[Any, str | int]:
    json_path = locator.get("json_path")
    if not isinstance(json_path, str) or not json_path.startswith("/"):
        raise ValueError(f"Missing JSON Pointer for {locator}")
    segments = [unescape_pointer(item) for item in json_path[1:].split("/")]
    if segments and segments[0] == "list" and "event_id" in locator:
        current: Any = event_owner(document, rel, locator)
    else:
        current = document
    for segment in segments[:-1]:
        if isinstance(current, list):
            if not segment.isdigit():
                raise ValueError(f"Expected an array index in locator {json_path}")
            current = current[int(segment)]
        elif isinstance(current, dict):
            current = current[segment]
        else:
            raise ValueError(f"Cannot traverse locator {json_path}")
    final: str | int = segments[-1]
    if isinstance(current, list):
        if not final.isdigit():
            raise ValueError(f"Expected an array index at end of {json_path}")
        final = int(final)
    elif not isinstance(current, dict):
        raise ValueError(f"Invalid parent value for {json_path}")
    return current, final


def event_script_expression_source(
    row: dict[str, Any], document: Any, rel: str,
) -> tuple[dict[str, Any], list[Any], str, str]:
    """Resolve a static command-122 JS string expression without executing it."""
    locator = row["source"]["locator"]
    if locator.get("expression_kind") != "variable_value":
        raise ValueError(f"Unsupported event script expression locator for {row['id']}")
    owner = event_owner(document, rel, locator)
    commands = owner.get("list", [])
    command_index = locator.get("command_index")
    if not isinstance(command_index, int) or not 0 <= command_index < len(commands):
        raise ValueError(f"Event script expression command is out of range for {row['id']}")
    command = commands[command_index]
    if not isinstance(command, dict) or command.get("code") != 122:
        raise ValueError(f"Event script expression is not command 122 for {row['id']}")
    params = command.get("parameters") or []
    if len(params) < 5 or params[3] != 4 or not isinstance(params[4], str):
        raise ValueError(f"Event script expression is not a static script operand for {row['id']}")
    start_id, end_id = params[0], params[1]
    if (start_id != locator.get("start_variable_id")
            or end_id != locator.get("end_variable_id")):
        raise ValueError(f"Event variable range changed for {row['id']}")
    rendered_ids = locator.get("rendered_variable_ids")
    if (not isinstance(rendered_ids, list) or not rendered_ids
            or any(not isinstance(item, int) or not start_id <= item <= end_id for item in rendered_ids)):
        raise ValueError(f"Invalid rendered variable IDs for {row['id']}")
    expression = params[4]
    try:
        value = ast.literal_eval(expression)
    except (SyntaxError, ValueError) as error:
        raise ValueError(f"Cannot decode static event script value for {row['id']}") from error
    if not isinstance(value, str):
        raise ValueError(f"Event script value is not a string for {row['id']}")
    return command, params, expression, value


def js_quote(value: str, quote: str) -> str:
    pieces = [quote]
    escapes = {"\\": "\\\\", "\n": "\\n", "\r": "\\r", "\t": "\\t",
               "\b": "\\b", "\f": "\\f", "\u2028": "\\u2028", "\u2029": "\\u2029"}
    for char in value:
        if char in escapes:
            pieces.append(escapes[char])
        elif char == quote:
            pieces.append("\\" + char)
        elif ord(char) < 0x20:
            pieces.append(f"\\u{ord(char):04x}")
        else:
            pieces.append(char)
    pieces.append(quote)
    return "".join(pieces)


def skip_json_space(text: str, index: int) -> int:
    while index < len(text) and text[index] in " \t\r\n":
        index += 1
    return index


def json_string_token(text: str, index: int) -> tuple[str, int, int]:
    try:
        value, end = json.JSONDecoder().raw_decode(text, index)
    except json.JSONDecodeError as error:
        raise ValueError("Malformed JSON string in static plugin configuration") from error
    if not isinstance(value, str):
        raise ValueError("Expected a JSON string in static plugin configuration")
    return value, index, end


def locate_json_path(text: str, start: int, end: int, target: tuple[str, ...]) -> tuple[int, int, str]:
    """Locate a JSON string by path while preserving all surrounding source bytes."""
    def parse_value(index: int, path: tuple[str, ...]) -> tuple[int, tuple[int, int, str] | None]:
        index = skip_json_space(text, index)
        if index >= end:
            raise ValueError("Unexpected end of static plugin JSON")
        char = text[index]
        hit = None
        if char == '"':
            value, token_start, token_end = json_string_token(text, index)
            if path == target:
                hit = (token_start, token_end, value)
            return token_end, hit
        if char == "{":
            index += 1
            index = skip_json_space(text, index)
            if index < end and text[index] == "}":
                return index + 1, None
            while index < end:
                index = skip_json_space(text, index)
                key, _key_start, key_end = json_string_token(text, index)
                index = skip_json_space(text, key_end)
                if index >= end or text[index] != ":":
                    raise ValueError("Malformed object in static plugin JSON")
                child_end, child_hit = parse_value(index + 1, path + (key,))
                if child_hit is not None:
                    hit = child_hit
                index = skip_json_space(text, child_end)
                if index < end and text[index] == "}":
                    return index + 1, hit
                if index >= end or text[index] != ",":
                    raise ValueError("Malformed object separator in static plugin JSON")
                index += 1
            raise ValueError("Unterminated object in static plugin JSON")
        if char == "[":
            index += 1
            item_index = 0
            index = skip_json_space(text, index)
            if index < end and text[index] == "]":
                return index + 1, None
            while index < end:
                child_end, child_hit = parse_value(index, path + (str(item_index),))
                if child_hit is not None:
                    hit = child_hit
                index = skip_json_space(text, child_end)
                if index < end and text[index] == "]":
                    return index + 1, hit
                if index >= end or text[index] != ",":
                    raise ValueError("Malformed array separator in static plugin JSON")
                index += 1
                item_index += 1
            raise ValueError("Unterminated array in static plugin JSON")
        token_end = index
        while token_end < end and text[token_end] not in ",]} \t\r\n":
            token_end += 1
        if token_end == index:
            raise ValueError("Malformed scalar in static plugin JSON")
        return token_end, None

    _parsed_end, found = parse_value(start, ())
    if found is None:
        raise ValueError(f"Static plugin JSON path not found: {target}")
    return found


def plugin_parameter_span(text: str, locator: dict[str, Any]) -> tuple[int, int, str]:
    match = PLUGIN_ASSIGNMENT.search(text)
    if not match:
        raise ValueError("Could not locate static $plugins configuration")
    try:
        _rows, array_end = json.JSONDecoder().raw_decode(text, match.end())
    except json.JSONDecodeError as error:
        raise ValueError("$plugins is not valid static JSON") from error
    index = locator.get("plugin_index")
    key = locator.get("parameter_key")
    name = locator.get("plugin_name")
    if not isinstance(index, int) or not isinstance(key, str) or not isinstance(name, str):
        raise ValueError("Incomplete plugin parameter locator")
    rows = plugin_rows_from_text(text, match.end())
    if not 0 <= index < len(rows) or rows[index].get("name") != name:
        raise ValueError("Plugin index/name mismatch in static configuration")
    return locate_json_path(text, match.end(), array_end, (str(index), "parameters", key))


def plugin_rows_from_text(text: str, start: int) -> list[dict[str, Any]]:
    try:
        rows, _end = json.JSONDecoder().raw_decode(text, start)
    except json.JSONDecodeError as error:
        raise ValueError("$plugins is not valid static JSON") from error
    if not isinstance(rows, list) or any(not isinstance(item, dict) for item in rows):
        raise ValueError("$plugins must be a static array of objects")
    return rows


def js_literal_at(text: str, locator: dict[str, Any], expected: str) -> dict[str, Any]:
    offset = locator.get("char_offset")
    if not isinstance(offset, int):
        raise ValueError("Missing JavaScript literal offset")
    for literal in iter_literals(text):
        if literal["start"] == offset:
            if literal.get("dynamic_template") or literal.get("value") != expected:
                raise ValueError("JavaScript literal source text mismatch")
            if literal.get("line") != locator.get("line"):
                raise ValueError("JavaScript literal line locator mismatch")
            return literal
    raise ValueError("JavaScript literal offset no longer identifies a string")


def text_file_line(document: str, line_number: int) -> tuple[list[str], int, str]:
    if not isinstance(line_number, int) or line_number < 1:
        raise ValueError("Text-file line locator must be a positive 1-based integer")
    lines = document.splitlines(keepends=True)
    if line_number > len(lines):
        raise ValueError("Text-file line locator is out of range")
    raw_line = lines[line_number - 1]
    ending = "\r\n" if raw_line.endswith("\r\n") else "\n" if raw_line.endswith("\n") else "\r" if raw_line.endswith("\r") else ""
    value = raw_line[:-len(ending)] if ending else raw_line
    return lines, line_number - 1, ending


def get_record_source_text(row: dict[str, Any], document: Any, rel: str) -> str:
    locator = row["source"]["locator"]
    writeback = row["source"]["writeback"]
    if writeback == "text_file_line":
        lines, index, ending = text_file_line(document, locator.get("line_number"))
        raw = lines[index]
        return raw[:-len(ending)] if ending else raw
    if writeback == "plugin_parameter":
        text = document
        start, end, value = plugin_parameter_span(text, locator)
        if not isinstance(value, str):
            raise ValueError(f"Located plugin parameter is not a string for {row['id']}")
        return value
    if writeback == "js_string_literal":
        literal = js_literal_at(document, locator, row["source_text"])
        return literal["value"]
    if writeback == "event_script_expression":
        _command, _params, _expression, value = event_script_expression_source(row, document, rel)
        return value
    if writeback == "json_string_leaf":
        parent, final = resolve_json_leaf(document, rel, locator)
        value = parent[final]
        if not isinstance(value, str):
            raise ValueError(f"Located value is not a string for {row['id']}")
        return value

    event = event_owner(document, rel, locator)
    commands = event.get("list", [])
    command_index = locator.get("command_index")
    if not isinstance(command_index, int) or not 0 <= command_index < len(commands):
        raise ValueError(f"Script command index out of range for {row['id']}")
    command = commands[command_index]
    params = command.get("parameters") or []
    script = params[0] if params and isinstance(params[0], str) else ""
    matches = list(ASSIGNMENT_RE.finditer(script))
    assignment_index = locator.get("assignment_index")
    if not isinstance(assignment_index, int) or not 0 <= assignment_index < len(matches):
        raise ValueError(f"Script assignment not found for {row['id']}")
    match = matches[assignment_index]
    if int(match.group(1)) != locator.get("variable_id"):
        raise ValueError(f"Script variable mismatch for {row['id']}")
    try:
        raw_value = ast.literal_eval(match.group(2))
    except (SyntaxError, ValueError) as error:
        raise ValueError(f"Cannot decode source script string for {row['id']}") from error
    structure = row.get("structure", {})
    if raw_value != structure.get("raw_value"):
        raise ValueError(f"Script source payload mismatch for {row['id']}")
    separator = structure.get("separator")
    return raw_value.split(separator, 1)[1] if separator and separator in raw_value else raw_value


def replace_source(row: dict[str, Any], document: Any, rel: str, translated: str) -> Any:
    locator = row["source"]["locator"]
    writeback = row["source"]["writeback"]
    if writeback == "text_file_line":
        if "\n" in translated or "\r" in translated:
            raise ValueError("Credits line translations may not introduce line breaks")
        lines, index, ending = text_file_line(document, locator.get("line_number"))
        lines[index] = translated + ending
        return "".join(lines)
    if writeback == "plugin_parameter":
        start, end, _value = plugin_parameter_span(document, locator)
        document = document[:start] + json.dumps(translated, ensure_ascii=False) + document[end:]
        return document
    if writeback == "js_string_literal":
        literal = js_literal_at(document, locator, row["source_text"])
        raw = literal["raw"]
        quote = raw[0]
        if quote == "`":
            # Static template strings have no interpolation; replace the whole
            # token with a safely quoted ordinary JS string. Dynamic templates
            # are rejected by js_literal_at and can never reach this branch.
            if "${" in raw:
                raise ValueError("Dynamic template-literal write-back is unsupported")
            replacement = js_quote(translated, '"')
        else:
            replacement = js_quote(translated, quote)
        return document[:literal["start"]] + replacement + document[literal["end"]:]
    if writeback == "event_script_expression":
        command, params, expression, _value = event_script_expression_source(row, document, rel)
        stripped = expression.lstrip()
        quote = stripped[0] if stripped and stripped[0] in "'\\\"" else '\"'
        params[4] = js_quote(translated, quote)
        command["parameters"] = params
        return document
    if writeback == "json_string_leaf":
        parent, final = resolve_json_leaf(document, rel, locator)
        parent[final] = translated
        return document

    event = event_owner(document, rel, locator)
    command = event["list"][locator["command_index"]]
    params = command.get("parameters") or []
    script = params[0]
    matches = list(ASSIGNMENT_RE.finditer(script))
    match = matches[locator["assignment_index"]]
    original_value = ast.literal_eval(match.group(2))
    structure = row.get("structure", {})
    header = structure.get("header", "")
    separator = structure.get("separator")
    replacement_value = f"{header}{separator}{translated}" if separator and separator in original_value else translated
    quote = match.group(2)[0]
    new_literal = js_quote(replacement_value, quote)
    params[0] = script[:match.start(2)] + new_literal + script[match.end(2):]
    command["parameters"] = params
    return document


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def apply_records(inputs: list[Path], source: Path, out: Path, check_only: bool,
                  require_complete: bool) -> dict[str, Any]:
    rows = read_jsonl_files(inputs)
    seen_ids: set[str] = set()
    translated_rows = []
    for row in rows:
        row_id = row.get("id", "<no id>")
        if row_id in seen_ids:
            raise ValueError(f"Duplicate translation ID: {row_id}")
        seen_ids.add(row_id)
        translated = validate_record(row, require_complete)
        if translated is not None:
            translated_rows.append(row)

    all_hashes: dict[str, set[str]] = defaultdict(set)
    raw_sources: dict[str, bytes] = {}
    for row in rows:
        rel = row["source"].get("file")
        if not isinstance(rel, str) or not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
            raise ValueError(f"Unsafe source path for {row['id']}")
        all_hashes[rel].add(row["source"]["sha256"])
    for rel, hashes in all_hashes.items():
        if len(hashes) != 1:
            raise ValueError(f"Records disagree on source hash: {rel}")
        raw = (source / rel).read_bytes()
        if sha256_bytes(raw) not in hashes:
            raise ValueError(f"Source file hash mismatch: {rel}")
        raw_sources[rel] = raw

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    target_locators: dict[tuple[str, str], str] = {}
    for row in translated_rows:
        locator_key = (row["source"]["file"], json.dumps(
            row["source"]["locator"], ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ))
        if locator_key in target_locators:
            raise ValueError(f"Multiple translated records target one source locator: {target_locators[locator_key]} and {row['id']}")
        target_locators[locator_key] = row["id"]
        grouped[row["source"]["file"]].append(row)

    outputs: dict[str, bytes] = {}
    original_bytes: dict[str, bytes] = {}
    for rel, items in grouped.items():
        raw = raw_sources[rel]
        original_bytes[rel] = raw
        if rel.lower().endswith(".js"):
            allowed = {"js_string_literal", "plugin_parameter"}
            if any(row["source"]["writeback"] not in allowed for row in items):
                raise ValueError(f"Unsupported non-JavaScript locator in {rel}")
            had_bom = raw.startswith(b"\xef\xbb\xbf")
            text = raw.decode("utf-8-sig")
            for row in items:
                current = get_record_source_text(row, text, rel)
                if current != row["source_text"]:
                    raise ValueError(f"Source text changed at locator for {row['id']}")
            # Descending static offsets keep later source locators valid. Plugin
            # parameters are re-resolved by their structural JSON path each time.
            def source_position(row: dict[str, Any]) -> int:
                locator = row["source"]["locator"]
                if row["source"]["writeback"] == "js_string_literal":
                    return locator["char_offset"]
                return plugin_parameter_span(text, locator)[0]
            for row in sorted(items, key=source_position, reverse=True):
                text = replace_source(row, text, rel, row["translation"])
            outputs[rel] = (b"\xef\xbb\xbf" if had_bom else b"") + text.encode("utf-8")
        elif rel.lower().endswith(".txt"):
            if any(row["source"]["writeback"] != "text_file_line" for row in items):
                raise ValueError(f"Unsupported locator in plain-text source {rel}")
            had_bom = raw.startswith(b"\xef\xbb\xbf")
            document = raw.decode("utf-8-sig")
            for row in items:
                current = get_record_source_text(row, document, rel)
                if current != row["source_text"]:
                    raise ValueError(f"Source text changed at locator for {row['id']}")
            for row in sorted(items, key=lambda item: item["source"]["locator"]["line_number"], reverse=True):
                document = replace_source(row, document, rel, row["translation"])
            outputs[rel] = (b"\xef\xbb\xbf" if had_bom else b"") + document.encode("utf-8")
        else:
            document = json.loads(raw.decode("utf-8"))
            for row in items:
                current = get_record_source_text(row, document, rel)
                if current != row["source_text"]:
                    raise ValueError(f"Source text changed at locator for {row['id']}")
            # Validate every original locator before making any mutation.
            for row in items:
                document = replace_source(row, document, rel, row["translation"])
            outputs[rel] = (json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")

    report = {
        "schema": "tgo-translation-apply-report-v1",
        "records_read": len(rows),
        "records_translated": len(translated_rows),
        "records_untranslated": len(rows) - len(translated_rows),
        "source_files_verified": len(raw_sources),
        "source_files_changed": len(outputs),
        "changed_files": {
            rel: {"source_sha256": sha256_bytes(original_bytes[rel]),
                  "output_sha256": sha256_bytes(outputs[rel]),
                  "translated_records": len(grouped[rel])}
            for rel in sorted(outputs)
        },
        "check_only": check_only,
    }
    if not check_only:
        for rel, data in outputs.items():
            atomic_write(out / rel, data)
        atomic_write(out / "apply_report.json",
                     (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, nargs="+", required=True,
                        help="translated JSONL file(s) or a directory containing JSONL files")
    parser.add_argument("--source", type=Path, default=SOURCE_ROOT,
                        help="unchanged TGO source root used by the export")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="new staging output under ignored google_drive/")
    parser.add_argument("--check", action="store_true", help="validate without writing files")
    parser.add_argument("--require-complete", action="store_true",
                        help="fail if any record has an empty translation")
    args = parser.parse_args()
    private_root = (REPO_ROOT / "google_drive").resolve()
    source = args.source.resolve()
    out = args.out.resolve()
    if source != private_root and private_root not in source.parents:
        raise ValueError("Refusing to read translation source outside ignored google_drive/")
    if out != private_root and private_root not in out.parents:
        raise ValueError("Refusing to write patched game data outside ignored google_drive/")
    if out == source or out in source.parents:
        raise ValueError("Output must not be the source root or one of its parent directories")
    report = apply_records(args.input, source, out, args.check, args.require_complete)
    print(f"Records: {report['records_read']}; translated: {report['records_translated']}; "
          f"untranslated: {report['records_untranslated']}")
    print(f"Source files verified: {report['source_files_verified']}; "
          f"files to change: {report['source_files_changed']}")
    print("No game code was executed; source files were not overwritten.")
    if args.check:
        print("Validation only; no files written.")
    else:
        print(f"New staged files written under: {out.relative_to(private_root).as_posix()}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
