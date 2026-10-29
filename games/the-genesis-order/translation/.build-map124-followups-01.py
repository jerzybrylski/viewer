#!/usr/bin/env python3
"""Build Polish drafts for Map 124 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map124-followups-01.jsonl'
TRANSLATIONS = {
    "This is it? There’s nothing here.": "To tyle? Nic tu nie ma.",
    "If I were to guess, there’s probably a secret entrance.": "Gdybym miał zgadywać, pewnie jest tu sekretne wejście.",
    "Spread out. Look for anything out of place.": "Rozejdźcie się. Szukajcie czegoś nie na miejscu.",
    "I don’t see anything.": "Nic nie widzę.",
    "Look harder.": "Szukaj dokładniej.",
    "Shit. This could take a while.": "Cholera. To może potrwać.",
    "Maybe one of these shipping containers is on top of a secret passage.": "Może jeden z tych kontenerów stoi na tajnym przejściu.",
    "Well?... Look and see.": "No?... Sprawdź.",
    "Get away from me, asshole.": "Spadaj ode mnie, dupku.",
    "What the hell!? You said you wanted it!": "Co jest, do cholery!? Mówiłaś, że chcesz!",
    "Get dressed. We need to get the hell out of here before the attendant gets back.": "Ubieraj się. Musimy spieprzać stąd, zanim wróci dozorca.",
    "Back to being a bitch.": "Znowu zachowujesz się jak zołza.",
    "Shit! Jon’s back!": "Cholera! Jon wrócił!",
    "Fuck!... Hide!": "Kurde!... Schowaj się!",
    "Maybe if you didn’t mess around so much, we’d already be gone.": "Gdybyś tyle nie kombinował, już by nas tu nie było.",
    "Don’t even pretend this is my fault.": "Nawet nie udawaj, że to moja wina.",
    "He’s distracted…": "Jest rozkojarzony…",
    "1Hero?": "1Hero?",
    "Oh… Hey, Jon. I have some stuff to sell you.": "O… Hej, Jon. Mam coś na sprzedaż.",
    "Some more treasures?": "Jeszcze jakieś skarby?",
    "Uhh… Yeah. I heard you inside of the warehouse.": "Yyy… Tak. Słyszałem cię w środku magazynu.",
    "Well… Show me what you got.": "Cóż… Pokaż, co masz.",
    "Hey, Jon. I’d like to inquire about a special project.": "Hej, Jon. Chciałbym zapytać o specjalny projekt.",
    "A special project? What're you thinking?": "Specjalny projekt? Co masz na myśli?",
    "I’ve got some things I need to store…": "Mam parę rzeczy do przechowania…",
    "Things I don’t want the cops finding out about.": "Takich, o których nie chcę, by gliny się dowiedziały.",
    "Say no more, 1Hero. I never want to know the details of a client's needs.": "Nie musisz mówić więcej, 1Hero. Nigdy nie chcę znać szczegółów potrzeb klienta.",
    "So, you can help?": "Więc pomożesz?",
    "Where would you store them? They can’t go here.": "Gdzie byś je przechował? Nie mogą tu zostać.",
    "My warehouse isn’t good enough for you?": "Mój magazyn ci nie odpowiada?",
    "It’s got to be secure.": "Musi być bezpiecznie.",
    "I’ve got you covered if it’s small. I have safes that can’t be broken into.": "Jeśli małe, mam sejfy, do których nie da się włamać.",
    "No… Not small… Something really big.": "Nie… Nie małe… Coś naprawdę dużego.",
    "How big?": "Jak duże?",
    "Uhhh… The size of a car.": "Yyyy… Wielkości samochodu.",
    "I’d ask what it is, but I don’t want to know…": "Spytałbym, co to, ale wolę nie wiedzieć…",
    "You bring it here, and I can help you out. But it’ll cost ya.": "Przywieź to tutaj, a ci pomogę. Ale będzie kosztować.",
    "Okay, Jon. I’ll think about it.": "Dobra, Jon. Przemyślę to.",
    "What do you need, detective?": "Czego potrzebujesz, detektywie?",
    "I need a spare apartment key.": "Potrzebuję zapasowego klucza do mieszkania.",
    "That Abraham girl lost another key?": "Ta dziewczyna Abraham znowu zgubiła klucz?",
    "No… I’m investigating someone else.": "Nie… Prowadzę obserwację kogoś innego.",
    "Ah. Doing a warrantless search?": "Aha. Przeszukanie bez nakazu?",
    "I’ll scratch your back, 1Hero. But you need to give me something first.": "Podrapię ci plecy, 1Hero. Ale musisz mi coś dać najpierw.",
    "I can find some treasures.": "Mogę znaleźć skarby.",
    "I’ve got something else in mind.": "Mam na myśli coś innego.",
    "I’ve been doing some diving in Casula Forest… I’m looking for underwater caves.": "Nurkowałem w Lesie Casula… Szukam podwodnych jaskiń.",
    "You want me to find a cave?": "Chcesz, żebym znalazł jaskinię?",
    "No… I want you to find something I lost while diving.": "Nie… Chcę, byś znalazł coś, co zgubiłem podczas nurkowania.",
    "Underwater? How would I do that?": "Pod wodą? Jak miałbym to zrobić?",
    "You’ve got a knack for finding treasure. I think you can handle it.": "Masz nosa do skarbów. Myślę, że dasz radę.",
    "What am I looking for?": "Czego mam szukać?",
    "A gold coin… Polished and shiny as of last month.": "Złotej monety… Wypolerowanej i błyszczącej miesiąc temu.",
    "I’ve searched for it since I dropped it, but I just can't seem to find it.": "Szukałem jej, odkąd ją zgubiłem, ale nijak nie mogę znaleźć.",
    "Where did you drop it?": "Gdzie ją zgubiłeś?",
    "It was near the waterfall, in heavy current.": "Było przy wodospadzie, w silnym nurcie.",
    "You can handle it. And when you find it, I’ll give you the key.": "Dasz radę. A gdy ją znajdziesz, dam ci klucz.",
    "Here, take my diving mask.": "Proszę, weź moją maskę do nurkowania.",
    "You’ll need more than this to handle the rough currents. But it’s a start.": "Będziesz potrzebował więcej niż tego, by poradzić sobie z rwącym nurtem. Ale to początek.",
    "You found my coin!": "Znalazłeś moją monetę!",
    "A deal’s a deal. What key do you need?": "Umowa to umowa. Jakiego klucza potrzebujesz?",
    "The key to the easternmost apartment.": "Klucza do najbardziej wschodniego mieszkania.",
    "Hey! Don’t touch that spool of copper. It’s valuable.": "Hej! Nie dotykaj tej szpuli miedzi. Jest cenna.",
    "How much do you want for it?": "Ile za nią chcesz?",
    "I’d part with it for $900.": "Oddałbym za 900 $.",
    "Seems steep.": "Dość drogo.",
    "Are you planning to go back to the mansion?": "Planujesz wrócić do rezydencji?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=124 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=67: raise SystemExit(f'Expected 67, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map124')
