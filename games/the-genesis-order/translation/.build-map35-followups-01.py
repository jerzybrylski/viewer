#!/usr/bin/env python3
"""Build Polish drafts for Map 35 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map35-followups-01.jsonl'
TRANSLATIONS = {
    "Please. Have a seat.": "Proszę. Proszę usiąść.",
    "You’re free to leave, but…": "Może pani wyjść, ale…",
    "I only need to ask you a few questions. It won’t take long.": "Mam tylko kilka pytań. To nie potrwa długo.",
    "I’ll do my best to help.": "Postaram się pomóc najlepiej jak potrafię.",
    "You’re right. She is a hard ass.": "Masz rację. Jest nie do wytrzymania.",
    "She doesn’t want to explore the Wilkes case any further.": "Nie chce dalej drążyć sprawy Wilkesa.",
    "What do you think? Do you think Madalyn just wanted money?": "A co pan myśli? Myśli pan, że Madalyn chodziło tylko o pieniądze?",
    "I don’t know. But I’d love to catch her.": "Nie wiem. Ale chciałbym ją dorwać.",
    "Well… If I find anything more, I’ll let you know.": "Cóż… Jeśli znajdę coś więcej, dam znać.",
    "I’ll show you the exit.": "Odprowadzę panią do wyjścia.",
    "Spill it, 1Hero. I want to know everything.": "Wyśpiewaj wszystko, 1Hero. Chcę wiedzieć wszystko.",
    "Who’s interrogating who in this room?": "Kto tu kogo przesłuchuje?",
    "Don’t give me that shit. Are you undercover? Are you working for that guild?...": "Nie wciskaj mi tego kitu. Działasz pod przykrywką? Pracujesz dla tej Gildii?...",
    "Why didn’t you call me yesterday?": "Czemu nie zadzwoniłeś do mnie wczoraj?",
    "Call you? About what?": "Zadzwonić? W jakiej sprawie?",
    "I don’t know… maybe Madalyn… maybe us.": "Nie wiem… może Madalyn… może my.",
    "Are we dating?": "Czy my się spotykamy?",
    "What do you mean? Are you saying there is nothing between us?": "Co masz na myśli? Mówisz, że nic nas nie łączy?",
    "I never said I wanted anything serious. Why are you acting like this?": "Nigdy nie mówiłem, że chcę czegoś poważnego. Czemu tak się zachowujesz?",
    "I thought I could trust you, 1Hero.": "Myślałam, że mogę ci zaufać, 1Hero.",
    "You can trust me. I’ve not lied to you.": "Możesz mi ufać. Nie okłamałem cię.",
    "You’re fucking those girls who came to your house, aren’t you?": "Pieprzysz te laski, które przychodzą do twojego domu, co?",
    "No!... Well, yes… Why do you care? I thought we were cool with that kind of thing.": "Nie!... No tak… A co cię to obchodzi? Myślałem, że nie mamy z tym problemu.",
    "You?...": "Ty?...",
    "What happened to the old guy?": "Co się stało ze starym?",
    "He’s preoccupied at the moment.": "Jest w tej chwili zajęty.",
    "I’ll tell you the same thing I told him. You’re making a mistake.": "Powiem ci to samo, co jemu. Popełniasz błąd.",
    "We’ll see about that…": "Zobaczymy…",
    "Excuse me. But Miss Cole has been cleared to leave.": "Przepraszam. Ale panna Cole została dopuszczona do wyjścia.",
    "I told you.": "Mówiłam przecież.",
    "Any chance I can get the Goblet of Santo Morales back?": "Jest szansa, że odzyskam Puchar Santo Moralesa?",
    "We’re keeping the cup.": "Zatrzymujemy puchar.",
    "You people are annoying as hell.": "Jesteście irytujący jak diabli.",
    "Just be glad you’re not behind bars.": "Ciesz się, że nie siedzisz za kratkami.",
    "Maybe I’ll see you around, 1Hero.": "Może jeszcze się spotkamy, 1Hero.",
    "I don’t get it. How’d you pull this off?": "Nie rozumiem. Jak ci się to udało?",
    "Think about it. You’re a smart guy.": "Pomyśl. Jesteś bystry.",
    "What’s going on here?...": "Co tu się dzieje?...",
    "I’m even more confused than before I talked to her.": "Jestem jeszcze bardziej zagubiony niż zanim z nią rozmawiałem.",
    "1Hero!?": "1Hero!?",
    "What the hell? Get out of here!": "Co jest, do cholery? Wynoś się stąd!",
    "That’s right, 1Hero. I’m your interrogator.": "Zgadza się, 1Hero. Ja cię przesłuchuję.",
    "She’s already been cleared… We need to find Kimura.": "Ona już została oczyszczona… Musimy znaleźć Kimurę.",
    "David… Andrea is leaving the country. She’s the Guild’s leader now.": "David… Andrea wyjeżdża z kraju. Teraz ona przewodzi Gildii.",
    "The rumors have already started circulating.": "Plotki już zaczęły krążyć.",
    "Well… It’s true.": "Cóż… To prawda.",
    "Seems your charisma has no limits.": "Wygląda na to, że twoja charyzma nie zna granic.",
    "You’re free to go. Someone vouched for you.": "Możesz iść. Ktoś za tobą poręczył.",
    "Huh? Who?": "Słucham? Kto?",
    "Believe me… I’m as shocked as you are.": "Uwierz mi… Jestem w takim samym szoku jak ty.",
    "I’m going to fix this.": "Naprawię to.",
    "As long as I don’t have to.": "Byle nie przeze mnie.",
    "Still trying to find Kimura? Good luck.": "Wciąż próbujesz znaleźć Kimurę? Powodzenia.",
    "We have a lot to cover. I hope you’re ready to absorb everything before we have to meet at the Channel 4 skyrise.": "Mamy sporo do omówienia. Mam nadzieję, że jesteś gotowy przyswoić wszystko, zanim spotkamy się w wieżowcu Channel 4.",
    "Lay it on me, Miss Kimura.": "Dawaj, panno Kimura.",
    "As you already know, the Eclipse Guild is falling and soon they will be eradicated.": "Jak już wiesz, Gildia Zaćmienia upada i wkrótce zostanie wykorzeniona.",
    "We’re up to 316 arrests now and suspect only a few dozen more stragglers are left.": "Mamy już 316 aresztowań i podejrzewamy, że zostało tylko kilkudziesięciu maruderów.",
    "Wow. I’m surprised there is any threat at all if the numbers are that low.": "Wow. Dziwię się, że w ogóle istnieje jeszcze jakieś zagrożenie, jeśli liczby są tak niskie.",
    "There isn’t a threat. At least, not anymore.": "Nie ma zagrożenia. Przynajmniej już nie.",
    "Our undercover operations have eliminated most of the members, but that information has to remain between the two of us.": "Nasze operacje pod przykrywką wyeliminowały większość członków, ale ta informacja musi pozostać między nami.",
    "Don’t let it slip, 1Hero. We’re not ready to tell the public about our inside men.": "Nie puść pary z ust, 1Hero. Nie jesteśmy gotowi powiedzieć opinii publicznej o naszych ludziach w środku.",
    "The secret is safe with me.": "Sekret jest bezpieczny.",
    "It’s true that a majority of Guild operations have taken place in this state, but most arrests have been concentrated in the southern counties.": "To prawda, że większość operacji Gildii miała miejsce w tym stanie, ale większość aresztowań skupiła się w południowych hrabstwach.",
    "So we’re in the clear up here in the north?": "Czyli tu, na północy, jesteśmy bezpieczni?",
    "We are now. But we need to convince the public.": "Teraz już tak. Ale musimy przekonać opinię publiczną.",
    "North Santiva will remain untouched by criminal activity.": "North Santiva pozostanie nietknięta działalnością przestępczą.",
    "I’ve followed their every move. The public needs to know that the Guild can not move without us knowing about it.": "Śledziłam każdy ich ruch. Społeczeństwo musi wiedzieć, że Gildia nie może się ruszyć bez naszej wiedzy.",
    "No more shootouts, no more public car chases, all the danger is behind us.": "Koniec ze strzelaninami, koniec z pościgami, całe niebezpieczeństwo za nami.",
    "No more excitement. Got it.": "Koniec z ekscytacją. Rozumiem.",
    "Take this seriously, 1Hero. There are fifteen civilians now dead because of Guild violence.": "Potraktuj to poważnie, 1Hero. Piętnastu cywilów zginęło przez przemoc Gildii.",
    "The cost of their crimes is not merely financial.": "Koszt ich zbrodni to nie tylko pieniądze.",
    "Sorry. I understand.": "Przepraszam. Rozumiem.",
    "Just remember, 1Hero: Over 300 arrests and most isolated in the south.": "Pamiętaj tylko, 1Hero: Ponad 300 aresztowań i większość na południu.",
    "What about Duncan Helmer?": "A co z Duncanem Helmerem?",
    "Don’t worry about him.": "Nie martw się o niego.",
    "Madalyn is also here, and I have reason to believe that Charles Wilkes was a Guild leader too.": "Madalyn też tu jest i mam powody sądzić, że Charles Wilkes również był przywódcą Gildii.",
    "You need to stay out of this case, 1Hero.": "Musisz trzymać się z dala od tej sprawy, 1Hero.",
    "But, Miss Kimura, Charles’ daughter could be in danger.": "Ale, panno Kimura, córka Charlesa może być w niebezpieczeństwie.",
    "If something happens here in North Santiva after we’ve told the public that it’s safe, we’ll look bad.": "Jeśli coś wydarzy się tu, w North Santiva, po tym jak powiedzieliśmy ludziom, że jest bezpiecznie, wyjdziemy na niekompetentnych.",
    "I assure you, 1Hero, nothing will happen.": "Zapewniam cię, 1Hero, nic się nie wydarzy.",
    "Shit. I need to get to the Channel 4 skyrise soon.": "Cholera. Niedługo muszę być w wieżowcu Channel 4.",
    "I’ll be there with you this first time. But after today, you’ll be taking these interviews by yourself.": "Będę tam z tobą tym pierwszym razem. Ale po dziś sam będziesz prowadził te wywiady.",
    "I’m a good judge of character, 1Hero.": "Jestem dobrym sędzią charakterów, 1Hero.",
    "Trust yourself.": "Zaufaj sobie.",
    "The interview starts in two hours. Security will meet you in the lobby.": "Wywiad zaczyna się za dwie godziny. Ochrona spotka się z tobą w holu.",
    "Damn. I’m getting nervous.": "Cholera. Zaczynam się denerwować.",
    "I should follow Andrea’s lead.": "Powinienem podążać za Andreą.",
    "I have a rigging cable. Perhaps I can attach this hook and make a grapple.": "Mam linę montażową. Może uda mi się przymocować hak i zrobić kotwiczkę.",
    "My office, 1Hero! Now!": "Do mojego biura, 1Hero! Teraz!",
    "I’m sorry, 1Hero. It was hot in the moment, but now…": "Przepraszam, 1Hero. Poniosło nas, ale teraz…",
    "Don’t worry. I’ll handle this.": "Nie martw się. Ja to załatwię.",
    "Are you kidding me? She’s going to fire you.": "Żartujesz? Ona cię wyleje.",
    "Not necessarily.": "Niekoniecznie.",
    "Why? You’re fucked.": "Dlaczego? Masz przechlapane.",
    "I have the commissioner on my side.": "Mam komisarza po swojej stronie.",
    "I’ll explain everything later. For now, I need to talk to Melissa.": "Wyjaśnię wszystko później. Na razie muszę porozmawiać z Melissą.",
    "Good luck, 1Hero…": "Powodzenia, 1Hero…",
    "Call me later.": "Zadzwoń później.",
    "Shit! Maybe I can blame it on that fake virus.": "Cholera! Może zwalę to na tego fałszywego wirusa.",
    "What have I gotten myself into now?": "W co ja się znowu wpakowałem?",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=35 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=100: raise SystemExit(f'Expected 100, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map35')
