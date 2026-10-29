#!/usr/bin/env python3
"""Build Polish drafts for Map 276 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map276-followups-01.jsonl'
TRANSLATIONS = {
    "Oh, God! Holy shit!": "O Boże! O cholera!",
    "Hahaha!": "Hahaha!",
    "Sometimes the simplest solution escapes us, even when in front of us all along.": "Czasem najprostsze rozwiązanie umyka nam, nawet gdy jest cały czas przed nami.",
    "It’s time for us to part, 1Hero.": "Czas się rozstać, 1Hero.",
    "Wait, what?": "Czekaj, co?",
    "My quest brings me to a new place… Somewhere far from here.": "Moja misja prowadzi mnie w nowe miejsce… Gdzieś daleko stąd.",
    "But you’ll be back, won’t you?": "Ale wrócisz, prawda?",
    "I won’t forget about you, 1Hero.": "Nie zapomnę o tobie, 1Hero.",
    "Let me come with you.": "Pozwól mi iść z tobą.",
    "I’m sorry, 1Hero. You’ll just have to leave this one unsolved.": "Przepraszam, 1Hero. Tę będziesz musiał zostawić nierozwiązaną.",
    "Our paths will cross again. I’m sure of it.": "Nasze ścieżki znów się przetną. Jestem pewna.",
    "Behave yourself.": "Zachowuj się.",
    "For you, 1Hero.": "Dla ciebie, 1Hero.",
    "Goodbye, Lillian.": "Żegnaj, Lillian.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=276 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=14: raise SystemExit(f'Expected 14, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map276')
