#!/usr/bin/env python3
"""Build Polish drafts for Map 174 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map174-followups-01.jsonl'
TRANSLATIONS = {
    "Shit… It’s gone.": "Cholera… Zniknęła.",
    "Holy hell! That woman sure does have a tasty pussy!": "O cholera! Ta kobieta ma naprawdę smakowitą cipkę!",
    "I… I don’t know. She didn’t come with us.": "Ja… Nie wiem. Nie przyszła z nami.",
    "Shit! We have to find her.": "Cholera! Musimy ją znaleźć.",
    "Do you think the woman took her?": "Myślisz, że kobieta ją zabrała?",
    "She wants Judy.": "Chce Judy.",
    "I need to talk to Father Solomon.": "Muszę porozmawiać z ojcem Solomonem.",
    "What’s he going to do?": "Co on zrobi?",
    "I assume she’s taking Sister Judy to the rift… Father can defeat the demons. He has the power.": "Zakładam, że zabiera siostrę Judy do szczeliny… Ojciec pokona demony. Ma moc.",
    "Let’s get the hell out of here.": "Wynośmy się stąd, do cholery.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=174 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=10: raise SystemExit(f'Expected 10, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map174')
