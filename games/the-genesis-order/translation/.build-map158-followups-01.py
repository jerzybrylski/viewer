#!/usr/bin/env python3
"""Build Polish drafts for Map 158 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map158-followups-01.jsonl'
TRANSLATIONS = {
    "You found him?": "Znalazłeś go?",
    "I told you I would.": "Mówiłem, że go znajdę.",
    "Welcome back, Detective Canmore.": "Witaj ponownie, detektywie Canmore.",
    "Here he is. Just like you asked.": "Oto on. Dokładnie jak prosiłaś.",
    "What would I do without you, Nellie?": "Co ja bym bez ciebie zrobiła, Nellie?",
    "Should we lock him up?": "Mamy go zamknąć?",
    "Leave… Everyone.": "Wyjdźcie… Wszyscy.",
    "I said leave.": "Powiedziałam: wynocha.",
    "You too, Nellie.": "Ty też, Nellie.",
    "Well… Here I am.": "No więc… Oto jestem.",
    "Not many people have gotten under my skin like you have.": "Niewielu ludzi zaszło mi tak za skórę jak ty.",
    "No… There’s more to it.": "Nie… Chodzi o coś więcej.",
    "I guess Carol’s not lying?": "Chyba Carol nie kłamie?",
    "She’s not the type to tell fibs.": "Ona nie jest typem kłamczuchy.",
    "Just who the hell are you?": "Kim ty, do cholery, jesteś?",
    "I was a thief when I met your mother… Not many people knew that though.": "Byłem złodziejem, gdy poznałem twoją matkę… Niewielu o tym wiedziało.",
    "So… This is the life you chose to live?": "Więc… takie życie wybrałeś?",
    "Exciting, isn’t it?": "Ekscytujące, prawda?",
    "Had I known your mother was pregnant, I might have stuck around.": "Gdybym wiedział, że twoja matka jest w ciąży, może bym został.",
    "But then again… Maybe not.": "Ale z drugiej strony… Może i nie.",
    "I’m not always… stable.": "Nie zawsze jestem… stabilny.",
    "I’ve spent a long time looking for you.": "Szukałem cię bardzo długo.",
    "I assume you don’t mean… Duncan.": "Zakładam, że nie masz na myśli… Duncana.",
    "Kirk?": "Kirk?",
    "I have a lot of aliases.": "Mam wiele aliasów.",
    "Why did you bring me here?": "Po co mnie tu sprowadziłaś?",
    "Andrea’s been playing you like a fiddle.": "Andrea robi z ciebie marionetkę.",
    "She’s my boss. Isn’t that how it works?": "Ona jest moją szefową. Tak to działa, nie?",
    "If you’re the type to get played… Sure.": "Jeśli jesteś typem, co daje się rozgrywać… Jasne.",
    "I’m not the only one taking orders from her.": "Nie tylko ja wykonuję jej rozkazy.",
    "I don’t take orders from Vayne.": "Ja nie wykonuję rozkazów Vayne.",
    "You think Andrea’s her only name?": "Myślisz, że Andrea to jej jedyne imię?",
    "She has an alias too?": "Ona też ma alias?",
    "Stick around long enough and maybe you’ll end up with one.": "Zostań wystarczająco długo, a może i ty się jakiegoś dorobisz.",
    "You’ve made my life difficult… But it sounds like I’m going to be your best friend.": "Utrudniłeś mi życie… Ale wygląda na to, że będziesz moim najlepszym przyjacielem.",
    "All the glory is coming your way. I’m going to feed you till you're full and fat.": "Cała chwała spłynie na ciebie. Będę cię karmić, aż będziesz tłusty i syty.",
    "So you know what Andrea’s plan is?": "Więc wiesz, jaki jest plan Andrei?",
    "It’s not the worst idea… At least I get to keep what I’ve built.": "To nie najgorszy pomysł… Przynajmniej zachowam to, co zbudowałem.",
    "It’s not my choice. I’d have you locked up.": "To nie mój wybór. Wolałbym cię zamknąć.",
    "Lock away your old man?...": "Zamknąłbyś własnego ojca?...",
    "Hey. Maybe we’d share a cell.": "Hej. Może dzielilibyśmy celę.",
    "I’m not like you.": "Nie jestem taki jak ty.",
    "Hey, I wasn’t like me either… You’re young.": "Hej, ja też nie byłem sobą… Jesteś młody.",
    "Vayne is not going to get between us… If we’re in this together, you and me… we have to talk.": "Vayne nie stanie między nami… Jeśli mamy iść w tym razem, ty i ja… musimy porozmawiać.",
    "Well… We’re talking.": "Cóż… Rozmawiamy.",
    "Hell, no.": "O cholera, nie.",
    "Heh. Neither do I.": "Heh. Ja też nie.",
    "So… Are you planning something?": "Więc… Planujesz coś?",
    "I’m planning to be a good boy, and I hope you do the same.": "Planuję być grzeczny i mam nadzieję, że ty też.",
    "I’ve played along so far, haven’t I?": "Dotąd współpracowałem, nie?",
    "She wanted to have my men killed.": "Chciała, żeby moi ludzie zostali zabici.",
    "Don’t pretend that you didn’t know.": "Nie udawaj, że nie wiedziałeś.",
    "Heh… Still… She’s not going to pull her punches just because I’m the big, scary bad guy.": "Heh… Wciąż… Nie będzie patyczkować się ze mną tylko dlatego, że jestem wielkim, strasznym złolem.",
    "And you want the heads up if she decides to throw you away.": "I chcesz cynk, jeśli zdecyduje się cię wystawić.",
    "Now you’re getting it.": "Teraz załapałeś.",
    "And you trust me?": "I ufasz mi?",
    "If I can’t trust my own flesh and blood, then who can I trust?": "Jeśli nie mogę ufać własnej krwi, to komu mam ufać?",
    "Vayne doesn’t want you here. So you better keep a low profile...": "Vayne nie chce cię tutaj. Lepiej trzymaj się na uboczu…",
    "I trust my men, but that woman has a way of getting what she wants.": "Ufam moim ludziom, ale ta kobieta potrafi dopiąć swego.",
    "Are we done?": "Skończyliśmy?",
    "I see that twinkle in your eye, 1Hero. You and me… We’re the same.": "Widzę ten błysk w oku, 1Hero. Ty i ja… Jesteśmy tacy sami.",
    "I’m an officer of the law.": "Jestem stróżem prawa.",
    "So is Vayne.": "Vayne też jest.",
    "So? What did he say?": "No i? Co powiedział?",
    "He doesn’t trust Andrea.": "Nie ufa Andrei.",
    "I don’t trust her either.": "Ja też jej nie ufam.",
    "So… Where does that leave things?": "Więc… Jak stoją sprawy?",
    "Duncan is looking for allies if things go south. I'm in the perfect situation for him.": "Duncan szuka sojuszników, jeśli sprawy się posypią. Jestem dla niego idealny.",
    "Good for you. It means you can stay close.": "Dobrze dla ciebie. To znaczy, że możesz trzymać się blisko.",
    "Yeah… I suppose that’s one way to look at it.": "Tak… Chyba tak można na to patrzeć.",
    "Brian’s waiting for you.": "Brian czeka na ciebie.",
    "Let’s go.": "Chodźmy.",
    "We’ve got them!": "Mamy je!",
    "Nice job, Canmore.": "Dobra robota, Canmore.",
    "It wasn’t easy, but Lillian had them locked away in magic chests.": "Nie było łatwo, ale Lillian trzymała je zamknięte w magicznych skrzyniach.",
    "Great… So, now what?": "Super… I co teraz?",
    "Keep an eye on the rift, but be careful…": "Miej oko na Szczelinę, ale ostrożnie…",
    "I assume that Lillian doesn’t have an internet connection in Hell, so she’ll be bringing the Toma here.": "Zakładam, że Lillian nie ma internetu w piekle, więc przyniesie tu Tomę.",
    "If I see any monsters, I’m shooting them immediately.": "Jeśli zobaczę jakieś potwory, od razu do nich strzelam.",
    "Try what you can, but the most important thing you need to remember is to never look at the Toma…": "Próbuj jak możesz, ale najważniejsze, byś nigdy nie patrzył na Tomę…",
    "If you see someone holding a statue, don’t look at it…": "Jeśli zobaczysz kogoś trzymającego posąg, nie patrz na niego…",
    "Tell your men the same.": "Powiedz to samo swoim ludziom.",
    "It’s not a joke, Bobby.": "To nie żart, Bobby.",
    "Believe me… I know.": "Uwierz mi… Wiem.",
    "Come on, 1Hero. Let’s see what the priest suggests we do next.": "Chodź, 1Hero. Zobaczmy, co ksiądz proponuje dalej.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=158 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=85: raise SystemExit(f'Expected 85, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map158')
