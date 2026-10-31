#!/usr/bin/env python3
"""Statically locate video-playback calls in TGO RPG Maker MV event data.

The scanner reads only `CommonEvents.json` and `Map*.json` (a directory with
extracted `www/data` or a ZIP of it, e.g. the original `data.zip`) and writes a
compact inventory of the places where the scenario starts a movie file.

Nothing is executed: the game's JavaScript is not run, no media is read and no
file in the game directory is modified. Video files themselves are never part of
this repository; only their names and the static command positions are recorded.

Detection is layered so that a mismatch of plugin/API naming cannot silently
produce a false negative:

* `confirmed` — a literal movie file name (`.mp4`, `.webm`, `.m4v`, `.mov`) or a
  known movie/video API call appears in a command,
* `candidate` — the command mentions "movie"/"video" (plugin command, comment or
  script line) without a literal file name, so a human must classify it,
* `dynamic` — a movie API is called with a non-literal argument (variable,
  expression); the Czytanka marks such a place without inventing a file name.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

SCHEMA = "tgo-movie-calls-v1"
SCANNER = "scan_movie_calls.py"

MOVIE_EXTENSIONS = ("mp4", "webm", "m4v", "mov")
LITERAL_MOVIE_RE = re.compile(
    r"(?i)([A-Za-z0-9_][A-Za-z0-9_\-./\\{}]*)\.(?:" + "|".join(MOVIE_EXTENSIONS) + r")\b"
)
PLAY_API_RE = re.compile(
    r"(?i)\b(playMovie(?:File)?|playVideo(?:File)?|showMovie|showVideo|loadMovie|loadVideo|"
    r"MoviePlayer|VideoPlayer|Scene_Movie|MovieSprite|VideoSprite|playMovieStream)\b"
)
MOVIE_WORD_RE = re.compile(r"(?i)\b(?:movie|movies|video|videos|film|cinematic)\b")
QUOTED_ARG_RE = re.compile(
    r'''(?i)(?:playMovie(?:File)?|playVideo(?:File)?|showMovie|showVideo|loadMovie|loadVideo|'''
    r'''MoviePlayer|VideoPlayer)\s*\(\s*['"]([^'"]+)['"]'''
)
SCRIPT_CONTINUATION_CODES = {655}
PLUGIN_COMMAND_CODES = {356, 357}
EVIDENCE_LIMIT = 240


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def iter_source_files(source: Path, data_zip: Path | None) -> Iterator[tuple[str, bytes]]:
    """Yield `(file name, raw bytes)` for CommonEvents.json and Map*.json only."""
    if data_zip is not None:
        with zipfile.ZipFile(data_zip) as archive:
            for info in sorted(archive.infolist(), key=lambda item: item.filename):
                name = Path(info.filename).name
                if info.is_dir() or not is_event_file(name):
                    continue
                yield name, archive.read(info)
        return
    for path in sorted(source.glob("*.json")):
        if is_event_file(path.name):
            yield path.name, path.read_bytes()


def is_event_file(name: str) -> bool:
    return name == "CommonEvents.json" or re.fullmatch(r"Map\d{3}\.json", name) is not None


def script_lines(parameters: list[Any]) -> list[str]:
    """Join an RPG Maker script command with its 655 continuation lines."""
    lines: list[str] = []
    for value in parameters:
        if isinstance(value, str):
            lines.append(value)
        elif isinstance(value, list):
            lines.extend(str(item) for item in value if isinstance(item, str))
    return lines


def command_strings(command: dict[str, Any]) -> list[str]:
    """Every string value carried by a command, at any nesting depth."""
    found: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, str):
            found.append(value)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)

    walk(command.get("parameters") or [])
    return found


def movie_file_from(text: str) -> str | None:
    match = LITERAL_MOVIE_RE.search(text)
    if not match:
        return None
    return re.split(r"[\\/]", match.group(0))[-1]


def trim(text: str) -> str:
    value = " ".join(text.split())
    return value if len(value) <= EVIDENCE_LIMIT else value[: EVIDENCE_LIMIT - 1] + "…"


def classify(code: int, texts: list[str], joined: str) -> tuple[str, str | None]:
    """Return `(strength, movie_file)` for one command.

    `confirmed` means a literal movie file name or a recognised movie API call.
    `candidate` is any remaining "movie"/"video" mention that needs review.
    """
    movie_file = movie_file_from(joined)
    if movie_file is not None:
        return "confirmed", movie_file
    quoted = QUOTED_ARG_RE.search(joined)
    if quoted is not None:
        return "confirmed", re.split(r"[\\/]", quoted.group(1))[-1]
    if PLAY_API_RE.search(joined):
        if code in PLUGIN_COMMAND_CODES:
            # Plugin command named like a movie API: the file name is probably in
            # the argument list, but without an extension it still needs review.
            for text in texts[2:]:
                if re.fullmatch(r"[A-Za-z0-9_\- .]+", text) and not text.isdigit():
                    return "candidate", text.strip()
        return "dynamic", None
    if MOVIE_WORD_RE.search(joined):
        if code in PLUGIN_COMMAND_CODES:
            for text in texts[2:]:
                if re.fullmatch(r"[A-Za-z0-9_\- .]+", text) and not text.isdigit():
                    return "candidate", text.strip()
        return "candidate", None
    return "", None


def event_scope(file_name: str, document: Any) -> Iterator[tuple[dict[str, Any], str, int | None, int | None, int | None, list[dict[str, Any]]]]:
    """Yield `(event, kind, map_id, event_id, page_number, commands)`."""
    if file_name == "CommonEvents.json":
        rows = document if isinstance(document, list) else []
        for row in rows:
            if not isinstance(row, dict) or not row.get("id"):
                continue
            commands = row.get("list") or []
            if commands:
                yield row, "common_event", None, int(row["id"]), None, commands
        return
    map_id = int(re.sub(r"\D", "", file_name))
    events = document.get("events") if isinstance(document, dict) else None
    for event in events or []:
        if not isinstance(event, dict) or not event.get("id"):
            continue
        for page_number, page in enumerate(event.get("pages") or [], 1):
            if not isinstance(page, dict):
                continue
            commands = page.get("list") or []
            if commands:
                yield event, "map", map_id, int(event["id"]), page_number, commands


def scan(source: Path, data_zip: Path | None) -> dict[str, Any]:
    calls: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    plugin_commands: Counter[str] = Counter()
    file_hashes: dict[str, str] = {}
    command_total = 0
    file_total = 0

    for file_name, raw in iter_source_files(source, data_zip):
        file_total += 1
        file_hashes[file_name] = sha256_bytes(raw)
        document = json.loads(raw.decode("utf-8-sig"))
        for event, kind, map_id, event_id, page_number, commands in event_scope(file_name, document):
            index = 0
            while index < len(commands):
                command = commands[index]
                if not isinstance(command, dict):
                    index += 1
                    continue
                command_total += 1
                code = command.get("code")
                if not isinstance(code, int):
                    index += 1
                    continue
                if code in PLUGIN_COMMAND_CODES:
                    texts = command_strings(command)
                    if texts:
                        plugin_commands[str(texts[0])] += 1
                    joined = "\n".join(texts)
                    step = 1
                else:
                    # Polecenie skryptowe 355 z kontynuacjami 655 tworzy jeden blok;
                    # oceniamy go raz, na pozycji pierwszego polecenia.
                    block: list[dict[str, Any]] = []
                    while index + len(block) < len(commands):
                        candidate = commands[index + len(block)]
                        code_of = candidate.get("code") if isinstance(candidate, dict) else None
                        if code_of not in {355, 655}:
                            break
                        block.append(candidate)
                    if block:
                        texts = [text for row in block for text in command_strings(row)]
                        joined = "\n".join(texts)
                        step = len(block)
                    else:
                        texts = command_strings(command)
                        joined = "\n".join(texts)
                        step = 1
                if joined.strip():
                    strength, movie_file = classify(code, texts, joined)
                    if strength:
                        record = {
                            "source_kind": kind,
                            "map_id": map_id,
                            "event_id": event_id,
                            "event_name": str(event.get("name") or ""),
                            "page_number": page_number,
                            "command_index": index,
                            "command_code": code,
                            "movie_file": movie_file,
                            "dynamic": strength == "dynamic",
                            "evidence": trim(joined),
                            "source_file": f"data/{file_name}",
                        }
                        (calls if strength in {"confirmed", "dynamic"} else candidates).append(record)
                index += step

    calls.sort(key=lambda row: (row["source_kind"], row["map_id"] or 0, row["event_id"],
                                row["page_number"] or 0, row["command_index"]))
    candidates.sort(key=lambda row: (row["source_kind"], row["map_id"] or 0, row["event_id"],
                                     row["page_number"] or 0, row["command_index"]))
    movie_files = sorted({row["movie_file"] for row in calls if row["movie_file"]})
    scopes = {(row["source_kind"], row["map_id"] or 0, row["event_id"], row["page_number"] or 0)
              for row in calls}
    return {
        "schema": SCHEMA,
        "scanner": SCANNER,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": {
            "mode": "zip" if data_zip is not None else "directory",
            "path": str(data_zip if data_zip is not None else source),
            "files": file_hashes,
        },
        "summary": {
            "files_scanned": file_total,
            "commands_scanned": command_total,
            "playback_calls": len(calls),
            "confirmed_calls": sum(1 for row in calls if not row["dynamic"]),
            "dynamic_calls": sum(1 for row in calls if row["dynamic"]),
            "review_candidates": len(candidates),
            "unique_movie_files": len(movie_files),
            "scenes_with_calls": len(scopes),
        },
        "plugin_commands": dict(sorted(plugin_commands.items(), key=lambda item: (-item[1], item[0]))),
        "movie_files": movie_files,
        "calls": calls,
        "candidates": candidates,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data-dir", type=Path, default=None,
                        help="katalog z rozpakowanym www/data (CommonEvents.json + Map*.json)")
    parser.add_argument("--data-zip", type=Path, default=None,
                        help="ZIP z www/data (np. oryginalny data.zip); alternatywa dla --data-dir")
    parser.add_argument("--out", type=Path, default=Path("movie_calls.json"),
                        help="plik wyjściowy JSON (domyślnie movie_calls.json)")
    parser.add_argument("--indent", type=int, default=2, help="wcięcie JSON (0 = kompaktowo)")
    args = parser.parse_args(argv)

    if (args.data_dir is None) == (args.data_zip is None):
        parser.error("podaj dokładnie jedno z --data-dir albo --data-zip")
    if args.data_dir is not None and not args.data_dir.is_dir():
        parser.error(f"nie ma katalogu: {args.data_dir}")
    if args.data_zip is not None and not args.data_zip.is_file():
        parser.error(f"nie ma pliku: {args.data_zip}")
    if args.out.exists():
        parser.error(f"plik wyjściowy już istnieje, nie nadpisuję: {args.out}")

    report = scan(args.data_dir or Path("."), args.data_zip)
    if report["summary"]["files_scanned"] == 0:
        print("Nie znaleziono CommonEvents.json ani Map*.json — sprawdź ścieżkę.", file=sys.stderr)
        return 2
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=args.indent or None) + "\n",
        encoding="utf-8", newline="\n",
    )
    summary = report["summary"]
    print(json.dumps({
        "out": str(args.out),
        "files_scanned": summary["files_scanned"],
        "commands_scanned": summary["commands_scanned"],
        "playback_calls": summary["playback_calls"],
        "confirmed_calls": summary["confirmed_calls"],
        "dynamic_calls": summary["dynamic_calls"],
        "review_candidates": summary["review_candidates"],
        "unique_movie_files": summary["unique_movie_files"],
        "scenes_with_calls": summary["scenes_with_calls"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
