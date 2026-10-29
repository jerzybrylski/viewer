import json
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl')
EVENTS = {
    33: {
        "Woah, this really is a big mess.": "Łał, ale tu bałagan.",
        "1Hero! Just in time.": "1Hero! W samą porę.",
        "Just in time for what? You’ve been dawdling for the past half hour, missy.": "Na co w samą porę? Od pół godziny się obijasz, młoda damo.",
        "No, I haven’t! We just don’t have anything good enough to clean up all this smoke and soot.": "Wcale nie! Po prostu nie mamy niczego, czym dałoby się porządnie usunąć ten dym i sadzę.",
        "And who’s fault is that? You used all the cleaning product we had on one little spot.": "A czyja to wina? Zużyłaś cały środek czyszczący na jedną małą plamę.",
        "But by golly does this spot look shiny.": "Ależ ta plama teraz lśni.",
        "I’d hate to leave this mess for morning. The smoke smell is going to get into the curtains.": "Nie chcę zostawiać tego bałaganu na rano. Zapach dymu wsiąknie w zasłony.",
        "Don’t worry. I’ll run out and grab something from the store to help clean the mess.": "Spokojnie. Skoczę do sklepu po coś, co pomoże nam posprzątać.",
        "I don’t think you’ll find anything strong enough. But I appreciate the offer.": "Nie sądzę, żebyś znalazł coś wystarczająco mocnego. Ale dziękuję za propozycję.",
        "Such a helpful man.": "Ależ pomocny z ciebie mężczyzna.",
    },
    42: {
        "Looks like you two found your clothes.": "Widzę, że znalazłyście ubrania.",
        "Problem solved. Nothing to see here, Ma!": "Problem rozwiązany. Nie ma tu na co patrzeć, mamo!",
        "You’re not exactly the most convincing liar, Hannah.": "Nie jesteś zbyt przekonującą kłamczuchą, Hannah.",
        "What are you talking about? She bought it, hook, line and sinker!": "O czym ty mówisz? Nabrała się bez reszty!",
        "Come on, you two. Next time you feel like stripping, maybe do it in your bedroom.": "No już, wy dwie. Następnym razem rozbierajcie się we własnej sypialni.",
        "You owe him a blowjob, Chloe.": "Jesteś mu winna loda, Chloe.",
        "Hannah!": "Hannah!",
        "Sorry, girls. I need to get going.": "Wybaczcie, dziewczyny. Muszę już iść.",
        "Thanks for stopping by.": "Dzięki, że wpadłeś.",
    },
    11: {
        "Where is Hannah and Chloe?": "Gdzie są Hannah i Chloe?",
        "They didn’t tell you?": "Nie powiedziały ci?",
        "Tell me what?": "Czego?",
        "They went to the cave.": "Poszły do jaskini.",
        "Bad weather is on its way. Hannah should know better.": "Idzie zła pogoda. Hannah powinna była o tym pomyśleć.",
        "It’s not far. I can go warn them.": "To niedaleko. Mogę je ostrzec.",
        "Thanks, 1Hero. Y’all better not linger out there.": "Dzięki, 1Hero. Nie siedźcie tam zbyt długo.",
        "Don’t worry. I’ll take care of it.": "Spokojnie. Zajmę się tym.",
    },
    57: {
        "Hannah, get a pot of boiling water ready.": "Hannah, przygotuj garnek wrzątku.",
        "You relax. We’ve got this.": "Ty odpoczywaj. Zajmiemy się tym.",
        "Last call for the ear of corn. Use it now or it’s going in the pot.": "Ostatnia szansa na tę kolbę kukurydzy. Bierz ją albo ląduje w garnku.",
        "Hahaha! That’s silly.": "Hahaha! Ale głupoty.",
        "Carol, you’re too funny.": "Carol, ale jesteś zabawna.",
        "Give it here. I’ll do it if you want to see it.": "Daj ją tutaj. Zrobię to, jeśli chcecie zobaczyć.",
        "Hahaha!": "Hahaha!",
        "Okay, girl… Catch.": "Dobra, mała… Łap.",
    },
    9: {
        "Thanks for helping Hannah. She sure does love it when you visit.": "Dzięki za pomoc Hannah. Bardzo lubi, kiedy ją odwiedzasz.",
        "It was our pleasure.": "Cała przyjemność po naszej stronie.",
        "Hannah tells me you and Chloe might start dating.": "Hannah mówi, że ty i Chloe możecie zacząć ze sobą chodzić.",
        "Oh, uhh… Don’t listen to Hannah. She’s just trying to embarrass me.": "Och, eee… Nie słuchaj Hannah. Chce mnie tylko zawstydzić.",
        "That sounds like my Hannah.": "To cała moja Hannah.",
    },
    36: {
        "Are you here for Hannah?": "Przyszedłeś do Hannah?",
        "Hannah! Wake up!": "Hannah! Obudź się!",
        "Sorry, 1Hero. Hannah’s being lazy today.": "Wybacz, 1Hero. Hannah dziś się leni.",
    },
    37: {
        "Whatcha’ doin’? Here to have some fun?": "Co porabiasz? Przyszedłeś się zabawić?",
        "Sorry, Hannah. Tomorrow is a workday.": "Wybacz, Hannah. Jutro jest dzień pracy.",
        "When is it going to stop raining?": "Kiedy wreszcie przestanie padać?",
    },
    61: {
        "Before I forget, here is the cornbread that Judy loves…": "Zanim zapomnę, oto chleb kukurydziany, który tak lubi Judy…",
        "See you this evening.": "Do zobaczenia wieczorem.",
        "See you then.": "Do zobaczenia.",
    },
    7: {"I shouldn’t go up there while Hannah is changing.": "Nie powinienem tam wchodzić, kiedy Hannah się przebiera."},
    17: {"We need something to clean up the mess.": "Potrzebujemy czegoś do posprzątania tego bałaganu."},
    39: {"Are you going to church tomorrow?": "Idziesz jutro do kościoła?"},
}
known = {r['id'] for r in map(json.loads, MERGED.read_text(encoding='utf-8').splitlines()) if r['translation'].strip()}
rows, missing = [], set()
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
path = ROOT / 'drafts/custom-dialogue-map23-followups-04.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8', newline='\n')
print(f'Wrote Map 23 follow-ups: {len(rows)} records across {len(EVENTS)} events')
