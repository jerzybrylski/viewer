#!/usr/bin/env python3
"""Build Polish drafts for Map 99 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map99-followups-01.jsonl'
TRANSLATIONS = {
    "It’s some sort of chapel.": "To jakaś kaplica.",
    "The mansion has a chapel?": "Rezydencja ma kaplicę?",
    "What is that thing?": "Co to za coś?",
    "Is it on fire?... It’s smoking.": "Czy to płonie?... Dymi.",
    "Stay here. Let me check this place out.": "Zostań tu. Rozejrzę się.",
    "I’m not liking this, 1Hero. Maybe we should leave.": "Nie podoba mi się to, 1Hero. Może powinniśmy odejść.",
    "Yeah… Let’s get out of here.": "Tak… Wynośmy się stąd.",
    "Seems this mansion is hiding a lot of secrets.": "Wygląda na to, że rezydencja kryje sporo sekretów.",
    "1Hero! Are you okay!?": "1Hero! Wszystko w porządku!?",
    "Yeah… I’m fine. I must have triggered a trap.": "Tak… Nic mi nie jest. Chyba uruchomiłem pułapkę.",
    "Whatever that thing was, it must be valuable to be protected by a trap.": "Cokolwiek to było, musi być cenne, skoro chroni je pułapka.",
    "Shit! Diana!... She might be in trouble.": "Cholera! Diana!... Może mieć kłopoty.",
    "Diana?": "Diana?",
    "Lillian… This chapel leads to a bunker. Are you safe from the Guild?": "Lillian… Ta kaplica prowadzi do bunkra. Jesteś bezpieczna przed Gildią?",
    "The man who broke into my home is of no concern to me.": "Mężczyzna, który włamał się do mojego domu, nie obchodzi mnie.",
    "But he’s close… What does he want?": "Ale jest blisko… Czego chce?",
    "What kind of trouble are you getting into?": "W jakie kłopoty się pakujesz?",
    "The Guild is no more. The man who seeks to take over for my father is destined for failure.": "Gildia już nie istnieje. Człowiek, który chce przejąć schedę po moim ojcu, skazany jest na porażkę.",
    "I’ve been tasked with taking him out.": "Dostałem zadanie, by go zdjąć.",
    "When? The bust is happening soon?": "Kiedy? Obława już niedługo?",
    "I don’t know… Something is off.": "Nie wiem… Coś jest nie tak.",
    "Stay focused, 1Hero. Your task is to find the Toma pieces. The Guild is no longer your problem.": "Skup się, 1Hero. Twoim zadaniem jest znaleźć fragmenty Tomy. Gildia to już nie twój problem.",
    "Yeah… Sorry about that, 1Hero.": "Tak… Przepraszam za to, 1Hero.",
    "You’re wrong… I still have a lot to give to that case…": "Mylisz się… Wciąż mam wiele do zaoferowania w tej sprawie…",
    "1Hero?": "1Hero?",
    "I’ll meet with you later.": "Spotkam się z tobą później.",
    "Don’t worry, 1Hero. I will take good care of her.": "Nie martw się, 1Hero. Dobrze się nią zaopiekuję.",
    "My father was a religious man. All who come here will find the Lord.": "Mój ojciec był człowiekiem religijnym. Wszyscy, którzy tu przyjdą, odnajdą Pana.",
    "I don’t believe Charles was your father.": "Nie wierzę, że Charles był twoim ojcem.",
    "You have many questions, 1Hero. There is still more to learn about me.": "Masz wiele pytań, 1Hero. Jest jeszcze więcej do odkrycia o mnie.",
    "Look at this place. What a creepy, dark chapel…": "Spójrz na to miejsce. Co za upiorna, mroczna kaplica…",
    "I guess Wilkes had his own church services here.": "Chyba Wilkes odprawiał tu własne nabożeństwa.",
    "We have to chase him!": "Musimy go gonić!",
    "Into the mansion? Are you crazy?": "Do rezydencji? Zwariowałeś?",
    "Creepy… Isn’t it?": "Upiorne… Prawda?",
    "I can sense something… Something very evil in this place.": "Czuję coś… Coś bardzo złego w tym miejscu.",
    "It’s Charles Wilkes’ private chapel.": "To prywatna kaplica Charlesa Wilkesa.",
    "We should not linger… Let’s move.": "Nie powinniśmy zwlekać… Ruszajmy.",
    "Of course… The demons wouldn’t enter a chapel.": "Oczywiście… Demony nie weszłyby do kaplicy.",
    "I fear this isn’t exactly a holy place.": "Obawiam się, że to nie do końca święte miejsce.",
    "Holy shit! It’s the soul crystal!": "Jasna cholera! To kryształ dusz!",
    "I’ve seen that before! What is it?": "Już to widziałem! Co to jest?",
    "Daemalius... He’s inside!...": "Daemalius... Jest w środku!...",
    "You better watch it! I’m a priest!": "Uważaj! Jestem księdzem!",
    "We’ll take you down!": "Dopadniemy cię!",
    "You’re here to stop her, aren’t you?": "Przyszłaś go powstrzymać, prawda?",
    "Just great! Now we have Daemalius to worry about.": "Świetnie! Teraz martwimy się jeszcze Daemaliusem.",
    "He’s going to the rift! He’s going to kill Madalyn!": "Idzie do szczeliny! Zamierza zabić Madalyn!",
    "Nellie and Ella are down there! We have to find them!": "Nellie i Ella są na dole! Musimy je znaleźć!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=99 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=49: raise SystemExit(f'Expected 49, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map99')
