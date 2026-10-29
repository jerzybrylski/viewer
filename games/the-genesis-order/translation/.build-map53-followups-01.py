#!/usr/bin/env python3
"""Build Polish drafts for Map 53 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map53-followups-01.jsonl'
TRANSLATIONS = {
    "Wow! Get a load of this waterfall!": "Wow! Zobaczcie ten wodospad!",
    "It’s so pretty.": "Jest taki piękny.",
    "Almost looks good enough to swim in.": "Wygląda prawie tak dobrze, że można by się wykąpać.",
    "It does look tempting.": "Rzeczywiście wygląda kusząco.",
    "Skinny dipping!": "Kąpiel na golasa!",
    "Haha. Oh, Hannah. I don’t think we need to get naked to swim.": "Haha. Oj, Hannah. Nie musimy rozbierać się do naga, żeby popływać.",
    "Well, darn. I didn’t bring a swimsuit.": "No kurczę. Nie wzięłam stroju kąpielowego.",
    "Neither did I, and it ain’t stopping me.": "Ja też nie, i wcale mnie to nie powstrzyma.",
    "Come on! Don’t chicken out!": "No dalej! Nie stchórzcie!",
    "Well… She did it.": "Cóż… Ona to zrobiła.",
    "I’ve lost count of how many times I’ve seen her topless.": "Straciłem rachubę, ile razy widziałem ją topless.",
    "The water is warm, y’all! Jump in!": "Woda jest ciepła, ludzie! Wskakujcie!",
    "I guess I could wear my underwear… so my clothes stay dry.": "Chyba mogę zostać w bieliźnie… żeby ubrania zostały suche.",
    "I’ll do it, if you do it.": "Zrobię to, jeśli ty to zrobisz.",
    "Alright! I’m coming.": "Dobra! Idę.",
    "No staring, 1Hero.": "Nie gap się, 1Hero.",
    "Ahh! It’s cold!": "Aaa! Zimna!",
    "Hahaha!": "Hahaha!",
    "Huh? I don’t know if I want to go in now.": "Huh? Nie wiem, czy chcę tam teraz wejść.",
    "You have to! We made a deal.": "Musisz! Umówiliśmy się.",
    "How cold is it?": "Jak zimna jest?",
    "Don’t be such a baby!": "Nie bądź taki beksa!",
    "Eeeek! It’s not warm, that’s for sure.": "Eee! Nie jest ciepła, to na pewno.",
    "It’s fine. Stop your bellyaching.": "Daj spokój. Przestań narzekać.",
    "Maybe I’ll stick to the shallow end.": "Może zostanę na płyciźnie.",
    "Suit yourself. I’m exploring!": "Jak chcesz. Ja idę zwiedzać!",
    "If you’re still cold, Chloe, you should ask 1Hero to coat you in cum…": "Jeśli wciąż ci zimno, Chloe, powinnaś poprosić 1Hero, żeby oblał cię spermą…",
    "Water feels warm now!": "Woda teraz wydaje się ciepła!",
    "I need to get to the bottom of this. Something isn’t right.": "Muszę dojść do sedna. Coś tu nie gra.",
    "I don’t understand. Is it the virus that everyone was talking about on the news?": "Nie rozumiem. Czy to wirus, o którym wszyscy mówili w wiadomościach?",
    "It’s okay, Chloe. I’ll figure it out. I know someone who might be able to identify this artifact I found in the pond.": "Spokojnie, Chloe. Rozgryzę to. Znam kogoś, kto może rozpoznać ten artefakt, który znalazłem w stawie.",
    "You think a magic rock made you shoot a dozen loads?": "Myślisz, że magiczny kamień sprawił, że strzeliłeś tuzin razy?",
    "It sounds silly when you say it like that.": "Głupio to brzmi, gdy tak to ujmujesz.",
    "I can ask Judy about demonic possession.": "Mogę zapytać Judy o opętanie demoniczne.",
    "A virus, a magic rock, and demonic possession…": "Wirus, magiczny kamień i opętanie demoniczne…",
    "What the hell is happening in our town?": "Co się, do cholery, dzieje w naszym mieście?",
    "Mass will be starting soon. I better get going.": "Msza zaraz się zacznie. Lepiej już pójdę.",
    "Already?": "Już?",
    "It’s going to get dark soon. Maybe we should go.": "Zaraz zrobi się ciemno. Może powinniśmy iść.",
    "At least we found a lovely place to swim.": "Przynajmniej znaleźliśmy urocze miejsce do pływania.",
    "It’s our private little hideout!": "To nasza mała prywatna kryjówka!",
    "Sure, Hannah.": "Jasne, Hannah.",
    "I swear I saw something come this way. I should warn Father Solomon that I saw something close by.": "Przysięgam, widziałam, jak coś tędy przeszło. Powinnam ostrzec ojca Solomona, że widziałam coś w pobliżu.",
    "Let me near her. I can do this.": "Pozwól mi podejść do niej. Dam radę.",
    "1Hero, when you see her, toss the chalice…": "1Hero, gdy ją zobaczysz, rzuć kielichem…",
    "If you miss, you’ll only have a split second to react.": "Jeśli spudłujesz, będziesz mieć tylko ułamek sekundy na reakcję.",
    "I’ll be careful not to miss.": "Uważaj, żeby nie spudłować.",
    "I’ll stay close.": "Zostanę blisko.",
    "Is this going to work?": "Czy to zadziała?",
    "She may not even show up. If she’s seen me already, it could be too late.": "Może nawet się nie pojawi. Jeśli już mnie widziała, może być za późno.",
    "Let’s hope she’s not seen you.": "Miejmy nadzieję, że cię nie widziała.",
    "Come, Judy. Stay close to me.": "Chodź, Judy. Trzymaj się blisko mnie.",
    "Go on, 1Hero. Hide in the bushes.": "Dalej, 1Hero. Schowaj się w krzakach.",
    "Are you sure, Chloe?": "Jesteś pewna, Chloe?",
    "Just don’t miss your throw.": "Tylko nie spudłuj rzutu.",
    "Ahh! It’s her!": "Aaa! To ona!",
    "Oh, shit! Wait! I don’t have it ready!": "O cholera! Czekaj! Nie mam gotowego!",
    "Stay back, monster!": "Trzymaj się z daleka, potworze!",
    "1Hero!? What the hell are you doing?": "1Hero!? Co ty, do cholery, robisz?",
    "Get back, demon!": "Odejdź, demonie!",
    "Shoo! Go away!": "Spadaj! Wynocha!",
    "What are you people doing in the woods?": "Co wy ludzie robicie w lesie?",
    "That’s not Madalyn.": "To nie Madalyn.",
    "Nellie!?": "Nellie!?",
    "Brian!?": "Brian!?",
    "Oh, my god! You look like an old man!": "O mój Boże! Wyglądasz jak starzec!",
    "What the hell are you doing at my church?": "Co, do cholery, robisz w moim kościele?",
    "That’s your church!?": "To twój kościół!?",
    "Who is this woman?": "Kim jest ta kobieta?",
    "I’m his ex-wife.": "Jestem jego byłą żoną.",
    "Father?": "Ojcze?",
    "Are you stalking me again?": "Znowu mnie stalkujesz?",
    "I never stalked you, fuckhead.": "Nigdy cię nie stalkowałem, dupku.",
    "Here we go again.": "Zaczyna się od nowa.",
    "How was I supposed to know you owned a church in North Santiva?": "Skąd miałem wiedzieć, że masz kościół w North Santiva?",
    "Sure, Nellie. You just happen to be spying on the very church that I am a part of.": "Jasne, Nellie. Tak się akurat składa, że szpiegujesz kościół, którego jestem częścią.",
    "Get over yourself.": "Przestań sobie schlebiać.",
    "Everybody, calm down.": "Wszyscy, spokój.",
    "1Hero, you’re all wet. You must be freezing.": "1Hero, jesteś cały mokry. Musisz marznąć.",
    "Come on, you two. Let’s get you inside…": "Chodźcie, wy dwoje. Zabiorę was do środka…",
    "You can explain everything to me once we get you dry.": "Wszystko mi wyjaśnicie, gdy się osuszycie.",
    "This day just keeps getting better and better.": "Ten dzień jest coraz lepszy i lepszy.",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=53 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=82: raise SystemExit(f'Expected 82, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map53')
