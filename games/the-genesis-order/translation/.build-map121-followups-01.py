#!/usr/bin/env python3
"""Build Polish drafts for Map 121 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map121-followups-01.jsonl'
TRANSLATIONS = {
    "I wonder what key would open this old chest.": "Zastanawiam się, jaki klucz otworzyłby tę starą skrzynię.",
    "Hey! You! Stop right there!": "Hej! Ty! Stój!",
    "Father Solomon. This is the police commissioner, Miss Kimura.": "Ojcze Solomonie. To komisarz policji, panna Kimura.",
    "I’m sorry you’ve been caught up in this investigation.": "Przykro mi, że została pani wciągnięta w to śledztwo.",
    "Unfortunately, you’ll now be expected to remain silent on a few top secret aspects of the case.": "Niestety, będzie się od pani oczekiwać milczenia w kilku ściśle tajnych aspektach sprawy.",
    "The Wilkes mansion is being used to contain and control the remnants of the Eclipse Guild.": "Rezydencja Wilkesów służy do powstrzymania i kontroli resztek Gildii Zaćmienia.",
    "This is highly top secret…": "To ściśle tajne…",
    "But Duncan is now under control and the Guild will be a honeypot to lure in the thieves that would otherwise be lying in wait...": "Ale Duncan jest już pod kontrolą, a Gildia będzie przynętą, by zwabić złodziei, którzy w przeciwnym razie czyhaliby w ukryciu...",
    "... preparing to fill in the power vacuum left by the fall of the Guild.": "...przygotowujących się do wypełnienia próżni władzy po upadku Gildii.",
    "Your presence at the mansion was unexpected, and I will see to it that nothing happens to you or your cathedral.": "Twoja obecność w rezydencji była nieoczekiwana i dopilnuję, by nic nie stało się tobie ani twojej katedrze.",
    "Do you know anything about Madalyn? Is she involved?": "Czy wiesz coś o Madalyn? Czy jest w to zamieszana?",
    "Both Madalyn Rose and Lillian Wilkes are being dealt with. Neither will be of concern to you.": "Zarówno Madalyn Rose, jak i Lillian Wilkes są już załatwione. Żadna z nich nie będzie już twoim zmartwieniem.",
    "Do what you can, I suppose. We’ll be preparing our own defenses here.": "Rób, co możesz, jak mniemam. My przygotujemy tutaj własną obronę.",
    "I simply ask that you stay away from the mansion.": "Proszę jedynie, byś trzymał się z daleka od rezydencji.",
    "Thanks for meeting with us, Miss Kimura.": "Dziękujemy za spotkanie, panno Kimura.",
    "It makes me feel a little better knowing the commissioner herself is on the case.": "Czuję się odrobinę lepiej, wiedząc, że sama pani komisarz prowadzi sprawę.",
    "And I apologize for this little mixup. It won’t happen again.": "I przepraszam za to małe nieporozumienie. Już się nie powtórzy.",
    "If you don’t mind, I must get back to my studies.": "Jeśli nie masz nic przeciwko, muszę wrócić do nauki.",
    "By all means.": "Oczywiście.",
    "Duncan is also tracking Morgan Deluna.": "Duncan śledzi również Morgan Delunę.",
    "He tried to rough up some locals while looking for her.": "Próbował zastraszyć kilku miejscowych, szukając jej.",
    "Dealing with criminals is never easy.": "Radzenie sobie z przestępcami nigdy nie jest łatwe.",
    "Nellie is with him. I will use her to track his every move. He will not be out of our control again.": "Nellie jest z nim. Wykorzystam ją, by śledzić każdy jego ruch. Nie wymknie się nam spod kontroli.",
    "He’s not suspicious of Nellie?": "Nie podejrzewa Nellie?",
    "Duncan and Nellie are on good terms. You can trust in that.": "Duncan i Nellie są w dobrych relacjach. Możesz na to liczyć.",
    "People I love could be in the crosshairs. You’re sure about this?": "Ludzie, których kocham, mogą być na celowniku. Jesteś tego pewna?",
    "I give you my word.": "Daję ci słowo.",
    "Don’t be so glum, 1Hero. It never gets easier.": "Nie bądź taki ponury, 1Hero. Nigdy nie jest łatwiej.",
    "That doesn't make me feel any better.": "Wcale nie czuję się przez to lepiej.",
    "It’s not supposed to.": "I nie ma.",
    "Why didn’t she tell me all this from the start?": "Czemu nie powiedziała mi tego wszystkiego od początku?",
    "Where is the nun?": "Gdzie jest zakonnica?",
    "Still in the bathroom… We need toilet paper.": "Wciąż w łazience… Potrzebujemy papieru toaletowego.",
    "Apparently she wipes after peeing.": "Najwyraźniej podciera się po sikaniu.",
    "I don’t need to know that…": "Nie muszę tego wiedzieć…",
    "Go back to her. I’ll find some.": "Wracaj do niej. Ja coś znajdę.",
    "Are you ready to place the crucifixes around the church?": "Jesteś gotowy, by rozmieścić krucyfiksy wokół kościoła?",
    "Let me stop by later. I have a few things I need to do really quick.": "Wpadnę później. Mam kilka spraw do szybkiego załatwienia.",
    "Where should we put the crucifixes?": "Gdzie powinniśmy położyć krucyfiksy?",
    "Let’s spread them out.": "Rozłóżmy je.",
    "We’ve placed the crosses around the church. We should be set now.": "Rozmieściliśmy krzyże wokół kościoła. Powinniśmy być gotowi.",
    "So, what do we do now?": "Więc co teraz robimy?",
    "I’m going back to the rift… I need your help, Father.": "Wracam do szczeliny… Potrzebuję twojej pomocy, ojcze.",
    "A bold idea. But it sounds too dangerous.": "Śmiały pomysł. Ale brzmi zbyt niebezpiecznie.",
    "Kimberly Foxx was kidnapped by Madalyn and brought into the rift… I have to save her.": "Kimberly Foxx została porwana przez Madalyn i wciągnięta do szczeliny… Muszę ją uratować.",
    "You saw Madalyn?": "Widziałeś Madalyn?",
    "The commissioner is looking for Madalyn, but you and I both know that’s a futile effort.": "Komisarz szuka Madalyn, ale oboje wiemy, że to daremny trud.",
    "Let’s go save her! I bet you could kick those demons’ asses, Dad.": "Chodźmy ją uratować! Założę się, że skopałbyś tyłki tym demonom, tato.",
    "You want to go into a portal… that in all likelihood leads to Hell… armed with a priest?": "Chcesz wejść do portalu… który najprawdopodobniej prowadzi do Piekła… uzbrojony w księdza?",
    "Nellie? What the hell are you doing here?": "Nellie? Co ty tu, do diabła, robisz?",
    "1Hero, Andrea doesn’t know I’m here… but… Duncan is looking for you.": "1Hero, Andrea nie wie, że tu jestem… ale… Duncan cię szuka.",
    "Is Duncan coming here?": "Czy Duncan tu idzie?",
    "No… He wants to meet 1Hero in the mansion.": "Nie… Chce spotkać się z 1Hero w rezydencji.",
    "Meet? Are you sure he’s not trying to have me killed?": "Spotkać się? Jesteś pewna, że nie próbuje mnie zabić?",
    "Clearly a trap.": "To oczywista pułapka.",
    "1Hero… He told me something… Something I don’t believe, but…": "1Hero… Powiedział mi coś… Coś, w co nie wierzę, ale…",
    "What did he tell you?": "Co ci powiedział?",
    "Duncan is a crazy person… I know it… But he’s telling me that 1Hero is his son.": "Duncan to wariat… Wiem o tym… Ale wmawia mi, że 1Hero to jego syn.",
    "Ha! What a loon.": "Ha! Co za wariat.",
    "What kind of weird plan is this? What’s his angle?": "Co to za dziwaczny plan? O co mu chodzi?",
    "I’ve been stepping on Duncan’s plans since I stumbled onto them. He’s trying to stop me.": "Plączę szyki Duncanowi, odkąd na nie trafiłem. Próbuje mnie powstrzymać.",
    "Why would this work?": "Czemu miałoby to zadziałać?",
    "I don’t know who my father was. I never met him… I’ve been looking for him since I was a child.": "Nie wiem, kim był mój ojciec. Nigdy go nie poznałem… Szukam go, odkąd byłem dzieckiem.",
    "And Duncan knows this?": "I Duncan o tym wie?",
    "If we’re going back to the rift, how can we sneak past him?": "Jeśli wracamy do szczeliny, jak mamy się obok niego przekraść?",
    "I can get you all inside.": "Mogę was wszystkich wprowadzić do środka.",
    "You’re leaving, Father?": "Wychodzisz, ojcze?",
    "I can’t leave Judy alone.": "Nie mogę zostawić Judy samej.",
    "Well, I’m not babysitting her.": "Cóż, ja nie będę jej pilnować.",
    "Detective Bhatt can help us.": "Detektyw Bhatt może nam pomóc.",
    "I want to help you, 1Hero… I really do.": "Chcę ci pomóc, 1Hero… Naprawdę.",
    "I’m coming with you. I can help you find Madalyn.": "Idę z tobą. Mogę pomóc ci znaleźć Madalyn.",
    "We’re coming, too. I will face her again.": "My też idziemy. Zmierzę się z nią ponownie.",
    "We can kill two birds with one stone… Madalyn and Duncan.": "Upieczemy dwie pieczenie na jednym ogniu… Madalyn i Duncan.",
    "No police this time. We’re on our own.": "Tym razem bez policji. Jesteśmy zdani na siebie.",
    "Just the way I like it.": "Tak jak lubię.",
    "This all sounds very dangerous.": "To wszystko brzmi bardzo niebezpiecznie.",
    "Don’t worry, girl. We’re all very badass. This is what we do.": "Nie martw się, mała. Wszyscy jesteśmy twardzielami. To jest to, co robimy.",
    "I can handle a demon, but a goon with a gun I’m less excited about.": "Z demonem sobie poradzę, ale zbir z pistoletem mniej mnie cieszy.",
    "Leave that to me. I’ll make sure no one sees you.": "Zostaw to mnie. Dopilnuję, żeby nikt was nie zobaczył.",
    "You want me to trust you?": "Chcesz, żebym ci zaufał?",
    "Don’t pretend you don’t. You know this is my wheelhouse.": "Nie udawaj, że nie. Wiesz, że to moja działka.",
    "Fine… We’ll leave as soon as the detective gets here. But no sooner.": "Dobrze… Ruszamy, gdy tylko detektyw tu dotrze. Ale nie wcześniej.",
    "Are you going to meet with Duncan?": "Zamierzasz spotkać się z Duncanem?",
    "It’ll buy us time.": "To kupi nam trochę czasu.",
    "You think he’ll keep you alive?": "Myślisz, że utrzyma cię przy życiu?",
    "I have a hunch he will.": "Mam przeczucie, że tak.",
    "You’re not telling us something.": "Coś przed nami ukrywasz.",
    "Police matters.": "Sprawy policyjne.",
    "Have you returned?": "Wróciłeś?",
    "I can’t stay long.": "Nie mogę zostać na długo.",
    "Are you staying safe?": "Uważasz na siebie?",
    "Everything's fine.": "Wszystko w porządku.",
    "Be careful, 1Hero. We don’t need you getting hurt.": "Uważaj, 1Hero. Nie chcemy, żebyś ucierpiał.",
    "I’ll be safe.": "Będę bezpieczny.",
    "Looking for help?": "Szukasz pomocy?",
    "1Hero? You’re back?": "1Hero? Wróciłeś?",
    "Just trying to work through some problems. Everything’s fine.": "Po prostu staram się rozwiązać pewne problemy. Wszystko w porządku.",
    "No time to waste. I need to grab Zephaniah’s journal.": "Nie ma czasu do stracenia. Muszę zabrać dziennik Zephaniaha.",
    "You’ve got quite a crew in the library. Must be a lot of reading that needs done.": "Masz niezłą ekipę w bibliotece. Pewnie sporo czytania do zrobienia.",
    "We’re slowly figuring things out.": "Powoli to rozgryzamy.",
    "I hope Father Solomon is safe.": "Mam nadzieję, że ojciec Solomon jest bezpieczny.",
    "The old lady has Chloe upset, but I thought she ate a mean pussy.": "Ta stara zdenerwowała Chloe, a myślałam, że nieźle wylizuje cipkę.",
    "Hannah!": "Hannah!",
    "I never want to see Madalyn again. Keep her away from us, 1Hero.": "Nigdy więcej nie chcę widzieć Madalyn. Trzymaj ją od nas z daleka, 1Hero.",
    "Everyone stay near the crucifixes, just to be safe.": "Wszyscy trzymajcie się blisko krucyfiksów, dla bezpieczeństwa.",
    "I’ll make sure the girls behave.": "Dopilnuję, żeby dziewczyny się zachowywały.",
    "So we can’t go into the woods?": "Więc nie możemy iść do lasu?",
    "Hannah! We’re dealing with ghosts and monsters. Now’s not the time for adventure.": "Hannah! Mamy do czynienia z duchami i potworami. Teraz nie czas na przygody.",
    "What happened to your father? Is he still in the mansion?": "Co się stało z twoim ojcem? Wciąż jest w rezydencji?",
    "Duncan is being guarded by Miss Bhatt… We captured him.": "Duncan jest pilnowany przez pannę Bhatt… Schwytano go.",
    "I guess he’s going to jail for a long time.": "Chyba pójdzie siedzieć na długo.",
    "If he’s lucky.": "Jeśli ma szczęście.",
    "A lot of people want him dead.": "Wielu ludzi chce jego śmierci.",
    "He means nothing to me… You were right about him.": "Nic dla mnie nie znaczy… Miałaś rację co do niego.",
    "If you need someone to talk to, I’m here.": "Jeśli potrzebujesz z kimś porozmawiać, jestem tu.",
    "I have seen everything in the church. If there are holy relics, they must be hidden very well.": "Widziałam wszystko w kościele. Jeśli są tam święte relikwie, muszą być bardzo dobrze ukryte.",
    "Arianna!": "Arianna!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=121 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=translations.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=118: raise SystemExit(f'Expected 118, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map121')