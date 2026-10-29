#!/usr/bin/env python3
"""Build Polish drafts for Map 139 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map139-followups-01.jsonl'
TRANSLATIONS = {
    "Damn! That was a hell of a swim.": "Cholera! Ale pływanie.",
    "We’re near the river… The current is strong toward the lake.": "Jesteśmy blisko rzeki… Prąd jest silny w stronę jeziora.",
    "So, what do we do now? Let me see the map.": "Więc co teraz? Pokaż mapę.",
    "There should be a cave near here.": "Gdzieś tu powinna być jaskinia.",
    "It’s an underwater cave… Too dangerous to risk it while holding our breath.": "To podwodna jaskinia… Za niebezpieczna, by ryzykować wstrzymując oddech.",
    "I think Jon suspected as much.": "Myślę, że Jon się tego domyślał.",
    "He gave me a couple of these…": "Dał mi parę takich…",
    "I’m not too sure about this. What if we get lost?": "Nie jestem pewna. A jeśli się zgubimy?",
    "Look at the map. It’s a straight shot. Short distance, too.": "Popatrz na mapę. To prosta droga. Krótki dystans.",
    "Hmm… It would also be going with the current.": "Hmm… Poza tym z prądem.",
    "Oh, yeah... The current is coming up from the south.": "O tak... Prąd idzie od południa.",
    "I think I see the cave.": "Chyba widzę jaskinię.",
    "Let’s give it a go.": "Spróbujmy.",
    "Stay close… If it takes more than twenty seconds, we’re turning back.": "Trzymaj się blisko… Jeśli zajmie to więcej niż dwadzieścia sekund, wracamy.",
    "I’ll be right behind you.": "Będę tuż za tobą.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=139 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=15: raise SystemExit(f'Expected 15, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map139')
