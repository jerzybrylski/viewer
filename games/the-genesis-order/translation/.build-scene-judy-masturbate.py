import json
from pathlib import Path
ROOT=Path('games/the-genesis-order/translation')
CANON=ROOT/'export-v1/custom_dialogue.jsonl'
MERGED=Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step2.jsonl')
OUT=ROOT/'drafts/custom-dialogue-scene-judy-masturbate-01.jsonl'
if OUT.exists(): raise SystemExit(f'Refusing to overwrite {OUT}')
MAP={
'Oh! Look at you.':'Och! Popatrz na siebie.',
'Uhh… Just watering the plant, Sister.':'Eee… Podlewam tylko roślinę, siostro.',
'Mmm. You are so big and strong.':'Mmm. Jesteś taki duży i silny.',
'Well, hello there, Sister Judy.':'Witaj, siostro Judy.',
'Thank you so much! You are my hero!':'Bardzo ci dziękuję! Jesteś moim bohaterem!',
"Okay, okay! I get it. You're starting to freak me out.":'Dobrze, dobrze! Rozumiem. Zaczynasz mnie przerażać.',
"It's so good to have such a loving man in my life.":'Jak dobrze mieć w życiu tak kochającego mężczyznę.',
'Uhh. Thanks, Judy.':'Eee… Dzięki, Judy.',
'Ever since you arrived at our church, I have been deep in thought.':'Odkąd przybyłeś do naszego kościoła, dużo rozmyślam.',
'What have you been thinking about, Sister Judy?':'O czym rozmyślałaś, siostro Judy?',
'You may not suspect it, but in my youth, I was in a relationship with a young man.':'Może cię to zdziwić, ale w młodości byłam związana z pewnym młodzieńcem.',
'Really?':'Naprawdę?',
'I very much enjoyed his company. He was like a best friend to me.':'Bardzo lubiłam jego towarzystwo. Był dla mnie jak najlepszy przyjaciel.',
'I wanted to spend all day with him.':'Chciałam spędzać z nim całe dnie.',
'Sounds like you had quite a fling going.':'Brzmi, jakby łączył was niezły romans.',
'It was a wonderful time. But…':'To był wspaniały czas. Ale…',
'It didn’t work out. Or more like, it couldn’t.':'Nie wyszło nam. A raczej nie mogło się udać.',
'I don’t understand.':'Nie rozumiem.',
'No matter how much I wanted to, I just couldn’t feel anything… romantic for him.':'Choć bardzo tego chciałam, nie potrafiłam poczuć do niego nic… romantycznego.',
'When I told him… he was heartbroken.':'Kiedy mu o tym powiedziałam… złamałam mu serce.',
'Maybe he just wasn’t the right one?':'Może po prostu nie był tym właściwym?',
'No, that wasn’t it… It’s something deeper… Something inside of me…':'Nie, nie o to chodziło… To coś głębszego… Coś we mnie…',
'I couldn’t feel any real romantic interest for anyone.':'Nie potrafiłam poczuć prawdziwego romantycznego zainteresowania nikim.',
'At all? That sounds strange.':'W ogóle? To brzmi dziwnie.',
'I know. But that’s how it was.':'Wiem. Ale tak właśnie było.',
'So the church seemed like a natural path for me.':'Dlatego kościół wydał mi się naturalną drogą.',
'For a while, it was fine.':'Przez jakiś czas było dobrze.',
'Something changed?':'Coś się zmieniło?',
'Yes. Until earlier today in the forest, I could say I was content with my lot in life.':'Tak. Jeszcze dziś, przed tym, co wydarzyło się w lesie, mogłam powiedzieć, że jestem zadowolona ze swojego życia.',
'What Mother Superior did to me, how it made me feel…':'To, co zrobiła mi matka przełożona, i to, jak się przez to poczułam…',
'I don’t know what to say.':'Nie wiem, co powiedzieć.',
'It’s like something has opened up in me that I never knew was there.':'Jakby otworzyło się we mnie coś, o czego istnieniu nie miałam pojęcia.',
'Sexual thoughts…':'Myśli o seksie…',
'It worries me. Now that I’m in service to God, I shouldn’t be having these sinful feelings.':'Niepokoi mnie to. Służę Bogu, więc nie powinnam mieć takich grzesznych pragnień.',
"I can't fulfill these desires, 1Hero. But I feel a strong urge that was absent before.":'Nie mogę spełniać tych pragnień, 1Hero. Ale czuję silną potrzebę, której wcześniej nie było.',
"You've gone your whole life without feeling sexual desire...":'Przez całe życie nie odczuwałaś pożądania…',
'But those feelings are normal.':'Ale takie uczucia są normalne.',
'Not for a nun.':'Nie dla zakonnicy.',
"There's something you can do that will help.":'Jest coś, co może ci pomóc.',
'What is it, 1Hero?':'Co takiego, 1Hero?',
'You have to touch yourself... down there.':'Musisz się dotknąć… tam na dole.',
'Oh, 1Hero… I... I feel the desire, but I am resisting.':'Och, 1Hero… Ja… Czuję pożądanie, ale próbuję mu się oprzeć.',
'If you want to feel better, you have to take care of yourself.':'Jeśli chcesz poczuć się lepiej, musisz sama o siebie zadbać.',
'But...':'Ale…',
'Touching yourself isn’t sex. It’s a perfectly acceptable way to deal with your urges.':'Dotykanie samej siebie to nie seks. To zupełnie dobry sposób na rozładowanie napięcia.',
'With a little practice, you’ll be able to manage your urges easily.':'Trochę poćwiczysz, a łatwiej zapanujesz nad swoimi pragnieniami.',
'You think so? I’m not sure. I don’t really know how to do it.':'Tak myślisz? Nie wiem. Nie bardzo wiem, jak to robić.',
'1Hero?':'1Hero?',
"It's okay, Judy. I'm going to help you.":'W porządku, Judy. Pomogę ci.',
'Oh, my...':'Ojej…',
'Do you trust me?':'Ufasz mi?',
'I... I do.':'Ja… Tak.',
"I won't hurt you. I promise.":'Nie skrzywdzę cię. Obiecuję.',
'1Hero! That’s my…':'1Hero! To moja…',
'Just relax. I’m going to stimulate your clit.':'Rozluźnij się. Będę stymulował twoją łechtaczkę.',
'My… clit? This is all so strange for me.':'Moją… łechtaczkę? To wszystko jest dla mnie takie dziwne.',
'I don’t know if this is really alright.':'Nie wiem, czy to naprawdę w porządku.',
'Oooo…1Hero.':'Oooo… 1Hero.',
'Are you ready for more?':'Jesteś gotowa na więcej?',
'I don’t know if I can take more.':'Nie wiem, czy zniosę więcej.',
'Sister Judy, to make the thoughts go away, you have to go all the way.':'Siostro Judy, żeby pozbyć się tych myśli, musisz doprowadzić to do końca.',
'All the way? What do you mean?':'Do końca? Co masz na myśli?',
'You have to finish. Then all the sinful thoughts will go away.':'Musisz dojść. Wtedy wszystkie grzeszne myśli znikną.',
'Finish?':'Dojść?',
'Let me show you.':'Pozwól, że ci pokażę.',
'Wooow… It’s so intense!':'Łaaał… To takie intensywne!',
'Would you like me to ease up?':'Mam zwolnić?',
'No! Keep going!':'Nie! Nie przestawaj!',
'Oh my, it feels good!':'Ojej, ale przyjemnie!',
'That’s it, Judy. Don’t fight it.':'Właśnie tak, Judy. Nie opieraj się.',
"Your finger... it's inside of me!":'Twój palec… Jest we mnie!',
'You’re so wet now, Judy. My finger is soaked.':'Jesteś już taka mokra, Judy. Mam cały palec mokry.',
'Something’s happening!':'Coś się dzieje!',
'Ooooooo…':'Ooooooo…',
'What just happened?':'Co się stało?',
'That feeling… What was it?':'To uczucie… Co to było?',
'You came, Judy. That’s what is supposed to happen.':'Doszłaś, Judy. Właśnie to miało się stać.',
'Your urge for sex should be gone. At least for now.':'Powinnaś już nie odczuwać takiej potrzeby seksu. Przynajmniej na razie.',
'You’re right! I don’t feel it so strongly now. Thanks be to God!':'Masz rację! Teraz już nie czuję tego tak mocno. Dzięki Bogu!',
'And thank you, 1Hero.':'I dziękuję tobie, 1Hero.',
'But was this really okay?':'Ale czy to naprawdę było w porządku?',
'Didn’t you like it?':'Nie podobało ci się?',
'I did…':'Podobało…',
'Maybe I shouldn’t.':'Może nie powinnam.',
'It’s normal to touch yourself, Sister Judy.':'To normalne, że się dotykasz, siostro Judy.',
'These desires are sinful though…':'Ale te pragnienia są grzeszne…',
'I shouldn’t be having them.':'Nie powinnam ich odczuwać.',
'You’re just feeling what everyone else does. It’s not bad.':'Po prostu czujesz to, co wszyscy. To nic złego.',
'If you don’t take care of them, then those thoughts will never go away.':'Jeśli sobie z nimi nie poradzisz, te myśli nigdy nie znikną.',
'This is a scary side of myself that I never knew existed. But…':'To przerażająca strona mnie, o której istnieniu nie wiedziałam. Ale…',
'I’m glad you were here to help me, 1Hero.':'Cieszę się, że byłeś tu, żeby mi pomóc, 1Hero.',
'1Hero…':'1Hero…',
'I’ve never been kissed like that before.':'Nigdy wcześniej nikt mnie tak nie całował.',
'I’m sorry, Sister Judy. I just got caught up in the moment.':'Przepraszam, siostro Judy. Po prostu poniosła mnie chwila.',
'It’s okay. You are a good friend…':'Nic nie szkodzi. Jesteś dobrym przyjacielem…',
'But I am still a nun, 1Hero.':'Ale wciąż jestem zakonnicą, 1Hero.',
'I understand.':'Rozumiem.',
}
known=set()
for line in MERGED.read_text(encoding='utf8').splitlines():
 row=json.loads(line)
 if row['translation'].strip(): known.add(row['id'])
rows=[]; missing=set()
for line in CANON.read_text(encoding='utf8').splitlines():
 row=json.loads(line); c=row['context']
 if c.get('source_kind')=='common_event' and c.get('event_id')==347:
  if row['id'] in known: continue
  source=row['source_text'].strip()
  if source in {'…','...','..'} or source.startswith('/'): continue
  target=MAP.get(source)
  if target is None: missing.add(source); continue
  row['translation']=target; rows.append(row)
if missing: raise SystemExit('Unmapped event 347 strings: '+repr(sorted(missing)))
OUT.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf8',newline='\n')
print(f'Wrote Judy self-exploration dialogue: {len(rows)} records from {len(MAP)} source strings')
