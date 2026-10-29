#!/usr/bin/env python3
"""Build Polish drafts for Map 199 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map199-followups-01.jsonl'
TRANSLATIONS = {
    "tgo:custom_dialogue:272ae8c6a455cf50cc48": "Judy? Jesteś wcześniej.",
    "tgo:custom_dialogue:f8d0c554e7d8c4714d5c": "Nie mogłam się doczekać. Tak bardzo chciałam cię zobaczyć.",
    "tgo:custom_dialogue:34f20e9ba6de00d8978d": "Haha… Och, Siostro. Nie możesz być długo z dala, co?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=199 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(r['id'])
    if tr is None: unmapped.add((ctx.get('event_id'), r['id'], src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=3: raise SystemExit(f'Expected 3, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map199')
