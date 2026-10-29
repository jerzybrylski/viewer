#!/usr/bin/env python3
"""Build Polish drafts for Map 258 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map258-followups-01.jsonl'
TRANSLATIONS = {
    "tgo:custom_dialogue:432523ccdf57592bba61": "Co za widok!",
    "tgo:custom_dialogue:fe2d6e8bed1f73656eae": "To zdjęcie powinno zadowolić sędziego.",
}
known=set()
for p in (ROOT/'drafts').rglob('*.jsonl'):
    for line in p.read_text(encoding='utf-8').splitlines():
        if line.strip():
            r=json.loads(line)
            if r.get('translation','').strip(): known.add(r['id'])
rows=[]
unmapped=set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    r=json.loads(line)
    ctx=r.get('context') or {}
    src=' '.join(r.get('source_text','').strip().split())
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=258 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(r['id'])
    if tr is None: unmapped.add((ctx.get('event_id'), r['id'], src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=2: raise SystemExit(f'Expected 2, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map258')
