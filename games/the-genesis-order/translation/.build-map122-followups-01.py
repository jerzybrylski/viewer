#!/usr/bin/env python3
"""Build Polish drafts for Map 122 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map122-followups-01.jsonl'
TRANSLATIONS = {
    "You sneaky bastard.": "Ty przebiegły draniu.",
    "I didn’t take you for the church type, detective.": "Nie brałem cię za kościelny typ, detektywie.",
    "Am I under arrest?": "Jestem aresztowany?",
    "This place is surrounded. You’re not going anywhere.": "To miejsce jest otoczone. Nigdzie nie pójdziesz.",
    "You're bluffing, detective.": "Blefuujesz, detektywie.",
    "Care to take that gamble?": "Chcesz zaryzykować?",
    "Heh… It’s not a gamble.": "Heh… To nie hazard.",
    "What the hell is he doing here?": "Co on, do diabła, tu robi?",
    "I was just wondering the same thing.": "Właśnie się nad tym samym zastanawiałam.",
    "It’s over. You’re all under arrest!": "Koniec. Wszyscy jesteście aresztowani!",
    "Haha. I don’t think so.": "Haha. Nie sądzę.",
    "What are you going to do, girly man?": "Co zamierzasz zrobić, fircyku?",
    "Bag him. He’s coming with us.": "Zaworek. Zabieramy go ze sobą.",
    "Are you sure that’s a good idea?": "Jesteś pewien, że to dobry pomysł?",
    "You’re making a mistake, Duncan.": "Popełniasz błąd, Duncan.",
    "You’re the one who made a mistake, officer.": "To ty popełniłeś błąd, oficerze.",
    "Let’s move. We’ve got to get out here before his backup arrives.": "Ruszamy. Musimy się stąd wydostać, zanim przybędą jego posiłki.",
    "Where are you bringing me?": "Gdzie mnie zabieracie?",
    "What about the amulet? We have to find it.": "A co z amuletem? Musimy go znaleźć.",
    "The boss said we’ve got to move, so let’s move.": "Szef kazał się ruszać, więc się ruszamy.",
    "Watch your step detective…": "Uważaj na krok, detektywie…",
    "A rat!": "Szczur!",
    "… Could I put it in something and keep it?": "… Mógłbym go w coś włożyć i zatrzymać?",
    "This pillar looks weak. I wonder what would happen if I hit it with a pickaxe.": "Ten filar wygląda słabo. Zastanawiam się, co by się stało, gdybym uderzył go kilofem.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=122 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=24: raise SystemExit(f'Expected 24, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map122')
