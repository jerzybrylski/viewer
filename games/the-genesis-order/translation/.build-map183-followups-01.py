#!/usr/bin/env python3
"""Build Polish drafts for Map 183 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map183-followups-01.jsonl'
TRANSLATIONS = {
    "Look who came to rescue us.": "Patrzcie, kto przyszedł nas ratować.",
    "1Hero, you’re here!": "1Hero, jesteś!",
    "What the hell do you ladies think you’re doing?": "Co wy, dziewczyny, do cholery wyprawiacie?",
    "Where are the demons?": "Gdzie są demony?",
    "A new haircut?": "Nowa fryzura?",
    "It’s not who you think it is.": "To nie ten, za kogo go uważasz.",
    "I’m Arianna.": "Jestem Arianna.",
    "They left you here? Is the rift really closed?": "Zostawili was tutaj? Czy Szczelina naprawdę jest zamknięta?",
    "The hero has arrived.": "Bohater przybył.",
    "Lilith!": "Lilith!",
    "Erica?": "Erica?",
    "That’s not Erica.": "To nie Erica.",
    "I know how to save Erica.": "Wiem, jak uratować Ericę.",
    "You are a lying demon! Erica’s soul is surely in the Empyrean.": "Jesteś kłamliwym demonem! Dusza Erici z pewnością jest w Empyreum.",
    "In Limbo.": "W Otchłani.",
    "She’s not going to hang around Limbo. Souls don’t linger there.": "Nie zostanie w Otchłani. Dusze tam nie zalegają.",
    "She was not supposed to look at the Toma.": "Nie powinna była patrzeć na Tomę.",
    "Then why did you give it to Kimberly to show everyone?": "To czemu dałaś ją Kimberly, by pokazała ją wszystkim?",
    "That’s not what happened!": "To nie tak było!",
    "Erica was not given a choice!": "Erica nie miała wyboru!",
    "You should have thought about that before you put the Toma back together.": "Powinnaś była pomyśleć o tym, zanim złożyłaś Tomę z powrotem.",
    "Erica’s soul must go to Hell.": "Dusza Erici musi trafić do piekła.",
    "Just how naughty was she?": "Jak bardzo była niegrzeczna?",
    "She won’t go to Hell. What are you talking about?": "Nie trafi do piekła. O czym ty mówisz?",
    "This body… It can be given back to Erica, but it must be on my turf.": "To ciało… Można je oddać Erice, ale musi to być na moim terenie.",
    "You mean… Her soul can go back into her body?": "Masz na myśli… Jej dusza może wrócić do ciała?",
    "The rift will allow this body to enter Hell… I can give it to her, but I need Madalyn’s body back.": "Szczelina pozwoli temu ciału wejść do piekła… Mogę je jej oddać, ale potrzebuję ciała Madalyn z powrotem.",
    "You’re trying to trick us.": "Próbujesz nas oszukać.",
    "Would you rather I keep Erica’s body?": "Wolisz, żebym zatrzymała ciało Erici?",
    "How do we make Erica go to Hell?": "Jak sprawić, by Erica trafiła do piekła?",
    "Through blasphemy.": "Przez bluźnierstwo.",
    "You’re insane.": "Jesteś szalona.",
    "You’re blind.": "Jesteś ślepy.",
    "How does Erica commit blasphemy if she’s already dead?": "Jak Erica ma dopuścić się bluźnierstwa, jeśli już nie żyje?",
    "She must use a holy relic as a sex toy.": "Musi użyć świętej relikwii jako zabawki erotycznej.",
    "That’s a sin against God! An unforgivable sin!": "To grzech przeciwko Bogu! Grzech niewybaczalny!",
    "That’s the point!": "O to chodzi!",
    "You would damn her to Hell just to bring her back to Earth? I will not be a part of this.": "Potępiłabyś ją do piekła tylko po to, by sprowadzić ją z powrotem na ziemię? Nie wezmę w tym udziału.",
    "How do we do it?": "Jak to zrobimy?",
    "1Hero!?": "1Hero!?",
    "The angel must do it. She has access to Limbo.": "Anioł musi to zrobić. Ma dostęp do Otchłani.",
    "This is a bad idea.": "To zły pomysł.",
    "I’m probably Hell-bound. Could you kill me?": "Pewnie i tak trafiłam do piekła. Mógłbyś mnie zabić?",
    "An interesting idea.": "Ciekawy pomysł.",
    "You would never find her. Limbo is many times bigger than your world…": "Nigdy byś jej nie znalazł. Otchłań jest wielokrotnie większa od waszego świata…",
    "The angel must do it.": "Anioł musi to zrobić.",
    "I will not!": "Nie zrobię tego!",
    "Arianna… Erica isn’t supposed to be dead… How is that God’s will?": "Arianna… Erica nie powinna nie żyć… Jak to jest wolą Boga?",
    "You don’t understand.": "Nie rozumiesz.",
    "As if you do?": "Jakbyś ty rozumiała?",
    "This is my fault… I should have been more careful.": "To moja wina… Powinnam była bardziej uważać.",
    "What have we done?": "Co myśmy zrobili?",
    "This is not your fault! The only one to blame is the fucking God who set this into motion!": "To nie wasza wina! Winny jest tylko pieprzony Bóg, który to wprawił w ruch!",
    "I will help… But I will not tell Erica to sin against God.": "Pomogę… Ale nie każę Erice grzeszyć przeciwko Bogu.",
    "Erica deserves to live. Tell her what to do and I’ll save her when she enters Hell.": "Erica zasługuje na życie. Powiedz jej, co ma zrobić, a ja ją uratuję, gdy wejdzie do piekła.",
    "Arianna?": "Arianna?",
    "I will try… But I will not risk falling from grace… I do not want to become a demon.": "Spróbuję… Ale nie zaryzykuję upadku z łaski… Nie chcę stać się demonem.",
    "Now give me back my body and Erica’s will be yours to hold safe.": "Teraz oddaj mi moje ciało, a ciało Erici będzie twoje, byś je strzegł.",
    "Any funny business and I’ll cut your head off.": "Jakiekolwiek wałki, a utnę ci głowę.",
    "Erica’s head?": "Głowę Erici?",
    "I say we trust her.": "Mówię, że jej ufam.",
    "Give me Erica’s body first.": "Najpierw oddaj mi ciało Erici.",
    "Absolutely.": "Oczywiście.",
    "Shit! What did I miss?": "Cholera! Co przegapiłem?",
    "Don’t let the angel fail us… Don’t let her value herself over Erica.": "Nie pozwól, by anioł nas zawiódł… Nie pozwól, by ceniła siebie bardziej niż Ericę.",
    "Arianna, are you okay?": "Arianna, wszystko w porządku?",
    "I… I came so close.": "Ja… Byłam tak blisko.",
    "You resisted!": "Oparłaś się!",
    "Too bad. You could have had a lot of fun.": "Szkoda. Mogłaś się świetnie bawić.",
    "Hey… Where are my clothes?": "Hej… Gdzie moje ubrania?",
    "That was wild… Check the ceiling.": "To było szalone… Sprawdź sufit.",
    "I don’t see them anywhere.": "Nigdzie ich nie widzę.",
    "My phone is with my clothes!": "Mój telefon jest przy ubraniach!",
    "You kids and your phones.": "Wy, dzieciaki, i wasze telefony.",
    "My phone is linked to my Lustagram account!": "Mój telefon jest połączony z moim kontem Lustagram!",
    "Fuck… You don’t think…": "Cholera… Chyba nie…",
    "She’s going to post the Toma to Lustagram.": "Zamierza wrzucić Tomę na Lustagram.",
    "Shit! We’re running out of time. We need to find the amulets.": "Cholera! Kończy nam się czas. Musimy znaleźć amulety.",
    "But… The relic…": "Ale… Relikwia…",
    "We better not piss off the demon if we expect her to save Erica’s soul.": "Lepiej nie wkurzać demona, jeśli liczymy, że uratuje duszę Erici.",
    "We’ll find a holy relic and the amulets… Let’s work fast.": "Znajdziemy świętą relikwię i amulety… Działajmy szybko.",
    "Are you all fighting in here?": "Wy się tu kłócicie?",
    "Why’s the pink one naked?": "Czemu ta różowa jest naga?",
    "There must be something to wear around here.": "Gdzieś tu muszą być jakieś ciuchy.",
    "Bobby… We need to talk.": "Bobby… Musimy porozmawiać.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=183 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=85: raise SystemExit(f'Expected 85, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map183')
