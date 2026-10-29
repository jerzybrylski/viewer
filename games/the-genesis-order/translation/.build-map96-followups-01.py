#!/usr/bin/env python3
"""Build Polish drafts for Map 96 follow-ups."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map96-followups-01.jsonl'
TRANSLATIONS = {
    "Sorry, Chloe. I didn’t mean to barge in on you.": "Przepraszam, Chloe. Nie chciałem ci przeszkadzać.",
    "I thought you were working today?": "Myślałem, że dziś pracujesz?",
    "I’m just checking in. There was a report of some pervert running around the neighborhood.": "Tylko wpadłem sprawdzić, co u ciebie. Było zgłoszenie o jakimś zboczeńcu biegającym po okolicy.",
    "Really? Did you catch them?": "Naprawdę? Złapali go?",
    "No. The officers who are supposed to be patrolling are still at the station.": "Nie. Funkcjonariusze, którzy mieli patrolować, wciąż są na komisariacie.",
    "Well, thanks for thinking about me. I’m glad you came.": "Cóż, dzięki, że o mnie pomyślałeś. Cieszę się, że przyszedłeś.",
    "Of course. I care a lot about you.": "Oczywiście. Bardzo mi na tobie zależy.",
    "I had so much fun last night. I’ve not stopped thinking about it.": "Tak świetnie się bawiłam wczoraj. Nie mogę przestać o tym myśleć.",
    "I’m happy to help you two.": "Cieszę się, że mogłam wam obojgu pomóc.",
    "It means a lot to have you show me how to handle… my urges.": "To dla mnie wiele znaczy, że pokazujesz mi, jak radzić sobie z… moimi pragnieniami.",
    "It was no surprise seeing Judy struggle, but I would have suspected that your mom would have taught you about masturbation.": "Nie dziwi mnie, że Judy miała trudności, ale podejrzewałam, że mama nauczyła cię o masturbacji.",
    "Are you kidding? I couldn’t imagine having that kind of talk with Mom!": "Żartujesz? Nie wyobrażam sobie takiej rozmowy z mamą!",
    "I hope you're not too hard on her. You know she has the same urges.": "Mam nadzieję, że nie jesteś na nią zbyt surowa. Wiesz, że ona ma te same pragnienia.",
    "Ugh! I don’t want to think about my mom in that way.": "Ugh! Nie chcę myśleć o mamie w ten sposób.",
    "I’m just saying that it must have been hard being a single mother.": "Po prostu mówię, że musiało być jej ciężko jako samotnej matce.",
    "I guess you’re right. I just wish she was more like other moms.": "Chyba masz rację. Chciałabym tylko, żeby była bardziej jak inne mamy.",
    "Like Carol?": "Jak Carol?",
    "Carol and her are so similar, Chloe.": "Carol i ona są tak podobne, Chloe.",
    "Yeah, but… you know. Mom is so concerned with her looks and is always teasing me and boys…": "Tak, ale… wiesz. Mama tak przejmuje się wyglądem i ciągle droczy się ze mną i chłopakami…",
    "I feel like she’s my sister sometimes… and I don’t like it.": "Czasem czuję się, jakby była moją siostrą… i nie podoba mi się to.",
    "Maybe she needs a man in her life.": "Może potrzebuje mężczyzny w swoim życiu.",
    "As much as I hate to think about it, you might be right.": "Choć nienawidzę o tym myśleć, możesz mieć rację.",
    "What about you, Chloe? Do you need a man in your life?": "A ty, Chloe? Potrzebujesz mężczyzny w swoim życiu?",
    "I don’t think I could handle it.": "Chyba bym tego nie udźwignęła.",
    "It’s so much pressure. Relationships suck.": "To taka presja. Związki są do bani.",
    "You sound like Judy.": "Brzmisz jak Judy.",
    "Sister Judy told you about her old boyfriend?": "Siostra Judy opowiedziała ci o swoim byłym chłopaku?",
    "She told me about her past.": "Opowiedziała mi o swojej przeszłości.",
    "Why do you think she didn’t have romantic feelings? Do you think there’s something wrong with her?": "Dlaczego myślisz, że nie miała romantycznych uczuć? Myślisz, że coś z nią nie tak?",
    "Everyone’s different.": "Każdy jest inny.",
    "I wonder if I have the same problem as she does.": "Zastanawiam się, czy mam ten sam problem co ona.",
    "You don’t want to fall in love?": "Nie chcesz się zakochać?",
    "I want to feel what we felt last night… but I don’t think that’s love.": "Chcę czuć to, co czuliśmy wczoraj… ale nie sądzę, by to była miłość.",
    "Haha. That’s normal.": "Haha. To normalne.",
    "You’re a fast learner.": "Szybko się uczysz.",
    "No… I mean… Did I do a good job with you?": "Nie… To znaczy… Czy dobrze się spisałam?",
    "Oh, uhh. Yeah, it was good.": "Och, yyy. Tak, było dobrze.",
    "That doesn’t sound convincing.": "Nie brzmi to przekonująco.",
    "You’re new to all of this. A handjob is a handjob.": "Jesteś w tym nowa. Ręczna robota to ręczna robota.",
    "Well, thanks. Not as good as Hannah’s pussy?": "No, dzięki. Nie tak dobra jak cipka Hannah?",
    "Chloe!?": "Chloe!?",
    "What about… her blowjob?": "A co z… jej lodem?",
    "Hannah’s blowjob? At the waterfall?": "Lód Hannah? Przy wodospadzie?",
    "Yeah. Was it good?": "Tak. Było dobre?",
    "Hahaha. Blowjobs are always good.": "Hahaha. Lody zawsze są dobre.",
    "Really? What about her teeth? It doesn’t hurt?": "Naprawdę? A jej zęby? Nie boli?",
    "Of course it doesn’t hurt.": "Oczywiście, że nie boli.",
    "Where’s my mom?": "Gdzie jest moja mama?",
    "She’s in the front yard.": "Jest na podwórku z przodu.",
    "I want to try it.": "Chcę tego spróbować.",
    "You want to try a blowjob?": "Chcesz spróbować loda?",
    "Would you be okay with that?": "Byłoby ci z tym dobrze?",
    "Uhh… Sure!": "Yyy… Pewnie!",
    "Of course. A guy can’t turn down a blowjob. Especially from a beautiful girl like you.": "Oczywiście. Facet nie odmówi loda. Zwłaszcza od tak pięknej dziewczyny jak ty.",
    "Haha. 1Hero, you are going to make me blush.": "Haha. 1Hero, zawstydzisz mnie.",
    "Are you sure you’re okay with this?": "Na pewno ci to odpowiada?",
    "I just want to try it…": "Po prostu chcę spróbować…",
    "Take off your pants.": "Zdejmij spodnie.",
    "Shit. I’ve got to go to Hannah’s place. I’ve got to talk to Chloe.": "Cholera. Muszę iść do Hannah. Muszę porozmawiać z Chloe.",
    "If you want to teach her about sex, you have my blessing.": "Jeśli chcesz nauczyć ją seksu, masz moje błogosławieństwo.",
    "I think it would do her a world of good to learn from you.": "Myślę, że wiele by jej dało uczenie się od ciebie.",
    "Heather… You know I had a big crush on her once.": "Heather… Wiesz, że kiedyś bardzo się w niej podkochiwałem.",
    "But… I kinda have something going on now.": "Ale… teraz chyba coś się u mnie dzieje.",
    "With another woman?": "Z inną kobietą?",
    "Maybe… I don’t know how serious it is.": "Może… Nie wiem, jak poważne to jest.",
    "Don’t feel pressured, 1Hero. You have your own life to live and Chloe has hers.": "Nie czuj presji, 1Hero. Masz swoje życie, a Chloe swoje.",
    "Thanks…": "Dzięki…",
    "I think you two need to talk about this kinda stuff more.": "Myślę, że powinniście więcej rozmawiać o takich sprawach.",
    "Talk about sex with Chloe? She freaks out every time I mention it.": "Rozmawiać o seksie z Chloe? Wariuje za każdym razem, gdy o tym wspomnę.",
    "Isn’t it normal for daughters and mothers to clash from time to time?": "Czy to nie normalne, że córki i matki czasem się ścierają?",
    "You’re a wise woman, Heather…": "Jesteś mądrą kobietą, Heather…",
    "But if you ask me… I think you should push through that uncomfortable barrier between you two.": "Ale moim zdaniem… powinnaś przełamać tę niezręczną barierę między wami.",
    "You’re right. Sometimes I think I need a man in my life.": "Masz rację. Czasem myślę, że potrzebuję mężczyzny w swoim życiu.",
    "You do, Heather. And Chloe knows it.": "Potrzebujesz, Heather. I Chloe o tym wie.",
    "I wish I were young again.": "Chciałabym znów być młoda.",
    "You just need someone who will see you for the beautiful woman you are.": "Potrzebujesz tylko kogoś, kto dostrzeże w tobie piękną kobietę, jaką jesteś.",
    "Thank you, 1Hero. I’m glad we could have this talk.": "Dziękuję, 1Hero. Cieszę się, że mogliśmy porozmawiać.",
    "Now, you better get over to the farm and let that girl suck your dick.": "A teraz lepiej idź na farmę i pozwól tej dziewczynie obciągnąć ci kutasa.",
    "Heather! You don’t have to say it like that.": "Heather! Nie musisz tak tego mówić.",
    "Come on, baby. We don’t need to beat around the bush…": "Daj spokój, kochanie. Nie musimy owijać w bawełnę…",
    "Lord knows Carol and I have no shame.": "Bóg wie, że Carol i ja nie mamy wstydu.",
    "Thanks for being in my life, Heather.": "Dzięki, że jesteś w moim życiu, Heather.",
    "And thank you for being there for Chloe and me.": "I dziękuję, że jesteś dla Chloe i dla mnie.",
    "Uhh, 1Hero…": "Yyy, 1Hero…",
    "I feel a lot better.": "Czuję się dużo lepiej.",
    "You’re a beautiful woman, Chloe.": "Jesteś piękną kobietą, Chloe.",
    "I want to do it again. I want to try new things.": "Chcę to zrobić znowu. Chcę spróbować nowych rzeczy.",
    "Feeling adventurous?": "Masz ochotę na przygodę?",
    "Here… Call me later.": "Proszę… Zadzwoń do mnie później.",
    "Are you going to tell Sister Judy?": "Powiesz siostrze Judy?",
    "Oh, God… I don’t think I can.": "O Boże… Chyba nie dam rady.",
    "I don’t know… We’ve kinda bonded over this…": "Nie wiem… Jakoś się przez to zbliżyłyśmy…",
    "Over talking about you.": "Rozmawiając o tobie.",
    "I know it’s silly… But she can’t stop talking about you…": "Wiem, że to głupie… Ale nie może przestać o tobie mówić…",
    "And I guess I can't stop either.": "I chyba ja też nie mogę przestać.",
    "Oh, my! I’m sorry!": "Ojej! Przepraszam!",
    "We did anal again! Lock the door!": "Znowu robiliśmy anal! Zamknij drzwi!",
    "Damn that door.": "Cholera, te drzwi.",
    "Thank God it was you that walked in and not Mom.": "Dzięki Bogu, że to ty wszedłeś, a nie mama.",
    "People are wondering what’s going on up here.": "Ludzie zastanawiają się, co tu się dzieje.",
    "Shit. Let’s get back to the party before Mom starts thinking the worst.": "Cholera. Wracajmy na imprezę, zanim mama pomyśli najgorsze.",
    "Is it the worst?": "Czy to najgorsze?",
    "You know what I mean. She’ll tease us.": "Wiesz, o co mi chodzi. Będzie nas drażnić.",
    "I must get back to the church soon. Would you like to come with me?": "Muszę niedługo wracać do kościoła. Chciałabyś pójść ze mną?",
    "I probably have to keep the others company.": "Chyba muszę dotrzymać towarzystwa reszcie.",
    "Everyone is welcome to come.": "Wszyscy są mile widziani.",
    "It would be nice to get away from the pool for a bit.": "Miło byłoby na chwilę odejść od basenu.",
    "Chloe! My clothes are in your bedroom.": "Chloe! Moje ubrania są w twojej sypialni.",
    "Oh, shit! I forgot. She changed in my bedroom!": "O cholera! Zapomniałam. Przebrała się w mojej sypialni!",
    "Coming, Sister Judy!": "Już idę, siostro Judy!",
    "I don’t know… Just keep a secret.": "Nie wiem… Po prostu zachowaj tajemnicę.",
    "Is it a secret?": "Czy to tajemnica?",
    "Oh, 1Hero. Are you changing here too?": "Och, 1Hero. Ty też się tu przebierasz?",
    "I was just leaving.": "Właśnie wychodziłam.",
    "Bye, 1Hero!": "Pa, 1Hero!",
    "I’m sure glad I met Ella. She’s a cool girl.": "Cieszę się, że poznałam Ellę. To fajna dziewczyna.",
    "Staying up late?": "Nie śpisz do późna?",
    "Can’t wait? We can fuck right now if you want.": "Nie możesz się doczekać? Możemy się pieprzyć od razu, jeśli chcesz.",
    "Haha, I’ll see you at the mansion, Chloe.": "Haha, do zobaczenia w rezydencji, Chloe.",
    "It’s nice being home.": "Dobrze być w domu.",
    "Dinner was delicious. But it’s nice to be back here at Chloe’s home.": "Kolacja była pyszna. Ale miło wrócić do domu Chloe.",
    "I hope I can see you again tomorrow, 1Hero.": "Mam nadzieję, że zobaczymy się znowu jutro, 1Hero.",
    "Thanks for coming over, 1Hero. I’m glad Ella is here too.": "Dzięki, że wpadłeś, 1Hero. Cieszę się, że Ella też jest.",
    "What are you doing back here so soon? Where is Sister Judy?": "Co tak szybko z powrotem? Gdzie jest siostra Judy?",
    "One of these days I’m gonna clobber a thief.": "Kiedyś dorwę złodzieja.",
    "Not again!": "Znowu!"
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
        or context.get('map_id') != 96
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
    raise SystemExit('Unmapped Map 96 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 126:
    raise SystemExit(f'Expected exactly 126 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 96 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
