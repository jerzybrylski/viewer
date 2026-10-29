#!/usr/bin/env python3
"""Build Polish drafts for Map 131 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map131-followups-01.jsonl'
TRANSLATIONS = {
    "The backup lock on my safe was triggered.": "Zapasowy zamek w sejfie został uruchomiony.",
    "Whoever broke in tried to open it and busted it.": "Ktoś próbował go otworzyć i go zepsuł.",
    "What’s inside?": "Co jest w środku?",
    "Something special to me… I don’t want to leave without it.": "Coś dla mnie wyjątkowego… Nie chcę odchodzić bez tego.",
    "Hmm… Let me see if I can open it.": "Hmm… Zobaczę, czy mogę to otworzyć.",
    "The problem is you can’t cut the safe open without a plasma torch.": "Problem w tym, że nie przetniesz sejfu bez palnika plazmowego.",
    "I can’t leave without getting something from my safe first.": "Nie mogę odejść bez zabrania czegoś z sejfu.",
    "The problem is you can’t cut the safe open without a welding torch.": "Problem w tym, że nie przetniesz sejfu bez palnika spawalniczego.",
    "Hmm… This safe is broken. How the hell could I unlock it?": "Hmm… Sejf jest zepsuty. Jak, u diabła, mógłbym go odblokować?",
    "My favorite katana!": "Moja ulubiona katana!",
    "We opened the safe so you could get a sword?": "Otworzyliśmy sejf, żebyś mógł dostać miecz?",
    "Hey. It means a lot to me.": "Hej. Dużo dla mnie znaczy.",
    "Now, let’s get out of here before the Guild goons come back.": "Teraz wynośmy się stąd, zanim wrócą zbiry Gildii.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=131 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=13: raise SystemExit(f'Expected 13, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map131')
