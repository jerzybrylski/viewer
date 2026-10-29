#!/usr/bin/env python3
"""Build Polish drafts for Map 85 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map85-followups-01.jsonl'
TRANSLATIONS = {
    "Paul! Not now!": "Paul! Nie teraz!",
    "Hey… You’re not Paul.": "Hej… Nie jesteś Paulem.",
    "You’re no public relations expert. I can tell.": "Nie jesteś ekspertem od PR, widzę.",
    "I'll learn fast. I always do.": "Szybko się nauczę. Zawsze tak robię.",
    "There’s a symbiosis between our professions, 1Hero.": "Nasze zawody są w symbiozie, 1Hero.",
    "Is that really how you see it?": "Tak to właśnie widzisz?",
    "Let’s go. They are waiting on us.": "Chodźmy. Czekają na nas.",
    "You’re a natural, 1Hero.": "Masz talent, 1Hero.",
    "You’ll keep the public’s eyes glued to Channel 4.": "Sprawisz, że widzowie nie oderwą oczu od Channel 4.",
    "My job is to calm the public. I’m here whenever you need me.": "Moim zadaniem jest uspokajanie społeczeństwa. Jestem do dyspozycji, kiedy mnie potrzebujesz.",
    "I’m going to rely on you, 1Hero. You’re my point of contact now.": "Będę na tobie polegać, 1Hero. Jesteś teraz moim punktem kontaktowym.",
    "You said in the interview that the Guild had over 900 members. How do you know that?": "Powiedziałeś w wywiadzie, że Gildia ma ponad 900 członków. Skąd to wiesz?",
    "Leaked documents from the twelve leaders.": "Wyciekłe dokumenty od dwunastu przywódców.",
    "Twelve leaders?": "Dwunastu przywódców?",
    "I’m sure you have the same documentation at the station.": "Jestem pewna, że macie tę samą dokumentację na posterunku.",
    "Let me ask: Was there a Wilkes listed as a leader?": "Pozwól, że zapytam: Czy wśród przywódców widniał jakiś Wilkes?",
    "Only six of the twelve were identified, but I don’t recall seeing a Wilkes.": "Zidentyfikowano tylko sześciu z dwunastu, ale nie przypominam sobie Wilkesa.",
    "Are you referring to Charles Wilkes?": "Masz na myśli Charlesa Wilkesa?",
    "Nevermind. I was just wondering if your information matched ours.": "Nieważne. Zastanawiałam się tylko, czy wasze informacje pokrywają się z naszymi.",
    "Is there something happening here in North Santiva that you aren’t telling me?": "Czy dzieje się tu, w North Santiva, coś, o czym mi nie mówisz?",
    "No. Everything is fine.": "Nie. Wszystko w porządku.",
    "Let’s help each other out, 1Hero.": "Pomóżmy sobie nawzajem, 1Hero.",
    "If you find something out, give us a call.": "Jeśli się czegoś dowiesz, zadzwoń do nas.",
    "Paul can arrange an interview on short notice.": "Paul może zorganizować wywiad w krótkim czasie.",
    "I’ll keep you posted, Kimberly.": "Będę cię informować, Kimberly.",
    "Don’t forget to change back to your… street outfit.": "Nie zapomnij przebrać się z powrotem w… strój uliczny.",
    "Right. Wouldn’t want to spend the rest of the day in this noose.": "Racja. Nie chciałbym spędzić reszty dnia w tym kagańcu.",
    "And I think Andrea is impressed too.": "I myślę, że Andrea też jest pod wrażeniem.",
    "Melissa is going to hate this.": "Melissa tego znienawidzi.",
    "I hope she watches the news tonight. Her face tomorrow will be priceless.": "Mam nadzieję, że obejrzy dziś wieczorem wiadomości. Jej mina jutro będzie bezcenna.",
    "Don’t be shy, 1Hero. Off with your clothes.": "Nie wstydź się, 1Hero. Zdejmuj ubrania.",
    "So we’re changing in front of each other now?": "Więc teraz przebieramy się przy sobie?",
    "Afraid of something?": "Boisz się czegoś?",
    "Let me see it, 1Hero.": "Pokaż mi go, 1Hero.",
    "My, my. What a stud. Shame we have to cover you up for the interview": "No, no. Co za ogier. Szkoda, że musimy cię zakryć na wywiad",
    "You want a real ratings boost? I know what we could do.": "Chcesz prawdziwego skoku oglądalności? Wiem, co moglibyśmy zrobić.",
    "You’re a cocky asshole, you know that?": "Jesteś zarozumiałym dupkiem, wiesz?",
    "I’ve been told that before.": "Już mi to mówiono.",
    "I think the three of us will be getting along nicely.": "Myślę, że nasza trójka będzie się świetnie dogadywać.",
    "Of course. I look forward to working with you Miss Foxx.": "Oczywiście. Nie mogę się doczekać współpracy, panno Foxx.",
    "1Hero told me everything. This could be one of the biggest stories in decades.": "1Hero powiedział mi wszystko. To może być jeden z największych newsów od dekad.",
    "We just need time to lure them in.": "Potrzebujemy tylko czasu, by ich zwabić.",
    "That’s why this interview is so important…": "Dlatego ten wywiad jest tak ważny…",
    "If the Guild thinks we don’t know where the painting is, they are sure to ramp up their search.": "Jeśli Gildia myśli, że nie wiemy, gdzie jest obraz, na pewno zintensyfikuje poszukiwania.",
    "But you’re sure it’s in the mansion.": "Ale jesteś pewna, że jest w rezydencji.",
    "Of course. We just need them to make a move, and then we’ve got them.": "Oczywiście. Musimy tylko sprawić, by wykonali ruch, a wtedy ich mamy.",
    "I know just what to say.": "Wiem dokładnie, co powiedzieć.",
    "Go get’em, tiger. Let’s see just how much those thieves want that treasure.": "Dalej, tygrysie. Zobaczmy, jak bardzo złodzieje pragną tego skarbu.",
    "Come on. We have a schedule to maintain.": "Chodźmy. Mamy harmonogram do utrzymania.",
    "We’re coming.": "Już idziemy.",
    "Break a leg, 1Hero.": "Powodzenia, 1Hero.",
    "Go replace the wireless transmitter in the mansion. It’s either broken or out of batteries.": "Wymień bezprzewodowy nadajnik w rezydencji. Albo jest zepsuty, albo wyczerpały się baterie.",
    "You’re keeping secrets from me… But I can respect that.": "Ukrywasz przede mną sekrety… Ale mogę to uszanować.",
    "I should change before I go to the set.": "Powinnam się przebrać, zanim pójdę na plan.",
    "I suppose Erica is going to want this outfit back. But I kinda like it.": "Chyba Erica będzie chciała ten strój z powrotem. Ale całkiem mi się podoba.",
    "Are you going to stand by and let Andrea do this?": "Zamierzasz stać z boku i pozwolić Andrei na to?",
    "I have no choice… At least, not right now…": "Nie mam wyboru… Przynajmniej nie teraz…",
    "Can you trust me?": "Ufasz mi?",
    "I’m safe here, 1Hero. This place has security guards.": "Jestem tu bezpieczna, 1Hero. To miejsce ma ochronę.",
    "How are you feeling? It’s been three long months.": "Jak się czujesz? Minęły trzy długie miesiące.",
    "Horny as hell.": "Napalona jak diabli.",
    "I can’t wait to fuck everyone.": "Nie mogę się doczekać, by przelecieć wszystkich.",
    "Good timing, 1Hero.": "W samą porę, 1Hero.",
    "Your interview is coming up. We were getting worried you wouldn’t make it in time.": "Zbliża się twój wywiad. Martwiliśmy się, że nie zdążysz na czas.",
    "Interview?": "Wywiad?",
    "Today’s interview about the mansion and the Guild takedown?": "Dzisiejszy wywiad o rezydencji i rozbiciu Gildii?",
    "Sorry, Kim, but I don’t know anything about an interview today.": "Przepraszam, Kim, ale nie wiem nic o dzisiejszym wywiadzie.",
    "What? Then who’s doing the interview?": "Co? Więc kto prowadzi wywiad?",
    "1Hero! There you are!": "1Hero! Jesteś!",
    "I’m glad you made it in time.": "Cieszę się, że zdążyłeś na czas.",
    "Paul, he doesn’t know anything about the interview.": "Paul, on nic nie wie o wywiadzie.",
    "Sorry, Paul.": "Przepraszam, Paul.",
    "If it’s not you, then who’s coming?": "Jeśli to nie ty, to kto przyjdzie?",
    "Ever since Andrea left, the force has been going downhill… How unprofessional.": "Odkąd Andrea odeszła, komenda stacza się w dół… Jakie to nieprofesjonalne.",
    "1Hero’s here… Why not let him do the segment? Viewers love him!": "1Hero tu jest… Czemu nie pozwolić mu poprowadzić segmentu? Widzowie go uwielbiają!",
    "Of course! 1Hero, you should do it. Just like old times.": "Oczywiście! 1Hero, powinieneś to zrobić. Jak za dawnych czasów.",
    "Well… Don’t want to disappoint my adoring fans.": "Cóż… Nie chcę zawieść moich uwielbiających fanów.",
    "Do I have any time to prepare?": "Czy mam czas, by się przygotować?",
    "Before your interview, we have a sex segment going on.": "Przed twoim wywiadem mamy segment o seksie.",
    "A sex segment!?": "Segment o seksie!?",
    "Ratings don’t lie, 1Hero – it’s pulling in a lot of viewers.": "Oglądalność nie kłamie, 1Hero – przyciąga wielu widzów.",
    "Everyone is thinking about sex these days, it seems.": "Wszyscy ostatnio myślą o seksie, jak widać.",
    "Come on, let’s head over to the studio.": "Chodźmy, przejdźmy do studia.",
    "Somebody’s in a good mood.": "Ktoś jest w dobrym nastroju.",
    "Hell yeah! We’re a hit!": "O tak! Jesteśmy hitem!",
    "The viewers loved us!": "Widzowie nas pokochali!",
    "And I’m not getting fired!": "I nie wylecą mnie z pracy!",
    "That’s great, Kim.": "Świetnie, Kim.",
    "Another investigation reveal might be in order.": "Może przydałoby się kolejne ujawnienie śledztwa.",
    "Well… Let’s not get carried away.": "Cóż… Nie zapędzajmy się.",
    "Looking forward to the dinner meeting?": "Nie możesz się doczekać kolacji?",
    "Oh, did you hear? Lilllian teamed up with Amanda Bancroft.": "Och, słyszałeś? Lillian połączyła siły z Amandą Bancroft.",
    "No, I hadn’t. That’s a surprise.": "Nie, nie słyszałem. To niespodzianka.",
    "I didn’t know Lillian was interested in the aphrodisiac business.": "Nie wiedziałem, że Lillian interesuje się biznesem afrodyzjaków.",
    "Same.": "Ja też nie.",
    "It’s hard to imagine what a woman of her talents needs aphrodisiacs for.": "Trudno sobie wyobrazić, po co kobiecie o jej talentach afrodyzjaki.",
    "Good question.": "Dobre pytanie.",
    "Maybe she’s there to help with the Aphrosia accusation.": "Może jest tam, by pomóc w oskarżeniu o Aphrosię.",
    "Aphrosia? You mean the sex virus?": "Aphrosia? Masz na myśli wirusa seksu?",
    "Bancroft’s company made it… Or so the rumors say.": "Firma Bancroft to stworzyła… A przynajmniej tak mówią plotki.",
    "Till dinnertime, 1Hero.": "Do kolacji, 1Hero.",
    "Till then.": "Do zobaczenia.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=85 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=trans.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=102: raise SystemExit(f'Expected 102, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map85')