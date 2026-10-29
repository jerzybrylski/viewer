#!/usr/bin/env python3
"""Build Polish drafts for Map 108 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map108-followups-01.jsonl'
TRANSLATIONS = {
    "I’m not strong enough.": "Nie jestem wystarczająco silny.",
    "Huh? It’s another room.": "Huh? To kolejne pomieszczenie.",
    "Hello… Don’t mind us. We’re just cleaning.": "Cześć… Nie zwracaj na nas uwagi. Tylko sprzątamy.",
    "He shouldn’t be here.": "On nie powinien tu być.",
    "I know, I know… But he’s tall and can reach the high areas.": "Wiem, wiem… Ale jest wysoki i dosięgnie wysoko.",
    "Please leave at once. I am busy and do not have time to deal with this.": "Proszę natychmiast wyjść. Jestem zajęta i nie mam czasu się tym zajmować.",
    "But, Lillian said…": "Ale Lillian powiedziała…",
    "She does not want him in the kitchen. Leave now.": "Ona nie chce go w kuchni. Wyjdź teraz.",
    "What are you doing? Making something?": "Co robisz? Coś robisz?",
    "I’m making honey tea for Madam Wilkes…": "Robię herbatę miodową dla pani Wilkes…",
    "But we seem to be out of honey.": "Ale chyba skończył się nam miód.",
    "I guess you should go get some.": "Chyba powinieneś po niego pójść.",
    "I will not leave the house.": "Nie opuszczę domu.",
    "Maybe I can help you out.": "Może mogę ci pomóc.",
    "Would you do that?": "Zrobiłbyś to?",
    "Sure, I can go get some honey.": "Jasne, mogę przynieść miód.",
    "Okay… But hurry up.": "Dobra… Ale pospiesz się.",
    "Oh, sorry. I’m still looking.": "Och, przepraszam. Wciąż szukam.",
    "You are acting very suspiciously.": "Zachowujesz się bardzo podejrzanie.",
    "I sure do…": "Owszem…",
    "Mother will be quite pleased.": "Matka będzie bardzo zadowolona.",
    "Mother?": "Matka?",
    "She has shown us a new life. To us, she is Mother…": "Ona pokazała nam nowe życie. Dla nas jest Matką…",
    "I do not expect someone like you to understand.": "Nie oczekuję, że ktoś taki jak ty zrozumie.",
    "If you’ll excuse me, I must leave before the tea cools.": "Jeśli pozwolisz, muszę iść, zanim herbata ostygnie.",
    "He left, but I don’t hear anything weird.": "Wyszedł, ale nie słyszę nic dziwnego.",
    "Come over here…": "Chodź tu…",
    "Listen.": "Posłuchaj.",
    "Hmm… Maybe it’s running water.": "Hmm… Może to lejąca się woda.",
    "No. Listen closely… It sounds like… something else.": "Nie. Posłuchaj uważnie… Brzmi jak… coś innego.",
    "See? I told you.": "Widzisz? Mówiłam ci.",
    "It looks like this barrel is blocking something…": "Wygląda na to, że ta beczka coś zasłania…",
    "Maybe if I can move it, we could hear it better.": "Może gdybym ją przesunęła, słyszelibyśmy lepiej.",
    "I tried to move it. It’s really heavy.": "Próbowałam ją przesunąć. Jest naprawdę ciężka.",
    "Let me see if I can move it.": "Pozwól, spróbuję ją przesunąć.",
    "It’s too heavy.": "Jest za ciężka.",
    "It’s heavy… But I think I can move it.": "Ciężka… Ale chyba dam radę ją przesunąć.",
    "Come on, 1Hero. Let’s not linger here…": "Chodź, 1Hero. Nie zatrzymujmy się tu…",
    "I’m already past my leaving time.": "Już dawno powinnam wyjść.",
    "Maybe we can come back tomorrow.": "Może wrócimy jutro.",
    "It’s the weekend, 1Hero. I’m not coming back until Monday.": "Jest weekend, 1Hero. Nie wrócę tu do poniedziałku.",
    "Do you have any plans tonight?": "Masz jakieś plany na wieczór?",
    "Inviting me on a date?": "Zapraszasz mnie na randkę?",
    "Well… I’m meeting some friends at Dick’s.": "Cóż… Spotykam się ze znajomymi u Dicka.",
    "Some friends? You mean Ella?": "Z jakimiś znajomymi? Masz na myśli Ellę?",
    "No, no… Chloe and Hannah… and Judy… From the church.": "Nie, nie… Chloe i Hannah… i Judy… Z kościoła.",
    "Who’s Judy?": "Kim jest Judy?",
    "Sister Judy… A nun from the church.": "Siostra Judy… Zakonnica z kościoła.",
    "Really? A nun?": "Naprawdę? Zakonnica?",
    "We’re showing her a good time tonight.": "Pokażemy jej dziś dobry czas.",
    "You’re up to something, aren’t you?": "Coś kombinujesz, prawda?",
    "No! She’s… Chloe’s friend.": "Nie! Ona jest… przyjaciółką Chloe.",
    "Okay, 1Hero. What time are you meeting there?": "Dobrze, 1Hero. O której się tam spotykacie?",
    "We’ll be there at seven.": "Będziemy tam o siódmej.",
    "Hey! What are you doing in here?": "Hej! Co tu robisz?",
    "Oh, sorry. I was just finishing up cleaning.": "Och, przepraszam. Właśnie kończyłam sprzątanie.",
    "Yeah. All done.": "Tak. Już skończone.",
    "I must ask you to leave. Please.": "Muszę cię poprosić o wyjście. Proszę.",
    "Yeah, we’re going.": "Tak, już idziemy.",
    "There they are.": "Tam są.",
    "Lillian!": "Lillian!",
    "My naughty, naughty lovers.": "Moi niegrzeczni, niegrzeczni kochankowie.",
    "I was horny! I brought him here to fuck.": "Byłam napalona! Przyprowadziłam go tu, żeby się pieprzyć.",
    "Don’t be afraid, Erica. You have nothing to hide… Right?": "Nie bój się, Erica. Nie masz nic do ukrycia… Prawda?",
    "We’re just two horny rabbits… But we’ll get going.": "Jesteśmy tylko dwoma napalonymi króliczkami… Ale już idziemy.",
    "Not so fast.": "Nie tak szybko.",
    "Goodbye, my lovers.": "Żegnajcie, kochankowie.",
    "Did she walk here in the nude?": "Czy ona przyszła tu nago?",
    "What the hell was that? I thought we were toast.": "Co to, do cholery, było? Myślałam, że po nas.",
    "That was her pussy juice, 1Hero!": "To był jej sok z cipki, 1Hero!",
    "She tastes amazing.": "Smakuje niesamowicie.",
    "How the hell does she do that?": "Jak ona, do cholery, to robi?",
    "She’s a vampire.": "Ona jest wampirem.",
    "Don’t joke about that… you might just be right.": "Nie żartuj z tego… możesz mieć rację.",
    "Whatever it was… I didn’t lose my job.": "Cokolwiek to było… Nie straciłam pracy.",
    "There’s no way she doesn’t suspect something… She’s not going to just let us get away.": "Nie ma mowy, żeby niczego nie podejrzewała… Nie puści nas tak po prostu.",
    "I don’t know about you, but I’m not hanging around to find out.": "Nie wiem jak ty, ale ja nie zamierzam tu zostać, żeby się przekonać.",
    "I’m going home. Any plans tonight?": "Idę do domu. Masz jakieś plany na wieczór?",
    "I’ve got to watch the church… We have a shortage of officers.": "Muszę pilnować kościoła… Mamy braki kadrowe.",
    "Keeping a lookout for Madalyn?": "Wypatrujesz Madalyn?",
    "Or someone else.": "Albo kogoś innego.",
    "If you’re looking for company, you know who to call.": "Jeśli szukasz towarzystwa, wiesz, do kogo zadzwonić.",
    "See ya around, Erica.": "Do zobaczenia, Erica.",
    "I was just… I had some questions.": "Ja tylko… miałam kilka pytań.",
    "What are you doing? Where is Lillian?": "Co robisz? Gdzie jest Lillian?",
    "We’ve not been able to find her. She must have known we were coming.": "Nie udało nam się jej znaleźć. Musiała wiedzieć, że idziemy.",
    "Whoever the hell she is, she’s committed quite the fraud.": "Kimkolwiek, do cholery, jest, dopuściła się niezłego oszustwa.",
    "How did you do it, Andrea?": "Jak to zrobiłaś, Andrea?",
    "Do what?": "Co zrobiłam?",
    "In two hours, Jon is going to open the bunker…": "Za dwie godziny Jon otworzy bunkier…",
    "What’s the deal? How did you arrange it?": "O co chodzi? Jak to załatwiłaś?",
    "We have the undercover team to thank for that.": "To zasługa zespołu tajniaków.",
    "Nellie?": "Nellie?",
    "There’s more to us than just Nellie…": "To nie tylko Nellie…",
    "I swear I heard voices coming from over here…": "Przysięgam, słyszałam głosy dochodzące stąd…",
    "I bet this place is ancient… Probably the plumbing.": "Założę się, że to miejsce jest starożytne… Pewnie hydraulika.",
    "I’m learning something new about myself.": "Dowiaduję się o sobie czegoś nowego.",
    "What would that be?": "Co takiego?",
    "I get horny when I’m creeped out.": "Robię się napalona, gdy się boję.",
    "Maybe this place has more of a romantic vibe.": "Może to miejsce ma bardziej romantyczny klimat.",
    "You know, Andrea, the public will get over it… Let’s arrest those goons and put them on trial.": "Wiesz, Andrea, ludzie to przełkną… Aresztujmy tych zbirów i postawmy ich przed sądem.",
    "You are charming me into changing my mind?": "Urokiem próbujesz zmienić moje zdanie?",
    "There’s love in the air. How about we do the right thing?": "W powietrzu czuć miłość. Może zróbmy to, co słuszne?",
    "Haha. Oh, 1Hero. You’re too naive.": "Haha. Och, 1Hero. Jesteś zbyt naiwny.",
    "Holy shit… I’m so fucking horny.": "Jasna cholera… Jestem tak, kurwa, napalona.",
    "Hey now… We’ve got work to do.": "Hej… Mamy pracę do wykonania.",
    "Maybe I was just hearing things… This is a dead end.": "Może tylko coś słyszałam… To ślepy zaułek.",
    "I bet Lillian is gone… Do you know who she was?": "Założę się, że Lillian zniknęła… Wiesz, kim była?",
    "We’ll turn this place upside down. No more Guild presence…": "Przewrócimy to miejsce do góry nogami. Koniec z obecnością Gildii…",
    "Whoever Lillian was, I’m sure we’ll figure it out.": "Kimkolwiek była Lillian, jestem pewna, że to rozgryziemy.",
    "What the hell do you think happened here?": "Jak myślisz, co się tu, do cholery, stało?",
    "Questions for another time. The important thing is that we seize the mansion and stop any more Guild activity…": "Pytania na inną okazję. Najważniejsze, by przejąć rezydencję i powstrzymać dalszą działalność Gildii…",
    "And you, 1Hero… Don’t be late.": "A ty, 1Hero… Nie spóźnij się.",
    "I’ll be at the warehouse. Don’t worry.": "Będę w magazynie. Nie martw się.",
    "What the hell are you still doing here? Leave before Duncan comes back!": "Co ty tu, do cholery, wciąż robisz? Wynoś się, zanim wróci Duncan!",
    "This place is huge. It could take a long time to find these amulets.": "To miejsce jest ogromne. Znalezienie amuletów może zająć sporo czasu.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=108 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=translations.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=116: raise SystemExit(f'Expected 116, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map108')