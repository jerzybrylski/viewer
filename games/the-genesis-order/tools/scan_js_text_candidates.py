#!/usr/bin/env python3
"""Statically inventory likely display strings in TGO JavaScript sources.

The result is a private review queue, not a translation export. Every candidate
is explicitly unclassified; this tool does not run JavaScript or infer dialogue.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

from build_source_manifest import plugin_rows
from export_translation import TOKEN_RE

REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = REPO_ROOT / "google_drive" / "the-genesis-order"
JS_ROOT = SOURCE_ROOT / "www" / "js"
DEFAULT_OUT = SOURCE_ROOT / "translation" / "review-v2"

DISPLAY_API_RE = re.compile(
    r"\b(?:drawText(?:Ex)?|addCommand|addText|setText|setHelpWindowItem|"
    r"drawActor(?:Name|Nickname|Profile)|drawItemName|drawCurrencyValue|"
    r"createCommandWindow|addOption|setItem|drawDescription|drawMessage|"
    r"Window_(?:Base|Selectable|Command|Options)|TextManager|Graphics\.print(?:Full)?Error|"
    r"(?:window\s*\.\s*)?(?:alert|confirm|prompt)|connectionType)\b"
)
UI_PARAMETER_RE = re.compile(
    r"(?:text|label|title|message|help|description|desc|command|name|prompt|"
    r"confirm|cancel|option|menu|category|header|question|word|caption|hint)",
    re.IGNORECASE,
)
NON_TEXT_PARAMETER_RE = re.compile(
    r"^(?:-?\d+(?:\.\d+)?|true|false|null|#[0-9a-f]{3,8}|(?:\d+,?)+)$",
    re.IGNORECASE,
)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def decode_js_string(raw: str) -> str:
    if raw.startswith("`"):
        body = raw[1:-1]
    else:
        body = raw[1:-1]
    out: list[str] = []
    i = 0
    while i < len(body):
        char = body[i]
        if char != "\\" or i + 1 >= len(body):
            out.append(char)
            i += 1
            continue
        nxt = body[i + 1]
        if nxt in "\r\n":
            i += 2
            if nxt == "\r" and i < len(body) and body[i] == "\n":
                i += 1
            continue
        simple = {"n": "\n", "r": "\r", "t": "\t", "b": "\b", "f": "\f", "v": "\v",
                  "0": "\0", "\\": "\\", "'": "'", '"': '"', "`": "`"}
        if nxt in simple:
            out.append(simple[nxt])
            i += 2
        elif nxt == "x" and i + 3 < len(body) and re.fullmatch(r"[0-9a-fA-F]{2}", body[i + 2:i + 4]):
            out.append(chr(int(body[i + 2:i + 4], 16)))
            i += 4
        elif nxt == "u":
            if i + 2 < len(body) and body[i + 2] == "{":
                end = body.find("}", i + 3)
                digits = body[i + 3:end] if end != -1 else ""
                if end != -1 and re.fullmatch(r"[0-9a-fA-F]{1,6}", digits):
                    out.append(chr(int(digits, 16)))
                    i = end + 1
                else:
                    out.extend(("\\", "u"))
                    i += 2
            elif i + 5 < len(body) and re.fullmatch(r"[0-9a-fA-F]{4}", body[i + 2:i + 6]):
                out.append(chr(int(body[i + 2:i + 6], 16)))
                i += 6
            else:
                out.extend(("\\", "u"))
                i += 2
        else:
            # Unknown escape sequences are preserved, not silently discarded.
            out.extend(("\\", nxt))
            i += 2
    return "".join(out)


def iter_literals(source: str) -> Iterator[dict[str, Any]]:
    """Yield quoted JS literals while skipping line/block comments.

    This conservative lexer is for review inventory only. Regex literals and
    nested template expressions may yield false negatives/positives; no result
    is promoted to a translatable record automatically.
    """
    i = 0
    line = 1
    length = len(source)
    while i < length:
        char = source[i]
        if char == "\n":
            line += 1
            i += 1
            continue
        if char == "/" and i + 1 < length and source[i + 1] == "/":
            end = source.find("\n", i + 2)
            i = length if end == -1 else end
            continue
        if char == "/" and i + 1 < length and source[i + 1] == "*":
            end = source.find("*/", i + 2)
            stop = length if end == -1 else end + 2
            line += source[i:stop].count("\n")
            i = stop
            continue
        if char not in "'\"`":
            i += 1
            continue
        start = i
        start_line = line
        quote = char
        i += 1
        escaped = False
        dynamic_template = False
        while i < length:
            current = source[i]
            if current == "\n":
                line += 1
            if quote == "`" and not escaped and source.startswith("${", i):
                dynamic_template = True
            if escaped:
                escaped = False
                i += 1
            elif current == "\\":
                escaped = True
                i += 1
            elif current == quote:
                i += 1
                raw = source[start:i]
                yield {
                    "raw": raw,
                    "value": None if dynamic_template else decode_js_string(raw),
                    "start": start,
                    "end": i,
                    "line": start_line,
                    "dynamic_template": dynamic_template,
                }
                break
            else:
                i += 1


def candidate_id(kind: str, locator: dict[str, Any]) -> str:
    payload = json.dumps(locator, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return f"tgo:{kind}:{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:20]}"


def make_record(kind: str, text: str, source_file: str, source_hash: str,
                locator: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "tgo-text-review-candidate-v1",
        "id": candidate_id(kind, locator),
        "category": kind,
        "classification": "unreviewed_candidate_not_translation",
        "source_text": text,
        "translation": "",
        "markup_tokens": TOKEN_RE.findall(text),
        "source": {"file": source_file, "sha256": source_hash, "locator": locator},
        "context": context,
    }


def config_candidates(path: Path, plugin_states: dict[str, str]) -> tuple[list[dict[str, Any]], Counter]:
    rows = plugin_rows(path)
    source_hash = file_sha256(path)
    candidates = []
    counts = Counter()
    rel = path.relative_to(SOURCE_ROOT).as_posix()
    for index, plugin in enumerate(rows):
        name = plugin.get("name")
        parameters = plugin.get("parameters")
        if not isinstance(name, str) or not isinstance(parameters, dict):
            continue
        for key, value in parameters.items():
            if not isinstance(value, str) or not value.strip() or NON_TEXT_PARAMETER_RE.fullmatch(value.strip()):
                continue
            counts["string_parameters"] += 1
            likely_ui = bool(UI_PARAMETER_RE.search(str(key)))
            counts["parameter_key_suggests_ui"] += likely_ui
            locator = {"file": rel, "plugin_index": index, "plugin_name": name,
                       "parameter_key": str(key), "json_path": f"/$plugins/{index}/parameters/{key}"}
            candidates.append(make_record(
                "plugin_parameter_candidate", value, rel, source_hash, locator,
                {"plugin_name": name, "plugin_status": plugin_states.get(name, "unknown"),
                 "parameter_key": str(key), "heuristic_ui_key": likely_ui},
            ))
    return candidates, counts


def scan_source_files() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not JS_ROOT.is_dir():
        raise FileNotFoundError(f"TGO JavaScript source directory not found: {JS_ROOT}")
    config_path = JS_ROOT / "plugins.js"
    config_rows = plugin_rows(config_path)
    states = {row.get("name"): ("enabled" if row.get("status") else "disabled")
              for row in config_rows if isinstance(row.get("name"), str)}
    records, parameter_counts = config_candidates(config_path, states)
    file_stats: dict[str, Any] = {}
    for path in sorted(JS_ROOT.rglob("*.js")):
        rel = path.relative_to(SOURCE_ROOT).as_posix()
        # Decode bytes without universal-newline conversion so char_offset refers
        # to the exact UTF-8 source text the applier will inspect and preserve.
        text = path.read_bytes().decode("utf-8-sig", errors="replace")
        digest = file_sha256(path)
        total = 0
        likely = 0
        dynamic = 0
        if "/libs/" not in rel and path.name != "plugins.js":
            for literal in iter_literals(text):
                total += 1
                if literal["dynamic_template"]:
                    dynamic += 1
                    continue
                value = literal["value"]
                if not isinstance(value, str) or not value.strip():
                    continue
                context_text = text[max(0, literal["start"] - 140):min(len(text), literal["end"] + 140)]
                api_hits = sorted(set(DISPLAY_API_RE.findall(context_text)))
                if not api_hits:
                    continue
                likely += 1
                locator = {"file": rel, "line": literal["line"],
                           "char_offset": literal["start"], "literal_index_in_file": total}
                plugin_name = path.stem if path.parent.name == "plugins" else None
                records.append(make_record(
                    "js_display_literal_candidate", value, rel, digest, locator,
                    {"nearby_display_api_names": api_hits,
                     "plugin_name": plugin_name,
                     "plugin_status": states.get(plugin_name, "not_a_configured_plugin")
                                      if plugin_name else "engine_source",
                     "literal_kind": "template" if literal["raw"].startswith("`") else "quoted",
                     "heuristic_only": True},
                ))
            # The connection-status getter returns a display value hundreds of
            # characters away from its drawText call. Its function-level data
            # flow was reviewed statically; include otherwise-missed returns.
            if path.name == "LovenseIntegration.js":
                function_start = text.find("lovense.connectionType = function")
                function_end = text.find("};", function_start) if function_start >= 0 else -1
                display_flow = re.search(r"drawText\([^;]*lovense\.connectionType\(\)", text)
                if function_start >= 0 and function_end > function_start and display_flow:
                    for literal_index, literal in enumerate(iter_literals(text), 1):
                        if (function_start < literal["start"] < function_end
                                and literal["value"] == "Not Connected"
                                and not literal["dynamic_template"]):
                            locator = {"file": rel, "line": literal["line"],
                                       "char_offset": literal["start"],
                                       "literal_index_in_file": literal_index}
                            records.append(make_record(
                                "js_display_literal_candidate", literal["value"], rel, digest, locator,
                                {"nearby_display_api_names": ["connectionType"],
                                 "plugin_name": "LovenseIntegration",
                                 "plugin_status": states.get("LovenseIntegration", "unknown"),
                                 "literal_kind": "quoted", "heuristic_only": False,
                                 "flow_evidence": "connectionType return value is concatenated into Window_DeviceList.drawText"},
                            ))
                            likely += 1
        file_stats[rel] = {"size_bytes": path.stat().st_size, "sha256": digest,
                           "string_literals_scanned": total,
                           "likely_display_context_candidates": likely,
                           "dynamic_template_literals": dynamic}
    counts = {
        "js_source_files": len(file_stats),
        "plugin_parameter_string_candidates": parameter_counts["string_parameters"],
        "plugin_parameter_keys_suggesting_ui": parameter_counts["parameter_key_suggests_ui"],
        "display_context_literal_candidates": sum(x["likely_display_context_candidates"] for x in file_stats.values()),
        "dynamic_template_literals_not_decoded": sum(x["dynamic_template_literals"] for x in file_stats.values()),
        "review_candidates_written": len(records),
        "js_files_excluded_from_literal_parse": [p.relative_to(SOURCE_ROOT).as_posix()
                                                   for p in sorted(JS_ROOT.glob("libs/*.js"))],
    }
    return records, {"counts": counts, "files": file_stats}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    out = args.out.resolve()
    private_root = (REPO_ROOT / "google_drive").resolve()
    if out != private_root and private_root not in out.parents:
        raise ValueError("Refusing to write text candidates outside ignored google_drive/")
    records, report = scan_source_files()
    out.mkdir(parents=True, exist_ok=True)
    records.sort(key=lambda row: (row["source"]["file"], row["id"]))
    temp = out / "js_text_candidates.jsonl.tmp"
    with temp.open("w", encoding="utf-8", newline="\n") as stream:
        for row in records:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    temp.replace(out / "js_text_candidates.jsonl")
    (out / "scan_manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"JS files scanned: {report['counts']['js_source_files']}")
    print(f"Review candidates written: {report['counts']['review_candidates_written']}")
    print("No candidate is automatically classified as translatable. Source strings were not printed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
