import json
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl')
EVENTS = {
    467: {
        "God damn it, Hannah!": "Cholera jasna, Hannah!",
        "Alia can’t swim good! We have to save her!": "Alia nie umie pływać! Musimy ją ratować!",
        "I told you! I can’t swim!": "Mówiłam wam! Nie umiem pływać!",
        "Don’t worry, I know mouth-to-mouth!": "Spokojnie, umiem robić sztuczne oddychanie!",
        "Hannah… She doesn’t need mouth-to-mouth.": "Hannah… Nie potrzebuje sztucznego oddychania.",
        "Wow! You saved me with a kiss!": "Łał! Uratowałeś mnie pocałunkiem!",
        "It’s called mouth-to-mouth and it saves people who can’t swim.": "To się nazywa sztuczne oddychanie. Ratuje ludzi, którzy nie umieją pływać.",
        "You’re so smart!": "Jesteś taki mądry!",
        "Oh, boy… I guess at least no one was hurt.": "No cóż… Przynajmniej nikomu nic się nie stało.",
        "Can you mouth-to-mouth my pussy?": "Zrobisz mi usta-usta na cipce?",
        "That’s my specialty!": "To moja specjalność!",
        "That… doesn't make sense.": "To… nie ma sensu.",
        "Damn, Hannah… You girls don’t waste any time.": "Cholera, Hannah… Wy dziewczyny nie tracicie czasu.",
        "Don’t worry… Hannah’s my best friend.": "Spokojnie… Hannah jest moją najlepszą przyjaciółką.",
        "But you met… like… thirty minutes ago.": "Ale poznałyście się… jakieś… trzydzieści minut temu.",
        "Oh, God! It tickles!": "O Boże! To łaskocze!",
        "What a weird couple.": "Co za dziwna para.",
        "Yes! Yes! Mouth-to-mouth my boobs!": "Tak! Tak! Zrób mi usta-usta na cyckach!",
        "Hannah… You’re in big trouble… You know that?": "Hannah… Masz poważne kłopoty… Wiesz o tym?",
        "Fuck me, daddy!": "Pieprz mnie, tatusiu!",
        "Dammit, Hannah… You’re a handful.": "Cholera, Hannah… Ale z ciebie wariatka.",
        "You love it!": "Uwielbiasz to!",
        "Save my nipples, Hannah!": "Ratuj moje sutki, Hannah!",
        "She’s… so gentle.": "Jest… taka delikatna.",
        "That’s not the Hannah I know.": "To nie ta Hannah, którą znam.",
        "I like your body, Alia. I’m glad you didn’t get eaten.": "Podoba mi się twoje ciało, Alia. Cieszę się, że cię nie pożarł.",
        "Yes! I’m so happy!": "Tak! Ale się cieszę!",
        "You can’t keep an alligator, Hannah.": "Nie możesz trzymać aligatora w domu, Hannah.",
        "Shut up and fuck me!": "Zamknij się i pieprz mnie!",
        "Oh, God! My pussy!": "O Boże! Moja cipka!",
        "Gimme some cum, daddy!": "Daj mi trochę spermy, tatusiu!",
        "Fuck, Hannah…": "Kurwa, Hannah…",
        "That was quite the adventure!": "Ależ to była przygoda!",
    },
    327: {
        "Oh, shit! Sorry!": "O cholera! Przepraszam!",
        "We’re soaked!": "Jesteśmy cali mokrzy!",
        "I said I wanted to jump in the pool, but really?": "Mówiłam, że chcę wskoczyć do basenu, ale serio?",
        "Getting revenge for all the teasin’?": "Mścisz się za te wszystkie docinki?",
        "Are you starting a war, 1Hero?": "Zaczynasz wojnę, 1Hero?",
        "I swear, I didn’t do it on purpose.": "Przysięgam, nie zrobiłem tego specjalnie.",
        "I don’t believe him. How about you, Carol?": "Nie wierzę mu. A ty, Carol?",
        "I think he’s being mighty ornery.": "Uważam, że zachował się wyjątkowo niegrzecznie.",
        "Ah! You’re cold!": "Ach! Jesteś zimny!",
        "How’s it feel, 1Hero?": "Jak się czujesz, 1Hero?",
        "What’s wrong? Can’t handle being a little wet?": "Co jest? Nie zniesiesz odrobiny wilgoci?",
        "Haha! I swear! I’m not trying to start something.": "Haha! Przysięgam! Nie chcę wszczynać awantury.",
        "Maybe I should tell Heather exactly what you did over at my place.": "Może powinnam opowiedzieć Heather, co dokładnie robiłeś u mnie.",
        "What did you see, 1Hero? I want to know.": "Co widziałeś, 1Hero? Chcę wiedzieć.",
        "He heard me having fun with myself and decided to come take a look.": "Usłyszał, jak sama się zabawiam, i postanowił to sprawdzić.",
        "Carol!?": "Carol!?",
        "Oh, my goodness. 1Hero!": "O mój Boże, 1Hero!",
        "I thought it was Hannah… I thought she was crying.": "Myślałem, że to Hannah… Że płacze.",
        "Haha! Oh, 1Hero. How embarrassing.": "Haha! Och, 1Hero. Ale wstyd.",
        "Hey, come on! Am I ever going to hear the end of it?": "No weźcie! Czy będziecie mi to wypominać do końca życia?",
        "What is it about me that you just had to take a peek?": "Co takiego we mnie jest, że musiałeś zerknąć?",
        "Oh, I bet I can take a guess. That naughty boy.": "Chyba wiem. Ten niegrzeczny chłopiec.",
        "Tell me, 1Hero.": "Powiedz mi, 1Hero.",
        "It’s my big knockers. Ain’t it?": "To moje wielkie cycki, prawda?",
        "Carol! Come on.": "Carol! No daj spokój.",
        "I think you’re right, Carol. He’s blushing.": "Chyba masz rację, Carol. Zarumienił się.",
        "Look at ‘em. What’s the matter?": "No, popatrz na nie. Coś nie tak?",
        "Does this do it for you, 1Hero?...": "Podoba ci się to, 1Hero?...",
        "Or do you prefer the bigger mommy milkers?": "A może wolisz większe cycki mamusi?",
        "Heather!?": "Heather!?",
        "If you’re going to be spying on us, you might as well soak up a free show.": "Skoro i tak nas podglądasz, możesz chociaż obejrzeć darmowy pokaz.",
        "I get it! I won't do it again, Carol.": "Rozumiem! Już tego nie zrobię, Carol.",
    },
    257: {
        "Try vinegar.": "Spróbuj octu.",
        "Try mustard.": "Spróbuj musztardy.",
        "Try soy sauce.": "Spróbuj sosu sojowego.",
        "Try yogurt.": "Spróbuj jogurtu.",
        "Try ketchup.": "Spróbuj ketchupu.",
        "Try sugar.": "Spróbuj cukru.",
        "Try baking soda.": "Spróbuj sody oczyszczonej.",
        "Try cornstarch.": "Spróbuj skrobi kukurydzianej.",
        "What else?": "Co jeszcze?",
        "Vinegar.": "Ocet.",
        "Mustard.": "Musztarda.",
        "Soy sauce.": "Sos sojowy.",
        "Yogurt.": "Jogurt.",
        "Ketchup.": "Ketchup.",
        "Sugar.": "Cukier.",
        "Baking soda.": "Soda oczyszczona.",
        "Cornstarch.": "Skrobia kukurydziana.",
        "Okay. Now what should I add?": "Dobrze. Co mam teraz dodać?",
        "The last ingredient is vinegar.": "Ostatnim składnikiem jest ocet.",
        "The last ingredient is mustard.": "Ostatnim składnikiem jest musztarda.",
        "The last ingredient is soy sauce.": "Ostatnim składnikiem jest sos sojowy.",
        "The last ingredient is yogurt.": "Ostatnim składnikiem jest jogurt.",
        "The last ingredient is ketchup.": "Ostatnim składnikiem jest ketchup.",
        "The last ingredient is sugar.": "Ostatnim składnikiem jest cukier.",
        "The last ingredient is baking soda.": "Ostatnim składnikiem jest soda oczyszczona.",
        "The last ingredient is cornstarch.": "Ostatnim składnikiem jest skrobia kukurydziana.",
        "I hope this works…": "Oby zadziałało…",
        "Eww! It tastes even worse!": "Fuj! Smakuje jeszcze gorzej!",
        "I don’t think you know what you’re doing either, 1Hero.": "Chyba ty też nie wiesz, co robisz, 1Hero.",
        "Hmm… I can figure this out.": "Hmm… Rozgryzę to.",
        "You’re welcome to try again.": "Możesz spróbować jeszcze raz.",
    },
    421: {
        "Come on! Make it quick.": "No dalej! Szybciej.",
        "Damn, girl! This really turns you on.": "Cholera, dziewczyno! Ale cię to podnieca.",
        "Only if she shares you.": "Tylko jeśli się tobą z nią podzieli.",
        "Is anyone coming?": "Ktoś idzie?",
        "You’re fine. I’ll tell you if I hear anything.": "Spokojnie. Dam znać, jeśli coś usłyszę.",
        "God! This is so wrong!": "Boże! To takie niewłaściwe!",
        "Shit… Hurry up and cum.": "Cholera… Szybciej, dojdź już.",
        "Ugh! Is that any way to treat a lady?": "Ugh! Tak się traktuje damę?",
        "That’s the spot! Fuck me!": "Właśnie tam! Pieprz mnie!",
        "Quiet, you two! We don’t want to get caught.": "Cicho, wy dwoje! Nie chcemy, żeby nas przyłapano.",
        "You like this, Erica?": "Podoba ci się, Erico?",
        "Harder, 1Hero.": "Mocniej, 1Hero.",
        "Go for it. I want a turn before Father comes looking for us.": "Dawaj. Chcę swojej kolejki, zanim Ojciec zacznie nas szukać.",
        "Ah! Yes! Really give it to me!": "Ach! Tak! Daj mi porządnie!",
        "Come on, baby. Cum for me.": "No dalej, kochanie. Dojdź dla mnie.",
        "Damn! You’re really giving it to her!": "Cholera! Ale jej dajesz!",
        "That was fucking fantastic!": "To było zajebiście fantastyczne!",
        "Come on, Chloe. It’s your turn.": "No dalej, Chloe. Teraz twoja kolej.",
        "Fuck me hard like you did Erica.": "Pieprz mnie mocno, tak jak Ericę.",
        "It’s heaven, girl.": "To niebo, dziewczyno.",
        "You okay, Chloe?": "Wszystko w porządku, Chloe?",
        "It’s good, 1Hero!": "Jest dobrze, 1Hero!",
        "No one’s coming. Give it to her good.": "Nikt nie idzie. Daj jej porządnie.",
        "Do it, 1Hero. Fuck me hard.": "Dawaj, 1Hero. Pieprz mnie mocno.",
        "Take my cock, Chloe.": "Bierz mojego kutasa, Chloe.",
        "I’m getting close.": "Jestem blisko.",
        "It’s okay. Cum for me.": "W porządku. Dojdź dla mnie.",
        "Sit on me!": "Usiądź na mnie!",
        "Erica… I want to taste you!": "Erico… Chcę cię skosztować!",
        "1Hero! You came inside of me!": "1Hero! Doszedłeś we mnie!",
        "Lucky girl.": "Szczęściara.",
    },
    332: {
        "Oh, damn! It’s a witch idol.": "O cholera! To bożek wiedźmy.",
        "You know what it is?": "Wiesz, co to jest?",
        "Of course I do. My grandma taught me everything about the witch doctors.": "Oczywiście. Babcia nauczyła mnie wszystkiego o szamanach.",
        "What do you know about this?": "Co o tym wiesz?",
        "I know you shouldn’t have taken that from the forest.": "Wiem, że nie powinieneś był zabierać tego z lasu.",
        "Yeah, yeah. I’ll give it to a museum as soon as I’m done with it.": "Dobra, dobra. Oddam to do muzeum, jak już skończę.",
        "I don’t know how to identify anything specific, I’m afraid.": "Niestety, nie potrafię rozpoznać żadnych szczegółów.",
        "What can you tell me? Anything?": "Co możesz mi powiedzieć? Cokolwiek?",
        "Probably not, 1Hero. I’m not a walking library.": "Raczej niewiele, 1Hero. Nie jestem chodzącą biblioteką.",
        "I think it has magic powers.": "Chyba ma magiczne moce.",
        "What? Are you serious?": "Co? Mówisz poważnie?",
        "I don’t know… After I picked it up, it made me feel… weird.": "Nie wiem… Kiedy to podniosłem, poczułem się… dziwnie.",
        "Weird? I don’t know of any old myths about feeling weird after picking up a rock.": "Dziwnie? Nie znam żadnych legend o dziwnym samopoczuciu po podniesieniu kamienia.",
        "It made me… cum a whole lot.": "Sprawiło, że… doszedłem naprawdę wiele razy.",
        "Wait, what do you mean?": "Zaraz, co masz na myśli?",
        "It made me super horny and then my friend jerked me off and I came over and over again.": "Strasznie mnie napaliło, a potem koleżanka zrobiła mi dobrze i dochodziłem raz za razem.",
        "It was with Hannah… And Chloe… It’s nothing serious.": "To były Hannah… i Chloe… Nic poważnego.",
        "1Hero! If what you’re saying is true, you may have found a piece of the Toma Leolo.": "1Hero! Jeśli mówisz prawdę, być może znalazłeś fragment Toma Leolo.",
        "Toma Leolo… It’s an old myth that has been passed down through generations of Casula natives…": "Toma Leolo… To stara legenda przekazywana z pokolenia na pokolenie wśród rdzennych mieszkańców Casuli…",
        "It’s a magic statue that grants sexual powers.": "To magiczny posąg, który obdarza mocami seksualnymi.",
        "It was so powerful, it was broken into six pieces and scattered throughout the land so no man could ever put it back together.": "Był tak potężny, że rozbito go na sześć części i rozrzucono po całej krainie, by żaden mężczyzna nie mógł go złożyć.",
        "They destroyed a magic statue to keep men from getting horny?": "Zniszczyli magiczny posąg, żeby mężczyźni się nie napalali?",
        "Well… That’s the tale. I know it doesn’t make sense.": "Cóż… Tak głosi legenda. Wiem, że to nie ma sensu.",
        "So, if you find all six pieces, you’ll cum even more?": "Czyli jeśli znajdziesz wszystkie sześć części, będziesz dochodził jeszcze częściej?",
        "That’s not how the tale goes. The statue grants lots of sexual powers. But I don’t know exactly what they are.": "Legenda tak nie mówi. Posąg zapewnia wiele mocy seksualnych, ale nie wiem dokładnie jakich.",
        "They say each piece grants a different power…": "Podobno każda część daje inną moc…",
        "I never believed it though. No one did…": "Nigdy w to nie wierzyłam. Nikt nie wierzył…",
        "It’s not supposed to be real.": "To nie powinno być prawdziwe.",
        "Well, shit. This thing may be worth a lot of money.": "No cholera. To może być warte fortunę.",
        "You better not sell it. I’ll totally turn you in.": "Lepiej tego nie sprzedawaj. Na pewno cię wsypię.",
    },
}
known = {r['id'] for r in map(json.loads, MERGED.read_text(encoding='utf-8').splitlines()) if r['translation'].strip()}
rows_by_event = {event_id: [] for event_id in EVENTS}
missing = set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    event_id = context.get('event_id')
    if context.get('source_kind') != 'common_event' or event_id not in EVENTS or row['id'] in known:
        continue
    source = row['source_text'].strip()
    if not source or source.startswith('/') or source in {'…', '...', '..'}:
        continue
    translation = EVENTS[event_id].get(source)
    if translation is None:
        missing.add((event_id, source))
        continue
    row['translation'] = translation
    rows_by_event[event_id].append(row)
if missing:
    raise SystemExit('Unmapped strings: ' + repr(sorted(missing)))
for event_id, rows in rows_by_event.items():
    path = ROOT / f'drafts/custom-dialogue-common-event-{event_id}-01.jsonl'
    if path.exists():
        raise SystemExit(f'Refusing to overwrite {path}')
    path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8', newline='\n')
    print(f'Wrote Common Event {event_id}: {len(rows)} records')
print('Total:', sum(map(len, rows_by_event.values())))
