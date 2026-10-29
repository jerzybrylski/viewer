#!/usr/bin/env python3
"""Build Polish drafts for Map 5 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map5-followups-01.jsonl'
TRANSLATIONS = {
    "I see you found my lost wallet and car fob! Here’s a reward.": "Widzę, że znalazłeś mój zgubiony portfel i brelok! Oto nagroda.",
    "I see you found my car fob! But I’ve lost my wallet. Can you find it?": "Widzę, że znalazłeś mój brelok! Ale zgubiłem portfel. Możesz go znaleźć?",
    "I see you found my wallet! But I’ve lost my car fob. Can you find it?": "Widzę, że znalazłeś mój portfel! Ale zgubiłem brelok. Możesz go znaleźć?",
    "I’m so stupid! I had a hole in my pocket and I lost my wallet and my car fob.": "Jaki jestem głupi! Miałem dziurę w kieszeni i zgubiłem portfel i brelok.",
    "You were right. You’re a pretty good detective. Here’s a reward.": "Miałeś rację. Jesteś całkiem niezłym detektywem. Oto nagroda.",
    "Nice ride.": "Niezła bryka.",
    "Come work for Channel 4 and maybe you could join me.": "Chodź pracować dla Channel 4, może do mnie dołączysz.",
    "Not so fast, Miss Foxx. He’s needed elsewhere.": "Nie tak szybko, panno Foxx. Gdzie indziej jest potrzebny.",
    "Maybe I’ll see you tomorrow.": "Może zobaczymy się jutro.",
    "We’ll see, won’t we?": "Zobaczymy, prawda?",
    "Damn… Which way did they go?": "Cholera… W którą stronę poszli?",
    "They?": "Oni?",
    "She’s with a friend… Erica.": "Jest z przyjaciółką… Ericą.",
    "Where the hell would they be running off to?": "Gdzie, do diabła, mogły uciec?",
    "Shit… I hope she’s not going to the commissioner.": "Cholera… Mam nadzieję, że nie idzie do pani komisarz.",
    "Would she do that?": "Zrobiłaby to?",
    "She said she’d take this story to her if I didn’t let her report on it.": "Powiedziała, że doniesie jej tę historię, jeśli nie pozwolę jej jej opublikować.",
    "Shit… I hope that’s where she went.": "Cholera… Mam nadzieję, że właśnie tam poszła.",
    "Where is the commissioner?": "Gdzie jest pani komisarz?",
    "Either at her house or at the station.": "Albo w domu, albo na posterunku.",
    "Don’t worry… I’ll find her.": "Nie martw się… Znajdę ją.",
    "Hopefully you can talk some sense into her.": "Mam nadzieję, że przemówisz jej do rozsądku.",
    "Kimberly! Where the hell were you?": "Kimberly! Gdzie, do diabła, byłaś?",
    "More like, where in Hell was I?": "Raczej: gdzie w piekle byłam?",
    "Don’t worry about it, Paul.": "Nie martw się, Paul.",
    "Thank you for finding her. It’s not like her to disappear like that.": "Dzięki, że ją znalazłeś. To do niej niepodobne, żeby tak znikać.",
    "She was at the mansion, Paul.": "Była w rezydencji, Paul.",
    "Heh… Oops. I guess we got caught again.": "Heh… Ups. Chyba znowu nas przyłapano.",
    "Can you keep her away? It’s not safe there.": "Możesz trzymać ją z daleka? To tam niebezpiecznie.",
    "You know how she is when she wants a story.": "Wiesz, jaka jest, gdy chce dorwać historię.",
    "It’s trespassing now. The state owns the mansion.": "To już wtargnięcie. Rezydencja należy do stanu.",
    "I’ll keep my eye on her.": "Będę miał na nią oko.",
    "You really believe all this, don’t you?": "Naprawdę wierzysz w to wszystko, prawda?",
    "Melissa… If you could see what I saw, you’d understand.": "Melissa… Gdybyś widziała, co ja widziałem, zrozumiałabyś.",
    "I’m tempted to try.": "Kusi mnie, żeby spróbować.",
    "Andrea would not be happy about that… Duncan’s goons are all over that place.": "Andrea nie byłaby z tego zadowolona… Ludzie Duncana obstawiają to miejsce.",
    "What did you learn?": "Czego się dowiedziałeś?",
    "Duncan met with me… He wants me to keep tabs on Andrea… and Andrea is having Nellie keep tabs on Duncan…": "Duncan spotkał się ze mną… Chce, żebym miał oko na Andreę… a Andrea kazała Nellie mieć oko na Duncana…",
    "Andrea is letting Duncan continue the Guild.": "Andrea pozwala Duncanowi kontynuować Gildię.",
    "Good God… Why would she do this?": "Na Boga… Dlaczego miałaby to robić?",
    "It’s now a honeypot operation.": "To teraz operacja wabika.",
    "And you’re in the middle of it.": "I jesteś w środku tego.",
    "Smack dab in the middle.": "W samym środku.",
    "Don’t keep me in the dark. I want to help you with this.": "Nie trzymaj mnie w niepewności. Chcę ci pomóc w tej sprawie.",
    "Expect a lot more cases to come our way.": "Spodziewaj się, że spadnie na nas znacznie więcej spraw.",
    "The girls are gone.": "Dziewczyny zniknęły.",
    "We can’t find Kimberly anywhere.": "Nie możemy nigdzie znaleźć Kimberly.",
    "I thought this place had security.": "Myślałem, że to miejsce ma ochronę.",
    "I saw nothing! I was watching like a hawk.": "Nic nie widziałem! Obserwowałem jak jastrząb.",
    "How long have they been missing?": "Jak długo ich nie ma?",
    "We just noticed.": "Dopiero zauważyliśmy.",
    "She’s in the mansion.": "Jest w rezydencji.",
    "Trust me. I’m positive she’s there.": "Zaufaj mi. Jestem pewien, że tam jest.",
    "We have to go get her!": "Musimy po nią iść!",
    "No! Stay here. You can’t go to the mansion.": "Nie! Zostańcie tutaj. Nie możecie iść do rezydencji.",
    "If she’s there, we have to help her.": "Jeśli tam jest, musimy jej pomóc.",
    "You can’t do anything… Leave this to me.": "Nic nie możecie zrobić… Zostawcie to mnie.",
    "Leave it to you? If she’s been kidnapped, we need cops!": "Zostawić tobie? Jeśli została porwana, potrzebujemy policji!",
    "Calm down… We’ll talk with the commissioner ourselves…": "Spokojnie… Porozmawiamy z panią komisarz sami…",
    "The mansion is off limits to everyone.": "Wstęp do rezydencji jest wzbroniony dla wszystkich.",
    "Yeah, yeah. I get it.": "Tak, tak. Rozumiem.",
    "She better be safe.": "Lepiej, żeby była bezpieczna.",
    "I’ll go get her.": "Pójdę po nią.",
    "What the hell are we supposed to do now?": "Co my mamy teraz, do cholery, robić?",
    "Give me a few hours… I know where to find her.": "Daj mi kilka godzin… Wiem, gdzie ją znaleźć.",
    "She’s not mentally healthy… You better know what you’re doing.": "Ona jest niestabilna psychicznie… Lepiej wiedz, co robisz.",
    "Come on. Let’s take a look at the security footage again.": "Chodź. Spójrzmy jeszcze raz na nagranie z monitoringu.",
    "Lillian is going to implant my cum inside of Erica… It’s a ritual that will complete the Toma Leolo... A dangerous magic idol.": "Lillian zamierza wszczepić moją spermę do Erici… To rytuał, który dopełni Toma Leolo... Niebezpiecznego magicznego idola.",
    "Ritual? Toma Leolo? Slow down… what are you talking about?": "Rytuał? Toma Leolo? Zwolnij… o czym ty mówisz?",
    "Melissa, this is going to sound crazy, but there is an artifact called the Toma Leolo that can bring damned souls back from Hell.": "Melissa, to zabrzmi szaleńczo, ale istnieje artefakt zwany Toma Leolo, który może przywrócić potępione dusze z piekła.",
    "And by putting my cum inside of Erica’s pussy, a ritual will be completed that will unleash demons into our world.": "A umieszczając moją spermę w cipce Erici, rytuał zostanie dopełniony i uwolni demony na nasz świat.",
    "That’s a lot to take in, 1Hero.": "Sporo do przetrawienia, 1Hero.",
    "Let’s suppose this is true… Erica’s been kidnapped against her will. We should tell Andrea.": "Załóżmy, że to prawda… Erica została porwana wbrew woli. Powinniśmy powiedzieć Andrei.",
    "I need Brian’s help.": "Potrzebuję pomocy Briana.",
    "The priest?": "Księdza?",
    "We’re dealing with demons… He can handle them.": "Mamy do czynienia z demonami… On sobie z nimi poradzi.",
    "I want to go with you.": "Chcę iść z tobą.",
    "Go to the church. I’ll meet you there.": "Idź do kościoła. Spotkamy się tam.",
    "What about Andrea?": "A co z Andreą?",
    "She won't help us. We’re on our own.": "Ona nam nie pomoże. Jesteśmy zdani na siebie.",
    "See you at the church, 1Hero.": "Do zobaczenia w kościele, 1Hero.",
    "I haven’t seen anything suspicious yet.": "Nie widziałem jeszcze nic podejrzanego.",
    "Ella!": "Ella!",
    "1Hero?": "1Hero?",
    "It’s Judy! I need to speak to Father Solomon.": "To Judy! Muszę porozmawiać z ojcem Solomonem.",
    "He should be in the studio.": "Powinien być w studiu.",
    "No sign of Kimberly or her goon posse.": "Ani śladu Kimberly czy jej zbirów.",
    "If you’re looking for Father Solomon, he’s in the studio.": "Jeśli szukasz ojca Solomona, jest w studiu.",
    "So far, nothing to report.": "Jak dotąd nic do zgłoszenia.",
    "Don’t involve the cops, 1Hero.": "Nie mieszaj w to policji, 1Hero.",
    "I’m here for the interview. What’s all this commotion?": "Przyszedłem na wywiad. O co tyle zamieszania?",
    "The interview isn’t happening.": "Wywiad się nie odbędzie.",
    "Thank God you don’t know.": "Dzięki Bogu, że nie wiesz.",
    "Fuck me, detective! I’m your biggest fan!": "Pieprz mnie, detektywie! Jestem twoją największą fanką!",
    "Will you autograph my boobs?": "Podpiszesz moje cycki?",
    "I’m horny! I need your cock!": "Jestem napalona! Potrzebuję twojego kutasa!",
    "Eat my pussy, Detective Canmore!": "Liż moją cipkę, Detektywie Canmore!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=5 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=97: raise SystemExit(f'Expected 97, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map5')
