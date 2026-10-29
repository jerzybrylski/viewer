import json
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl')
EVENTS = {
    55: {
        "Get away from him, you monster!": "Odsuń się od niego, potworze!",
        "I have a crucifix! You better get back!": "Mam krucyfiks! Lepiej się cofnij!",
        "You’re standing in my way! You will not take him from us!": "Stoisz mi na drodze! Nie odbierzesz nam go!",
        "It’s okay, Brian. I made peace with them.": "W porządku, Brian. Pogodziłem się z nimi.",
        "They’ve brainwashed you!": "Wyprali ci mózg!",
        "You are the one brainwashing the people of Earth!": "To ty pierzesz mózgi mieszkańcom Ziemi!",
        "I said, get back!": "Mówiłem, cofnij się!",
        "These worlds are governed by chaos. And it’s people like you that have let it happen.": "Tymi światami rządzi chaos. To tacy jak ty do tego dopuścili.",
        "You worship a false god!": "Czcisz fałszywego boga!",
        "Can we just make peace here?": "Możemy po prostu się pogodzić?",
        "It’s time, 1Hero. You know what to do.": "Pora, 1Hero. Wiesz, co robić.",
        "Well, shit. There she goes again.": "No cholera. Znowu to samo.",
        "Never better!... Where is Kimberly?": "Nigdy nie czułem się lepiej!... Gdzie jest Kimberly?",
        "Tasha ran with her to the church… I came back after I didn’t see you following us.": "Tasha pobiegła z nią do kościoła… Wróciłem, bo nie widziałem, żebyś szedł za nami.",
        "Brian, it’s okay. We beat Madalyn.": "Brian, wszystko w porządku. Pokonaliśmy Madalyn.",
        "My name is Father Solomon.": "Nazywam się ojciec Solomon.",
        "Yeah, yeah. Sure.": "Tak, tak. Jasne.",
        "What about Diana and Henry?": "A co z Dianą i Henrym?",
        "I don’t know where they went… They can fend for themselves.": "Nie wiem, dokąd poszli… Sami sobie poradzą.",
        "Did we win?": "Wygraliśmy?",
        "We saved Kimberly from the monsters… That’s good enough for now.": "Uratowaliśmy Kimberly przed potworami… Na razie wystarczy.",
    },
    9: {
        "What the hell are they doing?": "Co oni, do cholery, robią?",
        "Stay low so they don’t see us.": "Trzymaj się nisko, żeby nas nie zauważyli.",
        "I have no idea… But it’s a popular hangout spot for those creepy sick guys.": "Nie mam pojęcia… Ale ci przerażający chorzy często się tu kręcą.",
        "I just want a closer look.": "Chcę tylko podejść bliżej i się przyjrzeć.",
        "This is some sort of torture chamber.": "To jakiś rodzaj sali tortur.",
        "Who are they torturing?": "Kogo torturują?",
        "Us, if we don’t get out of here soon.": "Nas, jeśli szybko się stąd nie wyniesiemy.",
        "I don’t think that’s what it is.": "Nie sądzę, żeby o to chodziło.",
        "What are those sounds?": "Co to za odgłosy?",
        "There is something on the other side of that strange metal thing.": "Coś jest po drugiej stronie tego dziwnego metalowego czegoś.",
        "Another room?": "Kolejny pokój?",
        "Maybe. I can’t quite tell.": "Może. Trudno powiedzieć.",
        "We’re pushing our luck.": "Za bardzo ryzykujemy.",
        "As long as those lepers are around there’s no way to get through.": "Dopóki kręcą się tu trędowaci, nie ma jak się przedostać.",
        "So… What are you going to do?": "No… Co zamierzasz zrobić?",
        "I’ll come back later…": "Wrócę później…",
        "You don’t have to ask me twice.": "Nie musisz mi dwa razy powtarzać.",
    },
    57: {
        "What are you doing back here?": "Co tu znowu robisz?",
        "Erica is destroying the mansion!": "Erica niszczy rezydencję!",
        "Daemalius is blocking us from leaving! I have to go through the rift!": "Daemalius nie pozwala nam uciec! Muszę przejść przez rozdarcie!",
        "It’s a battle! They are fighting each other!": "Trwa walka! Biją się między sobą!",
        "What the fuck do we do now?": "Co, kurwa, mamy teraz zrobić?",
        "We go to Hell and we bring the bomb with us.": "Idziemy do piekła i zabieramy bombę ze sobą.",
        "How are we going to save Erica now?": "Jak teraz uratujemy Ericę?",
        "Lillian said her soul will appear on the altar in Hell.": "Lillian mówiła, że jej dusza pojawi się na ołtarzu w piekle.",
        "If she commits blasphemy.": "Jeśli popełni bluźnierstwo.",
        "She’ll do it! I believe in her.": "Zrobi to! Wierzę w nią.",
        "That's… kinda strange…": "To… trochę dziwne…",
        "Shit! We have to hurry!": "Cholera! Musimy się spieszyć!",
        "This place is going to collapse.": "To miejsce zaraz się zawali.",
        "There’s no escape?": "Nie ma ucieczki?",
        "Everyone, stop your bickering and let’s get our asses to Hell!": "Wszyscy przestańcie się kłócić i ruszajmy do piekła!",
        "What a day.": "Ależ dzień.",
        "I can’t follow… But I will do what I can from here.": "Nie mogę za wami iść… Ale pomogę, jak tylko będę mógł.",
    },
    93: {
        "What are you girls doing down here?": "Co wy tu robicie?",
        "How the hell do we open the rift?": "Jak, do cholery, otworzymy rozdarcie?",
        "We need to get that Toma.": "Musimy zdobyć Tomę.",
        "If we can stop Lilith and close the rift, they can keep the damn Toma.": "Jeśli powstrzymamy Lilith i zamkniemy rozdarcie, mogą sobie zatrzymać tę cholerną Tomę.",
        "How can you say that? They could find a way to use it.": "Jak możesz tak mówić? Mogą znaleźć sposób, żeby jej użyć.",
        "They could reopen the rift.": "Mogą ponownie otworzyć rozdarcie.",
        "You really think you can enter Hell and find a magic rock that, if you look at it, you’ll die?": "Naprawdę myślisz, że wejdziesz do piekła i znajdziesz magiczny kamień, na który wystarczy spojrzeć, by umrzeć?",
        "If anyone can do it, I can.": "Jeśli ktoś da radę, to ja.",
        "I’ve been through worse.": "Gorsze rzeczy już mnie spotkały.",
        "Worse? How is that possible?": "Gorsze? Jak to możliwe?",
        "I’ve lived a long life.": "Długo już żyję.",
        "Help us find the amulets.": "Pomóż nam znaleźć amulety.",
        "Fine. But we’ll have to deal with this rift eventually.": "Dobra. Ale w końcu będziemy musieli zająć się tym rozdarciem.",
        "Be careful, Ella. Finding the Toma isn’t worth losing your life.": "Uważaj, Ella. Żaden Toma nie jest wart utraty życia.",
    },
    82: {
        "1Hero… I think it’s open.": "1Hero… Chyba jest otwarte.",
        "Nevermind that. We need Father Solomon.": "Nieważne. Potrzebujemy ojca Solomona.",
        "Just go inside and take a peek.": "Po prostu wejdź i rzuć okiem.",
        "You take a look!": "Sam rzuć okiem!",
        "Both of you, shut up…": "Wy dwoje, zamknijcie się…",
        "1Hero… Take a look.": "1Hero… Zajrzyj tam.",
        "Not without Father Solomon.": "Nie bez ojca Solomona.",
        "Go in there, Vayne. You’re a woman. She’ll go easy on you.": "Wejdź tam, Vayne. Jesteś kobietą, będzie dla ciebie łagodniejsza.",
        "Shit. We’re wasting time.": "Cholera. Tracimy czas.",
    },
}
known = {r['id'] for r in map(json.loads, MERGED.read_text(encoding='utf-8').splitlines()) if r['translation'].strip()}
rows, missing = [], set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    event_id = context.get('event_id')
    if context.get('source_kind') != 'map' or context.get('map_id') != 116 or event_id not in EVENTS or row['id'] in known:
        continue
    source = row['source_text'].strip()
    if not source or source.startswith('/') or source in {'…', '...', '..'}:
        continue
    translation = EVENTS[event_id].get(source)
    if translation is None:
        missing.add((event_id, source))
        continue
    row['translation'] = translation
    rows.append(row)
if missing:
    raise SystemExit('Unmapped strings: ' + repr(sorted(missing)))
path = ROOT / 'drafts/custom-dialogue-map116-followups-04.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8', newline='\n')
print(f'Wrote Map 116 follow-ups: {len(rows)} records across {len(EVENTS)} events')
