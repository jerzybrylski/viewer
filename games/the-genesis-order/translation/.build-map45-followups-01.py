#!/usr/bin/env python3
"""Build Polish drafts for Map 45 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map45-followups-01.jsonl'
TRANSLATIONS = {
    "If you need to change your clothes, use the damn restroom!": "Jeśli musisz się przebrać, użyj cholernej łazienki!",
    "I can hear something on top of the locker. But I can’t jump high enough to reach it.": "Słyszę coś na szafce. Ale nie doskoczę tak wysoko, by to dosięgnąć.",
    "Who is this?": "Kto to?",
    "It’s me, 1Hero.": "To ja, 1Hero.",
    "You found my phone!": "Znalazłeś mój telefon!",
    "I sure did. It was on top of the locker.": "Owszem. Był na szafce.",
    "Silly me. I must have lost it there.": "Głupia ja. Pewnie go tam zgubiłam.",
    "Meet me at the diner, I can get it back from you there.": "Spotkajmy się w barze, tam go od ciebie odbiorę.",
    "Dick’s Grill?": "Dick's Grill?",
    "Yeah, that’s the one.": "Tak, ten.",
    "I don’t want to talk right now. There’s too many people around.": "Nie chcę teraz rozmawiać. Jest tu zbyt wielu ludzi.",
    "I’m just frazzled, that’s all.": "Jestem tylko roztrzęsiona, to wszystko.",
    "I didn’t think you’d take fighting so seriously.": "Nie sądziłem, że weźmiesz walkę tak poważnie.",
    "It’s not…": "To nie…",
    "Jealous? Of Diana’s fighting skills?": "Zazdrosna? O umiejętności walki Diany?",
    "No. I’m worried you’ll have sex with those girls.": "Nie. Martwię się, że prześpisz się z tymi dziewczynami.",
    "Huh? I didn’t take you for the jealous type.": "Huh? Nie brałam cię za zazdrosną.",
    "Just… Forget it. It’s nothing.": "Po prostu… Zapomnij. Nieważne.",
    "I’m not working with her, Ella. I’m fighting against the Eclipse Guild.": "Nie współpracuję z nią, Ella. Walczę przeciw Gildii Eclipse.",
    "What’s all that noise?...": "Co to za hałas?...",
    "Larry! I’m changing!": "Larry! Przebieram się!",
    "Ella’s… boobs!": "Cycki Elli!",
    "Fuck! Make a run for it!": "Kurwa! Wiejemy!",
    "Ella!?": "Ella!?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=45 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=24: raise SystemExit(f'Expected 24, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map45')
