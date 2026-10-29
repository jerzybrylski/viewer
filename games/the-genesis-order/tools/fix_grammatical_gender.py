#!/usr/bin/env python3
"""Rodzaj gramatyczny w tłumaczeniu TGO PL — mówca, adresat i orzecznik.

Zasada: forma gramatyczna zależy od tego, **kto mówi** (pierwsza osoba), **do
kogo mówi** (druga osoba) i **o kim mówi** (trzecia osoba). Tłumaczenie
powstawało partiami, bez wiedzy o mówcy, więc w tekście mieszały się formy
męskie i żeńskie. To narzędzie przywraca zgodność.

Zakres automatycznej poprawki (``--apply``):

* **pierwsza osoba** — czasowniki (``-łem``/``-łam``, ``-łbym``/``-łabym``)
  oraz orzeczniki po ``jestem/byłem/zostałem/czuję się/będę`` biorą rodzaj mówcy;
* **druga osoba** — to samo dla ``jesteś/byłeś/byłaś/będziesz``, ale **tylko**
  gdy dowód jest w samym zdaniu: wołacz z imieniem (``Hannah!``) albo zwrot do
  ``1Hero``. Obsada sceny bywa myląca — mówca może zwracać się do kogoś, kto
  w tej scenie nie ma kwestii — więc nie zgadujemy na jej podstawie.

Czego narzędzie **nie** robi: nie rusza trzeciej osoby (podmiot bywa domyślny,
coreferencji nie da się rozstrzygnąć bez sceny), kwestii bez znanego mówcy,
rzeczowników w narzędniku (``kościołem``, ``aniołem``) ani orzeczników
rzeczownikowych (``komisarzem``, ``wrogiem``) — kobieta mówi „jestem
komisarzem”, nie „komisarką”. Orzecznik przymiotnikowy zamieniamy tylko wtedy,
gdy przymiotnik nie jest podporządkowany rzeczownikowi (``jestem jedyną osobą``
zostaje — „osoba” jest żeńska niezależnie od mówcy) i gdy forma docelowa już
występuje w korpusie.

Wszystko, czego narzędzie nie rozstrzyga, trafia do ``residual`` w raporcie.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = ROOT / "translation"
DRAFTS = TRANSLATION / "drafts"
REPORT_JSON = TRANSLATION / "reports" / "gender_fix_v1.json"
REPORT_MD = ROOT / "docs" / "GENDER_AUDIT.md"

# Ta sama mapa kodów, co w `build_readalong.py` (pilnuje tego test).
SPEAKERS = {
    "Mc": "Mox", "Ad": "Andrea", "Ar": "Arianna", "Bo": "Bobby",
    "Br": "Brian", "Ca": "Carol", "Ch": "Chloe", "Da": "David",
    "Du": "Duncan", "El": "Ella", "Er": "Erica", "Hn": "Hannah",
    "He": "Heather", "Jo": "Jon", "Ju": "Judy", "Ki": "Kimberly",
    "La": "Larry", "Li": "Lillian", "Me": "Melissa", "Ho": "Zakapturzona postać",
    "Ne": "Nellie", "Ta": "Tasha", "Hr": "Henry", "Di": "Diana",
    "Ob": "Funkcjonariusz B", "Ml": "Madalyn", "Se": "Ochrona",
    "Pl": "Paul", "H1": "Oprych 1", "H2": "Oprych 2",
    "Oa": "Funkcjonariusz A", "Oc": "Funkcjonariusz C",
    "Hw": "Kobieta-popleczniczka", "D1": "Demon 1", "D2": "Demon 2", "D3": "Demon 3",
    "Mo": "Wzmocniony sługa", "Dj": "Demon Judy", "Gn": "Drab",
    "Al": "Alia", "Ll": "Lilith", "Ev": "Evie", "Dm": "Daemalius",
    "Jd": "Sędzia", "Lw": "Prawnik", "Am": "Amulet H.",
    "Si": "Simon", "Sm": "Smithfield", "NPC": "Postać niezależna",
}

FEMALE_SPEAKERS = {
    "Andrea", "Arianna", "Carol", "Chloe", "Diana", "Ella", "Erica", "Evie",
    "Hannah", "Heather", "Judy", "Kimberly", "Lillian", "Madalyn", "Melissa",
    "Nellie", "Tasha", "Alia", "Lilith", "Kobieta-popleczniczka", "Demon Judy",
}
MALE_SPEAKERS = {
    "Mox", "Bobby", "Brian", "David", "Duncan", "Jon", "Larry", "Henry",
    "Paul", "Simon", "Smithfield", "Prawnik", "Oprych 1", "Oprych 2",
    "Daemalius", "Drab", "Wzmocniony sługa",
}

# ── orzeczniki przymiotnikowe: pary rodzajowe spotkane w korpusie ───────────
# Lista jest zamknięta i pochodzi z przeglądu korpusu. Rzeczowniki („fanką”,
# „dziewczyną”, „komisarzem”) są tu celowo pominięte — one nie idą za mówcą.
ADJ_PAIRS = {
    "chory": "chora", "ciasny": "ciasna", "ciepły": "ciepła", "ciężki": "ciężka",
    "cudowny": "cudowna", "czysty": "czysta", "dobry": "dobra",
    "dorosły": "dorosła", "doskonały": "doskonała", "drugi": "druga",
    "duży": "duża", "fajny": "fajna", "gotowy": "gotowa", "godny": "godna",
    "grzeczny": "grzeczna", "głodny": "głodna", "głupi": "głupia",
    "idealny": "idealna", "inny": "inna", "kochany": "kochana",
    "lepszy": "lepsza", "martwy": "martwa", "miły": "miła", "mokry": "mokra",
    "mądry": "mądra", "młodszy": "młodsza", "młody": "młoda",
    "napalony": "napalona", "naprawiony": "naprawiona", "niegrzeczny": "niegrzeczna",
    "niesamowity": "niesamowita", "nieśmiertelny": "nieśmiertelna", "nowy": "nowa",
    "nudny": "nudna", "odważny": "odważna", "ogromny": "ogromna",
    "opętany": "opętana", "ostrożny": "ostrożna", "otwarty": "otwarta",
    "pewien": "pewna", "pewny": "pewna", "piękny": "piękna",
    "podarty": "podarta", "podekscytowany": "podekscytowana", "pomocny": "pomocna",
    "potrzebny": "potrzebna", "powiązany": "powiązana", "prawdziwy": "prawdziwa",
    "przepyszny": "przepyszna", "pyszny": "pyszna", "przeznaczony": "przeznaczona",
    "rozciągnięty": "rozciągnięta", "rozkojarzony": "rozkojarzona",
    "roztrzęsiony": "roztrzęsiona", "samolubny": "samolubna", "samotny": "samotna",
    "seksowny": "seksowna", "silniejszy": "silniejsza", "silny": "silna",
    "skończony": "skończona", "soczysty": "soczysta", "stary": "stara",
    "szalony": "szalona", "szczery": "szczera", "szczęśliwy": "szczęśliwa",
    "szybki": "szybka", "słodki": "słodka", "taki": "taka", "twardy": "twarda",
    "ukryty": "ukryta", "uroczy": "urocza", "uwięziony": "uwięziona",
    "ważny": "ważna", "wdzięczny": "wdzięczna", "widziany": "widziana",
    "wielki": "wielka", "większy": "większa", "winien": "winna",
    "wkurzony": "wkurzona", "wolny": "wolna", "wredny": "wredna",
    "wspaniały": "wspaniała", "wyjątkowy": "wyjątkowa", "wykończony": "wykończona",
    "wściekły": "wściekła", "zabawny": "zabawna", "zadowolony": "zadowolona",
    "zagubiony": "zagubiona", "zainteresowany": "zainteresowana",
    "zajęty": "zajęta", "zakochany": "zakochana", "zamieszany": "zamieszana",
    "zamknięty": "zamknięta", "zaskoczony": "zaskoczona",
    "zdenerwowany": "zdenerwowana", "zdolny": "zdolna", "zmęczony": "zmęczona",
    "związany": "związana", "zły": "zła", "cherlawy": "cherlawa",
    "ładniejszy": "ładniejsza", "ładny": "ładna", "śliczny": "śliczna",
    "śpiący": "śpiąca", "świetny": "świetna", "spostrzegawczy": "spostrzegawcza",
    "pruderyjny": "pruderyjna", "wrażliwy": "wrażliwa",
    "twój": "twoja", "mój": "moja", "swój": "swoja", "cały": "cała",
    "sam": "sama", "jeden": "jedna", "gotów": "gotowa", "rad": "rada",
    "zdrów": "zdrowa", "żonaty": "zamężna", "wdzięczny": "wdzięczna",
}
# kierunek żeński → męski; pierwsze (kanoniczne) pary mają priorytet
for _masc, _fem in list(ADJ_PAIRS.items()):
    ADJ_PAIRS.setdefault(_fem, _masc)

# Rzeczowniki w narzędniku wyglądające jak czas przeszły 1. osoby.
NOUN_INSTRUMENTAL = {
    "aniołem", "ciałem", "diabłem", "duszą", "imieniem", "jabłkiem", "kowadłem",
    "kozłem", "kościołem", "kryształem", "krzesłem", "masłem", "materiałem",
    "mianem", "naczyniem", "narzędziem", "okiem", "piórem", "pomysłem",
    "protokołem", "ramieniem", "sercem", "słowem", "stołem", "sumieniem",
    "szczęściem", "udziałem", "ustępem", "wieczorem", "wnętrzem", "wyborem",
    "wyznaniem", "zapałem", "zdaniem", "ziarnem", "złem", "źródłem", "życiem",
}

# Rzeczowniki żeńskie o osobowym znaczeniu, których mężczyzna nie użyje o sobie.
NOUN_PAIRS_MASC = {
    "detektywką": "detektywem",
    "pracoholiczką": "pracoholikiem",
}

# Czasowniki w czasie teraźniejszym, które kończą się jak forma przeszła.
PRESENT_TENSE = {"działam", "słucham", "mam", "znam", "wychodzę"}

# Tematy, których nie da się zamienić samą końcówką.
STEM_FIXES = {
    "szed": "sz",        # przyszedł → przyszła, wszedł → weszła
    "wzią": "wzię",      # wziął → wzięła
    "przyją": "przyję",  # przyjął → przyjęła
    "obją": "obję",
    "zaczą": "zaczę",
    "począ": "poczę",
}

FRAME_1P = (
    r"(?:nie\s+)?(?:jestem|byłem|byłam|zostałem|zostałam|będę|czuję się|"
    r"czułem się|czułam się|okazałem się|okazałam się|stałem się|stałam się|"
    r"staję się|robię się|wydaję się|zostaję)"
)
FRAME_2P = (
    r"(?:nie\s+)?(?:jesteś|byłeś|byłaś|zostaniesz|będziesz|czujesz się|"
    r"czułeś się|czułaś się|okazałeś się|okazałaś się|stałeś się|stałaś się|"
    r"stajesz się|robisz się|wydajesz się|zostajesz)"
)
FRAME_RE_1P = re.compile(FRAME_1P + r"\b", re.IGNORECASE)
FRAME_RE_2P = re.compile(FRAME_2P + r"\b", re.IGNORECASE)

VERB_1P_M = re.compile(r"\b[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+?(?:łem|łbym)\b")
VERB_1P_F = re.compile(r"\b[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+?(?:łam|łabym)\b")
VERB_2P_M = re.compile(r"\b[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+?(?:łeś|łbyś)\b")
VERB_2P_F = re.compile(r"\b[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+?(?:łaś|łabyś)\b")

WORD_RE = re.compile(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+")
SENTENCE_RE = re.compile(r"[^.!?…]+[.!?…]?", re.MULTILINE)
VOCATIVE_RE = re.compile(r"(?:^|[,!?…]\s*)([A-ZĄĆĘŁŃÓŚŹŻ][\wĄĆĘŁŃÓŚŹŻąćęłńóśźż]*)\s*[,!?]")

FRAME_FILLERS = {
    "w", "we", "z", "ze", "na", "do", "od", "dla", "przy", "po", "za", "o", "u",
    "teraz", "tu", "tutaj", "tak", "bardzo", "trochę", "już", "tylko", "jeszcze",
    "zbyt", "całkiem", "dość", "aż", "prawie", "dziś", "jednak", "kompletnie",
    "kimś", "czymś", "tam", "świetnie", "dobrze", "lepiej", "strasznie",
    "coraz", "nie", "chyba", "zupełnie", "wcale", "ciągle", "nadal", "wciąż",
    "go", "jej", "ich", "jego", "ci", "mi", "cię", "mnie", "się",
    "tego", "to", "tym", "tą", "tę", "te", "ten", "ta", "także", "również",
    "nawet", "przecież", "naprawdę", "zawsze", "nigdy", "zdecydowanie",
}
# Po tych słowach orzecznik nie jest już głową frazy — dalej stoi rzeczownik.
PHRASE_STOP = {"za", "do", "na", "w", "we", "z", "ze", "od", "dla", "przez", "po",
               "że", "by", "żeby", "aby", "bo", "ale", "i", "a", "czy", "jak",
               "gdy", "kiedy", "ponieważ", "więc", "lub", "albo", "niż", "przed"}

FEMALE_NAMES = {
    "Andrea", "Arianna", "Carol", "Chloe", "Diana", "Ella", "Erica", "Evie",
    "Hannah", "Heather", "Judy", "Kimberly", "Lillian", "Madalyn", "Melissa",
    "Nellie", "Tasha", "Alia", "Lilith",
}
MALE_NAMES = {
    "Mox", "Bobby", "Brian", "David", "Duncan", "Jon", "Larry", "Henry",
    "Paul", "Simon", "Smithfield", "Charles", "Wilkes", "Solomon", "Toma",
}
THIRD_PERSON_RE = re.compile(
    r"\b(?:" + "|".join(sorted(FEMALE_NAMES)) + r"|ona)\b[^.?!…]{0,30}?\b\w+(?:ł|li)\b"
)

HERO = "1Hero"
HERO_VOCATIVE_RE = re.compile(r"(?:^|[,!?…]\s*)1Hero\b\s*(?:[,!?…]|$)")


def speaker_of(row: dict[str, Any]) -> str | None:
    context = row.get("context") or {}
    header = context.get("custom_header")
    if not header:
        return None
    for code in re.findall(r"[A-Z][a-z0-9]|[A-Z]{2}", str(header)):
        if code in SPEAKERS:
            return SPEAKERS[code]
    return None


def gender_of(speaker: str | None) -> str | None:
    if speaker in FEMALE_SPEAKERS:
        return "F"
    if speaker in MALE_SPEAKERS:
        return "M"
    return None


def load_rows() -> dict[str, tuple[Path, dict[str, Any]]]:
    """Scalone tłumaczenia: ostatni niepusty wariant wygrywa (jak w merge)."""
    rows: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(DRAFTS.rglob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            record_id = row.get("id")
            if not record_id:
                continue
            if row.get("translation") or record_id not in rows:
                rows[record_id] = (path, row)
    return rows


def build_vocabulary(rows: dict[str, tuple[Path, dict[str, Any]]]) -> set[str]:
    vocab: set[str] = set()
    for _, row in rows.values():
        translation = row.get("translation")
        if translation:
            vocab.update(word.lower() for word in WORD_RE.findall(translation))
    return vocab


def sentence_spans(text: str) -> list[tuple[int, int]]:
    spans = []
    for match in SENTENCE_RE.finditer(text):
        if match.group(0).strip():
            spans.append((match.start(), match.end()))
    return spans


def name_gender(name: str) -> str | None:
    if name in FEMALE_NAMES:
        return "F"
    if name in MALE_NAMES:
        return "M"
    return None


def vocative_gender(sentence: str) -> str | None:
    genders = {name_gender(m.group(1)) for m in VOCATIVE_RE.finditer(sentence)}
    genders.discard(None)
    return genders.pop() if len(genders) == 1 else None


def swap_verb_form(word: str, gender: str, person: str) -> str | None:
    """Zamiana końcówki czasownika; zwraca formę docelową albo ``None``."""
    low = word.lower()
    if low in NOUN_INSTRUMENTAL or low in PRESENT_TENSE:
        return None
    if person == "1":
        pairs = {"łem": "łam", "łam": "łem", "łbym": "łabym", "łabym": "łbym"}
        wrong = ("łem", "łbym") if gender == "F" else ("łam", "łabym")
    else:
        pairs = {"łeś": "łaś", "łaś": "łeś", "łbyś": "łabyś", "łabyś": "łbyś"}
        wrong = ("łeś", "łbyś") if gender == "F" else ("łaś", "łabyś")
    for suffix in wrong:
        if not low.endswith(suffix):
            continue
        base = word[: len(word) - len(suffix)]
        fixed_base = base
        for stem, replacement in STEM_FIXES.items():
            if low.endswith(stem + suffix):
                fixed_base = word[: len(word) - len(stem) - len(suffix)] + replacement
                break
        target = fixed_base + pairs[suffix]
        if word[:1].isupper():
            target = target[:1].upper() + target[1:]
        return target
    return None


def predicate_edits(
    segment: str,
    base_offset: int,
    gender: str,
    person: str,
    vocabulary: set[str],
) -> list[dict[str, Any]]:
    """Orzeczniki przymiotnikowe po ramie ``jestem/jesteś/...``."""
    frame_re = FRAME_RE_1P if person == "1" else FRAME_RE_2P
    edits: list[dict[str, Any]] = []
    for match in frame_re.finditer(segment):
        tail = segment[match.end(): match.end() + 80]
        tail = re.split(r"[.!?…;:,]", tail, maxsplit=1)[0]
        tokens = list(WORD_RE.finditer(tail))[:5]
        converted = False
        skipped = 0
        for index, token in enumerate(tokens):
            word = token.group(0)
            low = word.lower()
            if not converted and low in FRAME_FILLERS:
                continue
            if low in {"jak", "niczym"}:
                break  # porównanie: „jestem jak ciepły bałwan”
            if not converted and low in PHRASE_STOP:
                break
            target_form = ADJ_PAIRS.get(low)
            noun_form = NOUN_PAIRS_MASC.get(low) if gender == "M" else None
            if target_form is None and noun_form is None:
                skipped += 1
                if skipped > 2:
                    break
                continue
            if noun_form is not None:
                target_form = noun_form
            else:
                if gender == "F" and low.endswith("a"):
                    break
                if gender == "M" and not low.endswith("a"):
                    break
            target = target_form.capitalize() if word[:1].isupper() else target_form
            # przymiotnik musi być głową frazy: po nim koniec zdania, spójnik
            # albo przyimek — nie rzeczownik
            following = tokens[index + 1].group(0).lower() if index + 1 < len(tokens) else None
            if following is not None and following not in PHRASE_STOP and following not in ADJ_PAIRS:
                break
            start = match.end() + token.start()
            edits.append(
                {
                    "old": word,
                    "new": target,
                    "kind": f"{person}os_orzecznik",
                    "_start": start + base_offset,
                    "_end": start + base_offset + len(word),
                }
            )
            converted = True
            if following is None or following in PHRASE_STOP or following not in ADJ_PAIRS:
                break
        if converted:
            continue
    return edits


def collect_edits(
    segment: str,
    base_offset: int,
    gender: str,
    person: str,
    vocabulary: set[str],
) -> list[dict[str, Any]]:
    edits: list[dict[str, Any]] = []
    verb_re = (VERB_1P_M if gender == "F" else VERB_1P_F) if person == "1" else (
        VERB_2P_M if gender == "F" else VERB_2P_F
    )
    for match in verb_re.finditer(segment):
        target = swap_verb_form(match.group(0), gender, person)
        if not target or target == match.group(0):
            continue
        if target.lower() not in vocabulary and match.group(0).lower() not in vocabulary:
            continue
        edits.append(
            {
                "old": match.group(0),
                "new": target,
                "kind": f"{person}os_czasownik",
                "_start": match.start() + base_offset,
                "_end": match.end() + base_offset,
            }
        )
    edits += predicate_edits(segment, base_offset, gender, person, vocabulary)
    return edits


def apply_edits(text: str, edits: list[dict[str, Any]]) -> tuple[str, list[dict[str, str]]]:
    accepted: list[dict[str, Any]] = []
    for edit in sorted(edits, key=lambda e: (e["_start"], -e["_end"])):
        if accepted and edit["_start"] < accepted[-1]["_end"]:
            continue
        accepted.append(edit)
    result = text
    for edit in sorted(accepted, key=lambda e: e["_start"], reverse=True):
        result = result[: edit["_start"]] + edit["new"] + result[edit["_end"]:]
    clean = [{k: v for k, v in edit.items() if not k.startswith("_")} for edit in accepted]
    return result, clean


def plan(
    rows: dict[str, tuple[Path, dict[str, Any]]],
    vocabulary: set[str],
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, str]]]]:
    changes: list[dict[str, Any]] = []
    residual: dict[str, list[dict[str, str]]] = defaultdict(list)

    for record_id, (_, row) in rows.items():
        translation = row.get("translation")
        if not translation:
            continue
        speaker = speaker_of(row)
        speaker_gender = gender_of(speaker)
        edits: list[dict[str, Any]] = []
        addressee: str | None = None
        basis = ""
        unresolved_second_person = False

        for start, end in sentence_spans(translation):
            sentence = translation[start:end]
            if speaker_gender:
                edits += collect_edits(sentence, start, speaker_gender, "1", vocabulary)
            sentence_addressee, sentence_basis = vocative_gender(sentence), "wołacz w zdaniu"
            if not sentence_addressee and HERO_VOCATIVE_RE.search(sentence):
                sentence_addressee, sentence_basis = "M", "zwrot do 1Hero (gracz)"
            if sentence_addressee:
                second = collect_edits(sentence, start, sentence_addressee, "2", vocabulary)
                if second:
                    edits += second
                    addressee, basis = sentence_addressee, sentence_basis
            elif (VERB_2P_M.search(sentence) or VERB_2P_F.search(sentence)
                  or FRAME_RE_2P.search(sentence)):
                unresolved_second_person = True

        if speaker_gender is None and (VERB_1P_M.search(translation) or VERB_1P_F.search(translation)
                                       or FRAME_RE_1P.search(translation)):
            residual["bez_znanego_mowcy_z_pierwsza_osoba"].append({"id": record_id, "text": translation})
        if unresolved_second_person:
            residual["druga_osoba_bez_jednoznacznego_adresata"].append({"id": record_id, "text": translation})
        if THIRD_PERSON_RE.search(translation) and not any(
            edit["kind"].startswith("1os") for edit in edits
        ):
            residual["trzecia_osoba_do_przegladu_w_grze"].append({"id": record_id, "text": translation})
        if re.search(r"\b(sam|sama)\b", translation, re.IGNORECASE) and not any(
            edit["old"].lower() in {"sam", "sama"} for edit in edits
        ):
            residual["sam_sama_do_recznego_przegladu"].append({"id": record_id, "text": translation})

        if not edits:
            continue
        text, clean = apply_edits(translation, edits)
        changes.append(
            {
                "id": record_id,
                "speaker": speaker,
                "speaker_gender": speaker_gender,
                "addressee_gender": addressee,
                "addressee_basis": basis,
                "before": translation,
                "after": text,
                "edits": clean,
                "source_text": row.get("source_text"),
                "category": row.get("category"),
            }
        )
    return changes, residual


def apply_changes(changes: list[dict[str, Any]], rows: dict[str, tuple[Path, dict[str, Any]]]) -> int:
    by_file: dict[Path, dict[str, str]] = defaultdict(dict)
    for change in changes:
        path, _ = rows[change["id"]]
        by_file[path][change["id"]] = change["after"]

    written = 0
    for path, replacements in by_file.items():
        out = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                out.append(line)
                continue
            row = json.loads(line)
            new_text = replacements.get(row.get("id"))
            if new_text is not None and row.get("translation") != new_text:
                row["translation"] = new_text
                line = json.dumps(row, ensure_ascii=False)
            out.append(line)
        path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
        written += 1
    return written


# Nazwy klas zmian z wcześniejszego przebiegu (zostają w dzienniku).
KIND_ALIASES = {
    "pierwsza_osoba_czasownik": "1os_czasownik",
    "druga_osoba_czasownik": "2os_czasownik",
    "1_osoba_orzecznik": "1os_orzecznik",
    "2_osoba_orzecznik": "2os_orzecznik",
    "1_osoba_warunkowy": "1os_warunkowy",
    "2_osoba_warunkowy": "2os_warunkowy",
}


def normalize_kinds(changes: list[dict[str, Any]]) -> None:
    for change in changes:
        for edit in change.get("edits", []):
            edit["kind"] = KIND_ALIASES.get(edit["kind"], edit["kind"])


def write_report(
    changes: list[dict[str, Any]],
    residual: dict[str, list[dict[str, str]]],
    path: Path,
) -> dict[str, Any]:
    kinds = Counter()
    for change in changes:
        for edit in change["edits"]:
            kinds[edit["kind"]] += 1
    previous: dict[str, Any] = {}
    if path.exists():
        try:
            previous = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = {}

    # raport jest kumulacyjny: wcześniejsze przebiegi zostają w dzienniku
    merged: dict[str, dict[str, Any]] = {entry["id"]: entry for entry in previous.get("change_log", [])}
    for entry in changes:
        old = merged.get(entry["id"])
        if old:
            entry = {
                **entry,
                "edits": old.get("edits", []) + entry["edits"],
                "before": old.get("before", entry["before"]),
                "passes": sorted(set(old.get("passes", [])) | {"orzeczniki"}),
            }
        else:
            entry = {**entry, "passes": ["orzeczniki"]}
        merged[entry["id"]] = entry
    for entry in merged.values():
        entry.setdefault("passes", ["czasowniki"])

    normalize_kinds(list(merged.values()))
    total_kinds = Counter()
    for entry in merged.values():
        for edit in entry.get("edits", []):
            total_kinds[edit["kind"]] += 1
    report = {
        "records_changed": len(merged),
        "edit_kinds": dict(sorted(total_kinds.items(), key=lambda item: -item[1])),
        "residual": {key: {"count": len(value)} for key, value in sorted(residual.items())},
        "residual_samples": {key: value[:40] for key, value in sorted(residual.items())},
        "change_log": list(merged.values()),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return report


def write_markdown(report: dict[str, Any], residual: dict[str, list[dict[str, str]]], path: Path) -> None:
    labels = {
        "1os_czasownik": "pierwsza osoba — czasownik (przeszły)",
        "1os_orzecznik": "pierwsza osoba — orzecznik przymiotnikowy",
        "1os_warunkowy": "pierwsza osoba — tryb warunkowy (`bym`)",
        "2os_czasownik": "druga osoba — czasownik (przeszły)",
        "2os_orzecznik": "druga osoba — orzecznik przymiotnikowy",
        "2os_warunkowy": "druga osoba — tryb warunkowy (`byś`)",
        "zaimek_sam": "zaimek `sam/sama` w zdaniu mówcy",
    }
    explanations = {
        "bez_znanego_mowcy_z_pierwsza_osoba": "brak mówcy w źródle — nie zgadujemy płci",
        "druga_osoba_bez_jednoznacznego_adresata": "adresat nie wynika ze zdania (brak wołacza i 1Hero)",
        "sam_sama_do_recznego_przegladu": "„sam/sama” odnosi się do podmiotu, nie do mówcy",
        "trzecia_osoba_do_przegladu_w_grze": "imię kobiety lub „ona” w pobliżu formy męskiej — do oceny w scenie",
    }
    kinds = report["edit_kinds"]
    lines = [
        "# Audyt rodzaju gramatycznego — TGO PL",
        "",
        "> Plik generuje `tools/fix_grammatical_gender.py`. Narzędzie nie tłumaczy:",
        "> przywraca zgodność rodzaju z mówcą (pierwsza osoba) i z adresatem (druga osoba),",
        "> a wszystko, czego nie da się rozstrzygnąć bez sceny, odkłada do listy reszty.",
        "",
        "## Podsumowanie",
        "",
        f"- Rekordy zmienione: **{report['records_changed']}**.",
        f"- Zmienione formy: **{sum(kinds.values())}**.",
        "",
        "## Rodzaje zmian",
        "",
        "| Wzorzec | Zmiany |",
        "|---|---:|",
    ]
    for kind, count in kinds.items():
        lines.append(f"| {labels.get(kind, kind)} | {count} |")
    lines += [
        "",
        "## Reszta do przeglądu w grze",
        "",
        "| Klasa | Rekordy | Dlaczego nie automatycznie |",
        "|---|---:|---|",
    ]
    for key, value in report["residual"].items():
        lines.append(f"| `{key}` | {value['count']} | {explanations.get(key, 'wymaga kontekstu')} |")
    lines += [
        "",
        "## Przykłady",
        "",
    ]
    for change in report.get("change_log", [])[:8]:
        lines.append(f"- **{change['speaker']}**: „{change['before']}” → „{change['after']}”")
    lines += [
        "",
        "## Zasady",
        "",
        "- **Pierwsza osoba** — czasownik i orzecznik przymiotnikowy biorą rodzaj mówcy",
        "  ustalonego z `custom_header` (ta sama mapa kodów co w Czytance).",
        "- **Druga osoba** — tylko z dowodem w zdaniu: wołacz z imieniem albo zwrot do `1Hero`.",
        "  Sama obsada sceny nie wystarcza — mówca może zwracać się do kogoś bez kwestii.",
        "- **Trzecia osoba** — nie ruszana automatycznie; podmiot bywa domyślny, a zgadywanie",
        "  coreferencji wprowadzałoby nowe błędy.",
        "- Orzecznik przymiotnikowy zmieniamy tylko wtedy, gdy żaden rzeczownik nim nie rządzi",
        "  („jestem jedyną osobą” zostaje); lista par przymiotnikowych jest zamknięta i przeglądana.",
        "- Rzeczowniki w narzędniku (`kościołem`, `aniołem`) i orzeczniki rzeczownikowe",
        "  (`komisarzem`, `wrogiem`) zachowują własny rodzaj.",
        "",
        "## Pełny dziennik",
        "",
        "Każdą zmianę (przed/po, mówca, adresat, podstawa) zawiera",
        "`translation/reports/gender_fix_v1.json`.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="zapisz zmiany w draftach")
    parser.add_argument("--report", type=Path, default=REPORT_JSON)
    parser.add_argument("--markdown", type=Path, default=REPORT_MD)
    args = parser.parse_args(argv)

    rows = load_rows()
    vocabulary = build_vocabulary(rows)
    changes, residual = plan(rows, vocabulary)

    written = 0
    if args.apply and changes:
        written = apply_changes(changes, rows)

    report = write_report(changes, residual, args.report)
    write_markdown(report, residual, args.markdown)
    print(json.dumps(
        {
            "records_changed": report["records_changed"],
            "edit_kinds": report["edit_kinds"],
            "files_written": written,
            "residual": {key: value["count"] for key, value in report["residual"].items()},
            "applied": bool(args.apply and changes),
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
