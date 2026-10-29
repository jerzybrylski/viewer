#!/usr/bin/env python3
"""Build Polish drafts for Map 43 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map43-followups-01.jsonl'
TRANSLATIONS = {
    "If this is regarding the case, Detective Bhatt should be here.": "Jeśli chodzi o sprawę, detektyw Bhatt powinna tu być.",
    "I trust you, and only you, Detective Canmore.": "Ufam tylko tobie, detektywie Canmore.",
    "Why me?": "Czemu ja?",
    "You believe my father may have been murdered. Correct?": "Wierzysz, że mój ojciec mógł zostać zamordowany. Zgadza się?",
    "I think it’s possible.": "Myślę, że to możliwe.",
    "My father’s reputation is important to me.": "Dobre imię mojego ojca jest dla mnie ważne.",
    "Someone stole from my father.": "Ktoś okradł mojego ojca.",
    "Who? What do you know?": "Kto? Co wiesz?",
    "Two very rare amulets have gone missing.": "Zaginęły dwa bardzo rzadkie amulety.",
    "Madalyn stole them?": "Madalyn je ukradła?",
    "I don’t understand it myself, but Madalyn convinced my father to get rid of rare artifacts that had been in our family for generations.": "Sama tego nie rozumiem, ale Madalyn przekonała mojego ojca, by pozbył się rzadkich artefaktów należących do naszej rodziny od pokoleń.",
    "Get rid of them?": "Pozbył się ich?",
    "My father sold them to the Eclipse Guild.": "Mój ojciec sprzedał je Gildii Eclipse.",
    "He had connections with the Guild?": "Miał powiązania z Gildią?",
    "Please. It’s not like that. My father was a good man.": "Proszę. To nie tak. Mój ojciec był dobrym człowiekiem.",
    "It was Madalyn. She was manipulating him.": "To Madalyn. Manipulowała nim.",
    "Maybe that’s how Madalyn used him for money.": "Może tak Madalyn wyciągała od niego pieniądze.",
    "Perhaps. But these family heirlooms should not be in the hands of a criminal organization.": "Być może. Ale te rodzinne pamiątki nie powinny być w rękach organizacji przestępczej.",
    "It would make sense that Madalyn would use off the books sales to get untraceable money.": "Miałoby sens, że Madalyn używała nieoficjalnych sprzedaży, by zdobyć nie do namierzenia pieniądze.",
    "How much are these amulets worth?": "Ile warte są te amulety?",
    "I don’t know. But I need them back. I’ll pay if I must.": "Nie wiem. Ale muszę je odzyskać. Zapłacę, jeśli będzie trzeba.",
    "This is really something that you should report to the police.": "To naprawdę coś, co powinnaś zgłosić na policję.",
    "I can only do so much.": "Mogę tylko tyle.",
    "I do not want his connection to the Guild to incriminate him, or paint my family in a negative light.": "Nie chcę, by jego powiązanie z Gildią go obciążało ani rzucało złego światła na rodzinę.",
    "You’re a detective. You must be able to contact the Guild.": "Jesteś detektywem. Musisz mieć kontakt do Gildii.",
    "You’re asking a lot.": "Wiele wymagasz.",
    "Please. Help me get in touch with the Eclipse Guild. I simply want to restore my family heirlooms to their proper place.": "Proszę. Pomóż mi skontaktować się z Gildią Eclipse. Chcę tylko przywrócić rodzinne pamiątki na właściwe miejsce.",
    "Tell me more about these amulets.": "Opowiedz mi więcej o amuletach.",
    "They were crafted in Egypt, over 3000 years ago.": "Wykonano je w Egipcie, ponad 3000 lat temu.",
    "What do they look like?": "Jak wyglądają?",
    "One is gold, with a turquoise gem centered on the piece, the other a black onyx and silver ring with an onyx center gem.": "Jeden jest złoty, z turkusowym klejnotem pośrodku, drugi to czarny pierścień onyksowo-srebrny z centralnym onyksem.",
    "They sound fancy.": "Brzmią szykownie.",
    "They are indeed valuable to me.": "Rzeczywiście są dla mnie cenne.",
    "I’ll see what I can do. The Eclipse Guild is nearly dead.": "Zobaczę, co da się zrobić. Gildia Eclipse jest prawie martwa.",
    "There are not many members left in that organization that haven’t been arrested.": "Niewielu już zostało w tej organizacji, których nie aresztowano.",
    "Your amulets may just be in an evidence locker somewhere.": "Twoje amulety mogą być w jakimś depozycie dowodów.",
    "Please, do what you can. If my father’s death was indeed a murder, it may be tied to a member of the Guild.": "Proszę, zrób, co możesz. Jeśli śmierć mojego ojca rzeczywiście była morderstwem, może być powiązana z członkiem Gildii.",
    "If we find out that your father was murdered, I’ll have no choice but to reopen the case…": "Jeśli okaże się, że twój ojciec został zamordowany, nie będę miał wyboru i wznowię sprawę…",
    "It may be hard to keep your father’s connections to the Guild a secret.": "Może być trudno utrzymać w tajemnicy powiązania twojego ojca z Gildią.",
    "I understand. You will do what you must.": "Rozumiem. Zrobisz, co musisz.",
    "If you find anything, please return to the mansion.": "Jeśli coś znajdziesz, proszę, wróć do rezydencji.",
    "Let’s keep our conversations private.": "Zachowajmy nasze rozmowy w tajemnicy.",
    "Okay, Lillian. I’ll let you know what I find.": "Dobra, Lillian. Dam znać, co znajdę.",
    "I know I saw someone.": "Wiem, że kogoś widziałem.",
    "Please find my family heirlooms. The Eclipse Guild must have them.": "Proszę, znajdź moje rodzinne pamiątki. Gildia Eclipse musi je mieć.",
    "I’ll see what contacts I can make. But no guarantees.": "Zobaczę, jakie kontakty mogę nawiązać. Ale bez gwarancji.",
    "1Hero!": "1Hero!",
    "Shit! You scared me.": "Cholera! Przestraszyłaś mnie.",
    "Sorry… Any luck?": "Przepraszam… Coś znalazłeś?",
    "I got this door open.": "Otworzyłem te drzwi.",
    "You did!? That’s Charles’ office!": "Zrobiłeś to!? To gabinet Charlesa!",
    "Erica! You’re okay!": "Erica! Cała i zdrowa!",
    "Please just leave before Duncan finds you.": "Proszę, po prostu wyjdź, zanim Duncan cię znajdzie.",
    "Fucking hell!...": "Ja pierdolę!...",
    "Don’t say I didn’t warn you.": "Nie mów, że cię nie ostrzegałem.",
    "1Hero, who the hell was that?": "1Hero, kim do cholery była ta?",
    "Umm… Her name is Nellie.": "Yyy… Nazywa się Nellie.",
    "She’s a thief. Or was a thief?": "Jest złodziejką. Albo była złodziejką?",
    "I’m really not sure.": "Sam nie jestem pewien.",
    "And why is a thief who just broke into Lillian’s mansion rubbing your cock?": "I czemu złodziejka, która dopiero co włamała się do rezydencji Lillian, pociera twojego fiuta?",
    "I have my suspicions… I can’t really say.": "Mam podejrzenia… Nie mogę naprawdę powiedzieć.",
    "There are three others… and they have guns.": "Jest jeszcze trójka… i mają broń.",
    "What is the Guild?": "Co to za Gildia?",
    "You were close enough to hear them talking?": "Byłaś wystarczająco blisko, by słyszeć ich rozmowę?",
    "I heard one of them talk about getting the Guild back on its feet.": "Słyszałam, jak jedno z nich mówi o postawieniu Gildii na nogi.",
    "It’s the Eclipse Guild. It’s a secret criminal organization.": "To Gildia Eclipse. To tajna organizacja przestępcza.",
    "And you’re helping them?": "I im pomagasz?",
    "Would you even tell me if you were?": "Czy w ogóle powiedziałbyś mi, gdybyś im pomagał?",
    "I’m not helping Nellie. I came here looking for you and Lillian.": "Nie pomagam Nellie. Przyszedłem tu, bo szukałem ciebie i Lillian.",
    "I’ll tell you everything later, I promise.": "Opowiem ci wszystko później, obiecuję.",
    "I need to find the other officers.": "Muszę znaleźć pozostałych funkcjonariuszy.",
    "And you’re coming with me.": "I idziesz ze mną.",
    "Don’t worry. I’ll keep you safe.": "Nie martw się. Będę cię chronić.",
    "Stay close and be quiet.": "Trzymaj się blisko i bądź cicho.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=43 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=74: raise SystemExit(f'Expected 74, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map43')
