#!/usr/bin/env python3
"""Build Polish drafts for Map 95 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map95-followups-01.jsonl'
TRANSLATIONS = {
    "Come on. Let’s shower together.": "Chodź. Weźmy prysznic razem.",
    "This better not be some sort of trick.": "Lepiej niech to nie będzie jakiś podstęp.",
    "Don’t you trust me?": "Nie ufasz mi?",
    "Not even a little bit.": "Ani trochę.",
    "Hop in, big man.": "Wskakuj, duży chłopie.",
    "Damn, Nellie. I didn’t expect a blowjob like that.": "Cholera, Nellie. Nie spodziewałem się takiego obciągania.",
    "Aren’t I a lucky woman? Finding a man like you.": "Czyż nie jestem szczęściarą? Znaleźć takiego mężczyznę jak ty.",
    "Are you playing me like a fiddle now?": "Oggrywasz mnie teraz jak skrzypce?",
    "Would I tell you if I were?": "Powiedziałabym ci, gdybym to robiła?",
    "If you give me head like that, maybe it’s worth it.": "Jeśli robisz laskę jak tamta, może warto.",
    "I know you don’t believe that, Captain America.": "Wiem, że w to nie wierzysz, Kapitanie Ameryka.",
    "1Hero? Are you in there?": "1Hero? Jesteś tam?",
    "Oh, uh… One moment, Judy.": "Och, yyy… Chwilę, Judy.",
    "You think she’ll suspect what we did in her bathroom?": "Myślisz, że podejrzewa, co zrobiliśmy w jej łazience?",
    "Shit. Come on, let’s get out of here.": "Cholera. Chodź, wynośmy się stąd.",
    "I better get back to Erica. Have to make sure everyone is safe.": "Lepiej wrócę do Eriki. Muszę upewnić się, że wszyscy są bezpieczni.",
    "Oh, God. I’m embarrassed.": "O Boże. Wstydzę się.",
    "Come on. It was fun.": "Daj spokój. Było fajnie.",
    "It was enjoyable… But our sinful activity is now known by the detective.": "Było przyjemnie… Ale nasz grzeszny występek jest teraz znany detektywowi.",
    "Haha. Don’t worry. It’s not a crime.": "Haha. Nie martw się. To nie przestępstwo.",
    "But… I think I took things too far.": "Ale… Chyba posunęłam się za daleko.",
    "I did it, Sister Judy… It’s not your fault.": "Zrobiłam to, siostro Judy… To nie twoja wina.",
    "Yes… I know the intentions… But…": "Tak… Znam intencje… Ale…",
    "Come on. Let’s not think about it too much.": "Daj spokój. Nie myślmy o tym za dużo.",
    "You’re right. You must leave to help Father.": "Masz rację. Musisz iść pomóc Ojcu.",
    "Let’s get you back to the library.": "Odprowadźmy cię do biblioteki.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=95 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=26: raise SystemExit(f'Expected 26, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map95')
