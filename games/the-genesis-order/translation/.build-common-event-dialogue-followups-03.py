#!/usr/bin/env python3
"""Build Polish drafts for additional Common Event scenes and interactions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-common-event-dialogue-followups-03.jsonl'
EVENT_IDS = {258, 259, 260, 261, 262, 301, 302, 303, 306, 308, 309, 319, 321, 322, 329, 333, 336, 337, 343, 360, 361, 367, 369, 370, 371, 379, 382}
TRANSLATIONS = {
    "I can pair up the snorkel and mask so I can see underwater easier.": "Mogę połączyć fajkę z maską, żeby lepiej widzieć pod wodą.",
    "Now that I have a pair of swim shoes, I should be able to swim in heavy current.": "Skoro mam już buty do pływania, powinienem poradzić sobie nawet z silnym nurtem.",
    "I can’t break into a cop car. They all have state-of-the-art electronic locking systems.": "Nie włamię się do radiowozu. Wszystkie mają najnowocześniejsze elektroniczne zamki.",
    "With the sunglasses, uniform and fake mustache, maybe I can get away with going back to the police station.": "W okularach przeciwsłonecznych, mundurze i sztucznych wąsach może uda mi się wrócić na posterunek.",
    "That should do it. Let’s head back to the library.": "To powinno wystarczyć. Wracajmy do biblioteki.",
    "What are you!?": "Co ty jesteś!?",
    "I’m... I’m... I’ve got to go!": "Ja... ja... Muszę iść!",
    "What is this thing?": "Co to za rzecz?",
    "I... I’ve never seen it. I don’t know what it could be.": "Ja... Nigdy czegoś takiego nie widziałem. Nie wiem, co to może być.",
    "Whatever it is, it was shaking and moving on its own.": "Cokolwiek to jest, drżało i poruszało się samo.",
    "Oh, dear... What sort of unholy trinket is this?": "Ojej... Co to za przeklęty drobiazg?",
    "God, I hope it’s not radioactive.": "Boże, mam nadzieję, że to nie jest radioaktywne.",
    "Do you mind if I take this back to the station? I’d love to get a closer look at it.": "Nie masz nic przeciwko, jeśli zabiorę to na posterunek? Chętnie przyjrzę się temu z bliska.",
    "By all means. Please, take it away from this place.": "Oczywiście. Proszę, zabierz to z tego miejsca.",
    "Hopefully, now you won't hear any more noises.": "Mam nadzieję, że teraz nie usłyszysz już żadnych hałasów.",
    "Come on and take it, dear. It’s all yours.": "No już, weź to, kochanie. Jest twoje.",
    "Thanks, Heather. You’ve done so much for me.": "Dzięki, Heather. Tak wiele dla mnie zrobiłaś.",
    "Of course, darling. You’re my big boy.": "Oczywiście, kochanie. Jesteś moim dużym chłopcem.",
    "Oh! So many muscles!": "O! Ale masz mięśnie!",
    "Damn! Not holding back, are you?": "Cholera! Nie oszczędzasz się, co?",
    "I’d say I’m taking pretty good care of myself. What do you think?": "Powiedziałbym, że całkiem dobrze o siebie dbam. Co ty na to?",
    "Beautiful as always.": "Jak zawsze piękny.",
    "I’m Detective Canmore. You can call me 1Hero.": "Jestem detektywem Canmore'em. Możesz mówić mi 1Hero.",
    "Well, 1Hero. If you’re here about the noise complaint, you’re about three hours late.": "Cóż, 1Hero, jeśli chodzi o skargę na hałas, spóźniłeś się jakieś trzy godziny.",
    "I’m looking for Erica Abraham.": "Szukam Eriki Abraham.",
    "Is she in trouble?": "Ma kłopoty?",
    "What the hell is this about?": "O co, do cholery, chodzi?",
    "If you go to jail, you still owe me the money.": "Nawet jeśli trafisz do więzienia, nadal będziesz mi winien pieniądze.",
    "Erica?": "Erica?",
    "Get lost, Jon.": "Spadaj, Jon.",
    "You’ve got one week, Erica.": "Masz tydzień, Erica.",
    "Hahaha.": "Hahaha.",
    "What the hell is a bukkake?": "Co to, do cholery, jest bukkake?",
    "That’s when you get a giant load on your face.": "To wtedy, kiedy ktoś oblewa ci twarz ogromną ilością spermy.",
    "A cumshot… It’s semen. Don’t you guys have the internet?": "Wytrysk… To sperma. Nie macie internetu?",
    "Hannah. Let’s go.": "Hannah, chodźmy.",
    "What do you think, Chloe? Do you think I’d look good with a face full of cum?": "Co myślisz, Chloe? Uważasz, że dobrze bym wyglądała z twarzą oblepioną spermą?",
    "Hannah! That’s wrong!": "Hannah! Tak nie wolno!",
    "Are you kidding me, girl? A thick white load on that pretty face would be crazy hot.": "Żartujesz, dziewczyno? Gęsta, biała sperma na tej ślicznej buzi byłaby niesamowicie podniecająca.",
    "Haha! Oh my. I feel naughty.": "Haha! Ojej. Czuję się niegrzeczna.",
    "You are naughty. You need to stop.": "Jesteś niegrzeczna. Musisz przestać.",
    "What… the… hell?": "Co... do... cholery?",
    "A dance video?...": "Filmik taneczny?...",
    "This is hilarious.": "Ale śmieszne.",
    "Is this what people are into these days?": "To właśnie kręci teraz ludzi?",
    "It’s… creative.": "To... kreatywne.",
    "And she is kinda cute…": "I jest nawet urocza…",
    "Sexy, even…": "Nawet seksowna…",
    "But all that pink… It’s weird.": "Ale ten róż… Dziwne.",
    "Is she not wearing any panties?": "Czy ona nie ma na sobie majtek?",
    "It might be cringe, but she has excellent balance.": "Może to żenujące, ale ma świetną równowagę.",
    "But, damn… She’s sexy.": "Ale, cholera… Jest seksowna.",
    "Ugh… I can’t believe I’m watching this.": "Ech… Nie wierzę, że to oglądam.",
    "Should I tell her I watched it?...": "Powiedzieć jej, że to oglądałem?...",
    "Too bad her number is not showing up.": "Szkoda, że nie wyświetla się jej numer.",
    "Hehe… Cute.": "Hehe… Urocze.",
    "So, rough! I love it!": "Tak ostro! Uwielbiam to!",
    "Oh, shit! I’ve made a big mistake.": "Cholera! Popełniłem wielki błąd.",
    "Is that?... A cucumber?": "Czy to?... Ogórek?",
    "Where did Hannah get that dildo from? Could it be Carol’s?": "Skąd Hannah wzięła tego dilda? Czy to Carol?",
    "I never pictured Carol as a sexual being…": "Nie sądziłem, że Carol ma w sobie tyle erotyzmu…",
    "But she’s really going at it.": "Ależ się do tego zabrała.",
    "Damn! Even playing with her ass.": "Cholera! Bawi się nawet swoim tyłkiem.",
    "I shouldn’t be spying on her…": "Nie powinienem jej podglądać…",
    "But… She’s pretty hot…": "Ale… Jest całkiem seksowna…",
    "What am I doing?": "Co ja robię?",
    "Looks like she’s enjoying her own flavor.": "Najwyraźniej podoba jej się własny smak.",
    "I wonder what it tastes like.": "Ciekawe, jak smakuje.",
    "Argh! What am I thinking?": "Agh! O czym ja myślę?",
    "Holy shit… I feel something.": "Cholera… Coś czuję.",
    "Just go away, 1Hero. Stop staring at Hannah’s mom.": "Idź sobie, 1Hero. Przestań gapić się na matkę Hannah.",
    "She’s really fingering herself now…": "Naprawdę wkłada sobie teraz palce…",
    "Is she going to cum?": "Czy zaraz dojdzie?",
    "1Hero!?": "1Hero!?",
    "Carol!": "Carol!",
    "1Hero!": "1Hero!",
    "Lillian?": "Lillian?",
    "Hannah!": "Hannah!",
    "Hannah?": "Hannah?",
    "1Hero?": "1Hero?",
    "You’re slow, 1Hero.": "Ale jesteś wolny, 1Hero.",
    "That’s because I actually have some muscles, Bobby.": "Bo ja przynajmniej mam mięśnie, Bobby.",
    "You’re fat from staring at a computer all day long.": "Utyłeś od całodziennego gapienia się w komputer.",
    "And you’re delusional from harassing helpless people all day long.": "A ty masz urojenia od całodziennego nękania bezbronnych ludzi.",
    "Show me just how tough you are, kid.": "Pokaż, jaki z ciebie twardziel, młody.",
    "You asked for it!": "Sam się o to prosiłeś!",
    "Just like I said... You’re slow.": "Tak jak mówiłem... Jesteś powolny.",
    "Lucky shot!": "Szczęśliwy traf!",
    "I’m toying with you, 1Hero. If I wanted to, you’d be out cold.": "Bawię się z tobą, 1Hero. Gdybym chciał, już byś leżał nieprzytomny.",
    "I’ve seen enough. It’s time to get back to work, 1Hero.": "Wystarczy. Czas wracać do pracy, 1Hero.",
    "Oh, shit! Melissa is going to use this shower.": "O cholera! Melissa zaraz będzie brała prysznic.",
    "Damn. She’s got one hell of a nice body.": "Cholera, ma naprawdę świetne ciało.",
    "I shouldn’t watch her… I need to report this to the higher-ups.": "Nie powinienem jej podglądać… Muszę zgłosić to przełożonym.",
    "Shit! I can’t spy on my boss…": "Cholera! Nie mogę podglądać swojej szefowej…",
    "Although, technically she did spy on me first.": "Chociaż technicznie rzecz biorąc, to ona pierwsza podglądała mnie.",
    "Does this make us even?": "Czy jesteśmy teraz kwita?",
    "Too bad she can be such a bitch to work for. I’d totally hit on her if I didn’t know her bossy side.": "Szkoda, że potrafi być taką suką w pracy. Zarywałbym ją, gdybym nie znał jej apodyktycznej strony.",
    "Those tits are incredible. No wonder all the officers give me shit about working for her.": "Ma niesamowite cycki. Nic dziwnego, że wszyscy funkcjonariusze docinają mi, że dla niej pracuję.",
    "She’s actually a total babe.": "Tak naprawdę jest niezłą laską.",
    "Just how much of a show am I going to see here?": "Ile jeszcze zobaczę?",
    "Is she going to turn back around?": "Czy się odwróci?",
    "Oh, boy! What an ass!": "O rany! Jaki tyłek!",
    "I’d like to motorboat that thing.": "Chciałbym zanurzyć twarz w tym biuście.",
    "Damn! I’m seeing too much.": "Cholera! Widzę za dużo.",
    "This will be burned into my brain forever.": "Tego widoku nie zapomnę do końca życia.",
    "I’ve got to stop. How am I going to look her in the eye after this?": "Muszę przestać. Jak spojrzę jej w oczy po czymś takim?",
    "Shit… I’ve seen too much. Now I’ll look guilty as hell if I report this.": "Cholera… Za dużo zobaczyłem. Jeśli to zgłoszę, będę wyglądał na winnego.",
    "It’s Judy!...": "To Judy!...",
    "Who’s she with?": "Z kim ona jest?",
    "That’s right, Sister. Give into your desires. It’s hopeless to resist.": "Właśnie tak, siostro. Poddaj się swoim pragnieniom. Nie ma sensu się opierać.",
    "But, Mother Superior! I must remain holy!": "Ależ, Matko Przełożona! Muszę pozostać czysta!",
    "It’s too late. Your path with God ends here.": "Za późno. Twoja droga z Bogiem kończy się tutaj.",
    "I must resist!": "Muszę się oprzeć!",
    "There, there, Sister. There is no need to fight it.": "Już dobrze, siostro. Nie musisz z tym walczyć.",
    "Your time with God is over. You will leave this place and find a new path…": "Twój czas z Bogiem dobiegł końca. Opuścisz to miejsce i znajdziesz nową drogę…",
    "A path of lustful desire.": "Drogę pełną pożądania.",
    "But, Mother Superior… A path of lust leads to darkness.": "Ale, Matko Przełożona… Droga pożądania prowadzi w ciemność.",
    "Would I lie to you?": "Czy kłamałabym?",
    "No… Mother…": "Nie… Matko…",
    "Get away from her!": "Odsuń się od niej!",
    "What happened to me?": "Co się ze mną stało?",
    "It’s okay, Judy. I’m here.": "Wszystko w porządku, Judy. Jestem przy tobie.",
    "Mmm…": "Mmm…",
    "Mmmmm! Yes!": "Mmmm! Tak!",
    "Mmmm!": "Mmmm!",
    "Oh, Lillian…": "Och, Lillian…",
    "Argh! Ahh!": "Agh! Ahh!",
    "Looks like another artifact segment.": "Wygląda na kolejny fragment artefaktu.",
    "Holy shit! It’s another witch idol!": "Cholera jasna! Kolejny bożek czarownic!",
    "I hope it doesn’t make me sick again.": "Mam nadzieję, że znowu nie zrobi mi się od niego niedobrze.",
    "What is it doing here in this chapel?": "Co to robi w tej kaplicy?",
    "Maybe Charles thought it looked interesting.": "Może Charles uznał, że wygląda ciekawie.",
    "This place creeps me out. Should we tell Lillian about this place?": "To miejsce mnie przeraża. Powinniśmy powiedzieć Lillian o tym?",
    "Leave it up to me. I’ll find out if she knows about what’s here.": "Zostaw to mnie. Dowiem się, czy wie, co tu jest.",
    "I’ll keep my mouth shut.": "Będę milczeć.",
    "Careful, you two.": "Uważajcie, oboje.",
    "I’m never careful.": "Nigdy nie uważam.",
    "Then this should be easy.": "W takim razie to będzie łatwe.",
    "Get on with it.": "No dalej.",
    "I told you I could handle myself.": "Mówiłam, że sama sobie poradzę.",
    "Luck!": "Szczęśliwy traf!",
    "Not bad. I didn’t expect to see that.": "Nieźle. Nie spodziewałem się tego.",
    "Come on, Tasha. Don’t be mad. She’s had a lot of training.": "No już, Tasha. Nie złość się. Ona dużo trenowała.",
    "How about you take on someone else with a bit of… training.": "Może zmierzysz się z kimś, kto ma trochę… doświadczenia.",
    "You’re on, old lady.": "No to dawaj, staruszko.",
    "Where did you train?": "Gdzie trenowałaś?",
    "My mother taught me everything I know…": "Wszystkiego, co umiem, nauczyła mnie matka…",
    "There was no room for failure where I came from.": "Tam, skąd pochodzę, nie było miejsca na porażkę.",
    "Show me what you know.": "Pokaż, co potrafisz.",
    "How’d you do that?": "Jak to zrobiłaś?",
    "Experience, little girl.": "Doświadczenie, dziewczynko.",
    "My name is Ella.": "Mam na imię Ella.",
    "Keep training, Ella.": "Trenuj dalej, Ello.",
    "I have seen my purpose through visions. Prayers to God have revealed my fate.": "W wizjach ujrzałem swoje przeznaczenie. Modlitwy do Boga objawiły mi mój los.",
    "An angel of the Lord has come to me in the night.": "Anioł Pański przyszedł do mnie nocą.",
    "The bishops can not see the visions. Perhaps corruption has reached the highest rungs of the church.": "Biskupi nie widzą tych wizji. Być może zepsucie dotarło na najwyższe szczeble Kościoła.",
    "Nevertheless, the second coming is upon us and we have mere months left on this plane.": "Mimo to powtórne przyjście jest bliskie, a na tym świecie zostało nam zaledwie kilka miesięcy.",
    "An angel has come and the convent is ready to serve the Lord and bring forth his Son.": "Przyszedł anioł, a klasztor jest gotów służyć Panu i wydać na świat Jego Syna.",
    "The Gate of Heaven is here in North Santiva and alongside the divine angel of light we shall bring forth the final days of humanity.": "Brama Niebios znajduje się tutaj, w North Santiva. U boku boskiego anioła światłości sprowadzimy ostatnie dni ludzkości.",
    "My resolve is strengthened by her guiding hand.": "Jej przewodnictwo umacnia moją determinację.",
    "Zephaniah was convinced the second coming of Christ was underway…": "Zephaniah był przekonany, że powtórne przyjście Chrystusa już się rozpoczęło…",
    "He convinced all the nuns… except Sister Judy.": "Przekonał wszystkie zakonnice… oprócz siostry Judy.",
    "The angel he speaks of… I wonder if that could be Madalyn, messing with his mind.": "Anioł, o którym mówi… Ciekawe, czy to Madalyn mieszała mu w głowie.",
    "The man wasn’t sane, in my humble opinion. But with this new revelation of his poisoning, I’m sure that something fishy is going on.": "Moim skromnym zdaniem ten człowiek nie był przy zdrowych zmysłach. Ale skoro wyszło na jaw, że go otruto, na pewno dzieje się tu coś podejrzanego.",
    "What’s the Gate of Heaven?": "Czym jest Brama Niebios?",
    "Never heard of such a place on Earth. It’s not a place you’d be able to access through a location on our human plane.": "Nigdy nie słyszałem o takim miejscu na Ziemi. Nie da się tam dotrzeć z żadnego miejsca w naszym ludzkim świecie.",
    "So it’s not a place in North Santiva?": "Czyli to nie jest miejsce w North Santiva?",
    "Haha. I’m afraid not.": "Haha. Obawiam się, że nie.",
    "This thing looks valuable…": "To wygląda na coś wartościowego…",
    "Wait… This looks like what Lillian was looking for…": "Chwila… To chyba to, czego szukała Lillian…",
    "She was missing two of these amulets…": "Brakowało jej dwóch takich amuletów…",
    "Why is it here under the church?": "Dlaczego to jest tutaj, pod kościołem?",
    "I thought she said they were stolen by the Guild.": "Myślałem, że mówiła, iż ukradła je Gildia.",
    "Oh shit! It’s Madalyn!...": "O cholera! To Madalyn!...",
    "She’s… fingering herself… out in the open?...": "Ona… masturbuje się… na widoku?...",
    "Now’s my chance to capture her… using the holy water.": "To moja szansa, żeby ją schwytać… używając wody święconej.",
    "I just have to remember what Father Solomon said.": "Muszę tylko przypomnieć sobie, co mówił ojciec Solomon.",
    "Damn. She’s so kinky. Why the hell would she be doing this here?": "Cholera. Jest strasznie perwersyjna. Czemu do diabła robi to tutaj?",
    "I hope she didn’t do something to Lillian.": "Mam nadzieję, że nic nie zrobiła Lillian.",
    "I have to get to her without being seen…": "Muszę się do niej dostać, żeby mnie nie zauważyła…",
    "She has her eyes closed. I can make a run for it…": "Ma zamknięte oczy. Mogę do niej podbiec…",
    "I sure hope this works.": "Oby się udało.",
    "What’s she doing? How’s she doing that?": "Co ona robi? Jak ona to robi?",
    "Shit. I have no idea what the hell I’m doing… I need Father Solomon’s help.": "Cholera. Nie mam pojęcia, co robię… Potrzebuję pomocy ojca Solomona.",
    "She’s some sort of monster.": "To jakiś potwór.",
    "It’s okay. Just relax. I won't put it inside.": "Spokojnie. Rozluźnij się. Nie włożę tego do środka.",
    "Judy?": "Judy?",
    "Holy shit! The dream was real!": "Cholera! Ten sen był prawdziwy!",
    "It’s another piece of that witch idol.": "To kolejny fragment tego bożka czarownic.",
    "What will happen this time?": "Co się stanie tym razem?",
    "Huh. I don’t feel any different.": "Hm. Nie czuję żadnej różnicy.",
    "I better get out of here before lightning strikes the creek.": "Lepiej stąd wyjdę, zanim piorun uderzy w potok.",
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
print(f'Wrote {len(rows)} Common Event scene lines across {len({r["context"]["event_id"] for r in rows})} events')
