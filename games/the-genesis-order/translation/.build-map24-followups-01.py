#!/usr/bin/env python3
"""Build Polish drafts for Map 24 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map24-followups-01.jsonl'
TRANSLATIONS = {
    "I’m sorry about what happened at the barn.": "Przepraszam za to, co stało się w stodole.",
    "It’s not your fault. Hannah just embarrasses me sometimes.": "To nie twoja wina. Hannah czasem mnie po prostu zawstydza.",
    "She’s a wild child for sure. Don’t even try to keep up with her.": "Zdecydowanie jest dzikuską. Nawet nie próbuj za nią nadążyć.",
    "She wouldn’t know a boundary if it hit her in the face.": "Nie rozpoznałaby granic, nawet gdyby uderzyły ją w twarz.",
    "What a lovely surprise! Did you get off work early?": "Co za miła niespodzianka! Wcześniej skończyłeś pracę?",
    "Yeah. Despite your best attempts to embarrass me earlier, I thought I’d stop by early to say hi to my favorite mom.": "Tak. Mimo twoich najlepszych prób, by mnie wcześniej zawstydzić, pomyślałem, że wpadnę wcześniej przywitać się z moją ulubioną mamą.",
    "Haha! Don’t tell Carol you said that.": "Haha! Nie mów Carol, że tak powiedziałeś.",
    "I was just going to get a bit of a tan before the girls got here. If you want, change into your swim trunks and join me in the backyard.": "Zamierzałam się trochę poopalać, zanim przyjdą dziewczyny. Jeśli chcesz, przebierz się w kąpielówki i dołącz do mnie na podwórku.",
    "Sure thing, Heather.": "Jasne, Heather.",
    "Oh, and while you’re upstairs changing, bring down the tanning oil.": "A, i gdy będziesz na górze się przebierać, przynieś olejek do opalania.",
    "You better keep an eye on Sister Judy. She’s pretty good at running away.": "Lepiej miej oko na siostrę Judy. Jest całkiem dobra w uciekaniu.",
    "I look forward to meeting Ella.": "Nie mogę się doczekać spotkania z Ellą.",
    "Invite Ella and Hannah over. Let’s have a party.": "Zaproś Ellę i Hannah. Zróbmy imprezę.",
    "Did you visit Judy last night?": "Odwiedziłeś Judy wczoraj wieczorem?",
    "I did. I’m sorry if I teased you.": "Tak. Przepraszam, jeśli ci dokuczałam.",
    "It’s okay. I enjoy talking with you, 1Hero.": "W porządku. Lubię z tobą rozmawiać, 1Hero.",
    "You sure did get along well with that news anchor.": "Naprawdę dobrze dogadałeś się z tą prezenterką.",
    "She’s even prettier in person.": "Na żywo jest jeszcze ładniejsza.",
    "You think you have a chance with her?": "Myślisz, że masz u niej szansę?",
    "Haha. No way.": "Haha. Nie ma mowy.",
    "I hope Father Solomon can help you on your mission.": "Mam nadzieję, że ojciec Solomon pomoże ci w misji.",
    "We saw you on TV, 1Hero!": "Widzieliśmy cię w telewizji, 1Hero!",
    "How did I do?": "Jak wypadłem?",
    "It was wonderful! You sure do have your hands full with that Kilt case.": "Było wspaniale! Masz pełne ręce roboty z tą sprawą Kilta.",
    "It’s the Guild case.": "To sprawa Gildii.",
    "You’re the expert.": "Jesteś ekspertem.",
    "Hey! It’s starting!": "Hej! Zaczyna się!",
    "Oh, shit! Let’s watch!": "O cholera! Oglądajmy!",
    "You should've seen these naughty old ladies drooling over your news spot.": "Powinieneś widzieć te niegrzeczne staruszki śliniące się na twój materiał.",
    "They are freakin’ me out!": "Przerażają mnie!",
    "I’m so happy to finally meet you, Miss Wilson.": "Tak się cieszę, że w końcu panią poznałam, panno Wilson.",
    "Thanks for letting her stay here, Mom.": "Dzięki, że pozwoliłaś jej tu zostać, mamo.",
    "Of course. I’m happy to make room for you after that thunderstorm.": "Oczywiście. Chętnie zrobię dla ciebie miejsce po tej burzy.",
    "It was quite a leak.": "To był niezły przeciek.",
    "I heard you fixed it right up.": "Słyszałam, że szybko to naprawiłeś.",
    "In the heart of the storm, no less.": "W samym środku burzy, na dodatek.",
    "How brave.": "Jak odważnie.",
    "Yes. Quite brave, indeed.": "Tak. Rzeczywiście, bardzo odważnie.",
    "Come, Sister. I’ll show you your room.": "Chodź, siostro. Pokażę ci pokój.",
    "She can stay in your room?": "Może zostać w twoim pokoju?",
    "Of course. I can sleep on the couch.": "Oczywiście. Mogę spać na kanapie.",
    "Oh, you don’t have to do that.": "Och, nie musisz tego robić.",
    "I’ve had a change of heart. I think I’ll swim with you ladies.": "Zmieniłam zdanie. Popływam z wami, dziewczyny.",
    "Judy’s going to love hearing that.": "Judy będzie zachwycona, słysząc to.",
    "She’s changing upstairs.": "Przebiera się na górze.",
    "Don’t get any ideas, 1Hero.": "Nie miej żadnych pomysłów, 1Hero.",
    "There’s definitely something between you two.": "Zdecydowanie coś między wami jest.",
    "I think Sister Judy’s in love.": "Myślę, że siostra Judy jest zakochana.",
    "She’s just experiencing a new world. She’s not going to cheat on God Himself.": "Ona po prostu poznaje nowy świat. Nie zamierza zdradzić samego Boga.",
    "Of course not. But she’s still very excited.": "Oczywiście, że nie. Ale wciąż jest bardzo podekscytowana.",
    "I’m going to change. I’ll meet you outside.": "Idę się przebrać. Spotkamy się na zewnątrz.",
    "Okay, 1Hero.": "Dobrze, 1Hero.",
    "Have fun tonight, darling.": "Baw się dobrze dziś wieczorem, kochanie.",
    "Don’t forget to pick up Sister Judy’s toothbrush from the church.": "Nie zapomnij zabrać szczoteczki siostry Judy z kościoła.",
    "I’m nervous, but also excited.": "Denerwuję się, ale też jestem podekscytowana.",
    "It’s just dinner. You’ll love it.": "To tylko kolacja. Pokochasz to.",
    "Heather? Are you home?": "Heather? Jesteś w domu?",
    "The door’s unlocked. Where is she?": "Drzwi są otwarte. Gdzie ona jest?",
    "1Hero! Is everything okay?": "1Hero! Wszystko w porządku?",
    "Yeah. It’s fine.": "Tak. W porządku.",
    "Chloe told me what happened. I can’t believe those thieves went to the church!": "Chloe powiedziała mi, co się stało. Nie mogę uwierzyć, że ci złodzieje poszli do kościoła!",
    "Everything will be okay. Backup arrived and those goons won't be visiting the church again.": "Wszystko będzie dobrze. Przybyło wsparcie i ci zbiry nie odwiedzą już kościoła.",
    "Thank God.": "Dzięki Bogu.",
    "Hannah and her left your place with Father Solomon.": "Hannah i ona wyszły od ciebie z ojcem Solomonem.",
    "Judy wasn’t at the church.": "Judy nie było w kościele.",
    "Really? Did she go with Hannah?": "Naprawdę? Poszła z Hannah?",
    "She wasn’t at Hannah’s place.": "Nie było jej u Hannah.",
    "I can check on Hannah and see if she’s with her at the farm.": "Mogę sprawdzić u Hannah, czy jest z nią na farmie.",
    "Oh, dear. Not again.": "Ojej. Znowu.",
    "Are you sure she’s not at the church?": "Jesteś pewien, że nie ma jej w kościele?",
    "Judy must be at the church. Are you sure you didn’t miss her?": "Judy musi być w kościele. Jesteś pewien, że jej nie przeoczyłeś?",
    "…She could have gone to the farm, I guess.": "…Chyba mogła pójść na farmę.",
    "What channel is it on?": "Na jakim kanale to leci?",
    "Channel 4.": "Channel 4.",
    "I can’t wait to see it!": "Nie mogę się doczekać, by to zobaczyć!",
    "Let’s watch 1Hero on the news!": "Oglądajmy 1Hero w wiadomościach!",
    "Chloe’s upset.": "Chloe jest zdenerwowana.",
    "Well, it’s a good thing she has some friends around right now.": "Cóż, dobrze, że ma teraz wokół siebie przyjaciół.",
    "1Hero… I feel guilty.": "1Hero… Czuję się winna.",
    "I think we should be careful.": "Myślę, że powinniśmy uważać.",
    "I’ll see you around, Heather.": "Do zobaczenia, Heather.",
    "Thanks for helping me, 1Hero.": "Dzięki za pomoc, 1Hero.",
    "Anytime.": "Zawsze.",
    "Ella is such a sweet girl.": "Ella to taka słodka dziewczyna.",
    "Don’t forget to call me if you’re looking to have some fun.": "Nie zapomnij zadzwonić, jeśli będziesz miał ochotę na zabawę.",
    "1Hero... Tell me: Have you had sex with Chloe?": "1Hero... Powiedz mi: Uprawiałeś seks z Chloe?",
    "Sort of… I mean… Yes… But…": "Tak jakby… To znaczy… Tak… Ale…",
    "We’ve not officially sealed the deal.": "Oficjalnie jeszcze tego nie przypieczętowaliśmy.",
    "Dammit… What are we doing?": "Cholera… Co my robimy?",
    "I know what you’re feeling.": "Wiem, co czujesz.",
    "Chloe wants you. I know she does.": "Chloe cię pragnie. Wiem, że tak jest.",
    "But she’s not ready.": "Ale nie jest gotowa.",
    "I just thought… I thought she’d be more forward with you… She’s not a child anymore.": "Po prostu myślałam… Myślałam, że będzie bardziej bezpośrednia… Nie jest już dzieckiem.",
    "1Hero…": "1Hero…",
    "Yes, Heather?": "Tak, Heather?",
    "Maybe we should cool it off.": "Może powinniśmy trochę przystopować.",
    "You might be right.": "Możesz mieć rację.",
    "The timing just isn’t right… Chloe needs me to be her old lady.": "Moment nie jest odpowiedni… Chloe potrzebuje, bym była jej starą.",
    "Don’t you dare think that moms can’t be hot.": "Nie waż się myśleć, że mamuśki nie mogą być gorące.",
    "Oh, 1Hero. You always know what to say.": "Och, 1Hero. Zawsze wiesz, co powiedzieć.",
    "Chloe will be fine. I’ll talk to her.": "Chloe będzie w porządku. Porozmawiam z nią.",
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
    tr=translations.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=101: raise SystemExit(f'Expected 101, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map24')