#!/usr/bin/env python3
"""Build Polish drafts for Map 86 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map86-followups-01.jsonl'
TRANSLATIONS = {
    "Maybe we’re looking in the wrong area. Certainly if the cops can’t find anything, there must not be anything back here.": "Może szukamy w złym miejscu. Jeśli gliny nie mogą nic znaleźć, to na pewno nic tu nie ma.",
    "Don’t be so sure. These guys aren’t detectives.": "Nie bądź taki pewien. Ci goście nie są detektywami.",
    "Okay, smart guy. Maybe you can find something.": "Dobra, mądralo. Może znajdziesz coś.",
    "If you’re so smart, then see if you can find what that key goes to.": "Skoro jesteś taki mądry, to zobacz, czy odkryjesz, do czego jest ten klucz.",
    "Canmore?": "Canmore?",
    "Bobby sent me here. What did you see?": "Przysłał mnie Bobby. Co widziałeś?",
    "I heard a sound and came to investigate. I saw two people run into the woods as soon as I opened the door.": "Usłyszałem dźwięk i przyszedłem sprawdzić. Widziałem, jak dwie osoby wbiegły do lasu, gdy tylko otworzyłem drzwi.",
    "I couldn’t tell. But I’m not going back there to find out. At least not in the dark.": "Nie mogłem rozpoznać. Ale nie wrócę tam, by się przekonać. Przynajmniej nie po ciemku.",
    "I saw him! Let’s move.": "Widziałem go! Ruszajmy.",
    "How the hell are we supposed to make progress when all directions are blocked?": "Jak, do cholery, mamy robić postępy, gdy wszystkie kierunki są zablokowane?",
    "Where did that Guild guy run off to? How did he get past all this brush?": "Gdzie zwiał ten gość z Gildii? Jak przeszedł przez te zarośla?",
    "This is hopeless. Where are we supposed to go?": "To beznadziejne. Dokąd mamy iść?",
    "There's something barricading the door.": "Coś barykaduje drzwi.",
    "Detective.": "Detektywie.",
    "Diana… I’m risking a lot to help you.": "Diana… Bardzo ryzykuję, by ci pomóc.",
    "I know. I won’t betray your trust.": "Wiem. Nie zawiodę twojego zaufania.",
    "Not the easiest thing to believe from a Guild member.": "Nie najłatwiej uwierzyć członkowi Gildii.",
    "The Guild will die. Believe me.": "Gildia umrze. Uwierz mi.",
    "The Guild might die with or without you.": "Gildia może umrzeć z tobą lub bez ciebie.",
    "Take this key…": "Weź ten klucz…",
    "It opens a locked door in the abandoned chapel.": "Otwiera zamknięte drzwi w opuszczonej kaplicy.",
    "What will I find there?": "Co tam znajdę?",
    "The secret back entrance to the bunker.": "Tajne tylne wejście do bunkra.",
    "I’m going to the warehouse to draw the guards to the entrance.": "Idę do magazynu, by zwabić strażników do wejścia.",
    "How will you do that?": "Jak to zrobisz?",
    "I know how to break in… I just have to get caught.": "Wiem, jak się włamać… Po prostu muszę dać się złapać.",
    "And then I sneak in the back and help save your friend, Henry?": "A potem ja wślizgnę się tyłem i pomogę uratować twojego przyjaciela, Henry'ego?",
    "What are you going to do after you get caught?": "Co zrobisz po tym, jak cię złapią?",
    "Run like hell.": "Będę spieprzać, ile sił w nogach.",
    "There’s a security system in the bunker that will set off if they don’t come to the entrance.": "W bunkrze jest system bezpieczeństwa, który się uruchomi, jeśli nie przyjdą do wejścia.",
    "They have to turn it off in order to surface… If I fail, the trap will trigger.": "Muszą go wyłączyć, by wyjść na powierzchnię… Jeśli zawiodę, pułapka się uruchomi.",
    "A trap?": "Pułapka?",
    "Be careful, 1Hero. If you can’t make it to Henry, you need to escape.": "Bądź ostrożny, 1Hero. Jeśli nie dasz rady dotrzeć do Henry'ego, musisz uciekać.",
    "I hope I’m helping the right people.": "Mam nadzieję, że pomagam właściwym ludziom.",
    "Hey! What are you doing back here?": "Hej! Co tu robisz?",
    "Shit! Split up!": "Cholera! Rozdzielmy się!",
    "See you at the warehouse!": "Widzimy się przy magazynie!",
    "Diana, Henry… You made it.": "Diana, Henry… Udało się.",
    "You’re lucky Henry is convinced to help you. I wanted to put a bullet in Duncan’s brain and get the hell out of here.": "Masz szczęście, że Henry dał się przekonać, by ci pomóc. Chciałem wpakować kulkę Duncanowi w mózg i zwiewać stąd.",
    "Then why didn’t you?": "To czemu tego nie zrobiłeś?",
    "The door’s been barricaded.": "Drzwi zostały zabarykadowane.",
    "Is there another way in?": "Jest inne wejście?",
    "What’s with the costume?": "Co z tym kostiumem?",
    "Erica looked at the Toma.": "Erica spojrzała na Tomę.",
    "My name is Arianna. I am an angel from the Empyrean.": "Nazywam się Arianna. Jestem aniołem z Empyreum.",
    "There’s no time to explain. Follow me.": "Nie ma czasu na wyjaśnienia. Chodź za mną.",
    "Demons are trying to steal Erica!": "Demony próbują porwać Ericę!",
    "We have to hide!": "Musimy się schować!",
    "This way!": "Tędy!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=86 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=49: raise SystemExit(f'Expected 49, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map86')
