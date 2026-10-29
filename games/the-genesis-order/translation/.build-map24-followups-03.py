import json
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl')
EVENTS = {
    35: {
        "Just stopping by to say hi.": "Wpadłem tylko się przywitać.",
        "Thanks for making time for the old lady.": "Dziękuję, że znalazłeś czas dla starszej pani.",
        "Thanks for the talk, 1Hero. We’re so lucky to have you in our lives.": "Dzięki za rozmowę, 1Hero. Mamy szczęście, że jesteś w naszym życiu.",
        "Are you okay, Heather?": "Wszystko w porządku, Heather?",
        "I’m fine. Are you okay?": "U mnie tak. A u ciebie?",
        "Well, when you figure it out. I’m here for you.": "Jak już sam to zrozumiesz, będę przy tobie.",
        "If you’re looking for Chloe she went to the church.": "Jeśli szukasz Chloe, poszła do kościoła.",
        "I’m still rattled by what I saw. What’s going on with you?": "Wciąż jestem wstrząśnięta tym, co zobaczyłam. Co się z tobą dzieje?",
        "Don’t worry. I wasn’t feeling myself.": "Nie martw się. Nie byłem sobą.",
        "Please take care of yourself.": "Proszę, dbaj o siebie.",
        "If you’re looking for Chloe, she went to Dick’s with Judy.": "Jeśli szukasz Chloe, poszła z Judy do Dicka.",
        "Chloe said she met a new girl and you’re her bodyguard.": "Chloe mówiła, że poznała nową dziewczynę, a ty jesteś jej ochroniarzem.",
        "Something like that. She’s internet famous.": "Mniej więcej. Jest znana w internecie.",
        "Wow! Sounds interesting.": "Wow! Brzmi ciekawie.",
        "I hope you youngsters had a nice time this evening.": "Mam nadzieję, że dobrze się dziś bawiliście, młodzi.",
        "I’m surprised to see you here on a Monday morning.": "Dziwię się, że widzę cię tu w poniedziałek rano.",
    },
    38: {
        "Oh, baby. Thank you.": "Och, kochanie. Dziękuję.",
        "So what happens now?": "Co teraz?",
        "What about Chloe?": "A co z Chloe?",
        "I guess life isn't simple. Is it?": "Życie nie jest proste, prawda?",
        "That, it’s not.": "Rzeczywiście nie jest.",
        "Oh no! I forgot about dinner. Chloe must be starving.": "O nie! Zapomniałam o kolacji. Chloe musi być głodna.",
        "She went to Carol’s with Judy.": "Poszła z Judy do Carol.",
        "Are they planning to come back?": "Zamierzają wrócić?",
        "I think so. But I don’t know when.": "Chyba tak. Ale nie wiem kiedy.",
        "I think it might rain tonight. I hope they’ve planned for the weather.": "Chyba będzie dziś padać. Mam nadzieję, że wzięły pod uwagę pogodę.",
        "Do you want to head over there? I’m sure Carol could feed us all. She’s a farmer after all.": "Chcesz tam pójść? Carol na pewno nas nakarmi. W końcu jest farmerką.",
        "Haha. Oh, 1Hero. I don’t think so.": "Haha. Och, 1Hero. Chyba nie.",
        "I think I’ll stay home and rest after all that exercise.": "Chyba zostanę w domu i odpocznę po tych wszystkich ćwiczeniach.",
        "We’re back to teasing?": "Znowu się ze mną droczysz?",
        "You know I can’t help myself.": "Wiesz, że nie mogę się powstrzymać.",
        "I don’t want this to be the end.": "Nie chcę, żeby to był koniec.",
        "I’m glad you said that… But what is this exactly?": "Cieszę się, że to mówisz… Ale czym właściwie jest to między nami?",
        "Go to Carol’s. The girls want to see you… Especially Judy.": "Idź do Carol. Dziewczyny chcą cię zobaczyć… Zwłaszcza Judy.",
        "Haha. I’m sure she does.": "Haha. Na pewno.",
        "Don’t break her heart.": "Nie złam jej serca.",
        "I know. I know.": "Wiem, wiem.",
        "See you later, dear.": "Do zobaczenia, kochanie.",
        "I can’t believe that happened. It’s so exciting…": "Nie mogę uwierzyć, że to się stało. Ależ to ekscytujące…",
        "But Chloe… What I did to her at the church.": "Ale Chloe… To, co z nią zrobiłem w kościele.",
        "I can’t be fooling around with them both… Can I?": "Nie mogę romansować z nimi obiema… Prawda?",
        "What would Chloe think if she knew?": "Co pomyślałaby Chloe, gdyby się dowiedziała?",
        "It feels good to be open about our relationship.": "Dobrze jest nie ukrywać naszego związku.",
        "It’s not good to keep too many secrets.": "Nie warto ukrywać zbyt wielu sekretów.",
    },
    5: {
        "It’s so good to see you, 1Hero.": "Miło cię widzieć, 1Hero.",
        "Hi, Miss Ray.": "Cześć, panno Ray.",
        "Hannah! You made it!": "Hannah! Udało ci się dotrzeć!",
        "What’s for supper?  I’m starvin’.": "Co na kolację? Umieram z głodu.",
        "Hannah Ray! Show some manners.": "Hannah Ray! Zachowuj się przyzwoicie.",
        "Make yourselves at home, I’m just going to set the plates.": "Rozgośćcie się, tylko nakryję do stołu.",
        "I’ll help you out, Heather.": "Pomogę ci, Heather.",
        "Congratulations on the house, 1Hero. You’ve grown into quite the man.": "Gratuluję domu, 1Hero. Wyrosłeś na prawdziwego mężczyznę.",
        "I couldn’t have done it without Heather.": "Nie dałbym rady bez Heather.",
        "Well, I look forward to talking all about it over dinner.": "Chętnie posłucham o tym przy kolacji.",
        "So, 1Hero. Are you going to invite us girls over to your new home?": "No dobrze, 1Hero. Zaprosisz nas do swojego nowego domu?",
        "It’s a bit empty at the moment.": "Na razie jest w nim trochę pusto.",
        "No rush. I’m sure you’re really busy.": "Nie ma pośpiechu. Wiem, że jesteś zajęty.",
        "No way! You’ve got to throw a party!": "Nie ma mowy! Musisz urządzić imprezę!",
        "Hannah! Don’t be pushy.": "Hannah! Nie naciskaj.",
        "Hannah’s right. I do want to show you my new place.": "Hannah ma rację. Chcę wam pokazać nowe mieszkanie.",
        "But, not until it’s ready.": "Ale dopiero, gdy będzie gotowe.",
        "Dinner’s ready.": "Kolacja gotowa.",
        "You didn’t tell her I was at the church, did you?": "Nie powiedziałaś jej, że byłem w kościele, prawda?",
        "No. I didn’t tell Hannah anything.": "Nie. Nic nie mówiłam Hannah.",
        "You’re seeing Sister Judy?": "Spotykasz się z siostrą Judy?",
        "I just… I trust her.": "Po prostu… Ufam jej.",
        "You know, you can come to me if you need any help.": "Wiesz, możesz do mnie przyjść, jeśli będziesz potrzebować pomocy.",
        "I’m fine. I don’t need help…": "Nic mi nie jest. Nie potrzebuję pomocy…",
        "Come on, let’s go eat.": "Chodźcie, jedzenie stygnie.",
    },
    12: {
        "Where’s Chloe? I thought she would be with you.": "Gdzie jest Chloe? Myślałam, że będzie z tobą.",
        "Oh, uhh. She went to the church.": "Och, eee. Poszła do kościoła.",
        "What brings you here? Looking to help me out in the garden?": "Co cię sprowadza? Chcesz mi pomóc w ogrodzie?",
        "What’s going on in the garden?": "Co się dzieje w ogrodzie?",
        "Carol is on her way over to help with the tomato plants. But really, it’s just an excuse to spread some gossip.": "Carol zaraz przyjdzie pomóc przy pomidorach. Ale tak naprawdę to tylko pretekst, żeby poplotkować.",
        "Gossip? What are you two talking about?": "Plotkować? O czym wy dwie rozmawiacie?",
        "Interrogating me, detective?": "Przesłuchujesz mnie, detektywie?",
        "I wasn’t expecting to see you here, 1Hero.": "Nie spodziewałam się, że cię tu zobaczę, 1Hero.",
        "She’s at the church.": "Jest w kościele.",
        "She’s still hanging around that place?": "Wciąż kręci się po tym miejscu?",
        "Here to help with the caterpillars, 1Hero?": "Przyszedłeś pomóc z gąsienicami, 1Hero?",
        "We’ve got a bad infestation.": "Mamy poważną plagę.",
        "1Hero doesn’t have time for caterpillars. He’s got a girlfriend now.": "1Hero nie ma czasu na gąsienice. Ma teraz dziewczynę.",
        "I don’t have a girlfriend.": "Nie mam dziewczyny.",
        "What’s her name, 1Hero?": "Jak ma na imię, 1Hero?",
        "I’m simply getting some help from someone involved in the Wilkes case.": "Po prostu korzystam z pomocy osoby związanej ze sprawą Wilkesów.",
        "Well, maybe you should get a girlfriend soon. I know what’s going on in that dirty mind of yours.": "Może powinieneś w końcu znaleźć sobie dziewczynę. Wiem, co chodzi ci po tej niegrzecznej głowie.",
        "And just how do you know what’s in 1Hero’s head?": "A skąd wiesz, co siedzi w głowie 1Hero?",
        "I don’t want to hear about this. When is Chloe getting back?": "Nie chcę o tym słuchać. Kiedy Chloe wróci?",
        "She’s been at the church for a while. She might be staying there for Mass.": "Jest w kościele już od jakiegoś czasu. Może zostanie na mszę.",
        "Hannah! Watch your language!": "Hannah! Uważaj na słowa!",
        "I’m gonna go find Chloe. It’s too nice a day to waste in an old building.": "Pójdę poszukać Chloe. Szkoda tak pięknego dnia na siedzenie w starym budynku.",
        "If you’re looking to help some old ladies, feel free to join us in the backyard.": "Jeśli chcesz pomóc starszym paniom, wpadnij do nas na podwórko.",
    },
    37: {
        "Just now leaving, 1Hero?": "Właśnie wychodzisz, 1Hero?",
        "You’re still awake?": "Wciąż nie śpisz?",
        "The couch is not exactly the most comfortable sleeping spot.": "Kanapa nie jest najwygodniejszym miejscem do spania.",
        "You’re kind for letting Judy use your bedroom.": "To miłe z twojej strony, że pozwoliłeś Judy spać w swojej sypialni.",
        "Sounded to me like you were plenty kind yourself.": "Z tego, co słyszałam, ty też byłeś dla niej bardzo miły.",
        "What did you hear?": "Co słyszałaś?",
        "Are you toying with a nun’s heartstrings, 1Hero?": "Bawisz się uczuciami zakonnicy, 1Hero?",
        "No! It’s not like that…": "Nie! To nie tak…",
        "She has these urges.": "Ma takie… potrzeby.",
        "Because you’re hanging around her.": "Bo kręcisz się koło niej.",
        "No, it’s from Madalyn… It’s hard to explain.": "Nie, to przez Madalyn… Trudno wyjaśnić.",
        "So you’re just helping her with these evil urges?": "Czyli po prostu pomagasz jej z tymi niecnymi pragnieniami?",
        "Heather… You might want to wash the sheets tomorrow morning.": "Heather… Rano może zechcesz wyprać pościel.",
        "Haha. Oh, 1Hero. What am I going to find? Judy juice, or a mixture of Canmore cum?": "Haha. Och, 1Hero. Co tam znajdę? Soki Judy czy mieszankę spermy Canmore’a?",
        "You might find a bit of both.": "Może trochę jednego i drugiego.",
        "Mmmm. Maybe I’ll sleep in it.": "Mmmm. Może w niej pośpię.",
        "Heather!": "Heather!",
        "I’m not going to let you live down what you did to Carol, you know.": "Nie pozwolę ci zapomnieć o tym, co zrobiłeś Carol.",
        "When you were very little you used to grab Carol’s boobs.": "Kiedy byłeś mały, ciągle łapałeś Carol za cycki.",
        "I was a kid.": "Byłem dzieckiem.",
        "I knew what you wanted…": "Wiedziałam, czego chciałeś…",
        "Are you a boob man?": "Lubisz cycki?",
        "Heather… You’re every bit as beautiful as Carol. You know that, right?": "Heather… Jesteś równie piękna jak Carol. Wiesz o tym, prawda?",
        "Would it kill you to tell me that every now and then?": "Czy tak trudno powiedzieć mi to od czasu do czasu?",
        "Heather…": "Heather…",
        "Thanks, stud muffin.": "Dzięki, przystojniaku.",
        "See you soon, Heather.": "Do zobaczenia, Heather.",
    },
}
known = {r['id'] for r in map(json.loads, MERGED.read_text(encoding='utf-8').splitlines()) if r['translation'].strip()}
rows, missing = [], set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    event_id = context.get('event_id')
    if context.get('source_kind') != 'map' or context.get('map_id') != 24 or event_id not in EVENTS or row['id'] in known:
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
path = ROOT / 'drafts/custom-dialogue-map24-followups-03.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8', newline='\n')
print(f'Wrote Map 24 follow-ups: {len(rows)} records across {len(EVENTS)} events')
