#!/usr/bin/env python3
"""Inwentarz do ręcznego audytu rodzaju. Nie ocenia poprawności i nie edytuje tekstu.

Obejmuje wszystkie niepuste tłumaczenia z walidowanego scalenia. Heurystyki
służą wyłącznie do kolejności przeglądu, nie jako dowód braku błędów. Wynik
zawiera kontekst z eksportu, lecz sąsiedztwo nie dowodzi adresata ani gałęzi.
"""
from __future__ import annotations

import argparse
import json
import re
import tempfile
from collections import Counter
from pathlib import Path

from merge_translation_batches import merge_batches

ROOT = Path(__file__).resolve().parents[1]
TRANS = ROOT / 'translation'
WORD = r'[^\W\d_]+'
PATTERNS = {
    'conditional_1': re.compile(r'\b(?:gdybym|żebym|abym|bym)\b', re.I),
    'conditional_2': re.compile(r'\b(?:gdybyś|żebyś|abyś|byś)\b', re.I),
    'first_person': re.compile(r'\b' + WORD + r'(?:łem|łam|łbym|łabym)\b', re.I),
    'second_person': re.compile(r'\b' + WORD + r'(?:łeś|łaś|łbyś|łabyś)\b', re.I),
    'predicate': re.compile(r'\b(?:jestem|jesteś|byłem|byłam|byłeś|byłaś|będę|będziesz|czuję się|czujesz się)\b', re.I),
    'third_or_detached': re.compile(r'\b' + WORD + r'(?:ł|ła|ło|li|ły)\b', re.I),
    'pronoun': re.compile(r'\b(?:sam|sama|sami|same|on|ona|oni|one)\b', re.I),
}


def tags(text: str) -> list[str]:
    return [name for name, regex in PATTERNS.items() if regex.search(text)]


def inventory(rows: list[dict], old_changes: set[str]) -> tuple[list[dict], dict]:
    out = []
    counts: Counter[str] = Counter()
    for row in rows:
        value = row.get('translation', '')
        if not value.strip():
            continue
        found = tags(value)
        counts.update(found)
        ctx = row.get('context') or {}
        out.append({'id': row['id'], 'category': row.get('category'),
                    'source_text': row.get('source_text'), 'translation': value,
                    'context': ctx, 'flags': found,
                    'previous_automatic_edit': row['id'] in old_changes,
                    # Stan jest jawny: heurystyka nigdy nie potwierdza poprawności.
                    'review_status': 'unreviewed'})
    def order(row: dict) -> tuple:
        c = row['context']
        return (str(c.get('source_kind') or ''), str(c.get('map_id') or '').zfill(4),
                str(c.get('event_id') or '').zfill(4), str(c.get('page_number') or '').zfill(4),
                c.get('command_index') if isinstance(c.get('command_index'), int) else -1, row['id'])
    out.sort(key=order)
    summary = {'translated_records': len(out), 'unreviewed_records': len(out),
               'flagged_records': sum(bool(r['flags']) for r in out),
               'unflagged_not_reviewed': sum(not r['flags'] for r in out),
               'previous_automatic_edits_in_inventory': sum(r['previous_automatic_edit'] for r in out),
               'flag_counts_overlapping': dict(sorted(counts.items())),
               'warning': 'Flagi to tylko heurystyki; brak flagi nie oznacza poprawności.'}
    return out, summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='Nowy plik JSONL; bez nadpisywania')
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    with tempfile.TemporaryDirectory(prefix='.gender-inventory-', dir=TRANS) as tmp:
        merged = Path(tmp) / 'merged.jsonl'
        report = merge_batches(TRANS / 'export-v1', sorted((TRANS / 'drafts').rglob('*.jsonl')), merged, TRANS)
        rows = [json.loads(line) for line in merged.read_text(encoding='utf8').splitlines() if line.strip()]
    previous = json.loads((TRANS / 'reports/gender_fix_v1.json').read_text(encoding='utf8'))
    output, summary = inventory(rows, {item['id'] for item in previous['change_log']})
    if summary['translated_records'] != report['with_translation']:
        raise ValueError('Liczba tłumaczeń w kolejce nie odpowiada scaleniu')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf8', newline='\n') as stream:
        for row in output:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
