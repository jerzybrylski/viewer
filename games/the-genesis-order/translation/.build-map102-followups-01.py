#!/usr/bin/env python3
"""Build Polish drafts for Map 102 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map102-followups-01.jsonl'
TRANSLATIONS = {
    "Damn. This wall isn’t coming down.": "Cholera. Ta ściana nie chce runąć.",
    "Looks like you made some progress.": "Wygląda na to, że poczyniłeś postępy.",
    "Do it again.": "Zrób to jeszcze raz.",
    "I broke the chisel.": "Złamałem dłuto.",
    "Well, use another one.": "Cóż, użyj innego.",
    "Maybe if I had a chisel I could break these rocks loose.": "Może gdybym miał dłuto, mógłbym poluzować te skały.",
    "It moved!": "Ruszyło się!",
    "Everyone okay?": "Wszystkim nic się nie stało?",
    "Wait… This isn’t a room. This is a cave.": "Czekaj… To nie pokój. To jaskinia.",
    "I always knew there was a cave system in Casula Forest, but I’ve never seen it.": "Zawsze wiedziałam, że w Lesie Casula jest system jaskiń, ale nigdy go nie widziałam.",
    "I wonder where it goes.": "Ciekawe, dokąd prowadzi.",
    "Careful. We’re not equipped for this.": "Ostrożnie. Nie jesteśmy na to przygotowani.",
    "I just want to peek.": "Chcę tylko zerknąć.",
    "Wait.": "Czekaj.",
    "Looks like an old storage room.": "Wygląda jak stary magazyn.",
    "Maybe there are some clues down here.": "Może na dole są jakieś wskazówki.",
    "Judging from the cobwebs, it doesn’t look like this place has been used in a long, long time.": "Sądząc po pajęczynach, to miejsce nie było używane od bardzo, bardzo dawna.",
    "Do you feel that?": "Czujesz to?",
    "There’s a breeze coming from this wall.": "Od tej ściany wieje.",
    "There’s another room on the other side.": "Po drugiej stronie jest kolejny pokój.",
    "That’s what I thought…": "Tak właśnie myślałam…",
    "This place has a basement.": "To miejsce ma piwnicę.",
    "Father, please do be careful.": "Ojcze, proszę, bądź ostrożny.",
    "Why was this place hidden?": "Czemu to miejsce było ukryte?",
    "This is a small basement… Maybe it was meant as a storm shelter.": "To mała piwnica… Może miała służyć jako schron przeciwburzowy.",
    "It’s bigger than it looks. This wall is covering another room.": "Jest większa, niż wygląda. Ta ściana zasłania kolejny pokój.",
    "Can you break through?": "Możesz się przebić?",
    "It’s just a matter of breaking up the stone…": "Kwestia rozbicia kamienia…",
    "Let me see if I can break it open.": "Zobaczę, czy dam radę to otworzyć.",
    "Give it a go, 1Hero.": "Spróbuj, 1Hero.",
    "Why would someone cover up a perfectly good room?...": "Czemu ktoś miałby zakrywać całkiem dobry pokój?...",
    "Makes me nervous to see what we’ll find.": "Robię się nerwowa na myśl o tym, co znajdziemy.",
    "Can you get through this wall or not?": "Dasz radę przebić się przez tę ścianę, czy nie?",
    "Give me a minute. I’ll figure it out.": "Daj mi chwilę. Rozgryzę to.",
    "She’s not lying.": "Ona nie kłamie.",
    "I’m done with you, 1Hero.": "Mam cię dość, 1Hero.",
    "You’re not a gift from God. You’re a cocky asshole.": "Nie jesteś darem od Boga. Jesteś zarozumiałym dupkiem.",
    "We found the Guild’s bunker! You should be thrilled!": "Znaleźliśmy bunkier Gildii! Powinieneś się cieszyć!",
    "If that redhead is not lying, then you’ve just led us into the middle of the commissioner’s undercover operation…": "Jeśli ta ruda nie kłamie, to właśnie wprowadziłeś nas w sam środek tajnej operacji pani komisarz…",
    "This is what happens when you go over my head.": "Tak to się kończy, gdy działasz za moimi plecami.",
    "Then we don’t say anything.": "Więc nic nie mówimy.",
    "Do you really think that’s an option?": "Naprawdę myślisz, że to opcja?",
    "Hey! We’re not finished!": "Hej! Nie skończyliśmy!",
    "Did you open it?": "Otworzyłeś to?",
    "1Hero! Carol found a key!": "1Hero! Carol znalazła klucz!",
    "Maybe it’s for this locked box.": "Może jest do tego zamkniętego pudła.",
    "It’s broken.": "Zepsute.",
    "Well, shucks. Anything else nifty down here?": "Cóż, szkoda. Coś jeszcze ciekawego na dole?",
    "Looks like a bunch of old stuff to me.": "Wygląda jak sterta starych gratów.",
    "Be careful. This opens up into to the cave system. If you go farther, you’ll get lost.": "Uważaj. To otwiera się na system jaskiń. Jeśli pójdziesz dalej, zgubisz się.",
    "We’re being careful.": "Będziemy ostrożni.",
    "Yeah. I don’t want to go into the caves. That sounds scary.": "Tak. Nie chcę iść do jaskiń. To brzmi strasznie.",
    "This place just needs a little renovation, that’s all.": "To miejsce potrzebuje tylko małego remontu, to wszystko.",
    "I sure am glad you busted those thieves. I suppose Sister Judy will be staying in her bedroom again.": "Tak się cieszę, że dorwałeś tych złodziei. Chyba siostra Judy znów będzie spać w swojej sypialni.",
    "Carol, is that you down there?": "Carol, to ty tam na dole?",
    "Oh, shit! It’s Mom!": "O cholera! To mama!",
    "Carol!?": "Carol!?",
    "Well, this is awkward.": "Cóż, to niezręczne.",
    "The three of you…?": "Wy troje…?",
    "Sorry, Heather. But we just got carried away after finding a secret porn stash.": "Przepraszam, Heather. Ale po prostu poniosło nas po znalezieniu sekretnego schowka porno.",
    "You found porn?": "Znaleźliście porno?",
    "Yeah… Want to see it?": "Tak… Chcesz zobaczyć?",
    "Chloe was okay with you two… fucking?": "Chloe nie przeszkadzało, że wy dwoje… pieprzycie się?",
    "Hell, yeah. It was a wild time.": "Oczywiście, że nie. To była szalona zabawa.",
    "I should go.": "Powinnam iść.",
    "Judy and I were looking for a bandage… Hannah scraped herself.": "Judy i ja szukałyśmy bandaża… Hannah się zadrapała.",
    "Hannah asked for a bandage? That doesn’t sound like her.": "Hannah prosi o bandaż? To do niej niepodobne.",
    "I insisted.": "Nalegałam.",
    "Always the caring mother.": "Zawsze troskliwa matka.",
    "I should get back.": "Powinnam wracać.",
    "It wouldn’t be fun if you never got caught.": "Nie byłoby zabawy, gdyby nigdy cię nie przyłapano.",
    "I’m glad you’re having fun still.": "Cieszę się, że wciąż się dobrze bawisz.",
    "Relax, 1Hero. Everything will be fine.": "Spokojnie, 1Hero. Wszystko będzie dobrze.",
    "The ground looks weak here. If I had a pickaxe, I could break it open.": "Ziemia wygląda tu słabo. Gdybym miał kilof, mógłbym ją rozbić.",
    "Arianna!": "Arianna!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=102 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=75: raise SystemExit(f'Expected 75, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map102')
