#!/usr/bin/env python3
"""Build Polish drafts for Map 166 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map166-followups-01.jsonl'
TRANSLATIONS = {
    "Hmmm…. A security room. Maybe Kimberly is on video.": "Hmm… Pomieszczenie ochrony. Może Kimberly jest na wideo.",
    "Come back when you have news on Kimberly's whereabouts.": "Wróć, gdy będziesz miał wieści o miejscu pobytu Kimberly.",
    "So far, nothing’s shown up on the cameras.": "Jak dotąd nic nie pojawiło się na kamerach.",
    "Nothing on the security cameras. Come back when you know where Kimberly is.": "Nic na kamerach ochrony. Wróć, gdy będziesz wiedział, gdzie jest Kimberly.",
    "Sir, I need you to leave the room.": "Proszę pana, muszę pana prosić o opuszczenie pokoju.",
    "Don’t worry, I know the biz! Buddy taught me! Maybe you’ve met him at the security conventions.": "Nie martw się, znam branżę! Buddy mnie nauczył! Może spotkałeś go na konwencjach ochrony.",
    "Who is Buddy?": "Kim jest Buddy?",
    "Wait, I don’t care.": "Czekaj, nie obchodzi mnie to.",
    "Oh, what’s this button do?": "Och, co robi ten przycisk?",
    "What… Don’t touch that!": "Co… Nie dotykaj tego!",
    "Simon, how about we check out the front of the building? There might be something there.": "Simon, może sprawdźmy przód budynku? Może coś tam jest.",
    "The front? No way, that’s too obvious.": "Przód? Nie ma mowy, to zbyt oczywiste.",
    "Criminals never come in the front way, everyone knows that!": "Przestępcy nigdy nie wchodzą frontem, każdy to wie!",
    "Criminals?": "Przestępcy?",
    "What we really need to do is check each room thoroughly.": "Tak naprawdę musimy dokładnie sprawdzić każdy pokój.",
    "Is there something I should know about?": "Czy jest coś, co powinienem wiedzieć?",
    "Do you need a briefing on criminal behavior, mister?": "Potrzebujesz odprawy o zachowaniu przestępczym, proszę pana?",
    "Don’t encourage him.": "Nie zachęcaj go.",
    "I don’t even understand what’s going on.": "Nawet nie rozumiem, co się dzieje.",
    "Wait, what’s that room?": "Czekaj, co to za pokój?",
    "You mean the storage room?": "Masz na myśli składzik?",
    "Yeah, something doesn’t add up.": "Tak, coś się nie zgadza.",
    "I’m going to check it out.": "Sprawdzę to.",
    "Simon, wait…": "Simon, czekaj…",
    "Detective, what’s this all about? And who’s Buddy?": "Detektywie, o co tu chodzi? I kim jest Buddy?",
    "Detective, what’s with that kid? And who’s Buddy?": "Detektywie, co z tym dzieciakiem? I kim jest Buddy?",
    "Just make sure he doesn’t cause any trouble.": "Tylko dopilnuj, by nie sprawiał kłopotów.",
    "Easier said than done.": "Łatwiej powiedzieć niż zrobić.",
    "That kid isn’t coming back, is he?": "Ten dzieciak nie wróci, co?",
    "Everything good?": "Wszystko w porządku?",
    "See you around.": "Do zobaczenia.",
    "See you, detective.": "Do zobaczenia, detektywie.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=166 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=32: raise SystemExit(f'Expected 32, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map166')
