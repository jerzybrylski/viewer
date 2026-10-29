#!/usr/bin/env python3
"""Build Polish drafts for Map 215 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map215-followups-01.jsonl'
TRANSLATIONS = {
    "I don't have any stones.": "Nie mam żadnych kamieni.",
    "What do you think? Can you cross?": "Co myślisz? Dasz radę przejść?",
    "Don’t let me hold you up.": "Nie chcę ci przeszkadzać.",
    "We’re going to have to cross here.": "Będziemy musieli przejść tutaj.",
    "Through the rapids? That’s not going to be easy.": "Przez bystrza? To nie będzie łatwe.",
    "Maybe we can find stepping stones to cross it.": "Może znajdziemy kamienie, by przejść.",
    "They would have to be pretty big stones.": "Musiałyby być całkiem duże.",
    "You’re strong. Let’s see what we can find.": "Jesteś silny. Zobaczmy, co znajdziemy.",
    "If we had some big rocks, we could use them as stepping stones.": "Gdybyśmy mieli duże skały, moglibyśmy ich użyć jako kamieni do przejścia.",
    "Maybe the stones are marked on the map.": "Może kamienie są zaznaczone na mapie.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=215 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=10: raise SystemExit(f'Expected 10, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map215')
