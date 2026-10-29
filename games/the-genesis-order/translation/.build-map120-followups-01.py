#!/usr/bin/env python3
"""Build Polish drafts for Map 120 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map120-followups-01.jsonl'
TRANSLATIONS = {
    "Detective? Where are you going?": "Detektywie? Dokąd idziesz?",
    "I don’t see anything. What’s she going to show me?": "Nic nie widzę. Co ona chce mi pokazać?",
    "Is this a secret door?...": "Czy to sekretne drzwi?...",
    "Something seems off.": "Coś jest nie tak.",
    "What I am about to show you must remain a secret between us. Do you understand?": "To, co zaraz ci pokażę, musi pozostać tajemnicą między nami. Rozumiesz?",
    "Yes. I’m ready.": "Tak. Jestem gotowy.",
    "I knew it. A secret room.": "Wiedziałam. Sekretny pokój.",
    "This is the painting?": "To ten obraz?",
    "The Storm on the Sea of Galilee, painted in 1633 and stolen by the Eclipse Guild in 1990.": "Burza na Morzu Galilejskim, namalowany w 1633 i skradziony przez Gildię Zaćmienia w 1990.",
    "How the hell did you find it?": "Jak, do cholery, go znaleźliście?",
    "We searched the mansion.": "Przeszukaliśmy rezydencję.",
    "Without a warrant?": "Bez nakazu?",
    "Careful, 1Hero. You’ve graduated to the next level…": "Ostrożnie, 1Hero. Awansowałeś na kolejny poziom…",
    "Not everything we do is by the rules.": "Nie wszystko, co robimy, jest zgodne z zasadami.",
    "So, was Duncan looking for it?": "Więc Duncan go szukał?",
    "Doubtful. His plans were much larger. But with this painting, we have what we need to pin him on the theft.": "Wątpliwe. Jego plany były znacznie większe. Ale dzięki temu obrazowi mamy to, czego potrzeba, by przypiąć mu kradzież.",
    "And just like that, the Guild is done and no one's the wiser that they’ve been operating here all along.": "I tak po prostu Gildia jest skończona i nikt nie dowie się, że cały czas tu działali.",
    "A simple, easy to digest story. We’ll look like heroes and the city will go on like nothing ever happened.": "Prosta, łatwa do przełknięcia historia. Wyjdziemy na bohaterów, a miasto będzie żyć, jakby nic się nie stało.",
    "Damn… We’re looking at a ten million dollar painting.": "Cholera… Patrzymy na obraz wart dziesięć baniek.",
    "Beautiful, isn’t it?": "Piękny, prawda?",
    "What’s next?": "Co dalej?",
    "Your interview with Kimberly airs tonight. We will inform Channel 4 that we have the painting and soon you’ll reveal it to the public.": "Twój wywiad z Kimberly leci dziś wieczorem. Poinformujemy Channel 4, że mamy obraz i wkrótce ujawnicie go publicznie.",
    "How soon?": "Jak szybko?",
    "We will let the story sit for a little while longer.": "Niech historia jeszcze trochę poleży.",
    "Why not move now?": "Czemu nie działać teraz?",
    "We’re scratching Paul’s back, so he’ll continue to scratch ours.": "Robimy przysługę Paulowi, więc on nadal będzie robić przysługi nam.",
    "You’re going to leave the hunt for the painting in the news cycle while Duncan is still out there?": "Zamierzacie zostawić polowanie na obraz w cyklu informacyjnym, podczas gdy Duncan wciąż jest na wolności?",
    "We will keep a police presence at the church and the mansion. People will stay safe.": "Zostawimy obecność policji w kościele i rezydencji. Ludzie będą bezpieczni.",
    "What’s Duncan’s ultimate plan? Why is he really here?": "Jaki jest ostateczny plan Duncana? Po co tu naprawdę jest?",
    "He’s here to take over where Charles left off.": "Jest tu, by przejąć tam, gdzie skończył Charles.",
    "So Charles was the leader all along?": "Więc Charles był przywódcą od początku?",
    "One of many, 1Hero.": "Jednym z wielu, 1Hero.",
    "How long have you known?": "Jak długo wiedziałaś?",
    "Since investigating his death. My team has gathered a lot of info that you’re not privy to.": "Od śledztwa w sprawie jego śmierci. Mój zespół zebrał sporo informacji, do których nie masz dostępu.",
    "Who all is on this team apart from Nellie? Are those treasure hunters on your team?": "Kto jest w tym zespole oprócz Nellie? Czy ci łowcy skarbów są w twoim zespole?",
    "The identities of the infiltrators will never be known to anyone but myself. It’s important…": "Tożsamości infiltratorów nigdy nie będą znane nikomu poza mną. To ważne…",
    "I hope you understand.": "Mam nadzieję, że rozumiesz.",
    "I’ll be honest with you, Andrea. I’m a nosy guy.": "Będę z tobą szczery, Andrea. Jestem wścibski.",
    "You’re a man whose potential has been squandered. I see it in you. I know you feel the same way.": "Jesteś człowiekiem, którego potencjał został zmarnowany. Widzę to w tobie. Wiem, że czujesz to samo.",
    "So this is it, then. This is how we operate.": "Więc tak to jest. Tak działamy.",
    "It should go without saying that not a word should be spoken about this painting until the time is right.": "Nie muszę mówić, że ani słowa o tym obrazie, dopóki nie nadejdzie właściwy moment.",
    "If any thief knew this was here, my life would be at risk.": "Gdyby którykolwiek złodziej wiedział, że tu jest, moje życie byłoby zagrożone.",
    "Of course. I won’t say anything.": "Oczywiście. Nikomu nie powiem.",
    "If Kimberly asks, tell her we’re still searching the mansion, but we’re positive it’s there.": "Jeśli Kimberly zapyta, powiedz, że wciąż przeszukujemy rezydencję, ale jesteśmy pewni, że tam jest.",
    "They want this story. We’ll give them everything they need… Just not now.": "Chcą tę historię. Damy im wszystko, czego potrzebują… Tylko nie teraz.",
    "Enjoy your weekend, 1Hero. What’s left of it.": "Miłego weekendu, 1Hero. Tego, co z niego zostało.",
    "Holy shit. What have I gotten myself into?": "O cholera. W co ja się wpakowałem?",
    "I want to climb the ladder, but this isn’t what I expected.": "Chcę piąć się po szczeblach, ale nie tego się spodziewałem.",
    "Damn. I’m looking at ten million dollars.": "Cholera. Patrzę na dziesięć baniek.",
    "What’s up with this place? Where is Kimura living now?": "Co jest z tym miejscem? Gdzie teraz mieszka Kimura?",
    "I’d like you to take inventory of what’s in this room… Need to make sure nothing goes missing.": "Chciałabym, żebyś zrobił inwentaryzację tego, co jest w tym pokoju… Musimy dopilnować, żeby nic nie zginęło.",
    "Will do, detective.": "Zrobi się, detektywie.",
    "I’m working on the inventory, detective.": "Pracuję nad inwentaryzacją, detektywie.",
    "Hello, officer. Have you completed inventory?": "Witaj, funkcjonariuszu. Skończyłeś inwentaryzację?",
    "Yes, detective. There was some kind of Guild document I found.": "Tak, detektywie. Znalazłem jakiś dokument Gildii.",
    "What the hell does this mean?": "Co to, do cholery, znaczy?",
    "What kind of special code would young Kirk Chesterfield have used?": "Jakiego specjalnego kodu użyłby młody Kirk Chesterfield?",
    "Nellie and Andrea probably wouldn’t know, since it was so long ago.": "Nellie i Andrea pewnie nie wiedziałyby, bo było to tak dawno.",
    "Good luck with your case, detective.": "Powodzenia w sprawie, detektywie.",
    "1Hero!": "1Hero!",
    "How’s it going, ladies?": "Co słychać, panie?",
    "We’re talking about fucking.": "Gadamy o pieprzeniu.",
    "And toys.": "I o zabawkach.",
    "Always a fun topic.": "Zawsze fajny temat.",
    "But I thought you were bored with sex, Arianna?": "Ale myślałam, że znudził ci się seks, Arianna?",
    "That’s why we’re talking about toys.": "Dlatego gadamy o zabawkach.",
    "There’s a lot out there. We can order some interesting stuff for the shop.": "Sporo tego jest. Możemy zamówić coś ciekawego do sklepu.",
    "Like double-sided dildos!": "Jak dwustronne dildo!",
    "Really big ones!": "Naprawdę duże!",
    "It’ll be hard to find something Henry’s size, you know.": "Trudno będzie znaleźć coś w rozmiarze Henry’ego, wiesz.",
    "I wish I could touch him.": "Chciałabym go dotknąć.",
    "And his magnificent cock.": "I jego wspaniałego kutasa.",
    "There might be a way.": "Może jest sposób.",
    "Arianna could bring you to Hell with her.": "Arianna mogłaby zabrać cię do piekła ze sobą.",
    "That way, you could touch Henry.": "Wtedy mogłabyś dotknąć Henry’ego.",
    "Really!? Can we do that?": "Naprawdę!? Możemy to zrobić?",
    "As long as you aren’t afraid of going to Hell.": "Dopóki nie boisz się iść do piekła.",
    "I think I could handle that.": "Chyba dałabym radę.",
    "That would be amazing!": "To byłoby niesamowite!",
    "I’ll be back later.": "Wrócę później.",
    "Let’s talk then about some toy ideas.": "Pogadammy wtedy o pomysłach na zabawki.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=120 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=81: raise SystemExit(f'Expected 81, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map120')
