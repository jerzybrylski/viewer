#!/usr/bin/env python3
"""Build Polish drafts for Map 202 follow-ups (LLM, kontekst)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map202-followups-01.jsonl'
TRANSLATIONS = {
    "Up there. See it?": "Tam na górze. Widzisz to?",
    "What, exactly?": "Co dokładnie?",
    "Who…": "Kto…",
    "Shhh…": "Ciii…",
    "It’s been too long. She’s not returning.": "Minęło za dużo czasu. Ona nie wróci.",
    "Have faith, brother. She has a plan.": "Miej wiarę, bracie. Ona ma plan.",
    "We must act.": "Musimy działać.",
    "And what would you suggest we do?": "A co proponujesz, żebyśmy zrobili?",
    "We still have the Anachorismos.": "Wciąż mamy Anachorismos.",
    "We will not use the Anachorismos. It was not her plan.": "Nie użyjemy Anachorismos. To nie był jej plan.",
    "We will give her one more week. If she does not return, we are using it.": "Damy jej jeszcze tydzień. Jeśli nie wróci, użyjemy go.",
    "You play with fire, brother.": "Igrasz z ogniem, bracie.",
    "I want it!": "Ja to chcę!",
    "Ella, that’s a bad idea.": "Ella, to zły pomysł.",
    "Don’t you see that big, ugly guy, and that demon?": "Nie widzisz tego wielkiego, brzydkiego faceta i tego demona?",
    "Nothing we can’t handle.": "Damy sobie radę.",
    "Ella!": "Ella!",
    "Don’t let him sound an alarm!": "Nie pozwól mu wszcząć alarmu!",
    "1Hero!": "1Hero!",
    "Duncan!": "Duncan!",
    "Lillian brought me here. She’s a demon! This is Hell!": "Lillian mnie tu sprowadziła. Ona jest demonem! To jest Piekło!",
    "Where is the Toma? Have you seen it?": "Gdzie jest Toma? Widziałeś ją?",
    "Why would I tell you?": "Czemu miałbym ci powiedzieć?",
    "We’ll kill you!": "Zabijemy cię!",
    "Come here.": "Chodź tu.",
    "See that box?": "Widzisz to pudło?",
    "What about it?": "Co z nim?",
    "The Toma Leolo is inside of there… I’ve been trying to get to it.": "Toma Leolo jest w środku… Próbuję się do niej dostać.",
    "Why do you care about it? How would you use it?": "Czemu ci na niej zależy? Jak chciałbyś jej użyć?",
    "Thanks to you and Henry, my Guild is all but dead…": "Przez ciebie i Henry’ego moja Gildia jest praktycznie martwa…",
    "That creepy statue can make me a new army… A better army.": "Ta upiorna statua może stworzyć dla mnie nową armię… Lepszą armię.",
    "You’re insane! We’re going to destroy it!": "Oszalałeś! Zamierzamy to zniszczyć!",
    "Like hell, you are!": "A właśnie że nie!",
    "Is it locked? Why can’t you get it?": "Jest zamknięte? Czemu nie możesz jej zdobyć?",
    "Locked tight… I can’t pick it.": "Zamknięte na głucho… Nie potrafię tego otworzyć.",
    "Where are the other demons? What is this place?": "Gdzie są inne demony? Co to za miejsce?",
    "It’s a temple… The little ones use it.": "To świątynia… Mali tego używają.",
    "This is crazy. Let’s get that Toma and get out of here.": "To szaleństwo. Weźmy tę Tomę i wynośmy się stąd.",
    "What makes you think you can reach it?": "Co ci każe myśleć, że dasz radę ją dosięgnąć?",
    "We’re smarter than you.": "Jesteśmy sprytniejsi od ciebie.",
    "Hahaha!": "Hahaha!",
    "Duncan… You’re crazy. Lilith is not going to let you use the Toma to make an army.": "Duncan… Oszalałeś. Lilith nie pozwoli ci użyć Tomy do stworzenia armii.",
    "On the contrary, that’s exactly the plan.": "Wręcz przeciwnie, dokładnie taki jest plan.",
    "Enough chitchat. Keep an eye on Duncan… I’ll pick the lock.": "Dość pogaduch. Miej oko na Duncana… Ja otworzę zamek.",
    "I’m not going anywhere… Be my guest.": "Nigdzie się nie wybieram… Proszę bardzo.",
    "Let’s hurry this up.": "Pospieszmy się z tym.",
    "I told you it would be no big deal.": "Mówiłem ci, że to żaden problem.",
    "So, now what? Are you going to sell it?": "I co teraz? Zamierzasz to sprzedać?",
    "I have no idea. But this place is a treasure trove.": "Nie mam pojęcia. Ale to miejsce to skarbnica.",
    "Andrea sent you here, didn’t she?": "To Andrea cię tu przysłała, prawda?",
    "Not this time, 1Hero.": "Nie tym razem, 1Hero.",
    "We’re already in Hell… If I kill him, where will he go?": "Już jesteśmy w Piekle… Jeśli go zabiję, dokąd trafi?",
    "Don’t kill him.": "Nie zabijaj go.",
    "Unless you know how to open that gate, leave me alone.": "Chyba że wiesz, jak otworzyć tę bramę, zostaw mnie w spokoju.",
    "You and I can be kings, 1Hero… And Lilith will be our queen.": "Ty i ja możemy być królami, 1Hero… A Lilith będzie naszą królową.",
    "That’s not happening.": "Nic z tego.",
    "The longer this takes, the riskier it gets.": "Im dłużej to trwa, tym większe ryzyko.",
    "Now let’s get the hell out of here.": "A teraz wynośmy się stąd w cholerę.",
    "How do we know the Toma is actually inside that box?": "Skąd wiemy, że Toma naprawdę jest w tym pudle?",
    "I have an idea of how we can figure it out.": "Mam pomysł, jak możemy to sprawdzić.",
    "Why don’t you look inside and see, Johnson?": "Czemu nie zajrzysz do środka i nie sprawdzisz, Johnson?",
    "I think you should.": "Myślę, że powinieneś.",
    "Hmm… I see the dilemma.": "Hmm… Widzę dylemat.",
    "I know it’s the Toma. You have no choice but to trust me.": "Wiem, że to Toma. Nie masz wyboru, musisz mi zaufać.",
    "Enough arguing. If it’s not the Toma, we’re screwed anyway. We can’t stay here forever.": "Dość kłótni. Jeśli to nie Toma, i tak mamy przechlapane. Nie możemy tu zostać na zawsze.",
    "Then let's move.": "To ruszajmy.",
    "Duncan… You’re coming with us.": "Duncan… Idziesz z nami.",
    "You’re messing with a powerful monster, 1Hero.": "Zadajesz się z potężnym potworem, 1Hero.",
    "Shut up. You’re lucky we didn't kill you.": "Zamknij się. Masz szczęście, że cię nie zabiliśmy.",
    "Lead the way, madam.": "Prowadź, madam.",
    "Mother… Daemalius will reveal his true form… He won’t be easy to trap.": "Matko… Daemalius ujawni swoją prawdziwą postać… Nie będzie łatwo go uwięzić.",
    "We need help. He’s going to leave Erica’s body… He’ll be stronger without it.": "Potrzebujemy pomocy. Opuści ciało Eriki… Bez niego będzie silniejszy.",
    "My body? I’m not in my body now?": "Moje ciało? Nie jestem teraz w swoim ciele?",
    "You’re a soul, young lady. You need an Earthly body to leave Hell.": "Jesteś duszą, młoda damo. Potrzebujesz ziemskiego ciała, żeby opuścić Piekło.",
    "How can we help?": "Jak możemy pomóc?",
    "I’m ready for war.": "Jestem gotowa do wojny.",
    "Me too! Let’s kick his ass!": "Ja też! Skopmy mu tyłek!",
    "He can not be defeated.": "Nie można go pokonać.",
    "He must be trapped. He is otherwise immortal in this realm.": "Trzeba go uwięzić. W przeciwnym razie jest nieśmiertelny w tym królestwie.",
    "How do we fight a demon?": "Jak mamy walczyć z demonem?",
    "How can we do anything against a demon in his own home?": "Co możemy zrobić przeciwko demonowi w jego własnym domu?",
    "As long as the doors to this temple remain shut, no demon can enter or leave.": "Dopóki drzwi tej świątyni pozostają zamknięte, żaden demon nie może wejść ani wyjść.",
    "Does that mean we’re safe here?": "To znaczy, że jesteśmy tu bezpieczni?",
    "Safer here than anywhere else in this place.": "Bezpieczniej tu niż gdziekolwiek indziej w tym miejscu.",
    "You say he’ll leave Erica’s body?": "Mówisz, że opuści ciało Eriki?",
    "Of course. He will gain more power without the human dragging him down.": "Oczywiście. Zyska więcej mocy, gdy nie będzie go ciągnął w dół człowiek.",
    "I will bring Erica to her body. 1Hero, you focus on distracting that demon.": "Sprowadzę Erikę do jej ciała. 1Hero, ty zajmij się odwracaniem uwagi tego demona.",
    "We’ve reached the end, Madalyn.": "Dotarliśmy do końca, Madalyn.",
    "Father… Go with Erica’s soul… Find the body and destroy the Toma.": "Ojcze… Idź z duszą Eriki… Znajdź ciało i zniszcz Tomę.",
    "What!? We will do no such thing!": "Co!? Nie zrobimy nic takiego!",
    "Daemalius wants it! And when he gets it, he will not hesitate to turn Earth into a realm of zombies.": "Daemalius jej pragnie! A gdy ją zdobędzie, bez wahania zamieni Ziemię w królestwo zombie.",
    "Just kill him! Why are we stalling?": "Po prostu go zabijcie! Czemu zwlekamy?",
    "We need that rock! What about my army?": "Potrzebujemy tej skały! A co z moją armią?",
    "There is no more army.": "Nie ma już żadnej armii.",
    "Tell me how to destroy it.": "Powiedz mi, jak to zniszczyć.",
    "Bless the statue with holy water while in the hands of the witch… Erica.": "Pobłogosław posążek wodą święconą, gdy będzie w rękach wiedźmy… Eriki.",
    "You can’t do this!": "Nie możecie tego zrobić!",
    "It will shatter into six pieces and will no longer take the souls of humans.": "Roztrzaska się na sześć kawałków i nie będzie już zabierać dusz ludzi.",
    "You promised me an army!": "Obiecałaś mi armię!",
    "What about the plan? I didn’t bring you to Earth for nothing!": "A co z planem? Nie sprowadziłam cię na Ziemię na darmo!",
    "Watch it! The plan is going forward… without the Toma.": "Uważaj! Plan idzie naprzód… bez Tomy.",
    "That’s impossible! What about the demons?": "To niemożliwe! A co z demonami?",
    "Trust me. I’ve been here since the beginning of time. I know what’s being sacrificed.": "Zaufaj mi. Jestem tu od początku czasu. Wiem, co jest poświęcane.",
    "He’s here.": "On tu jest.",
    "1Hero… Take this.": "1Hero… Weź to.",
    "I’ll use the other one on the Toma once we find Erica.": "Użyję drugiego na Tomie, gdy znajdziemy Erikę.",
    "Where… will I be?": "Gdzie… będę?",
    "We’ll find your body… Don’t worry.": "Znajdziemy twoje ciało… Nie martw się.",
    "Buy us time, 1Hero.": "Kup nam czas, 1Hero.",
    "We must move quickly.": "Musimy ruszać szybko.",
    "Can I fight?": "Mogę walczyć?",
    "You stay put, young lady.": "Zostań na miejscu, młoda damo.",
    "I’m going with you.": "Idę z wami.",
    "Nellie…": "Nellie…",
    "I’m going too. I want to fight.": "Ja też idę. Chcę walczyć.",
    "No way. You two stay here.": "Nie ma mowy. Wy dwie zostajecie tutaj.",
    "Diana… Stay with Duncan. I will go.": "Diana… Zostań z Duncanem. Ja pójdę.",
    "Shit… I can’t go out there without you, Lilith.": "Cholera… Nie dam rady wyjść tam bez ciebie, Lilith.",
    "Stay here. I will meet him in my own body.": "Zostań tutaj. Spotkam się z nim we własnym ciele.",
    "I’ll fight with you, 1Hero.": "Będę walczyć u twego boku, 1Hero.",
    "You’ll need me. I’m going.": "Będziesz mnie potrzebował. Idę.",
    "Follow my lead…": "Podążaj za mną…",
    "We’re coming out, Daemalius… And we’re bringing the Toma with us.": "Wychodzimy, Daemaliusie… I zabieramy Tomę ze sobą.",
}

known = set()
for path in (ROOT / 'drafts').rglob('*.jsonl'):
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            row = json.loads(line)
            if row.get('translation', '').strip():
                known.add(row['id'])

rows = []
unmapped = set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    row = json.loads(line)
    context = row.get('context') or {}
    source = ' '.join(row.get('source_text', '').strip().split())
    if (
        row['id'] in known
        or row.get('category') != 'custom_dialogue'
        or context.get('source_kind') != 'map'
        or context.get('map_id') != 202
        or context.get('translation_policy') == 'keep_source_value'
        or not source
        or source.lstrip().startswith('/')
        or not any(char.isalpha() for char in source)
    ):
        continue
    translation = TRANSLATIONS.get(source)
    if translation is None:
        unmapped.add((context.get('event_id'), source))
        continue
    row['translation'] = translation
    rows.append(row)

if unmapped:
    raise SystemExit('Unmapped Map 202 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 123:
    raise SystemExit(f'Expected exactly 123 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 202 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')