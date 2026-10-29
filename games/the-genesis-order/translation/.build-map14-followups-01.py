#!/usr/bin/env python3
"""Build Polish drafts for Map 14 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map14-followups-01.jsonl'
TRANSLATIONS = {
    "Do you have any idea what it’s like to stand outside all day? I’m covered in sunburn!": "Masz pojęcie, jak to jest stać cały dzień na zewnątrz? Jestem cały poparzony słońcem!",
    "Is that an aloe plant? Mind if I take it off your hands? I will reward you nicely.": "To aloes? Mogę go zabrać? Nagrodzę cię ładnie.",
    "Thanks! Here’s your reward. Take this key.": "Dzięki! Oto nagroda. Weź ten klucz.",
    "I guess if I want another aloe plant, I need to visit the farm.": "Chyba jeśli chcę kolejnego aloesu, muszę odwiedzić farmę.",
    "I can’t get my dog to eat its medicine. Can you help?": "Nie mogę zmusić psa do zjedzenia leku. Pomożesz?",
    "Hey! That’s a great idea!": "Hej! To świetny pomysł!",
    "Here, take some dog medicine for your troubles.": "Trzymaj, weź lekarstwo dla psa za fatygę.",
    "Why is my dog moving so slowly?": "Czemu mój pies porusza się tak wolno?",
    "Hey! No fireworks are allowed in the city.": "Hej! Żadne fajerwerki nie są dozwolone w mieście.",
    "1Hero! I was just…": "1Hero! Ja tylko…",
    "Hand over the fireworks, Larry.": "Oddaj fajerwerki, Larry.",
    "No way, dude. I spent a lot on these!...": "Nie ma mowy, stary. Sporo za nie zapłaciłem!...",
    "Perhaps you have something to trade for them?": "Może masz coś na wymianę?",
    "Woah! Vintage porn!": "Łał! Vintage porno!",
    "Good enough for you?": "Wystarczy ci to?",
    "Sure! Take my fireworks.": "Jasne! Bierz moje fajerwerki.",
    "Ugh! Not interested.": "Ugh! Nie jestem zainteresowana.",
    "Thanks for the porn!": "Dzięki za porno!",
    "Don’t talk so loudly!": "Nie mów tak głośno!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=14 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=19: raise SystemExit(f'Expected 19, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map14')
