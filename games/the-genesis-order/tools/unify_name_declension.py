#!/usr/bin/env python3
"""Ujednolicenie odmiany imion żeńskich zakończonych na ``-a`` (decyzja R-09).

Tło: korpus powstał w partiach, więc imiona były odmieniane tylko w części
wystąpień — obok siebie stały „sypialni Andrei” i „z Andrea”. Właściciel
zatwierdził ujednolicenie odmiany (bez ponownego tłumaczenia).

Narzędzie **nie jest** tłumaczeniem automatycznym. Przeprowadza wyłącznie
odmianę morfologiczną imienia w miejscach, w których przypadek da się ustalić
składniowo, i tylko dla imion na ``-a``. Stosuje dwie wąskie reguły:

1. **Wołacz** — imię jest bezpośrednim zwrotem do rozmówcy: stoi po przecinku
   przed znakiem interpunkcyjnym (``Cholera, Ella.`` → ``Cholera, Ello.``),
   otwiera zdanie przecinkiem (``Ella, chodź tu``) albo jest całą kwestią
   (``Ella!``).
2. **Dopełniacz** — imię jest rząddzone przez rzeczownik lub przyimek, które
   wymagają dopełniacza (``fragment Toma`` → ``fragment Tomy``, ``do Toma``).

Wszystko inne zostaje bez zmian i trafia do raportu jako pozycja do ręcznego
przejrzenia. To świadomy kompromis: wolimy nie zmieniać 500 poprawnych
mianowników niż wygenerować błędne formy w 200 zdaniach.

Narzędzie jest idempotentne (drugi przebieg nic nie zmienia), a każda zmiana
ma wpis w raporcie z ID rekordu i pełnym zdaniem przed/po.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = ROOT / "translation"
DRAFTS = TRANSLATION / "drafts"
REPORT = TRANSLATION / "reports" / "declension_r09_report.json"

# Formy dla imion żeńskich na -a. Klucz to mianownik (forma w źródle).
DECLENSION: dict[str, dict[str, str]] = {
    "Erica": {"gen": "Eriki", "dat": "Erice", "acc": "Ericę", "ins": "Ericą", "loc": "Erice", "voc": "Eriko"},
    "Andrea": {"gen": "Andrei", "dat": "Andrei", "acc": "Andreę", "ins": "Andreą", "loc": "Andrei", "voc": "Andreo"},
    "Arianna": {"gen": "Arianny", "dat": "Ariannie", "acc": "Ariannę", "ins": "Arianną", "loc": "Ariannie", "voc": "Arianno"},
    "Melissa": {"gen": "Melissy", "dat": "Melissie", "acc": "Melissę", "ins": "Melissą", "loc": "Melissie", "voc": "Melisso"},
    "Ella": {"gen": "Elli", "dat": "Elli", "acc": "Ellę", "ins": "Ellą", "loc": "Elli", "voc": "Ello"},
    "Toma": {"gen": "Tomy", "dat": "Tomie", "acc": "Tomę", "ins": "Tomą", "loc": "Tomie", "voc": "Tomo"},
    "Diana": {"gen": "Diany", "dat": "Dianie", "acc": "Dianę", "ins": "Dianą", "loc": "Dianie", "voc": "Diano"},
    "Tasha": {"gen": "Tashy", "dat": "Tashy", "acc": "Tashę", "ins": "Tashą", "loc": "Tashy", "voc": "Tasho"},
    "Alia": {"gen": "Alii", "dat": "Alii", "acc": "Alię", "ins": "Alią", "loc": "Alii", "voc": "Alio"},
}

# Rzeczowniki i przyimki, po których w polszczyźnie wymagany jest dopełniacz.
GENITIVE_GOVERNORS = (
    "fragment", "fragmenty", "fragmentu", "fragmentem", "kawałek", "kawałka",
    "ślad", "śladu", "część", "części", "zdjęcie", "zdjęcia", "do", "od", "u",
    "dla", "bez", "obok", "koło", "około", "wobec", "zamiast", "oprócz",
    "według", "poza", "wśród", "podczas", "dookoła", "naprzeciw",
)

NAME_RE = re.compile(
    r"(?<![\wŁŚŻŹĆŃÓĄĘ])(?P<name>" + "|".join(sorted(DECLENSION, key=len, reverse=True)) + r")(?![\wŁŚŻŹĆŃÓĄĘ])"
)
# Koniec frazy imienia: znak interpunkcyjny kończący zdanie/klauzulę.
CLAUSE_END = set(".!?…,;:")
# Znaczniki renderera (kolory, ikony, znaczniki HTML) nie są treścią zdania,
# więc przy ocenie sąsiedztwa imienia patrzymy na tekst widoczny dla gracza.
MARKUP_RE = re.compile(r"\\[A-Za-z]+(?:\[[^\]]*\])?|<[^>]+>")


def _preceding_word(text: str, start: int) -> tuple[str, str]:
    """Return (word_before_name_lowercased, raw_prefix) ignoring markup escapes."""
    prefix = text[:start]
    stripped = re.sub(r"\\c\[\d+\]", "", prefix).rstrip()
    words = stripped.split()
    if not words:
        return "", prefix
    return words[-1].lower().strip(",.;:!?…"), prefix


def _visible_neighbours(text: str, start: int, end: int) -> tuple[str, str]:
    """Return nearest player-visible characters before and after ``text[start:end]``."""
    before = after = ""
    for match in MARKUP_RE.finditer(text):
        pass
    hidden = [(m.start(), m.end()) for m in MARKUP_RE.finditer(text)]

    def is_hidden(index: int) -> bool:
        return any(begin <= index < finish for begin, finish in hidden)

    for index in range(start - 1, -1, -1):
        if not is_hidden(index):
            before = text[index]
            if not before.isspace():
                break
    for index in range(end, len(text)):
        if not is_hidden(index):
            after = text[index]
            if not after.isspace():
                break
    return before, after


def _is_whole_utterance(text: str, match: re.Match[str]) -> bool:
    before = re.sub(r"\\[A-Za-z]+(?:\[[^\]]*\])?", "", text[:match.start()]).strip(" „\"(")
    after = re.sub(r"\\[A-Za-z]+(?:\[[^\]]*\])?", "", text[match.end():]).strip(" ”\")")
    return before == "" and after.strip(" .!?…") == ""


def decide(text: str, match: re.Match[str]) -> tuple[str, str] | None:
    """Return (case, rule_id) when the grammatical case is determined, else None."""
    name = match.group("name")
    after = text[match.end():]
    before_char, next_char = _visible_neighbours(text, match.start(), match.end())
    word, _ = _preceding_word(text, match.start())

    if _is_whole_utterance(text, match):
        return "voc", "vocative_whole_utterance"
    # Wołacz: imię zamyka klauzulę po przecinku („Cholera, Ella.”).
    if before_char == "," and (next_char in CLAUSE_END or after.strip() == ""):
        return "voc", "vocative_comma_address"
    # Wołacz: imię otwiera zdanie i jest oddzielone przecinkiem („Ella, chodź tu”).
    if not text[:match.start()].strip(" „\"(") and next_char == ",":
        return "voc", "vocative_leading_address"
    # Wołacz w łańcuchu zwrotów: „Ella, Diana…” — drugie imię też jest adresatem.
    if before_char == "," and next_char in {"…", "!", "?", ","} and word in {
            name.lower() for name in DECLENSION}:
        return "voc", "vocative_address_chain"
    # Dopełniacz: rzeczownik/przyimek rządzący dopełniaczem.
    if word in GENITIVE_GOVERNORS:
        return "gen", "genitive_governor"
    return None


def transform(text: str) -> tuple[str, list[tuple[str, str, str, str]]]:
    """Return new text and a list of (name, case, rule, form) changes."""
    changes: list[tuple[str, str, str, str]] = []
    pieces: list[str] = []
    last = 0
    for match in NAME_RE.finditer(text):
        decision = decide(text, match)
        if decision is None:
            continue
        case, rule = decision
        form = DECLENSION[match.group("name")][case]
        pieces.append(text[last:match.start()])
        pieces.append(form)
        last = match.end()
        changes.append((match.group("name"), case, rule, form))
    pieces.append(text[last:])
    return "".join(pieces), changes


def iter_draft_rows(path: Path):
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            yield number, json.loads(line)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="zapisz zmiany w plikach draftów")
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument("--sample", type=int, default=0, help="pokaż N przykładowych zmian")
    args = parser.parse_args()

    by_rule: Counter[str] = Counter()
    by_name: Counter[str] = Counter()
    edited_files = 0
    edited_rows = 0
    seen: list[dict[str, Any]] = []
    occurrences = Counter()
    pending: list[dict[str, str]] = []

    for path in sorted(DRAFTS.rglob("*.jsonl")):
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
            for match in NAME_RE.finditer(text):
                occurrences["name_occurrence"] += 1
                if decide(text, match) is None:
                    pending.append({"id": row["id"], "name": match.group("name"), "text": text})
            new_text, changes = transform(text)
            if not changes:
                output.append(line)
                continue
            row["translation"] = new_text
            for name, case, rule, form in changes:
                by_rule[rule] += 1
                by_name[f"{name}->{form}"] += 1
                if len(seen) < 400:
                    seen.append({"id": row["id"], "name": name, "case": case, "rule": rule,
                                 "before": text, "after": new_text})
            output.append(json.dumps(row, ensure_ascii=False, sort_keys=True))
            touched = True
            edited_rows += 1
        if touched:
            edited_files += 1
            if args.apply:
                path.write_text("\n".join(output) + "\n", encoding="utf-8", newline="\n")

    report = {
        "schema": "tgo-declension-r09-report-v1",
        "decision": "R-09 — ujednolicenie odmiany imion na -a (decyzja właściciela 2026-10-29)",
        "mode": "apply" if args.apply else "dry-run",
        "name_occurrences": occurrences["name_occurrence"],
        "changed_occurrences": sum(by_rule.values()),
        "changed_rows": edited_rows,
        "changed_files": edited_files,
        "by_rule": dict(sorted(by_rule.items())),
        "by_form": dict(sorted(by_name.items())),
        "review_pending_occurrences": len(pending),
        "sample_changes": seen[:40],
    }
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: report[k] for k in ("mode", "name_occurrences", "changed_occurrences",
                                             "changed_rows", "changed_files", "by_rule",
                                             "review_pending_occurrences")}, ensure_ascii=False, indent=2))
    if args.sample:
        for item in seen[: args.sample]:
            print(f"\n[{item['rule']}] {item['id']}\n  PRZED: {item['before'][:150]}\n  PO:    {item['after'][:150]}")


if __name__ == "__main__":
    main()
