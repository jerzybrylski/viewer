#!/usr/bin/env python3
"""Przygotuj partie do KONTEKSTOWEGO przeglądu rodzaju; nigdy nie zmieniaj tekstu.

Wejście: JSONL z inventory_gender_review.py. Grupowanie identycznego tekstu i
nagłówka to oszczędność przeglądu, NIE dowód wspólnego mówcy/adresata. Każde
wystąpienie zachowuje osobny ID, warunki i sąsiedztwo. Wynik jest kolejką
kandydatów, nie raportem błędów ani poświadczeniem jakości pozostałego tekstu.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from fix_grammatical_gender import NOUN_INSTRUMENTAL, gender_of, speaker_of

WORD = r'[^\W\d_]+'
FIRST_M = re.compile(r'\b' + WORD + r'(?:łem|łbym)\b', re.I)
FIRST_F = re.compile(r'\b' + WORD + r'(?:łam|łabym)\b', re.I)
DETACHED_1 = re.compile(r'\b(?:gdybym|żebym|abym|bym)\b[^.!?…]{0,80}?\b' + WORD + r'(?:ła|ł)\b', re.I)
DETACHED_2 = re.compile(r'\b(?:gdybyś|żebyś|abyś|byś)\b[^.!?…]{0,80}?\b' + WORD + r'(?:ła|ł)\b', re.I)
SELF = re.compile(r'\b(?:sam|sama)\b', re.I)
PREDICATE = re.compile(r'\b(?:jestem|jesteś|byłem|byłam|byłeś|byłaś|będę|będziesz|czuję się|czujesz się)\b', re.I)
WINIEN = re.compile(r'\b(?:winien|winna)\b', re.I)
PLURAL = re.compile(r'\b(?:' + WORD + r'(?:liśmy|łyśmy|liście|łyście)|wszyscy|wszystkie|jesteśmy)\b', re.I)
ADJECTIVE = re.compile(r'\b' + WORD + r'(?:any|ana|ony|ona|ony|ona|owy|owa|ny|na)\b', re.I)
IDIOT = re.compile(r'\b(?:idiota|idiotka|idiotą|idiotkę|idiotę)\b', re.I)


def scene_key(row: dict) -> tuple | None:
    c = row.get('context') or {}
    kind = c.get('source_kind')
    if kind == 'map' and all(c.get(k) is not None for k in ('map_id', 'event_id', 'page_number')):
        return ('map', c['map_id'], c['event_id'], c['page_number'])
    if kind == 'common_event' and c.get('event_id') is not None:
        return ('common_event', c['event_id'])
    return None  # nie łączyć nieznanych lokatorów w fikcyjną scenę


def branch_constraints(row: dict) -> dict[tuple, Any]:
    """Tylko jawne alternatywy tej samej instrukcji są sprzeczne."""
    c = row.get('context') or {}
    constraints = {}
    for part in c.get('branch_path') or []:
        if not isinstance(part, dict):
            continue
        if part.get('kind') == 'choice_branch' and part.get('choice_group_id') is not None:
            constraints[('choice', part['choice_group_id'])] = part.get('option_index')
        elif part.get('kind') == 'condition' and part.get('command_index') is not None:
            constraints[('condition', part['command_index'])] = part.get('arm')
    return constraints


def compatible_branches(a: dict, b: dict) -> bool:
    left, right = branch_constraints(a), branch_constraints(b)
    return all(left[k] == right[k] for k in left.keys() & right.keys())


def signals(row: dict) -> list[str]:
    text = row.get('translation') or ''
    name = speaker_of(row)
    gender = gender_of(name)
    found = []
    wrong_pattern = FIRST_F if gender == 'M' else FIRST_M if gender == 'F' else None
    if wrong_pattern and any(m.group().lower() not in NOUN_INSTRUMENTAL for m in wrong_pattern.finditer(text)):
        found.append('mozliwa_niezgodnosc_pierwszej_osoby')
    if DETACHED_1.search(text):
        found.append('rozdzielny_tryb_pierwszej_osoby')
    if DETACHED_2.search(text):
        found.append('rozdzielny_tryb_adresata')
    if SELF.search(text):
        found.append('sam_sama_podmiot_do_ustalenia')
    if PREDICATE.search(text):
        found.append('orzecznik_do_przegladu')
    if WINIEN.search(text):
        found.append('winien_winna_podmiot_do_ustalenia')
    if PLURAL.search(text):
        found.append('rodzaj_liczby_mnogiej')
    if ADJECTIVE.search(text) or IDIOT.search(text):
        found.append('mozliwy_przymiotnik_lub_rzeczownik')
    if any(flag in {'first_person', 'second_person', 'third_or_detached', 'pronoun'}
           for flag in row.get('flags', [])):
        found.append('inna_forma_rodzajowa')
    if row.get('previous_automatic_edit'):
        found.append('wczesniejsza_automatyczna_zmiana')
    c = row.get('context') or {}
    if c.get('source_kind') == 'common_event' and c.get('event_id') in {454, 456} and name == 'Erica':
        found.append('znane_opetanie_tozsamosc_mowcy')
    return found


WEIGHTS = {
    'mozliwa_niezgodnosc_pierwszej_osoby': 8,
    'rozdzielny_tryb_pierwszej_osoby': 5,
    'rozdzielny_tryb_adresata': 5,
    'sam_sama_podmiot_do_ustalenia': 3,
    'orzecznik_do_przegladu': 2,
    'winien_winna_podmiot_do_ustalenia': 4,
    'rodzaj_liczby_mnogiej': 2,
    'mozliwy_przymiotnik_lub_rzeczownik': 1,
    'inna_forma_rodzajowa': 1,
    'wczesniejsza_automatyczna_zmiana': 4,
    'znane_opetanie_tozsamosc_mowcy': 8,
}


def build_batches(rows: list[dict], context_count: int = 2) -> tuple[list[dict], dict]:
    if context_count < 0:
        raise ValueError('context_count must be nonnegative')
    scene_rows: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = scene_key(row)
        if key is not None:
            scene_rows[key].append(row)
    indices = {}
    for key, group in scene_rows.items():
        group.sort(key=lambda r: ((r.get('context') or {}).get('command_index')
                                  if isinstance((r.get('context') or {}).get('command_index'), int) else -1,
                                  r['id']))
        for i, row in enumerate(group):
            indices[row['id']] = (key, i)

    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        if row.get('review_status') not in {'unreviewed', 'stale', 'deferred'}:
            continue
        found = signals(row)
        if not found:
            continue
        c = row.get('context') or {}
        # Dokładna treść źródła i przekładu plus nagłówek; wciąż osobna decyzja na ID.
        key = (row.get('category'), row.get('source_text'), row.get('translation'), c.get('custom_header'))
        grouped[key].append(row)

    batches = []
    for members in grouped.values():
        found = sorted({s for row in members for s in signals(row)})
        occurrences = []
        for row in members:
            loc = indices.get(row['id'])
            neighbors = []
            if loc:
                key, index = loc
                group = scene_rows[key]
                before = [r for r in group[:index] if compatible_branches(row, r)][-context_count:] if context_count else []
                after = [r for r in group[index + 1:] if compatible_branches(row, r)][:context_count]
                for other in before + after:
                    neighbors.append({'id': other['id'], 'source_text': other.get('source_text'),
                                      'translation': other.get('translation'),
                                      'context': other.get('context'), 'speaker_hint': speaker_of(other)})
            snapshot = {'id': row['id'], 'source_text': row.get('source_text'),
                        'translation': row.get('translation'), 'context': row.get('context'),
                        'neighbors': neighbors}
            snapshot_bytes = json.dumps(snapshot, ensure_ascii=False, sort_keys=True,
                                        separators=(',', ':')).encode('utf8')
            occurrences.append({'id': row['id'], 'review_status': row.get('review_status'),
                                'context': row.get('context'), 'neighbors': neighbors,
                                'context_snapshot_sha256': hashlib.sha256(snapshot_bytes).hexdigest()})
        occurrences.sort(key=lambda x: x['id'])
        head = members[0]
        batches.append({'source_text': head.get('source_text'), 'translation': head.get('translation'),
                        'category': head.get('category'), 'speaker_hint': speaker_of(head),
                        'speaker_hint_warning': 'Nagłówek może oznaczać ciało, nie tożsamość mówiącego.',
                        'signals': found, 'priority': sum(WEIGHTS[s] for s in found),
                        'occurrences': occurrences})
    batches.sort(key=lambda b: (-b['priority'], -len(b['occurrences']), b['occurrences'][0]['id']))
    eligible = [r for r in rows if r.get('review_status') in {'unreviewed', 'stale', 'deferred'}]
    summary = {'eligible_records': len(eligible), 'candidate_records': sum(len(b['occurrences']) for b in batches),
               'candidate_groups': len(batches), 'unflagged_eligible_records': len(eligible) - sum(len(b['occurrences']) for b in batches),
               'signal_counts_overlapping': dict(sorted(Counter(s for r in eligible for s in signals(r)).items())),
               'warning': 'Kandydaci to nie błędy; brak sygnału nie jest przeglądem. Decyzja osobno dla każdego ID i gałęzi.'}
    return batches, summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--max-groups', type=int, default=100, help='Maksymalna liczba grup w pliku')
    parser.add_argument('--offset', type=int, default=0, help='Pomiń tyle grup w bieżącym inwentarzu')
    parser.add_argument('--context', type=int, default=2, help='Liczba sąsiednich rekordów z każdej strony')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Odmowa nadpisania pliku wyjściowego')
    if args.max_groups <= 0 or args.context < 0 or args.offset < 0:
        parser.error('Limit musi być dodatni, a offset i kontekst nieujemne')
    with args.input.open(encoding='utf8') as stream:
        rows = [json.loads(line) for line in stream if line.strip()]
    ids = [r['id'] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError('Powtórzone ID w inwentarzu')
    batches, summary = build_batches(rows, args.context)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    selected = batches[args.offset:args.offset + args.max_groups]
    with args.output.open('x', encoding='utf8', newline='\n') as stream:
        for batch in selected:
            stream.write(json.dumps(batch, ensure_ascii=False, sort_keys=True) + '\n')
    summary['offset'] = args.offset
    summary['written_groups'] = len(selected)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
