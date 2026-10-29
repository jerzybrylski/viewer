#!/usr/bin/env python3
"""Build Polish drafts for Map 204 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map204-followups-01.jsonl'
TRANSLATIONS = {
    "Looking forward to getting your pussy blown?": "Nie możesz się doczekać, by zaliczyć cipkę?",
    "Maybe. I was thinking about taking charge this time.": "Może. Myślałam, by tym razem przejąć stery.",
    "Taking charge?": "Przejąć stery?",
    "Pussy facefucking.": "Cipkowe facefucking.",
    "Maybe Hannah’s actually a worse influence than I thought.": "Może Hannah ma na mnie gorszy wpływ, niż myślałam.",
    "How’s your first day of house arrest been?": "Jak mija pierwszy dzień aresztu domowego?",
    "I’m going to lose my mind in here… But at least it’s better than prison…": "Zwariuję tu… Ale przynajmniej lepiej niż w więzieniu…",
    "You know… I could use a man like you for a small job.": "Wiesz… Przydałby mi się taki gość jak ty do drobnej roboty.",
    "I owe you one, Andrea. But I’m not breaking the law.": "Jestem ci winna, Andrea. Ale nie będę łamać prawa.",
    "You won’t need to break any laws… hopefully.": "Nie będziesz musieć łamać prawa… mam nadzieję.",
    "It took a lot of money to get myself and Nellie off the hook… You were no small bargain either, 1Hero.": "Sporo kasy kosztowało wyciągnięcie mnie i Nellie z kłopotów… Ty też nie byłeś tani, 1Hero.",
    "You’re short on money?": "Brakuje ci kasy?",
    "To say the least… Luckily, I have a backup investment.": "Delikatnie mówiąc… Na szczęście mam zapasową inwestycję.",
    "A backup investment?": "Zapasową inwestycję?",
    "Crypto.": "Krypto.",
    "The thing is… I haven’t looked at that nonsense in many years… I have no idea how much money I have there.": "Rzecz w tym… Nie zaglądałam do tego badziewia od lat… Nie mam pojęcia, ile tam mam.",
    "Can’t you just look?": "Nie możesz po prostu sprawdzić?",
    "My crypto wallet is on a USB drive… And I don’t have it.": "Mój portfel krypto jest na pendrivie… I nie mam go.",
    "Let me guess… You left it in your old mansion.": "Zgaduję… Zostawiłaś go w starej rezydencji.",
    "Where is it? I’ll find it.": "Gdzie jest? Znajdę go.",
    "It’s in my old bedroom, in a safe… I don’t have the keys though.": "Jest w mojej starej sypialni, w sejfie… Ale nie mam kluczy.",
    "Can I break in?": "Mogę się włamać?",
    "You’re a good detective, 1Hero. I’m sure you can figure it out.": "Jesteś dobrym detektywem, 1Hero. Jestem pewna, że coś wymyślisz.",
    "I may have dropped my bedroom key in the yard after taking a dip in the hot tub.": "Chyba upuściłam klucz do sypialni w ogrodzie po kąpieli w jacuzzi.",
    "Any other clues?": "Inne wskazówki?",
    "The safe has a combination written down on a piece of paper… But I don’t remember where I hid it. It must be in the house somewhere.": "Sejf ma kombinację zapisaną na kartce… Ale nie pamiętam, gdzie ją schowałam. Musi być gdzieś w domu.",
    "Good news, 1Hero!": "Dobre wieści, 1Hero!",
    "What piece is this?...": "Co to za kawałek?...",
    "1Hero!?": "1Hero!?",
    "It must be hard making these life changes.": "Musi być ciężko wprowadzać takie życiowe zmiany.",
    "I needed a man like you in my life, 1Hero… I wish I’d known you twenty years ago.": "Potrzebowałam takiego faceta jak ty w życiu, 1Hero… Szkoda, że nie znałam cię dwadzieścia lat temu.",
    "When I was seven?": "Gdy miałam siedem lat?",
    "That’s not what I meant, smartass.": "Nie o to mi chodziło, mądralo.",
    "See you soon, Andrea.": "Do zobaczenia wkrótce, Andrea.",
    "Don’t let me get too lonely, 1Hero.": "Nie pozwól mi być zbyt samotną, 1Hero.",
    "Come back for another round any time, stud muffin.": "Wpadaj na kolejną rundkę, kiedy chcesz, ciasteczko.",
    "Enjoying my mansion?": "Podoba ci się moja rezydencja?",
    "It’s not bad.": "Nie jest zła.",
    "A lot of good times have been had there.": "Wiele dobrych chwil tam przeżyto.",
    "With many more to come.": "I wiele więcej przed nami.",
    "You’d better remember to invite me to them all.": "Lepiej pamiętaj, by zapraszać mnie na wszystkie.",
    "I wouldn’t dream of letting you miss out.": "Nie śmiałbym cię pominąć.",
    "That’s what I like to hear, sexy.": "To lubię słyszeć, przystojniaku.",
    "I’ll be by this evening, as planned.": "Będę wieczorem, jak planowano.",
    "We won’t start without you.": "Nie zaczniemy bez ciebie.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=204 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=48: raise SystemExit(f'Expected 48, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map204')
