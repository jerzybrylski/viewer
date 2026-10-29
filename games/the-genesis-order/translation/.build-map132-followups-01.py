#!/usr/bin/env python3
"""Build Polish drafts for Map 132 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map132-followups-01.jsonl'
TRANSLATIONS = {
    "Shit! Even the bedroom has been ransacked.": "Cholera! Nawet sypialnia splądrowana.",
    "Someone’s here!...": "Ktoś tu jest!...",
    "I better hide.": "Lepiej się schowam.",
    "Ella!": "Ella!",
    "1Hero!? What the hell are you doing here?": "1Hero!? Co ty, do cholery, tu robisz?",
    "Erica told me she heard something…": "Erica mówiła, że coś słyszała…",
    "Why the hell is your place a mess?": "Czemu, do cholery, masz taki bałagan?",
    "It’s nothing.": "To nic.",
    "It’s not nothing! Someone broke into your house.": "To nie nic! Ktoś włamał się do twojego domu.",
    "Oh, 1Hero… The video… It got leaked.": "Och, 1Hero… Film… Wyciekł.",
    "I know… I got fired.": "Wiem… Wyrzucili mnie.",
    "I’m so sorry, 1Hero… Something bad has happened.": "Tak mi przykro, 1Hero… Stało się coś złego.",
    "What’s going on, Ella? Tell me.": "Co się dzieje, Ella? Powiedz mi.",
    "Someone is looking for something that I stole.": "Ktoś szuka czegoś, co ukradłam.",
    "What did you steal?": "Co ukradłaś?",
    "I stole something from the Eclipse Guild and they want it back…": "Ukradłam coś z Gildii Eclipse i chcą to z powrotem…",
    "But I don’t have it.": "Ale nie mam tego.",
    "Oh, my God! You stole from the Guild?": "O mój Boże! Okradłaś Gildię?",
    "I know it’s wrong to steal. I didn’t mean to.": "Wiem, że kradzież jest zła. Nie chciałam.",
    "You didn’t mean to steal?": "Nie chciałaś kraść?",
    "It was just so pretty. I wanted it.": "Było takie ładne. Chciałam je mieć.",
    "What was it?": "Co to było?",
    "Some sort of amulet.": "Jakiś amulet.",
    "But I gave it away, and I don’t have it anymore.": "Ale oddałam go i już go nie mam.",
    "Holy shit… You stole one of the amulets that Lillian is looking for.": "Jasna cholera… Ukradłaś jeden z amuletów, których szuka Lillian.",
    "1Hero… My life’s in danger. I need to get out of here.": "1Hero… Moje życie jest w niebezpieczeństwie. Muszę się stąd wydostać.",
    "A bad man is looking for that Amulet. Who did you give it to?": "Zły człowiek szuka tego amuletu. Komu go dałaś?",
    "I gave it back to an old man who caught me with it.": "Oddałam go staremu mężczyźnie, który mnie na tym przyłapał.",
    "I don’t know what they could want with me now.": "Nie wiem, czego mogą ode mnie chcieć teraz.",
    "Don’t worry. I’m your bodyguard, remember? I’ll protect you.": "Nie martw się. Jestem twoim ochroniarzem, pamiętasz? Będę cię chronić.",
    "What about the church? Could I go there?": "A co z kościołem? Mogłabym tam iść?",
    "No! Don’t go there.": "Nie! Nie idź tam.",
    "… Heather. She can help you.": "…Heather. Ona może ci pomóc.",
    "Heather?": "Heather?",
    "You can stay with Chloe. Sister Judy is already there too. We’re protecting her as well.": "Możesz zostać u Chloe. Siostra Judy już tam jest. Chronimy ją również.",
    "From the Guild?": "Przed Gildią?",
    "Ella… The Guild bunker is under the church.": "Ella… Bunkier Gildii jest pod kościołem.",
    "Let’s get you out of here.": "Wynośmy cię stąd.",
    "I can’t leave yet. I need something.": "Nie mogę jeszcze odejść. Potrzebuję czegoś.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=132 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=39: raise SystemExit(f'Expected 39, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map132')
