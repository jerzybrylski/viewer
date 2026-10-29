import json
from pathlib import Path
ROOT=Path('games/the-genesis-order/translation')
CANON=ROOT/'export-v1/custom_dialogue.jsonl'
MERGED=Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step2.jsonl')
DRAFTS=ROOT/'drafts'
MAPS={
36:{
'You are certainly popular with the ladies.':'Cieszą się tobą wszystkie kobiety.',
'1Hero… Sister Judy told me what happened.':'1Hero… Siostra Judy opowiedziała mi, co się stało.',
'Everything that happened?':'Wszystko?',
'We must find a relic to save Erica!':'Musimy znaleźć relikwię, żeby ocalić Ericę!',
'And Lilith plans to attack… So we must also find the amulets.':'Lilith szykuje atak… Musimy też znaleźć amulety.',
'We’ll find the amulets.':'Znajdziemy amulety.',
'We have to hurry… Lillian has access to Ella’s Lustagram account.':'Musimy się pospieszyć… Lillian ma dostęp do konta Elli na Lustagramie.',
'What does that mean?':'Co to znaczy?',
'Shit… It means she’s going to post the Toma online.':'Cholera… Zamierza opublikować Tomę w internecie.',
'We have to move fast.':'Musimy działać szybko.',
'But we can’t harm Lilith… She’s the one who can bring back Erica.':'Ale nie możemy skrzywdzić Lilith… Tylko ona może przywrócić Ericę.',
'Then you better hurry up, because we can’t risk the fate of the world to save one person.':'Lepiej się pospieszcie, bo nie możemy ryzykować losu świata, żeby ocalić jedną osobę.',
'We don’t even know what the hell these amulets will do to her.':'Nawet nie wiemy, co te cholerne amulety jej zrobią.',
'That’s true… Even if we had them, I don’t know how to use them.':'To prawda… Nawet gdybyśmy je mieli, nie wiem, jak ich użyć.',
'Sounds like more reading is in store.':'Wygląda na to, że czeka nas dalsze czytanie.',
'What about the holy relic?':'A co ze świętą relikwią?',
'Now that we have.':'Tę już mamy.',
'Where?':'Gdzie?',
'I’m sure Zephaniah knew.':'Zephaniah na pewno wiedział.',
'You don’t know where he would have kept holy relics?':'Nie wiesz, gdzie mógł trzymać święte relikwie?',
'This place has a lot of junk lying around. Zephaniah was not the most organized priest…':'Wszędzie walają się tu różne graty. Zephaniah nie był najbardziej uporządkowanym księdzem…',
'I’m sure most of the stuff you’ll find here is fake.':'Większość rzeczy, które tu znajdziesz, na pewno jest fałszywa.',
'But we’re a Catholic church. Surely we have genuine relics.':'Ale to katolicki kościół. Na pewno mamy prawdziwe relikwie.',
'I fail to see how a relic is going to bring back Erica.':'Nie rozumiem, jak relikwia miałaby przywrócić Ericę.',
'Erica will have to put it inside of her… body.':'Erica będzie musiała włożyć ją do swojego… ciała.',
'Wait… What?':'Zaraz… Co?',
'She has to sin against God.':'Musi zgrzeszyć przeciwko Bogu.',
'Oh, my…':'Ojej…',
'Blasphemy?':'Bluźnierstwo?',
'Yep… Right in the pussy.':'Tak… Prosto do cipki.',
'Just whose idea was this?':'Czyj to był pomysł?',
'It’s Lilith’s plan… But it makes sense when you think about it.':'To plan Lilith… Ale kiedy się nad tym zastanowić, ma sens.',
'No need to sell me. I like the idea.':'Nie musisz mnie przekonywać. Podoba mi się ten pomysł.',
'How the hell is this supposed to work?':'Jak to, do cholery, ma zadziałać?',
'Well… God sends Erica to Hell… Lillian gives Erica her body back… She walks out of the rift a free woman.':'Bóg zsyła Ericę do piekła… Lillian oddaje jej ciało… A ona wychodzi z rozdarcia jako wolna kobieta.',
'Hence why we can’t close the rift and banish Lilith until Erica is back here alive.':'Dlatego nie możemy zamknąć rozdarcia ani wygnać Lilith, dopóki Erica nie wróci tu żywa.',
'That was her plan.':'Taki był jej plan.',
'No biggie. Save Erica, then kill Lillian. Easy.':'Żaden problem. Ocalimy Ericę, a potem zabijemy Lillian. Proste.',
'Then you better find the relic soon.':'Lepiej szybko znajdźcie tę relikwię.',
'Dad and I will figure out how to fuck Lilith up with the amulets.':'Tata i ja wymyślimy, jak za pomocą amuletów dokopać Lilith.',
'I can help you search, but how will we know if the relic is genuine?':'Mogę pomóc wam szukać, ale skąd będziemy wiedzieć, czy relikwia jest prawdziwa?',
'I can help with that.':'Mogę w tym pomóc.',
'I know we’re all running on fumes, but let’s stay focused. We all know what needs to be done.':'Wiem, że wszyscy jesteśmy wykończeni, ale skupmy się. Wiemy, co trzeba zrobić.',
'We can’t trust Lilith. If we know how to take out Lilith, we need to do it.':'Nie możemy ufać Lilith. Jeśli wiemy, jak ją pokonać, musimy to zrobić.',
'We’ll find the relic. Don’t worry.':'Znajdziemy relikwię. Nie martw się.',
'We’ll start the search for the amulets.':'Zaczniemy szukać amuletów.',
'The cops are all over the mansion.':'W rezydencji roi się od glin.',
'We’ll do it in secret.':'Zrobimy to potajemnie.',
'I’ll give you a description of the amulets so you know what to look for.':'Opiszę wam amulety, żebyście wiedzieli, czego szukać.',
'Thanks, Father.':'Dziękuję, ojcze.',
'I guess it’s up to us to find that relic.':'Chyba to na nas spadło znalezienie relikwii.',
'Arianna… How do we find it?':'Arianno… Jak ją znajdziemy?',
'A true holy relic causes pain to demons that are scheming against God.':'Prawdziwa święta relikwia sprawia ból demonom knującym przeciwko Bogu.',
'So… We need Lilith’s help?':'Czyli… Potrzebujemy pomocy Lilith?',
'Not exactly… The line between angel and demon is shaded with gray.':'Niezupełnie… Granica między aniołem a demonem nie jest wyraźna.',
'What does that mean?':'Co to znaczy?',
'I can sense the pain, too.':'Ja również potrafię wyczuć ten ból.',
'How does it work?':'Jak to działa?',
'I must approach the darkness… As I get closer, I will feel pain… Then I will sense the source of the pain.':'Muszę zbliżyć się do mroku… Im bliżej będę, tym mocniej zaboli… Wtedy wyczuję źródło bólu.',
'Like a metal detector.':'Jak wykrywacz metalu.',
'What darkness do you speak of?':'O jakim mroku mówisz?',
'Don’t worry about that. It’s something I have to figure out.':'Nie martw się tym. Muszę sama to rozgryźć.',
'We’re running low on time.':'Kończy nam się czas.',
'Everyone, split up. Bring anything you think might be a holy relic to me… I will test it.':'Rozdzielmy się. Przynieście mi wszystko, co może być świętą relikwią… Sprawdzę to.',
'I will do my best.':'Zrobię, co w mojej mocy.',
'Let’s hurry.':'Pospieszmy się.',
},
119:{
'Don’t leave Nellie waiting.':'Nie każ Nellie czekać.',
'Are the police helping you?':'Policja ci pomaga?',
'They are at the mansion… But there’s something else I must do.':'Są w rezydencji… Ale muszę jeszcze coś zrobić.',
'1Hero? Erica?...':'1Hero? Erico?...',
'What happened at Channel 4?':'Co się stało w Channel 4?',
'Uhh… We stopped the monster.':'Eee… Powstrzymaliśmy potwora.',
'What’s with the new outfit?':'Co to za nowy strój?',
'Umm… I was shopping at the angel store.':'Eee… Kupiłam go w sklepie dla aniołów.',
'Angel? You look more like a superhero.':'Anioł? Bardziej wyglądasz na superbohaterkę.',
'Girls… I need you to stay strong.':'Dziewczyny… Musicie być dzielne.',
'What’s wrong?':'Co się stało?',
'Judy is missing and Melissa is being held captive in the mansion.':'Judy zaginęła, a Melissa jest więziona w rezydencji.',
'No! You need to save them!':'Nie! Musicie je uratować!',
'I assure you… We will succeed.':'Zapewniam was… Uda nam się.',
'I’ve got to run. But we’ll be back soon.':'Muszę już lecieć. Wkrótce wrócimy.',
'Be careful, 1Hero.':'Uważaj na siebie, 1Hero.',
'Can I come with you?':'Mogę iść z wami?',
'Not now.':'Nie teraz.',
'Give him some space, Hannah.':'Daj mu trochę przestrzeni, Hannah.',
},
65:{
'What are you doing here?':'Co tu robisz?',
'I’m here to pick something up.':'Przyszedłem coś odebrać.',
'Why don’t you spend the night, I’m headed over to the mansion.':'Zostań na noc. Jadę do rezydencji.',
'What!? You’re supposed to stay here.':'Co!? Miałeś tu zostać.',
'I’d send another unit, but it’s Friday night.':'Wysłałabym inny patrol, ale jest piątkowy wieczór.',
'What’s going on at the mansion?':'Co się dzieje w rezydencji?',
'Someone was spotted snooping around… I’m not taking any chances. I need to get over there.':'Ktoś kręcił się tam podejrzanie… Nie będę ryzykować. Muszę tam jechać.',
'Stay here and make sure no one comes into the church. I’ll go to the mansion.':'Zostań tu i pilnuj, żeby nikt nie wszedł do kościoła. Ja pojadę do rezydencji.',
'Looking to score some points with the Wilkes girl?':'Chcesz zapunktować u panny Wilkes?',
'I’m doing you a favor.':'Wyświadczam ci przysługę.',
'I should be home right now.':'Powinienem być teraz w domu.',
'Ugh. Stop complaining.':'Ech. Przestań narzekać.',
'Don’t wait around. Get over there and check it out.':'Nie ociągaj się. Jedź tam i sprawdź sytuację.',
},
37:{
'For a place so big, it sure is short on fun stuff to do.':'Jak na tak duże miejsce, jest tu zaskakująco mało rozrywek.',
'Did you run over here in the rain!?':'Przybiegłaś tu w deszczu!?',
'Father told me what he saw. You are brave to venture into those woods at night.':'Ojciec opowiedział mi, co widział. Trzeba odwagi, żeby zapuszczać się nocą do tych lasów.',
'Why don’t you go to the woods?':'Może pójdziesz do lasu?',
'It’s not too bad out there.':'Nie jest tam aż tak źle.',
'I’ll keep you safe, Sister Judy.':'Będę cię chronić, siostro Judy.',
'Sister Judy doesn’t like the woods.':'Siostra Judy nie lubi lasu.',
'I ain’t walking home. Where is Ma?':'Nie będę wracać pieszo. Gdzie jest mama?',
'My hero.':'Mój bohater.',
},
49:{
'Father Solomon, I presume.':'Ojciec Solomon, jak mniemam.',
'Father, this is Detective Bhatt.':'Ojcze, to detektyw Bhatt.',
'Is there something wrong?':'Czy coś się stało?',
'We have some information on Madalyn Rose, the woman who was reported seen near your church.':'Mamy nowe informacje o Madalyn Rose, kobiecie widzianej w pobliżu pańskiego kościoła.',
'She may have been scouting this area for quite some time.':'Możliwe, że od dłuższego czasu obserwowała tę okolicę.',
'What do you mean?':'Co ma pani na myśli?',
'DNA from a hair sample was retrieved from the body of Father Zephaniah…':'Z ciała ojca Zephaniaha pobrano próbkę włosa do badania DNA…',
'It matches Madalyn’s DNA.':'Wynik pasuje do DNA Madalyn.',
'Do you think he was murdered?':'Myśli pani, że został zamordowany?',
'The cause of death was listed as a heart attack, but with this new information, we’d like to locate his belongings.':'Jako przyczynę śmierci podano zawał serca, ale w świetle nowych informacji chcielibyśmy odnaleźć jego rzeczy.',
'The police took everything. There’s not really anything left.':'Policja zabrała wszystko. Nic już tu nie zostało.',
'Zephaniah took heart meds, and we don’t have them.':'Zephaniah brał leki na serce, a nie mamy ich.',
'We suspect that they were never found and might still be hidden somewhere out of sight.':'Podejrzewamy, że ich nie znaleziono i nadal mogą być gdzieś ukryte.',
'I can show you my bedroom. It was the place where Father Zephaniah’s belongings were kept.':'Mogę pokazać wam swoją sypialnię. Tam trzymano rzeczy ojca Zephaniaha.',
'If you don’t mind.':'Jeśli nie ma ojciec nic przeciwko.',
},
20:{
'I need to leave this city... But not now.':'Muszę opuścić to miasto… Ale nie teraz.',
'Sister Judy, have you seen Chloe?':'Siostro Judy, widziałaś Chloe?',
'Oh, yes. She is praying in the chapel. She looked distraught.':'Tak. Modli się w kaplicy. Wyglądała na przygnębioną.',
'That might be my fault.':'To może być moja wina.',
'What happened?':'Co się stało?',
'Oh, uhh. I just put her in an awkward situation.':'Och, eee… Po prostu postawiłem ją w niezręcznej sytuacji.',
'I’d love to talk to her.':'Chętnie z nią porozmawiam.',
'Sure thing.':'Jasne.',
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
