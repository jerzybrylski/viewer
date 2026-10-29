import json
from pathlib import Path
ROOT=Path('games/the-genesis-order/translation')
CANON=ROOT/'export-v1/custom_dialogue.jsonl'
MERGED=Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step3.jsonl')
OUT=ROOT/'drafts/custom-dialogue-map31-tasha-inquiry-01.jsonl'
if OUT.exists(): raise SystemExit(f'Refusing to overwrite {OUT}')
MAP={
'A creative story, for sure.':'Trzeba przyznać, że niezła historia.',
'I did a little digging…':'Trochę poszperałem…',
"Diana and Henry won't like it, but I think you might just be a valuable person to keep around.":'Diana i Henry nie będą zachwyceni, ale może warto mieć cię po swojej stronie.',
'What can you tell me about your mom? Is she a spy?':'Co możesz powiedzieć o swojej matce? Jest szpiegiem?',
'Tasha, I need a two sided dildo.':'Tasha, potrzebuję dwustronnego dildo.',
'Have fun with your sex toys, 1Hero.':'Miłej zabawy z zabawkami erotycznymi, 1Hero.',
'Sorry about your job. But hopefully the mustache works out for ya.':'Przykro mi z powodu pracy. Może przynajmniej wąsy ci się przydadzą.',
'Henry can handle himself…':'Henry sam sobie poradzi…',
'Good luck, 1Hero. Sounds like you’ll need it.':'Powodzenia, 1Hero. Chyba ci się przyda.',
'Have anything you want to tell me about your friends?':'Chcesz mi coś powiedzieć o swoich znajomych?',
'Trust is a two-way street, detective…':'Zaufanie działa w obie strony, pani detektyw…',
'For your moms?':'Dla twoich mam?',
'I hope.':'Mam nadzieję.',
'You don’t have to believe me. But if you ever meet her, be warned.':'Nie musisz mi wierzyć. Ale jeśli kiedyś ją spotkasz, miej się na baczności.',
'I’ve been told to keep my mouth shut.':'Kazano mi trzymać język za zębami.',
'I’m not telling you shit.':'Nic ci, kurwa, nie powiem.',
'What!? No! For… my girlfriend and my… other girlfriend.':'Co!? Nie! To dla… mojej dziewczyny i… drugiej dziewczyny.',
'She’ll break you.':'Złamie cię.',
'You don’t look like the type of woman to take orders from anyone.':'Nie wyglądasz na kobietę, która słucha czyichś rozkazów.',
'Fine.':'Dobra.',
'Just how popular are you?':'Aż tak popularna jesteś?',
'I’ll keep that in mind.':'Zapamiętam to.',
'That includes you.':'Ciebie też.',
'Popular enough. Now, do you have it or not?':'Wystarczająco. Masz to czy nie?',
'Let me ask. Is she in North Santiva?':'Powiedz mi… Jest w North Santiva?',
'The only thing I have in stock are one-sided dildos…':'Mam na stanie tylko jednostronne dildo…',
'A demi-demon? Really?':'Półdemon? Naprawdę?',
'I don’t know. She was living in the big mansion, west of the city.':'Nie wiem. Mieszkała w wielkiej rezydencji na zachód od miasta.',
'If you’re looking for more info on Duncan, my lips are sealed.':'Jeśli szukasz informacji o Duncanie, nic ze mnie nie wyciągniesz.',
'But I can sell you two.':'Ale mogę sprzedać ci dwa.',
'But now, we can’t find her…':'Ale teraz nie możemy jej znaleźć…',
'The stories I can tell you about Madalyn would blow your mind.':'Opowieści, które mógłbym ci zdradzić o Madalyn, zwaliłyby cię z nóg.',
'Who ever said I wanted to talk to you about Duncan?':'Kto powiedział, że chcę z tobą rozmawiać o Duncanie?',
'If that’s the best you can do, then I’ll take them.':'Jeśli to najlepsze, co masz, to je biorę.',
'What she was doing here, I don’t know.':'Nie wiem, co tu robiła.',
'Do you have $200?':'Masz 200 dolarów?',
'I’m starting to wonder if I can trust you.':'Zaczynam się zastanawiać, czy mogę ci ufać.',
'I wish I could tell you more, detective.':'Chciałabym powiedzieć ci więcej, pani detektyw.',
'You’ve offered… an interesting perspective.':'Przedstawiłaś… ciekawy punkt widzenia.',
'That sounds expensive.':'To brzmi drogo.',
'You don’t believe in the supernatural, do you?':'Nie wierzysz w zjawiska nadprzyrodzone, prawda?',
'Stop by any time. The door is always open.':'Wpadaj, kiedy chcesz. Drzwi są zawsze otwarte.',
'Do you want them or not?':'Chcesz je, czy nie?',
'I’m a detective. I don’t believe in anything I don’t have evidence for.':'Jestem detektywką. Nie wierzę w nic, na co nie mam dowodów.',
'See ya later, Tasha.':'Na razie, Tasha.',
'If you’re going after Madalyn, you may want to adjust your worldview.':'Jeśli zamierzasz dopaść Madalyn, może czas zmienić poglądy.',
'Humor me. What makes you think she’s a demon?':'Zaspokój moją ciekawość. Dlaczego myślisz, że jest demonem?',
'Here you go…':'Proszę…',
'I thought I saw you come in here, detective.':'Wydawało mi się, że widziałam, jak pani tu wchodzi, pani detektyw.',
'Nellie? Are you following me?':'Nellie? Śledzisz mnie?',
'Mom!':'Mamo!',
'Tasha!':'Tasha!',
'Suit yourself.':'Jak chcesz.',
'What the hell are you doing here? You’re supposed to be in jail!':'Co ty, do cholery, tutaj robisz? Powinnaś siedzieć w więzieniu!',
'Wait… You’re Tasha’s mom?':'Zaraz… Jesteś matką Tashy?',
'I thought you were in Cape Vedra.':'Myślałem, że jesteś w Cape Vedra.',
'I moved.':'Przeprowadziłam się.',
'Shit… I don’t. I’ll come back in a bit.':'Cholera… Nie wiem. Wrócę później.',
'Did you break out of prison again?':'Znowu uciekłaś z więzienia?',
'Not this time.':'Tym razem nie.',
'They set you free? I don’t understand.':'Wypuścili cię? Nie rozumiem.',
'Yeah. Why don’t you explain it to the both of us.':'Tak. Może wyjaśnisz to nam obojgu.',
'And how the hell do you know my mom?':'I skąd, do cholery, znasz moją mamę?',
'I just interrogated her after she stole an artifact.':'Przesłuchałam ją po tym, jak ukradła artefakt.',
'I didn’t steal shit!':'Nic nie ukradłam!',
'That’s not true.':'To nieprawda.',
'I didn’t steal any NEW shit.':'Nie ukradłam żadnego NOWEGO gówna.',
'She had an artifact that was stolen by the Eclipse Guild.':'Miała artefakt skradziony przez Gildię Eclipse.',
'You’re working for the Guild?':'Pracujesz dla Gildii?',
'You know who the Guild is?':'Wiesz, czym jest Gildia?',
'Her friends also work for the Guild.':'Jej znajomi też pracują dla Gildii.',
'What!? That’s not true!':'Co!? To nieprawda!',
'I looked up the Guild files at the station and I know that Diana works as a thief.':'Sprawdziłam akta Gildii na posterunku. Wiem, że Diana jest złodziejką.',
'You’re wrong! She’s trying to kill Duncan.':'Mylisz się! Próbuje zabić Duncana.',
'Just who are these friends of yours, Tasha?':'Kim właściwie są ci twoi znajomi, Tasha?',
'They are treasure hunters. They don’t work for the Eclipse Guild.':'Są poszukiwaczami skarbów. Nie pracują dla Gildii Eclipse.',
'I saw the files. You can’t lie.':'Widziałam akta. Nie kłam.',
'Diana has no connection to them anymore. Duncan tried to kill her.':'Diana już z nimi nie współpracuje. Duncan próbował ją zabić.',
'You need to stay the hell away from the Guild. Do you hear me, Tasha?':'Trzymaj się z dala od Gildii, do cholery. Słyszysz, Tasha?',
'Now all the sudden you care about me?':'Nagle zaczęło ci na mnie zależeć?',
'I’m your mother.':'Jestem twoją matką.',
'How long have you been out of prison?':'Od jak dawna jesteś na wolności?',
'I was going to come find you… I just can’t right now.':'Chciałam cię odszukać… Ale teraz nie mogę.',
'What are you doing here, Mom?':'Co tu robisz, mamo?',
'I… I can’t tell you…':'Ja… Nie mogę ci powiedzieć…',
'But give me some time and I’ll come back for you…':'Daj mi trochę czasu, a wrócę po ciebie…',
'I’m getting my life back.':'Odzyskuję swoje życie.',
'Who are you rolling with?':'Z kim teraz trzymasz?',
'I have to go.':'Muszę iść.',
'Hey! Come back!':'Hej! Wracaj!',
}
known=set()
for line in MERGED.read_text(encoding='utf8').splitlines():
 row=json.loads(line)
 if row['translation'].strip(): known.add(row['id'])
rows=[]; missing=set()
for line in CANON.read_text(encoding='utf8').splitlines():
 row=json.loads(line); c=row['context']
 if c.get('source_kind')=='map' and c.get('map_id')==31 and c.get('event_id')==7:
  if row['id'] in known: continue
  source=row['source_text'].strip()
  if source in {'…','...','..'} or source.startswith('/'): continue
  target=MAP.get(source)
  if target is None: missing.add(source); continue
  row['translation']=target; rows.append(row)
if missing: raise SystemExit('Unmapped map31 event 7 strings: '+repr(sorted(missing)))
OUT.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf8',newline='\n')
print(f'Wrote map 31 Tasha/Nellie interview: {len(rows)} records from {len(MAP)} strings')
