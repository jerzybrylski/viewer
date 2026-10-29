#!/usr/bin/env python3
"""Build Polish drafts for Map 135 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map135-followups-01.jsonl'
TRANSLATIONS = {
    "Argh! Where is Mother!?": "Argh! Gdzie jest Matka!?",
    "Ahhh! Who the hell are you!?": "Aaa! Kim ty, do cholery, jesteś!?",
    "I need Mommy!": "Chcę mamy!",
    "Mommy!": "Mamusiu!",
    "I’ve got a gun!": "Mam pistolet!",
    "Oh, shit! There’s no ammo!": "O cholera! Nie ma amunicji!",
    "What the hell is that?...": "Co to, do cholery, jest?...",
    "Did they lock some sort of animal in here?...": "Czy zamknęli tu jakieś zwierzę?...",
    "Should I open it?": "Otworzyć to?",
    "Looks like some sort of button. I wonder what it does.": "Wygląda jak jakiś przycisk. Ciekawe, co robi.",
    "This must lead to the secret bunker entrance.": "To musi prowadzić do tajnego wejścia do bunkra.",
    "Where the hell did the monster guy go?": "Gdzie, do diabła, poszedł ten potwór?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=135 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=12: raise SystemExit(f'Expected 12, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map135')
