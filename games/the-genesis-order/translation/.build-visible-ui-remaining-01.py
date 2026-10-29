#!/usr/bin/env python3
"""Build a contextual LLM draft for the last reviewed visible UI strings."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'tools'))
from apply_translation import validate_record  # noqa: E402

DRAFTS = ROOT / 'drafts'
OUTPUT = DRAFTS / 'visible-ui-remaining-01.jsonl'

# These are authored in context: repeated placeholder text in the explicitly
# player-rendered TEST MAP messages, plus a split phone conversation line.
TRANSLATIONS = {
    ('native_message', 'Text goes here<br>Text goes here<br>Text goes here<br>'):
        'Tekst w tym miejscu<br>Tekst w tym miejscu<br>Tekst w tym miejscu<br>',
    ('phone_contact_ui', 'He’s going to be<br>'):
        'Będzie<br>',
    ('phone_text', 'TEXT'):
        'TEKST',
}
EXPECTED_COUNT = 9


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f'Refusing to overwrite existing draft: {OUTPUT}')

    already_translated: set[str] = set()
    for path in DRAFTS.rglob('*.jsonl'):
        for line in path.read_text(encoding='utf-8').splitlines():
            if line.strip():
                row = json.loads(line)
                if isinstance(row.get('translation'), str) and row['translation'].strip():
                    already_translated.add(row['id'])

    rows: list[dict] = []
    for path in (ROOT / 'export-v1').glob('*.jsonl'):
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            key = (row.get('category'), row.get('source_text'))
            if key not in TRANSLATIONS:
                continue
            if row['id'] in already_translated:
                continue
            context = row.get('context') or {}
            if context.get('translation_policy') == 'keep_source_value':
                raise SystemExit(f"Refusing protected source: {row['id']}")
            # Restrict these translations to the reviewed source contexts.
            if key[0] == 'native_message' and (
                context.get('map_id') != 2 or context.get('map_name') != 'TEST MAP'
            ):
                raise SystemExit(f"Unexpected native-message context: {row['id']}")
            if key[0] == 'phone_contact_ui' and not (
                context.get('event_id') == 17 and context.get('event_name') == 'PHONE - Select Item'
            ):
                raise SystemExit(f"Unexpected phone UI context: {row['id']}")
            if key[0] == 'phone_text' and not (
                context.get('map_id') == 2
                and context.get('map_name') == 'TEST MAP'
                and row.get('structure', {}).get('routed_common_event_id') == 53
                and row.get('structure', {}).get('variable_id') == 25
            ):
                raise SystemExit(f"Unexpected phone-text context: {row['id']}")
            row['translation'] = TRANSLATIONS[key]
            validate_record(row, require_complete=True)
            rows.append(row)

    if len(rows) != EXPECTED_COUNT:
        raise SystemExit(f'Expected exactly {EXPECTED_COUNT} records, got {len(rows)}')
    if len({row['id'] for row in rows}) != len(rows):
        raise SystemExit('Duplicate stable IDs in batch')

    OUTPUT.write_text(
        ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
        encoding='utf-8',
        newline='\n',
    )
    print(f'Wrote {len(rows)} contextual visible UI translations.')


if __name__ == '__main__':
    main()
