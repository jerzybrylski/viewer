#!/usr/bin/env python3
"""Build Polish drafts for Map 169 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map169-followups-01.jsonl'
TRANSLATIONS = {
    "What the hell are you doing back here? Unless you can fix a busted kitchen, get out!": "Co ty tu znowu robisz? Chyba że naprawisz zepsutą kuchnię, wynoś się!",
    "This sink is clogged. I need something to pull the water out, cause it isn’t going to drain.": "Zlew zapchany. Potrzebuję czegoś, by wyciągnąć wodę, bo nie spłynie.",
    "I can use my siphon to drain the sink.": "Mogę użyć syfonu, by opróżnić zlew.",
    "Hey! You fixed my kitchen. Nice job.": "Hej! Naprawiłaś kuchnię. Dobra robota.",
    "I’m on break. If you want food, cook it yourself.": "Mam przerwę. Chcesz jedzenie, ugotuj sobie sam.",
    "I can see something above the vent. I wonder if I could throw something at it and knock it down.": "Widzę coś nad kratką. Ciekawe, czy mogłabym w to czymś rzucić i strącić.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=169 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=6: raise SystemExit(f'Expected 6, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map169')
