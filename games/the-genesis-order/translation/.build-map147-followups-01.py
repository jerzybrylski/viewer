#!/usr/bin/env python3
"""Build Polish drafts for Map 147 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map147-followups-01.jsonl'
TRANSLATIONS = {
    "Hmm... I expected something more interesting.": "Hmm... Spodziewałam się czegoś ciekawszego.",
    "Something smells good.": "Coś ładnie pachnie.",
    "Still a ways to go.": "Jeszcze kawałek drogi.",
    "No, I think something smells great already.": "Nie, myślę, że już teraz pachnie świetnie.",
    "Are you sniffing my neck?": "Wąchasz moją szyję?",
    "Mmm, this is it.": "Mmm, to jest to.",
    "Stop that and get to work, mister.": "Przestań i bierz się do roboty, proszę pana.",
    "Sorry, my arms decided to wrap themselves around you instead.": "Przepraszam, moje ramiona postanowiły się wokół ciebie owinąć.",
    "Oh, is that so?": "O, tak?",
    "What are we working on?": "Nad czym pracujemy?",
    "The feast, of course. Everything you see here is going into it.": "Nad ucztą, oczywiście. Wszystko, co tu widzisz, do niej trafi.",
    "Wow, that’s a lot.": "Łał, tego jest dużo.",
    "Are you sure we have all of the food?": "Na pewno mamy całe jedzenie?",
    "Now that you mention it, maybe not.": "Skoro wspominasz, może nie.",
    "We’re missing a couple things.": "Brakuje paru rzeczy.",
    "No problem, I can assist with that.": "Nie ma sprawy, mogę pomóc.",
    "Will you? I know you just got home.": "Pomożesz? Wiem, że dopiero wróciłeś do domu.",
    "It’s okay. Nothing would make me happier than to help get this feast going.": "W porządku. Nic nie uszczęśliwi mnie bardziej niż pomoc przy uczcie.",
    "We’re missing the cornbread and we still need a dessert.": "Brakuje nam chleba kukurydzianego i wciąż potrzebujemy deseru.",
    "Do I need to make a dessert?": "Mam zrobić deser?",
    "I think Hannah was going to make something.": "Myślę, że Hannah miała coś zrobić.",
    "Well, now that we’ve finished our appetizer…": "Cóż, skoro skończyliśmy przystawkę…",
    "Who’s ready for dinner?": "Kto gotowy na kolację?",
    "Let me check on Erica and see.": "Sprawdzę, co u Eriki.",
    "Hopefully you can wake her up.": "Mam nadzieję, że ją obudzisz.",
    "I’m sure you can.": "Jestem pewna, że dasz radę.",
    "For now, I’ll keep everything warmed up. But we will have guests over soon.": "Na razie wszystko podtrzymam ciepłe. Ale wkrótce będziemy mieć gości.",
    "Just let me know when you and Erica are ready.": "Daj mi tylko znać, gdy ty i Erica będziecie gotowi.",
    "You know, you don’t really need to take up Andrea’s offer.": "Wiesz, nie musisz wcale korzystać z oferty Andrei.",
    "Just come over here whenever you want to experience luxury.": "Po prostu wpadaj tu, kiedy tylko chcesz zaznać luksusu.",
    "Ha, I’m sure you’d like that.": "Ha, jestem pewna, że byś chciał.",
    "So what’s next for our intrepid ex-Guild member?": "Więc co dalej dla naszego nieustraszonego byłego członka Gildii?",
    "Good question. I’ll hang out with my daughter some more, until something comes along.": "Dobre pytanie. Posiedzę jeszcze z córką, aż coś się nadejdzie.",
    "Don’t be a stranger. We’ve always got more fun toys coming in.": "Nie bądź obcy. Zawsze mamy więcej fajnych zabawek w drodze.",
    "I’m sure I’ll be stopping by soon.": "Jestem pewna, że wkrótce wpadnę.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=147 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=35: raise SystemExit(f'Expected 35, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map147')
