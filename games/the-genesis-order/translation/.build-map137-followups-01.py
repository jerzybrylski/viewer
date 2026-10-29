#!/usr/bin/env python3
"""Build Polish drafts for Map 137 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map137-followups-01.jsonl'
TRANSLATIONS = {
    "Stop! Don’t come closer!": "Stać! Nie podchodź bliżej!",
    "Leave them. We can take them on our own.": "Zostaw ich. Poradzimy sobie sami.",
    "We’ll be back.": "Wrócimy.",
    "God damn it! It’s over!": "Cholera! Koniec!",
    "It’s not over. Bobby will find them.": "To nie koniec. Bobby ich znajdzie.",
    "Where is Kimberly?": "Gdzie jest Kimberly?",
    "She’s on her way.": "Jest w drodze.",
    "We have to find a way out of here. We have to help Bobby find them.": "Musimy znaleźć wyjście stąd. Musimy pomóc Bobby'emu je znaleźć.",
    "They won't be unarmed for long. This was our one chance! Why the hell didn’t you shoot them, 1Hero?": "Niedługo nie będą bez broni. To była nasza jedyna szansa! Czemu, do cholery, nie zastrzeliłeś ich, 1Hero?",
    "We’re doing this the right way. Now look for a way out.": "Robimy to jak należy. Teraz szukaj wyjścia.",
    "There isn’t one, asshole. You need the passcode to unlock the security system.": "Nie ma go, dupku. Potrzebujesz kodu, żeby odblokować system bezpieczeństwa.",
    "Well, what is it?": "No to jaki jest?",
    "A lot of good it will do us! The keypad is outside!": "Wiele nam to da! Klawiatura jest na zewnątrz!",
    "Calm down! You’re not helping.": "Spokojnie! Nie pomagasz.",
    "I was the only one doing what they were supposed to be doing! This is all your fault!": "Ja jedyna robiłam to, co trzeba! To wszystko twoja wina!",
    "Shut up! When this is over, we’ll all be heroes and you’ll be a free woman.": "Zamknij się! Gdy to się skończy, wszyscy będziemy bohaterami, a ty będziesz wolną kobietą.",
    "Forgive me for doubting you, asshole!": "Wybacz, że w ciebie wątpiłam, dupku!",
    "Hey! Get us out of here!": "Hej! Wypuśćcie nas!",
    "The walls are too thick. No one can hear us.": "Ściany są za grube. Nikt nas nie słyszy.",
    "Then we’ll just have to wait for Bobby to get back.": "Więc po prostu poczekamy, aż Bobby wróci.",
    "Shit! This day just keeps getting better and better.": "Cholera! Ten dzień jest coraz lepszy.",
    "Fuck… Stuck in a dungeon with the two loudest complainers.": "Kurwa… Utknąłem w lochu z dwiema najgłośniejszymi marudami.",
    "Just shut up and wait for the officers.": "Po prostu zamknij się i czekaj na funkcjonariuszy.",
    "Where did they go? Where is Duncan?": "Dokąd poszli? Gdzie jest Duncan?",
    "Duncan left. They won't find him.": "Duncan wyszedł. Nie znajdą go.",
    "Don’t ask me. He just got up and left about two hours ago.": "Nie pytaj mnie. Po prostu wstał i wyszedł jakieś dwie godziny temu.",
    "He’s not in the bunker?": "Nie ma go w bunkrze?",
    "Kimberly isn’t going to like that.": "Kimberly to się nie spodoba.",
    "Still thinking we’ll be on the news tonight?": "Nadal myślisz, że będziemy dziś w wiadomościach?",
    "I have hope.": "Mam nadzieję.",
    "You said there's a back entrance?": "Mówiłaś, że jest tylne wejście?",
    "There is, but we don’t use it.": "Jest, ale nie używamy go.",
    "Can you use it?": "Możesz go użyć?",
    "I’ve seen it. They might escape…": "Widziałam je. Mogą uciec…",
    "Don’t worry… I know someone who has the back entrance covered.": "Nie martw się… Znam kogoś, kto ma obstawione tylne wejście.",
    "You’re shitting me… The Guild thief?": "Żartujesz… Złodziejka z Gildii?",
    "I trust her… enough.": "Ufam jej… na tyle.",
    "Fuck is right.": "Racja, kurwa.",
    "Hey! We’ll be fine.": "Hej! Będzie dobrze.",
    "You two fuck… Don’t you?": "Wy dwoje się pieprzycie… Prawda?",
    "I can see it. You two have lots of sexual tension.": "Widać to. Jest między wami mnóstwo napięcia seksualnego.",
    "Come on, Nellie.": "Daj spokój, Nellie.",
    "I don’t blame you. I’ve been fucking his brains out too.": "Nie obwiniam cię. Też wyruchałam go do nieprzytomności.",
    "Why am I not surprised?": "Czemu mnie to nie dziwi?",
    "Who do you like better, 1Hero? The bad girl or the good girl?": "Kogo wolisz, 1Hero? Niegrzeczną dziewczynkę czy grzeczną?",
    "Melissa isn’t a good girl.": "Melissa nie jest grzeczną dziewczynką.",
    "Shut up, 1Hero.": "Zamknij się, 1Hero.",
    "Heh… You could say that.": "Heh… Można tak powiedzieć.",
    "We’re not discussing this.": "Nie będziemy o tym dyskutować.",
    "Quite the cock, isn’t it?": "Niezły kutas, co?",
    "It’s… not bad.": "Jest… niezły.",
    "How about after all this mess, you let me get a head start?": "Może po tym bałaganie pozwolisz mi dać drapaka?",
    "You’re going to run?": "Zamierzasz uciekać?",
    "Better than going back to prison.": "Lepsze to niż wracać do więzienia.",
    "Stop it. You’re not going back to prison. If nothing else, I’ll take the fall.": "Przestań. Nie wrócisz do więzienia. Jeśli trzeba, wezmę winę na siebie.",
    "This operation is never going to end.": "Ta operacja nigdy się nie skończy.",
    "If those goons find an escape, you might be right.": "Jeśli tamci znajdą ucieczkę, możesz mieć rację.",
    "God damn it, ladies. Think positive.": "Cholera, dziewczyny. Myślcie pozytywnie.",
    "Entertain us, 1Hero.": "Zabaw nas, 1Hero.",
    "This isn’t the time for games, Nellie.": "To nie czas na zabawy, Nellie.",
    "For me it is. Now do something entertaining!": "Dla mnie jest. Teraz zrób coś zabawnego!",
    "I can’t take this anymore.": "Nie wytrzymam tego dłużej.",
    "You want entertainment? How about this?": "Chcecie rozrywki? To popatrzcie na to?",
    "I think I know where you learned to use that mouth of yours.": "Chyba wiem, gdzie nauczyłaś się tak używać ust.",
    "Hey! Look!... An air vent.": "Hej! Patrzcie!... Kratka wentylacyjna.",
    "Duh. The place has to have an air supply.": "No jasne. To miejsce musi mieć dopływ powietrza.",
    "Do you think one of you ladies could fit through it?": "Myślicie, że któraś z was zmieści się przez nią?",
    "Not the detective’s fat ass.": "Nie gruba dupa detektywa.",
    "Do you think you can fit, Nellie?": "Myślisz, że dasz radę, Nellie?",
    "I guess it’s worth a shot.": "Chyba warto spróbować.",
    "I’m inside!": "Jestem w środku!",
    "Can you move around?": "Możesz się poruszać?",
    "You can do it, Nellie.": "Dasz radę, Nellie.",
    "Damn my tits.": "Cholera, moje cycki.",
    "Are you stuck?": "Utknęłaś?",
    "Gimme a second!": "Daj mi sekundę!",
    "Haha! I fucking did it!": "Haha! Udało się, kurwa!",
    "Now let us out!": "Teraz nas wypuść!",
    "It's blocked.": "Zablokowane.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=137 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=79: raise SystemExit(f'Expected 79, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map137')
