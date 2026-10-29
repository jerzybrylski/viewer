#!/usr/bin/env python3
"""Build Polish drafts for Map 68 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map68-followups-01.jsonl'
TRANSLATIONS = {
    "Damn! How much farther does this go down?": "Cholera! Jak głęboko to schodzi?",
    "Looks like it could connect with the cave system.": "Wygląda, jakby mogło łączyć się z systemem jaskiń.",
    "I’m going to have a hard time explaining our absence to Lillian.": "Będę miał problem z wytłumaczeniem naszej nieobecności Lillian.",
    "Think of something, 1Hero. I suspect Lillian knows more than she’s letting on.": "Wymyśl coś, 1Hero. Podejrzewam, że Lillian wie więcej, niż mówi.",
    "I just don’t understand why there’s been twenty years since the last clue surfaced…": "Po prostu nie rozumiem, czemu minęło dwadzieścia lat od ostatniej wskazówki…",
    "If Charles truly was a Guild leader, how did he hide it for so long?": "Jeśli Charles naprawdę był przywódcą Gildii, jak ukrywał to tak długo?",
    "Let’s not get ahead of ourselves. If we can’t find our way out of here, that might be the least of our worries.": "Nie wybiegajmy w przyszłość. Jeśli nie znajdziemy wyjścia stąd, to może być najmniejsze zmartwienie.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=68 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=7: raise SystemExit(f'Expected 7, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map68')
