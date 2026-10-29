#!/usr/bin/env python3
"""Build Polish drafts for Map 240 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map240-followups-01.jsonl'
TRANSLATIONS = {
    "1Hero! The car won't start. I don’t know what’s wrong with it.": "1Hero! Auto nie chce odpalić. Nie wiem, co z nim jest.",
    "It’s okay, ma’am; Detective Canmore is on the case.": "Spokojnie, proszę pani; detektyw Canmore się tym zajmie.",
    "Thanks, darling. What would I do without you?": "Dziękuję, kochanie. Co ja bym bez ciebie zrobiła?",
    "Did you figure out why the car won't start?": "Dowiedziałeś się, czemu auto nie odpala?",
    "Working on it.": "Pracuję nad tym.",
    "Did you find out what the note with the coordinates was for?": "Dowiedziałeś się, do czego była notatka ze współrzędnymi?",
    "Still looking into it.": "Wciąż to sprawdzam.",
    "Hi, darling! What did you find?": "Hej, kochanie! Co znalazłeś?",
    "A briefcase… with the letters “KC” on it.": "Walizkę… z literami „KC” na niej.",
    "I seem to recall a certain person whose initials used to be KC…": "Kojarzę pewną osobę, której inicjały kiedyś brzmiały KC…",
    "Oh, my… Kirk Chesterfield.": "Ojej… Kirk Chesterfield.",
    "Why did your car have coordinates to Dad’s old briefcase?": "Czemu w twoim aucie były współrzędne do starej walizki taty?",
    "It used to be Kirk’s car.": "Kiedyś to było auto Kirka.",
    "Why do you have Dad’s used car?": "Czemu masz używane auto taty?",
    "He left it here with me, silly.": "Zostawił je u mnie, głuptasie.",
    "Back then, he was a different man. Crazy, yes, but not quite that crazy.": "Wtedy był innym człowiekiem. Szalonym, owszem, ale nie aż tak szalonym.",
    "Generous, too, huh?": "Hojnym też, co?",
    "Any idea what the code could be?": "Masz pomysł, jaki może być kod?",
    "No idea. Maybe you could try asking him?": "Nie mam pojęcia. Może spróbujesz go zapytać?",
    "He’s in jail, and I definitely don’t want to pay him a visit there.": "Siedzi w więzieniu i na pewno nie chcę go tam odwiedzać.",
    "He did try to murder me, after all.": "W końcu próbował mnie zamordować.",
    "Maybe someone knows something. I’ll ask around and glean what I can.": "Może ktoś coś wie. Popytam i wyciągnę, co się da.",
    "Cracked the code on the briefcase?": "Złamałeś kod do walizki?",
    "Heather… What was the license plate on the car before you owned it? Do you remember?": "Heather… Pamiętasz, jaką tablicę rejestracyjną miało auto, zanim je miałaś?",
    "Oh, yes. I remember exactly what it was…": "O tak. Pamiętam dokładnie, jaka była…",
    "Big Man.": "Big Man.",
    "Big Man? Oof…": "Big Man? Ojej…",
    "Alright, Dad.": "Dobra, tato.",
    "His old nickname.": "Jego stary pseudonim.",
    "Handle! He meant a nickname!": "Handle! Miał na myśli pseudonim!",
    "Did you figure it out?": "Rozgryzłaś to?",
    "It's 'bigman'!": "To „bigman”!",
    "Wow, that’s a good chunk of change.": "Łał, niezła sumka.",
    "For the sake of the public good, I’ll be sure to put that to good use.": "Dla dobra publicznego dopilnuję, by dobrze to wykorzystać.",
    "And this is… an ECU?": "A to jest… ECU?",
    "An ECU?": "ECU?",
    "It’s a computer for the car… Sometimes criminals swap them out to keep guys like me from grabbing their car’s logs.": "To komputer do auta… Czasem przestępcy je podmieniają, by tacy jak ja nie dorwali logów z auta.",
    "I wonder if this is the culprit.": "Ciekawe, czy to winowajca.",
    "Let’s see what happens when I swap the ECU.": "Zobaczmy, co się stanie, gdy podmienię ECU.",
    "This is harder than I thought… and it’s so hot in here.": "To trudniejsze, niż myślałem… i tak tu gorąco.",
    "Why don’t you make yourself more comfortable?": "Czemu się nie rozbierzesz, by było wygodniej?",
    "Oh, hubba, hubba!": "O, hubba, hubba!",
    "Ha.": "Ha.",
    "Knowing that the car was owned by a Guild member…": "Wiedząc, że auto należało do członka Gildii…",
    "Just what I suspected… It’s not logging data correctly.": "Tak jak podejrzewałem… Nie loguje danych poprawnie.",
    "And that broke the car?": "I to zepsuło auto?",
    "Intricately designed systems are not meant to be hacked.": "Misterne systemy nie są przeznaczone do hakowania.",
    "Let this be a lesson… If you hack software to cheat the system, don’t blame the developer when bugs happen.": "Niech to będzie lekcja… Jeśli hakujesz oprogramowanie, by oszukać system, nie wiń developera, gdy pojawią się bugi.",
    "This sounds personal. Bad experience?": "Brzmi osobiście. Złe doświadczenie?",
    "Now to see if the car starts…": "Teraz sprawdzić, czy auto odpali…",
    "Thank you so much, 1Hero!": "Dziękuję ci tak bardzo, 1Hero!",
    "That was much harder than it should have been, but we did it.": "To było dużo trudniejsze, niż powinno, ale daliśmy radę.",
    "This calls for a celebration.": "To zasługuje na świętowanie.",
    "Anything for my sweetheart.": "Wszystko dla mojej ukochanej.",
    "Yep, doesn’t start. I wonder what it could be?": "Tak, nie odpala. Ciekawe, co to może być?",
    "Perhaps there’s an owner’s manual in the glove box…": "Może w schowku jest instrukcja obsługi…",
    "These look like coordinates.": "To wyglądają jak współrzędne.",
    "What could be at this location? And why are they in the car’s glove box?": "Co może być w tym miejscu? I dlaczego są w schowku auta?",
    "I found something in the glove box.": "Znalazłem coś w schowku.",
    "Do you know what these coordinates are for?": "Wiesz, do czego są te współrzędne?",
    "No, dear, I don’t. I’m sorry.": "Nie, kochanie, nie wiem. Przykro mi.",
    "They must have been in there from the previous owner. I bought it as a used car.": "Musiały tam zostać po poprzednim właścicielu. Kupiłam jako używane.",
    "You think it has something to do with the car not working?": "Myślisz, że ma to coś wspólnego z tym, że auto nie działa?",
    "Unlikely, but it’s got my detective nature curious. Might be worth checking out.": "Wątpliwe, ale zaintrygowało moją detektywistyczną naturę. Może warto sprawdzić.",
    "There’s my little detective.": "Oto mój mały detektyw.",
    "Big detective, now.": "Duży detektyw, teraz.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=240 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=66: raise SystemExit(f'Expected 66, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map240')
