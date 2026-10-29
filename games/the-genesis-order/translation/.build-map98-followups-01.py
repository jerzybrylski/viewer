#!/usr/bin/env python3
"""Build Polish drafts for Map 98 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map98-followups-01.jsonl'
TRANSLATIONS = {
    "I don’t know, but let’s find out.": "Nie wiem, ale przekonajmy się.",
    "You have the key?": "Masz klucz?",
    "Yep. Let’s try it.": "Tak. Spróbujmy.",
    "I don’t know, but I fixed the key. Maybe it’ll work.": "Nie wiem, ale naprawiłem klucz. Może zadziała.",
    "Try it out.": "Wypróbuj.",
    "Hands in the air!": "Ręce do góry!",
    "You’re cornered. Give up.": "Jesteście osaczeni. Poddajcie się.",
    "I give up! Don’t shoot!": "Poddaję się! Nie strzelaj!",
    "Paul?": "Paul?",
    "You know this man?": "Znasz tego człowieka?",
    "He’s the producer at Channel 4.": "To producent z Channel 4.",
    "You bastards never give up.": "Wy, sukinsyny, nigdy nie odpuszczacie.",
    "What are you doing here, Paul?": "Co tu robisz, Paul?",
    "Going for a hike. It’s none of your business.": "Idę na spacer. Nie twój interes.",
    "You’re trespassing.": "Wtargnąłeś na teren prywatny.",
    "You’re under arrest!": "Jesteś aresztowany!",
    "The woods are a public park.": "Lasy to park publiczny.",
    "Let’s not do anything rash.": "Nie róbmy nic pochopnego.",
    "You can’t stop us from being in the park.": "Nie możecie zabronić nam przebywania w parku.",
    "Us?": "Nam?",
    "I’m not saying another word.": "Nie powiem ani słowa więcej.",
    "You’re in big trouble!": "Masz poważne kłopoty!",
    "Calm down. We’re not arresting him.": "Spokojnie. Nie aresztujemy go.",
    "Where’s the other one?": "Gdzie jest ten drugi?",
    "Let me go.": "Puśćcie mnie.",
    "Fine… You’re free to leave.": "Dobra… Możesz odejść.",
    "Uhh… Can I leave out the front?": "Yyy… Mogę wyjść przodem?",
    "Scared of the dark?": "Boisz się ciemności?",
    "I prefer not to get eaten alive by mosquitoes.": "Wolę nie zostać żywcem pożartym przez komary.",
    "Let’s get him out of here.": "Wyprowadźmy go stąd.",
    "Psst! 1Hero!": "Psst! 1Hero!",
    "Everything’s clear. Follow me.": "Teren czysty. Chodź za mną.",
    "You caught me, 1Hero.": "Przyłapałeś mnie, 1Hero.",
    "Kimberly!?": "Kimberly!?",
    "Shhhh. Not so loud.": "Ciii. Nie tak głośno.",
    "Something’s going on here. I want to know what it is.": "Coś tu się dzieje. Chcę wiedzieć co.",
    "I can’t let you trespass, Kimberly.": "Nie mogę pozwolić ci włamać się, Kimberly.",
    "What aren’t you telling me? What do you know about the Guild?": "Co przede mną ukrywasz? Co wiesz o Gildii?",
    "This isn’t what it looks like. There’s something far more mysterious going on here.": "To nie jest to, na co wygląda. Dzieje się tu coś znacznie bardziej tajemniczego.",
    "So you do know?": "Więc jednak wiesz?",
    "I wish I did.": "Chciałbym wiedzieć.",
    "You need my help.": "Potrzebujesz mojej pomocy.",
    "What are you talking about? I have the entire police force behind me.": "O czym ty mówisz? Mam za sobą całą policję.",
    "No, you don’t.": "Nie, nie masz.",
    "If the police cared about the thieves, they’d be searching the forest.": "Gdyby policji zależało na złodziejach, przeczesywałaby las.",
    "Something else is going on.": "Dzieje się coś innego.",
    "You’re very observant, Miss Foxx.": "Jesteś bardzo spostrzegawcza, panno Foxx.",
    "You need to have ears inside the mansion.": "Musisz mieć uszy wewnątrz rezydencji.",
    "We need a warrant for that.": "Na to potrzebujemy nakazu.",
    "Spoken like a true officer of the law.": "Jak na prawdziwego stróża prawa przystało.",
    "Let me bug the joint. I can get away with it.": "Pozwól mi założyć podsłuch. Mnie się upiecze.",
    "What!? You can’t get away with that.": "Co!? Nie ujdzie ci to na sucho.",
    "We’ve gotten away with far more.": "Uchodziło nam znacznie więcej.",
    "You people sure do take your jobs seriously.": "Wy to naprawdę poważnie traktujecie swoją pracę.",
    "You’re damned right we do. Let me help you.": "Akurat. Pozwól mi pomóc.",
    "I can’t be involved in this.": "Nie mogę być w to zamieszany.",
    "If you help me, you can have access to the recordings.": "Jeśli mi pomożesz, dostaniesz dostęp do nagrań.",
    "I’m not hearing this.": "Nie słyszę tego.",
    "I can’t do this alone.": "Nie dam rady sama.",
    "You have access to the mansion. I can give you three wireless transmitters with microphones.": "Masz dostęp do rezydencji. Mogę dać ci trzy bezprzewodowe nadajniki z mikrofonami.",
    "If I get caught, my job is toast!": "Jeśli mnie złapią, po robocie!",
    "Then don’t get caught.": "To nie daj się złapać.",
    "You are asking a lot.": "Wymagasz wiele.",
    "Do you want to know what’s going on inside that mansion?": "Chcesz wiedzieć, co dzieje się wewnątrz rezydencji?",
    "Then help me help you.": "To pomóż mi pomóc tobie.",
    "What exactly do I do?": "Co dokładnie mam zrobić?",
    "You have to hide them with the microphone pointed outward.": "Musisz je ukryć mikrofonem na zewnątrz.",
    "Listen: You have to get this exactly correct or we won't be able to hear shit.": "Słuchaj: musisz zrobić to dokładnie, bo inaczej nic nie usłyszymy.",
    "Can you? This is important.": "Dasz radę? To ważne.",
    "I’m fine. Just give me the damned bugs.": "W porządku. Dawaj te cholerne pluskwy.",
    "Here…": "Proszę…",
    "Check the signals too. They all need cell connections.": "Sprawdź też sygnał. Wszystkie potrzebują zasięgu.",
    "Don’t mess this up, 1Hero.": "Nie spieprz tego, 1Hero.",
    "When can we meet again?": "Kiedy znów się spotkamy?",
    "Wait… She doesn’t know my number.": "Czekaj… Ona nie zna mojego numeru.",
    "I suppose it is low risk. These aren’t the bugs we use at the station.": "Chyba ryzyko jest niskie. To nie są pluskwy, których używamy na posterunku.",
    "They would trace back to Channel 4.": "Prowadziłyby do Channel 4.",
    "Okay, Kimberly. I’m trusting you on this.": "Dobra, Kimberly. Zaufam ci w tej sprawie.",
    "The side entrance is beyond here.": "Boczne wejście jest dalej.",
    "Over the trench?": "Ponad rowem?",
    "Scared of heights, angel?": "Boisz się wysokości, aniołku?",
    "Scared of depths.": "Boję się głębi.",
    "We need a makeshift bridge.": "Potrzebujemy prowizorycznego mostu.",
    "Have you been this way?": "Byłaś tą drogą?",
    "Trust me. This is the right way.": "Zaufaj mi. To właściwa droga.",
    "I’ll find something we can use to cross.": "Znajdę coś, czym możemy przejść.",
    "I’ve got a ladder segment, but it’s not long enough on its own…": "Mam segment drabiny, ale sama jest za krótka…",
    "Good work. Let’s move.": "Dobra robota. Ruszajmy.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=98 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=88: raise SystemExit(f'Expected 88, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map98')
