#!/usr/bin/env python3
"""Build Polish drafts for Map 48 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map48-followups-01.jsonl'
TRANSLATIONS = {
    "Hmm, what was Carol talking about? I don’t see anything.": "Hmm, o czym mówiła Carol? Nic nie widzę.",
    "Carol! I don’t see anything!": "Carol! Nic nie widzę!",
    "Hold on! I’ll be there in a just a minute to show you!": "Zaraz! Będę za minutkę i ci pokażę!",
    "Hmm. I wonder what Carol is up to?": "Hmm. Ciekawe, co kombinuje Carol?",
    "That was a lot of fun, Carol.": "To była świetna zabawa, Carol.",
    "I’m glad you liked it, 1Hero. It’s been a long time since I had such a good dickin’.": "Cieszę się, że ci się podobało, 1Hero. Dawno nie miałam takiego dobrego pieprzenia.",
    "You make me feel like a new woman.": "Sprawiasz, że czuję się jak nowa kobieta.",
    "I’d be happy to make you feel that way again…": "Chętnie sprawię, że znów tak się poczujesz…",
    "But where is this going?": "Ale dokąd to zmierza?",
    "Oh, 1Hero. We’re just havin’ fun. Someday you’ll get tired of me and move on.": "Och, 1Hero. Po prostu się bawimy. Kiedyś znudzę ci się i pójdziesz dalej.",
    "Besides, you’re married to your work, remember?": "Poza tym jesteś żonaty z robotą, pamiętasz?",
    "Carol, that’s not fair.": "Carol, to nie fair.",
    "Life isn’t fair, hun. But it goes on, all the same.": "Życie nie jest fair, skarbie. Ale i tak toczy się dalej.",
    "Let’s just enjoy it while it lasts.": "Po prostu cieszmy się tym, póki trwa.",
    "What about Heather?": "A co z Heather?",
    "You gettin’ eyes for Heather?": "Zalazła ci w oko Heather?",
    "No! That’s not what I meant…": "Nie! Nie o to mi chodziło…",
    "You’re going to tell her about this, aren’t you?": "Zamierzasz jej o tym powiedzieć, prawda?",
    "I think this one’s a secret between you and me.": "Myślę, że to sekret między tobą a mną.",
    "Do you think Heather wants… something more?": "Myślisz, że Heather chce… czegoś więcej?",
    "Why don’t you ask her?": "Czemu jej nie spytasz?",
    "I’ve never thought about Heather that way.": "Nigdy nie myślałem o Heather w ten sposób.",
    "But you’ve thought about me?": "A o mnie myślałeś?",
    "I suppose you’re right… But I can’t cross that line… Heather wouldn’t either.": "Chyba masz rację… Ale nie mogę przekroczyć tej granicy… Heather też by nie przekroczyła.",
    "We best not upset Heather. Things between us have gone farther than either one of us could have predicted.": "Lepiej nie denerwować Heather. Sprawy między nami zaszły dalej, niż którekolwiek z nas mogło przewidzieć.",
    "Do you think we should stop?": "Myślisz, że powinniśmy przestać?",
    "Hell no… Just… Let’s keep this new development close to the chest.": "Jasna cholera, nie… Po prostu… Trzymajmy tę nowość w tajemnicy.",
    "Alright. I can live with that.": "Dobra. Mogę z tym żyć.",
    "As long as I get to see those beautiful breasts again.": "Dopóki znów zobaczę te piękne piersi.",
    "Hahahaha.": "Hahahaha.",
    "I’ll walk myself out… and I’ll be sure not to disturb Hannah’s beauty sleep.": "Sama wyjdę… i postaram się nie zakłócać słodkiego snu Hannah.",
    "A dump truck could drive through the house and she wouldn’t wake up.": "Przez dom mógłby przejechać tir, a ona by się nie obudziła.",
    "Haha! I’ll see you later.": "Haha! Do zobaczenia.",
    "See ya, hunky man.": "Do zobaczenia, przystojniaku.",
    "I had a good time, 1Hero. Maybe we can do it again sometime.": "Dobrze się bawiłam, 1Hero. Może powtórzymy to kiedyś.",
    "Having a nice evening, superstar?": "Miły wieczór, gwiazdorze?",
    "I’m on TV once and now I’m a superstar?": "Raz w TV i już jestem gwiazdor?",
    "You are to me.": "Dla mnie jesteś.",
    "What a surprise. Here for some fun?": "Co za niespodzianka. Przyszedłeś się zabawić?",
    "Chloe and Hannah are downstairs!": "Chloe i Hannah są na dole!",
    "I’m only jokin’!": "Tylko żartuję!",
    "But if you’re feeling horny, I can come over to your place.": "Ale jeśli masz ochotę, mogę wpaść do ciebie.",
    "Carol!": "Carol!",
    "Hahaha.": "Hahaha.",
    "You seem in a good mood.": "Wyglądasz na w dobrym nastroju.",
    "What can I say? Justice was served, and it feels great.": "Co tu dużo mówić? Sprawiedliwości stało się zadość i czuję się świetnie.",
    "You’re up early.": "Wcześnie wstałeś.",
    "How’d you sleep?": "Jak spałeś?",
    "Much better after that stuffin’ you gave me.": "Dużo lepiej po takim nadzieniu, jakie mi zafundowałeś.",
    "Would you like some tea and crumpets?": "Życzysz sobie herbatki i ciasteczek?",
    "Come, my good sir. I’ll show you my collection of girly dolls.": "Chodź, szanowny panie. Pokażę ci moją kolekcję laleczek.",
    "Haha! Of course I’ll let you accompany me to the ball.": "Haha! Oczywiście pozwolę ci towarzyszyć mi na balu.",
    "Hannah? What are you doing?": "Hannah? Co robisz?",
    "1Hero! Don’t look at me!": "1Hero! Nie patrz na mnie!",
    "What are you wearing!?": "Co masz na sobie!?",
    "What are you doing here!?": "Co tu robisz!?",
    "I came to invite you over to the pool party.": "Przyszedłem zaprosić cię na imprezę przy basenie.",
    "I got kidnapped!...": "Zostałam porwana!...",
    "Kidnapped?": "Porwana?",
    "By an evil beauty pageant director!": "Przez złą dyrektorkę konkursu piękności!",
    "She got me good! Look what she did to me!": "Dobra mnie dorwała! Zobacz, co mi zrobiła!",
    "Hahahaha!": "Hahahaha!",
    "Hey! Don’t laugh at me!": "Hej! Nie śmiej się ze mnie!",
    "You look ridiculous!": "Wyglądasz absurdalnie!",
    "Fuck you! You’re a meanie!": "Spierdalaj! Jesteś wredny!",
    "I’m sorry… I’ve just never seen you in a dress before.": "Przepraszam… Po prostu nigdy wcześniej nie widziałem cię w sukience.",
    "Who the hell is that?... Is Ma home already?": "Kto to, do cholery?... Mama już w domu?",
    "Hannah, I’m home!": "Hannah, jestem w domu!",
    "Quick, 1Hero!... You have to distract her.": "Szybko, 1Hero!... Musisz ją zagadać.",
    "Do it! I’ll never live this down!": "Zrób to! Nigdy tego nie odchoruję!",
    "Fine, fine, change back.": "Dobra, dobra, przebierz się z powrotem.",
    "My clothes are in my room!": "Moje ubrania są w pokoju!",
    "Do something! I can’t keep her distracted forever.": "Rób coś! Nie zagadam jej w nieskończoność.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=48 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=73: raise SystemExit(f'Expected 73, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map48')
