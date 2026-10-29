#!/usr/bin/env python3
"""Build Polish drafts for Map 200 follow-ups."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map200-followups-01.jsonl'
TRANSLATIONS = {
    "Ugh!... Ring the bells! He may be blinded, but he can hear you!": "Ugh!... Bij w dzwony! Może jest ślepy, ale cię słyszy!",
    "Nice try, but now the Toma is mine.": "Niezła próba, ale teraz Toma jest moja.",
    "Drink this, demon!": "Wypij to, demonie!",
    "Argh! It burns! I can't see!": "Argh! Parzy! Nie widzę!",
    "Attack!": "Atakuj!",
    "Push the stones into place. I think you can trap him from the sides!": "Przesuń kamienie na miejsce. Chyba możesz go uwięzić z boków!",
    "Shit! Daemalius saw me!": "Cholera! Daemalius mnie zobaczył!",
    "He stole the Toma… Maybe Henry should have helped take the chest.": "Ukradł Tomę… Może Henry powinien był pomóc nieść skrzynię.",
    "Lillian!": "Lillian!",
    "Leave the Toma where it lays… Find Erica’s body... Make sure the soul and body become one.": "Zostaw Tomę tam, gdzie leży… Znajdź ciało Eriki… Dopilnuj, by dusza i ciało stały się jednością.",
    "Leave the Toma?": "Zostawić Tomę?",
    "Evie! Where is Father Solomon? Where is Henry?": "Evie! Gdzie jest ojciec Solomon? Gdzie jest Henry?",
    "You’re too early.": "Jesteś za wcześnie.",
    "Too early?": "Za wcześnie?",
    "Yeah, this part of the game isn’t finished yet.": "Tak, ta część gry nie jest jeszcze skończona.",
    "These things take time… But don’t worry, you’re going to love the next chapter.": "Takie rzeczy wymagają czasu… Ale nie martw się, pokochasz kolejny rozdział.",
    "Thirteen is your lucky number, 1Hero.": "Trzynaście to twoja szczęśliwa liczba, 1Hero.",
    "You get to be the star in the largest reverse gangbang ever created!": "Zostaniesz gwiazdą największego odwróconego gangbangu, jaki kiedykolwiek stworzono!",
    "That can’t be accurate.": "To nie może być prawda.",
    "Well… It’s the largest one so far in this series.": "Cóż… To największy jak dotąd w tej serii.",
    "You’re not making any sense.": "Nie masz sensu.",
    "The person playing understands…": "Osoba grająca rozumie…",
    "Come back here in a couple weeks.": "Wróć tu za kilka tygodni.",
    "Woah! A personal portal! I’ve never seen one in person.": "Wow! Osobisty portal! Nigdy nie widziałem go na żywo.",
    "Let’s get moving.": "Ruszajmy.",
    "Goodbye, Evie. Even though we are sworn enemies, you were quite helpful. I owe you my gratitude.": "Żegnaj, Evie. Choć jesteśmy zaprzysiężonymi wrogami, byłaś bardzo pomocna. Jestem ci wdzięczny.",
    "I’m a big fan of Earth. I’d hate to see it ruined by a loser demon like Daemalius.": "Jestem wielką fanką Ziemi. Nie chciałabym, żeby zniszczył ją taki nieudacznik jak Daemalius.",
    "Diana’s probably worried sick.": "Diana pewnie martwi się na śmierć.",
    "Come on… Let’s not keep her waiting.": "Chodź… Nie każmy jej czekać.",
    "Woah… Wait a minute.": "Wow… Chwileczkę.",
    "I can’t save you this time, Henry… Your purpose has been served.": "Tym razem nie mogę cię uratować, Henry… Twoje zadanie zostało spełnione.",
    "So… This is the end of the line.": "Więc… To koniec drogi.",
    "I’m sorry. But that portal won’t work for you… You have no Earthly body… It’s been blown to bits.": "Przykro mi. Ale ten portal nie zadziała dla ciebie… Nie masz ziemskiego ciała… Zostało rozerwane na strzępy.",
    "Oh, God… He’s just a soul.": "O Boże… On jest tylko duszą.",
    "Are you sure? I feel fine.": "Na pewno? Czuję się dobrze.",
    "Don’t worry, Henry. There are perks to being a soul trapped in Hell.": "Nie martw się, Henry. Bycie duszą uwięzioną w Piekle ma swoje zalety.",
    "Perks?": "Zalety?",
    "You’re immortal now!": "Jesteś teraz nieśmiertelny!",
    "What good does that do here if I’m trapped?": "Co mi po tym, skoro jestem uwięziony?",
    "You’re not fully trapped… You can still visit Limbo!": "Nie jesteś całkiem uwięziony… Wciąż możesz odwiedzać Otchłań!",
    "I guess there’s no saving his body.": "Chyba nie da się uratować jego ciała.",
    "His body was turned into a fine mist.": "Jego ciało zamieniło się w drobną mgiełkę.",
    "You’d need a shell being to return to Earth… And I believe all of them are gone.": "Potrzebowałbyś istoty-powłoki, by wrócić na Ziemię… A chyba wszystkie przepadły.",
    "Damn…": "Cholera…",
    "Well, there is another way…": "Cóż, jest inny sposób…",
    "If you had the soul crystal, you could use that.": "Gdybyś miał kryształ dusz, mógłbyś go użyć.",
    "Wait, really?": "Czekaj, naprawdę?",
    "Of course, Henry. How do you think I did it?": "Oczywiście, Henry. Jak myślisz, jak ja to zrobiłam?",
    "So… We just need the soul crystal?": "Więc… Potrzebujemy tylko kryształu dusz?",
    "Do you know where it is?": "Wiesz, gdzie jest?",
    "I have it here…": "Mam go tutaj…",
    "It’s in the evil chapel behind the church… Hopefully it’s still there.": "Jest w złowrogiej kaplicy za kościołem… Mam nadzieję, że wciąż tam jest.",
    "I can get it. Hold tight.": "Mogę go zdobyć. Trzymaj się.",
    "Are they gone?": "Odeszli?",
    "Let’s get the fuck out of here.": "Wynośmy się stąd, do cholery.",
    "We stopped him from taking the artifact, but… he may come back.": "Powstrzymaliśmy go przed zabraniem artefaktu, ale… może wrócić.",
    "What about Erica?": "A co z Ericą?",
    "Yeah… Where’s Brian?": "Tak… Gdzie jest Brian?",
    "They chased after her body… We need to find her, and fast.": "Pobiegli za jej ciałem… Musimy ją znaleźć, i to szybko.",
    "Hey! Get back in there!": "Hej! Wracaj tam!",
    "It’s time to leave.": "Czas odejść.",
    "Yes! The Toma Leolo safe.": "Tak! Toma Leolo bezpieczna.",
    "Lilith chased after Daemalius… He could come back at any moment.": "Lilith pognała za Daemaliusem… Może wrócić w każdej chwili.",
    "Hey! Give that to us!": "Hej! Oddaj to nam!",
    "It’s over, Miss Deluna. We have it, and your contributions won’t go unpaid.": "To koniec, panno Deluna. Mamy to, a twój wkład nie pozostanie bez nagrody.",
    "Does this mean you’ll hold up your end of our bargain?": "Czy to znaczy, że dotrzymasz swojej części umowy?",
    "Hey! No one’s taking that statue! We need to find the priest.": "Hej! Nikt nie zabierze tego posągu! Musimy znaleźć księdza.",
    "Don’t let your old man down, Canmore. Surely we can all agree that the statue is safer in the Guild’s hands.": "Nie zawiedź starego, Canmore. Na pewno zgodzimy się, że posąg jest bezpieczniejszy w rękach Gildii.",
    "You’re not taking that statue, thief!": "Nie zabierzesz tego posągu, złodzieju!",
    "You’re not stopping me!": "Nie powstrzymasz mnie!",
    "Drop the weapon, Rinaldi!": "Rzuć broń, Rinaldi!",
    "Andrea!": "Andrea!",
    "You’re insane, Duncan. Madalyn isn’t going to share that treasure with you.": "Zwariowałeś, Duncan. Madalyn nie podzieli się z tobą tym skarbem.",
    "Destroy it and keep the pieces! It’s a win for everyone.": "Zniszcz to i zachowaj kawałki! To wygrana dla wszystkich.",
    "I need a new army!": "Potrzebuję nowej armii!",
    "Hahaha… An army is exactly what I intend to create!": "Hahaha… Armia to dokładnie to, co zamierzam stworzyć!",
    "Stop her!": "Zatrzymaj ją!",
    "Duncan! No!": "Duncan! Nie!",
    "Stay back! Don’t make me shoot you.": "Ani kroku! Nie zmuszaj mnie, bym strzelił.",
    "You’d shoot your own son?": "Strzeliłbyś do własnego syna?",
    "Son?": "Syn?",
    "Join us! Let’s get out of here.": "Dołącz do nas! Wynośmy się stąd.",
    "You’re not leaving with that statue.": "Nie wyjdziesz z tym posągiem.",
    "Fuck it… I guess I’m going back to jail.": "Pierdolić… Chyba wracam do więzienia.",
    "Sorry… Deal is off!": "Przepraszam… Umowa nieaktualna!",
    "Fuck! That bitch!": "Cholera! Ta suka!",
    "Stay back, Duncan!": "Zostań z tyłu, Duncan!",
    "Is it clear? Can we leave?": "Czy czysto? Możemy iść?",
    "It’s a standoff!": "To pat!",
    "What are you still doing here!? Find Erica near the altar! Now!": "Co tu jeszcze robisz!? Znajdź Ericę przy ołtarzu! Już!",
    "Mother!?": "Matko!?",
    "He’s coming back!": "On wraca!",
    "You can’t hide from me!": "Nie ukryjesz się przede mną!",
    "Come and get it!": "Chodź i weź to!",
    "Don’t let her destroy the Toma!": "Nie pozwól jej zniszczyć Tomy!",
    "Everyone! Run!": "Wszyscy! Uciekajcie!",
    "Let’s figure out a way to get past the monsters. We don’t want to set off any alarms.": "Wymyślmy, jak ominąć potwory. Nie chcemy włączyć alarmu.",
    "Bring us the soul crystal so we can save Henry. It should be in the dark chapel behind the mansion.": "Przynieś nam kryształ dusz, byśmy mogli uratować Henry'ego. Powinien być w mrocznej kaplicy za rezydencją.",
    "I can’t believe this is happening… What’s it like inside of a soul crystal?": "Nie mogę uwierzyć, że to się dzieje… Jak to jest w środku kryształu dusz?",
    "If you want to save Henry, you’ll need the soul crystal.": "Jeśli chcesz uratować Henry'ego, będziesz potrzebować kryształu dusz.",
    "So how does this work?": "Więc jak to działa?",
    "Does he have to spank it?": "Czy musi go klepnąć?",
    "Because…": "Bo…",
    "Henry… Just go into the soul crystal.": "Henry… Po prostu wejdź do kryształu dusz.",
    "Like… Walk into it?": "Tak… Po prostu wejść?",
    "What, that’s it?": "To wszystko?",
    "What were you expecting? Some kind of fancy ritual?": "Czego się spodziewałeś? Jakiegoś wymyślnego rytuału?",
    "Just get in there already.": "Po prostu tam wejdź.",
    "Needing my help until the very end, huh?": "Potrzebujesz mojej pomocy do samego końca, co?",
    "Goodbye, my love. See you when you get bored of living in a rock.": "Żegnaj, kochanie. Do zobaczenia, gdy znudzi ci się życie w kamieniu.",
    "What’s this!? A personal portal?": "Co to!? Osobisty portal?",
    "Good luck using it, dumbass. It’s bound to someone else.": "Powodzenia w użyciu, głupku. Jest powiązany z kimś innym.",
    "You ruined my plans!": "Zrujnowałeś moje plany!",
    "I’m a priest; it’s my job.": "Jestem księdzem; to moja praca.",
    "You’ll pay for this.": "Zapłacisz za to.",
    "Empty words, ugly fucker.": "Puste słowa, brzydalu.",
    "Arghhh! Not again!": "Arghhh! Znowu nie!",
    "Adios, Daemalius.": "Adios, Daemalius.",
    "Don’t you have a party to be going to?": "Nie powinieneś iść na imprezę?",
    "How do you know about that?": "Skąd o tym wiesz?",
    "I’m Evie. It’s my job to know what’s supposed to come next.": "Jestem Evie. Moim zadaniem jest wiedzieć, co będzie dalej.",
    "Nellie? What are you…": "Nellie? Co ty…",
    "1Hero!": "1Hero!",
    "Ella!?": "Ella!?",
    "The one and only.": "Jedyna i niepowtarzalna.",
    "In Hell? What business do you have here?": "W Piekle? Co tu robisz?",
    "Hell’s a special place. There’s a lot going on here.": "Piekło to wyjątkowe miejsce. Wiele się tu dzieje.",
    "Shit… More demons.": "Cholera… Więcej demonów.",
    "Let’s figure out a way to get past them. We don’t want to set off any alarms.": "Wymyślmy, jak je ominąć. Nie chcemy włączyć alarmu."
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
        or context.get('map_id') != 200
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
    raise SystemExit('Unmapped Map 200 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 129:
    raise SystemExit(f'Expected exactly 129 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 200 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
