#!/usr/bin/env python3
"""Build Polish drafts for Map 246 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map246-followups-01.jsonl'
TRANSLATIONS = {
    "Ugh, do we have to?": "Ugh, musimy?",
    "Porn, Nellie? Really? On the church TV, of all places?": "Porno, Nellie? Serio? Na telewizorze w kościele, ze wszystkich miejsc?",
    "Need you ask?": "Musisz pytać?",
    "No more porn in the church.": "Koniec z porno w kościele.",
    "That… might be a problem.": "To… może być problem.",
    "There might be more in the library.": "W bibliotece może być więcej.",
    "Dear Lord, give me strength.": "Panie Boże, daj mi siłę.",
    "Alright, let’s go.": "Dobra, chodźmy.",
    "Go?": "Iść?",
    "To the church library. No way am I letting you keep porn in the church.": "Do biblioteki kościelnej. Nie ma mowy, bym pozwoliła ci trzymać porno w kościele.",
    "Well, I wish I could say that was fun…": "Cóż, chciałabym powiedzieć, że było fajnie…",
    "But it was just awkward.": "Ale było tylko niezręcznie.",
    "By the way, how’d it taste? Good, right?": "Swoją drogą, jak smakowało? Dobre, prawda?",
    "Very funny. Let’s not talk about it.": "Bardzo zabawne. Nie rozmawiajmy o tym.",
    "You have the chest?": "Masz skrzynię?",
    "Right here…": "Tutaj…",
    "Let’s see what we got.": "Zobaczmy, co mamy.",
    "Nice! Not a bad haul.": "Nieźle! Niezły łup.",
    "It’s not cursed?": "Nie jest przeklęte?",
    "This is Casula shit… Only the Tikpak shit is cursed.": "To graty Casula… Tylko graty Tikpak są przeklęte.",
    "Sweet!": "Słodziutko!",
    "You know, I did all the real work… All you had to do was unlock a chest.": "Wiesz, ja zrobiłam całą prawdziwą robotę… Ty tylko otworzyłeś skrzynię.",
    "I know, we make such a great team! We’ll have to do this again sometime.": "Wiem, tworzymy świetny zespół! Musimy to kiedyś powtórzyć.",
    "That’s not what I’m implying.": "Nie to mam na myśli.",
    "This is my half… Now give me back Henry.": "To moja połowa… Teraz oddaj mi Henry'ego.",
    "Pleasure doing business, Detective Canmore.": "Przyjemność robić interesy, detektywie Canmore.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=246 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=26: raise SystemExit(f'Expected 26, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map246')
