#!/usr/bin/env python3
"""Build Polish drafts for Map 128 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map128-followups-01.jsonl'
TRANSLATIONS = {
    "Andrea, I can explain!": "Andrea, mogę wyjaśnić!",
    "Explain what? There is nothing that can be done now.": "Co tu wyjaśniać? Teraz już nic się nie da zrobić.",
    "It was a one-time thing… It won't happen again.": "To był jednorazowy wybryk… Już się nie powtórzy.",
    "It’s not true! That was Ella’s account!": "To nieprawda! To było konto Elli!",
    "It doesn’t matter. You can't be the face of the operation anymore.": "Nieważne. Nie możesz już być twarzą operacji.",
    "What a vulture… Foxx can’t help herself.": "Co za sęp… Foxx nie potrafi się powstrzymać.",
    "Well… What now?": "No więc… Co teraz?",
    "You’re fired.": "Jesteś zwolniony.",
    "We’re going in a new direction.": "Idziemy w nowym kierunku.",
    "But, Andrea…": "Ale, Andrea…",
    "You’re on my undercover team now. We can use this to disconnect you from the station.": "Jesteś teraz w moim zespole pod przykrywką. Możemy wykorzystać to, by odciąć cię od stacji.",
    "It means you’ll be operating under a new set of rules.": "To oznacza, że będziesz działać według nowych zasad.",
    "You’re a rogue agent now. You’ll follow my lead.": "Jesteś teraz agentem-rogue. Będziesz podążać za mną.",
    "Rogue agent?": "Agentem-rogue?",
    "Meet me at my home later this afternoon. I’ve got a mission for you and Nellie…": "Spotkajmy się u mnie dziś po południu. Mam misję dla ciebie i Nellie…",
    "You two are going to finish this.": "Wy to dokończycie.",
    "Clean out your desk. You’re off the force…": "Wyczyść biurko. Wylatujesz ze służby…",
    "You’re going to be escorted off the premises.": "Zostaniesz wyprowadzony z budynku.",
    "Fuck… I’m sorry, Andrea.": "Cholera… Przepraszam, Andrea.",
    "God damn it… Serves me right for trusting that Tasha girl.": "Cholera jasna… Dobrze mi tak, że zaufałem tej dziewczynie Taszy.",
    "Why the hell did she record us?": "Czemu, do cholery, nas nagrywała?",
    "I’m sorry, Andrea.": "Przepraszam, Andrea.",
    "Ready for a new day, Canmore?": "Gotowy na nowy dzień, Canmore?",
    "Andrea… We need to talk.": "Andrea… Musimy porozmawiać.",
    "Lillian.": "Lillian.",
    "Elaborate.": "Rozwiń.",
    "Erica… Lillian’s maid and the priest from Eve Cathedral… They went to check up on her.": "Erica… pokojówka Lillian i ksiądz z katedry Eve… Poszli ją sprawdzić.",
    "Duncan has new goons and the mansion is crawling with them…": "Duncan ma nowych zbirów i rezydencja aż się od nich roi…",
    "They got captured and we had to break out.": "Zostali złapani i musieliśmy się wyrwać.",
    "We? You got captured?": "My? Dałeś się złapać?",
    "You know Duncan is there. Tell me what’s going on.": "Wiesz, że Duncan tam jest. Powiedz mi, co się dzieje.",
    "What did you expect? We had to find Lillian.": "Czego się spodziewałeś? Musieliśmy odnaleźć Lillian.",
    "That woman has disappeared. She’s probably not even at the mansion.": "Ta kobieta zniknęła. Pewnie nawet nie ma jej w rezydencji.",
    "That’s not true. She was hiding.": "To nieprawda. Ukrywała się.",
    "You found her?": "Znaleźliście ją?",
    "We did and she was chased away… We don’t know where she is now.": "Tak, ale została przegnana… Nie wiemy, gdzie teraz jest.",
    "Father Solomon and Erica are now in danger. Duncan knows about them.": "Ojciec Solomon i Erica są teraz w niebezpieczeństwie. Duncan o nich wie.",
    "They aren’t in danger. I’ll handle this.": "Nie są w niebezpieczeństwie. Ja się tym zajmę.",
    "Forgive me for not simply trusting you, but these people are innocent bystanders. I need to know exactly what’s going on.": "Wybacz, że tak po prostu ci nie ufam, ale to niewinni ludzie. Muszę wiedzieć dokładnie, co się dzieje.",
    "Very well…": "Dobrze…",
    "I’ll go to the cathedral and personally meet with the priest.": "Pójdę do katedry i osobiście spotkam się z księdzem.",
    "Will you bring officers?": "Zabierzesz funkcjonariuszy?",
    "That won't be necessary.": "Nie będzie to konieczne.",
    "Because I have Duncan under tight control.": "Bo mam Duncana pod ścisłą kontrolą.",
    "You’re controlling Duncan?": "Kontrolujesz Duncana?",
    "Trust me. He won’t be bothering them anymore.": "Zaufaj mi. Nie będzie już ich niepokoić.",
    "Move along, 1Hero. I have other work to attend to.": "Idź dalej, 1Hero. Mam inne sprawy.",
    "Andrea… Duncan wasn’t there.": "Andrea… Duncana tam nie było.",
    "Here she is, commissioner.": "Oto ona, pani komisarz.",
    "Leave us.": "Zostaw nas.",
    "The cops showed up! I shot at them, but…": "Gliniarze się zjawili! Strzelałem do nich, ale…",
    "They are still alive!": "Wciąż żyją!",
    "They got arrested. What else could we have done?": "Zostali aresztowani. Co innego mogliśmy zrobić?",
    "What the hell was Bhatt doing at the warehouse?": "Co, do cholery, robiła Bhatt w magazynie?",
    "She tells me an anonymous tip came in about Jon’s warehouse…": "Mówi, że wpłynął anonimowy tip o magazynie Jona…",
    "Must have been a coincidence.": "Musiało to być przypadek.",
    "I don’t believe in coincidences…": "Nie wierzę w przypadki…",
    "Paul must have been listening on the scanner too… Damn.": "Paul musiał też nasłuchiwać skanera… Cholera.",
    "The place was packed. It didn’t go down like you said.": "Miejsce było nabite. Nie poszło tak, jak mówiłaś.",
    "Even if it had, Duncan was missing. Sounds like the whole plan failed on that front…": "Nawet gdyby poszło, Duncana brakowało. Wygląda na to, że cały plan zawalił się na tym froncie…",
    "But what does it matter now? We need to find Duncan.": "Ale jakie to ma teraz znaczenie? Musimy znaleźć Duncana.",
    "Kimberly is going to want an interview and we’re not telling her about Duncan…": "Kimberly będzie chciała wywiadu, a my nie mówimy jej o Duncanie…",
    "The case is closed today.": "Sprawa jest dziś zamknięta.",
    "We’re still interrogating his goons.": "Wciąż przesłuchujemy jego ludzi.",
    "You’re not doing anything, 1Hero.": "Ty nic nie robisz, 1Hero.",
    "It doesn’t matter what they say. The Guild dies tonight.": "Nieważne, co powiedzą. Gildia umiera dziś wieczorem.",
    "Does this mean I’m a free woman?": "Czy to oznacza, że jestem wolną kobietą?",
    "You didn’t obey orders.": "Nie wykonałaś rozkazów.",
    "Hey! I did my best!": "Hej! Starałam się jak mogłam!",
    "This isn’t over for you, Miss Cole.": "To jeszcze nie koniec, panno Cole.",
    "Is the Guild operation finished? What about the bigger team? There are more of us, right?": "Czy operacja Gildii jest zakończona? A co z większą ekipą? Jest nas więcej, prawda?",
    "Don’t worry about anyone but yourself, 1Hero. I’ll deal with closing the case.": "Nie martw się o nikogo poza sobą, 1Hero. Ja zajmę się zamknięciem sprawy.",
    "Let me go on the news. I can spin a story that’ll keep everyone off your tail.": "Pozwól mi wystąpić w wiadomościach. Mogę ukręcić historię, która odciągnie od ciebie wszystkich.",
    "Absolutely not. 1Hero can handle this.": "Absolutnie nie. 1Hero sobie z tym poradzi.",
    "It just so happens that Kimberly is interested in a live interview.": "Tak się składa, że Kimberly jest zainteresowana wywiadem na żywo.",
    "Then our future here is on your shoulders.": "Więc nasza przyszłość spoczywa na twoich barkach.",
    "You need to finish this.": "Musisz to dokończyć.",
    "If the Guild case is closed, what the hell am I supposed to do now?": "Jeśli sprawa Gildii jest zamknięta, to co ja mam, do cholery, teraz robić?",
    "I’ve got plans.": "Mam plany.",
    "Well… While you have plans, I've lost my place to stay.": "Cóż… Póki ty masz plany, ja straciłam dach nad głową.",
    "You’ll come home with me. We can discuss our future there.": "Zamieszkasz ze mną. Możemy tam omówić naszą przyszłość.",
    "You promised my record would be cleared.": "Obiecałaś, że moja kartoteka zostanie wyczyszczona.",
    "And you promised to kill Duncan’s henchmen.": "A ty obiecałeś zabić ludzi Duncana.",
    "It’s time to leave…": "Czas ruszać…",
    "You know what to do, right, 1Hero?": "Wiesz, co robić, prawda, 1Hero?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=128 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=85: raise SystemExit(f'Expected 85, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map128')
