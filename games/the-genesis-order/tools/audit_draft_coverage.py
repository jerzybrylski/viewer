#!/usr/bin/env python3
"""Audit TGO draft coverage without changing any tracked translation file.

Reads the canonical JSONL export and every draft JSONL (recursively, including
``drafts/hints/`` and ``drafts/ui-01/``), then reports:

* how many stable IDs have a non-empty translation,
* which IDs carry conflicting non-empty values and in which files,
* how the still-blank records split into measurable buckets.

The buckets are evidence labels, not translation decisions. In particular
``needs_review`` and ``proper_name`` require an explicit owner decision before
anything is copied or translated; this tool never writes a translation.

Only JSON text is read. No game code or binary asset is opened or executed.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from export_translation import EXTRA_CONTROL_RE, TOKEN_RE, tokens
from markup_signature import tokens_v2

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_EXPORT = REPO_ROOT / "games/the-genesis-order/translation/export-v1"
DEFAULT_DRAFTS = REPO_ROOT / "games/the-genesis-order/translation/drafts"

# Explicit filler markers copied verbatim from the game's own test/template maps.
# They are reported separately instead of being guessed as story text.
TEMPLATE_MARKERS = ("text goes here",)
NAME_CATEGORIES = {
    "credits",
    "database.actors.name",
    "database.items.name",
    "image_caption",
    "ui.variable_value",
}
LETTER_RE = re.compile(r"[A-Za-z\u00c0-\u024f\u0400-\u04ff]")
LOWERCASE_RE = re.compile(r"[a-z\u00df-\u00ff\u0101-\u024f\u0451-\u04ff]")
IDENTIFIER_RE = re.compile(r"^[\d\s#A-Z.&'-]{1,12}$")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"Expected a JSON object at {path}:{line_number}")
            rows.append(row)
    return rows


def load_canonical(path: Path) -> dict[str, dict[str, Any]]:
    paths = sorted(path.glob("*.jsonl")) if path.is_dir() else [path]
    if not paths:
        raise FileNotFoundError(f"No canonical JSONL found at {path}")
    rows: dict[str, dict[str, Any]] = {}
    for file in paths:
        for row in read_jsonl(file):
            rows[row["id"]] = row
    return rows


def draft_paths(root: Path) -> list[Path]:
    """Every draft file, including nested batch folders."""
    if root.is_file():
        return [root]
    return sorted(root.rglob("*.jsonl"))


def load_drafts(root: Path, base: Path | None = None) -> tuple[dict[str, list[tuple[str, str]]], int]:
    """Return ``{id: [(relative_file, translation), ...]}`` and the row count."""
    base = base or (root if root.is_dir() else root.parent)
    values: dict[str, list[tuple[str, str]]] = defaultdict(list)
    rows = 0
    paths = draft_paths(root)
    if not paths:
        raise FileNotFoundError(f"No draft JSONL found at {root}")
    for path in paths:
        name = path.relative_to(base).as_posix()
        for row in read_jsonl(path):
            rows += 1
            value = row.get("translation")
            if isinstance(value, str) and value.strip():
                values[row["id"]].append((name, value))
    return values, rows


def stripped_text(text: str) -> str:
    """Remove RPG Maker control tokens and HTML-ish tags from a source string."""
    return EXTRA_CONTROL_RE.sub(" ", TOKEN_RE.sub(" ", text))


def is_protected(row: dict[str, Any]) -> bool:
    return (row.get("context") or {}).get("translation_policy") == "keep_source_value"


def classify_blank(row: dict[str, Any]) -> tuple[str, str]:
    """Bucket a still-blank record with a short, checkable reason."""
    text = row.get("source_text") or ""
    plain = stripped_text(text)
    if is_protected(row):
        return "protected", "translation_policy=keep_source_value"
    if text.strip().startswith("/"):
        return "command", "slash-prefixed custom-dialogue command, not prose"
    if not LETTER_RE.search(plain):
        return "markup_only", "no letters left after removing control tokens"
    lowered = plain.lower()
    if any(marker in lowered for marker in TEMPLATE_MARKERS):
        return "template_placeholder", "editor template filler, not shipped prose"
    if row.get("category") == "credits":
        return "credits_roster", "backer name list; names are not translated"
    if row.get("category") in NAME_CATEGORIES:
        return "proper_name", "character/item name or gallery caption"
    if IDENTIFIER_RE.fullmatch(plain.strip()):
        return "identifier", "digits, codes or short markers; keep the source form"
    if not LOWERCASE_RE.search(plain):
        return "identifier", "single words in capitals only; likely a code or label"
    if tokens_v2(text) != tokens(text):
        return ("blocked_by_signature",
                "v1 signature glues a no-argument tag to the first word; "
                "see docs/ADR.md ADR 002")
    return "needs_review", "real wording with no translation yet"


def identical_translations(
    canonical: dict[str, dict[str, Any]],
    drafts: dict[str, list[tuple[str, str]]],
) -> list[dict[str, Any]]:
    """Non-empty drafts that merely repeat the English source in a prose category."""
    hits = []
    for row_id, entries in drafts.items():
        row = canonical.get(row_id)
        if row is None or row.get("category") in NAME_CATEGORIES or is_protected(row):
            continue
        source = row.get("source_text") or ""
        if len(LETTER_RE.findall(stripped_text(source))) < 3:
            continue
        for file, value in entries:
            if value.strip() == source.strip():
                hits.append({"id": row_id, "file": file, "category": row["category"],
                             "source_text": source})
    return sorted(hits, key=lambda item: (item["category"], item["source_text"], item["id"]))


def audit(canonical_dir: Path, drafts_dir: Path) -> dict[str, Any]:
    canonical = load_canonical(canonical_dir)
    drafts, draft_rows = load_drafts(drafts_dir)
    conflicts = [
        {"id": row_id, "category": canonical[row_id]["category"] if row_id in canonical else None,
         "source_text": canonical[row_id]["source_text"] if row_id in canonical else None,
         "values": [{"file": file, "translation": value} for file, value in entries]}
        for row_id, entries in drafts.items()
        if len({value for _, value in entries}) > 1
    ]
    conflicts.sort(key=lambda item: item["id"])

    covered = {row_id for row_id, entries in drafts.items() if row_id in canonical}
    unknown = sorted(set(drafts) - set(canonical))
    blank = [row for row_id, row in canonical.items() if row_id not in covered]

    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in blank:
        bucket, reason = classify_blank(row)
        buckets[bucket].append({"id": row["id"], "category": row["category"],
                                "source_text": row["source_text"],
                                "context": {key: (row.get("context") or {}).get(key)
                                            for key in ("event_name", "map_name", "speaker")},
                                "reason": reason})

    per_category = Counter(row["category"] for row in canonical.values())
    covered_per_category = Counter(canonical[row_id]["category"] for row_id in covered)
    blank_per_category = Counter(row["category"] for row in blank)
    return {
        "canonical_records": len(canonical),
        "canonical_categories": dict(sorted(per_category.items())),
        "draft_files": len(draft_paths(drafts_dir)),
        "draft_rows": draft_rows,
        "drafts_with_translation": sum(len(entries) for entries in drafts.values()),
        "covered_ids": len(covered),
        "covered_per_category": dict(sorted(covered_per_category.items())),
        "unknown_draft_ids": unknown,
        "conflicts": conflicts,
        "blank_records": len(blank),
        "blank_protected": sum(is_protected(row) for row in blank),
        "blank_translatable": sum(not is_protected(row) for row in blank),
        "blank_per_category": dict(sorted(blank_per_category.items())),
        "buckets": {name: sorted(items, key=lambda item: item["id"])
                    for name, items in sorted(buckets.items())},
        "bucket_counts": {name: len(items) for name, items in sorted(buckets.items())},
        "identical_translations": identical_translations(canonical, drafts),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Audyt pokrycia draftów — The Genesis Order",
        "",
        "> Plik generowany przez `tools/audit_draft_coverage.py`. Liczby pochodzą wyłącznie "
        "z kanonicznego eksportu i plików `translation/drafts/` (rekurencyjnie). "
        "Etykiety kubełków są dowodem, nie decyzją tłumaczeniową.",
        "",
        "## Podsumowanie",
        "",
        f"- Rekordy kanoniczne: **{report['canonical_records']}**.",
        f"- Pliki draftów: **{report['draft_files']}**, wierszy: **{report['draft_rows']}**.",
        f"- Unikalne ID z niepustym tłumaczeniem: **{report['covered_ids']}**.",
        f"- Puste rekordy ogółem: **{report['blank_records']}**, w tym "
        f"**{report['blank_protected']}** chronionych `keep_source_value` i "
        f"**{report['blank_translatable']}** do rozstrzygnięcia.",
        f"- Konflikty niepustych wariantów: **{len(report['conflicts'])}**.",
        f"- Tłumaczenia identyczne ze źródłem w kategorii prozatorskiej: "
        f"**{len(report['identical_translations'])}**.",
        "",
        "## Kubełki pustych rekordów",
        "",
        "| Kubełek | Rekordy | Znaczenie |",
        "|---|---:|---|",
    ]
    meanings = {
        "protected": "`keep_source_value` — wartość musi zostać bez zmian",
        "command": "komendy `custom_dialogue` zaczynające się od `/` — sterowanie, nie proza",
        "markup_only": "po usunięciu tokenów nie zostaje żadna litera",
        "blocked_by_signature": "sygnatura v1 skleja tag `\\fb` z pierwszym słowem (ADR 002)",
        "template_placeholder": "wypełniacz szablonu mapy testowej",
        "credits_roster": "listy nazw wspierających — nazw nie tłumaczymy",
        "proper_name": "imiona postaci, nazwy przedmiotów, podpisy galerii",
        "identifier": "kody, liczby i krótkie markery",
        "needs_review": "realny tekst bez tłumaczenia — wymaga decyzji i draftu",
    }
    for name, count in report["bucket_counts"].items():
        lines.append(f"| `{name}` | {count} | {meanings.get(name, '')} |")
    lines += ["", "## Pokrycie według kategorii", "",
              "| Kategoria | Rekordy | Z tłumaczeniem | Puste |", "|---|---:|---:|---:|"]
    for category, total in report["canonical_categories"].items():
        covered = report["covered_per_category"].get(category, 0)
        blank = report["blank_per_category"].get(category, 0)
        lines.append(f"| `{category}` | {total} | {covered} | {blank} |")
    review = report["buckets"].get("needs_review", [])
    lines += ["", f"## Rekordy `needs_review` ({len(review)})", ""]
    if review:
        lines += ["| ID | Kategoria | Źródło | Zdarzenie |", "|---|---|---|---|"]
        for item in review:
            event = (item["context"] or {}).get("event_name") or ""
            text = item["source_text"].replace("|", "\\|")
            lines.append(f"| `{item['id']}` | `{item['category']}` | {text} | {event} |")
    else:
        lines.append("Brak — wszystkie pozostałe puste rekordy są techniczne, nazwowe lub chronione.")
    conflicts = report["conflicts"]
    lines += ["", f"## Konflikty niepustych wariantów ({len(conflicts)})", ""]
    if conflicts:
        lines += ["| ID | Źródło | Warianty |", "|---|---|---|"]
        for item in conflicts:
            variants = "<br>".join(
                f"`{entry['file']}` → {entry['translation']}" for entry in item["values"])
            lines.append(f"| `{item['id']}` | {item['source_text']} | {variants} |")
    else:
        lines.append("Brak konfliktów.")
    identical = report["identical_translations"]
    lines += ["", f"## Tłumaczenia identyczne ze źródłem ({len(identical)})", ""]
    if identical:
        lines += ["| ID | Kategoria | Plik | Tekst |", "|---|---|---|---|"]
        for item in identical:
            lines.append(f"| `{item['id']}` | `{item['category']}` | `{item['file']}` | "
                         f"{item['source_text']} |")
    else:
        lines.append("Brak.")
    lines += ["", "## Odtworzenie", "", "```bash",
              "python3 games/the-genesis-order/tools/audit_draft_coverage.py \\",
              "  --markdown-out games/the-genesis-order/docs/COVERAGE_AUDIT.md",
              "```", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical", type=Path, default=DEFAULT_EXPORT)
    parser.add_argument("--drafts", type=Path, default=DEFAULT_DRAFTS)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--markdown-out", type=Path)
    parser.add_argument("--quiet", action="store_true", help="print only the summary")
    args = parser.parse_args()

    report = audit(args.canonical, args.drafts)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8", newline="\n")
    if args.markdown_out:
        args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_out.write_text(render_markdown(report), encoding="utf-8", newline="\n")
    summary = {
        "canonical_records": report["canonical_records"],
        "draft_files": report["draft_files"],
        "draft_rows": report["draft_rows"],
        "covered_ids": report["covered_ids"],
        "blank_records": report["blank_records"],
        "blank_translatable": report["blank_translatable"],
        "conflicts": len(report["conflicts"]),
        "identical_translations": len(report["identical_translations"]),
        "bucket_counts": report["bucket_counts"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not args.quiet:
        review = report["buckets"].get("needs_review", [])
        for item in review:
            print(f"{item['id']}\t{item['category']}\t{item['source_text']}")


if __name__ == "__main__":
    main()
