#!/usr/bin/env python3
"""Dokończenie odmiany imion w korpusie (decyzja R-13).

Tło: R-09 (`tools/unify_name_declension.py`) odmienił 383 wystąpienia imion na
``-a``, ale **628** wystąpień zostało w mianowniku jako „do przejrzenia”.
Przegląd z 2026-10-31 pokazał, że niemal wszystkie są poprawne (podmiot na
początku klauzuli, orzecznik po „jest/to/czy”), **poza** garstką miejsc,
w których przypadek da się ustalić — i to one są przedmiotem tego narzędzia.

Narzędzie rozszerza tabele rządu R-09 o te same reguły, których używa
`tools/hero_declension.py` dla imienia bohatera, plus:

1. **Rzeczowniki rządzące dopełniaczem** — „fragment/kawałki/posąg/użycie/
   pomocą Toma” → „…Tomy” (nazwa artefaktu, deklinacja jak imię żeńskie).
2. **Czasowniki z zamkniętej listy** — ``szuka``, ``użyje`` → dopełniacz;
   ``zdobądź``, ``złóż``, ``zniszcz``, ``uratuj``, ``odzyskaj`` → biernik.
3. **Przyimki** — te same tabele co dla bohatera (jednoznaczne + domyślne
   z wyjątkami ``z`` + źródło i „chodzi o”).
4. **Poprawka napisów systemowych** (``NATIVE_OVERRIDES``): angielskie
   „Get Melissa's phone number to unlock” zostało przetłumaczone bez
   dopełniacza („Zdobądź Melissa numer telefonu”); poprawka przywraca polski
   szyk i formę („Zdobądź numer telefonu Melissy”).

Wszystko, czego nie da się rozstrzygnąć, zostaje w mianowniku i trafia do
raportu jako ``pending`` z klasą słowa rządzącego. Narzędzie jest idempotentne,
domyślnie działa jako dry-run i **odmawia nadpisania istniejącego raportu**.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hero_declension as hero  # noqa: E402
import unify_name_declension as names  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "translation" / "drafts"
REPORT = ROOT / "translation" / "reports" / "declension_refine_v1.json"

# Rzeczowniki, po których imię artefaktu stoi w dopełniaczu („fragment Tomy”).
NOUN_GENITIVE_GOVERNORS: dict[str, str] = {
    governor: "gen"
    for governor in (
        "fragment", "fragmentu", "fragmenty", "fragmentów", "fragmentem", "fragmentami",
        "kawałek", "kawałka", "kawałki", "kawałków", "kawałkiem", "kawałkami",
        "posąg", "posągu", "posągi", "posągów", "posągiem", "posągami",
        "użycie", "użycia", "użyciem", "pomocą", "część", "części", "ślad", "śladu", "śladów",
        "złożenie", "zniszczenie", "odzyskanie", "zdobycie", "odnalezienie",
        "szukanie", "szukania", "szukaniu",
    )
}

# Czasowniki z jednoznacznym rządem — zamknięta lista, wyłącznie z korpusu.
VERB_CASES: dict[str, str] = {}
VERB_CASES.update({
    "szuka": "gen", "szukam": "gen", "szukasz": "gen", "szukają": "gen",
    "szukał": "gen", "szukała": "gen", "szukali": "gen", "szukać": "gen",
    "użyje": "gen", "użyję": "gen", "użyła": "gen", "użył": "gen",
    "używać": "gen", "używa": "gen", "używają": "gen",
    "kwestionuj": "gen", "kwestionować": "gen", "dopilnować": "gen",
    # „strzec czegoś”, „używać czegoś”, „dopełnić czegoś”
    "strzec": "gen", "strzeże": "gen", "strzegą": "gen",
    "strzegł": "gen", "strzegła": "gen", "strzegły": "gen",
    "używał": "gen", "używała": "gen", "użyli": "gen", "użyły": "gen", "używały": "gen",
    "dopełni": "gen", "dopełnić": "gen", "dopełnia": "gen",
})
VERB_CASES.update({
    "dokończyć": "acc", "dokończ": "acc", "dokończy": "acc", "dokończycie": "acc",
    "ukończyć": "acc", "ukończ": "acc", "skończyć": "acc",
    "złożyć": "acc", "złóż": "acc", "złóżmy": "acc", "złożyła": "acc", "złożył": "acc",
    "składam": "acc", "złożymy": "acc",
    "zniszczyć": "acc", "zniszcz": "acc", "zniszczy": "acc", "zniszczymy": "acc",
    "zniszczyła": "acc", "zniszczył": "acc",
    "uratować": "acc", "uratuj": "acc", "ratować": "acc",
    "odzyskać": "acc", "odzyskaj": "acc", "odzyskamy": "acc", "odzyskał": "acc",
    "zdobyć": "acc", "zdobądź": "acc", "zdobędziemy": "acc", "zdobyła": "acc", "zdobył": "acc",
    "zabrać": "acc", "zabierz": "acc", "zabieramy": "acc",
    "ukraść": "acc", "ukradł": "acc", "ukradli": "acc",
    "wyrwać": "acc", "wyrwij": "acc",
    "pobłogosławić": "acc", "pobłogosław": "acc",
    "powstrzymać": "acc", "powstrzymamy": "acc", "powstrzymaj": "acc",
    "opuścić": "acc", "zostawić": "acc",
    "sprowadzić": "acc", "sprowadzono": "acc", "sprowadził": "acc",
    "sprowadziła": "acc", "sprowadź": "acc",
})

# Napisy systemowe: angielskie „Get X's phone number to unlock” straciło
# w tłumaczeniu dopełniacz. Klucz to fragment do podmiany, wartość — nowy tekst.
# Pojedyncze zdania wymagające decyzji redakcyjnej (nie reguły ogólnej):
# (1) „Żaden Toma” — nazwa artefaktu jest żeńska („Toma została zniszczona”),
#     więc rodzajnik i orzecznik też muszą być żeńskie;
# (2) „nie odbierzecie nam Toma” — po przeczeniu dopełnienie idzie w dopełniaczu.
CURATED_OVERRIDES: dict[str, str] = {
    "Żaden Toma nie jest wart utraty życia.": "Żadna Toma nie jest warta utraty życia.",
    "Nie odbierzecie nam Toma Leolo!": "Nie odbierzecie nam Tomy Leolo!",
    # (3) „sprowadzono z powrotem Toma” — czasownik stoi dwa słowa przed imieniem,
    #     a przysłówek „z powrotem” nie rządzi przypadkiem; biernik po „sprowadzić”.
    "z powrotem Toma Leolo": "z powrotem Tomę Leolo",
    # (4) wielokropek rozcina klauzulę, więc rządzące „szukaniu” jest poza zasięgiem
    #     reguły; dopełniacz przywrócony ręcznie.
    "szukaniu… Toma i amuletów": "szukaniu… Tomy i amuletów",
}

NATIVE_OVERRIDES: dict[str, str] = {
    "Zdobądź\\c[14] Melissa \\c[0]numer telefonu":
        "Zdobądź numer telefonu \\c[14]Melissy\\c[0]",
    "Zdobądź\\c[14] Hannah \\c[0]numer telefonu":
        "Zdobądź numer telefonu \\c[14]Hannah\\c[0]",
    "Zdobądź\\c[14] Carol \\c[0]numer telefonu":
        "Zdobądź numer telefonu \\c[14]Carol\\c[0]",
}


def apply_overrides(text: str) -> tuple[str, list[dict[str, str]]]:
    """Podmień napisy systemowe; zwróć tekst i listę zastosowanych poprawek."""
    applied: list[dict[str, str]] = []
    for before, after in CURATED_OVERRIDES.items():
        if before in text:
            text = text.replace(before, after)
            applied.append({"before": before, "after": after})
    for before, after in NATIVE_OVERRIDES.items():
        if before in text:
            text = text.replace(before, after)
            applied.append({"before": before, "after": after})
    return text, applied


def decide(text: str, match: re.Match[str]) -> tuple[str, str] | None:
    """Zwróć ``(przypadek, reguła)`` albo ``None``, gdy przypadek jest niepewny."""
    base = names.decide(text, match)
    if base is not None:
        return base
    words = hero._words_before(text, match.start())
    governor = words[0] if words else ""
    previous = words[1] if len(words) > 1 else ""
    if not governor:
        return None
    if governor in hero.PREPOSITION_CASES:
        return hero.PREPOSITION_CASES[governor], f"preposition:{governor}"
    if governor in hero.DEFAULT_AMBIGUOUS:
        case = hero.DEFAULT_AMBIGUOUS[governor]
        if governor in {"z", "ze"} and previous in hero.GENITIVE_Z_GOVERNORS:
            return "gen", f"preposition:{governor}+{previous}"
        if governor == "o" and previous in hero.ACC_O_GOVERNORS:
            return "acc", f"preposition:{governor}+{previous}"
        return case, f"preposition_default:{governor}"
    if governor in NOUN_GENITIVE_GOVERNORS:
        return NOUN_GENITIVE_GOVERNORS[governor], f"noun:{governor}"
    if governor in VERB_CASES:
        return VERB_CASES[governor], f"verb:{governor}"
    return None


def transform(text: str) -> tuple[str, list[tuple[str, str, str, str]]]:
    """Zwróć nowy tekst i listę ``(imię, przypadek, reguła, forma)``."""
    text, _ = apply_overrides(text)
    pieces: list[str] = []
    changes: list[tuple[str, str, str, str]] = []
    last = 0
    for match in names.NAME_RE.finditer(text):
        decision = decide(text, match)
        if decision is None:
            continue
        case, rule = decision
        form = names.DECLENSION[match.group("name")][case]
        pieces.append(text[last:match.start()])
        pieces.append(form)
        last = match.end()
        changes.append((match.group("name"), case, rule, form))
    pieces.append(text[last:])
    return "".join(pieces), changes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--drafts", type=Path, default=DRAFTS)
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument("--apply", action="store_true", help="zapisz zmiany w draftach")
    parser.add_argument("--force", action="store_true", help="nadpisz istniejący raport")
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args(argv)

    if args.report.exists() and not args.force:
        raise SystemExit(f"Raport już istnieje: {args.report} — użyj --force lub innej ścieżki")

    by_rule: Counter[str] = Counter()
    by_form: Counter[str] = Counter()
    by_override: Counter[str] = Counter()
    changes: list[dict[str, str]] = []
    pending: list[dict[str, str]] = []
    pending_classes: Counter[str] = Counter()
    rows_changed = 0
    files_changed = 0

    for path in sorted(args.drafts.rglob("*.jsonl")):
        original = path.read_text(encoding="utf-8").splitlines()
        output: list[str] = []
        touched = False
        for line in original:
            if not line.strip():
                output.append(line)
                continue
            row = json.loads(line)
            text = row.get("translation")
            if not isinstance(text, str) or not text.strip():
                output.append(line)
                continue
            new_text, row_changes = transform(text)
            _, applied = apply_overrides(text)
            for item in applied:
                by_override[item["after"]] += 1
            if new_text == text:
                for match in names.NAME_RE.finditer(text):
                    if decide(text, match) is not None:
                        continue
                    words = hero._words_before(text, match.start())
                    governor = words[0] if words else ""
                    if not governor:
                        klass = "początek-klauzuli"
                    elif governor in hero.PREPOSITION_CASES or governor in hero.DEFAULT_AMBIGUOUS:
                        klass = f"przyimek:{governor}"
                    elif hero._is_verb_like(governor):
                        klass = f"czasownik-spoza-tabeli:{governor}"
                    else:
                        klass = f"inne:{governor}"
                    pending_classes[klass] += 1
                    if len(pending) < 400:
                        pending.append({"id": row.get("id"), "name": match.group("name"),
                                        "class": klass, "text": text})
                output.append(line)
                continue
            row["translation"] = new_text
            output.append(json.dumps(row, ensure_ascii=False, sort_keys=True))
            touched = True
            rows_changed += 1
            for name, case, rule, form in row_changes:
                by_rule[rule] += 1
                by_form[f"{name}->{form}"] += 1
                changes.append({"id": row.get("id"), "file": str(path.relative_to(ROOT)),
                                "name": name, "case": case, "rule": rule, "form": form,
                                "before": text, "after": new_text})
        if touched:
            files_changed += 1
            if args.apply:
                path.write_text("\n".join(output) + "\n", encoding="utf-8", newline="\n")

    report = {
        "schema": "tgo-declension-refine-v1",
        "decision": "R-13 — dokończenie odmiany imion (rzeczowniki, czasowniki, przyimki, napisy systemowe)",
        "mode": "apply" if args.apply else "dry-run",
        "changed_rows": rows_changed,
        "changed_files": files_changed,
        "changed_occurrences": sum(by_rule.values()),
        "by_rule": dict(sorted(by_rule.items())),
        "by_form": dict(sorted(by_form.items())),
        "native_overrides": dict(sorted(by_override.items())),
        "pending_occurrences": sum(pending_classes.values()),
        "pending_by_class": dict(pending_classes.most_common(40)),
        "pending_sample": pending[:40],
        "changes": changes,
    }
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=args.indent) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({key: report[key] for key in (
        "mode", "changed_occurrences", "changed_rows", "changed_files",
        "by_rule", "native_overrides", "pending_occurrences")},
        ensure_ascii=False, indent=2))
    for item in changes:
        print(f"\n[{item['rule']}] {item['name']} {item['id']}\n  PRZED: {item['before'][:150]}\n  PO:    {item['after'][:150]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
