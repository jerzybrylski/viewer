#!/usr/bin/env python3
"""Build Polish drafts for Map 127 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map127-followups-01.jsonl'
TRANSLATIONS = {
    "Detective Canmore, isn’t it?": "Detektyw Canmore, prawda?",
    "I’m the new commissioner, Mr. Smithfield. It’s good to finally meet our famous detective in person.": "Jestem nowym komisarzem, panie Smithfield. Miło wreszcie poznać słynnego detektywa osobiście.",
    "The pleasure is mine, Commissioner Smithfield.": "Cała przyjemność po mojej stronie, komisarzu Smithfield.",
    "Woah, is someone in trouble?": "Łał, ktoś ma kłopoty?",
    "What’s the matter, commissioner?": "Co się stało, komisarzu?",
    "My wallet! It’s gone!": "Mój portfel! Zniknął!",
    "I’m sure it’ll turn up. You probably just dropped it somewhere.": "Jestem pewna, że się znajdzie. Pewnie go gdzieś upuściłeś.",
    "I don’t think that’s right… I’m not forgetful like that.": "Nie sądzę… Nie jestem aż tak zapominalski.",
    "Alright. Where do you think it ended up?": "Dobra. Gdzie myślisz, że się podział?",
    "Do I look like a detective? That’s your job.": "Wyglądam na detektywa? To twoja robota.",
    "Uhh… right. I’ll get right on that.": "Yyy… jasne. Zaraz się tym zajmę.",
    "I’m sure it must be around here somewhere in the station.": "Jestem pewna, że musi być gdzieś tu na komendzie.",
    "Have you recovered my wallet yet? It must still be in the station somewhere.": "Odzyskałeś już mój portfel? Musi wciąż być gdzieś na komendzie.",
    "Good news!": "Dobre wieści!",
    "My wallet! Good work, Detective Canmore. So you caught the thief?": "Mój portfel! Dobra robota, detektywie Canmore. Więc złapałeś złodzieja?",
    "No, sir. I found the wallet in the gym.": "Nie, sir. Znalazłem portfel na siłowni.",
    "The gym? Could I have left it there by accident?… I’m not usually that clumsy.": "Na siłowni? Mógłbym go tam przypadkiem zostawić?… Zwykle nie jestem taki niezdarny.",
    "I don’t know what to tell you, commissioner.": "Nie wiem, co panu powiedzieć, komisarzu.",
    "We should be on high alert. Something seems off.": "Powinniśmy być czujni. Coś jest nie tak.",
    "Officers, stay here and guard the office until I get back from my meeting.": "Funkcjonariusze, zostańcie i pilnujcie biura, aż wrócę ze spotkania.",
    "Good work, detective. But keep your eyes peeled for any suspicious activity.": "Dobra robota, detektywie. Ale miej oko na podejrzaną aktywność.",
    "Hey, I have some new evidence for the commissioner.": "Hej, mam nowe dowody dla komisarza.",
    "The commissioner? Why not submit it directly to the property room?": "Dla komisarza? Czemu nie złożyć ich bezpośrednio do depozytu?",
    "It has to do with the Eclipse Guild. It’s from the Wilkes mansion. This has to go through the commissioner first for review.": "Dotyczą Gildii Eclipse. Są z rezydencji Wilkesów. To musi przejść najpierw przez komisarza do weryfikacji.",
    "Understood. We’ll leave it in his office.": "Rozumiem. Zostawimy to w jego biurze.",
    "Everything okay, Commissioner Smithfield?": "Wszystko w porządku, komisarzu Smithfield?",
    "No, everything is not okay… Keep guard and make sure I’m not disturbed.": "Nie, nie jest w porządku… Stańcie na straży i upewnijcie się, że nikt mi nie przeszkadza.",
    "I’m sorry, detective, but you can’t go through.": "Przepraszam, detektywie, ale nie możesz przejść.",
    "I need to speak with the commissioner.": "Muszę porozmawiać z komisarzem.",
    "The commissioner is not accepting any visitors for now. You’ll have to come back later.": "Komisarz nie przyjmuje teraz gości. Będziesz musiał wrócić później.",
    "Something’s fishy, detective.": "Coś tu śmierdzi, detektywie.",
    "My laptop is back, yet I have no idea how.": "Mój laptop wrócił, a nie mam pojęcia jak.",
    "Maybe don’t look a gift horse in the mouth?": "Może darowanemu koniowi nie zagląda się w zęby?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=127 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=33: raise SystemExit(f'Expected 33, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map127')
