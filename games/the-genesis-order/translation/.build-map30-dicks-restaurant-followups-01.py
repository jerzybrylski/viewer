#!/usr/bin/env python3
"""Build Polish drafts for the remaining Dick's/restaurant dialogue on Map 30."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
EVENTS = {
    10: {
        "Way to embarrass yourself, 1Hero.": "No i ładnie się ośmieszyłeś, 1Hero.",
    },
    11: {
        "My wife is cheating on me! What color shirt is that bastard wearing?": "Moja żona mnie zdradza! Jaką koszulę ma na sobie ten drań?",
        "I’m going to kick his ass!": "Skopię mu tyłek!",
    },
    13: {
        "Her style may be silly, but she’s pretty cute.": "Może ma dziwny styl, ale jest całkiem urocza.",
        "I know her type though. I better be careful not to get involved in any drama.": "Znam ten typ. Lepiej uważać, żeby nie wpakować się w żaden dramat.",
        "I wonder who these stalkers could be?": "Ciekawe, kim są ci prześladowcy.",
        "Maybe it’s just that kid from the gym…": "Może to tylko ten chłopak z siłowni…",
        "I could handle him.": "Z nim sobie poradzę.",
    },
    14: {
        "I made a fool of myself at the gym. I’m never going back…": "Ośmieszyłem się na siłowni. Już nigdy tam nie wrócę…",
        "Here’s a key, you can have my stuff.": "Masz klucz, możesz wziąć moje rzeczy.",
    },
    16: {
        "Hannah? Carol? What are you doing at Dick’s? Wasn’t Hannah cooking tonight?": "Hannah? Carol? Co robicie w Dick’s? Hannah nie miała dziś gotować?",
        "Hannah caused a bit of an accident.": "Hannah spowodowała mały wypadek.",
        "It's not my fault! You see fire, you put it out with water!": "To nie moja wina! Jak widzisz ogień, gasisz go wodą!",
        "Not when it's burning grease!": "Nie, jeśli pali się tłuszcz!",
        "Are you both okay?": "Nic wam nie jest?",
        "It was a scene for sure. But we survived.": "Było ostro, ale przeżyłyśmy.",
        "I really screwed the pooch, Ma. I’m sorry.": "Naprawdę nawaliłam, mamo. Przepraszam.",
        "Not as sorry as you’ll be when you have to clean up your mess.": "Nie tak bardzo, jak będziesz żałować, kiedy przyjdzie ci posprzątać ten bałagan.",
        "Aww, Ma! That could take forever.": "No weź, mamo! To może zająć wieki.",
        "Just how much of a mess did you make?": "Ale jak wielki bałagan zrobiłaś?",
        "Hey, 1Hero! You can help me with the cleaning, right?": "Hej, 1Hero! Pomożesz mi sprzątać, prawda?",
        "If you help, I’ll make it worth your while.": "Jeśli mi pomożesz, odwdzięczę ci się.",
        "What’s that s’posed to mean? Goin’ to cook up another oil fire, just for him?": "Co to ma znaczyć? Chcesz rozpalić kolejny pożar tłuszczu, specjalnie dla niego?",
        "Very funny, Ma.": "Bardzo śmieszne, mamo.",
        "I’m sure I can think of something good.": "Na pewno wymyślę coś dobrego.",
        "Haha, okay, Hannah. I’ll help you out.": "Haha, dobrze, Hannah. Pomogę ci.",
        "How ‘bout you join us, 1Hero? We’d love the company.": "Może do nas dołączysz, 1Hero? Chętnie dotrzymamy ci towarzystwa.",
        "I have something else to do first, but I’ll be by later.": "Najpierw muszę coś załatwić, ale później wpadnę.",
        "This ol’ lady not good enough company over dinner?": "Ta staruszka nie nadaje się na towarzystwo do kolacji?",
        "Not at all. But I have other dinner plans. I might tell you about it later.": "Ależ skąd. Mam już jednak inne plany na kolację. Może później ci o nich opowiem.",
        "As long as you show up to help me clean.": "Pod warunkiem, że przyjdziesz mi pomóc posprzątać.",
        "Don’t worry, Hannah, I’ll be there.": "Nie martw się, Hannah. Będę.",
        "I’ll see you ladies later.": "Do zobaczenia później, dziewczyny.",
        "See you, stud.": "Do zobaczenia, przystojniaku.",
        "You can’t keep bailing Hannah out of trouble. She’ll never learn.": "Nie możesz ciągle wyciągać Hannah z kłopotów. Nigdy się nie nauczy.",
        "I guess I’m just too much of a nice guy.": "Chyba jestem po prostu zbyt dobrym facetem.",
        "I hope dinner isn’t too busy.": "Mam nadzieję, że podczas kolacji nie będzie wielkiego ruchu.",
        "You’ll get the hang of it.": "Nabierzesz wprawy.",
    },
    17: {
        "Don’t forget to stop by later. There’s a mighty big mess that needs cleaning.": "Nie zapomnij później wpaść. Czeka tu naprawdę wielki bałagan do posprzątania.",
        "What have I gotten myself into?": "W co ja się wpakowałem?",
    },
    19: {
        "I’ll take a bottle of your finest wine.": "Poproszę butelkę najlepszego wina.",
        "That’ll be $1000.": "To będzie tysiąc dolarów.",
        "Oh... Uh... I’ll take a bottle of your cheapest wine.": "Och… Eee… Poproszę butelkę najtańszego wina.",
        "Okay... That’ll be $50.": "Dobrze… To będzie pięćdziesiąt dolarów.",
        "That sounds more like it.": "Tak brzmi lepiej.",
        "Come back when you have money.": "Wróć, jak będziesz mieć pieniądze.",
        "Do you have any bottles of wine?": "Masz jakieś butelki wina?",
        "I can sell you some red wine for $1000.": "Mogę sprzedać ci czerwone wino za tysiąc dolarów.",
        "I can sell you some red wine for $700.": "Mogę sprzedać ci czerwone wino za siedemset dolarów.",
        "I can sell you some red wine for $400.": "Mogę sprzedać ci czerwone wino za czterysta dolarów.",
        "I can sell you some red wine for $200.": "Mogę sprzedać ci czerwone wino za dwieście dolarów.",
        "Are you crazy!? That’s way too much.": "Zwariowałeś!? To zdecydowanie za dużo.",
    },
    21: {
        "If you’re looking for a deal, the Nacho’s fill you up.": "Jeśli szukasz czegoś w dobrej cenie, nachosy porządnie cię nasycą.",
        "Thanks, David. I’m not hungry though.": "Dzięki, David. Ale nie jestem głodny.",
        "Hey, 1Hero. Check out those hot moms over there.": "Hej, 1Hero. Zobacz tamte seksowne mamuśki.",
        "God damn it, David!": "Cholera jasna, David!",
        "What!? A guy can’t enjoy a little sightseeing.": "Co!? Facet nie może sobie popatrzeć?",
    },
    22: {
        "Care to join us for a late lunch?": "Dołączysz do nas na późny lunch?",
        "Sorry, Carol. I’m not hungry right now.": "Wybacz, Carol. Nie jestem teraz głodny.",
        "Maybe you can just get a cucumber salad.": "Może weź po prostu sałatkę z ogórkiem.",
        "Haha. You’re wild, Carol.": "Haha. Ale z ciebie dzikuska, Carol.",
        "Haha": "Haha",
    },
    23: {
        "Have fun with the girls tonight watching your TV show…": "Miłej zabawy z dziewczynami przy oglądaniu twojego programu…",
        "I can’t wait to see it myself.": "Sam nie mogę się doczekać, żeby go obejrzeć.",
        "Well, it’s not a show. It’s an interview.": "To nie program. To wywiad.",
        "I bet you look so handsome on TV.": "Założę się, że świetnie wyglądasz w telewizji.",
    },
    24: {
        "Well, I’m stuffed.": "Ale się najadłem.",
        "I could go for more, but we gotta get to the porn shop before it closes.": "Zjadłbym jeszcze, ale musimy zdążyć do sklepu erotycznego, zanim go zamkną.",
        "You’re still going on about that?": "Wciąż o tym mówisz?",
        "I’ll race you there!": "Założę się, że dotrę tam pierwsza!",
        "You can’t beat me! I’m a farm girl!": "Nie masz ze mną szans! Jestem dziewczyną ze wsi!",
        "Listen: You two go back home and I’ll make sure Hannah and Erica get home safe.": "Słuchajcie, wracajcie do domu, a ja dopilnuję, żeby Hannah i Erica bezpiecznie dotarły do siebie.",
        "Are you bringing her back to your place?": "Zabierasz ją do siebie?",
        "Maybe it was a mistake to invite Hannah.": "Może zaproszenie Hannah było błędem.",
        "No. She is a wonderful person. I’d like to get to know them both some more.": "Nie. To wspaniała osoba. Chciałbym lepiej poznać je obie.",
        "You want to go?": "Chcesz iść?",
        "I want to go with you, 1Hero.": "Chcę iść z tobą, 1Hero.",
        "Are you sure you can handle it?": "Na pewno sobie z tym poradzisz?",
        "I am… intrigued.": "Jestem… zaintrygowana.",
        "Well… Okay. Maybe you’ll find a toy that you like.": "No dobrze… Może znajdziesz zabawkę, która ci się spodoba.",
        "Oh! Hahaha… I don’t know.": "Och! Hahaha… Sama nie wiem.",
        "Stick with me, Sister. You’ll be fine.": "Trzymaj się mnie, siostro. Wszystko będzie dobrze.",
    },
    28: {
        "Are you coming back to party with us, 1Hero?": "Wrócisz do nas na imprezę, 1Hero?",
    },
    29: {
        "Stay a while and grab a drink.": "Zostań na chwilę i napij się czegoś.",
        "Not tonight, Erica.": "Nie dziś, Erica.",
        "I’m running late and my gluten-free meal is taking forever!": "Spóźnię się, a moje bezglutenowe danie robią całą wieczność!",
        "Are you on break too, detective? Or are you wasting tax money?": "Też masz przerwę, detektywie? Czy marnujesz pieniądze podatników?",
        "Fantastic! You got my order right.": "Fantastycznie! Podałaś mi właściwe zamówienie.",
        "Will you tip Judy?": "Dasz Judy napiwek?",
        "Since she’s pretty, I can spare a couple bucks.": "Jest ładna, więc mogę dorzucić parę dolców.",
        "Wow! Thanks for the tip!": "Wow! Dzięki za napiwek!",
        "What!? Are you trying to kill me? I can’t eat this!": "Co!? Chcesz mnie zabić? Nie mogę tego jeść!",
        "What’s with the sexy waitress?": "Co z tą seksowną kelnerką?",
        "Don’t get any ideas. That’s my girlfriend.": "Nie kombinuj. To moja dziewczyna.",
        "Nice job, detective. She’s a dime.": "Dobra robota, detektywie. Jest niezłą dziesiątką.",
    },
    33: {
        "1Hero?": "1Hero?",
        "Spend some time at the gym?": "Byłeś na siłowni?",
        "I’m looking for you. You aren’t answering your phone.": "Szukam cię. Nie odbierasz telefonu.",
        "It’s Saturday. It can’t wait?": "Jest sobota. To nie może zaczekać?",
        "Kimura wants to see us… tonight.": "Kimura chce się z nami spotkać… dziś wieczorem.",
        "What the hell did you do now?": "Co ty znowu, do cholery, zrobiłeś?",
        "Paul… The producer from Channel 4…": "Paul… Producent z Channel 4…",
        "He was caught snooping around the Wilkes’ mansion.": "Przyłapano go na kręceniu się po rezydencji Wilkesów.",
        "They are persistent bastards over there. They want a story…": "Ci z Channel 4 są cholernie uparci. Chcą mieć sensację…",
        "Kimura is going to give it to them.": "Kimura im ją da.",
        "So, Andrea’s going to tell them everything?": "Czyli Andrea powie im wszystko?",
        "She wants us to put together a presentation and give her a rundown of everything we’ve gathered so far…": "Chce, żebyśmy przygotowali prezentację i przedstawili jej podsumowanie wszystkich zebranych dotąd informacji…",
        "It’ll be up to her what we share.": "To ona zdecyduje, co ujawnimy.",
        "Christ. How much time do we have?": "Cholera. Ile mamy czasu?",
        "A few hours. Shall we head to the office?": "Kilka godzin. Jedziemy do biura?",
        "I can’t go in there like this. We can meet at my place.": "Nie mogę tak tam iść. Spotkajmy się u mnie.",
        "I live next to the Channel 4 skyrise… In the condos.": "Mieszkam w kompleksie apartamentów obok wieżowca Channel 4.",
        "I know. I’ve seen it.": "Wiem. Widziałem to miejsce.",
        "Ugh. I don’t even want to know how you know that…": "Ugh. Nawet nie chcę wiedzieć, skąd to wiesz…",
        "Ma’am. Our smoothie machine is broken, is there anything else you’d like?": "Proszę pani, zepsuła nam się maszyna do smoothie. Czy życzy sobie pani coś innego?",
        "Forget it. I’ve got other plans.": "Nieważne. Mam inne plany.",
        "Here we go.": "No to zaczynamy.",
    },
    34: {
        "Are you going to be joining us for lunch?": "Dołączysz do nas na lunch?",
        "Sorry, I have to work.": "Przepraszam, muszę pracować.",
        "Oh… That’s too bad.": "Och… Szkoda.",
    },
    35: {
        "Are you still working?": "Wciąż pracujesz?",
        "Yeah. I have to go chase after my boss.": "Tak. Muszę pobiec za szefową.",
    },
    36: {
        "Oh… She left right after we ate. You just missed her.": "Och… Wyszła zaraz po posiłku. Właśnie się minęliście.",
        "Were you waiting for me?": "Czekałaś na mnie?",
        "I just… Judy told me something.": "Po prostu… Judy coś mi powiedziała.",
        "I think I know what this is about… Are you mad?": "Chyba wiem, o co chodzi… Jesteś zła?",
        "Huh? No. I…": "Co? Nie. Ja…",
        "Hey, Ella. This is Chloe.": "Cześć, Ella. To Chloe.",
        "Oh, hello. Nice to meet you.": "Och, cześć. Miło cię poznać.",
        "You look… pretty.": "Wyglądasz… ładnie.",
        "She’s a cam girl.": "Jest dziewczyną z kamerki.",
        "You could’ve said I’m a gamer girl.": "Mogłeś powiedzieć, że jestem gamingową dziewczyną.",
        "Oh, my. What is it you do?": "Ojej. Czym się zajmujesz?",
        "Some… fun stuff.": "Takimi… przyjemnymi rzeczami.",
        "Are you here with 1Hero?": "Jesteś tu z 1Hero?",
        "I had lunch here with a friend earlier.": "Wcześniej jadłam tu lunch z przyjaciółką.",
        "I was hoping to steal away 1Hero for a moment.": "Miałam nadzieję porwać 1Hero na chwilę.",
        "I’d love to talk more. Maybe we can get some drinks.": "Chętnie jeszcze porozmawiam. Może napijemy się czegoś.",
        "Sure. I’ll grab the drinks. What do you ladies want?": "Jasne. Przyniosę drinki. Na co macie ochotę?",
        "A coffee would be nice.": "Poproszę kawę.",
        "Umm… I’ll just have an energy drink.": "Yyy… Ja poproszę napój energetyczny.",
        "Come on, Ella. Let’s get a table.": "Chodź, Ella. Zajmijmy stolik.",
    },
    38: {
        "I live right next door! Let’s go, before I start dripping on the floor.": "Mieszkam tuż obok! Chodźmy, zanim zacznę kapać na podłogę.",
        "God, Ella.": "Jezu, Ella.",
    },
    39: {
        "Hey! If you want that bag of chips, it’ll cost you $50.": "Hej! Jeśli chcesz tę paczkę chipsów, należy się pięćdziesiąt dolarów.",
        "That’s a rip-off!": "To zdzierstwo!",
        "If you want to take my only snack, I’m not parting with it for cheap.": "Jeśli chcesz zabrać mi jedyną przekąskę, nie oddam jej za bezcen.",
    },
    43: {
        "Why don’t you join us, 1Hero?": "Może do nas dołączysz, 1Hero?",
        "Thanks for the offer, Father, but I have something else to do.": "Dziękuję za zaproszenie, ojcze, ale mam coś do załatwienia.",
    },
    44: {
        "Don’t let them overwork you too much, stud.": "Nie daj im się zbytnio zaharować, przystojniaku.",
        "What? Who?": "Co? Komu?",
        "You can’t fool me, detective. I’ve been there and done that.": "Mnie nie oszukasz, detektywie. Znam to z własnego doświadczenia.",
    },
    45: {
        "I want ham! Chicken and beef are for poor people! If I can’t have ham, I’m going to kill myself!": "Chcę szynkę! Kurczak i wołowina są dla biedaków! Jeśli nie dostanę szynki, się zabiję!",
        "Calm down… They don’t serve ham here.": "Uspokój się… Nie podają tu szynki.",
        "I want ham, dammit!": "Chcę szynkę, do cholery!",
        "This doesn't look like ham to me.": "To mi nie wygląda na szynkę.",
        "Try it. It’s fancy ham… from Ratistan.": "Spróbuj. To wykwintna szynka… z Ratistanu.",
        "Ratistan? Sounds expensive.": "Ratistan? Brzmi drogo.",
        "Oh… Very expensive.": "Och… Bardzo drogo.",
        "Wow! It’s amazing!": "Wow! Jest przepyszna!",
        "You have great taste, sir. Will you leave a tip?": "Ma pan doskonały gust. Zostawi pan napiwek?",
        "Absolutely! This might be my new favorite restaurant.": "Oczywiście! Chyba właśnie znalazłem swoją nową ulubioną restaurację.",
        "Thank you, sir. You’re quite generous.": "Dziękuję, proszę pana. Jest pan bardzo hojny.",
        "This is disgusting! I will not eat it!": "To obrzydliwe! Nie będę tego jadł!",
    },
    46: {
        "Where is my burger?": "Gdzie jest mój burger?",
        "I told you! A burger! And no shake!... Milk makes me gassy.": "Mówiłem! Burger! I bez shake’a!... Mleko powoduje u mnie wzdęcia.",
        "Wow! That looks yummy!": "Wow! Wygląda pysznie!",
        "We’d appreciate a tip.": "Bylibyśmy wdzięczni za napiwek.",
        "Do I look like I have extra money laying around?": "Wyglądam, jakbym miał nadmiar pieniędzy?",
        "Fine… I’ll leave a tip.": "Dobra… Zostawię napiwek.",
        "You’re so kind, good sir.": "Jest pan taki miły.",
        "What!? I’m not eating this.": "Co!? Nie będę tego jadł.",
    },
    47: {
        "1Hero! You came!": "1Hero! Przyszedłeś!",
        "Judy! What the hell are you wearing?": "Judy! Co ty, do cholery, masz na sobie?",
        "What’s wrong? Is it too revealing?": "Co jest nie tak? Za dużo odsłania?",
        "Too revealing? You’re basically naked…": "Za dużo? Praktycznie jesteś naga…",
        "Now I see what’s happening…": "Teraz już rozumiem, co się dzieje…",
        "Hey! Where is my order!?": "Hej! Gdzie moje zamówienie!?",
        "I’m so sorry, sir.": "Bardzo przepraszam, proszę pana.",
        "I come to Dick’s for quality service! If I wanted bad service, I’d eat at the gym’s snack machine!": "Przychodzę do Dick’s dla obsługi na wysokim poziomie! Gdybym chciał kiepskiej obsługi, jadłbym przy automacie na siłowni!",
        "Shut up, Larry.": "Zamknij się, Larry.",
        "Hey! I am a paying customer.": "Hej! Jestem płacącym klientem.",
        "1Hero, please. I need tips.": "1Hero, proszę. Potrzebuję napiwków.",
        "This place is going downhill. My order is taking forever.": "Ta restauracja schodzi na psy. Na zamówienie czekam całą wieczność.",
        "I’m sorry. This is my first day.": "Przepraszam. To mój pierwszy dzień.",
        "My lunch break is nearly over and I’m still hungry.": "Zaraz kończy mi się przerwa na lunch, a wciąż jestem głodny.",
        "Lady! My mom is looking for me. Is my food ready yet?": "Proszę pani! Mama mnie szuka. Moje jedzenie jest już gotowe?",
        "I need help, 1Hero. I don’t know what I’m doing.": "Potrzebuję pomocy, 1Hero. Nie wiem, co robię.",
        "This job sucks, Judy. Are you sure you want to be here?": "Ta praca jest do bani, Judy. Na pewno chcesz tu pracować?",
        "I know I can do it… It’s just too stressful to learn… I need your help.": "Wiem, że dam radę… Po prostu nauka jest zbyt stresująca… Potrzebuję twojej pomocy.",
        "Okay… Let me give you a hand.": "Dobrze… Pomogę ci.",
        "It’s my manager!... I hope we did a good job.": "To mój kierownik!... Mam nadzieję, że dobrze nam poszło.",
        "I think we did.": "Chyba tak.",
        "Take a break, Judy. It’s slow now, but the dinner rush is not far away.": "Zrób sobie przerwę, Judy. Teraz jest spokojnie, ale zaraz zacznie się wieczorny ruch.",
        "He doesn’t seem upset.": "Nie wygląda na zdenerwowanego.",
        "How much did you make in tips so far?": "Ile dotąd dostałaś napiwków?",
        "The fat boy gave me a hundred dollars!": "Ten gruby chłopak dał mi sto dolarów!",
        "Wow! That’s really good!": "Wow! To naprawdę świetnie!",
        "What would you like, good sir?": "Co podać, szanowny panie?",
        "Heh… How about a couple of beers?": "Heh… Może parę piw?",
        "Now, that I can handle.": "Z tym sobie poradzę.",
    },
    49: {
        "I see what this is! You’re trying to fuck the waitress!": "Już wiem, co tu się dzieje! Próbujesz przelecieć kelnerkę!",
        "No! We were just… having a snack.": "Nie! My tylko… jedliśmy przekąskę.",
        "I’ve walked in on my fair share of people fucking to know what’s up.": "Wiele razy przyłapałem ludzi na seksie, więc wiem, co się święci.",
        "Wait… You have?": "Chwila… Naprawdę?",
        "I’m telling the manager!": "Powiem kierownikowi!",
        "No! Please! You can’t!": "Nie! Proszę! Nie możesz!",
        "Well… I can think of something I’d like in return for my silence.": "Cóż… W zamian za milczenie chciałbym coś dostać.",
        "Don’t even think about it.": "Nawet o tym nie myśl.",
        "I want a free ham every time I come to visit!": "Chcę darmową szynkę za każdym razem, gdy tu przyjdę!",
        "But… we don’t have ham.": "Ale… nie mamy szynki.",
        "Uhh… We do have ham. And I’m sure we can hook up this fine gentleman.": "Eee… Mamy szynkę. Na pewno coś dla tego miłego pana znajdziemy.",
        "Yes! You all have the best ham! See you tomorrow for lunch!": "Tak! Macie najlepszą szynkę! Do zobaczenia jutro na lunchu!",
        "What is he talking about?": "O czym on mówi?",
        "You know that rat we saw in your apartment?": "Pamiętasz tego szczura, którego widzieliśmy w twoim mieszkaniu?",
        "I cooked it and made… ‘’ham’’ with it.": "Przyrządziłem go i zrobiłem z niego… „szynkę”.",
        "Looks like the dinner crowd is starting… I better get back to work.": "Zaraz zacznie się wieczorny ruch… Lepiej wracam do pracy.",
        "You can do it, Judy. I believe in you.": "Dasz radę, Judy. Wierzę w ciebie.",
        "Thanks for lunch, 1Hero.": "Dzięki za lunch, 1Hero.",
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
    if context.get('source_kind') != 'map' or context.get('map_id') != 30 or row['id'] in known:
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
path = ROOT / 'drafts/custom-dialogue-map30-dicks-restaurant-followups-01.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8', newline='\n')
print(f'Wrote Map 30 Dick\'s restaurant follow-ups: {len(rows)} records across {len({r["context"]["event_id"] for r in rows})} events')
