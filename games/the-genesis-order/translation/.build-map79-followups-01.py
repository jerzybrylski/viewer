#!/usr/bin/env python3
"""Build Polish drafts for Map 79 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map79-followups-01.jsonl'
TRANSLATIONS = {
    "1Hero, what a pleasant surprise.": "1Hero, co za miła niespodzianka.",
    "I heard you were looking for me, Commissioner Kimura. Something about a new case?": "Słyszałam, że mnie szukałeś, komisarz Kimura. Chodzi o nową sprawę?",
    "So where were you? Your co-worker told me you were out, but he didn’t know why.": "Więc gdzie byłeś? Twój współpracownik mówił, że wyszedłeś, ale nie wiedział dlaczego.",
    "Oh, uh, I was out working a case.": "Och, yyy, prowadziłem sprawę.",
    "What case?": "Jaką sprawę?",
    "The Wilkes case.": "Sprawę Wilkesa.",
    "I thought Wilkes died of a heart attack.": "Myślałam, że Wilkes zmarł na zawał serca.",
    "I think there’s more to it than that.": "Myślę, że kryje się za tym coś więcej.",
    "You could say I’m following a hunch.": "Można powiedzieć, że idę za przeczuciem.",
    "A hunch? Do you often follow hunches when working cases?": "Przeczuciem? Często podążasz za przeczuciami, prowadząc sprawy?",
    "It’s part of being a detective.": "To część bycia detektywem.",
    "Sometimes things don’t feel right about a case. I have to figure out if there’s something more to those feelings.": "Czasem coś mi nie gra w sprawie. Muszę sprawdzić, czy za tym przeczuciem kryje się coś więcej.",
    "Hopefully not wasting department resources, I’m sure.": "Mam nadzieję, że nie marnujesz zasobów wydziału.",
    "Oh, of course not.": "Och, oczywiście, że nie.",
    "So what can I do for you, commissioner?": "Więc co mogę dla pani zrobić, pani komisarz?",
    "I guess you could say I’m following a hunch of my own.": "Chyba można powiedzieć, że ja też podążam za własnym przeczuciem.",
    "I’m thinking of offering you an opportunity.": "Myślę, żeby zaproponować ci pewną okazję.",
    "I’m glad you’re eager.": "Cieszę się, że jesteś chętny.",
    "But it’s getting late in the day now, and we’ll need some time to go over it.": "Ale robi się późno, a będziemy potrzebować czasu, by to omówić.",
    "Oh, sure. Maybe tomorrow?": "Och, jasne. Może jutro?",
    "How about we discuss it over dinner? Say, at my place, around 6pm?": "Może omówimy to przy kolacji? Powiedzmy, u mnie, około 18:00?",
    "Dinner? At your place?": "Kolacja? U pani?",
    "Uh, sure, that sounds great.": "Yyy, jasne, brzmi świetnie.",
    "Excellent. Let me give you the address.": "Doskonale. Podam ci adres.",
    "Oh, that’s okay, I know where you live.": "Och, nie trzeba, wiem, gdzie pani mieszka.",
    "You’re not stalking me, are you?": "Nie śledzisz mnie chyba?",
    "Oh, no, not at all!": "Och, nie, skądże!",
    "It’s just one of the fancier residences in town, and you do have a high profile. People talk.": "To po prostu jedna z bardziej eleganckich rezydencji w mieście, a pani ma wysoki profil. Ludzie gadają.",
    "A perfect excuse, but being stalked by a handsome young man might not be such a bad thing.": "Doskonała wymówka, ale bycie śledzoną przez przystojnego młodzieńca może nie być takie złe.",
    "Then I’ll see you this evening.": "Więc do zobaczenia dziś wieczorem.",
    "Oh, and I take it you’ll be wearing something…nicer, for dinner.": "I zakładam, że włożysz coś… ładniejszego na kolację.",
    "Oh, umm, sure thing.": "Och, yyy, oczywiście.",
    "Fantastic, 1Hero. Don’t be late.": "Fantastycznie, 1Hero. Nie spóźnij się.",
    "Absolutely. I’ll see you then, commissioner.": "Absolutnie. Do zobaczenia, pani komisarz.",
    "Wow, a dinner meeting with the commissioner! This could be great.": "Wow, kolacja z panią komisarz! To może być świetna okazja.",
    "I wonder what this opportunity could be.": "Ciekawe, co to za okazja.",
    "When Melissa finds out, she might be upset.": "Kiedy Melissa się dowie, może być niezadowolona.",
    "I’ll deal with that when the time comes.": "Zajmę się tym, kiedy nadejdzie czas.",
    "First, I’ll need to make a good impression on Andrea. Last time we talked, she caught me snooping around using Melissa’s login.": "Najpierw muszę zrobić dobre wrażenie na Andrei. Ostatnio gdy rozmawialiśmy, przyłapała mnie na szperaniu na loginie Melissy.",
    "I hope I don’t screw things up.": "Mam nadzieję, że niczego nie spieprzę.",
    "I should go prepared. A nice outfit and a bottle of wine is sure to impress.": "Powinienem się przygotować. Szykowny strój i butelka wina na pewno zrobią wrażenie.",
    "Time to go shopping.": "Czas na zakupy.",
    "The damn security guard took my belt buckle just because it was made of metal.": "Cholerny ochroniarz zabrał mi klamrę od paska tylko dlatego, że była metalowa.",
    "Wow! You found my belt buckle! My pants will finally stay up! Take this reward.": "Wow! Znalazłeś moją klamrę! W końcu spodnie nie będą spadać! Weź tę nagrodę.",
    "Feeling ready?": "Gotowy?",
    "I’m ready for it, Andrea.": "Jestem gotowy, Andrea.",
    "Commissioner Kimura while we’re on the clock.": "Pani komisarz Kimura, gdy jesteśmy na służbie.",
    "Oh, yeah. Right. Sorry.": "Och, tak. Jasne. Przepraszam.",
    "Come with me. We’ll discuss everything in the interrogation room.": "Chodź ze mną. Omówimy wszystko w pokoju przesłuchań.",
    "1Hero! There you are.": "1Hero! Jesteś.",
    "Sorry, Miss Kimura. I was out of the office this afternoon.": "Przepraszam, panno Kimura. Nie było mnie w biurze dziś po południu.",
    "Did you watch the segment?": "Oglądałeś segment?",
    "Yeah. Looked pretty good to me.": "Tak. Wyglądał całkiem nieźle.",
    "It was perfect. You did great.": "Był idealny. Spisałeś się świetnie.",
    "I’m glad to hear that… but…": "Cieszę się… ale…",
    "I heard about what happened at the Wilkes’ mansion.": "Słyszałem o tym, co stało się w rezydencji Wilkesów.",
    "So... What do we tell the public?": "Więc… Co mówimy opinii publicznej?",
    "We have to keep this under wraps.": "Musimy zachować to w tajemnicy.",
    "Lots of officers witnessed what happened.": "Wielu funkcjonariuszy było świadkami tego, co się wydarzyło.",
    "Everyone is convinced that it was a robbery attempt.": "Wszyscy są przekonani, że to była próba rabunku.",
    "This doesn’t have to tie back to the Guild.": "Nie musi się to wiązać z Gildią.",
    "I know who Nellie is… She was there.": "Wiem, kim jest Nellie… Była tam.",
    "1Hero, you have a specific job. The rest you must trust me with.": "1Hero, masz konkretne zadanie. Resztę musisz zostawić mnie.",
    "Then let me ask you. Should I ignore Nellie or should I arrest her?": "Więc zapytam. Mam ignorować Nellie, czy ją aresztować?",
    "If you suspect someone is with the Guild…": "Jeśli podejrzewasz, że ktoś jest z Gildii…",
    "Leave them alone and do not interfere.": "Zostaw ich w spokoju i nie wtrącaj się.",
    "Okay, Miss Kimura. You can trust me…": "Dobrze, panno Kimura. Może mi pani ufać…",
    "But I will do what I must to keep Lillian safe.": "Ale zrobię, co muszę, by zapewnić Lillian bezpieczeństwo.",
    "She’s safe. The officers will keep guard over her mansion.": "Jest bezpieczna. Funkcjonariusze będą pilnować jej rezydencji.",
    "I can’t help but feel the need to investigate further. Is there anything I can do?": "Nie mogę się oprzeć potrzebie dalszego śledztwa. Czy mogę coś zrobić?",
    "Don’t you have other cases?": "Nie masz innych spraw?",
    "Your focus with the Guild is public relations. If you have the itch to solve crime, then work on your other cases.": "Twoim zadaniem w Gildii jest PR. Jeśli swędzi cię, by rozwiązywać przestępstwa, zajmij się innymi sprawami.",
    "Shit. Why won't she just let me be a part of the undercover team?": "Cholera. Dlaczego po prostu nie pozwoli mi być częścią zespołu pod przykrywką?",
    "I’d make for a great spy!...": "Byłbym świetnym szpiegiem!...",
    "I think.": "Chyba.",
    "Heh… Maybe I am too cocky.": "Heh… Może jestem zbyt zarozumiały.",
    "Smooth moves, 1Hero.": "Gładka akcja, 1Hero.",
    "Shut up, Bobby.": "Zamknij się, Bobby.",
    "Did something fall down to the first floor?": "Czy coś spadło na parter?",
    "1Hero!?": "1Hero!?",
    "Are you stealing stuff from the office?": "Kradniesz rzeczy z biura?",
    "What the hell is this? Looks like old mint-flavored chewing gum in an ashtray.": "Co to, do cholery, jest? Wygląda jak stara guma miętowa w popielniczce.",
    "Why would a cat try to eat chewing gum?": "Po co kot miałby jeść gumę do żucia?",
    "Hey! Get back! That thing might have rabies.": "Hej! Cofnij się! To coś może mieć wściekliznę.",
    "Somehow a cat got into the building.": "Jakoś kot dostał się do budynku.",
    "Can’t you just grab it?": "Nie możesz go po prostu złapać?",
    "That’s not my area of expertise.": "To nie moja działka.",
    "Shit! It’s heading for the meeting rooms!": "Cholera! Kieruje się do salek konferencyjnych!",
    "Whatever shall we do?": "Cóż mamy począć?",
    "Did you find the cat?": "Znalazłeś kota?",
    "I got it! Turns out it was attracted to mint. Can you believe that?": "Mam go! Okazuje się, że przyciągnęła go mięta. Możesz w to uwierzyć?",
    "Whatever. Hand it over. I need to bring it to pest control.": "Nieważne. Dawaj go. Muszę go oddać do zwalczania szkodników.",
    "Pest control?": "Zwalczania szkodników?",
    "We have to euthanize it.": "Musimy go uśpić.",
    "What the hell else were you expecting?": "A czego innego się spodziewałeś?",
    "Hey! I found the cat. It’s my responsibility.": "Hej! To ja znalazłem kota. To moja odpowiedzialność.",
    "Fine. Do it yourself. I have more important things to attend to anyways.": "Dobra. Zrób to sam. I tak mam ważniejsze sprawy.",
    "Shit… What am I going to do with a cat? I guess I should bring him home before one of those officers gets a hold of it.": "Cholera… Co mam zrobić z kotem? Chyba powinienem zabrać go do domu, zanim któryś z funkcjonariuszy go dopadnie.",
    "I have an old key, but since you're so ugly it'll cost ya a pretty penny.": "Mam stary klucz, ale skoro jesteś taki brzydki, to będzie cię to słono kosztować.",
    "Wow! You sure are pretty. Here's a gift!": "Wow! Ale jesteś śliczna. Oto prezent!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=79 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=100: raise SystemExit(f'Expected 100, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map79')
