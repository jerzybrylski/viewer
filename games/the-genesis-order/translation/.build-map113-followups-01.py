#!/usr/bin/env python3
"""Build Polish drafts for Map 113 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map113-followups-01.jsonl'
TRANSLATIONS = {
    "I can use my wrench to tighten loose valve.": "Mogę użyć klucza, by dokręcić poluzowany zawór.",
    "Looks like the sink is clogged. I wonder if something is stopping it up.": "Wygląda, że zlew jest zapchany. Ciekawe, co go blokuje.",
    "I need a hacksaw.": "Potrzebuję piły do metalu.",
    "I need a blow torch.": "Potrzebuję palnika.",
    "I need a wrench.": "Potrzebuję klucza.",
    "I can use my tools to open the pipe and take a look.": "Mogę użyć narzędzi, by otworzyć rurę i zajrzeć.",
    "Huh. That’s odd. It looks like a key was stuck in the pipe.": "Huh. Dziwne. Wygląda, że klucz utknął w rurze.",
    "Want to hop in?": "Chcesz wskoczyć?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=113 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=8: raise SystemExit(f'Expected 8, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map113')
