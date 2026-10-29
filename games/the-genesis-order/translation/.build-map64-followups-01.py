#!/usr/bin/env python3
"""Build Polish drafts for Map 64 follow-ups (LLM)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CANON = ROOT / 'export-v1/custom_dialogue.jsonl'
OUTPUT = ROOT / 'drafts/custom-dialogue-map64-followups-01.jsonl'
TRANSLATIONS = {
    "The girls are in there. I better leave them alone.": "Dziewczyny są w środku. Lepiej zostawię je w spokoju.",
    "Damn, Carol! Looking good.": "Cholera, Carol! Wyglądasz świetnie.",
    "I thought you’d like my swimsuit, naughty boy.": "Myślałam, że spodoba ci się mój strój kąpielowy, niegrzeczny chłopcze.",
    "I can’t go in now. Carol is in there changing…": "Nie mogę teraz wejść. Carol się przebiera…",
    "Although…": "Chociaż…",
    "I bet she wouldn’t mind if I barged in on her…": "Założę się, że nie miałaby nic przeciwko, gdybym wparowała do niej…",
    "But what if someone sees us?": "Ale co jeśli ktoś nas zobaczy?",
    "Damn… I’m getting horny all of a sudden.": "Cholera… Nagle robię się napalona.",
    "Shit. I’m going for it.": "Cholera. Idę na to.",
    "What the hell was all that about…": "Co to wszystko miało być…",
    "Heather seemed… different…": "Heather wydawała się… inna…",
    "And so did Chloe.": "I Chloe też.",
    "Still not changed?": "Wciąż nie przebrana?",
    "I was just… Waiting for Judy.": "Ja tylko… Czekałam na Judy.",
    "1Hero? What are you doing up here?": "1Hero? Co tu robisz?",
    "Wow! Sister Judy, you look amazing.": "Łał! Siostro Judy, wyglądasz niesamowicie.",
    "I feel almost naked. Is it too much?": "Czuję się prawie nago. Czy to za dużo?",
    "No, it’s very cute.": "Nie, jest bardzo słodki.",
    "I do like cute things.": "Lubię słodkie rzeczy.",
    "I’m going to change into my swimsuit and swim with you two.": "Przebiorę się w strój i popływam z wami dwiema.",
    "Really! That’s wonderful!": "Naprawdę! To wspaniale!",
    "It’ll be nice to get some sun.": "Miło będzie złapać trochę słońca.",
    "I can’t wait to see you…": "Nie mogę się doczekać, by cię zobaczyć…",
    "I mean, I can’t wait to swim with you.": "To znaczy, nie mogę się doczekać pływania z tobą.",
    "I’ll be out soon.": "Zaraz wyjdę.",
    "Hannah! Leave the poor boy alone.": "Hannah! Zostaw biednego chłopaka w spokoju.",
    "It’s okay. She’s impatient. That’s all.": "W porządku. Jest niecierpliwa. To wszystko.",
    "Everyone’s seen me nude a million times. No biggie.": "Każdy widział mnie nago milion razy. Nic wielkiego.",
    "The bathroom’s all yours, Carol.": "Łazienka jest cała twoja, Carol.",
    "Thank you, my dear.": "Dziękuję, kochanie.",
    "Thanks for coming over. I always love seeing you.": "Dzięki, że wpadłaś. Zawsze uwielbiam cię widzieć.",
    "That was quite a scare tonight.": "To był niezły strach dziś wieczorem.",
    "You’re brave to help out. Maybe you’d make a good detective.": "Odważnie pomagasz. Może byłbyś dobrym detektywem.",
    "You’re brave enough, for sure.": "Na pewno jesteś wystarczająco odważna.",
    "Anything to help Sister Judy.": "Wszystko, by pomóc siostrze Judy.",
    "No! It went into Mom’s bedroom!": "Nie! Wbiegło do sypialni mamy!",
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
    if r['id'] in known or r.get('category')!='custom_dialogue' or ctx.get('source_kind')!='map' or ctx.get('map_id')!=64 or ctx.get('translation_policy')=='keep_source_value' or not src or src.lstrip().startswith('/') or not any(c.isalpha() for c in src): continue
    tr=TRANSLATIONS.get(src)
    if tr is None: unmapped.add((ctx.get('event_id'), src)); continue
    r['translation']=tr; rows.append(r)
if unmapped: raise SystemExit('Unmapped '+repr(sorted(unmapped)))
if OUTPUT.exists(): raise SystemExit(f'Refusing {OUTPUT}')
if len(rows)!=36: raise SystemExit(f'Expected 36, got {len(rows)}')
OUTPUT.write_text(''.join(json.dumps(x, ensure_ascii=False, sort_keys=True)+'\n' for x in rows), encoding='utf-8')
print(f'Wrote {len(rows)} Map64')
