#!/usr/bin/env python3
"""Build Polish drafts for Map 84 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map84-followups-01.jsonl'
TRANSLATIONS = {
    "I’m thinking tie, but no jacket.": "Myślę o krawacie, ale bez marynarki.",
    "Whatever you think will look good.": "Cokolwiek twoim zdaniem będzie dobrze wyglądać.",
    "Paul here. Speak to me.": "Tu Paul. Mów.",
    "The camera man is complaining that the sound guy touched his lens.": "Operator narzeka, że dźwiękowiec dotknął jego obiektywu.",
    "God fucking…": "Kurwa…",
    "1Hero, you know how to dress yourself, right?": "1Hero, umiesz się sam ubrać, prawda?",
    "Uhh… yes.": "Yyy… tak.",
    "Fantastic! Go pick out something nice and then go through the door that says on-air.": "Fantastycznie! Wybierz coś ładnego i przejdź przez drzwi z napisem na wizji.",
    "I’ll meet you in the studio.": "Spotkamy się w studiu.",
    "What about Miss Foxx? When do I get to meet her?": "A co z panną Foxx? Kiedy ją poznam?",
    "Don’t fanboy out on me, 1Hero. I suggest you follow your boss's lead.": "Nie rób ze mnie fana, 1Hero. Radzę słuchać szefa.",
    "She’s been here many times before.": "Była tu już wiele razy.",
    "Well thanks, Paul.": "Cóż, dzięki, Paul.",
    "Shit. He didn’t tell me which door was the changing room.": "Cholera. Nie powiedział mi, które drzwi to przebieralnia.",
    "Fuck it. I don’t want to be late. I’ll just pick a door.": "Pierdolę to. Nie chcę się spóźnić. Po prostu wybiorę drzwi.",
    "I have a metal hook. Perhaps I can attach this rigging cable and make a grapple.": "Mam metalowy hak. Może zamocuję tę linę i zrobię kotwiczkę.",
    "You came early.": "Przyszedłeś wcześniej.",
    "What’s up, Kimberly?": "Co tam, Kimberly?",
    "You’ve got to hear this.": "Musisz to usłyszeć.",
    "You have audio back from the transmitters?": "Masz dźwięk z nadajników?",
    "It’s… weird to say the least.": "To… delikatnie mówiąc dziwne.",
    "I see the new transmitter is online. Have any troubles?": "Widzę, że nowy nadajnik działa. Jakieś problemy?",
    "It’s fine… There’s definitely some crazy cult stuff happening there.": "W porządku… Zdecydowanie dzieje się tam jakieś szalone gówno kultu.",
    "Whatever’s happening, we’re going to hear it.": "Cokolwiek się dzieje, usłyszymy to.",
    "As soon as you hear anything interesting, call me.": "Jak tylko usłyszysz coś ciekawego, zadzwoń do mnie.",
    "What are you suggesting? Call me to pillow talk?": "Co sugerujesz? Zadzwonić, by pogadać do poduszki?",
    "Here, 1Hero. If you ever feel like… chatting, you could give me a call.": "Masz, 1Hero. Jeśli kiedykolwiek będziesz miał ochotę… pogadać, możesz do mnie zadzwonić.",
    "And what if I want to do more than just chat?": "A co jeśli chcę czegoś więcej niż gadania?",
    "Then you should definitely give me a call, Detective Handsome.": "Wtedy zdecydowanie powinieneś do mnie zadzwonić, detektywie Przystojniaku.",
    "Hot damn. I’m making moves on a celebrity and it’s working.": "Cholera. Podrywam celebrytkę i działa.",
    "Solving a case and getting pussy. Life can’t get better.": "Rozwiązywać sprawę i zaliczać. Życie nie może być lepsze.",
    "What do you got?": "Co masz?",
    "Come listen to this.": "Chodź posłuchać tego.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=84 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=33: raise SystemExit(f'Expected 33, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map84')
