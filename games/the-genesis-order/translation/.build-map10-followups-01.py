#!/usr/bin/env python3
"""Build Polish drafts for Map 10 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map10-followups-01.jsonl'
TRANSLATIONS = {
    "The sun is setting. I wonder if I’ll find Tasha’s friends.": "Słońce zachodzi. Ciekawe, czy znajdę przyjaciół Tashy.",
    "I have to be careful that I don't get seen…": "Muszę uważać, by nikt mnie nie zobaczył…",
    "What the hell? Who were those people?": "Co do cholery? Kim byli ci ludzie?",
    "Who is Duncan Helmer?": "Kim jest Duncan Helmer?",
    "The woman… She believes Charles was murdered too?": "Ta kobieta… Ona też wierzy, że Charles został zamordowany?",
    "I should tell Miss Bhatt.": "Powinienem powiedzieć pannie Bhatt.",
    "But will she believe me? She doesn’t trust my motives.": "Ale czy mi uwierzy? Nie ufa moim motywom.",
    "I should look up Duncan at the station… Figure out who he is.": "Powinienem sprawdzić Duncana na komendzie… Dowiedzieć się, kim jest.",
    "Well, I’ll be damned! It’s a path!": "Niech mnie diabli! To ścieżka!",
    "Let’s follow it!": "Chodźmy nią!",
    "Don’t worry, 1Hero. I won’t tell anyone about what happened…": "Nie martw się, 1Hero. Nikomu nie powiem o tym, co się stało…",
    "But if you’d like… I can talk to Sister Judy.": "Ale jeśli chcesz… Mogę porozmawiać z siostrą Judy.",
    "Maybe we shouldn’t tell a nun about something like that.": "Może nie powinniśmy mówić zakonnicy o czymś takim.",
    "A nun’s not gonna help you. If you get the itch, and your girlfriend ain’t around, give me a call.": "Zakonnica ci nie pomoże. Jeśli cię zaswędzi, a dziewczyny nie będzie w pobliżu, zadzwoń do mnie.",
    "I don’t have a girlfriend!": "Nie mam dziewczyny!",
    "Sorry it wasn’t more peaceful.": "Przepraszam, że nie było spokojniej.",
    "I miss spending time with you.": "Tęsknię za spędzaniem z tobą czasu.",
    "I do too.": "Ja też.",
    "Maybe one day you’ll come to church with me.": "Może kiedyś pójdziesz ze mną do kościoła.",
    "Maybe I will.": "Może pójdę.",
    "What the hell was that?...": "Co to, do cholery, było?...",
    "I need to talk to Jon at the warehouse. He deals with Casula artifacts…": "Muszę pogadać z Jonem w magazynie. Handluje artefaktami Casula…",
    "He might know what this artifact fragment is.": "Może będzie wiedział, czym jest ten fragment artefaktu.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=10 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=23: raise SystemExit(f'Expected 23, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map10')
