#!/usr/bin/env python3
"""Build Polish drafts for Map 282 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map282-followups-01.jsonl'
TRANSLATIONS = {
    "Who are you!?": "Kim jesteś!?",
    "I’m so sorry!": "Tak mi przykro!",
    "The laptop! It’s gone!": "Laptop! Zniknął!",
    "The laptop, sir?": "Laptop, sir?",
    "The one with all the Guild evidence on it!": "Ten ze wszystkimi dowodami Gildii!",
    "Detective! Your metal ball from the mansion is gone too!": "Detektywie! Twoja metalowa kula z rezydencji też zniknęła!",
    "It must be the work of the Guild. She’s some kind of masquerader thief.": "To musi być sprawka Gildii. To jakaś przebierana złodziejka.",
    "Quickly, scour the station to find her! We can’t let her escape!": "Szybko, przeczeszcie komisariat, by ją znaleźć! Nie możemy pozwolić jej uciec!",
    "Well… that wasn’t according to plan.": "Cóż… Nie poszło zgodnie z planem.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=282 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=9: raise SystemExit(f'Expected 9, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map282')
