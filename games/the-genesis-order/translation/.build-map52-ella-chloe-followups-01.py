#!/usr/bin/env python3
"""Build Polish drafts for player-facing Ella and Chloe dialogue on Map 52."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map52-ella-chloe-followups-01.jsonl'
TRANSLATIONS = {
    'I take it you like pink.': 'Widzę, że lubisz różowy.',
    'My favorite color, for sure.': 'Zdecydowanie mój ulubiony kolor.',
    'So, what do you say, 1Hero? A pretty nice reward. Isn’t it?': 'No i co ty na to, 1Hero? Całkiem niezła nagroda, prawda?',
    'I’ve never had sex like that before.': 'Nigdy wcześniej nie uprawiałem takiego seksu.',
    'Well, aren’t I a special girl to be your first anal experience.': 'No proszę, jestem wyjątkowa — to twój pierwszy raz z seksem analnym.',
    'Ella… I can’t always be on call. I’m a pretty busy man.': 'Ella… Nie zawsze mogę być na każde zawołanie. Jestem dość zajętym facetem.',
    'You came through today.': 'Dzisiaj mi pomogłeś.',
    'You’re right. But I’ve got a big case I’m working on.': 'Masz rację. Ale pracuję nad poważną sprawą.',
    'Sounds exciting! Care to share any juicy details?': 'Brzmi ekscytująco! Zdradzisz jakieś soczyste szczegóły?',
    'Sorry, I can’t share information about a case.': 'Przykro mi, nie mogę zdradzać szczegółów sprawy.',
    'I shared my ass with you, 1Hero. You can tell me something.': 'Dałam ci dupy, 1Hero. Możesz mi coś powiedzieć.',
    'Haha. I guess you’re right about that.': 'Haha. Chyba masz rację.',
    'You’re following my neighbor to the Wilkes Mansion. I saw you with her.': 'Widziałam, jak szedłeś z moją sąsiadką do rezydencji Wilkesów.',
    'Erica? Well… I might just be investigating a murder. But… I don’t know yet.': 'Erica? Cóż… Możliwe, że badam sprawę morderstwa. Ale… jeszcze nie mam pewności.',
    'Well, I hope it’s not too dangerous.': 'Mam nadzieję, że to nic zbyt niebezpiecznego.',
    'Honestly, I don’t know how dangerous this case might end up being…': 'Szczerze mówiąc, nie wiem, jak niebezpieczna może się okazać ta sprawa…',
    'I think there could be a larger criminal organization responsible.': 'Podejrzewam, że stoi za tym większa organizacja przestępcza.',
    'Oh, my… Operating in our city?': 'Ojej… Działają w naszym mieście?',
    'Possibly.': 'Możliwe.',
    'That sounds super interesting. But it has me even more worried.': 'To brzmi naprawdę ciekawie. Ale jeszcze bardziej się martwię.',
    'Don’t worry. This criminal organization is falling apart…': 'Nie martw się. Ta organizacja przestępcza się rozpada…',
    'There have been lots of arrests already.': 'Już dokonano wielu aresztowań.',
    'You’re talking about the Eclipse Guild.': 'Mówisz o Gildii Eclipse.',
    'You know about them?': 'Wiesz o nich?',
    'They have been all over the news lately. I didn’t know you were working on that case.': 'Ostatnio ciągle o nich mówią w wiadomościach. Nie wiedziałam, że pracujesz nad tą sprawą.',
    'Oh, well… I’m trying.': 'No cóż… Staram się.',
    'I can see that you’re a busy man, 1Hero.': 'Widzę, że masz sporo na głowie, 1Hero.',
    'If something serious happens, you can call me.': 'Gdyby stało się coś poważnego, możesz do mnie zadzwonić.',
    'I want you to have my phone number.': 'Chcę, żebyś miał mój numer telefonu.',
    'I never give this number away.': 'Nigdy nikomu nie podaję tego numeru.',
    "It’s safe with me, Ella. I won't tell anyone.": 'Możesz mi zaufać, Ella. Nikomu nie powiem.',
    'Sure, Ella. I can’t turn down helping a girl in need.': 'Jasne, Ella. Nie odmówię pomocy damie w potrzebie.',
    'Strip naked you two, join me on the bed.': 'Rozbierzcie się do naga i chodźcie do mnie na łóżko.',
    'Damn, girl! That was fast.': 'Nieźle, dziewczyno! Ale szybko.',
    'When it’s time, I’m ready.': 'Kiedy przyjdzie pora, będę gotowa.',
    'Is that bed big enough for the three of us?': 'Czy to łóżko pomieści nas troje?',
    'Don’t plan on having personal space, stud muffin.': 'Nie licz na odrobinę prywatności, przystojniaku.',
    'How about it, Erica? Are you ready?': 'No i jak, Erica? Gotowa?',
    'You know, Ella, you’re not my first girl.': 'Wiesz, Ella, nie jesteś pierwszą dziewczyną, z którą byłem.',
    'Ohh! You have experience. I like it.': 'Och! Masz doświadczenie. Podoba mi się.',
    'Damn! You’d make so much money on Lustagram!': 'Cholera! Zarabiałabyś kupę kasy na Lustagramie!',
    'You really think so?': 'Naprawdę tak myślisz?',
    'You’ve got a nice, exotic vibe.': 'Masz w sobie coś egzotycznego.',
    'Are you making fun of me?': 'Nabijasz się ze mnie?',
    'No way! Your look is totally in style right now.': 'Skąd! Twój styl jest teraz bardzo modny.',
    'What about me? Do you think the ladies would pay to watch this monster swing around?': 'A co ze mną? Myślisz, że dziewczyny zapłaciłyby za oglądanie tego potwora w akcji?',
    'Hahahaha.': 'Hahahaha.',
    '1Hero! Don’t be crude.': '1Hero! Nie bądź wulgarny.',
    'Sorry, 1Hero. There’s no market without stars like Erica and I.': 'Wybacz, 1Hero. Bez gwiazd takich jak Erica i ja nie ma rynku.',
    'Get on the bed, girl. I’ll show you just how pretty I think you are.': 'Chodź na łóżko, kochana. Pokażę ci, jak bardzo mi się podobasz.',
    'You and me both, girl. That was everything I thought it would be.': 'Mam tak samo. Było dokładnie tak, jak sobie wyobrażałam.',
    'What do you think, Erica? Would you like to live the life of a cam girl?': 'Co o tym myślisz, Erica? Chciałabyś zostać camgirl?',
    'Hahaha. You make it seem nice, Ella.': 'Hahaha. Przedstawiasz to w samych superlatywach, Ella.',
    'It beats some other lines of work. Trust me.': 'To lepsze niż niektóre inne zajęcia. Zaufaj mi.',
    'I think I’ll stick with being a housemaid for now.': 'Na razie zostanę przy pracy pokojówki.',
    'No need to rush home. Feel free to spend the night.': 'Nie musisz się spieszyć do domu. Możesz przenocować.',
    'I don’t mind if I do.': 'Chętnie skorzystam.',
    'Such a gracious host.': 'Cóż za wspaniała gospodyni.',
    'Dammit! Lillian is expecting me at the mansion!': 'Cholera! Lillian czeka na mnie w rezydencji!',
    'What’s wrong, you two? Long night?': 'Co z wami? Długa noc?',
    'Shit, shit, shit. It’s been fun. But I’ve got to get to work.': 'Cholera, cholera, cholera. Było miło, ale muszę iść do pracy.',
    'Erica…': 'Erica…',
    'Don’t worry, 1Hero. My uniform is at the mansion.': 'Nie martw się, 1Hero. Mój mundur jest w rezydencji.',
    'I’ll help you get into your home after work.': 'Pomogę ci dostać się do domu po pracy.',
    'Too bad you two aren’t into camming.': 'Szkoda, że nie kręci was praca przed kamerką.',
    'I make my own hours.': 'Sama ustalam sobie grafik.',
    'Sounds nice.': 'Brzmi nieźle.',
    'I’d never live that down with my family…': 'Rodzina nigdy by mi tego nie zapomniała…',
    'But, I’m glad it works for you.': 'Ale cieszę się, że tobie pasuje.',
    'You’re welcome back any time, Erica.': 'Możesz wrócić, kiedy tylko zechcesz, Erica.',
    'Maybe some one-on-one time… Just the girls and a couple of wet, tasty pussies.': 'Może spotkanie sam na sam… Tylko dziewczyny i parę mokrych, smakowitych cip.',
    'Damn, Ella. You never turn it off, do you?': 'Ella, ty nigdy nie odpuszczasz, co?',
    'See you later.': 'Do zobaczenia.',
    'You know, I will.': 'Wiesz, że wrócę.',
    'That’s one hell of a catch you got there, 1Hero.': 'Ale ci się trafiła dziewczyna, 1Hero.',
    'Just don’t get on her bad side, Ella.': 'Tylko jej nie podpadnij, Ella.',
    'I’m kinda scared… But also excited.': 'Trochę się boję… ale jestem też podekscytowana.',
    'And you’re sure you want this?': 'Na pewno tego chcesz?',
    'If it’s okay for Sister Judy, it’s okay for me.': 'Skoro siostrze Judy to nie przeszkadza, mnie też nie.',
    'You’re so pretty, Chloe! You have a girl-next-door vibe. It’s like you’re molded to fit that archetype.': 'Chloe, jesteś śliczna! Masz urok dziewczyny z sąsiedztwa. Jakbyś była stworzona do tej roli.',
    'Uhhh… Thanks.': 'Eee… Dzięki.',
    'That’s a good thing! You’d pull in a lot of money on Lustagram.': 'To dobrze! Zarabiałabyś fortunę na Lustagramie.',
    'If Judy can take it, I can too.': 'Skoro Judy dała radę, ja też dam.',
    'We’re going to need to train your butt.': 'Będziemy musiały wytrenować twój tyłek.',
    '1Hero. Can you find my buttplugs?': '1Hero, możesz znaleźć moje korki analne?',
    'Buttplugs?': 'Korki analne?',
    'There’s nothing to fear. I have three sizes…': 'Nie ma się czego bać. Mam trzy rozmiary…',
    'Small, medium and large.': 'Mały, średni i duży.',
    'By starting small and working up, you won’t feel any stretching.': 'Zaczniemy od małego i stopniowo przejdziemy do większych — nie poczujesz rozciągania.',
    'Sounds complicated.': 'Brzmi skomplikowanie.',
    'Trust me. You’ll feel nothing but pleasure.': 'Zaufaj mi. Poczujesz tylko przyjemność.',
    'Uh… Good question. I tend to lose things.': 'Eee… Dobre pytanie. Ciągle coś gubię.',
    'Check around my house. I’m sure they are here somewhere.': 'Rozejrzyj się u mnie w domu. Na pewno gdzieś tu są.',
    'Bring me more girls, 1Hero. I can train anybody to take it in the ass.': 'Sprowadzaj mi więcej dziewczyn, 1Hero. Każdą nauczę przyjmować w tyłek.',
    'I can’t wait to meet this naughty nun.': 'Nie mogę się doczekać, aż poznam tę niegrzeczną zakonnicę.',
    'Oh, uhh… Thanks.': 'Eee… Dzięki.',
    'I’m sorry, 1Hero. I must have accidentally moved my hips.': 'Przepraszam, 1Hero. Chyba przez przypadek poruszyłam biodrami.',
    'Maybe next time you let the boy plow your pussy.': 'Może następnym razem pozwolisz temu facetowi zerżnąć cię w cipkę.',
    'I can’t… I don’t want to upset Sister Judy.': 'Nie mogę… Nie chcę denerwować siostry Judy.',
    'It’s okay, Chloe. We’ll be careful next time.': 'W porządku, Chloe. Następnym razem będziemy ostrożne.',
    'I’ve got all three sizes. Now what?': 'Mam już wszystkie trzy rozmiary. Co teraz?',
    'You’re too funny, Chloe. But I respect the effort.': 'Ale z ciebie żartownisia, Chloe. Doceniam wysiłek.',
    'Now the magic begins.': 'A teraz zaczyna się magia.',
    'What made you decide to become a cam girl?': 'Co skłoniło cię do zostania camgirl?',
    'Let’s just say my previous job was a bit too stressful.': 'Powiedzmy, że poprzednia praca była trochę zbyt stresująca.',
    'Take off your pants, Chloe. You’re going to love this!': 'Zdejmij spodnie, Chloe. Spodoba ci się!',
    'I suppose it would be fun to have fans and be famous.': 'Chyba fajnie byłoby mieć fanów i być sławną.',
    'Okay… I trust you. But this better not hurt.': 'Dobrze… Ufam ci. Ale to lepiej niech nie boli.',
    'I wouldn’t call myself famous. But I do have my share of fans.': 'Nie nazwałabym siebie sławną. Ale mam trochę fanów.',
    "It won't.": 'Nie będzie.',
    'I think 1Hero might just get a fan following of his own.': 'Myślę, że 1Hero też mógłby zdobyć własnych fanów.',
    'The news broadcasts, silly!': 'Wiadomości, głuptasie!',
    'Oh, yeah. I’ve been told I’m good in front of a camera.': 'A, tak. Mówiono mi, że dobrze wypadałam przed kamerą.',
    'You know I think so!': 'Wiesz, że tak uważam!',
    'Just have to be more careful which camera.': 'Musisz tylko ostrożniej wybierać kamery.',
    'Looks like you found the buttplugs.': 'Widzę, że znalazłeś korki analne.',
    'Hahaha. Oh, Chloe. Maybe you can help me convince 1Hero to do a collaboration with me.': 'Hahaha. Och, Chloe. Może pomożesz mi namówić 1Hero na wspólny występ.',
    'Not all of them.': 'Nie wszystkie.',
    'Don’t even joke about that.': 'Nawet sobie z tego nie żartuj.',
    'Keep looking. We need all three.': 'Szukaj dalej. Potrzebujemy wszystkich trzech.',
    'I’m kidding.': 'Żartuję.',
    'I probably should get home. I told my mom that I’d come home after eating with Sister Judy.': 'Chyba powinnam wracać do domu. Powiedziałam mamie, że wrócę po kolacji z siostrą Judy.',
    'I’d love to meet Judy. She sounds like a fun nun.': 'Chętnie poznam Judy. Brzmi jak zakonnica z poczuciem humoru.',
    'Maybe 1Hero can invite Erica too, and we can all go to church together.': 'Może 1Hero zaprosi też Ericę i wszyscy pójdziemy razem do kościoła.',
    '… Or something else.': '…Albo zrobimy coś innego.',
    'I’ll think of something fun we can do.': 'Wymyślę coś fajnego, co możemy razem robić.',
    'Look around my place. I have three sizes of buttplugs. I need all three for this to work.': 'Rozejrzyj się u mnie. Mam korki analne w trzech rozmiarach. Potrzebuję wszystkich trzech, żeby to zadziałało.',
    'It was nice meeting you, Chloe.': 'Miło było cię poznać, Chloe.',
    'Same, Ella. See ya around.': 'Wzajemnie, Ella. Do zobaczenia.',
    'Thanks for the help. You sure know your way around some kinky things.': 'Dzięki za pomoc. Znasz się na tych perwersyjnych zabawach.',
    'When she’s ready for the real deal, let me know.': 'Daj znać, kiedy będzie gotowa na prawdziwe igraszki.',
    'Don’t get your hopes too high. If you want to get wild, Erica is your best bet.': 'Nie rób sobie zbyt wielkich nadziei. Jeśli chcesz zaszaleć, najlepszym wyborem będzie Erica.',
    'I already know what she’s capable of.': 'Wiem już, na co ją stać.',
    'See you later, Ella.': 'Do zobaczenia, Ella.',
    'Bye, stud muffin.': 'Pa, przystojniaku.',
}

known = set()
for path in (ROOT / 'drafts').rglob('*.jsonl'):
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
        or context.get('source_kind') != 'map'
        or context.get('map_id') != 52
        or context.get('translation_policy') == 'keep_source_value'
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
    raise SystemExit('Unmapped Map 52 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 135:
    raise SystemExit(f'Expected exactly 135 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 52 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
