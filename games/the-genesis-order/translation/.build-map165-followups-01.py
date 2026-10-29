#!/usr/bin/env python3
"""Build Polish drafts for Map 165 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map165-followups-01.jsonl'
TRANSLATIONS = {
    "Don’t tell anyone I’m in here. I’m homeless and these clothes can’t keep me warm…": "Nikomu nie mów, że tu jestem. Jestem bezdomny i te ubrania nie grzeją…",
    "Do you have anything to help me out, man?": "Masz coś, by mi pomóc, stary?",
    "I can’t give that away! I need it… at least for now.": "Nie mogę tego oddać! Potrzebuję tego… przynajmniej na razie.",
    "Not sure if that would be useful for me.": "Nie wiem, czy to by mi się przydało.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=165 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=4: raise SystemExit(f'Expected 4, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map165')
