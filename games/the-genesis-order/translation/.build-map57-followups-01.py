#!/usr/bin/env python3
"""Build Polish drafts for Map 57 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map57-followups-01.jsonl'
TRANSLATIONS = {
    "Please, have a seat.": "Proszę, usiądź.",
    "All finished, Lillian.": "Wszystko gotowe, Lillian.",
    "How did it taste?": "Jak smakowało?",
    "You’re not the woman I expected you to be, Lillian.": "Nie jesteś kobietą, jakiej się spodziewałem, Lillian.",
    "A welcome surprise, I hope.": "Mam nadzieję, że to miłe zaskoczenie.",
    "We best get dressed. Dinner will be served shortly.": "Lepiej się ubierzmy. Kolacja zostanie podana wkrótce.",
    "Is the meal to your liking, Madam?": "Czy posiłek pani odpowiada, madam?",
    "A job well done. The Lord has blessed you with many talents.": "Dobra robota. Pan obdarzył cię wieloma talentami.",
    "I do my best to serve the wishes of the Lord.": "Robię, co w mojej mocy, by służyć woli Pana.",
    "Go now. And pray.": "Idź teraz. I módl się.",
    "Yes, Madam.": "Tak, madam.",
    "I’ve worked up quite an appetite.": "Zrobiłam się dość głodna.",
    "Enjoy the meal, 1Hero.": "Smacznego, 1Hero.",
    "I’ve already had a pretty tasty snack, myself.": "Ja już miałam całkiem smaczną przekąskę.",
    "The first of many shared moments, I hope.": "Mam nadzieję, że to pierwszy z wielu wspólnych momentów.",
    "An excellent meal, Lillian.": "Doskonały posiłek, Lillian.",
    "I’m glad you enjoyed your meal.": "Cieszę się, że smakował ci posiłek.",
    "If you’ll excuse me, I must tend to my work.": "Jeśli pozwolisz, muszę zająć się pracą.",
    "Thanks for inviting us over, Lillian. It’s been an unexpectedly good time.": "Dziękujemy za zaproszenie, Lillian. To był nieoczekiwanie miły czas.",
    "I look forward to the next time we can enjoy each other's company.": "Nie mogę się doczekać następnego razu, gdy będziemy mogli cieszyć się swoim towarzystwem.",
    "Goodbye, 1Hero. Do you know the way out?": "Żegnaj, 1Hero. Wiesz, jak wyjść?",
    "I’ll show him.": "Odprowadzę go.",
    "That was crazy!": "To było szalone!",
    "Not a bad plan, 1Hero.": "Niezły plan, 1Hero.",
    "To earn her trust… I think she trusts us.": "By zdobyć jej zaufanie… Myślę, że nam ufa.",
    "Yeah. I think that’s safe to say.": "Tak. Można tak powiedzieć.",
    "It didn’t look like you had to try too hard.": "Nie wyglądało na to, że musiałaś się bardzo starać.",
    "I’ve never had a threesome before.": "Nigdy wcześniej nie miałam trójkąta.",
    "I’ll admit that was fun.": "Przyznam, że to była zabawa.",
    "What do you think of Lillian? Do you think she’s hiding something?": "Co myślisz o Lillian? Myślisz, że coś ukrywa?",
    "If she is, we’ll find it.": "Jeśli tak, znajdziemy to.",
    "What if she’s just a lonely girl we’re spying on?": "A co jeśli to tylko samotna dziewczyna, którą śledzimy?",
    "You’re a detective. Snooping around is your job.": "Jesteś detektywem. Węszenie to twoja praca.",
    "It seems we have some time alone. Maybe we can find something while we’re here.": "Wygląda na to, że mamy chwilę sami. Może znajdziemy coś, skoro tu jesteśmy.",
    "Let’s split up and search the mansion.": "Rozdzielmy się i przeszukajmy rezydencję.",
    "Just be careful, Erica.": "Tylko uważaj, Erica.",
    "I know this place well. I won’t get into trouble.": "Znam to miejsce dobrze. Nie wpadnę w kłopoty.",
    "Lillian didn’t seem to mind that I was late. But we shouldn't make a habit out of staying up late.": "Lillian nie wydawała się przejmować moim spóźnieniem. Ale nie powinniśmy przyzwyczajać się do zarywania nocy.",
    "Act cool, 1Hero. Someone’s in the kitchen and I don’t know if you’re really allowed to be here right now.": "Zachowuj się naturalnie, 1Hero. Ktoś jest w kuchni i nie wiem, czy naprawdę wolno ci tu teraz przebywać.",
    "Wait, who’s in the kitchen?": "Zaraz, kto jest w kuchni?",
    "Just… come on.": "Po prostu… chodź.",
    "Go find some honey and give it to the leper in the kitchen…": "Idź znajdź miód i daj go trędowatemu w kuchni…",
    "We need to get him to leave.": "Musimy sprawić, by wyszedł.",
    "Get him some honey and when he leaves we can check it out…": "Zanieś mu miód, a gdy wyjdzie, sprawdzimy to…",
    "But don’t go back in there without the honey. He’s getting suspicious.": "Ale nie wracaj tam bez miodu. Zaczyna być podejrzliwy.",
    "Erica, 1Hero. A surprise to see you here.": "Erica, 1Hero. Co za niespodzianka.",
    "I was just finishing up.": "Właśnie kończyłam.",
    "She… had a hard time reaching something.": "Ona… miała problem, by coś dosięgnąć.",
    "Such a helpful detective.": "Taki pomocny detektyw.",
    "Well… I should get going.": "Cóż… Powinnam już iść.",
    "Enjoy your weekend, Erica.": "Miłego weekendu, Erica.",
    "Thank you, Lillian.": "Dziękuję, Lillian.",
    "1Hero, stay behind. I want to speak with you.": "1Hero, zostań. Chcę z tobą porozmawiać.",
    "Uhh, okay.": "Yyy, jasne.",
    "See you at seven o'clock, 1Hero.": "Do zobaczenia o siódmej, 1Hero.",
    "Playing games without me?": "Bawicie się beze mnie?",
    "Huh? No… We were just… I was helping her out.": "Co? Nie… My tylko… Pomagałem jej.",
    "I hope I can trust that you’ll respect my wishes in the future.": "Mam nadzieję, że mogę liczyć, iż uszanujesz moje życzenia w przyszłości.",
    "Of course. I’m sorry, Lillian.": "Oczywiście. Przepraszam, Lillian.",
    "I would very much enjoy joining you next time you and Erica have an itch for a bit of excitement.": "Bardzo chętnie dołączę następnym razem, gdy ty i Erica poczujecie ochotę na odrobinę ekscytacji.",
    "Haha. I’m sure she’d love that.": "Haha. Jestem pewien, że bardzo by chciała.",
    "It is getting late. If you don’t mind, I'd like to be alone.": "Robi się późno. Jeśli nie masz nic przeciwko, chciałabym zostać sama.",
    "Yes, Lillian. I should get going.": "Tak, Lillian. Powinnam już iść.",
    "Did I fool her, or is she fooling me?": "Czy ją oszukałam, czy to ona oszukuje mnie?",
    "I need to figure out what’s going on under the kitchen…": "Muszę dowiedzieć się, co dzieje się pod kuchnią…",
    "But it’ll have to wait.": "Ale to musi poczekać.",
    "Hey, you two. I need some help… unlocking this door.": "Hej, wy dwoje. Potrzebuję pomocy… z otwarciem tych drzwi.",
    "It is not our place to enter that room. If you need help, find Lillian.": "Nie powinniśmy wchodzić do tego pokoju. Jeśli potrzebujesz pomocy, znajdź Lillian.",
    "It’s stuck. I just need a strong man to open it.": "Zacięły się. Potrzebuję tylko silnego mężczyzny, by je otworzyć.",
    "The door is locked. You need a key.": "Drzwi są zamknięte. Potrzebujesz klucza.",
    "Well… Shit.": "Cóż… Cholera.",
    "Hey! No flowers. Mother does not like you changing the decorations.": "Hej! Żadnych kwiatów. Matka nie lubi, gdy zmieniasz dekoracje.",
    "But it’s just so beautiful. I just want to see how it would look.": "Ale to takie piękne. Chcę tylko zobaczyć, jak by to wyglądało.",
    "Now’s my chance.": "Teraz moja szansa.",
    "Alright. I’m in.": "Dobra. Weszłam.",
    "Could I pry it open with something?": "Czy mogłabym to podważyć czymś?",
    "There's an opening in the wall.": "W ścianie jest otwór.",
    "Maybe if I put this eyeball in the socket…": "Może jeśli włożę to oko do oczodołu…",
    "I heard something!": "Coś słyszałam!",
    "Bobby… We’re running out of time.": "Bobby… Kończy nam się czas.",
    "Lilith, a demon from Hell, came through that portal and she has to be stopped.": "Lilith, demon z Piekła, przeszła przez ten portal i trzeba ją powstrzymać.",
    "With what? Magic?": "Czym? Magią?",
    "Of course that’s what you would say.": "Oczywiście, że tak powiesz.",
    "Bobby, they are in this mansion… I think.": "Bobby, oni są w tej rezydencji… Tak myślę.",
    "This mansion is a big place… Do you know what they look like?": "Ta rezydencja jest ogromna… Wiesz, jak wyglądają?",
    "Let me and my team search the mansion. I know we can find them.": "Pozwól mi i mojemu zespołowi przeszukać rezydencję. Wiem, że ich znajdziemy.",
    "Let’s say we find these amulets. What the hell then?": "Załóżmy, że znajdziemy te amulety. Co wtedy, do diabła?",
    "The priest will help us… He’ll figure out how to stop Lilith.": "Ksiądz nam pomoże… Wymyśli, jak powstrzymać Lilith.",
    "This sounds crazy… But I know what I saw.": "To brzmi szalenie… Ale wiem, co widziałam.",
    "It’s not a trick, Bobby. We need to stop her.": "To nie jest sztuczka, Bobby. Musimy ją powstrzymać.",
    "Fine… I’ll let you search the mansion, but my men will be keeping an eye on you.": "Dobrze… Pozwolę wam przeszukać rezydencję, ale moi ludzie będą mieć na was oko.",
    "Erica’s uniform?": "Mundur Eriki?",
    "She looks so sexy.": "Wygląda tak seksownie.",
    "I can bring Sister Judy and Kimberly back to the church…": "Mogę zabrać siostrę Judy i Kimberly z powrotem do kościoła…",
    "The father will need to know what’s happening.": "Ojciec musi wiedzieć, co się dzieje.",
    "We must also find a relic.": "Musimy też znaleźć relikwię.",
    "I can help you find one… What do they look like?": "Mogę pomóc wam jedną znaleźć… Jak wyglądają?",
    "It depends… I’m not familiar with relics at Eve Cathedral.": "To zależy… Nie znam relikwii z katedry Ewy.",
    "I am also not sure what we might have, but Father may be able to point us in the right direction.": "Też nie jestem pewna, co możemy mieć, ale ojciec może wskazać właściwy kierunek.",
    "Sister Judy… Do you have any idea where the amulets are?": "Siostro Judy… Masz pojęcie, gdzie są amulety?",
    "There is more than one?": "Jest ich więcej niż jeden?",
    "We gave it to someone… They took it to another room.": "Oddaliśmy go komuś… Zanieśli go do innego pokoju.",
    "In the mansion?": "W rezydencji?",
    "I have no idea where they put it. But that’s where I would look.": "Nie mam pojęcia, gdzie go położyli. Ale tam bym szukała.",
    "We’ll find them.": "Znajdziemy je.",
    "Let’s go back to the church.": "Wróćmy do kościoła.",
    "Father must be so worried.": "Ojciec musi być taki zmartwiony.",
    "So, where do we look for these amulets?": "Więc gdzie szukamy tych amuletów?",
    "They could be anywhere. Let’s spread out.": "Mogą być wszędzie. Rozdzielmy się.",
    "I know this place pretty well. I’ll see what I can find.": "Znam to miejsce całkiem dobrze. Zobaczę, co znajdę.",
    "I know it’s late, but Melissa is going to want to know what’s going on.": "Wiem, że jest późno, ale Melissa będzie chciała wiedzieć, co się dzieje.",
    "Melissa… Bobby is here at the mansion… We’re all going to search for the amulets.": "Melissa… Bobby jest tu w rezydencji… Wszyscy będziemy szukać amuletów.",
    "What time is it?": "Która godzina?",
    "Lillian is going to post the Toma on the internet… We have to stop her now.": "Lillian zamierza wystawić Tomę do internetu… Musimy ją teraz powstrzymać.",
    "I’ll head over soon.": "Wkrótce tam będę.",
    "This place is huge… How are we supposed to find anything?": "To miejsce jest ogromne… Jak mamy cokolwiek znaleźć?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=57 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=translations.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=116: raise SystemExit(f'Expected 116, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map57')