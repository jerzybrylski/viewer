import json
from pathlib import Path
ROOT=Path('games/the-genesis-order/translation')
CANON=ROOT/'export-v1/custom_dialogue.jsonl'
MERGED=Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step3.jsonl')
DRAFTS=ROOT/'drafts'
MAPS={
25:{
'I found the lost books.':'Znalazłam zaginione księgi.',
'We need to bring these back to Dad.':'Musimy zanieść je tacie.',
'I want to meet your dad!':'Chcę poznać twojego tatę!',
'You have to stay here and run the porn shop.':'Musisz tu zostać i prowadzić sklep porno.',
'You trust me with that?':'Powierzasz mi to?',
'No.':'Nie.',
'Oh.':'Och.',
'Mom! What are you doing here?':'Mamo! Co tu robisz?',
'Who’s the new girl?':'Kim jest ta nowa dziewczyna?',
'I’m Alia! You must be Tasha’s mom.':'Jestem Alia! Ty pewnie jesteś mamą Tashy.',
'How’d you guess?':'Jak zgadłaś?',
'‘Cause Tasha just said it.':'Bo Tasha właśnie mi powiedziała.',
'Mom’s going to be away longer, dear.':'Mamo, dłużej cię nie będzie, kochanie.',
'You’re in too deep, aren’t you?':'Wplątałaś się w coś poważnego, co?',
'The case has gotten a lot more complicated.':'Śledztwo mocno się skomplikowało.',
'Duncan’s not going to jail any time soon… It’s hard to explain.':'Duncan szybko nie trafi do więzienia… Trudno to wyjaśnić.',
'It’s top secret.':'To ściśle tajne.',
'What’s going on?':'Co się dzieje?',
'I thought Duncan was supposed to be dead.':'Myślałam, że Duncan miał nie żyć.',
'It’s not that easy.':'To nie takie proste.',
'Where are your friends?':'Gdzie są twoi przyjaciele?',
'Looking for your big, fat boyfriend.':'Szukają twojego wielkiego, grubego chłopaka.',
'They need to back off.':'Muszą się od niego odczepić.',
'Duncan is a threat to all of us. He’ll come back to Cape Vedra for revenge.':'Duncan zagraża nam wszystkim. Wróci do Cape Vedra, żeby się zemścić.',
'He’s under control now… Someone else is pulling the strings.':'Jest już pod kontrolą… Ktoś inny pociąga za sznurki.',
'Fuck that. Why would we leave him alive?':'Pieprzyć to. Czemu mielibyśmy zostawić go przy życiu?',
'Mom’s going to be mad if that man doesn’t kick the bucket.':'Mama się wścieknie, jeśli ten facet nie kopnie w kalendarz.',
'You’re putting us between a rock and hard place.':'Stawiasz nas między młotem a kowadłem.',
'Not my problem.':'To nie mój problem.',
'I have to leave. I have to bring these books to Dad.':'Muszę iść. Zaniosę te księgi tacie.',
'What is he studying?':'Nad czym pracuje?',
'These are Casula studies… We’re investigating the Idol of Souls.':'To księgi o Casula… Badamy Idola Dusz.',
'Let me help you with those.':'Pozwól, że ci pomogę.',
'I don’t need help.':'Nie potrzebuję pomocy.',
'Tasha… I’m your mother.':'Tasha… Jestem twoją matką.',
'Ugh! Fine…':'Ech! No dobra…',
'Alia!':'Alia!',
'Yes!?':'Tak!?',
'If anyone comes in, sell them porn and shit.':'Jeśli ktoś wejdzie, sprzedawaj mu pornografię i inne takie.',
'Yes!':'Tak!',
'And don’t let anyone steal anything.':'I nikomu nie pozwól niczego ukraść.',
'Only paying customers. Got it!':'Tylko płacący klienci. Jasne!',
'Are you going to be okay?':'Wszystko będzie dobrze?',
'Hmm… I doubt it.':'Hmm… Wątpię.',
'Well… Good luck.':'Cóż… Powodzenia.',
'Thanks!':'Dzięki!',
},
5:{
'See ya around, Tasha.':'Do zobaczenia, Tasha.',
'Careful out there, Henry.':'Uważaj na siebie, Henry.',
'Excuse me.':'Przepraszam.',
'Looking for something?':'Szukacie czegoś?',
'Oh, we’re just here because…':'Och, przyszliśmy tylko, bo…',
'I’ve never been in a porn shop before!':'Nigdy wcześniej nie byłam w sklepie porno!',
'These your girlfriends?':'To twoje dziewczyny?',
'Oh, uhhh. Just friends.':'Och, eee… Tylko przyjaciółki.',
'Just friends? Maybe you people avoided the infection.':'Tylko przyjaciółki? Może wam udało się uniknąć infekcji.',
'Infection?':'Infekcji?',
'There’s a sex virus going around.':'Krąży wirus przenoszony drogą płciową.',
'I don’t believe in that nonsense.':'Nie wierzę w takie bzdury.',
'The redhead is right. It’s a real thing.':'Ruda ma rację. To prawdziwa sprawa.',
'My name’s Hannah.':'Jestem Hannah.',
'Hello, Hannah. I like your style.':'Cześć, Hannah. Podoba mi się twój styl.',
'Why thank you, city girl.':'Dziękuję, mieszczucho.',
'Call me Tasha.':'Mów mi Tasha.',
'This here is my best friend Chloe.':'To moja najlepsza przyjaciółka Chloe.',
'And who’s the stud?':'A kto to ten przystojniak?',
'That’s 1Hero.':'To 1Hero.',
'I can’t believe you’re not tapping these sexy girls you’ve brought in here.':'Nie wierzę, że nie zaliczasz tych seksownych dziewczyn, które tu przyprowadziłeś.',
'Hey! This was Hannah’s idea.':'Hej! To był pomysł Hannah.',
'Can I interest you in a dildo? Or a pair of handcuffs?':'Może dildo? Albo para kajdanek?',
'1Hero’s already got the handcuffs.':'1Hero już ma kajdanki.',
'No, I don’t.':'Nie mam.',
'I’m a detective.':'Jestem detektywką.',
'I hope you’re not here for anything I’ve done.':'Mam nadzieję, że nie przyszłaś mnie aresztować.',
'Should I be worried?':'Mam się martwić?',
'Maybe what you three need is a good love potion.':'Może wam trojgu przydałby się dobry eliksir miłosny.',
'You sell love potions?':'Sprzedajesz eliksiry miłosne?',
'Best deal in town. I get them straight from the manufacturer.':'Najlepszy interes w mieście. Biorę je prosto od producenta.',
'No, thank you. We’re just looking.':'Nie, dziękujemy. Tylko się rozglądamy.',
'I think Chloe should buy a love potion.':'Myślę, że Chloe powinna kupić eliksir miłosny.',
'Hey! Why not you? You’re the one who is into this stuff.':'Hej! A czemu nie ty? To ty się tym interesujesz.',
'No, I’m not! I just wanted to see.':'Wcale nie! Chciałam tylko zobaczyć.',
'Resist all you want. But ever since the virus, this place has been booming.':'Możesz się opierać, ile chcesz. Odkąd pojawił się wirus, ten sklep przeżywa oblężenie.',
'Is that a real thing?':'To naprawdę istnieje?',
'Ignore your detective boyfriend. The virus is very real, and if you’re not infected now, you will be soon.':'Nie słuchaj swojego detektywa. Wirus naprawdę istnieje i jeśli jeszcze się nim nie zaraziłaś, wkrótce to nastąpi.',
'Okay, enough scary stories. Let’s get out of here.':'Dobra, koniec tych strasznych opowieści. Chodźmy stąd.',
'Oh my god! Look at these magazines!':'O mój Boże! Popatrzcie na te magazyny!',
'What are you into? We’ve got a bit of everything.':'Co cię interesuje? Mamy tu wszystko.',
}
}
known=set()
for line in MERGED.read_text(encoding='utf8').splitlines():
 row=json.loads(line)
 if row['translation'].strip(): known.add(row['id'])
all_rows=[json.loads(line) for line in CANON.read_text(encoding='utf8').splitlines()]
for eid,mapping in MAPS.items():
 out=DRAFTS/f'custom-dialogue-map31-event-{eid}-01.jsonl'
 if out.exists(): raise SystemExit(f'Refusing to overwrite {out}')
 rows=[]; missing=set()
 for row in all_rows:
  c=row['context']
  if c.get('source_kind')!='map' or c.get('map_id')!=31 or c.get('event_id')!=eid or row['id'] in known: continue
  source=row['source_text'].strip()
  if source in {'…','...','..'} or source.startswith('/'): continue
  target=mapping.get(source)
  if target is None: missing.add(source); continue
  row['translation']=target; rows.append(row)
 if missing: raise SystemExit(f'Unmapped map31 event {eid} strings: '+repr(sorted(missing)))
 out.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf8',newline='\n')
 print(f'Wrote map 31 event {eid}: {len(rows)} records from {len(mapping)} strings')
