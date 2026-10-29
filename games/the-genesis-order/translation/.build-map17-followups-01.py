#!/usr/bin/env python3
"""Build Polish drafts for Map 17 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map17-followups-01.jsonl'
TRANSLATIONS = {
    "I should go to the house and meet Heather.": "Powinienem pójść do domu i spotkać się z Heather.",
    "I should go talk to Hannah at the farm.": "Powinienem pójść porozmawiać z Hannah na farmie.",
    "I better get to Heather’s house. I don’t want to be late for dinner.": "Lepiej żebym dotarł do domu Heather. Nie chcę spóźnić się na kolację.",
    "If you’re going to be a detective, you need to know the city.": "Jeśli chcesz być detektywem, musisz znać miasto.",
    "How well do you know North Santiva?": "Jak dobrze znasz North Santivę?",
    "Time for a quiz, hot shot. If you prove yourself, I’ll give you a reward.": "Czas na quiz, chojraku. Jeśli się wykażesz, dam ci nagrodę.",
    "Good job, kid.": "Dobra robota, dzieciaku.",
    "You still got some learning to do.": "Masz jeszcze sporo do nauki.",
    "Late on a Monday?": "Spóźniony w poniedziałek?",
    "Keeping track of my hours now, Bobby?": "Liczy mi teraz godziny, Bobby?",
    "Keep it up and you won't be around long.": "Tak dalej, a długo tu nie zabawisz.",
    "Officer Rinaldi, we need to get to the warehouse soon. We don’t know how much longer she’ll be there.": "Oficerze Rinaldi, musimy niedługo dostać się do magazynu. Nie wiemy, jak długo ona tam jeszcze będzie.",
    "Did he say they are going to the warehouse?": "Czy on powiedział, że jadą do magazynu?",
    "Oh, shit! Are they arresting Jon?...": "O cholera! Aresztują Jona?...",
    "I never did check to see if Jon had a license to sell Casula artifacts…": "Nigdy nie sprawdziłem, czy Jon ma licencję na sprzedaż artefaktów Casuli…",
    "What if I’m mixed up in something illegal?": "A jeśli jestem zamieszany w coś nielegalnego?",
    "Shit… I’m already late for work. But I need to know what’s up at the warehouse.": "Cholera… już jestem spóźniony do pracy. Ale muszę się dowiedzieć, co się dzieje w magazynie.",
    "Apparently they have bigger fish to fry in there.": "Wygląda na to, że mają tam grubszą rybę do usmażenia.",
    "You’re lucky.": "Masz szczęście.",
    "I’m not out of the woods yet… I just made bail. But I think the judge likes my accent.": "Jeszcze nie wyszedłem z tego obronną ręką… ledwo wpłaciłem kaucję. Ale chyba sędzia lubi mój akcent.",
    "You don’t have anything to store away in my warehouse, do you?": "Nie masz czasem czegoś do przechowania w moim magazynie, co?",
    "That I don't, Jon.": "Nie mam, Jon.",
    "If you have any last minute treasures to sell, you better hurry. I have to be back in court in 48 hours…": "Jeśli masz jakieś skarby na ostatnią chwilę do sprzedania, lepiej się pospiesz. Za 48 godzin muszę być z powrotem w sądzie…",
    "Not sure if I’ll make it out of this one.": "Nie wiem, czy wyjdę z tego cało.",
    "Did you know they were Guild?": "Wiedziałeś, że należeli do Gildii?",
    "They never told me anything.": "Nigdy mi nic nie powiedzieli.",
    "But you knew.": "Ale wiedziałeś.",
    "That’s between me and my brain, 1Hero.": "To między mną a moim mózgiem, 1Hero.",
    "1Hero.": "1Hero.",
    "Yes, Melissa?": "Tak, Melissa?",
    "I want you to continue keeping tabs on Lillian.": "Chcę, żebyś dalej miał oko na Lillian.",
    "Am I on the Guild case now?": "Jestem teraz przy sprawie Gildii?",
    "I think there’s room for you to help David. But stay in your lane…": "Myślę, że jest miejsce, byś pomógł Davidowi. Ale trzymaj się swojego rewiru…",
    "Get comfortable with Lillian and start figuring out how much she knows.": "Zbliż się do Lillian i zacznij rozpracowywać, ile ona wie.",
    "She claims to be helping the sick. And perhaps she is…": "Twierdzi, że pomaga chorym. I może faktycznie pomaga…",
    "But I suspect there is more to the story.": "Ale podejrzewam, że to nie cała historia.",
    "What about Charles? Do you think Madalyn killed him?": "A co z Charlesem? Myślisz, że Madalyn go zabiła?",
    "We’re focusing on Lillian now.": "Teraz skupiamy się na Lillian.",
    "Any information you have, share it with David. It’s still his case.": "Jakiekolwiek informacje zdobędziesz, podziel się z Davidem. To wciąż jego sprawa.",
    "Yeah, I get it.": "Tak, rozumiem.",
    "If you want to earn my trust, don’t keep secrets from me.": "Jeśli chcesz zdobyć moje zaufanie, nie ukrywaj przede mną tajemnic.",
    "Huh? What would I be hiding?": "Słucham? Co niby miałbym ukrywać?",
    "You’re trying to go over my head, and I don’t like it.": "Próbujesz działać za moimi plecami, a ja tego nie lubię.",
    "If you know something, tell us now.": "Jeśli coś wiesz, powiedz to teraz.",
    "Don’t make me find out the hard way.": "Nie każ mi dowiadywać się na własnej skórze.",
    "Oh, uhh… Sure thing. I’m an open book.": "Och, yyy… Jasne. Jestem jak otwarta księga.",
    "I’m heading home early. I need to clean up.": "Zmykam dziś wcześniej do domu. Muszę się ogarnąć.",
    "Yeah, not sure the torn-stockings look is something you want others to see.": "Tak, nie jestem pewien czy look z podartymi pończochami to coś, co chcesz pokazywać innym.",
    "Talk to Lillian. Make up an excuse as to why we left…": "Pogadam z Lillian. Wymyśl jakąś wymówkę, dlaczego wyszliśmy…",
    "Don’t let her find out what we know.": "Nie daj jej odkryć, co wiemy.",
    "Ha! I was right! And now Melissa has no choice but to admit it to herself.": "Ha! Miałem rację! I teraz Melissa nie ma wyboru i musi przyznać to przed sobą.",
    "But the truth is, I’m still hiding information from her…": "Ale prawda jest taka, że wciąż ukrywam przed nią informacje…",
    "Lillian wants me to find amulets that are probably stolen. But if I tell her, she’s going to force me to do things her way.": "Lillian chce, żebym znalazł amulety, które pewnie są kradzione. Ale jeśli jej powiem, zmusi mnie, żebym robił wszystko po jej myśli.",
    "She talks about trusting me… I can’t trust her.": "Mówi o zaufaniu… Nie mogę jej ufać.",
    "I’m going to do things my way.": "Zrobię to po swojemu.",
    "This fire hydrant is leaking. Someone needs to tighten it with a wrench.": "Ten hydrant przecieka. Ktoś powinien dokręcić go kluczem.",
    "I can use my wrench to tighten this fire hydrant.": "Mogę użyć klucza, żeby dokręcić ten hydrant.",
    "I guess in the end, you didn’t have what it took.": "Myślę, że w końcu zabrakło ci tego, co trzeba.",
    "I wouldn’t be so sure of that.": "Nie byłbym tego taki pewien.",
    "Go fuck yourself, Bobby.": "Spierdalaj, Bobby.",
    "The electrical box is secrued with a fancy lock.": "Skrzynka elektryczna jest zabezpieczona wymyślnym zamkiem.",
    "Erica?": "Erica?",
    "1Hero! The mansion got raided.": "1Hero! Rezydencja została przeczesana.",
    "Yeah, I know. Are you okay?": "Tak, wiem. Nic ci nie jest?",
    "I’m fine, but it looks like I’m being interrogated again…": "Nic mi nie jest, ale wygląda na to, że znowu mnie przesłuchują…",
    "And Lillian… She’s gone. I haven’t seen her.": "I Lillian… Zniknęła. Nie widziałem jej.",
    "Get out of here, 1Hero. You’re not a detective anymore.": "Spadaj stąd, 1Hero. Nie jesteś już detektywem.",
    "Erica… Father Solomon needs your help.": "Erica… Ojciec Solomon potrzebuje twojej pomocy.",
    "Meet me at the church later. We need to talk.": "Spotkajmy się później w kościele. Musimy porozmawiać.",
    "I said scram!": "Mówiłem: spływaj!",
    "This damned exhaust system is rattling. What the hell do I need to secure it so it won’t rattle?": "Ten cholerny wydech grzechocze. Czym, do diabła, mam go zabezpieczyć, żeby przestał grzechotać?",
    "This is perfect! Thanks!": "To idealne! Dzięki!",
    "Here's a little reward, detective.": "Oto mała nagroda, detektywie.",
    "I lost two USB drives and I need to get them back.": "Zgubiłem dwa pendrive'y i muszę je odzyskać.",
    "What’s on them?": "Co jest na nich?",
    "None of your business!": "Nie twój interes!",
    "I see… So, what’s in it for me if I find them?": "Rozumiem… Więc co ja z tego będę miał, jeśli je znajdę?",
    "I’ll give you something in return.": "Dam ci coś w zamian.",
    "I found a USB drive upstairs.": "Znalazłem pendrive'a na górze.",
    "Nice! Here… Take this…": "Świetnie! Proszę… Weź to…",
    "Anything else?": "Coś jeszcze?",
    "Here's another USB drive.": "Oto kolejny pendrive.",
    "Great job! Take this…": "Świetna robota! Weź to…",
    "You're a lifesaver!": "Jesteś wybawcą!",
    "Any hints?": "Jakieś wskazówki?",
    "I suspect Bill and Frank from the upstairs office took them…": "Podejrzewam, że zabrali je Bill i Frank z biura na górze…",
    "Bill’s cube is the second from the right in the west wing…": "Biurko Billa to drugie od prawej w zachodnim skrzydle…",
    "Frank always has his coffee in the east wing. He sits in the middle chair at the south table.": "Frank zawsze pije kawę we wschodnim skrzydle. Siedzi na środkowym krześle przy południowym stole.",
    "Guess this is it.": "Chyba to już.",
    "Yeah, I got this. Wait for me here.": "Tak, ogarnę to. Poczekaj tu na mnie.",
    "How did it go?": "Jak poszło?",
    "Perfect. Did Arianna call?": "Idealnie. Dzwoniła Arianna?",
    "Hmm… I wonder what the hold up is.": "Hmm… Zastanawiam się, co tak trzyma.",
    "We’ve been waiting awhile.": "Czekamy już chwilę.",
    "Things got… complicated.": "Sprawy się… skomplikowały.",
    "Somehow I’m not surprised.": "Jakoś mnie to nie dziwi.",
    "She got in, but for some reason the commissioner caught her.": "Udało jej się wejść, ale z jakiegoś powodu złapał ją komisarz.",
    "She then disappeared with the laptop.": "Potem zniknęła z laptopem.",
    "That doesn’t sound so bad. Not ideal, but at least she got it.": "To nie brzmi tak źle. Nie idealnie, ale przynajmniej go zdobyła.",
    "Come on, let’s see if she came back to the house.": "Chodź, zobaczmy, czy wróciła do domu.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=17 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=100: raise SystemExit(f'Expected 100, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map17')
