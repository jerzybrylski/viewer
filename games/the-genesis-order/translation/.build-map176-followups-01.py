#!/usr/bin/env python3
"""Build Polish drafts for Map 176 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map176-followups-01.jsonl'
TRANSLATIONS = {
    "Someone stole my lunch! I think it was one of the officers.": "Ktoś ukradł mój lunch! Myślę, że to jeden z funkcjonariuszy.",
    "Hey, you found my lunch! Here’s a reward.": "Hej, znalazłaś mój lunch! Oto nagroda.",
    "I can use my glue! This should work.": "Mogę użyć kleju! To powinno zadziałać.",
    "I can see a fingerprint on the scanner, but how do I get a copy of it to break into the room?": "Widzę odcisk palca na skanerze, ale jak zdobyć kopię, by włamać się do pokoju?",
    "Find the crazy lady! Get the evidence back!": "Znajdź wariatkę! Odzyskaj dowody!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=176 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=5: raise SystemExit(f'Expected 5, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map176')
