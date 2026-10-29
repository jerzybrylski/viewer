import json
from pathlib import Path
ROOT=Path('games/the-genesis-order/translation')
CANON=ROOT/'export-v1/custom_dialogue.jsonl'
MERGED=Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step2.jsonl')
DRAFTS=ROOT/'drafts'
MAPS={
98:{
'Father Solomon, how are you holding up?':'Ojcze Solomonie, jak się trzymasz?',
'Nothing out of the ordinary. Have you spoken with the commissioner?':'Nic nadzwyczajnego. Rozmawiałeś z panią komisarz?',
'She’s heading here to meet with you personally.':'Jedzie tutaj, żeby spotkać się z tobą osobiście.',
'I’ll speak with her this morning and let you know the plan.':'Porozmawiam z nią rano i przedstawię ci plan.',
'Being in such close proximity to a mansion full of thieves makes me very uncomfortable…':'Bardzo mi nie odpowiada bliskość rezydencji pełnej złodziei…',
'But what really worries me is not having a full grasp on what Lillian wants.':'Najbardziej martwi mnie jednak to, że nie wiem, czego chce Lillian.',
'Madalyn too… She thinks Sister Judy is trying to stop her.':'Madalyn również… Uważa, że siostra Judy próbuje ją powstrzymać.',
'A virgin servant of the Lord can be quite frightening to a woman like that.':'Dziewica służąca Panu może być dla takiej kobiety całkiem przerażająca.',
'The police can’t help us against the powers of evil… We need to take matters into our own hands.':'Policja nie pomoże nam w walce z siłami zła… Musimy sami wziąć sprawy w swoje ręce.',
'How do we do that?':'Jak to zrobimy?',
'We arm this place to the teeth.':'Uzbroimy to miejsce po zęby.',
'Guns?':'Broń palna?',
'Crucifixes and holy water.':'Krucyfiksy i woda święcona.',
'Oh, yeah. That makes more sense.':'Aha. To ma więcej sensu.',
'Can you help me out?':'Możesz mi pomóc?',
'What do you need?':'Czego potrzebujesz?',
'Find me some crucifixes.':'Znajdź kilka krucyfiksów.',
'How many?':'Ile?',
'Enough so no demon can enter here without seeing one… Let’s call it five.':'Tyle, żeby żaden demon nie wszedł tu bez zobaczenia jednego… Powiedzmy, że pięć.',
'Okay… Five crucifixes.':'Dobrze… Pięć krucyfiksów.',
'And a good amount of holy water.':'I sporo wody święconej.',
'I’ll be in the library, studying. Bring them to me when you have them…':'Będę w bibliotece i będę się uczyć. Przynieś je, gdy już je zdobędziesz…',
'There may be some in storage. But if not, you may have to get creative.':'Kilka może być w schowku. Jeśli nie, trzeba będzie wykazać się pomysłowością.',
'Got it.':'Jasne.',
},
129:{
'Who the hell is calling me from work at this hour?':'Kto, do cholery, dzwoni do mnie z pracy o tej porze?',
'1Hero! There’s a giant glowing door in the basement of the Wilkes’ mansion!':'1Hero! W piwnicy rezydencji Wilkesów pojawiły się wielkie, świecące drzwi!',
'I told you. What did you see?':'A nie mówiłem? Co widziałaś?',
'I don’t know what happened, but some creepy-looking dudes walked into it and now it’s gone.':'Nie wiem, co się stało, ale weszło w nie kilku podejrzanych typów, a teraz drzwi zniknęły.',
'Another thing… Kimberly Foxx is here and she has a girlfriend with her.':'Jeszcze jedno… Jest tu Kimberly Foxx ze swoją dziewczyną.',
'What are you saying? Where are they?':'Co ty mówisz? Gdzie są?',
'Standing in the middle of the room! I swear there was no one there mere seconds ago!':'Stoją na środku pokoju! Przysięgam, że jeszcze chwilę temu nikogo tam nie było!',
'Get them! Don’t let them leave the mansion.':'Złapcie je! Nie pozwólcie im opuścić rezydencji.',
'But the monsters…':'Ale te potwory…',
'If the portal isn’t glowing, you’re safe… Now hurry up… Bring them to a room in the mansion and don’t let them out of your sight.':'Jeśli portal nie świeci, jesteś bezpieczny… Pospiesz się… Zaprowadź je do pokoju w rezydencji i nie spuszczaj z nich wzroku.',
'Is this some sort of trap? Why would Lillian leave the girls alone?':'To jakaś pułapka? Czemu Lillian zostawiłaby dziewczyny same?',
},
76:{
'I can’t wait to kick some ass.':'Nie mogę się doczekać, aż komuś przyłożę.',
'Nice of you to join us, 1Hero.':'Miło, że do nas dołączyłeś, 1Hero.',
'Any activity last night?':'Coś się działo w nocy?',
'It’s been quiet without Judy around. But it does seem attendance is up a bit.':'Bez Judy było spokojnie. Ale chyba frekwencja trochę wzrosła.',
'This is busy?':'To jest tłum?',
'Busier than usual…':'Większy niż zwykle…',
'I better get going. Thanks for stopping by to protect us.':'Lepiej już pójdę. Dzięki, że wpadłeś nas chronić.',
'Don’t mention it.':'Nie ma za co.',
'1Hero! You made it.':'1Hero! Udało ci się przyjść.',
'Where’s Hannah?':'Gdzie jest Hannah?',
'Not sure if she’s going to make it. She was still in her underwear when I left.':'Nie wiem, czy przyjdzie. Kiedy wychodziłam, wciąż była w samej bieliźnie.',
'Mass is starting soon.':'Zaraz zacznie się msza.',
},
67:{
'1Hero!? What’s going on?':'1Hero!? Co się dzieje?',
'Shit… A detective.':'Cholera… Detektyw.',
'Andrea would kill me if she knew, but we’re going back to the mansion to save Kimberly.':'Andrea by mnie zabiła, gdyby się dowiedziała, ale wracamy do rezydencji ratować Kimberly.',
'Why bring Guild thieves?':'Po co przyprowadzać złodziei z Gildii?',
'He’s better off with us than any dimwit on your force.':'Lepiej, żeby był z nami, niż z jakimkolwiek idiotą z twojego posterunku.',
'You will protect us, Miss Bhatt?':'Będzie nas pani chronić, panno Bhatt?',
'Apparently.':'Najwyraźniej.',
'Come on. Duncan’s waiting. We have to go.':'Chodź. Duncan czeka. Musimy ruszać.',
'You owe me an explanation, 1Hero.':'Jesteś mi winien wyjaśnienie, 1Hero.',
'I’ll tell you everything later.':'Później wszystko ci opowiem.',
'I’ll sneak everyone into the basement… 1Hero, I’ll meet you there and bring you to Duncan.':'Przemycę wszystkich do piwnicy… 1Hero, spotkam się tam z tobą i zaprowadzę cię do Duncana.',
'Be careful.':'Uważaj na siebie.',
'Nice to see you again, Miss Bhatt.':'Miło panią znów widzieć, panno Bhatt.',
'Would you like a tour of the church?':'Może oprowadzę panią po kościele?',
'I’ve seen it.':'Już go widziałam.',
'Come on. Let’s go back to the library.':'Chodźmy. Wracamy do biblioteki.',
'Yes. We must study.':'Tak. Musimy się uczyć.',
'Don’t let them out of your sight. There’s a cult looking to kidnap Erica… and they probably know she’s here.':'Nie spuszczaj ich z oczu. Sekta chce porwać Ericę… i pewnie wie, że tu jest.',
'I don’t like the sound of that.':'Nie podoba mi się to.',
'Good thing you’re a capable woman.':'Dobrze, że jesteś zaradną kobietą.',
},
55:{
'Looks like the weather is letting up. I’m heading home.':'Wygląda na to, że pogoda się poprawia. Wracam do domu.',
'How are we going to get into the safe?':'Jak otworzymy sejf?',
'We have people at the station that can handle that sort of thing.':'Na posterunku są ludzie, którzy się tym zajmą.',
'But there could be a code laying around. We could at least look.':'Ale gdzieś może leżeć kod. Możemy przynajmniej poszukać.',
'Feel free to try.':'Spróbujcie.',
'Thank you, Father Solomon, for letting us search for Zephaniah’s belongings.':'Dziękuję, ojcze Solomonie, że pozwolił nam pan szukać rzeczy Zephaniaha.',
'I’ll admit Madalyn scares me. I wish I knew what she wanted.':'Przyznam, że Madalyn mnie przeraża. Chciałabym wiedzieć, czego chce.',
'I can see about having some officers posted outside.':'Mogę postarać się o posterunek policji przed budynkiem.',
'Can you do that?':'Możesz to załatwić?',
'We’ll have to show there is a possible danger…':'Musimy wykazać, że istnieje zagrożenie…',
'Let’s wait and see what’s in that safe.':'Poczekajmy i zobaczmy, co jest w sejfie.',
'Thanks, detective.':'Dziękuję, pani detektyw.',
'Come on, Sister Judy. I’m excited to show you my place.':'Chodź, siostro Judy. Nie mogę się doczekać, aż pokażę ci mój dom.',
'It will be exciting to spend a night away.':'To będzie ekscytujące spędzić noc poza domem.',
'Just bring her back in one piece.':'Tylko przyprowadź ją z powrotem całą i zdrową.',
'Will do, Father.':'Oczywiście, ojcze.',
'Haha. You are so funny, Father Solomon.':'Haha. Jest ojciec bardzo zabawny, ojcze Solomonie.',
'Are you coming, 1Hero?':'Idziesz, 1Hero?',
'I’ll stop by.':'Wpadnę później.',
'Thank you, 1Hero.':'Dziękuję, 1Hero.',
'If there was anything left behind from Father Zephaniah’s time here, it would now be in the attic.':'Jeśli zostało tu coś po ojcu Zephaniahu, teraz powinno być na strychu.',
'Mind if I take a look?':'Mogę się rozejrzeć?',
'The doors are open, 1Hero.':'Drzwi są otwarte, 1Hero.',
'Thanks, Brian.':'Dzięki, Brian.',
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
