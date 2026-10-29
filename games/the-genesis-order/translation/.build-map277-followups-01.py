#!/usr/bin/env python3
"""Build Polish drafts for Map 277 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map277-followups-01.jsonl'
TRANSLATIONS = {
    "1Hero!": "1Hero!",
    "You snoop.": "Ty podglądaczu.",
    "What was that you just picked up?": "Co to właśnie podniosłeś?",
    "If you must know, it’s an old relic from a war fought long ago.": "Jeśli musisz wiedzieć, to stara relikwia z dawnej wojny.",
    "A relic? Why was it locked up in a place like this?": "Relikwia? Czemu była zamknięta w takim miejscu?",
    "Seems you’ve activated a trap.": "Wygląda, że aktywowałeś pułapkę.",
    "Me!? How do you know it wasn’t you?": "Ja!? Skąd wiesz, że to nie ty?",
    "What are you doing here, Lillian?": "Co tu robisz, Lillian?",
    "Being trapped with you, apparently.": "Utknęłam tu z tobą, najwyraźniej.",
    "I know the cause of your troubles, 1Hero.": "Znam przyczynę twoich kłopotów, 1Hero.",
    "Can I?": "Mogę?",
    "Please… I need your trust.": "Proszę… Potrzebuję twojego zaufania.",
    "I can’t say I understand your world or what you see as a utopia… But you have a good heart.": "Nie powiem, że rozumiem twój świat ani to, co uważasz za utopię… Ale masz dobre serce.",
    "I won’t let you down… I won't let any of my children down.": "Nie zawiodę cię… Nie zawiodę żadnego z moich dzieci.",
    "Come on, Lillian… It’s time to figure a way out of this place. If we work together, I’m sure we can figure it out.": "Chodź, Lillian… Czas znaleźć wyjście z tego miejsca. Jeśli popracujemy razem, na pewno coś wymyślimy.",
    "Hahaha! Oh, 1Hero, you are too funny.": "Hahaha! Och, 1Hero, jesteś zbyt zabawny.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=277 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=16: raise SystemExit(f'Expected 16, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map277')
