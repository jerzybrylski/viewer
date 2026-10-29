#!/usr/bin/env python3
"""Build Polish drafts for Map 103 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map103-followups-01.jsonl'
TRANSLATIONS = {
    "I see lights… What the hell is this?": "Widzę światła… Co to, do diabła, jest?",
    "I hear someone coming.": "Słyszę, że ktoś idzie.",
    "Was that… Nellie?": "Czy to była… Nellie?",
    "I think it was…": "Chyba tak…",
    "It’s some sort of underground Guild bunker.": "To jakiś podziemny bunkier Gildii.",
    "That was the woman from the mansion. She’s working for the Guild.": "To kobieta z rezydencji. Pracuje dla Gildii.",
    "Shit. We need to get out of here.": "Cholera. Musimy się stąd wydostać.",
    "Wait! She’s undercover… She’s working for us.": "Czekaj! Jest pod przykrywką… Pracuje dla nas.",
    "Just what the hell have you been hiding from me, 1Hero?": "Co ty przede mną ukrywałeś, 1Hero?",
    "That’s my ex-wife. She’s no police officer. I can tell you that.": "To moja była żona. Mogę ci powiedzieć, że nie jest policjantką.",
    "Come on. Let’s check it out.": "Chodź. Sprawdźmy to.",
    "You owe me an explanation!": "Jesteś mi winien wyjaśnienie!",
    "Brian, stay back. There are some real bad men down there.": "Brian, zostań z tyłu. Tam na dole są naprawdę źli ludzie.",
    "Go back to the surface, Father. We won’t be long.": "Wracaj na powierzchnię, Ojcze. Nie zabawimy długo.",
    "Is Andrea telling you something that she’s keeping from me?": "Czy Andrea mówi ci coś, co ukrywa przede mną?",
    "Getting information from anyone is like pulling teeth.": "Wydobycie informacji od kogokolwiek to jak rwanie zębów.",
    "I’m just being observant.": "Po prostu jestem spostrzegawcza.",
    "That’s odd. This locker key looks exactly like the ones found at Fit’s Gym.": "Dziwne. Ten klucz do szafki wygląda dokładnie jak te znalezione w Fit's Gym.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=103 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=18: raise SystemExit(f'Expected 18, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map103')
