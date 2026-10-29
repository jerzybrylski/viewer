#!/usr/bin/env python3
"""Build Polish drafts for Map 55 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map55-followups-02.jsonl'
TRANSLATIONS = {
    "Have you seen my coif?": "Widziałaś może mój czepiec?",
    "What’s a coif?": "Co to jest czepiec?",
    "My hat.": "Mój czepek.",
    "Sorry, Sister Judy, I’ve not seen it.": "Przepraszam, siostro Judy, nie widziałam go.",
    "What’s going on down there?": "Co się tam na dole dzieje?",
    "We found a basement… But it’s dark. You better stay up here.": "Znaleźliśmy piwnicę… Ale jest ciemno. Lepiej zostań tutaj na górze.",
    "1Hero… I should really get back to my studies.": "1Hero… Naprawdę powinnam wrócić do nauki.",
    "I must confess, I told Chloe about our little bedroom fun.": "Muszę wyznać, opowiedziałam Chloe o naszej małej zabawie w sypialni.",
    "I’m sure Chloe will have a story for you too.": "Jestem pewna, że Chloe też będzie miała dla ciebie jakąś historię.",
    "It’s dark.": "Jest ciemno.",
    "I’m devoted to God, but accepting the touch of a man… It makes me feel like a bad nun.": "Jestem oddana Bogu, ale przyjmowanie dotyku mężczyzny… Sprawia, że czuję się jak zła zakonnica.",
    "You’re a good woman, Sister Judy. You care for people, and that counts for something.": "Jesteś dobrą kobietą, siostro Judy. Troszczysz się o ludzi i to się liczy.",
    "I’ve enjoyed your company, but I think I need a moment to myself. There is much to process.": "Miło spędziłam z tobą czas, ale potrzebuję chwili dla siebie. Mam wiele do przemyślenia.",
    "I understand. I’m here for you whenever you need someone to talk to.": "Rozumiem. Jestem przy tobie, kiedy tylko będziesz potrzebować z kimś porozmawiać.",
    "Have a good night, Sister Judy.": "Dobranoc, siostro Judy.",
    "Good night, 1Hero.": "Dobranoc, 1Hero.",
    "I hope Arianna finds Erica soon.": "Mam nadzieję, że Arianna szybko znajdzie Ericę.",
    "I hope Erica's soul is safe.": "Mam nadzieję, że dusza Eriki jest bezpieczna.",
    "How are you two feeling?": "Jak się czujecie we dwójkę?",
    "This felt… right.": "To było… właściwe.",
    "It’s so nice to know there is a way to fight the evil urges without committing sinful sex.": "Tak miło wiedzieć, że istnieje sposób, by walczyć ze złymi pokusami bez popełniania grzesznego seksu.",
    "So, this is okay to do?": "Więc to wolno robić?",
    "We are not indulging in the sinful act. Right, 1Hero?": "Nie oddajemy się grzesznemu aktowi. Prawda, 1Hero?",
    "I don’t know much about religion, but I can tell you that masturbation isn’t sex.": "Nie znam się zbyt dobrze na religii, ale mogę ci powiedzieć, że masturbacja to nie seks.",
    "See, Chloe?": "Widzisz, Chloe?",
    "Sure… I guess that makes sense.": "Jasne… Chyba to ma sens.",
    "Thank you for your visit, 1Hero.": "Dziękuję za odwiedziny, 1Hero.",
    "Chloe, do you want me to walk you home?": "Chloe, chcesz żebym odprowadziła cię do domu?",
    "That would be nice.": "Byłoby miło.",
    "Please be safe. It’s getting late.": "Uważajcie na siebie. Robi się późno.",
    "Don’t worry, Sister. I’ll protect her.": "Nie martw się, siostro. Będę ją chronić.",
    "1Hero’s so brave.": "1Hero jest taki odważny.",
    "And strong!": "I silny!",
    "See you later, Sister Judy.": "Do zobaczenia później, siostro Judy.",
    "How much longer do I have to wait for the shower to open?": "Jak długo jeszcze mam czekać, aż zwolni się prysznic?",
    "I hope she’s not using all the hot water.": "Mam nadzieję, że nie zużywa całej ciepłej wody.",
    "Sister Judy is back already?": "Siostra Judy już wróciła?",
    "I wonder if she wants to have some fun while Father’s away.": "Ciekawe, czy chce się trochę zabawić, gdy nie ma ojca.",
    "1Hero!? I thought the nun was in here.": "1Hero!? Myślałam, że zakonnica jest w środku.",
    "Damn, Nellie. Nice… tats.": "Nieźle, Nellie. Fajne… tatuaże.",
    "Nice cock, studmuffin.": "Niezły kutas, ciacho.",
    "Are you done with the shower? What’s taking so long?": "Skończyłaś już z prysznicem? Co tak długo trwa?",
    "I’ve not even started.": "Jeszcze nawet nie zaczęłam.",
    "Why don’t we shower together?": "Może weźmiemy razem prysznic?",
    "Erica?": "Erica?",
    "Can you ladies keep an eye on her?": "Możecie, panie, mieć na nią oko?",
    "What’s wrong with her?": "Co się z nią dzieje?",
    "She’s… Not all there.": "Ona… Nie jest do końca sobą.",
    "I feel warmer.": "Czuję się cieplej.",
    "That’s a plus!": "To plus!",
    "We need to regulate her body temperature?": "Musimy uregulować temperaturę jej ciała?",
    "I feel dry.": "Czuję suchość.",
    "Don’t overthink it. Just make sure she doesn’t hurt herself.": "Nie rozkminiaj tego. Po prostu upewnij się, że nie zrobi sobie krzywdy.",
    "We’ll have her better in no time.": "Zaraz postawimy ją na nogi.",
    "Can’t say I understand; but if I can keep Hannah alive, I can keep this girl alive.": "Nie mówię, że rozumiem, ale skoro potrafiłam utrzymać Hannah przy życiu, to i tę dziewczynę utrzymam.",
    "We’ll make sure she’s safe.": "Dopilnujemy, żeby była bezpieczna.",
    "I will stay by her side as well.": "Ja też zostanę przy niej.",
    "Thank you, ladies.": "Dziękuję, panie.",
    "Well, this isn’t good.": "Cóż, to nie wygląda dobrze.",
    "Everything’s all wet!": "Wszystko jest mokre!",
    "My bedroom.": "Moja sypialnia.",
    "It’ll take a while to clean up this mess.": "Sprzątanie tego bałaganu chwilę zajmie.",
    "But it’s so late. Where are you going to sleep, Sister Judy?": "Ale jest tak późno. Gdzie będziesz spać, siostro Judy?",
    "I… I don’t know what I’m going to do.": "Ja… Nie wiem, co zrobię.",
    "Well… You can…": "Cóż… Możesz…",
    "You can stay with me!": "Możesz zostać u mnie!",
    "At your home?": "U ciebie w domu?",
    "Yeah! I’d love to show you my place.": "Tak! Chętnie pokażę ci moje miejsce.",
    "That’s mighty nice of you, Chloe.": "To bardzo miło z twojej strony, Chloe.",
    "Father, if you have a moment, I’d like to speak to you.": "Ojcze, jeśli masz chwilę, chciałabym z tobą porozmawiać.",
    "We did.": "Udało się.",
    "Thank you so much, Chloe. You are a life-saver.": "Dziękuję ci bardzo, Chloe. Ratujesz mi życie.",
    "I’m sure my mom would love to meet you too.": "Jestem pewna, że moja mama też chętnie cię pozna.",
    "Don’t worry, Judy. We’ll help you clean up your room once things dry up.": "Nie martw się, Judy. Pomożemy ci posprzątać pokój, gdy wszystko wyschnie.",
    "Thank you all for your generosity.": "Dziękuję wam wszystkim za hojność.",
    "Maybe 1Hero would like to come over to my place too.": "Może 1Hero też chciałby wpaść do mnie.",
    "Really!? I’d love to spend an evening with you two.": "Naprawdę!? Chętnie spędzę z wami wieczór.",
    "Yeah. It’ll be fun. We’ll keep your mind off of this leak.": "Tak. Będzie fajnie. Odwrócimy twoje myśli od tego wycieku.",
    "Did you find what you needed, 1Hero?": "Znalazłeś to, czego potrzebowałeś, 1Hero?",
    "We did. Father Zephaniah had a secret safe…": "Tak. Ojciec Zephaniah miał tajny sejf…",
    "We just need to figure out how to open it.": "Musimy tylko wymyślić, jak go otworzyć.",
    "I hope you find what you’re looking for.": "Mam nadzieję, że znajdziecie to, czego szukacie.",
    "Come on, Judy. Let’s get out of here.": "Chodź, Judy. Wynośmy się stąd.",
    "It smells so bad!": "Tak śmierdzi!",
    "We need some bleach.": "Potrzebujemy wybielacza.",
    "No, not bleach… We can clean it with something else that won't damage the carpet or sheets.": "Nie, nie wybielacza… Możemy to wyczyścić czymś innym, co nie zniszczy dywanu ani pościeli.",
    "I’ll find something.": "Znajdę coś.",
    "It smells so bad. I hope we can clean it.": "Tak śmierdzi. Mam nadzieję, że uda nam się to wyczyścić.",
    "You know, we have a bed here.": "Wiesz, mamy tu łóżko.",
    "You’re welcome to join us.": "Możesz do nas dołączyć.",
    "Haha, another time.": "Haha, innym razem.",
    "Erica’s not much of a talker.": "Erica nie jest zbyt rozmowna.",
    "She’s sick. But we’ll fix her up real soon.": "Jest chora. Ale szybko ją wyleczymy.",
    "Poor Judy. I hope we can help her.": "Biedna Judy. Mam nadzieję, że możemy jej pomóc.",
    "I want to go see the basement, but I know Judy would follow me.": "Chcę zobaczyć piwnicę, ale wiem, że Judy poszłaby za mną.",
    "Afraid she’ll get hurt?": "Boisz się, że zrobi sobie krzywdę?",
    "You found a basement?": "Znalazłeś piwnicę?",
    "A small one, yeah.": "Małą, tak.",
    "Anything cool down there?": "Coś fajnego tam na dole?",
    "Just a bunch of old, dusty junk as far as I can see.": "O ile widzę, tylko sterta starych, zakurzonych gratów.",
    "I feel an urge to go see this basement… But I know it’s too dangerous.": "Kusi mnie, żeby zobaczyć tę piwnicę… Ale wiem, że to zbyt niebezpieczne.",
    "1Hero! Look… There is a door!": "1Hero! Patrz… Tam są drzwi!",
    "That’s odd. Looks like a crawl space… but this church doesn't have a crawlspace.": "To dziwne. Wygląda jak schowek pod podłogą… Ale ten kościół nie ma takiej przestrzeni.",
    "Is there a basement?": "Czy tu jest piwnica?",
    "I guess it’s possible.": "Chyba to możliwe.",
    "Looks like a staircase that goes down to a dark space.": "Wygląda jak schody prowadzące w dół do ciemnej przestrzeni.",
    "There is a basement under my bedroom?": "Pod moją sypialnią jest piwnica?",
    "It wouldn’t be the first surprise I’ve found in this place.": "To nie byłaby pierwsza niespodzianka, jaką znalazłam w tym miejscu.",
    "Stay here. 1Hero and I will check it out.": "Zostań tutaj. 1Hero i ja to sprawdzimy.",
    "What’s going on, Sister Judy?": "Co się dzieje, siostro Judy?",
    "I’m reading the bible.": "Czytam Biblię.",
    "You’ve not read it yet?": "Jeszcze jej nie czytałaś?",
    "I read it all the time. Don’t you read the bible?": "Czytam ją cały czas. Nie czytasz Biblii?",
    "Is it really gonna be alright, 1Hero?": "Naprawdę będzie dobrze, 1Hero?",
    "Don’t worry, Carol. We’ll get through this.": "Nie martw się, Carol. Poradzimy sobie.",
    "I hardly slept last night. Maybe Erica’s sleepy.": "Prawie nie spałam w nocy. Może Erica jest śpiąca.",
    "It’s more complicated than that.": "To bardziej skomplikowane.",
    "I hardly slept last night.": "Prawie nie spałam ostatniej nocy.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=55 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=translations.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=118: raise SystemExit(f'Expected 118, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map55')