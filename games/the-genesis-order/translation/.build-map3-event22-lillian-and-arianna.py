import json
from pathlib import Path

ROOT = Path('games/the-genesis-order/translation')
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
MERGED = Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step6.jsonl')
OUT = ROOT / 'drafts/custom-dialogue-map3-event-22-01.jsonl'
if OUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUT}')

MAP = {
    'Looks like Melissa is calling me. I wonder what’s happened this time…': 'Chyba dzwoni Melissa. Ciekawe, co się tym razem stało…',
    'A rat attacked an old lady?': 'Szczur zaatakował starszą panią?',
    'Hello, this is 1Hero.': 'Halo, tu 1Hero.',
    'Hello, detective. This is Lillian Wilkes.': 'Halo, detektywie. Z tej strony Lillian Wilkes.',
    'Lillian? How did you get my number?': 'Lillian? Skąd masz mój numer?',
    'I called the station and they forwarded me to you.': 'Zadzwoniłam na posterunek i przełączyli mnie do ciebie.',
    'Why me? What do you need?': 'Dlaczego do mnie? Czego potrzebujesz?',
    'I appreciated your visit yesterday, but I’m afraid there is more to the story you need to hear.': 'Doceniam, że wczoraj mnie odwiedziłeś, ale obawiam się, że jest jeszcze coś, o czym powinieneś wiedzieć.',
    'Okay. I can come over. Let me just contact Detective Bhatt.': 'Dobrze. Przyjadę. Najpierw skontaktuję się z detektyw Bhatt.',
    'Please. I only want to speak with you.': 'Proszę. Chcę porozmawiać tylko z tobą.',
    'What’s this all about?': 'O co w tym wszystkim chodzi?',
    'It’s…  It’s Erica. She’s late for work.': 'To… To Erica. Spóźnia się do pracy.',
    'Can you please find her and accompany her to my mansion?': 'Czy możesz ją odnaleźć i odprowadzić do mojej rezydencji?',
    'I fear for her safety.': 'Boję się o jej bezpieczeństwo.',
    'Sure. I’ll make sure she arrives safely.': 'Jasne. Dopilnuję, żeby bezpiecznie dotarła na miejsce.',
    'That’s very strange.': 'To bardzo dziwne.',
    'I understand that Lillian may fear Madalyn, but something was off with that call…': 'Rozumiem, że Lillian może bać się Madalyn, ale coś mi nie pasowało w tej rozmowie…',
    'What’s she trying to hide from Melissa?': 'Co ona próbuje ukryć przed Melissą?',
    'What! She recorded us?!': 'Co!? Nagrała nas?!',
    'I need to talk to her about this. What if she sent this to her fans?': 'Muszę z nią o tym porozmawiać. A jeśli wysłała to swoim fanom?',
    'Hey there! Guess you got my message?': 'Hej! Widzę, że dostałeś moją wiadomość?',
    'We need to talk about this.': 'Musimy o tym porozmawiać.',
    'I knew you’d bite.': 'Wiedziałam, że połkniesz haczyk.',
    'Meet me at the gym. You can be my big, strong protector and keep me safe from stalkers and crazy fans.': 'Spotkajmy się na siłowni. Będziesz moim wielkim, silnym obrońcą i ochronisz mnie przed prześladowcami oraz szalonymi fanami.',
    'Alright, Ella. But we’re definitely going to talk about this.': 'Dobra, Ella. Ale na pewno jeszcze o tym porozmawiamy.',
    'See you there!': 'Do zobaczenia!',
    'I can’t believe she taped us doing it. What have I gotten myself into?': 'Nie mogę uwierzyć, że nagrała, jak to robiliśmy. W co ja się wpakowałem?',
    'I’ll have to be more careful in the future with her.': 'Następnym razem będę musiał bardziej na nią uważać.',
    '1Hero, I sense that you’ve been in close contact with something quite evil.': '1Hero, wyczuwam, że miałeś bliski kontakt z czymś naprawdę złowrogim.',
    'I saw her, Arianna. I saw the half-demon, Madalyn.': 'Widziałem ją, Arianno. Widziałem półdemona, Madalyn.',
    'A half-demon? Do those still exist on Earth?': 'Półdemon? Takie istoty wciąż istnieją na Ziemi?',
    'Apparently. I saw her teleport.': 'Najwyraźniej. Widziałem, jak się teleportowała.',
    'That is quite rare. Demi-demons require shell beings.': 'To niezwykle rzadkie. Półdemony potrzebują naczyń.',
    'I had no idea those still existed.': 'Nie miałem pojęcia, że takie istoty wciąż istnieją.',
    'What’s a shell being?': 'Czym jest takie naczynie?',
    'The offspring of a demon and a human is born without a soul.': 'Potomstwo demona i człowieka rodzi się bez duszy.',
    'Long ago, demonic idols were used to suck the soul from helpless humans, making way for an army of demons to wander the earth.': 'Dawno temu demoniczne idole wysysały dusze z bezbronnych ludzi, umożliwiając armii demonów swobodne chodzenie po ziemi.',
    'But that little mess was cleaned up. So, I have no idea how one could have slipped through the cracks.': 'Ale ten mały problem dawno rozwiązano. Nie mam pojęcia, jak jeden z nich mógł się prześlizgnąć niezauważony.',
    'Can a priest exorcize a demon’s soul from a human?': 'Czy ksiądz może wypędzić duszę demona z człowieka?',
    'Any holy servant of God can cast a demon back to Hell.': 'Każdy sługa Boży może odesłać demona z powrotem do piekła.',
    'Sounds easy enough.': 'Brzmi dość prosto.',
    'It sure is! You just need the exact right combination of holy relics and to recite the prayer exactly as it is written.': 'Oczywiście! Wystarczy tylko dobrać właściwe święte relikwie i wyrecytować modlitwę dokładnie tak, jak została zapisana.',
    'What relics? And where is it written?': 'Jakie relikwie? I gdzie zapisano tę modlitwę?',
    'Hmmm… Good questions.': 'Hmm… Dobre pytania.',
    'How is it easy if we have no idea where the right tools are?': 'Jak to może być proste, skoro nie wiemy nawet, gdzie znaleźć potrzebne rzeczy?',
    'Exorcism is not my specialty. But I’m sure everything will work out fine.': 'Egzorcyzmy nie są moją specjalnością. Ale jestem pewna, że wszystko dobrze się ułoży.',
    'I tend to always know the way.': 'Zazwyczaj wiem, którą drogą podążać.',
    'This sounds like an impossible task.': 'To brzmi jak niewykonalne zadanie.',
    'A call from David? I wonder what this is about.': 'Dzwoni David? Ciekawe, o co chodzi.',
    'Hey, David, what’s up?': 'Cześć, David. Co tam?',
    'You might want to get back to the office.': 'Lepiej wracaj do biura.',
    'Why? Melissa asked for me?': 'Dlaczego? Melissa mnie szuka?',
    'No, Melissa hasn’t been back yet.': 'Nie, Melissy jeszcze nie ma.',
    'It was Commissioner Kimura.': 'Chodziło o komisarz Kimurę.',
    'Kimura? Why was she looking for me?': 'Kimura? Po co mnie szukała?',
    'Maybe you should ask her yourself.': 'Może sam ją o to zapytasz.',
    'Shit… Alright, I’ll be right in.': 'Cholera… Dobra, zaraz będę.',
    'I wonder what Andrea could want me for?': 'Ciekawe, czego Andrea ode mnie chce.',
    'Shit! Of all the times to ditch work early.': 'Cholera! Akurat dziś musiałem urwać się wcześniej z pracy.',
    'I was just checking your itinerary for tomorrow, and it looks like you have quite a busy day.': 'Sprawdzałam właśnie twój plan na jutro. Wygląda na to, że czeka cię bardzo pracowity dzień.',
    'My itinerary?': 'Mój plan?',
    'It appears you are going to speak in front of hundreds of thousands of people! That’s amazing!': 'Wygląda na to, że przemówisz do setek tysięcy ludzi! To niesamowite!',
    'Oh, uhh, yeah. I’m a bit nervous.': 'A, no… Trochę się denerwuję.',
    'It’s hard for me to even picture fitting that many people into one place, but I sure am proud of you for drawing such a crowd.': 'Trudno mi sobie wyobrazić, żeby aż tyle osób zmieściło się w jednym miejscu, ale jestem z ciebie dumna, że przyciągnąłeś takie tłumy.',
    'You must be filled with interesting information that the people want to hear.': 'Musisz mieć mnóstwo ciekawych rzeczy do powiedzenia, skoro ludzie chcą cię słuchać.',
    'No, no, Arianna. It’s a TV broadcast…': 'Nie, Arianno. To transmisja telewizyjna…',
    'And I don’t really know what I’m going to say.': 'I tak naprawdę nie wiem, co powiem.',
    'Oh, my. And it’s already late in the evening. You have to think of something!': 'Ojej. A do tego jest już późny wieczór. Musisz coś wymyślić!',
    'I’m meeting with Andrea in the morning. She’ll bring me up to speed.': 'Rano spotykam się z Andreą. Wprowadzi mnie w temat.',
    'If you don’t mind, perhaps you can drop a kind word about the Creator. He sure does love when people talk about Him.': 'Jeśli nie masz nic przeciwko, wspomnij życzliwie o Stwórcy. Bardzo lubi, gdy ludzie o Nim mówią.',
    'Sounds like a… swell guy.': 'Brzmi jak… całkiem w porządku gość.',
    'He sure is swell!': 'Jest naprawdę wspaniały!',
    'I sense your day did not go as you had planned.': 'Wyczuwam, że twój dzień nie potoczył się zgodnie z planem.',
    'To say the least. I’m on thin ice.': 'To mało powiedziane. Jestem na cienkim lodzie.',
    'What’s wrong, 1Hero? What happened?': 'Co się stało, 1Hero? Coś się wydarzyło?',
    'Uhh… I did something dirty where I wasn’t supposed to.': 'Eee… Zrobiłem coś nieprzyzwoitego w miejscu, w którym nie powinienem.',
    'I don’t understand. It seems all humans do dirty things all the time…': 'Nie rozumiem. Wygląda na to, że ludzie bez przerwy robią nieprzyzwoite rzeczy…',
    'What’s different about this one?': 'Czym różniło się akurat to?',
    'You’re not supposed to do dirty stuff in the interrogation room.': 'Nie wolno robić takich rzeczy w pokoju przesłuchań.',
    'How wonderful! You have a place that you keep clean.': 'Jak wspaniale! Macie miejsce, które utrzymujecie w czystości.',
    'I’d love to visit one day.': 'Chętnie kiedyś je odwiedzę.',
    'It’s not that special.': 'Nie ma w nim nic wyjątkowego.',
    'A respite from all the filth of your world would be special to me.': 'Dla mnie wytchnienie od całego brudu waszego świata byłoby czymś wyjątkowym.',
    'Hmm… I’ll show you it one day.': 'Hmm… Kiedyś ci je pokażę.',
    '1Hero, I sense much conflict in those close to you. I worry that you are being careless in your actions.': '1Hero, wyczuwam wiele napięć wśród twoich bliskich. Martwię się, że postępujesz nieostrożnie.',
    'But, Arianna, aren’t my actions the will of the Lord?': 'Ale, Arianno, czy moje działania nie są wolą Pana?',
    'Your fate is guided, but it is up to you to make moral choices.': 'Twoim losem ktoś kieruje, ale to ty musisz podejmować moralne decyzje.',
    'I’m only human. If a hot piece of ass presents itself, I’m not holding back.': 'Jestem tylko człowiekiem. Jeśli trafi się gorący tyłek, nie będę się powstrzymywał.',
    'I’m not familiar with that expression. But it sounds painful for the ass.': 'Nie znam tego wyrażenia. Ale brzmi, jakby tyłek miał na tym ucierpieć.',
    'It means I’m going to have sex with a hot babe if the opportunity presents itself.': 'To znaczy, że jeśli nadarzy się okazja, prześpię się z atrakcyjną dziewczyną.',
    '1Hero! Whatever you do with pieces of flaming donkeys is your own business, but sexual relations outside of wedlock is too much.': '1Hero! To, co robisz z rozpalonymi tyłkami osłów, to twoja sprawa, ale seks poza małżeństwem to już przesada!',
    'It’s getting late. I should call Erica and make sure things are okay between us.': 'Robi się późno. Powinienem zadzwonić do Eriki i upewnić się, że między nami wszystko w porządku.',
    'Things got pretty heated in that interrogation room…': 'W pokoju przesłuchań zrobiło się gorąco…',
    'In more ways than one.': 'I to nie tylko w przenośni.',
    '1Hero?': '1Hero?',
    'Erica, how are you holding up?': 'Erica, jak się trzymasz?',
    'I’m fine, but could be better.': 'W porządku, choć mogłoby być lepiej.',
    'What’s wrong? Do you feel unsafe?': 'Co się stało? Nie czujesz się bezpiecznie?',
    'If you’re implying that I’d like some company, you’re not wrong.': 'Jeśli sugerujesz, że przydałoby mi się towarzystwo, to masz rację.',
    'Are you inviting me over to your place?': 'Zapraszasz mnie do siebie?',
    'Come on over, 1Hero. I’ll meet you out front.': 'Wpadaj, 1Hero. Będę czekać przed domem.',
    'Be there in a bit.': 'Zaraz będę.',
}

known = set()
for line in MERGED.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    if row['translation'].strip():
        known.add(row['id'])
rows = []
missing = set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    context = row['context']
    source = row['source_text'].strip()
    if (context.get('source_kind') != 'map' or context.get('map_id') != 3
            or context.get('event_id') != 22 or row['id'] in known):
        continue
    if not source or source.startswith('/') or source in {'…', '...', '..'}:
        continue
    translation = MAP.get(source)
    if translation is None:
        missing.add(source)
        continue
    row['translation'] = translation
    rows.append(row)
if missing:
    raise SystemExit('Unmapped Map 3 event 22 strings: ' + repr(sorted(missing)))
OUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote Map 3 event 22 Lillian/Arianna dialogue: {len(rows)} records from {len(MAP)} source strings')
