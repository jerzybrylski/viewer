#!/usr/bin/env python3
"""Build Polish drafts for Map 109 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map109-followups-01.jsonl'
TRANSLATIONS = {
    "The sound is coming from this grate!": "Dźwięk dochodzi z tej kratki!",
    "What’s that light? Is this some sort of furnace?": "Co to za światło? To jakiś piec?",
    "… That doesn’t sound like a furnace.": "…To nie brzmi jak piec.",
    "Fuck. There’s nowhere to hide.": "Cholera. Nie ma gdzie się schować.",
    "The new one doesn’t have a battery either.": "Nowa też nie ma baterii.",
    "What the hell am I supposed to do now?...": "Co ja, do cholery, mam teraz zrobić?...",
    "Was Kimberly supposed to give me a battery?": "Kimberly miała mi dać baterię?",
    "This new transmitter should fix it right up.": "Ten nowy nadajnik powinien wszystko naprawić.",
    "The sound is back!": "Dźwięk wrócił!",
    "… I can see an orange glow.": "…Widzę pomarańczową poświatę.",
    "What the hell is going on down there?": "Co się, do cholery, tam dzieje na dole?",
    "You were right, 1Hero. It worked.": "Miałeś rację, 1Hero. Zadziałało.",
    "The fire got put out?": "Ogień został ugaszony?",
    "Yeah. And the lepers went away… But I don’t know for how long.": "Tak. I trędowaci sobie poszli… Ale nie wiem, na jak długo.",
    "Ah! It’s that creepy sound!": "A! To ten upiorny dźwięk!",
    "It’s coming from the grate.": "Dochodzi z kratki.",
    "One second. I have a crowbar… I could pry open the grate.": "Chwileczkę. Mam łom… Mógłbym podważyć kratkę.",
    "Are you crazy? Let’s leave.": "Zwariowałeś? Chodźmy.",
    "We’re just going to look.": "Tylko zerkniemy.",
    "We!?": "My!?",
    "Come on Erica. Don’t you want to have a little fun?": "Daj spokój, Erica. Nie chcesz się trochę zabawić?",
    "I’m not about to have sex in a sewer.": "Nie zamierzam pieprzyć się w kanale.",
    "We don’t have to fuck to have fun.": "Nie musimy się pieprzyć, by się zabawić.",
    "Shit. Shit. Shit.": "Cholera. Cholera. Cholera.",
    "We’ll be fine.": "Będzie dobrze.",
    "I see a ladder… There’s another room down there.": "Widzę drabinę… Na dole jest kolejne pomieszczenie.",
    "A room?": "Pomieszczenie?",
    "Let’s be quick.": "Pospieszmy się.",
    "It’s a food storage room…": "To magazyn żywności…",
    "But what’s with all the clothes?": "Ale co z tymi wszystkimi ubraniami?",
    "Come on. We can’t stay here…": "Chodź. Nie możemy tu zostać…",
    "I’ve already been caught messing around once. I don’t know what would happen if I get caught again.": "Już raz przyłapano mnie na igraszkach. Nie wiem, co by było, gdybym znów wpadła.",
    "Don’t forget about the wireless transmitters… Don’t let anyone find them.": "Nie zapomnij o bezprzewodowych nadajnikach… Niech nikt ich nie znajdzie.",
    "Get dressed. Let’s get out of here.": "Ubierz się. Wynośmy się stąd.",
    "I should get out of here. I don’t know where Lillian went, but if she sees us now, it’ll look bad.": "Powinienem się stąd wynosić. Nie wiem, gdzie poszła Lillian, ale jeśli zobaczy nas teraz, źle to wygląda.",
    "You’re right. Let’s b-line to the exit.": "Masz rację. Spieprzajmy prosto do wyjścia.",
    "What are you doing in here?": "Co tu robisz?",
    "I’m hiding the Watcher’s Eye.": "Ukrywam Oko Obserwatora.",
    "Mother would not want you here.": "Matka nie chciałaby cię tu widzieć.",
    "The mansion is too large. We will store it here.": "Rezydencja jest za duża. Przechowamy je tutaj.",
    "You risk our security because you are lazy?": "Ryzykujesz nasze bezpieczeństwo, bo jesteś leniwy?",
    "No one will find it.": "Nikt go nie znajdzie.",
    "The rift must remain a secret.": "Szczelina musi pozostać tajemnicą.",
    "Do not worry, brother. No one will find the rift.": "Nie martw się, bracie. Nikt nie znajdzie szczeliny.",
    "So this is the item that lets them access what they’re calling the rift…": "Więc to przedmiot, który pozwala im uzyskać dostęp do tego, co nazywają szczeliną…",
    "But how?": "Ale jak?",
    "Mother trusts the detective enough to let him see the rift.": "Matka ufa detektywowi na tyle, by pozwolić mu zobaczyć szczelinę.",
    "It’s part of her plan. Now he will become one of us.": "To część jej planu. Teraz stanie się jednym z nas.",
    "We can find the Toma Leolo pieces ourselves. We don’t need his help.": "Możemy sami znaleźć fragmenty Tomy Leolo. Nie potrzebujemy jego pomocy.",
    "We are not equipped to search for such artifacts.": "Nie jesteśmy wyposażeni, by szukać takich artefaktów.",
    "Letting the detective inside of the rift was a bad idea. Mark my words.": "Wpuszczenie detektywa do szczeliny było złym pomysłem. Zapamiętaj moje słowa.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=109 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=51: raise SystemExit(f'Expected 51, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map109')
