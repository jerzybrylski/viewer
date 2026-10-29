#!/usr/bin/env python3
"""Build Polish drafts for player-facing Heather-family dialogue on Map 101."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map101-heather-sleepover-followups-01.jsonl'
TRANSLATIONS = {
    'What a beautiful bedroom… and so big.': 'Jaka piękna sypialnia… i jaka duża.',
    'Thanks, Mom.': 'Dzięki, mamo.',
    'I’ll get out of your way and let you three have a fun sleepover.': 'Nie będę wam przeszkadzać. Miłej nocki we trójkę.',
    'Oh, uhhh. I’m only staying for a little bit. I have work tomorrow.': 'Eee… Zostanę tylko chwilę. Jutro muszę pracować.',
    'You’re leaving, 1Hero?': 'Już wychodzisz, 1Hero?',
    'The night is young. I don’t have to leave any time soon.': 'Noc jest jeszcze młoda. Wcale nie muszę zaraz wychodzić.',
    'Tell us a story, 1Hero.': 'Opowiedz nam jakąś historię, 1Hero.',
    'Judy, he’s not a storyteller.': 'Judy, on nie jest gawędziarzem.',
    'I mean… About his detective work. I’m sure you have many interesting stories.': 'Chodzi mi… o jego pracę detektywa. Na pewno masz wiele ciekawych historii.',
    'Oh, uhhh. Yeah, I sure do.': 'Eee… No jasne, że mam.',
    'Huh? Like what?': 'Co? Na przykład jakie?',
    'Well, thanks.': 'No cóż, dzięki.',
    'No! I mean… I just want you to tell Judy the stories.': 'Nie! Chodzi mi o to… że chciałabym, żebyś opowiedział Judy te historie.',
    'Did I ever tell you about my first case?': 'Opowiadałem ci kiedyś o mojej pierwszej sprawie?',
    'I was tagging along with some officers, investigating an abandoned house…': 'Towarzyszyłem kilku funkcjonariuszom podczas przeszukania opuszczonego domu…',
    'Sounds scary.': 'Brzmi strasznie.',
    'I wasn’t afraid.': 'Nie bałem się.',
    '1Hero sure is brave.': '1Hero jest naprawdę odważny.',
    'I mean, it was supposed to be empty, and I was just scoping the scene with the senior detective.': 'To miał być pusty dom. Oglądałem miejsce zdarzenia razem z doświadczonym detektywem.',
    'But it wasn’t empty!?': 'Ale wcale nie był pusty!?',
    'All of the sudden, a dude jumped out from a closet and tackled my partner.': 'Nagle z szafy wyskoczył jakiś facet i powalił mojego partnera.',
    'Wait. That’s not the whole story.': 'Zaraz. To nie cała historia.',
    'Close enough.': 'Mniej więcej.',
    '1Hero wasn’t supposed to go into the house until the officers looked first.': '1Hero nie powinien był wchodzić do domu, zanim funkcjonariusze go nie przeszukają.',
    'We were looking at the same time.': 'Przeszukiwaliśmy go jednocześnie.',
    'What happened? Were you okay?': 'Co się stało? Nic ci się nie stało?',
    'I jumped on the guy and wrestled him off.': 'Rzuciłem się na niego i odciągnąłem go od partnera.',
    'The officers shot at us! Can you believe that?': 'Funkcjonariusze do nas strzelali! Możesz w to uwierzyć?',
    'How dangerous!': 'Ale niebezpiecznie!',
    'You were very lucky.': 'Miałeś mnóstwo szczęścia.',
    'Turns out it was just a homeless guy.': 'Okazało się, że to był tylko bezdomny.',
    'Did you get shot? Did the other man get shot?': 'Postrzelili cię? A tamtego mężczyznę?',
    'He missed.': 'Nie trafił.',
    'Tell me another one!': 'Opowiedz kolejną!',
    'Most of them are boring.': 'Większość z nich jest nudna.',
    'I just mean not every day is life and death. Right, 1Hero?': 'Chodzi mi tylko o to, że nie każdego dnia walczy się o życie. Prawda, 1Hero?',
    'Did you hear about the time someone tried to rob the station?': 'Słyszałaś o tym, jak ktoś próbował obrabować komisariat?',
    'You never told me that one.': 'O tym mi nie opowiadałeś.',
    'Oh! And the time my partner thought he saw a ghost and peed his pants.': 'A! I jeszcze ta historia, kiedy mój partner myślał, że zobaczył ducha, i ze strachu popuścił w spodnie.',
    'Wait… I have a few good tales.': 'Zaraz… Mam kilka dobrych historii.',
    '…and that’s why the dog threw up a human eyeball.': '…i dlatego pies zwymiotował ludzkim okiem.',
    'Oh my goodness, gracious me!...': 'O rany!...',
    'Tell me another!': 'Opowiedz jeszcze jedną!',
    'Sister Judy! You really want to hear another?': 'Siostro Judy! Naprawdę chce siostra usłyszeć kolejną?',
    'It’s just so exciting.': 'To takie ekscytujące.',
    'I think I’m going to go to bed.': 'Chyba pójdę już spać.',
    'But… It’s so early.': 'Ale… jest jeszcze tak wcześnie.',
    'It’s past midnight!': 'Jest już po północy!',
    'I’m sorry. I’m just so excited.': 'Przepraszam. Po prostu bardzo się podekscytowałam.',
    'It’s okay, Chloe. You can hit the hay. I’ll keep Sister Judy company.': 'Nic nie szkodzi, Chloe. Idź już spać. Dotrzymam siostrze Judy towarzystwa.',
    'Thank you, Chloe. And thank you, 1Hero.': 'Dziękuję, Chloe. I dziękuję tobie, 1Hero.',
    'Of course, Sister Judy. You mean the world to me…': 'Oczywiście, siostro Judy. Jesteś dla mnie całym światem…',
    'And I’ll help you clean up your bedroom tomorrow.': 'A jutro pomogę ci posprzątać sypialnię.',
    'Good night, Chloe.': 'Dobranoc, Chloe.',
    'If you need a bathroom, it is the door over there.': 'Łazienka jest za tamtymi drzwiami, gdybyś jej potrzebowała.',
    'Tell me more!': 'Opowiedz mi więcej!',
    'How about we just relax and try and get you tired?': 'Może po prostu się odprężymy i spróbujemy cię zmęczyć?',
    'You’re right. I should not stay up late. I need to get back to the church tomorrow.': 'Masz rację. Nie powinnam siedzieć do późna. Jutro muszę wrócić do kościoła.',
    'Stay here, 1Hero. I need to change.': 'Zostań tu, 1Hero. Muszę się przebrać.',
    'Just how far should I go to relax her?...': 'Ciekawe, jak daleko się posunąć, żeby ją odprężyć?...',
    'I mean… this is Heather’s bedroom after all.': 'W końcu to sypialnia Heather.',
    'It’s time to relax, 1Hero!': 'Czas się odprężyć, 1Hero!',
    'Fluffy is wiped. He had quite the adventure today.': 'Fluffy jest wykończony. Dziś miał mnóstwo przygód.',
    'I feel tired, 1Hero.': 'Jestem zmęczona, 1Hero.',
    'About time.': 'Najwyższy czas.',
    'It has been quite a day…': 'To był naprawdę długi dzień…',
    'I don’t know what I would do without you in my life.': 'Nie wiem, co bym bez ciebie zrobiła.',
    'You’re a sweet woman, Sister Judy.': 'Jesteś naprawdę kochana, siostro Judy.',
    'Do you think… you can do that again?': 'Myślisz, że… możesz zrobić to jeszcze raz?',
    'Of course. I very much enjoy helping you with these feelings you have.': 'Oczywiście. Bardzo lubię pomagać ci uporać się z tymi uczuciami.',
    'It is quite fun… Isn’t it?': 'To całkiem przyjemne… prawda?',
    'It’s important. Otherwise you’ll go crazy thinking about sex.': 'To ważne. Inaczej oszalejesz od ciągłego myślenia o seksie.',
    'You are a wise man for someone so young.': 'Jak na tak młodego mężczyznę, jesteś bardzo mądry.',
    'I’ve had a lot of experience.': 'Mam spore doświadczenie.',
    'I would love to spend some more time with you… alone.': 'Chętnie spędzę z tobą jeszcze trochę czasu… tylko we dwoje.',
    'Yeah, I’d like that.': 'Tak, chętnie.',
    'Please keep in touch.': 'Nie zapomnij się odezwać.',
    'It’s my pleasure.': 'Cała przyjemność po mojej stronie.',
    'Heather is going to smell it in the sheets…': 'Heather wyczuje to w pościeli…',
    'Maybe I should say something before she starts teasing me again.': 'Może powinienem coś powiedzieć, zanim znów zacznie się ze mnie nabijać.',
    'Are you still not sleeping?': 'Wciąż nie śpisz?',
    'I thought you were leaving, 1Hero.': 'Myślałam, że wychodzisz, 1Hero.',
    "I won't keep you awake.": 'Nie będę cię zatrzymywał.',
    'I’ll never complain about a visit from you.': 'Nigdy nie będę narzekać, gdy mnie odwiedzisz.',
    'It was nice meeting Sister Judy.': 'Miło było poznać siostrę Judy.',
    'You better be careful pulling ladies heartstrings, 1Hero. You’re quite charismatic.': 'Uważaj, żeby nie łamać kobietom serc, 1Hero. Masz w sobie sporo uroku.',
    'Did you have a good time tonight with Sister Judy?': 'Dobrze się bawiłeś dziś wieczorem z siostrą Judy?',
    'It was… eventful.': 'To był… intensywny wieczór.',
    'I lost the key to the safe. I really wish I had been more careful with it.': 'Zgubiłam klucz do sejfu. Szkoda, że nie byłam z nim ostrożniejsza.',
    'I found a key. It was under a boulder in your yard.': 'Znalazłem klucz. Leżał pod głazem w twoim ogródku.',
    'I’ll find it for you.': 'Znajdę go dla ciebie.',
    'Really? How did it get under a boulder?': 'Naprawdę? Jakim cudem znalazł się pod głazem?',
    'Is it the right one?': 'To ten właściwy?',
    'Oh, 1Hero. I didn’t hear you come in.': 'Och, 1Hero. Nie słyszałam, jak wchodziłeś.',
    'Let me try it…': 'Zaraz spróbuję…',
    'What are you doing, Heather?': 'Co robisz, Heather?',
    'I was just trying to open this safe. I lost the key weeks ago and I’ve yet to find it.': 'Próbowałam otworzyć sejf. Zgubiłam klucz kilka tygodni temu i wciąż go nie znalazłam.',
    'It’s fine. It’s just… I have some valuable things in here, and it’s driving me crazy that I lost that key.': 'Nic takiego. Po prostu… trzymam tu kilka cennych rzeczy i doprowadza mnie do szału, że zgubiłam klucz.',
    'I can help you find it.': 'Mogę pomóc ci go znaleźć.',
    'Will you do that for me?': 'Zrobisz to dla mnie?',
    'What’s in there?': 'Co tam jest?',
    'Want to take a look at some old photos?': 'Chcesz obejrzeć kilka starych zdjęć?',
    'Those are your family photos?': 'To zdjęcia twojej rodziny?',
    'I keep everything backed up on a thumb drive. These memories are important to me.': 'Mam kopię wszystkiego na pendrivie. Te wspomnienia są dla mnie ważne.',
    'Sure, Heather. I’d love to look at them with you.': 'Jasne, Heather. Chętnie je z tobą obejrzę.',
    'Great! Let’s go down to the big TV.': 'Świetnie! Chodźmy na dół, do dużego telewizora.',
    'You’re up early.': 'Wcześnie wstałeś.',
    'Are you going to stay for dinner?': 'Zostaniesz na kolacji?',
    'I’m going to church, believe it or not.': 'Idę do kościoła, uwierzysz?',
    'I appreciate the invite, but I should keep an eye on Ella.': 'Dzięki za zaproszenie, ale powinienem mieć oko na Ellę.',
    'Going to hang out with Sister Judy.': 'Idę spotkać się z siostrą Judy.',
    'She’ll be there.': 'Ona tam będzie.',
    'Looks like a diet book. Heather sure does read a lot about diet and exercise.': 'Wygląda na książkę o diecie. Heather naprawdę sporo czyta o odżywianiu i ćwiczeniach.',
    'I hope Sister Judy is okay at your place.': 'Mam nadzieję, że siostra Judy dobrze się u ciebie czuje.',
    'I hope you didn’t get too wet out there.': 'Mam nadzieję, że nie przemokłeś za bardzo.',
    'Get off the bed, Fluffy!': 'Złaź z łóżka, Fluffy!',
    '1Hero, catch him!': '1Hero, złap go!',
    'I’ll get him!': 'Już go łapię!',
    'Is this an aromatherapy machine?... It smells like spearmint.': 'To jakiś dyfuzor do aromaterapii?... Pachnie miętą zieloną.',
    'Huh… I think he just wanted to sleep on the bed.': 'Hm… Chyba po prostu chciał spać na łóżku.',
    'He looks so peaceful.': 'Wygląda na takiego spokojnego.',
    'Thank God… That thing has way too much energy.': 'Dzięki Bogu… Ten kot ma zdecydowanie za dużo energii.',
    'Chloe, are you wearing my panties?': 'Chloe, masz na sobie moje majtki?',
    'Dirty panties.': 'Brudne majtki.',
    'Hahaha!': 'Hahaha!',
    'Mom! Don’t laugh.': 'Mamo! Nie śmiej się.',
    'Is there cum on them?': 'Są na nich ślady spermy?',
    'Mine and hers.': 'Moje i jej.',
    '1Hero, can’t you keep a secret!?': '1Hero, nie umiesz dochować tajemnicy!?',
    'Seems you two had quite an adventure.': 'Wygląda na to, że przeżyliście niezłą przygodę.',
    'That cat is crazy. It wanted to be in your bedroom.': 'Ten kot jest szalony. Chciał wejść do twojej sypialni.',
    "I’m sorry, Mom. I won't let him in your room again.": 'Przepraszam, mamo. Nie wpuszczę go już do twojego pokoju.',
    'Let’s not be so hasty. I think Fluffy likes the bed.': 'Nie bądźmy takie pochopne. Chyba Fluffy lubi to łóżko.',
    'Stealing my man and my cat?': 'Odbijasz mi i faceta, i kota?',
    'Seems Fluffy is having an effect on her.': 'Wygląda na to, że Fluffy ma na nią wpływ.',
    'I have to admit, it would be nice to have something to take care of again.': 'Muszę przyznać, że miło byłoby znów mieć kim się opiekować.',
    'You still have me.': 'Przecież wciąż masz mnie.',
    'You’re all grown up, Chloe. You don’t need me anymore.': 'Jesteś już dorosła, Chloe. Nie potrzebujesz mnie.',
    'Don’t be sure about that.': 'Nie byłabym tego taka pewna.',
    'Carol!': 'Carol!',
    'Carol? How do you know it’s her?': 'Carol? Skąd wiesz, że to ona?',
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
        or context.get('map_id') != 101
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
    raise SystemExit('Unmapped Map 101 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 142:
    raise SystemExit(f'Expected exactly 142 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 101 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
