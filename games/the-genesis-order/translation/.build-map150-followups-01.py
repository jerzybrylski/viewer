#!/usr/bin/env python3
"""Build Polish drafts for Map 150 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map150-followups-01.jsonl'
TRANSLATIONS = {
    "Tasha!": "Tasha!",
    "Diana! Henry! You’re alive!": "Diana! Henry! Żyjecie!",
    "What’s going on? Why are you here?": "Co się dzieje? Dlaczego tu jesteście?",
    "We came to find Madalyn. We didn’t expect to find Duncan here too.": "Przyszliśmy szukać Madalyn. Nie spodziewaliśmy się zastać tu też Duncana.",
    "Madalyn wants us for something.": "Madalyn czegoś od nas chce.",
    "That’s what Duncan told us too. The question is: what for?": "Duncan też nam tak powiedział. Pytanie: czego?",
    "What happened to Lillian and the lepers? Are they still hiding?": "Co z Lillian i trędowatymi? Wciąż się ukrywają?",
    "Lillian and Madalyn are working together… At least, I’m pretty sure of that.": "Lillian i Madalyn współpracują… Przynajmniej tak mi się wydaje.",
    "Then where is everyone?": "Więc gdzie wszyscy są?",
    "Get back, you creep!": "Wynoś się, ty zboku!",
    "I’ve come to rescue you.": "Przyszedłem was uratować.",
    "Mother is in the chambers below.": "Matka jest w komnatach poniżej.",
    "And Madalyn?": "A Madalyn?",
    "The elder woman is not with us.": "Starszej kobiety nie ma z nami.",
    "We want to see Lillian.": "Chcemy zobaczyć Lillian.",
    "I will bring you to her. But only you and the maid.": "Zaprowadzę was do niej. Ale tylko ciebie i pokojówkę.",
    "Mother does not want visitors. She trusts only you.": "Matka nie chce gości. Ufa tylko tobie.",
    "We’re coming, creep.": "Idziemy, zboku.",
    "Only the maid and her companion.": "Tylko pokojówka i jej towarzysz.",
    "Fine… We’ll come with you.": "Dobra… Pójdziemy z tobą.",
    "For now?... Trust Lillian.": "Na razie?... Zaufaj Lillian.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=150 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=21: raise SystemExit(f'Expected 21, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map150')
