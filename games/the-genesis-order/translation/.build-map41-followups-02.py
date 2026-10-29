#!/usr/bin/env python3
"""Build Polish drafts for Map 41 follow-ups."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map41-followups-02.jsonl'
TRANSLATIONS = {
    "I’m not strong enough. I should work out more.": "Nie jestem wystarczająco silny. Powinienem więcej ćwiczyć.",
    "I’ve never shot a bow and arrow before… I’m scared.": "Nigdy wcześniej nie strzelałam z łuku… Boję się.",
    "It’s easy.": "To proste.",
    "How easy? It needs to be very easy!": "Jak bardzo proste? Musi być bardzo proste!",
    "Oh… Uhh… It’s very easy.": "Och… Yyy… To bardzo proste.",
    "Find the bow and arrow yet? We’re going to need it.": "Znalazłeś już łuk i strzały? Będziemy ich potrzebować.",
    "Why? Why would you need a bow and arrow?": "Po co? Po co wam łuk i strzały?",
    "So we can hunt down… the mama goat.": "Żeby upolować… mamę kozy.",
    "You want to kill it?": "Chcesz ją zabić?",
    "Just get me a bow!": "Po prostu przynieś mi łuk!",
    "Just get me a bow! Check the cave. You probably left it in there.": "Po prostu przynieś mi łuk! Sprawdź jaskinię. Pewnie tam go zostawiłeś.",
    "Did you find the bow and arrow?": "Znalazłeś łuk i strzały?",
    "Wow! Look at me!": "Wow! Spójrz na mnie!",
    "Be careful with that.": "Uważaj z tym.",
    "What do I do with it?": "Co mam z tym zrobić?",
    "You’re going to hit a target!": "Będziesz strzelać do celu!",
    "That sounds hard!": "To brzmi trudno!",
    "What!? You’re a natural! I’m sure you can do it!": "Co!? Masz talent! Na pewno dasz radę!",
    "You’re putting too much pressure on me!": "Za bardzo na mnie naciskasz!",
    "Good! You’ll need to shoot it under pressure once we’re in the field.": "Dobrze! W terenie też będziesz musiała strzelać pod presją.",
    "Hey! You’re not helping.": "Hej! Nie pomagasz.",
    "I literally made the bow and arrow.": "Dosłownie zrobiłam ten łuk i strzały.",
    "Come on, Alia… Let's practice.": "Daj spokój, Alia… Poćwiczmy.",
    "Now… What I want you to do is…": "Teraz… Chcę, żebyś zrobiła…",
    "Hot damn! You hit the barrel!": "Cholera! Trafiłaś w beczkę!",
    "Is that good?": "Czy to dobrze?",
    "Careful with that!": "Uważaj z tym!",
    "Wow! She hit the gas can!": "Wow! Trafiła w kanister!",
    "What are you aiming for?": "W co celujesz?",
    "I don’t know!": "Nie wiem!",
    "She’s clearly aiming for containers and she’s doing a hell of a job hitting them.": "Wyraźnie celuje w pojemniki i idzie jej świetnie.",
    "Am I good at this?": "Czy jestem w tym dobra?",
    "She hit the water tank!!!": "Trafiła w zbiornik z wodą!!!",
    "I did?": "Naprawdę?",
    "It’s a big target, but I ain’t complaining.": "To duży cel, ale nie narzekam.",
    "Maybe I am good at this!": "Może jednak jestem w tym dobra!",
    "I told you! You’re a killer!": "Mówiłam! Jesteś zabójczynią!",
    "I’m going to murder everyone!": "Zamorduję wszystkich!",
    "Come on! Let’s not waste any more time. It’s time to go on an adventure.": "Dalej! Nie traćmy więcej czasu. Czas na przygodę.",
    "Yeah! I’m an adventurer!": "Tak! Jestem poszukiwaczką przygód!",
    "We’re going to the church!": "Idziemy do kościoła!",
    "The church? What is she doing at the church that requires chains and weapons?...": "Kościół? Co ona robi w kościele, że potrzebuje łańcuchów i broni?...",
    "Oh, shit!... The alligator!": "O cholera!... Aligator!",
    "Hannah?... Alia?...": "Hannah?... Alia?...",
    "I better head to the church and stop them.": "Lepiej pójdę do kościoła i je powstrzymam.",
    "I can move that big bale. I just need to figure something out.": "Mogę przesunąć tę dużą belę. Muszę tylko coś wymyślić.",
    "Move that bale in the barn. Else, Ma’s gonna get real mad at me.": "Przesuń tę belę w stodole. Inaczej mama strasznie się na mnie wkurzy.",
    "I’m working on it, Hannah.": "Pracuję nad tym, Hannah.",
    "How are you going to move that big hay bale in the barn?": "Jak zamierzasz przesunąć tę dużą belę siana w stodole?",
    "Damn… It’s pretty heavy.": "Cholera… Jest dość ciężka.",
    "Push, 1Hero! Push!": "Pchaj, 1Hero! Pchaj!",
    "Don’t hurt your back.": "Uważaj na plecy.",
    "Good thing we have a big, strong man around.": "Dobrze, że mamy w pobliżu silnego faceta.",
    "Wow! Impressive stuff.": "Wow! Imponujące.",
    "Oh, that old thing is a Casula treasure.": "Och, to stara błyskotka Casuli.",
    "We find them all the time around here.": "Znajdujemy je tu cały czas.",
    "Is it valuable?": "Czy to cenne?",
    "Probably not. But, I hear there are gold ones found around these parts.": "Pewnie nie. Ale słyszałam, że w tych okolicach trafiają się złote.",
    "You’re right. Some can get pricey. Or, so I hear.": "Masz rację. Niektóre potrafią być drogie. Tak słyszałam.",
    "Wow! Let’s look for gold ones!": "Wow! Poszukajmy złotych!",
    "Easy there, Chloe. We need a license to harvest those old toys.": "Spokojnie, Chloe. Potrzebujemy licencji, żeby zbierać te stare zabawki.",
    "We’ll make more money with veggies and grains. But if you like it so much, you can have it, 1Hero.": "Więcej zarobimy na warzywach i zbożu. Ale skoro tak ci się podoba, możesz to mieć, 1Hero.",
    "Thanks. I might know a licensed dealer that can buy it.": "Dzięki. Może znam licencjonowanego handlarza, który to kupi.",
    "Alright. Time to load up the rest of the bales.": "Dobra. Czas załadować resztę bel.",
    "Go on, strong man. Move the bales out of the barn and we’ll load them into the truck.": "Dalej, silny człowieku. Wynoś bele ze stodoły, a my załadujemy je na ciężarówkę.",
    "Do you need any help?": "Potrzebujesz pomocy?",
    "I’ve got it. You can help Hannah outside.": "Poradzę sobie. Możesz pomóc Hannah na zewnątrz.",
    "All done! That wasn’t so hard.": "Gotowe! Wcale nie było tak trudno.",
    "Damn, it’s getting hot in here.": "Cholera, robi się tu gorąco.",
    "Did we really need to close the barn door?": "Naprawdę musieliśmy zamykać drzwi stodoły?",
    "We can’t be letting a draft in here, or the hay will go everywhere…": "Nie możemy tu wpuścić przeciągu, bo siano rozniesie się wszędzie…",
    "You don’t want to be raking all day long, do you?": "Nie chcesz przecież grabić cały dzień, prawda?",
    "It’s like an oven in here.": "Tu jest jak w piecu.",
    "Well, do something about it.": "To zrób coś z tym.",
    "Hannah!": "Hannah!",
    "Really? We’re stripping now?": "Serio? Teraz się rozbieramy?",
    "This is a farm, 1Hero. Take your damn shirt off and get back to work.": "To gospodarstwo, 1Hero. Zdejmij tę cholerną koszulkę i wracaj do roboty.",
    "I guess I thought this would be more fun.": "Chyba myślałem, że będzie zabawniej.",
    "Let’s just get this over with so we can get something to drink.": "Skończmy to wreszcie, żeby móc się czegoś napić.",
    "Actually… This is cooler.": "W sumie… Tak jest chłodniej.",
    "What a hunk!": "Co za ciacho!",
    "Now it’s your turn, Chloe.": "Teraz twoja kolej, Chloe.",
    "I’m not taking off my shirt!": "Nie zdejmę koszulki!",
    "You have a bra on, don’t you?": "Masz przecież stanik, nie?",
    "That’s not the point!": "Nie o to chodzi!",
    "I can finish up. Maybe you can wait outside in the cool breeze.": "Mogę dokończyć. Możesz poczekać na zewnątrz na chłodnym wietrze.",
    "No! She has to work too!": "Nie! Ona też ma pracować!",
    "Just open the barn door.": "Po prostu otwórz drzwi stodoły.",
    "Rules are rules. Ella won fair and square.": "Zasady to zasady. Ella wygrała uczciwie.",
    "Do your worst! I look forward to seeing you faceplant in front of mean ole Ma.": "Dawaj! Nie mogę się doczekać, jak zaliczysz glebę przed starą, wredną mamą.",
    "Your mom’s not mean.": "Twoja mama nie jest wredna.",
    "All this talk of goat food made me hungry.": "Cała ta gadka o jedzeniu dla kóz zgłodniałam.",
    "Let’s go eat some dinner.": "Chodźmy zjeść kolację.",
    "I guess we’ve no choice. Time to introduce you to Ma.": "Chyba nie mamy wyboru. Czas przedstawić cię mamie.",
    "It’s a bag of fertilizer, but it’s too heavy for me to carry around…": "To worek nawozu, ale jest za ciężki, żebym go nosiła…",
    "Maybe if I were stronger, I could take it.": "Może gdybym była silniejsza, dałabym radę go wziąć.",
    "Could I figure out how to fix a drive shaft?": "Czy udałoby mi się naprawić wał napędowy?",
    "Now, maybe you can keep a new memory for when you’re lonely.": "A teraz może będziesz mieć nowe wspomnienie, gdy poczujesz się samotny.",
    "I won’t soon forget this.": "Nigdy tego nie zapomnę.",
    "It’s a one time deal. Don’t go beggin’ for more.": "To jednorazowa akcja. Nie przychodź prosić o więcej.",
    "No more. You got it.": "Koniec. Zrozumiano.",
    "I better get back inside and make sure Hannah isn’t misbehaving.": "Lepiej wrócę do środka i dopilnuję, by Hannah nie broiła.",
    "Maybe tomorrow I can finally get around to moving that tractor.": "Może jutro w końcu uda mi się przestawić ten traktor.",
    "If I have time, maybe I can help you out.": "Jeśli będę mieć czas, może ci pomogę.",
    "I’d never turn down an offer for help from you, 1Hero.": "Nigdy nie odmówiłbym pomocy od ciebie, 1Hero.",
    "See ya tomorrow.": "Do zobaczenia jutro.",
    "Goodnight, Carol.": "Dobranoc, Carol.",
    "Bring me a working driveshaft and I can install it on the tractor.": "Przynieś mi sprawny wał napędowy, a zamontuję go w traktorze.",
    "I fixed the driveshaft.": "Naprawiłem wał napędowy.",
    "Let’s go! I can finally fix the tractor!": "Chodź! W końcu mogę naprawić traktor!",
    "Are you going to come with us? Don’t you have work tomorrow?": "Idziesz z nami? Nie musisz jutro do pracy?",
    "I can stay up a little longer.": "Mogę zostać jeszcze trochę dłużej.",
    "There’s something on the wall. How can I reach it?": "Coś jest na ścianie. Jak mam to dosięgnąć?",
    "Nice job, 1Hero.": "Dobra robota, 1Hero.",
    "What are we going to do with it now?": "Co z tym teraz zrobimy?",
    "It can stay in the barn until Hannah has time to build a pen…": "Może zostać w stodole, dopóki Hannah nie znajdzie czasu, by zbudować zagrodę…",
    "She’s going to love her new pet!": "Pokoche nowe zwierzątko!",
    "What if it climbs onto things in the barn? Won't that be dangerous?": "A jeśli będzie wspinać się po rzeczach w stodole? Nie będzie to niebezpieczne?",
    "Safer than being out there with the coyotes.": "Bezpieczniej niż tam na zewnątrz z kojotami.",
    "Maybe we can make a pen before dinner.": "Może zbudujemy zagrodę przed kolacją.",
    "If I don’t get cooking, there won't be any dinner before sundown.": "Jeśli nie zacznę gotować, nie będzie kolacji przed zachodem słońca.",
    "I can put something together. Something small that will keep it safe until Hannah gets back.": "Mogę coś sklecić. Coś małego, co utrzyma je w bezpieczeństwie, dopóki Hannah nie wróci.",
    "There’s wood out front. You two are welcome to try.": "Na zewnątrz jest drewno. Możecie spróbować.",
    "We can do it. It won't take long.": "Dam radę. To nie zajmie długo.",
    "I’ll get started cooking. It’ll be an hour before dinner.": "Zacznę gotować. Do kolacji została godzina.",
    "Plenty of time.": "Mnóstwo czasu.",
    "This will be fun! We can make the little guy a nice home.": "Będzie fajnie! Zrobimy małemu lokatorowi ładny domek.",
    "We’ll need some supplies.": "Będziemy potrzebować materiałów.",
    "Carol mentioned some wood in the front yard. I think it was covered in weeds last time I looked.": "Carol wspominała o drewnie na podwórku. Chyba ostatnio było zarośnięte chwastami.",
    "Something stuck to my electromagnet!": "Coś przykleiło się do mojego elektromagnesu!"
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
        or context.get('map_id') != 41
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
    raise SystemExit('Unmapped Map 41 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 130:
    raise SystemExit(f'Expected exactly 130 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 41 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
