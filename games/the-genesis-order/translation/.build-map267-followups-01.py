#!/usr/bin/env python3
"""Build Polish drafts for Map 267 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map267-followups-01.jsonl'
TRANSLATIONS = {
    "1Hero… Helping your friend move in?": "1Hero… Pomagasz przyjaciółce się wprowadzać?",
    "She’s pretty excited. I hope you go easy on her.": "Jest bardzo podekscytowana. Mam nadzieję, że będziesz dla niej łagodny.",
    "I am eager to rent from you, Jon. Do you have the key?": "Chcę wynająć od ciebie, Jon. Masz klucz?",
    "This place is pretty nice.": "To miejsce jest całkiem niezłe.",
    "And it’s right next to where I work.": "I jest tuż obok mojej pracy.",
    "I know how to buy in the right locations.": "Wiem, jak kupować w dobrych lokalizacjach.",
    "Thank you so much, Jon.": "Dziękuję ci bardzo, Jon.",
    "Where’s all your stuff? Only bringing one bag?": "Gdzie wszystkie twoje rzeczy? Tylko jedna torba?",
    "Oh… I don’t have much.": "Och… Nie mam wiele.",
    "I’m sure she’ll have a good time decorating this place.": "Jestem pewna, że będzie się świetnie bawić, urządzając to miejsce.",
    "Just be careful not to put too many holes in the drywall when hanging pictures.": "Tylko uważaj, by nie zrobić za wielu dziur w ścianach, wieszając obrazy.",
    "I need to take more pictures!": "Muszę robić więcej zdjęć!",
    "You’ll keep an eye on her, right, Jon?": "Będziesz miał na nią oko, prawda, Jon?",
    "You can trust me, 1Hero. Just make sure she’s on-time with payments.": "Możesz mi zaufać, 1Hero. Tylko dopilnuj, by płaciła na czas.",
    "You don’t have to worry about that. I have a job at Dick’s now.": "Nie musisz się martwić. Mam pracę w Dick's.",
    "Good luck. I could never work in the fast-food biz.": "Powodzenia. Nigdy nie dałbym rady w fast foodzie.",
    "I think Judy is cut out for it.": "Myślę, że Judy się do tego nadaje.",
    "I know I will succeed.": "Wiem, że dam radę.",
    "That’s the spirit… Good luck.": "To duch… Powodzenia.",
    "Ah! Did you see that!?": "A! Widziałaś to!?",
    "I saw a dog!": "Widziałam psa!",
    "That’s… impossible.": "To… niemożliwe.",
    "Holy shit! That’s a rat!": "Jasna cholera! To szczur!",
    "Ahh! It’s so huge!": "Aaa! Jaki ogromny!",
    "God damn it… Jon’s apartments have rats?": "Cholera… W apartamentach Jona są szczury?",
    "No! No!... It’s okay. I think it was a dog. I like dogs.": "Nie! Nie!... W porządku. Chyba to był pies. Lubię psy.",
    "Judy… It was a rat and you shouldn’t be living with rats.": "Judy… To był szczur i nie powinnaś mieszkać ze szczurami.",
    "But, 1Hero, I love this place. It’s my home.": "Ale, 1Hero, kocham to miejsce. To mój dom.",
    "Can we catch it and set him free?... Then I won’t have to live with a rat.": "Możemy go złapać i wypuścić?... Wtedy nie będę musiała żyć ze szczurem.",
    "That’s something Jon should do.": "To powinien zrobić Jon.",
    "Please, 1Hero. I do not want to get on his bad side. Can’t we just catch it?": "Proszę, 1Hero. Nie chcę mu podpaść. Nie możemy go po prostu złapać?",
    "Fine… I’ll help trap the rat.": "Dobra… Pomogę złapać szczura.",
    "I’m going to be late for work.": "Spóźnię się do pracy.",
    "You go to Dick’s; I’ll stay behind and deal with the rat.": "Ty idź do Dick's; ja zostanę i zajmę się szczurem.",
    "You’re my hero, 1Hero.": "Jesteś moim bohaterem, 1Hero.",
    "I’m happy to help, Judy. Now you better get going so you’re not late.": "Chętnie pomogę, Judy. Teraz lepiej leć, by się nie spóźnić.",
    "Will you visit after you catch the rat?": "Odwiedzisz po złapaniu szczura?",
    "I’ll stop by later.": "Wpadnę później.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=267 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=38: raise SystemExit(f'Expected 38, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map267')
