#!/usr/bin/env python3
"""Build Polish drafts for Map 160 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map160-followups-01.jsonl'
TRANSLATIONS = {
    "Alright, hotshot…": "Dobra, cwaniaku…",
    "Hit the moving target three times in a row without killing yourself or me, God forbid, and you’ll leave here with the gun.": "Traf trzy razy z rzędu w ruchomy cel, nie zabijając siebie ani, nie daj Boże, mnie, a wyjdziesz stąd z bronią.",
    "Grab the gun. Let’s see it.": "Złap broń. Pokaż.",
    "Let me by, Bobby.": "Przepuść mnie, Bobby.",
    "You’re not leaving here with that gun unless you hit three targets…": "Nie wyjdziesz stąd z tą bronią, dopóki nie trafisz trzech celów…",
    "If you want to pass, leave the gun.": "Jeśli chcesz przejść, zostaw broń.",
    "Be careful with that gun, newbie.": "Ostrożnie z tą bronią, nowicjuszu.",
    "Nice shot. But you need to hit three in a row.": "Ładny strzał. Ale musisz trafić trzy z rzędu.",
    "Not bad, detective. I guess you've proven you won’t shoot yourself.": "Nieźle, detektywie. Chyba udowodniłeś, że się nie zastrzelisz.",
    "Can I leave now?": "Mogę już iść?",
    "There must be some way to slow down that target.": "Musi być sposób, by spowolnić ten cel.",
    "Piece of cake.": "Bułka z masłem.",
    "Alright, hotshot. Let’s speed things up.": "Dobra, cwaniaku. Przyspieszmy.",
    "A bullseye, as usual.": "Dziesiątka, jak zwykle.",
    "Cocky bastard…": "Zuchwały drań…",
    "Not even a challenge.": "To nawet nie wyzwanie.",
    "Seems we’re both pretty good at this… How about we make things more interesting?": "Wygląda na to, że obaj jesteśmy w tym dobrzy… A może urozmaićmy?",
    "Care to take me in the ring?": "Masz ochotę wejść ze mną na ring?",
    "You’re kidding…": "Żartujesz…",
    "I’ve been training. You’ve been slacking. I’ll beat you easily.": "Trenowałem. Ty obijałeś się. Pokonam cię bez problemu.",
    "You’re half my size.": "Jesteś o połowę mniejszy ode mnie.",
    "Don’t exaggerate.": "Nie przesadzaj.",
    "Okay… We’ll break the tie with a little sparring session.": "Dobra… Rozstrzygniemy remis sparingiem.",
    "Suit up, big boy. Let’s do this.": "Wskakuj w strój, duży chłopcze. Zróbmy to.",
    "Your funeral.": "Sam się prosisz.",
    "Are you ready to see who’s the better shot?": "Gotowy, by zobaczyć, kto jest lepszym strzelcem?",
    "We’ll take three shots, each at a higher target speed…": "Oddamy trzy strzały, każdy przy większej prędkości celu…",
    "Whoever hits the target the most wins.": "Kto trafi najwięcej, wygrywa.",
    "I’ll go first.": "Ja pierwszy.",
    "Move aside… I got this.": "Zejdź… Ja to mam.",
    "That’s how it’s done.": "Tak się to robi.",
    "You think that’s impressive? Watch this.": "Myślisz, że to imponujące? Patrz na to.",
    "Now for the real challenge.": "Teraz prawdziwe wyzwanie.",
    "Give up, 1Hero. You can’t win.": "Poddaj się, 1Hero. Nie wygrasz.",
    "This is my last shot. You think I’ll choke?": "To mój ostatni strzał. Myślisz, że spękam?",
    "Hahaha! You missed!": "Hahaha! Spudłowałeś!",
    "My gun misfired!": "Broń mi się zacięła!",
    "Making excuses?": "Wymówki?",
    "Let me clean out my gun and we’ll try again.": "Pozwól, że wyczyszczę broń i spróbujemy znowu.",
    "Come back after you fix your equipment, big man.": "Wróć, gdy naprawisz sprzęt, duży człowieku.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=160 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=40: raise SystemExit(f'Expected 40, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map160')
