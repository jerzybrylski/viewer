#!/usr/bin/env python3
"""Build Polish drafts for Map 29 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map29-followups-01.jsonl'
TRANSLATIONS = {
    "I finally own a nice suit. This might come in handy one day.": "Wreszcie mam ładny garnitur. Może się kiedyś przyda.",
    "Father Solomon? What are you doing here?": "Ojciec Solomon? Co tu robisz?",
    "Just doing some shopping.": "Tylko zakupy.",
    "Who’s watching the church?": "Kto pilnuje kościoła?",
    "It’s just Sister Judy there right now. Hopefully she can keep visitors from wandering the place.": "Teraz jest tam tylko siostra Judy. Mam nadzieję, że powstrzyma gości przed włóczeniem się.",
    "Are you getting more visitors?": "Masz więcej gości?",
    "No. I was being sarcastic.": "Nie. Byłem sarkastyczny.",
    "That’s odd. It doesn’t seem like they sell aloe lotion. I wonder if I can make some myself?": "Dziwne. Wygląda, że nie sprzedają balsamu aloesowego. Ciekawe, czy mogę sam zrobić?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=29 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=8: raise SystemExit(f'Expected 8, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map29')
