#!/usr/bin/env python3
"""Raport odmiany imienia bohatera w Czytance (``1Hero`` → „Mox”).

Narzędzie jest **tylko audytem**: czyta drafty, przepuszcza każdy tekst przez
reguły z ``tools/hero_declension.py`` i zapisuje raport decyzji. Nie zmienia
plików tłumaczeń — drafty muszą zachować placeholder ``1Hero``, bo gra
podstawia tam imię gracza w runtime. Odmiana dzieje się wyłącznie na warstwie
Czytanki (``tools/build_readalong.py``).

Raport odpowiada na trzy pytania:

* ile wystąpień placeholdera jest w korpusie i w jakich przypadkach,
* które zdania zmienią się w Czytance (z uzasadnieniem reguły),
* które wystąpienia wymagają przeglądu, bo czasownik rządzący nie jest
  w zamkniętej tabeli (moduł nigdy nie zgaduje przypadku).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hero_declension  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "translation" / "drafts"
DEFAULT_REPORT = ROOT / "translation" / "reports" / "hero_declension_v1.json"


def display_path(path: Path) -> str:
    """Ścieżka względna do repo, także gdy `--drafts` podano względnie."""
    resolved = path if path.is_absolute() else path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(path)


def iter_rows(drafts: Path):
    for path in sorted(drafts.rglob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                yield path, json.loads(line)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--drafts", type=Path, default=DRAFTS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args(argv)

    if not args.drafts.is_dir():
        print(f"BŁĄD: brak katalogu z draftami: {args.drafts}", file=sys.stderr)
        return 2

    occurrences = 0
    records_with_placeholder = 0
    changed_records = 0
    by_case: Counter[str] = Counter()
    by_reason: Counter[str] = Counter()
    changes: list[dict] = []
    unresolved: list[dict] = []
    examples_by_case: dict[str, list[str]] = {}

    for path, row in iter_rows(args.drafts):
        text = row.get("translation")
        if not isinstance(text, str) or hero_declension.HERO_PLACEHOLDER not in text:
            continue
        records_with_placeholder += 1
        new_text, decisions = hero_declension.decline_text(text)
        occurrences += len(decisions)
        touched = False
        for decision in decisions:
            case = decision["case"] or "brak"
            by_case[case] += 1
            by_reason[str(decision["reason"])] += 1
            examples_by_case.setdefault(case, [])
            if len(examples_by_case[case]) < 3:
                examples_by_case[case].append(new_text)
            if decision["resolved"] and case not in {"nom", "voc"}:
                touched = True
            if not decision["resolved"]:
                unresolved.append({
                    "id": row.get("id"),
                    "file": display_path(path),
                    "text": text,
                    "reason": decision["reason"],
                })
        if touched:
            changed_records += 1
            if len(changes) < 200:
                changes.append({
                    "id": row.get("id"),
                    "file": display_path(path),
                    "before": text,
                    "after": new_text,
                })

    report = {
        "schema": "tgo-hero-declension-report-v1",
        "decision": "R-12 — imię bohatera w Czytance ma poprawne formy przypadków",
        "mode": "audit (drafty bez zmian; odmiana na warstwie Czytanki)",
        "hero": {"name": hero_declension.HERO_FORMS["nom"], "forms": hero_declension.HERO_FORMS},
        "records_with_placeholder": records_with_placeholder,
        "occurrences": occurrences,
        "records_changed_in_reading": changed_records,
        "by_case": dict(sorted(by_case.items())),
        "by_reason": dict(sorted(by_reason.items(), key=lambda item: -item[1])),
        "examples_by_case": examples_by_case,
        "changes": changes,
        "unresolved": unresolved,
        "unresolved_count": len(unresolved),
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=args.indent) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({
        "records_with_placeholder": records_with_placeholder,
        "occurrences": occurrences,
        "records_changed_in_reading": changed_records,
        "by_case": report["by_case"],
        "unresolved_count": report["unresolved_count"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
