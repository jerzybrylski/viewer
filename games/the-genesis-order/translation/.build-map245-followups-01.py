#!/usr/bin/env python3
"""Build Polish drafts for Map 245 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map245-followups-01.jsonl'
TRANSLATIONS = {
    "We hit the motherlode!": "Trafiliśmy na żyłę złota!",
    "Wait, 1Hero! Don’t touch anything!": "Czekaj, 1Hero! Niczego nie dotykaj!",
    "What? Something wrong?": "Co? Coś nie tak?",
    "It’s Tikpak treasure. It’s all cursed.": "To skarb Tikpak. Wszystko jest przeklęte.",
    "Cursed?": "Przeklęte?",
    "Remember what happened to the Guild? This must be where they put the cursed treasure they still had.": "Pamiętasz, co stało się z Gildią? To musi być miejsce, gdzie schowali przeklęty skarb, który im został.",
    "So… I can’t take any of it?": "Więc… Nie mogę nic wziąć?",
    "I’m afraid not, unless you want a first-row seat to the fate of the Eclipse Guild’s members.": "Obawiam się, że nie, chyba że chcesz bilet w pierwszym rzędzie na los członków Gildii Eclipse.",
    "That doesn’t sound appealing.": "Nie brzmi zachęcająco.",
    "But then what’s the key for, the one Tasha has?": "Ale to po co jest klucz, ten, który ma Tasha?",
    "Maybe there’s something more.": "Może jest coś więcej.",
    "Sounds good to me. I’m already dead, so it’ll be your funeral.": "Brzmi dobrze dla mnie. Ja już jestem martwy, więc to będzie twój pogrzeb.",
    "Don’t be so dramatic.": "Nie bądź taki dramatyczny.",
    "I doubt Duncan kept a key around for a treasure he didn’t want to touch anyway.": "Wątpię, by Duncan trzymał klucz do skarbu, którego i tak nie chciał tknąć.",
    "He’s crazy enough to try killing me, but he’s not suicidal.": "Jest na tyle szalony, by próbować mnie zabić, ale nie jest samobójcą.",
    "So Duncan tried to kill you, too, huh?": "Więc Duncan też próbował cię zabić, huh?",
    "Wait, what? He tried to kill you?": "Czekaj, co? Próbował cię zabić?",
    "And succeeded.": "I mu się udało.",
    "Then Evie brought me back.": "Potem Evie mnie przywróciła.",
    "Your dad’s a real jerk.": "Twój stary to niezły dupek.",
    "You’ll get no argument from me.": "Nie będę się spierać.",
    "Evie brought you back, huh?": "Evie cię przywróciła, huh?",
    "Why didn’t she do it again?": "Czemu nie zrobiła tego znowu?",
    "My time was up, I guess.": "Chyba mój czas się skończył.",
    "That’s too bad, man.": "Szkoda, stary.",
    "Just so you know, I’m grateful for your sacrifice.": "Tak, wiedz, że jestem wdzięczny za twoje poświęcenie.",
    "It was my fate… We all did what we had to do.": "Taki był mój los… Wszyscy zrobiliśmy, co musieliśmy.",
    "So how long do you plan to live in the crystal? Forever?": "Więc jak długo planujesz mieszkać w krysztale? Na zawsze?",
    "I haven’t really thought about it.": "Nie zastanawiałem się nad tym.",
    "A lot of lovely ladies were left behind, and I want to spend more time with them.": "Sporo ślicznych pań zostało w tyle i chcę spędzić z nimi więcej czasu.",
    "I can understand that.": "Mogę to zrozumieć.",
    "So after they move on?": "Więc po tym, jak odejdą?",
    "Depends on whether any of them will be joining me in Hell.": "Zależy, czy któraś z nich dołączy do mnie w piekle.",
    "What about kids?": "A co z dziećmi?",
    "Yeah… Definitely have several on the way.": "Tak… Na pewno kilka w drodze.",
    "I’m not sure what I’ll do about them.": "Nie jestem pewien, co z nimi zrobię.",
    "That’s tough. I don’t envy your position.": "To ciężkie. Nie zazdroszczę ci pozycji.",
    "Who knows? Could already have one or two of my own on the way, too.": "Kto wie? Może już mam jedno czy dwoje w drodze.",
    "Creampies are so much fun.": "Sperma w środku to taka frajda.",
    "Haha, yeah they are.": "Haha, tak jest.",
    "I’ve seen this before…": "Już to widziałem…",
    "Henry, can you stand on this pressure plate?": "Henry, możesz stanąć na tej płycie naciskowej?",
    "Trust me, I’ve seen this puzzle before.": "Uwierz mi, widziałem tę łamigłówkę wcześniej.",
    "So have I… That’s not the problem.": "Ja też… To nie problem.",
    "Oh… You’re a ghost.": "O… Jesteś duchem.",
    "Now you get it.": "Teraz załapałeś.",
    "I’ll find another way.": "Znajdę inny sposób.",
    "I'm sure you can figure this one out, detective.": "Jestem pewien, że to rozgryziesz, detektywie.",
    "Nice work, Detective Canmore.": "Dobra robota, detektywie Canmore.",
    "Clever old man… He used the Tikpak treasure to guard the real prize.": "Cwany staruszek… Użył skarbu Tikpak, by strzec prawdziwej nagrody.",
    "You don’t think this is cursed?": "Nie sądzisz, że to przeklęte?",
    "I suspect it isn’t, but Tasha will know. Bring it to her… If it’s cursed, you’ll have to bury it away where no one can find it.": "Podejrzewam, że nie, ale Tasha będzie wiedzieć. Zanieś jej… Jeśli przeklęte, będziesz musiał zakopać je tam, gdzie nikt nie znajdzie.",
    "That would suck… But I trust you.": "To byłoby do bani… Ale ufam ci.",
    "Looks a little heavy. Give me a hand?": "Wygląda na trochę ciężkie. Pomożesz?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=245 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=54: raise SystemExit(f'Expected 54, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map245')
