#!/usr/bin/env python3
"""Build Polish drafts for Map 69 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map69-followups-01.jsonl'
TRANSLATIONS = {
    "Come on. The creek is this way.": "Chodź. Strumień jest w tę stronę.",
    "Wait a minute. Is that a white dog up on the cliff side?": "Chwila. Czy to biały pies na zboczu klifu?",
    "What is that?": "Co to jest?",
    "Well, I’ll be damned. That’s a baby goat.": "Niech mnie diabli. To koźlątko.",
    "Where’s its mother?": "Gdzie jego matka?",
    "I see them around here every now and then. But I’ve never seen a baby all alone…": "Widuję je tu od czasu do czasu. Ale nigdy nie widziałam samego malucha…",
    "It’s not safe.": "To niebezpieczne.",
    "How’d he get up there?": "Jak on tam wszedł?",
    "Goats are amazing climbers.": "Kozy są niesamowitymi wspinaczami.",
    "We can’t leave him there. He’ll fall.": "Nie możemy go tam zostawić. Spadnie.",
    "I doubt he’d fall, but without a mother around the coyotes will get him.": "Wątpię, by spadł, ale bez matki w pobliżu dorwą go kojoty.",
    "How the hell are we going to reach it?": "Jak, u diabła, mamy do niego dotrzeć?",
    "I might be able to get to him.": "Może uda mi się do niego dostać.",
    "Get him down, 1Hero. Hannah would love a new pet.": "Zdejmij go, 1Hero. Hannah pokocha nowego pupila.",
    "What ever happened to those kittens you had?": "Co się stało z tymi kociakami, które miałaś?",
    "I’m sorry I asked.": "Przepraszam, że spytałam.",
    "If you don’t save him by dinner, he’s gonna be in the belly of a coyote.": "Jeśli nie uratujesz go do kolacji, wyląduje w brzuchu kojota.",
    "Hurry, 1Hero. I don’t want the baby goat to fall.": "Pospiesz się, 1Hero. Nie chcę, by koźlątko spadło.",
    "Come on, little fella’. Here’s some food.": "Chodź, maluszku. Mam jedzenie.",
    "Grab him, 1Hero!": "Łap go, 1Hero!",
    "He’s getting away!": "Ucieka!",
    "Come here little goat. I have a treat for you.": "Chodź, mała kózko. Mam dla ciebie przysmak.",
    "I don’t think he’s interested in that, 1Hero.": "Nie sądzę, by był tym zainteresowany, 1Hero.",
    "Gatorzilla is so cute!": "Gatorzilla jest taki słodki!",
    "Thanks for your help, 1Hero! I made two new friends today…": "Dzięki za pomoc, 1Hero! Zyskałam dziś dwóch nowych przyjaciół…",
    "Alia and Gatorzilla.": "Alię i Gatorzillę.",
    "Don’t you want to name it something else?": "Nie chcesz nazwać go jakoś inaczej?",
    "What’s wrong with Gatorzilla?": "Co złego w Gatorzilla?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=69 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=28: raise SystemExit(f'Expected 28, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map69')
