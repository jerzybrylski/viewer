#!/usr/bin/env python3
"""Build Polish drafts for Map 190 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map190-followups-01.jsonl'
TRANSLATIONS = {
    "You can’t get me, demons!": "Nie dorwiecie mnie, demony!",
    "I’ve never come across chests like these. I bet your amulets are in here.": "Nigdy nie widziałem takich skrzyń. Założę się, że wasze amulety są w środku.",
    "How do we open them?": "Jak je otworzyć?",
    "This mansion holds a lot of secrets. There are pathways in the walls.": "Ta rezydencja kryje mnóstwo sekretów. W ścianach są przejścia.",
    "I’ve noticed.": "Zauważyłem.",
    "It’s going to take a special key to open these chests. Keep your eyes peeled.": "Potrzeba specjalnego klucza, by otworzyć te skrzynie. Miejcie oczy otwarte.",
    "Hannah, stop it!": "Hannah, przestań!",
    "I've stopped! What are you complaining about?": "Przestałam! O co narzekasz?",
    "This is why I told you to stay at the church.": "Dlatego kazałem ci zostać w kościele.",
    "So what’s with the hair? Why do you need it?": "Więc o co chodzi z włosami? Po co ci one?",
    "It will open a gate to Hell.": "Otworzą bramę do piekła.",
    "Yep… I’ve used her hair before.": "Taa… Już używałem jej włosów wcześniej.",
    "I’ll help you find some… That Lillian girl sheds, I’m sure of it.": "Pomogę ci znaleźć trochę… Ta dziewczyna Lillian na pewno gubi włosy.",
    "No more monkey business… We have to hurry.": "Koniec z wygłupami… Musimy się pospieszyć.",
    "Come on. Let’s help.": "Chodź. Pomóżmy.",
    "Hey! Who’s in here?": "Hej! Kto tu jest?",
    "David? What the hell is he doing here?": "David? Co on, do cholery, tu robi?",
    "Wait… Did anyone lock the door?": "Czekaj… Czy ktoś zamknął drzwi?",
    "Shit! I gave him the backup key.": "Cholera! Dałem mu zapasowy klucz.",
    "Our clothes! We don’t have any!": "Nasze ubrania! Nie mamy żadnych!",
    "Everybody, hide!": "Wszyscy, chować się!",
    "Oh, boy! I love hiding!": "Ale fajnie! Uwielbiam chowanie!",
    "Where? There’s nowhere to run!": "Gdzie? Nie ma gdzie uciekać!",
    "That’s it… I retire.": "Tyle… Przechodzę na emeryturę.",
    "Well… At least I was able to get dressed in time.": "Cóż… Przynajmniej zdążyłem się ubrać na czas.",
    "How embarrassing!": "Jak żenująco!",
    "Is the game over already?": "Gra już skończona?",
    "Whose idea was it to leave all our clothes at the entry?": "Czyj to był pomysł, by zostawić wszystkie ubrania przy wejściu?",
    "I didn’t hear any complaints.": "Nie słyszałem żadnych narzekań.",
    "He’s an old man… Maybe his eyesight has gone bad.": "Jest stary… Może wzrok mu już nie dopisuje.",
    "Let’s hope so.": "Miejmy nadzieję.",
    "This problem could have been solved with a locked door.": "Ten problem można było rozwiązać zamkniętymi drzwiami.",
    "I seem to have this problem a lot.": "Mam ten problem dość często.",
    "I’m hungry. Can we eat?": "Jestem głodna. Możemy coś zjeść?",
    "Let’s go to Dick’s!": "Chodźmy do Dicka!",
    "Andrea’s paying!": "Andrea stawia!",
    "Hey! I’m broke now.": "Hej! Jestem spłukana.",
    "Does anyone have any coupons?": "Ma ktoś jakieś kupony?",
    "Last one there pays!": "Kto ostatni, ten płaci!",
    "Don’t you dare leave this house naked, young lady!": "Nie waż się wychodzić z tego domu nago, młoda damo!",
    "I have to make a pitstop at the porn shop.": "Muszę wpaść do sex shopu.",
    "I know I’m not paying!": "Wiem, że nie płacę!",
    "You and I both!": "Ja też nie!",
    "No one’s beating me there.": "Nikt mnie nie wyprzedzi.",
    "Want to bet?": "Założymy się?",
    "Are we really going to eat at that nasty place?": "Naprawdę będziemy jeść w tym obleśnym miejscu?",
    "Dick’s is wonderful! They have such good muffins.": "Dick's jest wspaniały! Mają takie dobre muffinki.",
    "Why do I have a feeling I’m paying for everyone?": "Czemu mam przeczucie, że płacę za wszystkich?",
    "Just how much do they pay you at Channel 4?": "Ile ci płacą w Channel 4?",
    "Oh, girl… It’s a lot!": "Och, dziewczyno… Dużo!",
    "I better go get dressed.": "Lepiej pójdę się ubrać.",
    "What a wild ride.": "Co za szalona jazda.",
    "As much as you worry me sometimes, I always knew you’d make it through.": "Choć czasem się o ciebie martwię, zawsze wiedziałam, że dasz radę.",
    "Let’s just hope nothing this crazy ever happens again.": "Miejmy tylko nadzieję, że nic tak szalonego już się nie wydarzy.",
    "Why do I have a feeling this is just the beginning?": "Czemu mam przeczucie, że to dopiero początek?",
    "Come on, Heather. Let’s go together.": "Chodź, Heather. Chodźmy razem.",
    "And with that, the battle to save the world was won…": "I tym sposobem bitwa o ocalenie świata została wygrana…",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=190 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=57: raise SystemExit(f'Expected 57, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map190')
