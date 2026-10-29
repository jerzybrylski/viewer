#!/usr/bin/env python3
"""Build Polish drafts for Map 230 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map230-followups-01.jsonl'
TRANSLATIONS = {
    "I have to go back to the station. I left my gun on my desk.": "Muszę wrócić na komendę. Zostawiłam broń na biurku.",
    "Oh, God. Melissa, you’re so unorganized.": "O Boże. Melissa, jesteś taka niezorganizowana.",
    "Not now, 1Hero.": "Nie teraz, 1Hero.",
    "Let me ask you… How did you do on your exam?": "Pozwól, że spytam… Jak poszedł ci egzamin?",
    "Exam?": "Egzamin?",
    "To get your gun… Did you have to hit targets?": "Na broń… Musiałaś trafiać w cele?",
    "I’m sure I did better than you.": "Jestem pewna, że poszło mi lepiej niż tobie.",
    "I don’t know about that. I’m a natural.": "Nie wiem. Jestem naturalnym talentem.",
    "Why don’t we make a bet?": "Może się założymy?",
    "What kind of bet?": "O jaki zakład?",
    "Come with me to the station. Let’s go to the shooting range…": "Chodź ze mną na komendę. Pójdźmy na strzelnicę…",
    "If I win, you have to be my maid for a month.": "Jeśli wygram, musisz być moją pokojówką przez miesiąc.",
    "What!? No way! You’re a slob!": "Co!? Nie ma mowy! Jesteś fleją!",
    "How dare you!? I’m not a slob!": "Jak śmiesz!? Nie jestem fleją!",
    "Fine… But if I win, you have to fuck me in the office.": "Dobra… Ale jeśli wygram, musisz mnie przelecieć w biurze.",
    "You’re going to get us both fired.": "Przez to oboje wylecimy.",
    "We just can’t get caught.": "Po prostu nie możemy dać się złapać.",
    "It won’t matter… You’re not going to win.": "Nieważne… I tak nie wygrasz.",
    "Then it’s a deal?": "Więc stoi?",
    "Come on, 1Hero… You have yourself a bet.": "Dawaj, 1Hero… Masz zakład.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=230 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=20: raise SystemExit(f'Expected 20, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map230')
