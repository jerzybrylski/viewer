#!/usr/bin/env python3
"""Build Polish drafts for Map 172 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map172-followups-01.jsonl'
TRANSLATIONS = {
    "I hear you! You better show yourself!": "Słyszę cię! Lepiej się pokaż!",
    "Ella!?": "Ella!?",
    "1Hero? Was that you making all that noise?": "1Hero? To ty robiłeś ten hałas?",
    "What are you doing down here?": "Co tu robisz?",
    "No one was here… I’m scoping it out.": "Nikogo tu nie było… Rozpoznaję teren.",
    "Someone else is down here… One of Duncan’s goons.": "Ktoś jeszcze tu jest… Jeden z ludzi Duncana.",
    "Is there another way out?": "Jest inne wyjście?",
    "The back entrance…": "Tylne wejście…",
    "I think the security is turned off, but just in case, let’s tread carefully…": "Chyba zabezpieczenia wyłączone, ale na wszelki wypadek idźmy ostrożnie…",
    "Let me guess… The walls move?": "Niech zgadnę… Ściany się ruszają?",
    "You got it. We have to go fast.": "Trafiłaś. Musimy biec szybko.",
    "I’m not the best runner. But I’ll try and keep up.": "Nie jestem najlepszą biegaczką. Ale postaram się nadążyć.",
    "Find a way to reset the security so we can get through.": "Znajdź sposób, by zresetować zabezpieczenia, żebyśmy mogli przejść.",
    "Don’t linger, 1Hero. We have to get to the rift if we're going to have any chance of taking back the Toma pieces.": "Nie ociągaj się, 1Hero. Musimy dotrzeć do szczeliny, jeśli mamy szansę odzyskać kawałki Tomy.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=172 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=14: raise SystemExit(f'Expected 14, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map172')
