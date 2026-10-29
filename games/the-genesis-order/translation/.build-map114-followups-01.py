#!/usr/bin/env python3
"""Build Polish drafts for remaining player-facing dialogue on Map 114."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map114-followups-01.jsonl'
TRANSLATIONS = {
    'Uhh… Nice place.': 'Eee… Ładne miejsce.',
    'I don’t need the comments.': 'Nie potrzebuję komentarzy.',
    'What? I’m just saying… could use a cleaning.': 'Co? Tylko mówię… przydałoby się tu posprzątać.',
    'Ugh. Wait here. I’ll change and get the files.': 'Ugh. Zaczekaj tutaj. Przebiorę się i przyniosę akta.',
    'You have them here?': 'Masz je tutaj?',
    'Just wait here.': 'Po prostu zaczekaj.',
    'What a mess… She could use a maid.': 'Ale bałagan… Przydałaby jej się pokojówka.',
    'The computer is on. She’s been working on Saturday?': 'Komputer jest włączony. Pracowała w sobotę?',
    'Do I dare try and guess her password?': 'Czy odważę się zgadnąć jej hasło?',
    'This is what we have. Let’s get to work.': 'To wszystko, co mamy. Do roboty.',
    'There’s one more thing.': 'Jest jeszcze jedna sprawa.',
    'I found an ID on the floor in the kitchen.': 'Znalazłem dowód osobisty na podłodze w kuchni.',
    'You were in the mansion’s kitchen?': 'Byłeś w kuchni rezydencji?',
    'I’ve been around the place a few times.': 'Bywałem tu kilka razy.',
    'Hmm… Lorenzo D. Scott.': 'Hmm… Lorenzo D. Scott.',
    'Expired last year. Not sure how it got into the Wilkes’ kitchen unless it belongs to one of those creepy lepers.': 'Stracił ważność w zeszłym roku. Nie wiem, jak trafił do kuchni Wilkesów, chyba że należy do jednego z tych upiornych trędowatych.',
    'Let’s run the name.': 'Sprawdźmy to nazwisko.',
    'Your computer is plugged into the station’s network?': 'Twój komputer jest podłączony do sieci komisariatu?',
    'A privilege I’m sure you’ll get once Andrea promotes you.': 'Jestem pewien, że dostaniesz takie uprawnienia, gdy Andrea cię awansuje.',
    'You think I have a promotion coming?': 'Myślisz, że dostanę awans?',
    'I have no idea what you and her have planned.': 'Nie mam pojęcia, co ty i ona planujecie.',
    'We have a match.': 'Mamy dopasowanie.',
    'What does it say?': 'Co tam jest napisane?',
    'Eclipse Guild… A warrant was issued last year but… no one was found.': 'Gildia Eclipse… W zeszłym roku wydano nakaz, ale… nikogo nie znaleziono.',
    'Well… It’s clear to me what’s going on.': 'Cóż… Już wiem, co tu się dzieje.',
    'And what would that be?': 'A mianowicie?',
    'Those lepers are former Guild… All of them.': 'Ci trędowaci to byli członkowie Gildii… Wszyscy.',
    'All of them?': 'Wszyscy?',
    'Charles was a Guild leader and those were his men…': 'Charles był przywódcą Gildii, a oni byli jego ludźmi…',
    'Madalyn came in and took over. Brainwashing the whole crew.': 'Madalyn wkroczyła i przejęła kontrolę. Wyprała mózgi całej ekipie.',
    'Kimura isn’t going to want to hear that.': 'Kimura nie zechce tego słyszeć.',
    'It’s the truth.': 'To prawda.',
    'It’s your theory.': 'To tylko twoja teoria.',
    'Come on. Let’s go over what we have.': 'Chodź. Przejrzyjmy to, co mamy.',
    'But you did want it?': 'Ale chciałeś tego?',
    'Would it kill you to smile every now and then?': 'Czy uśmiech od czasu do czasu tak bardzo by ci zaszkodził?',
    'I have never in my life been driven so insane by one person.': 'Nigdy w życiu jedna osoba nie doprowadzała mnie do takiego szału.',
    'I’ll take that as a compliment.': 'Uznam to za komplement.',
    'I’ll dry your damned clothes. Let’s get moving so we don’t keep Andrea waiting.': 'Wysuszę te cholerne ubrania. Ruszajmy, żeby nie kazać Andrei czekać.',
    'Holy hell! That woman is a good fuck.': 'O cholera! Ale ta kobieta świetnie się pieprzy.',
    'I better read up. I can’t let Andrea down.': 'Lepiej się przygotuję. Nie mogę zawieść Andrei.',
    'Lillian! She was here! She… took my cum!': 'Lillian! Była tu! Ona… zabrała moją spermę!',
    'How the hell did she get in here?... Where the hell did she go?': 'Jak, do cholery, się tu dostała?... Gdzie, do cholery, poszła?',
    'She’s a demon! She’s not human!': 'Ona jest demonem! Nie jest człowiekiem!',
    'She used her powers to teleport!': 'Użyła swoich mocy, żeby się teleportować!',
    'So, as far as we know, Charles died of a heart attack.': 'Z tego, co wiemy, Charles zmarł na zawał serca.',
    'That’s crazy!': 'To szaleństwo!',
    'I guess that’s the official answer.': 'Chyba taka jest oficjalna wersja.',
    'You said this place was haunted. You’re not as wrong as I thought.': 'Mówiłeś, że to miejsce jest nawiedzone. Nie byłeś tak daleki od prawdy, jak myślałem.',
    'Duncan Helmer is targeting the mansion.': 'Duncan Helmer wziął na cel rezydencję.',
    'A demon?... What’s going on?': 'Demon?... Co tu się dzieje?',
    'And don’t forget that Charles had a search warrant served at his home…': 'Nie zapominaj, że Charlesowi doręczono nakaz przeszukania domu…',
    'Shit! Erica!': 'Cholera! Erica!',
    'A connection with the Guild.': 'Powiązanie z Gildią.',
    'Erica?': 'Erica?',
    'There’s a lot of evidence here. I suspect he was involved with the Guild. But a leader?...': 'Jest tu sporo dowodów. Podejrzewam, że był zamieszany w działalność Gildii. Ale żeby był jej przywódcą?...',
    'She’s with Kimberly, in the Channel 4 building.': 'Jest z Kimberly w budynku Channel 4.',
    'Do we bring up Madalyn?': 'Wspominamy o Madalyn?',
    'We have to make sure she’s okay!...': 'Musimy się upewnić, że nic jej nie jest!...',
    'No. If we aren’t positive, we aren’t telling Kimura.': 'Nie. Jeśli nie mamy pewności, nie mówimy Kimurze.',
    'We still have some time.': 'Mamy jeszcze trochę czasu.',
    'You have somewhere else to be?': 'Masz jeszcze coś do załatwienia?',
    'I’ll meet you at Andrea’s at seven.': 'Spotkamy się u Andrei o siódmej.',
    'What the hell were you thinking? We were so close to finding a way into the Guild bunker.': 'Co ty sobie, do cholery, myślałeś? Byliśmy o krok od znalezienia wejścia do bunkra Gildii.',
    'It’s over, Melissa. Andrea will take it from here.': 'Po wszystkim, Melissa. Andrea się tym zajmie.',
    'Like hell, she is. I don’t trust her. Why isn’t she telling me what’s going on?': 'Akurat. Nie ufam jej. Czemu nie mówi mi, co się dzieje?',
    'Maybe you’re not trustworthy.': 'Może tobie nie można ufać.',
    'Fuck… You’re right… Andrea is not following the law.': 'Kurwa… Masz rację… Andrea łamie prawo.',
    'What did she tell you?': 'Co ci powiedziała?',
    'I’m part of her undercover team now.': 'Teraz jestem częścią jej zespołu działającego pod przykrywką.',
    'She’s using you.': 'Wykorzystuje cię.',
    'Well, what the hell am I supposed to do? This is my only option to stay on the case.': 'No to co, do cholery, mam zrobić? To jedyna szansa, żebym dalej prowadził tę sprawę.',
    'What are her orders? What’s she hiding?': 'Jakie ma rozkazy? Co ukrywa?',
    'You know I can’t tell you.': 'Wiesz, że nie mogę ci powiedzieć.',
    'We’re past that now. I’m going behind her back with or without you.': 'To już nie ma znaczenia. Zrobię to za jej plecami, z tobą albo bez ciebie.',
    'She wants me to kill everyone… The whole North Santiva Eclipse Guild.': 'Chce, żebym zabił wszystkich… Całą Gildię Eclipse w North Santiva.',
    'Assassinate them?': 'Mam ich zamordować?',
    'And make it look like a bust gone bad.': 'I upozorować, że obława poszła nie tak.',
    'She doesn’t want them talking.': 'Nie chce, żeby zaczęli mówić.',
    'The Guild has been here for years. She doesn’t want that on her record.': 'Gildia działa tu od lat. Nie chce, żeby odbiło się to na jej reputacji.',
    'What am I going to do? I don’t want to do it.': 'Co mam zrobić? Nie chcę tego robić.',
    'We don’t need Andrea to make a bust. I can do it without her.': 'Nie potrzebujemy Andrei do przeprowadzenia obławy. Damy radę bez niej.',
    'You’re going to make a move on the warehouse first? Before Andrea’s orders?': 'Chcesz najpierw uderzyć na magazyn? Zanim Andrea wyda rozkaz?',
    "It wouldn't be easy. But we have to know what we're getting into.": 'To nie będzie łatwe. Ale musimy wiedzieć, na co się piszemy.',
    'But you’ll be fired.': 'Ale cię zwolnią.',
    'Perhaps… Unless Miss Foxx were to credit the both of us with the bust.': 'Być może… Chyba że panna Foxx przypisze nam obojgu zasługę za tę obławę.',
    'I like the way you think. Let’s become the heroes before Andrea has any chance to paint the narrative.': 'Podoba mi się, jak myślisz. Zostańmy bohaterami, zanim Andrea zdąży przedstawić sprawę po swojemu.',
    'Andrea is only protecting herself. If she loses her job as commissioner, it’s her own fault.': 'Andrea tylko się chroni. Jeśli straci stanowisko komisarz, sama będzie sobie winna.',
    'So what are we going to do?': 'Więc co robimy?',
    'I need access to the Guild files.': 'Potrzebuję dostępu do akt Gildii.',
    'You don’t have access?': 'Nie masz dostępu?',
    'David and I lost access last week.': 'David i ja straciliśmy dostęp w zeszłym tygodniu.',
    'So, we need to hack in.': 'Czyli musimy się włamać do systemu.',
    'I need Andrea’s credentials.': 'Potrzebuję danych logowania Andrei.',
    'How do we get that?': 'Jak je zdobędziemy?',
    'Andrea doesn’t memorize her passwords. She keeps everything on a thumb drive.': 'Andrea nie zapamiętuje haseł. Trzyma wszystko na pendrivie.',
    'You want me to steal her thumb drive?': 'Chcesz, żebym ukradł jej pendrive’a?',
    'You’re goddamned right I can handle it.': 'Jasne, że sobie z tym poradzę.',
    'I like your style, Canmore.': 'Podoba mi się twój styl, Canmore.',
    'Where is it? At her house?': 'Gdzie on jest? U niej w domu?',
    'I don’t know. But you’re closer to her than I am. You’re our best bet.': 'Nie wiem. Ale jesteś jej bliższy niż ja. To nasza najlepsza szansa.',
    'The clock is ticking. I could be called to raid the bunker at any moment.': 'Czas ucieka. W każdej chwili mogą mnie wezwać do szturmu na bunkier.',
    'Then I suggest you hurry.': 'W takim razie lepiej się pospiesz.',
    'Get me that thumb drive and I’m sure I can find something that will give us the warrant we need to start the raid early.': 'Daj mi ten pendrive, a na pewno znajdę coś, co da nam podstawę do uzyskania nakazu i wcześniejszego rozpoczęcia obławy.',
    'I hope this works. There are lives depending on it.': 'Mam nadzieję, że się uda. Czyjeś życie od tego zależy.',
    'That’s new.': 'To coś nowego.',
    'Just hurry.': 'Po prostu się pospiesz.',
    'Steal the thumb drive from Andrea so we can break into the Guild files.': 'Ukradnij pendrive Andrei, żebyśmy mogli włamać się do akt Gildii.',
    'I won’t get in your way if you feel the need to help that thief. But don’t expect me to like it.': 'Nie będę cię powstrzymywać, jeśli chcesz pomóc tej złodziejce. Ale nie licz, że mi się to spodoba.',
    'Good luck with Andrea.': 'Powodzenia z Andreą.',
    'We’ll both need a little luck, I think.': 'Chyba oboje będziemy potrzebować trochę szczęścia.',
    'Well? Did you get the thumb drive?': 'No i? Masz pendrive’a?',
    'She left it in her safe. I can’t believe I was able to break in…': 'Zostawiła go w sejfie. Nie mogę uwierzyć, że udało mi się włamać…',
    'Let’s see if the password works.': 'Zobaczmy, czy hasło zadziała.',
    'Aren’t you interested in how I got it?': 'Nie ciekawi cię, jak go zdobyłem?',
    'What? Stop distracting me.': 'Co? Nie rozpraszaj mnie.',
    'Give me more time… Stop bothering me.': 'Daj mi więcej czasu… Przestań mi przeszkadzać.',
    'Nothing new.': 'Nic nowego.',
    'What the hell is that noise?': 'Co to, do cholery, za hałas?',
    'My place is haunted.': 'U mnie straszy.',
    'Who the hell…?': 'Kto, do cholery…?',
    'Haha. No, really. What is it?': 'Haha. Nie, tak serio, co to jest?',
    'There are some small issues in the kitchen.': 'W kuchni jest kilka drobnych problemów.',
    'What kind of issues?': 'Jakich problemów?',
    'Hey! Get out of my house!': 'Hej! Wynoś się z mojego domu!',
    'Diana!?': 'Diana!?',
    'I tailed you here, 1Hero… I need help.': 'Śledziłam cię, 1Hero… Potrzebuję pomocy.',
    'Who the hell are you?...': 'Kim, do cholery, jesteś?...',
    'Wait!... You’re a Guild thief.': 'Chwila!... Jesteś złodziejem Gildii.',
    'Former Guild thief, detective.': 'Byłą złodziejką Gildii, detektywie.',
    'Henry has been captured by Duncan.': 'Duncan schwytał Henry’ego.',
    'You know these people, 1Hero?': 'Znasz tych ludzi, 1Hero?',
    'Enemies of the Guild and the ones who plan to assassinate Duncan.': 'To wrogowie Gildii i ludzie, którzy planują zamach na Duncana.',
    'Well, the plan failed.': 'Cóż, plan się nie powiódł.',
    'I saw Henry in the bunker… He saved my life unintentionally.': 'Widziałam Henry’ego w bunkrze… Nieświadomie uratował mi życie.',
    'I know this might send us to jail, but I’m out of options.': 'Wiem, że możemy za to trafić do więzienia, ale nie mam wyboru.',
    'I’m not on the force anymore. So unless Melissa arrests you…': 'Nie służę już w policji. Chyba że Melissa cię aresztuje…',
    'Can you help us?...': 'Możesz nam pomóc?...',
    'Do you know where the entrance is to the bunker?': 'Wiesz, gdzie jest wejście do bunkra?',
    'The warehouse.': 'W magazynie.',
    'If we take her to a judge, she can help us justify a warrant…': 'Jeśli zaprowadzimy ją przed sędziego, pomoże nam uzasadnić wniosek o nakaz…',
    'We can raid the warehouse, arrest the Guild and then this would all be over.': 'Możemy przeprowadzić nalot na magazyn, aresztować członków Gildii i zakończyć tę sprawę.',
    'It would be the last thing Henry and I do before going to prison.': 'To będzie ostatnia rzecz, jaką zrobimy z Henrym, zanim trafimy do więzienia.',
    'If you want to save him, then end the Guild here and now.': 'Jeśli chcesz go uratować, musisz raz na zawsze skończyć z Gildią.',
    'Is there any other way? I’d wager that Jon has every angle covered. He’s going to be clean.': 'Jest jakiś inny sposób? Założę się, że Jon zabezpieczył się na każdą ewentualność. Nie będzie można mu niczego zarzucić.',
    'When you get the call from Andrea to move in, the whole Guild will be waiting in the warehouse.': 'Kiedy Andrea wezwie nas do akcji, cała Gildia będzie czekała w magazynie.',
    'Yeah, and Nellie and I will be there.': 'Tak, Nellie i ja też tam będziemy.',
    'Whatever Andrea has planned, get Nellie to stall…': 'Cokolwiek planuje Andrea, każ Nellie grać na zwłokę…',
    'I’ll send a unit there to investigate an anonymous tip.': 'Wyślę tam patrol, żeby sprawdził anonimowe zgłoszenie.',
    'The officers will arrive first.': 'Funkcjonariusze dotrą tam pierwsi.',
    'And the Guild will be unarmed.': 'A Gildia będzie bez broni.',
    'Arrests with no deaths.': 'Aresztowania bez ofiar.',
    'Including Henry.': 'W tym Henry’ego.',
    'Should I care?': 'A co mnie to obchodzi?',
    'Nellie’s not going to risk getting sent back to prison. She’s willing to do what it takes…': 'Nellie nie zaryzykuje powrotu do więzienia. Zrobi wszystko, co będzie trzeba…',
    'She’s going to kill them all.': 'Ona ich wszystkich zabije.',
    'We simply take that risk…': 'Po prostu podejmujemy ryzyko…',
    'Andrea needs to be held accountable for fucking up this case.': 'Andrea musi odpowiedzieć za spieprzenie tej sprawy.',
    'I won’t stand by and let her play executioner to save face.': 'Nie będę bezczynnie patrzeć, jak robi z siebie kata, żeby ratować własną skórę.',
    'You said he saved your life… Get him out of there, 1Hero.': 'Mówiłaś, że uratował ci życie… Wyciągnij go stamtąd, 1Hero.',
    'Meet me where you met the girl in black. I can help.': 'Spotkaj się ze mną tam, gdzie spotkałeś dziewczynę w czerni. Mogę pomóc.',
    'I should have you arrested.': 'Powinienem cię aresztować.',
    'You’ll have to catch me first.': 'Najpierw musisz mnie złapać.',
    'Girl in black?': 'Dziewczyna w czerni?',
    'I… I don’t know what she means.': 'Ja… Nie wiem, o czym ona mówi.',
    'Don’t bullshit me.': 'Nie wciskaj mi kitu.',
    'I’ll talk to Nellie… She won’t like it, but maybe I can talk her into stalling.': 'Porozmawiam z Nellie… Nie spodoba jej się to, ale może namówię ją, żeby grała na zwłokę.',
    'Don’t get into trouble, 1Hero. You’ve been a pain in the ass, but you’ve been a good man, I must admit.': 'Nie pakuj się w kłopoty, 1Hero. Byłeś upierdliwy, ale muszę przyznać, że jesteś porządnym facetem.',
    'Don’t throw that away.': 'Nie zaprzepaść tego.',
    'I’m still a good man, Melissa.': 'Wciąż jestem porządnym facetem, Melissa.',
    'Give me the word, and I’ll have officers swarm the warehouse.': 'Daj mi znać, a wyślę policjantów do magazynu.',
    'I will. It’s the right thing to do.': 'Tak zrobię. To właściwa decyzja.',
    'All done! Your shitty condo is slightly less shitty now.': 'Gotowe! Twoje gówniane mieszkanie jest teraz odrobinę mniej gówniane.',
    'I’m busy. Come back later.': 'Nie mam teraz czasu. Wróć później.',
    'Damn! That went from zero to a hundred real quick.': 'Cholera! Ale to błyskawicznie nabrało tempa.',
    'Can’t you see I’m horny?': 'Nie widzisz, że jestem napalona?',
    'What can we do, 1Hero? The odds are stacked against us. No one’s going to believe what’s happening until it’s too late.': 'Co możemy zrobić, 1Hero? Jesteśmy na straconej pozycji. Nikt nie uwierzy, co się dzieje, dopóki nie będzie za późno.',
    'We’ll stop Lilith and destroy the Toma Leolo.': 'Powstrzymamy Lilith i zniszczymy Tomę Leolo.',
}

known = set()
for path in (ROOT / 'drafts').rglob('*.jsonl'):
    if path == OUTPUT:
        continue
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
        or context.get('map_id') != 114
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
    raise SystemExit('Unmapped Map 114 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 178:
    raise SystemExit(f'Expected exactly 178 natural dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 114 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
