#!/usr/bin/env python3
"""Build Polish drafts for the remaining natural dialogue on Map 151."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map151-hell-followups-02.jsonl'
TRANSLATIONS = {
    'This is incredible!': 'To niesamowite!',
    'You can say that again. I can’t believe something like this exists.': 'Nie musisz mi mówić. Nie mogę uwierzyć, że coś takiego istnieje.',
    'I don’t see anyone.': 'Nikogo nie widzę.',
    'Shit… This is not a good place to hang out.': 'Cholera… To kiepskie miejsce na pogawędkę.',
    'Don’t be so scared.': 'Nie bój się tak.',
    'We’re literally standing in Hell.': 'Dosłownie stoimy w Piekle.',
    'And yet, I feel fine.': 'A mimo to czuję się dobrze.',
    'Unexpected guests! My lucky day!': 'Niespodziewani goście! Ale mam szczęście!',
    'Ahh! Get back!': 'Aah! Cofnij się!',
    'You’re so… beautiful!': 'Jesteś taka… piękna!',
    'That I am, my pretty human.': 'I owszem, moja śliczna człowieczko.',
    'Oh, shit! It’s happening again!': 'O cholera! Znowu się zaczyna!',
    'Wait! I must go back!': 'Czekaj! Muszę wrócić!',
    'She’s brainwashed!': 'Wyprano jej mózg!',
    'You’re coming with us, dear.': 'Chodź z nami, kochanie.',
    'Move it or lose it, sister!': 'Ruszać się, siostrzyczko!',
    'You’ll pay for that!': 'Zapłacisz mi za to!',
    'Now, now. 1Hero has been brainwashed by the priest. He doesn’t understand.': 'Spokojnie. Kapłan wyprał 1Hero mózg. On nie rozumie, co się dzieje.',
    'You’re the one brainwashing Kimberly!': 'To ty pierzesz Kimberly mózg!',
    'She got away.': 'Uciekła.',
    'Let them go. Kimberly understands our plight. She’ll do the right thing.': 'Puśćcie ich. Kimberly rozumie, w jakiej jesteśmy sytuacji. Postąpi właściwie.',
    'Get away from me!': 'Odsuń się ode mnie!',
    'You don’t want us to get away from you, human.': 'Nie chcesz, żebyśmy się od ciebie odsunęli, człowieku.',
    'Don’t run, 1Hero. We are here to help you.': 'Nie uciekaj, 1Hero. Chcemy ci pomóc.',
    'I know your tricks!': 'Znam wasze sztuczki!',
    'Yeah! And… I…': 'Tak! I… ja…',
    '…just want a little bit of pussy before I go.': '…chcę jeszcze przed wyjściem trochę cipki.',
    'I’m glad you’re here, 1Hero. This is a world of torment…': 'Cieszę się, że tu jesteś, 1Hero. To świat pełen cierpienia…',
    'I can fix it.': 'Mogę to naprawić.',
    'With the Toma?': 'Za pomocą Toma?',
    'Yes, my dear. The Toma will light the way and the damned will be spared an eternity of pain.': 'Tak, kochanie. Toma wskaże drogę, a potępieni unikną wieczności cierpienia.',
    'Yes, Mother! Our freedom is at hand!': 'Tak, Matko! Nasze wyzwolenie jest blisko!',
    'Well… I mean… Who wouldn’t want freedom?': 'Cóż… To znaczy… Kto nie chciałby być wolny?',
    'Give the boy some pussy, darlings.': 'Dajcie chłopcu trochę cipki, kochane.',
    'He looks even more delicious than the human woman!': 'Wygląda jeszcze smakowiciej niż ta ludzka kobieta!',
    'Jesus! It’s just like the Bible describes.': 'Jezu! Dokładnie tak, jak opisuje Biblia.',
    'This place looks awesome!': 'Ależ to miejsce jest niesamowite!',
    'Be careful. Demons wander this area.': 'Uważaj. Po okolicy krążą demony.',
    'I’m ready to face them.': 'Jestem gotowa stawić im czoła.',
    'How do we get past here? This place has lots of… fire.': 'Jak się przedostaniemy? Wszędzie jest… ogień.',
    'It’s Hell, Tasha. What did you expect?': 'To Piekło, Tasha. Czego się spodziewałaś?',
    'I’m sure I can find a way to get past.': 'Na pewno znajdę sposób, żeby się przedostać.',
    'We’ll need something special to put out these flames… Maybe some holy water.': 'Będziemy potrzebować czegoś specjalnego, by ugasić te płomienie… Może wody święconej.',
    'Ahh! The portal closed!': 'Aaa! Portal się zamknął!',
    'Where’s the other demon?': 'Gdzie jest drugi demon?',
    'You closed the rift?... How will he get through?': 'Zamknęłaś szczelinę?... Jak on się przez nią przedostanie?',
    'Trust me. He’ll figure it out quickly.': 'Zaufaj mi. Szybko coś wymyśli.',
    'No funny business, or I’ll shoot you!': 'Żadnych sztuczek, bo cię zastrzelę!',
    'This isn’t how it was supposed to be! Why did you come here?': 'To nie tak miało wyglądać! Po co tu przyszliście?',
    'The mansion was caving in. What did you expect us to do?': 'Rezydencja się waliła. Co mieliśmy zrobić?',
    'Run for the temple! There’s no time to wait!': 'Biegiem do świątyni! Nie ma czasu!',
    'This place has lots of… fire.': 'Wszędzie jest… ogień.',
    'We’ll need something special to put out those flames… Maybe some holy water.': 'Będziemy potrzebować czegoś specjalnego, by ugasić te płomienie… Może wody święconej.',
    'Hell yeah! Now we’re in business.': 'No jasne! Teraz zaczyna się zabawa.',
    'I want more pussy!': 'Chcę więcej cipki!',
    'Leave him, my children. He’s had enough.': 'Zostawcie go, moje dzieci. Wystarczy mu.',
    'No, I haven’t!': 'Nie, nie mam dość!',
    'Come. We must leave Mother with him.': 'Chodźcie. Zostawmy Matkę z nim.',
    'Aww. I wanted more.': 'Och, chciałam więcej.',
    'The time will come again soon, my dear.': 'Wkrótce znów będzie okazja, kochanie.',
    'Thank you, Mother.': 'Dziękuję, Matko.',
    'Can I have more of your pussy? Can I do your ass?': 'Mogę dostać więcej twojej cipki? Mogę wejść ci w tyłek?',
    'Calm down, 1Hero. You drank quite a bit of our love juice.': 'Spokojnie, 1Hero. Wypiłeś sporo naszego eliksiru miłości.',
    'Come. Let’s get you home.': 'Chodź. Zabierzmy cię do domu.',
    'Madalyn! Where is Judy? I know you’re in here!': 'Madalyn! Gdzie jest Judy? Wiem, że tu jesteś!',
    'Lillian! I know you’re sparing me… I need to know where Sister Judy is.': 'Lillian! Wiem, że mnie oszczędzasz… Muszę wiedzieć, gdzie jest siostra Judy.',
    'I should get the hell out of here and wait for Father.': 'Powinnam stąd uciekać i poczekać na ojca.',
    'What’s the rush, 1Hero?': 'Dokąd tak pędzisz, 1Hero?',
    'Madalyn! Hand over Judy!': 'Madalyn! Oddaj Judy!',
    'Haha! I think not!': 'Haha! Chyba nie!',
    'Where is Lillian? She’ll listen to me.': 'Gdzie jest Lillian? Ona mnie posłucha.',
    'Why don’t you go and meet her?': 'Czemu do niej nie pójdziesz?',
    'She’s here?': 'Jest tutaj?',
    'Across the bridge.': 'Po drugiej stronie mostu.',
    'I don’t trust you.': 'Nie ufam ci.',
    'You don’t have to trust me. Mother and I don’t always see eye to eye.': 'Nie musisz mi ufać. Matka i ja nie zawsze się zgadzamy.',
    'Show me Sister Judy. Let me know she’s safe.': 'Pokaż mi siostrę Judy. Chcę wiedzieć, że jest bezpieczna.',
    'You demand a lot, 1Hero. But I really think you should speak to Mother.': 'Dużo żądasz, 1Hero. Naprawdę uważam, że powinieneś porozmawiać z Matką.',
    'Where the hell do we even look for the way out of here?': 'Gdzie, do cholery, mamy szukać wyjścia?',
    'Ella!': 'Ella!',
    '1Hero! Go find Kimberly!': '1Hero! Znajdź Kimberly!',
    'You can’t fight them without Father Solomon.': 'Bez ojca Solomona ich nie pokonasz.',
    'It’s over, 1Hero. I’m not getting paid.': 'To koniec, 1Hero. Nie dostanę zapłaty.',
    'What are you saying? That’s the last thing you should be worried about.': 'Co ty mówisz? Nie to powinno cię teraz martwić.',
    'I thought about doing it, 1Hero… I thought about rescuing Duncan.': 'Myślałem o tym, 1Hero… Myślałem, żeby uratować Duncana.',
    'Andrea has left… Everything is over.': 'Andrea odeszła… To już koniec.',
    "Andrea's not getting out of this one… Everything is over.": 'Andrea tym razem się z tego nie wywinie… To już koniec.',
    'Then let me do this… Let me go out doing what I know.': 'Więc pozwól mi to zrobić… Pozwól mi zginąć, robiąc to, co umiem.',
    'Come on, Ella… There’s a life to live still.': 'No dalej, Ella… Przed nami jeszcze całe życie.',
    'Why isn’t it glowing?': 'Czemu nie świeci?',
    'It’s closed.': 'Jest zamknięta.',
    'Why did you come after me?': 'Dlaczego za mną poszedłeś?',
    'We’ll be fine. I gave Father the journal and he’ll figure out how to open it.': 'Poradzimy sobie. Dałem ojcu dziennik, a on znajdzie sposób, by go otworzyć.',
    'In the meantime, we’re going to have to survive down here.': 'Tymczasem musimy tu przetrwać.',
    'Let’s be useful. Let’s find Lillian.': 'Nie traćmy czasu. Znajdźmy Lillian.',
    'We don’t stand a chance against her.': 'Nie mamy z nią szans.',
    'She seems to be letting you off the hook… I think she likes you.': 'Wygląda na to, że ci odpuszcza… Chyba cię lubi.',
    'Are you suggesting I talk sense into a demon?': 'Sugerujesz, żebym przemówił demonowi do rozsądku?',
    'Enough to distract her… I’ll make the killing blow.': 'Wystarczy, żeby ją rozproszyć… Ja zadam śmiertelny cios.',
    'Ella…': 'Ella…',
    'Where the hell do we even look?': 'Gdzie do cholery mamy jej szukać?',
    'Shit! The portal is still closed.': 'Cholera! Portal nadal jest zamknięty.',
    'Good! I could use some practice!': 'Dobrze! Przyda mi się trochę treningu!',
    'Die, fuckers! You’ll never take me alive!': 'Gińcie, skurwysyny! Nigdy mnie nie złapiecie żywego!',
    'We did it! They’re dead!': 'Udało się! Nie żyją!',
    'Those demons are still here somewhere.': 'Te demony wciąż gdzieś tu są.',
    'Kill her!': 'Zabij ją!',
    'Did you get it, Dad?': 'Masz go, tato?',
    'We got it!': 'Mamy go!',
    'We’re pretty sure we got it.': 'Chyba go mamy.',
    'We have it.': 'Mamy go.',
    'Kirk!?': 'Kirk!?',
    'What!? Why is he here?': 'Co!? Dlaczego on tu jest?',
    'What the hell? How did he get here?': 'Co do cholery? Jak on się tu dostał?',
    'It’s a long story. Where are your men?': 'Długa historia. Gdzie są twoi ludzie?',
    'They still haven’t returned.': 'Wciąż nie wrócili.',
    'They probably got smashed.': 'Pewnie dostali niezły łomot.',
    'Hannah!': 'Hannah!',
    'No, they didn’t!': 'Nie, nie zginęli!',
    'The Lord will look after them.': 'Pan się nimi zaopiekuje.',
    'I’ll find them. Everyone, stay here.': 'Znajdę ich. Wszyscy zostańcie tutaj.',
    'Are you going back to the mansion?': 'Wracasz do rezydencji?',
    '1Hero, it’s too dangerous!': '1Hero, to zbyt niebezpieczne!',
    'It’s dangerous here, Heather… We need to make sure it’s safe to leave.': 'Tutaj też jest niebezpiecznie, Heather… Musimy sprawdzić, czy możemy bezpiecznie wyjść.',
    'Trust the boy… He knows what he’s doing.': 'Zaufaj chłopakowi… Wie, co robi.',
    'Be safe, 1Hero.': 'Uważaj na siebie, 1Hero.',
    'Fuck! I came!': 'Kurwa! Doszedłem!',
    'Hey, I don’t feel it anymore!': 'Hej, już tego nie czuję!',
    'The rift is open!': 'Szczelina jest otwarta!',
    'Where the hell is Lilith?': 'Gdzie do cholery jest Lilith?',
    'I hope Lillian is okay.': 'Mam nadzieję, że z Lillian wszystko w porządku.',
    'Hot damn! What a cool place!': 'Cholera! Ale odjazdowe miejsce!',
    'Cool? Not the word I’d use.': 'Odjazdowe? To nie jest słowo, którego bym użył.',
    'Everyone, stay near the rift. If any monster tries to attack you, go through it.': 'Wszyscy trzymajcie się blisko szczeliny. Jeśli zaatakuje was jakiś potwór, przejdźcie przez nią.',
    'What about the mansion? Isn’t it collapsing?': 'A co z rezydencją? Przecież się wali, prawda?',
    'You’re better off dying on Earth than being trapped here.': 'Lepiej zginąć na Ziemi niż utknąć tutaj.',
    'Bobby… You and your men keep an eye on the girls.': 'Bobby… Ty i twoi ludzie miejcie oko na dziewczyny.',
    'Father… We should find Erica… If she’s here.': 'Ojcze… Powinniśmy znaleźć Ericę… jeśli tu jest.',
    'Go to the altar… I will find the Toma.': 'Idź do ołtarza… Ja znajdę Tomę.',
    'Shouldn’t you have help?': 'Nie powinieneś wziąć kogoś do pomocy?',
    'A couple of treasure hunters could come in handy…': 'Kilku łowców skarbów mogłoby się przydać…',
    'Henry and Diana… Care to accompany me?': 'Henry, Diana… Pójdziecie ze mną?',
    'I’ll do what I can.': 'Zrobię, co w mojej mocy.',
    'Why not… Seems like a fine way to die.': 'Czemu nie… To chyba niezły sposób na śmierć.',
    'I’m coming with you, 1Hero.': 'Idę z tobą, 1Hero.',
    'Let’s save Erica.': 'Uratujmy Ericę.',
    'I’m going with Dad.': 'Idę z tatą.',
    'Stay put, young lady.': 'Zostań tutaj, młoda damo.',
    'Keep an eye on the rift, Tasha. It’s on you to fuck up Lillian if she causes trouble.': 'Miej oko na szczelinę, Tasha. Jeśli Lillian zacznie sprawiać kłopoty, masz ją rozwalić.',
    'If Lilith gives us any trouble, I’ll shoot her.': 'Jeśli Lilith będzie sprawiać kłopoty, zastrzelę ją.',
    'But we’re already in Hell… I don’t know what will happen.': 'Ale jesteśmy już w Piekle… Nie wiem, co się stanie.',
    'Who cares? I’ll still shoot her.': 'Kogo to obchodzi? I tak ją zastrzelę.',
    'Are we going to get attacked or not? I can’t stand waiting.': 'Zaatakują nas w końcu, czy nie? Nie znoszę czekać.',
    "Rinaldi wants us going back into the mansion... I don't know which is worse, here or there.": 'Rinaldi chce, żebyśmy wrócili do rezydencji… Nie wiem, co gorsze: tam czy tutaj.',
    'I don’t want to die here.': 'Nie chcę tu umierać.',
    "We'll check on the mansion and make sure it's safe before we let the girls leave.": 'Sprawdzimy rezydencję i upewnimy się, że jest bezpieczna, zanim pozwolimy dziewczynom wyjść.',
    'I take it that Erica is safe.': 'Rozumiem, że Erica jest bezpieczna.',
    'We’re just waiting for Lilith.': 'Czekamy tylko na Lilith.',
    'Is this Hell? It can’t be… right?': 'Czy to Piekło? To niemożliwe… prawda?',
    'This is the most terrifying place I’ve ever seen!': 'To najbardziej przerażające miejsce, jakie widziałam!',
    'You think they have farms in Hell? What would they farm?': 'Myślisz, że w Piekle są farmy? Co mogliby tam uprawiać?',
    'That bomb looks dangerous… This whole place looks dangerous.': 'Ta bomba wygląda groźnie… Całe to miejsce jest niebezpieczne.',
    'The mansion is collapsing. We have to be careful.': 'Rezydencja się wali. Musimy uważać.',
    'Canmore? Rinaldi?': 'Canmore? Rinaldi?',
    'What’s the status?': 'Jaka sytuacja?',
    'Is the mansion safe?': 'Czy rezydencja jest bezpieczna?',
    'It appears to have stabilized… The earthquakes are gone.': 'Wygląda na to, że się ustabilizowała… Trzęsienia ziemi ustały.',
    'Everyone, back to the mansion!': 'Wszyscy wracać do rezydencji!',
    'We’re not done here.': 'Jeszcze nie skończyliśmy.',
    'I’ll find Erica. Everyone else, go inside.': 'Znajdę Ericę. Reszta do środka.',
    'Diana… Make sure Duncan doesn’t escape. I’m going with 1Hero.': 'Diana… Dopilnuj, żeby Duncan nie uciekł. Idę z 1Hero.',
    'Don’t die for this, Henry.': 'Nie zgiń przez to, Henry.',
    'I’m going with 1Hero too!': 'Ja też idę z 1Hero!',
    'Oh no, you’re not!': 'O nie, nie pójdziesz!',
    'Come on, everyone! We have to go!': 'No dalej, wszyscy! Musimy iść!',
    'Lillian?': 'Lillian?',
    'She’s hurt.': 'Jest ranna.',
    '1Hero… Where is the Toma? Where is Daemalius?': '1Hero… Gdzie jest Toma? Gdzie Daemalius?',
    'It’s gone… We destroyed it.': 'Zniknęło… Zniszczyliśmy je.',
    'The priest is holding off Daemalius. We need to get out of here.': 'Kapłan powstrzymuje Daemaliusa. Musimy się stąd wydostać.',
    'You must destroy the rift… You have to trap Daemalius here.': 'Musisz zniszczyć szczelinę… Musisz uwięzić tu Daemaliusa.',
    'Where is Brian?': 'Gdzie jest Brian?',
    'Father Solomon! We can’t leave without him.': 'Ojcze Solomon! Nie możemy go zostawić.',
    'What are you doing, Mother?': 'Co robisz, Matko?',
    'We’re not going anywhere until you tell us why the Toma Leolo is in pieces!': 'Nigdzie nie idziemy, dopóki nie powiesz nam, dlaczego Toma Leolo jest rozbity na kawałki!',
    'That is not your concern!': 'To nie twoja sprawa!',
    'It was our ticket out of here and now it’s gone!': 'To była nasza przepustka stąd, a teraz przepadła!',
    'I’m scared!': 'Boję się!',
    'Run! I’ll wait for the priest!': 'Uciekajcie! Zaczekam na kapłana!',
    'Shit… I’ll come back!': 'Cholera… Wrócę!',
    'Just go!': 'Uciekaj!',
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
        or context.get('map_id') != 151
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
    raise SystemExit('Unmapped Map 151 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 192:
    raise SystemExit(f'Expected exactly 192 natural dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 151 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
