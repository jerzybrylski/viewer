#!/usr/bin/env python3
"""Build Polish drafts for player-facing Judy, Arianna, and church dialogue on Map 12."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map12-arianna-followups-01.jsonl'
TRANSLATIONS = {
    '1Hero! You made it!': '1Hero! Udało ci się dotrzeć!',
    '1Hero! I thought you’d be home.': '1Hero! Myślałam, że będziesz w domu.',
    'So, we’re good? It’s all mine?': 'Czyli wszystko gra? To wszystko moje?',
    'Why did you leave Heather’s house? They are worried sick.': 'Czemu wyszłaś z domu Heather? Strasznie się o ciebie martwią.',
    'Oh, my. I didn’t mean to frighten them. I was just…': 'Och, nie chciałam ich przestraszyć. Po prostu…',
    'I wanted to see you.': 'Chciałam cię zobaczyć.',
    'You could have called me.': 'Mogłaś do mnie zadzwonić.',
    'I must admit… I was worried you’d be with Erica.': 'Muszę przyznać… martwiłam się, że będziesz z Ericą.',
    'Huh? You wanted to see if she was spending the night?': 'Co? Chciałaś sprawdzić, czy zostanie na noc?',
    'Oh, 1Hero. I feel awful. I should not have done this.': 'Och, 1Hero. Jest mi okropnie wstyd. Nie powinnam była tego robić.',
    'It’s okay, Sister. Let’s go inside and talk.': 'W porządku, siostro. Chodźmy do środka i porozmawiajmy.',
    'Come on. Let’s go inside!': 'Chodź. Wejdźmy do środka!',
    'Are you awake yet, 1Hero?': 'Już nie śpisz, 1Hero?',
    'Hannah?': 'Hannah?',
    'Sister Judy, you gave us quite a scare last night.': 'Siostro Judy, ale nas wczoraj przestraszyłaś.',
    'You’re wanting to spend the night with the stud. I totally get it.': 'Zachciało ci się nocki z przystojniakiem. Doskonale cię rozumiem.',
    'I don’t blame you, Sister Judy. I’m sure you two had fun last night.': 'Nie mam ci tego za złe, siostro Judy. Na pewno dobrze się bawiliście wczoraj w nocy.',
    '1Hero is a gentleman.': '1Hero to dżentelmen.',
    'Not too much fun! Hahaha': 'Tylko nie za dobrze! Hahaha',
    'Oh, Hannah.': 'Och, Hannah.',
    'Come on, Sister. We’re going to church!': 'Chodź, siostro. Idziemy do kościoła!',
    'You’re going to church with them, Hannah?': 'Idziesz z nimi do kościoła, Hannah?',
    'Hell yeah. It’s better than being home right now.': 'Jasne, że tak. Lepsze to niż siedzenie teraz w domu.',
    'Heather and Ma are having a grown-up talk.': 'Heather i mama rozmawiają o dorosłych sprawach.',
    'You’re welcome at the church, Hannah.': 'Możesz z nami iść do kościoła, Hannah.',
    'Let’s not play sports though.': 'Tylko bez żadnych sportów.',
    'How about we read the bible!': 'Może poczytamy Biblię!',
    'Awwwwwwww!!!': 'Awwwwwwww!!!',
    'Would you rather go back to the farm?': 'Wolisz wrócić na farmę?',
    'Leave it to me. I’ll find something fun to do.': 'Zostaw to mnie. Wymyślę coś fajnego.',
    'I better follow them.': 'Lepiej za nimi pójdę.',
    'Go on. I’ll meet up with you later.': 'Idźcie. Dołączę do was później.',
    'Looks like a blown fuse…': 'Wygląda na przepalony bezpiecznik…',
    'Where can I find a replacement?': 'Gdzie znajdę zapasowy?',
    'What would you know? I just so happen to have a spare fuse.': 'A ty co możesz wiedzieć? Akurat mam zapasowy bezpiecznik.',
    'Feels good to be home.': 'Dobrze być w domu.',
    'Uncertain.': 'Trudno powiedzieć.',
    'What’s going on? Why didn’t you tell me about how Earthly love works?': 'Co się dzieje? Czemu nie powiedziałeś mi, jak działa ziemska miłość?',
    'This feeling for you remains, and I don’t know what to do about it.': 'Wciąż coś do ciebie czuję i nie wiem, co z tym zrobić.',
    'You’re an angel. I kind of thought you would already know about this stuff.': 'Jesteś aniołem. Myślałem, że takie rzeczy już znasz.',
    'Arianna…': 'Arianno…',
    'Especially when you’ve been so helpful already.': 'Zwłaszcza że już tyle razy mi pomogłeś.',
    'The lust burned so fiercely within me that I lost control of my actions.': 'Pożądanie płonęło we mnie tak mocno, że straciłam panowanie nad sobą.',
    'The Empyrean can be a strict place. What I know is what has been permitted for me to know.': 'Empyreum potrafi być surowym miejscem. Wiem tylko tyle, na ile mi pozwolono.',
    'What if that were to happen again?': 'A jeśli znowu do tego dojdzie?',
    'Arianna, love is not a bad thing…': 'Arianno, miłość nie jest niczym złym…',
    'At any point, this feeling could take over.': 'W każdej chwili to uczucie może przejąć kontrolę.',
    'This constant longing is supposed to be good?': 'To ciągłe tęsknienie ma być czymś dobrym?',
    'I’m afraid of what might happen when it does.': 'Boję się, co się wtedy stanie.',
    'It can be. It really just means you care a lot.': 'Może być. Tak naprawdę oznacza, że bardzo ci zależy.',
    'I could always help you satisfy it when it comes up. You know I’m always willing.': 'Mogę pomóc ci je zaspokoić, kiedy wróci. Wiesz, że zawsze chętnie pomogę.',
    'With so much care comes a risk. If something happens to me, then you could end up feeling terrible…': 'Tak silne uczucie niesie ze sobą ryzyko. Gdyby coś mi się stało, mogłoby ci być bardzo ciężko…',
    'Of that, I have no doubt.': 'Tego jestem pewien.',
    'If, on the other hand, it works out, then it can be an amazing thing.': 'Z drugiej strony, jeśli wszystko się ułoży, może być wspaniale.',
    'It might help in the short term…': 'Na krótką metę może pomóc…',
    'How do we get it to… work out?': 'Jak sprawić, żeby… wszystko się ułożyło?',
    'Yet even then, what if I become more violent or wild?': 'Ale nawet wtedy… co, jeśli stanę się bardziej agresywna albo nieokiełznana?',
    'There’s no easy answer to that.': 'Nie ma na to łatwej odpowiedzi.',
    'I couldn’t forgive myself if I were to hurt you.': 'Nie mogłabym sobie wybaczyć, gdybym cię skrzywdziła.',
    'This is sounding complicated.': 'To zaczyna się robić skomplikowane.',
    'No, this is something I need to deal with.': 'Nie, muszę się z tym uporać.',
    'I’m starting to miss how simple the Empyrean was.': 'Zaczynam tęsknić za prostotą Empyreum.',
    'Maybe we should talk about it…': 'Może powinniśmy o tym porozmawiać…',
    'Talking about it will help…': 'Rozmowa o tym pomoże…',
    'But it should be with other demons. They’ll know what’s going on.': 'Ale powinnam porozmawiać o tym z innymi demonami. One będą wiedziały, co się dzieje.',
    'Do you have this feeling, too? For me, as I have for you?': 'Czy ty też coś do mnie czujesz, tak jak ja do ciebie?',
    'I do care for you, of course.': 'Oczywiście, że mi na tobie zależy.',
    'I need answers, 1Hero.': 'Potrzebuję odpowiedzi, 1Hero.',
    'You know that I have a lot of important women in my life…': 'Wiesz, że w moim życiu jest wiele ważnych kobiet…',
    'Hell is a dangerous place and demons aren’t exactly angels.': 'Piekło to niebezpieczne miejsce, a demony nie są aniołkami.',
    'And you are a demon, while I’m a human… Someday, I’ll pass away, and you’ll have to move on.': 'A ty jesteś demonem, a ja człowiekiem… Kiedyś umrę, a ty będziesz musiał żyć dalej.',
    'It’s time I came to terms with my fellow demonkind.': 'Pora, żebym pogodziła się z innymi demonami.',
    'This makes me sad.': 'To mnie smuci.',
    'I don’t want to see you become like them.': 'Nie chcę, żebyś stał się taki jak oni.',
    'We can enjoy it while it lasts, though.': 'Możemy się tym cieszyć, póki trwa.',
    'I have become a demon, but my heart is still that of an angel’s.': 'Stałam się demonem, ale w sercu wciąż jestem aniołem.',
    'Enjoy it how?': 'Jak cieszyć się tym, póki trwa?',
    'Let me come along. It couldn’t hurt to have backup, in case things get heated.': 'Pozwól mi pójść z tobą. Dodatkowa pomoc nie zaszkodzi, jeśli zrobi się gorąco.',
    'Well… a lot of sex, for starters.': 'Cóż… na początek dużo seksu.',
    'Your offer is appreciated, but I would like to do this alone.': 'Doceniam twoją propozycję, ale chciałabym zrobić to sama.',
    'After all, I’m immortal, so it can only get so bad.': 'W końcu jestem nieśmiertelna, więc nic strasznego mi się nie stanie.',
    'If you want to spend some time together, you know where to find me.': 'Jeśli zechcesz spędzić ze mną trochę czasu, wiesz, gdzie mnie znaleźć.',
    'Who knows what Hell could hold in store for you?': 'Kto wie, co czeka cię w Piekle?',
    'Thank you, 1Hero. And…': 'Dziękuję, 1Hero. I…',
    'Perhaps you are right. I’ll be careful, 1Hero.': 'Może masz rację. Będę ostrożna, 1Hero.',
    'I… I love you.': 'Ja… kocham cię.',
    'That’s all I ask, Arianna.': 'Tylko o to proszę, Arianno.',
    'I love you, too, Arianna.': 'Ja też cię kocham, Arianno.',
    'I’ll come back soon.': 'Wrócę niedługo.',
    'Goodbye, Arianna.': 'Żegnaj, Arianno.',
    'I really don’t like the idea of letting her go there alone.': 'Bardzo nie podoba mi się pomysł, żeby pozwolić jej iść tam samej.',
    'It couldn’t hurt if I took a look around Hell…': 'Nie zaszkodzi, jeśli rozejrzę się po Piekle…',
    'And if we happen to cross paths, then it’ll be a happy coincidence.': 'A jeśli przypadkiem na siebie wpadniemy, będzie to miły zbieg okoliczności.',
    'Arianna, we need your help.': 'Arianno, potrzebujemy twojej pomocy.',
    'What do you need help with, 1Hero?': 'W czym potrzebujesz pomocy, 1Hero?',
    'Destroying evidence.': 'Musimy zniszczyć dowody.',
    'Oh! Thank God. I’m so bored here.': 'Och! Dzięki Bogu. Strasznie się tu nudzę.',
    'That was easier than I thought.': 'Poszło łatwiej, niż myślałem.',
    'The evidence is somewhere we can’t get to.': 'Dowody są w miejscu, do którego nie możemy się dostać.',
    'This is where your ability to teleport comes in handy.': 'Tu przyda się twoja zdolność teleportacji.',
    'Where do I have to teleport to?': 'Dokąd mam się teleportować?',
    'It’s the commissioner’s office at the police station.': 'Do biura komisarza na komisariacie.',
    'That’s a problem, because I’ve never been there.': 'W tym problem, że nigdy tam nie byłam.',
    'I can only teleport to places I’ve been to before.': 'Mogę teleportować się tylko do miejsc, w których już byłam.',
    'What if… what if we snuck you into the room?': 'A gdyby… gdybyśmy przemycili cię do tego pokoju?',
    'If she could be snuck in, we wouldn’t need her to begin with; you could do it yourself.': 'Gdyby dało się ją tam przemycić, w ogóle nie musielibyśmy jej angażować — sam mógłbyś to zrobić.',
    'No, I mean with the Oracle.': 'Nie, chodzi mi o Wyrocznię.',
    'If we could get her in while she’s inside the Oracle…': 'Gdyby udało się ją tam wprowadzić, kiedy będzie w środku Wyroczni…',
    'Then no one will know.': 'Wtedy nikt się nie dowie.',
    'Arianna can come out of the Oracle when the coast is clear, and then call us.': 'Arianna wyjdzie z Wyroczni, gdy będzie bezpiecznie, a potem do nas zadzwoni.',
    'Sounds like an adventure! It’s so nice to be useful again.': 'Brzmi jak przygoda! Miło znów się przydać.',
    'So she goes inside the Oracle… But how do we get the Oracle in?': 'Czyli ona wejdzie do Wyroczni… Ale jak przemycimy Wyrocznię do środka?',
    'Easy. I’ll submit it as evidence to the officers and tell them it came from the Wilkes mansion.': 'Proste. Przekażę ją funkcjonariuszom jako dowód i powiem, że pochodzi z rezydencji Wilkesów.',
    'As long as I tell them it’s Guild evidence, they’ll leave it for the commissioner in his office.': 'Jeśli powiem, że to dowód powiązany z Gildią, zostawią ją w biurze komisarza.',
    'So I’ll wait until I’m inside, and then BAM!... I’ll come out of the Oracle.': 'Poczekam, aż znajdę się w środku, a potem BAM!... Wyskoczę z Wyroczni.',
    'Right. Then you just have to boot up the laptop, navigate to the E drive, go into the Guild folder...': 'Jasne. Potem włącz laptop, otwórz dysk E: i wejdź do folderu Gildii…',
    '...and delete the files on Diana without touching any of the other Guild evidence.': '…i usuń pliki dotyczące Diany, nie ruszając pozostałych dowodów Gildii.',
    'Great! I’ll boot up the folder and defeat the files that have cursed Diana.': 'Świetnie! Otworzę folder i pokonam pliki, które rzuciły klątwę na Dianę.',
    'Umm… At minimum, yes.': 'Eee… To absolutne minimum.',
    'Only the files on Diana. We don’t want to do anything to all the other Guild files. There’s a lot of important evidence in them.': 'Tylko pliki dotyczące Diany. Nie ruszajmy pozostałych plików Gildii. Jest w nich mnóstwo ważnych dowodów.',
    'Sounds easy!': 'Brzmi prosto!',
    'Now… What’s a laugh top?': 'A teraz… co to jest ten „laptop do śmiechu”?',
    'Maybe this plan won’t work.': 'Może ten plan się nie uda.',
    'Relax, it’ll be fine.': 'Spokojnie, wszystko będzie dobrze.',
    'We’ll talk her through it step by step… It’ll be like helping a passenger land a plane.': 'Przeprowadzimy ją przez to krok po kroku… To będzie jak instruowanie pasażera, jak wylądować samolotem.',
    'Does that typically go well?': 'Czy to zwykle dobrze się kończy?',
    'But how will you speak to me if I’ll be all alone?': 'Ale jak będziecie ze mną rozmawiać, jeśli zostanę sama?',
    'You’ll need this phone.': 'Będziesz potrzebować tego telefonu.',
    'Hmmm...': 'Hmm…',
    'Once you’re out of the Oracle, give us a call on this phone.': 'Gdy wyjdziesz z Wyroczni, zadzwoń do nas.',
    'Are we sure she knows how to use a phone?': 'Na pewno umie korzystać z telefonu?',
    'I just have to figure out the right combination and I’ll have this pocket Oracle doing our bidding in no time!': 'Wystarczy, że odgadnę właściwą kombinację, a ta kieszonkowa Wyrocznia w mig zacznie robić, co jej każemy!',
    'Here, I’ll program it so you can just hit one button to dial us…': 'Proszę. Zaprogramuję go tak, żebyś mogła zadzwonić do nas jednym przyciskiem…',
    'And done. Just hit this button and then you’ll get us.': 'Gotowe. Naciśnij ten przycisk, a połączysz się z nami.',
    'Teamwork!': 'Ale zgrany z nas zespół!',
    'I’ve never been one to pray, but maybe now’s a good time to start.': 'Nigdy nie byłem skłonny do modlitwy, ale chyba teraz warto zacząć.',
    'Couldn’t hurt!': 'Nie zaszkodzi!',
    'It’ll be fine.': 'Wszystko będzie dobrze.',
    'I won’t disappoint you.': 'Nie zawiodę cię.',
    'It’s go time.': 'Czas działać.',
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
        or context.get('map_id') != 12
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
    raise SystemExit('Unmapped Map 12 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 140:
    raise SystemExit(f'Expected exactly 140 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 12 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
