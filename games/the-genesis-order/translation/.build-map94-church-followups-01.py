#!/usr/bin/env python3
"""Build Polish drafts for player-facing church and Tasha dialogue on Map 94."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map94-church-followups-01.jsonl'
TRANSLATIONS = {
    'Shit… I can’t go this way. I’ll get seen.': 'Cholera… Tędy nie przejdę. Ktoś mnie zobaczy.',
    'Wow! That was so cool!': 'Wow! To było super!',
    'You look so handsome on TV, 1Hero!': 'Świetnie wyglądasz w telewizji, 1Hero!',
    'Looks like we have a celebrity in our midst.': 'Mamy wśród nas gwiazdę.',
    'Haha. I don’t know about that.': 'Haha. Bez przesady.',
    'It’s the commissioner. She’s looking for me.': 'To komisarz. Szuka mnie.',
    'You have to go back to work?': 'Musisz wracać do pracy?',
    'I’m afraid so. I can’t keep her waiting.': 'Niestety. Nie mogę kazać jej czekać.',
    'Will you come back?': 'Wrócisz?',
    'Let him do his job, Sister.': 'Daj mu pracować, siostro.',
    'It’s okay. If there is time this evening, I’ll pay you a visit.': 'W porządku. Jeśli znajdę dziś wieczorem czas, wpadnę do was.',
    'I’ll stick around, Sister Judy.': 'Zostanę jeszcze, siostro Judy.',
    'Thank you all for visiting. It has been a wonderful day.': 'Dziękuję wam wszystkim za odwiedziny. To był wspaniały dzień.',
    'I better get going.': 'Lepiej już pójdę.',
    'It’s nice of you to visit Sister Judy. She’s such a kind woman.': 'Miło, że odwiedzasz siostrę Judy. To taka dobra kobieta.',
    'I sure did enjoy seeing you on TV, 1Hero.': 'Naprawdę miło było zobaczyć cię w telewizji, 1Hero.',
    'My, my. It’s looking worse than before.': 'Ojej. Wygląda gorzej niż poprzednio.',
    'All this water can’t be good for the wood.': 'Tyle wody nie służy drewnu.',
    '1Hero! The leak got worse.': '1Hero! Przeciek się powiększył.',
    'Damn! That looks bad.': 'Cholera! Wygląda źle.',
    'The storm is getting worse. It would be too dangerous to go onto the roof.': 'Burza się nasila. Wejście na dach byłoby zbyt niebezpieczne.',
    'The water is likely building up in the attic too.': 'Na strychu pewnie też zbiera się woda.',
    'Can you help, 1Hero?': 'Pomożesz, 1Hero?',
    'What do you say, 1Hero? Think you can get up on the roof without getting struck by lightning?': 'Jak myślisz, 1Hero, dasz radę wejść na dach i uniknąć pioruna?',
    'Oh, my. It’s too dangerous.': 'Ojej. To zbyt niebezpieczne.',
    'If we don’t plug it up soon, the water damage will be very costly.': 'Jeśli szybko tego nie załatamy, naprawa szkód będzie bardzo kosztowna.',
    'If I were younger, I’d be up there. But at my age, a fall from forty feet would kill me.': 'Gdybym była młodsza, sama bym tam weszła. Ale w moim wieku upadek z wysokości około dwunastu metrów mógłby mnie zabić.',
    'I’m sure 1Hero’s hard head would bounce right off the hard ground.': 'Z tak twardą głową 1Hero odbije się od ziemi.',
    'Thanks for the concern.': 'Dzięki za troskę.',
    'Here, 1Hero. This will plug the hole if you can make it to the roof.': 'Masz, 1Hero. Tym zatkasz dziurę, jeśli uda ci się wejść na dach.',
    'If we don’t fix this leak soon, the water damage will be expensive to fix.': 'Jeśli szybko nie naprawimy przecieku, usunięcie szkód po zalaniu będzie drogie.',
    'Don’t do anything dangerous. I’d rather have a wet church than an injured 1Hero.': 'Nie rób nic niebezpiecznego. Wolę zalany kościół niż rannego 1Hero.',
    '1Hero! You did it!': '1Hero! Udało ci się!',
    'Looks like you survived.': 'Wygląda na to, że przeżyłeś.',
    'Looks like I did.': 'Na to wygląda.',
    'How bad is the damage?': 'Jak duże są szkody?',
    'I hope the water isn’t leaking into the first floor.': 'Mam nadzieję, że woda nie przecieka na parter.',
    'We better go scout the damage.': 'Lepiej sprawdźmy, jakie są szkody.',
    'Be careful out there, 1Hero. I’m sure the roof is very slippery.': 'Uważaj, 1Hero. Dach pewnie jest bardzo śliski.',
    'Show them your skills, 1Hero. Let’s see if you can climb to the top of the church in a thunderstorm.': 'Pokaż, na co cię stać, 1Hero. Zobaczmy, czy potrafisz wspiąć się na szczyt kościoła podczas burzy.',
    'Something tells me you want me to fall.': 'Coś mi mówi, że chcesz, żebym spadł.',
    'You better go make up with Heather. She’s gonna be pissed after that comment you made.': 'Lepiej idź pogodzić się z Heather. Po tym, co powiedziałeś, będzie wściekła.',
    'How was she?': 'Jak się miała?',
    'Carol! That’s not the point!': 'Carol! Nie o to chodzi!',
    'Hope I’m not interrupting something.': 'Mam nadzieję, że nie przeszkadzam.',
    'Sounds like you and Heather had some fun with Hannah.': 'Wygląda na to, że dobrze się bawiliście z Hannah.',
    'Well… I mean…': 'Cóż… No…',
    'So this is just a thing now? We’re fucking each other’s daughters?': 'Czyli teraz pieprzymy się z córkami tej drugiej?',
    'I’m not opposed to it.': 'Nie mam nic przeciwko.',
    'Carol! We can’t keep doing this!': 'Carol! Nie możemy tak dalej!',
    'Maybe we should cool it for a while.': 'Może przez jakiś czas odpuśćmy.',
    'As long as I have my stud muffin, I’m happy.': 'Dopóki mam swojego przystojniaka, jestem szczęśliwa.',
    'Well… Let’s not jump to any rash decisions.': 'Cóż… Nie podejmujmy pochopnych decyzji.',
    'What’s gotten into you, Heather?': 'Co w ciebie wstąpiło, Heather?',
    'Chloe goes on and on about how much of a crush she has on 1Hero, and now here she is sharing him with you...': 'Chloe bez przerwy opowiada, jak bardzo podkochuje się w 1Hero, a teraz jeszcze dzieli się nim z tobą…',
    'Sounds like someone needs to have a talk with Chloe, and it ain’t us.': 'Wygląda na to, że ktoś powinien porozmawiać z Chloe. I nie chodzi o nas.',
    'Shit… I can’t control myself.': 'Cholera… Nie panuję nad sobą.',
    'What happened to relaxing, girl? Go with the flow. No one’s being harmed.': 'A co z odprężeniem, kochana? Daj się ponieść. Nikomu nie dzieje się krzywda.',
    'We’re sharing a young man with our daughters… Someone’s going to get hurt.': 'Dzielimy się z córkami młodym mężczyzną… Ktoś w końcu ucierpi.',
    'Heather… No offense, but it seems the only one hurt here is you.': 'Heather… Bez urazy, ale jedyna osoba, która tu cierpi, to ty.',
    'Probably shouldn’t have said that.': 'Chyba nie należało tego mówić.',
    'Heather and Chloe have a different relationship. They need more space.': 'Heather i Chloe łączy inna relacja. Potrzebują więcej przestrzeni.',
    'The truth is, I just want to have some fun… But I wonder if Heather is taking it more seriously.': 'Prawda jest taka, że chcę się tylko dobrze bawić… ale zastanawiam się, czy Heather nie traktuje tego poważniej.',
    'I think she’s in love with you… The way Chloe was.': 'Myślę, że ona cię kocha… tak jak Chloe kiedyś.',
    'You don’t think Chloe feels that way about me anymore?': 'Myślisz, że Chloe już nic do mnie nie czuje?',
    'Chloe had her tongue in my ass while you were watching… What do you think?': 'Chloe lizała mnie w tyłek, kiedy patrzyłeś… Jak myślisz?',
    'I think we’re just having fun.': 'Wydaje mi się, że po prostu dobrze się bawimy.',
    'Of course we are, dear…': 'Oczywiście, kochanie…',
    'Now you better go make up with Heather. She’s gonna be pissed after that comment you made.': 'Lepiej idź pogodzić się z Heather. Po tym, co powiedziałeś, będzie wściekła.',
    'Do you think it’s true?': 'Myślisz, że to prawda?',
    'It just might be… But that’s not the point…': 'Może… Ale nie o to chodzi…',
    'Go make her feel better, 1Hero. I know you can.': 'Idź ją pocieszyć, 1Hero. Wiem, że potrafisz.',
    '… I’ll try.': '…Spróbuję.',
    'Having some fun?': 'Dobrze się bawicie?',
    'Tasha?': 'Tasha?',
    'I should have known you’d cause trouble, Nellie.': 'Powinnam była wiedzieć, że narobisz kłopotów, Nellie.',
    '1Hero started it!': 'To 1Hero zaczął!',
    'Father!': 'Ojcze!',
    'We’re going to have to have a talk, Sister Judy.': 'Musimy sobie porozmawiać, siostro Judy.',
    'Father! It’s not what it looks like.': 'Ojcze! To nie tak, jak myślisz.',
    'Looks to me like you let 1Hero cum all over your pussy.': 'Wygląda mi na to, że 1Hero spuścił się na twoją cipkę.',
    'Damn, Tasha. No need to say it out loud.': 'Cholera, Tasha. Nie musisz mówić tego na głos.',
    'Ugh! How embarrassing.': 'Ugh! Ale wstyd.',
    'At least I have some good news.': 'Przynajmniej mam dobre wieści.',
    'The Idol of Souls is the Toma Leolo.': 'Idolem Dusz jest Toma Leolo.',
    'We already suspected that.': 'Już to podejrzewaliśmy.',
    'Now we know.': 'Teraz już wiemy.',
    'But what does it mean?': 'Ale co to oznacza?',
    'The army of the fallen refers to dead souls.': 'Armia Upadłych to dusze zmarłych.',
    'Army of the fallen?': 'Armia Upadłych?',
    'People who had died were brought back to life.': 'Ludzi, którzy umarli, przywrócono do życia.',
    'The witches were using the Toma to remove the souls of humans so that demons could use their bodies to come to Earth.': 'Czarownice używały Toma, by wyrywać dusze ludzi, żeby demony mogły w ich ciałach przybywać na Ziemię.',
    'The only humans to survive the Toma Leolo were those that diverted their gaze.': 'Jedyni ludzie, którzy przeżyli Tomę Leolo, odwrócili wzrok.',
    'Christians broke the idol into six pieces and damned the lost souls back to Hell.': 'Chrześcijanie rozbili idol na sześć części i odesłali potępione dusze z powrotem do Piekła.',
    'So, Lillian puts it back together and then she can use people to bring demons to Earth.': 'Czyli Lillian składa go z powrotem i może użyć ludzi, by sprowadzić demony na Ziemię.',
    'A badass plan, if I do say so myself.': 'Zajebisty plan, jak na mój gust.',
    'How can we stop her?': 'Jak ją powstrzymamy?',
    'She needs the descendant of a Casula witch.': 'Potrzebuje potomka czarownicy z rodu Casula.',
    'Erica…': 'Erica…',
    'But she also needs the seed of her lover.': 'Ale potrzebuje też nasienia swojego kochanka.',
    'That’s you, 1Hero.': 'A ty jesteś tym kochankiem, 1Hero.',
    'Is Erica safe?': 'Erica jest bezpieczna?',
    'She’s in a secure location…': 'Jest w bezpiecznym miejscu…',
    'Lillian needs me, too?': 'Lillian potrzebuje też mnie?',
    'Assuming Erica is in love with you.': 'O ile Erica jest w tobie zakochana.',
    'That’s why Lillian wanted 1Hero to cum inside of her during the ritual.': 'Dlatego Lillian chciała, żeby 1Hero spuścił się w niej podczas rytuału.',
    'Well, if she needs the both of us, she’s shit out of luck. I won’t help her.': 'Jeśli potrzebuje nas obojga, ma pecha. Nie pomogę jej.',
    'You and Erica both should stay away from the mansion. I can handle it from here.': 'Ty i Erica trzymajcie się z dala od rezydencji. Resztą się zajmę.',
    'Close the portal… The same way Zephaniah opened it.': 'Zamknąć portal… tak samo, jak Zephaniah go otworzył.',
    'Do you know how to close a portal?': 'Wiesz, jak zamknąć portal?',
    'How hard can it be?': 'Jak trudne to może być?',
    'It’s better than letting you and Erica get captured.': 'To lepsze niż pozwolić, żeby porwali ciebie i Ericę.',
    'Lillian can’t make me creampie Erica. I have some self-control.': 'Lillian nie zmusi mnie, żebym spuścił się w Erice. Panuję nad sobą.',
    'Ha!': 'Ha!',
    'Forgive me for doubting you.': 'Wybacz, że miałem wątpliwości.',
    'I must read Zephaniah’s journal.': 'Muszę przeczytać dziennik Zephaniaha.',
    'I suppose you want me to sneak you back into the mansion?': 'Domyślam się, że chcesz, żebym przemyciła cię z powrotem do rezydencji?',
    'How can I help?': 'W czym mogę pomóc?',
    'You can go back to work, Tasha. I can handle it from here.': 'Możesz wracać do pracy, Tasha. Resztą się zajmę.',
    'I want to kick Madalyn’s ass!': 'Chcę skopać Madalyn tyłek!',
    'Kick all you want, but you’re no match for a demon.': 'Kop ją, ile chcesz, ale i tak nie masz szans z demonem.',
    'And you are?': 'A ty masz?',
    'Hell yeah, I am.': 'Pewnie, że mam!',
    'Come on, Tasha. I’ll walk you back to the store.': 'Chodź, Tasha. Odprowadzę cię do sklepu.',
    'I’m trying to be a good mother.': 'Staram się być dobrą matką.',
    'No comment.': 'Bez komentarza.',
    'He didn’t say anything!': 'Nic nie powiedział!',
    'As for you, young lady…': 'A ty, młoda damo…',
    'You better be careful. You don’t want to lose that virginity of yours.': 'Uważaj. Nie chcesz chyba stracić dziewictwa.',
    'Oh yeah… Of course.': 'No tak… Oczywiście.',
    'Watch where you spill that seed, 1Hero.': 'Uważaj, gdzie rozlewasz swoje nasienie, 1Hero.',
    'Thank the Lord he didn’t come earlier.': 'Dzięki Panu, że nie przyszedł wcześniej.',
    'Sister Judy… We have to be careful.': 'Siostro Judy… musimy uważać.',
    'I know… I know… We can be private next time…': 'Wiem… wiem… Następnym razem możemy znaleźć ustronne miejsce…',
    'But… There was something exciting about doing it here.': 'Ale… robienie tego tutaj było ekscytujące.',
    'Careful. You’ll get addicted to that feeling too.': 'Uważaj. Od tego uczucia też można się uzależnić.',
    'It’s been a long day.': 'To był długi dzień.',
    'We found it, and it’s shiny gold and very long.': 'Znaleźliśmy to — jest złote, błyszczące i bardzo długie.',
    'Oh! Sounds kinky.': 'O! Brzmi perwersyjnie.',
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
        or context.get('map_id') != 94
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
    raise SystemExit('Unmapped Map 94 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 139:
    raise SystemExit(f'Expected exactly 139 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 94 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
