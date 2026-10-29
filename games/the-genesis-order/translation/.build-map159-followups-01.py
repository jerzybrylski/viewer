#!/usr/bin/env python3
"""Build Polish drafts for Map 159 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map159-followups-01.jsonl'
TRANSLATIONS = {
    "So you’re both spies?": "Więc oboje jesteście szpiegami?",
    "I’m the spy. He’s… my boyfriend.": "Ja jestem szpiegiem. On… jest moim chłopakiem.",
    "Like hell! He’s my boyfriend.": "Gówno prawda! On jest moim chłopakiem.",
    "How the hell do you know each other?": "Jak się, do cholery, znacie?",
    "We fucked on camera! It was all over the news.": "Pieprzyliśmy się na kamerze! Było o tym w wiadomościach.",
    "Ella!?": "Ella!?",
    "What? I’m just being honest.": "Co? Po prostu jestem szczera.",
    "Seems 1Hero gets around.": "Wygląda na to, że 1Hero się obraca.",
    "As long as we’re being honest, I’ve not met a woman I haven’t fucked in weeks.": "Skoro jesteśmy szczerzy, nie spotkałem kobiety, której bym nie przeleciał od tygodni.",
    "You can’t kill Duncan.": "Nie możesz zabić Duncana.",
    "It’s either him or me.": "Albo on, albo ja.",
    "Andrea told him not to pursue you.": "Andrea zabroniła mu cię ścigać.",
    "The commissioner… Duncan has orders from her not to hunt you down.": "Pani komisarz… Duncan ma od niej rozkazy, by cię nie ścigać.",
    "The commissioner? She’s giving him orders?": "Pani komisarz? Ona wydaje mu rozkazy?",
    "Seems the cat’s out of the bag.": "Wygląda na to, że tajemnica wyszła na jaw.",
    "I’ve spent a long time now trying to get right with Duncan… You’re saying it’s over?": "Sporo czasu spędziłem, próbując dogadać się z Duncanem… Mówisz, że to koniec?",
    "Unless he goes behind Andrea’s back.": "Chyba że pójdzie za plecami Andrei.",
    "You know… He’d totally do that.": "Wiesz… On by to zrobił.",
    "Wait a minute… I’ve seen your face.": "Czekaj… Widziałem twoją twarz.",
    "I didn’t always look like this.": "Nie zawsze tak wyglądałem.",
    "You’re a cam girl.": "Jesteś cam girl.",
    "Hence why 1Hero and I fucked on camera.": "Dlatego ja i 1Hero pieprzyliśmy się na kamerze.",
    "Haha! 1Hero’s getting into the cam business. What a turn of events.": "Haha! 1Hero wchodzi w biznes cam. Co za zwrot akcji.",
    "I’m not getting into the cam business.": "Nie wchodzę w biznes cam.",
    "So he says.": "Tak mówi.",
    "I’m not!": "Nie wchodzę!",
    "That video was my highest-viewed video.": "Ten film był moim najczęściej oglądanym.",
    "Shit… I don’t have my phone on me…": "Cholera… Nie mam przy sobie telefonu…",
    "I do! What’s the link?": "Ja mam! Jaki link?",
    "Stop it! We need to get Ella out of here.": "Przestańcie! Musimy wydostać Ellę stąd.",
    "Bullshit! I know how to escape this place. I’ve been here many times before.": "Bzdura! Wiem, jak uciec z tego miejsca. Byłam tu wiele razy.",
    "Give me the link!": "Daj mi link!",
    "Give me your phone.": "Daj mi telefon.",
    "I’ll trust you… I’ll leave the mansion.": "Zaufam ci… Opuścę rezydencję.",
    "I wouldn’t let your guard down. Not until we’re finished.": "Nie opuszczałbym gardy. Dopóki nie skończymy.",
    "That could be a while.": "To może potrwać.",
    "Duncan has a hard time letting things go.": "Duncan ma problem z odpuszczaniem.",
    "This is crazy… Duncan took my money… and now he has the amulet… The dude can’t let anything go.": "To szalone… Duncan zabrał moje pieniądze… i teraz ma amulet… Gość nie potrafi niczego odpuścić.",
    "Andrea’s calling the shots. He’s going to have to give in to her demands.": "Andrea rządzi. Będzie musiał ugiąć się przed jej żądaniami.",
    "How are you going to escape?": "Jak uciekniesz?",
    "Through the bunker… Trust me. I know this place.": "Przez bunkier… Uwierz mi. Znam to miejsce.",
    "I’ll see you later, Ella.": "Do zobaczenia później, Ella.",
    "Careful on your way out.": "Uważaj, wychodząc.",
    "Don’t let me regret this.": "Nie pozwól mi tego żałować.",
    "What a nice girl. I sure do like her style.": "Co za miła dziewczyna. Lubię jej styl.",
    "Have we had enough fun?": "Mieliśmy dość zabawy?",
    "Let’s get to work, 1Hero…": "Do roboty, 1Hero…",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=159 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=47: raise SystemExit(f'Expected 47, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map159')
