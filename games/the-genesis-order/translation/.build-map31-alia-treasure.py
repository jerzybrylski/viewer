import json
from pathlib import Path
ROOT=Path('games/the-genesis-order/translation')
CANON=ROOT/'export-v1/custom_dialogue.jsonl'
MERGED=Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step3.jsonl')
OUT=ROOT/'drafts/custom-dialogue-map31-alia-treasure-01.jsonl'
if OUT.exists(): raise SystemExit(f'Refusing to overwrite {OUT}')
MAP={
'Did you find the three lost books?':'Znalazłeś trzy zaginione księgi?',
'Picking up a toy for the party?':'Kupujesz zabawkę na imprezę?',
'How are you holding up, now that your dad is in jail?':'Jak się trzymasz, teraz kiedy twój ojciec siedzi w więzieniu?',
'Have you found the treasure yet?':'Znalazłaś już skarb?',
'I’m working on it.':'Pracuję nad tym.',
'Not a bad idea, but no.':'Niezły pomysł, ale nie.',
'It’s where he belongs… It’s time to move on.':'Tam jest jego miejsce… Czas iść dalej.',
'Still working on it.':'Wciąż nad tym pracuję.',
'A toy for later.':'Zabawka na później.',
'What about you? Miss him?':'A ty? Tęsknisz za nim?',
'Ha! Hardly.':'Ha! Ani trochę.',
'I’m glad to be putting that life behind me.':'Cieszę się, że zostawiam tamto życie za sobą.',
'Are you sure? Don’t feel any pull to go back?':'Na pewno? Nie ciągnie cię, żeby tam wrócić?',
'You’d been doing it for so long.':'Robiłaś to przecież tak długo.',
'True, but I’d prefer to stay out of jail.':'To prawda, ale wolę nie wracać do więzienia.',
'What are they talking about?':'O czym oni rozmawiają?',
'Diana is leaving, I think, but some kind of unfinished business.':'Chyba Diana wyjeżdża, ale ma jeszcze jakieś niedokończone sprawy.',
'So you don’t know where it actually is?':'Czyli nie wiesz, gdzie dokładnie jest?',
'Sorry, all I know is that it’s in the caves.':'Przykro mi, wiem tylko, że jest w jaskiniach.',
'I have to get back to Cape Vedra…':'Muszę wracać do Cape Vedra…',
'If you can find the chest, use this key to open it.':'Jeśli znajdziesz skrzynię, otwórz ją tym kluczem.',
'Damn. How am I going to find anything in the caves?':'Cholera. Jak mam cokolwiek znaleźć w jaskiniach?',
'If only I knew someone who knows the caves…':'Gdybym tylko znała kogoś, kto zna te jaskinie…',
'What’s this about?':'O co chodzi?',
'A treasure hunt.':'O poszukiwanie skarbów.',
'Wait, what? Treasure?':'Zaraz, co? Skarb?',
'I found this Guild map lying around Duncan’s private things in the bunker.':'Znalazłam tę mapę Gildii wśród prywatnych rzeczy Duncana w bunkrze.',
'It’s a good bet that whatever treasure he buried is somewhere in the caves.':'Pewnie zakopał ten skarb gdzieś w jaskiniach.',
'What makes you think it’s buried treasure?':'Skąd wiesz, że to zakopany skarb?',
'It came with the key I just gave Tasha.':'Mapa była razem z kluczem, który właśnie dałam Taszy.',
'Help me out, detective? If you bring the chest here, I’ll unlock it.':'Pomożesz mi, pani detektyw? Przynieś tu skrzynię, a ją otworzę.',
'We’ll split whatever’s inside fifty-fifty.':'Podzielimy się po równo tym, co będzie w środku.',
'Why not just give me the key? Bringing a whole chest is cumbersome.':'Czemu po prostu nie dasz mi klucza? Targanie całej skrzyni jest kłopotliwe.',
'I want to be sure to get my fair share.':'Chcę mieć pewność, że dostanę swoją część.',
'You don’t trust me?':'Nie ufasz mi?',
'Don’t take it personally; I don’t trust anyone.':'Nie bierz tego do siebie. Nikomu nie ufam.',
'I taught you well.':'Dobrze cię nauczyłam.',
'Oh, please.':'Daj spokój.',
'Hey…':'Hej…',
'As much as I enjoy watching mother-daughter time, I need to get back to Cape Vedra.':'Choć lubię patrzeć na rodzinne chwile matki i córki, muszę wracać do Cape Vedra.',
'See ya, but leave Henry with me.':'Na razie. Zostaw mi tylko Henry’ego.',
'If you insist.':'Skoro nalegasz.',
'1Hero, here’s the treasure map.':'1Hero, oto mapa skarbu.',
'I’m going to have so much fun with Henry.':'Będę się świetnie bawić z Henrym.',
'Don’t you think you’d be better off with a tangible dick? 1Hero’s not bad.':'Nie byłoby ci lepiej z prawdziwym kutasem? Kutas 1Hero nie jest zły.',
'Eww, I’m not sharing a dick with you, Mom.':'Fuj, nie będę się z tobą dzielić kutasem, mamo.',
'Henry’s all the man that I’ll ever need.':'Henry to jedyny mężczyzna, jakiego potrzebuję.',
'He’s still in that crystal, huh?':'Wciąż jest w tym krysztale, co?',
'For sure. Here, I’ll prove it.':'Jasne. Zaraz ci udowodnię.',
'Henry! Get the fuck out of that crystal!':'Henry! Wypierdalaj z tego kryształu!',
'Tasha!? Are you in trouble?':'Tasha!? Masz kłopoty?',
'Ha, something like that.':'Ha, mniej więcej.',
'Hahaha!':'Hahaha!',
'Hey, maybe Henry could help 1Hero?':'Hej, może Henry mógłby pomóc 1Hero?',
'I don’t see how a ghost could help.':'Nie widzę, jak duch mógłby pomóc.',
'Hey! I’m more than capable of helping! Let me help!':'Hej! Doskonale nadaję się do pomocy! Pozwólcie mi pomóc!',
'You don’t even know what we’re talking about.':'Nawet nie wiesz, o czym rozmawiamy.',
'I’m really bored.':'Strasznie się nudzę.',
'I don’t know how Evie lived in there for so long.':'Nie wiem, jak Evie wytrzymała tam tak długo.',
'I don’t like the idea of parting with my boy toy.':'Nie podoba mi się myśl, że miałabym rozstać się z moim zabawkowym chłopakiem.',
'He does have experience with this kind of thing, doesn’t he?':'Ma doświadczenie w takich sprawach, prawda?',
'Hmm, true. Perhaps his know-how could prove useful.':'Hmm, racja. Jego doświadczenie może się przydać.',
'What are we talking about?':'O czym rozmawiamy?',
'Buried treasure.':'O zakopanym skarbie.',
'Oh boy, a treasure hunt!':'Ale super, poszukiwanie skarbów!',
'Ever the treasure hunter.':'Zawsze z ciebie poszukiwaczka skarbów.',
'Well, maybe it would do him some good to go on an adventure.':'Może dobrze mu zrobi taka przygoda.',
'Alright, let’s do it.':'Dobra, ruszajmy.',
'I won’t let you down.':'Nie zawiodę was.',
'In the meantime, I’ll just have to find something else to play with.':'W międzyczasie muszę znaleźć sobie coś innego do zabawy.',
'Actually, I know just the thing.':'Właściwie wiem, co może się przydać.',
'Hopefully something exciting.':'Oby to było coś ekscytującego.',
'You’re going to love it.':'Na pewno ci się spodoba.',
'Don’t have too much fun while we’re gone, ladies.':'Tylko nie bawcie się za dobrze pod naszą nieobecność, panie.',
}
known=set()
for line in MERGED.read_text(encoding='utf8').splitlines():
 row=json.loads(line)
 if row['translation'].strip(): known.add(row['id'])
rows=[]; missing=set()
for line in CANON.read_text(encoding='utf8').splitlines():
 row=json.loads(line); c=row['context']
 if c.get('source_kind')=='map' and c.get('map_id')==31 and c.get('event_id')==26:
  if row['id'] in known: continue
  source=row['source_text'].strip()
  if source in {'…','...','..'} or source.startswith('/'): continue
  target=MAP.get(source)
  if target is None: missing.add(source); continue
  row['translation']=target; rows.append(row)
if missing: raise SystemExit('Unmapped map31 event 26 strings: '+repr(sorted(missing)))
OUT.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf8',newline='\n')
print(f'Wrote map 31 Alia/Tasha treasure dialogue: {len(rows)} records from {len(MAP)} strings')
