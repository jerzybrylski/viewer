#!/usr/bin/env python3
"""Build a small reviewed-draft batch for five additional Common Events."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl')

EVENTS = {
    340: {
        "Looks like a bunch of antique sculptures.": "Wyglądają na stare rzeźby.",
        "This place hasn’t been cleaned in a very long time.": "Od bardzo dawna nikt tu nie sprzątał.",
        "This is a Guild bunker. We’ve seen ones like this before.": "To bunkier Gildii. Widzieliśmy już podobne.",
        "How can you tell?": "Skąd wiesz?",
        "This is an inventory list…": "To spis inwentarza…",
        "Everything in this place is stolen.": "Wszystko tutaj jest kradzione.",
        "Shit! You must have set off some sort of trap.": "Cholera! Musiałeś uruchomić jakąś pułapkę.",
        "I didn’t touch anything.": "Nic nie dotykałem.",
        "There’s enough space. We may be able to squeeze back through.": "Jest tu dość miejsca. Może uda nam się przecisnąć z powrotem.",
        "Dammit. I can’t see if the entrance is shut or not.": "Cholera, nie widzę, czy wejście jest zamknięte.",
        "Help me get through.": "Pomóż mi się przedostać.",
        "Push me through!": "Przepchnij mnie!",
        "Okay, fine.": "Dobra, już.",
        "We’re trapped. The main entryway is sealed shut.": "Jesteśmy uwięzieni. Główne wejście jest zablokowane.",
        "Help me back through. We have to find a way out of here.": "Pomóż mi wrócić. Musimy znaleźć wyjście.",
        "Put some muscle behind it!": "Użyj trochę siły!",
        "This isn’t easy!": "To nie takie łatwe!",
        "Well, this didn’t work out as expected.": "No cóż, nie tak miało to wyglądać.",
        "Let’s find a way out of this mess…": "Znajdźmy wyjście z tej pułapki…",
        "And don’t disturb anything.": "I niczego nie ruszaj.",
        "We don’t want Lillian knowing we were here.": "Nie chcemy, żeby Lillian wiedziała, że tu byliśmy.",
        "If we can’t find a way out, we may hope that she does know we’re in here.": "Jeśli nie znajdziemy wyjścia, pozostanie nam mieć nadzieję, że wie, że tu jesteśmy.",
    },
    354: {
        "What the…?": "Co do…?",
        "Holy shit!...": "Ja pierdolę!...",
        "That naughty woman… What a hypocrite.": "Ta niegrzeczna kobieta… Co za hipokrytka.",
        "This is gold.": "To jest złoto.",
        "Looks like I’m not the only one defiling the workspace with sexual antics.": "Wygląda na to, że nie tylko ja urządzam sobie seksualne harce w pracy.",
        "How long has she been doing this?": "Jak długo już to robi?",
        "I was starting to wonder if Melissa had a sexual side to her…": "Zaczynałem się zastanawiać, czy Melissa ma w sobie jakąś erotyczną stronę…",
        "She’s such a tight-ass, I was beginning to think she had no ability to feel horny.": "Jest taką sztywniarą, że zaczynałem myśleć, iż w ogóle nie potrafi się podniecić.",
        "Damn, what a dirty girl!": "Cholera, ale z niej niegrzeczna dziewczynka!",
        "What’s she watching?...": "Co ona ogląda?…",
        "I can tell she’s looking at her monitor. Maybe if I just peek my head in…": "Widzę, że patrzy w monitor. Może tylko zajrzę…",
        "Oh!... my!... god!": "O… mój… Boże!",
        "No way! Is she really fingering herself to the interview?": "Nie wierzę! Naprawdę masturbuje się do wywiadu?",
        "Holy hell! She’s nasty as fuck!": "O rany! Ale z niej zboczucha!",
        "What’s getting her off? Could it be me?... Maybe Kimberly?... Or Andrea?": "Co ją tak podnieca? Może ja?... Kimberly?... A może Andrea?",
        "Is she into other women? Or is it possible…": "Pociągają ją kobiety? A może…",
        "She finds me hot?": "Uważa, że jestem seksowny?",
        "But… She hates my guts. Why would she be fingering herself while thinking about me?": "Ale… Przecież mnie nienawidzi. Czemu miałaby się masturbować, myśląc o mnie?",
        "Damn! She’s really going for it.": "Cholera! Ale się rozkręciła.",
        "1Hero!?": "1Hero!?",
        "Shit! Melissa!": "Cholera! Melissa!",
        "What the hell are you doing!? Close the door!": "Co ty, do cholery, wyprawiasz!? Zamknij drzwi!",
    },
    359: {
        "Maybe it’s the alcohol speaking, but I sure do find myself attracted to younger men these days.": "Może to alkohol, ale ostatnio coraz bardziej podobają mi się młodsi mężczyźni.",
        "With chiseled abs?": "Z wyrzeźbionymi mięśniami brzucha?",
        "Don’t flatter yourself, softy.": "Nie pochlebiaj sobie, mięczaku.",
        "Soft isn’t exactly how I’d describe myself right now.": "Nie powiedziałbym, że teraz jestem miękki.",
        "Ohhh. You’re pushing it now, aren’t you?": "Oho. Zaczynasz przesadzać, co?",
        "Oops. Looks like I forgot something.": "Ups. Chyba o czymś zapomniałem.",
        "Not worried about Kimura coming back?": "Nie boisz się, że Kimura wróci?",
        "She left us alone for a reason. I think she’d quite like it if you and I got to know each other… personally.": "Zostawiła nas samych nie bez powodu. Chyba chciałaby, żebyśmy poznali się bliżej… osobiście.",
        "Oh, yes! Mr. Canmore!": "Och, tak, panie Canmore!",
        "You’re wet, Miss Foxx.": "Jesteś mokra, panno Foxx.",
        "Let’s hope Andrea takes her time.": "Oby Andrea nie spieszyła się z powrotem.",
        "I want you to cum for me, Kimberly.": "Chcę, żebyś dla mnie doszła, Kimberly.",
        "It’s going to take more than that to make me cum.": "Nie wystarczy tyle, żebym doszła.",
        "Too bad I don’t have time to really explore this juicy pussy of yours.": "Szkoda, że nie mam czasu dokładniej poznać tej twojej soczystej cipki.",
        "Oh, fuck yes! Use that tongue of yours!": "O, kurwa, tak! Użyj języka!",
        "You’re a lucky boy… getting a taste of heaven.": "Masz szczęście, chłopcze… możesz zakosztować nieba.",
        "Ah! You’re making my head spin…": "Ach! Kręci mi się w głowie…",
        "I’ve not felt like this in a while.": "Dawno się tak nie czułam.",
        "Whatever you’re doing to me, it’s working.": "Cokolwiek ze mną robisz, działa.",
        "I guess I’ve got something you need.": "Chyba mam coś, czego potrzebujesz.",
        "Let’s fuck.": "Pieprzmy się.",
        "Am I interrupting something?": "Czy w czymś przeszkadzam?",
    },
    440: {
        "What happened to doing real work?...": "A co z prawdziwą pracą?...",
        "You must need a break.": "Pewnie potrzebujesz przerwy.",
        "Not that I’m complaining…": "Nie żebym narzekała…",
        "Oh, yes… That mouth of yours is always welcome on my cock.": "Och, tak… Twoje usta zawsze są mile widziane na moim kutasie.",
        "God, I needed this cock!": "Boże, tak bardzo potrzebowałam tego kutasa!",
        "What’s gotten into you, Melissa?...": "Co w ciebie wstąpiło, Melissa?...",
        "You were a bitch moments ago, and now you’re… extra friendly.": "Przed chwilą byłaś suką, a teraz… jesteś wyjątkowo miła.",
        "Shut the fuck up and give me that cock!": "Zamknij się, do cholery, i daj mi tego kutasa!",
        "God! Make me cum, baby!": "Boże! Doprowadź mnie do orgazmu, kochanie!",
        "Yes! My pussy is tingling!": "Tak! Aż mi cipka pulsuje!",
        "Taste my dripping wet pussy, 1Hero!": "Skosztuj mojej mokrej cipki, 1Hero!",
        "You love it! I know you love my juicy cunt!": "Podoba ci się! Wiem, że uwielbiasz moją soczystą cipkę!",
        "I want you! I need you!": "Chcę cię! Potrzebuję cię!",
        "Give it to me! Give me pleasure!": "Daj mi to! Daj mi rozkosz!",
        "Lillian!": "Lillian!",
        "… Oh, fuck!": "… Och, kurwa!",
        "It feels so good… Why are you doing this?": "Ale to przyjemne… Czemu to robisz?",
        "You’re trying to make me cum…": "Chcesz doprowadzić mnie do orgazmu…",
        "She wants my cum!": "Ona chce mojej spermy!",
        "Lillian! Stop!... Wait!": "Lillian! Przestań!... Czekaj!",
        "What the fuck!": "Co do cholery!",
        "Jesus! What the hell happened?": "Jezu! Co tu się, do cholery, stało?",
    },
    122: {
        "Hey, you!": "Hej, ty!",
        "Sup, dude.": "Siema, stary.",
        "Hey, man.": "Hej, stary.",
        "Scram! I’ve got things to do.": "Spadaj! Mam co robić.",
        "Go away! I’m busy.": "Odczep się! Nie mam czasu.",
        "Get back, dude! I don’t have time for you.": "Zjeżdżaj, stary! Nie mam dla ciebie czasu.",
        "Busy right now. Come back later.": "Nie teraz. Wróć później.",
        "Got things going on. Check back later.": "Mam teraz sprawy na głowie. Wpadnij później.",
        "Thanks dude!": "Dzięki, stary!",
        "Thanks! I owe you one.": "Dzięki! Odwdzięczę ci się.",
        "Kick ass!": "Dajesz czadu!",
        "Oh, no. This isn’t good.": "O nie. To niedobrze.",
    },
}

known = {r['id'] for r in map(json.loads, MERGED.read_text(encoding='utf-8').splitlines()) if r['translation'].strip()}
for batch in (ROOT / 'drafts').glob('*.jsonl'):
    for line in batch.read_text(encoding='utf-8').splitlines():
        if line.strip():
            row = json.loads(line)
            if row.get('translation', '').strip():
                known.add(row['id'])

rows_by_event = {event_id: [] for event_id in EVENTS}
missing = set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    event_id = context.get('event_id')
    if context.get('source_kind') != 'common_event' or event_id not in EVENTS or row['id'] in known:
        continue
    source = ' '.join(row['source_text'].strip().split())
    if not source or source.startswith('/') or source in {'…', '...', '..'} or not any(char.isalpha() for char in source):
        continue
    translation = EVENTS[event_id].get(source)
    if translation is None:
        translation = EVENTS[event_id].get(source.replace('’', "'"))
    if translation is None:
        translation = EVENTS[event_id].get(source.replace("'", '’'))
    if translation is None:
        missing.add((event_id, source))
        continue
    row['translation'] = translation
    rows_by_event[event_id].append(row)
if missing:
    raise SystemExit('Unmapped strings: ' + repr(sorted(missing)))
for event_id, rows in rows_by_event.items():
    if not rows:
        continue
    path = ROOT / f'drafts/custom-dialogue-common-event-{event_id}-01.jsonl'
    if path.exists():
        raise SystemExit(f'Refusing to overwrite {path}')
    path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8', newline='\n')
    print(f'Wrote Common Event {event_id}: {len(rows)} records')
print(f'Total: {sum(map(len, rows_by_event.values()))} records across {sum(bool(rows) for rows in rows_by_event.values())} events')
