#!/usr/bin/env python3
"""Build Polish drafts for Map 134 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map134-followups-01.jsonl'
TRANSLATIONS = {
    "He’s cornered!": "Jest osaczony!",
    "We got him!": "Mamy go!",
    "Looks like you’re going to have to keep your bedroom door shut until you can train him.": "Wygląda na to, że będziesz musiał trzymać drzwi sypialni zamknięte, dopóki go nie wytresujesz.",
    "Let’s just get out of here before Mom finds out the cat was in here.": "Wyjdźmy stąd, zanim mama odkryje, że kot tu był.",
    "Uhh… Why won't the door open?": "Yyy… Czemu drzwi się nie otwierają?",
    "Turn the knob.": "Przekręć klamkę.",
    "I’m trying. It’s locked.": "Próbuję. Są zamknięte.",
    "I guess we’ll have to get Heather to let us out.": "Chyba będziemy musiały poprosić Heather, by nas wypuściła.",
    "1Hero, no! She’ll make me get rid of the cat!": "1Hero, nie! Każe mi pozbyć się kota!",
    "If I break the door down, that will only make her even angrier.": "Jeśli wyważę drzwi, tylko jeszcze bardziej ją wkurzę.",
    "Can’t you pick the lock?": "Nie możesz wytrychować zamka?",
    "The hole is on the other side of the door… What kind of design is this?": "Dziurka jest po drugiej stronie drzwi… Co to za projekt?",
    "I have an idea…": "Mam pomysł…",
    "We’ll call Carol… She’ll help us.": "Zadzwonimy do Carol… Ona nam pomoże.",
    "It’ll take her a half hour to get here.": "Zajmie jej pół godziny, by tu dotrzeć.",
    "So… We just lay low for thirty minutes.": "Więc… Po prostu przeczekamy trzydzieści minut.",
    "I guess that is the best option…": "Chyba to najlepsza opcja…",
    "I’ll call her.": "Zadzwonię do niej.",
    "Carol… Chloe and I need some help.": "Carol… Chloe i ja potrzebujemy pomocy.",
    "And what are you two hiding from Heather this time?": "I co znowu ukrywacie przed Heather?",
    "We have a cat and we’re locked in Heather’s bathroom.": "Mamy kota i jesteśmy zamknięci w łazience Heather.",
    "Heather hates cats! How did you end up with a cat?": "Heather nienawidzi kotów! Jak skończyliście z kotem?",
    "It’s a long story. Just come over here and unlock Heather’s bathroom door and don’t let her see you do it.": "Długa historia. Po prostu przyjdź, odblokuj drzwi łazienki Heather i nie daj jej się zobaczyć.",
    "I’m on my way.": "Już jadę.",
    "She’s heading over.": "Już jedzie.",
    "I hope she hurries.": "Mam nadzieję, że się pospieszy.",
    "We’ll be fine. Just try and relax.": "Będzie dobrze. Spróbuj się odprężyć.",
    "Chloe!? 1Hero!?": "Chloe!? 1Hero!?",
    "Is there a cat in that box?": "Czy w tym pudle jest kot?",
    "Don’t let it run away!": "Nie pozwól mu uciec!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=134 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=30: raise SystemExit(f'Expected 30, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map134')
