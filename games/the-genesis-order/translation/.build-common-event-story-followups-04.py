#!/usr/bin/env python3
"""Build Polish drafts for remaining Common Event story and finale dialogue."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-common-event-story-followups-04.jsonl'
EVENT_IDS = {389, 400, 406, 407, 410, 414, 417, 422, 423, 425, 429, 444, 448, 449, 454, 458, 460, 462, 473, 486, 487}
TRANSLATIONS = {
    "Joining us this evening is Detective 1Hero Canmore with an update on the latest in the Eclipse Guild arrests.": "Do naszego studia dołącza dziś detektyw 1Hero Canmore, który opowie o najnowszych zatrzymaniach członków Gildii Eclipse.",
    "It’s a pleasure being here with you Miss Foxx.": "Miło mi gościć u pani, panno Foxx.",
    "Last time we met you told us there was no Guild activity in the city. Is that still the case? We sure do love our quiet town to stay that way.": "Ostatnim razem mówił pan, że w mieście nie ma żadnej aktywności Gildii. Czy nadal tak jest? Bardzo nam zależy, by nasze spokojne miasteczko takim pozostało.",
    "North Santiva will stay free of gangs, that’s my assurance to you. But we have uncovered quite a find hiding here in our city.": "Zapewniam, że North Santiva pozostanie wolne od gangów. Udało nam się jednak odkryć coś niezwykłego ukrytego w naszym mieście.",
    "Oh, really? What might that be?": "Naprawdę? Cóż takiego?",
    "Several decades ago a series of valuable paintings were stolen and as we speak officers are searching for a Rembrandt worth over ten million dollars.": "Kilkadziesiąt lat temu skradziono serię cennych obrazów. Właśnie teraz funkcjonariusze szukają Rembrandta wartego ponad dziesięć milionów dolarów.",
    "Ten million! That’s incredible!": "Dziesięć milionów! Niesamowite!",
    "It turns out a collector has come across the painting, but due to an early death we are unable to locate it.": "Okazuje się, że obraz znalazł pewien kolekcjoner, ale po jego przedwczesnej śmierci nie udało nam się ustalić, gdzie się znajduje.",
    "Unfortunately this has caught the eye of some thieves.": "Niestety, na obraz połakomiło się kilku złodziei.",
    "Eclipse Guild thieves?": "Złodzieje z Gildii Eclipse?",
    "That’s right Miss Foxx. And it’s up to us to find the painting first and make sure nothing happens in our city.": "Zgadza się, panno Foxx. Musimy odnaleźć obraz jako pierwsi i dopilnować, by w naszym mieście nic się nie stało.",
    "So the Guild is here?": "Czyli Gildia tu jest?",
    "I want to assure everyone that there are no gang operations in North Santiva.": "Chcę zapewnić wszystkich, że w North Santiva nie działają żadne gangi.",
    "We’ve simply come across their plan and are now working to intercept them.": "Po prostu natrafiliśmy na ich plan i teraz próbujemy ich powstrzymać.",
    "With any luck, they’ve probably already left town.": "Może mieliśmy szczęście i już wyjechali z miasta.",
    "Any chance a citizen might run across this painting?": "Czy jest szansa, że któryś z mieszkańców natknie się na ten obraz?",
    "Highly unlikely. We have information on the whereabouts and it won't be long before it’s in our possession.": "Mało prawdopodobne. Wiemy, gdzie może się znajdować, i wkrótce trafi w nasze ręce.",
    "Very exciting stuff! And I’m sure with a handsome man like you leading the way, that painting will be returned to its proper owner in no time.": "Ale emocje! Jestem pewna, że z takim przystojnym detektywem na czele szybko zwrócicie obraz prawowitemu właścicielowi.",
    "And now for a word from our sponsors.": "A teraz krótka przerwa na reklamy.",
    "Cut!... Great job.": "Cięcie!... Świetna robota.",
    "It may have been live-streamed.": "To mogła być transmisja na żywo.",
    "That’s right, North Santiva. Our detective friend has gotten caught up in a sex scandal.": "Zgadza się, mieszkańcy North Santiva. Nasz detektyw wplątał się w skandal seksualny.",
    "On the cusp of bringing down the Guild, Detective Canmore is spending his days creating sex-toy reviews for Lustagram.": "Tuż przed rozbiciem Gildii detektyw Canmore spędza dni, tworząc recenzje zabawek erotycznych na Lustagramie.",
    "Ella!": "Ella!",
    "1Hero!": "1Hero!",
    "Lillian!": "Lillian!",
    "Looks like someone’s impressed.": "Wygląda na to, że ktoś jest pod wrażeniem.",
    "Holy shit! It’s a Toma piece!": "Cholera! To fragment Toma!",
    "No way! Another magic rock thing!": "Niemożliwe! Kolejny magiczny kamień!",
    "It’s hard to explain…": "Trudno to wyjaśnić…",
    "It makes 1Hero cum a whole lot!": "Sprawia, że 1Hero dochodzi bardzo obficie!",
    "It has magical sex powers… There are six of them scattered around North Santiva.": "Ma magiczną moc seksualną… Sześć takich kamieni jest rozrzuconych po North Santiva.",
    "Hahaha. You’re joking.": "Hahaha. Żartujesz.",
    "Get ready, girls. This could get wild.": "Przygotujcie się, dziewczyny. Może być ostro.",
    "Wow! I’m so excited!": "Wow! Ale się cieszę!",
    "I don’t know if I can take another one of these.": "Nie wiem, czy dam radę jeszcze raz.",
    "Are you all being serious?": "Mówicie poważnie?",
    "Ahhhhhhhhh!": "Aaaaaaa!",
    "Is it the right book?": "Czy to właściwa książka?",
    "This is it, alright. But does it contain any useful info?": "To ta książka. Ale czy są w niej jakieś przydatne informacje?",
    "What about this one? It talks about a statue carried around by witches.": "A ta? Jest tu mowa o posągu noszonym przez czarownice.",
    "A statue? That sounds promising.": "Posąg? Brzmi obiecująco.",
    "‘’Both demon and heathen bring about a fall from Heaven’s grace through the worship of a false idol.’’": "‘’Demony i poganie sprowadzają na siebie utratę łaski Niebios, czcząc fałszywego bożka.’’",
    "That could mean almost anything. There are so many false idols.": "To może oznaczać niemal wszystko. Jest tyle fałszywych bożków.",
    "‘’A tribe of heathens, led by women and guided by the devils below, use the Idol of Souls to bring forth an army of the fallen.’’": "‘’Plemię pogan, prowadzone przez kobiety i kierowane przez diabły z głębin, posługuje się Idolem Dusz, by sprowadzić armię upadłych.’’",
    "Hmm… The Casula witches were the guardians of the Toma Leolo. Maybe that’s who the heathens are in this book?": "Hmm… Czarownice z Casuli strzegły Toma Leolo. Może to o nich mowa jako o poganach w tej książce?",
    "Are there any pictures?": "Są tu jakieś ilustracje?",
    "No images apart from this one…": "Poza tą nie ma żadnych ilustracji…",
    "Looks like a ritual location.": "Wygląda na miejsce odprawiania rytuałów.",
    "Did you see anything like this near the mansion, 1Hero?": "Widziałeś coś podobnego w pobliżu rezydencji, 1Hero?",
    "I was going to ask you the same.": "Miałem zapytać cię o to samo.",
    "It looks familiar.": "Wygląda znajomo.",
    "There’s more under the mansion that I’ve not seen.": "Pod rezydencją jest jeszcze więcej miejsc, których nie widziałem.",
    "Do you think the Toma Leolo is the idol this book is talking about?": "Myślisz, że Toma Leolo to bożek, o którym mówi ta książka?",
    "Maybe this ritual spot still exists.": "Może to miejsce rytuałów nadal istnieje.",
    "On the count of three, the match begins.": "Na trzy zaczynamy.",
    "Counting up from three or down from one?": "Odliczamy w górę od trzech czy w dół od jednego?",
    "Up from one.": "W górę, od jednego.",
    "On three?": "Na trzy?",
    "Let the countdown begin.": "Niech zacznie się odliczanie.",
    "He’s counting up!": "On liczy w górę!",
    "Let the countup begin.": "Niech zacznie się liczenie w górę.",
    "One… Two… Three!": "Raz… dwa… trzy!",
    "Ha! Is that all you got?": "Ha! Tylko na tyle cię stać?",
    "Damn, girl, you’re strong!": "Cholera, dziewczyno, ale jesteś silna!",
    "I’m a farm girl! I’ve got muscles!": "Jestem dziewczyną ze wsi! Mam mięśnie!",
    "Concentrate, Ella.": "Skup się, Ella.",
    "Just who the hell are you rooting for, 1Hero?": "Komu ty właściwie kibicujesz, 1Hero?",
    "Oh no! I’m too weak.": "O nie! Jestem za słaba.",
    "Hahaha!": "Hahaha!",
    "Looks like I won.": "Wygląda na to, że wygrałam.",
    "How so!?": "Jak to!?",
    "I don’t know! But you’re too girly to beat a real woman like myself.": "Nie wiem! Ale jesteś zbyt dziewczęca, by pokonać prawdziwą kobietę, taką jak ja.",
    "Now you’re talking bullshit.": "Teraz pieprzysz głupoty.",
    "Ahh, fuck! My leg!": "Kurwa! Moja noga!",
    "Ugh! Who the hell is that?": "Ech! Kto to, do cholery?",
    "It’s a cop!": "To glina!",
    "What’s with all the rocks, copper?": "O co chodzi z tymi kamieniami, glino?",
    "Look like artifacts.": "Wyglądają na artefakty.",
    "My lucky day.": "Ale mam szczęście.",
    "Leave Carol alone.": "Zostaw Carol w spokoju.",
    "And how the hell are you connected to all of this?": "A ty jak, do cholery, jesteś z tym związany?",
    "You’re not going to get away. Your team is gone.": "Nie uciekniesz. Twoja ekipa już przepadła.",
    "Heh. So you think.": "Heh. Tak ci się wydaje.",
    "Carol!": "Carol!",
    "Carol?": "Carol?",
    "Carol!?": "Carol!?",
    "Skip ahead. Look for Adam and Eve.": "Przewiń dalej. Poszukaj Adama i Ewy.",
    "Now we’re onto something.": "Teraz coś mamy.",
    "Seems you’ve met a celebrity in Hell, 1Hero.": "Wygląda na to, że spotkałeś w Piekle celebrytkę, 1Hero.",
    "She’s out for revenge?": "Chce się zemścić?",
    "I think I have an idea of what she wants.": "Chyba wiem, czego chce.",
    "Let’s keep reading.": "Czytajmy dalej.",
    "Damn. What assholes.": "Cholera. Co za dranie.",
    "The amulets!": "Amulety!",
    "Aren’t they what Duncan was looking for?": "Czy to nie ich szukał Duncan?",
    "Madalyn was looking for them…": "Madalyn ich szukała…",
    "Father Solomon should have this book. He needs to know what he’s up against.": "Ta książka powinna trafić do ojca Solomona. Musi wiedzieć, z czym przyjdzie mu się zmierzyć.",
    "I’ll bring it to him.": "Zaniosę mu ją.",
    "What good is casting her back into Hell if she can just leave again?": "Jaki sens ma odesłanie jej do Piekła, skoro może po prostu znowu stamtąd wyjść?",
    "Madalyn wanted them for a reason.": "Madalyn miała powód, żeby ich szukać.",
    "I cast you back to Hell!": "Odesłałem cię z powrotem do Piekła!",
    "Citizens of North Santiva, I am here to offer you a choice.": "Mieszkańcy North Santiva, przychodzę dać wam wybór.",
    "If you value your life on Earth, turn the TV off now.": "Jeśli cenicie swoje życie na Ziemi, natychmiast wyłączcie telewizory.",
    "The time has come for everyone to choose their own future.": "Nadszedł czas, by każdy wybrał własną przyszłość.",
    "What the hell did you do?": "Co ty, do cholery, zrobiłeś?",
    "I cast you back to Hell, demon! Be gone!": "Odesłałem cię do Piekła, demonie! Znikaj!",
    "Look away! Don’t make eye contact!": "Odwróć wzrok! Nie patrz jej w oczy!",
    "Father! Do something!": "Ojcze! Zrób coś!",
    "Well, well… A new body.": "No proszę… Nowe ciało.",
    "Where is she!? Where is Madalyn!?": "Gdzie ona jest!? Gdzie Madalyn!?",
    "Daemalius!": "Daemalius!",
    "Get out of that body! Now!": "Wynoś się z tego ciała! Natychmiast!",
    "An angel? On Earth?": "Anioł? Na Ziemi?",
    "I opened the rift to Hell… Or should I say I was forced to open the rift to Hell.": "Otworzyłem szczelinę do Piekła… A raczej zmuszono mnie, bym ją otworzył.",
    "Madalyn has formed an alliance with Lilith.": "Madalyn zawarła sojusz z Lilith.",
    "That bitch! She tricked me!": "Suka! Oszukała mnie!",
    "Demons?... What is the meaning of this!? Where did you get those bodies?": "Demony?... Co to ma znaczyć!? Skąd macie te ciała?",
    "What!? Who are you? Where did you come from?": "Co!? Kim jesteś? Skąd się wziąłeś?",
    "I am Daemalius… I was brought to Earth by humans, hundreds of years ago.": "Jestem Daemalius… Ludzie sprowadzili mnie na Ziemię setki lat temu.",
    "You’re not making any fucking sense. The rift was only now opened.": "Gadasz bez sensu. Szczelinę otwarto dopiero teraz.",
    "There’s no way you could have been here before the Toma Leolo was brought back.": "Nie mogłeś tu być, zanim sprowadzono z powrotem Toma Leolo.",
    "The Toma Leolo?": "Toma Leolo?",
    "Mother is building an army. Are you with us or do we need to fuck you up?": "Matka buduje armię. Jesteś z nami, czy mamy ci skopać tyłek?",
    "This is my world, and mine alone! That bitch is going to die!": "To mój świat i tylko mój! Ta suka zginie!",
    "It’s so nice to feel young again!": "Jak miło znów poczuć się młodo!",
    "Hey! I’ll shoot you! Stay back!": "Hej! Zastrzelę cię! Nie zbliżaj się!",
    "What do you think will happen?": "Jak myślisz, co się stanie?",
    "Don’t make me do it!": "Nie zmuszaj mnie!",
    "You worthless piece of human trash!": "Bezwartościowy ludzki śmieciu!",
    "Fuck you! You’re a fucking thief!": "Pierdol się! Jesteś zwykłym złodziejem!",
    "You want revenge for losing your precious Guild?": "Chcesz się zemścić za utratę swojej ukochanej Gildii?",
    "No one crosses me and lives to tell the tale.": "Nikt, kto ze mną zadziera, nie dożywa, by o tym opowiedzieć.",
    "Well… Consider me the first.": "Cóż… Uznaj mnie za pierwszego.",
    "Take him to jail.": "Zabrać go do więzienia.",
    "Diana!": "Diana!",
    "Such a pity…": "Jaka szkoda…",
    "The laws are changing and now your investors are running…": "Prawo się zmienia, a twoi inwestorzy uciekają…",
    "People like you and me are losing their place in this world.": "Ludzie tacy jak ty i ja tracą swoje miejsce w tym świecie.",
    "No, my dear… People like us are exactly what this world needs.": "Nie, moja droga… Ten świat potrzebuje właśnie takich ludzi jak my.",
    "Then what are we waiting for, Miss Bancroft?": "Na co więc czekamy, panno Bancroft?",
    "We were waiting for you, Lilith… We were waiting for you.": "Czekaliśmy na ciebie, Lilith… Czekaliśmy na ciebie.",
    "What is that? Did you take a relic from Hell?": "Co to jest? Wzięłaś relikwię z Piekła?",
    "It’s so pretty.": "Jest taka śliczna.",
    "That’s not something you should have.": "Nie powinnaś tego mieć.",
    "Oh, 1Hero… Look what I found.": "Och, 1Hero… Zobacz, co znalazłam.",
    "Chloe, what are you doing?": "Chloe, co ty robisz?",
    "Don’t you recognize these? It’s my mom’s panties.": "Nie poznajesz ich? To majtki mojej mamy.",
    "Are you really digging through dirty laundry?": "Naprawdę grzebiesz w brudnej bieliźnie?",
    "Don’t I look so sexy, 1Hero?": "Nie wyglądam seksownie, 1Hero?",
    "Chloe! Those panties are dirty!": "Chloe! Te majtki są brudne!",
    "And you love it! Don’t deny it.": "A to cię kręci! Nie zaprzeczaj.",
    "You naughty, naughty girl.": "Ty niegrzeczna, niegrzeczna dziewczynko.",
    "Oh, I feel naughty.": "Och, czuję się niegrzeczna.",
    "You like how that smells?...": "Podoba ci się ten zapach?...",
    "Oh, 1Hero… You’re so nasty… It’s making me horny.": "Och, 1Hero… Jesteś taki obrzydliwy… To mnie podnieca.",
    "You like this, don’t you?": "Podoba ci się, prawda?",
    "I don’t know what’s gotten into you, but I like it.": "Nie wiem, co w ciebie wstąpiło, ale podoba mi się to.",
    "Do you like seeing me in my hot mom’s panties, 1Hero?": "Podoba ci się widok mnie w majtkach mojej seksownej mamy, 1Hero?",
    "They are dirty, Chloe…": "Są brudne, Chloe…",
    "So dirty! I can feel it!": "Takie brudne! Czuję to!",
    "Yes, Chloe! Take my cock!": "Tak, Chloe! Weź mojego kutasa!",
    "I’m a bad, bad girl! Give it to me!": "Jestem niegrzeczną dziewczynką! Daj mi go!",
    "Cum for me, Chloe! Cum in your mom’s panties!": "Dojdź dla mnie, Chloe! Dojdź w majtki swojej mamy!",
    "Mom’s panties are soaked.": "Majtki mamy są całe mokre.",
    "I think we can soak them more.": "Myślę, że możemy je jeszcze bardziej zmoczyć.",
    "Give it to me, 1Hero.": "Daj mi go, 1Hero.",
    "Whatever shall we do? Perhaps we’ll die here together.": "Co my poczniemy? Może zginiemy tu razem.",
    "Lillian?": "Lillian?",
    "Oh, come on, 1Hero. Let’s spend our final moments alive having some fun.": "Daj spokój, 1Hero. Spędźmy nasze ostatnie chwile na odrobinie przyjemności.",
    "You’re trying to distract me.": "Próbujesz mnie rozproszyć.",
    "Well? Is it working?": "No i? Działa?",
    "God damn… Lillian.": "Cholera… Lillian.",
    "Stop it…": "Przestań…",
    "You don’t truly want me to stop.": "Tak naprawdę nie chcesz, żebym przestała.",
    "I know how to keep your mind in the right place.": "Wiem, jak sprowadzić twoje myśli na właściwe tory.",
    "You’ve done well, 1Hero… But you can not follow me.": "Dobrze się spisałeś, 1Hero… Ale nie możesz za mną iść.",
    "I have work to do far from here and you belong in North Santiva.": "Mam do wykonania zadanie daleko stąd, a twoje miejsce jest w North Santiva.",
    "But I will miss this mouth of yours…": "Ale będę tęsknić za tymi twoimi ustami…",
    "You know I can’t resist, Lillian.": "Wiesz, że nie umiem ci się oprzeć, Lillian.",
    "I am the mother you need.": "Jestem matką, której potrzebujesz.",
    "Lillian… Wait.": "Lillian… Zaczekaj.",
    "Still not content, 1Hero?": "Wciąż ci mało, 1Hero?",
    "It… It feels so good.": "To… Tak dobrze.",
    "Shit, I can really feel it!": "Cholera, naprawdę to czuję!",
    "Let the worry leave your body… Let all the ills of this world melt away.": "Pozwól, by troski opuściły twoje ciało… Niech znikną wszystkie cierpienia tego świata.",
    "Give me your love!": "Daj mi swoją miłość!",
    "Fantastic, as always. You’re one of a kind, 1Hero.": "Fantastycznie jak zawsze. Jesteś jedyny w swoim rodzaju, 1Hero.",
    "Damn, Lillian. That was amazing.": "Cholera, Lillian. To było niesamowite.",
}

known = set()
for path in (ROOT / 'drafts').glob('*.jsonl'):
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            row = json.loads(line)
            if row.get('translation', '').strip():
                known.add(row['id'])

rows = []
unmapped = set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    row = json.loads(line)
    context = row.get('context') or {}
    source = ' '.join(row.get('source_text', '').strip().split())
    if (
        row['id'] in known
        or row.get('category') != 'custom_dialogue'
        or context.get('source_kind') != 'common_event'
        or context.get('event_id') not in EVENT_IDS
        or not source
        or source.lstrip().startswith('/')
        or not any(char.isalpha() for char in source)
    ):
        continue
    translation = TRANSLATIONS.get(source)
    if translation is None:
        unmapped.add((context.get('event_id'), source))
        continue
    row['translation'] = translation
    rows.append(row)

if unmapped:
    raise SystemExit('Unmapped selected Common Event strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) < 190:
    raise SystemExit(f'Expected at least 190 records, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Common Event finale lines across {len({r["context"]["event_id"] for r in rows})} events')
