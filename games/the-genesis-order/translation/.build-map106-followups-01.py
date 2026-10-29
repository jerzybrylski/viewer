#!/usr/bin/env python3
"""Build Polish drafts for Map 106 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map106-followups-01.jsonl'
TRANSLATIONS = {
    "Come on, 1Hero. Stop dragging your feet.": "Dalej, 1Hero. Przestań się wlec.",
    "Wait. Did you hear that?": "Czekaj. Słyszałaś to?",
    "Someone’s over there.": "Ktoś tam jest.",
    "God damn it. Why is this my job now?": "Cholera. Czemu to teraz moja robota?",
    "Nellie!": "Nellie!",
    "1Hero! You need to get out of this cave. What are you still doing here?": "1Hero! Musisz wynieść się z tej jaskini. Co tu jeszcze robisz?",
    "Shit! How many people are you bringing down here?": "Cholera! Ilu ludzi tu sprowadzasz?",
    "You sure are pretty for a cave dweller.": "Jesteś całkiem ładna jak na mieszkankę jaskini.",
    "Nellie, there’s someone coming for you.": "Nellie, ktoś po ciebie idzie.",
    "What are you talking about, 1Hero?": "O czym ty mówisz, 1Hero?",
    "Madalyn. She’s looking for your hideout.": "Madalyn. Szuka twojej kryjówki.",
    "Charles Wilkes’ wife… She’s a powerful woman.": "Żona Charlesa Wilkesa… Potężna kobieta.",
    "What’s going on here? Who are you, lady?": "Co tu się dzieje? Kim jesteś, paniusiu?",
    "She’s Tasha’s mom… from the porn shop.": "To mama Tashy… ze sklepu porno.",
    "You live with a bunch of thieves?": "Mieszkasz ze złodziejami?",
    "You need to keep quiet, 1Hero.": "Musisz być cicho, 1Hero.",
    "You’re on the doorstep of her farm.": "Jesteś u progu jej farmy.",
    "Yeah! You’re nearly trespassing.": "Tak! Prawie tu włamujesz się na teren.",
    "We’re not robbing a fucking farm.": "Nie obrabiamy pieprzonej farmy.",
    "Damn straight you ain’t!": "Jasne, że nie!",
    "You need to leave, 1Hero. This is the worst possible place to have a meeting.": "Musisz odejść, 1Hero. To najgorsze możliwe miejsce na spotkanie.",
    "Kimura is pissed.": "Kimura jest wkurwiona.",
    "At you, I’m sure.": "Na ciebie, jestem pewna.",
    "There’s something happening here that’s bigger than the Guild case.": "Dzieje się tu coś większego niż sprawa Gildii.",
    "Dammit, 1Hero…": "Cholera, 1Hero…",
    "Let’s meet later.": "Spotkajmy się później.",
    "Here’s my number…": "Tu masz mój numer…",
    "It’s safe for you to leave the bunker?": "Bezpiecznie dla ciebie opuścić bunkier?",
    "I can go anywhere I want. I’ve got Duncan wrapped around my little finger.": "Mogę iść, gdzie chcę. Mam Duncana owiniętego wokół małego palca.",
    "I’d love to pick your brain.": "Chętnie bym pogrzebała ci w głowie.",
    "I’m sure that’s not the only part of me you want.": "Jestem pewna, że to nie jedyna część mnie, której chcesz.",
    "Hey, lady!": "Hej, paniusiu!",
    "Get out of here. If anyone sees you, we’re all fucked.": "Wynoś się stąd. Jeśli ktoś cię zobaczy, wszyscy mamy przerąbane.",
    "You better stay out of my field.": "Lepiej trzymaj się z dala od mojego pola.",
    "Come on, Hannah. Let’s get out of here.": "Chodź, Hannah. Wynośmy się stąd.",
    "Looks like there’s a box barely hanging off the ledge…": "Wygląda, że skrzynka ledwo trzyma się krawędzi…",
    "A good shake would make it fall.": "Dobre potrząśnięcie sprawi, że spadnie.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=106 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=37: raise SystemExit(f'Expected 37, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map106')
