#!/usr/bin/env python3
"""Build Polish drafts for Map 155 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map155-followups-01.jsonl'
TRANSLATIONS = {
    "I saw this… This place opens the rift.": "Widziałam to… To miejsce otwiera szczelinę.",
    "I don’t know… I only saw a glance. But there were three objects on these altars.": "Nie wiem… Zerknęłam tylko. Ale na ołtarzach były trzy przedmioty.",
    "A black feather, a long sharp tooth, and a horn.": "Czarne pióro, długi ostry kieł i róg.",
    "Sounds like demon parts.": "Brzmi jak części demona.",
    "What happens now? Is the rift open?": "Co teraz? Czy szczelina jest otwarta?",
    "Let’s go find out.": "Chodźmy sprawdzić.",
    "The demon pieces are gone. I wonder where they went.": "Kawałki demona zniknęły. Ciekawe, gdzie trafiły.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=155 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=7: raise SystemExit(f'Expected 7, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map155')
