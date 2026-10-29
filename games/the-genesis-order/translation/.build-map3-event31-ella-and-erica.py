import json
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step6.jsonl')
OUT = ROOT / 'drafts/custom-dialogue-map3-event-31-01.jsonl'
if OUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUT}')

MAP = {
    'This must be from Ella… And she sent a link in the message.': 'To musi być od Elli… Wysłała link w wiadomości.',
    'I wonder what she sent me.': 'Ciekawe, co mi wysłała.',
    'What!? Is she calling me?...': 'Co!? Dzwoni do mnie?...',
    'What do I say?': 'Co mam powiedzieć?',
    'Hello, Ella.': 'Cześć, Ello.',
    'It’s Erica. Did you already forget?': 'To Erica. Już zapomniałeś?',
    'Erica!?': 'Erica!?',
    'How many girls are you expecting a call from tonight?': 'Ile dziewczyn ma jeszcze do ciebie dziś zadzwonić?',
    'Oh, I just… got confused. That’s all.': 'Po prostu się… pomyliłem. Tyle.',
    'How’s your evening going?': 'Jak mija ci wieczór?',
    'I’m finished at the mansion. Don’t you want to meet up and discuss the details?': 'Skończyłam już w rezydencji. Może się spotkamy i omówimy szczegóły?',
    'Right now?': 'Teraz?',
    'When else?': 'A kiedy?',
    'But it’s so late.': 'Ale jest już tak późno.',
    'Tomorrow is Sunday. You can sleep in.': 'Jutro niedziela. Możesz się wyspać.',
    'Wait… So you’re coming over to my place?': 'Chwila… Czyli przyjdziesz do mnie?',
    'I’ve got to stop by the apartment and take a shower. Then I’ll be right over…': 'Muszę jeszcze wpaść do mieszkania i wziąć prysznic. Zaraz potem przyjadę…',
    'Where do you live?': 'Gdzie mieszkasz?',
    'Huh? Take a shower first?': 'Co? Najpierw prysznic?',
    'I stink! Don’t be in such a rush.': 'Śmierdzę! Nie spiesz się tak.',
    'That’s not what I meant.': 'Nie to miałem na myśli.',
    'Uhh… I’ll text you the address.': 'Eee… Wyślę ci adres.',
    'See you tonight, 1Hero.': 'Do zobaczenia wieczorem, 1Hero.',
    'Damn. I better make sure my place looks good for Erica.': 'Cholera. Lepiej ogarnę mieszkanie, zanim przyjdzie Erica.',
    'I wonder what she has to say that can’t wait until tomorrow?': 'Ciekawe, co takiego chce mi powiedzieć, że nie może poczekać do jutra.',
    'How exciting! Your new friend is coming over to your place, late at night!': 'Ale ekscytujące! Nowa znajoma wpada do ciebie późno w nocy!',
    'What do you think is going to happen?': 'Jak myślisz, co się wydarzy?',
    'I’m sure it’ll be wholesome activities…': 'Na pewno spędzimy czas w całkiem niewinny sposób…',
    'Right, 1Hero?': 'Prawda, 1Hero?',
    '…': '…',
    'Erica is pretty damned cute…': 'Erica jest naprawdę cholernie urocza…',
    'We’ll see.': 'Zobaczymy.',
    'Don’t forget, 1Hero. I am always watching.': 'Nie zapominaj, 1Hero. Cały czas cię obserwuję.',
    'Evening is approaching, 1Hero. Are you going to attend Mass?': 'Zbliża się wieczór, 1Hero. Idziesz na mszę?',
    'Huh? At Eve Cathedral?... I think I’ll pass.': 'Co? Do Katedry Ewy?... Chyba sobie odpuszczę.',
    'Not only have you worked on the Sabbath, but now you’re going to deny the Lord praise?': 'Nie dość, że pracowałeś w szabat, to jeszcze odmówisz Panu chwały?',
    'Hey, I’m helping fight crime. I think he’ll understand.': 'Hej, pomagam walczyć z przestępczością. Myślę, że zrozumie.',
    'You are truly on a noble quest, but you can not neglect fellowship.': 'Masz naprawdę szlachetną misję, ale nie możesz zaniedbywać wspólnoty wiernych.',
    'From the sound of things, I don’t think many people are going to Eve Cathedral these days.': 'Z tego, co słyszę, ostatnio niewiele osób chodzi do Katedry Ewy.',
    'So many souls, doomed for eternal torment.': 'Tyle dusz skazanych na wieczne męki.',
    'Eternal torment?': 'Wieczne męki?',
    'An unwashed soul will spend an eternity filled with sin, indulging in unholy desires, surrounded by those who have fallen from the path of light.': 'Nieoczyszczona dusza spędzi wieczność w grzechu, oddając się nieświętym żądzom i otoczona tymi, którzy zeszli ze ścieżki światła.',
    'You will dine on lard and candied cuisine, lacking in nourishment while the music of the devil plays loudly into your ears.': 'Będziesz zajadać się smalcem i kandyzowanymi słodyczami, pozbawionymi wartości odżywczych, a muzyka diabła będzie dudnić ci w uszach.',
    'Smoke and fungus will fill your body, and your mind will travel far from God, to places beyond anything you can imagine.': 'Dym i grzyby wypełnią twoje ciało, a umysł oddali się od Boga, trafiając w miejsca, których nie potrafisz sobie wyobrazić.',
    'So… What’s the alternative?': 'No dobrze… Jaka jest alternatywa?',
    'Give your soul to the Lord and you will spend eternity singing praise to God! Completely protected from desire!': 'Oddaj duszę Panu, a spędzisz wieczność, śpiewając chwałę Bogu! Będziesz całkowicie wolny od żądz!',
    'Well. I think the choice is obvious.': 'Cóż. Wybór wydaje się oczywisty.',
    'I agree! I’m so happy you’ve seen the light.': 'Zgadzam się! Tak się cieszę, że przejrzałeś na oczy.',
    'Someone is calling…': 'Ktoś dzwoni…',
    '1Hero! Are you there?': '1Hero! Jesteś tam?',
    'Ella? Are you okay?': 'Ella? Wszystko w porządku?',
    'I heard someone at my door, and when I answered it, they ran away!': 'Ktoś zapukał do moich drzwi. Kiedy otworzyłam, uciekł!',
    'What did they look like?': 'Jak wyglądał?',
    'They were wearing a red shirt and carrying a box…': 'Miał czerwoną koszulę i niósł jakieś pudełko…',
    'I think they may have stolen a package off my porch, but I don’t know what it was.': 'Chyba ukradł paczkę z mojego ganku, ale nie wiem, co w niej było.',
    'I’ll come over. Stay put.': 'Już jadę. Zostań na miejscu.',
    'Could it have been Larry from the gym?': 'To mógł być Larry z siłowni?',
    'It’s getting dark… Should I go to church with Chloe?': 'Robi się ciemno… Może pójdę z Chloe do kościoła?',
    'My phone’s ringing… I wonder who it is.': 'Dzwoni telefon… Ciekawe, kto to.',
    'Lillian? Is everything okay?': 'Lillian? Wszystko w porządku?',
    'I hope I’m not interrupting you. Is now a good time to talk?': 'Mam nadzieję, że ci nie przeszkadzam. Możemy teraz porozmawiać?',
    'Sure. What’s on your mind?': 'Jasne. O co chodzi?',
    'I’ve invited Erica Abraham to the mansion for dinner…': 'Zaprosiłam Ericę Abraham na kolację do rezydencji…',
    'I would be honored if you would join her and accompany her to my mansion.': 'Byłabym zaszczycona, gdybyś jej towarzyszył i przyprowadził ją do mojej rezydencji.',
    'Oh, well…': 'No cóż…',
    'Did you have other plans?': 'Masz inne plany?',
    'No. I can come over.': 'Nie. Mogę przyjść.',
    'Fantastic. Please meet Erica and assure her safe arrival. The sun is setting soon.': 'Wspaniale. Spotkaj się z Ericą i dopilnuj, żeby bezpiecznie dotarła do mnie. Niedługo zajdzie słońce.',
    'Sure. I’ll head right over.': 'Jasne. Już jadę.',
    'Thank you, detective.': 'Dziękuję, detektywie.',
    'Dinner? Maybe she’s lonely.': 'Kolacja? Może czuje się samotna.',
    'I feel bad that I can’t join Chloe…': 'Szkoda, że nie mogę dołączyć do Chloe…',
    'Maybe I am a workaholic.': 'Może jestem pracoholikiem.',
    'So, you’re skipping Mass?': 'Czyli opuszczasz mszę?',
    'You tell me. Should I skip dinner with Lillian or go to church?': 'Sama powiedz. Mam opuścić kolację z Lillian czy pójść do kościoła?',
    'I sense there’s something you need to do at the Wilkes Mansion.': 'Wyczuwam, że musisz coś zrobić w rezydencji Wilkesów.',
    'See? It’s not my fault. It’s fate.': 'Widzisz? To nie moja wina. Tak chciał los.',
    'You possess something with great power, 1Hero. I can sense it.': 'Masz przy sobie coś o wielkiej mocy, 1Hero. Wyczuwam to.',
    'Are you talking about my artifact?': 'Mówisz o moim artefakcie?',
    'I don’t know what it is you’ve found, but it emanates with dark power.': 'Nie wiem, co znalazłeś, ale emanuje mroczną mocą.',
    'It’s a Casula artifact… Or that’s what Jon says.': 'To artefakt Casuli… A przynajmniej tak twierdzi Jon.',
    'It made me… do something really dirty.': 'Sprawił, że… zrobiłem coś naprawdę nieprzyzwoitego.',
    'You were in great pain. I can sense it. What happened to you?': 'Bardzo cierpiałeś. Wyczuwam to. Co ci się stało?',
    'It made me cum a whole lot.': 'Spuściłem się chyba z milion razy.',
    'Come?': 'Doszedłeś?',
    'Uhh… I nearly drowned my best friend in semen. That’s not normal.': 'Eee… Prawie utopiłem najlepszą przyjaciółkę w spermie. To chyba nie jest normalne.',
    'Is she okay?': 'Nic jej nie jest?',
    'Yeah, she’s fine. I think she enjoyed being covered in it… It’s hard to explain.': 'Tak, wszystko z nią dobrze. Chyba podobało jej się, że ją oblałem… Trudno to wyjaśnić.',
    'I can’t say I understand human behavior, but it’s nice that you’re able to cover your friends in semen. It sounds lovely.': 'Nie rozumiem ludzkich zachowań, ale miło, że możesz oblewać przyjaciół spermą. Brzmi wspaniale.',
    'You shouldn’t have fought with that man, 1Hero. You’re not ready.': 'Nie powinieneś był z nim walczyć, 1Hero. Nie jesteś jeszcze gotowy.',
    'He got lucky. I can take him.': 'Miał szczęście. Dam mu radę.',
    'You are strong, and you have much to accomplish, but your ego is getting in the way.': 'Jesteś silny i masz wiele do zrobienia, ale przeszkadza ci twoje ego.',
    'I’m just having a bad day, Arianna. That’s all.': 'Po prostu mam kiepski dzień, Arianno. Tyle.',
    'I sense guilt in your heart. What have you done?': 'Wyczuwam w twoim sercu poczucie winy. Co zrobiłeś?',
    'Nothing.': 'Nic.',
    'You can not hide your feelings from me, 1Hero.': 'Nie ukryjesz przede mną swoich uczuć, 1Hero.',
    'My lead for the Wilkes case got away, I lost to a skinny asshole and I saw my boss naked…': 'Uciekł mi podejrzany w sprawie Wilkesów, przegrałem z chudym dupkiem i zobaczyłem nagą szefową…',
    'You tell me what’s on my heart.': 'Sama powiedz, co mi leży na sercu.',
    'Oh, my! A series of unfortunate events, for sure.': 'Ojej! Niezła seria niefortunnych zdarzeń.',
    'I will help you with the Wilkes case, but I can not help you with stinky buttholes or nude overseers.': 'Pomogę ci w sprawie Wilkesów, ale nie poradzę nic na śmierdzące tyłki ani nagich przełożonych.',
    'I said skinny asshole. Not stinky asshole.': 'Powiedziałem „chudy dupek”, nie „śmierdzący dupek”.',
    'It sounds like your world has an abundance of unique butt problems…': 'Wygląda na to, że w twoim świecie nie brakuje rozmaitych problemów z tyłkami…',
    'An unfortunate outcome of human kind’s fall from grace.': 'Niefortunny skutek upadku człowieka.',
    'Fall from grace?': 'Upadku człowieka?',
    'The mother of your kind, Eve…': 'Ewa, matka twojego rodzaju…',
    'She was a naughty girl.': 'Była niegrzeczną dziewczynką.',
    'Are you telling me the story from Genesis is true?': 'Chcesz mi powiedzieć, że historia z Księgi Rodzaju jest prawdziwa?',
    'Do you find it hard to believe?': 'Trudno ci w to uwierzyć?',
    'A talking snake, a poison apple… I would say it’s unbelievable…': 'Mówiący wąż, zatrute jabłko… Powiedziałbym, że to niewiarygodne…',
    'But then again, I’m talking to an angel. So, who am I to judge?': 'Ale z drugiej strony rozmawiam z aniołem. Kimże jestem, żeby to oceniać?',
    'When the Lord created mankind, his creation, Eve, disobeyed his orders.': 'Gdy Pan stworzył ludzkość, Ewa, jego dzieło, nie posłuchała jego rozkazów.',
    'I know the story.': 'Znam tę historię.',
    'Then you know why you’re doomed to a life of misery.': 'A więc wiesz, dlaczego czeka cię życie pełne cierpienia.',
    'Eve ate the fruit of knowledge.': 'Ewa zjadła owoc poznania.',
    'Not all of life is misery, Arianna.': 'Nie całe życie jest pasmem cierpień, Arianno.',
    'A story about knowledge being the enemy sounds like brainwashing to me.': 'Opowieść, w której wiedza jest wrogiem, brzmi jak pranie mózgu.',
    'Brainwashing!? Do you think I’m brainwashed?': 'Pranie mózgu!? Myślisz, że ktoś wyprał mi mózg?',
    'No way. You seem perfectly normal and not at all naive.': 'Skądże. Wydajesz się zupełnie normalna i wcale naiwna.',
    'Thank you, 1Hero! You’re so kind!': 'Dziękuję, 1Hero! Jesteś taki miły!',
    'Why do I feel like the middleman all of a sudden?': 'Dlaczego nagle czuję się jak pośrednik?',
    'What’s wrong, 1Hero? I sense conflict.': 'Co się stało, 1Hero? Wyczuwam, że coś cię dręczy.',
    'Where do I start? I’m walking a tightrope between Melissa and Andrea while also balancing Heather and Chloe on my shoulders.': 'Od czego zacząć? Chodzę po linie między Melissą a Andreą, a do tego dźwigam na barkach Heather i Chloe.',
    'That’s incredible! You are a man of many talents.': 'Niesamowite! Masz wiele talentów.',
    'I don’t mean it literally… I mean, my relationships are getting complicated.': 'Nie mówię dosłownie… Chodzi mi o to, że moje relacje robią się coraz bardziej skomplikowane.',
    'Oh, I see.': 'A, rozumiem.',
    'I feel like no matter what I do, someone’s going to get upset.': 'Mam wrażenie, że cokolwiek zrobię, ktoś się obrazi.',
    'You carry a lot of burden, but do not forget your purpose…': 'Dźwigasz wielki ciężar, ale nie zapominaj o swoim przeznaczeniu…',
    'A grave evil is upon us, and only you can stop it.': 'Zagraża nam straszliwe zło i tylko ty możesz je powstrzymać.',
    'Thanks, Arianna. I feel so much better now.': 'Dzięki, Arianno. Od razu mi lepiej.',
    'Wonderful! A healthy mind is a healthy soul.': 'Wspaniale! W zdrowym umyśle zdrowa dusza.',
    'Who’s calling me? I wonder if Melissa is mad I’m not in the office.': 'Kto dzwoni? Ciekawe, czy Melissa jest zła, że nie ma mnie w biurze.',
    '1Hero. We have a problem.': '1Hero. Mamy problem.',
    'Tell me about it. I saw Kimberly at the mansion.': 'Mów mi. Widziałem Kimberly w rezydencji.',
    'She wanted an interview and she came to the station.': 'Chciała przeprowadzić wywiad, więc przyszła na posterunek.',
    'Do you want me back at the station?': 'Mam wracać na posterunek?',
    'No. I convinced her to meet at my house. I don’t want that woman anywhere near the station or the mansion.': 'Nie. Namówiłam ją, żeby spotkała się ze mną w domu. Nie chcę jej ani w pobliżu posterunku, ani rezydencji.',
    'I can head over. When is the meeting?': 'Mogę przyjechać. O której spotkanie?',
    'Let’s not be too formal. I invited her over for drinks.': 'Nie bądźmy tacy oficjalni. Zaprosiłam ją na drinka.',
    'Let’s stay on her good side.': 'Lepiej nie zrażać jej do siebie.',
    'I get it. When should I be there?': 'Rozumiem. Kiedy mam przyjechać?',
    'I need something from you.': 'Potrzebuję, żebyś coś dla mnie zrobił.',
    'You’re near the mansion, correct?': 'Jesteś niedaleko rezydencji, prawda?',
    'Uhh, sure.': 'Eee, tak.',
    'I’m making a very special drink and I need raw aloe.': 'Przygotowuję wyjątkowy napój i potrzebuję świeżego aloesu.',
    'A drink with aloe?': 'Napój z aloesem?',
    'It’s… a special mixture.': 'To… specjalna mieszanka.',
    'The plant grows out west. Grab one and come over…': 'Ta roślina rośnie na zachodzie. Zerwij jedną i przyjedź…',
    'Kimberly will be here when you arrive.': 'Kiedy przyjedziesz, Kimberly już tu będzie.',
    'Don’t linger.': 'Nie ociągaj się.',
    'I guess Andrea is trying to make a good impression on Kimberly.': 'Chyba Andrea próbuje zrobić dobre wrażenie na Kimberly.',
    'If we’re going to convince Kimberly to look the other way, this better be one hell of a drink.': 'Jeśli mamy przekonać Kimberly, żeby przymknęła oko, ten drink musi być naprawdę mocny.',
}

known = set()
for line in MERGED.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    if row['translation'].strip():
        known.add(row['id'])
rows = []
missing = set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    source = row['source_text'].strip()
    if (context.get('source_kind') != 'map' or context.get('map_id') != 3
            or context.get('event_id') != 31 or row['id'] in known):
        continue
    if not source or source.startswith('/') or source in {'…', '...', '..'}:
        continue
    translation = MAP.get(source)
    if translation is None:
        missing.add(source)
        continue
    row['translation'] = translation
    rows.append(row)
if missing:
    raise SystemExit('Unmapped Map 3 event 31 strings: ' + repr(sorted(missing)))
OUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote Map 3 event 31 Ella/Erica dialogue: {len(rows)} records from {len(MAP)} source strings')
