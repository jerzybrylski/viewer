#!/usr/bin/env python3
"""Export confirmed TGO text channels to deterministic, locator-based JSONL.

This is a static RPG Maker MV data parser: it never imports or runs game JS.
The final extracted-text bundle is stored under games/the-genesis-order/translation;
original game assets remain under ignored google_drive/ and are never copied to Git.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = REPO_ROOT / "google_drive" / "the-genesis-order"
DATA_ROOT = SOURCE_ROOT / "data"
TRACKED_TRANSLATION_ROOT = REPO_ROOT / "games" / "the-genesis-order" / "translation"
DEFAULT_OUT = TRACKED_TRANSLATION_ROOT / "export-v1"
DEFAULT_REVIEWED_JS = SOURCE_ROOT / "translation" / "export-v1" / "reviewed_js_ui.jsonl"

ASSIGNMENT_RE = re.compile(
    r"\$gameVariables\s*\.\s*setValue\s*\(\s*(\d+)\s*,\s*"
    r"(\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')",
    re.IGNORECASE,
)
TOKEN_RE = re.compile(
    r"\\[A-Za-z]+(?:\[[^\]]*\])?|\\[{}]|<[^>]+>|%\d*(?:\$)?[sdif]"
)
POINTER_ESCAPE = str.maketrans({"~": "~0", "/": "~1"})

# Explicitly chosen display-language fields. Editor notes, asset names, map labels
# and JS literals are handled separately rather than assumed to be dialogue.
DATABASE_FIELDS: dict[str, tuple[str, ...]] = {
    "Actors.json": ("name", "nickname", "profile"),
    "Classes.json": ("name", "description"),
    "Items.json": ("name", "description", "message1", "message2", "message3", "message4"),
    "Weapons.json": ("name", "description", "message1", "message2", "message3", "message4"),
    "Armors.json": ("name", "description", "message1", "message2", "message3", "message4"),
    "Skills.json": ("name", "description", "message1", "message2", "message3", "message4"),
    "Enemies.json": ("name",),
    "States.json": ("name", "message1", "message2", "message3", "message4"),
}
SYSTEM_FIELDS = (
    "gameTitle", "currencyUnit", "elements", "weaponTypes", "armorTypes",
    "equipTypes", "skillTypes", "terms",
)
KNOWN_RENDERER_EVENTS = {53, 60, 222, 223, 224}
KNOWN_PHONE_LIST_EVENT = 17
KNOWN_PHONE_TEXT_EVENT = 54
KNOWN_UI_CHOICE_EVENTS = {17, 30, 54, 257, 263, 272}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_id(category: str, locator: dict[str, Any]) -> str:
    payload = json.dumps(locator, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]
    return f"tgo:{category}:{digest}"


def pointer(*parts: object) -> str:
    return "/" + "/".join(str(part).translate(POINTER_ESCAPE) for part in parts)


def tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def record(
    *, category: str, status: str, text: str, source_file: str,
    source_hash: str, locator: dict[str, Any], context: dict[str, Any] | None = None,
    structure: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema": "tgo-translation-record-v1",
        "id": canonical_id(category, locator),
        "category": category,
        "classification": status,
        "source_text": text,
        "translation": "",
        "markup_tokens": tokens(text),
        "source": {
            "file": source_file,
            "sha256": source_hash,
            "locator": locator,
            "writeback": (
                "plugin_parameter" if "plugin_index" in locator
                else "js_string_literal" if "char_offset" in locator
                else "event_script_expression" if locator.get("expression_kind") == "variable_value"
                else "json_string_leaf" if "json_path" in locator
                else "text_file_line" if "line_number" in locator and source_file.lower().endswith(".txt")
                else "script_string_literal"
            ),
        },
        "context": context or {},
        "structure": structure or {},
    }


def map_names(data_root: Path) -> dict[int, str]:
    path = data_root / "MapInfos.json"
    if not path.exists():
        return {}
    rows = load_json(path)
    return {
        row["id"]: row.get("name", "")
        for row in rows if isinstance(row, dict) and isinstance(row.get("id"), int)
    }


def actor_face_index(data_root: Path) -> dict[tuple[str, int], list[dict[str, Any]]]:
    path = data_root / "Actors.json"
    result: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    if not path.exists():
        return result
    for actor in load_json(path):
        if not isinstance(actor, dict) or not isinstance(actor.get("id"), int):
            continue
        face = actor.get("faceName")
        index = actor.get("faceIndex")
        if isinstance(face, str) and face and isinstance(index, int):
            result[(face, index)].append({
                "actor_id": actor["id"], "name": actor.get("name", "")
            })
    return result


def speaker_for(message_header: dict[str, Any], face_index: dict) -> dict[str, Any] | None:
    face = message_header.get("faceName")
    index = message_header.get("faceIndex")
    if not isinstance(face, str) or not face:
        return None
    candidates = face_index.get((face, index), [])
    if len(candidates) == 1:
        return {
            **candidates[0], "face_name": face, "face_index": index,
            "confidence": "unique_actor_face_match",
        }
    return {"face_name": face, "face_index": index, "confidence": "face_asset_only"}


def event_context(
    *, source_kind: str, map_id: int | None, map_name: str, event: dict[str, Any],
    page_number: int | None, page: dict[str, Any] | None, command_index: int,
    message_header: dict[str, Any] | None, face_index: dict,
    branch: list[dict[str, Any]],
) -> dict[str, Any]:
    context: dict[str, Any] = {
        "source_kind": source_kind,
        "event_id": event.get("id"),
        "event_name": event.get("name"),
        "page_number": page_number,
        "command_index": command_index,
        "branch_path": branch,
    }
    if map_id is not None:
        context.update({"map_id": map_id, "map_name": map_name})
    if page is not None:
        context["page_conditions"] = page.get("conditions", {})
    if message_header is not None:
        context["message_header"] = {
            key: message_header.get(key)
            for key in ("faceName", "faceIndex", "background", "positionType")
        }
        context["speaker"] = speaker_for(message_header, face_index)
    return context


def event_source_lists(data_root: Path, map_labels: dict[int, str]):
    for path in sorted(data_root.glob("Map[0-9][0-9][0-9].json")):
        map_id = int(path.stem[-3:])
        data = load_json(path)
        for event in data.get("events", []):
            if not isinstance(event, dict):
                continue
            for page_number, page in enumerate(event.get("pages", []), start=1):
                if isinstance(page, dict):
                    yield path, "map", map_id, map_labels.get(map_id, ""), event, page_number, page
    path = data_root / "CommonEvents.json"
    if path.exists():
        for event in load_json(path):
            if isinstance(event, dict) and isinstance(event.get("id"), int):
                yield path, "common_event", None, "", event, None, None


def command_records(
    *, path: Path, source_kind: str, map_id: int | None, map_name: str,
    event: dict[str, Any], page_number: int | None, page: dict[str, Any] | None,
    source_hash: str, face_index: dict,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    commands = event.get("list", []) if page is None else page.get("list", [])
    if not isinstance(commands, list):
        return [], []
    source_rel = path.relative_to(SOURCE_ROOT).as_posix()
    event_id = event.get("id")
    event_id_text = f"{event_id:03d}" if isinstance(event_id, int) else "unknown"
    choice_ids: dict[int, str] = {}
    for index, cmd in enumerate(commands):
        if isinstance(cmd, dict) and cmd.get("code") == 102:
            loc = {
                "file": source_rel, "event_id": event_id,
                "page_number": page_number, "command_index": index,
                "choice_options_path": pointer("list", index, "parameters", 0),
            }
            choice_ids[index] = canonical_id("choice_group", loc)

    records: list[dict[str, Any]] = []
    renderer_scaffolds: list[dict[str, Any]] = []
    message_header: dict[str, Any] | None = None
    message_block_id: str | None = None
    scroll_block_id: str | None = None
    branch_stack: list[dict[str, Any]] = []
    active_choice: tuple[int, str] | None = None
    for index, command in enumerate(commands):
        if not isinstance(command, dict):
            continue
        code = command.get("code")
        params = command.get("parameters") or []
        branch = [dict(item) for item in branch_stack]
        context = event_context(
            source_kind=source_kind, map_id=map_id, map_name=map_name,
            event=event, page_number=page_number, page=page, command_index=index,
            message_header=message_header, face_index=face_index, branch=branch,
        )
        if code == 101:
            message_header = {
                key: params[pos] if len(params) > pos else None
                for pos, key in enumerate(("faceName", "faceIndex", "background", "positionType"))
            }
            message_block_id = canonical_id("message_block", {
                "file": source_rel, "event_id": event_id, "page_number": page_number,
                "header_command_index": index,
            })
        elif code == 105:
            scroll_block_id = canonical_id("scroll_block", {
                "file": source_rel, "event_id": event_id, "page_number": page_number,
                "header_command_index": index,
            })
        elif code == 401 and params and isinstance(params[0], str) and params[0].strip():
            text = params[0]
            is_renderer = source_kind == "common_event" and event_id in KNOWN_RENDERER_EVENTS
            if is_renderer:
                renderer_scaffolds.append({"common_event_id": event_id, "command_index": index})
                continue
            category = "native_message_unclassified"
            # Code 401 is rendered as message-window text. Keep semantic subtype
            # (story, tutorial, notification, or UI) unclassified rather than
            # withholding a proven visible text surface from localization.
            classification = "confirmed_text_surface"
            if source_kind == "common_event" and event_id == KNOWN_PHONE_LIST_EVENT:
                category, classification = "phone_contact_ui", "confirmed_ui"
            elif source_kind == "common_event" and event_id == KNOWN_PHONE_TEXT_EVENT:
                category, classification = "phone_text", "confirmed_phone_channel"
            locator = {
                "json_path": pointer("list", index, "parameters", 0),
                "file": source_rel, "event_id": event_id, "page_number": page_number,
                "command_index": index, "command_code": code,
            }
            message_context = {
                **context,
                "message_block_id": message_block_id,
                "visibility_evidence": "RPG Maker MV command 401 is rendered in the message window.",
                "semantic_subtype": "dialogue_tutorial_notification_or_ui_unclassified",
            }
            message_structure = {
                "command_code": code,
                "message_block_id": message_block_id,
                "rendering_evidence": "visible_message_window_text",
            }
            if source_kind == "common_event" and event_id == 224:
                message_context.update({
                    "rendering_role_candidate": "image_cache_sequence",
                    "known_static_call_sites_to_common_event": 67,
                })
                message_structure["review_note"] = "This specific 401 is visible message-window text; the common event's separate image-cache role does not make it a renderer placeholder."
            records.append(record(
                category=category, status=classification, text=text,
                source_file=source_rel, source_hash=source_hash, locator=locator,
                context=message_context,
                structure=message_structure,
            ))
        elif code == 405 and params and isinstance(params[0], str) and params[0].strip():
            text = params[0]
            locator = {
                "json_path": pointer("list", index, "parameters", 0),
                "file": source_rel, "event_id": event_id, "page_number": page_number,
                "command_index": index, "command_code": code,
            }
            records.append(record(
                category="scrolling_text", status="confirmed_dialogue_or_ui", text=text,
                source_file=source_rel, source_hash=source_hash, locator=locator,
                context={**context, "scroll_block_id": scroll_block_id},
                structure={"command_code": code, "scroll_block_id": scroll_block_id},
            ))
        elif code == 102 and params and isinstance(params[0], list):
            options = params[0]
            group_id = choice_ids[index]
            ui = source_kind == "common_event" and event_id in KNOWN_UI_CHOICE_EVENTS
            for option_index, text in enumerate(options):
                if not isinstance(text, str) or not text.strip():
                    continue
                locator = {
                    "json_path": pointer("list", index, "parameters", 0, option_index),
                    "file": source_rel, "event_id": event_id, "page_number": page_number,
                    "command_index": index, "command_code": code,
                    "option_index": option_index,
                }
                records.append(record(
                    category="ui_choice" if ui else "choice_unclassified",
                    status="confirmed_ui" if ui else "confirmed_text_surface",
                    text=text, source_file=source_rel, source_hash=source_hash,
                    locator=locator,
                    context={**context, "choice_group_id": group_id,
                             "choice_index": option_index, "choice_count": len(options),
                             "cancel_type": params[1] if len(params) > 1 else None,
                             "default_type": params[2] if len(params) > 2 else None,
                             "visibility_evidence": "RPG Maker MV command 102 is displayed by the choice window.",
                             "semantic_subtype": "story_or_ui_choice" if ui else "story_or_ui_unclassified"},
                    structure={"command_code": code, "option_index": option_index,
                               "option_count": len(options), "choice_group_id": group_id},
                ))

        # Update a conservative structural branch stack for the next command.
        if code == 102:
            active_choice = (index, choice_ids[index])
        elif code == 111:
            branch_stack.append({"kind": "condition", "command_index": index,
                                 "parameters": params, "arm": "then"})
        elif code == 411:
            for item in reversed(branch_stack):
                if item["kind"] == "condition":
                    item["arm"] = "else"
                    break
        elif code == 412:
            for pos in range(len(branch_stack) - 1, -1, -1):
                if branch_stack[pos]["kind"] == "condition":
                    del branch_stack[pos:]
                    break
        elif code == 402:
            branch_stack.append({
                "kind": "choice_branch",
                "choice_command_index": active_choice[0] if active_choice else None,
                "choice_group_id": active_choice[1] if active_choice else None,
                "option_index": params[0] if params else None,
                "branch_label": params[1] if len(params) > 1 else None,
            })
        elif code == 403:
            branch_stack.append({
                "kind": "choice_cancel",
                "choice_command_index": active_choice[0] if active_choice else None,
                "choice_group_id": active_choice[1] if active_choice else None,
            })
        elif code == 404:
            while branch_stack and branch_stack[-1]["kind"] not in {"choice_branch", "choice_cancel"}:
                branch_stack.pop()
            if branch_stack:
                branch_stack.pop()
            active_choice = None
    return records, renderer_scaffolds


def routed_common_event(commands: list[dict[str, Any]], start: int, variable_id: int) -> int | None:
    for later in commands[start + 1:]:
        if not isinstance(later, dict):
            continue
        if later.get("code") in (355, 655):
            args = later.get("parameters") or []
            line = args[0] if args and isinstance(args[0], str) else ""
            if any(int(m.group(1)) == variable_id for m in ASSIGNMENT_RE.finditer(line)):
                return None
        if later.get("code") == 117:
            args = later.get("parameters") or []
            return args[0] if args and isinstance(args[0], int) else None
    return None


def script_branch_paths(commands: list[dict[str, Any]], source_rel: str,
                        event_id: int | None, page_number: int | None) -> list[list[dict[str, Any]]]:
    """Mirror RPG Maker conditional/choice nesting without choosing a route."""
    choice_ids = {}
    for index, command in enumerate(commands):
        if isinstance(command, dict) and command.get("code") == 102:
            choice_ids[index] = canonical_id("choice_group", {
                "file": source_rel, "event_id": event_id,
                "page_number": page_number, "command_index": index,
                "choice_options_path": pointer("list", index, "parameters", 0),
            })
    paths: list[list[dict[str, Any]]] = []
    stack: list[dict[str, Any]] = []
    active_choice: tuple[int, str] | None = None
    for index, command in enumerate(commands):
        paths.append([dict(item) for item in stack])
        if not isinstance(command, dict):
            continue
        code = command.get("code")
        params = command.get("parameters") or []
        if code == 102:
            active_choice = (index, choice_ids[index])
        elif code == 111:
            stack.append({"kind": "condition", "command_index": index,
                          "parameters": params, "arm": "then"})
        elif code == 411:
            for item in reversed(stack):
                if item["kind"] == "condition":
                    item["arm"] = "else"
                    break
        elif code == 412:
            for pos in range(len(stack) - 1, -1, -1):
                if stack[pos]["kind"] == "condition":
                    del stack[pos:]
                    break
        elif code == 402:
            stack.append({"kind": "choice_branch",
                          "choice_command_index": active_choice[0] if active_choice else None,
                          "choice_group_id": active_choice[1] if active_choice else None,
                          "option_index": params[0] if params else None,
                          "branch_label": params[1] if len(params) > 1 else None})
        elif code == 403:
            stack.append({"kind": "choice_cancel",
                          "choice_command_index": active_choice[0] if active_choice else None,
                          "choice_group_id": active_choice[1] if active_choice else None})
        elif code == 404:
            while stack and stack[-1]["kind"] not in {"choice_branch", "choice_cancel"}:
                stack.pop()
            if stack:
                stack.pop()
            active_choice = None
    return paths


def script_channel_records(
    *, path: Path, source_kind: str, map_id: int | None, map_name: str,
    event: dict[str, Any], page_number: int | None, page: dict[str, Any] | None,
    source_hash: str,
) -> list[dict[str, Any]]:
    commands = event.get("list", []) if page is None else page.get("list", [])
    if not isinstance(commands, list):
        return []
    source_rel = path.relative_to(SOURCE_ROOT).as_posix()
    event_id = event.get("id")
    branch_paths = script_branch_paths(commands, source_rel, event_id, page_number)
    page_conditions = page.get("conditions", {}) if isinstance(page, dict) else None
    result: list[dict[str, Any]] = []
    for index, command in enumerate(commands):
        if not isinstance(command, dict) or command.get("code") not in (355, 655):
            continue
        params = command.get("parameters") or []
        script = params[0] if params and isinstance(params[0], str) else ""
        for assignment_index, match in enumerate(ASSIGNMENT_RE.finditer(script)):
            variable_id = int(match.group(1))
            try:
                raw_value = ast.literal_eval(match.group(2))
            except (SyntaxError, ValueError):
                continue
            target = routed_common_event(commands, index, variable_id)
            if (variable_id, target) == (21, 60):
                separator = "."
                if separator not in raw_value:
                    continue
                header, text = raw_value.split(separator, 1)
                category, classification = "custom_dialogue", "confirmed_dialogue"
            elif (variable_id, target) == (21, 222):
                header, text, category, classification = "", raw_value, "arianna_hint", "confirmed_ui"
            elif (variable_id, target) == (25, 53):
                header, text, category, classification = "", raw_value, "phone_text", "confirmed_phone_channel"
            elif (variable_id, target) == (107, 223):
                header, text, category, classification = "", raw_value, "item_found_label", "confirmed_ui"
            elif target == 224 and variable_id in (97, 98):
                # CE224's two 401 lines are only a formatted renderer for these
                # two text variables; export caller literals instead of markup.
                header, text, category, classification = "", raw_value, "image_caption", "confirmed_ui"
            else:
                continue
            locator = {
                "file": source_rel,
                "event_id": event_id,
                "page_number": page_number,
                "command_index": index,
                "command_code": command.get("code"),
                "parameter_index": 0,
                "assignment_index": assignment_index,
                "script_literal_offset": match.start(2),
                "variable_id": variable_id,
                "routed_common_event_id": target,
            }
            context = {
                "source_kind": source_kind,
                "map_id": map_id,
                "map_name": map_name,
                "event_id": event_id,
                "event_name": event.get("name"),
                "page_number": page_number,
                "page_conditions": page_conditions,
                "command_index": index,
                "branch_path": branch_paths[index] if index < len(branch_paths) else [],
                "custom_header": header or None,
                "speaker": None,
                "speaker_status": "header_requires_mapping" if header else "unknown",
            }
            if category == "image_caption":
                context.update({
                    "visibility_evidence": "Static string assigned to a variable displayed by CE224 command 401.",
                    "rendered_placeholder_variable": variable_id,
                    "semantic_subtype": "gallery_or_scene_caption",
                })
            result.append(record(
                category=category, status=classification, text=text,
                source_file=source_rel, source_hash=source_hash,
                locator=locator, context=context,
                structure={
                    "command_code": command.get("code"),
                    "variable_id": variable_id,
                    "routed_common_event_id": target,
                    "raw_value": raw_value,
                    "header": header,
                    "separator": "." if header else None,
                    "script_literal": match.group(2),
                    **({"display_slot": "CE224_variable_caption"} if category == "image_caption" else {}),
                },
            ))
    return result


VARIABLE_ESCAPE_RE = re.compile(r"\\[Vv]\[(\d+)\]", re.IGNORECASE)
VARIABLE_DISPLAY_CODES = {
    401: "message_window",
    405: "scrolling_text",
    102: "choice_menu",
    402: "choice_branch_label",
}


def walk_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)


def variable_display_records(
    *, path: Path, source_kind: str, map_id: int | None, map_name: str,
    event: dict[str, Any], page_number: int | None, page: dict[str, Any] | None,
    source_hash: str,
) -> list[dict[str, Any]]:
    """Extract static script-expression values proven to reach visible text.

    RPG Maker's variable escape is resolved by the message/choice renderer, so
    a static string assigned through command 122 is a display value even though
    it is not itself stored in a command 401/102 string. Only literal JS string
    expressions are accepted; nonliteral expressions are deliberately skipped.
    """
    commands = event.get("list", []) if page is None else page.get("list", [])
    if not isinstance(commands, list):
        return []
    source_rel = path.relative_to(SOURCE_ROOT).as_posix()
    event_id = event.get("id")
    visible_by_variable: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for index, command in enumerate(commands):
        if not isinstance(command, dict):
            continue
        code = command.get("code")
        if code not in VARIABLE_DISPLAY_CODES:
            continue
        for text in walk_strings(command.get("parameters", [])):
            for match in VARIABLE_ESCAPE_RE.finditer(text):
                variable_id = int(match.group(1))
                evidence = {
                    "command_index": index,
                    "command_code": code,
                    "surface": VARIABLE_DISPLAY_CODES[code],
                }
                if evidence not in visible_by_variable[variable_id]:
                    visible_by_variable[variable_id].append(evidence)

    result: list[dict[str, Any]] = []
    for index, command in enumerate(commands):
        if not isinstance(command, dict) or command.get("code") != 122:
            continue
        params = command.get("parameters") or []
        if (len(params) < 5 or not isinstance(params[0], int)
                or not isinstance(params[1], int) or params[3] != 4
                or not isinstance(params[4], str)):
            continue
        start_id, end_id = params[0], params[1]
        if end_id < start_id:
            continue
        rendered_ids = [
            variable_id for variable_id in range(start_id, end_id + 1)
            if variable_id in visible_by_variable
        ]
        if not rendered_ids:
            continue
        try:
            value = ast.literal_eval(params[4])
        except (SyntaxError, ValueError):
            continue
        if not isinstance(value, str) or not value.strip():
            continue

        is_price = re.fullmatch(r"\$[0-9][0-9,]*(?:\.[0-9]+)?", value) is not None
        is_marker = value in {"•", ">>>"}
        translation_policy = "keep_source_value" if is_price or is_marker else None
        locator = {
            "file": source_rel,
            "event_id": event_id,
            "page_number": page_number,
            "command_index": index,
            "command_code": 122,
            "parameter_index": 4,
            "expression_kind": "variable_value",
            "start_variable_id": start_id,
            "end_variable_id": end_id,
            "rendered_variable_ids": rendered_ids,
        }
        context = {
            "source_kind": source_kind,
            "map_id": map_id,
            "map_name": map_name,
            "event_id": event_id,
            "event_name": event.get("name"),
            "page_number": page_number,
            "page_conditions": page.get("conditions", {}) if isinstance(page, dict) else None,
            "command_index": index,
            "visibility_evidence": "Static command 122 string value reaches an RPG Maker variable escape in a rendered message, scrolling-text line, or choice.",
            "rendered_variable_ids": rendered_ids,
            "visible_sinks": [
                sink for variable_id in rendered_ids
                for sink in visible_by_variable[variable_id]
            ],
            "semantic_subtype": "message_or_choice_value_unclassified",
        }
        if translation_policy:
            context.update({
                "translation_policy": translation_policy,
                "translation_policy_reason": (
                    "Preserve the displayed amount and currency to avoid diverging from gameplay costs."
                    if is_price else
                    "This is a non-linguistic UI marker; preserve it exactly."
                ),
            })
        result.append(record(
            category="ui.variable_value",
            status="confirmed_text_surface",
            text=value,
            source_file=source_rel,
            source_hash=source_hash,
            locator=locator,
            context=context,
            structure={
                "command_code": 122,
                "operand_type": 4,
                "expression_kind": "static_js_string_literal",
                "start_variable_id": start_id,
                "end_variable_id": end_id,
                "display_role": "price" if is_price else "marker" if is_marker else "localized_text",
            },
        ))
    return result


def add_json_leaf(
    records: list[dict[str, Any]], *, file_path: Path, file_hash: str,
    json_path: str, text: str, category: str, context: dict[str, Any],
    classification: str = "confirmed_text_surface",
) -> None:
    if not text.strip():
        return
    locator = {"file": file_path.relative_to(SOURCE_ROOT).as_posix(), "json_path": json_path}
    records.append(record(
        category=category, status=classification, text=text,
        source_file=locator["file"], source_hash=file_hash,
        locator=locator, context=context,
        structure={"json_path": json_path},
    ))


def database_records(data_root: Path, map_labels: dict[int, str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for filename, fields in DATABASE_FIELDS.items():
        path = data_root / filename
        if not path.exists():
            continue
        data = load_json(path)
        file_hash = sha256_bytes(path.read_bytes())
        for index, row in enumerate(data):
            if not isinstance(row, dict):
                continue
            record_id = row.get("id", index)
            for field in fields:
                text = row.get(field)
                if isinstance(text, str):
                    add_json_leaf(
                        records, file_path=path, file_hash=file_hash,
                        json_path=pointer(index, field), text=text,
                        category=f"database.{path.stem.lower()}.{field}",
                        context={"database_record_id": record_id, "record_name": row.get("name")},
                    )
    system_path = data_root / "System.json"
    if system_path.exists():
        system = load_json(system_path)
        file_hash = sha256_bytes(system_path.read_bytes())
        for field in SYSTEM_FIELDS:
            value = system.get(field)
            if isinstance(value, str):
                add_json_leaf(records, file_path=system_path, file_hash=file_hash,
                              json_path=pointer(field), text=value,
                              category=f"system.{field}", context={})
            elif isinstance(value, list):
                for index, text in enumerate(value):
                    if isinstance(text, str):
                        add_json_leaf(records, file_path=system_path, file_hash=file_hash,
                                      json_path=pointer(field, index), text=text,
                                      category=f"system.{field}", context={"list_index": index})
            elif isinstance(value, dict):
                def walk(node: Any, path_parts: tuple[object, ...]) -> None:
                    if isinstance(node, dict):
                        for key, child in node.items():
                            walk(child, path_parts + (key,))
                    elif isinstance(node, list):
                        for index, child in enumerate(node):
                            walk(child, path_parts + (index,))
                    elif isinstance(node, str):
                        add_json_leaf(records, file_path=system_path, file_hash=file_hash,
                                      json_path=pointer(field, *path_parts), text=node,
                                      category=f"system.{field}", context={"term_path": list(path_parts)})
                walk(value, ())
    map_info_path = data_root / "MapInfos.json"
    if map_info_path.exists():
        file_hash = sha256_bytes(map_info_path.read_bytes())
        for index, row in enumerate(load_json(map_info_path)):
            if isinstance(row, dict) and isinstance(row.get("name"), str):
                add_json_leaf(records, file_path=map_info_path, file_hash=file_hash,
                              json_path=pointer(index, "name"), text=row["name"],
                              category="map_label", context={"map_id": row.get("id"), "map_name": row["name"],
                                                              "visibility": "possible_ui_or_editor"})
    for path in sorted(data_root.glob("Map[0-9][0-9][0-9].json")):
        data = load_json(path)
        value = data.get("displayName")
        if isinstance(value, str) and value.strip():
            add_json_leaf(records, file_path=path, file_hash=sha256_bytes(path.read_bytes()),
                          json_path=pointer("displayName"), text=value,
                          category="map_display_name", context={"map_id": int(path.stem[-3:]),
                                                                 "map_name": map_labels.get(int(path.stem[-3:]), "")})
    credits = data_root / "Credits.txt"
    if credits.exists():
        file_hash = sha256_bytes(credits.read_bytes())
        for index, text in enumerate(credits.read_text(encoding="utf-8-sig").splitlines()):
            if text.strip():
                locator = {"file": credits.relative_to(SOURCE_ROOT).as_posix(),
                           "line_number": index + 1}
                records.append(record(
                    category="credits", status="confirmed_text_surface", text=text,
                    source_file=locator["file"], source_hash=file_hash,
                    locator=locator, context={"line_number": index + 1},
                    structure={"line_ending_preserved": True},
                ))
    return records


def natural_pointer_key(value: str) -> tuple[tuple[int, object], ...]:
    parts = []
    for part in value.strip("/").split("/") if value else []:
        parts.append((0, int(part)) if part.isdigit() else (1, part))
    return tuple(parts)


def source_order(entry: dict[str, Any]) -> tuple[Any, ...]:
    locator = entry["source"]["locator"]
    context = entry["context"]
    event_id = locator.get("event_id")
    if not isinstance(event_id, int):
        event_id = context.get("database_record_id", -1)
    return (
        entry["source"]["file"], event_id if isinstance(event_id, int) else -1,
        locator.get("page_number") if isinstance(locator.get("page_number"), int) else -1,
        locator.get("command_index") if isinstance(locator.get("command_index"), int) else -1,
        locator.get("option_index") if isinstance(locator.get("option_index"), int) else -1,
        locator.get("assignment_index") if isinstance(locator.get("assignment_index"), int) else -1,
        natural_pointer_key(locator.get("json_path", "")), entry["id"],
    )


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as stream:
        for entry in records:
            stream.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def load_reviewed_js_records(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    source_hashes: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid reviewed JS record at {path}:{line_number}: {error}") from error
        if not isinstance(row, dict) or row.get("schema") != "tgo-translation-record-v1":
            raise ValueError(f"Unsupported reviewed JS record at {path}:{line_number}")
        source = row.get("source") or {}
        locator = source.get("locator") or {}
        rel = source.get("file")
        if (not isinstance(rel, str) or not rel.startswith("www/js/")
                or Path(rel).is_absolute() or ".." in Path(rel).parts
                or locator.get("file") != rel):
            raise ValueError(f"Unsafe or inconsistent reviewed JS source at {path}:{line_number}")
        if canonical_id(row.get("category", ""), locator) != row.get("id"):
            raise ValueError(f"Reviewed JS ID/locator mismatch at {path}:{line_number}")
        source_hash = source.get("sha256")
        if not isinstance(source_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", source_hash):
            raise ValueError(f"Invalid reviewed JS source hash at {path}:{line_number}")
        if rel not in source_hashes:
            source_path = SOURCE_ROOT / rel
            if not source_path.is_file():
                raise FileNotFoundError(f"Reviewed JS source missing: {rel}")
            source_hashes[rel] = sha256_bytes(source_path.read_bytes())
        if source_hashes[rel] != source_hash:
            raise ValueError(f"Reviewed JS source hash mismatch for {rel}")
        rows.append(row)
    if len({row.get("id") for row in rows}) != len(rows):
        raise ValueError("Reviewed JS file contains duplicate canonical IDs")
    return rows


def export(out: Path, reviewed_js_path: Path | None = DEFAULT_REVIEWED_JS) -> dict[str, Any]:
    if not DATA_ROOT.is_dir():
        raise FileNotFoundError(f"TGO data directory not found: {DATA_ROOT}")
    map_labels = map_names(DATA_ROOT)
    face_index = actor_face_index(DATA_ROOT)
    all_records: list[dict[str, Any]] = []
    skipped_renderer: list[dict[str, Any]] = []
    data_file_hashes: dict[str, str] = {}
    for path in event_source_lists(DATA_ROOT, map_labels):
        file_path, source_kind, map_id, map_name, event, page_number, page = path
        source_rel = file_path.relative_to(SOURCE_ROOT).as_posix()
        if source_rel not in data_file_hashes:
            data_file_hashes[source_rel] = sha256_bytes(file_path.read_bytes())
        source_hash = data_file_hashes[source_rel]
        native, scaffolds = command_records(
            path=file_path, source_kind=source_kind, map_id=map_id, map_name=map_name,
            event=event, page_number=page_number, page=page,
            source_hash=source_hash, face_index=face_index,
        )
        all_records.extend(native)
        skipped_renderer.extend(scaffolds)
        all_records.extend(script_channel_records(
            path=file_path, source_kind=source_kind, map_id=map_id, map_name=map_name,
            event=event, page_number=page_number, page=page, source_hash=source_hash,
        ))
        all_records.extend(variable_display_records(
            path=file_path, source_kind=source_kind, map_id=map_id, map_name=map_name,
            event=event, page_number=page_number, page=page, source_hash=source_hash,
        ))
    all_records.extend(database_records(DATA_ROOT, map_labels))
    reviewed_js_records = load_reviewed_js_records(reviewed_js_path)
    all_records.extend(reviewed_js_records)
    all_records.sort(key=source_order)
    ids = [entry["id"] for entry in all_records]
    if len(ids) != len(set(ids)):
        duplicates = [key for key, count in Counter(ids).items() if count > 1]
        raise ValueError(f"Stable ID collision detected ({len(duplicates)} collisions)")

    out.mkdir(parents=True, exist_ok=True)
    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in all_records:
        by_category[entry["category"]].append(entry)
    output_names = []
    for category, rows in sorted(by_category.items()):
        safe = re.sub(r"[^a-z0-9]+", "_", category.lower()).strip("_")
        filename = f"{safe}.jsonl"
        write_jsonl(out / filename, rows)
        output_names.append(filename)

    record_source_hashes = {
        entry["source"]["file"]: entry["source"]["sha256"]
        for entry in all_records
    }
    category_counts = Counter(entry["category"] for entry in all_records)
    choices = [entry for entry in all_records
               if entry["category"] in {"ui_choice", "choice_unclassified"}]
    phone_script_count = sum(
        entry["category"] == "phone_text"
        and entry["source"]["locator"].get("variable_id") == 25
        for entry in all_records
    )
    phone_native_count = sum(
        entry["category"] == "phone_text"
        and entry["source"]["locator"].get("command_code") == 401
        for entry in all_records
    )
    choice_group_count = len({entry["context"].get("choice_group_id") for entry in choices})
    coverage_checks = {
        "custom_dialogue_entries": (category_counts["custom_dialogue"], 38638),
        "custom_dialogue_unique_payloads": (len({entry["source_text"] for entry in all_records
                                                  if entry["category"] == "custom_dialogue"}), 29647),
        "arianna_hint_entries": (category_counts["arianna_hint"], 705),
        "item_found_label_entries": (category_counts["item_found_label"], 649),
        "phone_script_entries": (phone_script_count, 17),
        "phone_native_401_entries": (phone_native_count, 13),
        "phone_contact_ui_entries": (category_counts["phone_contact_ui"], 378),
        "native_message_unclassified_entries": (category_counts["native_message_unclassified"], 1122),
        "image_caption_entries": (category_counts["image_caption"], 134),
        "variable_display_entries": (category_counts["ui.variable_value"], 262),
        "variable_display_protected_entries": (sum(
            entry["category"] == "ui.variable_value"
            and entry["context"].get("translation_policy") == "keep_source_value"
            for entry in all_records
        ), 128),
        "variable_display_translatable_entries": (sum(
            entry["category"] == "ui.variable_value"
            and entry["context"].get("translation_policy") != "keep_source_value"
            for entry in all_records
        ), 134),
        "reviewed_js_ui_entries": (len(reviewed_js_records), 35),
        "choice_groups": (choice_group_count, 695),
        "choice_options_total": (len(choices), 2110),
        "ui_choice_options": (category_counts["ui_choice"], 180),
        "renderer_401_rows_skipped": (len(skipped_renderer), 8),
    }
    report = {
        "schema": "tgo-translation-export-v1",
        "source_root": "google_drive/the-genesis-order",
        "output_contains_source_text": True,
        "source_data_scope": "RPG Maker MV JSON, Credits.txt, reviewed static JavaScript UI, and statically routed variable-string channels",
        "reviewed_js_ui_records": len(reviewed_js_records),
        "reviewed_js_ui_source_files": len({row["source"]["file"] for row in reviewed_js_records}),
        "known_omissions": [
            "All 2,110 native choice options and 1,122 non-renderer native 401 message rows are exported as confirmed visible surfaces; their semantic subtype (story, tutorial, notification, or UI) is intentionally not guessed.",
            "Static source audit covered 78 JavaScript files, 563 literal candidates, 35 confirmed UI records, and 528 content-free exclusions; no direct static message/choice/draw sinks were found in event-script code beyond the separately traced channels. Runtime-only text supplied by external devices, user data, or calculated values is not a translatable source literal.",
            "Static command-122 values routed through visible \\V escapes are exported when nonblank (262 records); 132 whitespace-only values are layout placeholders and are intentionally skipped. 128 prices/markers are protected from edits.",
            "Thirty-four item note fields were inspected and contain tag/metadata rather than prose; editor-only labels and non-display metadata remain outside the extraction schema.",
            "CE224 has 67 statically counted call sites that preload KSPAGE images; its two 401 rows are renderer scaffolds, and 134 static caller values in variables 97/98 are exported as image_caption records. Any text embedded inside the referenced images remains outside the media-free scope.",
            "Lovense device-provided names and nicknames are dynamic external data. Static mode labels PC/LAN/Web are included but protected because they are runtime operands; Not Connected is a translatable UI fallback.",
        ],
        "records": len(all_records),
        "jsonl_files": output_names,
        "category_counts": dict(sorted(category_counts.items())),
        "classification_counts": dict(sorted(Counter(entry["classification"] for entry in all_records).items())),
        "coverage_checks": {
            key: {"actual": actual, "expected": expected, "passed": actual == expected}
            for key, (actual, expected) in coverage_checks.items()
        },
        "coverage_checks_passed": all(actual == expected for actual, expected in coverage_checks.values()),
        "duplicate_source_texts": sum(count - 1 for count in Counter(
            (entry["category"], entry["source_text"]) for entry in all_records
        ).values() if count > 1),
        "skipped_renderer_401_count": len(skipped_renderer),
        "source_file_hashes": dict(sorted(record_source_hashes.items())),
        "stable_ids_unique": True,
    }
    manifest_path = out / "export_manifest.json"
    previous_files: set[str] = set()
    if manifest_path.is_file():
        try:
            previous = json.loads(manifest_path.read_text(encoding="utf-8"))
            if previous.get("schema") == "tgo-translation-export-v1":
                previous_files = {
                    name for name in previous.get("jsonl_files", [])
                    if isinstance(name, str) and Path(name).name == name and name.endswith(".jsonl")
                }
        except json.JSONDecodeError:
            previous_files = set()
    temporary_manifest = manifest_path.with_name(manifest_path.name + ".tmp")
    with temporary_manifest.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary_manifest, manifest_path)
    for stale_name in previous_files - set(output_names):
        stale_path = out / stale_name
        if stale_path.is_file():
            stale_path.unlink()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--reviewed-js", type=Path, default=DEFAULT_REVIEWED_JS,
                        help="curated JS UI JSONL produced by curate_js_translation.py")
    args = parser.parse_args()
    out = args.out.resolve()
    reviewed_js = args.reviewed_js.resolve()
    private_root = (REPO_ROOT / "google_drive").resolve()
    tracked_root = TRACKED_TRANSLATION_ROOT.resolve()
    allowed_out = ((out == private_root or private_root in out.parents)
                   or (out == tracked_root or tracked_root in out.parents))
    allowed_js = ((reviewed_js == private_root or private_root in reviewed_js.parents)
                  or (reviewed_js == tracked_root or tracked_root in reviewed_js.parents))
    if not allowed_out:
        raise ValueError("Refusing to export outside google_drive/ or the tracked translation directory")
    if not allowed_js:
        raise ValueError("Reviewed JS input must be under google_drive/ or the tracked translation directory")
    report = export(out, reviewed_js)
    try:
        display_path = out.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        display_path = str(out)
    print(f"Export directory: {display_path}")
    print(f"Records: {report['records']}; unique IDs: {report['stable_ids_unique']}")
    print("Categories:")
    for category, count in report["category_counts"].items():
        print(f"  {category}: {count}")
    print(f"Skipped known renderer rows: {report['skipped_renderer_401_count']}")
    print("Source strings are intentionally not printed. See export_manifest.json for omissions.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
