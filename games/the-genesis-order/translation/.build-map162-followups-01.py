#!/usr/bin/env python3
"""Build Polish drafts for Map 162 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map162-followups-01.jsonl'
TRANSLATIONS = {
    "Wow! Is this a Casula ruin?": "Łał! Czy to ruina Casula?",
    "Probably so. I can’t imagine what else it could be.": "Pewnie tak. Nie wyobrażam sobie, co innego mogłoby to być.",
    "What’s the puzzle?": "Jaka jest łamigłówka?",
    "Oh! I get it.": "O! Rozumiem.",
    "We’re going to need a tractor with a demolition arm if we’re to break open that rock.": "Będziemy potrzebować traktora z ramieniem wyburzeniowym, by rozbić tę skałę.",
    "No! Hannah! We just need to step on the pegs.": "Nie! Hannah! Musimy tylko stanąć na kołkach.",
    "That’s what I was thinking.": "O tym właśnie myślałam.",
    "I suppose we can try it your way.": "Chyba możemy spróbować twoim sposobem.",
    "Finders keepers!": "Kto pierwszy, ten lepszy!",
    "Hannah! Put it down!": "Hannah! Odłóż to!",
    "You’re even better than your mom!": "Jesteś nawet lepsza niż twoja mama!",
    "What did you all do while I was inside?": "Co robiliście, gdy byłam w środku?",
    "Nothing you didn’t do with my ma.": "Nic, czego nie robiłaś z moją mamą.",
    "Don’t be such a baby. We fucked each other’s moms. Who cares?": "Nie bądź taką beksą. Pieprzyliśmy się nawzajem z mamami. Kogo to obchodzi?",
    "Why didn’t you ask first?": "Czemu nie spytałaś najpierw?",
    "To be fair, we never asked Hannah before we did her mom.": "Sprawiedliwie, nigdy nie pytałyśmy Hannah, zanim pieprzyłyśmy jej mamę.",
    "Yeah… But…": "Tak… Ale…",
    "Sounds like you’re wanting special treatment.": "Brzmi, jakbyś chciała specjalnego traktowania.",
    "No!... Just… Don’t tell me… I don’t want to hear it.": "Nie!... Po prostu… Nie mów mi… Nie chcę tego słyszeć.",
    "Fine. I won’t tell you about the face ride she gave me and I don’t want to hear about you eating my ma’s ass.": "Dobra. Nie opowiem ci o face ride, jaki mi zafundowała, i nie chcę słyszeć o tym, jak obciągałaś dupę mojej mamy.",
    "I never told you that.": "Nigdy ci tego nie mówiłam.",
    "I just assumed… I mean, she’s got such a fat ass.": "Po prostu założyłam… Mam na myśli, ma taki wielki tyłek.",
    "Well… You guessed right, Hannah.": "Cóż… Zgadłaś, Hannah.",
    "Ewww!": "Fuj!",
    "You watched Ella eat your mom’s ass.": "Patrzyłaś, jak Ella liże dupę twojej mamy.",
    "Just what all have you been up to?": "Co wyście wyprawiali?",
    "Fine. No more sex talk… Unless you want to rub pussies or blow our privates.": "Dobra. Koniec z gadaniem o seksie… Chyba że chcecie pocierać cipki lub obciągać sobie ptaszki.",
    "We need to work on your language skills, Hannah.": "Musimy popracować nad twoimi umiejętnościami językowymi, Hannah.",
    "What about the artifact?": "A co z artefaktem?",
    "I can sell it to the warehouse owner… I’m a licensed artifact dealer.": "Mogę go sprzedać właścicielowi magazynu… Jestem licencjonowanym handlarzem artefaktów.",
    "You get us our money and then you can buy the boat.": "Załatwisz nam kasę, a potem możesz kupić łódź.",
    "I want to tell Sister Judy about the artifact!": "Chcę opowiedzieć siostrze Judy o artefakcie!",
    "Hannah! You forgot your clothes!": "Hannah! Zapomniałaś ubrań!",
    "Something is off about this location, but I’m not sure what it is.": "Coś jest nie tak z tym miejscem, ale nie jestem pewna co.",
    "A code. How am I supposed to crack the code?": "Kod. Jak mam złamać kod?",
    "There are initials… KC?": "Są inicjały… KC?",
    "KC… It couldn’t be…": "KC… To niemożliwe…",
    "Time to have a chat with Heather about this.": "Czas pogadać z Heather o tym.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=162 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=38: raise SystemExit(f'Expected 38, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map162')
