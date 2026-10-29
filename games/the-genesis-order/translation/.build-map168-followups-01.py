#!/usr/bin/env python3
"""Build Polish drafts for Map 168 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map168-followups-01.jsonl'
TRANSLATIONS = {
    "Jesus, woman! What the hell went on in here?": "Jezu, kobieto! Co tu się, do diabła, działo?",
    "I told you… There’s something odd about this place.": "Mówiłam… Coś dziwnego jest z tym miejscem.",
    "It’s not ghosts. You just have lots of issues that need to be addressed.": "To nie duchy. Po prostu masz masę spraw do załatwienia.",
    "Don’t waste time. We have to investigate Andrea.": "Nie marnuj czasu. Musimy zbadać Andreę.",
    "You’re more obsessed with work than I am… At least I keep my place clean.": "Jesteś bardziej opętana pracą niż ja… Przynajmniej ja utrzymuję dom w czystości.",
    "Did you come here to help or to scold me?": "Przyszłaś tu pomóc czy mnie strofować?",
    "Let me take care of this… I can’t even think with all this noise.": "Zajmę się tym… Nie mogę nawet myśleć przy tym hałasie.",
    "Fine. I’ll just be doing real work while you waste time.": "Dobra. Ja będę wykonywać prawdziwą pracę, gdy ty marnujesz czas.",
    "Wait! Explain exactly what’s happening so I know where to start.": "Czekaj! Wyjaśnij dokładnie, co się dzieje, bym wiedziała, od czego zacząć.",
    "The sink won't shut off, the dryer makes a rumbling sound, and the refrigerator makes noises twice per day for about an hour.": "Kran się nie zakręca, suszarka wydaje dudnienie, a lodówka hałasuje dwa razy dziennie przez około godzinę.",
    "Yeah… It’s not ghosts.": "Tak… To nie duchy.",
    "What an unappreciative bitch!...": "Co za niewdzięczna suka!...",
    "But seriously… She’s going to flood the place or burn it down if someone doesn’t address these issues.": "Ale serio… Zaleje to miejsce albo je spali, jeśli ktoś się tym nie zajmie.",
    "Good God… This thing is going to explode…": "Na Boga… To zaraz wybuchnie…",
    "It’s making a rumbling sound.": "Wydaje dudnienie.",
    "The sink won't shut off…": "Kran się nie zakręca…",
    "Just how expensive is Melissa’s water bill?": "Jak wysoki jest rachunek Melissy za wodę?",
    "Finally! Peace and quiet.": "Nareszcie! Cisza i spokój.",
    "Come by to clean my house?": "Wpadłeś posprzątać mój dom?",
    "Ugh… Not now.": "Ugh… Nie teraz.",
    "Coming to the dinner party tonight?": "Przyjdziesz dziś na kolację?",
    "Of course, Detective Canmore.": "Oczywiście, detektywie Canmore.",
    "See you then, Detective Bhatt.": "Do zobaczenia, detektyw Bhatt.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=168 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=23: raise SystemExit(f'Expected 23, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map168')
