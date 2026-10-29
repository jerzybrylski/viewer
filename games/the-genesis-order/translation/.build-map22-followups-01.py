#!/usr/bin/env python3
"""Build Polish drafts for Map 22 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map22-followups-01.jsonl'
TRANSLATIONS = {
    "You’ll have to excuse the darkness. The church is quite old.": "Wybacz ciemność. Kościół jest dość stary.",
    "I’ll admit, this place creeps me out.": "Przyznam, to miejsce mnie przeraża.",
    "It was built in the eighteenth century…": "Zbudowano go w osiemnastym wieku…",
    "Much of what’s here is a mystery to Father and me.": "Wiele z tego, co tu jest, pozostaje tajemnicą dla Ojca i dla mnie.",
    "The noise!": "Hałas!",
    "I heard it… It’s close.": "Słyszałam to… Jest blisko.",
    "It’s Chloe!": "To Chloe!",
    "She’s in danger.": "Jest w niebezpieczeństwie.",
    "I have to help Chloe.": "Muszę pomóc Chloe.",
    "I gotta get the hell out of here.": "Muszę stąd zwiewać.",
    "1Hero…": "1Hero…",
    "I’m… not a virgin anymore. Am I?": "Ja… już nie jestem dziewicą. Prawda?",
    "Strictly speaking… no, you’re not.": "Ściśle mówiąc… nie, nie jesteś.",
    "I never thought it possible that I’d be here.": "Nigdy nie myślałam, że to możliwe, bym tu była.",
    "I want to be a servant to the Lord… But I was never tested.": "Chcę służyć Panu… Ale nigdy nie byłam wystawiona na próbę.",
    "And now that I have been… Perhaps I am not in the place I belong.": "A teraz, gdy zostałam… Może nie jestem na właściwym miejscu.",
    "You mean you don’t want to be a nun?": "Chcesz powiedzieć, że nie chcesz być zakonnicą?",
    "I never thought I’d have a desire for sin. My will is weak.": "Nigdy nie myślałam, że zapragnę grzechu. Moja wola jest słaba.",
    "That’s not true. Madalyn tricked me. I shouldn’t have done what I did.": "To nieprawda. Madalyn mnie oszukała. Nie powinnam była tego robić.",
    "Don’t blame her and don’t blame yourself.": "Nie obwiniaj jej i nie obwiniaj siebie.",
    "When I was young, I tried so hard to find a partner. I wanted romance but it never came…": "Gdy byłam młoda, tak bardzo starałam się znaleźć partnera. Pragnęłam romansu, ale nigdy nie nadszedł…",
    "And now, that's all I can think about.": "A teraz to jedyne, o czym mogę myśleć.",
    "You’ve suppressed it for so long, it’s only normal that you’d have these feelings.": "Tłumiłaś to tak długo, to normalne, że masz takie uczucia.",
    "I have a thought, but dare I say it?": "Mam myśl, ale czy odważę się ją wypowiedzieć?",
    "You can tell me anything, Judy.": "Możesz mi powiedzieć wszystko, Judy.",
    "God’s will has failed those around me… I should never have become a nun.": "Wola Boga zawiodła tych wokół mnie… Nigdy nie powinnam była zostać zakonnicą.",
    "You are not the only one who’s questioning God’s will…": "Nie tylko ty kwestionujesz wolę Boga…",
    "I am on a holy mission, Judy. I am being guided by a servant of God Himself.": "Jestem na świętej misji, Judy. Prowadzi mnie sługa Samego Boga.",
    "The woman who was in my dreams… You’re being guided by an angel.": "Kobieta, która była w moich snach… Prowadzi cię anioł.",
    "We have to find our own way in life. The both of us.": "Musimy znaleźć własną drogę w życiu. Oboje.",
    "That’s a scary thought.": "To przerażająca myśl.",
    "It is, Judy. But it’s also true. You are strong and capable of making your own decisions.": "Jest, Judy. Ale to też prawda. Jesteś silna i zdolna do podejmowania własnych decyzji.",
    "You don’t have to be bound by the expectations of others.": "Nie musisz być związana oczekiwaniami innych.",
    "I never thought of myself as strong.": "Nigdy nie myślałam o sobie jako o silnej.",
    "Strength doesn’t come from muscles. Don’t sell yourself short.": "Siła nie pochodzi z mięśni. Nie lekceważ siebie.",
    "Come on, 1Hero. We shouldn’t keep Father waiting.": "Chodź, 1Hero. Nie powinniśmy kazać Ojcu czekać.",
    "Arianna… How are you holding up?": "Arianna… Jak się trzymasz?",
    "I’m getting used to this feeling… The human body is quite different from an angel’s body.": "Przyzwyczajam się do tego uczucia… Ludzkie ciało dość różni się od ciała anioła.",
    "It’s bizarre, seeing you like this.": "To dziwne, widzieć cię w takiej postaci.",
    "Would it make you more comfortable if I looked like this?": "Czy byłoby ci wygodniej, gdybym wyglądała tak?",
    "Ah! This feels much better.": "Ach! Tak jest dużo lepiej.",
    "Fuck! Where is Lilith!?": "Kurwa! Gdzie jest Lilith!?",
    "You’re not escaping that easily.": "Nie uciekniesz tak łatwo.",
    "That’s… So weird.": "To… takie dziwne.",
    "Get some rest, 1Hero. I can tell you need it.": "Odpocznij, 1Hero. Widzę, że tego potrzebujesz.",
    "1Hero! The consequences are dire!": "1Hero! Konsekwencje są poważne!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=22 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=46: raise SystemExit(f'Expected 46, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map22')
