#!/usr/bin/env python3
"""Build Polish drafts for Map 56 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map56-followups-01.jsonl'
TRANSLATIONS = {
    "Sounds like Sister Judy.": "Brzmi jak siostra Judy.",
    "1Hero. I sense some conflict in your mind.": "1Hero. Wyczuwam w tobie rozterkę.",
    "Arianna… Were you meant to be found by Sister Judy?": "Arianna… Czy siostra Judy miała cię odnaleźć?",
    "There are no mistakes in God's will. You are the one who found the Oracle and you are the one I will guide.": "W woli Boga nie ma przypadków. To ty odnalazłeś Wyrocznię i to ciebie będę prowadzić.",
    "I trust you, Arianna. I hope I’m doing the right thing.": "Ufam ci, Arianno. Mam nadzieję, że robię dobrze.",
    "I will always tell you the truth. I am incapable of anything else.": "Zawsze powiem ci prawdę. Nie potrafię inaczej.",
    "It’s getting late… Is it too late to help Carol out with the tractor?": "Robi się późno… Czy nie jest za późno, by pomóc Carol przy traktorze?",
    "The night is young.": "Noc jest młoda.",
    "No sign of the nun. Let’s hurry.": "Ani śladu zakonnicy. Pospieszmy się.",
    "You’re crazy, Nellie.": "Zwariowałaś, Nellie.",
    "Sorry, Father. I went into the woods without telling you.": "Przepraszam, ojcze. Poszłam do lasu, nie mówiąc ci.",
    "I thought you went to Chloe’s house.": "Myślałem, że poszłaś do domu Chloe.",
    "It’s all good now. I think we had a little mixup.": "Już wszystko dobrze. Chyba mieliśmy małe nieporozumienie.",
    "You need to be careful, Sister Judy. There are lots of dangers out there.": "Musisz uważać, siostro Judy. Na zewnątrz czyha wiele niebezpieczeństw.",
    "I know, Father. I won’t do it again.": "Wiem, ojcze. Już tego nie zrobię.",
    "Let’s hope that officers ward off those criminals.": "Miejmy nadzieję, że funkcjonariusze odstraszą tych przestępców.",
    "I’m going to do everything I can to end this soon.": "Zrobię wszystko, co w mojej mocy, by wkrótce to zakończyć.",
    "I will pray for it.": "Będę się o to modlić.",
    "I… I should get back to my studies.": "Ja… Ja powinnam wrócić do nauki.",
    "Chloe left not long ago. Are you looking for her?": "Chloe wyszła niedawno. Szukasz jej?",
    "Another evening visit from 1Hero. How wonderful.": "Kolejna wieczorna wizyta 1Hero. Jak cudownie.",
    "It’s good to see you again too, Sister Judy.": "Ciebie też miło znów widzieć, siostro Judy.",
    "Hopefully you don't have to save me from any spiders this time.": "Mam nadzieję, że tym razem nie będziesz musiał ratować mnie przed pająkami.",
    "Haha, I'm your knight in shining armor.": "Haha, jestem twoim rycerzem w lśniącej zbroi.",
    "Would you like to stay a while? I sure do enjoy your company.": "Zostaniesz na chwilę? Naprawdę lubię twoje towarzystwo.",
    "I’d like that, but I have somewhere to be. Maybe later this evening?": "Chciałbym, ale muszę być gdzie indziej. Może później wieczorem?",
    "I’ll look forward to it.": "Będę czekać.",
    "I look forward to spending time with you this evening.": "Nie mogę się doczekać, by spędzić z tobą wieczór.",
    "Judy? Are you okay?": "Judy? Wszystko w porządku?",
    "Have any luck?": "Miałaś szczęście?",
    "No sign of her yet. But I’ll keep looking.": "Jeszcze ani śladu. Ale będę szukać dalej.",
    "I’ve dealt with my share of difficult women in my life, but this Madalyn woman sounds like more than a handful.": "Miałem do czynienia z trudnymi kobietami w życiu, ale ta Madalyn to chyba coś więcej niż trudny orzech do zgryzienia.",
    "I better study up on exorcism.": "Lepiej podszkolę się z egzorcyzmów.",
    "Well if it isn’t 1Hero.": "No proszę, a toż to 1Hero.",
    "Uhh… Hi, Father Solomon.": "Yyy… Cześć, ojcze Solomonie.",
    "And what brings you here to the church on this lovely evening?": "I co sprowadza cię o tej pięknej porze do kościoła?",
    "Just saying hi to Sister Judy.": "Tak tylko wpadłem przywitać się z siostrą Judy.",
    "Of course… of course. A young handsome man like you I’m sure puts Sister Judy’s mind at ease just before bedtime.": "Oczywiście… oczywiście. Przystojny młodzieniec jak ty na pewno koi myśli siostry Judy przed snem.",
    "You know me… I’m here to help.": "Znasz mnie… Jestem tu, by pomóc.",
    "A detective and a gentleman.": "Detektyw i dżentelmen.",
    "Let me smell your fingers.": "Daj powąchać palce.",
    "Hahahahahaha! You should see your face.": "Hahahahahaha! Powinieneś zobaczyć swoją minę.",
    "No worries, 1Hero. I’m sure you’re a better man than me at your age.": "Spoko, 1Hero. Jestem pewien, że jesteś lepszym człowiekiem niż ja w twoim wieku.",
    "Ha. Right.": "Ha. Jasne.",
    "That’s not the kind of joke I’d expect to hear from an ordained priest of the church.": "Nie tego żartu spodziewałbym się po wyświęconym kapłanie.",
    "Well, I'm not a typical priest.": "Cóż, nie jestem typowym księdzem.",
    "I'm starting to wonder just how wild your past really was.": "Zaczynam się zastanawiać, jak dzika była twoja przeszłość.",
    "I've done things a man your age has probably never even heard of.": "Robiłem rzeczy, o jakich chłopak w twoim wieku pewnie nawet nie słyszał.",
    "My ex-wife was a wildcat...": "Moja była żona to była dzika kotka…",
    "She was so flexible, she could do any position in the Kama Sutra.": "Była tak giętka, że potrafiła każdą pozycję z Kamasutry.",
    "Let me ask you, 1Hero. Have you ever done an upside down cowgirl?": "Powiedz mi, 1Hero. Próbowałeś kiedyś odwróconej kowbojki?",
    "Gravity defying, I tell ya.": "Przeczące grawitacji, mówię ci.",
    "How she never got pregnant, I’ll never know. It’s a miracle.": "Jak nigdy nie zaszła w ciążę, nigdy nie zrozumiem. To cud.",
    "Sounds like you got lucky.": "Brzmi, jakbyś miał szczęście.",
    "Did I?": "Miałem?",
    "Well… Did you want a child of your own?": "Cóż… Chciałeś mieć własne dziecko?",
    "I think I would have been a good father.": "Myślę, że byłbym dobrym ojcem.",
    "You seem like you would have made for a cool dad.": "Wydajesz się, że byłbyś spoko tatą.",
    "But then again, the Lord guided me here. Who am I to question His will?": "Ale z drugiej strony, Pan poprowadził mnie tutaj. Kimże jestem, by kwestionować Jego wolę?",
    "You're a good man, Father Solomon.": "Jesteś dobrym człowiekiem, ojcze Solomonie.",
    "Don't worry about Judy. I'll protect her.": "Nie martw się o Judy. Będę jej chronił.",
    "Oh, uhh... Yeah. Of course. Sister Judy needs our help.": "Och, yyy… Tak. Oczywiście. Siostra Judy potrzebuje naszej pomocy.",
    "She has a complicated past with that woman, Madalyn. It's really done a number on her.": "Ma skomplikowaną przeszłość z tą kobietą, Madalyn. To naprawdę ją wykończyło.",
    "Whatever's happening here in North Santiva, I'll get to the bottom of it.": "Cokolwiek dzieje się tu w North Santiva, dojdę do sedna.",
    "I don’t mean to interrupt you two. But, 1Hero… Your clothes are dry.": "Nie chcę wam przerywać. Ale, 1Hero… Twoje ubrania są suche.",
    "As much as I’d love to stay, I need to get going.": "Choć chciałbym zostać, muszę ruszać.",
    "Wait. Father Solomon wanted me to make sure you don’t leave before he gets back.": "Poczekaj. Ojciec Solomon chciał, żebym dopilnowała, byś nie wyszedł, zanim wróci.",
    "Are you going to try and stop me?": "Spróbujesz mnie zatrzymać?",
    "Oh, dear…": "Ojej…",
    "Everything looks fine down here.": "Na dole wszystko wygląda dobrze.",
    "Check your bedroom, Sister Judy. The leak is right above your room.": "Sprawdź swoją sypialnię, siostro Judy. Przeciek jest dokładnie nad twoim pokojem.",
    "Oh, no.": "O nie.",
    "It may be several days before mass, but it takes time to prepare.": "Do mszy jeszcze kilka dni, ale przygotowania zajmują czas.",
    "The church sure is beautiful.": "Kościół jest naprawdę piękny.",
    "I saw her go outside… I should get back to my studies.": "Widziałam, jak wychodzi… Powinnam wrócić do nauki.",
    "Do you think you’ll stay in the cathedral tonight?": "Myślisz, że zostaniesz dziś na noc w katedrze?",
    "I suppose it’s safe now… But I sure had fun with Chloe at her place…": "Chyba teraz jest bezpiecznie… Ale świetnie się bawiłam z Chloe u niej…",
    "And with you at yours.": "I z tobą u ciebie.",
    "I’m sure Father Solomon is lonely without you.": "Jestem pewien, że ojciec Solomon jest samotny bez ciebie.",
    "You’re right. But I do hope you’ll visit.": "Masz rację. Ale mam nadzieję, że odwiedzisz.",
    "Of course I will.": "Oczywiście, że odwiedzę.",
    "Will you stay nearby?": "Zostaniesz w pobliżu?",
    "I don’t mean to keep you. I know you must get to the mansion with Father.": "Nie chcę cię zatrzymywać. Wiem, że musisz jechać do rezydencji z ojcem.",
    "Haha. It’s only the restroom. How long could it take?": "Haha. To tylko toaleta. Jak długo może to potrwać?",
    "This is kinda weird. But I guess it’s better safe than sorry.": "To trochę dziwne. Ale chyba lepiej dmuchać na zimne.",
    "Jesus… How much did she drink?": "Jezu… Ile ona wypiła?",
    "Judy? Are you okay in there?": "Judy? Wszystko w porządku tam w środku?",
    "One moment.": "Chwileczkę.",
    "Finally.": "Wreszcie.",
    "1Hero?": "1Hero?",
    "We’re out of toilet paper.": "Skończył się papier toaletowy.",
    "Do you need it?": "Potrzebujesz?",
    "Could you get some for me?": "Mógłbyś mi przynieść?",
    "Yes, Sister Judy. I will only be gone a moment.": "Tak, siostro Judy. Będę tylko chwilę.",
    "Arianna!": "Arianna!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=56 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=95: raise SystemExit(f'Expected 95, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map56')
