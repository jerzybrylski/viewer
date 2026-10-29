#!/usr/bin/env python3
"""Build Polish drafts for Map 51 follow-ups."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map51-followups-01.jsonl'
TRANSLATIONS = {
    "Well, 1Hero? What do you think?": "No i co, 1Hero? Co myślisz?",
    "You’ve got a nice place.": "Masz niezłe miejsce.",
    "It’s nice and private. And I want to keep it that way.": "Jest tu przyjemnie i prywatnie. I chcę, żeby tak zostało.",
    "Look, I can’t say I fully understand your situation, but private security isn’t my line of work.": "Słuchaj, nie mówię, że do końca rozumiem twoją sytuację, ale prywatna ochrona to nie moja działka.",
    "What’s wrong? A skinny fanboy too much for you to handle?": "Co jest? Chudy fanboy to dla ciebie za dużo?",
    "More like, not worth my time.": "Bardziej nie wart mojego czasu.",
    "You know, 1Hero. I think you should see my streaming room.": "Wiesz, 1Hero. Myślę, że powinieneś zobaczyć mój pokój do streamowania.",
    "Good luck, 1Hero. Come visit any time.": "Powodzenia, 1Hero. Wpadaj, kiedy chcesz.",
    "If you ever get tired of being a detective, I’ll pay you to mount me on cam.": "Jeśli znudzi ci się bycie detektywem, zapłacę ci za to, żebyś mnie przeleciał na kamerce.",
    "Live, to the world? I don’t think I’d want Heather seeing that.": "Na żywo, dla całego świata? Chyba nie chciałbym, żeby Heather to widziała.",
    "That’s too bad.": "Szkoda.",
    "Cool decor.": "Fajny wystrój.",
    "I’m glad you like it.": "Cieszę się, że ci się podoba.",
    "I didn’t expect I’d be here tonight.": "Nie spodziewałam się, że będę tu dziś wieczorem.",
    "Just how well do you two know each other?": "Jak dobrze się znacie?",
    "1Hero’s my bodyguard.": "1Hero to mój ochroniarz.",
    "I help her out from time to time.": "Pomagam jej od czasu do czasu.",
    "I’m so lucky to have a detective bodyguard.": "Mam szczęście, że mam detektywa jako ochroniarza.",
    "I would not have thought he’d have the time with how busy he’s been at work.": "Nie sądziłam, że znajdzie czas, skoro jest tak zapracowany.",
    "Do tell me! I’d love to hear all about it.": "Opowiadaj! Chętnie posłucham.",
    "The Wilkes mansion got broken into today.": "Dziś włamano się do rezydencji Wilkesów.",
    "No way! Who did it?": "Nie żartuj! Kto to zrobił?",
    "It was just a gang of thieves.": "To była tylko banda złodziei.",
    "Eclipse Guild thieves.": "Złodzieje z Gildii Eclipse.",
    "Eclipse Guild? Tell me more!": "Gildia Eclipse? Opowiedz więcej!",
    "We ran them out, but could not catch them. We don’t know if it was Guild activity.": "Przegoniliśmy ich, ale nie złapaliśmy. Nie wiemy, czy to była akcja Gildii.",
    "Huh? Yeah we do. It was that Duncan Heisenburg guy.": "Co? Jasne, że wiemy. To był ten Duncan Heisenburg.",
    "This is top secret stuff, Erica.": "To ściśle tajne, Erica.",
    "You can tell me.": "Możesz mi powiedzieć.",
    "No, I can’t… Sorry.": "Nie mogę… Przepraszam.",
    "How can you keep a secret from a girl you’ve been inside of?": "Jak możesz trzymać sekrety przed dziewczyną, w której byłeś?",
    "You two…?": "Wy dwoje…?",
    "Oh, yes. We’ve had some really fun times.": "Och, tak. Świetnie się bawiliśmy.",
    "I suppose I could have guessed.": "Mogłam się domyślić.",
    "Damn, Ella. You can’t keep a secret, can you?": "Cholera, Ella. Nie potrafisz dotrzymać tajemnicy, co?",
    "I’m so clumsy.": "Ale ze mnie niezdara.",
    "Keeping more secrets from me, 1Hero?": "Trzymasz przede mną więcej sekretów, 1Hero?",
    "Our relationship is professional… It’s just…": "Nasza relacja jest zawodowa… Po prostu…",
    "I like to get filled up from time to time. You can understand, right, Erica?": "Lubię być wypełniona od czasu do czasu. Rozumiesz, prawda, Erica?",
    "Damn, girl. You’re really forward, aren’t you?": "Cholera, dziewczyno. Jesteś naprawdę bezpośrednia, co?",
    "I know what I want.": "Wiem, czego chcę.",
    "I can respect that.": "Szanuję to.",
    "I’m guessing you two were planning to fuck tonight.": "Zgaduję, że planowaliście się dziś pieprzyć.",
    "Ella!": "Ella!",
    "Well, now you’re in my love dungeon.": "Cóż, teraz jesteś w moim lochu miłości.",
    "And what does that mean?": "I co to znaczy?",
    "It means we can play together.": "To znaczy, że możemy się razem pobawić.",
    "Not wasting any time, are you?": "Nie tracisz czasu, co?",
    "You better keep the cameras off.": "Lepiej wyłącz kamery.",
    "Cameras?": "Kamery?",
    "That’s how I make my money. I sell… content.": "Tak zarabiam. Sprzedaję… treści.",
    "Holy shit! That’s crazy!": "O cholera! To szalone!",
    "You must not be on Lustagram.": "Chyba nie masz Lustagrama.",
    "I don’t do that kind of stuff.": "Nie robię takich rzeczy.",
    "If you’re looking to learn, I can be your teacher.": "Jeśli chcesz się nauczyć, mogę być twoją nauczycielką.",
    "Erica’s not that type of lady.": "Erica nie jest taką damą.",
    "I could never do anything on camera. That’s too much.": "Nigdy nie mogłabym robić niczego przed kamerą. To za dużo.",
    "Wait right here. I have something to show you.": "Poczekaj tu. Mam ci coś do pokazania.",
    "Bodyguard?": "Ochroniarz?",
    "She’s famous on the internet.": "Jest sławna w internecie.",
    "She has stalkers?": "Ma stalkerów?",
    "At least one.": "Przynajmniej jednego.",
    "Sounds like you’re getting the better end of the deal.": "Wygląda na to, że to ty wychodzisz na tym lepiej.",
    "Taking a famous cam girl to pound town just to protect her from one measly stalker.": "Zabranie sławnej camgirl do łóżka tylko po to, by chronić ją przed jednym żałosnym stalkerem.",
    "Well… Famous on the internet.": "Cóż… Sławna w internecie.",
    "I can’t find it.": "Nie mogę tego znaleźć.",
    "What is it you’re looking for?": "Czego szukasz?",
    "Something very special to me. I wanted to share it with you.": "Coś dla mnie bardzo cennego. Chciałam się tym z tobą podzielić.",
    "Aww. That’s sweet. Can we help you look for it?": "Aww. To słodkie. Możemy pomóc ci szukać?",
    "I may have accidentally thrown it away.": "Chyba przypadkiem to wyrzuciłam.",
    "It’s a double-sided dildo.": "To dwustronne dildo.",
    "For two girls to fuck.": "Do pieprzenia się dwóch dziewczyn.",
    "Oh… I see.": "Och… Rozumiem.",
    "You wanted to share that… with me?": "Chciałaś się tym… podzielić ze mną?",
    "If I can find it. You want to fuck, right?": "Jeśli je znajdę. Chcesz się pieprzyć, prawda?",
    "Well… That was the plan… But I didn’t expect to be here.": "Cóż… Taki był plan… Ale nie spodziewałam się, że tu będę.",
    "1Hero, would you be a dear and go to the porn shop next door and grab a two-sider.": "1Hero, byłbyś kochany i skoczył do sex shopu obok po dwustronne dildo.",
    "Do we really need that?": "Naprawdę tego potrzebujemy?",
    "Of course! It’s my favorite toy to share with other girls.": "Oczywiście! To moja ulubiona zabawka do dzielenia się z innymi dziewczynami.",
    "Wait! What if I don’t want it?": "Czekaj! A jeśli nie chcę?",
    "Nonsense. You’ll love it.": "Bzdura. Pokochasz to.",
    "I’ll go see what I can find.": "Pójdę zobaczyć, co znajdę.",
    "1Hero!?": "1Hero!?",
    "What? I think it’s a good plan.": "Co? Myślę, że to dobry plan.",
    "Now you’re thinking with your dick.": "Teraz myślisz kutasem.",
    "Fine… I’ll try it.": "Dobra… Spróbuję.",
    "Don’t leave me alone for too long, 1Hero.": "Nie zostawiaj mnie samej na zbyt długo, 1Hero.",
    "You’re not alone. You have Ella to talk to.": "Nie jesteś sama. Masz Ellę do pogadania.",
    "I don’t know her.": "Nie znam jej.",
    "Sounds like that’s about to change.": "Wygląda na to, że zaraz się to zmieni.",
    "Go buy a double-sided dildo. I want to have some fun with Erica.": "Idź kupić dwustronne dildo. Chcę się zabawić z Ericą.",
    "It wasn’t easy, but I have a two sided dildo.": "Nie było łatwo, ale mam dwustronne dildo.",
    "Our hero!": "Nasz bohater!",
    "We’re going to have so much fun!": "Będziemy się świetnie bawić!",
    "Let’s go to the bedroom.": "Chodźmy do sypialni.",
    "You’re not recording in there, are you?": "Nie nagrywasz tam, prawda?",
    "Don’t be so paranoid. Everything is off.": "Nie bądź taką paranoiczką. Wszystko jest wyłączone.",
    "I better not end up on the internet. That place is full of creeps.": "Lepiej, żebym nie wylądowała w internecie. To miejsce jest pełne zboczeńców.",
    "They pay the bills, honey.": "Ale płacą rachunki, kochanie.",
    "You’re lucky, 1Hero.": "Masz szczęście, 1Hero.",
    "Don’t you think I know it?": "Myślisz, że tego nie wiem?",
    "Wow! You have a cool place.": "Wow! Masz fajne miejsce.",
    "I live with my mom for now. I did have a dorm room at Saint Dame University though…": "Na razie mieszkam z mamą. Miałam jednak akademik na Uniwersytecie Saint Dame…",
    "But not nearly as cool as this.": "Ale nawet w połowie nie tak fajny jak to.",
    "Come on. I’ll show you my streaming room.": "Chodź. Pokażę ci mój pokój do streamowania.",
    "Streaming room?": "Pokój do streamowania?",
    "Her bedroom.": "Jej sypialnię.",
    "Would you like to go to a party tonight?": "Chciałabyś pójść dziś na imprezę?",
    "What’s the special occasion?": "Jaka okazja?",
    "My news broadcast airs tonight… Chloe and Sister Judy want to watch it together.": "Dziś emitują mój materiał informacyjny… Chloe i siostra Judy chcą go razem obejrzeć.",
    "The nun!? Of course I want to go!": "Zakonnica!? Oczywiście, że chcę iść!",
    "Careful now. Don’t be too crude in front of Judy.": "Uważaj tylko. Nie bądź zbyt wulgarny przy Judy.",
    "You’ve fucked her ass! How careful do I really need to be?": "Zerżnąłeś ją w tyłek! Jak ostrożny niby mam być?",
    "Ella…": "Ella…",
    "What about Erica? Will she be there? Isn’t she your girlfriend?": "A co z Ericą? Będzie tam? Nie jest twoją dziewczyną?",
    "She’s at work, but I can see if she’d be available by dinner hour.": "Jest w pracy, ale mogę sprawdzić, czy będzie wolna na kolację.",
    "Bring her too! This will be so much fun!": "Przyprowadź ją też! Będzie super!",
    "Where’s the party?": "Gdzie ta impreza?",
    "I’ll text you the address later.": "Wyślę ci później adres."
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
        or context.get('map_id') != 51
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
    raise SystemExit('Unmapped Map 51 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 119:
    raise SystemExit(f'Expected exactly 119 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 51 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
