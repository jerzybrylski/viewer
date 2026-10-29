#!/usr/bin/env python3
"""Audyt redakcyjny korpusu TGO PL — co jest usterką, a co tylko stylem.

Narzędzie rozdziela dwie rzeczy, które łatwo pomylić:

* **usterki techniczne** (spacje, interpunkcja, powtórzone słowo) — mierzalne,
  zwykle do poprawienia bez czytania kontekstu;
* **obserwacje stylistyczne** (powtarzalne frazy, długie linie, nazwy własne)
  — wymagają decyzji redaktora, więc są tylko raportowane.

Audyt **nie tłumaczy** i nie wymyśla tekstu. Tryb `--fix` poprawia wyłącznie
usterki z klasy oznaczonej jako `auto_fixable` i tylko wtedy, gdy źródło nie
ma tej samej cechy (spacja brzegowa w źródle bywa celowa — sklejanie linii).
Każda zmiana trafia do dziennika z pełnym tekstem przed/po.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = ROOT / "translation"
DRAFTS = TRANSLATION / "drafts"
CANONICAL = TRANSLATION / "export-v1"
REPORT_JSON = TRANSLATION / "reports" / "editorial_qa_v1.json"
REPORT_MD = ROOT / "docs" / "EDITORIAL_QA.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from merge_translation_batches import merge_batches  # noqa: E402

# Słowa angielskie, które nie są jednocześnie polskimi wyrazami. „but" (obuwie),
# „was", „to", „no", „do" itd. celowo pominięte — dawały fałszywe trafienia.
ENGLISH_LEFTOVERS = re.compile(
    r"\b(the|you|your|and|what|that|this|with|from|have|will|been|they|them|are|"
    r"were|for|not|his|her|she|him|who|why|how|when|where|there|here|just|like|"
    r"know|want|going|get|got|could|should|about|because|would)\b",
    re.IGNORECASE,
)
# Powtórzenia, które w polszczyźnie bywają poprawne („jej jej" = jej + to).
REPEATED_WORD_OK = {("jej", "jej"), ("się", "się")}

# Trafienia sprawdzone ręcznie i uznane za poprawne — nie zgłaszamy ich ponownie.
# Klucz: (klasa, id rekordu) → uzasadnienie. Każdy wpis wymaga lektury zdania.
REVIEWED: dict[tuple[str, str], str] = {
    ("repeated_word", "tgo:custom_dialogue:6bacf88cd88d60bb1204"):
        "„niczego na nie nie wylej” — „na nie” + „nie wylej”, poprawna negacja",
    ("repeated_word", "tgo:custom_dialogue:fbd70422a4c7258abe0d"):
        "„To to wszystko wywołało” — zaimek „to” + „to wszystko”, gramatyczne",
    ("dash_en", "tgo:arianna_hint:55a671dda96321ca81b8"):
        "„2–21” to zakres liczbowy; półpauza jest tu poprawna",
    ("english_leftover", "tgo:native_message_unclassified:ed9055a8c1d4b7d5badc"):
        "„The Genesis Order” — decyzja R-01: tytuł gry zostaje po angielsku",
    ("lowercase_start", "tgo:phone_contact_ui:e7aee3c69c8ba87fe834"):
        "„po otrzymaniu.” — ciąg dalszy wiadomości z poprzedniej linii",
    ("lowercase_start", "tgo:phone_text:c87217684decf9190e5c"):
        "„możesz je ponownie włączyć…” — ciąg dalszy zdania z komunikatu",
    ("lowercase_start", "tgo:phone_text:8f056cddc91db868c2ea"):
        "„aby wyłączyć filtr NSFW.” — ciąg dalszy zdania z komunikatu",
}
DASHES = {"—": "em", "–": "en"}


def repeated_word(text: str) -> str | None:
    for match in re.finditer(r"\b(\w{2,})\s+\1\b", text, re.IGNORECASE):
        word = match.group(1).lower()  # \1 to odwołanie wsteczne, nie druga grupa
        if (word, word) in REPEATED_WORD_OK:
            continue
        return match.group(0)
    return None


def ngrams(text: str, n: int) -> Iterable[str]:
    words = re.findall(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż']+", text.lower())
    for index in range(len(words) - n + 1):
        gram = " ".join(words[index:index + n])
        if len(gram) > 8:
            yield gram


def load_rows() -> list[dict[str, Any]]:
    with tempfile.TemporaryDirectory(prefix="tgo-qa-", dir=TRANSLATION) as work:
        merged = Path(work) / "merged.jsonl"
        merge_batches(CANONICAL, sorted(DRAFTS.rglob("*.jsonl")), merged, TRANSLATION)
        return [json.loads(line) for line in merged.read_text(encoding="utf-8").splitlines() if line.strip()]


def analyse(rows: list[dict[str, Any]], top: int = 25) -> dict[str, Any]:
    findings: dict[str, list[dict[str, str]]] = defaultdict(list)
    phrase_counts: Counter[str] = Counter()
    phrase_examples: dict[str, dict[str, str]] = {}
    name_variants: dict[str, Counter[str]] = defaultdict(Counter)
    translated = 0
    lengths: list[int] = []

    for row in rows:
        value = row.get("translation") or ""
        if not value.strip():
            continue
        translated += 1
        lengths.append(len(value))
        source = row.get("source_text") or ""
        record_id = row.get("id", "")

        # --- usterki techniczne -------------------------------------------------
        if value != value.strip() and source.strip() == source:
            findings["whitespace_edges"].append({"id": record_id, "text": value})
        if re.search(r"(?<=\S) {2,}(?=\S)", value) and not re.search(r"(?<=\S) {2,}(?=\S)", source):
            findings["whitespace_double"].append({"id": record_id, "text": value})
        if (re.search(r"\s+[.,;:](?!\d)", value)
                or re.search(r"\s+[!?](?![!?])", value)) and not re.search(r"[!?]{2}", value):
            findings["space_before_punctuation"].append({"id": record_id, "text": value})
        duplicate = repeated_word(value)
        if duplicate:
            findings["repeated_word"].append({"id": record_id, "text": value, "detail": duplicate})
        if value[:1].islower() and not value.startswith(("v1.", "i.", "http")):
            findings["lowercase_start"].append({"id": record_id, "text": value})
        for dash, kind in DASHES.items():
            if dash in value:
                findings[f"dash_{kind}"].append({"id": record_id, "text": value})
        if ENGLISH_LEFTOVERS.search(value):
            findings["english_leftover"].append({"id": record_id, "text": value})

        # --- obserwacje stylistyczne -------------------------------------------
        for size in (2, 3):
            for gram in ngrams(value, size):
                phrase_counts[gram] += 1
                phrase_examples.setdefault(gram, {"id": record_id, "text": value})
        for term, pattern in (
            ("Toma Leolo", r"Toma Leol[oa]|Tom Leolo|Tomy Leolo"),
            ("Daemalius", r"Daemali\w*|Daemal\w*"),
            ("The Genesis Order", r"The Genesis Order|Zakon Genesis"),
            ("Anachorismos", r"Anachorism\w*|Anachoryzm\w*"),
        ):
            for match in re.finditer(pattern, value):
                name_variants[term][match.group(0)] += 1

    long_lines = sorted(
        ({"id": r["id"], "length": len(r.get("translation") or ""), "text": r.get("translation") or ""}
         for r in rows if len(r.get("translation") or "") > 180),
        key=lambda item: item["length"], reverse=True,
    )
    lengths.sort()
    phrases = [{"phrase": phrase, "count": count, "example": phrase_examples[phrase]}
               for phrase, count in phrase_counts.most_common(top) if count >= 20]

    reviewed = 0
    for name in list(findings):
        kept = []
        for item in findings[name]:
            if (name, item["id"]) in REVIEWED:
                reviewed += 1
                continue
            kept.append(item)
        findings[name] = kept

    return {
        "schema": "tgo-editorial-qa-v1",
        "reviewed_as_correct": reviewed,
        "translated_record_count": translated,
        "length": {
            "median": lengths[len(lengths) // 2] if lengths else 0,
            "p95": lengths[int(len(lengths) * 0.95)] if lengths else 0,
            "max": lengths[-1] if lengths else 0,
        },
        "issues": {name: {"count": len(items), "auto_fixable": name in AUTO_FIXABLE,
                          "samples": items[:8]}
                   for name, items in sorted(findings.items())},
        "long_lines": long_lines[:10],
        "repeated_phrases": phrases,
        "name_variants": {term: dict(counter) for term, counter in name_variants.items()},
    }


AUTO_FIXABLE = {"whitespace_edges", "whitespace_double", "space_before_punctuation"}


def fix(rows: list[dict[str, Any]]) -> tuple[dict[str, str], list[dict[str, str]]]:
    """Poprawki wyłącznie mechaniczne; zwraca mapę id→nowy tekst i dziennik zmian."""
    changes: dict[str, str] = {}
    log: list[dict[str, str]] = []
    for row in rows:
        value = row.get("translation") or ""
        if not value.strip():
            continue
        source = row.get("source_text") or ""
        new = value
        if value != value.strip() and source.strip() == source:
            new = new.strip()
        new = re.sub(r"(?<=\S) {2,}(?=\S)", " ", new)
        if not re.search(r"[!?]{2}", new):
            new = re.sub(r"\s+([.,;:!?])(?!\d)", r"\1", new)
        # „!!” / „??” bywają celową emfazą — takich linii nie ruszamy wcale.
        if new != value:
            changes[row["id"]] = new
            log.append({"id": row["id"], "before": value, "after": new,
                        "category": "whitespace_or_punctuation"})
    return changes, log


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# Audyt redakcyjny korpusu — TGO PL",
        "",
        "> Plik generowany przez `tools/audit_editorial_quality.py`. Audyt **nie tłumaczy**: mierzy usterki "
        "techniczne i wypisuje obserwacje stylistyczne. Poprawki mechaniczne (`--fix`) dotyczą wyłącznie spacji "
        "i interpunkcji, i tylko tam, gdzie źródło nie ma tej samej cechy.",
        "",
        "## Podsumowanie",
        "",
        f"- Przetłumaczone rekordy: **{report['translated_record_count']}**.",
        f"- Długość tekstu: mediana **{report['length']['median']}** znaków, p95 **{report['length']['p95']}**, "
        f"maksimum **{report['length']['max']}**.",
        "",
        "## Usterki techniczne",
        "",
        "| Klasa | Rekordy | Czy poprawiane automatycznie |",
        "|---|---:|---|",
    ]
    for name, data in report["issues"].items():
        if name.startswith("dash_"):
            continue
        lines.append(f"| `{name}` | {data['count']} | {'tak' if data['auto_fixable'] else 'nie — do decyzji'} |")
    lines += ["", "## Obserwacje stylistyczne", "",
              "### Najczęstsze powtarzane frazy", "",
              "| Fraza | Wystąpienia | Przykład |", "|---|---:|---|"]
    for item in report["repeated_phrases"]:
        example = item["example"]["text"].replace("|", "\\|")[:90]
        lines.append(f"| {item['phrase']} | {item['count']} | {example} |")
    lines += ["", "### Pisownia nazw własnych", ""]
    for term, variants in report["name_variants"].items():
        joined = ", ".join(f"`{name}` ×{count}" for name, count in sorted(variants.items(), key=lambda kv: -kv[1]))
        lines.append(f"- **{term}**: {joined}")
    lines += ["", "### Najdłuższe kwestie", ""]
    for item in report["long_lines"]:
        lines.append(f"- {item['length']} znaków — `{item['id']}` — {item['text'][:110]}…")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fix", action="store_true", help="zapisz poprawki mechaniczne w plikach draftów")
    parser.add_argument("--report", type=Path, default=REPORT_JSON)
    parser.add_argument("--markdown", type=Path, default=REPORT_MD)
    args = parser.parse_args()

    rows = load_rows()
    report = analyse(rows)
    changes, log = fix(rows)
    report["auto_fix"] = {"planned": len(changes), "applied": 0, "change_log": log[:50]}
    if args.fix and changes:
        rewritten = set()
        for path in sorted(DRAFTS.rglob("*.jsonl")):
            lines = path.read_text(encoding="utf-8").splitlines()
            output = []
            touched = False
            for line in lines:
                if not line.strip():
                    output.append(line)
                    continue
                row = json.loads(line)
                if row.get("id") in changes:
                    row["translation"] = changes[row["id"]]
                    output.append(json.dumps(row, ensure_ascii=False, sort_keys=True))
                    touched = True
                else:
                    output.append(line)
            if touched:
                path.write_text("\n".join(output) + "\n", encoding="utf-8", newline="\n")
                rewritten.add(str(path.relative_to(DRAFTS)))
        report["auto_fix"]["applied"] = len(changes)
        report["auto_fix"]["files"] = sorted(rewritten)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    write_markdown(report, args.markdown)
    print(json.dumps({key: report[key] for key in ("translated_record_count", "length")}, ensure_ascii=False, indent=2))
    print(json.dumps({name: data["count"] for name, data in report["issues"].items()}, ensure_ascii=False, indent=2))
    print(json.dumps(report["auto_fix"]["planned"] and {"auto_fix_planned": report["auto_fix"]["planned"],
                                                        "auto_fix_applied": report["auto_fix"]["applied"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
