#!/usr/bin/env python3
"""Build Polish drafts for Map 252 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map252-followups-01.jsonl'
TRANSLATIONS = {
    "Detective! I was attacked!": "Detektywie! Zaatakowano mnie!",
    "Attacked?": "Zaatakowano?",
    "He was too fast! I couldn’t catch him!": "Był za szybki! Nie mogłem go złapać!",
    "One moment I was inspecting the storage…": "Chwilę temu sprawdzałem magazyn…",
    "Then I moved back for a moment and something bumped me from behind.": "Potem cofnąłem się na moment i coś uderzyło mnie od tyłu.",
    "Before I knew what happened, these boxes dropped on me!": "Zanim się zorientowałem, te pudła spadły na mnie!",
    "You didn’t see them?": "Nie widziałeś ich?",
    "Yeah… I totally saw who did it and arrested them. We’re safe now.": "Taa… Totalnie widziałem, kto to zrobił i go aresztowałem. Teraz jesteśmy bezpieczni.",
    "… Really.": "… Serio.",
    "The building’s definitely secure now! Mission accomplished!": "Budynek na pewno teraz bezpieczny! Misja wykonana!",
    "Buddy would be proud of us.": "Buddy byłby z nas dumny.",
    "Riiight…": "Taaa…",
    "Let me see if I can help you out of this mess.": "Zobaczę, czy mogę cię wyciągnąć z tego bałaganu.",
    "Thanks, detective!": "Dzięki, detektywie!",
    "Come on, Simon, let’s head back to the studio to watch your mom’s interview finish.": "Chodź, Simon, wracajmy do studia oglądać końcówkę wywiadu twojej mamy.",
    "I thought I wasn’t supposed to be there?": "Myślałem, że nie powinienem tam być?",
    "Don’t worry about that.": "Nie martw się tym.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=252 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=17: raise SystemExit(f'Expected 17, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map252')
