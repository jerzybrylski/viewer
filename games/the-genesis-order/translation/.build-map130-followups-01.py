#!/usr/bin/env python3
"""Build Polish drafts for Map 130 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map130-followups-01.jsonl'
TRANSLATIONS = {
    "There’s a hot tub in the sunroom. Make yourself comfortable.": "W oranżerii jest jacuzzi. Rozgość się.",
    "A hot tub?": "Jacuzzi?",
    "Relax, 1Hero. After today, things are going to change.": "Odpocznij, 1Hero. Po dziś wszystko się zmieni.",
    "What the hell did this button do?": "Co ten przycisk zrobił, do cholery?",
    "I have to confess that I’m a little jealous of Erica and Judy.": "Muszę przyznać, że jestem trochę zazdrosna o Ericę i Judy.",
    "You’re always welcome to visit, you know that.": "Zawsze możesz nas odwiedzać, wiesz o tym.",
    "I’ll be sure to visit a lot.": "Na pewno będę często wpadać.",
    "So are you really going to keep Goatzilla and the gator?": "Więc naprawdę zatrzymasz Goatzillę i aligatora?",
    "I don’t know. I shouldn’t leave Mom to take care of them all the time…": "Nie wiem. Nie powinnam zostawiać mamy, by cały czas się nimi zajmowała…",
    "But Chloe doesn’t really want them around either.": "Ale Chloe też nie bardzo chce je mieć w pobliżu.",
    "I hope you figure something out.": "Mam nadzieję, że coś wymyślisz.",
    "So what’s the next big story for Channel 4’s leading news reporter?": "Jaki będzie następny wielki temat naczelnej reporterki Channel 4?",
    "The sex virus is becoming an international issue.": "Wirus seksu staje się problemem międzynarodowym.",
    "Something tells me we’re looking at an impending pandemic.": "Coś mi mówi, że patrzymy na nadchodzącą pandemię.",
    "Any interesting projects going on at your business in Osira?": "Jakieś ciekawe projekty w twoim biznesie w Osirze?",
    "We might have something in the works.": "Może coś się kroi.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=130 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=16: raise SystemExit(f'Expected 16, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map130')
