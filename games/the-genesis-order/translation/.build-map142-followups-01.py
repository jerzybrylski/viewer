#!/usr/bin/env python3
"""Build Polish drafts for Map 142 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map142-followups-01.jsonl'
TRANSLATIONS = {
    "Detective!?": "Detektywie!?",
    "The dude got away.": "Gość uciekł.",
    "Unacceptable! Find him!": "Niedopuszczalne! Znajdźcie go!",
    "We tried. He’s gone.": "Próbowaliśmy. Zniknął.",
    "Hey! You backstabber!": "Hej! Ty zdrajco!",
    "Go fuck yourself.": "Spierdalaj.",
    "Hey, freeze!": "Hej, stój!",
    "Don’t worry. I got him.": "Spokojnie. Mam go.",
    "You’re all fucking backstabbers.": "Wszyscy jesteście pierdolonymi zdrajcami.",
    "I don’t play nice with tenants that try and fuck me over.": "Nie zadzieram z lokatorami, którzy próbują mnie wykiwać.",
    "Drop the gun.": "Rzuć broń.",
    "The old man’s not here.": "Starego tu nie ma.",
    "Don’t be so sure. We’ll comb this place over.": "Nie bądź taki pewien. Przeczeszemy to miejsce.",
    "Why are you still here, 1Hero? You’re not a detective anymore.": "Czemu wciąż tu jesteś, 1Hero? Nie jesteś już detektywem.",
    "He’s with me.": "Jest ze mną.",
    "He can’t be at the scene of a crime.": "Nie może być na miejscu przestępstwa.",
    "You uniformed officers are all the same…": "Wy umundurowani wszyscy tacy sami…",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=142 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=17: raise SystemExit(f'Expected 17, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map142')
