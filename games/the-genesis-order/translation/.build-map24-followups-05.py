#!/usr/bin/env python3
"""Build Polish drafts for Map 24 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map24-followups-05.jsonl'
TRANSLATIONS = {
    "Oh, 1Hero. You scared me.": "Och, 1Hero. Przestraszyłeś mnie.",
    "Sorry, Heather.": "Przepraszam, Heather.",
    "It’s getting very late…": "Robi się bardzo późno…",
    "That was awkward.": "To było niezręczne.",
    "We’re going to watch your news show!": "Obejrzymy twój program informacyjny!",
    "If it’s okay with Mom.": "Jeśli mama pozwoli.",
    "Of course. You ladies are free to watch it here if you’d like. I totally understand why you’d want to stay away from the church.": "Oczywiście. Możecie go obejrzeć tutaj, jeśli chcecie. Rozumiem, czemu chcecie trzymać się z dala od kościoła.",
    "I’m just thankful that the Lord protected all of us.": "Jestem tylko wdzięczna, że Pan nas wszystkich ochronił.",
    "Enjoy the news segment.": "Miłego oglądania programu.",
    "Heading somewhere, Heather?": "Wybierasz się gdzieś, Heather?",
    "I’m going to Carol’s to help her cook.": "Idę do Carol pomóc jej gotować.",
    "We should invite Ella!": "Powinniśmy zaprosić Ellę!",
    "Ella?": "Ellę?",
    "She's a new friend of mine... A professional gamer of sorts.": "To moja nowa przyjaciółka… Coś w rodzaju profesjonalnej graczki.",
    "A gamer?": "Graczki?",
    "She’s a cool girl.": "Fajna dziewczyna.",
    "Just don’t leave Hannah out. She’ll throw a fit.": "Tylko nie pomijaj Hannah. Dostanie szału.",
    "Of course Hannah’s invited.": "Oczywiście Hannah jest zaproszona.",
    "What about dinner? Are you girls planning anything?": "A co z kolacją? Planujecie coś?",
    "I can cook something up for everyone.": "Mogę coś ugotować dla wszystkich.",
    "I can help. I used to cook at Saint Dame.": "Mogę pomóc. Gotowałam kiedyś w Saint Dame.",
    "Sounds like your evening is planned.": "Wygląda na zaplanowany wieczór.",
    "I’ll make sure there are no messes.": "Dopilnuję, by nie było bałaganu.",
    "We’ll be clean.": "Będziemy grzeczne.",
    "I better get going. Have fun.": "Lepiej już pójdę. Bawcie się dobrze.",
    "1Hero… Can you invite Ella?": "1Hero… Możesz zaprosić Ellę?",
    "I’ll let the other girls know there’s a party. What’s for dinner?": "Dam znać pozostałym dziewczynom, że jest impreza. Co na obiad?",
    "Chicken?": "Kurczak?",
    "How about chicken stir-fry? I think I remember how to make it.": "Może kurczak w stir-fry? Chyba pamiętam, jak to zrobić.",
    "I’ll let the girls know.": "Dam znać dziewczynom.",
    "Carol! You told her!?": "Carol! Powiedziałaś jej!?",
    "Of course I did. You knew I would.": "Oczywiście, że tak. Wiedziałaś, że tak zrobię.",
    "How much did you tell her?": "Ile jej powiedziałaś?",
    "Don’t worry. I didn’t tell her that you shot a load in front of me.": "Spokojnie. Nie powiedziałam jej, że spuściłeś się przede mną.",
    "It was more than just that.": "To było coś więcej.",
    "Calm down. I’m not going to go spilling too many secrets.": "Uspokój się. Nie wygadam zbyt wielu sekretów.",
    "Besides, I think Heather would get mighty jealous of our little fun.": "Poza tym myślę, że Heather byłaby potwornie zazdrosna o naszą małą zabawę.",
    "1Hero is here!": "1Hero tu jest!",
    "Looking good, girls.": "Wyglądacie świetnie, dziewczyny.",
    "Yeah, I got off work a bit early.": "Tak, wyszłam z pracy trochę wcześniej.",
    "Let’s go have some fun!": "Chodźmy się zabawić!",
    "Poor 1Hero. Surrounded by beautiful ladies and no relationships in sight.": "Biedny 1Hero. Otoczony pięknymi paniami i bez widoków na związek.",
    "You know how I feel.": "Wiesz, co czuję.",
    "Those girls will grow up and when they do, I think you’d make a good man for either one of them.": "Te dziewczyny dorosną i gdy to się stanie, myślę, że byłbyś dobrym facetem dla którejkolwiek z nich.",
    "Maybe you’re right… One day.": "Może masz rację… Kiedyś.",
    "Until then, you come to mama for all your needs. Ya hear?": "A do tego czasu przychodź do mamy po wszystko, czego potrzebujesz. Słyszysz?",
    "Carol? Are you serious?": "Carol? Mówisz poważnie?",
    "Don’t be so dramatic. I’m an old lady and you’re a man in his prime.": "Nie dramatyzuj. Jestem starą kobietą, a ty mężczyzną w kwiecie wieku.",
    "I’d love to help you with any… relationship problems. Physical or otherwise.": "Chętnie pomogę ci z… problemami w związku. Fizycznymi czy innymi.",
    "Haha… Yeah, sure thing, Carol.": "Haha… Jasne, Carol.",
    "She’s going to help you? What problems do you have, 1Hero?": "Ona ci pomoże? Jakie masz problemy, 1Hero?",
    "It’s not a big deal, Arianna.": "To nic wielkiego, Arianna.",
    "Is it something I can help you with?": "Czy mogę ci jakoś pomóc?",
    "Now that you mention it… Just how physical are you allowed to be?": "Skoro pytasz… Jak fizyczna możesz być?",
    "I don’t understand? Physical?": "Nie rozumiem? Fizyczna?",
    "Carol is helping me with… sexual problems.": "Carol pomaga mi z… problemami seksualnymi.",
    "Oh, my! I can never help you with that! It is forbidden!": "Ojej! Nigdy nie mogłabym ci w tym pomóc! To zakazane!",
    "So you’ve never done anything sexual at all?": "Więc nigdy nie robiłaś nic seksualnego?",
    "I sat on a rounded stone once. But I felt nothing! I swear!": "Usiadłam raz na zaokrąglonym kamieniu. Ale nic nie poczułam! Przysięgam!",
    "Let’s just say, hypothetically, that you and I had sex.": "Powiedzmy, hipotetycznie, że ty i ja uprawialiśmy seks.",
    "It’s just a hypothetical.": "To tylko hipoteza.",
    "I would lose my wings! I would be cast out of the empyrean, forced to live among demonkind, or worse yet, to live a mortal life among humans!": "Straciłabym skrzydła! Zostałabym wygnana z empyreum, zmuszona żyć wśród demonów, albo jeszcze gorzej, wieść śmiertelne życie wśród ludzi!",
    "We’re not that bad.": "Nie jesteśmy tacy źli.",
    "Let us never speak of such things again.": "Nigdy więcej o tym nie rozmawiajmy.",
    "I have no knowledge of that sinful act and will not burden my mind with such thoughts.": "Nie mam pojęcia o tym grzesznym akcie i nie będę obciążać umysłu takimi myślami.",
    "You’ve never been wet… down there?": "Nigdy nie byłaś wilgotna… tam na dole?",
    "I’m not listening! I’m not listening!": "Nie słucham! Nie słucham!",
    "Then I guess Carol is going to have to help me in that department.": "W takim razie Carol będzie musiała mi pomóc w tej sprawie.",
    "Oh, boy. Humankind is so dirty.": "O rany. Ludzkość jest taka brudna.",
    "I’ll live.": "Przeżyję.",
    "Carol told us everything.": "Carol opowiedziała nam wszystko.",
    "What are you going to do, 1Hero?": "Co zrobisz, 1Hero?",
    "I talked to Andrea… There’s nothing I can do right now.": "Rozmawiałem z Andreą… Na razie nic nie mogę zrobić.",
    "Are you going to try and save your dad like in Star Wars?": "Zamierzasz spróbować ocalić tatę jak w Gwiezdnych Wojnach?",
    "The guy needs to be in jail… I just want this to end.": "Ten gość powinien siedzieć… Chcę, by to się skończyło.",
    "We should have told you. But in our mind, Kirk was dead.": "Powinniśmy ci powiedzieć. Ale w naszej głowie Kirk nie żył.",
    "He’s a psychopath. I didn’t want him in our lives.": "To psychopata. Nie chciałam go w naszym życiu.",
    "You could have just told me.": "Mogłaś mi po prostu powiedzieć.",
    "The man you had in your mind was who we wanted you to live up to.": "Człowiek, którego miałeś w głowie, to ten, do którego chcieliśmy, byś dorastał.",
    "It’s true. You were such a good kid… We didn’t want to lose that.": "To prawda. Byłeś takim dobrym dzieckiem… Nie chcieliśmy tego stracić.",
    "You didn’t trust me?": "Nie ufałaś mi?",
    "You don’t know Kirk. He would have manipulated you. He would have dragged you into his den of thieves.": "Nie znasz Kirka. Zmanipulowałby cię. Wciągnąłby cię do swojej jaskini złodziei.",
    "You don’t know that.": "Nie wiesz tego.",
    "Look what he became. I’m glad you never knew him.": "Popatrz, kim się stał. Cieszę się, że go nie znałeś.",
    "Chloe!": "Chloe!",
    "I’m being honest with you, 1Hero.": "Jestem z tobą szczera, 1Hero.",
    "… I don’t know what to think. This is all so crazy…": "… Nie wiem, co myśleć. To wszystko takie szalone…",
    "How could this happen?": "Jak to mogło się stać?",
    "The Lord tests us in mysterious ways.": "Pan wystawia nas na próbę w tajemniczy sposób.",
    "There’s no test here… The man will go to jail.": "Nie ma tu żadnej próby… Ten człowiek pójdzie do więzienia.",
    "I do hope you never have to face him.": "Mam nadzieję, że nigdy nie będziesz musiał stawić mu czoła.",
    "That’s not for me to decide… Kimura has her own plans.": "To nie ode mnie zależy… Kimura ma własne plany.",
    "Does she know…?": "Czy ona wie…?",
    "No. She won’t know this… It’s not relevant.": "Nie. Nie dowie się o tym… To nieistotne.",
    "I’ll tell you one thing: If that man comes snooping around the farm again, I’ll take him down myself.": "Powiem jedno: Jeśli ten facet znów będzie się kręcił wokół farmy, sama go załatwię.",
    "You go, Ma!": "Brawo, mamo!",
    "Sounds like you should stay away from him.": "Brzmi, jakbyś powinna trzymać się od niego z daleka.",
    "You are welcome here.": "Jesteś tu mile widziana.",
    "I think it’s best to stay here, at least until I can learn more about what’s going on.": "Myślę, że najlepiej zostać tu, przynajmniej dopóki nie dowiem się więcej o tym, co się dzieje.",
    "Where will they sleep?": "Gdzie będą spać?",
    "There’s plenty of room.": "Miejsca jest pod dostatkiem.",
    "Tomorrow morning I’m heading to the church to check up on Father Solomon… Perhaps Sister Judy can come with me.": "Jutro rano idę do kościoła sprawdzić, co u ojca Solomona… Może siostra Judy pójdzie ze mną.",
    "Oh! I like that idea very much.": "O! Bardzo mi się podoba ten pomysł.",
    "Aww! I wanted to have fun with Sister Judy!": "Aww! Chciałam pobawić się z siostrą Judy!",
    "Then go to church tomorrow morning.": "Więc idź jutro rano do kościoła.",
    "Oh, fooey!": "Och, do licha!",
    "If you’re planning to leave, you better get moving. The storm is only going to get worse later tonight.": "Jeśli planujesz wyjść, lepiej ruszaj. Burza będzie tylko gorsza później wieczorem.",
    "Thank you for the hospitality, Miss Heather.": "Dziękuję za gościnność, panno Heather.",
    "You’re welcome here any time, Sister.": "Jesteś tu zawsze mile widziana, Siostro.",
    "See you tomorrow morning, Sister Judy.": "Do zobaczenia jutro rano, siostro Judy.",
    "Goodbye.": "Do widzenia.",
}
known=set()
for p in (ROOT/'drafts').rglob('*.jsonl'):
    for line in p.read_text(encoding='utf-8').splitlines():
        if line.strip():
            r=json.loads(line)
            if r.get('translation','').strip(): known.add(r['id'])
rows=[]
unmapped=set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    r=json.loads(line)
    ctx=r.get('context') or {}
    src=' '.join(r.get('source_text','').strip().split())
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=24 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=111: raise SystemExit(f'Expected 111, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map24')
