#!/usr/bin/env python3
"""Build Polish drafts for Map 107 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map107-followups-01.jsonl'
TRANSLATIONS = {
    "You’re scaring me, 1Hero.": "Przerażasz mnie, 1Hero.",
    "I’ll be back. If anything happens, call me…": "Wrócę. Jeśli coś się stanie, zadzwoń do mnie…",
    "I think we’re getting close to figuring out what’s going on in this city.": "Myślę, że zbliżamy się do rozgryzienia, co dzieje się w tym mieście.",
    "1Hero!?": "1Hero!?",
    "Ella!?": "Ella!?",
    "Ella! Quiet down! I’m looking for Duncan.": "Ella! Ciszej! Szukam Duncana.",
    "Ella’s a former Guild thief… Duncan’s been looking for her.": "Ella to była złodziejka Gildii… Duncan jej szuka.",
    "And you’re Duncan’s right-hand woman.": "A ty jesteś prawą ręką Duncana.",
    "I am not!": "Nie jestem!",
    "She’s a spy.": "Ona jest szpiegiem.",
    "Hey!? What’s going on in there?": "Hej!? Co tam się dzieje?",
    "Shit! She’s not supposed to be here.": "Cholera! Nie powinna tu być.",
    "No shit, I’m not. I’m here for Duncan.": "Jasne, że nie powinnam. Przyszłam po Duncana.",
    "You’re going to die…": "Umrzesz…",
    "If anything’s hidden here, we’ll find it… But it’ll take some time.": "Jeśli coś tu ukryto, znajdziemy to… Ale zajmie to trochę czasu.",
    "I’d say this is like finding a needle in a haystack, but I’ve learned not to underestimate you.": "Powiedziałabym, że to jak szukanie igły w stogu siana, ale nauczyłam się cię nie nie doceniać.",
    "Boo!": "Buu!",
    "Hannah!?": "Hannah!?",
    "Surprised to see me?": "Zaskoczony, że mnie widzisz?",
    "I’m here to help! Tell me what to do.": "Przyszłam pomóc! Powiedz, co robić.",
    "Go back to the church! You shouldn’t be here!": "Wracaj do kościoła! Nie powinnaś tu być!",
    "Like hell! What are you looking for? You clearly need something.": "Gówno prawda! Czego szukasz? Wyraźnie czegoś potrzebujesz.",
    "I’m looking for demon parts.": "Szukam części demona.",
    "I can help find them! I know what they look like!": "Mogę pomóc je znaleźć! Wiem, jak wyglądają!",
    "What!? No, you don’t!": "Co!? Nie, nie wiesz!",
    "That won’t stop me!": "To mnie nie powstrzyma!",
    "Fine… Stay close to me. Look for long blonde hairs on the ground.": "Dobra… Trzymaj się blisko mnie. Szukaj długich blond włosów na ziemi.",
    "Hairs?": "Włosów?",
    "Lillian’s hairs can trigger the rift.": "Włosy Lillian mogą wywołać szczelinę.",
    "Wow! Chloe’s going to love hearing about this.": "Łał! Chloe pokocha usłyszeć o tym.",
    "Stay close.": "Trzymaj się blisko.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=107 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=31: raise SystemExit(f'Expected 31, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map107')
