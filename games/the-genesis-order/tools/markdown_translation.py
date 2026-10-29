#!/usr/bin/env python3
"""Build contextual Markdown from TGO JSONL and import translations by stable ID.

The checked-in JSONL contains extracted source text by user request; generated
Markdown, imported translations, and original game assets remain under ignored
google_drive/. No game code is executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from export_translation import REPO_ROOT, SOURCE_ROOT, canonical_id, tokens

DEFAULT_INPUT = REPO_ROOT / "games" / "the-genesis-order" / "translation" / "export-v1"
DEFAULT_MARKDOWN = SOURCE_ROOT / "translation" / "markdown-draft-v1"
DEFAULT_IMPORT = SOURCE_ROOT / "translation" / "import-v1" / "translated.jsonl"
START_RE = re.compile(
    r'^<!-- TGO-RECORD-START:([0-9a-f]{16}) id="([^"]+)" sha256="([0-9a-f]{64})" -->$',
    re.MULTILINE,
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_jsonl(paths: Iterable[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in paths:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f"Invalid JSONL at {path}:{line_number}: {error}") from error
                if not isinstance(row, dict) or not isinstance(row.get("id"), str):
                    raise ValueError(f"Invalid record at {path}:{line_number}")
                if row["id"] in seen:
                    raise ValueError(f"Duplicate canonical ID: {row['id']}")
                seen.add(row["id"])
                if row.get("schema") != "tgo-translation-record-v1":
                    raise ValueError(f"Unsupported canonical schema for {row['id']}")
                source = row.get("source") or {}
                locator = source.get("locator") or {}
                if row["id"] != canonical_id(row.get("category", ""), locator):
                    raise ValueError(f"ID/locator mismatch for {row['id']}")
                rows.append(row)
    if not rows:
        raise ValueError("No canonical translation records found")
    return rows


def input_paths(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        paths = sorted(path.glob("*.jsonl"))
        if paths:
            return paths
    raise FileNotFoundError(f"No JSONL input found at {path}")


def safe_fence(text: str, language: str = "") -> str:
    runs = [len(match.group(0)) for match in re.finditer(r"`+", text)]
    fence = "`" * max(3, (max(runs) + 1) if runs else 3)
    return f"{fence}{language}\n{text}{'' if text.endswith(chr(10)) else chr(10)}{fence}"


def safe_stem(value: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._-")
    return stem or "source"


def source_identity(row: dict[str, Any]) -> tuple[Any, ...]:
    context = row.get("context") or {}
    locator = row["source"]["locator"]
    rel = row["source"]["file"]
    event_id = context.get("event_id", locator.get("event_id"))
    if rel.startswith("data/Map") and re.fullmatch(r"data/Map\d{3}\.json", rel):
        return ("map", rel)
    if rel == "data/CommonEvents.json" and isinstance(event_id, int):
        return ("common_event", event_id)
    return ("reference", rel)


def destination_for(identity: tuple[Any, ...]) -> str:
    kind = identity[0]
    if kind == "map":
        return f"maps/{Path(identity[1]).stem}.md"
    if kind == "common_event":
        return f"common-events/CE{identity[1]:03d}.md"
    return f"references/{safe_stem(identity[1].replace('/', '__'))}.md"


def row_order(row: dict[str, Any]) -> tuple[Any, ...]:
    context = row.get("context") or {}
    locator = row["source"]["locator"]
    return (
        context.get("event_id", locator.get("event_id", -1)) if isinstance(context.get("event_id", locator.get("event_id", -1)), int) else -1,
        context.get("page_number", locator.get("page_number", -1)) if isinstance(context.get("page_number", locator.get("page_number", -1)), int) else -1,
        context.get("command_index", locator.get("command_index", -1)) if isinstance(context.get("command_index", locator.get("command_index", -1)), int) else -1,
        context.get("choice_index", locator.get("option_index", -1)) if isinstance(context.get("choice_index", locator.get("option_index", -1)), int) else -1,
        locator.get("assignment_index", -1) if isinstance(locator.get("assignment_index", -1), int) else -1,
        locator.get("line_number", -1) if isinstance(locator.get("line_number", -1), int) else -1,
        locator.get("json_path", ""), row["id"],
    )


def record_nonce(row: dict[str, Any]) -> str:
    context_json = json.dumps(row.get("context", {}), ensure_ascii=False, sort_keys=True)
    structure_json = json.dumps(row.get("structure", {}), ensure_ascii=False, sort_keys=True)
    source_text = row.get("source_text", "")
    seed = f"{row['id']}\0{row['source']['sha256']}"
    attempt = 0
    while True:
        nonce = hashlib.sha256(f"{seed}\0{attempt}".encode("utf-8")).hexdigest()[:16]
        if nonce not in source_text and nonce not in context_json and nonce not in structure_json:
            return nonce
        attempt += 1


def render_record(row: dict[str, Any]) -> str:
    nonce = record_nonce(row)
    context = row.get("context") or {}
    source = row["source"]
    locator = source["locator"]
    id_text = row["id"]
    headline = row.get("category", "record").replace("_", " ")
    lines = [
        f'<!-- TGO-RECORD-START:{nonce} id="{id_text}" sha256="{source["sha256"]}" -->',
        f"### {headline}",
        f"- ID: `{id_text}`",
        f"- Classification: `{row.get('classification', '')}`",
        f"- Source: `{source.get('file', '')}`",
        f"- Locator: {safe_fence(json.dumps(locator, ensure_ascii=False, sort_keys=True), 'json')}",
    ]
    speaker = context.get("speaker")
    if speaker:
        lines.append(f"- Speaker metadata: {safe_fence(json.dumps(speaker, ensure_ascii=False, sort_keys=True), 'json')}")
    if context.get("custom_header"):
        lines.append(f"- Custom speaker/header: `{context['custom_header']}` (mapping status: `{context.get('speaker_status', 'unknown')}`)")
    lines.extend([
        "",
        "**Source text (read-only):**",
        safe_fence(row.get("source_text", ""), "text"),
        "",
        "<details><summary>Branch, page, choice and structure metadata</summary>",
        "",
        "Context:",
        safe_fence(json.dumps(context, ensure_ascii=False, indent=2, sort_keys=True), "json"),
        "",
        "Markup tokens:",
        safe_fence(json.dumps(row.get("markup_tokens", []), ensure_ascii=False), "json"),
        "",
        "Write-back structure:",
        safe_fence(json.dumps(row.get("structure", {}), ensure_ascii=False, indent=2, sort_keys=True), "json"),
        "",
        "</details>",
        "",
        "Edit only the JSON string after `TGO-TRANSLATION:`. Keep JSON escaping valid; use `\\n` for a line break inside the target.",
        f"<!-- TGO-TARGET:{nonce} -->",
        "TGO-TRANSLATION: " + json.dumps(row.get("translation", ""), ensure_ascii=False),
        f"<!-- TGO-RECORD-END:{nonce} -->",
        "",
    ])
    # Marker collisions inside the immutable source/context would make parsing
    # ambiguous; record_nonce ensures this nonce is absent from those values.
    return "\n".join(lines)


def render_document(identity: tuple[Any, ...], rows: list[dict[str, Any]]) -> str:
    kind = identity[0]
    if kind == "map":
        header = [
            f"# {Path(identity[1]).stem} — event data in source order",
            "",
            "> This file follows map/event/page/command order from the source. It is not a claim about story chronology or a single canonical playthrough. Conditional pages, choices and their branches remain separate in each record's metadata.",
            "",
        ]
        records_with_events = [r for r in rows if isinstance((r.get("context") or {}).get("event_id", r["source"]["locator"].get("event_id")), int)]
        metadata_rows = [r for r in rows if r not in records_with_events]
        if metadata_rows:
            header.extend(["## Map-level labels and metadata", ""])
            header.extend(render_record(row) for row in metadata_rows)
        events: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for row in records_with_events:
            context = row.get("context") or {}
            events[context.get("event_id", row["source"]["locator"].get("event_id"))].append(row)
        for event_id, event_rows in sorted(events.items()):
            event_name = next(((r.get("context") or {}).get("event_name") for r in event_rows if (r.get("context") or {}).get("event_name")), None)
            header.extend([f"## Event {event_id}" + (f" — {event_name}" if event_name else ""), ""])
            pages: dict[Any, list[dict[str, Any]]] = defaultdict(list)
            for row in event_rows:
                context = row.get("context") or {}
                page = context.get("page_number", row["source"]["locator"].get("page_number"))
                pages[page].append(row)
            for page, page_rows in sorted(pages.items(), key=lambda pair: (-1 if pair[0] is None else pair[0])):
                header.extend([f"### Page {page if page is not None else '—'}", ""])
                header.extend(render_record(row) for row in sorted(page_rows, key=row_order))
        return "\n".join(header)
    if kind == "common_event":
        event_rows = sorted(rows, key=row_order)
        event_name = next(((r.get("context") or {}).get("event_name") for r in event_rows if (r.get("context") or {}).get("event_name")), None)
        header = [
            f"# Common Event {identity[1]}" + (f" — {event_name}" if event_name else ""),
            "",
            "> This is a reusable event definition, not an invocation-specific scene. Call sites should be read separately; do not duplicate this block into a single assumed route.",
            "",
        ]
        header.extend(render_record(row) for row in event_rows)
        return "\n".join(header)
    header = [
        f"# Reference text — {Path(identity[1]).name}",
        "",
        "> Non-scene text surface. This document preserves source identity and context; it is not ordered as narrative dialogue.",
        "",
    ]
    header.extend(render_record(row) for row in sorted(rows, key=row_order))
    return "\n".join(header)


def _write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def build_markdown(input_path: Path, out: Path, replace_existing: bool = False) -> dict[str, Any]:
    private_root = (REPO_ROOT / "google_drive").resolve()
    out = out.resolve()
    if out != private_root and private_root not in out.parents:
        raise ValueError("Refusing to write generated Markdown outside ignored google_drive/")
    if out.exists() and any(out.iterdir()):
        if not replace_existing:
            raise FileExistsError(f"Markdown output is not empty: {out}; use --replace only when overwriting is intended")
        existing_manifest = out / "markdown_manifest.json"
        if not existing_manifest.is_file():
            raise ValueError("Refusing to replace a non-empty directory without a recognized generator manifest")
    rows = read_jsonl(input_paths(input_path))
    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[source_identity(row)].append(row)
    rendered: dict[str, str] = {}
    for identity, group_rows in grouped.items():
        rel = destination_for(identity)
        if rel in rendered:
            raise ValueError(f"Multiple source groups map to one Markdown file: {rel}")
        rendered[rel] = render_document(identity, group_rows)
    readme = (
        "# TGO contextual Markdown draft\n\n"
        "Generated from canonical JSONL. The ordering is source order, not a canonical story route. "
        "Do not alter record IDs, source hashes, or source blocks. Edit only `TGO-TRANSLATION:` JSON strings. "
        "This draft may include `needs_review` material and is not yet approved as a translator delivery package.\n"
    )
    rendered["README.md"] = readme
    old_manifest_path = out / "markdown_manifest.json"
    old_generated: set[str] = set()
    if out.exists() and old_manifest_path.is_file() and replace_existing:
        old = json.loads(old_manifest_path.read_text(encoding="utf-8"))
        if old.get("schema") != "tgo-markdown-package-v1":
            raise ValueError("Refusing to replace an output without a recognized TGO manifest")
        old_generated = {p for p in old.get("generated_files", []) if isinstance(p, str) and Path(p).as_posix() == p and not Path(p).is_absolute() and ".." not in Path(p).parts}
        for rel in old_generated:
            target = (out / rel).resolve()
            if out not in target.parents:
                raise ValueError(f"Unsafe generated-file path in prior manifest: {rel}")
    out.mkdir(parents=True, exist_ok=True)
    generated_files = []
    file_hashes = {}
    for rel, content in sorted(rendered.items()):
        encoded = content.encode("utf-8")
        target = out / rel
        _write_atomic(target, encoded)
        generated_files.append(rel)
        file_hashes[rel] = sha256_bytes(encoded)
    # Remove only files explicitly listed by this generator's previous manifest.
    for stale in old_generated - set(generated_files):
        target = (out / stale).resolve()
        if out in target.parents and target.is_file():
            target.unlink()
    categories = Counter(row["category"] for row in rows)
    manifest = {
        "schema": "tgo-markdown-package-v1",
        "records": len(rows),
        "documents": len(rendered) - 1,
        "generated_files": generated_files,
        "document_sha256": file_hashes,
        "category_counts": dict(sorted(categories.items())),
        "source_files": len({row["source"]["file"] for row in rows}),
        "source_order_only": True,
        "translator_delivery_ready": False,
    }
    _write_atomic(out / "markdown_manifest.json", (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return manifest


def parse_markdown_blocks(markdown_root: Path) -> dict[str, tuple[str, str]]:
    if markdown_root.is_file():
        paths = [markdown_root]
    elif markdown_root.is_dir():
        paths = sorted(markdown_root.rglob("*.md"))
    else:
        raise FileNotFoundError(f"Markdown input not found: {markdown_root}")
    translations: dict[str, tuple[str, str]] = {}
    for path in paths:
        text = path.read_text(encoding="utf-8")
        starts = list(START_RE.finditer(text))
        for start in starts:
            nonce, record_id, source_hash = start.groups()
            end_marker = f"<!-- TGO-RECORD-END:{nonce} -->"
            end = text.find(end_marker, start.end())
            if end == -1:
                raise ValueError(f"Missing end marker for {record_id} in {path}")
            body = text[start.end():end]
            target_marker = f"<!-- TGO-TARGET:{nonce} -->"
            if body.count(target_marker) != 1:
                raise ValueError(f"Expected exactly one translation target for {record_id} in {path}")
            tail = body.split(target_marker, 1)[1]
            target_lines = re.findall(r"(?m)^TGO-TRANSLATION: (.*)$", tail)
            if len(target_lines) != 1:
                raise ValueError(f"Expected exactly one TGO-TRANSLATION line for {record_id} in {path}")
            try:
                target = json.loads(target_lines[0])
            except json.JSONDecodeError as error:
                raise ValueError(f"Translation target is not a JSON string for {record_id} in {path}") from error
            if not isinstance(target, str):
                raise ValueError(f"Translation target is not a string for {record_id} in {path}")
            if record_id in translations:
                raise ValueError(f"Duplicate Markdown record ID: {record_id}")
            translations[record_id] = (source_hash, target)
    return translations


def import_markdown(input_path: Path, markdown_root: Path, out: Path,
                    require_complete: bool = False, check_only: bool = False) -> dict[str, Any]:
    private_root = (REPO_ROOT / "google_drive").resolve()
    out = out.resolve()
    if out != private_root and private_root not in out.parents:
        raise ValueError("Refusing to write source text outside ignored google_drive/")
    rows = read_jsonl(input_paths(input_path))
    by_id = {row["id"]: row for row in rows}
    translated = parse_markdown_blocks(markdown_root)
    unknown = sorted(set(translated) - by_id.keys())
    if unknown:
        raise ValueError(f"Markdown contains unknown IDs: {unknown[:5]}")
    translated_count = 0
    for record_id, (source_hash, target) in translated.items():
        row = by_id[record_id]
        if source_hash != row["source"]["sha256"]:
            raise ValueError(f"Source hash mismatch in Markdown for {record_id}")
        if target and tokens(target) != row["markup_tokens"]:
            raise ValueError(f"Markup/token mismatch in Markdown translation for {record_id}")
        if ((row.get("context") or {}).get("translation_policy") == "keep_source_value"
                and target.strip() and target != row["source_text"]):
            raise ValueError(f"Protected source value changed in Markdown for {record_id}")
        if not target and require_complete:
            raise ValueError(f"Empty translation in Markdown for {record_id}")
        row["translation"] = target
        translated_count += bool(target.strip())
    if require_complete:
        missing = sorted(set(by_id) - set(translated))
        if missing:
            raise ValueError(f"Markdown is missing {len(missing)} canonical records")
        blank = [row["id"] for row in rows if not row["translation"].strip()]
        if blank:
            raise ValueError(f"{len(blank)} canonical records have empty translations")
    output_digest = hashlib.sha256()
    out.parent.mkdir(parents=True, exist_ok=True) if not check_only else None
    temp = out.with_name(out.name + ".tmp")
    stream = None if check_only else temp.open("w", encoding="utf-8", newline="\n")
    try:
        for row in rows:
            encoded_line = (json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
            output_digest.update(encoded_line)
            if stream is not None:
                stream.write(encoded_line.decode("utf-8"))
        if stream is not None:
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        if stream is not None:
            stream.close()
    if not check_only:
        os.replace(temp, out)
    report = {
        "schema": "tgo-markdown-import-report-v1",
        "canonical_records": len(rows),
        "markdown_records": len(translated),
        "records_with_translation": translated_count,
        "records_missing_from_markdown": len(set(by_id) - set(translated)),
        "out_of_scope_ids": 0,
        "output_sha256": output_digest.hexdigest(),
        "complete_required": require_complete,
        "check_only": check_only,
    }
    if not check_only:
        _write_atomic(out.with_name(out.stem + "_report.json"), (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build", help="build contextual Markdown draft")
    build.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    build.add_argument("--out", type=Path, default=DEFAULT_MARKDOWN)
    build.add_argument("--replace", action="store_true", help="replace only files listed in a prior generated manifest")
    importer = sub.add_parser("import", help="import Markdown translations into canonical JSONL")
    importer.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    importer.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    importer.add_argument("--out", type=Path, default=DEFAULT_IMPORT)
    importer.add_argument("--require-complete", action="store_true")
    importer.add_argument("--check", action="store_true", help="validate without writing the JSONL bundle")
    args = parser.parse_args()
    if args.command == "build":
        manifest = build_markdown(args.input, args.out, args.replace)
        print(f"Markdown draft: {manifest['documents']} documents; records: {manifest['records']}; sources: {manifest['source_files']}")
        print(f"Output: {args.out}")
        print("Source order only; conditional branches preserved; not approved for translator delivery.")
    else:
        report = import_markdown(args.input, args.markdown, args.out, args.require_complete, args.check)
        print(f"Canonical records: {report['canonical_records']}; translated: {report['records_with_translation']}; "
              f"missing from Markdown: {report['records_missing_from_markdown']}")
        if args.check:
            print("Validation only; no translated JSONL was written.")
        else:
            print(f"Imported JSONL written under ignored google_drive/: {args.out}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
