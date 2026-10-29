#!/usr/bin/env python3
"""Build Polish drafts for Map 18 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map18-followups-01.jsonl'
TRANSLATIONS = {
    "I’m not ready yet. I need a nice suit before I dare have dinner with the commissioner.": "Jeszcze nie jestem gotowy. Potrzebuję eleganckiego garnituru, zanim odważę się iść na kolację z panią komisarz.",
    "I’m not ready yet. I should bring some wine and not show up empty handed.": "Jeszcze nie jestem gotowy. Powinienem przynieść wino i nie przychodzić z pustymi rękami.",
    "I’ve got the wine, and I’ve got a nice suit… I’m ready.": "Mam wino i mam elegancki garnitur… Jestem gotowy.",
    "1Hero. Nice of you to come over on such short notice.": "1Hero. Miło, że wpadłeś tak szybko.",
    "I’m looking forward to speaking with the two of you.": "Cieszę się, że mogę porozmawiać z wami obojgiem.",
    "Thank you for being able to meet at my home.": "Dziękuję, że mogliście spotkać się u mnie w domu.",
    "I’d love our chat to be comfortable.": "Chciałabym, żeby nasza rozmowa była komfortowa.",
    "And private.": "I prywatna.",
    "1Hero, did you bring the aloe plant?": "1Hero, przyniosłeś aloes?",
    "This drink of yours sounds interesting.": "Twój trunek brzmi interesująco.",
    "Something my great-grandfather taught me.": "Nauczył mnie tego mój pradziadek.",
    "An old family recipe? Sounds intriguing.": "Stary rodzinny przepis? Brzmi intrygująco.",
    "Come this way. I’ll show you my home.": "Chodź tędy. Pokażę ci mój dom.",
    "Actually, I left it at my home just across the way. I’ll be right back.": "Właściwie zostawiłem go w domu tuż obok. Zaraz wracam.",
    "Don’t be long, 1Hero.": "Nie zwlekaj, 1Hero.",
    "I forgot to pick up an aloe plant.": "Zapomniałem wziąć aloesu.",
    "It’s the damn operation… The mansion belongs to the state…": "To przez tę operację… Rezydencja należy do stanu…",
    "We’re giving up?": "Poddajemy się?",
    "Keep it a secret, Erica… This is far from over.": "Zachowaj to w tajemnicy, Erica… To jeszcze dalekie od końca.",
    "I’ll be safe, 1Hero. I need to talk to Kimberly.": "Będę bezpieczna, 1Hero. Muszę porozmawiać z Kimberly.",
    "Let her know I didn’t mean for this to happen.": "Daj jej znać, że nie chciałam, by do tego doszło.",
    "I will… I understand.": "Przekażę… Rozumiem.",
    "Well, I guess that’s one way to handle things…": "Cóż, chyba tak można to załatwić…",
    "I hope Kimberly isn’t too pissed at me.": "Mam nadzieję, że Kimberly nie jest na mnie zbyt wściekła.",
    "Don’t fuck this up.": "Nie spieprz tego.",
    "You don’t mean that. You’d love to see me fall from grace.": "Nie mówisz serio. Chciałabyś zobaczyć, jak wypadam z łask.",
    "Not at the expense of my work.": "Nie kosztem mojej pracy.",
    "This isn’t really your work anymore.": "To już nie jest twoja praca.",
    "I’m still a part of this case, 1Hero. And you still work for me.": "Nadal jestem częścią tej sprawy, 1Hero. I nadal dla mnie pracujesz.",
    "And I look forward to more… private meetings.": "I liczę na kolejne… prywatne spotkania.",
    "Where the hell is she?": "Gdzie ona, do cholery, jest?",
    "She’s not answering the door?": "Nie otwiera drzwi?",
    "She must be away.": "Pewnie jej nie ma.",
    "I’ll see if I can figure out where she is.": "Spróbuję dowiedzieć się, gdzie jest.",
    "Jon!?": "Jon!?",
    "I’m here to meet with the commissioner.": "Przyszedłem spotkać się z panią komisarz.",
    "Lucky me… This is my client.": "Szczęściarz ze mnie… To mój klient.",
    "Huh?...": "Słucham?...",
    "Holy shit! She’s shipping treasures!": "O cholera! Ona przemyca skarby!",
    "How much is she paying you?": "Ile ci płaci?",
    "Not a dime. After this, my record is clean.": "Ani grosza. Potem moja kartoteka jest czysta.",
    "You’re here.": "Jesteś tutaj.",
    "You don’t have to kill Duncan… She’ll never know.": "Nie musisz zabijać Duncana… Ona nigdy się nie dowie.",
    "Does it matter if she knows? My fate is tied to hers… What choice do I have?": "Czy to ma znaczenie, czy się dowie? Mój los jest związany z jej… Jaki mam wybór?",
    "Nellie… Duncan’s not lying…": "Nellie… Duncan nie kłamie…",
    "Shit… You’re his son.": "Cholera… Jesteś jego synem.",
    "I have no idea how… But it’s true.": "Nie mam pojęcia jak… Ale to prawda.",
    "I thought it was just more of his crazy ramblings.": "Myślałem, że to tylko jego chore brednie.",
    "Carol and Heather… They knew him when they were much younger.": "Carol i Heather… Znały go, gdy były znacznie młodsze.",
    "I don’t know what to tell you, 1Hero… But we’re in a pickle.": "Nie wiem, co ci powiedzieć, 1Hero… Ale mamy problem.",
    "If you have any ideas, I’m all ears…": "Jeśli masz jakieś pomysły, słucham…",
    "But you and I both know I lied to Andrea…": "Ale oboje wiemy, że okłamałem Andreę…",
    "If I wanted to take Duncan down, I could. He trusts me.": "Gdybym chciał dorwać Duncana, mógłbym. Ufa mi.",
    "Give me some time, Nellie.": "Daj mi trochę czasu, Nellie.",
    "I’m guessing we don’t have a lot.": "Chyba nie mamy go wiele.",
    "Girl problems?": "Problemy z dziewczynami?",
    "Not this time…": "Nie tym razem…",
    "Guild problems.": "Problemy z Gildią.",
    "Nope! I don’t want to hear about it.": "Nie! Nie chcę o tym słyszeć.",
    "1Hero, have you seen the commissioner?": "1Hero, widziałeś panią komisarz?",
    "We can’t find her. She’s disappeared.": "Nie możemy jej znaleźć. Zniknęła.",
    "Heather?": "Heather?",
    "1Hero?": "1Hero?",
    "I was about to ask you the same thing.": "Chciałem zapytać cię o to samo.",
    "I’ve been thinking about upgrading my home, but it can only get so big.": "Zastanawiałem się nad powiększeniem domu, ale da się go powiększyć tylko do pewnego stopnia.",
    "So I’m considering buying a new home.": "Więc rozważam kupno nowego domu.",
    "New home? So you were thinking about buying this mansion?": "Nowy dom? Więc myślałeś o kupnie tej rezydencji?",
    "I’m sorry, 1Hero, but this place is super expensive. A detective just doesn’t make that kind of money.": "Przepraszam, 1Hero, ale to miejsce jest super drogie. Detektyw po prostu nie zarabia takich pieniędzy.",
    "You might be surprised.": "Możesz się zdziwić.",
    "Unless you have a lot of money, I won’t be.": "Chyba że masz dużo pieniędzy, nie zdziwię się.",
    "I’m good at investing.": "Jestem dobry w inwestowaniu.",
    "Oh really? Wouldn’t have anything to do with your side hustle with Jon?": "Och, naprawdę? To nie ma nic wspólnego z twoją fuchą u Jona?",
    "Might be a part of it.": "Może częściowo.",
    "Well, if you’re really interested, I could sell it to you.": "Cóż, jeśli naprawdę jesteś zainteresowany, mogę ci ją sprzedać.",
    "You’re the realtor?": "Ty jesteś agentką nieruchomości?",
    "Yours truly.": "We własnej osobie.",
    "How did that happen?": "Jak do tego doszło?",
    "I wasn’t supposed to be, but I got a phone call from the state.": "Nie miałam nią być, ale dostałam telefon ze stanu.",
    "They asked me to handle it after they decided a public auction wouldn’t bring in the funds they wanted.": "Poprosili mnie, żebym się tym zajęła, po tym jak uznali, że publiczna aukcja nie przyniesie takich funduszy, jakich chcą.",
    "Alright, so how do we do this? You helped me the last time through everything.": "Dobra, więc jak to zrobimy? Ostatnim razem przeprowadziłaś mnie przez wszystko.",
    "As long as you have the money, I can get the paperwork together. We just have to get the judge to sign off on it.": "Dopóki masz pieniądze, mogę przygotować papiery. Musimy tylko zdobyć podpis sędziego.",
    "I have the money, but where is the realtor?": "Mam pieniądze, ale gdzie jest agentka nieruchomości?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=18 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=82: raise SystemExit(f'Expected 82, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map18')
