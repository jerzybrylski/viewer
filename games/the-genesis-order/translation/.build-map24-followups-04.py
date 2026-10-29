import json
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl')
EVENTS = {
    61: {
        "Oh! Hannah’s naked again.": "Och! Hannah znów jest naga.",
        "Hey, Heather! Looks like I’m in time for a pool party.": "Hej, Heather! Chyba zdążyłem na imprezę przy basenie.",
        "You sure are. Is that what you’re wearing?": "Zdążyłeś. Naprawdę zamierzasz tak pływać?",
        "I’m always prepared. Come on, ladies! Let's not talk about my underwear anymore.": "Zawsze jestem przygotowany. No dalej, dziewczyny! Skończmy już rozmawiać o mojej bieliźnie.",
        "Come on! I want to see what she does.": "No dalej! Chcę zobaczyć, co zrobi.",
        "Hey! Watch out for bears!": "Hej! Uważajcie na niedźwiedzie!",
        "I know you all had your little fun outside earlier. But if Hannah needs some company, I can swim with her.": "Wiem, że wcześniej trochę się zabawiliście na dworze. Ale jeśli Hannah potrzebuje towarzystwa, mogę z nią popływać.",
        "She ran away from home… Carol saw her wearing makeup.": "Uciekła z domu… Carol widziała ją w makijażu.",
        "Makeup?": "W makijażu?",
        "And one of Carol’s dresses.": "I w jednej z sukienek Carol.",
        "Hannah in a dress!?": "Hannah w sukience!?",
        "I was shocked too.": "Też byłam w szoku.",
        "Why the hell would Hannah voluntarily wear a dress and makeup?": "Po co, do cholery, Hannah miałaby dobrowolnie założyć sukienkę i makijaż?",
        "Sounds like she was trying to impress someone.": "Wygląda na to, że chciała komuś zaimponować.",
        "I… I doubt it.": "W… Wątpię.",
        "A big hunk like you, who wouldn’t want a piece?": "Która nie chciałaby uszczknąć czegoś dla siebie, skoro jesteś takim przystojniakiem?",
        "Enough, Mom.": "Wystarczy, mamo.",
        "Hey, if you’re going to use my backyard as a place to fool around, you can’t blame me for being a little flirty.": "Hej, jeśli używacie mojego podwórka do baraszkowania, nie dziwcie się, że trochę z wami flirtuję.",
        "I wasn’t fooling around!": "Wcale nie baraszkowałem!",
        "To be fair… Ella egged on Sister Judy.": "Trzeba przyznać… Ella zachęcała siostrę Judy.",
        "You... took her virginity?": "Ty… odebrałeś jej dziewictwo?",
        "No!...": "Nie!...",
        "We’re not fucking, Mom!": "Nie pieprzymy się, mamo!",
        "It’s okay if you are.": "Jeśli tak, to nie ma sprawy.",
        "I don’t do that… It’s not like that at all.": "Nie robię takich rzeczy… To wcale tak nie wygląda.",
        "Sure… I totally believe you.": "Jasne… Wierzę ci na słowo.",
        "Hey! It’s true!": "Hej! To prawda!",
    },
    47: {
        "Let’s see if I remember how to work this TV.": "Zobaczmy, czy pamiętam, jak obsługiwać ten telewizor.",
        "There we go.": "No, już.",
        "Do you remember this?": "Pamiętasz to?",
        "Hey! This is the trip we took to Cape Vedra.": "Hej! To nasza wycieczka do Cape Vedra.",
        "We met there while you were still going to school.": "Poznaliśmy się tam, kiedy jeszcze chodziłeś do szkoły.",
        "That was a fun trip.": "To była udana wycieczka.",
        "Look at cute little Chloe. She was infatuated with you.": "Spójrz na małą Chloe. Była w tobie zakochana po uszy.",
        "And there I am, not giving her any attention.": "A ja nawet nie zwracałem na nią uwagi.",
        "You drove her wild.": "Doprowadzałeś ją do szaleństwa.",
        "We had a lot of good times, but she was like a little sister to me.": "Dobrze się razem bawiliśmy, ale była dla mnie jak młodsza siostra.",
        "I get it, 1Hero. You two were very different.": "Rozumiem, 1Hero. Bardzo się od siebie różniliście.",
        "You were quite the trouble maker.": "Byłeś niezłym rozrabiaką.",
        "Oh, my. What a picture.": "O rany. Co za zdjęcie.",
        "I always thought of you as an ass man, 1Hero.": "Zawsze myślałam, że jesteś fanem tyłków, 1Hero.",
        "I clearly liked something about this angle.": "Wyraźnie coś mi się w tym ujęciu podobało.",
        "Now you’re the one teasing me.": "Teraz to ty się ze mnie droczysz.",
        "This is my favorite picture of us. What a wonderful day.": "To moje ulubione wspólne zdjęcie. Ależ to był wspaniały dzień.",
        "I’m lucky I had you around. We always had such great times together.": "Miałam szczęście, że byłeś obok. Zawsze świetnie się razem bawiliśmy.",
        "I think we needed each other…": "Chyba byliśmy sobie potrzebni…",
        "Being a single mom isn’t easy.": "Samotne macierzyństwo nie jest łatwe.",
    },
    54: {
        "You found a painting in the mansion? You never told me this.": "Znalazłeś obraz w rezydencji? Nic mi nie mówiłeś.",
        "I didn’t find it. It was someone else.": "To nie ja go znalazłem. Ktoś inny.",
        "Well… I don’t really know.": "Cóż… Sama nie wiem.",
        "So, what’s the wait? You know where Duncan is?": "Na co więc czekamy? Wiesz, gdzie jest Duncan?",
        "It’s up to the commissioner. I’m not in charge.": "To zależy od komisarz. Ja tu nie dowodzę.",
        "I’m sure you’ll catch those thieves, 1Hero. You’re so smart.": "Na pewno złapiesz tych złodziei, 1Hero. Jesteś taki bystry.",
        "1Hero looks so good on TV!": "1Hero świetnie wygląda w telewizji!",
        "Haha. Thanks, Hannah.": "Haha. Dzięki, Hannah.",
        "That was fun. What are we going to do now?": "Było fajnie. Co teraz zrobimy?",
        "I’ve got to go back to the mansion.": "Muszę wrócić do rezydencji.",
        "Huh? Why?": "Co? Dlaczego?",
        "I think Lillian knows more than she’s letting on… She wants to tell me something.": "Chyba Lillian wie więcej, niż mówi… Chce mi coś wyznać.",
        "Is it a trap?": "To pułapka?",
        "Don’t worry, Erica. There are officers there. She wouldn’t dare try and sacrifice me to her weird demon gods.": "Spokojnie, Erica. Są tam funkcjonariusze. Nie odważy się złożyć mnie w ofierze swoim dziwnym demonicznym bogom.",
        "Demon god!?": "Demonicznym bogom!?",
        "I’m joking.": "Żartuję.",
        "Maybe you’re not joking.": "Może wcale nie żartujesz.",
        "Please do be careful.": "Proszę, uważaj na siebie.",
        "Mom will probably be home soon. Maybe we should do the dishes.": "Mama niedługo pewnie wróci. Może pozmywamy naczynia.",
        "I’ll supervise!": "Będę nadzorować!",
    },
    6: {
        "I can’t wait to hop on that dick again.": "Nie mogę się doczekać, aż znów usiądę na tym kutasie.",
        "Jesus, Heather.": "Jezu, Heather.",
        "I’ve been starving for the past three months, dear.": "Od trzech miesięcy jestem wygłodniała, kochanie.",
        "You better really give it to me.": "Lepiej porządnie mnie zerżnij.",
        "It sure is quiet around here… I like it this way.": "Ale tu cicho… Podoba mi się tak.",
        "No hankering for a new adventure?": "Nie ciągnie cię do nowej przygody?",
        "Haha… Oh, 1Hero.": "Haha… Och, 1Hero.",
        "How is it, now that Chloe moved out?": "Jak to jest, odkąd Chloe się wyprowadziła?",
        "It’s alright.": "Nie jest źle.",
        "And in case she gets homesick, her room is just the way she left it.": "Gdyby zatęskniła za domem, jej pokój wciąż wygląda tak, jak go zostawiła.",
        "You’re a good mom.": "Jesteś dobrą mamą.",
        "I do my part.": "Robię, co do mnie należy.",
        "Also a super sexy mom.": "I do tego superseksowną mamą.",
        "Oh my, stud. Maybe after dinner tonight, this mom can show you just how sexy she really is.": "Ojej, przystojniaku. Może dziś po kolacji ta mamusia pokaże ci, jaka naprawdę jest seksowna.",
        "So you’re coming to dinner?": "Czyli przyjdziesz na kolację?",
        "Wouldn’t miss it for the world, hun.": "Nie opuściłbym jej za żadne skarby, kochanie.",
        "I’ll see you then.": "W takim razie do zobaczenia.",
        "Looking forward to it.": "Już się nie mogę doczekać.",
    },
    45: {
        "1Hero? Do you know where my mom went?": "1Hero? Wiesz, dokąd poszła moja mama?",
        "I thought she was here?": "Myślałem, że jest tutaj.",
        "Perhaps she went out to eat at the restaurant.": "Może poszła coś zjeść w restauracji.",
        "She doesn’t normally eat out.": "Zwykle nie jada poza domem.",
        "She might be at the gym. Did you tell her you were coming home?": "Może jest na siłowni. Powiedziałeś jej, że wracasz do domu?",
        "No. I just thought she’d be here.": "Nie. Myślałem, że po prostu tu będzie.",
        "I’ll see if I can find her.": "Spróbuję ją znaleźć.",
        "I’m so hungry… Maybe we should go to Hannah’s.": "Jestem taka głodna… Może pójdziemy do Hannah.",
        "She has food?": "Ma coś do jedzenia?",
        "Carol always cooks up something good.": "Carol zawsze przygotuje coś dobrego.",
        "Don’t worry. Carol loves company…": "Spokojnie. Carol lubi gości…",
        "Come on. Let’s go before Hannah eats everything.": "Chodźmy, zanim Hannah wszystko zje.",
        "Would you come with us, 1Hero?": "Pójdziesz z nami, 1Hero?",
        "I might be able to take a dinner break.": "Może uda mi się zrobić przerwę na kolację.",
        "You shouldn’t be working on the weekend.": "Nie powinieneś pracować w weekend.",
        "But then who would keep you ladies safe?": "A kto wtedy będzie was chronił?",
        "You’re so thoughtful.": "Ale jesteś troskliwy.",
        "I’ll meet you at the farm later.": "Spotkamy się później na farmie.",
    },
}
known = {r['id'] for r in map(json.loads, MERGED.read_text(encoding='utf-8').splitlines()) if r['translation'].strip()}
rows, missing = [], set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    event_id = context.get('event_id')
    if context.get('source_kind') != 'map' or context.get('map_id') != 24 or event_id not in EVENTS or row['id'] in known:
        continue
    source = row['source_text'].strip()
    if not source or source.startswith('/') or source in {'…', '...', '..'}:
        continue
    translation = EVENTS[event_id].get(source)
    if translation is None:
        missing.add((event_id, source))
        continue
    row['translation'] = translation
    rows.append(row)
if missing:
    raise SystemExit('Unmapped strings: ' + repr(sorted(missing)))
path = ROOT / 'drafts/custom-dialogue-map24-followups-04.jsonl'
if path.exists():
    raise SystemExit(f'Refusing to overwrite {path}')
path.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows), encoding='utf-8', newline='\n')
print(f'Wrote Map 24 follow-ups: {len(rows)} records across {len(EVENTS)} events')
