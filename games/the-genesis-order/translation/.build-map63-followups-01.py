#!/usr/bin/env python3
"""Build Polish drafts for Map 63 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map63-followups-01.jsonl'
TRANSLATIONS = {
    "1Hero! Thank god you’re here!": "1Hero! Bogu dzięki, że jesteś!",
    "It’s really coming down out there!": "Ale leje na dworze!",
    "At least we have some light now…": "Przynajmniej mamy teraz trochę światła…",
    "We’re safe as long as we’re in here.": "Dopóki tu jesteśmy, jesteśmy bezpieczni.",
    "I guess we’ll just have to wait it out.": "Chyba po prostu będziemy musieli to przeczekać.",
    "This place is incredible… It’s huge!": "To miejsce jest niesamowite… Ogromne!",
    "Isn’t it!?": "Prawda!?",
    "Wow! I didn’t notice how deep it went.": "Wow! Nie zauważyłem, jak głęboka jest.",
    "It doesn’t surprise me that there is a cave here. These stone mountains must be littered with cavernous pockets like this.": "Nie dziwi mnie, że tu jest jaskinia. Te kamienne góry muszą być pełne takich kieszeni.",
    "I’ve heard about caves in the forest. But I didn’t suspect that there would be one on your farm.": "Słyszałem o jaskiniach w lesie. Ale nie podejrzewałem, że na twojej farmie też jest jedna.",
    "Well, now we have another place to party.": "Cóż, teraz mamy kolejne miejsce na imprezę.",
    "It’s not as pretty as the waterfall, but it sure is nice and quiet.": "Nie jest tak ładna jak wodospad, ale przynajmniej cicho i spokojnie.",
    "You brought something?": "Coś przyniosłaś?",
    "I may have forgotten the lantern, but I remembered the real prize.": "Może zapomniałam latarki, ale pamiętam o prawdziwej nagrodzie.",
    "What did you bring?": "Co przyniosłaś?",
    "Get a load of this!": "Patrzcie na to!",
    "Woah! You brought liquor?": "Wow! Przyniosłaś alkohol?",
    "What!?... No!": "Co!?... Nie!",
    "I brought a bottle!": "Przyniosłam butelkę!",
    "An empty liquor bottle?": "Pustą butelkę po alkoholu?",
    "Stop focusing on the liquor! Don’t you get it?": "Przestań się skupiać na alkoholu! Nie rozumiesz?",
    "We can play spin the bottle!": "Możemy zagrać w butelkę!",
    "I thought y’all would be excited.": "Myślałam, że się ucieszycie.",
    "Do you seriously want to play a kissing game?": "Naprawdę chcesz grać w całowanie?",
    "We need to kill some time. What else do you want to do?": "Musimy jakoś zabić czas. Co innego chcesz robić?",
    "I don’t think Chloe feels comfortable with that idea.": "Chyba Chloe nie czuje się z tym pomysłem komfortowo.",
    "No more bellyaching! We’re going to play, and that’s final.": "Koniec narzekania! Zagramy i koniec.",
    "Maybe it won't be that bad.": "Może nie będzie tak źle.",
    "Okay, Hannah. What are the rules?": "Dobra, Hannah. Jakie są zasady?",
    "Everyone, sit in a circle!": "Wszyscy siadamy w kółku!",
    "Alright. Let’s see who goes first.": "Dobra. Zobaczmy, kto zaczyna.",
    "What luck! 1Hero is the first to go.": "Co za szczęście! 1Hero zaczyna.",
    "What do I have to do?": "Co mam zrobić?",
    "Hold your horses! I have to spin again to see who you have to kiss.": "Wstrzymaj konie! Muszę zakręcić jeszcze raz, żeby zobaczyć, kogo masz pocałować.",
    "This is very silly, Hannah.": "To bardzo głupie, Hannah.",
    "I agree. Maybe we can just sit and talk.": "Zgadzam się. Może po prostu usiądziemy i pogadamy.",
    "I’m spinning again!": "Kręcę ponownie!",
    "Looks like Chloe is the winner!": "Wygląda na to, że Chloe wygrała!",
    "What if it had landed on you? Do you want me to kiss you?": "A gdyby wypadło na ciebie? Chcesz, żebym cię pocałowała?",
    "It didn’t land on me! It landed on Chloe, and now you have to kiss her.": "Nie wypadło na mnie! Wypadło na Chloe i teraz musisz ją pocałować.",
    "I guess rules are rules.": "Chyba zasady to zasady.",
    "Are we really going to do this?": "Naprawdę to zrobimy?",
    "Of course you’re going to do it! You can’t cheat!": "Oczywiście, że to zrobicie! Nie możecie oszukiwać!",
    "Come on, 1Hero. You’re not scared, are you?": "No dalej, 1Hero. Nie boisz się, prawda?",
    "Okay. Let’s do this.": "Dobra. Zróbmy to.",
    "Now it’s Chloe’s turn!": "Teraz kolej Chloe!",
    "No way! I’m not doing that!": "Nie ma mowy! Nie zrobię tego!",
    "That’s the rules!": "Takie są zasady!",
    "Sounds like the storm has passed. I think we need to leave before things get out of hand.": "Wygląda na to, że burza przeszła. Chyba musimy wyjść, zanim sprawy wymkną się spod kontroli.",
    "Too late for that.": "Za późno na to.",
    "Well, I had fun. Too bad Chloe is too scared.": "Cóż, ja się świetnie bawiłam. Szkoda, że Chloe się boi.",
    "I’m not going to have sex on a dare.": "Nie zamierzam uprawiać seksu na zakład.",
    "Aww! You have to try it. It feels so good.": "Aww! Musisz spróbować. To takie przyjemne.",
    "It didn’t hurt at all?": "Wcale nie bolało?",
    "No way!...": "Mowy nie ma!...",
    "Well, it kinda hurt going in at first.": "Cóż, na początku trochę bolało przy wejściu.",
    "I knew it!": "Wiedziałam!",
    "It’s not that bad! You’re such a girl!": "Nie jest tak źle! Ale z ciebie beksa!",
    "You’re a girl too!": "Sama jesteś beksą!",
    "Hey! Stop fighting. Let’s go before Carol starts to worry.": "Hej! Przestańcie się kłócić. Chodźmy, zanim Carol zacznie się martwić.",
    "Listen to Daddy before he spanks us.": "Posłuchaj tatusia, zanim dostaniemy lanie.",
    "I know where we are!": "Wiem, gdzie jesteśmy!",
    "There’s an opening to the outside.": "Jest wyjście na zewnątrz.",
    "We’re on Carol’s farm.": "Jesteśmy na farmie Carol.",
    "You’ve been here before?": "Byłeś tu już wcześniej?",
    "Last night, during the storm that came through.": "Zeszłej nocy, podczas burzy, która przeszła.",
    "So that’s why you were late for work? Staying up late with friends?": "Więc dlatego spóźniłeś się do pracy? Zarywałeś noc z przyjaciółmi?",
    "Can’t you just be happy we’ve found a way out?": "Nie możesz po prostu cieszyć się, że znaleźliśmy wyjście?",
    "Let’s get out of here.": "Chodźmy stąd.",
    "Look, 1Hero. There’s no ghosts or nothin’.": "Spójrz, 1Hero. Tu nie ma żadnych duchów ani nic takiego.",
    "We’re not looking for ghosts, we’re looking for an underground bunker.": "Nie szukamy duchów, szukamy podziemnego bunkra.",
    "Really? That’s where the bad guys are?": "Naprawdę? Tam są ci źli faceci?",
    "Something like that… But I only want to make sure there’s nothing in here so I don’t have to worry about you and Carol.": "Coś w tym stylu… Ale chcę tylko upewnić się, że nic tu nie ma, żeby nie musieć się martwić o ciebie i Carol.",
    "We can take care of some cave thieves.": "Poradzimy sobie z jakimiś jaskiniowymi złodziejami.",
    "Not these guys, you can’t.": "Nie z tymi nie dacie rady.",
    "Well, let's find out if we’ve got some thieves living in our cave.": "Cóż, przekonajmy się, czy mamy w jaskini jakichś złodziei.",
    "Ugh… Who’s the leader here?": "Ugh… Kto tu dowodzi?",
    "Holy shit! This is Hannah’s cave!": "O cholera! To jaskinia Hannah!",
    "We’re close to the farm?": "Jesteśmy blisko farmy?",
    "1Hero!?": "1Hero!?",
    "Carol!?": "Carol!?",
    "We made it!": "Udało się!",
    "How did you break through so fast?": "Jak tak szybko się przebiłaś?",
    "I got bored… Don’t underestimate a bored farm woman with a pickaxe.": "Znudziłam się… Nie doceniaj znudzonej farmerki z kilofem.",
    "Damn, woman. You’re strong as hell.": "Cholera, kobieto. Jesteś silna jak diabli.",
    "We found a Casula treasure! It’s right near here.": "Znaleźliśmy skarb Casuli! Jest tuż obok.",
    "Yeah, and it’s filled with traps!": "Tak, i pełno tam pułapek!",
    "Hannah’s going to get herself into trouble now.": "Hannah wpakuje się teraz w kłopoty.",
    "Let’s just hope there’s no more traps after we disarmed it.": "Miejmy nadzieję, że nie ma więcej pułapek po tych, które rozbroiliśmy.",
    "Sounds like you two got lucky.": "Wygląda na to, że mieliście szczęście.",
    "Heh. That’s one way to put it.": "Heh. Tak to można ująć.",
    "Come on. Let’s get you kids something to drink.": "Chodźcie. Napijcie się czegoś, dzieciaki.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=63 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=92: raise SystemExit(f'Expected 92, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map63')
