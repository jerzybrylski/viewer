#!/usr/bin/env python3
"""Build Polish drafts for the remaining Toma/rift dialogue on Map 125."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
EVENTS = {
    10: {
        "Kimberly! Wait up.": "Kimberly! Zaczekaj.",
        "This is what I saw! This was in my dream!": "To właśnie widziałam! Śniło mi się to!",
        "Damn! This place is bigger than I thought.": "Cholera! To miejsce jest większe, niż myślałam.",
        "Creepy… What the hell are these statues?": "Ale tu upiornie… Co to, do cholery, za posągi?",
        "This stone here… It’s part of the Toma Leolo.": "Ten kamień… To fragment Toma Leolo.",
        "The Toma… It’s a magic rock… It’s part of a Casula idol.": "Toma… To magiczny kamień… Fragment bożka Casula.",
        "Casula? Judging from the symbol on the floor I’d say this is more along the lines of Christian demonic.": "Casula? Sądząc po symbolu na podłodze, powiedziałabym, że ma to raczej związek z chrześcijańską demonologią.",
        "I don’t know how it connects, but I have three other pieces of this statue…": "Nie wiem, jak to się łączy, ale mam jeszcze trzy fragmenty tego posągu…",
        "They have… interesting effects.": "Mają… ciekawe właściwości.",
        "Just what type of effects are you talking about?": "O jakich właściwościach mówisz?",
        "Sexual stuff.": "Seksualnych.",
        "Haha. Are you kidding me?": "Haha. Żartujesz?",
        "I’m serious. The last one I found made my dick bigger.": "Mówię poważnie. Po znalezieniu poprzedniego urósł mi kutas.",
        "Just… Don’t touch it.": "Po prostu… Nie dotykaj go.",
    },
    11: {
        "What the hell was that?": "Co to, do cholery, było?",
        "I told you… It’s the Toma.": "Mówiłem ci… To Toma.",
        "But the feeling… I felt so horny.": "Ale to uczucie… Byłam tak podniecona.",
        "I felt it too… It must be the stone doing it.": "Ja też to poczułem… To pewnie działanie kamienia.",
        "This is amazing! The magic rocks, the satanic cult hideout… This will give us content for years!": "Niesamowite! Magiczne kamienie, kryjówka satanistycznej sekty… Mamy materiał na lata!",
        "You’re really going to report on magic sex rocks?": "Naprawdę zamierzasz robić reportaż o magicznych kamieniach do seksu?",
        "Something’s up and we’re going to break the story.": "Coś tu się dzieje i opiszemy to jako pierwsi.",
        "Quiet… Did you hear that?": "Cicho… Słyszałeś to?",
        "Fuck. Let’s get out of here before more of them show up.": "Kurwa. Wynośmy się stąd, zanim pojawi się ich więcej.",
        "This isn’t over, 1Hero.": "To jeszcze nie koniec, 1Hero.",
    },
    26: {
        "Mother may trust you, but I do not.": "Matka może ci ufać, ale ja nie.",
    },
    29: {
        "Take him to the rift. I will be there shortly.": "Zabierzcie go do szczeliny. Zaraz tam będę.",
        "Can he enter?": "Może wejść?",
        "He can, and he will.": "Może i wejdzie.",
        "Hey! What are you talking about?": "Hej! O czym wy mówicie?",
    },
    40: {
        "Kimberly!? What are you doing down here?": "Kimberly!? Co ty tu robisz na dole?",
        "I know so much now, 1Hero! What a story!": "Teraz wiem już tak dużo, 1Hero! Ależ to będzie historia!",
        "Where is Lillian? What did you see?": "Gdzie jest Lillian? Co widziałaś?",
        "There’s a portal to another world! And I’m going to break the story.": "Jest tu portal do innego świata! Opiszę to jako pierwsza.",
        "In time, my dear.": "W swoim czasie, kochana.",
        "Lillian! The cops are here.": "Lillian! Przyjechała policja.",
        "An unfortunate turn of events, but do not fret…": "Niefortunny obrót spraw, ale nie martw się…",
        "Once you complete the Toma, we will have all we need to bring peace.": "Gdy ukończysz Tomę, będziemy mieć wszystko, czego potrzeba, by zaprowadzić pokój.",
        "How much more time do you need, 1Hero?": "Ile jeszcze czasu potrzebujesz, 1Hero?",
        "Well… I… It’s not completed yet.": "Cóż… Ja… Jeszcze nie jest gotowa.",
        "We will stay hidden until you’ve completed the statue… Then salvation can come to the worlds of chaos.": "Pozostaniemy w ukryciu, dopóki nie ukończysz posągu… Wtedy zbawienie dotrze do światów chaosu.",
        "Kimberly, the Guild bust is happening today!": "Kimberly, nalot na Gildię odbędzie się dzisiaj!",
        "Shit… I need to get back to the office… I need to prepare.": "Cholera… Muszę wracać do biura… Muszę się przygotować.",
        "The Guild is not the story…": "Gildia nie jest tu najważniejsza…",
        "Miss Foxx… You are going to show the world something they’ve never imagined in their wildest dreams.": "Panno Foxx… Pokażesz światu coś, o czym nawet w najśmielszych marzeniach nie śnił.",
        "You’re… going to tell everyone?": "Zamierzasz… wszystkim powiedzieć?",
        "Yes, 1Hero. It’s time.": "Tak, 1Hero. Pora.",
        "No offense, but this is all kinda hard to believe… You’ll look crazy.": "Bez urazy, ale trudno w to uwierzyć… Wyjdziesz na wariatkę.",
        "I’ll… look crazy.": "Wyjdę… na wariatkę.",
        "Don’t listen to that. The people are ready to know the truth.": "Nie słuchaj go. Ludzie są gotowi poznać prawdę.",
        "Of course… They need to know the truth.": "Oczywiście… Muszą poznać prawdę.",
        "You have to help me, Kimberly. If you don’t, Nellie will go to jail and Melissa will lose her job.": "Musisz mi pomóc, Kimberly. Jeśli tego nie zrobisz, Nellie trafi do więzienia, a Melissa straci pracę.",
        "I… I should help him.": "Ja… Powinnam mu pomóc.",
        "Do what you must, but between the two of you I expect the Toma Leolo to be completed…": "Rób, co musisz, ale oczekuję, że we dwoje ukończycie Tomę Leolo…",
        "We understand.": "Rozumiemy.",
        "Let me help. I can help find the Toma pieces.": "Pozwól mi pomóc. Mogę poszukać fragmentów Tomy.",
        "Absolutely not. You must remain hidden. We must buy 1Hero time.": "Absolutnie nie. Musisz pozostać w ukryciu. Musimy zyskać dla 1Hero na czasie.",
        "Of course, Mother.": "Oczywiście, Matko.",
        "Our time is coming to an end. Do not fail Mother.": "Nasz czas dobiega końca. Nie zawiedź Matki.",
        "I’m handling it.": "Panuję nad sytuacją.",
        "Can we get out of here without getting spotted by the police?": "Możemy stąd wyjść, nie dając się zauważyć policji?",
        "Let’s tread carefully.": "Zachowajmy ostrożność.",
    },
    47: {
        "Oh, my Lord! What is she doing down here?": "O mój Boże! Co ona tu robi na dole?",
        "I tried to stop her.": "Próbowałem ją powstrzymać.",
        "Damn! What is this place?": "Cholera! Co to za miejsce?",
        "Lillian!": "Lillian!",
        "There are men taking over the mansion, 1Hero.": "1Hero, jacyś ludzie przejmują rezydencję.",
        "Duncan’s henchmen.": "Ludzie Duncana.",
        "What’s going on, Lillian? You’re working with Madalyn and she’s working with Duncan.": "Co się dzieje, Lillian? Współpracujesz z Madalyn, a ona z Duncanem.",
        "The Toma pieces… They are all here.": "Fragmenty Toma… Wszystkie tu są.",
        "We must combine the pieces, 1Hero. Our lives are at stake.": "Musimy połączyć fragmenty, 1Hero. Nasze życie jest zagrożone.",
        "You’re not answering my question.": "Nie odpowiedziałaś na moje pytanie.",
        "Does Duncan know about this place?": "Duncan wie o tym miejscu?",
        "No one’s supposed to be down here!": "Nikt nie powinien tu być!",
        "Where is Madalyn?": "Gdzie jest Madalyn?",
        "You want to escape this mansion? Then let’s complete the Toma–now!": "Chcecie uciec z tej rezydencji? To dokończmy Tomę. Natychmiast!",
        "How the hell do you expect us to do that?": "Jak, do cholery, mamy to zrobić?",
        "It’s in your blood, Erica.": "Masz to we krwi, Erico.",
        "Do not worry, my dear. We simply require your… special ancestry…": "Nie martw się, kochana. Potrzebujemy jedynie twojego… wyjątkowego pochodzenia…",
        "The ritual will be quite… pleasurable.": "Rytuał będzie całkiem… przyjemny.",
        "Ritual?": "Rytuał?",
        "Leave us, my children.": "Zostawcie nas, moje dzieci.",
        "What are you going to do to Erica?": "Co zamierzasz zrobić Erice?",
        "I’m not going to do anything to her…": "Nic jej nie zrobię…",
        "You are.": "Ty to zrobisz.",
    },
    50: {
        "Get back, you monster!": "Cofnij się, potworze!",
        "Argh! How the hell did you get down here!?": "Argh! Jak ty się, do cholery, dostałeś na dół!?",
        "Woah! Did I miss some excitement?": "Łał! Coś mnie ominęło?",
        "Damn. What were you all doing?": "Cholera. Co wy wszyscy robiliście?",
        "No! You’re ruining everything!": "Nie! Wszystko niszczycie!",
        "I said get back!": "Mówiłem, żebyś się cofnął!",
        "If you want me, come and get me!": "Jeśli mnie chcesz, to chodź i mnie złap!",
        "She’s heading for the rift!": "Zmierza do szczeliny!",
        "The rift?": "Do szczeliny?",
        "We have to get out of here before Duncan realizes we’re gone.": "Musimy się stąd wydostać, zanim Duncan zauważy, że nas nie ma.",
        "Stopping that monster.": "Powstrzymuję tego potwora.",
        "The Toma pieces… They stopped glowing.": "Fragmenty Toma… Przestały świecić.",
        "Take them. Let’s get out of here.": "Weźcie je. Wynośmy się stąd.",
        "You will not take the Toma Leolo from us!": "Nie odbierzecie nam Toma Leolo!",
        "Kill them!": "Zabijcie ich!",
        "Don’t harm them!": "Nie róbcie im krzywdy!",
        "We’re taking the Toma pieces.": "Zabieramy fragmenty Tomy.",
        "Like hell you are!": "Chyba śnisz!",
        "Hey! Let me go!": "Hej! Puśćcie mnie!",
        "Put my dad down, you monster!": "Odłóż mojego tatę, potworze!",
        "Dad?": "Tato?",
        "Tasha?": "Tasha?",
    },
    59: {
        "Do you know where you’re going?": "Wiesz, dokąd idziesz?",
    },
    63: {
        "Looks like Duncan didn’t kill 1Hero.": "Wygląda na to, że Duncan nie zabił 1Hero.",
        "About damn time. What took you so long?": "No najwyższy czas. Co cię tak zatrzymało?",
        "Uhhh… No specific reason.": "Yyy… Bez konkretnego powodu.",
        "Where did Henry and Diana go?": "Dokąd poszli Henry i Diana?",
        "Scoping out the mansion.": "Rozglądają się po rezydencji.",
        "We split up. Tasha and I will handle Madalyn… Those goons upstairs are more of a target for the adventurers.": "Rozdzieliliśmy się. Tasha i ja zajmiemy się Madalyn… Tym zbirami na górze mogą zająć się poszukiwacze przygód.",
        "So… They are going to kill Duncan?": "Czyli… Zamierzają zabić Duncana?",
        "Yeah… Of course.": "Tak… Oczywiście.",
        "How do we get into the rift?": "Jak dostać się do szczeliny?",
        "I know how to activate it. I’ll meet you there…": "Wiem, jak ją aktywować. Spotkamy się na miejscu…",
        "You’ll know it when you see it.": "Rozpoznasz ją, gdy ją zobaczysz.",
        "Come on, Tasha. Stay close to me.": "Chodź, Tasha. Trzymaj się blisko mnie.",
    },
    66: {
        "Erica!": "Erica!",
    },
    67: {
        "Ahhh… That feels much better.": "Ach… Od razu lepiej.",
        "Shit! The Toma!": "Cholera! Toma!",
        "What the hell happened to us?": "Co się z nami, do cholery, stało?",
        "Wasn’t it amazing!?": "Czyż to nie było niesamowite!?",
        "Lillian! She got away!": "Lillian! Uciekła!",
        "Shit… Get dressed. We need to find Father Solomon.": "Cholera… Ubieraj się. Musimy znaleźć ojca Solomona.",
        "Well, I’ll be damned. A basement!": "No proszę. Piwnica!",
        "She got away! She has the Toma!": "Uciekła! Ma Tomę!",
        "The priest told me you’d be having a party down here. I didn’t believe him at first.": "Ksiądz mówił, że urządzicie sobie tu przyjęcie. Na początku mu nie wierzyłem.",
        "We’ve got a problem, Duncan.": "Mamy problem, Duncan.",
        "We have to hurry! Lillian escaped!": "Musimy się pospieszyć! Lillian uciekła!",
        "There’s no time to waste. We need to go to the rift.": "Nie ma czasu do stracenia. Musimy iść do szczeliny.",
        "No one’s going anywhere.": "Nikt nigdzie nie idzie.",
        "We should listen to him… The Wilkes’ daughter and her minions escaped through here.": "Powinniśmy go posłuchać… Córka Wilkesa i jej sługusy uciekli tędy.",
        "This is attached to the bunker?": "To jest połączone z bunkrem?",
        "Not the bunker. It attaches to Hell.": "Nie z bunkrem. To przejście prowadzi do Piekła.",
        "Hahaha!...": "Hahaha!...",
        "Stop wasting time!": "Przestańcie marnować czas!",
        "Hey! Stop him!": "Hej! Zatrzymajcie go!",
    },
    81: {
        "Thank the Lord! Everyone is safe.": "Dzięki Panu! Wszyscy są bezpieczni.",
        "It must be that Daemalius creature. It’s angry.": "To pewnie ten stwór, Daemalius. Jest wściekły.",
        "Are we trapped down here?": "Jesteśmy tu uwięzieni?",
        "I don’t want to die like this.": "Nie chcę tak umierać.",
        "Suck it up! We’re here to do a mission.": "Weź się w garść! Jesteśmy tu na misji.",
        "Can you open the rift?": "Możesz otworzyć szczelinę?",
        "I have what I need.": "Mam wszystko, czego potrzebuję.",
        "Do you hear that?": "Słyszycie to?",
        "It stopped.": "Przestało.",
        "Can we escape?": "Możemy uciec?",
        "Father… Here is the demon part… Open the rift.": "Ojcze… Oto część demona… Otwórz szczelinę.",
        "We’re not far from the entry. I’ll bring the girls back to the church.": "Wejście jest niedaleko. Odprowadzę dziewczyny do kościoła.",
        "Hell no! We’re in this together.": "Chyba śnisz! Jesteśmy w tym razem.",
        "Hannah! You nearly got us killed.": "Hannah! Prawie nas pozabijałaś.",
        "This is war!": "To wojna!",
        "Let’s leave before that lightning storm returns.": "Chodźmy, zanim wróci burza z piorunami.",
        "Argh! Phooey!": "Argh! A niech to!",
    },
    90: {
        "I don’t care what you say, I’m getting my army!": "Nie obchodzi mnie, co mówisz. Zdobędę swoją armię!",
        "The Guild will be bigger and better than ever!": "Gildia będzie większa i potężniejsza niż kiedykolwiek!",
        "Hahahahahahahahahaha!": "Hahahahahahahahahaha!",
        "Duncan, the Toma Leolo was destroyed. It’s over. Put the gun down.": "Duncan, Toma Leolo została zniszczona. To koniec. Odłóż broń.",
        "No! I don’t believe it! It can be put back together!": "Nie! Nie wierzę! Da się ją złożyć z powrotem!",
        "You’re crazy! Can’t you see? What’s left?": "Zwariowałeś! Nie widzisz? Co z niej zostało?",
        "Take one step and this officer is dead!": "Zrób jeszcze krok, a ten funkcjonariusz zginie!",
        "You! Don’t get too close!": "Ty! Nie podchodź bliżej!",
        "Dad.": "Tato.",
        "So now you acknowledge me, son?": "A więc teraz się do mnie przyznajesz, synu?",
        "It’s over, Dad. You need to put the gun down.": "To koniec, tato. Odłóż broń.",
        "You arrogant whelp! I’ll put the gun down when I want to!": "Ty arogancki szczeniaku! Odłożę broń, kiedy zechcę!",
        "Maybe you should stay down… son.": "Może powinieneś leżeć… synu.",
        "Kirk, no!": "Kirk, nie!",
        "Finally, the cavalry has arrived.": "Nareszcie przybyła odsiecz.",
        "Arrest them!": "Aresztować ich!",
        "Vayne! You have to do something!": "Vayne! Musisz coś zrobić!",
        "I told you, Duncan: it’s over.": "Mówiłem ci, Duncan. To koniec.",
        "We lost.": "Przegraliśmy.",
        "I’m sorry, Nellie, but you’re also under arrest.": "Przykro mi, Nellie, ale ciebie też muszę aresztować.",
        "Can’t say it’s a surprise.": "Nie mogę powiedzieć, że jestem zaskoczona.",
        "Bobby, it wasn’t her fault. She didn’t know what she was doing.": "Bobby, to nie jej wina. Nie wiedziała, co robi.",
        "Get your hands off my mom!": "Zostaw moją mamę!",
        "Calm down, Tasha… I’m not escaping this one.": "Spokojnie, Tasha… Tym razem się nie wywinę.",
        "Detective Canmore, we have to bring you in, too.": "Detektywie Canmore, pana też musimy zabrać na komisariat.",
        "Well, I don’t think that’s necessary.": "Nie sądzę, żeby to było konieczne.",
        "Sergeant Rinaldi, you know the orders.": "Sierżancie Rinaldi, zna pan rozkazy.",
        "1Hero…": "1Hero…",
        "He’ll be alright, Heather.": "Nic mu nie będzie, Heather.",
        "You’re arresting a detective!?": "Aresztujecie detektywa!?",
        "Don’t worry… We’ll get him out of this… somehow.": "Nie martw się… Jakoś go z tego wyciągniemy…",
        "What about her? You have a permit for that gun, miss?": "A co z nią? Ma pani pozwolenie na tę broń?",
        "She’s a thief!": "To złodziejka!",
        "She saved us… That’s not her gun.": "Uratowała nas… Ta broń nie należy do niej.",
        "She’s alright, don’t worry about her.": "Nic jej nie będzie. Nie martw się o nią.",
        "I think it might be time to scram.": "Chyba pora się stąd zmywać.",
        "What kind of happy ending is this? How dare you arrest the good guys!": "Co to za szczęśliwe zakończenie? Jak śmiecie aresztować dobrych ludzi!",
        "Use some common sense! 1Hero’s not a bad man!": "Użyjcie rozumu! 1Hero nie jest złym człowiekiem!",
        "Please!": "Proszę!",
        "This isn’t over… We’ll have our trial.": "To jeszcze nie koniec… Staniemy przed sądem.",
        "You’ll pay for this! All of you will!": "Zapłacicie za to! Wszyscy!",
        "Yeah, yeah… Move it, Helmer.": "Dobra, dobra… Ruszaj się, Helmer.",
        "Don’t worry… I have a feeling things will work out just fine.": "Nie martw się… Mam przeczucie, że wszystko dobrze się ułoży.",
    },
}

known = set()
for path in (ROOT / 'drafts').rglob('*.jsonl'):
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            row = json.loads(line)
            if row.get('translation', '').strip():
                known.add(row['id'])
rows = []
missing = set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    source = ' '.join(row['source_text'].strip().split())
    if context.get('source_kind') != 'map' or context.get('map_id') != 125 or row['id'] in known:
        continue
    if not source or source.startswith('/') or source in {'…', '...', '..'} or not any(char.isalpha() for char in source):
        continue
    event_id = context.get('event_id')
    translation = EVENTS.get(event_id, {}).get(source)
    if translation is None:
        translation = EVENTS.get(event_id, {}).get(source.replace('’', "'"))
    if translation is None:
        translation = EVENTS.get(event_id, {}).get(source.replace("'", '’'))
    if translation is None:
        missing.add((event_id, source))
        continue
    row['translation'] = translation
    rows.append(row)
if missing:
    raise SystemExit('Unmapped strings: ' + repr(sorted(missing)))
path = ROOT / 'drafts/custom-dialogue-map125-toma-rift-followups-01.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8', newline='\n')
print(f'Wrote Map 125 Toma/rift follow-ups: {len(rows)} records across {len({r["context"]["event_id"] for r in rows})} events')
