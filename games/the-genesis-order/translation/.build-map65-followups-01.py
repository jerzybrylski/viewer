#!/usr/bin/env python3
"""Build Polish drafts for Map 65 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map65-followups-01.jsonl'
TRANSLATIONS = {
    "Unless you can tame that baloney pony, you’re going to need to come to me for help.": "Chyba że oswoisz tego kiełbasianego kucyka, będziesz musiał przyjść do mnie po pomoc.",
    "It’s not like I can control it. Chloe kissed me, for Christ’s sake.": "To nie tak, że mogę to kontrolować. Chloe mnie pocałowała, na litość boską.",
    "I said I can't control it.": "Mówiłam, że nie mogę tego kontrolować.",
    "You kissed Chloe?": "Pocałowałaś Chloe?",
    "You dumb fucker!": "Ty durny skurwielu!",
    "What did I do!?": "Co zrobiłam!?",
    "Chloe is in love with you!": "Chloe jest w tobie zakochana!",
    "Chloe won't have sex with me. She’s not ready for a relationship.": "Chloe nie będzie się ze mną pieprzyć. Nie jest gotowa na związek.",
    "She’ll fuck you if she stops getting brainwashed by those nuns at the church.": "Przeleci cię, jeśli przestanie jej prać mózg banda zakonnic z kościoła.",
    "That girl needs a real hobby. Something to get her mind off of all that virgin nun business.": "Tej dziewczynie potrzeba prawdziwego hobby. Czegoś, co odciągnie ją od tego całego dziewiczego, zakonnego biznesu.",
    "Who’s high and mighty now? You just lost your virginity last night.": "Kto tu teraz świętoszkuje? Dopiero wczoraj straciłaś dziewictwo.",
    "That ain’t true!": "To nieprawda!",
    "You can’t lie to me, Hannah. I can see right through you.": "Nie możesz mnie okłamać, Hannah. Przejrzałam cię na wylot.",
    "Damn your detective brain!": "Cholera, twój detektywistyczny mózg!",
    "It’s okay, Hannah. I’m not judging you.": "Spoko, Hannah. Nie oceniam cię.",
    "Well, we ain’t fuckin’ until we fix Chloe.": "Cóż, nie będziemy się pieprzyć, dopóki nie naprawimy Chloe.",
    "But… I mean… A little fun here and there won’t hurt. Will it?": "Ale… to znaczy… Odrobina zabawy tu i tam nie zaszkodzi. Zasz? ",
    "If Chloe finds out about this, she’ll kill me.": "Jeśli Chloe się o tym dowie, zabije mnie.",
    "We’re not in love. We’re just friends with benefits.": "Nie jesteśmy zakochani. Jesteśmy tylko przyjaciółmi z korzyściami.",
    "You think she’ll be okay with that?": "Myślisz, że jej to odpowiada?",
    "No need to tell her anything. It’s our secret.": "Nie trzeba jej nic mówić. To nasza tajemnica.",
    "I’m here to help you, 1Hero. But in the end, you better fuck that girl.": "Jestem tu, by ci pomóc, 1Hero. Ale ostatecznie lepiej żebyś przeleciał tę dziewczynę.",
    "We both want the best for Chloe…": "Obie chcemy dla Chloe jak najlepiej…",
    "I don’t want to break her heart any more than you do.": "Nie chcę łamać jej serca bardziej niż ty.",
    "You two were always meant to be. That’s what I always thought.": "Wy dwoje zawsze byliście sobie przeznaczeni. Tak zawsze myślałam.",
    "Maybe you’re right. But she’s still not ready.": "Może masz rację. Ale wciąż nie jest gotowa.",
    "Are you done in there, Hannah?": "Skończyłaś tam, Hannah?",
    "We’re still changing, Ma!": "Wciąż się przebieramy, mamo!",
    "Who else is in there?": "Kto tam jeszcze jest?",
    "1Hero is changing with me! No need to get your panties in a ruffle!": "1Hero się ze mną przebiera! Nie musisz się tak spinać!",
    "Hannah! She’s going to suspect something.": "Hannah! Ona coś podejrzewa.",
    "No, she ain't. It’s me we’re talking about. I do shit like this all the time.": "Nie, nie podejrzewa. To ja. Robię takie rzeczy cały czas.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=65 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=32: raise SystemExit(f'Expected 32, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map65')
