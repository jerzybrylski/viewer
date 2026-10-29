#!/usr/bin/env python3
"""Build Polish drafts for additional Common Event NPC and house-visit dialogue."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-common-event-npc-barks-followups-02.jsonl'
EVENT_IDS = {123, 124, 126, 128, *range(143, 155), 242, 254}
TRANSLATIONS = {
    'You know I’m always here for you.': 'Wiesz, że zawsze możesz na mnie liczyć.',
    'Must you bother me right now?': 'Musisz mi teraz przeszkadzać?',
    'I can’t talk right now. Leave me alone.': 'Nie mogę teraz rozmawiać. Zostaw mnie w spokoju.',
    'Please come back to me later.': 'Proszę, wróć później.',
    'I’m sorry, but I’m a bit busy right now.': 'Przykro mi, ale jestem teraz trochę zajęta.',
    'I don’t understand what you’re doing.': 'Nie rozumiem, co robisz.',
    'You’re confusing me.': 'Mieszasz mi w głowie.',
    'Is this normal behavior for you?': 'Zawsze tak się zachowujesz?',
    'Fantastic job!': 'Świetna robota!',
    'Thank you so much!': 'Bardzo ci dziękuję!',
    'My sincere gratitude!': 'Jestem ci niezmiernie wdzięczna!',
    'Oh, phooey!': 'A niech to!',
    'God bless it!': 'Niech to szlag!',
    'My intuition tells me this is not good.': 'Przeczucie podpowiada mi, że to nic dobrego.',
    'Get stuffed! I don’t have time for you.': 'Spadaj! Nie mam dla ciebie czasu.',
    'Bugger off! I’m busy.': 'Odczep się! Jestem zajęty.',
    'You’re an annoying brat. Aren’t ya?': 'Ale z ciebie upierdliwy smarkacz, co?',
    'Got a lot going on. Come back a bit later.': 'Mam teraz sporo na głowie. Wróć później.',
    'Nice job. Dickhead.': 'Dobra robota, idioto.',
    'Way to waste my time.': 'Świetnie zmarnowałeś mój czas.',
    'You have no idea what you’re doing. Do ya?': 'Nie masz pojęcia, co robisz, co?',
    'Cheers, mate. You’ve done well.': 'Dzięki, stary. Dobra robota.',
    'You came through. Good on ya.': 'Spisałeś się. Tak trzymaj.',
    'Thanks a lot, mate.': 'Wielkie dzięki, stary.',
    'A job well done!': 'Dobra robota!',
    'Bugger me!': 'No nieźle!',
    'Bloody fuck!': 'Kurwa mać!',
    'Why do I have a feeling this won’t end well?': 'Czemu mam przeczucie, że to się źle skończy?',
    'Pleasure doing business with ya.': 'Miło robić z tobą interesy.',
    'I appreciate the business.': 'Doceniam naszą współpracę.',
    'Let’s see if you’ve got some treasure.': 'Zobaczmy, czy masz jakieś skarby.',
    'Let’s see what you got, mate.': 'Zobaczmy, co masz, stary.',
    'What’s this junk you’re showing me?': 'Co za rupiecie mi pokazujesz?',
    'What am I going to do with that trash?': 'Co mam zrobić z tymi śmieciami?',
    'Worthless garbage. Got something else?': 'Bezwartościowy złom. Masz coś jeszcze?',
    'Leave me!': 'Zostaw mnie!',
    'I’m busy at the moment.': 'Jestem teraz zajęta.',
    'What is this garbage?': 'Co to za śmieć?',
    'Are you insane?': 'Zwariowałeś?',
    'This is not a good situation.': 'To nie wygląda dobrze.',
    'I’m quite concerned.': 'Bardzo się niepokoję.',
    'Good to see you.': 'Miło cię widzieć.',
    'How are you doing?': 'Jak się masz?',
    "How's it going?": 'Co słychać?',
    'Oh! Hi.': 'O! Cześć.',
    'What would you like?': 'Czego sobie życzysz?',
    'Go away.': 'Idź sobie.',
    'Leave me alone.': 'Zostaw mnie w spokoju.',
    "Not right now. I'm busy..": 'Nie teraz. Jestem zajęta.',
    'Plase come back later.': 'Wróć później.',
    "Sorry. I can't talk right now.": 'Przepraszam. Nie mogę teraz rozmawiać.',
    "I don't think that's right.": 'Chyba coś się nie zgadza.',
    "I don't understand.": 'Nie rozumiem.',
    "I'm not sure what you mean.": 'Nie jestem pewna, co masz na myśli.',
    "What? I don't get it.": 'Co? Nie rozumiem.',
    "What? I'm confused.": 'Co? Pogubiłam się.',
    "You're so helpful.": 'Ale jesteś pomocny.',
    "You're too kind.": 'Jesteś zbyt miły.',
    "That's very kind of you.": 'To bardzo miłe z twojej strony.',
    'Hannah. Care to visit me at my place?': 'Hannah, wpadniesz do mnie?',
    'Need some tender love and care, 1Hero?': 'Potrzebujesz czułości i troski, 1Hero?',
    'I’d love to hang out.': 'Chętnie się z tobą spotkam.',
    'I’ll head on over.': 'Już do ciebie jadę.',
    'What a kick-ass house!': 'Ale odjazdowy dom!',
    'Nice place, 1Hero!': 'Ładne miejsce, 1Hero!',
    'You should see the bedroom.': 'Powinieneś zobaczyć sypialnię.',
    'Show me the way.': 'Prowadź.',
    'I ain’t going into the bedroom with you alone.': 'Nie pójdę z tobą sama do sypialni.',
    'You’re so damn horny, 1Hero.': 'Ależ ty jesteś napalony, 1Hero.',
    'This can’t be right. This house looks abandoned.': 'To niemożliwe. Ten dom wygląda na opuszczony.',
    'Want to come over to my place?': 'Chcesz wpaść do mnie?',
    'Looking to meet up, 1Hero?': 'Chcesz się spotkać, 1Hero?',
    'If you’ve got some free time, come on over.': 'Jeśli masz chwilę, wpadnij.',
    'Heading your way.': 'Już do ciebie jadę.',
    'I like your house, 1Hero.': 'Podoba mi się twój dom, 1Hero.',
    'Care to see the bedroom?': 'Chcesz zobaczyć sypialnię?',
    'Want to go to the bedroom?': 'Chcesz pójść do sypialni?',
    'Bedroom?... Uhh. I think I should go.': 'Sypialnia?... Eee, chyba już pójdę.',
    'Does someone live here?... This can’t be the right place.': 'Ktoś tu mieszka?... To chyba nie to miejsce.',
    'Chloe, do you want to hang out at my place?': 'Chloe, chcesz wpaść do mnie?',
    'Sure! I’ll head right over.': 'Jasne! Już do ciebie jadę.',
    'Wow! 1Hero sure has done a lot to his house.': 'Wow! 1Hero naprawdę sporo zrobił w swoim domu.',
    'Do you like what I’ve done to the place?': 'Podoba ci się, co zrobiłem z tym miejscem?',
    'You’ve done so much! And in such a short time!': 'Tyle tu zmieniłeś! I to w tak krótkim czasie!',
    'Sure… I’d like that.': 'Jasne… Chętnie.',
    'Oh, hey… I can’t stay long.': 'Och, cześć… Nie mogę zostać długo.',
    'It’s just… I should get back home.': 'Po prostu… Powinnam wracać do domu.',
    'What am I doing here?... Judy would be upset with me.': 'Co ja tu robię?... Judy byłaby na mnie zła.',
    'If you’re feeling lonely, how about coming over to my place?': 'Jeśli czujesz się samotna, może wpadniesz do mnie?',
    'Going to keep me company, 1Hero?': 'Dotrzymasz mi towarzystwa, 1Hero?',
    'Come on over.': 'Wpadaj.',
    'A low key house. I like it.': 'Skromny dom. Podoba mi się.',
    'Nice digs, 1Hero… even if a little… boring.': 'Niezła chata, 1Hero… choć trochę… nudna.',
    'The bedroom is a lot less boring.': 'Sypialnia jest znacznie ciekawsza.',
    'I’d like to see it.': 'Chętnie ją zobaczę.',
    'You invited me over just for that? I don’t think so.': 'Zaprosiłeś mnie tylko po to? Chyba nie.',
    'No way does a young man like 1Hero live here. I must be at the wrong place.': 'Niemożliwe, żeby taki młody facet jak 1Hero tu mieszkał. Chyba pomyliłam adres.',
    'Hi, Carol. I’d love to have your company right now.': 'Cześć, Carol. Chętnie spędziłbym teraz z tobą trochę czasu.',
    'Feeling lonely, 1Hero?': 'Samotny, 1Hero?',
    'It’s mighty lonely here.': 'Strasznie tu samotno.',
    'Well, we don’t want that, now do we? I’ll head on over.': 'Nie chcemy przecież, żeby tak było, prawda? Już jadę.',
    'What a lovely home. 1Hero is growing up so fast.': 'Jaki piękny dom. 1Hero tak szybko dorasta.',
    'You sure have an impressive little home.': 'Masz naprawdę imponujący domek.',
    'Thanks, Carol. You should see the bedroom.': 'Dzięki, Carol. Powinnaś zobaczyć sypialnię.',
    'Lead the way, hunky man.': 'Prowadź, przystojniaku.',
    'It’s lovely. But I can’t stay too long.': 'Jest uroczo. Ale nie mogę zostać zbyt długo.',
    "Is this the right place? It doesn't look very inviting.": 'Czy to na pewno tutaj? To miejsce nie wygląda zbyt zachęcająco.',
    'Care to come over and discuss something interesting?': 'Wpadniesz do mnie, żeby porozmawiać o czymś ciekawym?',
    'Why don’t you come over and find out.': 'Może wpadniesz i sam się przekonasz.',
    'I think I can make that happen.': 'Myślę, że da się to załatwić.',
    'You’ve got a nice pad, 1Hero.': 'Masz niezłą chatę, 1Hero.',
    'How about I show you the best room in the house.': 'Może pokażę ci najlepszy pokój w tym domu.',
    'What do ya think?': 'Co o tym myślisz?',
    'I’m taking a big risk being here… I have to go.': 'Wiele ryzykuję, będąc tutaj… Muszę już iść.',
    'This is a big risk. I have to get out of here.': 'To zbyt ryzykowne. Muszę się stąd wydostać.',
    'Hi, Lillian. If you’re feeling lonely, you’re welcome to stop by my place.': 'Cześć, Lillian. Jeśli czujesz się samotna, możesz do mnie wpaść.',
    'Perhaps you are the one feeling lonely.': 'Może to ty czujesz się samotny.',
    'I’d love to have your company.': 'Chętnie spędzę z tobą trochę czasu.',
    'I’ll stop by shortly.': 'Niedługo wpadnę.',
    'See you soon, Lillian.': 'Do zobaczenia, Lillian.',
    'I wasn’t expecting much. But this will do.': 'Nie spodziewałam się wiele, ale może być.',
    'A lovely home for a single man.': 'Uroczy dom jak na samotnego mężczyznę.',
    'How about we head to the bedroom? You’ll love it.': 'Może pójdziemy do sypialni? Spodoba ci się.',
    'Show it to me, 1Hero.': 'Pokaż mi ją, 1Hero.',
    'What do you think of my humble home?': 'Co sądzisz o moim skromnym domu?',
    'It’s… confined. I should head back home.': 'Jest… ciasno. Powinnam wracać do domu.',
    'This looks like a trap. I’m not going into that place.': 'To wygląda na pułapkę. Nie wejdę do środka.',
    'Why don’t you come over and we can discuss some cases?': 'Może wpadniesz do mnie i porozmawiamy o kilku sprawach?',
    'You drive me crazy, 1Hero… I’ll head over.': 'Doprowadzasz mnie do szaleństwa, 1Hero… Już jadę.',
    'He afforded this house on his salary?... Damn.': 'Stać go na taki dom z jego pensji?... Nieźle.',
    'Not a bad home, is it?': 'Całkiem niezły dom, prawda?',
    'Not sure how you afford all this…': 'Nie wiem, jak cię stać na to wszystko…',
    'I have my ways.': 'Mam swoje sposoby.',
    'Where shall we go?': 'Dokąd pójdziemy?',
    'How about the bedroom?': 'Może do sypialni?',
    'What do you want to talk about?': 'O czym chcesz porozmawiać?',
    'I was thinking about doing something more physical than talking.': 'Myślałem o czymś bardziej fizycznym niż rozmowa.',
    'Ugh… Have you no shame?': 'Ech… Nie masz za grosz wstydu?',
    'What am I doing here? This is ridiculous.': 'Co ja tu robię? To niedorzeczne.',
    'Hi, Heather. Would you like to visit me at my house?': 'Cześć, Heather. Wpadniesz do mnie?',
    'Sure, sweetheart! I’ll come over right away.': 'Jasne, kochanie! Już do ciebie jadę.',
    'I’m so proud of 1Hero for making such a lovely home.': 'Jestem taka dumna z 1Hero. Stworzył sobie taki piękny dom.',
    'Thanks for helping me buy my first home.': 'Dziękuję, że pomogłaś mi kupić mój pierwszy dom.',
    'I love what you’ve done! It’s so beautiful.': 'Uwielbiam to, co tu zrobiłeś! Jest tak pięknie.',
    'Not as beautiful as you.': 'Nie tak pięknie jak ty.',
    'Oh, 1Hero. Maybe we should go to the bedroom.': 'Och, 1Hero. Może powinniśmy pójść do sypialni.',
    'You have such a beautiful home. I’m glad I stopped by.': 'Masz taki piękny dom. Cieszę się, że wpadłam.',
    'Do you want to stay?': 'Chcesz zostać?',
    'Oh… I should really get home.': 'Och… Naprawdę powinnam już wracać do domu.',
    'I should really go back home. This feels wrong.': 'Naprawdę powinnam wracać do domu. To nie w porządku.',
    'Would you like to come visit my place, Judy?': 'Judy, chciałabyś wpaść do mnie?',
    'I’d love to visit you!': 'Chętnie cię odwiedzę!',
    'Come on over!': 'Wpadaj!',
    'I’ll be there soon.': 'Zaraz będę.',
    'What a wonderful home! It’s so pretty.': 'Cudowny dom! Jest taki ładny.',
    'It’s so big inside of here.': 'W środku jest tak dużo miejsca.',
    'There’s something else big I can show you in the bedroom.': 'W sypialni mogę ci pokazać coś jeszcze większego.',
    'Really!? I’d love to see it!': 'Naprawdę!? Chętnie to zobaczę!',
    'It’s nice, 1Hero. But I can’t stay long.': 'Ładnie tu, 1Hero. Ale nie mogę zostać długo.',
    'Is this the right place? I’m not so sure about this.': 'Czy to na pewno tutaj? Nie jestem tego taka pewna.',
    'Have any free time to visit your partner in crime?': 'Masz chwilę, żeby spotkać się ze swoją wspólniczką?',
    'You naughty boy. I’ll head over now.': 'Ty niegrzeczny chłopcze. Już jadę.',
    'This a pretty nice house for a detective.': 'Całkiem ładny dom jak na detektywa.',
    'What do you think of my place?': 'Co sądzisz o moim domu?',
    'Are you taking bribes?': 'Bierzesz łapówki?',
    'I make some money on the side.': 'Dorobię sobie na boku.',
    'Show me the bedroom.': 'Pokaż mi sypialnię.',
    'I’d thought we’d meet in the bedroom.': 'Myślałam, że spotkamy się w sypialni.',
    'I’m busy, 1Hero.': 'Jestem zajęta, 1Hero.',
    'Ugh. I can’t get seen here. What am I thinking?': 'Ech. Nie mogę pozwolić, żeby ktoś mnie tu zobaczył. Co ja sobie myślę?',
    'Care to visit my place? Perhaps we should meet up for a discussion.': 'Wpadniesz do mnie? Może powinniśmy spotkać się i porozmawiać.',
    'Perhaps a visit is in order. I’ll be there soon.': 'Chyba powinnam wpaść. Zaraz będę.',
    'Looks like someone’s skimming off the top.': 'Wygląda na to, że ktoś podbiera część pieniędzy.',
    'Trying to impress me?': 'Próbujesz mi zaimponować?',
    'Indeed.': 'Właśnie tak.',
    'Something physical.': 'Coś bardziej fizycznego.',
    '1Hero!... I’m busy.': '1Hero!... Jestem zajęta.',
    'I can’t get seen here. I need to leave.': 'Nie mogę pozwolić, żeby ktoś mnie tu zobaczył. Muszę iść.',
    'Congrats on the mansion. It’s good to see you’re putting all that hard-earned money to good use.': 'Gratuluję rezydencji. Dobrze widzieć, że dobrze wykorzystujesz ciężko zarobione pieniądze.',
    'Good job on the treasure hunt. Quite a nice haul.': 'Dobra robota podczas poszukiwań skarbów. Całkiem niezły łup.',
    'Any luck with finding that tomb?': 'Udało ci się znaleźć ten grobowiec?',
    'Congrats again, 1Hero.': 'Jeszcze raz gratuluję, 1Hero.',
    'By the way, I’m open for business, if you know what I mean.': 'A tak przy okazji, jestem otwarta na interesy, jeśli wiesz, co mam na myśli.',
    'Haha, I’ll keep that in mind, Jon.': 'Haha, będę o tym pamiętał, Jon.',
    'Be careful with that bomb. It could destroy a building.': 'Uważaj z tą bombą. Mogłaby zniszczyć cały budynek.',
    'Your timebomb will be ready today, but I need to focus right now.': 'Twoja bomba zegarowa będzie gotowa jeszcze dziś, ale teraz muszę się skupić.',
    'Bring me a detonator, then the bomb is yours.': 'Przynieś mi detonator, a bomba będzie twoja.',
    'Bring me three handguns from the bottom of the lake, along with a detonator; then the bomb and crossbow are yours.': 'Przynieś mi z dna jeziora trzy pistolety i detonator, a bomba oraz kusza będą twoje.',
    'Don’t worry, 1Hero. I’m not going to get you into trouble.': 'Nie martw się, 1Hero. Nie wpędzę cię w kłopoty.',
    'The best place to find treasure is in the woods. But you have to be very close to one to see it.': 'Najlepiej szukać skarbów w lesie. Musisz jednak podejść bardzo blisko, żeby je dostrzec.',
    'It looks like you’ve discovered a crafting scroll.': 'Wygląda na to, że znalazłeś zwój rzemieślniczy.',
    'A crafting scroll?': 'Zwój rzemieślniczy?',
    'It’s a secret recipe for creating new and useful items!': 'To tajny przepis na wytwarzanie nowych, przydatnych przedmiotów!',
    'Sounds interesting. But it’s gone now. I don’t know where it went.': 'Brzmi ciekawie. Ale już go nie ma. Nie wiem, dokąd zniknął.',
    'It went to Limbo!': 'Trafił do Limbo!',
    'Don’t worry, 1Hero. I can help you craft new items.': 'Nie martw się, 1Hero. Pomogę ci wytwarzać nowe przedmioty.',
    'Here, let me add something new to your inventory.': 'Proszę, dodam coś nowego do twojego ekwipunku.',
    'It sure will! Just select Angelcraft from your inventory to start crafting!': 'Na pewno się przyda! Wybierz „Angelcraft” z ekwipunku, żeby zacząć wytwarzać przedmioty!',
    'Sounds like this will come in handy.': 'Wygląda na to, że się przyda.',
    'Using Angelcrafting, I can magically bring into existence useful items for your quest!': 'Dzięki Angelcraft potrafię magicznie tworzyć przydatne przedmioty na twoją wyprawę!',
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
if len(rows) < 180:
    raise SystemExit(f'Expected at least 180 records, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Common Event lines across {len({r["context"]["event_id"] for r in rows})} events')
