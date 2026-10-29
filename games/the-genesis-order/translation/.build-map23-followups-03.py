import json
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl')
PRIOR = [
    ROOT / 'drafts/custom-dialogue-map23-followups-02.jsonl',
    ROOT / 'drafts/custom-dialogue-map9-events-82-55-97-17-95-01.jsonl',
    ROOT / 'drafts/custom-dialogue-map9-events-59-78-8-4-43-01.jsonl',
    ROOT / 'drafts/custom-dialogue-map9-followups-05.jsonl',
]
EVENTS = {
    12: {
        "Thanks for being there for me, 1Hero.": "Dzięki, że przy mnie jesteś, 1Hero.",
        "You’re a good teacher.": "Jesteś dobrym nauczycielem.",
        "I hope Hannah doesn’t tickle you anymore.": "Mam nadzieję, że Hannah już cię nie łaskocze.",
        "Haha. Maybe I should keep my pants on around her.": "Haha. Może powinienem przy niej nie zdejmować spodni.",
        "I don’t know how I feel about seeing Ma get a dickin’.": "Nie wiem, co myśleć o tym, że ktoś rżnie mamę.",
        "I hope it’s okay.": "Mam nadzieję, że wszystko w porządku.",
        "If you fall in love with Ma, I’ll kick your ass.": "Jeśli zakochasz się w mamie, skopię ci tyłek.",
        "I’m so hungry!": "Ale jestem głodna!",
        "Dinner’s almost ready. Did you put the goat back in its pen?": "Kolacja prawie gotowa. Wprowadziłaś kozła z powrotem do zagrody?",
        "I totally forgot.": "Całkiem o tym zapomniałam.",
        "I’ll go check on him.": "Pójdę do niego zajrzeć.",
    },
    59: {
        "What’s wrong, Carol?": "Co się stało, Carol?",
        "I just got this letter from the court.": "Właśnie dostałam pismo z sądu.",
        "It says the state is taking over my farm.": "Piszą, że państwo przejmuje moją farmę.",
        "Because of the Casula ruins in the cave. Somehow they know about them.": "Chodzi o ruiny Casula w jaskini. W jakiś sposób się o nich dowiedzieli.",
        "The letter says the government has a responsibility to preserve indigenous culture.": "W piśmie napisano, że rząd ma obowiązek chronić kulturę rdzennych mieszkańców.",
        "For some reason, it also mentions clearing and developing the rest of the farm for ‘’government housing’’.": "Z jakiegoś powodu wspominają też o wyburzeniu i zabudowaniu reszty farmy pod „mieszkania rządowe”.",
        "That sounds weird.": "To brzmi podejrzanie.",
        "I don’t want to lose my home, 1Hero.": "Nie chcę stracić domu, 1Hero.",
        "There must be something you can do.": "Musi być coś, co możesz zrobić.",
        "Raise hell is what I’m going to do.": "Zrobię taką awanturę, jakiej jeszcze nie widzieli.",
        "I’m goin’ to give the judge who signed this a piece of my mind!": "Powiem temu sędziemu, który to podpisał, co o nim myślę!",
        "Well, that’s…": "No cóż…",
        "Oooh, boy.": "Oho, będzie się działo.",
    },
    38: {
        "Ma! What are you doing back already?": "Mamo! Czemu tak szybko wróciłaś?",
        "Hannah! Where are your pants?": "Hannah! Gdzie masz spodnie?",
        "Chloe? What are you three up to?": "Chloe? Co wy trzy wyprawiacie?",
        "Uhh… Carol…": "Eee… Carol…",
        "We were just looking for Chloe’s shirt.": "Szukałyśmy tylko koszuli Chloe.",
        "How does that explain the lack of pants?": "I co ma do tego brak spodni?",
        "We’ve got major clothes problems.": "Mamy poważny problem z ubraniami.",
        "Well, good luck. I’m sure 1Hero is being very helpful.": "No to powodzenia. Jestem pewna, że 1Hero bardzo wam pomaga.",
        "What the hell is she doing back? I thought you said she’d be gone for an hour.": "Co ona tu robi? Mówiłaś, że nie będzie jej przez godzinę.",
        "She was! She must have forgotten something.": "Nie było jej! Musiała o czymś zapomnieć.",
        "Don’t worry. Carol is cool about this kind of stuff.": "Spokojnie. Carol nie robi problemów z takich rzeczy.",
        "She’s going to tell my mom. She tells her everything.": "Powiem mamie. Ona opowiada jej wszystko.",
        "Who cares? It’s not like no one’s ever seen us naked.": "Kogo to obchodzi? To nie tak, że nikt nigdy nie widział nas nago.",
        "Argh! Why does everything have to suck!": "Argh! Czemu wszystko musi być beznadziejne?!",
        "Stop your belly-achin’!": "Przestań marudzić!",
        "Put your clothes back on. I’ll smooth things over with Carol.": "Ubierzcie się. Załatwię to z Carol.",
    },
    6: {
        "If you’re just going to cause trouble, maybe you should stay home.": "Jeśli masz tylko sprawiać kłopoty, może lepiej zostań w domu.",
        "What?! I want to go to Heather’s house too!": "Co?! Ja też chcę iść do Heather!",
        "That’s all I came here to ask. No need to pick on me.": "Tylko o to chciałem zapytać. Nie musisz się na mnie wyżywać.",
        "Poor 1Hero. Got your feelin’s hurt?": "Biedny 1Hero. Uraziłam twoje uczucia?",
        "You know, I bought that house I was telling you about.": "Wiesz, kupiłam ten dom, o którym ci opowiadałam.",
        "Time to party!": "Czas na imprezę!",
        "It’s still not much to look at. I need to fix it up.": "Na razie nie wygląda najlepiej. Muszę go wyremontować.",
        "I’ve got a plan for you, 1Hero.": "Mam dla ciebie plan, 1Hero.",
        "I’m going to play matchmaker with you.": "Zostanę twoją swatką.",
        "See ya tonight at dinner.": "Do zobaczenia wieczorem przy kolacji.",
        "Okay, Dad!": "Dobrze, tato!",
        "And maybe put some clothes on.": "I może coś na siebie załóż.",
    },
}

known = {r['id'] for r in map(json.loads, MERGED.read_text(encoding='utf-8').splitlines()) if r['translation'].strip()}
for path in PRIOR:
    for line in path.read_text(encoding='utf-8').splitlines():
        known.add(json.loads(line)['id'])
rows = []
missing = set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    event_id = context.get('event_id')
    if context.get('source_kind') != 'map' or context.get('map_id') != 23 or event_id not in EVENTS or row['id'] in known:
        continue
    source = row['source_text'].strip()
    if not source or source.startswith('/') or source in {'…', '...', '..'}:
        continue
    translation = EVENTS[event_id].get(source)
    if translation is None:
        missing.add((event_id, source))
        continue
    row['translation'] = translation
    rows.append(row)
if missing:
    raise SystemExit('Unmapped strings: ' + repr(sorted(missing)))
path = ROOT / 'drafts/custom-dialogue-map23-followups-03.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8', newline='\n')
print(f'Wrote Map 23 follow-ups: {len(rows)} records across {len(EVENTS)} events')
