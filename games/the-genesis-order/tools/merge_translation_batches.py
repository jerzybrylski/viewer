#!/usr/bin/env python3
"""Merge partial TGO drafts into the full canonical export, without changing it.

Only translation may differ from the canonical row. The output must be a new
file under the tracked TGO translation workspace or ignored google_drive/.
No game sources are read or executed.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from apply_translation import validate_record
from markdown_translation import DEFAULT_INPUT, REPO_ROOT, input_paths, read_jsonl


def merge_batches(canonical: Path, batches: list[Path], out: Path,
                  private_root: Path = REPO_ROOT / 'google_drive') -> dict[str, Any]:
    root, out = private_root.resolve(), out.resolve()
    tracked = (REPO_ROOT / 'games/the-genesis-order/translation').resolve()
    canonical_root = (tracked / 'export-v1').resolve()
    if root not in out.parents and tracked not in out.parents:
        raise ValueError('Output must be under the translation workspace or ignored google_drive/')
    if out == canonical_root or canonical_root in out.parents:
        raise ValueError('Refusing to modify the canonical source export')
    rows = read_jsonl(input_paths(canonical))
    by_id = {row['id']: row for row in rows}
    for row in rows:
        validate_record(row, False)
        if row['translation'].strip():
            raise ValueError('Canonical input must be a blank source export')
    seen: dict[str, str] = {}
    for batch in batches:
        for path in input_paths(batch):
            with path.open(encoding='utf-8') as stream:
                for lineno, line in enumerate(stream, 1):
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    if not isinstance(row, dict) or not isinstance(row.get('id'), str):
                        raise ValueError(f'Invalid row at {path}:{lineno}')
                    source = by_id.get(row['id'])
                    if source is None:
                        raise ValueError(f"Unknown ID: {row['id']}")
                    if {k: v for k, v in row.items() if k != 'translation'} != {
                        k: v for k, v in source.items() if k != 'translation'
                    }:
                        raise ValueError(f"Canonical metadata changed: {row['id']}")
                    value = validate_record(row, False)
                    if value is None:
                        continue
                    if row['id'] in seen and seen[row['id']] != value:
                        raise ValueError(f"Conflicting translations: {row['id']}")
                    seen[row['id']] = value
    for row in rows:
        if row['id'] in seen:
            row['translation'] = seen[row['id']]
    out.parent.mkdir(parents=True, exist_ok=True)
    # exclusive creation: never silently overwrite a prior draft
    with out.open('x', encoding='utf-8', newline='\n') as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    protected = sum((r.get('context') or {}).get('translation_policy') == 'keep_source_value' for r in rows)
    pending = sum(not r['translation'].strip() and
                  (r.get('context') or {}).get('translation_policy') != 'keep_source_value' for r in rows)
    return {'records': len(rows), 'with_translation': len(seen),
            'protected': protected, 'pending_translatable': pending, 'output': str(out)}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--canonical', type=Path, default=DEFAULT_INPUT)
    p.add_argument('--batch', type=Path, action='append', required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(merge_batches(args.canonical, args.batch, args.out), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
