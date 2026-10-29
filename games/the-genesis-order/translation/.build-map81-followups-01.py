#!/usr/bin/env python3
"""Build Polish drafts for Map 81 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map81-followups-01.jsonl'
TRANSLATIONS = {
    "I’m too scared to fire the receptionist at Channel 4. But she leaves junk everywhere!": "Boję się zwolnić recepcjonistkę z Channel 4. Ale wszędzie zostawia śmieci!",
    "Box up 4 bags of junk that she’s left inside the Channel 4 building, tell her to leave and I’ll give you a reward.": "Spakuj 4 torby śmieci, które zostawiła w budynku Channel 4, każ jej odejść, a dam ci nagrodę.",
    "The receptionist jumped out of the window.": "Recepcjonistka wyskoczyła przez okno.",
    "Thanks for doing my dirty work. What would you like as a reward?": "Dzięki za odwalenie brudnej roboty. Jaką chciałbyś nagrodę?",
    "Thanks for doing my dirty work.": "Dzięki za odwalenie brudnej roboty.",
    "There she is!...": "Tam jest!...",
    "She’s talking to Erica.": "Rozmawia z Ericą.",
    "Huh? Where are they going?": "Huh? Dokąd idą?",
    "Paul! I saw Kimberly.": "Paul! Widziałam Kimberly.",
    "She left the building just moments ago.": "Wyszła z budynku zaledwie chwilę temu.",
    "Come on! Let’s find her.": "Chodź! Znajdźmy ją.",
    "I’m Detective Canmore. I’m here for the interview.": "Jestem detektyw Canmore. Przyszedłem na wywiad.",
    "Ah, yes. Detective. The commissioner arrived moments ago.": "Ach, tak. Detektywie. Pani komisarz przybyła chwilę temu.",
    "The segment will be taping soon. Come with me.": "Segment będzie nagrywany wkrótce. Chodź ze mną.",
    "He’s here. We’re coming up.": "On tu jest. Już idziemy na górę.",
    "Miss Foxx is waiting for you upstairs.": "Panna Foxx czeka na pana na górze.",
    "If you don’t have an appointment I can’t just let you up.": "Jeśli nie ma pan wizyty, nie mogę pana wpuścić na górę.",
    "I need to speak to him now!": "Muszę z nim teraz porozmawiać!",
    "Miss Kimura. I’m sorry I didn’t come to you earlier, but…": "Panno Kimura. Przepraszam, że nie przyszedłem wcześniej, ale…",
    "We’re going to clear this up with Paul and then there will be absolutely no one else allowed near that mansion apart from those I authorize.": "Wyjaśnimy to z Paulem, a potem nikomu poza upoważnionymi przeze mnie nie będzie wolno zbliżać się do rezydencji.",
    "Are we going to bring in more security? Lillian’s not going to like that.": "Czy zamierzamy sprowadzić więcej ochrony? Lillian to się nie spodoba.",
    "That won't be necessary. I have a different plan.": "To nie będzie konieczne. Mam inny plan.",
    "What’s all this about?": "O co tu chodzi?",
    "Are you kidding me? Interfering with our efforts to find the thieves responsible for breaking into the Wilkes mansion?": "Żartujesz sobie? Przeszkadzasz nam w odnalezieniu złodziei odpowiedzialnych za włamanie do rezydencji Wilkesów?",
    "That’s not what I was doing.": "Nie to robiłem.",
    "What exactly do you expect to find? If you want to know something about the mansion, come to us.": "Czego dokładnie spodziewasz się znaleźć? Jeśli chcesz się czegoś dowiedzieć o rezydencji, przyjdź do nas.",
    "No offense, Commissioner, but you know as well as I do that’s not how it works.": "Bez urazy, pani komisarz, ale pani wie równie dobrze jak ja, że tak to nie działa.",
    "I’ve cooperated with your organization. Do you not trust me?": "Współpracowałem z waszą organizacją. Nie ufa mi pani?",
    "What the hell did you do, Paul?": "Co ty, do cholery, zrobiłeś, Paul?",
    "He was caught snooping around the mansion at night.": "Został przyłapany na szpiegowaniu wokół rezydencji w nocy.",
    "There are officers posted there, looking for thieves. You could have been shot.": "Są tam posterunki, szukają złodziei. Mogłeś zostać zastrzelony.",
    "They are looking for thieves? In Wilkes’ back yard?": "Szukają złodziei? Na podwórku Wilkesów?",
    "Are you suggesting we’re hiding something from you?": "Sugerujesz, że coś przed tobą ukrywamy?",
    "Only one way to be sure.": "Tylko jeden sposób, by się upewnić.",
    "Miss Kimura has been nothing but helpful to us in the past.": "Panna Kimura zawsze była dla nas bardzo pomocna.",
    "The public has a right to know what’s happening. The Guild operates here in North Santiva.": "Społeczeństwo ma prawo wiedzieć, co się dzieje. Gildia działa tu, w North Santiva.",
    "Is that what you want to hear? That the thieves are connected to the Eclipse Guild?": "To chcesz usłyszeć? Że złodzieje są powiązani z Gildią Zaćmienia?",
    "Is it true?": "Czy to prawda?",
    "You run a news segment on Sunday.": "Prowadzisz segment informacyjny w niedzielę.",
    "Meet Canmore and I here tonight. We’ll give you everything we know.": "Spotkaj się z Canmorem i ze mną tu dziś wieczorem. Przekażemy ci wszystko, co wiemy.",
    "A very generous offer.": "Bardzo hojna oferta.",
    "What’s in it for you?": "Co wy na tym zyskacie?",
    "In return, you stay the hell away from the mansion.": "W zamian trzymasz się, do cholery, z daleka od rezydencji.",
    "What do you think, Kim?": "Co o tym myślisz, Kim?",
    "Of course. If Miss Kimura is willing to work with us, I see no reason to interfere with her investigation.": "Oczywiście. Jeśli panna Kimura chce z nami współpracować, nie widzę powodu, by ingerować w jej śledztwo.",
    "We can film the slot tonight at seven.": "Możemy nagrać materiał dziś o siódmej.",
    "We’ll be there.": "Będziemy tam.",
    "We’re going to tell them everything.": "Powiemy im wszystko.",
    "Call Miss Bhatt. Prepare a presentation.": "Zadzwoń do panny Bhatt. Przygotuj prezentację.",
    "Right now? She won’t be at work.": "Teraz? Nie będzie w pracy.",
    "Find her…": "Znajdź ją…",
    "Organize everything you have and meet me at my home in four hours.": "Zorganizuj wszystko, co masz, i spotkaj się ze mną w moim domu za cztery godziny.",
    "Great. Melissa is going to be really happy to see me on Saturday.": "Świetnie. Melissa będzie naprawdę szczęśliwa, widząc mnie w sobotę.",
    "I hope her office number forwards to her cell phone.": "Mam nadzieję, że jej numer biurowy przekierowuje na komórkę.",
    "Shit. No answer.": "Cholera. Brak odpowiedzi.",
    "I could visit her at her home.": "Mogłabym odwiedzić ją w domu.",
    "This day is just getting better and better.": "Ten dzień staje się coraz lepszy.",
    "Did you find Kimberly?": "Znalazłaś Kimberly?",
    "1Hero, I’m glad you’re here.": "1Hero, cieszę się, że jesteś.",
    "I haven’t been able to get anywhere with security.": "Nie udało mi się nic wskórać z ochroną.",
    "Detective Canmore, is this man with you? What’s going on?": "Detektywie Canmore, czy ten mężczyzna jest z panem? Co się dzieje?",
    "What’s all the commotion about?": "O co to całe zamieszanie?",
    "Paul, we have a problem!": "Paul, mamy problem!",
    "1Hero, what’s wrong? Where’s Kim?": "1Hero, co się dzieje? Gdzie jest Kim?",
    "She’s… very troubled right now. I think she’ll be here soon.": "Ona… jest teraz bardzo zmartwiona. Myślę, że wkrótce tu będzie.",
    "And when she gets here, she’s going to try broadcasting something crazy.": "A gdy tu dotrze, spróbuje wyemitować coś szalonego.",
    "Again? God damn it.": "Znowu? Cholera.",
    "Paul, this is very important: She can’t be allowed to broadcast that message. No matter what.": "Paul, to bardzo ważne: Nie można jej pozwolić na wyemitowanie tej wiadomości. Za żadną cenę.",
    "Yeah, I know. If we let her go on-air like that, we’d lose our audience.": "Tak, wiem. Jeśli pozwolimy jej wejść na antenę w ten sposób, stracimy publiczność.",
    "There’s more. She has people helping her.": "Jest coś jeszcze. Ma ludzi, którzy jej pomagają.",
    "People? Who?": "Ludzi? Kogo?",
    "Dangerous people, Paul. You need to be careful.": "Niebezpiecznych ludzi, Paul. Musisz uważać.",
    "How dangerous are we talking about?": "Jak bardzo niebezpiecznych?",
    "You might call them… monsters.": "Można by ich nazwać… potworami.",
    "And they won’t go down easily.": "I nie padną łatwo.",
    "This doesn’t make any sense. Who are you people?": "To nie ma sensu. Kim wy, ludzie, jesteście?",
    "They’re friends of mine, here to help.": "To moi przyjaciele, przyszli pomóc.",
    "What about the police? Where are they?": "A co z policją? Gdzie ona jest?",
    "Yeah, 1Hero, does Commissioner Kimura know what’s going on?": "Tak, 1Hero, czy komisarz Kimura wie, co się dzieje?",
    "The commissioner is… indisposed. She can’t assist us.": "Pani komisarz jest… niedysponowana. Nie może nam pomóc.",
    "I’ll see about getting help from the police station. In the meantime, my friends will help you in case anything happens.": "Zobaczę, czy uda się sprowadzić pomoc z posterunku. W międzyczasie moi przyjaciele pomogą wam, gdyby coś się stało.",
    "Don’t worry, the Lord is with us.": "Nie martw się, Pan jest z nami.",
    "1Hero… why is there a priest here?": "1Hero… czemu tu jest ksiądz?",
    "When things get hairy, we’ll need him.": "Gdy zrobi się gorąco, będziemy go potrzebować.",
    "Monsters and priests? This has to be some kind of joke.": "Potwory i księża? To musi być jakiś żart.",
    "I wish it were... I should go to the studio. If the worst should happen and they make it there, that’s where I need to be.": "Chciałbym, żeby to był żart... Powinienem iść do studia. Jeśli najgorsze się stanie i tam dotrą, muszę tam być.",
    "I’ll back you up, Father.": "Będę cię wspierać, ojcze.",
    "1Hero?": "1Hero?",
    "Paul, Father Solomon is right. If something happens, you should listen to him.": "Paul, ojciec Solomon ma rację. Jeśli coś się stanie, powinieneś go posłuchać.",
    "As long as nothing goes on air, I’ll trust you... for now. But I’d really like to know what’s going on.": "Dopóki nic nie pójdzie na antenę, zaufam ci... na razie. Ale naprawdę chciałbym wiedzieć, co się dzieje.",
    "Explanations will have to wait. Right now, we have to act fast. They could show up at any moment.": "Wyjaśnienia będą musiały poczekać. Teraz musimy działać szybko. Mogą pojawić się w każdej chwili.",
    "I don’t understand what’s going on. If there’s danger, police should be here.": "Nie rozumiem, co się dzieje. Jeśli jest niebezpieczeństwo, policja powinna tu być.",
    "I’m working on that. Trust me.": "Pracuję nad tym. Zaufaj mi.",
    "I’ll clear the public areas… After that, I’ll head over to the security room to watch the cameras for anything suspicious.": "Oczyszczę strefy publiczne… Potem udam się do ochrony, by obserwować kamery pod kątem czegoś podejrzanego.",
    "I’ll scope out the perimeter. The earlier we see them coming, the better.": "Sprawdzę teren wokół budynku. Im wcześniej ich zobaczymy, tym lepiej.",
    "Let’s just hope they use the front door.": "Miejmy nadzieję, że wejdą frontowymi drzwiami.",
    "There’s no other way in.": "Nie ma innego wejścia.",
    "I'll help with the perimeter.": "Pomogę przy obchodzie.",
    "1Hero… How sure are you Judy is safe?": "1Hero… Jak bardzo jesteś pewien, że Judy jest bezpieczna?",
    "Fairly confident… But I’ll check on her when I get to the police station.": "Dość pewny… Ale sprawdzę, co u niej, gdy dotrę na posterunek.",
    "Okay, this is a lot.": "Dobra, to wiele.",
    "But if Kimberly’s new weirdo bodyguards are on the way, I guess I’d better get to locking down the building, and make sure the studio is secure.": "Ale jeśli nowi dziwaczni ochroniarze Kimberly są w drodze, chyba lepiej zacznę zabezpieczać budynek i upewnię się, że studio jest bezpieczne.",
    "Aren’t I always?": "Czyż nie zawsze?",
    "I don’t really look forward to being surrounded by police.": "Nie za bardzo cieszę się na myśl o otoczeniu przez policję.",
    "Don’t worry, I’ve got your back.": "Nie martw się, mam twoje plecy.",
    "For now, let’s just focus on stopping the apocalypse.": "Na razie skupmy się po prostu na powstrzymaniu apokalipsy.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=81 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=translations_dict.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=106: raise SystemExit(f'Expected 106, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map81')