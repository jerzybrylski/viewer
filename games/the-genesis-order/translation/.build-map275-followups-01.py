#!/usr/bin/env python3
"""Build Polish drafts for Map 275 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map275-followups-01.jsonl'
TRANSLATIONS = {
    "Do you think the cat understands what you’re saying?": "Myślisz, że kot rozumie, co mówisz?",
    "My God! It’s in the air vent!": "Mój Boże! Jest w szybie wentylacyjnym!",
    "No, no, no. This isn’t my job. This is your area, detective.": "Nie, nie, nie. To nie moja robota. To twój rewir, detektywie.",
    "My job?": "Moja robota?",
    "You’re the raccoon guy.": "Ty jesteś od szopów.",
    "Who said that!?": "Kto tak powiedział!?",
    "Huh? I thought everyone called you the raccoon guy.": "Huh? Myślałem, że wszyscy nazywają cię panem od szopów.",
    "It’s not a raccoon.": "To nie szop.",
    "So you are the raccoon guy.": "Więc jesteś panem od szopów.",
    "I’m not going to capture an escaped cat.": "Nie będę łapać zbiegłego kota.",
    "Then someone will have to explain why there’s the smell of dead feline coming from the vents in about a week.": "W takim razie ktoś będzie musiał wytłumaczyć, skąd za tydzień smród martwego kota z wentylacji.",
    "Fine… I’ll capture the damn cat.": "Dobra… Złapię cholernego kota.",
    "I knew we could count on the raccoon man.": "Wiedziałem, że możemy liczyć na pana od szopów.",
    "I’m not a raccoon man!": "Nie jestem panem od szopów!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=275 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=14: raise SystemExit(f'Expected 14, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map275')
