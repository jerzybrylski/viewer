#!/usr/bin/env python3
"""Build Polish drafts for player-facing church dialogue on Map 6."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map6-church-followups-02.jsonl'
TRANSLATIONS = {
    'Dammit! I’m too late.': 'Cholera! Spóźniłem się.',
    'Father Solomon. There you are.': 'Ojcze Solomonie. Tu jesteś.',
    'Waiting for me?': 'Czekałeś na mnie?',
    'Tell me about it. I’ve got to fix the roof, and fast.': 'Nie mów. Muszę szybko naprawić dach.',
    'That’s not what I’m talking about.': 'Nie o tym mówię.',
    'Come on, 1Hero. Let’s go inside.': 'Chodź, 1Hero. Wejdźmy do środka.',
    'It’s strange, but I found her clothes on the floor.': 'To dziwne, ale znalazłem jej ubrania na podłodze.',
    'You went into her bedroom?': 'Byłeś w jej sypialni?',
    'No… They were in the chapel.': 'Nie… Były w kaplicy.',
    'Why would Sister Judy leave her clothes on the chapel floor?': 'Dlaczego siostra Judy zostawiłaby ubrania na podłodze kaplicy?',
    'That’s what I’m wondering.': 'Właśnie się nad tym zastanawiam.',
    'No sign of her inside.': 'Nie ma jej w środku.',
    'I think she changed into something else…': 'Chyba przebrała się w coś innego…',
    'Perhaps she’s going into town.': 'Może poszła do miasta.',
    'That’s not like her. She hasn’t been into town on her own.': 'To do niej niepodobne. Nie chodziła sama do miasta.',
    'I’ve gone with her a few times, but this is all very strange.': 'Byłem z nią kilka razy, ale to wszystko jest bardzo dziwne.',
    'Could she have gone for a walk in the woods?': 'Może poszła na spacer do lasu?',
    'Sometimes Judy and I go for hikes. But she doesn’t change her clothes when we do.': 'Czasami chodzimy z Judy na piesze wycieczki. Ale wtedy się nie przebiera.',
    'I think that’s the next place we should check.': 'Myślę, że to kolejne miejsce, które powinniśmy sprawdzić.',
    'What gives? The commissioner promised me someone would watch the church.': 'Co jest? Komisarz obiecał, że ktoś będzie pilnował kościoła.',
    'I don’t know what to tell you, but she wants me at the Wilkes mansion.': 'Nie wiem, co ci powiedzieć, ale chce mnie w rezydencji Wilkesów.',
    'Isn’t there anyone in your unit that can take your place?': 'Czy w twoim wydziale nie ma nikogo, kto mógłby cię zastąpić?',
    'Sure. On Monday.': 'Jasne. W poniedziałek.',
    'Dammit, Bobby.': 'Cholera, Bobby.',
    'Out of my way. I’m running late.': 'Zejdź mi z drogi. Spóźniam się.',
    'I’m happy to see Sister Judy has company, but I wish you all wouldn’t destroy the church.': 'Cieszę się, że siostra Judy ma towarzystwo, ale wolałbym, żebyście nie niszczyli kościoła.',
    'Sorry about that, Father. I’ll fix it right up.': 'Przepraszam, ojcze. Zaraz to naprawię.',
    'Father, I’ve got some glass to replace your window.': 'Ojcze, mam szybę na wymianę do okna.',
    'You’re a great problem solver.': 'Świetnie rozwiązujesz problemy.',
    'I knew you’d find a way to fix it.': 'Wiedziałem, że znajdziesz sposób, żeby to naprawić.',
    'Come on, 1Hero. I’ll help you install it.': 'Chodź, 1Hero. Pomogę ci to zamontować.',
    'It looks just like new!': 'Wygląda jak nowe!',
    'Hopefully we don’t have any more incidents.': 'Mam nadzieję, że nie będzie już więcej incydentów.',
    'I’m sorry, Papa Brian. I just can’t control my strength.': 'Przepraszam, tato Brianie. Po prostu nie panuję nad swoją siłą.',
    'It’s quite alright, Hannah. You’re welcome at the church.': 'Wszystko w porządku, Hannah. Zawsze jesteś mile widziana w kościele.',
    'I sure love all this company. It makes me feel at home.': 'Uwielbiam to całe towarzystwo. Czuję się jak w domu.',
    'Oh! The news segment is starting soon!': 'O! Zaraz zaczyna się program informacyjny!',
    'News segment?': 'Program informacyjny?',
    '1Hero will be on TV tonight.': '1Hero będzie dziś wieczorem w telewizji.',
    'I’d love to see it!': 'Chętnie to zobaczę!',
    'Shit. We gotta get back to Heather’s place.': 'Cholera. Musimy wracać do Heather.',
    'I think I’ll stay here and watch it with Judy.': 'Chyba zostanę tu i obejrzę to z Judy.',
    'Your mom’s gonna be mighty mad at you.': 'Twoja mama będzie na ciebie wściekła.',
    'We have a TV upstairs. I’m sure we can get the broadcast.': 'Mamy telewizor na górze. Na pewno złapiemy transmisję.',
    'I’d love to stay. But I better get going. My mom will be waiting for me.': 'Chętnie bym została. Ale lepiej już pójdę. Mama będzie na mnie czekać.',
    'Tell my mom that I’ll be home later tonight.': 'Powiedz mamie, że wrócę później wieczorem.',
    'See ya around, Sister and Pa!': 'Do zobaczenia, siostro i tato!',
    'What an interesting girl.': 'Co za ciekawa dziewczyna.',
    'Let’s turn on the TV. I want to see 1Hero’s news show.': 'Włączmy telewizor. Chcę zobaczyć program 1Hero.',
    'Don’t expect too much. It’s a pretty short segment.': 'Nie spodziewaj się zbyt wiele. To dość krótki materiał.',
    'Come on! Let’s go watch it.': 'Chodź! Chodźmy to obejrzeć.',
    'Maybe bringing Hannah here was a mistake.': 'Może przyprowadzenie tu Hannah było błędem.',
    'Better guard the windows.': 'Lepiej pilnujcie okien.',
    'Please help fix the broken window. I don’t want any spiders to get into the church.': 'Proszę, pomóż naprawić wybite okno. Nie chcę, żeby pająki dostały się do kościoła.',
    'Are you gonna fix that window or do you want to play a game?': 'Naprawisz to okno czy chcesz się pobawić?',
    'You should be helping me fix it, Hannah. You broke it.': 'Powinnaś mi pomóc je naprawić, Hannah. To ty je stłukłaś.',
    'Your hard noggin broke it!': 'Twoja twarda głowa je stłukła!',
    'Hannah!': 'Hannah!',
    'Just keeping tabs on you.': 'Tylko mam na ciebie oko.',
    'You followed me here?': 'Przyszedłeś tu za mną?',
    'What a pretty church. I didn’t expect a man like you to be spending time at a place like this.': 'Jaki ładny kościół. Nie spodziewałam się, że facet taki jak ty spędza czas w takim miejscu.',
    'Why are you here, 1Hero? Solving a case?': 'Co tu robisz, 1Hero? Rozwiązujesz sprawę?',
    'I was spending some time with friends.': 'Spędzałem czas z przyjaciółmi.',
    'This place looks empty.': 'Wygląda na puste.',
    'Planning to rob it?': 'Planujesz to obrabować?',
    'Not at the moment.': 'Nie w tej chwili.',
    'I know Andrea has an undercover unit. Are you going to tell me what’s up or keep me in the dark?': 'Wiem, że Andrea ma jednostkę pod przykrywką. Powiesz mi, o co chodzi, czy dalej będziesz trzymał mnie w niewiedzy?',
    'Let’s keep things in the dark.': 'Niech na razie pozostanie w tajemnicy.',
    'Should I tell Andrea about her? If I’m working on the Guild case now, I should know who is in the undercover unit.': 'Powinienem powiedzieć Andrei o niej? Skoro teraz pracuję nad sprawą Gildii, powinienem wiedzieć, kto jest w jednostce pod przykrywką.',
    'Let’s take down that demon and make sure no one hurts Sister Judy.': 'Dopadnijmy tego demona i dopilnujmy, żeby nikt nie skrzywdził siostry Judy.',
    'Once you gather what we need, come back here and we’ll go catch Madalyn together.': 'Gdy zbierzesz to, czego potrzebujemy, wróć tutaj i razem złapiemy Madalyn.',
    'I think I got what we need.': 'Chyba mam to, czego potrzebowaliśmy.',
    'Good work, 1Hero.': 'Dobra robota, 1Hero.',
    'What does this mean? Can we capture her?': 'Co to znaczy? Możemy ją schwytać?',
    'I’m very worried.': 'Bardzo się martwię.',
    'I’ll stay close by. She wouldn’t dare mess with a priest.': 'Zostanę w pobliżu. Nie odważy się zadzierać z księdzem.',
    'Everyone, stay close to me.': 'Wszyscy, trzymajcie się blisko mnie.',
    'Please make sure Chloe is safe.': 'Proszę, dopilnuj, żeby Chloe była bezpieczna.',
    'I saw her. She’s near the waterfall to the east.': 'Widziałem ją. Jest przy wodospadzie na wschodzie.',
    'What’s the plan, Father?': 'Jaki jest plan, ojcze?',
    'You’re going to need a special relic… A holy chalice filled with holy water.': 'Będziesz potrzebować specjalnej relikwii… Świętego kielicha wypełnionego wodą święconą.',
    'What will that do?': 'Co to da?',
    'The cup will delay any attempt to flee, and the water will hold her in place.': 'Kielich opóźni każdą próbę ucieczki, a woda przytrzyma ją w miejscu.',
    'How will he lure her out of hiding?': 'Jak ją wywabi z ukrycia?',
    'Let me go with you.': 'Pozwól mi iść z tobą.',
    'Madalyn wanted me before… Maybe she’ll come for me again.': 'Madalyn już mnie chciała… Może znów po mnie przyjdzie.',
    'It’s dangerous, Chloe.': 'To niebezpieczne, Chloe.',
    'Not if we’re ready to take her on.': 'Nie, jeśli będziemy gotowi się z nią zmierzyć.',
    'Oh, Chloe.': 'Och, Chloe.',
    'Could it work?': 'Czy to może zadziałać?',
    '1Hero… I will guard the girls. You need to gather what we need to make the holy water relic.': '1Hero… Ja przypilnuję dziewczyn. Musisz zebrać to, czego potrzeba, by stworzyć relikwię z wodą święconą.',
    'Take this…': 'Weź to…',
    'I’ll find what we need.': 'Znajdę to, czego potrzeba.',
    'Once you do, come back to me and we can go into the forest together.': 'Gdy to zrobisz, wróć do mnie i razem pójdziemy do lasu.',
    'We can do it. It’ll work.': 'Dam radę. To się uda.',
    "I won't let you down.": 'Nie zawiodę cię.',
    'Seems you might be onto something, 1Hero.': 'Wygląda na to, że coś odkryłeś, 1Hero.',
    'Zephaniah didn’t have any medications held as evidence. There was never a formal investigation since it was deemed a heart attack.': 'Zephaniah nie miał żadnych leków zabezpieczonych jako dowód. Nigdy nie prowadzono formalnego śledztwa, bo uznano to za zawał serca.',
    'Just like Charles Wilkes.': 'Tak jak Charles Wilkes.',
    'Not quite the same…': 'Nie do końca to samo…',
    'Charles had medication in his system at the time of death.': 'Charles miał leki w organizmie w chwili śmierci.',
    'Hi, Sister Judy. This is my boss, Detective Bhatt.': 'Cześć, siostro Judy. To mój szef, detektyw Bhatt.',
    'A pleasure to meet you, Sister.': 'Miło cię poznać, siostro.',
    'What brings you here this afternoon?': 'Co sprowadza was tu dziś po południu?',
    '1Hero has told me that you had a run in with Madalyn Rose.': '1Hero mówił, że miałaś spotkanie z Madalyn Rose.',
    'Oh, yes. It was quite frightening…': 'Och, tak. To było dość przerażające…',
    'I was once very close to her, but she’s not the woman I thought I knew.': 'Kiedyś byłyśmy bardzo blisko, ale to nie ta sama kobieta, którą znałam.',
    'Did you know Father Zephaniah?': 'Znałaś ojca Zephaniaha?',
    'Not as well as the other nuns. I came here from Saint Dame University not long ago.': 'Nie tak dobrze jak inne zakonnice. Przybyłam tu z Uniwersytetu Saint Dame niedawno.',
    'We believe that the former priest may have had a connection with Madalyn.': 'Wierzymy, że były ksiądz mógł mieć związek z Madalyn.',
    'We’d sure love to look around.': 'Chętnie się rozejrzymy.',
    'Yes. Please, come inside.': 'Tak. Proszę, wejdźcie do środka.',
    'I can use the shingle to cover up the hole.': 'Mogę użyć gontu, by zakryć dziurę.',
    'We found something.': 'Coś znaleźliśmy.',
    'The nun was in the woods. She says she was looking for you.': 'Zakonnica była w lesie. Mówi, że cię szukała.',
    'Don’t know. She ran off crying.': 'Nie wiem. Uciekła z płaczem.',
    'What the hell, Bobby?': 'Co jest, Bobby?',
    'Hey! I’m not here to chase a nun.': 'Hej! Nie jestem tu, żeby ganiać zakonnicę.',
    'I don’t see any thieves. Where the hell are they?': 'Nie widzę żadnych złodziei. Gdzie oni, do cholery, są?',
    'Keep looking.': 'Szukaj dalej.',
    'You’re not being helpful.': 'Nie jesteś pomocny.',
    '1Hero! Are you here to play soccer with us?': '1Hero! Przyszedłeś zagrać z nami w piłkę?',
    'We’re not playing soccer! You’ll break another window.': 'Nie gramy w piłkę! Zbijesz kolejne okno.',
    'I’d like to show Heather the church.': 'Chciałbym pokazać Heather kościół.',
    'Looks impressive.': 'Wygląda imponująco.',
    'Don’t go wandering off.': 'Nie oddalaj się.',
    'It’s not that dangerous. We’ll be fine.': 'Nie jest tak niebezpiecznie. Poradzimy sobie.',
    'I know my way around the forest. Maybe we can go for a hike?': 'Znam się na lesie. Może wybierzemy się na wycieczkę?',
    'Ella…?': 'Ella…?',
    'Let’s not go too far.': 'Nie chodźmy zbyt daleko.',
    'And I thought you were tough.': 'A myślałam, że jesteś twardzielem.',
    'Just trying to keep safety in mind.': 'Po prostu staram się myśleć o bezpieczeństwie.',
    'I like the way you think, Ella.': 'Podoba mi się twój sposób myślenia, Ella.',
    'Come on! Let’s go on an adventure!': 'Chodź! Ruszamy na przygodę!',
    'Hey! Let me lead the way!': 'Hej! Pozwólcie, że poprowadzę!',
    'Come, Heather. I’ll show you inside.': 'Chodź, Heather. Pokażę ci środek.',
    'Lead the way, Sister Judy.': 'Prowadź, siostro Judy.',
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
        or context.get('map_id') != 6
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
    raise SystemExit('Unmapped Map 6 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 137:
    raise SystemExit(f'Expected exactly 137 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 6 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
