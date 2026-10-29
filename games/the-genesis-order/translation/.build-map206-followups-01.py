#!/usr/bin/env python3
"""Build Polish drafts for Map 206 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map206-followups-01.jsonl'
TRANSLATIONS = {
    "Looking forward to the party?": "Nie możesz się doczekać imprezy?",
    "You know it.": "Jasne, że się cieszę.",
    "How do you like my apartment?": "Jak ci się podoba moje mieszkanie?",
    "It’s nice… A lot nicer than Ella’s right now…": "Fajne… Dużo fajniejsze niż Elli teraz…",
    "Poor girl’s apartment was ransacked.": "Biedaczce mieszkanie splądrowano.",
    "How’s life with Hannah?": "Jak życie z Hannah?",
    "Crazy. Like you wouldn’t believe.": "Szalone. Nie uwierzysz.",
    "The worst is when she decides to bring her pets to visit.": "Najgorsze, gdy postanawia przyprowadzić zwierzaki w odwiedziny.",
    "I’m really tired of watching my step around that gator.": "Mam dość uważania na kroki wokół tego aligatora.",
    "Oof, I’m sorry to hear that.": "Och, współczuję.",
    "Is it all bad?": "Czy jest całkiem źle?",
    "Well… the times when we get intimate can be a lot of fun.": "Cóż… chwile, gdy jesteśmy intymni, potrafią być bardzo zabawne.",
    "She has a lot of wild energy.": "Ma w sobie mnóstwo dzikiej energii.",
    "She does.": "Ma.",
    "Also doesn’t hurt that she’s amazing at blowing pussy.": "Nie zaszkodzi też, że świetnie pieści cipkę.",
    "Hahaha!": "Hahaha!",
    "I’ll see you at dinner this evening.": "Do zobaczenia na obiedzie wieczorem.",
    "See you then, Chloe.": "Do zobaczenia, Chloe.",
    "Enjoying the free life?": "Cieszysz się wolnym życiem?",
    "Not what you were hoping?": "Nie tego się spodziewałaś?",
    "Not that I mind.": "Nie że mi przeszkadza.",
    "I visit Mom everyday, almost.": "Odwiedzam mamę codziennie, prawie.",
    "Someone has to take care of Gatorzilla, after all.": "Ktoś musi zająć się Gatorzillą, w końcu.",
    "I guess the country girl can be taken out of the country, but the country can’t be taken out of the country girl.": "Chyba można wyciągnąć dziewczynę ze wsi, ale wsi z dziewczyny nie wyciągnie.",
    "What are you? Some kind of poet now?": "Co ty? Jakiś poeta teraz?",
    "Uh, I don’t think that was really poetry.": "Yh, nie sądzę, by to była poezja.",
    "Sounds like a song lyric to me.": "Brzmi jak tekst piosenki dla mnie.",
    "If it could be sung in a song, then it’s poetry.": "Jeśli można to zaśpiewać, to poezja.",
    "What?... What are we even talking about?": "Co?... O czym my w ogóle rozmawiamy?",
    "I’m hungry.": "Jestem głodna.",
    "Oh, yeah. Are you coming to dinner?": "O, tak. Idziesz na obiad?",
    "Of course! And I made a little something for dessert…": "Oczywiście! I zrobiłam coś na deser…",
    "Uhh… What is this?": "Yyy… Co to jest?",
    "It’s a bundle of cherries buried in six cups of sugar.": "To pęczek wiśni zakopany w sześciu filiżankach cukru.",
    "And we’ll eat this?": "I to zjemy?",
    "Of course we’ll eat it, knucklehead! What do you think we’d do with it?": "Oczywiście, że zjemy, tępaku! Co innego byśmy z tym zrobili?",
    "We’re going to get sick.": "Rozchorujemy się.",
    "I said we’re going to love it.": "Mówiłam, że pokochamy to.",
    "It’s sweet!": "Jest słodkie!",
    "I’m sure it is.": "Jestem pewna, że jest.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=206 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=42: raise SystemExit(f'Expected 42, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map206')
