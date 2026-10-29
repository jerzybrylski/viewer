import json
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl')
EVENTS = {
    14: {
        "I hope we didn’t push things too far at the creek.": "Mam nadzieję, że nad strumieniem nie posunęliśmy się za daleko.",
        "I don’t think that’s what Heather is worried about.": "Nie sądzę, żeby to martwiło Heather.",
        "It has something to do with a magic rock.": "To ma coś wspólnego z magicznym kamieniem.",
        "If you have any news on your case, I’d love to hear it.": "Jeśli masz jakieś wieści w sprawie, chętnie ich posłucham.",
        "I can only share so much, but if I find anything new I’ll let you know.": "Nie mogę zdradzić zbyt wiele, ale dam ci znać, jeśli czegoś się dowiem.",
        "Did you talk to Heather?": "Rozmawiałeś z Heather?",
        "All’s well.": "Wszystko w porządku.",
        "She didn’t say anything?": "Nic nie powiedziała?",
        "Would she have something to tell me?": "Miałaby mi coś do powiedzenia?",
        "No… Just… You know… She’s been acting kinda funny.": "Nie… Po prostu… Wiesz… Dziwnie się ostatnio zachowuje.",
        "Cause she’s worried about you. You know how much she cares about you.": "Bo się o ciebie martwi. Wiesz, jak bardzo jej na tobie zależy.",
        "Are the girls settled into Hannah’s room?": "Dziewczyny zadomowiły się w pokoju Hannah?",
        "It’s a small bed, but they can manage.": "Łóżko jest małe, ale dadzą sobie radę.",
        "You suspect any visits in the night?": "Podejrzewasz nocne odwiedziny?",
        "Judy won’t do that.": "Judy by tego nie zrobiła.",
        "She’s a nun.": "Jest zakonnicą.",
        "She’s also a woman.": "Ale jest też kobietą.",
        "Carol…": "Carol…",
        "I’m going up to change. The couch is all yours.": "Idę się przebrać. Kanapa jest do twojej dyspozycji.",
        "See ya later, Carol.": "Do zobaczenia, Carol.",
        "Guess we’re stuck here. That storm isn’t letting up.": "Chyba utknęliśmy. Burza nie odpuszcza.",
        "Might as well get to bed… It’s going to be an early morning tomorrow.": "Lepiej położyć się spać… Jutro trzeba wcześnie wstać.",
        "This isn’t the most comfortable couch.": "Ta kanapa nie jest zbyt wygodna.",
        "I wonder if Hannah is being nice to Judy…": "Ciekawe, czy Hannah jest miła dla Judy…",
        "I wonder what Heather’s doing right now.": "Ciekawe, co teraz robi Heather.",
        "What’s up with Carol? She’s hiding something.": "Co jest z Carol? Coś przede mną ukrywa.",
        "Ugh… I can’t sleep.": "Ugh… Nie mogę zasnąć.",
        "I need a snack.": "Przydałaby mi się przekąska.",
        "You better get to church. You’re running late.": "Lepiej idź już do kościoła. Spóźnisz się.",
        "Did you find Hannah?": "Znalazłeś Hannah?",
        "She went to Heather’s… In her underwear.": "Poszła do Heather… w samej bieliźnie.",
        "That girl is going to get herself into a lot of trouble.": "Ta dziewczyna narobi sobie kłopotów.",
        "I don’t need any help with dinner, but thanks for the offer.": "Nie potrzebuję pomocy przy kolacji, ale dziękuję za propozycję.",
        "Supper will be ready once you get back from the barn.": "Kolacja będzie gotowa, kiedy wrócisz ze stodoły.",
    },
    32: {
        "Thanks for helping us with the mess, 1Hero.": "Dzięki za pomoc w sprzątaniu, 1Hero.",
        "No problem, Carol.": "Nie ma sprawy, Carol.",
        "Any luck finding something?": "Udało ci się coś znaleźć?",
        "Yeah, this soot cleaner should do the trick.": "Tak, ten środek do czyszczenia sadzy powinien pomóc.",
        "Looks like 1Hero saved the day again.": "Wygląda na to, że 1Hero znów uratował sytuację.",
        "Where would we be without him?": "Co byśmy bez niego zrobiły?",
        "Sleeping in a stinky house, for one thing!": "Na przykład spałybyśmy w śmierdzącym domu!",
        "Alright, let’s get this done…": "Dobra, zabierajmy się do roboty…",
        "…before Hannah falls asleep from eating too much at Dick’s.": "…zanim Hannah zaśnie po obżarstwie u Dicka.",
        "I ain’t going to fall asleep. I can handle a big meal.": "Nie zasnę. Dam radę zjeść porządny posiłek.",
        "Let’s focus on cleaning for now.": "Na razie skupmy się na sprzątaniu.",
        "Just like new!": "Jak nowe!",
        "Hannah.": "Hannah.",
        "So much for your reward, whatever that was s’posed to be.": "Czyli nici z twojej nagrody, czymkolwiek miała być.",
        "No worries. I just like helping you ladies out.": "Nie szkodzi. Lubię wam pomagać.",
        "Nonsense. I think you should still get something for your troubles.": "Ależ skąd. I tak należy ci się coś za fatygę.",
        "How about you head up to my bedroom? I think you’ll like what you’ll find.": "Może wejdziesz do mojej sypialni? Chyba spodoba ci się to, co tam znajdziesz.",
        "Your bedroom?": "Do twojej sypialni?",
        "Up the stairs. I know you know where it is. Ya little snooper.": "Na górę po schodach. Wiem, że znasz drogę, mały podglądaczu.",
        "I hope my reward isn’t a cucumber.": "Mam nadzieję, że nagrodą nie będzie ogórek.",
        "You’ll just have to go up and see.": "Musisz wejść na górę i sam się przekonać.",
        "Don’t worry, 1Hero. I talked Heather down from the cliff.": "Nie martw się, 1Hero. Uspokoiłam Heather.",
        "I’d ask you what you said, but maybe I’d rather not know.": "Zapytałbym, co jej powiedziałaś, ale może lepiej nie wiedzieć.",
        "Having a fun evening, 1Hero?": "Miło spędzasz wieczór, 1Hero?",
        "Oh, she went home about an hour ago.": "Och, wróciła do domu jakieś godzinę temu.",
        "I heard you had quite the party at Heather’s house.": "Słyszałam, że u Heather była niezła impreza.",
    },
    13: {
        "1Hero! Girls only!": "1Hero! Wstęp tylko dla dziewczyn!",
        "Have fun, girls.": "Dobrej zabawy, dziewczyny.",
        "1Hero? What are you doing back?": "1Hero? Co ty tu znowu robisz?",
        "You better not flake on our pool party later.": "Lepiej nie wystaw nas później na imprezie przy basenie.",
        "Coming back for seconds?": "Wróciłeś po dokładkę?",
        "Sorry, Hannah. I can’t stay.": "Wybacz, Hannah. Nie mogę zostać.",
        "I hope you can fix the bathroom. I don’t want to have to go outside.": "Mam nadzieję, że naprawisz łazienkę. Nie chcę załatwiać się na dworze.",
        "The plumbing issues are fixed.": "Problemy z kanalizacją są już naprawione.",
        "Oh, thank God. I was getting worried.": "Och, dzięki Bogu. Zaczynałam się martwić.",
        "What are you doing outside? You’re going to catch a cold.": "Co robisz na dworze? Przeziębisz się.",
        "Oh, uhh… I was just looking for that goat.": "Och, eee… Szukałam tego kozła.",
        "I hope the little guy is okay.": "Mam nadzieję, że nic mu nie jest.",
        "1Hero?": "1Hero?",
        "I don’t feel so good.": "Nie czuję się najlepiej.",
        "Is it your stomach?": "Boli cię brzuch?",
        "I’m okay.": "Nic mi nie jest.",
        "Come here. Sit down.": "Chodź tutaj. Usiądź.",
    },
    46: {
        "Oh, thank God. It’s over.": "Och, dzięki Bogu. Już po wszystkim.",
        "If I told you it was a magic rock, would you believe me?": "Gdybym powiedział, że to przez magiczny kamień, uwierzyłabyś mi?",
        "What are you talking about? It’s like you were possessed.": "O czym ty mówisz? Zachowywałeś się, jakbyś był opętany.",
        "I had a dream last night…": "Miałem wczoraj w nocy sen…",
        "About this?": "O tym?",
        "There’s something really strange going on in the Casula forest.": "W lesie Casula dzieje się coś naprawdę dziwnego.",
        "Do you have a fever?": "Masz gorączkę?",
        "Let’s get dressed before Carol gets back.": "Ubierzmy się, zanim Carol wróci.",
        "It’s raining cats and dogs out there!": "Ale leje!",
        "Did Judy stay at the church?": "Judy została w kościele?",
        "She’s preparing for Mass.": "Przygotowuje się do mszy.",
        "Yeah. She’s reading and being boring.": "Tak. Czyta i jest nudna.",
        "You can afford to read a book or two, young lady.": "Tobie też przydałoby się przeczytać jakąś książkę, młoda damo.",
        "I learn from doing, not reading.": "Uczę się przez działanie, nie czytanie.",
        "It’s getting late. Are you ready to go home, Chloe?": "Robi się późno. Jesteś gotowa wracać do domu, Chloe?",
        "You’re not staying for lunch?": "Nie zostaniesz na lunch?",
        "I just… have a lot to do around the house today.": "Po prostu… mam dziś dużo do zrobienia w domu.",
        "But I was going to play with Hannah.": "Ale miałam się bawić z Hannah.",
        "You’re not a kid, Chloe.": "Nie jesteś już dzieckiem, Chloe.",
        "I’m fine. I just need to get going.": "Wszystko w porządku. Muszę już iść.",
        "Well, if there’s anything you need help with, let us know.": "Jeśli będziesz potrzebować pomocy, daj nam znać.",
        "Don’t stay out too late tonight, Chloe.": "Nie siedź dziś zbyt długo poza domem, Chloe.",
        "What the hell happened while we were gone?": "Co się, do cholery, stało, kiedy nas nie było?",
        "It’s nothing. Don’t worry about it.": "Nic takiego. Nie martw się.",
        "Leave the boy alone, girls. He’s busy.": "Dajcie chłopakowi spokój, dziewczyny. Jest zajęty.",
        "I should get going too.": "Ja też powinienem już iść.",
        "Don’t work on the weekend, 1Hero.": "Nie pracuj w weekend, 1Hero.",
        "There’s a lot going on with work. I should get going.": "Mam sporo spraw w pracy. Muszę już iść.",
        "You’re welcome back any time.": "Zawsze możesz do nas wpaść.",
        "Whatever happened here, it’s got Heather rattled.": "Cokolwiek się tu wydarzyło, Heather jest tym wstrząśnięta.",
    },
    58: {
        "Come for some lovin’, hunky man?": "Przyszedłeś po trochę czułości, przystojniaku?",
        "Heh, not today.": "Heh, nie dzisiaj.",
        "Actually, I wanted to ask you about… my dad.": "Właściwie chciałem zapytać cię o… mojego tatę.",
        "That’s depressing. Why talk about him?": "Ale ponury temat. Po co o nim rozmawiać?",
        "I’m trying to get into an old briefcase of his.": "Próbuję otworzyć jego stary neseser.",
        "There’s a code. To break it, I require some kind of special info, maybe a name or numbers.": "Jest zamknięty na szyfr. Żeby go złamać, potrzebuję jakiejś szczególnej informacji, może imienia albo liczb.",
        "Any idea what might have been special to young Kirk Chesterfield?": "Masz pomysł, co mogło być ważne dla młodego Kirka Chesterfielda?",
        "Kirk could be sentimental.": "Kirk bywał sentymentalny.",
        "There was a big party he was throwing. He was in rare form then, even for Kirk.": "Urządził kiedyś wielką imprezę. Nawet jak na Kirka był wtedy w wyjątkowym nastroju.",
        "Heather gave him a nickname during the party because of it.": "Heather nadała mu wtedy przezwisko.",
        "He immediately loved it, and started referring to himself that way for the rest of the party…": "Od razu mu się spodobało i przez resztę imprezy sam tak o sobie mówił…",
        "Wish I could remember it for you…": "Szkoda, że nie mogę sobie przypomnieć…",
        "Are you sure you can’t recall?": "Na pewno nic sobie nie przypominasz?",
        "I know that he loved it so much, he had a special license plate made that said it.": "Wiem, że tak mu się spodobało, że zamówił sobie specjalną tablicę rejestracyjną z tym napisem.",
        "Maybe if you could find that, you’d have what you need.": "Może jeśli ją znajdziesz, będziesz mieć potrzebną informację.",
        "A license plate…": "Tablica rejestracyjna…",
        "Alright, I’ll see what I can find.": "Dobrze, zobaczę, co uda mi się znaleźć.",
        "No problem, studmuffin. Don’t forget to come back and show me some sugar later.": "Nie ma sprawy, przystojniaku. Wpadnij później i okaż mi trochę czułości.",
        "You can bet on it.": "Możesz na to liczyć.",
    },
}

known = set()
for line in MERGED.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    if row['translation'].strip():
        known.add(row['id'])
for path in [ROOT / 'drafts/custom-dialogue-map9-events-82-55-97-17-95-01.jsonl', ROOT / 'drafts/custom-dialogue-map9-events-59-78-8-4-43-01.jsonl', ROOT / 'drafts/custom-dialogue-map9-followups-05.jsonl']:
    for line in path.read_text(encoding='utf-8').splitlines():
        known.add(json.loads(line)['id'])
rows = []
missing = set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    event_id = context.get('event_id')
    if context.get('source_kind') != 'map' or context.get('map_id') != 23 or event_id not in EVENTS or row['id'] in known:
        continue
    source = row['source_text'].strip()
    if not source or source.startswith('/') or source in {'…', '...', '..'}:
        continue
    translation = EVENTS[event_id].get(source)
    if translation is None:
        missing.add((event_id, source))
        continue
    row['translation'] = translation
    rows.append(row)
if missing:
    raise SystemExit('Unmapped strings: ' + repr(sorted(missing)))
path = ROOT / 'drafts/custom-dialogue-map23-followups-02.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote Map 23 follow-ups: {len(rows)} records across {len(EVENTS)} events')
