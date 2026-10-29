#!/usr/bin/env python3
"""Build contextual LLM drafts for the Map 46 crafting prompts."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
TOOLS = ROOT.parent / 'tools'
sys.path.insert(0, str(TOOLS))
from apply_translation import validate_record  # noqa: E402

CANON = ROOT / 'export-v1/native_message.jsonl'
DRAFTS = ROOT / 'drafts'
OUTPUT = DRAFTS / 'native-message-map46-crafting-01.jsonl'

# LLM translations for the repeated Map 46 crafting prompts, reviewed in the shared crafting UI context.
TRANSLATIONS = {
    r'\fs[22]<br> <br>\fs[25]\fn<Josefin Sans SemiBold>\fbCraft this item?':
        r'\fs[22]<br> <br>\fs[25]\fn<Josefin Sans SemiBold>\fbWytworzyć ten przedmiot?',
    r'\fs[22]<br> <br>\fs[25]\fn<Josefin Sans SemiBold>\fbYou have items missing from this recipe.':
        r'\fs[22]<br> <br>\fs[25]\fn<Josefin Sans SemiBold>\fbBrakuje ci przedmiotów potrzebnych do tego przepisu.',
}

# Strip renderer-only tokens before checking that a source contains actual words.
RENDERER_TOKEN = re.compile(r'\\[A-Za-z]+(?:\[[^\]]*\])?|<[^>]*>')

def main() -> None:
    known: set[str] = set()
    for path in DRAFTS.rglob('*.jsonl'):
        for line in path.read_text(encoding='utf-8').splitlines():
            if line.strip():
                row = json.loads(line)
                if isinstance(row.get('translation'), str) and row['translation'].strip():
                    known.add(row['id'])

    rows: list[dict] = []
    unmapped: list[str] = []
    for line in CANON.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        source = row.get('source_text', '')
        context = row.get('context') or {}
        display_source = RENDERER_TOKEN.sub('', source).strip()
        if (
            row['id'] in known
            or row.get('category') != 'native_message'
            or context.get('map_id') != 46
            or context.get('translation_policy') == 'keep_source_value'
            or source not in TRANSLATIONS
            or not source.strip()
            or source.lstrip().startswith('/')
            or not any(char.isalpha() for char in display_source)
        ):
            continue
        translated = TRANSLATIONS.get(source)
        if translated is None:
            unmapped.append(row['id'] + ': ' + repr(source))
            continue
        row['translation'] = translated
        rows.append(row)

    if unmapped:
        raise SystemExit('Unmapped player-facing source strings:\n' + '\n'.join(unmapped))
    if OUTPUT.exists():
        raise SystemExit(f'Refusing to overwrite existing draft: {OUTPUT}')
    if len(rows) != 94:
        raise SystemExit(f'Expected exactly 94 records, got {len(rows)}')
    if len({row['id'] for row in rows}) != len(rows):
        raise SystemExit('Duplicate stable IDs in batch')
    for row in rows:
        validate_record(row, require_complete=True)

    OUTPUT.write_text(
        ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
        encoding='utf-8',
        newline='\n',
    )
    event_count = len({(row.get('context') or {}).get('event_id') for row in rows})
    print(f'Wrote {len(rows)} translated crafting UI records from Map 46 across {event_count} events.')

if __name__ == '__main__':
    main()
