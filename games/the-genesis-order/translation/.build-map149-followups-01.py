#!/usr/bin/env python3
"""Build Polish drafts for Map 149 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map149-followups-01.jsonl'
TRANSLATIONS = {
    "Come on. We’re really close.": "Chodź. Jesteśmy naprawdę blisko.",
    "Kill’em!": "Zabić ich!",
    "Hey, guys… Uhh… I’m the maid.": "Hej, panowie… Yyy… Jestem pokojówką.",
    "Looking for more trouble, Mr. Canmore?": "Szukasz więcej kłopotów, panie Canmore?",
    "You don’t look so tough.": "Nie wyglądasz groźnie.",
    "Yes, he does!": "Owszem, wygląda!",
    "I suppose I should kill you… But maybe I’ll just kill grandpa and the girls.": "Chyba powinienem cię zabić… Ale może po prostu zabiję dziadka i dziewczyny.",
    "I’m a priest. You’d go straight to hell.": "Jestem księdzem. Trafiłeś prosto do piekła.",
    "I’m going to hell anyways.": "I tak idę do piekła.",
    "Stop! Wait!": "Stój! Czekaj!",
    "Give us the word and we’ll fill them with lead.": "Daj nam znak, a naszpikujemy ich ołowiem.",
    "No… The old lady wouldn’t like that. She has other plans.": "Nie… Staruszka by tego nie chciała. Ma inne plany.",
    "Madalyn!": "Madalyn!",
    "What does she want with us?": "Czego od nas chce?",
    "I don’t know and I don’t care. But consider yourselves lucky.": "Nie wiem i nie obchodzi mnie. Ale uważajcie się za szczęściarzy.",
    "She’s here, young lady.": "Ona tu jest, młoda damo.",
    "Take them to the holding room.": "Zabierzcie ich do pokoju przetrzymywania.",
    "Where are you taking us?": "Dokąd nas zabieracie?",
    "Shut up and move!": "Zamknij się i ruszaj!",
    "She’s using you, and when she’s done she’ll kill you.": "Wykorzystuje cię i gdy skończy, zabije cię.",
    "Shut up, bitch!": "Zamknij się, suko!",
    "Watch your language!": "Uważaj na język!",
    "Move it, grandpa.": "Ruszaj, dziadku.",
    "You better figure this out fast.": "Lepiej szybko to rozgryź.",
    "Why don’t you come in and spend some one-on-one time with me in the meantime, detective?": "Może w międzyczasie wpadniesz i spędzisz trochę czasu sam na sam ze mną, detektywie?",
    "Hahahahahahahaha!": "Hahahahahahahaha!",
    "1Hero!...": "1Hero!...",
    "I’ll work faster!": "Popracuję szybciej!",
    "What the hell is going on, 1Hero?": "Co się dzieje, 1Hero?",
    "There she is!": "Tam jest!",
    "Carol? Heather?... What’s everyone doing here?": "Carol? Heather?... Co wszyscy tu robią?",
    "We’re looking for Hannah.": "Szukamy Hannah.",
    "I’m not going back to the church!": "Nie wracam do kościoła!",
    "Where is everyone? Where is Father Solomon?": "Gdzie wszyscy? Gdzie jest ojciec Solomon?",
    "Everyone’s waiting at the rift.": "Wszyscy czekają przy szczelinie.",
    "Are we going to see it?": "Zobaczymy ją?",
    "No! We’re getting you ladies back to safety.": "Nie! Sprowadzamy was z powrotem w bezpieczne miejsce.",
    "Where is Erica? Did you save her?": "Gdzie jest Erica? Uratowałeś ją?",
    "It’s complicated… We’re working on it.": "To skomplikowane… Pracujemy nad tym.",
    "What in tarnations!?": "Co u diabła!?",
    "Everyone, watch out!": "Uważajcie wszyscy!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=149 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=41: raise SystemExit(f'Expected 41, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map149')
