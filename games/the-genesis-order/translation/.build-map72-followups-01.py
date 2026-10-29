#!/usr/bin/env python3
"""Build Polish drafts for Map 72 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map72-followups-01.jsonl'
TRANSLATIONS = {
    "Damn, 1Hero! How did you do that?": "Cholera, 1Hero! Jak ty to zrobiłeś?",
    "Looks like someone’s been working out.": "Wygląda na to, że ktoś ostatnio ćwiczył.",
    "Do we dare venture further?": "Odważymy się iść dalej?",
    "If you want to go on a hike, maybe I should come with you.": "Jeśli chcesz iść na wędrówkę, może powinnam iść z tobą.",
    "Yes, daddy! Show us little girls the way!": "Tak, tatusiu! Pokaż nam, małym dziewczynkom, drogę!",
    "Hey! I’m just trying to be nice.": "Hej! Po prostu staram się być miły.",
    "Of course you can come with us!": "Oczywiście, że możesz iść z nami!",
    "Sister Judy! Are you back here?": "Siostro Judy! Jesteś tam?",
    "Sister Judy! It’s me! Chloe!": "Siostro Judy! To ja! Chloe!",
    "If she went into the woods, she may have left clues.": "Jeśli poszła do lasu, mogła zostawić ślady.",
    "Let me look around and see what I can find.": "Rozejrzę się i zobaczę, co znajdę.",
    "I do hope she’s safe.": "Mam nadzieję, że jest bezpieczna.",
    "Thanks for the help, 1Hero.": "Dzięki za pomoc, 1Hero.",
    "It isn’t like Sister Judy to just leave without telling me.": "To niepodobne do siostry Judy, by tak po prostu odejść bez słowa.",
    "I hope she’s okay.": "Mam nadzieję, że nic jej nie jest.",
    "Sister Judy and I sometimes go hiking in the woods. But we never go very far.": "Siostra Judy i ja czasem chodzimy na wędrówki po lesie. Ale nigdy nie oddalamy się za daleko.",
    "What’s wrong, little fella’? Are you hungry?": "Co jest, maluchu? Głodny jesteś?",
    "I have some black pepper.": "Mam trochę czarnego pieprzu.",
    "I have some soy beans.": "Mam trochę soi.",
    "I have some oats.": "Mam trochę owsa.",
    "I have some barley.": "Mam trochę jęczmienia.",
    "I have some corn.": "Mam trochę kukurydzy.",
    "I have some goat dessert.": "Mam trochę koziego deseru.",
    "Sorry, I don’t have any food.": "Przepraszam, nie mam żadnego jedzenia.",
    "I guess it’s not too happy.": "Chyba nie jest zbyt szczęśliwy.",
    "Where should we be looking?": "Gdzie powinniśmy szukać?",
    "Just keep your eyes peeled.": "Po prostu miej oczy otwarte.",
    "Now what? What are we looking for?": "I co teraz? Czego szukamy?",
    "I don’t know. Look for footprints.": "Nie wiem. Szukaj śladów.",
    "You’re being very unhelpful.": "Jesteś bardzo niepomocny.",
    "Is this really as far as we can go?": "Czy to naprawdę tak daleko, jak możemy iść?",
    "It sure is peaceful back here.": "Tu z tyłu jest naprawdę spokojnie.",
    "I’m trying to be safe and not go too far, but Hannah is getting antsy.": "Staram się być bezpieczny i nie iść za daleko, ale Hannah robi się niespokojna.",
    "I hope Hannah doesn’t break another window.": "Mam nadzieję, że Hannah znowu nie wybije szyby.",
    "What’s wrong, 1Hero? Are you okay?": "Co jest, 1Hero? Wszystko w porządku?",
    "It’s nothing… Maybe Judy can tell you about it later.": "To nic… Może Judy opowie ci o tym później.",
    "Did something happen?": "Coś się stało?",
    "It’s… nothing.": "To… nic.",
    "Go get Heather! She’s on my team!": "Zawołaj Heather! Ona jest w mojej drużynie!",
    "Thank God Heather is here. She can help me take down the gator if he comes back.": "Dzięki Bogu, że Heather tu jest. Pomoże mi powalić aligatora, jeśli wróci.",
    "Don’t bother the alligator, Hannah.": "Nie zaczepiaj aligatora, Hannah.",
    "You know some nice people, 1Hero. I feel lucky to have met you.": "Znasz fajnych ludzi, 1Hero. Cieszę się, że cię poznałam.",
    "Everything seems safe here so far.": "Jak dotąd wszystko wydaje się tu bezpieczne.",
    "Demons, Guild and alligators. I’m not so sure about that.": "Demony, Gildia i aligatory. Nie jestem tego taka pewna.",
    "Hey, I’m still standing.": "Hej, wciąż stoję.",
    "I hope Judy is doing okay. That must have been very frightening for her.": "Mam nadzieję, że Judy ma się dobrze. To musiało być dla niej bardzo przerażające.",
    "I don’t think any of us remained frightened for long.": "Chyba żadne z nas nie pozostało długo przerażone.",
    "Do you think Carol would be upset to know you fooled around with her daughter?": "Myślisz, że Carol byłaby zła, gdyby dowiedziała się, że bawiłeś się z jej córką?",
    "You know… I’ll probably tell her all the juicy details myself.": "Wiesz… Pewnie sama opowiem jej wszystkie soczyste szczegóły.",
    "Damn! I’d like to be a fly on the wall during that conversation.": "Cholera! Chciałbym być muchą na ścianie przy tej rozmowie.",
    "Do you think I could eat Heather’s pussy?": "Myślisz, że mógłbym polizać cipkę Heather?",
    "I just can’t stop thinking about her pussy!": "Nie mogę przestać myśleć o jej cipce!",
    "What have we unlocked in you, Hannah?": "Co w tobie odblokowaliśmy, Hannah?",
    "1Hero! Come play with us!": "1Hero! Chodź się z nami pobawić!",
    "Mom went inside to talk to Carol.": "Mama weszła do środka porozmawiać z Carol.",
    "Yeah. She won’t play soccer with us.": "Tak. Nie chce z nami grać w piłkę.",
    "You ladies up for an adventure?": "Panie, macie ochotę na przygodę?",
    "What kind of adventure?": "Jaką przygodę?",
    "There’s some sort of ancient-looking puzzle in the forest.": "W lesie jest jakaś starożytna łamigłówka.",
    "A puzzle?": "Łamigłówka?",
    "Seems like it. I can’t open it myself.": "Chyba tak. Sam nie mogę jej otworzyć.",
    "You need the help of a couple girls?": "Potrzebujesz pomocy paru dziewczyn?",
    "Of course he does! Let’s go!": "Oczywiście, że tak! Chodźmy!",
    "I can’t do everything myself.": "Nie mogę zrobić wszystkiego sam.",
    "1Hero! We have a problem!": "1Hero! Mamy problem!",
    "Already? Why are you naked? What happened?": "Już? Czemu jesteś naga? Co się stało?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=72 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=66: raise SystemExit(f'Expected 66, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map72')
