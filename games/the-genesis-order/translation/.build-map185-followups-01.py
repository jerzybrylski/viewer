#!/usr/bin/env python3
"""Build Polish drafts for Map 185 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map185-followups-01.jsonl'
TRANSLATIONS = {
    "I don’t see anything… What do you need?": "Nic nie widzę… Czego potrzebujesz?",
    "You see that chest up on the chandelier? Can you jump up there and cut it down?": "Widzisz tę skrzynię na żyrandolu? Możesz tam wskoczyć i ją ściąć?",
    "I see it!... Watch this.": "Widzę!... Patrz na to.",
    "Is it the amulet?": "To amulet?",
    "I’m afraid not.": "Obawiam się, że nie.",
    "I’ll keep looking.": "Będę dalej szukać.",
    "I’ve spent a lot of time in this mansion and I’ve never seen this before.": "Spędziłam dużo czasu w tej rezydencji i nigdy tego nie widziałam.",
    "Shit… It’s Daemalius.": "Cholera… To Daemalius.",
    "A powerful demon… We have to get you ladies out of here.": "Potężny demon… Musimy wyprowadzić panie stąd.",
    "It seems safe here. We must not be near metal.": "Tu wydaje się bezpiecznie. Musimy nie być blisko metalu.",
    "If it’s a lightning storm, we have to watch our step.": "Jeśli to burza z piorunami, musimy uważać na krok.",
    "I’ll guide everyone out… one at a time.": "Wyprowadzę wszystkich… jedno po drugim.",
    "I’m scared, 1Hero!": "Boję się, 1Hero!",
    "Judy! Come with me!": "Judy! Chodź ze mną!",
    "Everyone, stay where it’s safe. I’ll be back.": "Wszyscy zostańcie tam, gdzie bezpiecznie. Wrócę.",
    "Oh, what the hell.": "O, do cholery.",
    "1Hero! You’re safe!": "1Hero! Jesteś bezpieczny!",
    "She’s safe under the mansion. We can wait out whatever this is there.": "Ona jest bezpieczna pod rezydencją. Możemy tam przeczekać, cokolwiek to jest.",
    "Chloe… You’re next. Come with me.": "Chloe… Teraz ty. Chodź ze mną.",
    "I know a clear path! Everyone, follow me!": "Znam czystą ścieżkę! Wszyscy za mną!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=185 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=20: raise SystemExit(f'Expected 20, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map185')
