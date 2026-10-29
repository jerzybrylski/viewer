#!/usr/bin/env python3
"""Build Polish drafts for remaining player-facing dialogue on Map 19."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map19-followups-01.jsonl'
TRANSLATIONS = {
    "That's odd.": "To dziwne.",
    'I finished at the church.': 'Skończyłem w kościele.',
    'Don’t rush your work, 1Hero.': 'Nie spiesz się, 1Hero.',
    'We’re all good, it was just a cat.': 'Wszystko w porządku, to był tylko kot.',
    'You’ve got a lot to learn.': 'Wiele jeszcze musisz się nauczyć.',
    'You knew that case was bogus. What’s the surprise?': 'Wiedziałeś, że ta sprawa była lipna. Co cię dziwi?',
    'Keep your damn mouth shut.': 'Trzymaj, do cholery, język za zębami.',
    'Do I have to go back to the office?': 'Muszę wracać do biura?',
    'Follow my lead, and just listen.': 'Rób, co mówię, i po prostu słuchaj.',
    'They’re with me.': 'Są ze mną.',
    'So, that’s it?': 'To już wszystko?',
    'Go find the maid, 1Hero.': 'Znajdź pokojówkę, 1Hero.',
    'But I thought…': 'Ale myślałem…',
    'I want to know more about this Madalyn woman.': 'Chcę dowiedzieć się więcej o tej Madalyn.',
    'I appreciate your help, 1Hero.': 'Dziękuję za pomoc, 1Hero.',
    'Do you remember the Saint Dame University case?': 'Pamiętasz sprawę z Uniwersytetu Saint Dame?',
    'Uhh… Refresh me.': 'Eee… Przypomnij mi.',
    'We’ll talk about this later, Paul.': 'Porozmawiamy o tym później, Paul.',
    'Madalyn Rose was the mother superior at Saint Dame Church.': 'Madalyn Rose była matką przełożoną w kościele Saint Dame.',
    'Wait… The one who kidnapped those girls?': 'Chwila… Tą, która porwała tamte dziewczyny?',
    'And then murdered a priest.': 'A potem zamordowała księdza.',
    'You think it’s her?': 'Myślisz, że to ona?',
    'There’s only one way to find out.': 'Jest tylko jeden sposób, żeby się przekonać.',
    'I’ll find the maid.': 'Znajdę pokojówkę.',
    'He wasn’t the only one. He’s distracting us.': 'Nie tylko on. Chce nas odciągnąć od sprawy.',
    'Do you remember her name?': 'Pamiętasz jej imię?',
    'I know. I’ll see what I can find.': 'Wiem. Sprawdzę, co uda mi się znaleźć.',
    'Erica Abraham… Lives in the apartments downtown.': 'Erica Abraham… Mieszka w apartamentach w centrum.',
    'So, you did listen.': 'Czyli jednak słuchałeś.',
    'I’ll find her and bring her in for questioning.': 'Znajdę ją i sprowadzę na przesłuchanie.',
    'I’ll meet you back at the office.': 'Spotkamy się w biurze.',
    'I knew there was more to this case.': 'Wiedziałem, że w tej sprawie jest coś więcej.',
    'Too bad Miss Bhatt doesn’t listen to me.': 'Szkoda, że panna Bhatt mnie nie słucha.',
    'I better not let her down. I need to find Erica.': 'Nie mogę jej zawieść. Muszę znaleźć Ericę.',
    'Bobby? What’s going on?': 'Bobby? Co się dzieje?',
    'What’s going on? What do you want to show me?': 'Co się dzieje? Co chcesz mi pokazać?',
    'We’re reducing the police presence here. Commissioner’s orders.': 'Ograniczamy tu obecność policji. Rozkaz komisarz.',
    'There’s a storage bunker under our feet.': 'Pod nami znajduje się schron magazynowy.',
    'Is Lillian aware?': 'Lillian o tym wie?',
    'Welcome back, 1Hero. What brings you here?': 'Witaj ponownie, 1Hero. Co cię sprowadza?',
    'We can’t find the girl.': 'Nie możemy znaleźć dziewczyny.',
    'I’ve been working on your case, and I’ve made some connections with people who know Duncan Helmer.': 'Pracowałem nad twoją sprawą i nawiązałem kontakt z ludźmi, którzy znają Duncana Helmera.',
    'Is anyone looking for her?': 'Ktoś jej szuka?',
    'Duncan Helmer?': 'Duncan Helmer?',
    'We’re not babysitters, 1Hero.': 'Nie jesteśmy niańkami, 1Hero.',
    'He’s one of the leaders of the Eclipse Guild. He would know who stole your father’s amulets.': 'Jest jednym z przywódców Gildii Eclipse. Może wiedzieć, kto ukradł amulety twojego ojca.',
    'If what I suspect is true, then Charles could very well have been a Guild leader and Lillian may be continuing the family business.': 'Jeśli moje podejrzenia są słuszne, Charles mógł być przywódcą Gildii, a Lillian może kontynuować rodzinny interes.',
    'If you’re so concerned, then you find her.': 'Jeśli tak się martwisz, sam ją znajdź.',
    'Come, 1Hero. Let us speak inside.': 'Chodź, 1Hero. Porozmawiajmy w środku.',
    'So, how do we get to the bunker?': 'Więc jak dostać się do schronu?',
    'I’ve not figured that out yet. I was hoping to see something obvious.': 'Jeszcze tego nie ustaliłem. Liczyłem, że zauważę coś oczywistego.',
    'Sorry, ma’am. I said no interviews.': 'Przykro mi, proszę pani. Mówiłam, że nie udzielamy wywiadów.',
    'Do you know who I am?': 'Wie pani, kim jestem?',
    'Please leave the premises.': 'Proszę opuścić teren.',
    '1Hero! Thank God you’re here.': '1Hero! Dzięki Bogu, że jesteś.',
    'Kimberly? What are you doing here?': 'Kimberly? Co tu robisz?',
    "Trying to film a segment for Channel 4 Tonight, but these knuckleheads won't give me an interview.": 'Próbuję nagrać materiał dla „Channel 4 Tonight”, ale ci durnie nie chcą udzielić mi wywiadu.',
    'God dammit! Why is she still here?': 'Niech to szlag! Czemu ona wciąż tu jest?',
    'What’s going on here at the Wilkes’ mansion? Care to comment?': 'Co się dzieje w rezydencji Wilkesów? Chcecie to skomentować?',
    'No comments! Now leave.': 'Bez komentarza! A teraz proszę odejść.',
    'Was Charles Wilkes a Guild leader? Has the Guild been operating out of North Santiva?': 'Czy Charles Wilkes był przywódcą Gildii? Czy Gildia działała z North Santiva?',
    'Get her out of here, 1Hero.': 'Zabierz ją stąd, 1Hero.',
    'Kimberly… We can’t really talk about what’s going on here.': 'Kimberly… Nie możemy rozmawiać o tym, co tu się dzieje.',
    '1Hero… I thought you’d be more helpful.': '1Hero… Myślałam, że będziesz bardziej pomocny.',
    'Look… The daughter of Charles is in danger from thieves trying to take advantage of the lack of security.': 'Słuchaj… Córce Charlesa grożą złodzieje, którzy chcą wykorzystać brak ochrony.',
    'You can’t fool me, 1Hero. I know more than you think.': 'Nie oszukasz mnie, 1Hero. Wiem więcej, niż myślisz.',
    'If you don’t leave, you’re under arrest.': 'Jeśli nie odejdziesz, aresztuję cię.',
    'Fine. I see how it is. I wonder if the commissioner will share your lack of enthusiasm for informing the people.': 'Dobra, rozumiem. Ciekawe, czy komisarz też nie będzie chciała informować ludzi.',
    'It’s her orders… No interviews.': 'Taki jest jej rozkaz… Żadnych wywiadów.',
    "Kimura won't be happy that your broad is here filming the mansion.": 'Kimurze nie spodoba się, że twoja laska nagrywa tu materiał.',
    'I had no idea she was here.': 'Nie wiedziałem, że tu jest.',
    'Don’t make my job hard, 1Hero.': 'Nie utrudniaj mi pracy, 1Hero.',
    'No sign of any thieves. But I suspect the lady inside isn’t too happy about our presence.': 'Nie ma śladu złodziei. Ale podejrzewam, że pani w środku nie jest zadowolona z naszej obecności.',
    'I’m sure she isn’t.': 'Jestem tego pewien.',
    'I could probably figure out a way to get inside… But I think I’d rather keep watch right here.': 'Pewnie znalazłbym sposób, żeby dostać się do środka… Ale chyba wolę pilnować tego miejsca.',
    "We’re not getting in. Just wait 'til the daughter gets back.": 'Nie wejdziemy do środka. Poczekaj, aż córka wróci.',
    'Oh great, another detective. Today just keeps getting better.': 'No świetnie, kolejny detektyw. Ten dzień robi się coraz lepszy.',
    "What's that supposed to mean?": 'Co to ma znaczyć?',
    "I dunno, detective. If you're so smart, you tell me.": 'Nie wiem, detektywie. Skoro jesteś taki mądry, sam mi powiedz.',
    'Lay off it, Bobby.': 'Daj spokój, Bobby.',
    'You ready for another round, tough guy?': 'Gotowy na kolejną rundę, twardzielu?',
    'Sure, handle it with your fists like a couple of Neanderthals.': 'Jasne, załatwcie to pięściami jak para neandertalczyków.',
    'See, Bobby? This is why you aren’t a detective.': 'Widzisz, Bobby? Właśnie dlatego nie jesteś detektywem.',
    'I could have broken in if I tried harder.': 'Dałbym radę się włamać, gdybym bardziej się postarał.',
    'Stop arguing. We need to find Lillian.': 'Przestańcie się kłócić. Musimy znaleźć Lillian.',
    'Shut it.': 'Zamknij się.',
    'You shut it.': 'Sam się zamknij.',
    'Children, can we get back to the task at hand?': 'Dzieci, możemy wrócić do tego, co mamy zrobić?',
    'Shouldn’t you be inside with Lillian? Why are you outside?': 'Nie powinieneś być w środku z Lillian? Czemu jesteś na zewnątrz?',
    'The wonderful weather, genius.': 'Podziwiamy tę wspaniałą pogodę, geniuszu.',
    "The door's locked and no one answered.": 'Drzwi są zamknięte i nikt nie odpowiada.',
    'That’s strange. Why wouldn’t she answer the door?': 'Dziwne. Czemu nie otwiera?',
    "You were sent here to warn her, weren't you?": 'Przysłano cię, żeby ją ostrzec, prawda?',
    "What if she's already in danger?": 'A jeśli już jest w niebezpieczeństwie?',
    "Slow down, hotshot. We don't have a warrant or probable cause.": 'Spokojnie, cwaniaku. Nie mamy nakazu ani uzasadnionego podejrzenia.',
    'Listen to gramps, Mike Tyson. No warrant.': 'Posłuchaj dziadka, Mike’u Tysonie. Nie mamy nakazu.',
    "Right. Like you've ever cared about a warrant before, Bobby.": 'Jasne. Jakbyś kiedykolwiek przejmował się nakazem, Bobby.',
    "What're you trying to say?": 'Co próbujesz powiedzieć?',
    'Are all young men this obtuse these days?': 'Czy wszyscy młodzi faceci są teraz tacy tępi?',
    "While you figure that out, I'm going to try calling Erica.": 'A wy sobie myślcie, a ja spróbuję zadzwonić do Eriki.',
    'She’s not picking up…': 'Nie odbiera…',
    'Strange. She should be at work right now.': 'Dziwne. Powinna być teraz w pracy.',
    'Like we said. You deaf or slow, detective?': 'Mówiliśmy ci. Jesteś głuchy czy powolny, detektywie?',
    'Let me try picking the lock if this is so urgent.': 'Daj mi spróbować otworzyć zamek, skoro to takie pilne.',
    'This oughta be good.': 'To będzie ciekawe.',
    'Can you do this any faster, David?': 'Możesz się pospieszyć, David?',
    'Out of the way, old man. I’ll show you how to open a door.': 'Z drogi, staruszku. Pokażę ci, jak się otwiera drzwi.',
    'Ha! You showed me, wood-for-brains.': 'Ha! Ale mi pokazałeś, bezmózgu.',
    'Ugh. Keep trying; I’ll look for another way in.': 'Ech. Próbuj dalej, a ja poszukam innego wejścia.',
    'It looks like a window is open up there. Can I reach it with something?': 'Wygląda na to, że tam na górze jest otwarte okno. Czy mogę do niego sięgnąć za pomocą czegoś?',
    'What the hell is he doing?': 'Co on, do cholery, wyprawia?',
    'You got lucky today.': 'Dziś ci się poszczęściło.',
    "Officers have each other's back. What happened today wasn’t luck.": 'Funkcjonariusze zawsze wspierają swoich. To, co się dziś stało, nie było szczęściem.',
    'I guess the threat is waning…': 'Chyba zagrożenie słabnie…',
    'We’ve got this detective.': 'Panujemy nad sytuacją, detektywie.',
    'It’s too dark. Whoever is still around the mansion is going to be hard to spot.': 'Jest zbyt ciemno. Trudno będzie dostrzec kogokolwiek kręcącego się przy rezydencji.',
    'I sure hope I don’t have to take on a gang of thieves by myself.': 'Mam nadzieję, że nie będę musiał sam mierzyć się z bandą złodziei.',
    'Once night falls, it’ll be hard to see anyone roaming around the mansion.': 'Kiedy zapadnie noc, trudno będzie dostrzec kogokolwiek kręcącego się wokół rezydencji.',
    'These cops are a pain in the ass. Did you manage to get inside?': 'Ci gliniarze są upierdliwi. Udało ci się wejść do środka?',
    'Yeah… But Lilith escaped with the Toma.': 'Tak… Ale Lilith uciekła z Tomą.',
    'Hey. Move aside. I need to speak to Lillian.': 'Proszę się odsunąć. Muszę porozmawiać z Lillian.',
    'No one’s allowed to enter until Officer Rinaldi gets here.': 'Nikt nie może wejść, dopóki nie przyjedzie funkcjonariusz Rinaldi.',
    'What are you talking about? I need to get inside now.': 'O czym ty mówisz? Muszę natychmiast wejść do środka.',
    'The girl isn’t here.': 'Dziewczyny tu nie ma.',
    'I have no clue. Get out of here.': 'Nie mam pojęcia. Wynoś się stąd.',
    'How long will it be before Bobby gets here?': 'Kiedy przyjedzie Bobby?',
    'Not long. He’s on his way.': 'Niedługo. Już jedzie.',
    'Hey! You’re not allowed here anymore.': 'Hej! Nie wolno ci już tu wchodzić.',
    'I need to get through. I need to speak to the commissioner.': 'Muszę przejść. Muszę porozmawiać z komisarz.',
    'Damn! It’s raining cats and dogs.': 'Cholera! Leje jak z cebra.',
    'Welcome to North Santiva.': 'Witaj w North Santiva.',
    'Careful. Let Erica lead the way.': 'Uważaj. Pozwól Erice prowadzić.',
    'Where are all the cops?': 'Gdzie są wszyscy policjanci?',
    'Andrea withdrew them. We should be safe.': 'Andrea ich wycofała. Powinniśmy być bezpieczni.',
    'You all have to leave! I have to go back inside.': 'Wszyscy musicie odejść! Muszę wrócić do środka.',
    'Duncan doesn’t know you’re a mole?': 'Duncan nie wie, że jesteś wtyczką?',
    'It’s complicated, 1Hero.': 'To skomplikowane, 1Hero.',
    'Erica!?': 'Erica!?',
    'I thought you were going to be let go. How much longer are you going to be doing this?': 'Myślałam, że cię zwolnią. Jak długo jeszcze będziesz to robić?',
    'She won’t stop, Tasha.': 'Nie przestanie, Tasha.',
    'Hey! Fuck you! When this is over, I’m finished.': 'Hej! Pierdol się! Jak to się skończy, odchodzę.',
    'We need to kill him. That will put a stop to everything.': 'Musimy go zabić. To zakończy całą sprawę.',
    'It’s not going to happen.': 'Nie ma mowy.',
    'Get out of here before he sees us!': 'Uciekaj stąd, zanim nas zobaczy!',
    'Come on. We have to go.': 'Chodźmy. Musimy iść.',
    'Be careful in there, Nellie.': 'Uważaj tam, Nellie.',
    'I can handle myself, Brian.': 'Sama sobie poradzę, Brian.',
    "Let's go back to the cathedral.": 'Wracajmy do katedry.',
    'Looks like Duncan’s guards are not out front…': 'Wygląda na to, że strażników Duncana nie ma przed wejściem…',
    'I better be careful if I go inside.': 'Lepiej uważać, jeśli wejdę do środka.',
    'Woah! Step back!': 'O rany! Cofnij się!',
    'Oh my goodness!': 'O mój Boże!',
    'The Guild is in there. But we can’t get in.': 'Gildia jest w środku, ale nie możemy się tam dostać.',
    'Melissa!': 'Melissa!',
    'How did they escape?': 'Jak im się udało uciec?',
    "Should've just killed Duncan.": 'Trzeba było po prostu zabić Duncana.',
    'We have to save her…': 'Musimy ją uratować…',
    'Officers! There is a detective in there!': 'Funkcjonariusze! W środku jest detektyw!',
    'What? How come we didn’t know?': 'Co? Dlaczego o tym nie wiedzieliśmy?',
    'Nevermind that! I need to get in there!': 'Nieważne! Muszę się tam dostać!',
    'We’re trying! We can’t just barge in. The doors have been barricaded.': 'Próbujemy! Nie możemy tak po prostu wedrzeć się do środka. Drzwi zabarykadowano.',
    'Fuck! Go through the back.': 'Cholera! Wejdźcie od tyłu.',
    'You’re not even supposed to be here, Canmore. Scram.': 'W ogóle nie powinno cię tu być, Canmore. Zmykaj.',
    '1Hero…': '1Hero…',
    "Let's sneak in ourselves.": 'Zakradnijmy się tam sami.',
    'I was just thinking the same.': 'Właśnie o tym samym pomyślałem.',
    'Through the church.': 'Przez kościół.',
    'Or the creek west of the mansion.': 'Albo przez strumień na zachód od rezydencji.',
    'Sounds like we have options.': 'Wygląda na to, że mamy kilka możliwości.',
    'I’ll wait… Someone should be here in case they get the front door open.': 'Zaczekam… Ktoś powinien tu być, gdyby udało im się otworzyć frontowe drzwi.',
    'Then I’ll stay here with you.': 'W takim razie zostanę tu z tobą.',
    'Don’t draw attention to yourselves.': 'Nie zwracajcie na siebie uwagi.',
    'Arianna… Are there any powers you have that can help us?': 'Arianna… Masz jakieś moce, które mogłyby nam pomóc?',
    'I don’t know. I’ve never been in a human body before.': 'Nie wiem. Nigdy wcześniej nie byłam w ludzkim ciele.',
    'I know where Diana is. I’ll run ahead and let her know the plan.': 'Wiem, gdzie jest Diana. Pobiegnę przodem i powiem jej o planie.',
    'We’re here to save Melissa and find Lilith… We’re not killing Duncan.': 'Jesteśmy tu, żeby uratować Melissę i znaleźć Lilith… Nie zabijemy Duncana.',
    'And we’re not sticking around once those cops get inside.': 'A kiedy policjanci dostaną się do środka, znikamy stąd.',
    'See you around back.': 'Do zobaczenia z tyłu.',
    'Which direction should we embark?': 'W którą stronę powinniśmy ruszyć?',
    'I look forward to a showdown with Madalyn… I just hope we can save your friend.': 'Nie mogę się doczekać starcia z Madalyn… Mam tylko nadzieję, że uda nam się uratować twoją przyjaciółkę.',
    'If the police open the front door, I’ll make my way to the basement.': 'Jeśli policja otworzy frontowe drzwi, zejdę do piwnicy.',
    'Don’t get caught.': 'Nie daj się złapać.',
    'Erica? Are you feeling okay?': 'Erica? Dobrze się czujesz?',
    'I’m cold.': 'Jest mi zimno.',
    'Not sure why we keep asking her. She’s always cold.': 'Nie wiem, po co wciąż ją pytamy. Zawsze jest jej zimno.',
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
        or context.get('source_kind') != 'map'
        or context.get('map_id') != 19
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
    raise SystemExit('Unmapped Map 19 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 185:
    raise SystemExit(f'Expected exactly 185 natural dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 19 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
