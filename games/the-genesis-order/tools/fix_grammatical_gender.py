#!/usr/bin/env python3
"""Wymusza zgodność rodzaju gramatycznego z płcią mówcy i adresata.

Polski oznacza rodzaj w czasie przeszłym i w orzeczeniu imiennym. Tłumaczenie
powstało bez wiedzy o tym, kto wypowiada daną kwestię, więc w korpusie mieszają
się formy męskie i żeńskie. To narzędzie naprawia wyłącznie formy, których
rodzaj da się ustalić z danych gry:

* **pierwsza osoba** — rodzaj bierze się z mówcy (`context.custom_header` →
  mapa kodów mówcy, ta sama co w `build_readalong.py`);
* **druga osoba** — rodzaj bierze się z adresata; przyjmujemy go tylko wtedy,
  gdy w scenie (to samo źródło + mapa/event/strona) **wszyscy pozostali
  mówcy o znanej płci są tej samej płci**;
* **trzecia osoba** — świadomie pominięta. Podmiot bywa domyślny, a zgadywanie
  coreferencji wprowadzałoby błędy; skan trafia do raportu jako materiał do QA.

Narzędzie nie zmienia `source_text`, nie rusza rekordów bez tłumaczenia i nie
dotyka plików gry. Zmiany trafiają wyłącznie do `translation` w draftach.
Uruchamiaj `--check` przed `--fix`; drugi przebieg `--fix` musi dać zero zmian.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[3]
GAME_ROOT = REPO_ROOT / "games" / "the-genesis-order"
DRAFTS = GAME_ROOT / "translation" / "drafts"
REPORT_JSON = GAME_ROOT / "translation" / "reports" / "gender_fix_v1.json"
REPORT_MD = GAME_ROOT / "docs" / "GENDER_AUDIT.md"

# Kopia mapy z build_readalong.py; test pilnuje, żeby obie pozostały identyczne.
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

HERO_NAME = "Mox"
NARRATOR = "Narrator / mówca nieustalony"

FEMALE_SPEAKERS = {
    "Andrea", "Arianna", "Carol", "Chloe", "Diana", "Ella", "Erica", "Evie",
    "Hannah", "Heather", "Judy", "Kimberly", "Lillian", "Madalyn", "Melissa",
    "Nellie", "Tasha", "Alia", "Lilith", "Demon Judy", "Kobieta-popleczniczka",
}
MALE_SPEAKERS = {
    "Mox", "Bobby", "Brian", "David", "Duncan", "Jon", "Larry", "Henry",
    "Paul", "Simon", "Smithfield", "Daemalius", "Oprych 1", "Oprych 2",
    "Prawnik", "Drab",
}

# Rzeczowniki w narzędniku kończące się tak samo jak czas przeszły 1. os.
NOUN_NOT_VERB = {
    "aniołem", "ciałem", "diabłem", "kowadłem", "kozłem", "kościołem",
    "kryształem", "masłem", "materiałem", "pomysłem", "protokołem", "stołem",
    "tyłem", "udziałem", "zapałem", "złem", "źródłem",
}
# Czas teraźniejszy, nie przeszły — rodzaju nie ma.
PRESENT_NOT_PAST = {"działam"}

# Orzecznik po „jestem / jesteś / czuję się…”. Tylko pary potwierdzone w korpusie
# plus nieregularne, których nie da się wyprowadzić regułą końcówki.
ADJ_PAIRS = {
    "aresztowany": "aresztowana", "bezpieczny": "bezpieczna", "bogaty": "bogata",
    "dobry": "dobra", "doskonały": "doskonała", "dumny": "dumna",
    "fałszywy": "fałszywa", "głodny": "głodna", "głupi": "głupia",
    "gotowy": "gotowa", "gotów": "gotowa", "idealny": "idealna",
    "jedyny": "jedyna", "leniwy": "leniwa", "mały": "mała",
    "martwy": "martwa", "mądry": "mądra", "młody": "młoda",
    "możliwy": "możliwa", "nagi": "naga", "napalony": "napalona",
    "następny": "następna", "nierozważny": "nierozważna",
    "niegrzeczny": "niegrzeczna", "niewinny": "niewinna",
    "oddany": "oddana", "odważny": "odważna", "ostatni": "ostatnia",
    "pewien": "pewna", "pewny": "pewna", "pierwszy": "pierwsza",
    "pijany": "pijana", "piękny": "piękna", "podekscytowany": "podekscytowana",
    "poważny": "poważna", "prawdziwy": "prawdziwa",
    "przerażony": "przerażona", "przygotowany": "przygotowana",
    "przystojny": "przystojna", "pijany": "pijana", "rad": "rada",
    "sam": "sama", "samolubny": "samolubna", "samotny": "samotna",
    "seksowny": "seksowna", "silny": "silna", "skuty": "skuta",
    "spóźniony": "spóźniona", "sprytny": "sprytna", "stary": "stara",
    "szczęśliwy": "szczęśliwa", "śliczny": "śliczna", "świetny": "świetna",
    "twardy": "twarda", "uparty": "uparta", "uroczy": "urocza",
    "uwięziony": "uwięziona", "uzależniony": "uzależniona",
    "ważny": "ważna", "wdzięczny": "wdzięczna", "winien": "winna",
    "winny": "winna", "wkurzony": "wkurzona", "wolny": "wolna",
    "wybrany": "wybrana", "wykończony": "wykończona",
    "wystraszony": "wystraszona", "wściekły": "wściekła",
    "zadowolony": "zadowolona", "zainteresowany": "zainteresowana",
    "zajęty": "zajęta", "zakochany": "zakochana", "zamieszany": "zamieszana",
    "zaskoczony": "zaskoczona", "zawiedziony": "zawiedziona",
    "zdenerwowany": "zdenerwowana", "zdrowy": "zdrowa",
    "zdziwiony": "zdziwiona", "zmęczony": "zmęczona",
    "zrozpaczony": "zrozpaczona", "żonaty": "zamężna",
    "taki": "taka", "jaki": "jaka", "tamten": "tamta",
}
ADJ_FEM_TO_MASC = {}
for _m, _f in ADJ_PAIRS.items():
    ADJ_FEM_TO_MASC.setdefault(_f, _m)

# Nieregularne formy 3. os. dla konstrukcji „bym/byś + czasownik”.
VERB3_MASC_TO_FEM = {
    "był": "była", "miał": "miała", "mógł": "mogła", "chciał": "chciała",
    "szedł": "szła", "wszedł": "weszła", "wyszedł": "wyszła",
    "przyszedł": "przyszła", "odszedł": "odeszła", "podszedł": "podeszła",
    "doszedł": "doszła", "zszedł": "zszła", "wziął": "wzięła",
    "zaczął": "zaczęła", "zajął": "zajęła", "jął": "jęła",
    "stanął": "stanęła", "wstał": "wstała", "spadł": "spadła",
    "jadł": "jadła", "wiedział": "wiedziała", "widział": "widziała",
    "usłyszał": "usłyszała", "zobaczył": "zobaczyła", "zrobił": "zrobiła",
    "powiedział": "powiedziała", "poszedł": "poszła", "przyszedł": "przyszła",
    "został": "została", "znalazł": "znalazła", "cierpiał": "cierpiała",
    "spuścił": "spuściła", "zerżnął": "zerżnęła", "poznał": "poznała",
    "trzymał": "trzymała", "dostał": "dostała", "zemdlał": "zemdlała",
    "wyprał": "wyprała", "possał": "possała", "leżał": "leżała",
    "wrócił": "wróciła", "przestał": "przestała", "pokrył": "pokryła",
    "posunął": "posunęła", "zabił": "zabiła", "ukradł": "ukradła",
    "porozmawiał": "porozmawiała", "wydał": "wydała", "przemówił": "przemówiła",
    "użył": "użyła", "dotarł": "dotarła", "robił": "robiła",
    "strzelił": "strzeliła", "wspiął": "wspięła", "namówił": "namówiła",
    "towarzyszył": "towarzyszyła", "mieszał": "mieszała",
}

COPULA = (
    r"(?:jestem|byłem|byłam|czuję się|czułem się|czułam się|stałem się|"
    r"stałam się|zostałem|zostałam|zostaję|staję się|"
    r"jesteś|byłeś|byłaś|czujesz się|czułeś się|czułaś się|stałeś się|"
    r"stałaś się|zostałeś|zostałaś|stajesz się|zostajesz)"
)

def has_masculine_vocative(text: str) -> bool:
    for match in re.finditer(r"\b([A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+)\b", text):
        if match.group(1).lower() in MASCULINE_VOCATIVES:
            return True
    return False


def gender_of(speaker: str) -> str | None:
    if speaker in FEMALE_SPEAKERS:
        return "F"
    if speaker in MALE_SPEAKERS:
        return "M"
    return None


def speaker_for(row: dict[str, Any]) -> str:
    """Ta sama logika co w build_readalong.speaker_for (bez zależności od buildera)."""
    context = row.get("context") or {}
    if row.get("category") == "custom_dialogue":
        header = str(context.get("custom_header") or "")
        if header == "I can’t be wasting time" and context.get("map_id") == 3 and context.get("event_id") in range(1, 17):
            return HERO_NAME
        if header == "NPC":
            return "Postać niezależna"
        match = re.match(r"^@?([A-Z][a-z]|[A-Z]\d)", header)
        if match:
            prefix = match.group(1)
            if prefix in SPEAKERS:
                return SPEAKERS[prefix]
            return f"Mówca nieustalony ({prefix})"
        return "Mówca nieustalony"
    speaker = context.get("speaker")
    if speaker:
        return str(speaker)
    header = context.get("message_header") or {}
    face = header.get("faceName")
    if face:
        return str(face)
    return NARRATOR


def scene_key(row: dict[str, Any]) -> tuple[Any, ...]:
    context = row.get("context") or {}
    return (
        context.get("source_kind"),
        context.get("map_id"),
        context.get("event_id"),
        context.get("page_number"),
    )


def load_rows() -> list[dict[str, Any]]:
    """Rekordy unikalne po `id`; wygrywa ostatnie niepuste tłumaczenie.

    Partie draftów bywają nakładkowe: ten sam `id` może wystąpić w kilku
    plikach, a scalanie bierze ostatnią niepustą wartość. Analiza musi widzieć
    dokładnie to, co zobaczy merge, inaczej liczniki i podmiany się rozjadą.
    """
    by_id: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for path in sorted(DRAFTS.rglob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            rid = row["id"]
            previous = by_id.get(rid)
            if previous is None:
                order.append(rid)
                by_id[rid] = row
            elif (row.get("translation") or "").strip():
                by_id[rid] = row
    return [by_id[rid] for rid in order]


def scene_index(rows: Iterable[dict[str, Any]]) -> dict[tuple[Any, ...], list[dict[str, Any]]]:
    scenes: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        scenes[scene_key(row)].append(row)
    for group in scenes.values():
        group.sort(key=lambda r: ((r.get("context") or {}).get("command_index") or 0, r.get("id") or ""))
    return scenes


def addressee_gender(scene: list[dict[str, Any]], row: dict[str, Any]) -> tuple[str | None, str]:
    """Rodzaj adresata, jeśli wszyscy pozostali mówcy sceny mają jedną płeć."""
    speaker = speaker_for(row)
    others = {
        gender_of(speaker_for(other))
        for other in scene
        if speaker_for(other) != speaker
    }
    others.discard(None)
    if len(others) == 1:
        return others.pop(), "jednolita płeć pozostałych mówców sceny"
    if not others:
        return None, "brak innych mówców o znanej płci"
    return None, "scena mieszana lub nieustalona"


def _replace_suffix(word: str, old: str, new: str) -> str:
    return word[: -len(old)] + new if word.endswith(old) else word


# Tematy nieregularne: „iść” zmienia rdzeń (szedł → szła), a czasowniki na -ąć
# mają oboczność ą/ę (wziąłem → wzięłam).
# „we-” i „ze-” zmieniają temat inaczej niż pozostałe złożenia „iść”:
# weszłam → wszedłem, zeszła → zszedł. Muszą być przed regułą ogólną.
IRREGULAR_OVERRIDES = {
    "wszedłem": "weszłam", "weszłam": "wszedłem",
    "wszedłeś": "weszłaś", "weszłaś": "wszedłeś",
    "zszedłem": "zeszłam", "zeszłam": "zszedłem",
    "zszedłeś": "zeszłaś", "zeszłaś": "zszedłeś",
}
THIRD_PERSON_OVERRIDES = {
    "wszedł": "weszła", "weszła": "wszedł",
    "zszedł": "zeszła", "zeszła": "zszedł",
}

IRREGULAR_1 = (
    ("szedłem", "szłam"), ("szedłeś", "szłaś"),
    ("szedłbym", "szłabym"), ("szedłbyś", "szłabyś"),
    ("ąłem", "ęłam"), ("ąłeś", "ęłaś"),
    ("ąłbym", "ęłabym"), ("ąłbyś", "ęłabyś"),
)
IRREGULAR_1_REVERSE = tuple((new, old) for old, new in IRREGULAR_1[:2])
IRREGULAR_1_REVERSE += (("ęłam", "ąłem"), ("ęłaś", "ąłeś"))
IRREGULAR_1_REVERSE += (("ęłabym", "ąłbym"), ("ęłabyś", "ąłbyś"))


def _first_person_forms(word: str, gender: str) -> str:
    """Zamienia 1. osobę na rodzaj; obsługuje tematy nieregularne."""
    if word.lower() in IRREGULAR_OVERRIDES:
        target = IRREGULAR_OVERRIDES[word.lower()]
        return target.capitalize() if word[0].isupper() else target
    table = IRREGULAR_1 if gender == "F" else IRREGULAR_1_REVERSE
    for old, new in table:
        if word.endswith(old):
            return word[: -len(old)] + new
    if gender == "F":
        return _replace_suffix(word, "łbym", "łabym") if word.endswith("łbym") else _replace_suffix(word, "łem", "łam")
    return _replace_suffix(word, "łabym", "łbym") if word.endswith("łabym") else _replace_suffix(word, "łam", "łem")


def _second_person_forms(word: str, gender: str) -> str:
    if word.lower() in IRREGULAR_OVERRIDES:
        target = IRREGULAR_OVERRIDES[word.lower()]
        return target.capitalize() if word[0].isupper() else target
    table = IRREGULAR_1 if gender == "F" else IRREGULAR_1_REVERSE
    for old, new in table:
        if word.endswith(old):
            return word[: -len(old)] + new
    if gender == "F":
        return _replace_suffix(word, "łbyś", "łabyś") if word.endswith("łbyś") else _replace_suffix(word, "łeś", "łaś")
    return _replace_suffix(word, "łabyś", "łbyś") if word.endswith("łabyś") else _replace_suffix(word, "łaś", "łeś")


def first_person_edits(text: str, gender: str) -> list[tuple[int, int, str, str]]:
    """Zamienia 1. osobę na rodzaj mówcy. Zwraca (start, end, nowy, kategoria)."""
    edits: list[tuple[int, int, str, str]] = []
    if gender == "F":
        for match in re.finditer(r"\b[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+(?:łem|łbym)\b", text):
            word = match.group(0)
            if word.lower() in NOUN_NOT_VERB:
                continue
            edits.append((match.start(), match.end(), _first_person_forms(word, "F"), "pierwsza_osoba_czasownik"))
    else:
        for match in re.finditer(r"\b[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+(?:łam|łabym)\b", text):
            word = match.group(0)
            if word.lower() in PRESENT_NOT_PAST:
                continue
            edits.append((match.start(), match.end(), _first_person_forms(word, "M"), "pierwsza_osoba_czasownik"))
    return edits


def second_person_edits(text: str, gender: str) -> list[tuple[int, int, str, str]]:
    edits: list[tuple[int, int, str, str]] = []
    if gender == "F":
        for match in re.finditer(r"\b[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+(?:łeś|łbyś)\b", text):
            word = match.group(0)
            edits.append((match.start(), match.end(), _second_person_forms(word, "F"), "druga_osoba_czasownik"))
    else:
        for match in re.finditer(r"\b[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+(?:łaś|łabyś)\b", text):
            word = match.group(0)
            edits.append((match.start(), match.end(), _second_person_forms(word, "M"), "druga_osoba_czasownik"))
    return edits


SKIP_TOKENS = {
    "tak", "bardzo", "trochę", "zbyt", "cholernie", "niezbyt", "całkiem",
    "nadal", "jeszcze", "już", "chyba", "po", "prostu", "coraz", "bardziej",
    "mniej", "niż", "jakoś", "strasznie", "okropnie", "nieco", "wyjątkowo",
    "szczególnie", "niesamowicie", "piekielnie", "diabelnie", "zawsze",
    "ciągle", "wciąż", "jeszcze", "równie", "tak", "sobie", "się", "teraz",
}


def _adjective_target(token: str, gender: str) -> str | None:
    """Forma przeciwnej płci: słownik + stopień wyższy („młodsza” → „młodszy”)."""
    lower = token.lower()
    if gender == "F":
        if lower in ADJ_PAIRS:
            return ADJ_PAIRS[lower]
        if lower.endswith("szy"):
            return lower[:-3] + "sza"
        return None
    if lower in ADJ_FEM_TO_MASC:
        return ADJ_FEM_TO_MASC[lower]
    if lower.endswith("sza"):
        return lower[:-3] + "szy"
    return None


def predicate_chain_edits(text: str, start: int, gender: str, kind: str) -> list[tuple[int, int, str, str]]:
    """Orzecznik po łączniku: „taki/a”, przysłówki, potem przymiotnik.

    Łańcuch jest potrzebny, bo „Jestem taka wolna” ma rodzaj w dwóch słowach.
    Zatrzymujemy się na przecinku lub na pierwszym słowie spoza słownika, żeby
    nie sięgać do dalszej części zdania, która może opisywać coś innego.
    """
    edits: list[tuple[int, int, str, str]] = []
    converted = 0
    for match in re.finditer(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+|[.,;:!?…]", text[start:start + 90]):
        token = match.group(0)
        if token in ".,;:!?":
            break
        if token == "…":
            continue
        target = _adjective_target(token, gender)
        if target is not None:
            replacement = target.capitalize() if token[0].isupper() else target
            if replacement != token:
                edits.append((start + match.start(), start + match.end(), replacement, kind))
                converted += 1
            if converted >= 3:
                break
            continue
        if token.lower() in SKIP_TOKENS:
            continue
        break
    return edits


def adjective_edits(text: str, gender: str, persons: str) -> list[tuple[int, int, str, str]]:
    """Orzecznik po „jestem / jesteś / czuję się…”; persons: '1' albo '2'."""
    frames = {
        "1": r"(?:jestem|czuję się|stałem się|stałam się|zostałem|zostałam|zostaję|staję się)",
        "2": r"(?:jesteś|czujesz się|stałeś się|stałaś się|zostałeś|zostałaś|stajesz się|zostajesz)",
    }[persons]
    edits: list[tuple[int, int, str, str]] = []
    for match in re.finditer(rf"\b{frames}\b", text, re.IGNORECASE):
        edits += predicate_chain_edits(text, match.end(), gender, f"{persons}_osoba_orzecznik")
    return edits


CONDITIONAL_PRONOUNS = (
    "bym", "byś", "żebym", "żebyś", "abym", "abyś", "gdybym", "gdybyś",
    "bylebym", "bylebyś", "iżbym", "iżbyś", "ażebym", "ażebyś",
)
CONDITIONAL_SKIP = {
    "nie", "już", "tak", "sobie", "się", "wreszcie", "wtedy", "też", "jednak",
    "w", "końcu", "przecież", "chyba", "nawet", "tam", "tu", "tutaj", "znowu",
    "znów", "jeszcze", "może", "pewnie", "właśnie", "także", "zbyt", "bardzo",
    "trochę", "lepiej", "gorzej", "chętnie", "również", "jedynie", "tylko",
}
MASC_IRREGULAR = {"mogła": "mógł"}


def third_person_to_fem(word: str) -> str | None:
    low = word.lower()
    if low in THIRD_PERSON_OVERRIDES:
        return THIRD_PERSON_OVERRIDES[low]
    if low in VERB3_MASC_TO_FEM:
        return VERB3_MASC_TO_FEM[low]
    if low.endswith("szedł"):
        return low[: -len("szedł")] + "szła"
    if low.endswith("ął"):
        return low[:-2] + "ęła"
    if low.endswith("ał"):
        return low[:-2] + "ała"
    if low.endswith(("ił", "ył", "uł")):
        return low[:-1] + "ła"
    return None


def third_person_to_masc(word: str) -> str | None:
    low = word.lower()
    if low in THIRD_PERSON_OVERRIDES:
        return THIRD_PERSON_OVERRIDES[low]
    if low in MASC_IRREGULAR:
        return MASC_IRREGULAR[low]
    if low.endswith("szła"):
        return low[: -len("szła")] + "szedł"
    if low.endswith("ęła"):
        return low[:-3] + "ął"
    if low.endswith("ła"):
        return low[:-1]  # „wiedziała” → „wiedział”, „zrobiła” → „zrobił”
    return None


def conditional_edits(text: str, gender: str, persons: str) -> list[tuple[int, int, str, str]]:
    """„bym/byś + czasownik”: rodzaj siedzi w formie 3. osoby po zaimku.

    Obsługuje też złożenia („Bylebym nie musiała”, „gdybyś powiedział”) i
    przysłówki między zaimkiem a czasownikiem.
    """
    # 1. osoba: wyłącznie formy na -m (bym, żebym, gdybym…). Formy na -ś
    # dotyczą adresata, więc mieszanie ich z rodzajem mówcy dawało błędy.
    if persons == "1":
        pronouns = tuple(p for p in CONDITIONAL_PRONOUNS if p.endswith("m"))
    else:
        pronouns = tuple(p for p in CONDITIONAL_PRONOUNS if p.endswith("ś"))
    pattern = r"\b(" + "|".join(sorted(pronouns, key=len, reverse=True)) + r")\b"
    edits: list[tuple[int, int, str, str]] = []
    for match in re.finditer(pattern, text, re.IGNORECASE):
        cursor = match.end()
        converted_at = None
        for _ in range(5):
            token = re.compile(r"\s*([A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+)").match(text, cursor)
            if not token:
                break
            word = token.group(1)
            lowered = word.lower()
            if lowered in CONDITIONAL_SKIP:
                cursor = token.end()
                continue
            if gender == "F" and lowered.endswith("ł") and not lowered.endswith("ł" + "a"):
                target = third_person_to_fem(word)
            elif gender == "M" and lowered.endswith("ła"):
                target = third_person_to_masc(word)
            else:
                target = None
            if target is None:
                break
            replacement = target.capitalize() if word[0].isupper() else target
            edits.append((token.start(1), token.end(1), replacement, f"{persons}_osoba_warunkowy"))
            if replacement != word:
                edits += predicate_chain_edits(text, token.end(1), gender, f"{persons}_osoba_warunkowy")
            converted_at = token.end(1)
            break
        if converted_at is None:
            continue
    return edits


FEMALE_NAMES = sorted(
    {name for name in SPEAKERS.values() if name in FEMALE_SPEAKERS}
    | {"Andrea", "Arianna", "Carol", "Chloe", "Diana", "Ella", "Erica", "Evie",
       "Hannah", "Heather", "Judy", "Kimberly", "Lillian", "Madalyn", "Melissa",
       "Nellie", "Tasha", "Alia", "Lilith"}
)
MALE_NAMES = sorted(
    {name for name in SPEAKERS.values() if name in MALE_SPEAKERS}
    | {"David", "Bobby", "Brian", "Jon", "Duncan", "Larry", "Henry", "Paul"}
)

# Wołacze rodzaju męskiego: jeśli taki wyraz pada w kwestii, adresat bywa
# mężczyzną (np. „Jesteś wolny, pająku”), mimo że obsada sceny jest żeńska.
MASCULINE_VOCATIVES = {
    "pająku", "chłopcze", "synu", "bracie", "ojcze", "panie", "doktorze",
    "kapitanie", "szefie", "kolego", "draniu", "dupku", "gnojku", "mistrzu",
    "księże", "chłopaku", "typie", "śmieciu", "bękarcie", "zdrajco", "tchórzu",
    "głupcze", "idioto", "kretynie", "debilu", "palancie", "ciulu", "sukinsynu",
    "skurwysynu", "syneczku",
}


def clause_bounds(text: str, position: int) -> tuple[int, int]:
    boundaries = ".,!?…;:"
    start = max((text.rfind(char, 0, position) for char in boundaries), default=-1) + 1
    ends = [index for index in (text.find(char, position) for char in boundaries) if index != -1]
    return start, (min(ends) if ends else len(text))


def self_pronoun_edits(text: str, gender: str, anchors: list[tuple[int, int]]) -> list[tuple[int, int, str, str]]:
    """„sam/sama” w tym samym zdaniu, w którym zmieniliśmy czasownik mówcy.

    Poza takim zdaniem „sam” bywa zgodne z innym rzeczownikiem („ten sam
    problem”, „sama pani komisarz”), więc tam go nie ruszamy — trafia do raportu.
    """
    target = "sama" if gender == "F" else "sam"
    edits: list[tuple[int, int, str, str]] = []
    for match in re.finditer(r"\b(sam|sama)\b", text):
        if match.group(0) == target:
            continue
        start, end = clause_bounds(text, match.start())
        if not any(start <= position < end for position, _ in anchors):
            continue
        before = text[max(0, match.start() - 12):match.start()]
        if match.group(0) == "sama" and re.search(r"\b(ta|ten|to|tego|tej|tą|tym)\s+$", before, re.IGNORECASE):
            continue
        edits.append((match.start(), match.end(), target, "zaimek_sam"))
    return edits


def third_person_name_edits(text: str) -> list[tuple[int, int, str, str]]:
    """Imię żeńskie/męskie bezpośrednio rządzące czasownikiem 3. osoby."""
    edits: list[tuple[int, int, str, str]] = []
    for name in FEMALE_NAMES:
        for match in re.finditer(
            rf"(?:(?<=^)|(?<=[.!?…]\s)|(?<=,\s)){re.escape(name)}\s+(?:się\s+)?([A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+ł)\b",
            text,
        ):
            word = match.group(1)
            if word.lower().endswith("ła"):
                continue
            target = third_person_to_fem(word)
            if target is None:
                continue
            replacement = target.capitalize() if word[0].isupper() else target
            edits.append((match.start(1), match.end(1), replacement, "trzecia_osoba_imie"))
    for name in MALE_NAMES:
        for match in re.finditer(
            rf"(?:(?<=^)|(?<=[.!?…]\s)|(?<=,\s)){re.escape(name)}\s+(?:się\s+)?([A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+ła)\b",
            text,
        ):
            word = match.group(1)
            target = third_person_to_masc(word)
            if target is None:
                continue
            replacement = target.capitalize() if word[0].isupper() else target
            edits.append((match.start(1), match.end(1), replacement, "trzecia_osoba_imie"))
    return edits


def apply_edits(text: str, edits: list[tuple[int, int, str, str]]) -> tuple[str, list[tuple[int, int, str, str]]]:
    """Nakłada zmiany od końca, pomijając nakładające się i puste."""
    result = text
    applied: list[tuple[int, int, str, str]] = []
    limit = len(text)
    for start, end, new, kind in sorted(edits, key=lambda e: e[0], reverse=True):
        if end > limit:
            continue
        if result[start:end] == new:
            continue
        result = result[:start] + new + result[end:]
        applied.append((start, end, new, kind))
        limit = start
    applied.reverse()
    return result, applied


def plan(rows: list[dict[str, Any]]) -> tuple[dict[str, str], list[dict[str, Any]], dict[str, Any]]:
    scenes = scene_index(rows)
    changes: dict[str, str] = {}
    log: list[dict[str, Any]] = []
    stats: Counter[str] = Counter()
    skipped_unknown = 0

    for row in rows:
        text = row.get("translation") or ""
        if not text.strip():
            continue
        speaker = speaker_for(row)
        speaker_gender = gender_of(speaker)
        scene = scenes[scene_key(row)]
        addressee, basis = addressee_gender(scene, row)

        edits: list[tuple[int, int, str, str]] = []
        if speaker_gender:
            edits += first_person_edits(text, speaker_gender)
            edits += adjective_edits(text, speaker_gender, "1")
            edits += conditional_edits(text, speaker_gender, "1")
        # Druga osoba tylko przy znanym mówcy: narrator/nieustalony zwraca się
        # do gracza, a nie do obsady sceny, więc płeć adresata z obsady kłamie.
        if speaker_gender and addressee and addressee != speaker_gender and not has_masculine_vocative(text):
            edits += second_person_edits(text, addressee)
            edits += adjective_edits(text, addressee, "2")
            edits += conditional_edits(text, addressee, "2")
        edits += third_person_name_edits(text)

        if edits and speaker_gender:
            anchors = [(start, end) for start, end, _, kind in edits
                       if kind.startswith(("pierwsza_osoba", "1_osoba"))]
            if anchors:
                edits += self_pronoun_edits(text, speaker_gender, anchors)
        if edits and speaker_gender and addressee and addressee != speaker_gender:
            anchors = [(start, end) for start, end, _, kind in edits
                       if kind.startswith(("druga_osoba", "2_osoba"))]
            if anchors:
                edits += self_pronoun_edits(text, addressee, anchors)

        if not edits:
            if speaker_gender is None:
                skipped_unknown += 1
            continue

        new_text, applied = apply_edits(text, edits)
        if new_text == text:
            continue
        changes[row["id"]] = new_text
        log.append({
            "id": row["id"],
            "speaker": speaker,
            "speaker_gender": speaker_gender,
            "addressee_gender": addressee,
            "addressee_basis": basis,
            "before": text,
            "after": new_text,
            "edits": [{"kind": kind, "to": new} for _, _, new, kind in applied],
            "locator": {
                key: (row.get("context") or {}).get(key)
                for key in ("source_kind", "map_id", "event_id", "page_number", "command_index")
            },
        })
        for _, _, _, kind in applied:
            stats[kind] += 1

    report = {
        "schema": "tgo-gender-fix-v1",
        "translated_records": sum(1 for r in rows if (r.get("translation") or "").strip()),
        "records_changed": len(changes),
        "records_without_known_speaker": skipped_unknown,
        "edit_kinds": dict(stats),
        "speaker_gender_coverage": {
            "female_speakers": sorted(FEMALE_SPEAKERS),
            "male_speakers": sorted(MALE_SPEAKERS),
        },
        "change_log": log,
    }
    return changes, log, report


FIRST_PERSON_ANY = re.compile(r"\b[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+(?:łem|łam|łbym|łabym)\b")
SECOND_PERSON_ANY = re.compile(r"\b[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+(?:łeś|łaś|łbyś|łabyś)\b")
SAM_ANY = re.compile(r"\b(sam|sama)\b")


def residuals(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Czego narzędzie **nie** rozstrzyga — materiał do QA, nie do automatycznej zmiany."""
    scenes = scene_index(rows)
    unknown_speaker: list[dict[str, str]] = []
    ambiguous_addressee = 0
    ambiguous_samples: list[dict[str, str]] = []
    sam_cases: list[dict[str, str]] = []
    third_person: list[dict[str, str]] = []
    for row in rows:
        text = row.get("translation") or ""
        if not text.strip():
            continue
        speaker = speaker_for(row)
        speaker_gender = gender_of(speaker)
        if speaker_gender is None and FIRST_PERSON_ANY.search(text):
            unknown_speaker.append({"id": row["id"], "speaker": speaker, "text": text})
        if speaker_gender and SECOND_PERSON_ANY.search(text):
            addressee, _ = addressee_gender(scenes[scene_key(row)], row)
            if addressee is None:
                ambiguous_addressee += 1
                if len(ambiguous_samples) < 20:
                    ambiguous_samples.append({"id": row["id"], "speaker": speaker, "text": text})
        if SAM_ANY.search(text):
            sam_cases.append({"id": row["id"], "speaker": speaker, "text": text})
        if re.search(r"\b(?:ona|jej|ją|nią|niej)\b", text, re.IGNORECASE) and re.search(r"\b\w+ł\b", text):
            if len(third_person) < 20:
                third_person.append({"id": row["id"], "speaker": speaker, "text": text})
    return {
        "bez_znanego_mowcy_z_pierwsza_osoba": {"count": len(unknown_speaker), "records": unknown_speaker},
        "druga_osoba_bez_jednoznacznego_adresata": {"count": ambiguous_addressee, "samples": ambiguous_samples},
        "sam_sama_do_recznego_przegladu": {"count": len(sam_cases), "records": sam_cases},
        "trzecia_osoba_do_przegladu_w_grze": {"count": len(third_person), "samples": third_person},
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# Audyt rodzaju gramatycznego — PL",
        "",
        "Raport generuje `tools/fix_grammatical_gender.py`. Podstawą jest płeć mówcy",
        "(pierwsza osoba) i płeć adresata ustalona z jednorodnej obsady sceny (druga osoba).",
        "",
        f"- Tłumaczone rekordy: **{report['translated_records']:,}**.".replace(",", " "),
        f"- Rekordy zmienione: **{report['records_changed']:,}**.".replace(",", " "),
        "",
        "## Rodzaje zmian",
        "",
        "| Kategoria | Liczba |",
        "|---|---:|",
    ]
    for kind, count in sorted(report["edit_kinds"].items(), key=lambda item: -item[1]):
        lines.append(f"| {kind} | {count} |")
    residual = report.get("residual") or {}
    if residual:
        lines += ["", "## Czego narzędzie nie rozstrzyga", ""]
        lines.append(f"- Kwestie bez znanego mówcy z pierwszą osobą: **{residual['bez_znanego_mowcy_z_pierwsza_osoba']['count']}**.")
        lines.append(f"- Druga osoba bez jednoznacznego adresata: **{residual['druga_osoba_bez_jednoznacznego_adresata']['count']}**.")
        lines.append(f"- Kwestie z „sam/sama” do ręcznego przeglądu: **{residual['sam_sama_do_recznego_przegladu']['count']}**.")
        lines.append(f"- Zdania z zaimkiem 3. osoby i czasownikiem na „-ł” (próbka): **{residual['trzecia_osoba_do_przegladu_w_grze']['count']}**.")
        lines += ["", "Pełne listy są w `translation/reports/gender_fix_v1.json` w sekcji `residual`.", ""]
    lines += [
        "## Zasady",
        "",
        "- **Pierwsza osoba** — forma przyjmuje płeć mówcy z `custom_header` (ta sama mapa kodów co w Czytance).",
        "- **Druga osoba** — forma przyjmuje płeć adresata tylko wtedy, gdy wszyscy pozostali mówcy sceny o znanej płci są jednej płci.",
        "- **Tryb warunkowy** — `bym/byś` + czasownik przyjmuje płeć mówcy (1. os.) albo adresata (2. os.); formy 2. osoby nie są nigdy liczone płcią mówcy.",
        "- **Trzecia osoba** — nie ruszana automatycznie: podmiot bywa domyślny, a zgadywanie coreferencji wprowadzałoby błędy. Wymaga przeglądu w grze.",
        "- **„sam/sama”** — tylko w tym samym zdaniu, w którym zmieniono czasownik mówcy; samodzielnie rodzaj zależy od podmiotu, nie od mówcy (`ten sam problem`, `sama pani komisarz`).",
        "- Rzeczowniki w narzędniku (`kościołem`, `ciałem`) i czas teraźniejszy (`działam`) są wyłączone z podmiany.",
        "",
        "## Pełny dziennik",
        "",
        "Każdą zmianę (przed/po, mówca, adresat, podstawa) zawiera `translation/reports/gender_fix_v1.json`.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="zapisz zmiany do draftów")
    parser.add_argument("--report", type=Path, default=REPORT_JSON)
    parser.add_argument("--markdown", type=Path, default=REPORT_MD)
    args = parser.parse_args()

    rows = load_rows()
    changes, log, report = plan(rows)
    previous: dict[str, Any] = {}
    if args.report.exists():
        try:
            previous = json.loads(args.report.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = {}
    report["applied"] = False
    if args.fix and changes:
        touched_files = []
        for path in sorted(DRAFTS.rglob("*.jsonl")):
            lines = path.read_text(encoding="utf-8").splitlines()
            output = []
            touched = False
            for line in lines:
                if not line.strip():
                    output.append(line)
                    continue
                row = json.loads(line)
                if row.get("id") in changes and (row.get("translation") or "").strip():
                    row["translation"] = changes[row["id"]]
                    output.append(json.dumps(row, ensure_ascii=False, sort_keys=True))
                    touched = True
                else:
                    output.append(line)
            if touched:
                path.write_text("\n".join(output) + "\n", encoding="utf-8", newline="\n")
                touched_files.append(str(path.relative_to(DRAFTS)))
        report["applied"] = True
        report["files"] = touched_files

    applied_rows = []
    for row in rows:
        clone = dict(row)
        if row["id"] in changes:
            clone["translation"] = changes[row["id"]]
        applied_rows.append(clone)
    report["residual"] = residuals(applied_rows)
    if not changes and previous.get("change_log"):
        # Ponowny przebieg nie kasuje historii: drafty są już poprawione,
        # a raport ma nadal pokazywać, co i dlaczego zmieniono.
        report["change_log"] = previous["change_log"]
        report["records_changed"] = previous.get("records_changed", 0)
        report["edit_kinds"] = previous.get("edit_kinds", {})
        report["applied"] = previous.get("applied", False)
        report["residual"] = residuals(rows)

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    write_markdown(report, args.markdown)
    print(json.dumps({
        "translated_records": report["translated_records"],
        "records_changed": report["records_changed"],
        "edit_kinds": report["edit_kinds"],
        "applied": report["applied"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
