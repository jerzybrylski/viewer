#!/usr/bin/env python3
"""Build Polish drafts for Map 104 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map104-followups-01.jsonl'
TRANSLATIONS = {
    "That was beautiful, boss.": "To było piękne, szefie.",
    "Yeah. You’re a talented man.": "Tak. Jesteś utalentowanym człowiekiem.",
    "I’ve got a few talents up my sleeve.": "Mam kilka talentów w zanadrzu.",
    "Talented and sexy.": "Utalentowany i seksowny.",
    "Just how much time are we going to kill down here?": "Ile jeszcze czasu będziemy tu zabijać?",
    "We’ve got to wait out the heat, sugarplum.": "Musimy przeczekać gorący okres, kotku.",
    "Stop yer bitchin’, Nel.": "Przestań narzekać, Nel.",
    "At least we got plenty of booze.": "Przynajmniej mamy mnóstwo alkoholu.",
    "We’re getting everything back, boys…": "Odzyskamy wszystko, chłopcy…",
    "The Guild is ours for the taking.": "Gildia jest na wyciągnięcie ręki.",
    "A toast to Helmer! Our fearless leader!": "Toast za Helmera! Naszego nieustraszonego przywódcę!",
    "No, Igor. A toast to Morgan.": "Nie, Igor. Toast za Morgana.",
    "That lowly thief?": "Za tego nędznego złodzieja?",
    "That amulet was worth more money than you, Victor.": "Ten amulet był wart więcej niż ty, Victor.",
    "No… That thief gave us the motivation we needed to take what is rightfully ours.": "Nie… Ten złodziej dał nam motywację, której potrzebowaliśmy, by odebrać to, co słusznie nasze.",
    "And now Wilkes is dead! Good riddance!": "A teraz Wilkes nie żyje! Dobrze mu tak!",
    "Soon, everything that was stolen from me will be back in my possession and the Guild will be led by one man.": "Wkrótce wszystko, co mi skradziono, wróci w moje ręce, a Gildią będzie przewodzić jeden człowiek.",
    "An incredible feat. You’ve killed half of our members somehow.": "Niesamowite osiągnięcie. Jakoś zabiłeś połowę naszych członków.",
    "A weapon fell onto my lap. The purge was necessary. Don’t you agree?": "Broń sama wpadła mi w ręce. Czystka była konieczna. Nie zgadzasz się?",
    "Kill’em all!": "Zabijcie ich wszystkich!",
    "You’ve got what it takes, boss...": "Masz to, szefie...",
    "Sometimes I wonder if Nellie shares our same loyalty.": "Czasem zastanawiam się, czy Nellie podziela naszą lojalność.",
    "What the fuck did you just say?": "Co, kurwa, właśnie powiedziałeś?",
    "Nothing… I was just sayin’...": "Nic… Tak tylko mówiłem…",
    "You keep your god-damn mouth shut or I’ll staple it shut.": "Trzymaj swoją pieprzoną gębę na kłódkę, albo ci ją zszyję.",
    "He’ll do it. I’ve seen it.": "On to zrobi. Widziałem.",
    "Yes, boss. I’m sorry.": "Tak, szefie. Przepraszam.",
    "Enough drinking. I want a cookie.": "Dość picia. Chcę ciastko.",
    "Come on, boss. I made peanut butter cookies.": "No dawaj, szefie. Zrobiłam ciastka z masłem orzechowym.",
    "Oh! My favorite!": "O! Moje ulubione!",
    "You better watch yourself.": "Lepiej uważaj na siebie.",
    "If Duncan is mad, I’m mad.": "Jeśli Duncan jest wkurzony, ja też jestem wkurzony.",
    "Ass kisser.": "Lizus.",
    "Shut up. The both of you.": "Zamknijcie się. Oboje.",
    "I can’t stand it here. I’m going back out.": "Nie wytrzymam tutaj. Wychodzę.",
    "The boss hates it when you leave.": "Szef nie lubi, gdy wychodzisz.",
    "He’ll never stop me.": "Nigdy mnie nie powstrzyma.",
    "Such a bitch.": "Co za suka.",
    "Nellie, shhh!": "Nellie, ciii!",
    "What the fuck are you doing here? What is she doing here?": "Co ty tu, kurwa, robisz? Co ona tu robi?",
    "Calm down, Nellie.": "Uspokój się, Nellie.",
    "I told you to stop following me.": "Mówiłam ci, żebyś przestał za mną łazić.",
    "You dumb fucks. I’m working for Kimura. You aren’t supposed to be here.": "Wy durne chuje. Pracuję dla Kimury. Nie powinno was tu być.",
    "I knew it.": "Wiedziałam.",
    "No one, and I mean no one is supposed to know I’m a mole. You have to get out of here now.": "Nikt, absolutnie nikt nie ma wiedzieć, że jestem kretem. Musicie się stąd wynosić, natychmiast.",
    "You’re in no position to be demanding anything from me, detective.": "Nie jesteś w pozycji, by czegokolwiek ode mnie żądać, detektyw.",
    "If she wasn’t working with us, she’d have already called for help.": "Gdyby z nami nie współpracowała, już dawno wezwałaby pomoc.",
    "If they find out about me, I won’t be the only one losing their head…": "Jeśli się o mnie dowiedzą, nie tylko ja stracę głowę…",
    "There are agents infiltrating the entire Guild… Kimura has an entire team.": "Agenci infiltrowali całą Gildię… Kimura ma cały zespół.",
    "Shit. You aren’t supposed to know. She’s going to flip her lid.": "Cholera. Nie powinnaś tego wiedzieć. Ona oszaleje.",
    "Oh, god. I think I’m going to throw up.": "O Boże. Chyba zwymiotuję.",
    "Shit. Get out of here.": "Cholera. Wynoście się stąd.",
    "Hey! Who the hell is that woman?": "Hej! Kim, do cholery, jest ta kobieta?",
    "None of your business, Daggett.": "To nie twój interes, Daggett.",
    "You better start talking, Nellie.": "Lepiej zacznij gadać, Nellie.",
    "If you must know. She’s my girlfriend… Vanessa.": "Skoro musisz wiedzieć. To moja dziewczyna… Vanessa.",
    "What did she say?": "Co ona powiedziała?",
    "Come on, Vanessa. I want you to meet someone.": "Chodź, Vanessa. Chcę, żebyś kogoś poznała.",
    "Go on. Smooth talk her. She’s drunk.": "No dalej. Zagadaj ją. Jest pijana.",
    "Vanessa, this is Phyliss Daggett. One badass thief.": "Vanessa, to jest Phyliss Daggett. Niezła złodziejka.",
    "You’re damn right I’m a badass.": "Cholernie dobrze, że jestem twardzielką.",
    "Maybe I had you all wrong, Nellie. I thought you were choking down Duncan’s dick.": "Może źle cię oceniłem, Nellie. Myślałem, że obciągasz Duncanowi.",
    "Disgusting.": "Obrzydliwe.",
    "If you’re a muff diver, that changes everything.": "Jeśli jesteś lesbą, to wszystko zmienia.",
    "I love eating pussy. Chicks are my thing. Men… are gross.": "Uwielbiam lizać cipkę. Babki to moja bajka. Faceci… są obrzydliwi.",
    "We don’t owe you a show.": "Nie jesteśmy wam winne przedstawienia.",
    "You’re a lying bitch!": "Kłamliwa suko!",
    "Come on and sit down, Phyliss. You’re going to fall.": "Chodź, usiądź, Phyliss. Przewrócisz się.",
    "Are you saying I’m drunk?": "Mówisz, że jestem pijana?",
    "Relax. Everything is fine.": "Spokojnie. Wszystko jest w porządku.",
    "Bull… fucking… shit.": "Gówno… jebane… gówno.",
    "Kill him…": "Zabijcie go…",
    "Yes, boss.": "Tak, szefie.",
    "And don’t get blood on the carpet. I hate it when you get blood on the carpet.": "I nie pobrudźcie krwią dywanu. Nienawidzę, gdy brudzicie krwią dywan.",
    "Good riddance. That guy gives me the creeps.": "Dobrze, że się go pozbyliśmy. Ten gość przyprawia mnie o gęsią skórkę.",
    "You heard the man. Go get a gun. And make it fast.": "Słyszeliście faceta. Przynieście spluwę. I to szybko.",
    "But the guns are on the other side of the facility. Let’s just choke him out.": "Ale spluwy są po drugiej stronie obiektu. Po prostu go udusimy.",
    "Yeah, do it.": "Tak, zróbcie to.",
    "I’m not doing it. You do it!": "Ja tego nie zrobię. Ty to zrób!",
    "It was your idea!": "To był twój pomysł!",
    "Go… get… the… gun!": "Idźcie… po… broń!",
    "We’ll be back in 8 minutes. Are you okay alone?": "Wrócimy za 8 minut. Poradzisz sobie sam?",
    "I’ll be fine. He’s tied up.": "Dam radę. Jest związany.",
    "Hey. Aim away from the carpet.": "Hej. Celuj z dala od dywanu.",
    "What? Toward the piano? That’ll make him even more mad.": "Co? W stronę pianina? To go jeszcze bardziej wkurzy.",
    "Don’t you know what the hell you’re doing?": "Czy wy w ogóle wiecie, co robicie, do cholery?",
    "If you’re so smart, why don’t you shoot him.": "Skoro jesteś taki mądry, czemu go nie zastrzelisz.",
    "God, damn it…": "Cholera…",
    "Give me the gun.": "Daj mi spluwę.",
    "Don’t worry. I won’t get blood anywhere…": "Nie martw się. Nie pobrudzę krwią nigdzie…",
    "Watch and learn.": "Patrz i ucz się.",
    "Oops! wrong room.": "Ups! Zły pokój.",
    "What are you doing? Go after him!": "Co robisz? Łap go!",
    "First thing’s first.": "Najpierw najważniejsze.",
    "The gun’s jammed.": "Spluwa się zacięła.",
    "Huh? How do you know that?": "Co? Skąd wiesz?",
    "Give me the damn gun.": "Daj mi tę cholerną spluwę.",
    "It’s jammed?": "Zacięła się?",
    "Yeah. Take a look.": "Tak. Zobacz sam.",
    "They’ll kill you!": "Zabiją cię!",
    "Take it…": "Weź to…",
    "I’ll tell them you’re some sort of Houdini.": "Powiem im, że jesteś jakimś Houdinim.",
    "I’ve got a story to tell…": "Mam historię do opowiedzenia…",
    "Duncan will buy it. Trust me.": "Duncan to kupi. Zaufaj mi.",
    "Good luck, Nellie.": "Powodzenia, Nellie.",
    "I need to get the hell away from here.": "Muszę się stąd, kurwa, wydostać.",
    "Shit… Did they really take my amulet?": "Cholera… Naprawdę zabrali mój amulet?",
    "It’s gone.": "Nie ma go.",
    "What the hell took you so long?": "Co cię, do cholery, tak długo zatrzymało?",
    "I had to be sure I did it right.": "Musiałam się upewnić, że zrobiłam to dobrze.",
    "You all have caused enough trouble. You have to get out of here.": "Narobiliście już dość kłopotów. Musicie się stąd wynosić.",
    "What about the drunk lady? She’s going to wake up soon.": "A co z pijaną babką? Wkrótce się obudzi.",
    "She’ll forget everything. She’s a drunk.": "Zapomni wszystko. Jest pijana.",
    "If you’re lying…": "Jeśli kłamiesz…",
    "Stay away from me. You’re going to blow my cover.": "Trzymaj się ode mnie z daleka. Zdekonspirujesz mnie.",
    "Don’t let Kimura know you saw me.": "Nie daj poznać Kimurze, że mnie widziałaś.",
    "Somehow I think that is out of my hands at this point.": "Jakoś myślę, że to już nie w moich rękach.",
}
known=set()
for p in (ROOT/'drafts').rglob('*.jsonl'):
    for line in p.read_text(encoding='utf-8').splitlines():
        if line.strip():
            r=json.loads(line)
            if r.get('translation','').strip(): known.add(r['id'])
rows=[]
unmapped=set()
for line in CANON.read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    r=json.loads(line)
    ctx=r.get('context') or {}
    src=' '.join(r.get('source_text','').strip().split())
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=104 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=translations.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=117: raise SystemExit(f'Expected 117, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map104')