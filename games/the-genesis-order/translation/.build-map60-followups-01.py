#!/usr/bin/env python3
"""Build Polish drafts for Map 60 follow-ups."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map60-followups-01.jsonl'
TRANSLATIONS = {
    "What a coincidence. We were just talking about you.": "Co za zbieg okoliczności. Właśnie o tobie rozmawialiśmy.",
    "What were you doing at the warehouse, 1Hero?": "Co robiłeś w magazynie, 1Hero?",
    "Don’t listen to Bobby. He’s stirring up shit.": "Nie słuchaj Bobby'ego. Miesza.",
    "How many times do I have to pull you back on track? You have no business at the warehouse.": "Ile razy mam cię sprowadzać na właściwe tory? Nie masz czego szukać w magazynie.",
    "I’m making connections. In Jon’s line of business, he almost certainly comes across some shady characters.": "Nawiązuję kontakty. W branży Jona pewnie ciągle trafia się podejrzanych typów.",
    "Like you, 1Hero?": "Jak ty, 1Hero?",
    "Are you suggesting that I’m doing something illegal?": "Sugerujesz, że robię coś nielegalnego?",
    "Why can’t you kids get along?": "Czemu nie możecie się dogadać?",
    "1Hero needs to learn respect.": "1Hero musi nauczyć się szacunku.",
    "Bobby needs to learn how to not be an asshole.": "Bobby musi nauczyć się nie być dupkiem.",
    "As much as I would enjoy watching a pissing match between you two, I need to hit the showers.": "Choć chętnie obejrzałbym wasze przepychanki, muszę iść pod prysznic.",
    "Funny you should say that, because 1Hero here challenged me to a boxing match.": "Zabawne, że o tym mówisz, bo 1Hero wyzwał mnie na walkę bokserską.",
    "What!? No, I didn't!": "Co!? Nie, nie wyzwałem!",
    "Unsurprising.": "Nic dziwnego.",
    "I get it, 1Hero. You’re on your ass all day. You wouldn’t want to fight a real cop.": "Rozumiem, 1Hero. Cały dzień siedzisz na tyłku. Nie chciałbyś walczyć z prawdziwym gliną.",
    "I would whoop your skinny ass.": "Spiorę ci ten chudy tyłek.",
    "Take me in the ring. Let’s see how well a detective can handle a trained officer.": "Wejdź ze mną na ring. Zobaczmy, jak detektyw radzi sobie z wyszkolonym funkcjonariuszem.",
    "We’ve all been through training, Bobby.": "Wszyscy przeszliśmy szkolenie, Bobby.",
    "But some of us actually take it seriously.": "Ale niektórzy naprawdę traktują je poważnie.",
    "You’re on. We’ll see just how seriously you take your police training.": "Stoi. Zobaczymy, jak poważnie traktujesz szkolenie policyjne.",
    "You’re a cocky kid, 1Hero. But maybe you can prove to me that your physical abilities match your claimed mental abilities.": "Jesteś zarozumiałym dzieciakiem, 1Hero. Może udowodnisz, że twoja sprawność fizyczna dorównuje rzekomym zdolnościom umysłowym.",
    "Go get changed, 1Hero. Let’s do this before lunch. I’m starting to get hungry.": "Przebierz się, 1Hero. Zróbmy to przed obiadem. Zaczynam być głodny.",
    "This will be quick. Don’t you worry.": "To będzie szybkie. Nie martw się.",
    "I can’t go in there. The ladies would kill me.": "Nie mogę tam wejść. Babki by mnie zabiły.",
    "Are you sure about this, 1Hero?": "Na pewno tego chcesz, 1Hero?",
    "You’re a skinny twerp, Bobby. You don’t stand a chance.": "Jesteś chudym wymoczkiem, Bobby. Nie masz szans.",
    "You better focus, 1Hero.": "Lepiej się skup, 1Hero.",
    "Ring the bell, Melissa.": "Uderz w gong, Melissa.",
    "Ding, ding… Asshole.": "Ding, ding… Dupku.",
    "But, Miss Bhatt!": "Ale, panno Bhatt!",
    "You’re already late enough. It’s time to actually get something done for a change…": "I tak już jesteś spóźniony. Czas wreszcie zrobić coś pożytecznego…",
    "Get back to your cube.": "Wracaj do boksu.",
    "I’ll take you on, any time, any day, 1Hero.": "Mogę z tobą walczyć kiedykolwiek, gdziekolwiek, 1Hero.",
    "You won't be so lucky next time.": "Następnym razem nie będziesz miał tyle szczęścia.",
    "I suggest you take a shower, 1Hero. We don’t need you stinking up the office.": "Radzę ci wziąć prysznic, 1Hero. Nie chcemy, żebyś smrodził w biurze.",
    "I barely broke a sweat.": "Prawie się nie spociłem.",
    "Yeah. He only lasted a few seconds.": "Tak. Wytrzymał tylko kilka sekund.",
    "Don’t feel bad, 1Hero. I’m sure Melissa will go easy on you this afternoon after witnessing that beating.": "Nie przejmuj się, 1Hero. Jestem pewna, że Melissa odpuści ci dziś po południu po tym laniu.",
    "It was a lucky shot!": "To był szczęśliwy cios!",
    "Just looking to enjoy a morning workout.": "Chciałem po prostu zaliczyć poranny trening.",
    "Have you ever tried yoga, 1Hero?": "Próbowałeś kiedyś jogi, 1Hero?",
    "As a matter of fact, I have.": "Tak się składa, że tak.",
    "Seems like you’re more into boxing from what I’ve seen.": "Z tego, co widziałam, wolisz boks.",
    "I’m a man of many talents.": "Jestem człowiekiem wielu talentów.",
    "Why don’t you go change and join me for a yoga session?": "Czemu się nie przebierzesz i nie dołączysz do mnie na sesję jogi?",
    "I find it’s the perfect way to start the day.": "Uważam, że to idealny sposób na rozpoczęcie dnia.",
    "I’d be happy to, Miss Kimura.": "Z przyjemnością, panno Kimura.",
    "Are you ready, hot stuff?": "Gotowy, przystojniaku?",
    "It’s yoga. I can handle it.": "To tylko joga. Dam radę.",
    "Yoga is not about strength alone…": "Joga to nie tylko siła…",
    "You may be strong, but how flexible are you?": "Możesz być silny, ale jak bardzo jesteś gibki?",
    "Who’s dick did you have to suck to get this close to the Commissioner?": "Komu musiałeś obciągnąć, żeby zbliżyć się do komisarza?",
    "I need to get my workout in. How long is this going to take?": "Muszę zrobić trening. Jak długo to potrwa?",
    "Well, we’ve discovered some new connection to the old priest at Eve Cathedral.": "Odkryliśmy nowe powiązanie ze starym księdzem z katedry Eve.",
    "Okay. Tell me everything.": "Dobrze. Opowiedz mi wszystko.",
    "Uhhh… Okay.": "Yyy… Dobrze.",
    "What are you doing? Where’s Judy?": "Co robisz? Gdzie jest Judy?",
    "She’s in the ladies’ room... She’s been in there for a while.": "Jest w damskiej toalecie… Siedzi tam już chwilę.",
    "Is something wrong? Did you say something to her?": "Coś nie tak? Powiedziałeś jej coś?",
    "Despite her best efforts to strike up a conversation, I haven’t said a word to her.": "Mimo jej starań, by zacząć rozmowę, nie odezwałem się do niej ani słowem.",
    "Judy, are you okay?": "Judy, wszystko w porządku?",
    "Hmm, no answer.": "Hmm, brak odpowiedzi.",
    "Maybe she’s being shy…": "Może się wstydzi…",
    "She’s in there.": "Jest w środku.",
    "Then why isn’t she responding?": "Więc czemu nie odpowiada?",
    "Did she eat the tacos at Dick’s?": "Czy jadła tacos u Dicka?",
    "I need to find a way to get in and check on her.": "Muszę znaleźć sposób, by wejść i sprawdzić, co u niej.",
    "I’d normally complain. But as long as I’m here, I’m not filling out paperwork.": "Normalnie bym narzekał. Ale skoro tu jestem, nie muszę wypełniać papierów.",
    "It’s not too late if you want to pull out of the bet.": "Nie jest za późno, jeśli chcesz wycofać się z zakładu.",
    "Are you scared?": "Boisz się?",
    "Join me when you’re ready.": "Dołącz, gdy będziesz gotowy.",
    "Are you sure you want to do this? You might get hurt.": "Na pewno tego chcesz? Możesz oberwać.",
    "You’re the one who’s going to get hurt.": "To ty oberwiesz.",
    "Not fast enough, 1Hero?": "Za wolno, 1Hero?",
    "You cheated! You jumped the gun.": "Oszukiwałeś! Falstart!",
    "Get your ass up and get ready to defend yourself.": "Podnoś tyłek i szykuj się do obrony.",
    "Oh, now you’re going to get my full wrath.": "Och, teraz poznasz mój prawdziwy gniew.",
    "Bring it!": "Dawaj!",
    "I better be quick if I want to dodge her attacks. Whatever side she attacks from, I should move to the other.": "Muszę być szybki, żeby uniknąć jej ataków. Z której strony zaatakuje, powinienem ruszyć w przeciwną.",
    "Dammit, 1Hero! How are you so fast?": "Cholera, 1Hero! Jak możesz być taki szybki?",
    "Come on, Melissa… I’ll help you up.": "Chodź, Melissa… Pomogę ci wstać.",
    "Haha! I got you!": "Haha! Mam cię!",
    "Hey! No fair!": "Hej! To nie fair!",
    "A win is a win.": "Wygrana to wygrana.",
    "I won! This doesn’t count.": "Wygrałem! To się nie liczy.",
    "Be at my place tomorrow morning. I’ve quite a big mess for you to clean up.": "Bądź u mnie jutro rano. Mam spory bałagan do posprzątania.",
    "Hey! You didn’t win!": "Hej! Nie wygrałeś!",
    "Had enough, 1Hero?": "Masz dość, 1Hero?",
    "You got lucky. Let’s go again.": "Miałeś szczęście. Jeszcze raz.",
    "1Hero!?": "1Hero!?",
    "Diana!? What the hell?... How did you get in here?": "Diana!? Co do cholery?... Jak się tu dostałaś?",
    "Fuck… I must be getting slow.": "Cholera… Chyba zwalniam.",
    "You stole the commissioner's wallet… You’re staging a scene.": "Ukradłaś portfel komisarza… Robisz scenę.",
    "1Hero… You have to let me go. I’m not here to cause trouble.": "1Hero… Musisz mnie puścić. Nie przyszłam sprawiać kłopotów.",
    "Look… 1Hero… I copied his keycard…": "Słuchaj… 1Hero… Skopiowałam jego kartę dostępu…",
    "I need to get into his office to access Eclipse Guild files.": "Muszę dostać się do jego biura, żeby dostać pliki Gildii Eclipse.",
    "There’s a laptop with sensitive files on it…": "Jest tam laptop z wrażliwymi plikami…",
    "Unless I destroy them, the police will discover my residence in Cape Vedra.": "Jeśli ich nie zniszczę, policja odkryje moje miejsce pobytu w Cape Vedra.",
    "That would make my life difficult. I don’t want to have to go on the run.": "To by utrudniło mi życie. Nie chcę musieć uciekać.",
    "And I thought all this was behind us.": "A myślałem, że mamy to już za sobą.",
    "How about this? You give me the wallet, and I’ll take care of your problem myself.": "A może tak? Oddasz mi portfel, a ja sam zajmę się twoim problemem.",
    "I won’t destroy all the Guild files, but I’ll make sure all records of you are expunged.": "Nie zniszczę wszystkich plików Gildii, ale dopilnuję, by wszystkie zapisy o tobie zostały usunięte.",
    "You’d do that for me?": "Zrobiłbyś to dla mnie?",
    "I owe you for showing mercy to my dad. It’s the least I can do.": "Jestem ci winien za okazanie litości mojemu tacie. To najmniejsze, co mogę zrobić.",
    "Okay, I’ll trust you.": "Dobrze, zaufam ci.",
    "You’ll also need this to get in.": "Będziesz też tego potrzebować, żeby wejść.",
    "It’s a copy, so he’ll never know you have it.": "To kopia, więc nigdy się nie dowie, że ją masz.",
    "The files are on a laptop in his office. You’ll need to navigate to the E drive and find the EG directory. Everything is there.": "Pliki są na laptopie w jego biurze. Musisz przejść na dysk E: i znaleźć katalog EG. Wszystko tam jest.",
    "My information might be off somehow, so we’ll need to stay in contact in case something comes up.": "Moje informacje mogą być nieścisłe, więc musimy pozostać w kontakcie na wypadek, gdyby coś się pojawiło.",
    "Call me with that once you’re inside his office.": "Zadzwoń do mnie z tego, gdy będziesz w jego biurze.",
    "I hope so, detective. I’m really counting on you here.": "Mam nadzieję, detektywie. Bardzo na tobie polegam.",
    "Once you’ve used the card to get into the commissioner’s office at the police station, don’t forget to call me.": "Gdy użyjesz karty, by wejść do biura komisarza na komisariacie, nie zapomnij do mnie zadzwonić.",
    "1Hero? What happened?": "1Hero? Co się stało?",
    "The commissioner set a bunch of officers to guard his office while he’s away…": "Komisarz ustawił kilku funkcjonariuszy, by pilnowali jego biura podczas nieobecności…",
    "I think he suspects something is up.": "Chyba coś podejrzewa.",
    "Is there any way you can get by them?": "Czy jest sposób, by ich ominąć?",
    "Ha. Maybe if I could magically teleport inside…": "Ha. Może gdybym mógł magicznie teleportować się do środka…",
    "Wait, that’s it!": "Czekaj, to jest to!",
    "You’re going to teleport?": "Zamierzasz się teleportować?"
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
        or context.get('map_id') != 60
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
    raise SystemExit('Unmapped Map 60 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 119:
    raise SystemExit(f'Expected exactly 119 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 60 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
