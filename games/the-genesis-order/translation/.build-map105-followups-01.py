#!/usr/bin/env python3
"""Build Polish drafts for Map 105 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map105-followups-01.jsonl'
TRANSLATIONS = {
    "Hey! Watch yourself!": "Hej! Uważaj!",
    "Sorry, Hannah.": "Przepraszam, Hannah.",
    "You should warn me before you go hitting rocks in a cave!": "Powinieneś mnie ostrzec, zanim zaczniesz walić w skały w jaskini!",
    "If it’s too dangerous, you can go back.": "Jeśli jest za niebezpiecznie, możesz wrócić.",
    "It ain't too dangerous if you stop being a clutz!": "Nie jest za niebezpiecznie, jeśli przestaniesz być niezdarą!",
    "Just... Watch your step.": "Po prostu... Patrz pod nogi.",
    "If we’re going to keep going, maybe we should invite Chloe.": "Jeśli mamy iść dalej, może powinniśmy zaprosić Chloe.",
    "What? No way! This is too dangerous for her.": "Co? Nie ma mowy! To za niebezpieczne dla niej.",
    "But it’s not for me?": "A dla mnie nie?",
    "You’re different, Hannah. You’re a tough girl.": "Jesteś inna, Hannah. Jesteś twarda dziewczyna.",
    "Am I too tough?": "Jestem za twarda?",
    "I don’t know. You don’t seem to care too much about me.": "Nie wiem. Wydaje się, że niewiele cię obchodzę.",
    "Of course I care about you. Where did this come from?": "Oczywiście, że mi na tobie zależy. Skąd to się wzięło?",
    "I’m not lady-like and therefore you can drop a rock on old Hannah.": "Nie jestem damą, więc możesz zrzucić skałę na starą Hannah.",
    "How come you fell in love with Chloe?": "Czemu zakochałeś się w Chloe?",
    "I was young and she was available.": "Byłem młody i była dostępna.",
    "So was I.": "Ja też byłam.",
    "Are you… jealous?": "Jesteś… zazdrosna?",
    "I never thought about it, 1Hero. It never crossed my mind.": "Nigdy o tym nie myślałam, 1Hero. Nigdy mi to nie przyszło do głowy.",
    "If you ain’t hooking up with Chloe, then what are you waiting for?": "Jeśli nie umawiasz się z Chloe, to na co czekasz?",
    "Chloe’s not ready for a relationship. Believe me, I’ve tried.": "Chloe nie jest gotowa na związek. Uwierz, próbowałem.",
    "I know, 1Hero. I know you did.": "Wiem, 1Hero. Wiem, że próbowałeś.",
    "Come on. Let’s get dressed and get out of here.": "Chodź. Ubierzmy się i wynośmy się stąd.",
    "Those rocks you tried to crush me with made a bridge.": "Te skały, którymi próbowałaś mnie zmiażdżyć, zrobiły most.",
    "I wasn’t…": "Ja nie…",
    "Huh. I guess they did.": "Huh. Chyba tak.",
    "Let's go deeper!": "Chodźmy głębiej!",
    "So what’s the plan, 1Hero? Are we gonna attack?": "Więc jaki jest plan, 1Hero? Zaatakujemy?",
    "No! We’re not fighting them… Nellie is a good guy.": "Nie! Nie walczymy z nimi… Nellie jest w porządku.",
    "She’s an undercover cop?": "Jest tajną policjantką?",
    "I never said that.": "Nigdy tego nie powiedziałem.",
    "You can tell me. I’m your best friend!": "Możesz mi powiedzieć. Jestem twoim najlepszym przyjacielem!",
    "I’m in deep trouble with the commissioner. I’m not allowed to say anything… Sorry, Hannah.": "Mam grube kłopoty u pani komisarz. Nie wolno mi nic mówić… Przepraszam, Hannah.",
    "Are you saying you can’t trust me?": "Mówisz, że nie możesz mi zaufać?",
    "Are you going to tell Chloe about this?": "Powiesz o tym Chloe?",
    "Of course! We need more help if we’re gonna take down the thieves.": "Oczywiście! Potrzebujemy więcej pomocy, jeśli mamy dorwać złodziei.",
    "Hannah!": "Hannah!",
    "The only thing I want you to do is keep an eye out whenever you’re home.": "Jedyne, czego chcę, to byś miała oko, gdy jesteś w domu.",
    "You think they’ll come to rob us?": "Myślisz, że przyjdą nas okraść?",
    "Just watch out... And if you see anything, let me know.": "Po prostu uważaj... I jeśli coś zobaczysz, daj znać.",
    "I can do that.": "Dam radę.",
    "I better get home. Mama’s going to be worried if she thinks I’ve gone into the cave.": "Lepiej wrócę do domu. Mama będzie się martwić, jeśli pomyśli, że weszłam do jaskini.",
    "I’ll leave soon. I just want to check out something.": "Wkrótce wyjdę. Chcę tylko coś sprawdzić.",
    "There's no point in swimming if I can't see anything to get.": "Nie ma sensu pływać, jeśli nie widzę nic do zdobycia.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=105 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=44: raise SystemExit(f'Expected 44, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map105')
