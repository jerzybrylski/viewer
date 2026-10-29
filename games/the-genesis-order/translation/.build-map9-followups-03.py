import json
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl')

EVENTS = {
    82: {
        "I thought you’d be with the girls.": "Myślałem, że będziesz z dziewczynami.",
        "Everyone went to the church. I thought I’d come stop by.": "Wszyscy poszli do kościoła. Pomyślałem, że wpadnę.",
        "Looking to hang out with the old ladies?": "Chcesz posiedzieć ze starszymi paniami?",
        "I just wanted to take a look at something in the woods.": "Chciałem tylko rozejrzeć się w lesie.",
        "Related to your case?": "To coś związanego ze sprawą?",
        "Possibly… There are thieves running around the forest… Can’t be too safe.": "Możliwe… Po lesie kręcą się złodzieje… Lepiej dmuchać na zimne.",
        "Care for some company?": "Przydałoby ci się towarzystwo?",
        "It’s a beautiful morning… And maybe we can have a little fun in the woods while we’re at it.": "Piękny poranek… A przy okazji możemy się trochę zabawić w lesie.",
        "Carol!": "Carol!",
        "Hannah’s gone for the day, I’m sure.": "Hannah na pewno nie wróci przez cały dzień.",
        "What’s going on out here?": "Co tu się dzieje?",
        "1Hero’s stopped by to take a hike in the woods.": "1Hero wpadł, żeby wybrać się na spacer po lesie.",
        "Enjoying the cool morning weather?": "Cieszysz się rześkim porankiem?",
        "Just wanting to look for some clues in the forest.": "Chciałem tylko poszukać wskazówek w lesie.",
        "How did things go with Judy last night?": "Jak minął wczorajszy wieczór z Judy?",
        "Things got a bit heated after dinner… We stopped by the porn shop.": "Po kolacji zrobiło się dość gorąco… Wstąpiliśmy do sklepu porno.",
        "You brought a nun to a porn shop?": "Zabrałeś zakonnicę do sklepu porno?",
        "I knew it was a bad idea. I don’t know what I was thinking.": "Wiedziałem, że to zły pomysł. Nie wiem, co sobie myślałem.",
        "You have to remember, she has very little life experience outside of church life.": "Pamiętaj, że poza życiem w kościele ma niewielkie doświadczenie.",
        "I know. I think she’s a bit jealous too.": "Wiem. Chyba jest też trochę zazdrosna.",
        "If you’re not careful, she’s gonna fall for you.": "Jeśli nie będziesz ostrożny, zakocha się w tobie.",
        "1Hero knows what he’s doing. He’ll make the right choices.": "1Hero wie, co robi. Podejmie właściwe decyzje.",
        "I think I need a day away from the youngsters.": "Chyba przyda mi się dzień z dala od młodzieży.",
        "Hahaha. You’ve got a soft spot for us old ladies, for sure.": "Hahaha. Na pewno masz słabość do starszych pań.",
        "I guess you could say that.": "Można tak powiedzieć.",
        "And believe me. I’ve got a soft, warm and tight spot for you too.": "A uwierz mi, ja też mam dla ciebie miękkie, ciepłe i ciasne miejsce.",
        "Oh, Carol. 1Hero doesn’t like teasing anymore.": "Och, Carol. 1Hero nie lubi już takich żartów.",
        "Like hell he doesn’t.": "Wcale nie!",
        "Come on! Let’s go hiking before the weather turns.": "Chodź! Wybierzmy się na spacer, zanim pogoda się zepsuje.",
    },
    55: {
        "Are you joining the girls tonight, 1Hero?": "Dołączysz dziś wieczorem do dziewczyn, 1Hero?",
        "Me? No. I’m just walking Chloe here. I’ve got to get back to the church.": "Ja? Nie. Odprowadzam tylko Chloe. Muszę wracać do kościoła.",
        "Going to church now?": "Idziesz teraz do kościoła?",
        "He’s working.": "Jest w pracy.",
        "I’m going to talk with the nun there. She’s got some information that might help me with my case.": "Porozmawiam z zakonnicą. Ma informacje, które mogą pomóc mi w sprawie.",
        "Always a hard worker… Good luck with that, 1Hero.": "Zawsze taki pracowity… Powodzenia, 1Hero.",
        "Thanks for walking with me, 1Hero.": "Dzięki, że mnie odprowadziłeś, 1Hero.",
        "Working on the tractor?": "Naprawiasz traktor?",
        "The damn thing won't start and it’s a pain in the ass to get around it.": "Ten cholerny grat nie chce odpalić, a manewrowanie nim to mordęga.",
        "I told Hannah not to park it here.": "Mówiłam Hannah, żeby tu go nie parkowała.",
        "Going to be a late night?": "Zapowiada się późna noc?",
        "At least the weather seems good… for now.": "Przynajmniej pogoda na razie dopisuje…",
        "Besides, it’s good to give the girls some privacy.": "Poza tym dobrze dać dziewczynom trochę prywatności.",
        "Well, I’d offer some company, but I’ve gotta run.": "Chętnie dotrzymałabym ci towarzystwa, ale muszę lecieć.",
        "Aww, too bad. Would be nice to spend some time with a real man.": "Aww, szkoda. Miło byłoby spędzić trochę czasu z prawdziwym mężczyzną.",
        "More teasing?": "Znowu się ze mną droczysz?",
        "You know, Hannah’s been talking about you.": "Wiesz, Hannah ostatnio o tobie mówiła.",
        "Hopefully nothing too bad.": "Mam nadzieję, że nie mówiła nic złego.",
        "You’ve matured quite a bit, 1Hero.": "Bardzo dojrzałeś, 1Hero.",
        "Here we are, a Sunday night and the girls are having a sleepover.": "No proszę, niedzielny wieczór, a dziewczyny urządzają sobie nocowankę.",
        "No school tomorrow.": "Jutro nie ma szkoły.",
        "They need to grow up.": "Powinny wreszcie dorosnąć.",
        "I know. Just give them time.": "Wiem. Daj im trochę czasu.",
        "I’m running out of patience, but I admit it’s better than being lonely in the house.": "Kończy mi się cierpliwość, ale przyznaję, że to lepsze niż samotność w domu.",
        "It gets mighty quiet around here when Hannah’s not rampaging around.": "Robi się tu strasznie cicho, gdy Hannah nie szaleje po okolicy.",
        "You know, I’ll always visit.": "Wiesz, zawsze będę cię odwiedzał.",
    },
    97: {
        "Hannah! You’re terrifying the little fella!": "Hannah! Przerażasz tego biedaka!",
        "I’m gonna catch him! Just you watch!": "Złapię go! Zobaczysz!",
        "The goat’s back?": "Kozioł wrócił?",
        "Looks like he survived.": "Wygląda na to, że przeżył.",
        "Hey! It’s 1Hero and Heather!": "Hej! To 1Hero i Heather!",
        "I’m stopping by to help your mom cook some dinner.": "Wpadłem pomóc twojej mamie przygotować kolację.",
        "Oh boy! What are we having?": "O rany! Co będzie na kolację?",
        "Well, if you’re up for it, we’re having a party with Chloe and Judy.": "Jeśli masz ochotę, urządzamy dziś przyjęcie z Chloe i Judy.",
        "You’re having a party?": "Urządzacie przyjęcie?",
        "The girls are going to watch 1Hero on the news. You should join them, Hannah.": "Dziewczyny będą oglądać 1Hero w wiadomościach. Dołącz do nich, Hannah.",
        "Sounds like a lot of fun. I guess us old ladies aren’t invited.": "Brzmi świetnie. Chyba nas, starszych pań, nie zaproszono.",
        "Oh, Carol. Let’s sit this one out.": "Och, Carol. Tym razem odpuśćmy.",
        "But what’s for supper?": "Ale co będzie na kolację?",
        "Chloe and Judy are going to cook chicken stir-fry.": "Chloe i Judy zrobią kurczaka z warzywami z patelni.",
        "I’m heading over!": "Już idę!",
        "Be back for bedtime, ya hear?": "Wróć przed porą spania, jasne?",
        "Yes, Ma!": "Tak jest, mamo!",
        "Looks like that little goat is pretty fast.": "Ten mały kozioł jest całkiem szybki.",
        "We almost had it.": "Prawie go złapaliśmy.",
        "It’s nice weather out. Maybe we have some time before dinner to search for it.": "Ładna dziś pogoda. Może zdążymy go poszukać przed kolacją.",
        "I don’t know. I’m getting pretty hungry.": "Nie wiem. Robię się już głodna.",
        "It’s early. I can help you if you want.": "Jest jeszcze wcześnie. Mogę ci pomóc, jeśli chcesz.",
        "Alright. Let’s see if we can’t get a hold of that little goat.": "Dobra. Zobaczmy, czy uda nam się złapać tego koziołka.",
    },
    17: {
        "Are you talking about cases with people outside the station?": "Rozmawiasz o sprawach z ludźmi spoza komisariatu?",
        "Oh, uhh… I was just speculating on some things.": "Och, eee… Po prostu snułem przypuszczenia.",
        "You’re careless, 1Hero.": "Jesteś nieostrożny, 1Hero.",
        "Is 1Hero showing you the tractor? You know he helped fix it last night.": "1Hero pokazuje ci traktor? Wiesz, że wczoraj wieczorem pomagał go naprawić.",
        "1Hero is pretty helpful.": "1Hero jest bardzo pomocny.",
        "I hope he wasn’t too late for work after a late night here at the farm.": "Mam nadzieję, że po tej późnej nocy na farmie nie spóźnił się do pracy.",
        "He’s often late.": "Często się spóźnia.",
        "1Hero! You shouldn’t be late for work.": "1Hero! Nie powinieneś spóźniać się do pracy.",
        "As much as I’d love to stay and chat, 1Hero and I have to get back to the station.": "Chętnie zostałabym pogawędzić, ale 1Hero i ja musimy wracać na komisariat.",
        "It was nice to meet you, Melissa.": "Miło było cię poznać, Melissa.",
        "You’re welcome on the farm any time.": "Zawsze jesteś mile widziany na farmie.",
        "Okay! Yeah! All is good! Goodbye!": "Dobrze! Tak! Wszystko gra! Do widzenia!",
        "When do you get off work?": "O której kończysz pracę?",
        "Not for a while. I really gotta go.": "Jeszcze nieprędko. Naprawdę muszę już iść.",
        "We’re having a pool party. Care to join us?": "Urządzamy przyjęcie przy basenie. Dołączysz do nas?",
        "Yeah! You should stop by, 1Hero.": "Tak! Wpadnij, 1Hero.",
        "We’d love to have your company.": "Będzie nam miło, jeśli do nas dołączysz.",
        "You all are embarrassing the hell out of me.": "Ale mnie zawstydzacie.",
        "Hahaha!": "Hahaha!",
        "Oh, 1Hero. You are too cute.": "Och, 1Hero. Ale jesteś słodki.",
        "Look… I’ll stop by after work. But I’ve got to get back to the station.": "Słuchajcie… Wpadnę po pracy. Ale teraz muszę wracać na komisariat.",
        "Hooray!": "Hura!",
        "Alright, 1Hero. Get your ass back to work now.": "Dobra, 1Hero. A teraz ruszaj tyłek do pracy.",
        "See you all later.": "Do zobaczenia później.",
    },
    95: {
        "1Hero! What took you so long at the church?! You had us worried!": "1Hero! Czemu tak długo zabawiłeś w kościele?! Martwiłyśmy się!",
        "It’s fine, Hannah. The cops came.": "Wszystko dobrze, Hannah. Przyjechała policja.",
        "Did you get the criminals?": "Złapaliście przestępców?",
        "We’re working on it. But it’ll be over soon.": "Pracujemy nad tym. Wkrótce będzie po wszystkim.",
        "Church sure is exciting! I want to go again.": "W kościele jest naprawdę ciekawie! Chcę tam wrócić.",
        "Hannah…": "Hannah…",
        "Duncan’s not coming back to the church.": "Duncan już nie wróci do kościoła.",
        "He got what he came for.": "Dostał to, po co przyszedł.",
        "You should have let me clobber him!": "Trzeba było pozwolić mi go stłuc!",
        "You better be careful, Hannah.": "Lepiej uważaj, Hannah.",
        "Listen to the man, sweetheart. If you see those thieves, you better run.": "Posłuchaj go, kochanie. Jeśli zobaczysz tych złodziei, uciekaj.",
        "Hmf!": "Phi!",
        "She went back to the church with Papa Brian.": "Wróciła do kościoła z ojcem Brianem.",
        "I didn’t see her there.": "Nie widziałem jej tam.",
        "Oh, no! Drakan got her!": "O nie! Drakan ją dopadł!",
        "Hannah! Don’t be so negative!": "Hannah! Nie bądź taką pesymistką!",
        "Duncan’s not looking for Judy, he was looking for an amulet…": "Duncan nie szukał Judy, tylko amuletu…",
        "I’m sure she’s fine. I’ll find her.": "Na pewno nic jej nie jest. Znajdę ją.",
        "Are you going to arrest them?": "Zamierzasz ich aresztować?",
        "Yes. It’s just about over.": "Tak. To już prawie koniec.",
        "Get’em, 1Hero!": "Dorwać ich, 1Hero!",
    },
}

known = set()
for line in MERGED.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    if row['translation'].strip():
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
path = ROOT / 'drafts/custom-dialogue-map9-events-82-55-97-17-95-01.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote Map 9 follow-ups: {len(rows)} records across {len(EVENTS)} events')
