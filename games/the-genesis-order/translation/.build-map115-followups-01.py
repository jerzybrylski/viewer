#!/usr/bin/env python3
"""Build Polish drafts for Map 115 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map115-followups-01.jsonl'
TRANSLATIONS = {
    "We only picked up worthless chatter from two of the transmitters, but the third picked up something quite creepy.": "Odebraliśmy tylko bezwartościowe pogaduchy z dwóch nadajników, ale trzeci wychwycił coś dość upiornego.",
    "Which one was that?": "Który to był?",
    "The one coming from the east side of the mansion.": "Ten ze wschodniej strony rezydencji.",
    "… The food storage room.": "… Spiżarni.",
    "Let me hear it.": "Daj posłuchać.",
    "Listen to this.": "Posłuchaj tego.",
    "What the hell is that?": "Co to, do cholery, jest?",
    "I heard something similar, but faint when I was in the kitchen.": "Słyszałam coś podobnego, ale cicho, gdy byłam w kuchni.",
    "What’s going on over there? Some sort of cult activity?": "Co się tam dzieje? Jakaś działalność kultu?",
    "Did you get anything else?": "Masz coś jeszcze?",
    "That was the end of the recording. The transmitter stopped responding after this.": "To był koniec nagrania. Nadajnik przestał odpowiadać po tym.",
    "It’s broken?": "Zepsuty?",
    "Or out of batteries… But the other two are still online.": "Albo wyczerpały się baterie… Ale pozostałe dwa wciąż działają.",
    "I don’t know what it could be, but something strange is happening at the mansion.": "Nie wiem, co to może być, ale w rezydencji dzieje się coś dziwnego.",
    "We can figure this out, 1Hero.": "Rozgryziemy to, 1Hero.",
    "If Andrea finds out I’m helping you do this, my career is over.": "Jeśli Andrea dowie się, że ci w tym pomagam, moja kariera jest skończona.",
    "I know this is a big risk to you. But we’ll make it worth your effort.": "Wiem, że to dla ciebie duże ryzyko. Ale wynagrodzimy twój wysiłek.",
    "I’m not going to take bribes. I’m only in this because I want to know what’s going on at the mansion…": "Nie zamierzam brać łapówek. Jestem w to zaangażowana tylko dlatego, że chcę wiedzieć, co dzieje się w rezydencji…",
    "Kimura is not too keen on the idea of me interfering with… her own operations.": "Kimura nie jest zachwycona pomysłem, bym ingerowała w… jej własne operacje.",
    "It’s about a stolen painting.": "Chodzi o skradziony obraz.",
    "A stolen painting?": "Skradziony obraz?",
    "A highly valuable Rembrandt. The Guild wants it and they are here to steal it…": "Niezwykle cenny Rembrandt. Gildia go pragnie i jest tu, by go ukraść…",
    "But we’re working on it and that’s why you have to stay away from the mansion.": "Ale pracujemy nad tym i dlatego musisz trzymać się z daleka od rezydencji.",
    "Holy shit! You’re luring them in? Then why keep guard there?": "Jasna cholera! Wabiacie ich? Więc po co tam straż?",
    "We can’t make it easy. It would be too obvious…": "Nie możemy im tego ułatwiać. Byłoby to zbyt oczywiste…",
    "But they will be back.": "Ale wrócą.",
    "Now isn’t that interesting.": "Teraz to interesujące.",
    "You want a good story? Then let us do our job, and you’ll get the scoop after we arrest them.": "Chcesz dobrą historię? Pozwól nam wykonać pracę, a dostaniesz newsa po ich aresztowaniu.",
    "What about Wilkes? And the daughter?": "A co z Wilkesem? I córką?",
    "That’s something you and I are going to figure out together…": "To coś, co razem rozgryziemy…",
    "Just promise me you’re on our side. We’ll give you what you want, you just have to wait.": "Po prostu obiecaj mi, że jesteś po naszej stronie. Dam ci to, czego chcesz, tylko musisz poczekać.",
    "Sounds like we’re going to have an interesting interview tonight…": "Zapowiada się ciekawy wywiad dziś wieczorem…",
    "Next time you’re in the mansion, replace the broken one with this.": "Następnym razem, gdy będziesz w rezydencji, wymień zepsuty na ten.",
    "Andrea has arrived. Are you ready?": "Andrea przybyła. Jesteś gotowy?",
    "Shit. I still need to change.": "Cholera. Muszę się jeszcze przebrać.",
    "We’ll get ready. See you in the studio.": "Przygotujemy się. Do zobaczenia w studiu.",
    "Let’s go. I’ll fix you up.": "Chodźmy. Doprowadzę cię do porządku.",
    "Any time, Detective.": "Zawsze, detektywie.",
    "I’ve been checking the recordings and nothing stood out, but in the last hour we got this.": "Sprawdzałam nagrania i nic nie zwracało uwagi, ale w ostatniej godzinie dostaliśmy to.",
    "There’s something in that room that opens a secret passage.": "W tym pokoju jest coś, co otwiera tajne przejście.",
    "1Hero… I had a dream last night.": "1Hero… Miałam dziś w nocy sen.",
    "I dreamt of a secret passage. There was an eye and a gargoyle…": "Śniło mi się tajne przejście. Było tam oko i gargulec…",
    "It’s probably just a coincidence… But this is creeping me out.": "To pewnie tylko zbieg okoliczności… Ale to mnie przeraża.",
    "What exactly did you see in your dream?": "Co dokładnie widziałaś w swoim śnie?",
    "Well… There was a group of women… But they were in a shadow… Very hard to see.": "Cóż… Była tam grupa kobiet… Ale były w cieniu… Bardzo trudno dostrzec.",
    "The room was old… Orange-lit from flames, but too dark to make much out.": "Pokój był stary… Pomarańczowo oświetlony płomieniami, ale zbyt ciemny, by cokolwiek dostrzec.",
    "I had a similar dream. I don’t think it’s a coincidence.": "Miałam podobny sen. Nie sądzę, by to był zbieg okoliczności.",
    "Shit. This is spooky stuff, 1Hero.": "Cholera. To upiorne sprawy, 1Hero.",
    "What do you think they are hiding?": "Jak myślisz, co ukrywają?",
    "I’ve seen it… There is a room like you describe. Dark, but lit with torches.": "Widziałam to… Jest pokój taki, jak opisujesz. Ciemny, ale oświetlony pochodniami.",
    "Yeah…": "Tak…",
    "You can’t go back there. We’re risking getting caught.": "Nie możesz tam wracać. Ryzykujemy, że nas przyłapią.",
    "We won’t get caught. I just want to see this place for myself.": "Nie przyłapią nas. Chcę tylko zobaczyć to miejsce na własne oczy.",
    "There’s no point.": "Nie ma sensu.",
    "Of course there is! I’m a reporter. I want to know.": "Oczywiście, że jest! Jestem reporterką. Chcę wiedzieć.",
    "Look… You’re going to have a story soon. Just be patient.": "Posłuchaj… Wkrótce będziesz mieć historię. Po prostu bądź cierpliwa.",
    "Does it involve this creepy room?": "Czy ma to związek z tym upiornym pokojem?",
    "No… The painting… It’s…": "Nie… Obraz… To…",
    "There’s something else going on, and I think you know it.": "Dzieje się coś jeszcze i myślę, że o tym wiesz.",
    "You’re making this difficult, Kimberly.": "Utrudniasz sprawę, Kimberly.",
    "Come on, 1Hero. We’re in this together…": "No dalej, 1Hero. Jesteśmy w tym razem…",
    "We’re very similar, you and I. You know I won't let this go.": "Jesteśmy bardzo podobni, ty i ja. Wiesz, że tego nie odpuścę.",
    "We can’t just go in there and start looking around. Lillian or the lepers will see you.": "Nie możemy tam po prostu wejść i rozglądać się. Lillian lub trędowaci cię zobaczą.",
    "You’re smart. Isn’t there a way to sneak around?": "Jesteś sprytny. Nie ma sposobu, by się zakraść?",
    "Erica… She can help us.": "Erica… Ona może nam pomóc.",
    "Lillian’s maid… She’s been helping me spy on her.": "Pokojówka Lillian… Pomagała mi ją szpiegować.",
    "Great!... How can she help us?": "Świetnie!... Jak może nam pomóc?",
    "She’s good at distraction… Let me talk to her.": "Jest dobra w odwracaniu uwagi… Pozwól mi z nią porozmawiać.",
    "Get her help, 1Hero. There’s something going on under that mansion and I need to know what it is.": "Zdobądź jej pomoc, 1Hero. Pod tą rezydencją dzieje się coś i muszę wiedzieć, co to jest.",
    "I can’t keep secrets from my producer, 1Hero.": "Nie mogę trzymać tajemnic przed moim producentem, 1Hero.",
    "Let’s keep this so-called rift room between us… At least for now.": "Zachowajmy ten tak zwany pokój szczeliny między nami… Przynajmniej na razie.",
    "Okay… I’ll trust you.": "Dobrze… Zaufam ci.",
    "See ya later, Kimberly.": "Do zobaczenia później, Kimberly.",
    "See if Lillian’s maid will help us sneak into the mansion.": "Zobacz, czy pokojówka Lillian pomoże nam zakraść się do rezydencji.",
    "Nothing’s coming up on the audio. The transmitters have been silent.": "Nic nie słychać na audio. Nadajniki milczą.",
    "How long have you been listening?": "Jak długo słuchasz?",
    "I’ve been in this room since I left the mansion. If something happens, I’ll let you know.": "Byłam w tym pokoju, odkąd wyszłam z rezydencji. Jeśli coś się stanie, dam ci znać.",
    "There’s something you’re not telling me.": "Coś przede mną ukrywasz.",
    "Just let me hear the audio.": "Po prostu daj mi posłuchać nagrania.",
    "Listen…": "Posłuchaj…",
    "I don’t know what the hell they're talking about.": "Nie mam pojęcia, o czym, do cholery, mówią.",
    "What is the rift, 1Hero? Tell me.": "Czym jest szczelina, 1Hero? Powiedz mi.",
    "Who knows? They are crazy.": "Kto wie? Są szaleni.",
    "Why would I trust you with anything?": "Czemu miałabym ci cokolwiek powierzyć?",
    "We have the same goal. We both want to know what’s happening at that mansion.": "Mamy ten sam cel. Oboje chcemy wiedzieć, co dzieje się w tej rezydencji.",
    "You just want a story. You’ll step all over the investigation to get it.": "Chcesz tylko historii. Przejedziesz się po śledztwie, by ją zdobyć.",
    "You’re not part of the investigation anymore.": "Nie jesteś już częścią śledztwa.",
    "Thanks to you!": "Dzięki tobie!",
    "1Hero… I’ve been having dreams ever since we went into that secret basement.": "1Hero… Mam sny, odkąd weszliśmy do tej tajnej piwnicy.",
    "I know you’re hiding something.": "Wiem, że coś ukrywasz.",
    "You have no idea what you’re talking about. You’re just having nightmares.": "Nie masz pojęcia, o czym mówisz. Masz tylko koszmary.",
    "I’m going to find out, one way or another.": "Dowiem się, tak czy inaczej.",
    "You promised not to visit the mansion again.": "Obiecałeś, że nie odwiedzisz już rezydencji.",
    "You’re not a detective anymore. I’ll do what I have to do.": "Nie jesteś już detektywem. Zrobię, co muszę.",
    "Stay away from the mansion, Kimberly.": "Trzymaj się z daleka od rezydencji, Kimberly.",
    "You can’t hide this from me, 1Hero.": "Nie ukryjesz tego przede mną, 1Hero.",
    "You don’t know what you’re getting into.": "Nie wiesz, w co się pakujesz.",
    "And that’s supposed to make me back down?": "I to ma sprawić, że się wycofam?",
    "If you go there, you’ll get caught. I’m not helping you this time.": "Jeśli tam pójdziesz, przyłapią cię. Tym razem ci nie pomogę.",
    "I’ll see ya around.": "Do zobaczenia.",
    "I want to see what’s in that mansion’s basement.": "Chcę zobaczyć, co jest w piwnicy tej rezydencji.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=115 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=translations.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=101: raise SystemExit(f'Expected 101, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map115')