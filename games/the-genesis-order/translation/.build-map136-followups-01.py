#!/usr/bin/env python3
"""Build Polish drafts for Map 136 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map136-followups-01.jsonl'
TRANSLATIONS = {
    "I have to be careful. Diana said that a trap might trigger if the security system is not turned off.": "Muszę uważać. Diana mówiła, że pułapka może się uruchomić, jeśli system zabezpieczeń nie zostanie wyłączony.",
    "I can't leave yet.": "Nie mogę jeszcze odejść.",
    "God damn it. Now what?": "Cholera. Co teraz?",
    "Oh, yes. I’ve been here before…": "O tak. Byłem tu już wcześniej…",
    "This leads to that creepy chapel.": "To prowadzi do tej upiornej kaplicy.",
    "Wilkes’ private church…": "Prywatny kościół Wilkesa…",
    "I take it this door isn’t supposed to be locked.": "Zakładam, że te drzwi nie powinny być zamknięte.",
    "Something must have triggered the security system.": "Coś musiało uruchomić system zabezpieczeń.",
    "Don’t worry. There’s got to be something close by that will reset the system.": "Spokojnie. Gdzieś w pobliżu musi być coś, co zresetuje system.",
    "Looks like I figured it out.": "Wygląda na to, że to rozgryzłem.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=136 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=10: raise SystemExit(f'Expected 10, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map136')
