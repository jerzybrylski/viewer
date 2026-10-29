#!/usr/bin/env python3
"""Build Polish drafts for Map 153 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map153-followups-01.jsonl'
TRANSLATIONS = {
    "Sit still, you monster!": "Siedź spokojnie, potworze!",
    "Hannah!": "Hannah!",
    "Don’t worry, Hannah! I’ll save you!": "Nie martw się, Hannah! Uratuję cię!",
    "It sucks that my gator pet got away, but at least we got to have fun!": "Szkoda, że mój aligator zwiał, ale przynajmniej mieliśmy frajdę!",
    "And that’s all it is… fun.": "I tylko tyle to jest… zabawa.",
    "That was wild.": "To było szalone.",
    "Miss Heather sure is fun to play with.": "Panna Heather to niezła zabawa.",
    "I’m glad we could enjoy each other’s company… Maybe we should do it again sometime.": "Cieszę się, że mogliśmy nacieszyć się sobą… Może powinniśmy to kiedyś powtórzyć.",
    "Come on! Let’s get back to the church. I gotta find my clothes.": "Chodź! Wracajmy do kościoła. Muszę znaleźć ubrania.",
    "Does she plan on running around the cathedral naked?": "Czy ona zamierza biegać nago po katedrze?",
    "Let them enjoy the view.": "Niech nacieszą oczy.",
    "Damn, Heather. What’s gotten into you?… You seem… naughtier.": "Cholera, Heather. Co w ciebie wstąpiło?… Wydajesz się… niegrzeczniejsza.",
    "Hey… If Carol can have fun with Chloe, why can’t I enjoy Hannah?": "Hej… Skoro Carol może bawić się z Chloe, czemu ja nie mogę nacieszyć się Hannah?",
    "Seems fair to me…": "Brzmi fair dla mnie…",
    "But what about Chloe?": "A co z Chloe?",
    "She’s in it for the excitement… I can see that now.": "Ona jest w tym dla ekscytacji… Teraz to widzę.",
    "What does it mean for us?": "Co to znaczy dla nas?",
    "Chloe is young and she wants to fool around…": "Chloe jest młoda i chce się pobawić…",
    "I don’t think she’s looking for love.": "Nie sądzę, by szukała miłości.",
    "Do you think?": "Myślisz?",
    "I was her age… If she’s involving Carol, then she’s not being serious.": "Byłam w jej wieku… Jeśli angażuje Carol, to nie podchodzi do tego poważnie.",
    "1Hero… If you want to have more fun, how about giving me a call from time to time?": "1Hero… Jeśli chcesz więcej zabawy, może zadzwonisz do mnie od czasu do czasu?",
    "So… We’re doing this?": "Więc… Robimy to?",
    "I’m learning from Carol… Don’t be so dramatic.": "Uczę się od Carol… Nie dramatyzuj.",
    "Come on. Let’s go before Hannah gets into more trouble.": "Chodź. Lecimy, zanim Hannah wpadnie w kolejne kłopoty.",
    "Look! She’s trapped!": "Patrz! Jest uwięziona!",
    "I can’t swim! Especially with a big lizard that wants to eat me!": "Nie umiem pływać! Zwłaszcza z wielką jaszczurką, która chce mnie zeżreć!",
    "Try it now! 1Hero is here!": "Spróbuj teraz! 1Hero tu jest!",
    "What!? No! Don’t swim!": "Co!? Nie! Nie pływaj!",
    "Okay! I’m still not swimming.": "Dobra! Wciąż nie pływam.",
    "What do we do, 1Hero? Tasha will never be my friend if we get Alia killed!": "Co robimy, 1Hero? Tasha nigdy nie będzie moją przyjaciółką, jeśli Alia zginie!",
    "We have to distract the alligator.": "Musimy odwrócić uwagę aligatora.",
    "I can tie it up. But not in deep water. I’d be dead as a doorknob!": "Mogę go związać. Ale nie w głębokiej wodzie. Byłabym martwa jak kłoda!",
    "So that’s why you bought the bondage equipment.": "Więc dlatego kupiłaś sprzęt do wiązania.",
    "I know what I’m doing! Just lure the gator under me!": "Wiem, co robię! Po prostu zwiń aligatora pode mnie!",
    "Hannah! You can’t jump from there! You’ll get hurt!": "Hannah! Nie możesz stamtąd skakać! Zrobisz sobie krzywdę!",
    "I know what I’m doing! Trust me!": "Wiem, co robię! Zaufaj mi!",
    "How am I going to get that alligator’s attention?": "Jak mam zwrócić uwagę tego aligatora?",
    "Look for bait, 1Hero!": "Poszukaj przynęty, 1Hero!",
    "Don’t worry, Hannah. I have an idea.": "Nie martw się, Hannah. Mam pomysł.",
    "Swim for safety, Alia! I got the gator!": "Płyń w bezpieczne miejsce, Alia! Mam aligatora!",
    "Someone save me!": "Niech ktoś mnie uratuje!",
    "I almost got him!": "Prawie go mam!",
    "Hannah!?": "Hannah!?",
    "Save me!": "Ratunku!",
    "Don’t worry, girl! I got ya!": "Nie martw się, dziewczyno! Mam cię!",
    "That thing looks worn out.": "To coś wygląda na wykończone.",
    "I did a number on him, that’s for sure.": "Dałam mu niezły łomot, to pewne.",
    "I can’t believe you wrestled that thing!": "Nie mogę uwierzyć, że walczyłaś z tym bydlakiem!",
    "I told y'all I could handle it.": "Mówiłam wam, że dam radę.",
    "What are you going to do with it? It will cost a fortune to feed it.": "Co z nim zrobisz? Będzie kosztować fortunę, by go wykarmić.",
    "I’m a farm girl. If anyone can handle it, it’s me.": "Jestem dziewczyną z farmy. Jeśli ktoś da radę, to ja.",
    "Well… Ask your mother.": "Cóż… Zapytaj matkę.",
    "Yes, daddy.": "Tak, tatusiu.",
    "Stop calling me that!": "Przestań tak do mnie mówić!",
    "Can we go now? I don’t know how much more adventure I can take.": "Możemy już iść? Nie wiem, ile jeszcze przygód zniosę.",
    "She’s… different.": "Ona jest… inna.",
    "You get used to it.": "Przyzwyczaisz się.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=153 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=58: raise SystemExit(f'Expected 58, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map153')
