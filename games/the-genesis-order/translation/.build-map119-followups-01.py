#!/usr/bin/env python3
"""Build Polish drafts for Map 119 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map119-followups-01.jsonl'
TRANSLATIONS = {
    "Wow! You sure do have a lot of stuff.": "Łał! Masz naprawdę sporo rzeczy.",
    "She makes a bit of a mess.": "Robi trochę bałaganu.",
    "This ain’t no mess. These are my treasures.": "To nie bałagan. To moje skarby.",
    "Everyone behaving?": "Wszyscy grzeczni?",
    "Are we all going to sleep on this bed?": "Będziemy wszyscy spać na tym łóżku?",
    "Haha. I’ll be sleeping on the couch.": "Haha. Ja będę spać na kanapie.",
    "It would be mighty cozy to have 1Hero with us.": "Byłoby strasznie przytulnie mieć 1Hero z nami.",
    "No more sex talk, Hannah.": "Koniec z gadką o seksie, Hannah.",
    "I didn’t say anything!": "Nic nie mówiłam!",
    "It’s getting late, when are you all going to sleep?": "Robi się późno, kiedy pójdziecie spać?",
    "We can’t sleep yet! We have to play games!": "Nie możemy jeszcze spać! Musimy grać w gry!",
    "Let’s get on the internet!": "Wbijmy do internetu!",
    "Hannah, that computer is too old.": "Hannah, ten komputer jest za stary.",
    "I don’t have a computer. It looks pretty.": "Nie mam komputera. Wygląda ładnie.",
    "Grandpappy gave it to me. It glows green!": "Dał mi go dziadek. Świeci na zielono!",
    "Can I play it?": "Mogę pograć?",
    "Sure! Knock yourself out.": "Jasne! Szalej.",
    "I guess I’ll get ready for bed. I’ll just be downstairs.": "Chyba pójdę się położyć. Będę na dole.",
    "Are you coming with us tomorrow morning?": "Idziesz z nami jutro rano?",
    "If Ma makes me go, then you have to go too!": "Jeśli mama mnie zmusi, to ty też musisz iść!",
    "Look, 1Hero. This computer can spell anything you type. Watch!": "Patrz, 1Hero. Ten komputer potrafi przeliterować wszystko, co wpiszesz. Patrz!",
    "I’m glad it makes you happy.": "Cieszę się, że cię to cieszy.",
    "It’s going to be a tight squeeze… The three of us on this one little bed.": "Będzie ciasno… My trzy na jednym małym łóżku.",
    "Your bigger concern is probably Hannah’s snoring.": "Bardziej martwiłoby cię chrapanie Hannah.",
    "It’s a perfect night for ghost stories.": "Idealna noc na opowieści o duchach.",
    "Don’t keep Judy up all night.": "Nie trzymaj Judy całą noc.",
    "1Hero!?": "1Hero!?",
    "We’re changing! Give us a minute!": "Przebieramy się! Daj nam chwilę!",
    "I thought you had to go to bed?": "Myślałem, że miałaś iść do łóżka?",
    "God damn it, 1Hero! Chloe won't go into the woods with me.": "Cholera, 1Hero! Chloe nie chce iść ze mną do lasu.",
    "What’s in the woods?": "Co jest w lesie?",
    "I just want to go on an adventure. I’m bored!": "Po prostu chcę przeżyć przygodę. Nudzi mi się!",
    "You can invite Erica.": "Możesz zaprosić Ericę.",
    "She’s busy.": "Jest zajęta.",
    "What about Judy?": "A co z Judy?",
    "Are you kidding me?...": "Żartujesz sobie?...",
    "I don’t know. She doesn’t hang around the apartments anymore.": "Nie wiem. Już nie kręci się wokół apartamentów.",
    "If you really must go into the woods with a friend, maybe you should talk to Tasha.": "Jeśli koniecznie musisz iść do lasu z przyjacielem, może powinnaś pogadać z Tashą.",
    "The porn shop lady?": "Tą panią z sex shopu?",
    "You know her. She can become your new friend.": "Znasz ją. Może zostać twoją nową przyjaciółką.",
    "Is she tough enough to handle me?": "Czy jest wystarczająco twarda, by sobie ze mną poradzić?",
    "Haha… I think so, Hannah.": "Haha… Myślę, że tak, Hannah.",
    "Hot damn! Let’s go to the porn shop!": "Gorąco! Chodźmy do sex shopu!",
    "You want me to come with you?": "Chcesz, bym poszła z tobą?",
    "If you can keep up!": "Jeśli nadążysz!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=119 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=45: raise SystemExit(f'Expected 45, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map119')
