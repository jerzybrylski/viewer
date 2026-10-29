import json
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl')
DRAFTS = [
    ROOT / 'drafts/custom-dialogue-map9-events-82-55-97-17-95-01.jsonl',
    ROOT / 'drafts/custom-dialogue-map9-events-59-78-8-4-43-01.jsonl',
]
EVENTS = {
    108: {
        "Morgan! I know you’re in there!": "Morgan! Wiem, że tam jesteś!",
        "Shit! It’s Duncan!": "Cholera! To Duncan!",
        "You’re not getting out of this one.": "Tym razem ci się nie upiecze.",
        "Get your ass out here!": "Wychodź natychmiast!",
        "Why are you here?": "Po co tu przyszedłeś?",
        "I was going to steal back the amulet. I just needed more time.": "Chciałem odzyskać amulet. Potrzebowałem tylko więcej czasu.",
        "Charles is dead. Do you want to join him in hell?": "Charles nie żyje. Chcesz do niego dołączyć w piekle?",
        "You can’t run!": "Nie uciekniesz!",
        "Move aside. I’ll break down the door.": "Odsuń się. Wyważę drzwi.",
        "No! Leave the house alone.": "Nie! Zostaw ten dom w spokoju.",
        "Fuck! I need to do something.": "Kurwa! Muszę coś zrobić.",
        "Don’t protect her, Carol. She’s a thief.": "Nie broń jej, Carol. To złodziejka.",
    },
    127: {
        "Are you crazy, Hannah? You can’t keep an alligator.": "Zwariowałaś, Hannah? Nie możesz trzymać aligatora.",
        "You put that thing back in the water.": "Odłóż to stworzenie do wody.",
        "Too bad you can’t keep it, Hannah. But at least you still have your goat.": "Szkoda, że nie możesz go zatrzymać, Hannah. Przynajmniej został ci kozioł.",
        "Goatzilla needs a buddy, Ma.": "Goatzilli przydałby się kumpel, mamo.",
        "It’ll eat the goat, Hannah.": "Zje kozła, Hannah.",
        "I’ll have no more talk of it. You let that thing go in the creek.": "Koniec dyskusji. Wypuść to stworzenie do strumienia.",
        "Don’t worry. I was planning to keep it in the creek anyways.": "Spokojnie. I tak planowałam zostawić go w strumieniu.",
        "Can I pet him?": "Mogę go pogłaskać?",
        "Sure! Let’s release him together… as a team.": "Jasne! Wypuśćmy go razem… jako drużyna.",
        "You’re my best friend!": "Jesteś moim najlepszym przyjacielem!",
        "I think we’re going to get along just fine.": "Chyba świetnie się dogadamy.",
        "How the hell is that girl still alive?": "Jakim cudem ta dziewczyna wciąż żyje?",
    },
    58: {
        "Sorry, 1Hero. If you’re here to hang out, I’m heading out.": "Wybacz, 1Hero. Jeśli wpadłeś pogadać, to właśnie wychodzę.",
        "Something is up with mom. I can’t shake how strange she was acting earlier.": "Z mamą coś jest nie tak. Nie mogę przestać myśleć, jak dziwnie się wcześniej zachowywała.",
        "You’re going home?": "Wracasz do domu?",
        "For now…": "Na razie…",
        "I just want to check up on her.": "Chcę tylko zobaczyć, co u niej.",
        "What do you think is going on?": "Jak myślisz, co się dzieje?",
        "Let’s call it a midlife crisis.": "Nazwijmy to kryzysem wieku średniego.",
        "I don’t think she likes getting older. Can you blame her?": "Chyba nie podoba jej się starzenie. Można ją winić?",
        "She can’t be young forever.": "Nie będzie wiecznie młoda.",
        "I think she’ll appreciate you going home to talk to her.": "Myślę, że doceni, że wrócisz z nią porozmawiać.",
        "…I hope it’s not me that’s driving Heather crazy.": "…Mam nadzieję, że to nie przeze mnie Heather wariuje.",
    },
    123: {
        "Hey, 1Hero!... Erica here tells me there could be some treasure in our cave.": "Hej, 1Hero!... Erica mówi, że w naszej jaskini może być jakiś skarb.",
        "Or somewhere near it.": "Albo gdzieś w pobliżu.",
        "I’ve been in there… I don’t know if there’s a tomb to find, but Jon says there could be.": "Byłem tam… Nie wiem, czy jest tam jakiś grobowiec, ale Jon twierdzi, że może być.",
        "Can we explore the cave?": "Możemy zbadać jaskinię?",
        "We’d have to find a way to open it back up… We collapsed it in a few months back.": "Musielibyśmy jakoś ją z powrotem otworzyć… Zawaliliśmy ją kilka miesięcy temu.",
        "There’s plenty of other areas to explore.": "Jest mnóstwo innych miejsc do zbadania.",
        "It would take explosives or a hell of a lot of elbow grease to get that cave open.": "Trzeba by użyć materiałów wybuchowych albo włożyć mnóstwo pracy, żeby otworzyć tę jaskinię.",
        "We should go to the creek.": "Powinniśmy iść nad strumień.",
        "Heh… It’s Erica’s new job.": "Heh… To nowa praca Eriki.",
        "I’m a treasure hunter now.": "Jestem teraz poszukiwaczką skarbów.",
        "See ya at the creek, 1Hero.": "Do zobaczenia nad strumieniem, 1Hero.",
    },
    88: {
        "It’s 1Hero!...": "To 1Hero!...",
        "Look! Judy’s here.": "Patrz! Judy przyszła.",
        "Yeah, I can see that.": "Tak, widzę.",
        "Are you gonna eat supper with us? Mom’s cooking something.": "Zjesz z nami kolację? Mama coś gotuje.",
        "I think I just might.": "Chyba się skuszę.",
        "Hannah has such a beautiful farm.": "Hannah ma przepiękną farmę.",
        "It’s a fun place to hang out.": "Fajnie się tu spędza czas.",
        "Let’s play some ball!": "Pobawmy się piłką!",
        "I think I’ll head inside to talk to your mom.": "Chyba pójdę do środka porozmawiać z twoją mamą.",
        "Suit yourself. We’re gonna have some fun!": "Jak wolisz. My będziemy się świetnie bawić!",
    },
    30: {
        "Well, well. Look who finally woke up.": "No proszę, kto wreszcie się obudził.",
        "Ya damn lazy bastard! I thought you were flakin’ on us.": "Ty leniwy draniu! Myślałam, że nas wystawiłeś.",
        "What took you so long, 1Hero?": "Czemu tak długo ci zeszło, 1Hero?",
        "Sorry, I slept in.": "Wybacz, zaspałem.",
        "Don’t let Hannah bully you, 1Hero. She’s extra ornery today.": "Nie daj się Hannah, 1Hero. Dziś jest wyjątkowo zadziorna.",
        "I’m just so happy to have Chloe and 1Hero here.": "Po prostu tak się cieszę, że Chloe i 1Hero tu są.",
        "Whatever you say, Hannah.": "Jak sobie życzysz, Hannah.",
        "Well, c’mon. Let’s see what we got waiting for us.": "No chodźcie. Zobaczmy, co na nas czeka.",
    },
    75: {
        "What are you up to, Carol?": "Co porabiasz, Carol?",
        "Took some time, but I finally have a buyer for the hay.": "Trochę to trwało, ale w końcu znalazłam kupca na siano.",
        "Well, that’s good news.": "To dobra wiadomość.",
        "I’ll have to drive a good 40 miles. Almost not worth the gas money…": "Muszę przejechać jakieś 40 mil. Prawie nie opłaca się za paliwo…",
        "But so few farmers around here have livestock to feed these days.": "Ale niewielu okolicznych farmerów ma teraz zwierzęta do wykarmienia.",
        "Need some company?": "Przyda ci się towarzystwo?",
        "I’ll be fine. If you’re looking to kill some time, maybe keep the girls company and make sure Hannah stays out of trouble.": "Poradzę sobie. Jeśli chcesz zabić trochę czasu, dotrzymaj dziewczynom towarzystwa i pilnuj, żeby Hannah nie wpakowała się w kłopoty.",
    },
    52: {
        "Ah! Stay back snake!...": "Ach! Zostań tam, wężu!...",
        "Is it hungry?...": "Jest głodny?...",
        "What do snakes eat?": "Co jedzą węże?",
        "I know! I can feed him the caterpillars.": "Wiem! Mogę nakarmić go gąsienicami.",
        "Did it work?": "Udało się?",
    },
    71: {
        "Off work early?": "Wcześnie skończyłeś pracę?",
        "My boss went home to change. I’m not exactly going to sit in my cube for the rest of the day.": "Moja szefowa pojechała do domu się przebrać. Nie zamierzam siedzieć w boksie do końca dnia.",
        "Thanks for fixing the tractor. Saved me some time this morning.": "Dzięki za naprawę traktora. Zaoszczędziłeś mi dziś rano trochę czasu.",
        "Hannah did all the work. I just gathered the parts.": "Całą robotę wykonała Hannah. Ja tylko zebrałem części.",
        "Well, I guess you two make a good team.": "Wygląda na to, że tworzycie zgrany zespół.",
    },
    7: {
        "Is no one home?": "Nikogo nie ma w domu?",
        "Hannah, are you in there?": "Hannah, jesteś tam?",
        "I can hear the TV is on…": "Słyszę, że telewizor jest włączony…",
        "The door’s unlocked.": "Drzwi są otwarte.",
    },
    92: {
        "This is harder than it looks.": "To trudniejsze, niż się wydaje.",
        "This is fun. This is all I want to do tonight.": "To świetna zabawa. Właśnie to chcę dziś robić.",
        "I understand, Sister.": "Rozumiem, siostro.",
        "But… Maybe later we can discuss some other things.": "Ale… Może później porozmawiamy o czymś innym.",
    },
    37: {
        "Where are all the bales, 1Hero?": "Gdzie są wszystkie bele, 1Hero?",
        "Uhh, I’m still working on it.": "Eee, jeszcze nad tym pracuję.",
        "Push them out here to us and we’ll load them up in the truck.": "Wypchnij je tutaj, a załadujemy je na ciężarówkę.",
    },
    57: {
        "I told ya I could fix it fast.": "Mówiłam, że szybko to naprawię.",
        "How far away is this cave?": "Jak daleko stąd jest ta jaskinia?",
        "Just right on the other side of the field.": "Zaraz za polem.",
    },
    93: {
        "Unless you’re going to play with us, get out of the way!": "Jeśli nie chcesz się z nami bawić, zejdź nam z drogi!",
        "Don’t tell Sister, but my butt is burning.": "Nie mów siostrze, ale piecze mnie tyłek.",
        "Did we go too far?": "Przesadziłyśmy?",
    },
    36: {
        "Get back in there and push them bales out here!": "Wracaj tam i wypychaj te bele!",
        "Okay! Okay!": "Dobra! Dobra!",
    },
    60: {
        "I know my way around a tractor. Just wait right there.": "Znam się na traktorach. Poczekaj tutaj.",
        "Moment of truth. Let’s see if she’ll run.": "Chwila prawdy. Zobaczmy, czy odpali.",
    },
    73: {
        "Coming over to eat, 1Hero?": "Przyjdziesz na kolację, 1Hero?",
        "Not tonight, but thanks for the offer.": "Nie dziś, ale dzięki za zaproszenie.",
    },
    85: {
        "This barrel will do nicely. Have you found the black powder?": "Ta beczka będzie w sam raz. Znalazłeś proch?",
        "I’m still looking.": "Wciąż szukam.",
    },
    96: {
        "Clobber them thieves! Get’em good!": "Dołóżcie tym złodziejom! Nie oszczędzajcie ich!",
        "Heh. I will, Hannah.": "Heh. Tak zrobię, Hannah.",
    },
    35: {"I’ve got it. I just need to push the bales out of the barn.": "Już wiem. Muszę tylko wypchnąć bele ze stodoły."},
    76: {"Ouch! My shoes slipped.": "Auć! Poślizgnęły mi się buty."},
    112: {"There’s nowhere to go.": "Nie ma dokąd pójść."},
}

known = set()
for line in MERGED.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    if row['translation'].strip():
        known.add(row['id'])
for batch in DRAFTS:
    for line in batch.read_text(encoding='utf-8').splitlines():
        row = json.loads(line)
        known.add(row['id'])
rows = []
missing = set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    event_id = context.get('event_id')
    if context.get('source_kind') != 'map' or context.get('map_id') != 9 or event_id not in EVENTS or row['id'] in known:
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
path = ROOT / 'drafts/custom-dialogue-map9-followups-05.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote Map 9 follow-ups: {len(rows)} records across {len(EVENTS)} events')
