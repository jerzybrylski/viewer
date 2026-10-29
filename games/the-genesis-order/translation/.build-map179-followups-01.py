#!/usr/bin/env python3
"""Build Polish drafts for Map 179 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map179-followups-01.jsonl'
TRANSLATIONS = {
    "Argh! Intruders!": "Argh! Intruz!",
    "Get them!": "Dopadnijcie ich!",
    "So, what’s the trick?": "Więc jaki jest trik?",
    "Careful… Demons could be in there.": "Ostrożnie… W środku mogą być demony.",
    "It’s a temple… I'd wager our Toma is in there.": "To świątynia… Założyłbym się, że nasza Toma jest w środku.",
    "There’s got to be a way to open it… Look around and see what you can find.": "Musi być sposób, by to otworzyć… Rozejrzyj się i zobacz, co znajdziesz.",
    "These bells seemed to have fit.": "Te dzwony jakby pasowały.",
    "You think that has something to do with the door?": "Myślisz, że to ma coś wspólnego z drzwiami?",
    "It’s worth a shot.": "Warto spróbować.",
    "What?... You want to ring the bells?... It might draw attention.": "Co?... Chcesz zadzwonić dzwonami?... To może zwrócić uwagę.",
    "Fuck it. Let’s see what happens.": "Pieprzyć to. Zobaczmy, co się stanie.",
    "I think it worked!": "Chyba zadziałało!",
    "Get it!": "Bierz to!",
    "Coming to your senses?": "Odzyskujesz zmysły?",
    "If you want the statue, you must leave the humans alone.": "Jeśli chcesz posąg, musisz zostawić ludzi w spokoju.",
    "Oh, shit! I see myself!": "O cholera! Widzę siebie!",
    "You are not their mother… Let’s clear their world and take it over; this is our chance.": "Nie jesteś ich matką… Oczyśćmy ich świat i go przejmijmy; to nasza szansa.",
    "And who would rule?": "I kto miałby rządzić?",
    "Of course there would be room for a queen.": "Oczywiście znalazłoby się miejsce dla królowej.",
    "What a generous offer.": "Co za hojna oferta.",
    "Do you take me for an idiot? What are you planning to do?": "Masz mnie za idiotkę? Co planujesz zrobić?",
    "Shit… Her body is getting away.": "Cholera… Jej ciało ucieka.",
    "You want it? Come and take it!": "Chcesz to? Chodź i weź!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=179 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=23: raise SystemExit(f'Expected 23, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map179')
