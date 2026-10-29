import json
from pathlib import Path
ROOT=Path('games/the-genesis-order/translation')
CANON=ROOT/'export-v1/custom_dialogue.jsonl'
MERGED=Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step3.jsonl')
OUT=ROOT/'drafts/custom-dialogue-map31-followups-01.jsonl'
if OUT.exists(): raise SystemExit(f'Refusing to overwrite {OUT}')
MAPS={
22:{
'Did someone drop a book?':'Ktoś zgubił książkę?',
'1Hero… This is Alia.':'1Hero… To Alia.',
'Hello, Alia.':'Cześć, Alia.',
'She’s helping with the Casula studies.':'Pomaga nam w badaniach nad Casula.',
'Cool. Are you an expert on Casula culture?':'Fajnie. Znasz się na kulturze Casula?',
'I’m adopted.':'Jestem adoptowana.',
'She’s not an expert, 1Hero… These books are from Diana’s collection.':'Nie jest ekspertką, 1Hero… Te książki pochodzą ze zbiorów Diany.',
'I carried them here.':'Przyniosłam je tutaj.',
'I told you to put them in a bag.':'Mówiłam, żebyś włożyła je do torby.',
'You walked here from Cape Vedra?':'Przyszłaś tu pieszo z Cape Vedra?',
'Haha! No, silly. I came here in a car.':'Haha! Nie, głuptasie. Przyjechałam samochodem.',
'Are these all the books?':'To wszystkie książki?',
'Yep! I brought twelve books.':'Tak! Przyniosłam dwanaście książek.',
'There are only nine.':'Jest ich tylko dziewięć.',
'Hmm… I must have dropped a few.':'Hmm… Chyba kilka zgubiłam.',
'Did you leave them in your mom’s car?':'Zostawiłaś je w samochodzie mamy?',
'No! I had twelve books! I swear.':'Nie! Miałam dwanaście książek! Przysięgam.',
'She probably dropped them.':'Pewnie je zgubiła.',
'I did wander around a lot after I got here.':'Po przyjeździe sporo się tu kręciłam.',
'Oh, God. Why did I trust you with anything?':'O Boże. Czemu powierzyłem ci cokolwiek?',
'Well… We have nine books. That’s better than no books.':'Cóż… Mamy dziewięć ksiąg. To lepsze niż żadna.',
'Go find the lost books. I’m going to start reading.':'Idź poszukaj zaginionych książek. Ja zacznę czytać.',
'Are you running the porn shop now, Alia?':'To ty teraz prowadzisz sklep porno, Alia?',
'I hope not. I’m not good at running things.':'Mam nadzieję, że nie. Nie umiem niczym zarządzać.',
'I can help you find the lost books.':'Mogę pomóc ci znaleźć zaginione księgi.',
'Can you give me some clues?':'Możesz dać mi jakieś wskazówki?',
'I’m bad at clues too.':'Ze wskazówkami też kiepsko u mnie.',
'We’ll be heading over to the library shortly.':'Niedługo ruszymy do biblioteki.',
},
21:{
'It’s off now. How do you feel?':'Już wyłączone. Jak się czujesz?',
'What an awesome invention! This could change the sex toy world!':'Ale genialny wynalazek! Może zrewolucjonizować rynek zabawek erotycznych!',
'My friend likes to push boundaries.':'Moja przyjaciółka lubi przekraczać granice.',
'I’d love to meet her.':'Chętnie ją poznam.',
'As fun as that was, I don’t want to stick around if you’re going live.':'Choć było fajnie, nie chcę tu zostawać, jeśli zaraz zaczynasz transmisję na żywo.',
'Give me the phone, Tasha. I’ll schedule a live event.':'Daj mi telefon, Tasha. Zaplanuję transmisję na żywo.',
'No need. I’ll handle it.':'Nie trzeba. Sama się tym zajmę.',
'You know how to use Lustagram?':'Umiesz obsługiwać Lustagram?',
'You know, I have a shipment of love potions coming today.':'Wiesz, dziś ma przyjść dostawa eliksirów miłosnych.',
'You want me to review it?':'Mam ją zrecenzować?',
'I can’t leave the shop to go pick it up, but if you run to the warehouse and grab it for me, maybe we can do something tonight.':'Nie mogę zamknąć sklepu i po nią pojechać, ale jeśli skoczysz do magazynu i odbierzesz ją za mnie, może coś dziś wieczorem razem zrobimy.',
'Uhh… I can’t. I’m busy this afternoon.':'Eee… Nie mogę. Jestem dziś po południu zajęty.',
'I know Jon at the warehouse. I can grab it for you.':'Znam Jona z magazynu. Mogę ją dla ciebie odebrać.',
'Would you?':'Naprawdę?',
'Yeah, I can handle it.':'Tak, dam sobie z tym radę.',
'I’ll see if I can make time later for another stream.':'Zobaczę, czy później znajdę czas na kolejną transmisję.',
'Are you ready to go live?':'Gotowa na transmisję?',
'That’s my queue to leave.':'To mój znak, że pora wyjść.',
'Lock the door behind you.':'Zamknij za sobą drzwi.',
'There’s no way love potions work. But I’ll humor her and grab her package from the warehouse.':'Eliksiry miłosne na pewno nie działają. Ale niech jej będzie — odbiorę paczkę z magazynu.',
'I wonder why she doesn’t ship it straight to her store?':'Ciekawe, czemu nie wysyła tego prosto do sklepu.',
},
23:{
'Sounds like I missed all the fun.':'Wygląda na to, że ominęła mnie cała zabawa.',
'Promise?':'Obiecujesz?',
'Looking to buy something?':'Chcesz coś kupić?',
'You’re always welcome here, 1Hero.':'Zawsze jesteś tu mile widziany, 1Hero.',
"Use that treasure map to find the chest. Bring it to me and I'll unlock it.":'Znajdź skrzynię, korzystając z tej mapy skarbów. Przynieś ją, a otworzę zamek.',
'We make a good team, Detective Canmore.':'Dobrze nam się współpracuje, detektywie Canmore.',
'Enjoying your new home?':'Podoba ci się nowy dom?',
},
14:{
'What the hell? Where is Tasha?':'Co jest, do cholery? Gdzie jest Tasha?',
'She must be in the back room. She wouldn’t just leave the store unattended.':'Musi być na zapleczu. Nie zostawiłaby sklepu bez opieki.',
'1Hero. I don’t sense Tasha anywhere nearby.':'1Hero. Nigdzie w pobliżu nie wyczuwam Tashy.',
'Huh? What the hell is she thinking?':'Co? Co ona sobie myśli?',
'She is picking up a shipment that has arrived from a far away land.':'Odbiera dostawę, która przybyła z dalekiej krainy.',
'Hmm. I wonder where that could be.':'Hmm. Ciekawe, skąd mogła przybyć.',
'You fucked me over, Tasha.':'Wystawiłaś mnie, Tasha.',
'I got fired after everyone saw the sex video you recorded.':'Wyrzucili mnie z pracy, kiedy wszyscy zobaczyli nagrany przez ciebie filmik erotyczny.',
'Oh, that thing?':'A, ten filmik?',
'Yeah! That thing!':'Tak! Właśnie ten!',
'That’s a lame thing to get fired over.':'Zwolnienie za coś takiego to żenada.',
'Why the hell did you do it?':'Po co, do cholery, to zrobiłaś?',
'There’s a record button on the phone! If I see a button, I’m going to hit it.':'W telefonie jest przycisk nagrywania! Jak widzę przycisk, to go naciskam.',
'What kind of excuse is that?':'Co to za wymówka?',
'Listen! You just need to change your style and lay low for a while. Then you’ll get your job right back.':'Słuchaj! Zmień styl i przez jakiś czas się nie wychylaj. Wtedy odzyskasz pracę.',
'That’s not how it works.':'To tak nie działa.',
'You should wear a mustache. It’ll make you look more like a cop. They’ll love it.':'Powinnaś zapuścić wąsy. Będziesz wyglądać bardziej jak gliniarz. Na pewno im się spodoba.',
'That’s the stupidest idea I’ve ever heard.':'To najgłupszy pomysł, jaki słyszałem.',
'Wear it and go lay on the charm.':'Załóż je i oczaruj wszystkich.',
'You’re a real troublemaker, you know that?':'Wiesz, że jesteś niezłym urwisem?',
},
20:{
'It’s so… colorful.':'Ależ… kolorowo.',
'You better watch yourself, Sister. You don’t want to get addicted to a place like this.':'Lepiej uważaj, siostro. Nie chcesz się uzależnić od takiego miejsca.',
"Don’t worry, we won't stay long.":'Nie martw się, nie zostaniemy tu długo.',
'Give me the black one.':'Daj mi ten czarny.',
'The vibrator?':'Wibrator?',
'Find something you like?':'Znalazłaś coś, co ci się podoba?',
'Come here, 1Hero.':'Chodź tutaj, 1Hero.',
'It vibrates like hell.':'Ależ mocno wibruje.',
'Vibrate?':'Wibruje?',
'Judy… I’m sorry.':'Judy… Przepraszam.',
'I don’t know what tastes better, 1Hero’s cum or Erica’s mouth.':'Nie wiem, co smakuje lepiej: sperma 1Hero czy usta Eriki.',
'Do I taste like beer?':'Czy smakuję jak piwo?',
'Hahahaha!':'Hahahaha!',
'I… I’ve got to leave.':'Ja… Muszę już iść.',
'Oh, no. We went too far.':'O nie. Posunęliśmy się za daleko.',
'I want to buy one!':'Chcę jeden kupić!',
'We’re too much for her, 1Hero.':'Jesteśmy dla niej zbyt przytłaczający, 1Hero.',
},
27:{
'Where did you go today?':'Gdzie dziś byłaś?',
'I went to the library and then Mom drove me here.':'Byłam w bibliotece, a potem mama mnie tu podwiozła.',
'What did you do after you got here?':'Co robiłaś, kiedy już tu dotarłaś?',
'I was hungry, so I ate.':'Byłam głodna, więc coś zjadłam.',
'What did you eat?':'Co zjadłaś?',
'I wanted a ketchup sandwich, but the chef made me make my own and called me an idiot.':'Chciałam kanapkę z keczupem, ale kucharz kazał mi zrobić ją samej i nazwał mnie idiotką.',
'Feel free to talk to me again if you need more help.':'Wróć do mnie, jeśli będziesz potrzebować dalszej pomocy.',
},
33:{
'That’s weird. Where are Tasha and Nellie?':'Dziwne. Gdzie są Tasha i Nellie?',
'Have you seen Tasha or Nellie?':'Widziałeś Tashę albo Nellie?',
'They went to the back.':'Poszły na zaplecze.',
'Anytime, 1Hero. But I should warn you: they’re a bit preoccupied.':'Kiedy tylko chcesz, 1Hero. Ostrzegam tylko, że są trochę zajęte.',
'Preoccupied?':'Zajęte?',
},
29:{
'Do you think Kimberly is okay? I hope we can find a way to save her.':'Myślisz, że Kimberly nic nie jest? Mam nadzieję, że znajdziemy sposób, by ją ocalić.',
'We’ll find a way to save her, Erica.':'Znajdziemy sposób, żeby ją ocalić, Erico.',
'As long as she doesn’t keep running back in every time we get her out.':'O ile nie będzie za każdym razem wracać tam, gdy ją stamtąd wyciągniemy.',
},
31:{"Sorry, 1Hero. I'm busy with treasure hunter business.":'Przykro mi, 1Hero. Mam sprawy związane z poszukiwaniem skarbów.'},
}
known=set()
for line in MERGED.read_text(encoding='utf8').splitlines():
 row=json.loads(line)
 if row['translation'].strip(): known.add(row['id'])
all_rows=[json.loads(line) for line in CANON.read_text(encoding='utf8').splitlines()]
rows=[]; missing={}
for row in all_rows:
 c=row['context']
 if c.get('source_kind')!='map' or c.get('map_id')!=31 or row['id'] in known: continue
 eid=c.get('event_id'); mapping=MAPS.get(eid)
 if mapping is None: continue
 source=row['source_text'].strip()
 if source in {'…','...','..'} or source.startswith('/'): continue
 target=mapping.get(source)
 if target is None: missing.setdefault(eid,set()).add(source); continue
 row['translation']=target; rows.append(row)
if missing: raise SystemExit('Unmapped Map 31 follow-up strings: '+repr({e:sorted(v) for e,v in missing.items()}))
OUT.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf8',newline='\n')
print(f'Wrote remaining Map 31 story/shop dialogue: {len(rows)} records across {len(MAPS)} events')
