#!/usr/bin/env python3
"""Build Polish drafts for Map 257 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map257-followups-01.jsonl'
TRANSLATIONS = {
    "Well, I’ll be damned… At least you have good taste in art. I have one just like it at home.": "No nie, niech mnie… Przynajmniej masz dobry gust artystyczny. Mam w domu taki sam.",
    "Heh… Somehow I doubt yours is ‘’just like it’’.": "Heh… Jakoś wątpię, by twój był „taki sam”.",
    "Ahem, let’s get to the point.": "Ech, przejdźmy do sedna.",
    "What’s this about some dingy farm?": "Co to za sprawa z jakąś obskurną farmą?",
    "Dingy? I’ll have you know it’s a beautiful farm!": "Obskurną? To piękna farma!",
    "‘’Your Honor’’.": "„Wysoki Sądzie”.",
    "… Your Honor.": "…Wysoki Sądzie.",
    "I got this notice from the court that my farm is being taken over by the state.": "Dostałam zawiadomienie z sądu, że moja farma jest przejmowana przez stan.",
    "Ah yes, this matter.": "Ach, tak, ta sprawa.",
    "Unfortunately, there’s nothing that can be done about this.": "Niestety, nic nie da się z tym zrobić.",
    "The state has a responsibility to preserve ancient Casula culture, and your farm happens to be right on top of it.": "Stan ma obowiązek zachować starożytną kulturę Casula, a twoja farma leży akurat na niej.",
    "This is ridiculous! You can’t take my home from me! I have a beautiful house and I’m not giving that up!": "To śmieszne! Nie możecie zabrać mi domu! Mam piękny dom i nie zamierzam go oddać!",
    "Beautiful? I somehow doubt that… Now a mansion overlooking the river… that will be beautiful.": "Piękny? Jakoś wątpię… Za to rezydencja z widokiem na rzekę… ta będzie piękna.",
    "Mansion?": "Rezydencja?",
    "Uh, did I say mansion?": "Yh, czy powiedziałem rezydencja?",
    "Are you going to build a mansion on my land!?": "Zamierzasz zbudować rezydencję na mojej ziemi!?",
    "You must have misheard me. I meant government housing.": "Musiałaś mnie źle usłyszeć. Miałem na myśli budownictwo komunalne.",
    "You know, there are much more scenic places in North Santiva for the state to build government housing on.": "Wiesz, są znacznie bardziej malownicze miejsca w North Santiva, gdzie stan mógłby budować budownictwo komunalne.",
    "Are there? Not that I’m interested, but go on.": "Są? Nie że jestem zainteresowany, ale mów dalej.",
    "The Casula Forest has a lot of nice, undeveloped areas.": "Las Casula ma sporo ładnych, niezabudowanych terenów.",
    "In my experience, there’s a lot of Casula culture to be found there, too.": "Z mojego doświadczenia, można tam też znaleźć sporo kultury Casula.",
    "No doubt the state could claim some of that land for preservation.": "Bez wątpienia stan mógłby przejąć część tej ziemi pod ochronę.",
    "Land that would require a nice mansion to oversee the preservation of the area.": "Ziemię, która wymagałaby ładnej rezydencji do nadzorowania ochrony terenu.",
    "I mean, government housing.": "To znaczy, budownictwa komunalnego.",
    "Hmm, interesting.": "Hmm, ciekawe.",
    "What the hell.": "A niech to.",
    "Are you certain, detective? I think the court is going to need evidence to prove your case.": "Jesteś pewien, detektywie? Myślę, że sąd będzie potrzebował dowodów na poparcie twojej sprawy.",
    "Absolutely. I’ll head over right now and come back with photos of a suitable area.": "Absolutnie. Skoczę tam zaraz i wrócę ze zdjęciami odpowiedniego terenu.",
    "Okay, detective. I’ll withhold judgment until you return. But you had better be quick about it.": "Dobrze, detektywie. Wstrzymam się z wyrokiem, aż wrócisz. Ale lepiej się pospiesz.",
    "Miss Ray, you can return home. I’ll let you know the result…": "Panno Ray, możesz wracać do domu. Dam znać o wyniku…",
    "I’m not going anywhere until this is done.": "Nigdzie się nie ruszę, dopóki to się nie skończy.",
    "God damn it… Hurry this up, detective.": "Cholera… Pospiesz się, detektywie.",
    "Don’t worry, Carol. I’ve got this.": "Nie martw się, Carol. Ogarnę to.",
    "You had better, 1Hero. I can’t imagine losing my farm to this doofus.": "Lepiej, 1Hero. Nie wyobrażam sobie stracić farmy przez tego idiotę.",
    "So what’s this about, Your Honor?": "O co chodzi, Wysoki Sądzie?",
    "A robbery! Right here under your nose, no less!": "Kradzież! Tuż pod twoim nosem, na dodatek!",
    "Someone stole something from you?": "Ktoś coś ci ukradł?",
    "What did they take?": "Co zabrali?",
    "Well… uh…": "Cóż… yyy…",
    "Yes, Your Honor, what did they take?": "Tak, Wysoki Sądzie, co zabrali?",
    "My pen!": "Mój długopis!",
    "Your pen?": "Twój długopis?",
    "Hahaha.": "Hahaha.",
    "Of course I am! It was very, very important to me.": "Oczywiście, że tak! Był dla mnie bardzo, bardzo ważny.",
    "You have to get it back right away.": "Musisz go odzyskać natychmiast.",
    "Uh huh. How ‘bout you file a report on that, and we’ll get right on it.": "Mhm. Może złóż na to raport, a my się tym od razu zajmiemy.",
    "A report?": "Raport?",
    "Good day, Your Honor.": "Miłego dnia, Wysoki Sądzie.",
    "You! It was you, wasn’t it?": "Ty! To ty, prawda?",
    "Me? I was busy talking with Bobby. Do you see me holding your… missing pen?": "Ja? Byłem zajęty rozmową z Bobbym. Widzisz u mnie twój… zagubiony długopis?",
    "You know damn well what was taken.": "Dobrze wiesz, co zostało zabrane.",
    "If you’re so upset about it, why not file a report for it?": "Jeśli tak ci zależy, czemu nie zgłosisz kradzieży?",
    "Or maybe reporting the theft of a painting – one already reported to be stolen – could be a problem?": "A może zgłoszenie kradzieży obrazu – który już został zgłoszony jako skradziony – byłoby problemem?",
    "You owe your promotion to me, detective… Don’t forget that.": "Swój awans zawdzięczasz mnie, detektywie… Nie zapominaj o tym.",
    "And you owe your future Koi pond to Kimura… Don’t you forget that.": "A ty swój przyszły stawik koi zawdzięczasz Kimurze… Nie zapominaj o tym.",
    "It’ll be a kick-ass mansion, Canmore.": "To będzie zajebista rezydencja, Canmore.",
    "I’m sure it will be.": "Jestem pewien, że będzie.",
    "We have a buyer.": "Mamy kupca.",
    "1Hero? So you want to buy Andrea's old mansion, huh?": "1Hero? Więc chcesz kupić starą rezydencję Andrei, huh?",
    "It’s a great place. The jacuzzi alone is amazing.": "Świetne miejsce. Samo jacuzzi jest niesamowite.",
    "A koi pond might be better.": "Stawik koi mógłby być lepszy.",
    "I think I’ll stick with the jacuzzi.": "Chyba zostanę przy jacuzzi.",
    "Fair enough. Look, I like you, detective. So how about the state cuts you a little slack?": "Fair enough. Słuchaj, lubię cię, detektywie. Więc może stan przymknie oko?",
    "No property taxes?": "Bez podatku od nieruchomości?",
    "Hahaha, that’s a good one. No, of course you’ll have to pay property taxes.": "Hahaha, niezły. Nie, oczywiście będziesz musiał płacić podatek od nieruchomości.",
    "But on the bright side, we’ll give you a special discount on the mansion sale.": "Ale z dobrej strony, damy ci specjalną zniżkę na sprzedaż rezydencji.",
    "The least we could do for our famous public servant.": "Tyle możemy zrobić dla naszego słynnego funkcjonariusza.",
    "Miss Wilson, let’s make that happen.": "Panno Wilson, zróbmy to.",
    "You’ve got it, Your Honor.": "Zrozumiano, Wysoki Sądzie.",
    "If that’s all, I need to get going.": "Jeśli to wszystko, muszę iść.",
    "I made the mistake of eating those tacos again…": "Znowu zjadłem te tacos…",
    "The mansion is yours!": "Rezydencja jest twoja!",
    "The mansion is mine!": "Rezydencja jest moja!",
    "I’m so proud of you, 1Hero.": "Jestem z ciebie taka dumna, 1Hero.",
    "I can hardly believe I pulled this off… It took so much work.": "Ledwo mogę uwierzyć, że mi się udało… Tyle pracy.",
    "Come on, 1Hero. This calls for a celebratory drink.": "Chodź, 1Hero. Należy ci się drink z okazji świętowania.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=257 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=77: raise SystemExit(f'Expected 77, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map257')
