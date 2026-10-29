#!/usr/bin/env python3
"""Build Polish drafts for Map 291 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map291-followups-01.jsonl'
TRANSLATIONS = {
    "Feels good to get off your feet?": "Dobrze zdjąć nogi z podłogi?",
    "This mansion is so much work!": "Ta rezydencja to tyle pracy!",
    "Maybe we should downsize?": "Może powinniśmy zmniejszyć metraż?",
    "We’ll soon have use for all the extra space around here.": "Wkrótce znajdziemy zastosowanie dla całej tej przestrzeni.",
    "You’ll be a great mother.": "Będziesz wspaniałą matką.",
    "I hope so. It’s going to be a lot of work.": "Mam nadzieję. To będzie sporo pracy.",
    "You won’t have to do it alone.": "Nie będziesz musiała robić tego sama.",
    "It’s comforting to know I can count on you, 1Hero.": "To pocieszające, że mogę na ciebie liczyć, 1Hero.",
    "Always.": "Zawsze.",
    "So, about that foot massage?": "Więc, co z tym masażem stóp?",
    "Oh yeah?": "O tak?",
    "Oh yeah.": "O tak.",
    "I knew I chose the right man.": "Wiedziałam, że wybrałam właściwego mężczyznę.",
    "But… my feet are feeling very dry. I’m not sure a massage would feel good.": "Ale… moje stopy są bardzo suche. Nie wiem, czy masaż byłby przyjemny.",
    "Maybe I can get something for them.": "Może mogę coś na to zaradzić.",
    "There must be a good lotion at the store.": "W sklepie na pewno jest dobry balsam.",
    "Well, I don’t usually find those helpful.": "Cóż, zazwyczaj nie znajduję ich pomocnymi.",
    "I do know of a special lotion that my grandma used to make.": "Znam specjalny balsam, który robiła moja babcia.",
    "A Casula recipe?": "Przepis Casula?",
    "Right. It’s worked wonders in the past.": "Zgadza się. W przeszłości działał cuda.",
    "Unfortunately, you have to gather the ingredients to make it.": "Niestety, musisz zebrać składniki, by go zrobić.",
    "Sounds like a lot of work for a lotion…": "Brzmi jak sporo pracy dla balsamu…",
    "1Hero!": "1Hero!",
    "But I don’t mind doing it for my lovely lady.": "Ale nie mam nic przeciwko, by zrobić to dla mojej ukochanej.",
    "That’s what I like to hear from my man.": "To lubię słyszeć od mojego mężczyzny.",
    "So what am I looking for?": "Więc czego mam szukać?",
    "One of them, the Casula flower, is found deep in the Casula Forest.": "Jeden z nich, kwiat Casula, rośnie głęboko w Lesie Casula.",
    "Another grows in the depths of the Casula Caves: Casula moss…": "Kolejny rośnie w głębi Jaskiń Casula: mech Casula…",
    "It grows near water.": "Rośnie w pobliżu wody.",
    "The other one is easier to find: aloe vera.": "Trzeci jest łatwiejszy do znalezienia: aloes.",
    "Did you get everything?": "Zdobyłeś wszystko?",
    "I’ve got it.": "Mam.",
    "Let’s give those feet some attention.": "Zajmijmy się tymi stopami.",
    "Well? Is dinner ready?": "No i? Obiad gotowy?",
    "But for now, I’m feeling famished.": "Ale na razie czuję się wygłodniała.",
    "You are eating for two.": "Jesz za dwoje.",
    "You don’t have to tell me that.": "Nie musisz mi tego mówić.",
    "I’ll go check with Judy, but it should be ready.": "Sprawdzę u Judy, ale powinien być gotowy.",
    "I hope so. Don’t make me wait too long.": "Mam nadzieję. Nie każ mi czekać za długo.",
    "Let me go check on how Judy is doing with preparing dinner.": "Pójdę sprawdzić, jak Judy radzi sobie z przygotowaniem obiadu.",
    "I’ll wait for good news.": "Poczekam na dobre wieści.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=291 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=43: raise SystemExit(f'Expected 43, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map291')
