#!/usr/bin/env python3
"""Build Polish drafts for Map 97 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map97-followups-01.jsonl'
TRANSLATIONS = {
    "I can use my hatchet to chop down this old, dead tree.": "Mogę użyć siekierki, by ściąć to stare, martwe drzewo.",
    "Where did he go?": "Gdzie on poszedł?",
    "He’s run into the woods. It’ll be hard to track him.": "Uciekł do lasu. Będzie go trudno wytropić.",
    "Oh, no. What will happen to him?": "O nie. Co się z nim stanie?",
    "Let’s just wait. Maybe he’ll come back out if we stop chasing him.": "Po prostu poczekajmy. Może wróci, jeśli przestaniemy go gonić.",
    "I guess this is a nice place to relax.": "Chyba to miłe miejsce, by odpocząć.",
    "This is my old swimming hole. I used to take Hannah here when she was a baby to teach her how to swim.": "To moje stare kąpielisko. Zabierałam tu Hannah, gdy była malutka, by nauczyć ją pływać.",
    "I don’t know about swimming, but perhaps it’s a good place to get some sun in private.": "Nie wiem, jak z pływaniem, ale może to dobre miejsce, by poopalać się na osobności.",
    "Let’s go skinny dipping!": "Chodźmy na nago!",
    "In the nude?": "Na nago?",
    "That’s what skinny dipping is. Unless you want to get your clothes wet and dirty.": "Na tym polega kąpiel na golasa. Chyba że chcesz zmoczyć i ubrudzić ubrania.",
    "No one’s going to see us. It’s safe.": "Nikt nas nie zobaczy. To bezpieczne.",
    "Ain’t nobody stopping me. Come on, 1Hero. Give it a try.": "Nikt mnie nie powstrzyma. Dalej, 1Hero. Spróbuj.",
    "I’ve been skinny dipping before.": "Już kąpałam się na golasa wcześniej.",
    "Hahaha. Don’t be so shy you two.": "Hahaha. Nie bądźcie tacy nieśmiali, wy dwoje.",
    "It’s comfortable.": "Jest wygodnie.",
    "Are you getting in the water, Heather?": "Wchodzisz do wody, Heather?",
    "I’ll watch you two have fun.": "Popatrzę, jak się bawicie.",
    "Off with the clothes young man.": "Zdejmuj ubrania, młodzieńcze.",
    "You promise not to tease me?": "Obiecujesz, że nie będziesz się nabijać?",
    "That’s asking a lot.": "Wiele wymagasz.",
    "No teasing from me.": "Z mojej strony bez nabijania.",
    "Shit! Is it raining?": "Cholera! Pada?",
    "Dammit. I thought we had at least an hour.": "Cholera. Myślałam, że mamy co najmniej godzinę.",
    "What about the baby goat?": "A co z koźlątkiem?",
    "We should get back inside.": "Powinniśmy wrócić do środka.",
    "At least get away from the water. Don’t want to get struck by lightning.": "Przynajmniej odejdź od wody. Nie chcesz dostać piorunem.",
    "The poor baby.": "Biedne maleństwo.",
    "He’ll live through some rain. It’s nightfall he’d have to worry about.": "Przeżyje deszcz. Martwić się powinien o zapadający zmierzch.",
    "Come on. Let’s get back. I’ll find the baby goat once the weather clears.": "Chodź. Wracajmy. Poszukam koźlęcia, gdy pogoda się przejaśni.",
    "Where should we start looking, 1Hero?": "Gdzie powinniśmy zacząć szukać, 1Hero?",
    "Not sure… Let me check the map.": "Nie jestem pewien… Sprawdźmy mapę.",
    "I can use my wading shoes to go in the creek without getting all wet.": "Mogę użyć butów do brodzenia, by wejść do strumienia, nie mocząc się całkiem.",
    "Damn, it sure is dense back here… How do we get through?": "Cholera, ale tu gęsto… Jak się przebić?",
    "We have to swim… It's easier going south with the current, but it’s a dead end.": "Musimy płynąć… Łatwiej na południe z prądem, ale to ślepy zaułek.",
    "So let’s swim north.": "Więc popłyńmy na północ.",
    "It’s rough water. Can you handle it?": "To rwąca woda. Dasz radę?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=97 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=37: raise SystemExit(f'Expected 37, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map97')
