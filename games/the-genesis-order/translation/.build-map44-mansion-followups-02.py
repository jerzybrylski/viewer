#!/usr/bin/env python3
"""Build Polish drafts for Map 44 follow-ups."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map44-mansion-followups-02.jsonl'
TRANSLATIONS = {
    "Wow. An impressive looking room.": "Wow. Imponująco wyglądający pokój.",
    "Don’t act so surprised, 1Hero. You’ve seen it before.": "Nie udawaj takiego zdziwionego, 1Hero. Już tu byłeś.",
    "Oh, uh…": "Och, yyy…",
    "We have time before dinner. I’d love to chat before the food is ready.": "Mamy czas przed kolacją. Chętnie porozmawiam, zanim jedzenie będzie gotowe.",
    "Uh, sure.": "Yyy, jasne.",
    "Everyone, get underground! Now!": "Wszyscy, pod ziemię! Już!",
    "I feel safer knowing I have the police guarding my home. But I can’t help but worry about my father’s reputation if people find out what’s going on.": "Czuję się bezpieczniej, wiedząc, że policja pilnuje domu. Ale nie mogę nie martwić się o reputację ojca, jeśli ludzie dowiedzą się, co się dzieje.",
    "Your safety is the most important thing now. Your father’s past may not be able to remain hidden forever.": "Twoje bezpieczeństwo jest teraz najważniejsze. Przeszłości twojego ojca nie da się ukrywać wiecznie.",
    "If you find another secret passage, I want to see it.": "Jeśli znajdziesz kolejne tajne przejście, chcę je zobaczyć.",
    "I’ve got the key, but I don’t know what it opens.": "Mam klucz, ale nie wiem, co otwiera.",
    "It’s got to be something outside.": "To musi być coś na zewnątrz.",
    "You’re very observant, Erica.": "Jesteś bardzo spostrzegawcza, Erica.",
    "Would I make a good detective?": "Nadawałabym się na detektywa?",
    "Come on, let’s go outside and take a look.": "Chodź, wyjdźmy na zewnątrz i poszukajmy.",
    "We can’t go far. The forest behind the mansion is very dense.": "Nie możemy zajść daleko. Las za rezydencją jest bardzo gęsty.",
    "So, what’s the plan?": "No to jaki jest plan?",
    "Go in there and get them to move away from the kitchen hall.": "Wejdź tam i spraw, żeby odeszli od korytarza przy kuchni.",
    "I didn’t think that far ahead… Just… Waggle your butt.": "Nie pomyślałam tak daleko… Po prostu… Pokręć tyłkiem.",
    "Just try something.": "Po prostu coś spróbuj.",
    "Ugh… Can you make a scene? Fall down or something?": "Ugh… Możesz zrobić scenę? Przewrócić się czy coś?",
    "You know… Those leper dudes almost blew their lids last time I tried to spruce this place up with flowers.": "Wiesz… Ci kolesie w maskach prawie eksplodowali, gdy ostatnio próbowałam ozdobić to miejsce kwiatami.",
    "They don’t like flowers?": "Nie lubią kwiatów?",
    "No… It’s the candles… Apparently the yellow flower I wanted to put in the room was a fire hazard.": "Nie… Chodzi o świece… Podobno żółty kwiat, który chciałam wstawić, był zagrożeniem pożarowym.",
    "Bingo!": "Bingo!",
    "They are talking about the Acacia flower… Its oils are highly flammable.": "Mówią o kwiecie akacji… Jego olejki są wysoce łatwopalne.",
    "So… How does that help us?": "Więc… jak nam to pomoże?",
    "Start a fire.": "Wznieć ogień.",
    "Are you crazy!?": "Zwariowałaś!?",
    "Just a small one. They’ll have to react to it.": "Tylko mały. Będą musieli zareagować.",
    "That’ll make quite the commotion.": "To wywoła spore zamieszanie.",
    "We only need a small fire. You three can handle it.": "Potrzebujemy tylko małego ognia. Wy troje dacie radę.",
    "Okay. If you think it’ll work.": "Dobrze. Jeśli myślisz, że zadziała.",
    "It grows in the forest near water sources. I’ll see if I can find one.": "Rośnie w lesie blisko źródeł wody. Zobaczę, czy znajdę jedną.",
    "Did you find the flower in the forest?": "Znalazłeś kwiat w lesie?",
    "Not yet. Give me a minute.": "Jeszcze nie. Daj mi chwilę.",
    "Here. I’ve got the flower.": "Proszę. Mam kwiat.",
    "So... What should I do?": "Więc... Co mam zrobić?",
    "Get a little too close to the candles and touch them to the fire…": "Podejdź odrobinę za blisko świec i dotknij ich ogniem…",
    "Then throw it to the ground so you don’t get burnt.": "Potem rzuć go na ziemię, żeby się nie poparzyć.",
    "What if it doesn’t work?": "A jeśli nie zadziała?",
    "It’ll work.": "Zadziała.",
    "Okay. Here goes nothing.": "Dobra. To nic, próbujemy.",
    "What do you need? This area is already clean.": "Czego potrzebujesz? Tu już jest czysto.",
    "Are you sure? Maybe I should check.": "Na pewno? Może powinnam sprawdzić.",
    "Hey! Wait just a minute!": "Hej! Zaczekaj chwilę!",
    "I know where the food storage is. I’ll get this mystery eyeball thing and you start looking for something out of place.": "Wiem, gdzie jest spiżarnia. Wezmę tę tajemniczą gałkę oczną, a ty zacznij szukać czegoś niepasującego.",
    "Out of place? This whole mansion is filled with odd-looking things.": "Niepasującego? Cała rezydencja jest pełna dziwnych rzeczy.",
    "Just wait here and try not to get seen.": "Po prostu zostań tu i postaraj się nie zostać zauważonym.",
    "These statues make no sense. They’ve been placed on top of the carpet…": "Te posągi nie mają sensu. Postawiono je na dywanie…",
    "Something is off.": "Coś jest nie tak.",
    "This sure is a heavy statue. I can’t move it with my hands.": "Ten posąg jest naprawdę ciężki. Nie przesunę go rękami.",
    "Try not to look suspicious, 1Hero…": "Staraj się nie wyglądać podejrzanie, 1Hero…",
    "The old man could come back at any moment.": "Stary może wrócić w każdej chwili.",
    "Can we trust him?": "Czy możemy mu ufać?",
    "Could I trust any of you?": "Czy ja mogę ufać któremukolwiek z was?",
    "There’s going to be a hell of a lot of officers coming down on this mansion if you’re hiding something.": "Zjedzie tu mnóstwo funkcjonariuszy, jeśli coś ukrywasz.",
    "There is nothing to fear, 1Hero.": "Nie masz się czego bać, 1Hero.",
    "Not surprised, are you?": "Nie jesteś zaskoczony, prawda?",
    "I’ve seen a lot, Lillian.": "Wiele widziałem, Lillian.",
    "What are you two standing around for? Go find the girl.": "Co tak stoicie? Idźcie szukać dziewczyny.",
    "Leave, 1Hero. And stay away.": "Odejdź, 1Hero. I trzymaj się z daleka.",
    "I’m not leaving Kimberly inside that rift.": "Nie zostawię Kimberly w tym pęknięciu.",
    "I’ll send some men down there to retrieve her. She’ll be returned safely.": "Wyślę tam ludzi, żeby ją sprowadzili. Wróci cała i zdrowa.",
    "That won’t work. She’s not in our world.": "To nie zadziała. Ona nie jest w naszym świecie.",
    "She’s in the basement, 1Hero.": "Jest w piwnicy, 1Hero.",
    "We’ll stop Madalyn. This doesn’t concern you.": "Zatrzymamy Madalyn. To nie twoja sprawa.",
    "Leave before Duncan comes back.": "Odejdź, zanim wróci Duncan.",
    "Try and keep everyone away from here. I don’t know how long it’ll take.": "Postaraj się trzymać wszystkich z dala. Nie wiem, ile to potrwa.",
    "Huh? I’m coming with you.": "Co? Idę z tobą.",
    "No, you’re not!": "Nie idziesz!",
    "Why would you?": "Po co?",
    "You don’t. Trust me.": "Nie ufasz. Zaufaj mi.",
    "No fair!": "To niesprawiedliwe!",
    "Just… Give us time. Keep Duncan’s men away from us.": "Po prostu… daj nam czas. Trzymaj ludzi Duncana z daleka.",
    "Thanks, Nellie.": "Dzięki, Nellie.",
    "A pleasant surprise.": "Miła niespodzianka.",
    "Maybe you’ll get off my ass about the last amulet.": "Może wreszcie odpuścisz mi ten ostatni amulet.",
    "Are those rock pieces valuable?": "Czy te kawałki skał są cenne?",
    "More than you can imagine, young man.": "Bardziej, niż możesz sobie wyobrazić, młody człowieku.",
    "Shit. Duncan’s here and he’s given Madalyn the Toma pieces.": "Cholera. Duncan już tu jest i oddał Madalyn kawałki Tomy.",
    "I doubt we can take them… And even if we could… Andrea would be pissed.": "Wątpię, byśmy dali im radę… A nawet gdyby… Andrea byłaby wściekła.",
    "Who cares about Duncan? We can take down Madalyn…": "Kto by się przejmował Duncanem? Możemy dopaść Madalyn…",
    "We just need to wait until she’s alone.": "Musimy tylko poczekać, aż zostanie sama.",
    "Maybe this was a mistake.": "Może to był błąd.",
    "I know where she’s going… As soon as they leave, we need to get down there.": "Wiem, dokąd idzie… Gdy tylko wyjdą, musimy zejść na dół.",
    "Come on. Let’s hide.": "Chodź. Schowajmy się.",
    "1Hero!?": "1Hero!?",
    "Nellie!?": "Nellie!?",
    "She’s with us.": "Jest z nami.",
    "No time to explain.": "Nie ma czasu na tłumaczenia.",
    "A secret chamber?": "Tajna komnata?",
    "Hell no!... What’s down there?": "Nie ma mowy!... Co tam jest na dole?",
    "Argh! Come back!": "Argh! Wracaj!",
    "Nellie!?...": "Nellie!?...",
    "Rawr!": "Rarrr!",
    "Let’s get out of here!": "Wynośmy się stąd!",
    "Come on, 1Hero. You can help me look for her.": "Chodź, 1Hero. Możesz pomóc mi jej szukać.",
    "She went into the rift. I don’t know how to open it.": "Weszła w pęknięcie. Nie wiem, jak je otworzyć.",
    "I might remember how.": "Może pamiętam, jak.",
    "How the hell would she know how to do that?": "Skąd ona, do cholery, miałaby wiedzieć, jak to zrobić?",
    "I thought I heard a scuffle.": "Zdawało mi się, że słyszałem szamotaninę.",
    "I didn’t hear anything… But I’ll keep an eye out.": "Nic nie słyszałem… Ale będę miał oko.",
    "It’s Melissa!": "To Melissa!",
    "Where’s Duncan?": "Gdzie jest Duncan?",
    "Madalyn is here!": "Madalyn tu jest!",
    "How many of those henchmen are left?": "Ilu tych pachołków jeszcze zostało?",
    "That should be all of them.": "To powinni być wszyscy.",
    "You’re lucky you’re a woman.": "Masz szczęście, że jesteś kobietą.",
    "And why’s that?": "Dlaczego?",
    "Your soul is safe.": "Twoja dusza jest bezpieczna.",
    "What the hell do you want?": "Czego, do cholery, chcesz?",
    "An army, my dear…": "Armii, moja droga…",
    "Duncan Helmer made a deal.": "Duncan Helmer zawarł układ.",
    "You’re relying on him for more men?": "Liczysz, że dostarczy ci więcej ludzi?",
    "Your prize awaits you, my children.": "Nagroda na was czeka, moje dzieci.",
    "Did that door just shut? Was that Nellie? Is someone else in here?": "Czy te drzwi się właśnie zamknęły? To była Nellie? Jest tu ktoś jeszcze?",
    "Judy!?": "Judy!?",
    "Father! What is happening?": "Ojcze! Co się dzieje?",
    "All the girls are here.": "Wszystkie dziewczyny tu są.",
    "I have to go back for the others.": "Muszę wrócić po pozostałe.",
    "It’s safe underground…": "Na dole jest bezpiecznie…",
    "Judy, come with me.": "Judy, chodź ze mną.",
    "Yes, Father.": "Tak, ojcze.",
    "Go down these steps. You’ll be safe.": "Zejdź po tych schodach. Będziesz bezpieczna.",
    "Go rescue the others!": "Idź ratować pozostałe!"
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
        or context.get('map_id') != 44
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
    raise SystemExit('Unmapped Map 44 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 125:
    raise SystemExit(f'Expected exactly 125 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 44 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
