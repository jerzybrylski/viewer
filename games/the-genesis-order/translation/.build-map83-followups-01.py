#!/usr/bin/env python3
"""Build Polish drafts for Map 83 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map83-followups-01.jsonl'
TRANSLATIONS = {
    "If it isn’t the man of the hour.": "Jeśli to nie człowiek godziny.",
    "1Hero, that’s what you’re wearing in the interview?": "1Hero, w tym chcesz wystąpić w wywiadzie?",
    "No worries. We’ll get him changed up.": "Bez obaw. Przebierzemy go.",
    "Make sure lighting fixed the blow out.": "Upewnij się, że oświetlenie naprawiło prześwietlenie.",
    "No more blaming it on the camera man.": "Koniec z zwalaniem na kamerzystę.",
    "Sorry. Busy morning.": "Przepraszam. Zajęty poranek.",
    "Detective Canmore, what can I call you? Mr. Canmore?": "Detektywie Canmore, jak mam się do pana zwracać? Panie Canmore?",
    "1Hero is fine.": "1Hero wystarczy.",
    "Hi, 1Hero. I’m Paul. I’m the producer of Kimberly’s show.": "Cześć, 1Hero. Jestem Paul. Jestem producentem programu Kimberly.",
    "Let’s get you to the changing rooms.": "Zaprowadźmy cię do garderoby.",
    "Bring the commissioner to the studio.": "Przyprowadźcie panią komisarz do studia.",
    "Clean him up nice, Paul.": "Doprowadź go do porządku, Paul.",
    "We always do, Commish.": "Zawsze, pani komisarz.",
    "Come on. We’re crunched for time.": "Chodź. Goni nas czas.",
    "I’ve put all your junk in this box and now you have to take your stuff and leave.": "Wpakowałem wszystkie twoje graty do tego pudła i teraz musisz zabrać swoje rzeczy i wyjść.",
    "Are you firing me?!": "Wyrzucasz mnie!?",
    "Sorry. But, that’s life.": "Przepraszam. Ale takie jest życie.",
    "Welcome back, 1Hero.": "Witaj ponownie, 1Hero.",
    "I wanted to get here early. I need to change.": "Chciałem przyjść wcześniej. Muszę się przebrać.",
    "We got you covered. Kimberly wants to meet with you now.": "Mamy wszystko gotowe. Kimberly chce się teraz z tobą spotkać.",
    "Don’t worry, 1Hero. She’s got something to show you. Head down the hall. I’ll see you on set.": "Bez obaw, 1Hero. Ma ci coś do pokazania. Idź korytarzem. Zobaczymy się na planie.",
    "Hey! What gives!?": "Hej! O co chodzi!?",
    "Sorry, 1Hero. But someone had to break this story.": "Przepraszam, 1Hero. Ale ktoś musiał nagłośnić tę historię.",
    "I thought we were partners.": "Myślałem, że byliśmy partnerami.",
    "Are you kidding me? You’ve given me plenty of content to work with.": "Żartujesz? Dostarczyłaś mi mnóstwo materiału.",
    "And this is how you treat me?": "I tak mnie traktujesz?",
    "I’m making you a star. People will love it.": "Robię z ciebie gwiazdę. Ludzie to pokochają.",
    "I lost my job.": "Straciłem pracę.",
    "Sorry to hear that, but you should be here with me.": "Współczuję, ale powinieneś być tu ze mną.",
    "You want me working at Channel 4?": "Chcesz, żebym pracował w Channel 4?",
    "Paul wants it too. You’re a natural for this work.": "Paul też tego chce. Masz naturalny talent do tej roboty.",
    "I’m a detective, Kimberly.": "Jestem detektywem, Kimberly.",
    "Not anymore, it sounds like.": "Podobno już nie.",
    "Calm down, 1Hero. I’m only teasing you.": "Spokojnie, 1Hero. Tylko cię drażnię.",
    "That job meant the world to me!": "Ta praca znaczyła dla mnie wszystko!",
    "I’m sorry… I didn’t realize…": "Przepraszam… Nie zdawałam sobie sprawy…",
    "But the offer stands. You’ll make a lot more money here.": "Ale oferta nadal stoi. Zarobisz tu znacznie więcej.",
    "I… I can’t. I’ve got something else going on.": "Ja… Ja nie mogę. Mam coś innego na głowie.",
    "Really? Private detective work?": "Naprawdę? Prywatne śledztwo?",
    "Any details you care to share?": "Chcesz zdradzić jakieś szczegóły?",
    "See ya around, Kimberly.": "Do zobaczenia, Kimberly.",
    "Do you still want updates about our audio transmitters?": "Nadal chcesz aktualizacje o naszych nadajnikach audio?",
    "… I want to stay in the loop.": "… Chcę być na bieżąco.",
    "You’re still on the case, aren’t you?": "Nadal prowadzisz sprawę, prawda?",
    "Goodbye, Kimberly.": "Do widzenia, Kimberly.",
    "1Hero? Where is Melissa?": "1Hero? Gdzie jest Melissa?",
    "She must still be interrogating one of Duncan’s goons.": "Pewnie wciąż przesłuchuje któregoś z ludzi Duncana.",
    "I hope she hurries up. We want to air the segment tonight and a live interview will do wonders for ratings.": "Mam nadzieję, że się pospieszy. Chcemy wyemitować segment dziś wieczorem, a wywiad na żywo świetnie podbije oglądalność.",
    "This is the big story.": "To wielka sprawa.",
    "It’s the start of something even bigger. You know that.": "To początek czegoś jeszcze większego. Wiesz o tym.",
    "Don’t be so quick to trust Lillian.": "Nie ufaj tak szybko Lillian.",
    "Why wouldn’t I?": "Czemu miałabym nie ufać?",
    "Are you kidding me? She’s up to something.": "Żartujesz? Coś kombinuje.",
    "She seems nice to me. Plus, I get access to the story of the century.": "Wydaje mi się miła. Poza tym mam dostęp do historii stulecia.",
    "Go change, 1Hero. I’ll meet you on set.": "Idź się przebierz, 1Hero. Spotkamy się na planie.",
    "I better be careful about how this plays out. I need to paint us as heroes to save our jobs, but I don’t want to piss off Andrea.": "Lepiej uważam, jak to rozegrać. Muszę przedstawić nas jako bohaterów, by ratować posady, ale nie chcę wkurzyć Andrei.",
    "Good job, 1Hero. We’ll air the segment Sunday night.": "Dobra robota, 1Hero. Wyemitujemy segment w niedzielny wieczór.",
    "People are going to love the heist angle.": "Ludzie pokochają wątek napadu.",
    "So you’re not going to snoop around the mansion anymore?": "Więc nie będziesz już szperać wokół rezydencji?",
    "As long as we have you.": "Dopóki mamy ciebie.",
    "I’m looking for Kimberly. I need to get something back from her.": "Szukam Kimberly. Muszę coś od niej odzyskać.",
    "Kimberly’s gone crazy. She’s going on and on about demons and Hell. What’s going on?": "Kimberly oszalała. W kółko gada o demonach i piekle. Co się dzieje?",
    "Can I talk to her?": "Mogę z nią porozmawiać?",
    "She’s pissed. I won’t let her go on the air with her acting like a crazy person…": "Jest wkurzona. Nie pozwolę jej wejść na antenę, gdy zachowuje się jak wariatka…",
    "You can try and talk some sense into her, but I don’t know where she went.": "Możesz spróbować przemówić jej do rozsądku, ale nie wiem, dokąd poszła.",
    "Maybe you can salvage this situation… Bring us the stolen painting and you go live with it.": "Może da się uratować sytuację… Przynieś nam skradziony obraz, a wejdziesz na żywo z nim.",
    "No way! I’m not a news broadcaster.": "Nie ma mowy! Nie jestem prezenterem.",
    "Hey, you’re better than nothing… And people love you!": "Hej, jesteś lepszy niż nic… A ludzie cię kochają!",
    "Let me find Kimberly.": "Pozwól, że znajdę Kimberly.",
    "The clock is ticking. We may have to cancel tonight's broadcast.": "Czas ucieka. Możemy musieć odwołać dzisiejszą emisję.",
    "Good luck finding Kimberly. She stormed off after I told her she can’t go on-air with her demon story.": "Powodzenia w szukaniu Kimberly. Wybiegła wściekła, gdy powiedziałem, że nie może wejść na antenę z historią o demonach.",
    "Hopefully you can talk some sense into Kimberly.": "Mam nadzieję, że przemówisz Kimberly do rozsądku.",
    "I still don’t understand how everyone got off so lightly.": "Wciąż nie rozumiem, jak wszyscy uszli tak lekko.",
    "Justice was served.": "Sprawiedliwości stało się zadość.",
    "If you see Miss Foxx, let us know.": "Jeśli zobaczysz pannę Foxx, daj nam znać.",
    "I heard the news. Congratulations on being a free man.": "Słyszałem wiadomości. Gratulacje, jesteś wolnym człowiekiem.",
    "Everything okay, Paul? How’d it work out?": "Wszystko w porządku, Paul? Jak to wyszło?",
    "Ha! Great, like you wouldn’t believe.": "Ha! Świetnie, lepiej niż myślisz.",
    "Turns out that stunt you and Kim pulled was a big hit and brought in great ratings.": "Okazuje się, że ta sztuczka, którą wykręciliście z Kim, była hitem i przyniosła świetną oglądalność.",
    "The fines will be a few million, but the profits are closing in on a hundred mil!": "Kary wyniosą kilka milionów, ale zyski zbliżają się do stu baniek!",
    "That’s good, right?": "To dobrze, prawda?",
    "Never in my many years of producing would I have expected porn on TV to be met with such enthusiasm.": "Przez wszystkie moje lata jako producent nigdy nie spodziewałem się, że porno w TV spotka się z takim entuzjazmem.",
    "Perhaps the world is changing.": "Może świat się zmienia.",
    "I hear you got Andrea’s old mansion.": "Słyszę, że dostałeś starą rezydencję Andrei.",
    "I managed to swing it, yeah. It’s a great place.": "Udało się, tak. Świetne miejsce.",
    "Uh huh, yeah. Really great for a detective.": "Mhm, tak. Naprawdę świetne dla detektywa.",
    "Detectives must make out better than I thought.": "Detektywi muszą zarabiać lepiej, niż myślałem.",
    "I might know a thing or two about smart investing.": "Może znam się trochę na mądrym inwestowaniu.",
    "Right, smart investing. You’ll have to show me some of your tricks.": "Jasne, mądre inwestowanie. Będziesz musiał pokazać mi kilka sztuczek.",
    "Another time, perhaps. See you around, Paul.": "Może innym razem. Do zobaczenia, Paul.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=83 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=90: raise SystemExit(f'Expected 90, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map83')
