#!/usr/bin/env python3
"""Build Polish drafts for Map 167 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map167-followups-01.jsonl'
TRANSLATIONS = {
    "Heather… You are beautiful, and not just for a woman in her forties.": "Heather… Jesteś piękna, i to nie tylko jak na kobietę po czterdziestce.",
    "Thanks, 1Hero. You make me feel better.": "Dzięki, 1Hero. Sprawiasz, że czuję się lepiej.",
    "If having sex makes you feel young again, I’m happy to oblige.": "Jeśli seks sprawia, że czujesz się znowu młodo, chętnie pomogę.",
    "Oblige?": "Pomogę?",
    "Who are we kidding? Your body makes me rock hard. I drool over the thought of fucking that tight pussy of yours.": "Kogo oszukujemy? Twoje ciało sprawia, że jestem twardy jak skała. Ślinię się na myśl o pieprzeniu tej twojej ciasnej cipki.",
    "As a matter of fact….": "Właściwie to…",
    "Are you all cage fighting in there?": "Urządzacie tam walki w klatce?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=167 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=7: raise SystemExit(f'Expected 7, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map167')
