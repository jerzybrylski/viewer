#!/usr/bin/env python3
"""Build Polish drafts for the remaining police-station dialogue on Map 32."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
EVENTS = {
    15: {
        "Erica Abraham?": "Erica Abraham?",
        "She’s willing to talk to us.": "Zgodziła się z nami porozmawiać.",
        "Let’s get this on the record…": "Zapiszmy to w protokole…",
        "Am I under suspicion?": "Jestem podejrzana?",
        "Relax. She’s a bit of a hard ass. That’s all.": "Spokojnie. Po prostu jest trochę surowa.",
    },
    22: {
        "1Hero? Did you just walk in?": "1Hero? Dopiero co wszedłeś?",
        "Oh, uhh... I was just checking out some stuff around town before heading in.": "Och, yyy… Rozglądałem się po mieście, zanim tu przyszedłem.",
        "You’re late.": "Spóźniłeś się.",
        "I’m going to the gymnasium. Is there something you need to tell me before you log into your computer?": "Idę na salę gimnastyczną. Jest coś, co powinieneś mi powiedzieć, zanim zalogujesz się na komputerze?",
        "You tell me. Anything I should know?": "To ty mi powiedz. Jest coś, o czym powinienem wiedzieć?",
        "You mean… The Guild file access? I can explain.": "Masz na myśli… dostęp do akt Gildii? Mogę to wyjaśnić.",
        "That’s David’s job. Don’t make him angry.": "To sprawa Davida. Nie denerwuj go.",
        "Oh, yeah.": "A, no tak.",
        "I don’t know how you accessed those files, but stick to your own work and leave David alone.": "Nie wiem, jak dostałeś się do tych akt, ale zajmij się własną pracą i zostaw Davida w spokoju.",
        "Right, right. Sorry. It won’t happen again.": "Jasne, jasne. Przepraszam. To się nie powtórzy.",
        "I’m watching you, 1Hero.": "Mam cię na oku, 1Hero.",
        "Wait… If she checked the file access, it would be her name that comes up.": "Chwila… Jeśli sprawdziła dostęp do akt, w rejestrze powinno być jej nazwisko.",
        "How did she know it was me who accessed the files?": "Skąd wiedziała, że to ja otworzyłem te akta?",
        "Either Andrea told her, or she’s spying on my computer.": "Albo Andrea jej powiedziała, albo szpieguje mój komputer.",
        "God damn it. Of course she’s spying on my computer.": "Cholera jasna. Oczywiście, że szpieguje mój komputer.",
        "I should have known.": "Mogłem się domyślić.",
        "Up early this morning, 1Hero?": "Dziś wcześnie wstałeś, 1Hero?",
        "Melissa, I need to talk to you.": "Melissa, muszę z tobą porozmawiać.",
        "Walk with me, 1Hero.": "Chodź ze mną, 1Hero.",
        "Coming back to the office this late?": "Wracasz do biura tak późno?",
        "I’m meeting with Andrea.": "Spotykam się z Andreą.",
        "What the hell did you do to Melissa? She’s been locked in her office all day.": "Co ty, do cholery, zrobiłeś Melissie? Siedzi zamknięta w gabinecie cały dzień.",
        "She’s mad at me. No surprise.": "Jest na mnie zła. Nic dziwnego.",
        "She’s going to fire you one day.": "Pewnego dnia cię zwolni.",
        "You really want to do this?": "Naprawdę chcesz to zrobić?",
        "Finally ready to become a man?": "W końcu jesteś gotów stać się mężczyzną?",
        "Rinaldi! Watch your attitude.": "Rinaldi! Uważaj na ton.",
        "That’s right, 1Hero. You’re training with me.": "Zgadza się, 1Hero. Będziesz trenować ze mną.",
        "Have fun and good luck.": "Baw się dobrze i powodzenia.",
        "If you can’t hit a target, you won’t get a gun.": "Jeśli nie trafisz w cel, nie dostaniesz broni.",
        "I’ll pass your test. Don’t you worry.": "Zdam twój test. Nie martw się.",
    },
    28: {
        "Out of my way! Someone’s trying to hack into my computer.": "Z drogi! Ktoś próbuje włamać się do mojego komputera.",
        "Sounds serious.": "Brzmi poważnie.",
        "I better hurry. I don’t know how long he plans on searching for the hacker.": "Lepiej się pospieszę. Nie wiem, jak długo zamierza szukać hakera.",
    },
    29: {
        "I’m expecting a package. Are you the delivery man?": "Czekam na paczkę. To pan jest kurierem?",
        "This doesn’t look like my box.": "To nie wygląda na moją paczkę.",
    },
    32: {
        "How annoying!": "Co za irytujące!",
    },
    45: {
        "Whatever you say, Miss Bhatt.": "Jak pani sobie życzy, panno Bhatt.",
        "1Hero, Miss Abraham will be in the interrogation room whenever you’re ready.": "1Hero, panna Abraham będzie czekać w pokoju przesłuchań, kiedy będziesz gotów.",
        "Seems you’ve done a good job taking my case from me.": "Widzę, że dobrze ci idzie odbieranie mi sprawy.",
        "Are you actually upset?": "Naprawdę jesteś zła?",
        "If you’re going to step on my toes, that means you’re doing all the paperwork too.": "Jeśli zamierzasz wchodzić mi w drogę, to ty wypełnisz całą papierkową robotę.",
        "I’m done.": "Mam dość.",
        "I’m under direct orders from Kimura. Don’t blame me.": "Dostałem bezpośredni rozkaz od Kimury. Nie obwiniaj mnie.",
        "I had your energy once, 1Hero.": "Kiedyś i ja miałem tyle zapału co ty, 1Hero.",
        "Don’t you think we owe it to the people to try and actually do some good here?": "Nie sądzisz, że jesteśmy winni ludziom, by spróbować zrobić tu coś dobrego?",
        "After almost four decades, I don’t get paid enough to keep caring.": "Po prawie czterdziestu latach nie płacą mi wystarczająco, żebym nadal się przejmował.",
        "She’s ready, 1Hero.": "Jest gotowa, 1Hero.",
        "I’m putting a lot of trust in you.": "Bardzo ci ufam.",
        "If Commissioner Kimura is going to trust you, then I have no choice but to do the same.": "Skoro komisarz Kimura ci ufa, nie mam wyboru i też muszę ci zaufać.",
        "If you let her down, you let me down.": "Jeśli ją zawiedziesz, zawiedziesz też mnie.",
        "There will be no second chances this time.": "Tym razem nie będzie drugiej szansy.",
        "If she drops you, then so will I.": "Jeśli ona cię skreśli, ja też.",
    },
    46: {
        "Coming in late again?": "Znowu się spóźniasz?",
        "Just mind your own business, David.": "Po prostu pilnuj własnego nosa, David.",
        "What the hell did you do to Melissa? She’s been avoiding her office all morning.": "Co ty, do cholery, zrobiłeś Melissie? Od rana unika swojego gabinetu.",
        "Maybe she’s meeting with Kimura in the gym…": "Może spotyka się z Kimurą na siłowni…",
        "Seems they got it locked down.": "Wygląda na to, że zamknęli ją na klucz.",
    },
    48: {
        "1Hero. Looking for something?": "1Hero. Czegoś szukasz?",
        "Hello, Miss Kimura. Melissa was looking for you.": "Dzień dobry, pani Kimura. Melissa pani szukała.",
        "I’m running a bit late.": "Trochę się spóźniam.",
        "She left to get some evidence checked out.": "Poszła zbadać pewne dowody.",
        "Do you know what this is about?": "Wiesz, o co chodzi?",
        "I figured out some new developments.": "Odkryłem kilka nowych faktów.",
        "Walk with me, 1Hero. You can give me the rundown.": "Chodź ze mną, 1Hero. Po drodze zdasz mi relację.",
        "Uhh, sure thing.": "Yyy, jasne.",
    },
    53: {
        "I can see a key way up there. But my shoes are too slippery to climb a marble column.": "Widzę tam wysoko klucz, ale moje buty są zbyt śliskie, żebym wspiął się po marmurowej kolumnie.",
    },
    54: {
        "Uhhh… Yeah. I’m here.": "Yyy… Tak. Jestem tutaj.",
        "Get out of here, Canmore. You’re not supposed to be here.": "Wynoś się stąd, Canmore. Nie powinno cię tu być.",
    },
    63: {
        "Canmore? What are you doing here?": "Canmore? Co ty tu robisz?",
        "It’s okay. He’s with me.": "W porządku. Jest ze mną.",
        "How are the interrogations going?": "Jak idą przesłuchania?",
        "The woman is mostly clueless, but I’m making slow progress.": "Ta kobieta niewiele wie, ale powoli robię postępy.",
        "What about the dude?": "A co z tym facetem?",
        "The uniformed officers have him. They won't release him to me.": "Zajmują się nim mundurowi. Nie chcą mi go przekazać.",
        "You know how they are.": "Wiesz, jacy oni są.",
        "Dammit. We need as much info as possible for Kimberly.": "Cholera. Musimy zdobyć jak najwięcej informacji dla Kimberly.",
        "Paul wants to do a live broadcast.": "Paul chce przeprowadzić transmisję na żywo.",
        "An interview?": "Wywiad?",
        "With both of us. Are you up for it?": "Z nami obojgiem. Dasz radę?",
        "We better prepare.": "Lepiej się przygotujmy.",
        "I’m doing my best. But I can only get so much in such a limited time.": "Staram się, jak mogę. Ale w tak krótkim czasie nie zdołam zdobyć zbyt wielu informacji.",
        "Too bad I can’t help…": "Szkoda, że nie mogę pomóc…",
        "You know, I have a disguise… I could try and sneak over there.": "Wiesz, mam przebranie… Mógłbym spróbować się tam zakraść.",
        "1Hero! That’s illegal. You’ll get arrested and then it’ll be you on the other side of the interrogation table.": "1Hero! To nielegalne. Aresztują cię i sam zasiądziesz po drugiej stronie stołu przesłuchań.",
        "Haha. Don’t worry about me.": "Haha. Nie martw się o mnie.",
        "Still cocky.": "Nadal taki pewny siebie.",
        "Should I change?": "Powinienem się przebrać?",
        "Don’t tell Andrea about any of this.": "Nie mów Andrei o niczym.",
        "The cat will be out of the bag soon enough.": "I tak niedługo wszystko wyjdzie na jaw.",
        "Let’s become heroes first.": "Najpierw zostańmy bohaterami.",
        "Andrea!?": "Andrea!?",
        "I was checking up on the interrogations.": "Sprawdzałam, jak idą przesłuchania.",
        "I need to speak with you. Now!": "Muszę z tobą porozmawiać. Natychmiast!",
    },
    67: {
        "1Hero, there you are.": "1Hero, jesteś.",
        "One of the goons escaped?": "Jeden ze zbirów uciekł?",
        "You have to find him, 1Hero.": "Musisz go znaleźć, 1Hero.",
        "We’re not sure where he went.": "Nie wiemy, dokąd poszedł.",
        "None of the officers saw him leave?": "Żaden z funkcjonariuszy nie widział, jak wychodził?",
        "Any idea what his plan might be?": "Masz pomysł, jaki może mieć plan?",
        "I have to attend to other matters…": "Muszę zająć się innymi sprawami…",
        "1Hero, find him and bring him back to the station.": "1Hero, znajdź go i przyprowadź z powrotem na komisariat.",
        "She should be sending officers to search for him.": "Powinna wysłać funkcjonariuszy, żeby go poszukali.",
        "For some reason, she wanted you.": "Z jakiegoś powodu chciała właśnie ciebie.",
        "Those goons know that Duncan wanted them killed.": "Ci zbiry wiedzą, że Duncan chciał ich zabić.",
        "Do you think he’s going back to Duncan?": "Myślisz, że wróci do Duncana?",
        "Where is the lady goon?": "Gdzie jest ta bandytka?",
        "She’s still here.": "Wciąż tu jest.",
        "If he’s planning to leave the country, he’s going to need help.": "Jeśli planuje uciec z kraju, będzie potrzebował pomocy.",
        "Any idea who might be helping him?": "Masz pomysł, kto może mu pomagać?",
        "You have a gun on you, right?": "Masz przy sobie broń, prawda?",
        "Armed and ready…": "Uzbrojony i gotowy…",
        "Maybe we should continue this meeting in your office.": "Może dokończymy rozmowę w twoim gabinecie.",
    },
    68: {
        "Where’s David going? I thought he would stay at his desk.": "Dokąd idzie David? Myślałem, że zostanie przy biurku.",
    },
    69: {
        "Bobby vouched for me.": "Bobby za mnie poręczył.",
        "I wouldn’t have expected that.": "Nie spodziewałbym się tego.",
        "Have you seen Henry… Or Diana?": "Widziałaś Henry’ego… Albo Dianę?",
        "They must have escaped somehow.": "Musieli jakoś uciec.",
        "No sign of Madalyn either.": "Madalyn też nigdzie nie widać.",
        "Melissa… Madalyn is… uhh… The soul of an angel is in her body.": "Melissa… Madalyn… yyy… W jej ciele jest dusza anioła.",
        "That’s an odd compliment.": "To dość dziwny komplement.",
        "No! Literally… Arianna, an angel from Heaven, is now controlling Madalyn’s body.": "Nie! Dosłownie… Arianna, anioł z Nieba, przejęła kontrolę nad ciałem Madalyn.",
        "Of course. Why not?": "Oczywiście. Czemu nie?",
        "Lilith is now inside of Erica’s body.": "Lilith jest teraz w ciele Eriki.",
        "The demon?": "Ten demon?",
        "Yeah! You’re getting it.": "Tak! Zaczynasz rozumieć.",
        "Where’s Erica… Erica’s soul?": "Gdzie jest Erica… Jej dusza?",
        "I… I think she’s gone.": "Ja… Chyba jej już nie ma.",
        "Shit. Is that true? Certainly in this crazy world of magic there’s a way to save her.": "Cholera. To prawda? W tym szalonym, magicznym świecie musi być jakiś sposób, żeby ją uratować.",
        "You know about as much as I do…": "Wiesz tyle samo co ja…",
        "We have to stop Lilith… We have to stop any more innocent people from becoming victims of her plot.": "Musimy powstrzymać Lilith… Nie możemy pozwolić, by jej intryga pochłonęła kolejne niewinne ofiary.",
        "That statue needs to be destroyed.": "Ten posąg trzeba zniszczyć.",
        "I know… We’ll figure something out.": "Wiem… Coś wymyślimy.",
        "1Hero… It’s getting late. I should head home.": "1Hero… Robi się późno. Powinnam wracać do domu.",
        "I’m sorry I got you wrapped up in this.": "Przepraszam, że cię w to wciągnąłem.",
        "Sounds like the whole world is now wrapped up in this.": "Wygląda na to, że wciągnął się w to cały świat.",
    },
    71: {
        "Where’s that judge!?": "Gdzie jest ten sędzia!?",
        "Woah, Carol, you might want to tone it down a little.": "Hej, Carol, może trochę spuścisz z tonu.",
        "Messing with a judge can get very serious, very quickly.": "Zadzieranie z sędzią może szybko skończyć się bardzo poważnie.",
        "I don’t care! Where is he!?": "Nie obchodzi mnie to! Gdzie on jest!?",
        "What’s the meaning of this? Why are you screaming, woman?": "Co to ma znaczyć? Czemu krzyczysz, kobieto?",
        "So it’s you? I have some words for you.": "A więc to ty? Mam ci coś do powiedzenia.",
        "Now hold on just a minute, Carol.": "Zaczekaj chwilę, Carol.",
        "Your Honor, Miss Ray received a court order about her farm…": "Wysoki Sądzie, panna Ray otrzymała nakaz sądowy dotyczący jej farmy…",
        "One signed by your hand.": "Podpisany przez pana.",
        "Maybe we could discuss this matter in your chambers, Your Honor?": "Może moglibyśmy omówić tę sprawę w pańskim gabinecie, Wysoki Sądzie?",
        "I’m busy.": "Jestem zajęty.",
        "You’re about to be in a world of pain if you don’t fix this!": "Zaraz bardzo tego pożałujesz, jeśli tego nie naprawisz!",
        "Stop yelling!": "Przestań krzyczeć!",
        "I want a meeting now!": "Chcę się z tobą spotkać. Natychmiast!",
        "Jesus, woman… Very well. Follow me.": "Jezu, kobieto… Dobrze. Chodź za mną.",
    },
    73: {
        "1Hero!": "1Hero!",
        "Business in court today?": "Sprawy sądowe załatwione?",
        "All settled.": "Wszystko załatwione.",
        "Good to hear.": "Dobrze słyszeć.",
        "What’s new with you?": "Co u ciebie nowego?",
        "New recruits.": "Nowi rekruci.",
        "Problems?": "Jakieś problemy?",
        "They hardly know their hands from their feet.": "Ledwo ogarniają, co mają robić.",
        "I’m sure they’ll get better.": "Na pewno się poprawią.",
        "Sure they will, as long as they can learn to keep their hands to themselves.": "Na pewno, o ile nauczą się trzymać ręce przy sobie.",
        "Guessing you heard about the peephole drama?": "Domyślam się, że słyszałeś o aferze z judaszem?",
        "The one in the shower stalls? Someone finally got caught?": "Tym w kabinach prysznicowych? W końcu kogoś przyłapali?",
        "Yeah. A couple of our new female recruits discovered it.": "Tak. Odkryło go kilka naszych nowych rekrutek.",
        "Oof, I think I see where this is going.": "Uff, chyba wiem, do czego to zmierza.",
        "Maybe not the way you’re thinking.": "Może nie tak, jak myślisz.",
        "Turns out they decided to use it themselves.": "Okazało się, że same postanowiły z niego skorzystać.",
        "Waited for one of the male recruits to use the shower…": "Poczekały, aż jeden z rekrutów pójdzie pod prysznic…",
        "Then started hootin’ and hollerin’ at him.": "A potem zaczęły na niego gwizdać i krzyczeć.",
        "Oh damn. So it was the guy who complained?": "O rany. Czyli to facet poskarżył się na nie?",
        "Oh no. Wouldn’t have been so bad if it ended there.": "Nie. Nie byłoby tak źle, gdyby na tym się skończyło.",
        "Instead, the guy gave them a show.": "Zamiast tego facet dał im niezłe przedstawienie.",
        "A higher-up ended up walking in on him as he reached the finale…": "Wtedy wszedł jeden z przełożonych, akurat gdy facet dochodził do finału…",
        "And the finale ended up all over the higher-up.": "A potem finał wylądował na przełożonym.",
        "Hahaha!": "Hahaha!",
        "Anyway, now I have three recruits already suspended, at a time when we don’t have people to spare.": "Tak czy inaczej, mam już trzech zawieszonych rekrutów, a teraz nie możemy sobie pozwolić na braki kadrowe.",
        "Lots of calls?": "Dużo zgłoszeń?",
        "The city is going crazy, 1Hero.": "W mieście wszystkim odbiło, 1Hero.",
        "A couple days ago, a couple just started fucking in a park in broad daylight.": "Kilka dni temu para zaczęła pieprzyć się w parku, w biały dzień.",
        "Yesterday there was a striptease by a group of young women in front of Dick’s.": "Wczoraj grupa młodych kobiet zrobiła striptiz przed Dick’s.",
        "Just today we had to stop a gangbang in the middle of a grocery store.": "Dziś musieliśmy przerwać grupowy seks pośrodku sklepu spożywczego.",
        "Those are just the most memorable incidents.": "A to tylko najbardziej pamiętne przypadki.",
        "People are crazy over sex these days.": "Ludziom ostatnio kompletnie odbiło na punkcie seksu.",
        "Sounds like a whole lot of fun to me.": "Dla mnie brzmi to całkiem zabawnie.",
        "To make matters worse, there’s a condom shortage now.": "Jakby tego było mało, brakuje teraz prezerwatyw.",
        "If nothing changes, there could be a lot of big bellies going around in the next few months.": "Jeśli nic się nie zmieni, za kilka miesięcy będzie mnóstwo ciężarnych.",
        "Doesn’t sound so bad to me.": "Dla mnie to nie brzmi tak źle.",
        "Thief!": "Złodziej!",
        "Your Honor?": "Wysoki Sądzie?",
        "My office! Now, Rinaldi! It’s a matter of urgent importance.": "Do mojego gabinetu! Natychmiast, Rinaldi! To pilna sprawa.",
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
    if context.get('source_kind') != 'map' or context.get('map_id') != 32 or row['id'] in known:
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
path = ROOT / 'drafts/custom-dialogue-map32-station-followups-01.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8', newline='\n')
print(f'Wrote Map 32 station follow-ups: {len(rows)} records across {len({r["context"]["event_id"] for r in rows})} events')
