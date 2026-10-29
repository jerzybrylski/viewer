import json
from collections import Counter
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step6.jsonl')
OUT = ROOT / 'drafts/custom-dialogue-map3-events-41-47-56-01.jsonl'
if OUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUT}')

MAPS = {
    41: {
        '1Hero, I’m worried about Ella.': '1Hero, martwię się o Ellę.',
        'I heard some loud noises coming from her apartment and I went to check on her and she was gone.': 'Słyszałam głośne hałasy dobiegające z jej mieszkania. Poszłam sprawdzić, co się dzieje, ale jej nie było.',
        'Loud noises?': 'Głośne hałasy?',
        'It sounded like someone was trashing the place. Something is wrong.': 'Brzmiało, jakby ktoś demolował mieszkanie. Coś jest nie tak.',
        'Okay. I’ll head over.': 'Dobrze. Już jadę.',
    },
    47: {
        '1Hero. You look concerned.': '1Hero. Wyglądasz na zmartwionego.',
        'Andrea has a connection to the Guild that’s deeper than this investigation… or her so-called honeypot.': 'Andrea jest powiązana z Gildią znacznie głębiej, niż wynikałoby z tego śledztwa… i jej rzekomej roli przynęty.',
        'It’s… It probably doesn’t really matter to you, Arianna.': 'To… Pewnie nie ma to dla ciebie większego znaczenia, Arianno.',
        'Everything is happening for a reason. Every step in your journey I am here to guide you.': 'Wszystko dzieje się z jakiegoś powodu. Jestem tu, by prowadzić cię na każdym kroku.',
        'If there’s a gateway to Hell, does that mean there can be a gateway to Heaven too?': 'Skoro istnieje portal do piekła, to czy może istnieć też portal do Nieba?',
        'A gateway to the Empyrean?... I would be surprised…': 'Portal do Empyreum?... Zdziwiłabym się…',
        'But how did you get here? Does the Oracle have a tiny portal in it?': 'Ale jak się tu dostałaś? Czy Wyrocznia ma w sobie mały portal?',
        'Honestly… I don’t know. I am as surprised as you that I am able to be here on Earth with you.': 'Szczerze… Nie wiem. Tak samo jak ty jestem zaskoczona, że mogę być tu, na Ziemi, razem z tobą.',
        'Are you part human?': 'Czy masz w sobie coś z człowieka?',
        'No, silly. I am a pure angel.': 'Nie, głuptasie. Jestem czystym aniołem.',
        'I consider myself a good detective, but this otherworldly stuff gets confusing…': 'Uważam się za dobrego detektywa, ale te sprawy z zaświatów robią się zagmatwane…',
        'According to Zephaniah, only humans can pass through the rift.': 'Według Zephaniaha tylko ludzie mogą przechodzić przez rozdarcie.',
        "And a good thing that holds true. We wouldn't want any demons slipping through.": 'I dobrze. Nie chcielibyśmy, żeby przedostał się tędy jakiś demon.',
        'Melissa is calling?': 'Dzwoni Melissa?',
        'Where the hell are you?': 'Gdzie ty, do cholery, jesteś?',
        'Why? What do you need?': 'A czemu? Czego potrzebujesz?',
        'Something’s happened at the station.': 'Coś się stało na posterunku.',
        'One of Duncan’s henchmen made an escape.': 'Jeden z ludzi Duncana uciekł.',
        'The commissioner just arrived… I’ve got to go.': 'Właśnie przyjechała pani komisarz… Muszę kończyć.',
        'Shit. How the hell did he get out?': 'Cholera. Jak on zdołał uciec?',
        '1Hero! Something bad has happened!': '1Hero! Stało się coś złego!',
        'I know! I’m heading to the church now. I need Father’s help…': 'Wiem! Jadę teraz do kościoła. Potrzebuję pomocy księdza…',
        'Lillian is a demon!': 'Lillian to demon!',
        'No, 1Hero. She can’t be. She went through the portal.': 'Nie, 1Hero. To niemożliwe. Przeszła przez portal.',
        'I saw her teleport! She just did it!': 'Widziałem, jak się teleportowała! Zrobiła to na moich oczach!',
        'But… It’s impossible… Her body is human. She’s not a demon.': 'Ale… To niemożliwe… Ma ludzkie ciało. Nie jest demonem.',
        'If her body is human, she’s got a demon’s soul. I know what I saw…': 'Jeśli ma ludzkie ciało, to jej dusza należy do demona. Wiem, co widziałem…',
        'The Toma may already be completed… She’s going to use it to bring demons to Earth!': 'Toma może być już ukończona… Użyje jej, by sprowadzić demony na Ziemię!',
        'Go, 1Hero! I will help you in any way I can!': 'Leć, 1Hero! Pomogę ci, jak tylko będę mogła!',
        'Lillian has a mouthful of my cum!': 'Lillian ma w ustach pełno mojej spermy!',
        'She’s going to blow it up Erica’s pussy!': 'Zaraz wdmucha ją do cipki Eriki!',
        'Who knows what other sexual things they are going to do to her!?': 'Kto wie, co jeszcze seksualnego jej zrobią!?',
        'Cum up the ass? Are they going to French kiss with my cum? I don’t know…': 'Spuszczą się jej do tyłka? Będą się namiętnie całować z moją spermą w ustach? Nie wiem…',
        '1Hero… I get the point.': '1Hero… Już rozumiem.',
        'A bunch of really sexy girls and demons are going to play with my cum and it’s going to bring about the end of the world!': 'Stado seksownych dziewczyn i demonów będzie się bawić moją spermą, a przez to nastąpi koniec świata!',
        'Hurry up, 1Hero! You’re not helping the situation by being so… descriptive.': 'Pospiesz się, 1Hero! Nie pomagasz, gdy tak… szczegółowo to opisujesz.',
        'Oh, yeah… I’m on my way.': 'A, tak… Już jadę.',
        'Arianna, I need your help.': 'Arianno, potrzebuję twojej pomocy.',
        'You need my guidance?': 'Potrzebujesz mojego przewodnictwa?',
        'Lillian completed the Toma!...': 'Lillian ukończyła Tomę!...',
        'She’s already starting to build an army!': 'Już zaczyna tworzyć armię!',
        'No! That can’t be. You were meant to stop her...': 'Nie! To niemożliwe. Miałeś ją powstrzymać…',
        'She has an army?': 'Ma armię?',
        'They are trapped in Hell… But…': 'Są uwięzieni w piekle… Ale…',
        'Lillian is Lilith!': 'Lillian to Lilith!',
        'You didn’t know that?': 'Nie wiedziałaś?',
        'Of course I didn’t know that! She’s a demon!': 'Oczywiście, że nie wiedziałem! Przecież to demon!',
        'Her name is Lillian. Wasn’t it obvious?': 'Ma na imię Lillian. To nie było oczywiste?',
        'What!? Obvious?... I don’t know these things!': 'Co!? Oczywiste?... Skąd miałem to wiedzieć!',
        'Next time I’ll be sure to tell you.': 'Następnym razem na pewno ci powiem.',
        'All I know is that the woman who comes through the portal looks a lot different from the woman I saw in Hell.': 'Wiem tylko, że kobieta, która przechodzi przez portal, wygląda zupełnie inaczej niż ta, którą widziałem w piekle.',
        'Lilith can’t leave Hell through a rift… She must be doing something to escape.': 'Lilith nie może opuścić piekła przez rozdarcie… Musi kombinować, jak się stąd wydostać.',
        'Can we trap her inside?... Can we close the rift for good?': 'Możemy ją tam uwięzić?... Zamknąć rozdarcie na zawsze?',
        'What a great idea!': 'Świetny pomysł!',
        'Great! How do we do it?': 'Świetnie! Jak to zrobić?',
        'What a great question!': 'Świetne pytanie!',
        'I’m a bit lost, 1Hero… But this must be the Lord’s path…': 'Trochę się w tym gubię, 1Hero… Ale to musi być droga wyznaczona przez Pana…',
        'You will find a way!': 'Znajdziesz sposób!',
        'Arianna… Why does Lillian want these three weird amulets?': 'Arianno… Po co Lillian te trzy dziwne amulety?',
        'I wish I knew more about her desires. But I’m sure it’s not good.': 'Chciałabym wiedzieć więcej o jej zamiarach, ale z pewnością nie wróżą nic dobrego.',
        'There’s a book that talked about amulets being able to take away her power.': 'Czytałem w książce, że amulety mogą odebrać jej moc.',
        'That would certainly be a reason to not have them in the hands of your enemies.': 'To z pewnością dobry powód, by nie oddawać ich w ręce wrogów.',
        'I had two of them and now they are gone.': 'Miałem dwa, ale już ich nie mam.',
        'What did you do with them!?': 'Co z nimi zrobiłeś!?',
        'They got stolen.': 'Ukradziono mi je.',
        'Who would do such a thing? Did that demon woman steal from you?': 'Kto mógłby coś takiego zrobić? Ta demonica ci je ukradła?',
        'First… My father… Duncan… He stole the one I found under the church.': 'Najpierw… Mój ojciec… Duncan. Ukradł ten, który znalazłem pod kościołem.',
        'And the other one?': 'A co z drugim?',
        'I found another one in Andrea’s treasure collection… Sister Judy stole that one.': 'Znalazłem drugi w kolekcji skarbów Andrei… Ten ukradła siostra Judy.',
        'Why do people close to you keep stealing your stuff?': 'Dlaczego twoi bliscy ciągle kradną ci rzeczy?',
        'That’s not the point. Lillian now has all three amulets.': 'Nieważne. Lillian ma teraz wszystkie trzy amulety.',
        'I wish I had paid more attention in angel school… But I believe that an amulet with the power of God cannot be destroyed.': 'Szkoda, że nie uważałam na lekcjach w anielskiej szkole… Wierzę jednak, że amuletu z mocą Boga nie da się zniszczyć.',
        'In that case, there’s a chance we can find all three.': 'W takim razie możemy je wszystkie odzyskać.',
        'Do you know where she’s hiding them?': 'Wiesz, gdzie je ukrywa?',
        'She doesn’t leave the mansion very often… But I don’t know where else she could have gone.': 'Rzadko opuszcza rezydencję… Ale nie wiem, gdzie indziej mogłaby je ukryć.',
        'But we’re running out of time. I need to find Kimberly and get the Toma back.': 'Ale kończy nam się czas. Muszę odnaleźć Kimberly i odzyskać Tomę.',
        'Don’t let that idol see the light of day.': 'Nie pozwól, by ten idol ujrzał światło dzienne.',
        'I know… Lillian has a plan… She’s being selective on who she lets see it…': 'Wiem… Lillian ma plan… Ostrożnie wybiera, komu pozwala go zobaczyć…',
        'Otherwise, it would probably already be too late.': 'W przeciwnym razie pewnie byłoby już za późno.',
        'You will succeed, 1Hero. It is God’s will.': 'Uda ci się, 1Hero. Taka jest wola Boga.',
    },
    56: {
        'I should give Nellie a call… Perhaps she can help me figure out this briefcase.': 'Powinienem zadzwonić do Nellie… Może pomoże mi rozgryźć tę teczkę.',
        'Hi, Nellie. I have some questions for you.': 'Cześć, Nellie. Chciałem cię o coś zapytać.',
        'Uh oh, it’s Detective Canmore. Should I be worried?': 'Oho, detektyw Canmore. Mam się martwić?',
        'Heh, no. But you know my dad better than anyone.': 'Heh, nie. Ale znasz mojego ojca lepiej niż ktokolwiek.',
        'I’m trying to break into an old briefcase of his, but I don’t know the code.': 'Próbuję otworzyć jego starą teczkę, ale nie znam szyfru.',
        'Any ideas?': 'Masz jakiś pomysł?',
        'An old briefcase? I don’t know anything about that.': 'Starą teczkę? Nic o niej nie wiem.',
        'But codes…': 'Ale szyfry…',
        'The Eclipse Guild had a system for generating codes, back when the Guild had several leaders.': 'Gdy Gildią Zaćmienia kierowało kilka osób, mieli system generowania szyfrów.',
        'I wasn’t really involved at the time the system was developed, so I can’t help you with that.': 'Nie brałam udziału w tworzeniu tego systemu, więc nie potrafię ci pomóc.',
        'Sorry, 1Hero. Wish I could be more help.': 'Przykro mi, 1Hero. Chciałabym bardziej pomóc.',
        'No, it’s okay. I’ll figure it out.': 'Nie szkodzi. Sam coś wymyślę.',
        'Busy, then?': 'Czyli masz teraz urwanie głowy?',
        'Yeah, you could say I’m on a case.': 'Można tak powiedzieć. Prowadzę śledztwo.',
    },
}

known = {
    json.loads(line)['id']
    for line in MERGED.read_text(encoding='utf-8').splitlines()
    if json.loads(line)['translation'].strip()
}
rows = []
missing = set()
counts = Counter()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    event_id = context.get('event_id')
    if context.get('source_kind') != 'map' or context.get('map_id') != 3 or event_id not in MAPS:
        continue
    if row['id'] in known:
        continue
    source = row['source_text'].strip()
    if not source or source.startswith('/') or source in {'…', '...', '..'}:
        continue
    translation = MAPS[event_id].get(source)
    if translation is None:
        missing.add((event_id, source))
        continue
    row['translation'] = translation
    rows.append(row)
    counts[event_id] += 1
if missing:
    raise SystemExit('Unmapped strings: ' + repr(sorted(missing)))
OUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} records: ' + ', '.join(f'event {event}={count}' for event, count in sorted(counts.items())))
