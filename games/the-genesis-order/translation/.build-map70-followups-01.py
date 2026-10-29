#!/usr/bin/env python3
"""Build Polish drafts for Map 70 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map70-followups-01.jsonl'
TRANSLATIONS = {
    "Diana?": "Diana?",
    "I didn’t expect to see her here.": "Nie spodziewałam się jej tutaj.",
    "Who was she?": "Kim ona była?",
    "That was Madalyn.": "To była Madalyn.",
    "Where are my clothes!?": "Gdzie moje ubrania!?",
    "Here, Judy. I have your clothes.": "Tutaj, Judy. Mam twoje ubrania.",
    "Hey! What is he doing here?": "Hej! Co on tu robi?",
    "I saw Madalyn! She was here!": "Widziałam Madalyn! Była tutaj!",
    "Why the hell is she still here?": "Czemu, do cholery, wciąż tu jest?",
    "She still has the soul inside of her.": "Wciąż ma w sobie duszę.",
    "The soul? What are you talking about?": "Duszę? O czym mówisz?",
    "It doesn’t concern you.": "To cię nie dotyczy.",
    "What has possessed her? You must tell me.": "Co nią zawładnęło? Musisz mi powiedzieć.",
    "She has a demon’s soul inside of her.": "Ma w sobie duszę demona.",
    "Sister Judy! You’re safe!": "Siostro Judy! Jesteś bezpieczna!",
    "I don’t know what happened to me. I remember Mother Superior speaking to me.": "Nie wiem, co się ze mną stało. Pamiętam, że rozmawiała ze mną Matka Przełożona.",
    "Mother Superior? She left the church with the other nuns.": "Matka Przełożona? Opuściła kościół z innymi siostrami.",
    "She’s talking about Madalyn.": "Mówi o Madalyn.",
    "The Mother Superior of Saint Dame University.": "Matka Przełożona Saint Dame University.",
    "That old woman? You saw her?": "Ta stara kobieta? Widziałaś ją?",
    "Yes! She came into the church while you were gone…": "Tak! Weszła do kościoła, gdy was nie było…",
    "I was frightened, but I do not remember much of what happened next.": "Przestraszyłam się, ale niewiele pamiętam z tego, co było potem.",
    "I can take a wild guess.": "Mogę się domyślić.",
    "She’s a succubus. Her goal is sex.": "Ona jest sukubem. Jej celem jest seks.",
    "I felt it… A sinful desire.": "Poczułam to… Grzeszne pragnienie.",
    "Are you telling me that she’s a demon?": "Mówisz, że ona jest demonem?",
    "A demi-demon.": "Pół-demonem.",
    "I know I’m a priest, but color me skeptical.": "Wiem, że jestem księdzem, ale pozwól, że będę sceptyczny.",
    "It’s all true.": "To wszystko prawda.",
    "And who are you?": "A ty kim jesteś?",
    "They are Guild people… Thieves.": "To ludzie Gildii… Złodzieje.",
    "We don’t work for the Guild!": "Nie pracujemy dla Gildii!",
    "Diana does. You can’t hide it. I saw the files.": "Diana pracuje. Nie ukryjesz tego. Widziałem akta.",
    "That was a past life…": "To było poprzednie życie…",
    "And now you’re here to kill Duncan.": "I teraz jesteście tu, by zabić Duncana.",
    "There is a demonic presence here. I’ve had visions of it.": "Jest tu demoniczna obecność. Miałem jej wizje.",
    "Whatever is here, it tried to brainwash Sister Judy.": "Cokolwiek tu jest, próbowało zrobić pranie mózgu siostrze Judy.",
    "It must be true. Father Parker… He was a monster.": "To musi być prawda. Ojciec Parker… Był potworem.",
    "The priest you thought you knew was a demon named Daemalius.": "Ksiądz, którego myślałaś, że znasz, był demonem o imieniu Daemalius.",
    "Madalyn was his sister and she took his soul…": "Madalyn była jego siostrą i zabrała jego duszę…",
    "That is how she’s able to move in and out of our world.": "Dzięki temu może przenikać między naszym światem.",
    "She moves in and out of our world?": "Przenika między naszymi światami?",
    "Think of it as teleportation.": "Pomyśl o tym jak o teleportacji.",
    "It’s true. I saw it too.": "To prawda. Też to widziałam.",
    "This all sounds super scary!": "To wszystko brzmi super strasznie!",
    "But why would she want Sister Judy?": "Ale czemu chciałaby siostry Judy?",
    "If what you say is true, we’re not exactly friendly with demonic spirits.": "Jeśli to, co mówisz, jest prawdą, nie jesteśmy zbyt przyjaźni demonicznym duchom.",
    "I’ve never performed an exorcism, but…": "Nigdy nie odprawiałem egzorcyzmu, ale…",
    "You think she’s afraid of you?": "Myślisz, że się ciebie boi?",
    "My guess is as good as yours. But I’m not going to feel safe knowing a teleporting monster is roaming the woods.": "Tyle wiem, co ty. Ale nie będę czuć się bezpiecznie, wiedząc, że teleportujący się potwór grasuje po lesie.",
    "Diana… Do you think she’s looking for us?": "Diana… Myślisz, że ona nas szuka?",
    "What more can she want from us?": "Czego więcej może od nas chcieć?",
    "Sounds like Sister Judy isn’t the only one that has a history with Madalyn.": "Wygląda na to, że siostra Judy nie jest jedyną, która ma przeszłość z Madalyn.",
    "Madalyn is connected to the Guild.": "Madalyn jest powiązana z Gildią.",
    "Because her husband was an Eclipse Guild leader…": "Bo jej mąż był przywódcą Gildii Zaćmienia…",
    "Charles Wilkes.": "Charles Wilkes.",
    "Congratulations, detective. Looks like you’ve figured it out.": "Gratulacje, detektywie. Wygląda na to, że rozgryzłeś to.",
    "I don’t get it. Madalyn comes here to use Charles and then kill him.": "Nie rozumiem. Madalyn przychodzi tu, wykorzystuje Charlesa, a potem go zabija.",
    "What did she gain from him and why is she still here?": "Co na nim zyskała i czemu wciąż tu jest?",
    "I’m on the case. But it would help if you were honest with me.": "Prowadzę sprawę. Ale byłoby łatwiej, gdybyś była ze mną szczera.",
    "If you think we’re thieves, then why would we tell you anything?": "Jeśli uważasz, że jesteśmy złodziejami, to czemu mielibyśmy ci cokolwiek mówić?",
    "Are you?": "A jesteście?",
    "You know why we’re here… We’re here for Duncan.": "Wiesz, dlaczego tu jesteśmy… Jesteśmy tu dla Duncana.",
    "You think the Guild is dying? It’s only changing leadership.": "Myślisz, że Gildia umiera? Tylko zmienia przywództwo.",
    "So Duncan is taking over where Charles left off?": "Więc Duncan przejmuje tam, gdzie skończył Charles?",
    "Yes. Isn’t it obvious?": "Tak. Czy to nie oczywiste?",
    "If Charles was a Guild leader, where are his subordinates? Where are the other Guild members?": "Jeśli Charles był przywódcą Gildii, gdzie są jego podwładni? Gdzie są pozostali członkowie Gildii?",
    "The Guild is still operating here. And it’s not going away until Duncan Helmer is dead.": "Gildia wciąż tu działa. I nie zniknie, dopóki Duncan Helmer nie zginie.",
    "Come on, Diana. We don’t need his help.": "Chodź, Diana. Nie potrzebujemy jego pomocy.",
    "I can grant you immunity.": "Mogę załatwić wam immunitet.",
    "Nice try, detective.": "Niezła próba, detektywie.",
    "We don’t believe you.": "Nie wierzymy ci.",
    "Are they working on the same case as you, 1Hero?": "Czy oni pracują nad tą samą sprawą co ty, 1Hero?",
    "Those people aren’t detectives, dear.": "Ci ludzie nie są detektywami, kochanie.",
    "They have connections to a criminal organization.": "Mają powiązania z organizacją przestępczą.",
    "You didn’t arrest them?": "Nie aresztowałeś ich?",
    "This case is complicated. It’s hard to explain.": "Ta sprawa jest skomplikowana. Trudno wyjaśnić.",
    "Going off the books, 1Hero?": "Działasz poza protokołem, 1Hero?",
    "Come on. Let’s get Sister Judy back inside.": "Chodź. Odprowadźmy siostrę Judy do środka.",
    "Thank you for coming to my rescue. I am fortunate to have such caring people in my life.": "Dziękuję, że przyszliście mi na ratunek. Mam szczęście, że mam w życiu tak troskliwych ludzi.",
    "Of course, Judy. We couldn’t let anything bad happen to you.": "Oczywiście, Judy. Nie mogliśmy pozwolić, by stało ci się coś złego.",
    "Those bees look angry. I better keep my distance.": "Te pszczoły wyglądają na wściekłe. Lepiej trzymać dystans.",
    "I can use my blow torch to smoke out the bees.": "Mogę użyć palnika, żeby wykurzyć pszczoły dymem.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=70 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=83: raise SystemExit(f'Expected 83, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map70')
