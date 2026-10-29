#!/usr/bin/env python3
"""Build Polish drafts for Map 140 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map140-followups-01.jsonl'
TRANSLATIONS = {
    "Oh, shit. It’s really muddy.": "O cholera. Tu jest naprawdę błotniście.",
    "Gross… Can we walk around it?": "Obrzydliwe… Możemy to obejść?",
    "I ain’t afraid of a little mud.": "Nie boję się odrobiny błota.",
    "It’s dry over here…": "Tu jest sucho…",
    "Ahhh!!!": "Aaaa!!!",
    "Oh my God! A gator!": "O mój Boże! Aligator!",
    "What the hell? They are this far north?": "Co jest, do cholery? One zapuszczają się tak daleko na północ?",
    "Damn. That was a close call.": "Cholera. Było blisko.",
    "We can’t stop now! Let’s keep going!": "Nie możemy teraz przestać! Chodźmy dalej!",
    "No way! I’m not getting eaten by an alligator.": "Nie ma mowy! Nie dam się zeżreć aligatorowi.",
    "Well… I could shoot it.": "Cóż… Mógłbym go zastrzelić.",
    "No! Don’t do that!": "Nie! Nie rób tego!",
    "Let’s run for it. I bet it can’t chase us.": "Uciekajmy. Założę się, że nie może nas gonić.",
    "Ha! An alligator could outrun all of us.": "Ha! Aligator prześcignąłby nas wszystkich.",
    "I know my animals.": "Znam się na zwierzętach.",
    "She’s probably right.": "Pewnie ma rację.",
    "I guess we should turn back.": "Chyba powinniśmy zawrócić.",
    "No! We can keep going, we just need to shock the water.": "Nie! Możemy iść dalej, wystarczy porazić wodę prądem.",
    "Whenever I go to uncle's alligator farm, he uses an electric charge to scare them away from the dock.": "Gdy chodzę na farmę aligatorów wujka, używa ładunku elektrycznego, by odstraszyć je od pomostu.",
    "How are we supposed to do that? It sounds dangerous.": "Jak mamy to zrobić? Brzmi niebezpiecznie.",
    "1Hero can figure it out!": "1Hero to rozgryzie!",
    "Until then, I guess we should stay back.": "Do tego czasu chyba powinniśmy trzymać się z tyłu.",
    "I agree.": "Zgadzam się.",
    "You’re all scaredy cats!": "Jesteście cykorami!",
    "This is as far as we go, Hannah.": "Tu kończy się nasza trasa, Hannah.",
    "I’d rather see an alligator than one of those Guild goons.": "Wolę zobaczyć aligatora niż jednego z tych zbirów z Gildii.",
    "I ain’t afraid of no gator.": "Nie boję się żadnego aligatora.",
    "I hope Mom isn’t bothering Sister Judy too much.": "Mam nadzieję, że mama za bardzo nie zawraca głowy siostrze Judy.",
    "Maybe if I shock the water, the gator will leave.": "Może jeśli porażę wodę, aligator sobie pójdzie.",
    "Holy shit! She was right!": "Jasna cholera! Miała rację!",
    "Will it stay away?": "Zostanie z daleka?",
    "He’s terrified of us now. We’re in the clear…": "Teraz boi się nas jak ognia. Mamy wolną drogę…",
    "Hey… What’s this?": "Hej… Co to jest?",
    "Is something supposed to happen?": "Czy coś ma się stać?",
    "Is it broken?": "Zepsute?",
    "Maybe it’s not what you think it is.": "Może to nie to, co myślisz.",
    "You people are crazy.": "Jesteście szaleni.",
    "Nevermind, I guess.": "Nieważne, chyba.",
    "Damn. I thought we were gonna have some more fun.": "Cholera. Myślałem, że będzie więcej zabawy.",
    "We didn’t get very far.": "Nie zaszliśmy za daleko.",
    "I’m bored! Let’s play soccer!": "Nudzi mi się! Zagrajmy w piłkę nożną!",
    "I think we should play to shut her up.": "Myślę, że powinniśmy grać, by ją uciszyć.",
    "Fine… We’ll do what Hannah wants to do… again!": "Dobra… Zrobimy to, czego chce Hannah… znowu!",
    "That’s really strange. I expected something to happen.": "To naprawdę dziwne. Spodziewałem się, że coś się stanie.",
    "I can see him over there! Do you see it?": "Widzę go tam! Widzicie go?",
    "Don’t even think about it, Hannah.": "Nawet o tym nie myśl, Hannah.",
    "I hope that big alligator stays way over there.": "Mam nadzieję, że ten wielki aligator zostanie tam, gdzie jest.",
    "Hannah!?": "Hannah!?",
    "Heather… Where is Hannah?": "Heather… Gdzie jest Hannah?",
    "She was here earlier.": "Była tu wcześniej.",
    "Where’s the alligator?": "Gdzie jest aligator?",
    "Oh, my… I don’t see it.": "Ojej… Nie widzę go.",
    "You don’t think…": "Chyba nie…",
    "I bet Hannah went chasing after it.": "Założę się, że Hannah pognała za nim.",
    "Shit… Why did I leave her alone?": "Cholera… Czemu zostawiłem ją samą?",
    "I’ll go find her.": "Pójdę ją znaleźć.",
    "But… You’ll get wet.": "Ale… Zmoczysz się.",
    "The water isn’t that deep… I have a solution.": "Woda nie jest taka głęboka… Mam rozwiązanie.",
    "Heh. That’s one way to solve the problem.": "Heh. To jeden ze sposobów rozwiązania problemu.",
    "You’ll get your shorts wet.": "Zamoczysz szorty.",
    "They’ll dry.": "Wyschną.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=140 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=61: raise SystemExit(f'Expected 61, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map140')
