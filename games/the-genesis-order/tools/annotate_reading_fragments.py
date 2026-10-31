#!/usr/bin/env python3
"""Wstaw znaczniki wstawek wideo do fragmentów Czytanki (TGO1..TGO12).

Narzędzie bierze fragmenty tekstu czytania (pliki .txt z Drive `TGO/dostawy/`)
i plik matkę `reading/v1/chronological_script_PL.md`, dopasowuje bloki
fragmentów do epizodów pliku matki i wstawia w te same miejsca znaczniki
wstawek wideo (`> **🎬 Wstawka wideo:** ...`), zachowując styl zakończeń linii
oraz całą treść fragmentu bez zmian.

Dopasowanie jest statyczne i deterministyczne:
  * nagłówek `## ...` fragmentu wskazuje epizod pliku matki (nazwy są unikalne),
  * preambuła (kwestie przed pierwszym nagłówkiem) trafia do epizodu, w którym
    występuje jej pierwsza kwestia,
  * kwestie dopasowywane są przez `difflib.SequenceMatcher` po normalizacji
    (białe znaki, cudzysłowy, myślniki, wielokropki),
  * znacznik wideo trafia tylko tam, gdzie w pliku matce stoi pomiędzy dwiema
    dopasowanymi kwestiami (albo między nagłówkiem epizodu a pierwszą kwestią),
  * kwestie spoza pliku matki (własne redakcje użytkownika) zostają nietknięte
    i są raportowane.

Narzędzie nigdy nie nadpisuje istniejących plików wyjściowych.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

MARKER_PREFIX = "> **🎬 Wstawka wideo:**"
DIALOG_RE = re.compile(r"^\*\*(.+?):\*\* (.+)$")
HEADER_PREFIX = "## "

_TRANSLATE = str.maketrans(
    {
        "\u00a0": " ",
        "\u2018": "'",
        "\u2019": "'",
        "\u201a": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u201e": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
    }
)


def norm(text: str) -> str:
    """Znormalizuj tekst kwestii do porównania."""
    text = text.translate(_TRANSLATE).rstrip()
    if text.endswith("\\"):  # zabezpieczenie przed ucieczką z Markdown
        text = text[:-1]
    text = text.rstrip("  ")
    return re.sub(r"\s+", " ", text).strip()


# --------------------------------------------------------------------------
# plik matka
# --------------------------------------------------------------------------


class Episode:
    """Epizod pliku matki: nagłówek, kwestie i linie znaczników wideo."""

    __slots__ = ("index", "header", "start", "end", "dialogs", "markers")

    def __init__(self, index: int, header: str, start: int) -> None:
        self.index = index
        self.header = header
        self.start = start
        self.end = start
        self.dialogs: list[tuple[int, str]] = []  # (linia w matce, tekst znormalizowany)
        self.markers: list[int] = []  # linie w matce ze znacznikiem wideo


class Master:
    """Plik matka Czytanki: kolejne epizody i ich kwestie."""

    def __init__(self, text: str) -> None:
        self.lines = text.replace("\r\n", "\n").split("\n")
        self.episodes: list[Episode] = []
        self.by_header: dict[str, Episode] = {}
        self.duplicate_headers: list[str] = []
        self._parse()

    def _parse(self) -> None:
        current: Episode | None = None
        for i, line in enumerate(self.lines):
            if line.startswith(HEADER_PREFIX):
                current = Episode(len(self.episodes), line[len(HEADER_PREFIX):], i)
                self.episodes.append(current)
                key = norm(current.header)
                if key in self.by_header:
                    self.duplicate_headers.append(current.header)
                else:
                    self.by_header[key] = current
                continue
            if current is None:
                continue
            current.end = i + 1
            if line.startswith(MARKER_PREFIX):
                current.markers.append(i)
            match = DIALOG_RE.match(line.rstrip())
            if match:
                current.dialogs.append((i, norm(match.group(2))))

    def episodes_with_text(self, text: str) -> list[Episode]:
        key = norm(text)
        return [ep for ep in self.episodes if any(t == key for _, t in ep.dialogs)]


# --------------------------------------------------------------------------
# dopasowanie bloku do epizodu
# --------------------------------------------------------------------------


def map_block(fragment_dialogs: list[str], episode: Episode) -> dict[int, int]:
    """Zmapuj indeksy kwestii bloku na indeksy kwestii epizodu pliku matki."""
    master_texts = [text for _, text in episode.dialogs]
    matcher = difflib.SequenceMatcher(None, master_texts, fragment_dialogs, autojunk=False)
    mapping: dict[int, int] = {}
    for master_start, frag_start, size in matcher.get_matching_blocks():
        for offset in range(size):
            mapping[frag_start + offset] = master_start + offset
    return mapping


def markers_before(episode: Episode, index: int) -> list[int]:
    """Znaczniki między nagłówkiem epizodu a kwestią `index`."""
    return [m for m in episode.markers if episode.start < m < episode.dialogs[index][0]]


def markers_between(episode: Episode, first: int, second: int) -> list[int]:
    """Znaczniki leżące między dwiema kwestiami epizodu."""
    lo, hi = episode.dialogs[first][0], episode.dialogs[second][0]
    return [m for m in episode.markers if lo < m < hi]


# --------------------------------------------------------------------------
# fragment
# --------------------------------------------------------------------------


class Block:
    """Blok fragmentu: nagłówek (dla preambuły brak) i jego kwestie."""

    __slots__ = ("header", "dialogs", "start", "end")

    def __init__(self, header: str | None, start: int) -> None:
        self.header = header
        self.dialogs: list[tuple[int, str, str]] = []  # (linia, mówca, tekst znormalizowany)
        self.start = start
        self.end = start


def split_fragment(lines: list[str]) -> list[Block]:
    """Podziel fragment na preambułę i bloki zaczynające się od `## `."""
    first_header = next((i for i, line in enumerate(lines) if line.startswith(HEADER_PREFIX)), None)
    prelude_end = first_header if first_header is not None else len(lines)
    prelude = Block(None, 0)
    prelude.end = prelude_end
    blocks = [prelude]
    current = prelude
    for i, line in enumerate(lines):
        if line.startswith(HEADER_PREFIX) and i >= prelude_end:
            current = Block(line[len(HEADER_PREFIX):], i)
            blocks.append(current)
        current.end = i + 1
        match = DIALOG_RE.match(line.rstrip())
        if match:
            current.dialogs.append((i, match.group(1), norm(match.group(2))))
    return blocks


def find_episode(block: Block, master: Master, carry: int) -> tuple[Episode | None, str]:
    """Ustal epizod pliku matki dla bloku fragmentu."""
    if block.header is not None:
        episode = master.by_header.get(norm(block.header))
        if episode is not None:
            return episode, "nagłówek"
        return None, "brak nagłówka w pliku matce"
    if not block.dialogs:
        return None, "brak kwestii"
    candidates = master.episodes_with_text(block.dialogs[0][2])
    if not candidates:
        return None, "pierwsza kwestia nie występuje w pliku matce"
    if len(candidates) == 1:
        return candidates[0], "pierwsza kwestia (jednoznaczna)"
    later = [ep for ep in candidates if ep.index >= carry]
    chosen = later[0] if later else candidates[0]
    return chosen, f"pierwsza kwestia (wybór z {len(candidates)} kandydatów)"


def render(lines: list[str], insert_before: dict[int, list[str]]) -> str:
    """Zbuduj nową treść, wstawiając znaczniki bez zmiany pozostałych linii."""
    out: list[str] = []
    skip: set[int] = set()
    for i, line in enumerate(lines):
        if i in skip:
            continue
        pending = insert_before.get(i, [])
        if pending:
            if out and out[-1].strip():
                out.append("")
            out.extend(pending)
            out.append("")
            if line.strip() == "":  # pochłoń istniejącą pustą linię
                continue
        out.append(line)
    pending = insert_before.get(len(lines), [])
    if pending:
        if out and out[-1].strip():
            out.append("")
        out.extend(pending)
        out.append("")
    return "\n".join(out)


def annotate_fragment(path: Path, master: Master, carry: int) -> tuple[str, dict, int]:
    """Zwróć (nowa treść, raport dla pliku, indeks epizodu na potrzeby kolejnego pliku)."""
    raw = path.read_bytes().decode("utf-8-sig")
    newline = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.replace("\r\n", "\n").split("\n")

    insert_before: dict[int, list[str]] = {}
    report: dict = {
        "file": path.name,
        "bytes_in": len(raw.encode("utf-8")),
        "newline": "CRLF" if newline == "\r\n" else "LF",
        "blocks": [],
        "markers": [],
        "unmatched_dialogs": [],
        "markers_inserted": 0,
    }

    episode_cursor = carry
    for block in split_fragment(lines):
        episode, how = find_episode(block, master, episode_cursor)
        entry = {
            "header": block.header,
            "episode": episode.header if episode else None,
            "matched_by": how,
            "dialogs": len(block.dialogs),
            "matched": 0,
            "markers": 0,
        }
        report["blocks"].append(entry)

        if episode is None:
            entry["error"] = "nie dopasowano epizodu"
            for line_no, speaker, text in block.dialogs:
                report["unmatched_dialogs"].append(
                    {"line": line_no + 1, "speaker": speaker, "text": text[:160]}
                )
            continue

        mapping = map_block([text for _, _, text in block.dialogs], episode)
        entry["matched"] = len(mapping)
        previous: int | None = None

        for frag_index, (line_no, speaker, text) in enumerate(block.dialogs):
            if frag_index not in mapping:
                report["unmatched_dialogs"].append(
                    {"line": line_no + 1, "speaker": speaker, "text": text[:160]}
                )
                continue
            index = mapping[frag_index]
            if previous is None:
                marker_lines = markers_before(episode, index)
            elif index > previous:
                marker_lines = markers_between(episode, previous, index)
            else:
                marker_lines = []
            if marker_lines:
                payload = [master.lines[m].rstrip() for m in marker_lines]
                insert_before.setdefault(line_no, []).extend(payload)
                entry["markers"] += len(payload)
                report["markers_inserted"] += len(payload)
                for m, text_marker in zip(marker_lines, payload):
                    report["markers"].append(
                        {
                            "line": line_no + 1,
                            "marker": text_marker,
                            "master_line": m + 1,
                            "episode": episode.header,
                        }
                    )
            previous = index
            episode_cursor = episode.index

        # znaczniki po ostatniej kwestii bloku — tylko gdy blok wyczerpuje epizod
        if previous is not None and previous == len(episode.dialogs) - 1:
            trailing = [m for m in episode.markers if episode.dialogs[previous][0] < m < episode.end]
            if trailing:
                payload = [master.lines[m].rstrip() for m in trailing]
                insert_before.setdefault(block.dialogs[-1][0] + 1, []).extend(payload)
                entry["markers"] += len(payload)
                report["markers_inserted"] += len(payload)
                for m, text_marker in zip(trailing, payload):
                    report["markers"].append(
                        {
                            "line": block.dialogs[-1][0] + 2,
                            "marker": text_marker,
                            "master_line": m + 1,
                            "episode": episode.header,
                        }
                    )

    result = render(lines, insert_before)
    report["bytes_out"] = len(result.encode("utf-8"))
    return result, report, episode_cursor


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def numeric_key(path: Path) -> tuple[int, str]:
    match = re.search(r"(\d+)", path.stem)
    return (int(match.group(1)) if match else 10**6, path.stem)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--master", required=True, type=Path, help="plik matka Czytanki (Markdown)")
    parser.add_argument("--fragments", required=True, type=Path, help="katalog z fragmentami .txt")
    parser.add_argument("--out", required=True, type=Path, help="katalog wyjściowy (nie może istnieć)")
    parser.add_argument("--report", type=Path, help="ścieżka raportu JSON")
    parser.add_argument("--indent", type=int, default=2, help="wcięcie raportu JSON")
    args = parser.parse_args(argv)

    if not args.master.is_file():
        print(f"BŁĄD: brak pliku matki: {args.master}", file=sys.stderr)
        return 2
    if not args.fragments.is_dir():
        print(f"BŁĄD: brak katalogu z fragmentami: {args.fragments}", file=sys.stderr)
        return 2
    if args.out.exists():
        print(f"BŁĄD: katalog wyjściowy już istnieje: {args.out}", file=sys.stderr)
        return 3

    files = sorted(
        (p for p in args.fragments.iterdir() if p.suffix.lower() == ".txt"), key=numeric_key
    )
    if not files:
        print(f"BŁĄD: brak plików .txt w {args.fragments}", file=sys.stderr)
        return 2

    master = Master(args.master.read_bytes().decode("utf-8-sig"))
    if master.duplicate_headers:
        print(
            f"UWAGA: zduplikowane nagłówki w pliku matce: {master.duplicate_headers[:3]}",
            file=sys.stderr,
        )

    args.out.mkdir(parents=True)
    reports = []
    carry = 0
    total_markers = 0
    for path in files:
        text, report, carry = annotate_fragment(path, master, carry)
        out_path = args.out / path.name
        if out_path.exists():
            print(f"BŁĄD: plik wyjściowy już istnieje: {out_path}", file=sys.stderr)
            return 3
        if report["newline"] == "CRLF":
            text = text.replace("\n", "\r\n")
        out_path.write_text(text, encoding="utf-8", newline="")
        reports.append(report)
        total_markers += report["markers_inserted"]
        print(
            f"{path.name:12s} bloki {len(report['blocks']):3d}  "
            f"wstawki {report['markers_inserted']:3d}  "
            f"niedopasowane kwestie {len(report['unmatched_dialogs']):3d}",
            file=sys.stderr,
        )

    summary = {
        "master": str(args.master),
        "fragments": str(args.fragments),
        "files": len(reports),
        "markers_total": total_markers,
        "unmatched_total": sum(len(r["unmatched_dialogs"]) for r in reports),
        "reports": reports,
    }
    if args.report:
        if args.report.exists():
            print(f"BŁĄD: raport już istnieje: {args.report}", file=sys.stderr)
            return 3
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(summary, ensure_ascii=False, indent=args.indent) + "\n", encoding="utf-8"
        )
    print(
        f"OK: {len(reports)} plików, {total_markers} wstawek, "
        f"{summary['unmatched_total']} niedopasowanych kwestii",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
