#!/usr/bin/env python3
"""Build Polish drafts for Map 66 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map66-followups-01.jsonl'
TRANSLATIONS = {
    "You know, you’re hard to work with sometimes.": "Wiesz, czasem ciężko się z tobą pracuje.",
    "If you can’t handle it, you can request a transfer.": "Jeśli nie dajesz rady, możesz poprosić o przeniesienie.",
    "I can handle anything.": "Dam radę ze wszystkim.",
    "Of course that’s what you would believe.": "Oczywiście, że tak uważasz.",
    "Are we going to look for a way out, or argue?": "Będziemy szukać wyjścia, czy się kłócić?",
    "I knew I could figure it out.": "Wiedziałam, że to rozgryzę.",
    "Don’t get cocky, 1Hero. We still don’t know where this leads.": "Nie bądź zarozumiały, 1Hero. Wciąż nie wiemy, dokąd to prowadzi.",
    "Only one way to find out.": "Jeden sposób, by się przekonać.",
    "I can see something on that statue. I wonder if I could throw something at it and knock it down.": "Widzę coś na posągu. Ciekawe, czy mogłabym w to czymś rzucić i strącić.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=66 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=9: raise SystemExit(f'Expected 9, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map66')
