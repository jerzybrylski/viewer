#!/usr/bin/env python3
"""Build Polish drafts for player-facing commissioner dialogue on Map 34."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map34-commissioner-followups-01.jsonl'
TRANSLATIONS = {
    'I’m sorry, Miss Bhatt. I was just researching on the internet…': 'Przepraszam, panno Bhatt. Szukałem czegoś w internecie…',
    'We got a call from Eve Cathedral.': 'Dostaliśmy zgłoszenie z katedry Eve.',
    'Really? The church?...': 'Naprawdę? Z kościoła?...',
    'The priest suspects someone is trying to rob them.': 'Ksiądz podejrzewa, że ktoś próbuje ich okraść.',
    'Someone trying to steal from a church? What evidence do we have to go on?': 'Ktoś chce okraść kościół? Na jakich dowodach opieramy tę sprawę?',
    'A noise complaint.': 'Skarga na hałas.',
    'And what else?': 'A co jeszcze?',
    'The priest heard something last night and this morning we got the call.': 'Ksiądz coś słyszał w nocy, a dziś rano dostaliśmy zgłoszenie.',
    'It’s just… How is this a case?': 'Ale… co to za sprawa?',
    'Too busy to leave the office?': 'Za dużo pracy, żeby wyjść z biura?',
    'I can head over there… but it’s looking stormy outside.': 'Mogę tam pojechać… ale na dworze zbiera się na burzę.',
    'Then you better get moving.': 'W takim razie lepiej ruszaj.',
    'Is this my punishment?': 'To ma być moja kara?',
    'Take the case, 1Hero. I’m not arguing with you.': 'Weź tę sprawę, 1Hero. Nie będę się z tobą kłócić.',
    'What about David? He hasn’t left the office in weeks.': 'A co z Davidem? Nie wychodził z biura od tygodni.',
    'I told you, I’m not arguing.': 'Mówiłam, że nie będę się kłócić.',
    'I’m heading over to the Wilkes Mansion later this afternoon.': 'Po południu jadę do rezydencji Wilkesów.',
    'The Wilkes case? Can I come?': 'Sprawa Wilkesów? Mogę pojechać z tobą?',
    'Deal with the church and then we can talk.': 'Najpierw zajmij się kościołem, potem porozmawiamy.',
    'I thought you said the case was closed.': 'Myślałem, że sprawa jest zamknięta.',
    'There’s some loose ends to tie up.': 'Zostało kilka niedokończonych spraw.',
    'Do you think Charles Wilkes was murdered?': 'Myślisz, że Charles został zamordowany?',
    'This isn’t your case, 1Hero...': 'To nie twoja sprawa, 1Hero...',
    'Go to Eve Cathedral. We’ll talk later.': 'Jedź do katedry Eve. Porozmawiamy później.',
    'If I finish early, I’m coming to the mansion.': 'Jeśli skończę wcześniej, pojadę do rezydencji.',
    'Don’t rush your work. I can handle the Wilkes case without your help.': 'Nie spiesz się. Sama poradzę sobie ze sprawą Wilkesów.',
    'Okay, I’m leaving…': 'Dobra, już idę…',
    'See you in a bit.': 'Do zobaczenia za chwilę.',
    'Don’t rush, 1Hero.': 'Nie spiesz się, 1Hero.',
    'I can handle it, Miss Bhatt.': 'Poradzę sobie, panno Bhatt.',
    'Cocky kid.': 'Pyszałkowaty dzieciak.',
    'What do you need, 1Hero? Looking for something to do?': 'Czego potrzebujesz, 1Hero? Szukasz sobie zajęcia?',
    'If you’re going to speak with Lillian Wilkes, do it sooner rather than later.': 'Jeśli chcesz porozmawiać z Lillian Wilkes, zrób to jak najszybciej.',
    'David’s been sent to the mansion. Don’t be late for your interview.': 'David pojechał do rezydencji. Nie spóźnij się na rozmowę.',
    'Showing your face at the office again?': 'Znowu pokazujesz się w biurze?',
    'I’ll stop by the church later.': 'Później zajrzę do kościoła.',
    'Just checking in with you.': 'Po prostu sprawdzam, co u ciebie.',
    'I know what I’m doing.': 'Wiem, co robię.',
    'When you get back, I want to meet with you.': 'Jak wrócisz, chcę z tobą porozmawiać.',
    'I guess I’m back.': 'No i wróciłem.',
    'Yes, Miss Bhatt.': 'Tak, panno Bhatt.',
    'What the hell do you think you’re doing!?': 'Co ty, do cholery, wyprawiasz!?',
    'Sorry, Melissa… Erica and I have become… close.': 'Przepraszam, Melissa… Erica i ja… zbliżyliśmy się do siebie.',
    'You think that gives you free reign over the interrogation room for your sex antics?': 'Myślisz, że możesz sobie urządzać igraszki seksualne w pokoju przesłuchań, kiedy tylko chcesz?',
    "It won't happen again.": 'To się więcej nie powtórzy.',
    'You should be fired and if it wasn’t for your arrangement with Kimura, you’d already be out the door.': 'Powinieneś wylecieć, a gdyby nie twoja umowa z Kimurą, już dawno byłbyś za drzwiami.',
    'Well then I guess it’s good I went out of my way to make something happen in this department for a change.': 'W takim razie dobrze, że wreszcie ruszyłem ten wydział z miejsca.',
    'Is that what you think? You think we sit around twiddling our thumbs because we don’t bite on every coincidence?': 'Tak uważasz? Myślisz, że siedzimy z założonymi rękami, bo nie rzucamy się na każdy zbieg okoliczności?',
    'I was right. Don’t forget that!': 'Miałem rację. Nie zapominaj o tym!',
    'How many times were you wrong before you finally hit on something?': 'Ile razy się myliłeś, zanim w końcu na coś trafiłeś?',
    'You have no idea what you’re doing. You’ve never been told no in your whole life.': 'Nie masz pojęcia, co robisz. Przez całe życie nikt ci nie odmawiał.',
    'You’re just a bitter, jealous woman!': 'Jesteś zgorzkniałą, zazdrosną kobietą!',
    'What did you say to me!?': 'Coś ty do mnie powiedział!?',
    'If all I have keeping me here is Kimura, then I don’t need to impress you anymore.': 'Jeśli jedyne, co mnie tu trzyma, to Kimura, nie muszę już ci imponować.',
    'You keep that tongue of yours under control.': 'Lepiej trzymaj język na wodzy.',
    'You’ve put all your eggs in that basket of hers and now you better put your money where your mouth is.': 'Postawiłeś wszystko na nią, więc teraz poprzyj swoje słowa czynami.',
    'You’ll see. I’m going places, Melissa.': 'Jeszcze zobaczysz. Zajdę daleko, Melissa.',
    'Get out of my office.': 'Wynoś się z mojego biura.',
    'I was right.': 'Miałem rację.',
    'You were lucky.': 'Miałeś szczęście.',
    'Fuck this. She has her head so far up her own ass she can’t see what Andrea sees in me.': 'Pieprzyć to. Ma głowę tak głęboko we własnym tyłku, że nie widzi, co Andrea we mnie dostrzega.',
    'I’m not just a pretty face. I’m a damn good detective and I know it.': 'Nie jestem tylko ładną buźką. Jestem cholernie dobrym detektywem i dobrze o tym wiem.',
    'I saw everything, Melissa!': 'Wszystko widziałem, Melissa!',
    'You fucking spy!': 'Ty pieprzony podglądaczu!',
    'Hey! You spy on me plenty. You’ve been gunning for me ever since I started here!': 'Hej! Sama mnie ciągle obserwujesz. Od początku próbujesz mnie załatwić!',
    'You have some attitude!': 'Ale masz tupet!',
    'You’re a hypocrite!': 'Jesteś hipokrytką!',
    'You were watching the interview.': 'Oglądałaś przesłuchanie.',
    'It’s not what you think.': 'To nie tak, jak myślisz.',
    'Unless you’re a carpet muncher, it’s exactly what I think.': 'Chyba że kręcą cię kobiety, to dokładnie tak, jak myślę.',
    'You cocky asshole!': 'Ty zarozumiały dupku!',
    'You like it. Admit it.': 'Podoba ci się. Przyznaj.',
    'Listen here, 1Hero. Perhaps you and I are not that different.': 'Posłuchaj, 1Hero. Może wcale tak bardzo się nie różnimy.',
    'Clearly, if you’re willing to finger yourself in the office.': 'Najwyraźniej, skoro masturbujesz się w biurze.',
    'So… No one likes a tattle-tale.': 'Więc… Nikt nie lubi donosicieli.',
    'So, we’re keeping secrets?': 'Czyli będziemy dochowywać tajemnic?',
    'Unless you want to lose your job, not a word of this to anyone.': 'Jeśli nie chcesz stracić pracy, nikomu ani słowa.',
    'Are you kidding me? I’m not telling a soul…': 'Żartujesz? Nikomu nie pisnę słówka…',
    'But… what you did was way worse than what I did.': 'Ale… to, co ty zrobiłaś, było o wiele gorsze niż to, co ja zrobiłem.',
    'What!? You literally came all over a woman in the interrogation room!': 'Co?! Dosłownie spuściłeś się na kobiecie w pokoju przesłuchań!',
    'And you’re twiddling your bean to a subordinate!': 'A ty robiłaś sobie dobrze, myśląc o podwładnym!',
    'I did no such thing!': 'Nic takiego nie robiłam!',
    'I saw the whole thing! You can’t lie!': 'Widziałem wszystko! Nie kłam!',
    'I’m going home.': 'Idę do domu.',
    'Now that you came?': 'Teraz, kiedy doszłaś?',
    'Argh!!': 'Argh!!',
    'Get out of my way!': 'Zejdź mi z drogi!',
    'This is priceless. She’s been a thorn in my side for a long time now.': 'Bezcenne. Od dawna działa mi na nerwy.',
    'Finally the tables are turning.': 'Wreszcie role się odwracają.',
    'But the thought of Melissa thinking about me… sexually…': 'Ale sama myśl, że Melissa wyobraża sobie mnie… w łóżku…',
    'No… No way. I’m not going to fuck my boss.': 'Nie… Nie ma mowy. Nie będę pieprzył się z szefową.',
    'But… Would I, if she wanted to?': 'Ale… czy zrobiłbym to, gdyby chciała?',
    'To say I’m disappointed would be an understatement.': 'Powiedzieć, że jestem rozczarowana, to mało.',
    'Had I known there was an undercover operation taking place, I’d have kept my distance.': 'Gdybym wiedziała, że trwa tajna operacja, trzymałabym się od tego z daleka.',
    '1Hero, what the hell do you think you’re doing?': '1Hero, co ty, do cholery, wyprawiasz?',
    'There’s more to this than just the Eclipse Guild…': 'Chodzi o coś więcej niż tylko Gildię Eclipse…',
    'There are people in danger.': 'Ludzie są w niebezpieczeństwie.',
    'We’re on the verge of taking down the Guild. It’s imperative that the operation remains hidden…': 'Jesteśmy o krok od rozbicia Gildii. Operacja musi pozostać tajna…',
    'I understand… but…': 'Rozumiem… ale…',
    'Do you have any idea what would happen if Nellie gets caught?': 'Masz pojęcie, co się stanie, jeśli Nellie wpadnie?',
    'The operation is a bust?': 'Operacja zakończy się klapą?',
    'She gets killed…': 'Zabiją ją…',
    'No one is stepping in.': 'Nikt nie zamierza interweniować.',
    'What if an innocent person gets killed?': 'A jeśli zginie niewinny człowiek?',
    'These aren’t your decisions to make.': 'To nie ty o tym decydujesz.',
    'There are officers posted at the mansion. Perhaps we could do the same for the church.': 'Przy rezydencji są funkcjonariusze. Może tak samo zrobimy z kościołem.',
    'Questions are already rising about the lack of search efforts in the forest…': 'Coraz więcej osób pyta, dlaczego nie prowadzimy poszukiwań w lesie…',
    'This is getting very messy.': 'Sytuacja robi się coraz bardziej zagmatwana.',
    'No one has to know about the secret basement in the church. We just need someone watching it to make sure things are safe.': 'Nikt nie musi wiedzieć o tajnej piwnicy w kościele. Wystarczy, że ktoś będzie jej pilnował, żeby upewnić się, że wszystko jest w porządku.',
    'I’m pulling officers from the mansion. I can reassign one person to keep watch of the church.': 'Wycofuję funkcjonariuszy z rezydencji. Mogę przydzielić jedną osobę do pilnowania kościoła.',
    'Just one?': 'Tylko jedną?',
    'One is plenty.': 'Jedna wystarczy.',
    'Yes, Miss Kimura. I think that’ll be fine.': 'Tak, panno Kimura. Myślę, że to wystarczy.',
    '1Hero, I want you to show the officer the church, but do not mention this secret basement.': '1Hero, pokaż funkcjonariuszowi kościół, ale nie wspominaj o tajnej piwnicy.',
    'Just how far into the cave does the Guild bunker reach?': 'Jak daleko w głąb jaskini sięga bunkier Gildii?',
    'Stop asking questions, 1Hero. This isn’t your operation…': 'Przestań zadawać pytania, 1Hero. To nie twoja operacja…',
    'Public relations is your focus now.': 'Teraz skup się na kontaktach z mediami.',
    'I’m just worried… I know someone who lives very near the cave.': 'Po prostu się martwię… Znam kogoś, kto mieszka blisko jaskini.',
    'The Guild is not looking to harm civilians.': 'Gildia nie zamierza krzywdzić cywilów.',
    'The best advice I can give to you and your friends is to stay away… stay far away.': 'Najlepsza rada, jakiej mogę udzielić tobie i twoim znajomym, brzmi: trzymajcie się z daleka… bardzo daleka.',
    'Yes, Miss Kimura. We understand.': 'Tak, panno Kimura. Rozumiemy.',
    'You’re on thin ice, 1Hero.': 'Jesteś na cienkim lodzie, 1Hero.',
    'Why the hell did you tell her?': 'Po co, do cholery, jej o tym powiedziałeś?',
    'I’m not risking my job so you can play hero for a case that’s not yours.': 'Nie będę ryzykować pracy, żebyś mógł bawić się w bohatera w sprawie, która do ciebie nie należy.',
    'I’m just protecting innocent people.': 'Po prostu chronię niewinnych ludzi.',
    'Bullshit. This is all about you.': 'Bzdura. Chodzi tylko o ciebie.',
    'Go to the church. Don’t be late.': 'Jedź do kościoła. Nie spóźnij się.',
    'Show some professionalism. What’s wrong with you?': 'Zachowuj się profesjonalnie. Co z tobą nie tak?',
    'Andrea is hiding something.': 'Andrea coś ukrywa.',
    'I’m not surprised.': 'Wcale mnie to nie dziwi.',
    'She’s got a lot of artwork in her house… She’s still keeping that stolen Rembrandt in her house...': 'Ma w domu mnóstwo dzieł sztuki… Wciąż trzyma tam skradzionego Rembrandta…',
    'Why not keep it at the station?': 'Czemu nie trzyma go na komisariacie?',
    'I stumbled into a room in her house… It had countless artifacts.': 'Trafiłem przypadkiem na pokój w jej domu… Było tam mnóstwo artefaktów.',
    'She’s keeping treasures for herself?': 'Zatrzymuje skarby dla siebie?',
    'I think she’s been working with the Guild for a long, long time.': 'Myślę, że od bardzo dawna współpracuje z Gildią.',
    'As well as being the police commissioner? You think that’s possible?': 'I jednocześnie jest komisarzem policji? Uważasz, że to możliwe?',
    'Duncan Helmer told me her name is Vayne.': 'Duncan Helmer powiedział mi, że nazywa się Vayne.',
    'I’ve heard that name before. Wasn’t there a Vayne Stone connected to Charles Wilkes in his hidden file?': 'Już słyszałem to nazwisko. Czy w tajnych aktach Charlesa Wilkesa nie było czegoś o Vayne Stone?',
    'Can you see what you can find?': 'Możesz sprawdzić, co da się znaleźć?',
    'Not here… It’ll be traced back to me.': 'Nie tutaj… Namierzą, że to ja.',
    'We have Andrea’s USB drive… Can you do it from your house?': 'Mamy pendrive Andrei… Możesz to sprawdzić u siebie?',
    'Yeah… I think I can do it without getting tracked.': 'Tak… Chyba uda mi się zrobić to tak, żeby mnie nie namierzyli.',
    'That goon is not going back to Duncan, but he is probably looking to get a fake passport.': 'Ten zbir nie wróci do Duncana, ale pewnie spróbuje zdobyć fałszywy paszport.',
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
        or context.get('map_id') != 34
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
    raise SystemExit('Unmapped Map 34 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 143:
    raise SystemExit(f'Expected exactly 143 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 34 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
