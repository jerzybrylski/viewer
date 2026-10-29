#!/usr/bin/env python3
"""Build Polish drafts for player-facing courtroom dialogue on Map 203."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map203-courtroom-followups-01.jsonl'
TRANSLATIONS = {
    "A woman of the law, sworn to defend our city from crime...": 'Stróżka prawa, która przysięgła chronić nasze miasto przed przestępczością…',
    "... was responsible for propping up the largest criminal organization in our country's history.": '…odpowiadała za wspieranie największej organizacji przestępczej w historii naszego kraju.',
    'She recruits a woman who escaped from prison!... A woman who still has several years left to serve… A dangerous and unremorseful thief!': 'Zwerbowała kobietę, która uciekła z więzienia!... Kobietę, która ma jeszcze odsiedzieć kilka lat… Niebezpieczną złodziejkę bez krzty skruchy!',
    'Aided by an officer of the law… 1Hero Canmore… A murderer and a right-hand man to Andrea Kimura’s criminal enterprise.': 'Z pomocą stróża prawa… 1Hero Canmore’a… Mordercy i prawej ręki przestępczego imperium Andrei Kimury.',
    'With a little luck, these low-lifes would be tarnishing the art world and undermining the science of archeology...': 'Przy odrobinie szczęścia te szumowiny zbezcześciłyby świat sztuki i skompromitowały archeologię…',
    '... under the leadership of a psychotic lunatic… Duncan Helmer.': '…pod przywództwem psychopatycznego szaleńca… Duncana Helmera.',
    'Thank God we stopped them when we did…': 'Dzięki Bogu, że zdążyliśmy ich powstrzymać…',
    'And after all this… After decades of deceit… You expect me to simply walk out of this courtroom?': 'I po tym wszystkim… Po dekadach oszustw… Oczekujecie, że po prostu wyjdę z tej sali sądowej?',
    'Boring!': 'Nuda!',
    'Hannah!': 'Hannah!',
    'This is an outrage!': 'To skandal!',
    'Another outburst like that and I’ll charge you with contempt.': 'Jeszcze jeden taki wybryk, a oskarżę cię o obrazę sądu.',
    'You’ve clearly been bribed!': 'Najwyraźniej cię przekupiono!',
    'I will not stand for such accusations!': 'Nie będę tolerować takich oskarżeń!',
    'Your glasses literally have golden dollar signs in them.': 'W twoich okularach są dosłownie złote znaki dolara.',
    'These are prescription glasses! Remove this man from my courtroom.': 'To okulary korekcyjne! Proszę usunąć tego człowieka z mojej sali sądowej.',
    'On charges of theft, criminal conspiracy, and corruption, I find the defendant, Andrea Kimura, guilty.': 'Za kradzież, spisek kryminalny i korupcję uznaję oskarżoną Andreę Kimurę za winną.',
    'Finally some justice.': 'Wreszcie jakaś sprawiedliwość.',
    'I hereby order Andrea Kimura to house arrest for a period of one year.': 'Niniejszym skazuję Andreę Kimurę na roczny areszt domowy.',
    'Quite fair.': 'Dość sprawiedliwie.',
    'On the charges of theft and criminal conspiracy, I find the defendant, Nellie Cole, not guilty.': 'Uznaję oskarżoną Nellie Cole za niewinną zarzucanych jej kradzieży i udziału w spisku kryminalnym.',
    'Miss Cole, you are hereby cleared of your criminal record for your role in taking down the Eclipse Guild kingpin, Duncan Helmer.': 'Panno Cole, niniejszym oczyszczam pani kartotekę karną w związku z pani udziałem w obaleniu przywódcy Gildii Eclipse, Duncana Helmera.',
    'Oh, come on! This is outrageous, Your Honor!': 'No nie! To skandal, Wysoki Sądzie!',
    'Order in the court!': 'Proszę o spokój na sali!',
    'Paul! Be quiet!': 'Paul! Cisza!',
    'On the charges of theft and criminal conspiracy, I find the defendant, 1Hero Canmore, not guilty…': 'Uznaję oskarżonego 1Hero Canmore’a za niewinnego zarzucanych mu kradzieży i udziału w spisku kryminalnym…',
    'Your dedication to the force is admirable and I hereby promote you to senior detective.': 'Pańskie oddanie służbie jest godne podziwu. Niniejszym awansuję pana na starszego detektywa.',
    'Can a judge do that?': 'Sędzia może tak zrobić?',
    'Congratulations, 1Hero.': 'Gratulacje, 1Hero.',
    'Looks like we’re peers, Mr. Canmore.': 'Wygląda na to, że jesteśmy teraz równorzędnymi funkcjonariuszami, panie Canmore.',
    'Excited?': 'Cieszysz się?',
    'This court stands adjourned.': 'Zamykam posiedzenie sądu.',
    'I’m a free man!': 'Jestem wolny!',
    'Hell yeah, baby! We’re free!': 'No jasne, kochanie! Jesteśmy wolni!',
    'Corruption is awesome!': 'Korupcja jest wspaniała!',
    'Shh!': 'Ciii!',
    'I don’t know what to say, Andrea…': 'Nie wiem, co powiedzieć, Andrea…',
    'I held up my end of the bargain.': 'Dotrzymałem swojej części umowy.',
    'I don’t know how you do it, 1Hero… You always find a way to win.': 'Nie wiem, jak ty to robisz, 1Hero… Zawsze znajdujesz sposób, żeby wygrać.',
    'What can I say?': 'Cóż mogę powiedzieć?',
    'You’re a good man, 1Hero.': 'Jesteś dobrym człowiekiem, 1Hero.',
    'Same to you, Jon. You don’t know how much you’ve helped not just me, but the whole world.': 'Wzajemnie, Jon. Nie wiesz, jak bardzo pomogłeś nie tylko mnie, ale i całemu światu.',
    'I’ll take your word for it.': 'Zaufam ci na słowo.',
    'What’s going on here? How did you pull this off?': 'Co tu się dzieje? Jak to załatwiłeś?',
    'Calm down, Paul. There’s no story here… I have something far juicier we can discuss later.': 'Spokojnie, Paul. Nie ma tu żadnej sensacji… Później opowiem ci coś znacznie ciekawszego.',
    'Congratulations on your promotion, 1Hero.': 'Gratulacje z okazji awansu, 1Hero.',
    'I take it you had something to do with that.': 'Czyli to twoja sprawka?',
    'I look forward to working with you on the next case, detective.': 'Nie mogę się doczekać kolejnej wspólnej sprawy, detektywie.',
    'It seems Miss Bhatt and I will be getting a lot closer in the coming months.': 'Wygląda na to, że w nadchodzących miesiącach zbliżę się do panny Bhatt.',
    'You didn’t hear? Andrea is now Melissa’s neighbor.': 'Nie słyszałeś? Andrea jest teraz sąsiadką Melissy.',
    'Wait… What happened to your mansion?': 'Chwila… Co się stało z twoją rezydencją?',
    'Let’s just say… I downgraded a bit.': 'Powiedzmy, że teraz mieszkam trochę skromniej.',
    'We better hire 1Hero’s replacement, and fast.': 'Musimy jak najszybciej znaleźć zastępstwo za 1Hero.',
    'Can I be a detective?': 'Mogę zostać detektywem?',
    'Haha! Could you imagine?': 'Haha! Wyobrażasz to sobie?',
    'Hey, 1Hero, do you know where Ella is?': 'Hej, 1Hero, wiesz, gdzie jest Ella?',
    'She hasn’t been showing up online…': 'Nie pojawia się ostatnio w sieci…',
    'Is she okay? Is… she in trouble?': 'Wszystko z nią w porządku? Czy… wpakowała się w kłopoty?',
    'The investigation into Morgan Deluna is ongoing. We can’t comment any further.': 'Śledztwo w sprawie Morgan Deluny wciąż trwa. Nie możemy ujawnić nic więcej.',
    'I’m sorry, Larry, I can’t help you.': 'Przykro mi, Larry, nie mogę ci pomóc.',
    'Come on, Dad. Let’s go get some lunch.': 'Chodź, tato. Idziemy coś zjeść.',
    'I’m starving!': 'Umieram z głodu!',
    'Seems I’m not the only one who lost her home.': 'Wygląda na to, że nie tylko ja straciłam dom.',
    'I think I can get used to condo life… It’s quaint.': 'Chyba przywyknę do życia w mieszkaniu… Jest przytulne.',
    'Too bad the mansion is locked up… It would be the perfect place for a party.': 'Szkoda, że rezydencja jest zamknięta… To byłoby idealne miejsce na imprezę.',
    'You know… The state owns the mansion.': 'Wiesz… rezydencja należy teraz do państwa.',
    'Unfortunate.': 'Szkoda.',
    'Guess who’s in charge of the keys?': 'Zgadnij, kto ma klucze?',
    'You crazy bastard.': 'Ty szalony draniu.',
    'Is it safe there?': 'To miejsce jest bezpieczne?',
    'It’s been inspected and deemed structurally sound… and now it’s for sale!': 'Została sprawdzona i uznana za konstrukcyjnie bezpieczną… a teraz jest na sprzedaż!',
    'Woohoo! 1Hero bought a mansion!': 'Juhu! 1Hero kupił rezydencję!',
    'Haha! Not quite, Hannah.': 'Haha! Niezupełnie, Hannah.',
    'I don’t know how I feel about sneaking into that mansion again.': 'Nie wiem, co sądzić o ponownym włamaniu się do tej rezydencji.',
    'Oh, Mom. Just let loose. It’ll be fine.': 'Och, mamo. Wyluzuj, wszystko będzie dobrze.',
    'What about Ella? Where is she?': 'A co z Ellą? Gdzie ona jest?',
    'I have a feeling she’ll show up to the party.': 'Mam przeczucie, że wpadnie na imprezę.',
    'Well, I’m up for letting loose!': 'No, ja chętnie zaszaleję!',
    'Count me in!': 'Piszę się na to!',
    'Me, too!': 'Ja też!',
    'And me!': 'I ja!',
    'Let’s be naughty!': 'Bądźmy niegrzeczni!',
    'I like your attitude, Sister.': 'Podoba mi się twoje podejście, siostro.',
    'I ain’t going to an orgy dressed like this.': 'Nie pójdę na orgię w takim stroju.',
    'Technically, it’s a reverse gangbang.': 'Technicznie rzecz biorąc, to odwrócony gangbang.',
    'Wait… What about Andrea? She’s under house arrest?': 'Chwila… A co z Andreą? Jest w areszcie domowym?',
    'Don’t worry about that. I’ve made arrangements.': 'Nie martw się, wszystko już załatwione.',
    'Everyone, meet at the mansion in two hours.': 'Wszyscy spotykamy się w rezydencji za dwie godziny.',
    'Don’t be late, girls.': 'Nie spóźnijcie się, dziewczyny.',
    'I’m never late!': 'Ja się nigdy nie spóźniam!',
    'I didn’t know judges could promote police personnel.': 'Nie wiedziałem, że sędziowie mogą awansować funkcjonariuszy policji.',
    'Life’s full of surprises.': 'Życie jest pełne niespodzianek.',
    'I’m glad you’re back, Canmore.': 'Cieszę się, że wróciłeś, Canmore.',
    'How is freedom feeling?': 'Jak smakuje wolność?',
    'Congratulations on the promotion, detective.': 'Gratulacje z okazji awansu, detektywie.',
    'Hello, Your Honor.': 'Dzień dobry, Wysoki Sądzie.',
    'Did you know there are Koi fish that cost six figures?... I bet they have magic powers… No… I’m certain they have magic powers.': 'Wiesz, że karpie koi mogą kosztować sześciocyfrowe sumy?... Założę się, że mają magiczne moce… Nie… Jestem pewien, że mają magiczne moce.',
    'You’re looking great today, Your Honor.': 'Świetnie dziś wyglądasz, Wysoki Sądzie.',
    'Remember, the location needs to be very scenic. Only the best for government housing.': 'Pamiętaj, miejsce musi być bardzo malownicze. W końcu to lokum dla przedstawiciela władz.',
    'Good luck with your fish.': 'Powodzenia z rybami.',
    'Put any more thought into adding a koi pond? It’s a good investment.': 'Myślałeś jeszcze o tym, żeby założyć staw z karpiami koi? To dobra inwestycja.',
    'No need to suck up, detective. Just enjoy your freedom.': 'Nie musisz mi się podlizywać, detektywie. Po prostu ciesz się wolnością.',
    'Magic fish.': 'Magiczne ryby.',
    'Not quite, Your Honor. The jacuzzi is working out nicely.': 'Nie całkiem, Wysoki Sądzie. Jacuzzi świetnie działa.',
    'Any reason you’re not in your office?': 'Jakiś powód, dla którego nie siedzisz w swoim gabinecie?',
    'A shame. If you ever want advice on how to set up the pond, don’t be a stranger.': 'Szkoda. Gdybyś chciał porady, jak urządzić staw, wiesz, gdzie mnie znaleźć.',
    'Always investigating something. Huh, detective?': 'Zawsze coś śledzisz, co, detektywie?',
    'Just asking.': 'Tak tylko pytam.',
    'I’m waiting for a phone call to the courtroom phone.': 'Czekam na telefon, który ma zadzwonić na salę rozpraw.',
    'Are you messing with the phone, 1Hero?': 'Majstrujesz przy telefonie, 1Hero?',
    'Oh… Sorry, judge.': 'Och… Przepraszam, Wysoki Sądzie.',
    'I hope you find something in the Casula Forest, 1Hero.': 'Mam nadzieję, że coś znajdziesz w Lesie Casula, 1Hero.',
    'Good news! I found the perfect spot for… the state’s government housing.': 'Dobre wieści! Znalazłem idealne miejsce na… rządową posiadłość.',
    'This looks amazing! I can build a fishing pier and maybe put some nice expensive Japanese koi fish in there.': 'Wygląda świetnie! Mogę zbudować pomost i wpuścić do stawu piękne, drogie japońskie karpie koi.',
    'A koi pond for your mansion?': 'Staw z karpiami koi przy twojej rezydencji?',
    'Government housing!': 'Mieszkanie służbowe!',
    'So we’re good?': 'Czyli wszystko załatwione?',
    'Great work, detective.': 'Dobra robota, detektywie.',
    'So does this mean my farm is safe… Your Honor?': 'Czy to znaczy, że moja farma jest bezpieczna… Wysoki Sądzie?',
    'We’ll see… Now go back to your country bumpkin life and give that loud voice of yours a rest.': 'Zobaczymy… A teraz wracaj do swojego prowincjonalnego życia i daj odpocząć temu donośnemu głosowi.',
    'Country bumpkin, huh?': 'Prowincjuszka, co?',
    'Excuse me, Your Honor, but it’s not like the state really needs two mansions.': 'Wybacz, Wysoki Sądzie, ale chyba państwo nie potrzebuje dwóch rezydencji.',
    'Government houses.': 'Rządowe mieszkania.',
    'Right, government houses.': 'Zgadza się, rządowe mieszkania.',
    'Yes, good point.': 'Tak, słuszna uwaga.',
    'Very well, Miss Ray. The court will rescind the state seizure of your land.': 'W porządku, panno Ray. Sąd uchyla decyzję państwa o przejęciu pani ziemi.',
    'Damn straight.': 'No ba!',
    'Now if you’ll excuse me, I need to take a long overdue bathroom break.': 'A teraz, jeśli pani pozwoli, muszę wreszcie skorzystać z toalety.',
    'I really need to stop eating spicy tacos.': 'Naprawdę muszę przestać jeść ostre tacos.',
    'I won’t lose my farm!': 'Nie stracę swojej farmy!',
    'See? It all worked out.': 'Widzisz? Wszystko dobrze się skończyło.',
    'Only thanks to you, 1Hero.': 'Tylko dzięki tobie, 1Hero.',
    'If it had been left up to that judge, I don’t know what would’ve happened.': 'Gdyby wszystko zależało od tego sędziego, nie wiem, co by się stało.',
    'I’m sure you could’ve figured out a way.': 'Jestem pewna, że i tak znalazłbyś jakieś wyjście.',
    'Seeing as how we’re all alone here, maybe we could tarry a bit…': 'Skoro jesteśmy tu sami, może trochę się zabawimy…',
    '… and see how that would’ve played out?': '…i zobaczymy, jak by się to potoczyło?',
    'Oh?': 'Ach tak?',
    'Your Honor, my farm is in danger… Whatever shall I do?': 'Wysoki Sądzie, moja farma jest zagrożona… Co ja pocznę?',
    'Miss Carol Ray, you stand before the court to contest an order of the state. Please state your case.': 'Pani Carol Ray, staje pani przed sądem, by zaskarżyć decyzję władz. Proszę przedstawić swoją sprawę.',
    'I’m just a simple country farmer. My farm is everything to me.': 'Jestem zwykłą wiejską farmerką. Moja farma jest dla mnie wszystkim.',
    'But then I received this order from the court, and…': 'Ale potem dostałam to postanowienie z sądu i…',
    'It says the state is taking my farm away!': 'Państwo odbiera mi moją farmę!',
    'Please, Your Honor, help me!': 'Proszę, Wysoki Sądzie, niech mi pan pomoże!',
    'I understand your plight, Miss Ray.': 'Rozumiem pani położenie, panno Ray.',
    'But there’s more to this matter, isn’t there? Something about Casula ruins.': 'Ale jest tu coś jeszcze, prawda? Chodzi o ruiny Casula.',
    'Yes, I recently discovered Casula ruins in a cave on my land.': 'Tak, niedawno odkryłam ruiny Casula w jaskini na mojej ziemi.',
    'And now the state is saying it has to preserve them.': 'A teraz państwo twierdzi, że trzeba je chronić.',
    'That’s why they’re taking my land away, Your Honor.': 'Dlatego odbierają mi ziemię, Wysoki Sądzie.',
    'It’s a very serious matter, Miss Ray. The state has a responsibility to secure the history of the state’s indigenous culture.': 'To poważna sprawa, panno Ray. Państwo ma obowiązek chronić historię rdzennej kultury tego regionu.',
    'So I’m to be left out of hearth and home?': 'Czyli mam zostać bez dachu nad głową?',
    'You can’t do this to me!': 'Nie możecie mi tego zrobić!',
    'Order in the court! Miss Ray, you will calm yourself down, or I will hold you in contempt of the court.': 'Proszę o spokój na sali! Panno Ray, proszę się uspokoić, inaczej ukarzę panią za obrazę sądu.',
    'Of course, Your Honor!': 'Oczywiście, Wysoki Sądzie!',
    'Good. Now about your situation…': 'Dobrze. Wracając do pani sprawy…',
    'The state has a strong case here. I’m afraid that if you have nothing more to add, I’ll have to rule in favor of the state.': 'Państwo ma mocne argumenty. Jeśli nie ma pani nic więcej do dodania, będę musiał orzec na korzyść państwa.',
    'Oh, no, Your Honor!': 'O nie, Wysoki Sądzie!',
    'As it turns out, I would like to offer up something for the consideration of the court.': 'Właściwie chciałabym przedstawić sądowi coś, co może mieć znaczenie dla sprawy.',
    'But it’s very sensitive. May I approach the bench, Your Honor?': 'To jednak bardzo delikatna sprawa. Czy mogę podejść do ławy, Wysoki Sądzie?',
    'Hmm, very well, Miss Ray. I’ll allow it.': 'Hmm, dobrze, panno Ray. Proszę.',
    'You won’t regret it, Your Honor.': 'Nie pożałuje pan, Wysoki Sądzie.',
    'Damn, you got really serious at the end.': 'Cholera, pod koniec zrobiłaś się naprawdę poważna.',
    'I had to make sure I got the outcome I wanted.': 'Musiałam mieć pewność, że sprawa zakończy się po mojej myśli.',
    'Come on, I’ll see you home.': 'Chodź, odprowadzę cię do domu.',
    'Don’t worry about me. I’ll head home on my own in a minute.': 'Nie martw się o mnie. Zaraz sama wrócę do domu.',
    'You should get back to work.': 'Wracaj do pracy.',
    'Sticking around?': 'Zostajesz tu?',
    'Just admiring your office, 1Hero. It’s quite lovely.': 'Podziwiam tylko twoje biuro, 1Hero. Jest naprawdę ładne.',
    'You might make the judge mad if he finds you hanging around here.': 'Sędzia może się wkurzyć, jeśli przyłapie cię tu na kręceniu się bez celu.',
    'Don’t you worry about that.': 'Tym się nie martw.',
    'Well, if you insist. I’ll see you later, Carol.': 'Skoro nalegasz. Do zobaczenia, Carol.',
    'See you later, studmuffin.': 'Do zobaczenia, przystojniaku.',
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
        or context.get('map_id') != 203
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
    raise SystemExit('Unmapped Map 203 strings: ' + repr(sorted(unmapped)))
if OUTPUT.exists():
    raise SystemExit(f'Refusing to overwrite {OUTPUT}')
if len(rows) != 171:
    raise SystemExit(f'Expected exactly 171 player-facing dialogue lines, found {len(rows)}')
OUTPUT.write_text(
    ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows),
    encoding='utf-8',
    newline='\n',
)
print(f'Wrote {len(rows)} Map 203 dialogue lines across {len({r["context"]["event_id"] for r in rows})} events')
