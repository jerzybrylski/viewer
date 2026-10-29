#!/usr/bin/env python3
"""Build Polish drafts for remaining short Common Event NPC responses."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-common-event-npc-barks-followups-01.jsonl'
EVENT_IDS = {17, 23, 27, *range(103, 122)}
TRANSLATIONS = {
    'Amulet K?': 'Amulet K?',
    'Likely referring to one of the amulets Lillian was talking about.': 'Pewnie chodzi o jeden z amuletów, o których mówiła Lillian.',
    'And Morgan Deluna?... A guild member?': 'A Morgan Deluna?... Członek gildii?',
    'Is this the person who Charles sold the artifact to?': 'Czy to tej osobie Charles sprzedał artefakt?',
    'He makes it sound like he’s buying it… Or stealing it.': 'Brzmi, jakby chciał go kupić… albo ukraść.',
    'I better not lose this phone. I might make more sense of the message later.': 'Lepiej nie zgubić tego telefonu. Może później uda mi się lepiej zrozumieć tę wiadomość.',
    'I need to find all four bags of junk before I box them up.': 'Muszę znaleźć wszystkie cztery worki rupieci, zanim je zapakuję.',
    'I can use the Antibiotic Cream to fix my leg!': 'Krem z antybiotykiem wyleczy mi nogę!',
    'Let’s see what the letter says…': 'Zobaczmy, co jest w liście…',
    'Holy shit. Madalyn did kill Zephaniah!': 'Cholera jasna. Madalyn naprawdę zabiła Zephaniaha!',
    'I need to show this to Father Solomon.': 'Muszę pokazać to ojcu Solomonowi.',
    "Looks like the creek near Carol's farm.": 'Wygląda na strumyk przy farmie Carol.',
    'Bring the chest to Tasha.': 'Zanieś skrzynię Tashy.',
    'Can you tell me what to do next?': 'Możesz mi powiedzieć, co mam dalej robić?',
    'How the hell would I know what you should do next? Give me something to work with.': 'Skąd, do cholery, mam wiedzieć, co masz teraz zrobić? Daj mi coś konkretnego.',
    'Oh… I thought you’d just know what to do.': 'Och… Myślałem, że po prostu będziesz wiedział, co robić.',
    'I’m not psychic.': 'Nie jestem jasnowidzem.',
    "You’ve finished this chapter! But don't worry, new content is never more than a couple weeks away.": 'Ukończyłeś ten rozdział! Ale bez obaw — nowe treści pojawią się już za kilka tygodni.',
    'You’ve finished this chapter, but you’ve missed some secrets. Don’t be afraid to talk to strangers.': 'Ukończyłeś ten rozdział, ale ominęło cię kilka sekretów. Nie bój się rozmawiać z nieznajomymi.',
    'There’s something in the ground, but I can’t get to it without a tool.': 'Pod ziemią coś jest, ale bez narzędzia się tam nie dostanę.',
    'Get a load of this.': 'Spójrz na to.',
    'Look what I have.': 'Patrz, co mam.',
    'I’ve got this.': 'Mam to.',
    'Will this work?': 'Czy to się nada?',
    'I can’t afford that.': 'Nie stać mnie na to.',
    'I don’t have enough money.': 'Nie mam wystarczająco dużo pieniędzy.',
    'This isn’t right.': 'To się nie zgadza.',
    'I can’t open it.': 'Nie mogę tego otworzyć.',
    'Leave it to me.': 'Zostaw to mnie.',
    'I can handle this.': 'Poradzę sobie.',
    'I could use one of these.': 'Przydałoby mi się coś takiego.',
    'Hello, there.': 'Witaj.',
    "Can't you see I'm busy?": 'Nie widzisz, że jestem zajęty?',
    "Leave! I'm busy.": 'Odejdź! Jestem zajęty.',
    'Get out of here. I have better things to do.': 'Wynoś się stąd. Mam ważniejsze sprawy na głowie.',
    "I'm preoccupied. Come back later.": 'Jestem zajęty. Wróć później.',
    "I'm unable to talk right now.": 'Nie mogę teraz rozmawiać.',
    'What is this supposed to do?': 'Do czego to ma służyć?',
    "I'm grateful for your efforts.": 'Jestem ci wdzięczny za pomoc.',
    "This won't end well.": 'To się źle skończy.',
    'I have a feeling this wont be good.': 'Mam przeczucie, że to nie wróży nic dobrego.',
    'Not now! I’ve got things to do.': 'Nie teraz! Mam coś do zrobienia.',
    'Get going now. I’m busy.': 'Ruszaj. Jestem zajęta.',
    'Come back in a bit. I’m busy right now.': 'Wróć za chwilę. Jestem teraz zajęta.',
    'Come back in a bit. I’m busy.': 'Wróć za chwilę. Jestem zajęta.',
    'Sorry, sugar. Can’t talk right now.': 'Przykro mi, kochanie. Nie mogę teraz rozmawiać.',
    'And just what is this for?': 'A do czego to właściwie służy?',
    'Come on now! You’re smarter than that.': 'No dalej! Stać cię na więcej.',
    'What in the hell is this?': 'Co to, do cholery, jest?',
    "Well, aren't you a kind gentleman?": 'No proszę, jaki z ciebie uprzejmy dżentelmen.',
    'Thanks a lot, sugar.': 'Wielkie dzięki, kochanie.',
    'Dad blast it!': 'Niech to szlag!',
    "What's new with ya?": 'Co tam nowego?',
    'Why, hello there sweet thing.': 'Witaj, przystojniaku.',
    'What in tarnations?': 'Co u licha?',
    'Oh, my goodness me.': 'O rety!',
    'Hiya!': 'Cześć!',
    'Salutations!': 'Witaj!',
    'Leave me alone!': 'Daj mi spokój!',
    'I’m busy right now. Go away!': 'Jestem teraz zajęta. Znikaj!',
    'Stop bothering me.': 'Przestań mi przeszkadzać.',
    'Uhh, what’s wrong with you?': 'Eee, co z tobą nie tak?',
    'Are you a total noob?': 'Jesteś kompletnym noobem?',
    'Did you read the walkthrough?': 'Czy czytałeś solucję?',
    'Thanks a ton!': 'Wielkie dzięki!',
    'Mmhmm?': 'Mhm?',
    'Hi!': 'Cześć!',
    'Cheers!': 'Dzięki!',
    'Sod off!': 'Spadaj!',
    'Thanks a bunch!': 'Wielkie dzięki!',
    'I really appreciate it.': 'Naprawdę to doceniam.',
    'That’s very kind.': 'To bardzo miłe.',
    'Smashing!': 'Świetnie!',
    'Bloody hell!': 'Cholera jasna!',
    'Alright mate?': 'W porządku, stary?',
    'Oh, greetings.': 'Och, witaj.',
    'I’m busy right now. Go away.': 'Jestem teraz zajęta. Odejdź.',
    'I can’t talk to you now.': 'Nie mogę teraz z tobą rozmawiać.',
    'What is this supposed to be for?': 'Do czego to ma służyć?',
    'What are you trying to do?': 'Co próbujesz zrobić?',
    'You’re really helpful.': 'Naprawdę mi pomagasz.',
    'Thanks a lot!': 'Dzięki wielkie!',
    'Blessed day.': 'Błogosławionego dnia.',
    'Got a lot to do. Go away.': 'Mam dużo do zrobienia. Idź sobie.',
    'I’ve got things going on. I can’t talk.': 'Mam teraz sporo na głowie. Nie mogę rozmawiać.',
    'I’m preoccupied. Come back later.': 'Jestem zajęta. Wróć później.',
    'What’s this supposed to do?': 'Do czego to ma służyć?',
    'Thanks! Appreciate it.': 'Dzięki! Doceniam to.',
    'Thank you for helping me out.': 'Dziękuję za pomoc.',
    'Good job. I owe you one.': 'Dobra robota. Jestem ci winna przysługę.',
    'Heaven be praised!': 'Niech będzie pochwalony Pan!',
    'I don’t feel good about this.': 'Nie podoba mi się to.',
    'Something tells me this isn’t good.': 'Mam przeczucie, że to nic dobrego.',
    'Don’t interrupt me when I’m busy.': 'Nie przerywaj, kiedy jestem zajęty.',
    'Who told you I was free to talk? Go away.': 'Kto ci powiedział, że mam czas na rozmowę? Wynoś się.',
    'Get out of here before I lose my shit.': 'Wynoś się stąd, zanim puszczą mi nerwy.',
    'Check back later. I’ve got a lot going on right now.': 'Wróć później. Mam teraz sporo na głowie.',
    'I’ve got stuff to do. Come back later.': 'Mam coś do zrobienia. Wróć później.',
    'Is this some kind of joke?': 'To jakiś żart?',
    'What the hell are you thinking?': 'Co ty, do cholery, sobie myślisz?',
    'You disappoint me.': 'Zawiodłeś mnie.',
    'Nice job.': 'Dobra robota.',
    'I’m not happy about this.': 'Nie podoba mi się to.',
    'Hello there, darling.': 'Witaj, kochanie.',
    'Hello, sweetheart.': 'Cześć, skarbie.',
    'Now is not a good time.': 'Teraz nie jest dobry moment.',
    'Come back later, darling.': 'Wróć później, kochanie.',
    'Sorry, dear, I’m busy.': 'Przykro mi, kochanie, jestem zajęta.',
    'That’s not going to work, darling.': 'To się nie uda, kochanie.',
    'Thank you, darling!': 'Dziękuję, kochanie!',
    'You’re the best, sweetheart!': 'Jesteś najlepszy, skarbie!',
    'Darn!': 'A niech to!',
    'I’m busy right now.': 'Jestem teraz zajęta.',
    'I have things to do. Go away.': 'Mam coś do zrobienia. Odejdź.',
    'Can’t you see now is not a good time?': 'Nie widzisz, że to nie jest dobry moment?',
    'I can’t talk right now. Come back later.': 'Nie mogę teraz rozmawiać. Wróć później.',
    'What am I supposed to do with that?': 'Co mam z tym zrobić?',
    'What are you thinking?': 'Co ty sobie myślisz?',
    'How is this going to help?': 'Jak to ma pomóc?',
    'I think you misread the clues.': 'Chyba źle odczytałeś wskazówki.',
    'I’m worried about this.': 'Martwię się tym.',
    'Hey there!': 'Cześć!',
    'I’m busy! Now get going.': 'Jestem zajęta! A teraz ruszaj.',
    'Bless yer heart.': 'Niech cię Bóg błogosławi.',
    'That’s very helpful.': 'To bardzo pomocne.',
    'Woohoo!': 'Hura!',
    'Dag nab it!': 'Do licha!',
    'Damn it all to hell!': 'Niech to wszystko szlag trafi!',
    'Oh, boy. This ain’t good.': 'O rany. To nie wróży nic dobrego.',
    'I’m busy! Go away.': 'Jestem zajęta! Odejdź.',
    'I don’t have time for you right now.': 'Nie mam teraz dla ciebie czasu.',
    'I have better things to do. Please leave.': 'Mam ważniejsze sprawy. Proszę, odejdź.',
    'I’ve no time for temptations, please go.': 'Nie mam czasu na pokusy. Proszę, idź sobie.',
    'Please come back another time.': 'Proszę, przyjdź innym razem.',
    'I am busy right now. Can you come back later?': 'Jestem teraz zajęty. Możesz wrócić później?',
    'What is this all about?': 'O co w tym wszystkim chodzi?',
    'Perhaps you should pray for guidance.': 'Może powinieneś pomodlić się o wskazówki.',
    'Blessed are those who serve.': 'Błogosławieni, którzy służą.',
    'Praise the Lord!': 'Chwała Panu!',
    'Rats!': 'Kurczę!',
    'Oh, pooey!': 'Ojejku!',
    'By the cross?!': 'Na krzyż?!',
    'Angels on high?!': 'O, anioły w niebie?!',
    'Oh, no. I’m worried.': 'O nie. Martwię się.',
    'I fear the worst.': 'Obawiam się najgorszego.',
    'Come, this way.': 'Chodź tędy.',
    'Get out of here! I’m busy.': 'Wynoś się! Jestem zajęta.',
    'I’ve got things going on. Go away.': 'Mam teraz coś na głowie. Idź sobie.',
    'Go away, unless you want your own cement shoes.': 'Znikaj, chyba że chcesz dostać betonowe buty.',
    'I’ve got a bad feeling here.': 'Mam złe przeczucia.',
    'I’m a busy woman. Leave!': 'Jestem zajęta. Zostaw mnie!',
    'Can’t talk right now. Busy.': 'Nie mogę teraz rozmawiać. Jestem zajęta.',
    'What the hell is this?': 'Co to, do cholery, jest?',
    'You’re a lifesaver.': 'Ratujesz mi życie.',
    "I don't know about this.": 'Sama nie wiem, czy to dobry pomysł.',
    "This doesn't look good.": 'To nie wygląda dobrze.',
    "This can't be good.": 'To nie wróży nic dobrego.',
    'I have things to do. Leave at once!': 'Mam coś do zrobienia. Odejdź natychmiast!',
    'Get out of my sight.': 'Znikaj mi z oczu.',
    'I’m preoccupied at the moment.': 'Jestem teraz zajęta.',
    'Why are you wasting my time?': 'Czemu marnujesz mój czas?',
    'Is that the best you can offer?': 'To najlepsze, co możesz zaoferować?',
    'You don’t know what you’re doing, do you?': 'Nie wiesz, co robisz, prawda?',
    'You’ve earned my gratitude.': 'Zasłużyłeś na moją wdzięczność.',
    'I thank you for what you’ve done.': 'Dziękuję za to, co zrobiłeś.',
    'I appreciate your assistance.': 'Doceniam twoją pomoc.',
    'I have my doubts about this.': 'Mam co do tego wątpliwości.',
    'You again?': 'Znowu ty?',
    "What's happenin'?": 'Co tam słychać?',
    'What are you thinking about?': 'O czym myślisz?',
    "What's on your mind?": 'Co ci chodzi po głowie?',
    'Just go away.': 'Po prostu idź sobie.',
    "Can't talk right now.": 'Nie mogę teraz rozmawiać.',
    "Not right now. I'm busy.": 'Nie teraz. Jestem zajęta.',
    "Now aren't you a nice guy.": 'No proszę, jaki z ciebie miły gość.',
    'Hey you.': 'Hej, ty.',
    'Does this work?': 'Czy to działa?',
    'Here it is.': 'Proszę, oto.',
    "I can't afford that.": 'Nie stać mnie na to.',
    "I don't have enough money.": 'Nie mam wystarczająco dużo pieniędzy.',
    "I don't think so.": 'Chyba nie.',
    "It won't work.": 'To nie zadziała.',
    "This isn't right.": 'To się nie zgadza.',
    "It's a clue!": 'To wskazówka!',
    "There's something here.": 'Coś tu jest.',
    'Get out of here. I’ve got things to do.': 'Wynoś się stąd. Mam coś do zrobienia.',
    'Will you please stop annoying me?': 'Czy możesz przestać mnie denerwować?',
    'Does it look like I have time to talk?': 'Czy wyglądam, jakbym miał czas na rozmowę?',
    'I’m preoccupied at the moment. Come back later.': 'Jestem teraz zajęty. Wróć później.',
    'I don’t have time for this.': 'Nie mam na to czasu.',
    'I’m too old for nonsense.': 'Jestem za stary na takie bzdury.',
    'Appreciate the help.': 'Doceniam pomoc.',
    'Thanks a lot, kid.': 'Dzięki, młody.',
    'Looks like it worked!': 'Wygląda na to, że się udało!',
    'Crap!': 'Cholera!',
    'God dammit!': 'Niech to szlag!',
    'Get out of here. I’m busy.': 'Wynoś się stąd. Jestem zajęty.',
    'Does it look like I’m free to talk? Go away.': 'Czy wyglądam, jakbym miał czas na rozmowę? Znikaj.',
    'Scram. I’m busy.': 'Spadaj. Jestem zajęty.',
    'Come back later. Now’s not a good time.': 'Wróć później. To nie jest dobry moment.',
    'Got things to do. Check back later.': 'Mam coś do zrobienia. Wróć później.',
    'What the hell? Are you dumb?': 'Co do cholery? Jesteś głupi?',
    'What’s this supposed to be for?': 'Do czego to ma służyć?',
    'Appreciate it.': 'Dzięki, doceniam to.',
    'My gut tells me this is bad.': 'Mam złe przeczucia.',
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
    event_id = context.get('event_id')
    if (
        row['id'] in known
        or row.get('category') != 'custom_dialogue'
        or context.get('source_kind') != 'common_event'
        or event_id not in EVENT_IDS
        or not source
        or source.lstrip().startswith('/')
        or not any(char.isalpha() for char in source)
    ):
        continue
    translation = TRANSLATIONS.get(source)
    if translation is None:
        unmapped.add((event_id, source))
        continue
    row['translation'] = translation
    rows.append(row)

if unmapped:
    raise SystemExit('Unmapped selected Common Event strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) < 200:
    raise SystemExit(f'Expected at least 200 records, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Common Event NPC responses across {len({r["context"]["event_id"] for r in rows})} events')
