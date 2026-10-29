#!/usr/bin/env python3
"""Build Polish drafts for the remaining mansion/undercover dialogue on Map 87."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
EVENTS = {
    13: {
        "Dammit. Where did they go?": "Cholera. Gdzie oni poszli?",
        "This is the back door…": "To tylne wejście…",
        "This mansion is nestled against Casula Forest. The forest is very thick here…": "Rezydencja leży tuż przy lesie Casula. W tym miejscu las jest bardzo gęsty…",
        "Shit… It might be difficult to track them.": "Cholera… Trudno będzie ich wytropić.",
        "We have to move, now!": "Musimy ruszać. Natychmiast!",
        "Send three of your officers into the forest.": "Wyślij trzech funkcjonariuszy do lasu.",
        "We’re going to need to post up and watch the exits.": "Musimy się rozstawić i obstawić wyjścia.",
        "Lillian’s safety is of the utmost importance right now.": "Bezpieczeństwo Lillian jest teraz najważniejsze.",
        "Greenly, Duffy, Alapopskalius, go chase after them.": "Greenly, Duffy, Alapopskalius, ruszajcie za nimi.",
        "And stick together!": "I trzymajcie się razem!",
        "The rest of you, come with me. We’re not letting that lunatic come back here.": "Reszta za mną. Nie pozwolimy temu szaleńcowi tu wrócić.",
        "Boy, am I glad you showed up, Miss Bhatt.": "Ależ się cieszę, że pani przyszła, panno Bhatt.",
        "David, I thought I told you to wait for backup.": "David, mówiłam ci, żebyś zaczekał na wsparcie.",
        "Blame Bobby.": "To wina Bobby’ego.",
        "We need to talk.": "Musimy porozmawiać.",
        "I’m too close to retirement to let you get me killed, 1Hero.": "Jestem zbyt blisko emerytury, żeby pozwolić ci mnie zabić, 1Hero.",
        "What the hell did I do?": "Co ja, do cholery, zrobiłem?",
        "Please let the others know about our new guests.": "Proszę, poinformuj pozostałych o naszych nowych gościach.",
        "Yes, madam.": "Tak jest, proszę pani.",
        "I’m so sorry about this, 1Hero.": "Bardzo mi przykro, 1Hero.",
        "It’s okay, Lillian. It seems your father has left you more than just a mansion.": "W porządku, Lillian. Wygląda na to, że ojciec zostawił ci coś więcej niż tylko rezydencję.",
        "What are you going to do? Are they going to come back for treasure?": "Co zamierzasz zrobić? Wrócą po skarb?",
        "My father has many treasures, but I am not aware of any treasure room…": "Mój ojciec miał wiele skarbów, ale nic mi nie wiadomo o żadnym skarbcu…",
        "At least, nothing that’s more valuable than what is easily seen.": "Przynajmniej nie o niczym cenniejszym niż to, co widać na pierwszy rzut oka.",
        "Clearly that man wanted something special.": "Najwyraźniej ten człowiek szukał czegoś wyjątkowego.",
        "He’s a Guild leader. He’d be looking for artifacts.": "To przywódca Gildii. Pewnie szuka artefaktów.",
        "I feel my safety has been compromised.": "Nie czuję się już bezpieczna.",
        "I hate to be the bearer of worse news, but I found Madalyn.": "Nie chcę przynosić jeszcze gorszych wieści, ale znalazłem Madalyn.",
        "And that’s bad news? Where is she?": "I to zła wiadomość? Gdzie jest?",
        "She was in the woods.": "Była w lesie.",
        "She’s still here? That can’t be true. What more would she want from my family?": "Wciąż tu jest? To niemożliwe. Czego jeszcze chce od mojej rodziny?",
        "Damn! Do you think she’s linked to that Guild guy?": "Cholera! Myślisz, że ma coś wspólnego z tym człowiekiem z Gildii?",
        "I don’t know… Something strange is happening.": "Nie wiem… Dzieje się coś dziwnego.",
        "What’s wrong, 1Hero? What did you see?": "Co się stało, 1Hero? Co widziałeś?",
        "This will sound crazy, but Madalyn disappeared…": "To zabrzmi niedorzecznie, ale Madalyn zniknęła…",
        "She just vanished into thin air.": "Po prostu rozpłynęła się w powietrzu.",
        "The forest is very thick. She could have easily evaded your search efforts.": "Las jest bardzo gęsty. Mogła łatwo wymknąć się waszym poszukiwaniom.",
        "It wasn’t like that. I was right up next to her… We had her cornered…": "To nie tak. Stałem tuż obok niej… Nie miała dokąd uciec…",
        "Then she just went up in a puff of smoke.": "A potem rozpłynęła się w obłoku dymu.",
        "She did something… She had a smoke bomb.": "Coś zrobiła… Miała bombę dymną.",
        "No! She was naked. She didn’t have anything on her.": "Nie! Była naga. Nie miała przy sobie niczego.",
        "This all sounds very strange.": "To wszystko brzmi bardzo dziwnie.",
        "Trust me. Madalyn is doing something… supernatural.": "Zaufaj mi. Madalyn robi coś… nadprzyrodzonego.",
        "I didn’t take you for the type to believe such things.": "Nie sądziłam, że wierzysz w takie rzeczy.",
        "I don’t!... I mean… I didn’t.": "Nie wierzę!... To znaczy… Nie wierzyłem.",
        "Something is going on in the forest and I need to figure it out.": "Coś się dzieje w lesie i muszę się dowiedzieć co.",
        "Maybe you should tell us what you know, 1Hero.": "Może powiesz nam, co wiesz, 1Hero.",
        "I don’t know what’s going on.": "Nie wiem, co się dzieje.",
        "You knew that woman… and she knew that Guild dude.": "Znałeś tę kobietę… a ona znała tego faceta z Gildii.",
        "You have a connection to the woman, 1Hero?": "Łączy cię coś z tą kobietą, 1Hero?",
        "That’s Nellie… She’s the mother of a friend of mine.": "To Nellie… Matka mojego znajomego.",
        "You talk about trust, yet you have this connection to the Guild that you didn’t tell us about?": "Mówisz o zaufaniu, a sam zataiłeś przed nami swoje powiązania z Gildią?",
        "It’s not like that. I just met the woman. I didn’t know anything about her connection to the Guild.": "To nie tak. Dopiero ją poznałem. Nie wiedziałem, że ma powiązania z Gildią.",
        "I didn’t know until recently.": "Dowiedziałem się o tym dopiero niedawno.",
        "I’m sure 1Hero has good intentions. I trust him.": "Jestem pewna, że 1Hero ma dobre intencje. Ufam mu.",
        "I’m going to figure this out. But until I do, you’re going to need to trust us…": "Rozwiążę tę sprawę. Ale do tego czasu musicie nam zaufać…",
        "We’ll make sure no one enters your home, Lillian.": "Dopilnujemy, żeby nikt nie wszedł do twojego domu, Lillian.",
        "I don’t like the idea of having surveillance. But I understand.": "Nie podoba mi się pomysł nadzoru, ale rozumiem.",
        "Thank you, Miss Bhatt, for showing up when you did. I could almost call your timing divine.": "Dziękuję, panno Bhatt, że przybyła pani w samą porę. Można by rzec, że to boskie zrządzenie.",
        "Just doing our job, Miss Wilkes.": "Po prostu wykonujemy swoją pracę, panno Wilkes.",
        "Well, 1Hero, it seems you were onto something, after all.": "Cóż, 1Hero, wygląda na to, że jednak coś podejrzewałeś.",
        "Just a…lucky hunch, Miss Bhatt.": "To tylko… szczęśliwe przeczucie, panno Bhatt.",
        "Stop it. I’m sure working for me can be infuriating.": "Przestań. Wiem, że praca dla mnie potrafi doprowadzić do szału.",
        "But I give credit where it’s due, and you saw something I missed. Good job.": "Ale doceniam zasługi, a ty zauważyłeś coś, co mi umknęło. Dobra robota.",
        "Err… thank you, Miss Bhatt.": "Eee… dziękuję, panno Bhatt.",
        "You have the green light to watch her.": "Masz zielone światło, żeby ją obserwować.",
        "Gain her trust, and find out what she knows.": "Zdobądź jej zaufanie i dowiedz się, co wie.",
        "About her father and the Guild?": "O jej ojcu i Gildii?",
        "About everything. Duncan Helmer didn’t break in here for no reason.": "O wszystkim. Duncan Helmer nie włamał się tu bez powodu.",
        "She has a connection to him.": "Coś ją z nim łączy.",
        "We need to know who she really is.": "Musimy się dowiedzieć, kim naprawdę jest.",
        "Sure thing. And thank you. I won’t let you down.": "Jasne. Dziękuję. Nie zawiodę pani.",
        "See that you don’t.": "Lepiej tego nie rób.",
        "We’ll need to throw Lillian off about our suspicions. Follow my lead.": "Musimy odwrócić uwagę Lillian od naszych podejrzeń. Rób, co mówię.",
        "Shall we?": "Zaczynamy?",
    },
    17: {
        "Get back or the commissioner gets a bullet in the head!": "Cofnijcie się, albo pani komisarz dostanie kulkę w głowę!",
        "1Hero!?": "1Hero!?",
        "Let her go, asshole!": "Puść ją, dupku!",
        "Heh! Nice shot, kiddo.": "Heh! Niezły strzał, mała.",
        "I knew I could depend on you, 1Hero.": "Wiedziałam, że mogę na tobie polegać, 1Hero.",
        "You have a lot of nerve, showing up here. Expect to assassinate me?": "Masz tupet, że tu przychodzisz. Zamierzasz mnie zabić?",
        "I helped 1Hero.": "Pomogłam 1Hero.",
        "Listen to the lady. She saved my life and probably yours.": "Posłuchaj jej. Uratowała mi życie, a pewnie i twoje.",
        "We followed your goon through the old bunker.": "Śledziliśmy twojego zbira przez stary bunkier.",
        "Uh, yeah. We totally tracked him down.": "No tak. Udało nam się go wytropić.",
        "That son of a bitch! Trying to get revenge on me, I’m sure.": "Skurwysyn! Na pewno chciał się na mnie zemścić.",
        "Well, he’s dead now.": "Cóż, już nie żyje.",
        "What the hell do we do now? Pretend he got away?": "Co my teraz, do cholery, zrobimy? Udawać, że uciekł?",
        "I say we kill Morgan and then bury both bodies in the forest.": "Zabijmy Morgan, a potem zakopmy oba ciała w lesie.",
        "Duncan! Your obsession with revenge is going to lead to my downfall.": "Duncan! Twoja obsesja na punkcie zemsty doprowadzi mnie do zguby.",
        "Do you want to sleep at night, Duncan?": "Chcesz móc spokojnie spać, Duncan?",
        "Haha! You’re the least of my concerns.": "Haha! Najmniej się o ciebie martwię.",
        "I have nothing left. You’ve backed me into a corner.": "Nie mam już nic. Zapędziłeś mnie w kozi róg.",
        "That was my money you took!": "Zabrałeś moje pieniądze!",
        "Charles gave it to me!": "Charles mi je dał!",
        "Leave us, Duncan… I’ll make the girl whole.": "Zostaw nas, Duncan… Wyrównam dziewczynie straty.",
        "Fine… We’ll do it your way.": "Dobra… Zrobimy po twojemu.",
        "How much money are we talking about?": "O jakich pieniądzach mówimy?",
        "Ten million dollars.": "Dziesięć milionów dolarów.",
        "I’ve got a gold treasure she can take.": "Mam złoty skarb, który może wziąć.",
        "Tell me you didn’t bring a piece of Nadia’s treasure here.": "Powiedz, że nie przyniosłeś tu fragmentu skarbu Nadii.",
        "I never touched it. I know the rules.": "Nigdy go nie tknąłem. Znam zasady.",
        "Morgan… You’ll get two million.": "Morgan… Dostaniesz dwa miliony.",
        "We’re even now, Morgan… But you cross me again and I’ll double the price on your head.": "Jesteśmy kwita, Morgan… Ale jeśli jeszcze raz mi podpadniesz, podwoję nagrodę za twoją głowę.",
        "Come on, Victor. Time to have you put into the ground.": "Chodź, Victor. Pora cię zakopać.",
        "Holy shit! I’m getting paid!...": "Ja pierdolę! Dostanę kasę!...",
        "Wait… How do you have the power to order Duncan around?": "Chwila… Skąd masz władzę, żeby rozkazywać Duncanowi?",
        "This is my operation now… Charles went crazy.": "Teraz to moja operacja… Charles postradał zmysły.",
        "I suspected something was wrong with him.": "Podejrzewałam, że coś jest z nim nie tak.",
        "You’re lucky he didn’t get you killed.": "Masz szczęście, że nie doprowadził do twojej śmierci.",
        "He almost did.": "Prawie mu się udało.",
        "How long have you been planning this… takeover?": "Od jak dawna planujesz ten… przewrót?",
        "The Guild was doomed to fall… Quite literally cursed.": "Gildia była skazana na upadek… Dosłownie ciążyła na niej klątwa.",
        "Thanks to you and Nellie, I’ve managed to put together something new.": "Dzięki tobie i Nellie udało mi się stworzyć coś nowego.",
        "This operation should be run by one individual… Not twelve.": "Tą organizacją powinna kierować jedna osoba… Nie dwanaście.",
        "So you’re the sole leader?": "Czyli jesteś jedyną przywódczynią?",
        "You and I are going to be very powerful, 1Hero.": "Razem będziemy bardzo potężni, 1Hero.",
        "Duncan’s not going to like that.": "Duncanowi się to nie spodoba.",
        "He has no choice. It’s either die, or be led by me.": "Nie ma wyboru. Albo zginie, albo będzie mi podlegał.",
        "If the Guild’s not dead… Am I still on the payroll?": "Skoro Gildia wciąż istnieje… Nadal jestem na liście płac?",
        "I could use a woman with your beauty.": "Przydałaby mi się kobieta taka piękna jak ty.",
        "I can fight. I’m damn good at it.": "Umiem walczyć. I to cholernie dobrze.",
        "Ella? You’ve got a ticket out. Why would you want back in?": "Ella? Masz szansę się stąd wydostać. Po co miałabyś wracać?",
        "To earn that eight million back.": "Żeby odzyskać te osiem milionów.",
        "Beautiful and persistent… I like it.": "Piękna i uparta… Podoba mi się.",
        "The Guild is finally under the rule of a female… This should be interesting.": "Gildią wreszcie rządzi kobieta… To będzie ciekawe.",
        "It’s a honeypot… Don’t go thinking you’ll be stealing artifacts.": "To miodowa pułapka… Nie myśl, że będziesz kraść artefakty.",
        "Let me worry about that, 1Hero.": "Zostaw to mnie, 1Hero.",
        "Nellie and you have been integral to this operation, but I could always use more loyal associates.": "Ty i Nellie odegraliście kluczową rolę w tej operacji, ale zawsze przydadzą mi się lojalni współpracownicy.",
        "I’m your woman.": "Jestem twoją kobietą.",
        "I killed that hitman. Isn’t that enough?": "Zabiłam tego płatnego mordercę. To nie wystarczy?",
        "I have my own way of testing those around me… just ask 1Hero.": "Mam własne sposoby sprawdzania ludzi wokół siebie… Zapytaj 1Hero.",
        "Remove your clothes, Morgan Deluna.": "Rozbierz się, Morgan Deluna.",
        "You can call me Ella.": "Mów mi Ella.",
    },
    33: {
        "Okay. It’s clear… Come on.": "Dobrze. Czysto… Chodź.",
        "Can I call you?": "Mogę do ciebie zadzwonić?",
        "Come to my office Monday. We can go over the findings there.": "Przyjdź do mojego biura w poniedziałek. Omówimy tam ustalenia.",
        "1Hero. Is everything okay?": "1Hero. Wszystko w porządku?",
        "Oh, uhh. There was a report of suspicious activity, but all is clear.": "Och, yyy. Zgłoszono podejrzaną aktywność, ale wszystko jest już w porządku.",
        "It’s getting late. Are you still working?": "Robi się późno. Nadal pracujesz?",
        "Just heading out now. I’m looking forward to the weekend.": "Właśnie wychodzę. Nie mogę się doczekać weekendu.",
        "I assume the officer outside will be staying?": "Zakładam, że funkcjonariusz na zewnątrz zostanie?",
        "Yes. He’ll keep his eye peeled for anything suspicious.": "Tak. Będzie wypatrywał wszystkiego, co podejrzane.",
        "Take care, 1Hero.": "Trzymaj się, 1Hero.",
    },
    34: {
        "No sign of Lillian. What’s next?": "Nie ma śladu po Lillian. Co teraz?",
        "Wait here. I’ll find Kimberly.": "Zaczekaj tutaj. Znajdę Kimberly.",
        "Holy shit! Kimberly Foxx!": "Ja pierdolę! Kimberly Foxx!",
        "You must be the maid.": "Ty pewnie jesteś pokojówką.",
        "Kimberly, meet Erica.": "Kimberly, poznaj Ericę.",
        "1Hero’s been telling me you’re helping him with his case.": "1Hero mówił mi, że pomagasz mu w śledztwie.",
        "There’s something going on here… There’s a secret area in this mansion.": "Coś się tu dzieje… W tej rezydencji jest tajne pomieszczenie.",
        "No shit. I’ve seen it.": "No raczej. Widziałam je.",
        "We have an opportunity to find our way inside and see for ourselves what’s going on.": "Możemy się tam dostać i na własne oczy zobaczyć, co się dzieje.",
        "We just need you to distract the guards long enough for us to find the entrance.": "Musisz tylko zająć strażników na tyle długo, żebyśmy znaleźli wejście.",
        "How long do you need?": "Ile czasu potrzebujecie?",
        "We know where the eye… the key is.": "Wiemy, gdzie jest oko… klucz.",
        "We just have to figure out where to use it.": "Musimy tylko ustalić, gdzie go użyć.",
        "I can buy you some time. But you better hurry.": "Mogę dać wam trochę czasu. Ale lepiej się pospieszcie.",
        "We’ve got this.": "Poradzimy sobie.",
        "There’s a guard in the next room. I’ll pull him away and then the clock starts.": "W następnym pokoju jest strażnik. Odciągnę go, a wtedy zaczniecie działać.",
        "But be careful.": "Tylko uważajcie.",
    },
    36: {
        "I’m going to keep tabs on the transmitters. Don’t forget we’re in this together.": "Będę monitorować nadajniki. Pamiętaj, że jesteśmy w tym razem.",
        "You’re right. This isn’t over… It’s just the beginning.": "Masz rację. To jeszcze nie koniec… To dopiero początek.",
        "I want to know what they are hiding.": "Chcę wiedzieć, co ukrywają.",
        "… Me too.": "… Ja też.",
        "See you around, 1Hero. Enjoy the news segment tonight.": "Do zobaczenia, 1Hero. Miłego oglądania wiadomości dziś wieczorem.",
        "For now.": "Na razie.",
        "What are they hiding down there, 1Hero?": "Co oni tam ukrywają, 1Hero?",
        "I saw the Toma piece and a pentagram on the floor…": "Widziałem fragment Toma i pentagram na podłodze…",
        "There were six hooded statues all surrounding it.": "Otaczało go sześć posągów w kapturach.",
        "What about the sound? Did you hear it?": "A ten dźwięk? Słyszałeś go?",
        "No… If we’re going to figure out what’s being hidden down there, I’ll need to figure out a way to get deeper.": "Nie… Jeśli mamy odkryć, co ukrywają na dole, muszę znaleźć sposób, by dostać się głębiej.",
        "How will you do it?": "Jak to zrobisz?",
        "The place is crawling with those leper dudes. It won’t be easy.": "To miejsce roi się od tych trędowatych typów. Nie będzie łatwo.",
        "I just hope to God I’m not some sort of planned sacrifice to Satan.": "Mam tylko nadzieję, że nie jestem przeznaczony na jakąś ofiarę dla Szatana.",
        "From the looks of things, the Toma pieces appear to be part of some ritual.": "Wygląda na to, że fragmenty Toma są częścią jakiegoś rytuału.",
        "I don’t know what it could be, but I can try and find out.": "Nie wiem, co to może być, ale spróbuję się dowiedzieć.",
        "You think it’s a Casula ritual?": "Myślisz, że to rytuał Casula?",
        "If it is, I’ll see what I can find.": "Jeśli tak, poszukam czegoś na ten temat.",
        "You better leave too. Lillian might ask what we’ve been discussing.": "Ty też lepiej już idź. Lillian może zapytać, o czym rozmawialiśmy.",
        "Good call.": "Słuszna uwaga.",
    },
    44: {
        "I thought my dick was getting crushed.": "Myślałem, że zmiażdżysz mi kutasa.",
        "You shot quite a lot of cum in my pussy, 1Hero.": "Wstrzyknąłeś mi do cipki mnóstwo spermy, 1Hero.",
        "A warm reminder of the loyalty the two of you have for this new and improved operation.": "Ciepłe przypomnienie o waszej lojalności wobec tej nowej, ulepszonej organizacji.",
        "Stop by this evening… I’ll make sure you get your two million.": "Wpadnij dziś wieczorem… Dopilnuję, żebyś dostała swoje dwa miliony.",
        "You have that kind of money?": "Masz aż tyle pieniędzy?",
        "Haha… Oh, 1Hero. There’s so much more than that.": "Haha… Och, 1Hero. Mam znacznie więcej.",
        "I didn’t do anything!": "Nic nie zrobiłem!",
        "You killed Duncan’s henchman… Andrea is pulling the strings…": "Zabiłeś człowieka Duncana… Andrea pociąga za sznurki…",
        "Duncan has no power.": "Duncan nie ma już władzy.",
        "You really think Duncan’s going to let this happen?": "Naprawdę myślisz, że Duncan na to pozwoli?",
        "A girl can dream, can’t she?": "Dziewczyna może sobie pomarzyć, prawda?",
        "Watch your back, Ella.": "Uważaj na siebie, Ella.",
        "I always have.": "Zawsze uważam.",
    },
    49: {
        "Are you wasting our time, 1Hero?": "Marnujesz nasz czas, 1Hero?",
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
    if context.get('source_kind') != 'map' or context.get('map_id') != 87 or row['id'] in known:
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
path = ROOT / 'drafts/custom-dialogue-map87-mansion-ambush-followups-01.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8', newline='\n')
print(f'Wrote Map 87 mansion follow-ups: {len(rows)} records across {len({r["context"]["event_id"] for r in rows})} events')
