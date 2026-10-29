import json
from pathlib import Path
ROOT=Path('games/the-genesis-order/translation')
CANON=ROOT/'export-v1/custom_dialogue.jsonl'
MERGED=Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step2.jsonl')
DRAFTS=ROOT/'drafts'
MAPS={
110:{
'Nellie? What are you doing here?':'Nellie? Co tu robisz?',
'Helping Tasha carry books.':'Pomagam Taszy nieść książki.',
'She insisted.':'Uparła się.',
'Maybe these Casula books will finally give you the answers you need.':'Może te księgi Casula wreszcie dadzą ci potrzebne odpowiedzi.',
'Just what the hell are you planning to do?':'Co ty, do cholery, planujesz?',
'I’m guessing we’ve not seen the last of that secret mansion basement.':'Zgaduję, że jeszcze nie raz trafimy do tej sekretnej piwnicy w rezydencji.',
'Oh, dear. I hope all the danger is behind us.':'Ojej. Mam nadzieję, że niebezpieczeństwo już minęło.',
'Don’t bet on it.':'Nie liczyłbym na to.',
'Do you expect me to sneak you into the mansion again?':'Oczekujesz, że znowu przemycę cię do rezydencji?',
'Come on, Nellie. I’ll explain what we know.':'Chodź, Nellie. Wyjaśnię ci, co wiemy.',
"Aren't you going to help them study?":'Nie pomożesz im w nauce?',
'I think I need a break.':'Chyba potrzebuję przerwy.',
'Working hard?':'Ciężko pracujesz?',
'I miss you, 1Hero.':'Tęsknię za tobą, 1Hero.',
'Sister Judy… We’ve barely been apart.':'Siostro Judy… Ledwie się rozstaliśmy.',
'Yet I can’t stop thinking about you.':'A jednak nie mogę przestać o tobie myśleć.',
"Y'all want to go on an adventure?":'Macie ochotę na przygodę?',
'We’re not going on an adventure.':'Nie wybieramy się na żadną przygodę.',
'I’m a bit busy.':'Jestem trochę zajęta.',
'Yes. We’re very busy.':'Tak. Jesteśmy bardzo zajęte.',
'Doing what?':'Czym?',
'Studying.':'Nauką.',
'Always hard at work.':'Zawsze takie pracowite.',
'Sounds boring.':'Brzmi nudno.',
'Let’s go to the basement!':'Chodźmy do piwnicy!',
'Be careful, Hannah.':'Uważaj, Hannah.',
'What’s wrong?':'Co się stało?',
'I wanted to speak to you in my bedroom.':'Chciałam z tobą porozmawiać w mojej sypialni.',
'Would the bathroom work?':'Może być łazienka?',
'Maybe.':'Może.',
'I can’t see, God damn it!':'Cholera jasna, nic nie widzę!',
'Don’t rub your eyes!':'Nie pocieraj oczu!',
'I got a splinter in my eye!':'Wpadła mi drzazga do oka!',
'Oh, my!':'Ojej!',
'It’s not a splinter.':'To nie drzazga.',
'It hurts!':'Boli!',
'Let’s rinse your eyes out with some water…':'Przepłuczmy ci oko wodą…',
'Sorry, Sister.':'Przepraszam, siostro.',
},
115:{
'Slow down, Miss Bhatt. What happened?':'Proszę zwolnić, panno Bhatt. Co się stało?',
'1Hero! Tell them what we saw.':'1Hero! Powiedz im, co widzieliśmy.',
'Well… Lillian was sucking my cock…':'Cóż… Lillian ssała mojego kutasa…',
'Not that part!':'Nie o tę część chodzi!',
'Lillian disappeared in front of your eyes?':'Lillian zniknęła na twoich oczach?',
'Did you find another magic rock?':'Znaleźliście kolejny magiczny kamień?',
'We have a bigger problem… The Toma Leolo might already be completed.':'Mamy większy problem… Toma Leolo może być już ukończona.',
'Shit. We have to act fast.':'Cholera. Musimy działać szybko.',
'I can sneak us into the mansion.':'Mogę przemycić nas do rezydencji.',
'What’s the problem?':'W czym problem?',
'We can’t let Lillian complete the Toma Leolo.':'Nie możemy pozwolić Lillian dokończyć Tomy Leolo.',
'What’s the big deal?':'W czym problem?',
'It’s a really big deal.':'To bardzo poważna sprawa.',
'Anyone who looks at the completed idol will die… But not in a good way.':'Każdy, kto spojrzy na ukończony posąg, umrze… Ale nie tak zwyczajnie.',
'Is there a good way to die?':'Jest jakiś dobry sposób na śmierć?',
'Your soul will die, but your body will remain.':'Umrze twoja dusza, ale ciało pozostanie.',
'Isn’t that how it usually works?':'Czy tak właśnie zwykle nie jest?',
'A fully animated and sentient body will remain.':'Pozostanie w pełni ruchome ciało, zachowujące świadomość.',
'Holy shit! I ain’t letting no one make my body smelly!':'O cholera! Nie pozwolę, żeby ktoś zrobił z mojego ciała śmierdzącego trupa!',
'If all she needs is my seed, then it might be too late.':'Jeśli potrzebuje tylko mojego nasienia, może być już za późno.',
'So what’s the plan?':'Jaki jest plan?',
'Stay here with the girls. I’ll go with 1Hero to the rift.':'Zostań tutaj z dziewczynami. Pójdę z 1Hero do rozdarcia.',
'Shouldn’t we call the police?':'Nie powinniśmy wezwać policji?',
'It’s not that simple.':'To nie takie proste.',
'Andrea’s operation is in the mansion… No police allowed.':'Operacja Andrei odbywa się w rezydencji… Policja nie może tam wejść.',
'I’m coming with you. I need to see this for myself.':'Idę z wami. Muszę zobaczyć to na własne oczy.',
'Heather… Carol… Can you keep watch?':'Heather… Carol… Możecie mieć oko na sytuację?',
'Of course!':'Oczywiście!',
'I can help too.':'Ja też mogę pomóc.',
'We’ll try and hurry, but I don’t know what to expect.':'Postaramy się pospieszyć, ale nie wiem, czego się spodziewać.',
'Without Nellie, we should sneak in through the back way…  Luckily there is a way through the bunker.':'Bez Nellie musimy zakraść się od tyłu… Na szczęście przez bunkier da się przejść.',
'In the caves?':'Przez jaskinie?',
'Yep. Right under the church.':'Tak. Prosto pod kościołem.',
'Woah!':'Łał!',
'Then let’s move.':'W takim razie ruszajmy.',
'1Hero… Be careful.':'1Hero… Uważaj na siebie.',
'I will… Make sure Judy is safe.':'Będę… Dopilnuj, żeby Judy była bezpieczna.',
'We have the holy cross. God is on our side.':'Mamy święty krzyż. Bóg jest po naszej stronie.',
'Hell yeah, he is.':'No jasne, że jest.',
'See you soon.':'Do zobaczenia.',
},
33:{
'What are we going to do now? Is Sister Judy safe?':'Co teraz zrobimy? Czy siostra Judy jest bezpieczna?',
"I won't leave her side. I’ll stay here in the church with her.":'Nie odstąpię jej na krok. Zostanę z nią w kościele.',
'Thank you, Father Solomon. You’ve been so kind to me.':'Dziękuję, ojcze Solomonie. Był pan dla mnie taki życzliwy.',
'I’ll get to the bottom of this. When I’m finished, Madalyn will be behind bars.':'Dojdę do prawdy. Gdy skończę, Madalyn trafi za kratki.',
'Sounds to me like that won’t hold her.':'Nie sądzę, żeby kraty ją powstrzymały.',
'Can you do an exorcism spell on her, Father?':'Może ojciec rzucić na nią zaklęcie wypędzające demony?',
'Haha. Oh, Chloe. It’s not that simple.':'Haha. Och, Chloe. To nie takie proste.',
'But if she fears us, she’ll keep her distance from me.':'Ale jeśli będzie się nas bała, nie zbliży się do mnie.',
'A true demon is no match for the power of God.':'Prawdziwy demon nie ma szans z mocą Boga.',
'I feel safe with you, Father. You have not let me down.':'Czuję się przy ojcu bezpiecznie. Nie zawiódł mnie pan.',
'I’ll stay with you too, Sister Judy…':'Ja też zostanę z tobą, siostro Judy…',
'At least until it’s time for bed.':'Przynajmniej do pory snu.',
'I very much enjoy our talks.':'Bardzo lubię nasze rozmowy.',
'We’re here for you.':'Jesteśmy przy tobie.',
'I can’t thank you enough.':'Nie wiem, jak ci dziękować.',
'Come on, Chloe. Let us speak alone, in my bedroom.':'Chodź, Chloe. Porozmawiajmy na osobności, w mojej sypialni.',
'Sure thing.':'Jasne.',
'Sister Judy has told me stories of her time at Saint Dame University…':'Siostra Judy opowiadała mi o swoich czasach na Uniwersytecie Saint Dame…',
'But I never imagined that evil woman being an actual demon.':'Ale nigdy nie przypuszczałem, że ta zła kobieta naprawdę jest demonem.',
'I would have thought that sounded crazy… But I’ve seen so much now. I believe it’s true.':'Uznałbym to za szaleństwo… Ale tyle już widziałem. Wierzę, że to prawda.',
"You're in deeper than you expected, I’m sure.":'Na pewno wplątałeś się w coś poważniejszego, niż się spodziewałeś.',
'You can say that again.':'Żebyś wiedział.',
'When it comes to the spiritual, I can help you.':'W sprawach duchowych mogę ci pomóc.',
'Come to me whenever you need help.':'Przyjdź do mnie, gdy będziesz potrzebował pomocy.',
'Thanks, Father Solomon.':'Dziękuję, ojcze Solomonie.',
},
97:{
'Duncan’s going to know where to find you.':'Duncan będzie wiedział, gdzie cię znaleźć.',
'Any way to bring back the police presence?':'Da się przywrócić policyjną ochronę?',
'The commissioner is going to have to make a move, undercover operation be damned.':'Pani komisarz będzie musiała zareagować. Niech diabli wezmą tajną operację.',
'He can only be alive because she wants him alive. There’s no other reason for it.':'On żyje tylko dlatego, że ona chce, żeby żył. Nie ma innego wytłumaczenia.',
'Duncan has too much influence… We should have known this would be impossible.':'Duncan ma zbyt duże wpływy… Powinniśmy wiedzieć, że to będzie niemożliwe.',
'Fuck that dude!':'Pieprzyć tego typa!',
'What’s going to happen to Lillian?... She’s going to be caught.':'Co się stanie z Lillian?... Złapią ją.',
'She’s probably hiding inside the rift… I don’t know if Duncan can chase her there.':'Pewnie ukrywa się w rozdarciu… Nie wiem, czy Duncan może za nią tam wejść.',
'That rift leads to hell. He’d be wise to not chase her.':'To rozdarcie prowadzi do piekła. Lepiej, żeby za nią nie szedł.',
'If Duncan comes looking for the priest, we can be here to intercept him.':'Jeśli Duncan przyjdzie po księdza, możemy tu na niego zaczekać.',
'Can we handle that?':'Damy sobie z tym radę?',
'I can help.':'Mogę pomóc.',
'Let me get with the commissioner. I’ll fix this.':'Porozmawiam z panią komisarz. Załatwię to.',
'It’s very late. I should get back home.':'Jest bardzo późno. Powinnam wracać do domu.',
'Lillian wants you, Erica. Stay away from the mansion.':'Lillian cię szuka, Erico. Trzymaj się z dala od rezydencji.',
'I know… I will.':'Wiem… Będę.',
'Thanks for your help, Erica.':'Dziękuję za pomoc, Erico.',
'I’ll stop by later. We can figure this out.':'Wpadnę później. Razem coś wymyślimy.',
'Of course.':'Oczywiście.',
'What’s going on? What are you studying?':'Co się dzieje? Czego się uczycie?',
'The Toma Leolo…':'Tomy Leolo…',
'I’ll show you everything we know.':'Pokażę ci wszystko, co wiemy.',
},
}
known=set()
for line in MERGED.read_text(encoding='utf8').splitlines():
 row=json.loads(line)
 if row['translation'].strip(): known.add(row['id'])
all_rows=[json.loads(line) for line in CANON.read_text(encoding='utf8').splitlines()]
for eid,mapping in MAPS.items():
 out=DRAFTS/f'custom-dialogue-map20-event-{eid}-01.jsonl'
 if out.exists(): raise SystemExit(f'Refusing to overwrite {out}')
 rows=[]; missing=set()
 for row in all_rows:
  c=row['context']
  if c.get('source_kind')!='map' or c.get('map_id')!=20 or c.get('event_id')!=eid or row['id'] in known: continue
  source=row['source_text'].strip()
  if source in {'…','...','..'} or source.startswith('/'): continue
  target=mapping.get(source)
  if target is None: missing.add(source); continue
  row['translation']=target; rows.append(row)
 if missing: raise SystemExit(f'Unmapped map 20 event {eid} strings: '+repr(sorted(missing)))
 out.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf8',newline='\n')
 print(f'Wrote map 20 event {eid}: {len(rows)} records from {len(mapping)} strings')
