import json
from collections import Counter
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step8.jsonl')
OUTPUTS = {
    24: ROOT / 'drafts/custom-dialogue-map24-followups-02.jsonl',
    23: ROOT / 'drafts/custom-dialogue-map23-event-44-01.jsonl',
    116: ROOT / 'drafts/custom-dialogue-map116-event-4-01.jsonl',
    9: ROOT / 'drafts/custom-dialogue-map9-event-124-01.jsonl',
}
for path in OUTPUTS.values():
    if path.exists():
        raise SystemExit(f'Refusing to overwrite {path}')

MAPS = {
    (24, 55): {
        'What a pleasant surprise.': 'Co za miła niespodzianka.',
        'Heather, this is Ella.': 'Heather, to Ella.',
        'I think I recognize you from the gym.': 'Chyba kojarzę cię z siłowni.',
        'Oh, yeah! I’ve seen you doing yoga there. You must be Chloe’s mother.': 'A, tak! Widziałam, jak ćwiczysz tam jogę. Musisz być mamą Chloe.',
        'Nice to meet you, Ella.': 'Miło cię poznać, Ello.',
        'You’re just in time for a pool party.': 'W samą porę. Urządzamy imprezę przy basenie.',
        'You’re having a pool party?': 'Urządzacie imprezę przy basenie?',
        'I have to go shopping, but Sister Judy and Chloe are here.': 'Muszę iść na zakupy, ale siostra Judy i Chloe są na miejscu.',
        'Ella!': 'Ella!',
        'It’s so nice to see you again!': 'Tak miło znów cię widzieć!',
        'Looking good, you two!': 'Świetnie wyglądacie, dziewczyny!',
        'Are you here to swim?': 'Przyszłaś popływać?',
        'I’d sure like to.': 'Bardzo chętnie.',
        'Come on! I’ll show you our pool.': 'Chodź! Pokażę ci nasz basen.',
        'I hope I’m not intruding.': 'Mam nadzieję, że nie przeszkadzam.',
        'Of course not. Go and have some fun.': 'Ależ skąd. Idźcie się zabawić.',
        'Heather… Ella needs our help.': 'Heather… Ella potrzebuje naszej pomocy.',
        'I’ve gotten Judy wrapped up with the Guild and now Ella is too.': 'Wciągnąłem Judy w sprawy Gildii, a teraz również Ellę.',
        'They broke into her home.': 'Włamali się do jej domu.',
        'Oh, dear. That’s awful.': 'Ojej. To straszne.',
        'Can she stay here tonight? We’re taking down the Guild very soon… But until then, I’m worried.': 'Może zostać tu na noc? Wkrótce rozbijemy Gildię… Ale do tego czasu się o nią martwię.',
        'You think she’ll be safe here?': 'Myślisz, że będzie tu bezpieczna?',
        'You have no connection to her and no connection to the case. It would be impossible for anyone to find her here.': 'Nie jesteś z nią powiązana ani nie masz związku ze sprawą. Nikt nie wpadnie na to, żeby jej tu szukać.',
        'Of course, dear. She’s welcome to spend the night…': 'Oczywiście, kochanie. Może u nas przenocować…',
        'I’m sure Chloe and Judy would like the extra company too.': 'Chloe i Judy też na pewno ucieszą się z towarzystwa.',
        'Are you heading back to work?': 'Wracasz do pracy?',
        'No… But it’s a long story… I’ll tell you later.': 'Nie… To długa historia… Opowiem ci później.',
        'Okay, dear. I’ll see you later.': 'Dobrze, kochanie. Do zobaczenia później.',
        'Bye, Heather.': 'Pa, Heather.',
    },
    (24, 28): {
        'Heading out before supper?': 'Wychodzisz przed kolacją?',
        'Oh, I was just going to go to church.': 'Och, właśnie miałam iść do kościoła.',
        'Again?': 'Znowu?',
        'I just want to hang out with Sister Judy this evening.': 'Chcę po prostu spędzić ten wieczór z siostrą Judy.',
        'Is everything okay, Chloe?': 'Wszystko w porządku, Chloe?',
        'I’m fine, Mom.': 'W porządku, mamo.',
        'Where are you heading off to, Chloe?': 'Dokąd idziesz, Chloe?',
        'Just going to the church.': 'Po prostu do kościoła.',
        'You need to come over for supper!': 'Musisz przyjść na kolację!',
        'I just want to be alone for a little while.': 'Chcę tylko pobyć sama przez jakiś czas.',
        'Give her some space, Hannah.': 'Daj jej trochę spokoju, Hannah.',
        '1Hero! We have to save her.': '1Hero! Musimy ją uratować.',
        'Don’t be out too late, dear.': 'Nie wracaj zbyt późno, kochanie.',
        'It’s been fun, Heather. But we should head back and get started on dinner.': 'Było miło, Heather. Ale powinnyśmy wrócić i zacząć przygotowywać kolację.',
        'What’s for dinner, Ma?': 'Co będzie na kolację, mamo?',
        'You tell me. You’re the one cooking tonight.': 'Sama mi powiedz. To ty dziś gotujesz.',
        'Hannah!': 'Hannah!',
        'I’m sure you’ll make something delicious, Hannah.': 'Na pewno przygotujesz coś pysznego, Hannah.',
        'She’s getting better at cooking.': 'Coraz lepiej jej idzie gotowanie.',
        "If I’m cooking, then it's the chef's choice.": 'Skoro ja gotuję, menu wybieram ja.',
        'Whatever you say, darling.': 'Jak sobie życzysz, kochanie.',
        'Take care.': 'Trzymaj się.',
        'Staying for dinner, 1Hero?': 'Zostajesz na kolację, 1Hero?',
        'I hate to leave you alone, but I better get going.': 'Nie chcę zostawiać cię samej, ale lepiej już pójdę.',
        'Thanks for coming over, 1Hero.': 'Dzięki, że wpadłeś, 1Hero.',
        'Any time, Heather.': 'Zawsze do usług, Heather.',
        'What is it that Chloe talks about with Sister Judy?': 'O czym Chloe rozmawia z siostrą Judy?',
        'Are they talking about me?': 'Czy rozmawiają o mnie?',
    },
    (23, 44): {
        'Shit. How long has the phone been ringing?': 'Cholera. Jak długo już dzwoni ten telefon?',
        'Hannah?': 'Hannah?',
        'Well, I’ve been busy outside.': 'Cóż, byłam zajęta na zewnątrz.',
        'With, 1Hero.': 'Z 1Hero.',
        'You’re damned right. I’ll tell you about it later.': 'No pewnie. Opowiem ci później.',
        'Why is Hannah calling?': 'Czemu Hannah dzwoni?',
        'Calm your horses. I’ll pick you up.': 'Spokojnie. Przyjadę po ciebie.',
        'Hannah’s bored and wants a ride home.': 'Hannah się nudzi i chce, żeby ją odwieźć do domu.',
        'Hahaha. She’s not built for church.': 'Hahaha. Kościół nie jest dla niej.',
        'That girl has attention deficit.': 'Ta dziewczyna nie potrafi się skupić.',
        'Don’t be so hard on her.': 'Nie bądź dla niej taka surowa.',
        'Are you kidding me? I’m way too soft…': 'Żartujesz? Jestem dla niej o wiele za łagodna…',
        'You all stay back and watch some TV. I’ll be back soon.': 'Wy zostańcie i pooglądajcie telewizję. Niedługo wrócę.',
        'You don’t want company?': 'Nie chcesz, żeby ktoś z tobą pojechał?',
        "The truck is too small for all of us. I won't be long.": 'Ciężarówka jest za mała dla nas wszystkich. Niedługo wrócę.',
        'See you soon, Carol.': 'Do zobaczenia, Carol.',
        'Drive safe.': 'Jedź ostrożnie.',
        'Be careful in the bathroom. We’ve had a hell of a lot of plumbing issues lately.': 'Uważaj w łazience. Ostatnio mamy mnóstwo problemów z kanalizacją.',
        'I hope the plumbing issues aren’t too bad. Does she expect us to go outside behind a tree?': 'Oby te problemy z rurami nie były poważne. Co, mamy załatwiać się za drzewem?',
        'I bet I can fix it.': 'Założę się, że potrafię to naprawić.',
        'Don’t make a mess.': 'Tylko nie narób bałaganu.',
        'I’ve got some tools that might do that job.': 'Mam narzędzia, które mogą się przydać.',
        'Ma! We’re hungry!': 'Mamo! Jesteśmy głodne!',
        'Where’re your manners, young lady!?': 'Gdzie twoje maniery, młoda damo!?',
        'Carol, this is Ella.': 'Carol, to Ella.',
        'Well, aren’t you pretty?': 'No proszę, jaka śliczna.',
        'She’s a girly girl. But she has an arm on her.': 'Jest bardzo dziewczęca, ale ma niezły rzut.',
        'Nice to meet you, Carol. I would never have thought a woman as young as you would be a mother.': 'Miło cię poznać, Carol. Nigdy bym nie pomyślała, że ktoś tak młody jak ty ma już dzieci.',
        'Oh! Haha, aren’t you a charmer?': 'Och! Haha, ale z ciebie czaruś.',
        'Hmph!': 'Phi!',
        'Stop your belly-aching, Hannah. Dinner will be ready soon.': 'Przestań marudzić, Hannah. Kolacja będzie niedługo.',
        'What’s for dinner?': 'Co będzie na kolację?',
        'Ella, have you ever picked corn?': 'Ella, zbierałaś kiedyś kukurydzę?',
        'Our corn isn’t ripe yet.': 'Nasza kukurydza jeszcze nie dojrzała.',
        'That’s not totally true. There are some that are ready.': 'To nie do końca prawda. Kilka kolb już dojrzało.',
        'Have you been pickin’ our corn?': 'Podskubywałaś naszą kukurydzę?',
        'If we work together, we can find some ripe ones.': 'Jeśli poszukamy razem, znajdziemy dojrzałe kolby.',
        'Sounds fun!': 'Brzmi fajnie!',
        'Let’s hurry!': 'Pospieszmy się!',
    },
    (116, 4): {
        'Ella!': 'Ella!',
        '1Hero!': '1Hero!',
        'The monsters escaped!': 'Potwory uciekły!',
        'We saw monsters!': 'Widzieliśmy potwory!',
        'Nellie left before the demons came out of the rift. She hasn’t returned!': 'Nellie wyszła, zanim demony wydostały się z rozdarcia. Jeszcze nie wróciła!',
        'A smoke break? I don’t know.': 'Poszła zapalić? Nie wiem.',
        'Erica’s body is gone!': 'Ciało Eriki zniknęło!',
        'I failed to save her.': 'Nie udało mi się jej uratować.',
        'Did you dye your hair?': 'Przefarbowałaś włosy?',
        'Are those wings?': 'Czy to skrzydła?',
        'A demon named Daemalius took Erica and he’s looking to take revenge on Madalyn.': 'Demon imieniem Daemalius porwał Ericę i chce zemścić się na Madalyn.',
        'Another demon?': 'Kolejny demon?',
        'Madalyn tricked him and used him to open the rift.': 'Madalyn go oszukała i wykorzystała, żeby otworzyć rozdarcie.',
        'Did you see Lilith? Did the demons have the Toma with them?': 'Widziałeś Lilith? Demony miały ze sobą Tomę?',
        'Negative. Only demons and no statue to be seen.': 'Nie. Były tam tylko demony, żadnego posągu.',
        'I have no idea where Lillian is.': 'Nie mam pojęcia, gdzie jest Lillian.',
        'Guess who has a bomb?': 'Zgadnij, kto ma bombę.',
        'You have a bomb?': 'Masz bombę?',
        'Are you here to arrest me?': 'Przyszłaś mnie aresztować?',
        'Not exactly the highest priority right now.': 'To nie jest teraz nasz najpilniejszy problem.',
        'Tasha, Daemalius is back!': 'Tasha, Daemalius wrócił!',
        'We lost her… This new demon named Daemalius took her.': 'Straciliśmy ją… Porwał ją nowy demon, Daemalius.',
        'We have to open the rift and bomb the shit out of it.': 'Musimy otworzyć rozdarcie i rozwalić je w drobny mak.',
        'That’s not the plan.': 'To nie jest plan.',
        'We lost Erica and we have a bomb. It’s worth a shot.': 'Straciliśmy Ericę, a mamy bombę. Warto spróbować.',
        'It could work… All of the worlds are vulnerable to attack.': 'To może zadziałać… Wszystkie światy są narażone na atak.',
        'Daemalius wants revenge. He’ll come here. I know it.': 'Daemalius chce zemsty. Przyjdzie tutaj. Wiem to.',
        '1Hero… What do we do?': '1Hero… Co robimy?',
        'I…': 'Ja…',
        'Find hairs from Lillian or any other demon part…': 'Znajdź włosy Lillian albo inną część demona…',
        'You know what to do, 1Hero.': 'Wiesz, co robić, 1Hero.',
        'If this new monster comes here, what the hell are we supposed to do?': 'Jeśli ten nowy potwór tu przyjdzie, co mamy, do cholery, zrobić?',
        'We have an arsenal of holy weapons.': 'Mamy cały arsenał świętej broni.',
        'I can help. I can help protect everyone.': 'Mogę pomóc. Mogę wszystkich chronić.',
        'I’ve got the amulets.': 'Mam amulety.',
        'And we have holy bombs.': 'Mamy też święte bomby.',
        'This is insane.': 'To szaleństwo.',
        'Father can handle demons. I’ve seen it.': 'Ojciec potrafi radzić sobie z demonami. Widziałem to.',
        'Why are you here? Who’s keeping an eye on the girls?': 'Czemu tu jesteś? Kto pilnuje dziewczyn?',
        'They are safe in the church. Stay focused.': 'Są bezpieczne w kościele. Skup się.',
        'Hey… Where’s Mom?': 'Hej… Gdzie jest mama?',
        'I’ll search the mansion for Nellie… and see if I can find more demon parts to open the rift.': 'Przeszukam rezydencję w poszukiwaniu Nellie… i sprawdzę, czy znajdę więcej części demona, by otworzyć rozdarcie.',
        'Erica’s soul could be waiting for us on the other side.': 'Dusza Eriki może czekać na nas po drugiej stronie.',
        'If only we had the body…': 'Gdybyśmy tylko mieli jej ciało…',
        'Father… Stay here and make sure everyone is safe.': 'Ojcze… Zostań tutaj i dopilnuj, żeby wszyscy byli bezpieczni.',
        'Hurry and open the rift. We have to save Erica… And find the Toma.': 'Pospiesz się i otwórz rozdarcie. Musimy uratować Ericę… i odnaleźć Tomę.',
        'Lillian!': 'Lillian!',
        'Has Erica arrived?': 'Erica już dotarła?',
        'She’s in Hell…': 'Jest w piekle…',
        'Shit… What a mess.': 'Cholera… Ale bałagan.',
        'You can’t hide, sister!': 'Nie ukryjesz się, siostrzyczko!',
        'Having trouble keeping up, brother?': 'Nie nadążasz, braciszku?',
        'You’ve chosen the wrong place to run. Do you dare bring me to Hell?': 'Źle wybrałeś miejsce ucieczki. Naprawdę chcesz zabrać mnie do piekła?',
        'What better place to end this feud?': 'Czy jest lepsze miejsce, by zakończyć ten spór?',
        'Uhh… That could be a problem… The girls are in Hell too.': 'Eee… To może być problem… Dziewczyny też są w piekle.',
        'You can’t run anymore. It’s time to make this right.': 'Nie możesz już uciekać. Czas to naprawić.',
        'Shit!... Run!': 'Cholera!... Uciekaj!',
    },
    (9, 124): {
        'You’re just in time, 1Hero.': 'W samą porę, 1Hero.',
        'I get to pet a goat!': 'Mogę pogłaskać kozła!',
        'You have to catch him first!': 'Najpierw musisz go złapać!',
        'Hannah!': 'Hannah!',
        'Get ’em, girl!': 'Dawaj, mała!',
        'I can’t do it.': 'Nie dam rady.',
        'If you can’t catch a little goat, how do you expect to catch… a bigger goat!': 'Skoro nie potrafisz złapać małego kozła, jak chcesz złapać… większego kozła!',
        'Do I have to catch a bigger goat?': 'Muszę złapać większego kozła?',
        'Is that what you’re up to, Hannah? Looking for the goat’s mother?': 'O to ci chodzi, Hannah? Szukasz matki tego kozła?',
        'Yeah!... Of course!... Now help me train Alia.': 'Tak!... Oczywiście!... A teraz pomóż mi trenować Alię.',
        'You’ve got the look of a killer!': 'Masz minę zabójczyni!',
        'I’m a good judge of character… Now, let me show you how it’s done.': 'Znam się na ludziach… Patrz, pokażę ci, jak to się robi.',
        'See! It’s easy!': 'Widzisz? To łatwe!',
        'You sure are fast!': 'Ale jesteś szybka!',
        'Of course I’m fast… Maybe you have a different skill we can use.': 'Oczywiście, że jestem szybka… Może masz jakiś inny talent, który się przyda.',
        'I’m sorry. I don’t have skills.': 'Przykro mi. Nie mam żadnych talentów.',
        'Nonsense! Let’s see if you can aim… Let me get my bow and arrow.': 'Bzdura! Sprawdźmy, czy umiesz celować… Przyniosę łuk i strzały.',
        'I didn’t know I look like a killer.': 'Nie wiedziałam, że wyglądam na zabójczynię.',
        'You… don’t…': 'No… nie…',
        'Don’t tell Hannah… I think she’d get upset.': 'Nie mów Hannah… Chyba by się zdenerwowała.',
        'Hey! What did you do with my bow and arrow?': 'Hej! Co zrobiłaś z moim łukiem i strzałami?',
        'I’m sorry!': 'Przepraszam!',
        'I’m not talking to you.': 'Nie odzywam się do ciebie.',
        'I don’t have it, Hannah. You probably lost it.': 'Nie mam go, Hannah. Pewnie sama go zgubiłaś.',
        'I’ve got speed, Alia has aim, you’ve got detective power…': 'Ja jestem szybka, Alia dobrze celuje, a ty masz detektywistyczny zmysł…',
        'Go find it!': 'Idź go znaleźć!',
        'Ask nicely.': 'Poproś ładnie.',
        'Please, daddy… Get us adorable girls a nice bow and arrow.': 'Proszę, tatusiu… Kup nam, uroczym dziewczynkom, porządny łuk i strzały.',
        'That sounds fun. I want to try it.': 'Brzmi fajnie. Też chcę spróbować.',
        'See, 1Hero! You’re going to let us down if you don’t help.': 'Widzisz, 1Hero? Zawiedziesz nas, jeśli nam nie pomożesz.',
        'Come on, Alia! I’ll show you the barn while 1Hero finds the bow and arrow he lost.': 'Chodź, Alia! Pokażę ci stodołę, a 1Hero poszuka swojego zgubionego łuku i strzał.',
        'I didn’t lose it…': 'Wcale go nie zgubiłem…',
        'What’s she up to?': 'Co ona kombinuje?',
    },
}

known = set()
for line in MERGED.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    if row['translation'].strip():
        known.add(row['id'])
rows_by_map = {map_id: [] for map_id in OUTPUTS}
missing = set()
counts = Counter()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    map_id = context.get('map_id')
    event_id = context.get('event_id')
    key = (map_id, event_id)
    if context.get('source_kind') != 'map' or key not in MAPS or row['id'] in known:
        continue
    source = row['source_text'].strip()
    if not source or source.startswith('/') or source in {'…', '...', '..'}:
        continue
    translation = MAPS[key].get(source)
    if translation is None:
        missing.add((key, source))
        continue
    row['translation'] = translation
    rows_by_map[map_id].append(row)
    counts[key] += 1
if missing:
    raise SystemExit('Unmapped strings: ' + repr(sorted(missing)))
for map_id, rows in rows_by_map.items():
    OUTPUTS[map_id].write_text(
        ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
        encoding='utf-8',
        newline='\n',
    )
    print(f'Wrote Map {map_id} follow-up dialogue: {len(rows)} records')
print('Event counts:', ', '.join(f'Map {m} event {e}={n}' for (m, e), n in sorted(counts.items())))
