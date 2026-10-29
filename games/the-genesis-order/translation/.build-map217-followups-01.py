#!/usr/bin/env python3
"""Build Polish drafts for Map 217 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map217-followups-01.jsonl'
TRANSLATIONS = {
    "Damn! That’s a lot of treasure.": "Cholera! Ale skarbów.",
    "Is this a tomb?": "Czy to grobowiec?",
    "Looks like it.": "Wygląda na to.",
    "I guess Jon was right… What’s he going to do now?": "Chyba Jon miał rację… Co teraz zrobi?",
    "Sell the artifacts, I suppose.": "Sprzeda artefakty, przypuszczam.",
    "Who buys this stuff?": "Kto kupuje takie rzeczy?",
    "Museums… Archaeologists… That’s my guess.": "Muzea… Archeolodzy… Tak zgaduję.",
    "It feels… wrong.": "Czuję, że to… niewłaściwe.",
    "It would be, but Jon has a permit.": "Byłoby, ale Jon ma pozwolenie.",
    "Yeah… I guess that makes sense.": "Tak… Chyba ma to sens.",
    "What’s this?...": "Co to jest?...",
    "We’re trapped.": "Jesteśmy uwięzieni.",
    "Don’t panic… I’m sure there’s a way to get out.": "Bez paniki… Na pewno jest sposób, by się wydostać.",
    "I’m not panicking… Are you panicking?": "Nie panikuję… Ty panikujesz?",
    "Hey… We made it out of Hell. I’m sure we can make it out of this.": "Hej… Wydostaliśmy się z piekła. Jestem pewien, że wydostaniemy się i stąd.",
    "It was my ancestors that made this place, maybe I can help get us out.": "To moi przodkowie zbudowali to miejsce, może pomogę nam się wydostać.",
    "Heh… Any ideas?": "Heh… Jakieś pomysły?",
    "Well… Stepping on this plate put us in this mess, maybe stepping somewhere else can get us out.": "Cóż… Stanięcie na tej płycie wpakowało nas w kłopoty, może stanięcie gdzie indziej nas wydostanie.",
    "If it were me building this place, I’d sure as hell make a way to escape.": "Gdybym ja budował to miejsce, na pewno zrobiłbym drogę ucieczki.",
    "Maybe the map has a hint.": "Może mapa ma wskazówkę.",
    "It’s not a tomb… It was hiding a treasure!": "To nie grobowiec… Ukrywał skarb!",
    "Damn! That looks expensive!": "Cholera! To wygląda drogo!",
    "Maybe we’ll be rich.": "Może będziemy bogaci.",
    "I’ll be rich. This was my job.": "Ja będę bogaty. To była moja robota.",
    "You subcontracted me. I get to keep half.": "Podzleciłeś mi to. Należy mi się połowa.",
    "We’ll get nothing if we don’t make it out of here.": "Nic nie dostaniemy, jeśli się stąd nie wydostaniemy.",
    "We’ve looked everywhere. Any more ideas?": "Przeszukaliśmy wszędzie. Jakieś inne pomysły?",
    "You know… My grandma told me stories about the Casula and their temple traps.": "Wiesz… Babcia opowiadała mi historie o Casula i ich pułapkach w świątyni.",
    "Anything useful?": "Coś przydatnego?",
    "I don’t know if they were true, but the tribal leaders made sex rituals open secret pathways.": "Nie wiem, czy były prawdziwe, ale wodzowie plemienni sprawiali, że seksualne rytuały otwierały tajne przejścia.",
    "That sounds like a load of bullshit.": "Brzmi jak totalna bzdura.",
    "My grandma loved those stories… So many kinky stories.": "Babcia uwielbiała te historie… Tyle sprośnych opowieści.",
    "Apparently they made lots of stone dildos… some with magic powers.": "Podobno zrobili mnóstwo kamiennych dildo… niektóre z magicznymi mocami.",
    "Did you see anything around here that looked like it would fit in your pussy?": "Widziałaś tu coś, co pasowałoby do twojej cipki?",
    "Eww… I don’t think so.": "Fuj… Chyba nie.",
    "What other stories?": "Jakie inne historie?",
    "Magical triple penetrations… Magical giant cocks…": "Magiczne potrójne penetracje… Magiczne wielkie kutasy…",
    "I know that one.": "Znam tę.",
    "Come on, 1Hero… Let’s try some stuff.": "Daj spokój, 1Hero… Spróbujmy paru rzeczy.",
    "Do you have a better idea?": "Masz lepszy pomysł?",
    "I guess it couldn’t hurt.": "Chyba nie zaszkodzi.",
    "That’s not a very romantic thing to say if you’re wanting to get me wet.": "To nie jest zbyt romantyczne, jeśli chcesz mnie podniecić.",
    "Oh yeah? Maybe this is a better way to start things off…": "O tak? Może to lepszy sposób na rozpoczęcie…",
    "Holy shit! It worked!": "Jasna cholera! Zadziałało!",
    "No way! Did we really open up a new path by fucking?": "Niemożliwe! Naprawdę otworzyliśmy nową ścieżkę, pieprząc się?",
    "Come on! Let’s go before we get trapped again.": "Dalej! Chodźmy, zanim znowu zostaniemy uwięzieni.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=217 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=46: raise SystemExit(f'Expected 46, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map217')
