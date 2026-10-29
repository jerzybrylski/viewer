#!/usr/bin/env python3
"""Build Polish drafts for Map 59 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map59-followups-01.jsonl'
TRANSLATIONS = {
    "The gym’s closed for the next hour.": "Siłownia zamknięta na następną godzinę.",
    "Is the commissioner in there?": "Pani komisarz jest w środku?",
    "I said, gym’s closed.": "Mówiłem, siłownia zamknięta.",
    "I’m working directly for Kimura. I should be able to work out with her if I want to.": "Pracuję bezpośrednio dla Kimury. Powinienem móc poćwiczyć z nią, jeśli chcę.",
    "Who the hell do you think you are?": "Za kogo ty się uważasz?",
    "Come, on man. Let me in. You can’t use the gym as a meeting room.": "Daj spokój, stary. Wpuść mnie. Nie możesz używać siłowni jako sali konferencyjnej.",
    "What’s in it for me?": "Co ja z tego będę miał?",
    "You want a bribe? Really?": "Chcesz łapówki? Serio?",
    "Give me $2,000 and you can work out with the boss.": "Daj 2 000 $ i możesz poćwiczyć z szefową.",
    "Fine. How about $500?": "Dobra. A może 500 $?",
    "It ain’t happening.": "Nie ma mowy.",
    "Okay, $50. But that is as low as I’ll go.": "Dobra, 50 $. Ale to najniżej, jak zejdę.",
    "Shit. I don’t have that much money.": "Cholera. Nie mam tyle kasy.",
    "I’ll be back.": "Wrócę.",
    "If that’s what it’ll take, then take the money.": "Jeśli tego trzeba, to bierz kasę.",
    "Pleasure doing business with you.": "Przyjemność robić interesy.",
    "I want to talk to Duncan’s other henchman, but I’d never be able to make it past the guard…": "Chcę porozmawiać z drugim zbirami Duncana, ale nigdy nie przejdę obok strażnika…",
    "Hurry up with the interrogation. I can’t stand guard all day.": "Pospiesz się z przesłuchaniem. Nie mogę stać na warcie cały dzień.",
    "Wait here.": "Poczekaj tutaj.",
    "The gym is closed for the next hour.": "Siłownia zamknięta na następną godzinę.",
    "How’d the test go?": "Jak poszedł test?",
    "I passed with flying colors.": "Zdałem celująco.",
    "Heh. I thought for sure Bobby would fail you on principle.": "Heh. Myślałem, że Bobby z zasady cię uwali.",
    "Melissa… I may need some help.": "Melissa… Może potrzebuję pomocy.",
    "You? Need help?": "Ty? Potrzebujesz pomocy?",
    "I’m going somewhere with the priest from Eve Cathedral.": "Wybieram się gdzieś z księdzem z katedry Eve.",
    "Father Solomon.": "Ojcem Solomonem.",
    "I’m worried about leaving the nun alone.": "Martwię się, zostawiając zakonnicę samą.",
    "… And for some reason you don’t want officers at the church.": "…I z jakiegoś powodu nie chcesz funkcjonariuszy w kościele.",
    "Do you think you could stop by the church later and keep Sister Judy company?": "Mogłabyś wpaść później do kościoła i dotrzymać towarzystwa siostrze Judy?",
    "1Hero asking for help. How could I say no?": "1Hero prosi o pomoc. Jak mogłabym odmówić?",
    "You’ll come?": "Przyjdziesz?",
    "I’ll head over later.": "Wpadnę później.",
    "Don’t let anyone know.": "Niech nikt się nie dowie.",
    "What’s the secret?": "Jaki sekret?",
    "Going over Andrea’s head… of course.": "Ominięcie Andrei… oczywiście.",
    "Consider it done.": "Uznaj, że załatwione.",
    "What would happen if I used my stun gun on it?": "Co by się stało, gdybym użyła paralizatora na tym?",
    "Hey!? What the hell?": "Hej!? Co jest, do cholery!?",
    "Oops! I overloaded the circuit. Now I can’t see anything…": "Ups! Przeciążyłam obwód. Teraz nic nie widzę…",
    "How can I make it out of here?": "Jak mam się stąd wydostać?",
    "I’m not sure what stunt you pulled at the Channel 4 building, but you owe me an explanation.": "Nie wiem, jaką sztuczkę odwaliłeś w budynku Channel 4, ale jesteś mi winien wyjaśnienie.",
    "Is this your doing? Did you convince them to let me go?": "To twoja sprawka? Przekonałeś ich, żeby mnie wypuścili?",
    "Guilty as charged.": "Przyznaję się.",
    "Bobby… You’re not going to believe me, but those dead bodies in the studio were demons.": "Bobby… Nie uwierzysz mi, ale te martwe ciała w studiu to były demony.",
    "Yeah… I don’t believe you.": "Taa… Nie wierzę ci.",
    "You don’t have to. I just need you to do one thing and it’ll all become clear.": "Nie musisz. Potrzebuję tylko, żebyś zrobił jedną rzecz i wszystko stanie się jasne.",
    "There’s a room in the mansion that is secret. You have to make sure no one goes down there.": "W rezydencji jest sekretny pokój. Musisz dopilnować, by nikt tam nie schodził.",
    "You want me to keep officers from doing their job searching the mansion?": "Chcesz, żebym powstrzymał funkcjonariuszy przed przeszukiwaniem rezydencji?",
    "Once you see what’s down there, you’ll understand.": "Gdy zobaczysz, co tam jest na dole, zrozumiesz.",
    "What’s down there?": "Co tam jest na dole?",
    "A portal to Hell.": "Portal do piekła.",
    "Hahaha!": "Hahaha!",
    "You’re a hotshot, aren’t you?": "Jesteś cwaniak, co?",
    "You can handle yourself.": "Potrafisz o siebie zadbać.",
    "Damn right, I can.": "Jasne, że potrafię.",
    "There’s a switch on the east gargoyle just past the entry to the mansion…": "Na wschodnim gargulcu tuż za wejściem do rezydencji jest przełącznik…",
    "It will open up a secret pathway that will lead to the portal.": "Otworzy sekretne przejście prowadzące do portalu.",
    "Go inside and see for yourself.": "Wejdź i zobacz na własne oczy.",
    "You must be joking.": "Chyba żartujesz.",
    "But, Bobby… Once you see it, you must run and don’t look back.": "Ale, Bobby… Gdy to zobaczysz, musisz uciekać i nie oglądać się za siebie.",
    "Trying to scare me?": "Próbujesz mnie nastraszyć?",
    "You’ll be scared. Believe me.": "Będziesz się bał. Uwierz mi.",
    "If what you say is true, I should bring the whole department down there.": "Jeśli to, co mówisz, jest prawdą, powinienem sprowadzić tam cały wydział.",
    "No! That’s what she’ll want you to do!...": "Nie! To właśnie ona chciałaby, żebyś zrobił!...",
    "You have to be sneaky.": "Musisz być cwany.",
    "Fine… Since we’re trusting each other now… I’ll do it.": "Dobra… Skoro teraz sobie ufamy… Zrobię to.",
    "I’ll help you take down the commissioner… But there are other loose ends.": "Pomogę ci dorwać panią komisarz… Ale są inne luźne końce.",
    "I don’t know yet… But I have an idea.": "Jeszcze nie wiem… Ale mam pomysł.",
    "Some artifact hunting.": "Polowanie na artefakty.",
    "You’re driving me crazy, 1Hero.": "Doprowadzasz mnie do szału, 1Hero.",
    "Yeah, I tend to do that to people.": "Tak, mam taki talent do ludzi.",
    "There better be a magic road to Hell. This better not be a joke.": "Lepiej, żeby była magiczna droga do piekła. To lepiej niech nie będzie żart.",
    "I wish it were.": "Chciałbym, żeby był.",
    "Bobby… Be very careful.": "Bobby… Bądź bardzo ostrożny.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=59 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=75: raise SystemExit(f'Expected 75, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map59')
