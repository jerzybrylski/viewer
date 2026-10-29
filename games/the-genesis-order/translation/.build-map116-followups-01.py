#!/usr/bin/env python3
"""Build Polish drafts for Map 116 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map116-followups-01.jsonl'
TRANSLATIONS = {
    "Ouch! What the hell was that all about?": "Auć! Co to, do cholery, było?",
    "Quiet… It’s happening.": "Cicho… To się dzieje.",
    "It glows brightly for this one.": "Dla tej świeci jasno.",
    "1Hero!": "1Hero!",
    "Father! Lilith! We saw her!": "Ojcze! Lilith! Widzieliśmy ją!",
    "We beat her at her own game.": "Pokonałyśmy ją jej własną bronią.",
    "You won that battle. But you’ve lost the war.": "Wygrałyście bitwę. Ale przegrałyście wojnę.",
    "We have to stop her!": "Musimy ją powstrzymać!",
    "One step ahead. Henry is already on the way.": "O krok do przodu. Henry już jest w drodze.",
    "Let’s join him.": "Dołączmy do niego.",
    "You are forbidden from entering the rift. Go back to the surface.": "Masz zakaz wchodzenia w szczelinę. Wracaj na powierzchnię.",
    "Do not question it, 1Hero. I know what’s best.": "Nie kwestionuj tego, 1Hero. Wiem, co najlepsze.",
    "Step away from the rift. You are not allowed back in without Mother.": "Odsuń się od szczeliny. Nie wolno ci z powrotem bez Matki.",
    "It doesn’t look open to me.": "Nie wygląda dla mnie na otwartą.",
    "Did we do something wrong?": "Zrobiliśmy coś źle?",
    "Wait… Something is happening.": "Czekaj… Coś się dzieje.",
    "Come on! Let’s go find Lillian!": "Dalej! Chodźmy znaleźć Lillian!",
    "We can’t just go in there! It’s dangerous.": "Nie możemy tam tak po prostu wejść! To niebezpieczne.",
    "We won't go far…": "Nie pójdziemy daleko…",
    "Ugh… What’s gotten into her?": "Ugh… Co w nią wstąpiło?",
    "How does it open?": "Jak to się otwiera?",
    "I just need some items. I’ll only be a moment.": "Potrzebuję tylko paru przedmiotów. Chwileczkę.",
    "The clock is ticking, 1Hero.": "Czas ucieka, 1Hero.",
    "Holy shit! Look at that!": "Jasna cholera! Patrz na to!",
    "Thank God I’m a priest, or I’d be pissing my pants right about now.": "Dzięki Bogu, że jestem księdzem, bo już bym się posikał ze strachu.",
    "I’ve been in there before…": "Byłem tam już wcześniej…",
    "I’ve got your back, 1Hero.": "Masz moje wsparcie, 1Hero.",
    "I’m bored. When are we going to kick some demon ass?": "Nudzę się. Kiedy skopiemy tyłki demonom?",
    "Be useful and get my men back.": "Bądź użyteczny i odzyskaj moich ludzi.",
    "We’ll take care of anything that comes through that portal.": "Zajmiemy się wszystkim, co przejdzie przez portal.",
    "Get that Toma artifact, 1Hero.": "Zdobądź artefakt Tomy, 1Hero.",
    "You’re really good at handling that katana.": "Naprawdę dobrze radzisz sobie z kataną.",
    "Almost as good as I am at handling a cock.": "Prawie tak dobrze, jak ja radzę sobie z fiutem.",
    "Good luck, 1Hero. I have no idea how you plan to open this weird portal.": "Powodzenia, 1Hero. Nie mam pojęcia, jak planujesz otworzyć ten dziwny portal.",
    "Open the rift already.": "Otwórz już szczelinę.",
    "No sign of any amulets.": "Ani śladu amuletów.",
    "Are you keeping an eye on the rift?": "Masz oko na szczelinę?",
    "Just a coincidence.": "Tylko zbieg okoliczności.",
    "That girl in the armor is freaking me out. Why is she wearing armor!?": "Ta dziewczyna w zbroi mnie przeraża. Czemu nosi zbroję!?",
    "If I see anything, I’ll give you a call.": "Jeśli coś zobaczę, zadzwonię.",
    "I don’t trust those scheming ladies.": "Nie ufam tym knującym paniom.",
    "Just keep an eye on the rift and let me know if you see anything.": "Po prostu miej oko na szczelinę i daj znać, jeśli coś zobaczysz.",
    "This is all crazy. This has to be a trick.": "To wszystko szalone. To musi być podstęp.",
    "Find my mom. We could use her help.": "Znajdź moją mamę. Przydałaby się jej pomoc.",
    "I know you want to do what’s right, 1Hero… The world is at stake.": "Wiem, że chcesz postąpić słusznie, 1Hero… Stawką jest świat.",
    "I’ll find a way to open the rift.": "Znajdę sposób, by otworzyć szczelinę.",
    "Don’t worry, 1Hero… Erica’s soul will be okay. One way or another.": "Nie martw się, 1Hero… Dusza Eriki będzie bezpieczna. Tak czy inaczej.",
    "I came here to kill Duncan and now we’re dealing with demons.": "Przyszedłem tu zabić Duncana, a teraz mamy do czynienia z demonami.",
    "I’m here for a reason, 1Hero… I believe we’ll succeed.": "Jestem tu nie bez powodu, 1Hero… Wierzę, że nam się uda.",
    "Shit… This isn’t looking good.": "Cholera… To nie wygląda dobrze.",
    "Arianna? Are you here?...": "Arianna? Jesteś tutaj?...",
    "I wonder if there’s a clear path to the surface.": "Ciekawe, czy jest czysta droga na powierzchnię.",
    "Hannah!": "Hannah!",
    "Mom!... Where is Dad?": "Mamo!... Gdzie jest tata?",
    "I have to go back!": "Muszę wracać!",
    "He’s holding back the demon!": "Wstrzymuje demona!",
    "The priest is doing battle?": "Ksiądz toczy bitwę?",
    "I have to save him!": "Muszę go uratować!",
    "No! Let me go… I’ll make sure he gets out.": "Nie! Puść mnie… Dopilnuję, by wydostał się.",
    "Wait… I sense…": "Czekaj… Czuję…",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=116 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=60: raise SystemExit(f'Expected 60, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map116')
