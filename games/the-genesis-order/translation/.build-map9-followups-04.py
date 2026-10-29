import json
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl')
EVENTS = {
    59: {
        "1Hero? What are you still doing here?": "1Hero? Co ty tu jeszcze robisz?",
        "Oh, uhh… The tractor needs fixed.": "Och, eee… Trzeba naprawić traktor.",
        "And you’re going to fix it?": "I ty go naprawisz?",
        "What are you two doing out here?": "Co wy tu robicie?",
        "It’s still early. I wanted to go see Hannah’s cave.": "Jest jeszcze wcześnie. Chciałem zobaczyć jaskinię Hannah.",
        "Cave?": "Jaskinię?",
        "I was messing around in the field and pried a rock away from the cliff side.": "Bawiłam się na polu i odsunęłam kamień od zbocza.",
        "I uncovered a cave.": "Odkryłam jaskinię.",
        "But it’s dark out.": "Ale jest ciemno.",
        "I’m not afraid.": "Nie boję się.",
        "Come on, 1Hero. You can come with us.": "Chodź, 1Hero. Możesz iść z nami.",
        "We’re going to have to go through the corn field to get around the tractor.": "Musimy przejść przez pole kukurydzy, żeby ominąć traktor.",
        "I thought you said we weren’t going to get muddy.": "Mówiłaś, że się nie ubrudzimy.",
        "Don’t be a baby.": "Nie bądź beksą.",
        "I’m wearing good shoes! I’m not going to get them muddy in the corn field.": "Mam na sobie dobre buty! Nie będę ich brudzić w polu kukurydzy.",
        "Well, unless we can get the tractor working, we have no choice. The path is blocked.": "Jeśli nie uruchomimy traktora, nie mamy wyboru. Droga jest zablokowana.",
        "The drive shaft just needs fixed. Can you do that?": "Trzeba tylko naprawić wał napędowy. Dasz radę?",
        "Did Mom take off that drive shaft?": "Mama zdjęła ten wał napędowy?",
        "Yeah. It’s in the barn.": "Tak. Jest w stodole.",
        "Maybe we should just go back inside. The weather’s not looking good.": "Może wróćmy do środka. Pogoda się pogarsza.",
        "Let’s go into the barn.": "Chodźmy do stodoły.",
    },
    78: {
        "1Hero, whatcha up to?": "1Hero, co porabiasz?",
        "I’m worried about that cave behind your field.": "Martwię się o tę jaskinię za twoim polem.",
        "You think it’s haunted?": "Myślisz, że jest nawiedzona?",
        "Huh? No!...": "Co? Nie!...",
        "There’s some bad people in there and a bad person is looking for them.": "W środku są źli ludzie i szuka ich jeszcze gorszy człowiek.",
        "What the hell are you saying?": "Co ty, do cholery, wygadujesz?",
        "It’s all top secret.": "To ściśle tajne.",
        "If you’re going into my cave, I’m coming with you.": "Jeśli idziesz do mojej jaskini, idę z tobą.",
        "You’re not allowed.": "Nie wolno ci.",
        "Like hell I ain’t! This is my property.": "A właśnie, że wolno! To moja ziemia.",
        "Fine. I just want to have a quick look.": "Dobra. Chcę tylko szybko rzucić okiem.",
        "I’ll race ya!": "Założę się z tobą na wyścig!",
        "Hey! Don’t go in there without me!": "Hej! Nie wchodź tam beze mnie!",
        "Thankfully Hannah is taking it easy.": "Na szczęście Hannah tym razem nie szaleje.",
        "I think I’ve had enough fun for one night.": "Chyba wystarczy mi wrażeń na jedną noc.",
    },
    8: {
        "Hannah sure is a rude girl.": "Hannah bywa naprawdę nieuprzejma.",
        "She’s got a wild side, that’s for sure.": "Na pewno ma dziką stronę.",
        "She believes you should wed another woman?": "Uważa, że powinieneś poślubić inną kobietę?",
        "I may have told her I had feelings for Chloe… But that was long ago.": "Mogłem jej powiedzieć, że coś czuję do Chloe… Ale to było dawno temu.",
        "If you have feelings for the girl, you should tell her.": "Jeśli coś do niej czujesz, powinieneś jej o tym powiedzieć.",
        "Don’t you want the Lord to bring you children?": "Czyż nie pragniesz, by Pan zesłał ci dzieci?",
        "Woah! Not so fast there, Arianna.": "Hej! Nie tak szybko, Arianno.",
        "What is it you’re waiting for?": "Na co więc czekasz?",
        "I’ve got things I need to do.": "Mam kilka spraw do załatwienia.",
        "Well, if you ever need my help, you know what to do.": "Jeśli będziesz potrzebował mojej pomocy, wiesz, co robić.",
        "Do you remember how to open your inventory?": "Pamiętasz, jak otworzyć ekwipunek?",
        "Yeah, I got it.": "Tak, wiem.",
        "Just look upon the Oracle of the Seraph and I will be there to guide you.": "Spójrz na Wyrocznię Serafina, a będę tam, by cię poprowadzić.",
        "Oh, shit! I better hurry up. I didn’t expect a storm to come through.": "O cholera! Lepiej się pospieszę. Nie spodziewałem się burzy.",
        "Did the girls run off? I hope they didn’t go far. I’m hungry…": "Dziewczyny uciekły? Mam nadzieję, że nie zaszły daleko. Zgłodniałem…",
        "Now, to find some spice for Carol.": "Teraz trzeba znaleźć trochę przypraw dla Carol.",
        "Sounds like Ella and Hannah are having some fun.": "Wygląda na to, że Ella i Hannah dobrze się bawią.",
        "Hey! Shoot him!": "Hej! Zastrzel go!",
    },
    4: {
        "I can’t face Carol right now. I don’t know what came over me.": "Nie mogę teraz spojrzeć Carol w oczy. Nie wiem, co we mnie wstąpiło.",
        "Hannah? What the hell? Let me in.": "Hannah? Co jest? Wpuść mnie.",
        "We’re busy. Come back later.": "Jesteśmy zajęte. Wróć później.",
        "Are you getting into trouble?": "Wpakowałaś się w kłopoty?",
        "I said, go away!": "Mówiłam, idź sobie!",
        "What the hell is that girl up to?": "Co ta dziewczyna wyprawia?",
        "Oh yeah! I have a key to the house…": "A tak! Mam klucz do domu…",
        "Let’s see what trouble she’s getting into.": "Zobaczmy, w co się wpakowała.",
        "I wonder if there is a way to unlock the door.": "Ciekawe, czy da się otworzyć te drzwi.",
    },
    43: {
        "That was the last hay bale.": "To była ostatnia bela siana.",
        "Now the hard part begins.": "Teraz zaczyna się ciężka robota.",
        "I’m going to bring this load to the cow farm down the way…": "Zawiozę ten ładunek na pobliską farmę krów…",
        "Hannah, be sure all the loose hay is cleaned up from the barn.": "Hannah, posprzątaj całe luźne siano w stodole.",
        "We’ll have it all cleaned up by the time you get back.": "Wszystko będzie posprzątane, zanim wrócisz.",
        "The sun is getting high in the sky. Better get moving.": "Słońce jest już wysoko. Lepiej ruszajmy.",
        "We can handle it.": "Dam sobie radę.",
        "Thanks, Chloe!": "Dzięki, Chloe!",
        "Come on, you two. It’s gonna be some hot work.": "No dalej, wy dwoje. Czeka nas gorąca robota.",
        "What do we have to do?": "Co mamy robić?",
        "We have to rake up the barn floor from all the loose hay.": "Musimy zgrabić całe luźne siano z podłogi stodoły.",
    },
}

known = set()
for line in MERGED.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    if row['translation'].strip():
        known.add(row['id'])
for line in (ROOT / 'drafts/custom-dialogue-map9-events-82-55-97-17-95-01.jsonl').read_text(encoding='utf-8').splitlines():
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
path = ROOT / 'drafts/custom-dialogue-map9-events-59-78-8-4-43-01.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote Map 9 follow-ups: {len(rows)} records across {len(EVENTS)} events')
