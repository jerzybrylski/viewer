#!/usr/bin/env python3
"""Build Polish drafts for Map 7 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map7-followups-01.jsonl'
TRANSLATIONS = {
    "Come on. Answer the door.": "No dalej. Otwórz drzwi.",
    "Detective Canmore?": "Detektyw Canmore?",
    "Hello, Officer.": "Dzień dobry, oficerze.",
    "Are you looking for Detective Bhatt?": "Szukasz detektyw Bhatt?",
    "Uhh, yeah. I have to discuss a case with her.": "Yh, tak. Muszę omówić z nią sprawę.",
    "You just missed her. She left not long ago and headed west… Maybe to the store.": "Właśnie ją minąłeś. Wyszła niedawno i poszła na zachód… Może do sklepu.",
    "Oh, thanks. I’ll see if I can catch up with her.": "O, dzięki. Zobaczę, czy ją dogonię.",
    "I’ve lost my cat! It’s a dark, black cat that moves very fast. I hope he’s not gone far.": "Zgubiłam kota! To czarny, czarny kot, który bardzo szybko się porusza. Mam nadzieję, że nie poszedł daleko.",
    "Did you find my lost cat?": "Znalazłeś mojego zgubionego kota?",
    "Thank you so much! Here’s a reward!": "Dziękuję ci bardzo! Oto nagroda!",
    "I was just enjoying the nice weather.": "Po prostu cieszyłam się ładną pogodą.",
    "You’re not coming to visit me, are you?": "Nie przychodzisz mnie odwiedzić, co?",
    "No work on a Sunday, I promise.": "Bez pracy w niedzielę, obiecuję.",
    "Enjoy your weekend. I’ll see you bright and early tomorrow morning.": "Miłego weekendu. Do zobaczenia jutro rano.",
    "See you in the office.": "Do zobaczenia w biurze.",
    "How did you know Melissa lived here?": "Skąd wiedziałeś, gdzie mieszka Melissa?",
    "I live closeby.": "Mieszkam niedaleko.",
    "You live around here? How much are they paying officers these days?": "Mieszkasz w okolicy? Ile płacą teraz funkcjonariuszom?",
    "Move along, detective.": "Spadaj, detektywie.",
    "Alright, let’s stick to the topic at hand and get this over with fast.": "Dobra, trzymajmy się tematu i załatwmy to szybko.",
    "Sounds like a plan. Andrea will be expecting us at seven.": "Brzmi jak plan. Andrea będzie na nas czekać o siódmej.",
    "See ya around, Melissa.": "Do zobaczenia, Melissa.",
    "You better watch what you say in the office.": "Lepiej uważaj, co mówisz w biurze.",
    "Heh.": "Heh.",
    "I can see something on the other side of the fence. I wonder if I could throw something at it and knock it down.": "Widzę coś po drugiej stronie płotu. Ciekawe, czy mógłbym w to rzucić i to zrzucić.",
    "Here for some action? I do love your youthful stamina.": "Przyszedłeś po akcję? Uwielbiam twoją młodzieńczą wytrzymałość.",
    "Ha, no, not today.": "Ha, nie, nie dziś.",
    "I’ve come to discuss Guild business.": "Przyszedłem omówić interesy Gildii.",
    "Haha, you? This should be good.": "Haha, ty? To będzie dobre.",
    "Not exactly what you think. I found an old briefcase of my dad’s.": "Nie do końca tak, jak myślisz. Znalazłem starą walizkę taty.",
    "But it needs a code to unlock it. Looks complicated.": "Ale potrzebuje kodu, by ją otworzyć. Wygląda skomplikowanie.",
    "Nellie mentioned the Guild had a system for generating codes.": "Nellie wspomniała, że Gildia miała system generowania kodów.",
    "We did. Maybe not as complicated as you think.": "Mieliśmy. Może nie tak skomplikowany, jak myślisz.",
    "I don’t recall how it worked though.": "Nie pamiętam jednak, jak działał.",
    "So that’s it? Damn.": "Więc tyle? Cholera.",
    "Not so fast. Somewhere in my mansion you can find a document explaining it.": "Nie tak szybko. Gdzieś w mojej rezydencji znajdziesz dokument to wyjaśniający.",
    "Being such a smart detective, I’m sure you could figure it out from there.": "Będąc tak bystrym detektywem, na pewno to rozgryziesz.",
    "Right. Don’t suppose you remember where, exactly?": "Jasne. Nie pamiętasz przypadkiem gdzie, dokładnie?",
    "Sorry, Detective Canmore. You’ll just have to put those sleuthing skills to good use.": "Przepraszam, detektywie Canmore. Będziesz musiał użyć umiejętności śledczych.",
    "Thanks, Andrea. I’ll get right on that.": "Dziękuję, Andrea. Zajmę się tym od razu.",
    "Don’t be a stranger.": "Nie bądź obcy.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=7 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=41: raise SystemExit(f'Expected 41, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map7')
