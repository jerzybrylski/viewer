#!/usr/bin/env python3
"""Build Polish drafts for Map 100 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map100-followups-01.jsonl'
TRANSLATIONS = {
    "I think you’re turning a new leaf, Melissa.": "Chyba przechodzisz przemianę, Melissa.",
    "Seems you’re actually listening to me.": "Wygląda na to, że naprawdę mnie słuchasz.",
    "If you’re suggesting that I don’t listen, you’re dead wrong.": "Jeśli sugerujesz, że nie słucham, to grubo się mylisz.",
    "Why do you have to be so difficult? It would make both our lives easier if you just relaxed once in a while.": "Dlaczego musisz być taka trudna? Obojgu byłoby łatwiej, gdybyś czasem odpuściła.",
    "Stop trying to push my buttons and start searching.": "Przestań naciskać mi guziki i zacznij szukać.",
    "Whatever you say, boss.": "Jak sobie życzysz, szefowo.",
    "How do we open it? Is there a key?": "Jak to otworzyć? Jest jakiś klucz?",
    "It’s a combination safe… The code probably died with Zephaniah.": "To sejf szyfrowy… Kod pewnie umarł razem z Zephaniahem.",
    "We might have to brute force it.": "Może będziemy musieli go sforsować.",
    "Well, shit. That’ll take a while.": "No cholera. To trochę potrwa.",
    "Hey. Where are you going?": "Hej. Dokąd idziesz?",
    "We’re not going to open it right now.": "Nie otworzymy go teraz.",
    "But there are other things we could do.": "Ale są inne rzeczy, które moglibyśmy zrobić.",
    "I don’t have time for this! I have to fix the roof, and fast!": "Nie mam na to czasu! Muszę szybko naprawić dach!",
    "The safe is locked. I’ll need to find a code if I’m going to open it up.": "Sejf jest zamknięty. Będę musiał znaleźć kod, jeśli mam go otworzyć.",
    "I can’t believe I figured it out.": "Nie mogę uwierzyć, że to rozgryzłem.",
    "It’s the medicine! This is what Melissa said we needed.": "To lekarstwo! To właśnie Melissa mówiła, że potrzebujemy.",
    "I’ll hold onto this and show it to Melissa at work tomorrow.": "Zatrzymam to i pokażę Melissie w pracy jutro.",
    "I wonder if all the lines in this old journal are as interesting as this.": "Ciekawe, czy wszystkie linijki w tym starym dzienniku są równie interesujące.",
    "You got into the safe?": "Dostałeś się do sejfu?",
    "Your advice worked. There was a note in the attic.": "Twoja rada zadziałała. Na strychu była notatka.",
    "What I expected…": "Tego się spodziewałem…",
    "His heart medication was in here along with a personal journal.": "Jego lek na serce był tutaj razem z osobistym dziennikiem.",
    "I hope they help in your investigation.": "Mam nadzieję, że pomogą w śledztwie.",
    "He didn’t have his medication in his system when he died…": "Nie miał leku w organizmie, gdy umarł…",
    "Perhaps he had turned to the Lord for medical advice.": "Może zwrócił się do Pana po poradę medyczną.",
    "We’re not all that crazy, 1Hero.": "Nie wszyscy jesteśmy aż tak szaleni, 1Hero.",
    "Let’s just hope we don’t find anything sinister in Zeph’s past.": "Miejmy nadzieję, że nie znajdziemy nic złowieszczego w przeszłości Zepha.",
    "If you find anything, please let me know.": "Jeśli coś znajdziesz, daj mi znać, proszę.",
    "Of course, Father. You’ll be one of the first to know.": "Oczywiście, ojcze. Będziesz jednym z pierwszych, którzy się dowiedzą.",
    "One of these days life will return to normal. But not yet.": "Któregoś dnia życie wróci do normy. Ale jeszcze nie.",
    "We’ll get through this, 1Hero.": "Przejdziemy przez to, 1Hero.",
    "A quiet evening without Judy here.": "Cichy wieczór bez Judy tutaj.",
    "We’ll bring her back in one piece.": "Sprowadzimy ją całą i zdrową.",
    "Judy seems full of vigor this morning.": "Judy wydaje się dziś pełna wigoru.",
    "We had a fun night.": "Mieliśmy fajną noc.",
    "Careful not to have too much fun.": "Uważaj, żeby nie bawić się za dobrze.",
    "Did you speak to Tasha?": "Rozmawiałeś z Tashą?",
    "I don’t want to talk about it.": "Nie chcę o tym rozmawiać.",
    "Going to the Bible for Casula wisdom won’t work…": "Sięganie do Biblii po mądrość Casuli nie zadziała…",
    "I need some help.": "Potrzebuję pomocy.",
    "I’ll let Erica know.": "Dam znać Erice.",
    "I must help Father study.": "Muszę pomóc ojcu w nauce.",
    "Are you going to tell Chloe what happened?": "Powiesz Chloe, co się stało?",
    "For Chloe’s sake… perhaps not.": "Dla dobra Chloe… może lepiej nie.",
    "Big day tomorrow.": "Wielki dzień jutro.",
    "We’ll get through this, 1Hero. God is with us.": "Przejdziemy przez to, 1Hero. Bóg jest z nami.",
    "I’m getting too old for adventures.": "Robię się za stary na przygody.",
    "Any new adventures, 1Hero?": "Jakieś nowe przygody, 1Hero?",
    "You never know what’s just around the corner.": "Nigdy nie wiesz, co czai się za rogiem.",
    "I hope we can find those amulets.": "Mam nadzieję, że uda nam się znaleźć te amulety.",
    "Don’t worry. Like I said, I’m a treasure hunter. You can count on me when it comes to this kind of thing.": "Spokojnie. Jak mówiłem, jestem łowcą skarbów. Możesz na mnie liczyć w takich sprawach.",
    "I’ve been up for such a long time… I can hardly see straight.": "Nie śpię od tak dawna… Ledwo widzę na oczy.",
    "Dad! Wake the fuck up! We have the amulets!": "Tato! Obudź się, do cholery! Mamy amulety!",
    "Tasha!? How long was I asleep?": "Tasha!? Jak długo spałem?",
    "Don’t worry, I kept reading.": "Nie martw się, czytałam dalej.",
    "Father, we found the amulets. They were in the mansion.": "Ojcze, znaleźliśmy amulety. Były w rezydencji.",
    "Great job!...": "Świetna robota!...",
    "Now to figure out what it means.": "Teraz trzeba rozgryźć, co to znaczy.",
    "You need to encompass her in the three amulets.": "Musisz otoczyć ją trzema amuletami.",
    "Yeah… I read about it.": "Tak… Czytałem o tym.",
    "What does that mean exactly? How the hell do we lure her into a trap?": "Co to dokładnie znaczy? Jak, do cholery, zwabimy ją w pułapkę?",
    "Can we surround the rift door with the amulets?": "Możemy otoczyć drzwi Szczeliny amuletami?",
    "What we need is a lasso gun.": "Potrzebujemy pistoletu na lasso.",
    "Your mom told you about the lasso gun!?": "Mama ci opowiedziała o pistolecie na lasso!?",
    "Yeah. She used it to capture security guards at the bank.": "Tak. Użyła go, by schwytać ochroniarzy w banku.",
    "Oh… Yes… That’s what we used it for.": "Och… Tak… Właśnie do tego go użyliśmy.",
    "Do you have one?": "Masz taki?",
    "I can build one. It’s simple.": "Mogę zbudować. To proste.",
    "Are you sure about this? What does encompass mean? Do the amulets need to touch her?": "Jesteś tego pewien? Co znaczy otoczyć? Czy amulety muszą jej dotknąć?",
    "No! That’s not what it said.": "Nie! Nie tak było napisane.",
    "How do we know she won't just escape?": "Skąd wiemy, że po prostu nie ucieknie?",
    "Maybe you should think about that part.": "Może powinieneś przemyśleć tę część.",
    "Show me where you saw this written down. I don’t believe a Jewish book is going to talk about a lasso.": "Pokaż mi, gdzie widziałeś to zapisane. Nie wierzę, że żydowska księga będzie mówić o lassie.",
    "It didn’t talk about a lasso! That was my idea!": "Nie było tam mowy o lassie! To był mój pomysł!",
    "Are you making this up?": "Wymyślasz to sobie?",
    "Argh! I’ll show you!": "Argh! Pokażę ci!",
    "Can we hurry this up?": "Możemy to przyspieszyć?",
    "Patience, 1Hero. The last thing we want is to give Lillian back the amulets because we didn’t know what to do with them.": "Cierpliwości, 1Hero. Ostatnią rzeczą, jakiej chcemy, to oddać Lillian amulety, bo nie wiedzieliśmy, co z nimi zrobić.",
    "He has a point.": "Ma rację.",
    "Let’s stop wasting time.": "Przestańmy marnować czas.",
    "This storm just won't stop.": "Ta burza po prostu nie chce ustać.",
    "If there’s still a world left after all of this, things are going to be different.": "Jeśli po tym wszystkim wciąż będzie istniał świat, wszystko będzie inaczej.",
    "Kimberly Foxx is going to have a lot of content for her show.": "Kimberly Foxx będzie miała mnóstwo materiału na swój program.",
    "Heh. Years worth.": "Heh. Na lata.",
    "I have to say, you’re far from boring, 1Hero.": "Muszę przyznać, że jesteś daleki od nudy, 1Hero.",
    "Aren’t you glad you realized just how amazing I am?": "Nie cieszysz się, że odkryłeś, jak niesamowity jestem?",
    "You son of a bitch.": "Ty skurwielu.",
    "1Hero? Are you going to help me or not?": "1Hero? Pomożesz mi czy nie?",
    "Oh, uhh… I just finished…": "Och, yyy… Właśnie skończyłem…",
    "Ain’t nothing to be embarrassed about.": "Nie ma się czego wstydzić.",
    "Come on… We better go keep an eye on poor Erica.": "Chodź… Lepiej miejmy oko na biedną Ericę.",
    "I hope she doesn’t tell her father what she saw.": "Mam nadzieję, że nie powie ojcu, co widziała.",
    "Hehe. I think we have bigger things to worry about.": "Hehe. Myślę, że mamy większe zmartwienia.",
    "Ugh… There’s the 1Hero I know.": "Ugh… Oto 1Hero, którego znam.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=100 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=95: raise SystemExit(f'Expected 95, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map100')
