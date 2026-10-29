#!/usr/bin/env python3
"""Build Polish drafts for Map 73 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map73-followups-01.jsonl'
TRANSLATIONS = {
    "Looks like this clock is powered by batteries. Maybe I could use them.": "Wygląda na to, że ten zegar jest zasilany bateriami. Może mógłbym je wykorzystać.",
    "Feel free to look around. I have a leak to deal with upstairs.": "Rozgość się. Mam przeciek do ogarnięcia na górze.",
    "Don’t worry, Father. We won’t disturb your belongings.": "Nie martw się, ojcze. Nie będziemy ruszać twoich rzeczy.",
    "It's locked.": "Zamknięte.",
    "Need help?": "Potrzebujesz pomocy?",
    "Keep an eye on the nun. I can handle this.": "Miej oko na zakonnicę. Ja się tym zajmę.",
    "Heather…": "Heather…",
    "1Hero?": "1Hero?",
    "I didn’t mean anything by what I said.": "Nie miałem nic złego na myśli w tym, co powiedziałem.",
    "Am I the only one being hurt by this?": "Czy tylko ja cierpię przez to?",
    "Do you feel hurt?": "Czy czujesz ból?",
    "I just… want you.": "Ja po prostu… pragnę cię.",
    "To yourself?": "Dla siebie?",
    "Oh, God. It’s so silly… You are like my time machine…": "O Boże. To takie głupie… Jesteś jak mój wehikuł czasu…",
    "When we fuck…": "Gdy się pieprzymy…",
    "Hey, 1Hero. Hello, Miss Wilson.": "Hej, 1Hero. Cześć, panno Wilson.",
    "Oh, uhhh… Hey, Father.": "Och, yyy… Hej, ojcze.",
    "I was just… Looking for the restroom.": "Tak tylko… Szukałem toalety.",
    "Oh! How rude of me. Let me unlock my bathroom…": "Och! Ale ze mnie niegrzeczny. Pozwól, że odblokuję łazienkę…",
    "I keep it locked so the parishioners don't wander into my medicine cabinet.": "Trzymam ją zamkniętą, żeby parafianie nie zaglądali do mojej apteczki.",
    "Oh, uhh… Thank you, Father.": "Och, yyy… Dziękuję, ojcze.",
    "Is everything okay, 1Hero? Our trip to the demon world certainly must have you frazzled.": "Wszystko w porządku, 1Hero? Wyprawa do demonicznego świata musiała cię wykończyć.",
    "You know… I feel okay.": "Wiesz… Czuję się dobrze.",
    "Careful, 1Hero. Those monsters will try to manipulate you.": "Uważaj, 1Hero. Te potwory spróbują tobą manipulować.",
    "Noted, Father… Are you still studying?": "Przyjęte, ojcze… Nadal się uczysz?",
    "I feel I’m close to figuring something out, but not sure…": "Czuję, że jestem blisko rozgryzienia czegoś, ale nie jestem pewien…",
    "Well… I better get back to it.": "Cóż… Lepiej wrócę do tego.",
    "What the hell is 1Hero doing in there?": "Co, do cholery, 1Hero robi w środku?",
    "What a nice restroom.": "Co za ładna toaleta.",
    "Oh, yes. I told you it was nice.": "Och, tak. Mówiłem, że jest ładna.",
    "And that concludes our tour.": "I to kończy naszą wycieczkę.",
    "Good golly! Smells like sex in there.": "O rany! Śmierdzi tam seksem.",
    "Hope I didn’t cut you rabbits short.": "Mam nadzieję, że nie przerwałem wam, króliczki.",
    "You caught us, Father.": "Przyłapałeś nas, ojcze.",
    "How about next time use Judy’s bedroom? Quite a bit more comfortable, I would think.": "Może następnym razem użyjcie sypialni Judy? Znacznie wygodniej, jak sądzę.",
    "You think the nun would mind some stains on the sheets?": "Myślisz, że zakonnica miałaby coś przeciwko plamom na prześcieradłach?",
    "Carol!... How embarrassing.": "Carol!... Ale wstyd.",
    "Don’t worry. Brian is cool.": "Nie martw się. Brian jest spoko.",
    "Like I tell 1Hero… It’s not fun unless you get caught from time to time.": "Jak mówię 1Hero… Zabawa jest dopiero wtedy, gdy czasem dacie się złapać.",
    "I wish I had your outlook on life, Carol.": "Chciałabym mieć twoje podejście do życia, Carol.",
    "You’ll get there. Just need to get 1Hero to fuck that stick out of your ass.": "Dojdziesz do tego. Musisz tylko pozwolić 1Hero wyruchać ten kij z twojej dupy.",
    "Uhh… I don’t think that’s how the saying goes.": "Yyy… Nie sądzę, że tak to przysłowie brzmi.",
    "Hey. Someone’s got to look out for us.": "Hej. Ktoś musi na nas uważać.",
    "Haha. A lot of good it did.": "Haha. Na wiele się to zdało.",
    "Come on. Let’s go chat.": "Chodźmy. Pogadajmy.",
    "Can I come?": "Mogę iść?",
    "1Hero! This is girl talk time.": "1Hero! Teraz czas na babskie pogaduchy.",
    "Well… What’s left to tease me about? I’ve done it all with you ladies… and your daughters.": "Cóż… Co jeszcze możecie ze mnie zadrwić? Robiłem już wszystko z wami babkami… i waszymi córkami.",
    "Don’t worry. I’m sure we can find lots of stuff to talk about.": "Nie martw się. Na pewno znajdziemy mnóstwo tematów.",
    "Hehe! Oh, Carol.": "Hehe! Och, Carol.",
    "You’re saying a police officer found Sister Judy and Kimberly near the rift?": "Mówisz, że policjant znalazł siostrę Judy i Kimberly przy Szczelinie?",
    "I sent him there… Bobby Rinaldi… He’s keeping them at the mansion.": "Wysłałem go tam… Bobby Rinaldi… Trzyma je w rezydencji.",
    "What about the demons? Did he see them?": "A co z demonami? Widział je?",
    "They are not with the girls. The girls are alone.": "Nie ma ich z dziewczynami. Dziewczyny są same.",
    "We have to get over there and save them.": "Musimy tam iść i je uratować.",
    "Hold on, Father… It might be a trap.": "Poczekaj, ojcze… To może być pułapka.",
    "You think Lilith is trying to lure the priest into a trap?": "Myślisz, że Lilith próbuje zwabić księdza w pułapkę?",
    "Isn’t it just too convenient?": "Czy to nie zbyt wygodne?",
    "Still awake?": "Jeszcze nie śpisz?",
    "We’ve found Sister Judy.": "Znaleźliśmy siostrę Judy.",
    "Huh? Where is she?": "Huh? Gdzie ona jest?",
    "At the mansion, alongside Kimberly Foxx.": "W rezydencji, wraz z Kimberly Foxx.",
    "We must save them!": "Musimy je uratować!",
    "I sense a trap… Lillian knows that Father Solomon would go after them.": "Wyczuwam pułapkę… Lillian wie, że ojciec Solomon poszedłby po nie.",
    "You can’t just leave them there.": "Nie możesz ich tam zostawić.",
    "Arianna and I will go get them and bring them back here… The crosses will protect them.": "Arianna i ja po nie pójdziemy i przyprowadzimy je tutaj… Krzyże je ochronią.",
    "Let's hurry before Lilith finds them.": "Pospieszmy się, zanim Lilith je znajdzie.",
    "Bobby said the portal closed. But we should hurry.": "Bobby powiedział, że portal się zamknął. Ale powinniśmy się pospieszyć.",
    "Same here. I can help.": "Ja też mogę pomóc.",
    "What about the cops? Will they let you in?": "A co z glinami? Wpuszczą cię?",
    "Bobby will let us in. He trusts me now.": "Bobby mnie wpuści. Teraz mi ufa.",
    "I just hope Sister Judy is okay… Lilith did a number on her.": "Mam tylko nadzieję, że siostra Judy jest cała… Lilith nieźle ją sponiewierała.",
    "I can bless them… I can undo the brainwashing Lilith has put upon them.": "Mogę je pobłogosławić… Mogę cofnąć pranie mózgu, które nałożyła na nie Lilith.",
    "Come on… new Madalyn. I’ll show you the way.": "Chodź… nowa Madalyn. Pokażę ci drogę.",
    "Bring them back safe.": "Przyprowadź je bezpiecznie.",
    "I’m going to talk to Bobby… He’ll let us search the mansion… He has to.": "Porozmawiam z Bobbym… Pozwoli nam przeszukać rezydencję… Musi.",
    "I don’t trust cops, but we need to be able to search that mansion.": "Nie ufam glinom, ale musimy mieć możliwość przeszukania rezydencji.",
    "Get a few hours of rest, Henry… I’ll try and do the same.": "Odpocznij kilka godzin, Henry… Ja spróbuję zrobić to samo.",
    "Diana and I can find those amulets… We’re built for this.": "Diana i ja możemy znaleźć te amulety… Jesteśmy do tego stworzeni.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=73 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=79: raise SystemExit(f'Expected 79, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map73')
