#!/usr/bin/env python3
"""Build Polish drafts for Map 67 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map67-followups-01.jsonl'
TRANSLATIONS = {
    "Shit… A dead end.": "Cholera… Ślepy zaułek.",
    "I doubt it. This is clearly an escape route.": "Wątpię. To wyraźnie trasa ucieczki.",
    "It opened up!": "Otworzyło się!",
    "Look! It’s where the bad guys live!": "Patrz! Tu mieszkają źli goście!",
    "It’s part of the mansion… Some sort of hidden escape route. It’s not the bunker.": "To część rezydencji… Jakiś ukryty szlak ucieczki. To nie bunkier.",
    "Damn. I didn’t know all this was in here.": "Cholera. Nie wiedziałem, że to wszystko tu jest.",
    "So, where do we go?": "Więc dokąd idziemy?",
    "I’ll figure out something.": "Coś wymyślę.",
    "Should we go up those stairs?": "Iść tymi schodami?",
    "No, that leads to the mansion. We need to go deeper into the cave.": "Nie, to prowadzi do rezydencji. Musimy zejść głębiej w jaskinię.",
    "God dammit! That was loud!": "Kurwa! Ale głośno!",
    "Look! The cave goes deeper.": "Patrz! Jaskinia ciągnie się głębiej.",
    "Let’s find that bonker!": "Znajdźmy ten bunkier!",
    "It’s called a bunker!": "Nazywa się bunkier!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=67 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=14: raise SystemExit(f'Expected 14, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map67')
