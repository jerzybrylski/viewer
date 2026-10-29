#!/usr/bin/env python3
"""Build Polish drafts for Map 143 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map143-followups-01.jsonl'
TRANSLATIONS = {
    "It’s the man of the hour!": "Oto człowiek wieczoru!",
    "Hi, Paul.": "Cześć, Paul.",
    "This is going to be great! Just relax, 1Hero. A lot of people will be tuned in tonight.": "Będzie świetnie! Wyluzuj, 1Hero. Mnóstwo ludzi będzie dziś oglądać.",
    "Not exactly the most relaxing thing to hear.": "Nie najłatwiej się przy tym zrelaksować.",
    "Hey! Your girl got away!": "Hej! Twoja dziewczyna uciekła!",
    "Not now, Bobby!": "Nie teraz, Bobby!",
    "Where the hell are you going?": "Gdzie ty, do cholery, idziesz?",
    "The mansion.": "Do rezydencji.",
    "Good luck. Last I heard, there’s a shootout there.": "Powodzenia. Ostatnio słyszałem, że trwa tam strzelanina.",
    "1Hero! We’re coming with you!": "1Hero! Idziemy z tobą!",
    "We trust you. Show us the way.": "Ufamy ci. Prowadź.",
    "I’m ready to kick ass!": "Jestem gotów skopać tyłki!",
    "None of you can go to the mansion. It’s on lockdown.": "Żadne z was nie może iść do rezydencji. Jest zamknięta.",
    "Don’t worry, officer. We’re under strict orders from God Himself.": "Spokojnie, oficerze. Mamy ścisłe rozkazy od samego Boga.",
    "Is 1Hero calling himself God now?": "Czy 1Hero uważa się teraz za Boga?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=143 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=15: raise SystemExit(f'Expected 15, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map143')
