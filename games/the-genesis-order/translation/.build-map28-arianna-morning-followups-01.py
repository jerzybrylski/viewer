#!/usr/bin/env python3
"""Build Polish drafts for the remaining Arianna/home dialogue on Map 28."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
EVENTS = {
    5: {
        "Alright. I’ve got a lot on my plate today. I need to get to the station.": "Dobrze. Mam dziś mnóstwo spraw na głowie. Muszę jechać na komisariat.",
    },
    6: {
        "Good morning, sleepyhead.": "Dzień dobry, śpiochu.",
        "Arianna?...": "Arianna?...",
        "You sure do like to sleep.": "Naprawdę lubisz sobie pospać.",
        "Hannah is going to be pissed!": "Hannah będzie wściekła!",
        "Don’t worry. She’ll be there when you get to the farm.": "Nie martw się. Będzie na farmie, kiedy tam dotrzesz.",
        "Damn. I hate to keep brushing off Heather.": "Cholera. Nie znoszę, że ciągle zbywam Heather.",
        "She’s been asking me to work out with her for months now.": "Od miesięcy prosi, żebym z nią poćwiczył.",
        "What’s wrong, 1Hero? Do you need training?": "Coś nie tak, 1Hero? Potrzebujesz treningu?",
        "I think I’m in pretty good shape.": "Chyba jestem całkiem nieźle zbudowany.",
        "That woman loves you very much. You should spend time with her.": "Ta kobieta bardzo cię kocha. Powinieneś spędzać z nią więcej czasu.",
        "She loves me?": "Ona mnie kocha?",
        "She bought you this house. No?": "Kupiła ci ten dom, prawda?",
        "Well… She helped me buy it…": "Cóż… Pomogła mi go kupić…",
        "You’re right. I should spend more time with her.": "Masz rację. Powinienem spędzać z nią więcej czasu.",
        "She’s been there for me through everything.": "Zawsze była przy mnie, cokolwiek się działo.",
        "I sense she’s been close with you for a long time.": "Czuję, że od dawna jesteście sobie bliscy.",
        "She helped me through some hard times when I was a kid.": "Pomogła mi przetrwać trudne chwile, kiedy byłem dzieckiem.",
        "You’re lucky to have people close to you.": "Masz szczęście, że masz bliskich.",
        "I just get so obsessed with work… I tend to neglect my relationships.": "Tak pochłania mnie praca… Zaniedbuję przez to relacje z bliskimi.",
        "Speaking of work… I need to meet that Tasha girl.": "Skoro mowa o pracy… Muszę spotkać się z tą Tashą.",
        "If she can get me some good info on Madalyn, maybe I can impress Melissa and she’ll let me reopen the case.": "Jeśli zdobędzie dla mnie jakieś informacje o Madalyn, może zaimponuję Melissie i pozwoli mi wznowić śledztwo.",
        "Your spirit for this case is a blessing and curse.": "Twoje zaangażowanie w tę sprawę jest i błogosławieństwem, i przekleństwem.",
        "Sounds like you’ve figured me out, Arianna.": "Wygląda na to, że mnie rozgryzłaś, Arianno.",
        "You should be glad I’m here to help you.": "Powinieneś się cieszyć, że jestem tu, by ci pomóc.",
        "You’ve got a big day ahead of you. Better get out there.": "Czeka cię ważny dzień. Lepiej ruszaj.",
        "Wake up, 1Hero.": "Obudź się, 1Hero.",
        "Ugh… I’m still tired.": "Ugh… Wciąż jestem zmęczony.",
        "The sun has been up for many hours.": "Słońce wstało już wiele godzin temu.",
        "Oh, shit! I’m late for work!": "O cholera! Spóźnię się do pracy!",
        "You were up very late. How long did you spend in that cave?": "Długo siedziałeś w nocy. Ile czasu spędziłeś w tej jaskini?",
        "No time to explain, Arianna. I’ve got to get to work.": "Nie ma czasu na wyjaśnienia, Arianno. Muszę jechać do pracy.",
        "Better hurry, 1Hero. Your fate requires it.": "Pospiesz się, 1Hero. Taki jest twój los.",
        "You’re up early today, 1Hero.": "Dziś wcześnie wstałeś, 1Hero.",
        "Time to impress the boss.": "Pora zaimponować szefowej.",
        "I also need to warn Lillian about Madalyn… But first thing’s first.": "Muszę też ostrzec Lillian przed Madalyn… Ale najpierw najważniejsze.",
        "Don’t be late, 1Hero.": "Nie spóźnij się, 1Hero.",
        "Time for work, sleepyhead.": "Pora do pracy, śpiochu.",
        "I’ve got something to share with my boss…": "Mam coś do powiedzenia szefowej…",
        "I managed to open a safe in the church.": "Udało mi się otworzyć sejf w kościele.",
        "You think she’ll be impressed?": "Myślisz, że jej zaimponuję?",
        "She’ll never show it. She’s got a stick up her ass.": "Nigdy tego nie okaże. Jest sztywna jak kij od szczotki.",
        "Oh, dear! How painful.": "Ojej! Jakie to bolesne.",
        "I should have seen that coming.": "Mogłem się tego spodziewać.",
        "1Hero, you better hurry and get to work.": "1Hero, lepiej pospiesz się do pracy.",
        "Why? I’m not running late.": "Po co? Nie spóźnię się.",
        "I can sense a strong focus on your energy coming from the station.": "Czuję, że z komisariatu emanuje silna energia skupiona na tobie.",
        "Everyone’s thinking about you… and it’s not good!": "Wszyscy o tobie myślą… i nie są to dobre myśli!",
        "Fine. Fine. I’ll hurry.": "Dobra, dobra. Pospieszę się.",
    },
    9: {
        "I’m bored, 1Hero. I’m going home.": "Nudzę się, 1Hero. Wracam do domu.",
        "So… Are we going to do anything?": "No więc… Zamierzamy coś zrobić?",
        "I’ve got other things I could be doing. What’s your plan?": "Mógłbym teraz robić wiele innych rzeczy. Jaki masz plan?",
        "There’s a lot to do on the farm. I better get going.": "Na farmie jest mnóstwo do zrobienia. Lepiej już pójdę.",
        "I don’t often leave the mansion. Why have you invited me here if you have no plans?": "Rzadko opuszczam rezydencję. Po co mnie tu zaprosiłeś, skoro nic nie zaplanowałeś?",
        "This is a nice room, but perhaps I should get back to the church now.": "To ładny pokój, ale chyba powinnam już wrócić do kościoła.",
        "I can’t just linger around. What the hell is there to do here?": "Nie mogę tak bezczynnie siedzieć. Co tu, do cholery, można robić?",
        "I’m a busy woman. How long is this going to take?": "Jestem zajętą kobietą. Ile to jeszcze potrwa?",
        "This is ridiculous. I’m not waiting around here.": "To niedorzeczne. Nie będę tu czekać.",
        "What exactly are we doing here?": "Co właściwie tu robimy?",
        "Uhhh… What’s going on?": "Yyy… Co się dzieje?",
        "A lovely room, but I should get going.": "Pokój jest śliczny, ale powinnam już iść.",
    },
    10: {
        "Judy… It’s morning.": "Judy… Już rano.",
        "I had a wonderful time last night…": "Wspaniale się bawiłam zeszłej nocy…",
        "But I worry about Chloe.": "Ale martwię się o Chloe.",
        "She should be coming over here soon.": "Niedługo powinna tu przyjść.",
        "I feel bad for scaring her.": "Źle się czuję, że ją przestraszyłam.",
        "It’s not your fault. We should have been more careful with our plans last night.": "To nie twoja wina. Powinniśmy byli lepiej zaplanować wczorajszy wieczór.",
        "I bet that’s her.": "Założę się, że to ona.",
        "I better get dressed.": "Lepiej się ubiorę.",
    },
    13: {
        "Shit? Is that Heather?": "Cholera, to Heather?",
        "Another girlfriend?": "Kolejna dziewczyna?",
        "No, no… Just wait here.": "Nie, nie… Zaczekaj tutaj.",
    },
    19: {
        "There’s no place I’d rather be in a thunderstorm than here with you, 1Hero.": "Podczas takiej burzy nie chciałabym być nigdzie indziej niż tutaj, z tobą, 1Hero.",
        "You’re adorable, Sister Judy.": "Jesteś urocza, siostro Judy.",
        "You can just call me Judy.": "Mów mi po prostu Judy.",
        "It’s fixed!": "Naprawione!",
        "Yeah. It was just a fuse.": "Tak. To był tylko bezpiecznik.",
        "I must say, it would have been very cozy to spend the night under candle light.": "Muszę przyznać, że noc przy świecach byłaby bardzo romantyczna.",
        "There’s no reason we couldn’t still light a few candles.": "Nic nie stoi na przeszkodzie, żebyśmy i tak zapalili kilka świec.",
        "We can pretend the lights are out!": "Możemy udawać, że nie ma prądu!",
        "Haha. Or we can turn the lights off.": "Haha. Albo po prostu zgasić światło.",
        "Even better!": "Jeszcze lepiej!",
    },
    20: {
        "The power’s gone out.": "Wyłączyli prąd.",
        "Stay here. I’ll check on it.": "Zostań tutaj. Sprawdzę, co się stało.",
    },
    22: {
        "Damn! That weather is getting really bad.": "Cholera! Pogoda robi się naprawdę paskudna.",
        "Thank you, 1Hero. I’m so glad I met you.": "Dziękuję, 1Hero. Tak się cieszę, że cię poznałam.",
        "Well… I’m certainly making your life more exciting.": "Cóż… Z pewnością urozmaicam ci życie.",
        "Anything you’d like to do before bed?": "Chcesz coś zrobić przed snem?",
        "Maybe…": "Może…",
    },
    23: {
        "Mother Superior!": "Matko przełożona!",
        "Madalyn!": "Madalyn!",
        "I thought this would be much more difficult.": "Myślałam, że będzie znacznie trudniej.",
        "What did you do to Sister Judy?": "Co zrobiłaś siostrze Judy?",
        "Haha. And you believe it was the nun whom I was influencing…": "Haha. Naprawdę sądzisz, że wpływałam na zakonnicę…",
        "No, my dear. It was you who needed the push. The woman was ready to break her vow.": "Nie, kochana. To ty potrzebowałaś zachęty. Ona była gotowa złamać śluby.",
        "What have I done!?": "Co ja zrobiłam!?",
        "You were chosen, Sister. But you have fallen. The damned will be saved and you will not stop me.": "Zostałaś wybrana, siostro, ale upadłaś. Potępieni zostaną zbawieni, a ty mnie nie powstrzymasz.",
        "I don’t know what you mean.": "Nie wiem, o czym mówisz.",
        "Don’t act stupid, Sister! You were chosen by the angel of God.": "Nie udawaj głupiej, siostro! Zostałaś wybrana przez anioła Bożego.",
        "You’re wrong, Madalyn.": "Mylisz się, Madalyn.",
        "Time’s up, my dear.": "Twój czas minął, kochana.",
        "She was using a piece of the Toma statue!": "Używała fragmentu posągu Toma!",
        "Shit! Duncan has the other pieces…": "Cholera! Duncan ma pozostałe fragmenty…",
        "That means they have all six pieces!": "To znaczy, że mają już wszystkie sześć fragmentów!",
        "What will happen?": "Co się stanie?",
        "I don’t know… Lillian says the Toma Leolo will save the worlds of chaos.": "Nie wiem… Lillian mówi, że Toma Leolo ocali światy chaosu.",
        "I have to go to the cathedral. I have to tell Father Solomon.": "Muszę iść do katedry. Muszę powiedzieć ojcu Solomonowi.",
        "But the storm… and it’s so late.": "Ale ta burza… I jest już tak późno.",
        "Stay here… I’m going to the mansion.": "Zostań tutaj… Jadę do rezydencji.",
        "I thought you were going to the cathedral.": "Myślałam, że jedziesz do katedry.",
        "Father Solomon and I will face Lillian…": "Ojciec Solomon i ja zmierzymy się z Lillian…",
        "Don’t worry. I’ll put an end to this.": "Nie martw się. Położę temu kres.",
        "Father is a good man. He can help you.": "Ojciec to dobry człowiek. Może ci pomóc.",
        "I believe in him.": "Wierzę w niego.",
        "Everything’s going to be okay. I promise.": "Wszystko będzie dobrze. Obiecuję.",
    },
    25: {
        "Father Solomon can help you. He is a good man.": "Ojciec Solomon może ci pomóc. To dobry człowiek.",
        "Father and I will figure out what’s going on. Madalyn won’t hurt you anymore.": "Ojciec i ja dowiemy się, co się dzieje. Madalyn już więcej cię nie skrzywdzi.",
        "I will pray for us both.": "Będę się modlić za nas oboje.",
    },
    26: {
        "1Hero, it’s morning.": "1Hero, już rano.",
        "Ugh… I stayed up too late last night.": "Ugh… Wczoraj siedziałem do późna.",
        "The storm has passed. The sun is shining.": "Burza minęła. Świeci słońce.",
        "Shit. I need to get to work… Andrea is expecting me.": "Cholera. Muszę iść do pracy… Andrea na mnie czeka.",
        "Is it safe to go back to the cathedral? It sounds like you had quite the adventure last night.": "Czy w katedrze jest już bezpiecznie? Wygląda na to, że zeszłej nocy przeżyłeś niezłą przygodę.",
        "I’m going to talk to the commissioner. She’ll help us make sure it’s safe.": "Porozmawiam z panią komisarz. Pomoże nam sprawdzić, czy jest bezpiecznie.",
        "Someone’s at the door.": "Ktoś jest przy drzwiach.",
    },
    54: {
        "Arianna!": "Arianna!",
        "1Hero! I didn’t know what to do!": "1Hero! Nie wiedziałam, co robić!",
        "It’s alright. You got the laptop?": "W porządku. Masz laptopa?",
        "This strange device? Yes, I got it.": "To dziwne urządzenie? Tak, mam je.",
        "That’s something, at least. What happened?": "Przynajmniej tyle. Co się stało?",
        "I don’t know! I tried to leave the Oracle, but I couldn’t!": "Nie wiem! Próbowałam opuścić Wyrocznię, ale nie mogłam!",
        "I kept trying… but when I was able to get out, a strange man was there!": "Próbowałam dalej… A kiedy w końcu się wydostałam, stał tam jakiś dziwny mężczyzna!",
        "He started yelling at me when I appeared.": "Zaczął na mnie krzyczeć, kiedy się pojawiłam.",
        "So I grabbed the device and left.": "Więc chwyciłam urządzenie i uciekłam.",
        "I didn’t know what else to do.": "Nie wiedziałam, co innego mogę zrobić.",
        "You were stuck?... That’s weird.": "Utknęłaś?... Dziwne.",
        "Have you ever had that problem before?": "Zdarzyło ci się to wcześniej?",
        "Never!": "Nigdy!",
        "Now that I think about it, I usually have the Oracle with me.": "Jak się nad tym zastanowić, zazwyczaj mam przy sobie Wyrocznię.",
        "Does it have to be opened by someone?": "Ktoś musi ją otworzyć?",
        "Well… someone has always been there before when I’ve come out of the Oracle.": "Cóż… Zawsze ktoś tam był, gdy wychodziłam z Wyroczni.",
        "Whatever happened, we now have to deal with the fact that Arianna removed evidence right in front of the police commissioner.": "Cokolwiek się stało, musimy teraz zająć się tym, że Arianna zabrała dowód na oczach komisarza policji.",
        "Am I in trouble?": "Mam kłopoty?",
        "Running off with the laptop right in front of him was definitely not good.": "Ucieczka z laptopem sprzed samego nosa komisarza zdecydowanie nie pomogła.",
        "But as long as you don’t let the commissioner see you again, it’ll be fine.": "Ale jeśli komisarz cię więcej nie zobaczy, wszystko będzie dobrze.",
        "Our problem now is that we have to return it without getting caught.": "Teraz musimy go zwrócić, nie dając się złapać.",
        "I could just teleport right now and put it back.": "Mogłabym się teraz teleportować i odłożyć go na miejsce.",
        "That’s not a good idea. The station will be on high alert now.": "To zły pomysł. Komisariat jest teraz w stanie najwyższej gotowości.",
        "What about you? Just tell them you recovered it.": "A ty? Po prostu powiedz, że go odzyskałeś.",
        "No way. They’ll definitely think I was involved. It’s simply too suspicious.": "Nie ma mowy. Na pewno pomyślą, że byłem w to zamieszany. To zbyt podejrzane.",
        "I’ll do it. It’s my fault, so I’ll fix it.": "Ja to zrobię. To moja wina, więc to naprawię.",
        "Now that I’ve been there, it’s no problem to go back.": "Skoro już tam byłam, powrót nie będzie problemem.",
        "It will be risky.": "To będzie ryzykowne.",
        "I’m a demon. What are they going to do?": "Jestem demonem. Co mi zrobią?",
        "She makes a good point.": "Ma rację.",
        "The laptop...": "Laptop…",
        "It’s done.": "Gotowe.",
        "All you need to do is put it back where you found it.": "Musisz tylko odłożyć go tam, gdzie go znalazłaś.",
        "I can do that!": "Dam radę!",
        "Make sure you’re not seen.": "Uważaj, żeby nikt cię nie zobaczył.",
        "I know what to do. I have a plan.": "Wiem, co robić. Mam plan.",
        "A plan? Shit… I can already tell this will end badly.": "Plan? Cholera… Już widzę, że źle się to skończy.",
        "Hope your girl knows what she’s doing.": "Oby twoja dziewczyna wiedziała, co robi.",
        "I can’t teleport directly back to the office… The crazy man might see me again.": "Nie mogę teleportować się prosto z powrotem do biura… Ten szaleniec mógłby znów mnie zobaczyć.",
        "I have to carefully make my way back and make sure no one’s inside.": "Muszę ostrożnie wrócić i sprawdzić, czy nikogo nie ma w środku.",
    },
    59: {
        "I knew you could. Never a doubt in my mind.": "Wiedziałem, że dasz radę. Ani przez chwilę w ciebie nie wątpiłem.",
        "Heh… Of course.": "Heh… Oczywiście.",
        "Thank you both. Now I can return to Cape Vedra without looking over my shoulder.": "Dziękuję wam obojgu. Teraz mogę wrócić do Cape Vedra, nie oglądając się za siebie.",
        "Happy to help!": "Chętnie pomogliśmy!",
        "So heading back to Cape Vedra?": "Czyli wracasz do Cape Vedra?",
        "Not just yet. Henry and I will soon be joining a dear friend of ours on her treasure hunt.": "Jeszcze nie. Wkrótce z Henrym dołączymy do naszej drogiej przyjaciółki i jej poszukiwań skarbów.",
        "That sounds exciting.": "Brzmi ekscytująco.",
        "What’s the treasure?": "Jaki skarb?",
        "Sorry, I can’t disclose the details.": "Wybacz, nie mogę zdradzić szczegółów.",
        "Oh, I didn’t mean to pry. But guiding people is in my nature.": "Och, nie chciałam być wścibska. Po prostu mam w naturze pomagać innym znaleźć drogę.",
        "It would be nice having you around, but I think we can handle it.": "Miło byłoby mieć cię przy sobie, ale chyba sobie poradzimy.",
        "Thanks again for all your help.": "Jeszcze raz dziękujemy za całą twoją pomoc.",
        "You are most welcome!": "Cała przyjemność po mojej stronie!",
        "You too, 1Hero.": "Tobie również, 1Hero.",
        "Glad to assist, and don’t be a stranger.": "Cieszę się, że mogłem pomóc. Nie zapominaj o nas.",
        "I’m sure we’ll meet again.": "Na pewno jeszcze się spotkamy.",
        "1Hero, I have a surprise. The laptop wasn’t the only thing I found in the commissioner’s office.": "1Hero, mam niespodziankę. Laptop nie był jedyną rzeczą, którą znalazłam w gabinecie komisarza.",
        "You took something else?": "Zabrałaś coś jeszcze?",
        "A love potion.": "Eliksir miłosny.",
        "Hahaha.": "Hahaha.",
        "I’m going to try it!": "Wypróbuję go!",
        "This could be interesting.": "To może być ciekawe.",
        "So? How do you feel?": "No i? Jak się czujesz?",
        "I… I don’t know. What should I be feeling?": "Ja… Nie wiem. Co powinnam czuć?",
        "Warm, maybe hot? And very, very horny.": "Ciepło, może gorąco? I wielką, wielką ochotę na seks.",
        "Hmph. That’s not how I feel at all.": "Hmph. Wcale się tak nie czuję.",
        "You’re a demon. It might not work on demons.": "Jesteś demonem. Może eliksir nie działa na demony.",
        "Oh, phooey.": "Och, do licha.",
        "So much for that idea.": "No i nici z tego pomysłu.",
        "You don’t need any liquid motivation.": "Nie potrzebujesz płynnej zachęty.",
    },
    60: {
        "Oh no, 1Hero. The heat is not so bad now, yet I still feel something when I look at you.": "O nie, 1Hero. Żar już nie jest tak silny, a mimo to coś czuję, kiedy na ciebie patrzę.",
        "Perhaps being a demon means I can never be satisfied.": "Może bycie demonem oznacza, że nigdy nie zaznam spełnienia.",
        "Lust isn’t a bad thing.": "Pożądanie nie jest niczym złym.",
        "I don’t know… This feeling isn’t…": "Nie wiem… To uczucie nie jest…",
        "It’s not just about sex.": "Tu nie chodzi tylko o seks.",
        "There’s something more to it.": "Jest w tym coś więcej.",
        "Arianna…": "Arianno…",
        "Being a demon… It’s all so new to me… Perhaps I now need guidance.": "Bycie demonem… To dla mnie wszystko takie nowe… Może teraz potrzebuję przewodnictwa.",
        "Perhaps I should befriend other demons.": "Może powinnam zaprzyjaźnić się z innymi demonami.",
        "I wouldn’t want you hanging out with bad influences.": "Nie chciałbym, żebyś zadawała się z kimś, kto ma na ciebie zły wpływ.",
        "But, 1Hero… They are my kind now.": "Ale, 1Hero… Teraz to moi pobratymcy.",
        "Arianna?...": "Arianna?...",
        "I feel lost.": "Czuję się zagubiona.",
        "Maybe we could go together sometime.": "Może kiedyś moglibyśmy pójść razem.",
        "You would come with me?": "Poszedłbyś ze mną?",
        "I need to protect you, Arianna.": "Muszę cię chronić, Arianno.",
        "Oh, 1Hero… You’re so kind… But…": "Och, 1Hero… Jesteś taki dobry… Ale…",
        "For now, I need some time to think.": "Na razie muszę to przemyśleć.",
        "Could Arianna… be in love with me?": "Czy Arianna… może być we mnie zakochana?",
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
    if context.get('source_kind') != 'map' or context.get('map_id') != 28 or row['id'] in known:
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
path = ROOT / 'drafts/custom-dialogue-map28-arianna-morning-followups-01.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8', newline='\n')
print(f'Wrote Map 28 Arianna follow-ups: {len(rows)} records across {len({r["context"]["event_id"] for r in rows})} events')
