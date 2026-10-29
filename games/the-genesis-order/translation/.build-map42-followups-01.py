#!/usr/bin/env python3
"""Build Polish drafts for Map 42 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map42-followups-01.jsonl'
TRANSLATIONS = {
    "What the hell’s going on up here?": "Co się, do cholery, dzieje na górze?",
    "I’m sorry. I was startled.": "Przepraszam. Wystraszyłam się.",
    "Forgive me. Don’t let me get in the way of your work.": "Wybacz. Nie chcę przeszkadzać w pracy.",
    "You serve the master well, young lady.": "Służysz panu dobrze, młoda damo.",
    "It’s just a job.": "To tylko praca.",
    "The master?": "Pan?",
    "The great one. Service brings peace to all.": "Wielki. Służba przynosi pokój wszystkim.",
    "Well… I’m glad you’re at peace.": "Cóż… Cieszę się, że zaznajesz spokoju.",
    "You must fight the temptations of this world, or you will never find true peace.": "Musisz walczyć z pokusami tego świata, inaczej nigdy nie zaznasz prawdziwego spokoju.",
    "Those guys are so creepy.": "Ci faceci są tacy przerażający.",
    "Temptations?": "Pokusami?",
    "I think Madalyn messed with their heads.": "Myślę, że Madalyn namieszała im w głowach.",
    "Ever since I saw her, I’ve gotten sexual vibes from this place.": "Odkąd ją zobaczyłam, czuję seksualne wibracje z tego miejsca.",
    "Sexual vibes?": "Seksualne wibracje?",
    "Perhaps it’s the outfit that she made me wear, but I feel eyes on me…": "Może to przez strój, który kazała mi nosić, ale czuję na sobie spojrzenia…",
    "Lustful eyes.": "Pożądliwe spojrzenia.",
    "From what I've heard about Madalyn, she can have an effect on people.": "Z tego, co słyszałem o Madalyn, potrafi wpływać na ludzi.",
    "Whatever she did, it lingers in this place. I can still feel it.": "Cokolwiek zrobiła, wciąż unosi się w tym miejscu. Wciąż to czuję.",
    "Just how much of this mansion do you have access to?": "Jak dużą część rezydencji masz na oku?",
    "I want you to keep an eye on Lillian.": "Chcę, żebyś miała oko na Lillian.",
    "You don’t trust her?": "Nie ufasz jej?",
    "There’s not much about this place that leaves me with a feeling of trust.": "Niewiele w tym miejscu napawa mnie zaufaniem.",
    "You can say that again. What do you think she’s up to?": "Można tak powiedzieć. Jak myślisz, co kombinuje?",
    "She claims to be ignorant, but I think she has some unlawful connections.": "Twierdzi, że nic nie wie, ale myślę, że ma nielegalne powiązania.",
    "Don’t worry about it. You’re not in danger…": "Nie martw się. Nie grozi ci niebezpieczeństwo…",
    "Charles made some… poor decisions.": "Charles podjął… złe decyzje.",
    "This may have been about money all along.": "Może od początku chodziło o pieniądze.",
    "I don’t see much of the mansion, but where I can, I’ll keep an eye on things.": "Nie widzę wiele z rezydencji, ale gdzie mogę, będę mieć oczy otwarte.",
    "I better leave. I suspect Lillian wouldn't like me lingering around.": "Lepiej już pójdę. Podejrzewam, że Lillian nie spodobałoby się, gdybym się tu kręciła.",
    "If I find anything else interesting, I’ll let you know.": "Jeśli znajdę coś jeszcze ciekawego, dam znać.",
    "Sit with me, 1Hero. I want to hear all about what you know.": "Usiądź ze mną, 1Hero. Chcę usłyszeć wszystko, co wiesz.",
    "Seems we’ve gotten lucky that no one saw us.": "Wygląda na to, że mamy szczęście, że nikt nas nie widział.",
    "Perhaps next time you can show me your bedroom.": "Może następnym razem pokażesz mi swoją sypialnię.",
    "1Hero, I still need your help, but I’m afraid to ask for it.": "1Hero, wciąż potrzebuję twojej pomocy, ale boję się o nią poprosić.",
    "What will become of the amulets?": "Co stanie się z amuletami?",
    "If they’re stolen goods, then they’ll be seized.": "Jeśli to kradzione dobra, zostaną zajęte.",
    "I really want them back in my possession.": "Bardzo chcę je odzyskać.",
    "You’ve inherited a lot from your father. Do you really need them?": "Odziedziczyłaś sporo po ojcu. Naprawdę ich potrzebujesz?",
    "Perhaps I ask too much.": "Może wymagam za wiele.",
    "Look, Lillian. If you’re worried about the Guild, then leave it to me.": "Posłuchaj, Lillian. Jeśli martwisz się Gildią, zostaw to mnie.",
    "They are dying and we are arresting and charging most of the members.": "Umierają i aresztujemy większość członków.",
    "And it looks like soon Duncan will meet his end as well.": "I wygląda na to, że wkrótce Duncan też doczeka końca.",
    "It’s almost over, Lillian. Trust me.": "To prawie koniec, Lillian. Zaufaj mi.",
    "Is someone calling you?": "Ktoś do ciebie dzwoni?",
    "Sorry. I’ve got to take this. It’s work.": "Przepraszam. Muszę odebrać. To praca.",
    "Give me one second.": "Daj mi sekundę.",
    "The Toma Leolo is not a toy.": "Toma Leolo to nie zabawka.",
    "On the contrary, each piece of that idol makes for wonderful… entertainment.": "Wręcz przeciwnie, każdy kawałek tego idola to wspaniała… rozrywka.",
    "Mother would be upset to know you’re using it.": "Matka byłaby zła, gdyby wiedziała, że jej używasz.",
    "You are in no position to comment on Mother’s wishes.": "Nie jesteś w pozycji, by komentować życzenia Matki.",
    "You should be looking for the amulets.": "Powinnaś szukać amuletów.",
    "If I knew where they were, I’d already have them.": "Gdybym wiedziała, gdzie są, już bym je miała.",
    "We’re lucky to still have Kimpet.": "Mamy szczęście, że wciąż mamy Kimpet.",
    "The Guild is not dying like you promised. They have returned to take our place.": "Gildia nie umiera tak, jak obiecywałaś. Wrócili, by zająć nasze miejsce.",
    "There is a stalemate thanks to the detective…": "Mamy pat, dzięki detektywowi…",
    "Once we have what we need, there will be nothing to worry about.": "Gdy będziemy mieć to, czego potrzebujemy, nie będzie czym się martwić.",
    "Mother trusts the detective to find the other two amulets.": "Matka ufa detektywowi, że znajdzie pozostałe dwa amulety.",
    "We don’t need them.": "Nie potrzebujemy ich.",
    "But Mother insists.": "Ale Matka nalega.",
    "We only need the Toma and then everything will fall into place.": "Potrzebujemy tylko Tomy i wtedy wszystko się ułoży.",
    "A great danger we will face if we can not account for all three.": "Czeka nas wielkie niebezpieczeństwo, jeśli nie policzymy wszystkich trzech.",
    "Mother trusts the detective, but if the Guild has returned, perhaps a new strategy is needed.": "Matka ufa detektywowi, ale jeśli Gildia wróciła, może potrzebna jest nowa strategia.",
    "What is it you plan to do?": "Co planujesz zrobić?",
    "I must find the underground lair. There is a path I’ve not yet checked.": "Muszę znaleźć podziemną kryjówkę. Jest ścieżka, której jeszcze nie sprawdziłam.",
    "Another cave entrance?": "Kolejne wejście do jaskini?",
    "Someone is here.": "Ktoś tu jest.",
    "She was here.": "Ona tu była.",
    "What? Like on the couch?": "Co? Na kanapie?",
    "Yeah… Eating herself out.": "Tak… Robiła sobie dobrze oralnie.",
    "Huh? How is that possible?": "Huh? Jak to możliwe?",
    "The Toma… The magic witch idol.": "Toma… Magiczny idolo-wiedźmy.",
    "Are you sure about this, 1Hero? Are you sure you’re not seeing things?": "Jesteś tego pewien, 1Hero? Nie wydaje ci się?",
    "I swear! She had a conversation with one of those sick dudes.": "Przysięgam! Rozmawiała z jednym z tych chorych gości.",
    "So the lepers are in on it too?": "Więc trędowaci też są w to zamieszani?",
    "It’s true…": "To prawda…",
    "That isn’t exactly filling me with a sense of safety.": "Nie napełnia mnie to poczuciem bezpieczeństwa.",
    "I need your help. We need to figure out what’s going on here.": "Potrzebuję twojej pomocy. Musimy rozgryźć, co tu się dzieje.",
    "I’ve been spying on Lillian all week. I’ve never spotted Madalyn or heard anything weird.": "Szpiegowałam Lillian cały tydzień. Nigdy nie zauważyłam Madalyn ani niczego dziwnego.",
    "Keep your ears open. I need to check out the cave.": "Miej uszy otwarte. Muszę sprawdzić jaskinię.",
    "Madalyn is looking for the Guild bunker. I’ve seen it, but I don’t know how far it reaches.": "Madalyn szuka bunkra Gildii. Widziałam go, ale nie wiem, jak daleko sięga.",
    "You’re going to search the Casula caves?": "Zamierzasz przeszukać jaskinie Casula?",
    "Trust me. If anything suspicious happens, give me a call.": "Zaufaj mi. Jeśli wydarzy się coś podejrzanego, zadzwoń.",
    "I’ll keep my eye out, but don’t leave me hanging. If you find anything, tell me.": "Będę mieć oko, ale nie zostawiaj mnie na lodzie. Jeśli coś znajdziesz, powiedz mi.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=42 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=83: raise SystemExit(f'Expected 83, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map42')
