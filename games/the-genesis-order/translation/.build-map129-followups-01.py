#!/usr/bin/env python3
"""Build Polish drafts for Map 129 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map129-followups-01.jsonl'
TRANSLATIONS = {
    "Does she want me to get in the hot tub?...": "Chce, żebym wszedł do jacuzzi?...",
    "I see you’ve made yourself at home.": "Widzę, że zadomowiłeś się.",
    "Damn, Andrea. You look good in that bikini.": "Cholera, Andrea. Świetnie wyglądasz w tym bikini.",
    "How about a drink of champagne, young man?": "Może kieliszek szampana, młodzieńcze?",
    "What have we here?...": "Cóż my tu mamy?...",
    "You do know how to shoot a gun, don’t you, 1Hero?": "Umiesz strzelać z pistoletu, prawda, 1Hero?",
    "I do. But what about you?": "Umiem. A ty?",
    "Heh. You bet I’ll be ready.": "Heh. Na pewno będę gotowa.",
    "How long has she been undercover?": "Jak długo jest pod przykrywką?",
    "Ever since she tried to escape from prison.": "Odkąd próbowała uciec z więzienia.",
    "Your type of agent?": "Agentka w twoim typie?",
    "You’re getting it, 1Hero. That woman has talent…": "Łapiesz, 1Hero. Ta kobieta ma talent…",
    "And best of all, she’s exactly the type of woman the Guild would use.": "I co najlepsze, to dokładnie typ kobiety, który Gildia by wykorzystała.",
    "As far as Duncan knows, she was successful in escaping prison.": "Z tego co Duncan wie, udało jej się uciec z więzienia.",
    "Heh. Not a bad idea.": "Heh. Niezły pomysł.",
    "I’ve been doing this a long time.": "Robię to od dawna.",
    "Get dressed, 1Hero. And stay alert. I could call you at any time.": "Ubierz się, 1Hero. I bądź czujny. Mogę zadzwonić w każdej chwili.",
    "Yeah… I get it.": "Taa… Rozumiem.",
    "Here’s my contact. Feel free to call me.": "Tu masz mój kontakt. Śmiało dzwoń.",
    "I’m always willing to have a little… chat.": "Zawsze chętnie… pogadam.",
    "Going to disappear again?": "Znikniesz znowu?",
    "Maybe. If I do, I’ll make sure you have a way to get in touch.": "Może. Jeśli tak, upewnię się, że masz sposób, by się ze mną skontaktować.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=129 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=22: raise SystemExit(f'Expected 22, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map129')
