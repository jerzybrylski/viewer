import json
import collections
from pathlib import Path
ROOT=Path('games/the-genesis-order/translation')
CANON=ROOT/'export-v1/custom_dialogue.jsonl'
MERGED=Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step3.jsonl')
OUT=ROOT/'drafts/custom-dialogue-map20-followups-01.jsonl'
if OUT.exists(): raise SystemExit(f'Refusing to overwrite {OUT}')
MAPS={
57:{
'1Hero! You came.':'1Hero! Przyszedłeś.',
'Of course, Sister Judy. We need to clean that room of yours.':'Oczywiście, siostro Judy. Musimy posprzątać twój pokój.',
'It’s pretty bad, 1Hero… It smells like mold.':'Jest naprawdę źle, 1Hero… Czuć stęchliznę.',
'Oh, boy. That’s not good.':'Ojej. To niedobrze.',
'I hope the bed is not ruined. We can’t afford to be buying new beds with our low attendance.':'Mam nadzieję, że łóżko nie jest zniszczone. Przy tak niskiej frekwencji nie stać nas na nowe.',
'I’m sure we can clean it.':'Na pewno uda nam się je wyczyścić.',
'Come on. Let’s get to work.':'No chodź. Zabierajmy się do pracy.',
'I feel very refreshed today. I slept so well last night.':'Czuję się dziś wypoczęta. Wczoraj w nocy świetnie spałam.',
},
29:{
'I’ll check the west end. But she may have gone outside.':'Sprawdzę zachodnią część. Mogła jednak wyjść na zewnątrz.',
'Does she ever go into town?':'Czy ona czasem jeździ do miasta?',
'I’m the one who does the shopping. Judy prefers to stay at the church…':'To ja robię zakupy. Judy woli zostawać w kościele…',
'This is unusual for her.':'To do niej niepodobne.',
'We’ll find her. Don’t worry.':'Znajdziemy ją. Nie martw się.',
},
28:{
'What brings you here, 1Hero?':'Co cię tu sprowadza, 1Hero?',
'Father Solomon is away, shopping. I am watching the church while he is away.':'Ojciec Solomon wyszedł na zakupy. Pilnuję kościoła, póki go nie ma.',
'Do you need to investigate anything here?':'Musisz tu coś zbadać?',
'Nothing planned. But you never know where a clue might pop up.':'Nie mam planów. Nigdy nie wiadomo, gdzie trafi się wskazówka.',
},
42:{
'I can use my container to collect some of this holy water.':'Mogę użyć swojego pojemnika, żeby nabrać trochę tej wody święconej.',
'If I had a container I could collect some of this holy water.':'Gdybym miał pojemnik, mógłbym nabrać trochę tej wody święconej.',
'What if I used an unholy container to collect holy water?':'A gdybym użył nieświętego pojemnika do nabrania wody święconej?',
},
100:{
'Ugh! I’m mortified that Mom saw us.':'Ugh! Umieram ze wstydu, że mama nas zobaczyła.',
'We were just having fun. It’s not a big deal.':'Po prostu dobrze się bawiliśmy. To nic takiego.',
'It’s just weird… That’s all.':'To po prostu dziwne… Tyle.',
},
117:{
'Tasha said you came all over a book. Must have been a really good book!':'Tasha mówiła, że spuściłeś się na książkę. Musiała być naprawdę ciekawa!',
'You know you can count on me if you need muscle.':'Możesz na mnie liczyć, jeśli potrzebujesz krzepy.',
'I’ll keep you in mind, Hannah.':'Będę o tym pamiętał, Hannah.',
},
120:{
'All’s clear, detective. No sign of any ghosts here.':'Czysto, pani detektyw. Nie ma tu żadnych duchów.',
'Something seems off about Erica.':'Z Ericą jest chyba coś nie tak.',
'I’ll explain everything later, Carol.':'Wszystko wyjaśnię później, Carol.',
},
15:{
'I hope you solve your case, 1Hero. I believe in you.':'Mam nadzieję, że rozwiążesz tę sprawę, 1Hero. Wierzę w ciebie.',
'Thanks, Chloe. And if I can help you in any way, let me know.':'Dzięki, Chloe. Jeśli mogę ci jakoś pomóc, daj znać.',
},
23:{
'Please help us with the broken rigging cable. The chapel is a dangerous place with a swinging chandelier.':'Pomóż nam naprawić zerwaną linę podtrzymującą żyrandol. Kołyszący się żyrandol sprawia, że kaplica jest niebezpieczna.',
'You are a kind man, 1Hero.':'Jesteś dobrym człowiekiem, 1Hero.',
},
38:{
'Sister Judy is safe. Perhaps I should go with you.':'Siostra Judy jest bezpieczna. Może powinienem pójść z tobą.',
'Stay here with Judy. If I see anything, I’ll come back for you.':'Zostań tutaj z Judy. Jeśli coś zauważę, wrócę po ciebie.',
},
39:{
'Please be careful, 1Hero.':'Uważaj na siebie, 1Hero.',
'I will, Chloe.':'Będę, Chloe.',
},
51:{
'Uhh, guys. We have a big problem.':'Eee, słuchajcie. Mamy poważny problem.',
'It’s the leak…':'Chodzi o przeciek…',
},
56:{
'The police officer is not very friendly.':'Ten policjant nie jest zbyt miły.',
'He’s a pain in the ass for sure, but he’ll keep you safe.':'To upierdliwy typ, ale będzie was chronił.',
},
68:{
'She’s getting ready. When does church start?':'Przygotowuje się. Kiedy zaczyna się msza?',
'One hour… I just pray that people show up.':'Za godzinę… Oby tylko ludzie przyszli.',
},
99:{
'Still hanging around the church?':'Wciąż kręcisz się przy kościele?',
'You’ll be able to go home tonight. I’ll make sure everything’s okay.':'Dziś wieczorem będziesz mogła wrócić do domu. Dopilnuję, żeby wszystko było w porządku.',
},
104:{
'Where is the detective?':'Gdzie jest detektyw?',
'Melissa should be here soon.':'Melissa powinna niedługo przyjść.',
},
108:{
'Do I smell funny?':'Czy dziwnie pachnę?',
'My face smells like bleach.':'Moja twarz pachnie wybielaczem.',
},
109:{
'I wonder where Mom went.':'Ciekawe, dokąd poszła mama.',
'Something seemed funny about Carol and Mom.':'Z Carol i mamą było coś dziwnego.',
},
118:{
'Tasha sure does know a lot about history.':'Tasha naprawdę dużo wie o historii.',
'Don’t get hurt, 1Hero. Come back safe.':'Nie daj się zranić, 1Hero. Wróć cały i zdrowy.',
},
1:{'I don’t think we should wander until our tasks are complete.':'Nie powinniśmy się włóczyć, dopóki nie wykonamy wszystkich zadań.'},
24:{'I’ve got my eye on you, 1Hero.':'Będę cię obserwować, 1Hero.'},
63:{'This will be a long night.':'To będzie długa noc.'},
64:{'We’ve got things under control. I feel safer knowing we’re being looked after.':'Panujemy nad sytuacją. Czuję się bezpieczniej, wiedząc, że ktoś nas pilnuje.'},
102:{'1Hero! The consequences would be dire!':'1Hero! Konsekwencje byłyby tragiczne!'},
103:{'I’m not too happy about hanging around here.':'Niezbyt mi się podoba to siedzenie tutaj.'},
105:{'I do hope everyone stays safe.':'Mam nadzieję, że wszystkim nic się nie stanie.'},
106:{'Be careful at the mansion, 1Hero.':'Uważaj w rezydencji, 1Hero.'},
107:{'Thank the Lord that Father Brian wasn’t here… Hannah was buck naked!':'Dzięki Bogu, że ojca Briana tu nie było… Hannah była kompletnie naga!'},
121:{'Despite your best efforts to defile this book, I’m still able to read it.':'Mimo twoich starań, by sprofanować tę księgę, wciąż potrafię ją odczytać.'},
}
known=set()
for line in MERGED.read_text(encoding='utf8').splitlines():
 row=json.loads(line)
 if row['translation'].strip(): known.add(row['id'])
rows=[]; missing=collections.defaultdict(set)
for line in CANON.read_text(encoding='utf8').splitlines():
 row=json.loads(line); c=row['context']
 if c.get('source_kind')!='map' or c.get('map_id')!=20 or row['id'] in known: continue
 eid=c.get('event_id'); mapping=MAPS.get(eid)
 if mapping is None: continue
 source=row['source_text'].strip()
 if source in {'…','...','..'} or source.startswith('/'): continue
 target=mapping.get(source)
 if target is None: missing[eid].add(source); continue
 row['translation']=target; rows.append(row)
if missing: raise SystemExit('Unmapped follow-up strings: '+repr({e:sorted(v) for e,v in missing.items()}))
OUT.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf8',newline='\n')
print(f'Wrote remaining Map 20 story dialogue: {len(rows)} records across {len(MAPS)} events')
