#!/usr/bin/env python3
"""Build Polish drafts for Map 145 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map145-followups-01.jsonl'
TRANSLATIONS = {
    "Don’t expect me to talk, officer. I want a lawyer.": "Nie licz, że będę gadać, oficerze. Chcę prawnika.",
    "You have information and you’re going to give it to me.": "Masz informacje i mi je dasz.",
    "What makes you think I care what you have to say?": "Co sprawia, że myślisz, iż obchodzi mnie, co masz do powiedzenia?",
    "Because I saved your life.": "Bo uratowałem ci życie.",
    "You killed my partner.": "Zabiłeś mojego partnera.",
    "The commissioner wanted you dead. You’re only here because of me.": "Pani komisarz chciała, byś zginął. Jesteś tu tylko przeze mnie.",
    "You cops are all the same. I know your tricks.": "Wy gliny jesteście wszyscy tacy sami. Znam wasze sztuczki.",
    "I don’t have a lot of time, so I’m not going to play games with you.": "Nie mam dużo czasu, więc nie będę się z tobą bawić.",
    "You worked for Charles Wilkes, didn’t you?": "Pracowałeś dla Charlesa Wilkesa, prawda?",
    "Your facts are wrong, officer.": "Twoje fakty są błędne, oficerze.",
    "So you’re here to take over. Nellie Cole killed Charles and now you’re going to take his place.": "Więc przyszedłeś przejąć stery. Nellie Cole zabiła Charlesa i teraz ty zajmiesz jego miejsce.",
    "What are you going to do for me? Why should I give you anything?": "Co dla mnie zrobisz? Czemu mam ci cokolwiek dać?",
    "You want to barter? I bet you’d want to know who Nellie Cole really is.": "Chcesz się targować? Założę się, że chciałbyś wiedzieć, kim naprawdę jest Nellie Cole.",
    "A spy?": "Szpiegiem?",
    "Kind of hard to trust anyone in your line of work I suppose.": "Chyba trudno ufać komukolwiek w twojej branży.",
    "How many others are there?": "Ilu innych jest?",
    "Where’s Duncan? What’s the plan?": "Gdzie jest Duncan? Jaki jest plan?",
    "Duncan left the bunker right before you arrived…": "Duncan opuścił bunkier tuż przed twoim przybyciem…",
    "I was picking up a shipment… Or so I was told.": "Miałem odebrać dostawę… Tak mi powiedziano.",
    "Yeah, the shipment was bullshit.": "Taa, ta dostawa to bujda.",
    "Don’t get on our bad side, officer.": "Nie zadzieraj z nami, oficerze.",
    "Give me more information and I’ll do the same.": "Daj mi więcej informacji, a ja zrobię to samo.",
    "Your spy killed a man in cold blood.": "Twój szpieg zabił człowieka z zimną krwią.",
    "You don’t know?": "Nie wiesz?",
    "Wilkes went crazy. He was slipping. We’re here to set things right.": "Wilkes zwariował. Słabł. Jesteśmy tu, by wszystko naprawić.",
    "Wilkes’ lover sure had him by the balls.": "Kochanka Wilkesa trzymała go za jaja.",
    "His wife… his daughter… whoever it was, she’s fucking things up.": "Jego żona… jego córka… kimkolwiek była, pierdoli sprawę.",
    "Her name is Madalyn, and she was looking for an amulet.": "Nazywa się Madalyn i szukała amuletu.",
    "She stole it from Duncan… She hired a thief…": "Ukradła go Duncanowi… Wynajęła złodziejkę…",
    "Morgan… something. I can’t remember her name.": "Morgan… coś tam. Nie pamiętam nazwiska.",
    "Morgan Deluna? A woman?": "Morgan Deluna? Kobieta?",
    "That’s what sparked this. Charles flew too close to the sun…": "To to wszystko wywołało. Charles poleciał za blisko słońca…",
    "You don’t want to piss off Duncan.": "Nie chcesz wkurzać Duncana.",
    "Do you know where Morgan is?": "Wiesz, gdzie jest Morgan?",
    "No clue.": "Nie mam pojęcia.",
    "She’s dead.": "Nie żyje.",
    "Well, I’ll be damned. Duncan always gets his man.": "No nie… Duncan zawsze dorwie swojego człowieka.",
    "After this, he’s all that’s left of the Guild.": "Po tym on jest wszystkim, co zostało z Gildii.",
    "Heh… So you think.": "Heh… Tak myślisz.",
    "A cursed treasure won’t bring us down. We’re slippery.": "Przeklęty skarb nas nie pogrąży. Jesteśmy śliscy.",
    "You’re not an interrogator, are you?": "Nie jesteś przesłuchującym, prawda?",
    "Shut the fuck up.": "Zamknij się.",
    "What’s going on in there?": "Co tam się dzieje?",
    "Uhh… Need another ten.": "Yyy… Potrzeba jeszcze dziesięciu.",
    "Hurry it up.": "Pospiesz się.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=145 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=45: raise SystemExit(f'Expected 45, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map145')
