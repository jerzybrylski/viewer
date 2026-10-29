#!/usr/bin/env python3
"""Build Polish drafts for Map 47 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map47-followups-01.jsonl'
TRANSLATIONS = {
    "How do you do, good sir?": "Witam, szanowny panie?",
    "Is that Hannah in Carol’s room?": "Czy to Hannah w pokoju Carol?",
    "What are you still doing here?": "Co ty tu jeszcze robisz?",
    "Just hanging out with Chloe and Hannah.": "Po prostu siedzę z Chloe i Hannah.",
    "Don’t stay up too late.": "Nie siedźcie za długo.",
    "You better hurry and find Hannah and Chloe. Bad weather is on the way.": "Lepiej pospiesz się i znajdź Hannah i Chloe. Nadciąga brzydka pogoda.",
    "When I told you to keep an eye on Hannah, I didn’t expect this.": "Gdy kazałam ci mieć oko na Hannah, nie spodziewałam się tego.",
    "I walked in on Hannah and Chloe… It wasn’t my idea.": "Wpadłem na Hannah i Chloe… To nie był mój pomysł.",
    "Why are you back?": "Czemu wróciłaś?",
    "I forgot my wallet, and the truck needs a tank full of gas if I’m going to make the trip.": "Zapomniałam portfela, a ciężarówka potrzebuje pełnego baku, jeśli mam zdążyć w podróż.",
    "Look, Carol. Please don’t tell Heather about Chloe…": "Słuchaj, Carol. Proszę, nie mów Heather o Chloe…",
    "She’s been having troubles with sex stuff, and the more Heather knows about it the more it makes Chloe angry.": "Ma problemy ze sprawami łóżkowymi i im więcej Heather wie, tym bardziej Chloe się złości.",
    "You kids worry too much. I think it would do her some good to talk to her mom.": "Wy, dzieciaki, za bardzo się martwicie. Myślę, że dobrze by jej zrobiła rozmowa z mamą.",
    "You’re not wrong… But now’s not a good time to push her. She’s working through problems.": "Masz rację… Ale teraz nie jest dobry czas, by na nią naciskać. Pracuje nad problemami.",
    "You know, 1Hero, I thought you were above kid games.": "Wiesz, 1Hero, myślałam, że jesteś ponad dziecinne zabawy.",
    "I’m helping the only way I know how.": "Pomagam, jak tylko umiem.",
    "I hope you’re being a good influence on those two. They need to grow up.": "Mam nadzieję, że masz dobry wpływ na te dwie. Muszą dorosnąć.",
    "I know, I know.": "Wiem, wiem.",
    "See ya soon, 1Hero. Don’t get into too much trouble while I’m gone.": "Do zobaczenia wkrótce, 1Hero. Nie wpakuj się w zbyt duże kłopoty, gdy mnie nie będzie.",
    "Hey, ladies. Did you sleep in?": "Hej, dziewczyny. Zaspaliście?",
    "I’ve got to get back to the church to change.": "Muszę wrócić do kościoła się przebrać.",
    "It’s too early. Let’s sleep just a few more hours.": "Za wcześnie. Pośpijmy jeszcze parę godzin.",
    "Mass starts in thirty minutes!": "Msza zaczyna się za trzydzieści minut!",
    "Okay… Twenty more minutes.": "Dobra… Jeszcze dwadzieścia minut.",
    "I’ll be there soon, Sister Judy.": "Wkrótce tam będę, siostro Judy.",
    "I look forward to seeing you there.": "Nie mogę się doczekać, by cię tam zobaczyć.",
    "Make sure Hannah gets ready.": "Dopilnuj, by Hannah się przygotowała.",
    "Why the hell did I promise I’d go to boring church?": "Po co, do cholery, obiecałem, że pójdę do nudnego kościoła?",
    "Hannah! You better change. I thought you’d already left by now.": "Hannah! Lepiej się przebierz. Myślałem, że już wyszłaś.",
    "Ma! I don’t want to go.": "Mamo! Nie chcę iść.",
    "You’re a grownup. You don’t have to go.": "Jesteś dorosła. Nie musisz iść.",
    "If you’re coming, you better hurry.": "Jeśli idziesz, lepiej się pospiesz.",
    "Fine… I’ll meet you there.": "Dobra… Spotkamy się tam.",
    "Are you coming Carol?": "Idziesz, Carol?",
    "Oh, I’ve got some things to tend to here. But you all have fun.": "Och, mam tu parę rzeczy do ogarnięcia. Ale bawcie się dobrze.",
    "I’ll be on guard duty. The officer posted there left.": "Będę na warcie. Funkcjonariusz stamtąd odszedł.",
    "Always working.": "Zawsze w pracy.",
    "1Hero? Have you seen Hannah?": "1Hero? Widziałeś Hannah?",
    "I was just looking for her.": "Właśnie jej szukałem.",
    "In my bedroom?": "W mojej sypialni?",
    "Well… I mean, she wasn’t there.": "Cóż… To znaczy, nie było jej tam.",
    "The thought of you sneaking around my bedroom makes me think naughty thoughts.": "Myśl o tym, jak zakradasz się do mojej sypialni, budzi we mnie niegrzeczne myśli.",
    "Carol…": "Carol…",
    "Hannah ran off into the woods or something. Let’s bang one out.": "Hannah uciekła gdzieś do lasu. Chodź, bzykniemy raz.",
    "I don’t think we should.": "Nie sądzę, byśmy powinni.",
    "Ma! Don’t look!": "Mamo! Nie patrz!",
    "What is that on your face? Are you wearing makeup?": "Co masz na twarzy? Masz makijaż?",
    "It’s not what it looks like! I fell into a ketchup pinata!": "To nie tak, jak wygląda! Wpadłam do pinaty z ketchupem!",
    "Hahahaha!": "Hahahaha!",
    "That didn’t go well.": "To nie poszło dobrze.",
    "Did she know where your cock was?": "Wiedziała, gdzie jest twój fiut?",
    "Like you said… The cat’s out of the bag.": "Jak mówiłaś… Kot wyleciał z worka.",
    "Poor girl must be mortified. I’ve not seen her in makeup. It’s not her style.": "Biedna dziewczyna musi być przerażona. Nie widziałem jej w makijażu. To nie w jej stylu.",
    "Well… And she had my cock in her mouth.": "Cóż… I miała mojego fiuta w buzi.",
    "I’d ask you to go find her, but I’m sure you have work to do.": "Poprosiłbym cię, byś ją odnalazł, ale jestem pewna, że masz robotę.",
    "About that… I got fired.": "A propos… Wyrzucili mnie.",
    "Sort of… I’m still on the case, but I’m undercover now.": "W pewnym sensie… Wciąż prowadzę sprawę, ale teraz pod przykrywką.",
    "Oh! Sounds exciting.": "O! Brzmi ekscytująco.",
    "The problem is, I may have to kill people now.": "Problem w tym, że może będę musiał teraz zabijać ludzi.",
    "It’s… It’s complicated.": "To… To skomplikowane.",
    "You’re assassinating thieves now?": "Teraz likwidujesz złodziei?",
    "I’ve been told the bust will go bad. I have a feeling things won’t go well.": "Powiedziano mi, że obława pójdzie źle. Mam przeczucie, że nie skończy się dobrze.",
    "1Hero… You’re a good man. You’ll find a way to make arrests without resorting to killing.": "1Hero… Jesteś dobrym człowiekiem. Znajdziesz sposób, by dokonać aresztowań bez uciekania się do zabijania.",
    "1Hero… Promise me you won’t kill anyone.": "1Hero… Obiecaj, że nikogo nie zabijesz.",
    "Just… Be safe.": "Po prostu… Bądź bezpieczny.",
    "I’m gettin’ changed for the party.": "Przebieram się na imprezę.",
    "See you there, Hannah.": "Do zobaczenia tam, Hannah.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=47 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=67: raise SystemExit(f'Expected 67, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map47')
