#!/usr/bin/env python3
"""Build a separate reviewed-draft batch for selected Map 44 mansion events."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl')
OUT = ROOT / 'drafts/custom-dialogue-map44-mansion-followups-01.jsonl'

EVENTS = {
    27: {
        "Enough hide-and-seek.": "Dość tej zabawy w chowanego.",
        "Well, if it isn’t the new lady of the manor. We’ve had our eye on you.": "No proszę, nowa pani na włościach. Mamy cię na oku.",
        "You found me; now kindly get out.": "Znalazłeś mnie. A teraz bądź tak miły i wynoś się.",
        "Ha! Kitten has claws.": "Ha! Koteczka ma pazurki.",
        "I suggest you watch yourself, young lady.": "Lepiej uważaj, panienko.",
        "Tell me where the gold digger is before I start removing those little claws.": "Powiedz, gdzie jest ta łowczyni fortuny, zanim obetnę ci te pazurki.",
        "I’m sure I don’t know what you’re talking about.": "Nie mam pojęcia, o czym mówisz.",
        "Why have you invaded my father’s home?": "Po co wtargnęliście do domu mojego ojca?",
        "Charles' daughter?...": "Córka Charlesa?...",
        "You have no business here. Whatever dealings you had with my father, it’s over.": "Nie macie tu czego szukać. Cokolwiek łączyło was z moim ojcem, to już koniec.",
        "Yes… I can see the resemblance. You’ve got his eyes.": "Tak… Widzę podobieństwo. Oczy masz po nim.",
        "People said I had my father’s eyes…": "Mówili, że mam oczy po ojcu…",
        "Thinking about it, I suppose I have his whole head.": "Jak się nad tym zastanowić, chyba całą głowę mam po nim.",
        "Uhh, boss. The freezer stopped working last month.": "Eee, szefie. Zamrażarka zepsuła się już w zeszłym miesiącu.",
        "Thanks for reminding me, you insensitive dolt!": "Dzięki, że mi przypomniałeś, ty bezduszny tępaku!",
        "Madam, what would you like me to do?": "Proszę pani, co mam zrobić?",
        "Oh ho, who is this ugly fella?": "Oho, a kto to taki brzydal?",
        "Certainly he must be one of Charles’... associates.": "To musi być jeden ze wspólników Charlesa…",
        "And by the look of him, he’s deeply afflicted by the Curse of Nadia, but…": "Wygląda na to, że Klątwa Nadii mocno go dotknęła, ale…",
        "Why isn’t he dead yet?": "Dlaczego jeszcze nie umarł?",
        "I beg your pardon?": "Słucham?",
        "I’d have guessed Nadia’s curse would have done its job by now…": "Myślałem, że klątwa Nadii już dawno zrobiła swoje…",
        "How has the Curse not killed him yet?": "Jak to możliwe, że klątwa go jeszcze nie zabiła?",
        "I do not believe in fairy tales or curses.": "Nie wierzę ani w bajki, ani w klątwy.",
        "But perhaps it is his life of purpose and devotion that grants him respite from an early grave.": "Ale może życie pełne celu i oddania uchroniło go przed przedwczesną śmiercią.",
        "What is it that you want, Mr…?": "Czego pan chce, panie…?",
        "You mean to tell me that dear old daddy didn’t tell you about Uncle Helmer?": "Chcesz mi powiedzieć, że kochany tatuś nie wspomniał ci o wujku Helmerze?",
        "My father is dead, and I have no business with you.": "Mój ojciec nie żyje i nie mam z tobą żadnych interesów.",
        "I’m afraid you’re wrong, Lillian.": "Obawiam się, że się mylisz, Lillian.",
        "I don’t know you. I want nothing to do with you.": "Nie znam cię. Nie chcę mieć z tobą nic wspólnego.",
        "Where’s the treasure room?": "Gdzie jest skarbiec?",
        "Don’t play dumb. We’re here for the goods and unless you plan to join your father in hell, we’re not leaving without them.": "Nie udawaj głupiej. Przyszliśmy po skarby i nie wyjdziemy bez nich, chyba że chcesz dołączyć do ojca w piekle.",
        "There is no treasure room, I assure you. And that means you’ve no further business here.": "Zapewniam, że nie ma tu skarbca. A to oznacza, że nie macie już tu czego szukać.",
        "Thank you for the visit, but I must insist you and your friends depart at once.": "Dziękuję za wizytę, ale nalegam, żebyście natychmiast opuścili ten dom.",
        "Hmm. Perhaps a more immediate example is necessary.": "Hmm. Chyba przyda się bardziej bezpośredni przykład.",
        "Do you know where this carpet is from, Miss Wilkes?": "Wie pani, skąd pochodzi ten dywan, panno Wilkes?",
        "It helps to know where the original is from if you need to order a new one.": "Warto wiedzieć, skąd pochodzi oryginał, jeśli trzeba zamówić nowy.",
        "And cursed blood can be so difficult to clean. Trust me, I know.": "A przeklętą krew tak trudno się czyści. Proszę mi wierzyć, wiem coś o tym.",
        "Everybody, freeze!": "Wszyscy, stać!",
        "Duncan Helmer, you and your friends are under arrest.": "Duncan Helmer, ty i twoi ludzie jesteście aresztowani.",
        "What the hell is going on? This place was supposed to be clear.": "Co tu się, do cholery, dzieje? Miejsce miało być czyste.",
        "Calm down. He’s got a pea shooter…": "Spokojnie. Ma tylko pukawkę…",
        "I think the odds are still in our favor.": "Chyba nadal mamy przewagę.",
        "Oh shit.": "O cholera.",
        "More unwanted guests?": "Kolejni nieproszeni goście?",
        "What was that about odds?": "A co mówiłeś o przewadze?",
        "You, up on the balcony. I expect if you were armed, you’d have already drawn your weapon.": "Ty, na balkonie. Gdybyś był uzbrojony, już dawno wyciągnąłbyś broń.",
        "Higher ground and superior numbers only work when you’re armed, gentlemen.": "Przewaga wysokości i liczebności działa tylko wtedy, gdy ma się broń, panowie.",
        "A single officer armed with a pistol? I should feel insulted.": "Jeden policjant z pistoletem? Powinienem poczuć się urażony.",
        "Dammit, Bobby, I told you we needed to wait for backup.": "Cholera, Bobby, mówiłem ci, że mieliśmy poczekać na wsparcie.",
        "You didn’t tell me they had machine guns, old man.": "Nie mówiłeś, że mają karabiny maszynowe, staruszku.",
        "They have machine guns.": "Oni mają karabiny maszynowe.",
        "Don’t do something you’ll regret, Duncan.": "Nie rób czegoś, czego będziesz żałował, Duncan.",
        "My only regret is how long this is taking.": "Żałuję tylko, że to tak długo trwa.",
        "It’s time to end this unplanned rendezvous.": "Czas zakończyć to nieplanowane spotkanie.",
        "Duncan, we’ve gotta go. More police are on the way.": "Duncan, musimy się zbierać. Nadjeżdża więcej policjantów.",
        "Doubtful, my tattooed little dove.": "Wątpię, moja wytatuowana gołąbeczko.",
        "I told you she was with them, 1Hero.": "Mówiłem ci, że ona jest z nimi, 1Hero.",
        "Stop right there, missy!": "Stój, panienko!",
        "Good one, Bobby. Doing great.": "Świetnie, Bobby. Idzie ci doskonale.",
        "How about we kill them and then you and I can find Charles’ vault.": "Może ich zabijemy, a potem znajdziemy skarbiec Charlesa?",
        "How does that sound, sweetheart?": "Co ty na to, kochanie?",
        "You fuckin’ meathead. What if you’re wrong? Are you prepared to take on the entire police force?": "Ty tępy osiłku. A co, jeśli się mylisz? Chcesz się zmierzyć z całą policją?",
        "I’m willing to take that chance, Nellie.": "Zaryzykuję, Nellie.",
        "Shit… What do we do?": "Cholera… Co robimy?",
        "You’ll regret this, Duncan!": "Pożałujesz tego, Duncan!",
        "I’ll shoot! I’ll do it!": "Strzelę! Zrobię to!",
        "Bobby, your safety is on.": "Bobby, masz włączony bezpiecznik.",
        "Kill them all. Leave no one alive.": "Zabijcie wszystkich. Nie zostawcie nikogo przy życiu.",
        "Drop the weapons! Now!": "Rzućcie broń! Natychmiast!",
        "What are the odds looking like now, big man?": "No i jak teraz wyglądają twoje szanse, wielkoludzie?",
        "Duncan Helmer, you’re under arrest.": "Duncan Helmer, jesteś aresztowany.",
        "Not today, detective!": "Nie dzisiaj, detektywie!",
    },
    102: {
        "They’re breaking through the barrier!": "Przebijają się przez barierę!",
        "Let them come. We’ll see who is ready to serve their new mother.": "Niech przychodzą. Zobaczymy, kto jest gotów służyć swojej nowej matce.",
        "Open up! It’s over!": "Otwierać! To koniec!",
        "What the hell happened to you?": "Co się z tobą, do cholery, stało?",
        "Nevermind that!": "Nieważne!",
        "Looks like you’re going to jail, Duncan.": "Wygląda na to, że trafisz do więzienia, Duncan.",
        "I don’t know what’s going on, but one of you promised me an escape.": "Nie wiem, co tu się dzieje, ale ktoś z was obiecał, że pomoże mi uciec.",
        "We’re leaving now.": "Wychodzimy. Natychmiast.",
        "1Hero, come with us!": "1Hero, chodź z nami!",
        "I can only take one.": "Mogę zabrać tylko jedną osobę.",
        "Everyone, freeze!": "Wszyscy, stać!",
        "What took you so long!?": "Czemu to tyle trwało!?",
        "1Hero, how did you get in here? Where is everyone?": "1Hero, jak się tu dostałeś? Gdzie wszyscy?",
        "They escaped.": "Uciekli.",
        "Arrest him!": "Aresztować go!",
        "Hey! Get your hands off of me!": "Hej! Ręce precz!",
        "Until we find the commissioner, you aren’t going anywhere.": "Dopóki nie znajdziemy komisarza, nigdzie się stąd nie ruszysz.",
        "Who the hell is this?": "Kto to, do cholery, jest?",
        "Shit… The Rose woman… She’s here?": "Cholera… Pani Rose… Jest tutaj?",
        "I think you’re mistaken.": "Chyba się mylisz.",
        "I’ll explain everything later.": "Wszystko wyjaśnię później.",
        "Arianna!": "Arianna!",
        "Chase her! She’s a wanted murderer!": "Za nią! Jest poszukiwaną morderczynią!",
        "And what are you doing here, Detective Bhatt?": "A co pani tu robi, detektyw Bhatt?",
        "I was looking for the Guild… Same as you.": "Szukam Gildii… Tak samo jak wy.",
        "Where are the henchmen? Where’s the leader?": "Gdzie są poplecznicy? Gdzie ich przywódca?",
        "Listen… There are things in this mansion you need to stay away from if you value your life.": "Słuchajcie… W tej rezydencji są rzeczy, od których powinniście trzymać się z daleka, jeśli wam życie miłe.",
        "How do we get out of this one, 1Hero?": "Jak się z tego wykaraskamy, 1Hero?",
        "Come on. You’re both under arrest.": "No już. Oboje jesteście aresztowani.",
        "Search the mansion. Look for anyone hiding.": "Przeszukać rezydencję. Sprawdźcie, czy ktoś się nie ukrywa.",
        "Come on, you two.": "No już, wy dwoje.",
    },
    93: {
        "It’s clear.": "Czysto.",
        "You brought a cop into my home?": "Przyprowadziłeś policjanta do mojego domu?",
        "And a priest.": "I księdza.",
        "Take them away.": "Zabrać ich.",
        "Hey! Stay away from me!": "Hej! Trzymaj się ode mnie z daleka!",
        "Duncan! You can’t take him! We need him!": "Duncan! Nie możesz go zabrać! Jest nam potrzebny!",
        "You’re in big trouble… Canmore.": "Masz poważne kłopoty… Canmore.",
        "He doesn’t know, does he?": "On nie wie, prawda?",
        "Know what?": "Czego?",
        "1Hero!? Miss Bhatt!?": "1Hero!? Pani Bhatt!?",
        "Andrea! Kimberly and Erica… They are in the mansion.": "Andrea! Kimberly i Erica… Są w rezydencji.",
        "Why did you come here? Why didn’t you tell us?": "Po co tu przyszliście? Czemu nam nie powiedzieliście?",
        "Because that’s not our only problem.": "Bo to nie nasz jedyny problem.",
        "Get that fucking reporter! Now!": "Dorwać tego pierdolonego reportera! Już!",
        "You shouldn’t be here, Melissa.": "Nie powinno cię tu być, Melissa.",
        "Don’t let anyone leave.": "Nikomu nie pozwólcie wyjść.",
        "Be careful with Miss Foxx.": "Uważaj na pannę Foxx.",
        "I’m not stupid.": "Nie jestem głupia.",
        "Andrea! We need Father Solomon!": "Andrea! Potrzebujemy ojca Solomona!",
        "What are you going on about?": "O czym ty mówisz?",
        "I can’t believe this is what you’ve been doing… Helping the Guild.": "Nie mogę uwierzyć, że tym się zajmowałaś… Pomagałaś Gildii.",
        "You are not privy to this part of the case. You’re in big trouble for being here.": "Nie powinnaś znać szczegółów tej części śledztwa. Masz poważne kłopoty, że tu przyszłaś.",
        "Enough! We need to go to the rift! Now!": "Dość! Musimy iść do szczeliny! Natychmiast!",
        "There’s nothing down there, 1Hero.": "Na dole nic nie ma, 1Hero.",
        "There is! And we need to stop it!": "Jest! I musimy to powstrzymać!",
        "Well? Go on…": "No i co? Dalej…",
        "But we need Father.": "Ale potrzebujemy ojca.",
        "There’s nothing down there. It’s empty.": "Na dole nic nie ma. Jest pusto.",
    },
    24: {
        "1Hero! Look!...": "1Hero! Spójrz!...",
        "A hidden staircase.": "Ukryte schody.",
        "I think we’ve found it.": "Chyba znaleźliśmy.",
        "Hey! Don’t get seen!": "Hej! Nie daj się zauważyć!",
        "1Hero! Hurry up! They are coming!": "1Hero! Pospiesz się! Idą!",
        "Come on! It’s too heavy to move!...": "No dalej! To za ciężkie, żeby to przesunąć!...",
        "How the hell did they open this?": "Jak oni, do cholery, to otworzyli?",
        "We found it… And there’s a Toma Leolo fragment down there.": "Znaleźliśmy to… Na dole jest fragment Toma Leolo.",
        "Wait… Did you two fuck?": "Chwila… Pieprzyliście się?",
        "I take it you have some experience with these stones.": "Domyślam się, że masz doświadczenie z tymi kamieniami.",
        "You need to get her out of here. Lillian is back!": "Musisz ją stąd zabrać. Lillian wróciła!",
        "We can talk about it later. For now, let’s get you away from the mansion before someone sees you.": "Porozmawiamy o tym później. Na razie zabierzmy cię z rezydencji, zanim ktoś cię zobaczy.",
        "Ah! Get back!": "Ach! Cofnij się!",
        "Demons!": "Demony!",
        "What did you do with Bobby? Where are the girls?": "Co zrobiliście z Bobbym? Gdzie są dziewczyny?",
        "The amulets are gone! How did you find them?": "Amulety zniknęły! Jak je znaleźliście?",
        "If you want them, they are inside the church.": "Jeśli ich chcecie, są w kościele.",
        "Fuck you! You know we won’t go near there.": "Pieprz się! Wiesz, że nie zbliżymy się do kościoła.",
        "Don’t come any closer unless you want to lose that body of yours.": "Nie zbliżaj się, jeśli nie chcesz stracić swojego ciała.",
        "You brought the witch.": "Przyprowadziłeś czarownicę.",
        "We’re here to bring Erica’s body to Hell.": "Przybyliśmy zabrać ciało Eriki do piekła.",
        "Then let me take your burden from you. We’ll bring her to where she needs to go.": "Pozwól więc, że zdejmę z ciebie ten ciężar. Zabierzemy ją tam, gdzie powinna trafić.",
        "Fuck no! I will only answer to Lilith herself.": "Nie ma mowy! Będę słuchać tylko samej Lilith.",
        "I said stay back!": "Mówiłem, żebyś się nie zbliżał!",
    },
    25: {
        "Don’t tell me how to lead my men.": "Nie pouczaj mnie, jak mam dowodzić moimi ludźmi.",
        "These are not your men.": "To nie są twoi ludzie.",
        "They are now.": "Teraz już są.",
        "Don’t you forget what I did for you. The Guild is yours, but I’m calling the shots.": "Nie zapominaj, co dla ciebie zrobiłem. Gildia jest twoja, ale ja tu wydaję rozkazy.",
        "Of course, Your Highness.": "Oczywiście, wasza wysokość.",
        "Don’t be a smart ass, Duncan.": "Nie pyskuj, Duncan.",
        "Pst. 1Hero.": "Psst. 1Hero.",
        "Kimberly!?": "Kimberly!?",
        "Shhh! Don’t let them hear us.": "Ciii! Nie pozwól im nas usłyszeć.",
        "Stay away from Morgan. Let her go. And for the love of God, stay away from the priest.": "Trzymaj się z dala od Morgan. Puść ją. I na miłość boską, nie zbliżaj się do księdza.",
        "I told you – they came sniffing around here.": "Mówiłem ci — zaczęli tu węszyć.",
        "Then turn them back…": "To ich odeślij…",
        "I’ve already dealt with the priest…": "Już się zająłem księdzem…",
        "You’re being loud, Duncan… Try being quiet for a change.": "Głośno się zachowujesz, Duncan… Spróbuj dla odmiany siedzieć cicho.",
        "I’ve got a business to run. Maybe you should mind your own.": "Prowadzę interesy. Może zajmij się swoimi.",
        "You won’t have anything if you keep this up.": "Jeśli tak dalej pójdzie, nic ci nie zostanie.",
        "What the hell are you doing here, Kimberly?": "Co ty tu, do cholery, robisz, Kimberly?",
        "I told you. Trying to find Lillian.": "Mówiłem ci. Próbuję znaleźć Lillian.",
        "Can’t you see the place is crawling with Guild people?": "Nie widzisz, że roi się tu od ludzi z Gildii?",
        "Seems your case isn’t over.": "Wygląda na to, że twoja sprawa jeszcze się nie skończyła.",
        "You’re not supposed to know about any of this…": "Nie powinnaś nic o tym wiedzieć…",
        "What are you going to say on the news?": "Co powiesz w wiadomościach?",
        "Hopefully I have bigger fish to fry.": "Mam nadzieję, że będę mieć ważniejsze sprawy na głowie.",
        "Hey! Wait!": "Hej! Zaczekaj!",
    },
    51: {
        "Shit… It would be a lot easier if Erica was working today.": "Cholera… Byłoby o wiele łatwiej, gdyby Erica dziś pracowała.",
        "I wonder if she’d be able to come over and help me get by the guards.": "Ciekawe, czy mogłaby tu przyjechać i pomóc mi ominąć strażników.",
        "I’ll give her a call.": "Zadzwonię do niej.",
        "Erica. How’s your weekend been?": "Erica. Jak minął ci weekend?",
        "Hungover!": "Mam kaca!",
        "That Hannah girl sure can drink.": "Ta Hannah potrafi wypić.",
        "Yeah, she’s a wild one…": "No, niezła z niej wariatka…",
        "Hey, would you happen to be heading to the mansion soon?": "Hej, wybierasz się może niedługo do rezydencji?",
        "It’s the weekend, 1Hero. I’m not going to work.": "Jest weekend, 1Hero. Nie idę do pracy.",
        "What if I said I needed your help?": "A gdybym powiedział, że potrzebuję twojej pomocy?",
        "You’re working?": "Pracujesz?",
        "Not exactly. I just need to check something out.": "Niezupełnie. Muszę tylko coś sprawdzić.",
        "You’re working.": "Czyli jednak pracujesz.",
        "No! I swear! I’m… spying.": "Nie! Przysięgam! Ja… prowadzę obserwację.",
        "Are you whispering?": "Szepczesz?",
        "Yeah. I’m at the mansion now. I need to get to the kitchen.": "Tak. Jestem już w rezydencji. Muszę dostać się do kuchni.",
        "Lillian won’t be expecting me.": "Lillian się mnie nie spodziewa.",
        "She’s not around… Just show up and help me get by a couple lepers.": "Nie ma jej w pobliżu… Po prostu przyjdź i pomóż mi przemknąć obok kilku trędowatych.",
        "What are we trying to do?": "Co właściwie próbujemy zrobić?",
        "I need to fix something that’s broken… Something that will help me spy on Lillian.": "Muszę naprawić pewną zepsutą rzecz… Dzięki niej będę mógł szpiegować Lillian.",
        "Anything naughty going to happen?": "Czy wydarzy się coś niegrzecznego?",
        "You’re lucky I’m bored. Meet me at my place and we’ll head over together.": "Masz szczęście, że się nudzę. Spotkajmy się u mnie i pojedziemy tam razem.",
        "See ya in a bit.": "Do zobaczenia za chwilę.",
    },
}

known = {r['id'] for r in map(json.loads, MERGED.read_text(encoding='utf-8').splitlines()) if r['translation'].strip()}
for batch in (ROOT / 'drafts').glob('*.jsonl'):
    for line in batch.read_text(encoding='utf-8').splitlines():
        if line.strip():
            row = json.loads(line)
            if row.get('translation', '').strip():
                known.add(row['id'])

rows = []
missing = set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    event_id = context.get('event_id')
    if context.get('source_kind') != 'map' or context.get('map_id') != 44 or event_id not in EVENTS or row['id'] in known:
        continue
    source = ' '.join(row['source_text'].strip().split())
    if not source or source.startswith('/') or source in {'…', '...', '..'} or not any(char.isalpha() for char in source):
        continue
    translation = EVENTS[event_id].get(source)
    if translation is None:
        translation = EVENTS[event_id].get(source.replace('’', "'"))
    if translation is None:
        translation = EVENTS[event_id].get(source.replace("'", '’'))
    if translation is None:
        missing.add((event_id, source))
        continue
    row['translation'] = translation
    rows.append(row)
if missing:
    raise SystemExit('Unmapped strings: ' + repr(sorted(missing)))
if OUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUT}')
OUT.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8', newline='\n')
print(f'Wrote Map 44 mansion follow-ups: {len(rows)} records across {len(EVENTS)} events')
