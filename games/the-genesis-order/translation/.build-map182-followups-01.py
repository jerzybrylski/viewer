#!/usr/bin/env python3
"""Build Polish drafts for Map 182 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map182-followups-01.jsonl'
TRANSLATIONS = {
    "tgo:custom_dialogue:33c0de35fe9c36169df9": "Wygląda jak generator wysokiego napięcia… Ale brakuje w nim części.",
    "tgo:custom_dialogue:91a2dc903a0e02d41ca2": "Potrzebuje koła pasowego i paliwa do generatora.",
    "tgo:custom_dialogue:d34e372e2b588c319d7d": "Mogę użyć koła silnika, by naprawić generator.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=182 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(r['id'])
    if tr is None: unmapped.add((ctx.get('event_id'), r['id'], src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=3: raise SystemExit(f'Expected 3, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map182')
