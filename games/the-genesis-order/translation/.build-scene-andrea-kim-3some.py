import json
from pathlib import Path
ROOT=Path('games/the-genesis-order/translation')
CANON=ROOT/'export-v1/custom_dialogue.jsonl'
MERGED=Path('google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step2.jsonl')
OUT=ROOT/'drafts/custom-dialogue-scene-andrea-kim-3some-01.jsonl'
if OUT.exists(): raise SystemExit(f'Refusing to overwrite {OUT}')
MAP={
'You’re running late.':'Spóźniasz się.',
'Commissioner!?':'Pani komisarz!?',
'Andrea! We were just changing.':'Andrea! Właśnie się przebierałyśmy.',
'Changing in front of each other? Perhaps something is blossoming between you two.':'Przebieracie się przy sobie? Może coś zaczyna się między wami rozwijać.',
'Well, uhh…':'No cóż…',
'We’re strictly professional… We were just saving time.':'Łączą nas wyłącznie sprawy zawodowe… Po prostu oszczędzałyśmy czas.',
'I’m not stupid, Miss Foxx…':'Nie jestem głupia, panno Foxx…',
'In fact, I’m jealous.':'Właściwie to zazdroszczę.',
'Uhh… Of who?':'Eee… Komu?',
'You get this lovely news anchor all to yourself, Mr. Canmore.':'Pan ma tę uroczą prezenterkę tylko dla siebie, panie Canmore.',
'Of course, we won’t tell anybody about this.':'Oczywiście nikomu o tym nie powiemy.',
'Oh, yes. I trust the both of you.':'O tak. Ufam wam obojgu.',
'I didn’t expect you so early, Miss Kimura.':'Nie spodziewałam się pani tak wcześnie, panno Kimura.',
'Well, now that I’m here…':'Cóż, skoro już tu jestem…',
'Why don’t we make things a little more… complicated.':'Może trochę… skomplikujemy sytuację.',
'Andrea?':'Andrea?',
'Are you serious?':'Mówisz poważnie?',
'Ever since I caught the both of you getting down and dirty in my dining room, the thought of you two fucking hasn’t left my mind.':'Odkąd przyłapałam was na igraszkach w mojej jadalni, nie mogę przestać myśleć o tym, jak się pieprzycie.',
'I don’t know what came over me.':'Nie wiem, co we mnie wstąpiło.',
'No need to apologize. I’m glad I caught you.':'Nie musisz przepraszać. Cieszę się, że was przyłapałam.',
'You’re going to give me the scoop?':'Dasz mi newsa?',
'What has 1Hero told you?':'Co powiedział ci 1Hero?',
'Once you catch the Guild stealing the stolen Rembrandt, you’ll let us have the story.':'Kiedy przyłapiecie Gildię na kradzieży skradzionego Rembrandta, pozwolisz nam opisać tę historię.',
'It depends.':'To zależy.',
'On what?':'Od czego?',
'Why don’t you get on your knees and ask nicely.':'Może uklękniesz i ładnie poprosisz.',
'What can I say, Kimberly. I think we’re going to have to sweeten the deal.':'Co mogę powiedzieć, Kimberly? Chyba musimy nieco uatrakcyjnić tę ofertę.',
'Are we?':'Naprawdę?',
'You’ll get the scoop.':'Dostaniesz tego newsa.',
'What was stolen?':'Co skradziono?',
'Something worth over ten million.':'Coś wartego ponad dziesięć milionów.',
'Seriously?':'Poważnie?',
'Damn. I didn’t even know that.':'Cholera. Nawet o tym nie wiedziałam.',
'Imagine being the one to break that story.':'Wyobraź sobie, że to ty pierwsza podajesz tę wiadomość.',
'Well then… I better make it worth your effort.':'W takim razie… Lepiej wynagrodzę twój wysiłek.',
'Oh, yes! Miss Foxx! You’re so naughty.':'Och, tak! Panno Foxx! Ale z pani niegrzeczna dziewczynka.',
'That’s it baby. Give the commissioner what she needs.':'Właśnie tak, kochanie. Daj pani komisarz to, czego potrzebuje.',
'I should have expected such wonderful tongue work from the voice of a network.':'Po głosie gwiazdy telewizji można się było spodziewać tak wprawnego języka.',
'Her pussy is very tight.':'Jej cipka jest bardzo ciasna.',
'I bet she loves every inch of it.':'Założę się, że uwielbia każdy centymetr.',
'She’s so wet!':'Ale mokra!',
'How does that taste, my dear?':'Jak ci smakuje, kochanie?',
'Enjoying the warm, juicy flavor of my dripping wet pussy?':'Smakuje ci moja ciepła, soczysta i ociekająca sokami cipka?',
'Andrea… I never took you for such a naughty woman.':'Andrea… Nie sądziłam, że jesteś taką niegrzeczną kobietą.',
'I know what I want, and you’re giving it to me.':'Wiem, czego chcę, a ty mi to dajesz.',
'It seems both Detective Canmore and myself are getting more than expected from this relationship.':'Wygląda na to, że zarówno detektyw Canmore, jak i ja, dostajemy z tej relacji więcej, niż się spodziewaliśmy.',
'He’s drilling me so deep!':'Ale głęboko mnie pieprzy!',
'I want to feel your pussy.':'Chcę poczuć twoją cipkę.',
'Please, Andrea. Take what you want.':'Proszę, Andrea. Bierz, co chcesz.',
'Ah! Oh, my!':'Ach! Ojej!',
'Soaked… I love it.':'Cała mokra… Uwielbiam to.',
'Isn’t she warm, Miss Kimura.':'Czyż nie jest ciepła, panno Kimura?',
'Very.':'Bardzo.',
'You’ve really got us going, Miss Foxx. Are we going to be late?':'Nieźle nas pani rozgrzała, panno Foxx. Spóźnimy się?',
'No… It’s okay. Keep going.':'Nie… W porządku. Nie przestawaj.',
'You ladies are so sexy together.':'Ależ jesteście razem seksowne.',
'Fuck. I’m so horny.':'Kurwa. Ale jestem napalony.',
'And clearly, 1Hero is wanting for more.':'I wyraźnie 1Hero ma ochotę na więcej.',
'Oh, uhh… I’d love to.':'Och, eee… Z przyjemnością.',
'Ah! My cock!...':'Ach! Mój kutas!...',
'Careful!':'Uważaj!',
'Go on, 1Hero. Give the woman your big fat cock.':'No dalej, 1Hero. Daj tej kobiecie swojego wielkiego kutasa.',
'I’m going to sit on your face, dear. You’re going to get me off.':'Usiądę ci na twarzy, kochanie. Doprowadzisz mnie do orgazmu.',
'Go on, Kimberly. We’re in this together.':'No dalej, Kimberly. Jesteśmy w tym razem.',
'Damn, you two are kinky.':'Cholera, ale z was perwersyjna para.',
'Oh, fuck me! That’s good!':'O kurwa, pieprz mnie! Ale dobrze!',
'Yes! What a pussy!':'Tak! Co za cipka!',
'I’ve always dreamed of sitting on this perfect face.':'Zawsze marzyłam, żeby usiąść na tej pięknej twarzy.',
'Kimberly Foxx’s face… pressed against my crotch… it’s overwhelming!':'Twarz Kimberly Foxx… przyciśnięta do mojego krocza… To zbyt wiele!',
'Eat that pussy, Kim.':'Liż tę cipkę, Kim.',
'Come on, Canmore. Give it to her!':'No dalej, Canmore. Dawaj!',
'Yes, Andrea!':'Tak, Andrea!',
'You like my tits, 1Hero?':'Podobają ci się moje cycki, 1Hero?',
'So good.':'Ale dobrze.',
'Fuck her like you mean it, 1Hero.':'Pieprz ją porządnie, 1Hero.',
'Fuck! This is good!':'Kurwa! Ale dobrze!',
'Eat it, Kimberly! Drink my pussy!':'Liż, Kimberly! Spijaj moje soki!',
'Damn! So hot!':'Cholera! Ale gorąco!',
'I’m going to squirt all over her face.':'Zaraz trysnę jej na twarz.',
'Damn, Andrea… It’s so hot… I’m…':'Cholera, Andrea… Ale gorąco… Ja…',
'I’m going to cum!':'Zaraz dojdę!',
'Impressive load, 1Hero.':'Niezły wytrysk, 1Hero.',
'It’s not the first time I’ve had the pleasure.':'To nie pierwszy raz, kiedy mam tę przyjemność.',
'That was incredible, ladies.':'To było niesamowite, panie.',
'Now… Let’s not keep Paul waiting. You have an interview to conduct, young man.':'A teraz… Nie każmy Paulowi czekać. Młody człowieku, masz do przeprowadzenia wywiad.',
'Come on. Let’s get cleaned up.':'No chodźcie. Ogarnijmy się.',
}
known=set()
for line in MERGED.read_text(encoding='utf8').splitlines():
 row=json.loads(line)
 if row['translation'].strip(): known.add(row['id'])
rows=[]; missing=set()
for line in CANON.read_text(encoding='utf8').splitlines():
 row=json.loads(line); c=row['context']
 if c.get('source_kind')=='common_event' and c.get('event_id')==386:
  if row['id'] in known: continue
  source=row['source_text'].strip()
  if source in {'…','...','..'} or source.startswith('/'): continue
  target=MAP.get(source)
  if target is None: missing.add(source); continue
  row['translation']=target; rows.append(row)
if missing: raise SystemExit('Unmapped event 386 strings: '+repr(sorted(missing)))
OUT.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf8',newline='\n')
print(f'Wrote Andrea/Kim/Canmore scene: {len(rows)} records from {len(MAP)} source strings')
