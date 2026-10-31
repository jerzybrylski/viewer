#!/usr/bin/env python3
"""Statically locate video-playback calls in TGO RPG Maker MV event data.

The scanner reads only `CommonEvents.json` and `Map*.json` (a directory with
extracted `www/data` or a ZIP of it, e.g. the original `data.zip`) and writes a
compact inventory of the places where the scenario starts a movie file.

Nothing is executed: the game's JavaScript is not run, no media is read and no
file in the game directory is modified. Video files themselves are never part of
this repository; only their names and the static command positions are recorded.

The game plays clips through the `ysp.VideoPlayer` API from script commands:

* `ysp.VideoPlayer.newVideo('Name', slotId)` creates a clip in a slot,
* `ysp.VideoPlayer.playVideoById(slotId)` starts it,
* `ysp.VideoPlayer.setLoopById(slotId)` makes it loop,
* `stopVideoById` / `releaseVideo` / `isReady` are control and polling calls, not
  playback starts, so they are not marked.

One marker is produced per script block that creates and starts a clip, with the
slot/name pair resolved inside that block (and from earlier blocks of the same
event page when the game splits them). Names without a matching movie file, and
calls whose argument is not a literal, are reported honestly instead of guessed.

A generic fallback still catches literals such as `Foo.mp4` or other movie APIs,
so the tool stays usable if the plugin or the calling convention changes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
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
    r"(?i)\b(playMovie(?:File)?|playVideo(?:File)?|showMovie|showVideo|loadMovie|VideoSprite|MovieSprite)\b"
)
MOVIE_WORD_RE = re.compile(r"(?i)\b(?:movie|movies|video|videos|film|cinematic)\b")
QUOTED_ARG_RE = re.compile(
    r"""\b(playMovie(?:File)?|playVideo(?:File)?|showMovie|showVideo|loadMovie)\s*\(\s*['"]([^'"]+)['"]""",
    re.IGNORECASE,
)
VIDEO_PLUGIN_CALL_RE = re.compile(r"\bysp\.VideoPlayer\.(\w+)\s*\(")
NEW_VIDEO_RE = re.compile(r"\bnewVideo\s*\(\s*'([^']*)'\s*(?:,\s*(\d+))?\s*\)")
PLAY_BY_ID_RE = re.compile(r"\bplayVideoById\s*\(\s*(\d+)\s*\)")
LOOP_BY_ID_RE = re.compile(r"\bsetLoopById\s*\(\s*(\d+)\s*\)")
PLUGIN_COMMAND_CODES = {356, 357}
SCRIPT_LEADING_CODE = 355
SCRIPT_CONTINUATION_CODE = 655
EVIDENCE_LIMIT = 240


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_event_file(name: str) -> bool:
    return name == "CommonEvents.json" or re.fullmatch(r"Map\d{3}\.json", name) is not None


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


def load_movie_files(path: Path) -> dict[str, str]:
    """Map ``nazwa-bez-rozszerzenia`` → rzeczywista nazwa pliku wideo.

    Wejściem jest albo lista nazw (jedna w wierszu), albo CSV inwentaryzacji
    instalacji z kolumną `RelativePath`. Rozszerzenie bierzemy z rzeczywistego
    pliku; niczego nie dopisujemy „na wiarę”.
    """
    text = path.read_text(encoding="utf-8-sig")
    names: list[str] = []
    if "," in text.splitlines()[0] or "RelativePath" in text:
        for row in csv.DictReader(io.StringIO(text)):
            value = row.get("RelativePath") or row.get("relative_path") or ""
            if value:
                names.append(re.sub(r"[\\/]+", "/", value).rsplit("/", 1)[-1])
    else:
        names = [line.strip() for line in text.splitlines() if line.strip()]
    resolved: dict[str, str] = {}
    for name in names:
        stem = re.sub(r"(?i)\.(?:" + "|".join(MOVIE_EXTENSIONS) + r")$", "", name)
        # Warianty „-l” to klipy w niskiej jakości; przy nazwie bazowej wolimy HQ.
        if stem.lower().endswith("-l"):
            continue
        resolved.setdefault(stem.casefold(), name)
    return resolved


def trim(text: str) -> str:
    value = " ".join(text.split())
    return value if len(value) <= EVIDENCE_LIMIT else value[: EVIDENCE_LIMIT - 1] + "…"


def script_blocks(commands: list[dict[str, Any]]) -> Iterator[tuple[int, list[dict[str, Any]]]]:
    """Grupuj polecenia skryptowe `355` z kontynuacjami `655` w bloki.

    Zwraca `(indeks pierwszego polecenia bloku, polecenia bloku)`. Pozostałe
    polecenia są zwracane pojedynczo, z własnym indeksem.
    """
    index = 0
    while index < len(commands):
        command = commands[index]
        if not isinstance(command, dict):
            index += 1
            continue
        block: list[dict[str, Any]] = []
        while index + len(block) < len(commands):
            current = commands[index + len(block)]
            code = current.get("code") if isinstance(current, dict) else None
            if code == SCRIPT_LEADING_CODE or (block and code == SCRIPT_CONTINUATION_CODE):
                block.append(current)
            else:
                break
        if block:
            yield index, block
            index += len(block)
        else:
            yield index, [command]
            index += 1


def block_text(block: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for command in block:
        for value in command.get("parameters") or []:
            if isinstance(value, str):
                parts.append(value)
            elif isinstance(value, list):
                parts.extend(str(item) for item in value if isinstance(item, str))
    return "\n".join(parts)


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


def resolve_extension(name: str, movie_files: dict[str, str] | None) -> tuple[str, bool]:
    """Zwróć `(nazwa pliku, czy plik znaleziono)` bez zgadywania rozszerzenia."""
    if not name:
        return "", False
    if re.search(r"(?i)\.(?:" + "|".join(MOVIE_EXTENSIONS) + r")$", name):
        return name, True if movie_files is None else name.casefold() in {
            value.casefold() for value in (movie_files or {}).values()
        }
    if movie_files:
        found = movie_files.get(name.casefold())
        if found:
            return found, True
        return name, False
    return name, False


def scan(source: Path, data_zip: Path | None, movie_files: dict[str, str] | None = None) -> dict[str, Any]:
    calls: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    plugin_commands: Counter[str] = Counter()
    api_calls: Counter[str] = Counter()
    file_hashes: dict[str, str] = {}
    command_total = 0
    file_total = 0

    for file_name, raw in iter_source_files(source, data_zip):
        file_total += 1
        file_hashes[file_name] = sha256_bytes(raw)
        document = json.loads(raw.decode("utf-8-sig"))
        for event, kind, map_id, event_id, page_number, commands in event_scope(file_name, document):
            slots: dict[int, dict[str, Any]] = {}
            for command_index, block in script_blocks(commands):
                command_total += len(block)
                text = block_text(block)
                if not text.strip():
                    continue
                code = block[0].get("code")
                if code in PLUGIN_COMMAND_CODES:
                    first_line = text.split("\n", 1)[0]
                    plugin_commands[first_line] += 1

                base = {
                    "source_kind": kind,
                    "map_id": map_id,
                    "event_id": event_id,
                    "event_name": str(event.get("name") or ""),
                    "page_number": page_number,
                    "command_index": command_index,
                    "command_code": code,
                    "source_file": f"data/{file_name}",
                }

                # 1) Właściwe API gry: ysp.VideoPlayer.newVideo(name, slot) + playVideoById(slot).
                new_videos = NEW_VIDEO_RE.findall(text)
                plays = PLAY_BY_ID_RE.findall(text)
                loops = set(LOOP_BY_ID_RE.findall(text))
                if new_videos:
                    for name, slot_id in new_videos:
                        key = int(slot_id) if slot_id else 0
                        slots[key] = {"name": name, "loop": key in {int(item) for item in loops}}
                if plays:
                    local = {int(slot): info for slot, info in slots.items()}
                    block_new = {int(slot) if slot else 0: name for name, slot in new_videos}
                    for slot_id in plays:
                        slot = int(slot_id)
                        name = block_new.get(slot) or (local.get(slot) or {}).get("name") or ""
                        movie_file, found = resolve_extension(name, movie_files)
                        api_calls["ysp.VideoPlayer.newVideo+playVideoById"] += 1
                        calls.append({
                            **base,
                            "movie_name": name,
                            "movie_file": movie_file or None,
                            "file_exists": found,
                            "dynamic": not name,
                            "loop": slot in {int(item) for item in loops} or bool(
                                (slots.get(slot) or {}).get("loop")),
                            "slot_id": slot,
                            "api": "ysp.VideoPlayer",
                            "evidence": trim(text),
                        })
                    continue

                # 2) Fallback: literalna nazwa pliku albo inne API odtwarzacza.
                literal = LITERAL_MOVIE_RE.search(text)
                quoted = QUOTED_ARG_RE.search(text)
                if literal or quoted:
                    name = literal.group(0).rsplit("/", 1)[-1] if literal else quoted.group(2)
                    movie_file, found = resolve_extension(name, movie_files)
                    calls.append({
                        **base,
                        "movie_name": re.sub(r"(?i)\.(?:" + "|".join(MOVIE_EXTENSIONS) + r")$", "", name),
                        "movie_file": movie_file,
                        "file_exists": found,
                        "dynamic": False,
                        "loop": False,
                        "slot_id": None,
                        "api": "literal",
                        "evidence": trim(text),
                    })
                    continue
                if PLAY_API_RE.search(text):
                    calls.append({
                        **base,
                        "movie_name": "",
                        "movie_file": None,
                        "file_exists": False,
                        "dynamic": True,
                        "loop": False,
                        "slot_id": None,
                        "api": "unknown_api",
                        "evidence": trim(text),
                    })
                    continue

                # 3) Wzmianka „movie/video” bez nazwy pliku — tylko do przeglądu.
                if MOVIE_WORD_RE.search(text) and code in PLUGIN_COMMAND_CODES | {108, 408}:
                    candidates.append({**base, "evidence": trim(text)})

    def sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
        return (row["source_kind"], row["map_id"] or 0, row["event_id"],
                row["page_number"] or 0, row["command_index"])

    calls.sort(key=sort_key)
    candidates.sort(key=sort_key)
    movie_files_used = sorted({row["movie_file"] for row in calls if row["movie_file"]})
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
        "movie_file_source": str(movie_files) if movie_files else None,
        "summary": {
            "files_scanned": file_total,
            "commands_scanned": command_total,
            "playback_calls": len(calls),
            "confirmed_calls": sum(1 for row in calls if not row["dynamic"]),
            "dynamic_calls": sum(1 for row in calls if row["dynamic"]),
            "looping_calls": sum(1 for row in calls if row.get("loop")),
            "missing_movie_files": sum(1 for row in calls if row["movie_file"] and not row["file_exists"]),
            "review_candidates": len(candidates),
            "unique_movie_files": len(movie_files_used),
            "scenes_with_calls": len(scopes),
            "api_calls": dict(sorted(api_calls.items())),
        },
        "plugin_commands": dict(sorted(plugin_commands.items(), key=lambda item: (-item[1], item[0]))),
        "movie_files": movie_files_used,
        "calls": calls,
        "candidates": candidates,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data-dir", type=Path, default=None,
                        help="katalog z rozpakowanym www/data (CommonEvents.json + Map*.json)")
    parser.add_argument("--data-zip", type=Path, default=None,
                        help="ZIP z www/data (np. oryginalny data.zip); alternatywa dla --data-dir")
    parser.add_argument("--movie-files", type=Path, default=None,
                        help="lista nazw plików wideo albo CSV inwentaryzacji (RelativePath) do ustalenia rozszerzeń")
    parser.add_argument("--out", type=Path, default=Path("movie_calls.json"),
                        help="plik wyjściowy JSON (domyślnie movie_calls.json)")
    parser.add_argument("--indent", type=int, default=2, help="wcięcie JSON (0 = bez wcięć)")
    parser.add_argument("--compact", action="store_true",
                        help="wersja do śledzenia w Git: bez fragmentów poleceń (evidence) i bez hashów plików źródłowych")
    args = parser.parse_args(argv)

    if (args.data_dir is None) == (args.data_zip is None):
        parser.error("podaj dokładnie jedno z --data-dir albo --data-zip")
    if args.data_dir is not None and not args.data_dir.is_dir():
        parser.error(f"nie ma katalogu: {args.data_dir}")
    if args.data_zip is not None and not args.data_zip.is_file():
        parser.error(f"nie ma pliku: {args.data_zip}")
    if args.movie_files is not None and not args.movie_files.is_file():
        parser.error(f"nie ma pliku: {args.movie_files}")
    if args.out.exists():
        parser.error(f"plik wyjściowy już istnieje, nie nadpisuję: {args.out}")

    movie_files = load_movie_files(args.movie_files) if args.movie_files else None
    report = scan(args.data_dir or Path("."), args.data_zip, movie_files)
    report["movie_file_source"] = str(args.movie_files) if args.movie_files else None
    if report["summary"]["files_scanned"] == 0:
        print("Nie znaleziono CommonEvents.json ani Map*.json — sprawdź ścieżkę.", file=sys.stderr)
        return 2
    if args.compact:
        # Wersja do Gita: bez fragmentów poleceń i bez pól, które da się odtworzyć
        # z danych gry (nazwa eventu, ścieżka pliku źródłowego).
        keep = ("source_kind", "map_id", "event_id", "page_number", "command_index",
                "movie_name", "movie_file", "file_exists", "dynamic", "loop", "slot_id", "api")
        report["calls"] = [{key: row[key] for key in keep if key in row} for row in report["calls"]]
        report["candidates"] = [{key: row[key] for key in keep if key in row} for row in report["candidates"]]
        report["source"].pop("files", None)
        report["compact"] = True
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
        "missing_movie_files": summary["missing_movie_files"],
        "review_candidates": summary["review_candidates"],
        "unique_movie_files": summary["unique_movie_files"],
        "scenes_with_calls": summary["scenes_with_calls"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
