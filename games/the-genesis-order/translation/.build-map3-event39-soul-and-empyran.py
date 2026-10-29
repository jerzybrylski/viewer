import json
from pathlib import Path
ROOT=Path('games/the-genesis-order/translation')
CANON=ROOT/'export-v1/custom_dialogue.jsonl'
MERGED=Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step4.jsonl')
OUT=ROOT/'drafts/custom-dialogue-map3-event-39-01.jsonl'
if OUT.exists(): raise SystemExit(f'Refusing to overwrite {OUT}')
MAP={
'Your mind is conflicted, 1Hero. What’s wrong?':'Masz mętlik w głowie, 1Hero. Co się stało?',
'1Hero. You worry deeply for your friends. I can sense it.':'1Hero. Bardzo martwisz się o przyjaciół. Czuję to.',
'1Hero… You radiate with the afterglow of magic. What happened?':'1Hero… Promieniejesz magiczną energią. Co się stało?',
'Someone’s calling.':'Ktoś dzwoni.',
'Here we go. Another chance to impress Andrea…':'No proszę. Kolejna okazja, żeby zaimponować Andrei…',
'It’s… nothing. I’m just juggling a lot of secrets.':'To… nic. Po prostu mam za dużo sekretów do ukrycia.',
'I’m so close to the finish line… But there’s so many questions left unanswered.':'Jestem już tak blisko mety… A wciąż tyle pytań bez odpowiedzi.',
'I found Madalyn’s piece of the Toma Leolo under the mansion…':'Znalazłem kawałek Tomy Leolo należący do Madalyn pod rezydencją…',
'And I need it…':'A ja go potrzebuję…',
'It’s not good to hold secrets. The truth is always the right path.':'Nie powinieneś mieć sekretów. Prawda zawsze jest właściwą drogą.',
'The more I learn the more I feel I don’t know what’s going on.':'Im więcej się dowiaduję, tym mniej rozumiem, co się dzieje.',
'Had a bit of fun with Kimberly Foxx using it.':'Trochę się nim pobawiłem z Kimberly Foxx.',
'Lord give me strength.':'Panie, dodaj mi sił.',
'I don’t know… Some things are best unsaid.':'Nie wiem… O niektórych rzeczach lepiej nie mówić.',
'There is a demonic energy in this town. You may be close to solving your Guild case, but there is a deeper mystery.':'W tym mieście czuć demoniczną energię. Może jesteś blisko rozwiązania sprawy Gildii, ale kryje się tu głębsza tajemnica.',
'You better tread carefully, 1Hero! We still don’t know what those magic rocks are supposed to do.':'Lepiej stąpaj ostrożnie, 1Hero! Nadal nie wiemy, do czego służą te magiczne kamienie.',
'A call from the office? What now?':'Telefon z biura? Co tym razem?',
'1Hero? Are you praying?':'1Hero? Modlisz się?',
'Oh my! You shouldn’t hide things from others.':'Ojej! Nie powinieneś niczego ukrywać przed innymi.',
'Madalyn is planning something and it involves a secret area under the mansion.':'Madalyn coś planuje. Chodzi o tajne pomieszczenie pod rezydencją.',
'They are Casula in origin… Erica says she’ll look into it. She’s a Casula native.':'Pochodzą z Casula… Erica obiecała to zbadać. Jest stamtąd.',
'Kimberly. What’s up?':'Kimberly. Co się dzieje?',
'It’s a figure of speech.':'To tylko przenośnia.',
'Well… Then aren’t clothes a lie?':'Cóż… Czy w takim razie ubrania nie są kłamstwem?',
'She needs some weird amulets for some reason, and Lillian trusts me to find these weird Toma statues.':'Z jakiegoś powodu potrzebuje dziwnych amuletów, a Lillian ufa mi i każe szukać tych dziwnych posągów Tomy.',
'But I did notice a symbol on the floor next to six statues.':'Zauważyłem jednak symbol na podłodze obok sześciu posągów.',
'Detective Canmore speaking.':'Przy telefonie detektyw Canmore.',
'Do you have some time to meet?':'Masz czas, żeby się spotkać?',
'I think you were praying! Have you found the Lord?':'Chyba się modliłeś! Odnalazłeś Pana?',
'What!? What does that mean?':'Co!? Co to znaczy?',
'You have too much trust, 1Hero. You need to watch your back.':'Za bardzo ufasz innym, 1Hero. Musisz uważać.',
'What are you talking about?':'O czym ty mówisz?',
'1Hero. I’m leaving the church.':'1Hero. Wychodzę z kościoła.',
'Is something wrong?':'Coś się stało?',
'Nope. Just a sexy angel.':'Nie. Po prostu spotkałem seksownego anioła.',
'Why don’t you take off those shiny panties and bras? Are you hiding something?':'Czemu nie zdejmiesz tych błyszczących majtek i stanika? Coś ukrywasz?',
'I know what I’m doing. I need to stay close to Lillian. I need access to that mansion.':'Wiem, co robię. Muszę trzymać się blisko Lillian i mieć dostęp do tej rezydencji.',
'One of the statues was holding a piece of the Toma with the other five empty-handed.':'Jeden z posągów trzymał kawałek Tomy, a pozostałe pięć miało puste ręce.',
'Bobby? What are you talking about?':'Bobby? O czym ty mówisz?',
'We’ve got some new audio from the east transmitter.':'Mamy nowe nagranie ze wschodniego nadajnika.',
'Oh, 1Hero.':'Och, 1Hero.',
'That has nothing to do with anything.':'To nie ma z tym nic wspólnego.',
'This is certainly a task for humans. Your ability to navigate a sea of deception is impressive.':'To zadanie dla ludzi. Imponuje mi, jak poruszasz się po morzu kłamstw.',
'And the symbol on the floor?':'A co z symbolem na podłodze?',
'Kimura wants me back at the mansion. Something has her spooked.':'Kimura chce, żebym wrócił do rezydencji. Coś ją wystraszyło.',
'More creepy sounds?':'Znowu jakieś upiorne dźwięki?',
'You don’t want to end up in Hell, do you?':'Nie chcesz chyba skończyć w piekle, prawda?',
'Just seems a bit hypocritical.':'To po prostu trochę obłudne.',
'There’s no deception where you come from?':'U was nie ma kłamstw?',
'A pentagram.':'Pentagram.',
'Then who’s going to watch the church?':'Kto będzie pilnował kościoła?',
'No… This time it’s two people talking… Just head over. We need to talk.':'Nie… Tym razem rozmawiały dwie osoby… Po prostu przyjedź. Musimy pogadać.',
'I don’t know. Maybe I do.':'Nie wiem. Może tak.',
'I’m not going to get naked… I would get cold.':'Nie będę się rozbierać… Zmarzłabym.',
'The Empyrean is a world of pure truth bound by the word of God.':'Empyreum to świat czystej prawdy, podporządkowany słowu Boga.',
'Are you sure? What did it look like?':'Na pewno? Jak to wyglądało?',
'Not my problem.':'To nie mój problem.',
'Okay. See ya soon.':'Dobrze. Do zobaczenia.',
'1Hero!':'1Hero!',
'I could warm you up.':'Mógłbym cię rozgrzać.',
'There is no need for distrust where I come from. We simply obey His command.':'W moim świecie nie ma powodów do nieufności. Po prostu wykonujemy Jego polecenia.',
'It was a star inside of a circle.':'To była gwiazda w okręgu.',
'It is your problem!':'To twój problem!',
'If I can’t impress Andrea, my life might turn into hell.':'Jeśli nie zaimponuję Andrei, moje życie może zamienić się w piekło.',
'We’ll have no more discussion about that, young man!':'Nie będziemy już o tym rozmawiać, młody człowieku!',
'And if you don’t?':'A jeśli nie?',
'Oh! You mean a pentacle! That is a symbol of the element of earth! How lovely.':'Och! Chodzi ci o pentakl! To symbol żywiołu ziemi! Jak pięknie.',
'If you want to guard it, be my guest. You’re lucky I’m even calling you.':'Jeśli chcesz go pilnować, proszę bardzo. Masz szczęście, że w ogóle do ciebie dzwonię.',
'You have such a strong commitment to your work.':'Naprawdę bardzo angażujesz się w swoją pracę.',
'Our light turns to darkness and we are forever separated from God.':'Nasze światło zamienia się w ciemność, a my zostajemy na zawsze oddzieleni od Boga.',
'Well… The statues were looking at it upside down.':'Cóż… Posągi patrzyły na niego do góry nogami.',
'God damn it, Bobby.':'Cholera jasna, Bobby.',
'It’s who I am, Arianna':'Taki już jestem, Arianno.',
'Seems a bit unfair.':'To trochę niesprawiedliwe.',
'Upside down!?':'Do góry nogami!?',
'I’m not sticking around.':'Nie zostanę tu dłużej.',
'The same commitment to God and you’d be a shoe in for heaven.':'Gdybyś tak samo oddał się Bogu, miałbyś pewne miejsce w niebie.',
'You must never question His command.':'Nigdy nie wolno kwestionować Jego rozkazów.',
'Yeah.':'Tak.',
'What’s the sex life like in heaven?':'Jak wygląda życie seksualne w niebie?',
'There must be a lot of resentment in Hell.':'W piekle musi być sporo urazy.',
'1Hero! That is a symbol of Satanism!':'1Hero! To symbol satanizmu!',
'Shit. Doesn’t anyone on his team work weekends?':'Cholera. Nikt z jego zespołu nie pracuje w weekendy?',
'1Hero! There is no sex in heaven!':'1Hero! W niebie nie ma seksu!',
'As long as they are not among us in the Empyrean.':'Byle tylko nie znaleźli się wśród nas w Empyreum.',
'Are you that shocked? I mean, the mansion is being controlled by a demi-demon.':'Naprawdę cię to dziwi? Rezydencją rządzi półdemon.',
'You’re not a very good salesman, Arianna.':'Nie jesteś najlepszą handlarką, Arianno.',
'So hell is like a hot fiery rug that all the undesirables get swept under.':'Czyli piekło to ognisty dywan, pod który zamiata się wszystkich niepożądanych.',
'And just when I thought you had some good news.':'A już myślałem, że masz jakieś dobre wieści.',
'What do you think it means?':'Jak myślisz, co to znaczy?',
'A perfect way to put it!':'Świetnie to ująłeś!',
'It means that the demon wants to use those Toma pieces in some sort of satanic ritual.':'To znaczy, że demon chce użyć tych kawałków Tomy w jakimś satanistycznym rytuale.',
'That sounds like a recipe for disaster.':'Brzmi jak przepis na katastrofę.',
'Any guesses on what that ritual will do?':'Masz jakiś pomysł, do czego posłuży ten rytuał?',
'Perhaps I don’t quite understand.':'Chyba nie do końca rozumiem.',
"It could be to summon a demon, but that won't be possible since there are no more shell beings.":'Mogłoby chodzić o przyzwanie demona, ale to niemożliwe, bo nie ma już istot-powłok.',
'Except Madalyn.':'Poza Madalyn.',
'For Madalyn to accept a new soul she would have to remove her existing possession.':'Żeby Madalyn przyjęła nową duszę, musiałaby pozbyć się obecnego opętania.',
'Damalius…':'Damalius…',
'Do you think she’d give up that soul?':'Myślisz, że zrezygnowałaby z tej duszy?',
'I need to figure out what these Toma pieces are for.':'Muszę ustalić, do czego służą te kawałki Tomy.',
}
known=set()
for line in MERGED.read_text(encoding='utf8').splitlines():
 row=json.loads(line)
 if row['translation'].strip(): known.add(row['id'])
rows=[]; missing=set()
for line in CANON.read_text(encoding='utf8').splitlines():
 row=json.loads(line); c=row['context']
 if c.get('source_kind')=='map' and c.get('map_id')==3 and c.get('event_id')==39:
  if row['id'] in known: continue
  source=row['source_text'].strip()
  if source in {'…','...','..'} or source.startswith('/'): continue
  target=MAP.get(source)
  if target is None: missing.add(source); continue
  row['translation']=target; rows.append(row)
if missing: raise SystemExit('Unmapped map3 event 39 strings: '+repr(sorted(missing)))
OUT.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf8',newline='\n')
print(f'Wrote map 3 event 39 Toma/Empyrean dialogue: {len(rows)} records from {len(MAP)} source strings')
