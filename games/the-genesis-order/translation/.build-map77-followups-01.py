#!/usr/bin/env python3
"""Build Polish drafts for Map 77 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map77-followups-01.jsonl'
TRANSLATIONS = {
    "You almost got me killed.": "Mało brakowało, a byś mnie zabił.",
    "What the hell are you talking about? Where were you?": "O czym ty, do cholery, mówisz? Gdzie byłeś?",
    "I was in Duncan’s lair, with a gun to my head.": "Byłem w legowisku Duncana, z lufą przy głowie.",
    "I told you to keep an eye on Duncan, not try and arrest him.": "Kazałem ci mieć Duncana na oku, nie próbować go aresztować.",
    "If it wasn’t for Nellie, I’d be dead… And I don’t know how much longer she can stay undercover…": "Gdyby nie Nellie, byłbym martwy… I nie wiem, jak długo jeszcze da radę działać pod przykrywką…",
    "This has to end now.": "To musi się teraz skończyć.",
    "You’re not calling the shots, 1Hero. Know your place.": "To nie ty tu wydajesz rozkazy, 1Hero. Znaj swoje miejsce.",
    "Treasure hunters have infiltrated the bunker. They plan to kill Duncan.": "Łowcy skarbów przeniknęli do bunkra. Planują zabić Duncana.",
    "Infiltrated? How the hell do you know that?": "Przeniknęli? Skąd, do cholery, to wiesz?",
    "I saw one of them while I was escaping.": "Widziałem jednego z nich, gdy uciekałem.",
    "There’s nothing interesting about this. We need to infiltrate that bunker now!...": "W tym nie ma nic ciekawego. Musimy przeniknąć do bunkra teraz!...",
    "People’s lives are at risk.": "Życie ludzi jest zagrożone.",
    "Calm down. You’re getting emotional.": "Spokojnie. Robisz się emocjonalny.",
    "What’s the plan? Tell me.": "Jaki jest plan? Mów.",
    "I’ve got good news… One of the undercover team has found something in Charles’ mansion.": "Mam dobre wieści… Jeden z zespołu pod przykrywką coś znalazł w rezydencji Charlesa.",
    "Really? What did they find?": "Naprawdę? Co znaleźli?",
    "Something that will give us a big public relations win.": "Coś, co da nam duży PR-owy sukces.",
    "I’m not going to sit back and watch innocent people die just for PR wins.": "Nie będę siedział bezczynnie i patrzył, jak giną niewinni tylko dla PR-owych zwycięstw.",
    "Don’t disappoint me, 1Hero. I chose you for a reason.": "Nie zawiedź mnie, 1Hero. Wybrałem cię nie bez powodu.",
    "Because I look good on camera?": "Bo dobrze wyglądam na kamerze?",
    "Wait here. I think we need to take things to the next level.": "Poczekaj. Myślę, że musimy wejść na kolejny poziom.",
    "Now, I owe you the plan. Isn’t that right?": "Teraz jestem ci winna plan. Zgadza się?",
    "How are we taking him down? I’m ready.": "Jak go dopadniemy? Jestem gotowa.",
    "Go upstairs. I’ll meet you there shortly.": "Idź na górę. Wkrótce do ciebie dołączę.",
    "Shit... I can’t think with my cock…": "Cholera… Nie mogę myśleć, gdy mój fiut…",
    "If she doesn’t have answers…": "Jeśli ona nie ma odpowiedzi…",
    "Could I just walk away?": "Mógłbym po prostu odejść?",
    "If Kimberly asks, tell her we’re still searching the mansion, but we’re positive the painting is there.": "Jeśli Kimberly zapyta, powiedz, że wciąż przeszukujemy rezydencję, ale jesteśmy pewni, że obraz tam jest.",
    "You’re early.": "Wcześnie jesteś.",
    "You fired me. I’m bored.": "Wyrzuciłaś mnie. Nudzę się.",
    "Come, 1Hero. We should celebrate.": "Chodź, 1Hero. Powinniśmy świętować.",
    "Celebrate?": "Świętować?",
    "The end of the Guild case.": "Koniec sprawy Gildii.",
    "It will be after you and Nellie do your job.": "Będzie po tym, jak ty i Nellie wykonacie robotę.",
    "And what job would that be?": "A jaka to robota?",
    "Not so fast, 1Hero. Let’s wait for Nellie to get here before we go discussing details.": "Nie tak szybko, 1Hero. Poczekajmy, aż Nellie tu dotrze, zanim zaczniemy omawiać szczegóły.",
    "Want a drink?": "Napijesz się?",
    "If you’re offering.": "Jeśli stawiasz.",
    "Who can afford to buy this place now that it’s for sale?... Doesn’t Kimura want her stuff?": "Kogo stać teraz na kupno tego miejsca, skoro jest na sprzedaż?... Kimura nie chce swoich rzeczy?",
    "Good to see you could make it, David.": "Dobrze, że udało ci się dotrzeć, David.",
    "Free food is hard to say no to.": "Trudno odmówić darmowemu jedzeniu.",
    "Quite a nice house you have.": "Całkiem ładny dom masz.",
    "Thanks! It was a little pricey, but worth it.": "Dzięki! Był trochę drogi, ale warto było.",
    "Mm-hmm, a very, very nice house for a detective.": "Mhm, bardzo, bardzo ładny dom jak na detektywa.",
    "The free food is that way.": "Darmowe jedzenie tam.",
    "I hope there’s cherries with sugar.": "Mam nadzieję, że są wiśnie z cukrem.",
    "Ella!": "Ella!",
    "In the flesh!": "We własnej osobie!",
    "Wow, this is a pleasant surprise.": "Łał, co za miła niespodzianka.",
    "When I heard you were having a shindig, I knew I just had to make an appearance.": "Gdy usłyszałam, że robisz imprezę, wiedziałam, że muszę się pojawić.",
    "You’re definitely welcome.": "Jesteś zdecydowanie mile widziana.",
    "So you bought Andrea’s mansion, huh?": "Więc kupiłeś rezydencję Andrei, huh?",
    "The treasure hunting business must be going well.": "Biznes łowców skarbów musi iść dobrze.",
    "I like to say I’m really good at investing.": "Lubię mówić, że jestem naprawdę dobry w inwestowaniu.",
    "Of course, investing.": "Oczywiście, inwestowaniu.",
    "Well, don’t be a stranger–the party’s that way.": "Cóż, nie bądź obcy — impreza tam.",
    "Nice pad, 1Hero. Moving up in the world, I see.": "Niezłe mieszkanko, 1Hero. Pniecie się w górę, widzę.",
    "Life has been good to me of late.": "Ostatnio życie mnie rozpieszcza.",
    "Glad you could make it from Osira.": "Cieszę się, że mogłeś przybyć z Osiry.",
    "I understand you’re a busy person now.": "Rozumiem, że jesteś teraz zajętą osobą.",
    "The aphrodisiac business is booming, it’s true.": "Biznes afrodyzjakowy kwitnie, to prawda.",
    "Yet a break once in a while is desirable.": "A przerwa od czasu do czasu jest pożądana.",
    "I’d like to hear more about how your work is going.": "Chciałbym usłyszeć więcej o tym, jak idzie ci praca.",
    "You have quite a crowd growing in the next room. Perhaps you should check on them.": "Masz całkiem spory tłum w sąsiednim pokoju. Może powinieneś ich sprawdzić.",
    "Anytime you want, you’re welcome to come use the jacuzzi.": "Kiedy tylko chcesz, możesz wpaść skorzystać z jacuzzi.",
    "Hello!": "Halo!",
    "Enjoy the party?": "Dobra impreza?",
    "Yeah, it was fun.": "Tak, była fajna.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=77 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=68: raise SystemExit(f'Expected 68, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map77')
