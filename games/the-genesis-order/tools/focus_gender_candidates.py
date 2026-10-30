#!/usr/bin/env python3
"""Wąska kolejka POTENCJALNYCH niezgodności; nigdy nie poprawia tłumaczeń.

Heurystyki wysokiej selektywności są świadomie niepełne. Adresat ze sąsiednich
kwestii jest HIPOTEZĄ, a nie dowodem; skoki, warunki i opętanie mogą ją obalić.
Nie należy interpretować braku sygnału jako poprawności ani stosować zmian hurtowo.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from fix_grammatical_gender import ADJ_PAIRS, NOUN_INSTRUMENTAL, PRESENT_TENSE, gender_of, speaker_of
from prepare_gender_review_batches import compatible_branches, scene_key

WORD = r'[^\W\d_]+'
FIRST = re.compile(r'\b' + WORD + r'(?:łabym|łbym|łam|łem)\b', re.I)
SECOND = re.compile(r'\b' + WORD + r'(?:łabyś|łbyś|łaś|łeś)\b', re.I)
DETACHED_FIRST = re.compile(r'\b(?:gdybym|żebym|abym|bym)\b[^.!?…,;:]{0,65}?\b(' + WORD + r'(?:ła|ł))\b', re.I)
DETACHED_SECOND = re.compile(r'\b(?:gdybyś|żebyś|abyś|byś)\b[^.!?…,;:]{0,65}?\b(' + WORD + r'(?:ła|ł))\b', re.I)
WINIEN = re.compile(r'\b(winien|winna)\b', re.I)
SELF_PREFIX = re.compile(r'^\s*(sam|sama)\b', re.I)
# Krótka, jawna lista par wyłącznie do sygnalizowania, bez zamian w tłumaczeniu.
PAIRS = {m: f for m, f in ADJ_PAIRS.items() if not m.endswith('a') and f.endswith('a')
         and m not in {'sam', 'taki', 'twój', 'mój', 'swój', 'cały', 'jeden'}}
PAIRS.update({'skłonny': 'skłonna', 'daleki': 'daleka', 'zaangażowany': 'zaangażowana',
              'bogaty': 'bogata', 'ukarany': 'ukarana'})
MASC = set(PAIRS)
FEM = set(PAIRS.values())
FRAME = re.compile(r'\b(jestem|byłem|byłam|będę|czuję się|jesteś|byłeś|byłaś|będziesz|czujesz się)\b', re.I)
TOKENS = re.compile(WORD, re.I)
BREAK = re.compile(r'[.!?…,:;]')


def verb_gender(word: str) -> str | None:
    word = word.lower()
    if word.endswith(('łabym', 'łam', 'łabyś', 'łaś', 'ła')):
        return 'F'
    if word.endswith(('łbym', 'łem', 'łbyś', 'łeś', 'ł')):
        return 'M'
    return None


def incompatible_form(matches, expected: str) -> list[str]:
    return [m.group(0) for m in matches if m.group(0).lower() not in NOUN_INSTRUMENTAL | PRESENT_TENSE
            and verb_gender(m.group(0)) not in (None, expected)]


def opposite_detached(pattern, text: str, expected: str) -> list[str]:
    return [m.group(1) for m in pattern.finditer(text) if verb_gender(m.group(1)) not in (None, expected)]


def predicate_mismatches(text: str, speaker_gender: str | None, target_gender: str | None) -> list[dict]:
    findings = []
    for m in FRAME.finditer(text):
        frame = m.group(1).lower()
        expected = target_gender if frame in {'jesteś', 'byłeś', 'byłaś', 'będziesz', 'czujesz się'} else speaker_gender
        if not expected:
            continue
        tail = BREAK.split(text[m.end():], maxsplit=1)[0]
        for token in TOKENS.findall(tail)[:5]:
            word = token.lower()
            actual = 'M' if word in MASC and word not in FEM else 'F' if word in FEM and word not in MASC else None
            if actual and actual != expected:
                findings.append({'kind': 'orzecznik', 'frame': frame, 'form': token, 'expected_gender_hint': expected})
                break
    return findings


def neighboring_speakers(rows: list[dict], index: int, window: int = 5) -> tuple[str | None, list[str]]:
    """Wskazówka: najbliższy inny mówca; sprzeczne strony nie są rozstrzygane."""
    row = rows[index]
    name = speaker_of(row)
    if not name:
        return None, []
    sides = []
    for candidates in (reversed(rows[max(0, index-window):index]), rows[index+1:index+1+window]):
        for other in candidates:
            if not compatible_branches(row, other):
                continue
            candidate = speaker_of(other)
            if candidate and candidate != name and gender_of(candidate):
                sides.append((candidate, other['id']))
                break
    if not sides or len({x[0] for x in sides}) != 1:
        return None, [item[1] for item in sides]
    return sides[0][0], [item[1] for item in sides]


def evidence(row: dict, addressee: str | None = None, related_ids: list[str] | None = None) -> list[dict]:
    text = row.get('translation') or ''
    speaker = speaker_of(row)
    speaker_gender = gender_of(speaker)
    target_gender = gender_of(addressee)
    results = []
    if speaker_gender:
        forms = incompatible_form(FIRST.finditer(text), speaker_gender)
        forms += opposite_detached(DETACHED_FIRST, text, speaker_gender)
        for match in re.finditer(r'\b(?:powinienem|powinnam)\b', text, re.I):
            if ('F' if match.group(0).lower() == 'powinnam' else 'M') != speaker_gender:
                forms.append(match.group(0))
        if forms:
            results.append({'kind': 'pierwsza_osoba', 'forms': forms, 'speaker_hint': speaker,
                            'expected_gender_hint': speaker_gender})
        m = SELF_PREFIX.search(text)
        if (m and not SECOND.search(text) and
                (('F' if m.group(1).lower() == 'sama' else 'M') != speaker_gender)):
            results.append({'kind': 'sam_sama', 'forms': [m.group(1)], 'speaker_hint': speaker,
                            'expected_gender_hint': speaker_gender})
    if target_gender:
        forms = incompatible_form(SECOND.finditer(text), target_gender)
        forms += opposite_detached(DETACHED_SECOND, text, target_gender)
        for match in WINIEN.finditer(text):
            before = re.split(r'[.!?…;]', text[:match.start()])[-1]
            if re.search(r'\b(?:jestem|czuję\s+się)\b', before, re.I):
                continue  # pierwsza osoba, nie adresat
            if ('F' if match.group(1).lower() == 'winna' else 'M') != target_gender:
                forms.append(match.group(1))
        if forms:
            results.append({'kind': 'adresat_z_sasiedztwa', 'forms': forms, 'addressee_hypothesis': addressee,
                            'expected_gender_hint': target_gender, 'related_ids': related_ids or []})
    for item in predicate_mismatches(text, speaker_gender, target_gender):
        item['speaker_hint'] = speaker
        item['addressee_hypothesis'] = addressee
        item['related_ids'] = related_ids or []
        results.append(item)
    return results


def focus(rows: list[dict]) -> tuple[list[dict], dict]:
    scenes = defaultdict(list)
    for row in rows:
        key = scene_key(row)
        if key is not None:
            scenes[key].append(row)
    scene_index = {}
    for key, group in scenes.items():
        group.sort(key=lambda r: ((r.get('context') or {}).get('command_index')
                                  if isinstance((r.get('context') or {}).get('command_index'), int) else -1, r['id']))
        for i, row in enumerate(group):
            scene_index[row['id']] = (key, i)
    results = []
    for row in rows:
        if row.get('review_status') not in {'unreviewed', 'stale', 'deferred'}:
            continue
        scene = scene_index.get(row['id'])
        target, related = neighboring_speakers(scenes[scene[0]], scene[1]) if scene else (None, [])
        matches = evidence(row, target, related)
        if matches:
            results.append({'id': row['id'], 'source_text': row.get('source_text'),
                            'translation': row.get('translation'), 'context': row.get('context'),
                            'review_status': row.get('review_status'), 'evidence': matches,
                            'warning': 'Hipoteza, nie dowód. Sprawdź faktycznego mówcę, adresata i gałąź.'})
    results.sort(key=lambda x: (-len(x['evidence']), x['id']))
    counts = Counter(item['kind'] for row in results for item in row['evidence'])
    return results, {'candidates': len(results), 'evidence_counts_overlapping': dict(sorted(counts.items())),
                     'warning': 'Wąskie sito jest niepełne. Brak trafienia nie oznacza poprawności.'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Odmowa nadpisania pliku wyjściowego')
    with args.input.open(encoding='utf8') as f:
        rows = [json.loads(line) for line in f if line.strip()]
    if len({r['id'] for r in rows}) != len(rows):
        raise ValueError('Powtórzone ID')
    candidates, summary = focus(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf8', newline='\n') as f:
        for row in candidates:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
