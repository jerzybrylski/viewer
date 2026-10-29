import json
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step10.jsonl')

EVENTS = {375: {'I think 1Hero would enjoy a toy like this.': 'Myślę, że 1Hero spodobałaby się taka zabawka.', 'How does it work? Do you put it in your pussy?': 'Jak to działa? Wkłada się to do cipki?', 'You press it against your clit… or maybe your dick.': 'Przykładasz do łechtaczki… albo do kutasa.', 'Haha. No toys for me.': 'Haha. Nie potrzebuję zabawek.', 'What? You don’t think you’d like it?': 'Co? Myślisz, że by ci się nie spodobało?', 'I bet it would make you cum, 1Hero.': 'Założę się, że doprowadziłoby cię do orgazmu, 1Hero.', '1Hero doesn’t need that. Don’t be silly.': '1Hero tego nie potrzebuje. Nie wygłupiaj się.', 'I prefer the real thing.': 'Wolę prawdziwą rzecz.', 'Hahaha. You naughty boy.': 'Hahaha. Ale z ciebie niegrzeczny chłopiec.', 'Want to try it out? I can lock the door.': 'Chcesz spróbować? Mogę zamknąć drzwi.', '1Hero’s not going to cum from a silly vibrator.': '1Hero nie dojdzie od jakiegoś głupiego wibratora.', 'I bet he would.': 'Założę się, że dojdzie.', 'I second that bet.': 'Też tak obstawiam.', 'Haha. Don’t even think about it.': 'Haha. Nawet o tym nie myśl.', 'Come on, babe. Let’s give them a show.': 'No dalej, kochanie. Zróbmy im przedstawienie.', 'Do it, 1Hero. Let’s impress Sister.': 'Dawaj, 1Hero. Zaimponujmy siostrze.', 'You’re going to let your sister make you cum? You are kinky.': 'Pozwolisz siostrze doprowadzić się do orgazmu? Ale z ciebie zboczeniec.', 'She’s not my sister.': 'Ona nie jest moją siostrą.', 'Come on. Don’t tease him.': 'No dalej. Nie drocz się z nim.', 'Erica!': 'Erica!', 'Hard as a rock!': 'Twardy jak skała!', 'Oh, dear!': 'Ojej!', 'Well, 1Hero? How’s it feel?': 'No i jak, 1Hero? Jakie to uczucie?', "It sucks… I told you. A toy won't make me cum.": 'Beznadzieja… Mówiłem. Zabawka nie doprowadzi mnie do orgazmu.', 'He’s lying! Go harder!': 'Kłamie! Mocniej!', 'This is the max setting.': 'To maksymalna moc.', 'If you want to feel something crazy, put your mouth on it.': 'Jeśli chcesz poczuć coś niesamowitego, weź to do ust.', 'On the toy?': 'Tę zabawkę?', "Tickles your teeth, doesn't it?": 'Łaskocze w zęby, co?', 'Holy moly! She’s got his weiner in her mouth!': 'O rany! Trzyma jego siusiaka w ustach!', 'That… feels better.': 'To… lepsze.', 'It looks painful.': 'Wygląda boleśnie.', 'Oh! Shit!': 'Och! Cholera!', '1Hero!?': '1Hero!?', 'That looks intense!': 'Ależ to wygląda!', 'That feels… really good!': 'To jest… naprawdę przyjemne!', 'Now this is a sales pitch.': 'To dopiero skuteczna reklama.', 'No kidding.': 'Nie żartuj.', 'There’s plenty of toys to go around.': 'Zabawek wystarczy dla wszystkich.', 'Sorry… It’s good. Everything is good.': 'Przepraszam… Jest dobrze. Wszystko jest dobrze.', 'That’s it, girl. Work that cock.': 'Właśnie tak, kochanie. Zajmij się tym kutasem.', 'Make him cum! And you win the bet!': 'Doprowadź go do orgazmu, a wygrasz zakład!', 'Shit, shit, shit!': 'Cholera, cholera, cholera!', 'Faster! Faster! Make him cum!': 'Szybciej! Szybciej! Doprowadź go!', 'How much longer are you going to last?': 'Jak długo jeszcze wytrzymasz?', 'I’m… cumming!': 'Już… dochodzę!', 'It’s in her mouth!': 'Jest w jej ustach!', 'Dear heavens!': 'O rany!', 'What are you doing, Erica? Swallow it.': 'Co robisz, Erica? Połknij.', 'No way! I want some!': 'Nie ma mowy! Ja też chcę!', 'You’ve got a kinky harem, 1Hero.': 'Masz naprawdę zboczony harem, 1Hero.', 'Hannah!': 'Hannah!'}}

known = set()
for line in MERGED.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    if row['translation'].strip():
        known.add(row['id'])
rows_by_event = {event_id: [] for event_id in EVENTS}
missing = set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    event_id = context.get('event_id')
    if context.get('source_kind') != 'common_event' or event_id not in EVENTS or row['id'] in known:
        continue
    source = row['source_text'].strip()
    if not source or source.startswith('/') or source in {'…', '...', '..'}:
        continue
    translation = EVENTS[event_id].get(source)
    if translation is None:
        missing.add((event_id, source))
        continue
    row['translation'] = translation
    rows_by_event[event_id].append(row)
if missing:
    raise SystemExit('Unmapped strings: ' + repr(sorted(missing)))
for event_id, rows in rows_by_event.items():
    path = ROOT / f'drafts/custom-dialogue-common-event-{event_id}-01.jsonl'
    if path.exists():
        raise SystemExit(f'Refusing to overwrite {path}')
    path.write_text(
        ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
        encoding='utf-8',
        newline='\n',
    )
    print(f'Wrote Common Event {event_id}: {len(rows)} records')
print('Total:', sum(map(len, rows_by_event.values())))
