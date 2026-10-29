#!/usr/bin/env python3
"""Build Polish drafts for Map 58 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map58-followups-01.jsonl'
TRANSLATIONS = {
    "Wow! What an office.": "Łał! Co za biuro.",
    "I used to clean it. But then one day, Charles told me to leave and then he started locking the door.": "Kiedyś je sprzątałam. Ale pewnego dnia Charles kazał mi odejść i zaczął zamykać drzwi.",
    "Are these Casula artifacts?": "Czy to artefakty Casula?",
    "Some of them, yes. He was a collector of ancient art.": "Niektóre tak. Był kolekcjonerem sztuki starożytnej.",
    "I didn’t know that.": "Nie wiedziałam.",
    "That reminds me… I found something in the forest.": "Przy okazji… Coś znalazłam w lesie.",
    "What? An artifact?": "Co? Artefakt?",
    "A piece of one… Take a look.": "Kawałek… Zobacz.",
    "Come on, Erica. Let’s search this place before we get caught.": "Chodź, Erica. Przeszukajmy to miejsce, zanim nas przyłapią.",
    "I want to know more about Charles’ past…": "Chcę dowiedzieć się więcej o przeszłości Charlesa…",
    "Just look for anything that might give away some information.": "Po prostu szukaj czegokolwiek, co może zdradzić jakieś informacje.",
    "Huh? What’s this in the garbage? Looks like a phone.": "Huh? Co to w śmieciach? Wygląda jak telefon.",
    "Bingo! It’s a burner phone.": "Bingo! To telefon na kartę.",
    "All flip phones these days are burner phones… trust me.": "Wszystkie telefony z klapką to dziś telefony na kartę… wierz mi.",
    "Why would Charles have a burner phone?": "Po co Charles miałby telefon na kartę?",
    "Can you open it?": "Możesz go otworzyć?",
    "It’s likely encrypted. If I can’t figure out the passcode, the phone is probably programmed to delete the data.": "Pewnie zaszyfrowany. Jeśli nie odgadnę kodu, telefon jest pewnie zaprogramowany, by skasować dane.",
    "Maybe there’s a passkey hidden somewhere.": "Może gdzieś ukryty jest klucz.",
    "What? Like, inside of a book? That could take forever to find.": "Co? Jak, w książce? To mogłoby zająć wieki.",
    "Shit… At least we have something.": "Cholera… Przynajmniej coś mamy.",
    "Do you think anyone will notice it’s missing?": "Myślisz, że ktoś zauważy, że go nie ma?",
    "It’s been in the garbage this whole time. I don’t think anyone is coming into this office.": "Leżał w śmieciach przez cały czas. Nie sądzę, by ktoś przychodził do tego biura.",
    "I trust you know what you’re doing, 1Hero. But I better get home.": "Ufam, że wiesz, co robisz, 1Hero. Ale lepiej wrócę do domu.",
    "It’s been a wild night.": "To była szalona noc.",
    "This is fun, 1Hero. I’m glad I met you.": "To zabawne, 1Hero. Cieszę się, że cię poznałam.",
    "Today’s my lucky day!": "Dziś mój szczęśliwy dzień!",
    "I just need to figure out the passcode to this burner phone.": "Muszę tylko rozgryźć kod do tego telefonu na kartę.",
    "I don’t like this sneaking around. I’d rather just try our luck against them.": "Nie podoba mi się to skradanie. Wolałabym spróbować szczęścia przeciw nim.",
    "Are you crazy?": "Zwariowałaś?",
    "1Hero’s got a gun.": "1Hero ma broń.",
    "And I’m sure all of Duncan’s henchmen do too.": "I jestem pewna, że wszyscy ludzie Duncana też mają.",
    "Be patient, young lady.": "Bądź cierpliwa, młoda damo.",
    "I’ll go take a peek. I can’t imagine they are going to stick around that room.": "Pójdę zerknąć. Nie wyobrażam sobie, by mieli zostać w tym pokoju.",
    "Be careful, 1Hero. This place can be a maze.": "Uważaj, 1Hero. To miejsce to labirynt.",
    "The guards moved to the entry.": "Strażnicy przenieśli się do wejścia.",
    "But I found a way around.": "Ale znalazłam obejście.",
    "Really? Where?": "Naprawdę? Gdzie?",
    "Come back and let us know what you find.": "Wróć i daj nam znać, co znajdziesz.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=58 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=38: raise SystemExit(f'Expected 38, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map58')
