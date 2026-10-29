import json
from pathlib import Path
ROOT=Path('games/the-genesis-order/translation')
CANON=ROOT/'export-v1/custom_dialogue.jsonl'
OUT=ROOT/'drafts/custom-dialogue-npc-system-01.jsonl'
if OUT.exists(): raise SystemExit(f'Refusing to overwrite {OUT}')
DATA=r'''Do you believe in the sex virus? I think it’s fake.	Wierzysz w wirusa seksu? Moim zdaniem to bzdura.
Do you believe in the sex virus? I think it might be real.	Wierzysz w wirusa seksu? Może naprawdę istnieje.
Do you believe in the sex virus? I keep hearing about people getting caught having sex in public.	Wierzysz w wirusa seksu? Ciągle słyszę o ludziach przyłapanych na seksie w miejscach publicznych.
I think I might have the sex virus. Better get away from me.	Chyba mam wirusa seksu. Lepiej trzymaj się ode mnie z daleka.
I think I might have the sex virus. I’ve been having a lot of strong sexual urges lately.	Chyba mam wirusa seksu. Ostatnio mam bardzo silny popęd seksualny.
I think I might have the sex virus. I can’t stop thinking about sex.	Chyba mam wirusa seksu. Nie mogę przestać myśleć o seksie.
You look like you have the sex virus. Stay away from me.	Wyglądasz, jakbyś miał wirusa seksu. Trzymaj się ode mnie z daleka.
You look like you have the sex virus. How does it feel to want sex all the time?	Wyglądasz, jakbyś miał wirusa seksu. Jak to jest ciągle mieć ochotę na seks?
You look like you have the sex virus. Wanna have a go?	Wyglądasz, jakbyś miał wirusa seksu. Chcesz spróbować?
I heard about a sex virus on the news. Sounds scary.	W wiadomościach mówili o wirusie seksu. Brzmi przerażająco.
I heard about a sex virus on the news. Sounds interesting.	W wiadomościach mówili o wirusie seksu. Brzmi ciekawie.
I heard about a sex virus on the news. Sounds kinky.	W wiadomościach mówili o wirusie seksu. Brzmi pikantnie.
What’s all this talk about a sex virus? Is that a real thing?	O co tyle gadania o wirusie seksu? To naprawdę istnieje?
What’s all this talk about a sex virus? Have you noticed anything different about the people around you?	O co tyle gadania o wirusie seksu? Zauważyłeś coś innego u ludzi wokół siebie?
What’s all this talk about a sex virus? Isn’t it normal to just want to fuck all the time?	O co tyle gadania o wirusie seksu? Czy to nie normalne, że człowiek ciągle ma ochotę na seks?
Today is payday! I’ve got to get home and see if I have money in the mail.	Dziś wypłata! Muszę wrócić do domu i sprawdzić, czy w skrzynce czekają pieniądze.
I ran out of money. I think I have some more in my home mailbox.	Skończyły mi się pieniądze. Chyba mam jeszcze trochę w domowej skrzynce pocztowej.
Sometimes I find things on the ground. But with my bad vision,  I have to be really close to see them.	Czasem znajduję rzeczy na ziemi. Mam kiepski wzrok, więc muszę podejść naprawdę blisko, żeby je zobaczyć.
Some say there are cool artifacts to be found in the woods.	Mówią, że w lesie można znaleźć fajne artefakty.
The ground can be hard this time of year.	O tej porze roku ziemia bywa twarda.
You can buy sexy photos at the grocery store! What a great world we live in!	W sklepie spożywczym kupisz seksowne zdjęcia! Ależ wspaniały świat!
If I wasn’t so embarrassed, I’d shop at the porn store. I hear Lisa Stonewell has some new content.	Gdybym się tak nie wstydził, poszedłbym do sklepu porno. Słyszałem, że Lisa Stonewell ma coś nowego.
Some guy offered me a key to find his lost stuff. He looked fancy.	Jakiś facet zaoferował mi klucz, żebym odnalazł jego zgubione rzeczy. Wyglądał na eleganta.
I saw someone taking out the trash over by the apartments. What the hell was he doing?	Widziałem kogoś wynoszącego śmieci przy apartamentowcu. Co on, do cholery, wyprawiał?
I saw a guy going to the store who had a hole in his pocket.	Widziałem faceta idącego do sklepu z dziurą w kieszeni.
Sometimes I see treasure chests laying around. If you find a key, you can open it!	Czasem widuję porzucone skrzynie ze skarbami. Jeśli znajdziesz klucz, możesz je otworzyć!
They sell some sexy stuff at Publics.	W Publics sprzedają różne seksowne rzeczy.
I invited my friends over to my house, but it was too ugly for them to stay.	Moi znajomi wpadli do mnie, ale dom był tak brzydki, że nie chcieli zostać.
I like to use my cell phone to call people. Have you done that?	Lubię dzwonić do ludzi z komórki. Też tak robisz?
I hate public shows of affection. Have you been to the skyscraper lately?	Nie znoszę publicznego okazywania uczuć. Byłeś ostatnio w wieżowcu?
There was a very angry guy at Dick's.	Przy Dick’s kręcił się jakiś wściekły facet.
The smarter you are, the more money you can make.	Im mądrzejszy jesteś, tym więcej możesz zarobić.
Sometimes I have access to a new area. It shows up on my map as a green block.	Czasem odblokowuję nowy obszar. Na mapie pojawia się jako zielone pole.
There’s a phone in the locker room that won't stop ringing.	W szatni dzwoni telefon, który nie chce przestać.
When I find something valuable, I bury it under a tree. But only closeby where I live.	Kiedy znajduję coś cennego, zakopuję to pod drzewem. Tylko gdzieś niedaleko domu.
I found a rusty toy in the shade of a tree on the ground. Rusty objects are hard to see sometimes.	Trafiła mi się zardzewiała zabawka na ziemi, w cieniu drzewa. Zardzewiałe przedmioty czasem trudno zauważyć.
I saw some nasty stuff at the XXX shop. I love it!	Widziałem obrzydlistwa w sklepie XXX. Uwielbiam to!
I saw a treasure chest on top of a fire escape. I wonder what’s inside.	Na górze schodów przeciwpożarowych widziałem skrzynię ze skarbem. Ciekawe, co jest w środku.
I got so mad, I threw some money on top of a soda machine.	Tak się wściekłem, że rzuciłem trochę pieniędzy na automat z napojami.
It’s common courtesy to call your new friends.	Nowych znajomych wypada czasem do siebie zadzwonić.
If you want to make a woman happy, buy her an outfit.	Chcesz uszczęśliwić kobietę? Kup jej strój.
I saw a fast moving cat near the porn shop. I wonder if it’s lost.	Widziałem szybko biegnącego kota koło sklepu porno. Ciekawe, czy się zgubił.
There’s a man near the condos that was worried about his cat.	Przy apartamentowcach był facet, który martwił się o swojego kota.
I dropped a key in the church yard. Without a metal detector, it’ll be impossible to find.	Klucz wylądował na terenie kościoła. Bez wykrywacza metalu nie da się go znaleźć.
If you want an easy win, take the metal detector to the church yard. Trust me.	Chcesz łatwej wygranej? Zabierz wykrywacz metalu na teren kościoła. Zaufaj mi.
Nothing is creepier than a chest in an attic. Who knows what could be inside?	Nic nie jest straszniejsze niż skrzynia na strychu. Kto wie, co może być w środku?
I had a pet snake that I fed caterpillars. But I got rid of it… Snakes belong on a farm.	Miałem węża i karmiłem go gąsienicami. Ale już go nie mam… Węże powinny mieszkać na farmie.
There’s a lady at Dick’s that tried to get me to take her locker key. Sounds like a scam to me.	Jakaś kobieta przy Dick’s próbowała wcisnąć mi klucz do szafki. Śmierdzi mi to przekrętem.
There’s a locker in the gym that hasn’t been open in a long time. I wonder what’s inside.	W siłowni od dawna nie otwierano jednej szafki. Ciekawe, co jest w środku.
If you know the city, you can test your knowledge at the police station.	Jeśli znasz miasto, możesz sprawdzić swoją wiedzę na komisariacie.
Legend has it that there’s a treasure chest next to a waterfall.	Podobno obok wodospadu jest skrzynia ze skarbem.
I better make sure my place looks nice before I start having people over.	Lepiej posprzątać i urządzić mieszkanie, zanim zacznę zapraszać gości.
You should never leave food at the dinner table. At least feed it to the animals.	Nie zostawiaj jedzenia na stole. Rzuć je chociaż zwierzętom.
I used to find lockpicks in the grass and use them to open chests. But not anymore.	Kiedyś znajdowałem wytrychy w trawie i otwierałem nimi skrzynie. Ale już nie.
There are rats near the grocery store! They don’t even sell cheese there.	Przy sklepie spożywczym są szczury! A przecież nie sprzedają tam nawet sera.
When a key falls from the sky, I always pick it up.	Zawsze podnoszę klucz, który spada z nieba.
Have you ever seen a bush that looks out of place? You should chop them down!	Widziałeś krzak, który nie pasował do otoczenia? Trzeba takie wycinać!
Crucifixes and churches go together like peanut butter and chocolate.	Krucyfiksy i kościoły pasują do siebie jak masło orzechowe i czekolada.
Don’t you hate people who protest in front of naughty places?	Nie denerwują cię ludzie protestujący przed nieprzyzwoitymi miejscami?
If I ever can’t turn a valve, a little grease loosens it up.	Jeśli nie mogę odkręcić zaworu, trochę smaru rozwiązuje problem.
Legend has it a magical basketball appears in the women’s shower room.	Podobno w damskiej szatni pod prysznicem pojawia się magiczna piłka do koszykówki.
If you ever want to play basketball, step one is to grab the ball.	Jeśli chcesz zagrać w koszykówkę, najpierw znajdź piłkę.
Have you ever used a ball to knock something off of high places?	Używałeś kiedyś piłki, żeby strącić coś z wysokości?
Is it true that there are treasure chests in the caves around here?	Naprawdę są tu w jaskiniach skrzynie ze skarbami?
Have you ever seen a creepy gargoyle? I heard they live in caves.	Widziałeś kiedyś upiorną gargulę? Słyszałem, że żyją w jaskiniach.
Rich people have the best shovels. I wish I could search a rich person’s house for a nice shovel.	Bogaci mają najlepsze łopaty. Chciałbym przeszukać dom jakiegoś bogacza i znaleźć porządną łopatę.
If you see a vase, smash it! You never know what’s inside.	Jeśli widzisz wazon, rozbij go! Nigdy nie wiadomo, co jest w środku.
You look nicely dressed. I should go shopping at Publics for a nice sexy outfit.	Świetnie wyglądasz. Też muszę skoczyć do Publics po seksowny strój.
Don’t forget to call your friends. Life is more fun when you spend time with loved ones.	Nie zapominaj dzwonić do znajomych. Życie jest fajniejsze, gdy spędza się czas z bliskimi.
I found out they sell sexy photos of people at Publics. How is that possible?	Odkryłem, że w Publics sprzedają seksowne zdjęcia ludzi. Jak to możliwe?
There’s an old saying that a recipe can be found near a ticking clock.	Podobno przepis można znaleźć w pobliżu tykającego zegara.
I have a lot of old books in my office. Maybe I should donate more of them to the church.	W moim biurze leży mnóstwo starych książek. Może warto oddać część do kościoła.
In the old days, people kept books in their office. Now, everything is digital.	Kiedyś trzymano książki w biurach. Teraz wszystko jest cyfrowe.
I stopped going to church because they wanted bigger offerings. I guess big offerings give big rewards.	Nie chodzę już do kościoła, bo chcieli coraz większych datków. Chyba duże datki przynoszą większe nagrody.
Sometimes there are places that produce better treasures than other places.	Niektóre miejsca obfitują w lepsze skarby niż inne.
How do you farm aloe plants? It’s a good cure for sunburn.	Jak uprawiać aloes? Dobrze pomaga na oparzenia słoneczne.
Is it true there are treasure chests in the forest?	Naprawdę są w lesie skrzynie ze skarbami?
If you want to piss off rich people, break their yard vases!	Chcesz wkurzyć bogaczy? Rozbij im wazony w ogrodzie!
Dumbbells can be found in gyms. But also strong girls buy them for their houses.	Hantle znajdziesz na siłowni. Ale silne dziewczyny kupują je też do domu.
Metal vases can be broken if you’re strong enough. I sold a metal vase to the police force long ago.	Metalowy wazon da się rozbić, jeśli jesteś dość silny. Dawno temu sprzedałem taki policji.
Safes can hold valuable stuff. But sometimes they just hold random metal junk.	W sejfach można trzymać cenne rzeczy. Ale czasem trafia się w nich tylko jakiś metalowy złom.
I saw someone at the police station whose pants kept falling down.	Na komisariacie widziałem faceta, któremu ciągle zsuwały się spodnie.
I saw a treasure chest next to a fancy home. I wonder what’s inside.	Obok eleganckiego domu stała skrzynia ze skarbem. Ciekawe, co jest w środku.
I got so mad I tossed a key on top of the church roof. You’d need to climb pretty high to reach it.	Tak się wściekłem, że rzuciłem klucz na dach kościoła. Trzeba się nieźle wspiąć, żeby go dosięgnąć.
I keep having these dreams about a corn field and a hidden treasure, high on a cliff.	Ciągle śni mi się pole kukurydzy i ukryty skarb wysoko na klifie.
Rock climbing near a waterfall is dangerous, but rewarding.	Wspinaczka przy wodospadzie jest niebezpieczna, ale się opłaca.
There are good rock climbing walls in the forest.	W lesie są świetne ścianki wspinaczkowe.
Climbing cave walls is fun, but be careful.	Wspinaczka po ścianach jaskiń jest fajna, ale uważaj.
I bet there are interesting things in that mansion to the west.	Ciekawe, co kryje ta rezydencja na zachodzie.
I’m buying some fancy things to impress my new girlfriend.	Kupuję eleganckie rzeczy, żeby zaimponować nowej dziewczynie.
Every time I flush a key down the toilet I write a note and put it on the 2nd floor.	Za każdym razem, gdy spuszczam klucz w toalecie, zapisuję notatkę i zostawiam ją na drugim piętrze.
The key to plumbing fixes is to find a way behind the walls.	Żeby naprawić hydraulikę, trzeba znaleźć drogę za ścianę.
You don’t have to go to the XXX shop to get sexy photos. Publics has them too!	Nie musisz iść do sklepu XXX po seksowne zdjęcia. W Publics też je mają!
I left an old book on the second story of the church. Maybe I’ll pick it up next Sunday.	Zostawiłem starą książkę na drugim piętrze kościoła. Może odbiorę ją w następną niedzielę.
Someone came into my home and broke all my vases! What was he searching for?	Ktoś wszedł do mojego domu i potłukł wszystkie wazony! Czego szukał?
I found a metal ring and tossed it up high after. You’ll find some odd things near the apartments.	Znalazłem metalową obrączkę i potem rzuciłem ją wysoko. Dziwne rzeczy można znaleźć przy apartamentowcach.
A little bit of glue goes a long way in joining two halves.	Nawet odrobina kleju wystarczy, by połączyć dwie połówki.
There’s drama happening at Channel 4. I hear the receptionist is getting fired.	W Channel 4 dzieje się niezła drama. Podobno zwolnią recepcjonistkę.
There’s an old saying that the dirtiest books can be found in a farm woman’s bedroom.	Podobno najbrudniejsze książki można znaleźć w sypialni wiejskiej gospodyni.
I saw a treasure chest on the other side of a river once. It was hard to see through the leaves.	Kiedyś widziałem skrzynię ze skarbem po drugiej stronie rzeki. Trudno było ją wypatrzyć przez liście.
There are so many leaks around town that can be fixed with a wrench. It’s not wise to waste water.	W mieście jest mnóstwo przecieków, które można naprawić kluczem. Nie warto marnować wody.
Every time I see a storage chest inside someone’s house, I open it. Am I a bad person?	Za każdym razem, gdy widzę skrzynię w czyimś domu, otwieram ją. Czy jestem złym człowiekiem?
The police station is a pretty old building. I hear there are cracks in the interior walls.	Komisariat to dość stary budynek. Podobno w ścianach są pęknięcia.
Climbing marble surfaces is hard unless you have grippy shoes.	Wspinanie się po marmurze jest trudne, jeśli nie masz butów z dobrą przyczepnością.
The police station has the most beautiful marble columns.	Na komisariacie są najpiękniejsze marmurowe kolumny.
Every time I go cave spelunking I look for treasure chests.	Za każdym razem, gdy eksploruję jaskinię, szukam skrzyń ze skarbami.
Are there buried treasures in the caves here?	Czy w tutejszych jaskiniach są zakopane skarby?
Thieves don’t break into rich people’s houses cause it’s too hard to pick their safe locks… or so I hear.	Podobno złodzieje nie włamują się do domów bogaczy, bo trudno otworzyć ich sejfy.
It can get cold at night. I hope no one has to suffer through the cold.	Nocą robi się zimno. Oby nikt nie musiał marznąć.
Metal doesn’t burn. If you’re looking for something metal in a barrel of wood, burning the wood will reveal the metal.	Metal się nie pali. Jeśli szukasz czegoś metalowego w beczce z drewnem, spal drewno, a znajdziesz metal.
The creepiest books are found in basements.	Najstraszniejsze książki leżą w piwnicach.
I wonder what kind of books rich people read.	Ciekawe, jakie książki czytają bogacze.
If you have the chance, take everything you can from a mansion.	Jeśli masz okazję, zabierz z rezydencji wszystko, co się da.
You’d be shocked at what you could find in an unplowed field. The secret is to find a way into the dense foliage.	Nie uwierzysz, co można znaleźć na niezaoranym polu. Trzeba tylko przedrzeć się przez gęste zarośla.
I saw a hobo hanging over by the dock.	Widziałem bezdomnego kręcącego się przy przystani.
I found something naughty in my kitchen. What is it with always finding naughty things in kitchens?	Znalazłem coś niegrzecznego w kuchni. Czemu ciągle trafiam na takie rzeczy w kuchniach?
There’s nothing better than buying porn the old fashioned way.	Nie ma to jak kupić porno tak jak za dawnych lat.
I learned so much more about my best friend in the shadow of a windmill.	W cieniu wiatraka dowiedziałem się o najlepszym przyjacielu znacznie więcej.
Sometimes I wonder if someone places treasures in the cave on purpose to bring in tourists.	Czasem się zastanawiam, czy ktoś celowo ukrywa skarby w jaskiniach, żeby przyciągnąć turystów.
Even fancy people have shitty lockboxes.	Nawet bogacze mają kiepskie kasetki na pieniądze.
I saw some old looking treasures near the warehouse.	Widziałem jakieś stare skarby przy magazynie.
You haven’t bought a treasure detector yet? It’s totally worth the money.	Jeszcze nie kupiłeś wykrywacza skarbów? Naprawdę warto.
Whenever I need to find something, I always follow the fish. I find a lot of stuff in the water.	Kiedy czegoś szukam, zawsze idę za rybami. W wodzie znajduję mnóstwo rzeczy.
If you’re going cave diving, be sure you’re prepared and you don’t drown. A good pair of shoes is a must.	Jeśli wybierasz się na nurkowanie w jaskini, przygotuj się i uważaj, żeby się nie utopić. Dobre buty to podstawa.
If you want to see your friends nude, there’s something you should buy at the store.	Jeśli chcesz zobaczyć znajomych nago, jest coś, co możesz kupić w sklepie.
There is so much history in old farm houses. You just have to know where to look.	W starych domach wiejskich kryje się mnóstwo historii. Trzeba tylko wiedzieć, gdzie szukać.
If I wanted to break into something in a secret room, I'd bring a hacksaw.	Do włamania do czegoś w tajnym pomieszczeniu przydałaby się piła do metalu.
If you want to see your friends nude, check the store from time to time. You never know what might go on sale.	Jeśli chcesz zobaczyć znajomych nago, zaglądaj od czasu do czasu do sklepu. Nigdy nie wiesz, co trafi na wyprzedaż.
I left my safe outside and it got so rusty I couldn’t open it… Same with my car. It’s not wise to leave metal stuff outside. It’ll rust.	Sejf zostawiony na dworze tak zardzewiał, że nie dało się go otworzyć… Z samochodem było tak samo. Metalowych rzeczy nie warto trzymać na zewnątrz, bo zardzewieją.
I put my catnip in my food pantry. Cats are just like people!	Trzymam kocimiętkę w spiżarni. Koty są jak ludzie!
How do they open the manholes around the city? It’s something I always wondered.	Jak otwiera się miejskie włazy? Zawsze mnie to zastanawiało.
Why do people write down their lock codes? That’s not very secure!	Po co ludzie zapisują kody do zamków? To niezbyt bezpieczne!
I misplaced my secret code, but then I remembered that I wrote it above the mirror.	Zgubiłem tajny kod, ale potem przypomniałem sobie, że zapisałem go nad lustrem.
Why do spooky places always have numbers written on the walls?	Czemu w upiornych miejscach zawsze są liczby napisane na ścianach?
If you’re storing food for a long time, be sure to check the code written on the package.	Jeśli przechowujesz jedzenie przez dłuższy czas, sprawdź kod na opakowaniu.
Avoid demonic numbers if you value your soul.	Nie zadzieraj z demonicznymi liczbami, jeśli cenisz sobie duszę.
There's nothing like finishing a good meal and then hiding stuff in the wall.	Nie ma to jak zjeść dobry posiłek, a potem schować coś w ścianie.
I’m a pervert! I want to rummage around a pretty ladies changing room!	Jestem zboczeńcem! Chcę pogrzebać w przebieralni pięknych kobiet!
Do they still sell sexy clothes at the grocery store?	Czy w sklepie spożywczym nadal sprzedają seksowne ciuchy?
I’d crawl through walls and into spooky places to learn how to please a woman with my mouth.	Przeczołgałbym się przez ściany i do upiornych miejsc, żeby nauczyć się zadowalać kobietę ustami.
At the end of the hallway is where I learned everything about the person I love.	Na końcu korytarza dowiedziałem się wszystkiego o ukochanej osobie.
I left a safe in the woods. I bet it’s all rusted by now.	Zostawiłem sejf w lesie. Pewnie już cały zardzewiał.
You shouldn’t leave dangerous chemicals outside in bins. Even if they are far from your house.	Nie zostawiaj niebezpiecznych chemikaliów na zewnątrz, nawet jeśli są daleko od domu.
You’d think big boulders would be worthless, but people pay a lot of money to have them in their yards.	Wydaje się, że wielkie głazy są bezużyteczne, ale ludzie płacą kupę kasy, żeby mieć je w ogródku.
If I were looking for treasure, I’d look under the thickest weeds I could find.	Gdybym szukał skarbów, zajrzałbym pod najgęstsze chwasty, jakie znajdę.
The naughtiest thing I ever learned how to do I learned next to a pond.	Najbardziej niegrzecznej rzeczy nauczyłem się nad stawem.
Young suburban ladies always hide their diaries in the strangest places. But always in their bedrooms.	Młode kobiety z przedmieść chowają pamiętniki w najdziwniejszych miejscach. Ale zawsze w sypialni.
Rats love cheese.	Szczury uwielbiają ser.
I saw a feral cat near the woods, behind thick weeds. I bet it would hate to eat human food.	Widziałem zdziczałego kota koło lasu, za gęstymi krzakami. Założę się, że nie tknąłby ludzkiego jedzenia.
If you have the opportunity, you should play a piano! The perfect note for every song starts with middle C.	Jeśli masz okazję, zagraj na pianinie! Idealny dźwięk do każdej piosenki zaczyna się od środkowego C.
If you see a weed, kill it! You never know what you might find.	Jeśli widzisz chwast, wyrwij go! Nigdy nie wiadomo, co znajdziesz.
Turning over stones in the woods is a good way to get a bug bite!... Or find something.	Przewracanie kamieni w lesie to dobry sposób, żeby złapać robaka!... Albo coś znaleźć.
It’s a pain in the ass to ship dumbbells.	Wysyłanie hantli to niezły ból w tyłku.
There’s an old wives’ tale that says treasure can be found by following roaches… I think I saw that in a video game once.	Jest takie stare porzekadło, że karaluchy prowadzą do skarbu… Chyba widziałem to kiedyś w grze.
I need to impress my boss… I should decorate my home to look nicer.	Muszę zaimponować szefowi… Przydałoby się ładniej urządzić dom.
I saw a belly dancer outfit at Publics! I wish I could afford it.	W Publics widziałem strój tancerki brzucha! Szkoda, że mnie na niego nie stać.
Have you seen that mansion on the hill? I bet there are cool treasures under it.	Widziałeś tę rezydencję na wzgórzu? Na pewno są pod nią fajne skarby.
There’s a creepy metal box near the skyrise!	Koło wieżowca stoi upiorna metalowa skrzynia!
I saw a very strange metal box near the strip center.	Przy pasażu handlowym widziałem bardzo dziwną metalową skrzynię.
I saw an orange glow right in the dead center of the church. I wonder what it was.	Zobaczyłem pomarańczową poświatę w samym środku kościoła. Ciekawe, co to było.
Right before I ate dinner out, I threw an old key high into the air. It never came back down.	Tuż przed wyjściem na kolację wyrzuciłem stary klucz wysoko w powietrze. Nigdy nie spadł.
I can throw a book really far! As long as I throw it from a high-up window, to the north… It might land in a tree, though.	Potrafię rzucić książką bardzo daleko! Wystarczy wyrzucić ją z wysokiego okna na północ… Tylko może wylądować na drzewie.
Don’t miss out on good sales at Publics!	Nie przegap dobrych wyprzedaży w Publics!
If you want to impress your boss, you better make sure your house is nice.	Chcesz zaimponować szefowi? Zadbaj o porządek w domu.
I learned how to do some naughty things over a nice dinner at someone’s home.	Podczas miłej kolacji u kogoś nauczyłem się kilku niegrzecznych rzeczy.
It’s crazy how rough the water currents get underground.	Pod ziemią prądy wodne potrafią być naprawdę silne.
You know rich people are hiding stuff in their homes. Lots of switches and buttons that lead to secrets.	Bogacze ukrywają różne rzeczy w swoich domach. Pełno tam przełączników i przycisków prowadzących do sekretów.
Cops use orange cones to keep people away from things. But they can’t keep out a good hacker!	Gliniarze stawiają pomarańczowe pachołki, żeby odgrodzić jakieś miejsce. Ale dobrego hakera nic nie powstrzyma!
I wonder if there are any sexy gifts at the store. I don’t like going into the porn shop.	Ciekawe, czy w sklepie są jakieś seksowne prezenty. Nie lubię chodzić do sklepu porno.
If you’re going to climb a cliff, you better be prepared to battle aggressive birds.	Jeśli zamierzasz wspinać się na klif, przygotuj się na walkę z agresywnymi ptakami.
I almost got crushed once… I had some wild fun that night.	Prawie mnie zmiażdżyło… Ale tej nocy było naprawdę ostro.
I got bear mace for my birthday, but the only predators around here are coyotes.	Na urodziny dostałem gaz pieprzowy na niedźwiedzie, ale jedynymi drapieżnikami w okolicy są kojoty.
Why would you need to lock away garden tools? You’d have to be a rich, out-of-touch buffoon to do that!	Po co zamykać narzędzia ogrodowe? Trzeba być bogatym, oderwanym od rzeczywistości bufonem!
Sneaking around at night and breaking jars near mansions can get you some nice loot.	Wkradanie się nocą i rozbijanie słoików przy rezydencjach może przynieść niezły łup.
I saw a weird shaft stored away at the church. I shouldn't snoop around.	W kościele widziałem dziwny metalowy pręt schowany na zapleczu. Lepiej się nie wtrącać.
The nice house by the police station has a metal jar behind a tree. Why would you hide such a nice ornament?	W ładnym domu przy komisariacie, za drzewem, stoi metalowy wazon. Po co ktoś chował taką ozdobę?
When life gives you tool pieces, make tools! That’s what my dad always said.	Jak życie daje ci części do narzędzi, zrób z nich narzędzia! Tak zawsze mówił mój tata.
I hear there are car thieves near the apartments. Better have some self-defense ready if you go there.	Podobno przy apartamentowcach grasują złodzieje samochodów. Lepiej mieć czym się bronić, jeśli tam pójdziesz.
Those people in the fancy condos leave their Christmas lights up all year!	Mieszkańcy tych eleganckich apartamentów zostawiają świąteczne lampki przez cały rok!
Can you see naked people at the store? What kind of world are we living in!?	W sklepie można oglądać nagich ludzi? Co za czasy!?
Have you ever had sex near a creek? I learned how to do butt-stuff there!	Uprawiałeś kiedyś seks nad strumieniem? To tam nauczyłem się zabaw analnych!
People drop stuff on the sidewalks and just leave them there. Litterbugs!	Ludzie rzucają rzeczy na chodnik i zostawiają je tam. Śmieciarze!
I lost my notepad inside of the Channel 4 office building.	Zgubiłem notatnik w budynku Channel 4.
I used to do audio mixing. I wish I could work for Kimberly Foxx. I want to get to know her better… if you know what I mean.	Kiedyś zajmowałem się miksowaniem dźwięku. Chciałbym pracować dla Kimberly Foxx. Chętnie bym ją lepiej poznał… jeśli wiesz, o co mi chodzi.
You know all the stuff interrogators write down is also recorded. What a waste of time.	Wszystko, co zapisują przesłuchujący, jest też nagrywane. Co za strata czasu.
All the best stuff at the library is locked away.	W bibliotece wszystkie najlepsze rzeczy są zamknięte na klucz.
If you have money, spend it! That’s how I live my life.	Masz pieniądze? Wydawaj je! Tak właśnie żyję.
I left an important key deep in my basement. Such a pain in the ass to walk all the way down there and back.	Zostawiłem ważny klucz głęboko w piwnicy. Okropnie męczące, tyle razy tam schodzić i wracać.
Warehouses are such big places. I’m surprised more stuff doesn’t get lost there.	Magazyny są ogromne. Dziwię się, że nie ginie tam więcej rzeczy.
I love going shopping!	Uwielbiam zakupy!
Ever see something naughty in a room full of books?	Widziałeś kiedyś coś niegrzecznego w pokoju pełnym książek?
Just when you think you’ve put everything in the right place, someone comes along and scatters stuff all around the house.	Gdy już wszystko ułożysz na swoim miejscu, zawsze znajdzie się ktoś, kto porozrzuca rzeczy po całym domu.
I will never go into another cave after seeing a spider as big as a bowling ball.	Po tym, jak trafił mi się pająk wielki jak kula do kręgli, nie wejdę już do żadnej jaskini.
I never buy my girlfriend the right outfit. I should just break up with her.	Nigdy nie kupuję dziewczynie odpowiednich ubrań. Chyba powinienem z nią zerwać.
I love shopping! Do you?	Uwielbiam zakupy! A ty?
If you need to impress a lady, buy more stuff!	Chcesz zaimponować kobiecie? Kup jej więcej rzeczy!
Nothing puts me in the mood like alligator spotting.	Nic nie nastraja mnie tak jak wypatrywanie aligatorów.
Never shoot at electrical outlets. You could cause a fire.	Nigdy nie strzelaj do gniazdek elektrycznych. Możesz wywołać pożar.
I learned so much about my girlfriend after I fucked her in my personal library room.	Wiele się dowiedziałem o dziewczynie po tym, jak przeleciałem ją w swoim prywatnym pokoju bibliotecznym.
Valuable knowledge is oftentimes guarded by men with guns.	Cennej wiedzy często strzegą uzbrojeni mężczyźni.
I can never do enough shopping.	Nigdy dość zakupów.
Is it illegal for a homeless person to wear a cop uniform to stay warm?	Czy bezdomny może założyć policyjny mundur, żeby się ogrzać? To nielegalne?
Would you dress in a sexy woman’s outfit if that’s all you had to wear? I guess a homeless man might.	Założyłbyś seksowny damski strój, gdyby to było jedyne, co masz do ubrania? Pewnie bezdomny by założył.
I was sitting down near the lobby of the skyrise and I saw something on the other side of the room. What was it?	Siedziałem niedaleko holu wieżowca i zobaczyłem coś po drugiej stronie. Co to mogło być?
Don’t forget to spend money. You don’t want to die rich.	Nie zapomnij wydawać pieniędzy. Nie chcesz umrzeć bogaty.
Do they teach butt-stuff at the church? Or are they completely anti-sex?	Czy w kościele uczą zabaw analnych? A może są całkowicie przeciwni seksowi?
Private people hide dark secrets in dark places. I put all my dark secrets in my bomb shelter.	Skryci ludzie chowają mroczne sekrety w mrocznych miejscach. Ja trzymam wszystkie swoje w schronie.
There’s a woman who looks distressed near the apartments. I wonder what her deal is.	Przy apartamentowcach jest jakaś zmartwiona kobieta. Ciekawe, co się z nią dzieje.
I buried something in my backyard, but no one will find it without some serious CSI tools.	Zakopałem coś na podwórku, ale nikt tego nie znajdzie bez porządnego sprzętu CSI.
I put a lot of junk in my storm shelter… including naughty stuff I don’t want my kids to see.	Do schronu przeciwburzowego wrzuciłem mnóstwo gratów… w tym niegrzeczne rzeczy, których nie chcę pokazywać dzieciom.
I got a new job at a factory. It’s like a confusing maze! They have to put arrows on the floor for employees to follow.	Dostałem nową pracę w fabryce. To istny labirynt! Na podłodze musieli namalować strzałki, żeby pracownicy wiedzieli, którędy iść.
Have you ever watched the sunlight fade away only to see a new star fill the night sky? You’ll never see such a sight in a basement.	Widziałeś kiedyś, jak zachodzi słońce, a na nocnym niebie pojawia się nowa gwiazda? W piwnicy nie zobaczysz takiego widoku.
Don't be cheap! Spend money now or die rich.	Nie bądź skąpy! Wydawaj pieniądze teraz, zamiast umrzeć bogatym.
I blocked a hole in the wall with a cone, but that didn't stop someone from entering it.	Zatkałem dziurę w ścianie stożkiem, ale i tak ktoś przez nią wszedł.
I dropped a piece of metal on the floor in a messy room. I almost needed a metal detector to find it, but alas I stepped right on it.	Upuściłem kawałek metalu na podłogę w zagraconym pokoju. Prawie potrzebowałem wykrywacza metalu, ale na szczęście sam na niego nadepnąłem.
I bought a poster from the store but it was torn!	Kupiłem plakat w sklepie, ale był podarty!
I bought a poster from the store, but it was torn!	Kupiłem plakat w sklepie, ale był podarty!
If you do butt stuff, you’re going to Hell!	Jeśli lubisz seks analny, pójdziesz do piekła!
Have you been shopping lately?	Byłeś ostatnio na zakupach?
I hate tall decorations. It’s so easy to lose small things on top of them.	Nie cierpię wysokich ozdób. Łatwo zgubić coś małego na ich szczycie.
It’s always kind when a stranger helps a stranded motorist.	Miło, gdy obcy pomaga kierowcy, który utknął na drodze.
Have you ever touched a Tesla coil? It’s… shocking!	Dotykałeś kiedyś cewki Tesli? To… wstrząsające!
I hide copies of my keys in my house… The far west end. Don’t tell anyone.	Chowam zapasowe klucze w domu… Na samym zachodnim końcu. Nikomu nie mów.
I hid a key behind a bush in my side yard. But I changed my lock, so it’s useless.	Schowałem klucz za krzakiem na bocznym podwórku. Ale wymieniłem zamek, więc klucz jest bezużyteczny.
Don’t drop keys down the drain. When you wash your hands after you pee, be careful.	Nie wrzucaj kluczy do odpływu. Uważaj, gdy myjesz ręce po sikaniu.
Don’t you hate it when you find a key right next to a bunch of locked boxes and it doesn’t fit any of them?	Nie wkurza cię, gdy znajdujesz klucz tuż obok zamkniętych skrzynek, a on nie pasuje do żadnej?
I hid a key in a book, but then I opened the book and it fell on the floor.	Schowałem klucz w książce, ale gdy ją otworzyłem, wypadł na podłogę.
Someone hired me to find a lost key in the caves. I reached a dead end and never found it.	Miałem znaleźć zgubiony klucz w jaskiniach. Dotarłem do ślepego zaułka i niczego nie znalazłem.
I had amazing sex in the courtyard of a mansion once… Why am I saying this to a stranger?	Kiedyś uprawiałem niesamowity seks na dziedzińcu rezydencji… Czemu opowiadam o tym obcej osobie?
I love puzzles but the ones at the store are so expensive.	Uwielbiam łamigłówki, ale te w sklepie są strasznie drogie.
If you lose a fishing bait in the trees, you’d have to swim to it to get it back… The forest is so dense by the lake!	Jeśli zgubisz przynętę wśród drzew, musisz za nią dopłynąć… Las nad jeziorem jest bardzo gęsty!
Distance swimmers get the dirtiest sex. I wish I were a distance swimmer.	Pływacy długodystansowi uprawiają najbrudniejszy seks. Chciałbym być jednym z nich.
I love shopping. Don’t you?	Uwielbiam zakupy. A ty?
I heard that evil people bury keys after they die. What the Hell does that mean?	Słyszałem, że źli ludzie chowają klucze po śmierci. O co, do cholery, w tym chodzi?
If holy temples preach against sex, does that mean unholy temples teach you better sex?	Skoro świątynie dobra potępiają seks, to czy te złe uczą lepszego seksu?
I had a key on me, but I lost it sometime around my brother’s court date.	Miałem przy sobie klucz, ale zgubiłem go chyba w okolicach rozprawy mojego brata.
If you’re going to do something dirty, keep it in the bedroom!	Jeśli masz zamiar robić coś niegrzecznego, rób to w sypialni!
It’s a felony to use phones in the police station. What kind of bullshit is that?	Używanie telefonów na komisariacie to przestępstwo. Co to za bzdura?
Do you think they keep records in Hell? I’d love to see what kind of documentation can be found in that place!	Myślisz, że w piekle prowadzą dokumentację? Chętnie zobaczyłbym, jakie akta można tam znaleźć!
I love downloading puzzle games on my phone. They are so rewarding to beat!	Uwielbiam ściągać gry logiczne na telefon. Dają tyle satysfakcji, gdy uda się je przejść!
Have you ever wanted to see your friends naked? I do! That’s why I spend so much time learning to craft.	Chciałbyś zobaczyć nagich znajomych? Ja tak! Dlatego tyle czasu poświęcam tworzeniu przedmiotów.
With my bad back, I never pick up things that fall out of my pocket… Even at my own kitchen table.	Przez mój chory kręgosłup nie podnoszę rzeczy, które wypadają mi z kieszeni… nawet przy własnym kuchennym stole.
I’d love to know what kind of stuff is in the commissioner's bedroom. She’s so hot!	Chętnie zobaczyłbym, co jest w sypialni pani komisarz. Jest taka seksowna!
I love buying porn! Don't you?	Uwielbiam kupować porno! A ty?
Maps are super helpful! When in doubt, read a map.	Mapy są bardzo pomocne. Jak nie wiesz, co robić, zajrzyj na mapę.
If I ever found a motherload of treasure, I’d make sure I didn’t miss a single piece.	Gdybym znalazł ogromny skarb, dopilnowałbym, żeby nie przepadł ani jeden kawałek.
Why do bugs and animals always lead you to interesting things?	Czemu robaki i zwierzęta zawsze prowadzą do ciekawych miejsc?
I’m addicted to puzzle games!	Jestem uzależniony od gier logicznych!
Sometimes I don’t understand how certain ingredients can produce things that make no sense based on the ingredients.	Czasem nie rozumiem, jak z pewnych składników mogą powstawać rzeczy, które w ogóle do nich nie pasują.
Sometimes porn can be so expensive.	Czasem porno bywa strasznie drogie.
Solving puzzles is good for your health.	Rozwiązywanie zagadek jest dobre dla zdrowia.
I wonder if angels are sexy…	Ciekawe, czy anioły są seksowne…
Do you think cavemen wrote down instructions on making ancient weapons?	Myślisz, że jaskiniowcy zapisywali instrukcje tworzenia starożytnej broni?
I’d go for a hike, but there are too many sticks everywhere.	Poszedłbym na spacer, ale wszędzie leżą patyki.
Watch your step in the forest, you don’t want to step on a sharp rock.	Uważaj w lesie, żeby nie nadepnąć na ostry kamień.
The mansion on the hill is the only place I’ve ever seen a crow.	Jedynym miejscem, gdzie widziałem kruka, jest rezydencja na wzgórzu.
Why is it that people who pay rent always have hemp in their house?... Maybe it’s just my friends.	Czemu ludzie płacący czynsz zawsze mają w domu konopie?... Może tylko moi znajomi.
Do you know how to make a weapon? I need a weapon.	Umiesz zrobić broń? Potrzebuję broni.
People who push rocks off the cliffs in the forest are risking crushing a hiker.	Ludzie zrzucający głazy z klifów w lesie ryzykują, że zmiażdżą jakiegoś wędrowca.
Keep your eyes peeled in the forest. You never know what you might find.	Miej oczy szeroko otwarte w lesie. Nigdy nie wiadomo, co znajdziesz.
The porn variety here in the city is amazing!	W tym mieście jest niesamowity wybór pornografii!
I took a hike in the woods and hit a dead end… I did some crazy sex stuff there and wrote it all down!	Wybrałem się na spacer po lesie i dotarłem do ślepego zaułka… Uprawiałem tam szalony seks i wszystko zapisałem!
MILF porn is the best porn. I’m sure of it!	Najlepsze porno to MILF-y! Jestem tego pewien!
My boyfriend ran into the wall and my lost car key fell off the top of a mirror frame. Can you believe that?	Mój chłopak uderzył w ścianę, a zgubiony klucz do samochodu spadł z ramy lustra. Możesz w to uwierzyć?
I learned so much from fucking this slut I know in my wife’s bedroom. She should be appreciative.	Wiele się nauczyłem, pieprząc tę sukę, którą znam, w sypialni mojej żony. Powinna mi być wdzięczna.
Have you seen that amazing pussy-trick porn video? It’s amazing!	Widziałeś ten niesamowity film porno ze sztuczkami cipką? Jest rewelacyjny!
There’s nothing hotter than a native girl… Does that make me racist?	Nie ma nic seksowniejszego niż miejscowa dziewczyna… Czy to czyni mnie rasistą?
I wonder if it’s hard to see things in Hell… There’s no sunlight in Hell!	Ciekawe, czy w piekle trudno cokolwiek zobaczyć… Nie ma tam słońca!
If I were sent to Hell, I wouldn’t know what to do… Perhaps there are signs to look for.	Gdybym trafił do piekła, nie wiedziałbym, co robić… Może są tam jakieś znaki.
Did you know there is porn starring a nun?	Wiesz, że istnieje porno z zakonnicami?
I dropped my garage key in the backyard. There’s no way I’m finding it now.	Zgubiłem klucz do garażu na podwórku. Już go nie znajdę.
What’s dirtier, sex or garages?	Co jest brudniejsze: seks czy garaże?
I like to buy unique porn.	Lubię kupować nietypowe porno.
Have you ever chased a roach? They are so fast!	Goniłeś kiedyś karalucha? Są niesamowicie szybkie!
The real treasure is the sex you have along the way.	Prawdziwym skarbem jest seks po drodze.
Treasure hunters are such horn-dogs.	Poszukiwacze skarbów to straszne napaleńce.
If you see something you want far away, sometimes you can get to it from a different area.	Jeśli coś, czego chcesz, jest daleko, czasem można dotrzeć do tego z innego miejsca.
Sometimes storage closets hold naughty secrets.	W schowkach czasem kryją się niegrzeczne sekrety.
There are some amazing views in the forest. Makes me want to take a picture of them.	W lesie są niesamowite widoki. Aż chce się je sfotografować.
Did you hear that the old news lady from Channel 4 is making porn now!?	Słyszałeś, że była prezenterka z Channel 4 kręci teraz porno!?
I saw some cop sweating a lot about something. I wonder what his problem was.	Widziałem policjanta, który strasznie się pocił. Ciekawe, co mu dolegało.
Our city’s judge looks mighty rich… I wonder what he has in his office.	Sędzia naszego miasta wygląda na bardzo bogatego… Ciekawe, co trzyma w biurze.
I've always dreamed of getting tied up and fucked on a beach. Is that weird to say?	Zawsze marzyłem, żeby ktoś związał mnie i zerżnął na plaży. Dziwnie to brzmi?
Do you think angels celebrate Christmas? I wonder what gifts they get.	Myślisz, że anioły obchodzą Boże Narodzenie? Ciekawe, jakie dostają prezenty.
Once, a rat stole my house key and I found it in the wall.	Kiedyś szczur ukradł mi klucz do domu. Znalazłem go w ścianie.
Once a rat stole my house key and I found it in the wall.	Kiedyś szczur ukradł mi klucz do domu. Znalazłem go w ścianie.
My favorite kind of porn is pussy eating from behind. It’s so hot!	Najbardziej lubię porno z jedzeniem cipki od tyłu. Ależ to podniecające!
Do you think the sexy girls living in the apartments are hiding anything sexy? I love sexy things!	Myślisz, że seksowne dziewczyny z apartamentowców coś ukrywają? Uwielbiam takie rzeczy!
Every time my cat gets a stomach ache, it seeks out mint leaves. I heard it grows in the Casula Forest near water.	Za każdym razem, gdy mojego kota boli brzuch, szuka liści mięty. Podobno rośnie przy wodzie w lesie Casula.
Why do people hide keys in their bathrooms?	Dlaczego ludzie chowają klucze w łazience?
I was meeting with someone who told me he saw two keys in one room! What kind of crazy world do we live in?	Rozmawiałem z kimś, kto widział dwa klucze w jednym pokoju! Co za szalone czasy!
MILF porn is so hot!	Porno z MILF-ami jest takie gorące!
Kinky moms hide naughty shit in their bathrooms… Trust me.	Niegrzeczne matki chowają świństwa w łazienkach… Wiem, co mówię.
High-level executives are into some wild shit.	Kierownicy wysokiego szczebla lubią ostre rzeczy.
I saw a beautiful woman head into a cave.	Widziałem piękną kobietę wchodzącą do jaskini.
What the hell is with the roach problem in this city? Are they coming from the caves?	Co jest z tym problemem karaluchów w mieście? Przychodzą z jaskiń?
People lock keys in lockers… But you need a key to get a key?... That’s too weird for me!	Ludzie zamykają klucze w szafkach… Ale żeby wyjąć klucz, trzeba mieć klucz?... To dla mnie za dziwne!
The naughtiest things are found deep in dark places.	Najbardziej niegrzeczne rzeczy kryją się głęboko w ciemnych miejscach.
You’d need to use TNT to scare me from a good doggy style fucking.	Tylko TNT odwiodłoby mnie od porządnego rżnięcia na pieska.
There are some porn videos that just go too far.	Niektóre filmy porno posuwają się za daleko.
There’s a guy who gives expensive gifts to sexy ladies, but will charge an ugly guy like you an arm and a leg.	Jest facet, który kupuje seksownym kobietom drogie prezenty, ale od brzydala takiego jak ty zedrze majątek.
There’s a rumor that the executives at the police station have tunnels between their offices.	Podobno kierownicy na komisariacie mają tunele łączące ich biura.
Have you seen the latest porn video?	Widziałeś najnowszy film porno?
You ever wonder what lies up in the rafters of tall gymnasiums? I tried to find out by burrowing a hole in the wall upstairs but then I got expelled from school for vandalism.	Zastanawiałeś się kiedyś, co jest na belkach pod sufitem w wysokiej sali gimnastycznej? Próbowałem się tam dostać, wiercąc dziurę w ścianie na piętrze, ale wyrzucili mnie ze szkoły za wandalizm.
Have you ever thought about the police commissioner getting kinky? I know I do.	Zastanawiałeś się kiedyś, czy pani komisarz lubi ostre zabawy? Ja często o tym myślę.
My best friend died... I'm pretty sure she went to Hell.	Moja najlepsza przyjaciółka zmarła… Jestem prawie pewien, że trafiła do piekła.
Arrows are amazing at pointing to where you need to go.	Strzałki świetnie pokazują drogę.
Do you think detective skills will work in the afterlife?	Myślisz, że umiejętności detektywa przydadzą się w zaświatach?
The porn shop lady has a video you can buy!	Kobieta ze sklepu porno ma film na sprzedaż!
You think anything good is buried in Hell? That’s where I’m going for what I did to my neighbor's dog.	Myślisz, że w piekle jest coś wartego znalezienia? Ja tam idę za to, co zrobiłem psu sąsiada.
Have you seen that new porn video going around with those silver-haired crazy ladies?	Widziałeś nowy film porno z tymi szalonymi siwowłosymi kobietami?
I wonder if they have sex in Heaven... Do angels know how to have sex?	Ciekawe, czy w niebie uprawia się seks… Czy anioły wiedzą, jak to robić?
I wonder if there is a geological history in Hell.	Ciekawe, czy piekło ma jakąś historię geologiczną.
I like solving puzzles as long as I get a reward.	Lubię rozwiązywać zagadki, jeśli dostaję za to nagrodę.
I’m at a loss for words.	Brak mi słów.
You look like a man who has his shit together.	Wyglądasz na faceta, który ma wszystko pod kontrolą.
I’ve got nothing to tell you.	Nie mam ci nic do powiedzenia.
I’m busy. Go away.	Jestem zajęty. Idź sobie.
You look like you have the sex virus. Stay away.	Wyglądasz, jakbyś miał wirusa seksu. Trzymaj się z daleka.
Don’t talk to me.	Nie rozmawiaj ze mną.
'''
MAP={}
for line in DATA.splitlines():
 if not line: continue
 source,target=line.split('\t',1)
 MAP[source]=target
known=set()
for pattern in ('custom-dialogue-repeated-*.jsonl','custom-dialogue-scene-*-01.jsonl','custom-dialogue-npc-system-*.jsonl'):
 for p in (ROOT/'drafts').glob(pattern):
  for line in p.read_text(encoding='utf8').splitlines():
   row=json.loads(line)
   if row.get('translation','').strip(): known.add(row['id'])
rows=[]
missing=set()
for line in CANON.read_text(encoding='utf8').splitlines():
 row=json.loads(line)
 c=row['context']
 if c.get('source_kind')=='common_event' and c.get('event_id')==25:
  source=row['source_text'].strip()
  target=MAP.get(source)
  if target is None: missing.add(source); continue
  if row['id'] not in known:
   row['translation']=target
   rows.append(row)
if missing: raise SystemExit('Unmapped event-25 source strings: '+repr(sorted(missing)))
OUT.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf8',newline='\n')
print(f'Wrote NPC-system records from {len(MAP)} source strings: {len(rows)}; reused/previously drafted IDs: {342-len(rows)}')
