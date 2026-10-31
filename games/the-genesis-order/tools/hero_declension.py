#!/usr/bin/env python3
"""Odmiana imienia bohatera w Czytance (placeholder ``1Hero`` → formy „Mox”).

W plikach gry i w draftach bohater występuje jako placeholder ``1Hero``,
podstawiany w runtime imieniem gracza — dlatego **w grze** nie da się go
odmienić statycznie (imię jest dynamiczne). W Czytance imię jest stałe
(decyzja właściciela: bohater to „Mox”), więc odmiana jest możliwa i potrzebna:
bez niej w tekście stały „z Mox”, „dla Mox”, „o Mox”.

Ten moduł zawiera wyłącznie **reguły odmiany jednego imienia** — nie jest
tłumaczeniem automatycznym i nie rusza żadnego innego słowa. Formy:

    Mox → Moxa (dopełniacz, biernik), Moxowi (celownik),
          Moxem (narzędnik), Moxie (miejscownik), Mox (mianownik, wołacz)

Przypadek ustalany jest z najbliższego rządzącego słowa:

1. **Przyimek o jednym rządzie** (``do``, ``dla``, ``o`` mówiące, ``przy``,
   ``dzięki``…) — przypadek wynika z tabeli; to najpewniejsza grupa.
2. **Przyimek dwuznaczny** (``z``, ``w``, ``na``, ``za``, ``pod``, ``między``,
   ``o``) — reguła domyślna plus wąskie wyjątki:
   * ``z`` daje narzędnik, chyba że czasownik przed przyimkiem znaczy
     „pochodzić/wyjść/śmiać się” — wtedy dopełniacz (``To wyszło z 1Hero?``),
   * ``o`` daje miejscownik, chyba że przed nim stoi „chodzi/chodziło”
     (``Chodzi o 1Hero`` — biernik),
   * ``na`` i ``za`` dają biernik (``Zbliżenia na 1Hero``, ``zastępstwo za 1Hero``),
   * ``w`` daje miejscownik (``podkochuje się w 1Hero``),
   * ``pod`` i ``między`` dają narzędnik.
3. **Czasownik** — mała, zamknięta lista czasowników, których rząd jest
   jednoznaczny (``chroń``, ``widziałam`` → biernik; ``pomóc`` → celownik;
   ``słuchaj`` → dopełniacz).

Wszystko inne zostaje w mianowniku (wołacz i podmiot są w polszczyźnie
identyczne z mianownikiem) i jest raportowane jako ``unresolved`` — moduł
nigdy nie zgaduje przypadku.

Każda podmiana zwraca decyzję z uzasadnieniem, żeby dało się ją przejrzeć
i przetestować (``decline_text``).
"""

from __future__ import annotations

import re

HERO_PLACEHOLDER = "1Hero"

# Formy imienia bohatera widoczne w Czytance.
HERO_FORMS: dict[str, str] = {
    "nom": "Mox",
    "voc": "Mox",
    "gen": "Moxa",
    "dat": "Moxowi",
    "acc": "Moxa",
    "ins": "Moxem",
    "loc": "Moxie",
}

# Przyimki o jednym rządzie przypadka.
PREPOSITION_CASES: dict[str, str] = {
    # dopełniacz
    "do": "gen", "od": "gen", "u": "gen", "dla": "gen", "bez": "gen",
    "obok": "gen", "koło": "gen", "około": "gen", "wobec": "gen",
    "zamiast": "gen", "oprócz": "gen", "według": "gen", "poza": "gen",
    "wśród": "gen", "podczas": "gen", "naprzeciw": "gen", "dookoła": "gen",
    # celownik
    "ku": "dat", "dzięki": "dat", "wbrew": "dat", "przeciw": "dat",
    "przeciwko": "dat",
    # narzędnik
    "nad": "ins", "przed": "ins",
    # miejscownik
    "przy": "loc", "po": "loc",
    # biernik
    "przez": "acc", "poprzez": "acc",
}

# Przyimki, których rząd zależy od kontekstu: reguła domyślna + wyjątki niżej.
DEFAULT_AMBIGUOUS: dict[str, str] = {
    "z": "ins", "ze": "ins",
    "w": "loc", "we": "loc",
    "na": "acc",
    "za": "acc",
    "pod": "ins",
    "między": "ins",
    "o": "loc",
}

# „z” + czasownik pochodzenia/źródła → dopełniacz („wyszło z kogoś”).
GENITIVE_Z_GOVERNORS = frozenset({
    "wyszedł", "wyszła", "wyszło", "wyszli", "wyjść", "wyjdź",
    "pochodzi", "pochodzą", "pochodzić",
    "dowiedział", "dowiedziała", "dowiedziałem", "dowiedziałam", "dowiedzieć",
    "usłyszał", "usłyszała", "usłyszałem", "usłyszałam", "usłyszeć",
    "śmiał", "śmiała", "śmiej", "śmiać",
    "zrezygnował", "zrezygnowała", "zrezygnuj", "zrezygnować",
    "spadł", "spadła", "spaść", "zdjął", "zdjęła", "zdjąć",
    "wrócił", "wróciła", "wrócić", "przyjechał", "przyjechała", "przyjechać",
    "wyciągnął", "wyciągnęła", "wyjął", "wyjęła", "zszedł", "zeszła",
    "spuścił", "spuściła", "uciekł", "uciekła", "wymknął", "wymknęła",
    "cieszy", "cieszył", "cieszyła", "ucieszył", "ucieszyła",
})

# „o” + „chodzi/chodziło” → biernik („Chodzi o kogoś”).
ACC_O_GOVERNORS = frozenset({"chodzi", "chodziło", "chodzić", "zapytać", "zapytaj"})

# Rzeczowniki, po których imię stoi w dopełniaczu („program 1Hero”).
NOUN_GENITIVE_GOVERNORS = frozenset({"program", "zdjęcie", "zdjęcia", "autograf", "nagranie"})

# Czasowniki z jednoznacznym rządem; mała, zamknięta lista z korpusu.
VERB_CASES: dict[str, str] = {
    # biernik
    "chroń": "acc", "chronić": "acc", "chronię": "acc",
    "widział": "acc", "widziała": "acc", "widziałam": "acc",
    "widziałem": "acc", "widziałeś": "acc", "widzieli": "acc", "widzieć": "acc",
    "zobacz": "acc", "zobaczyć": "acc", "zobaczyłem": "acc", "zobaczyłam": "acc",
    "znajdź": "acc", "znaleźć": "acc", "znalazł": "acc", "znalazła": "acc",
    "zabierz": "acc", "zabrać": "acc", "zapytaj": "acc", "zapytać": "acc",
    "kocham": "acc", "kochać": "acc", "zostaw": "acc", "zostawić": "acc",
    "obudź": "acc", "obudzić": "acc", "poznaj": "acc", "poznać": "acc",
    "uratuj": "acc", "uratować": "acc", "pocałuj": "acc", "pocałować": "acc",
    "przytul": "acc", "przytulić": "acc", "zaproś": "acc", "zaprosić": "acc",
    "odwiedź": "acc", "odwiedzić": "acc", "przynieś": "acc", "przynieść": "acc",
    # celownik
    "pomóż": "dat", "pomóc": "dat", "pomogę": "dat", "pomaga": "dat", "pomagać": "dat",
    "daj": "dat", "dać": "dat", "dam": "dat",
    "powiedz": "dat", "powiedzieć": "dat",
    "dziękuję": "dat", "dziękować": "dat",
    "ufam": "dat", "ufać": "dat", "wierzę": "dat", "wierzyć": "dat",
    "zazdroszczę": "dat", "zazdrościć": "dat",
    "przeszkadza": "dat", "przeszkadzać": "dat",
    "kup": "dat", "kupić": "dat", "pokaż": "dat", "pokazać": "dat",
    # biernik — czasowniki dopisane po przeglądzie 2026-10-31
    "ujeżdżać": "acc", "ujeżdżam": "acc", "puścić": "acc", "puść": "acc",
    "zabił": "acc", "zabiła": "acc", "zabić": "acc", "wyprał": "acc", "wyprać": "acc",
    "skrzywdzić": "acc", "skrzywdzę": "acc", "pragnę": "acc", "pragnąć": "acc",
    "porwały": "acc", "porwał": "acc", "porwała": "acc", "porwać": "acc",
    "namówić": "acc", "namów": "acc", "poprosić": "acc", "poprosisz": "acc",
    "znasz": "acc", "znać": "acc", "zna": "acc", "zgłaszam": "acc", "zgłosić": "acc",
    "oglądać": "acc", "doprowadzić": "acc", "wprawiaj": "acc", "wprawić": "acc",
    "mieć": "acc", "mam": "acc", "masz": "acc", "miałem": "acc", "miałam": "acc",
    # celownik — dopisane po przeglądzie 2026-10-31
    "pozwolić": "dat", "pozwól": "dat", "pomogłam": "dat", "pomogłeś": "dat",
    "powiedziałaś": "dat", "powiedziałeś": "dat", "powiedział": "dat",
    "powiedziała": "dat", "mówię": "dat", "mówiłam": "dat", "mówiłem": "dat",
    # dopełniacz
    "słuchaj": "gen", "słuchać": "gen",
    "szukaj": "gen", "szukać": "gen",
    "ucz": "gen", "uczyć": "gen", "naucz": "gen", "nauczyć": "gen",
}

# Znaki, które mogą dokleić się do słowa rządzącego.
_TRIM = " \t\n„”\"'()[]{}…,.;:!?—-"

# Znaczniki tekstu gry (kolory, ikony) — pomijane przy szukaniu słowa rządzącego.
_MARKUP_RE = re.compile(r"\\[A-Za-z]+(?:\[[^\]]*\])?|<[^>]+>")

_PLACEHOLDER_RE = re.compile(r"\b1Hero\b")


def _clean_before(text: str, index: int) -> str:
    """Zwróć tekst przed ``index`` bez znaczników renderera."""
    return _MARKUP_RE.sub(" ", text[:index])


def _words_before(text: str, index: int, limit: int = 3) -> list[str]:
    """Słowa przed ``index`` w tej samej klauzuli, od najbliższego.

    Granicę klauzuli wyznacza interpunkcja kończąca zdanie oraz średnik, dwukropek
    i znak nowej linii — dzięki temu „Jestem… 1Hero.” nie bierze „jestem” za
    słowo rządzące.
    """
    cleaned = _clean_before(text, index)
    segment = re.split(r"[.!?…;:\n]", cleaned)[-1]
    raw = re.split(r"\s+", segment.rstrip())
    words = [word.strip(_TRIM).lower() for word in raw if word.strip(_TRIM)]
    return list(reversed(words))[:limit]


# Heurystyka „to jest czasownik”: końcówki osobowe i bezokolicznikowe.
_VERB_LIKE = re.compile(
    r"(?:ł|ła|ło|li|ły|aj|asz|isz|ysz|ałem|ałam|iłem|yłem|ałeś|ałaś|"
    r"esz|iem|am|em|ąć|ić|yć|ać|eć|ć)$"
)


def _is_verb_like(word: str) -> bool:
    return len(word) > 3 and bool(_VERB_LIKE.search(word))


def _is_vocative(text: str, index: int) -> bool:
    """Czy placeholder jest zwrotem do bohatera (wołacz = mianownik)?"""
    before = _MARKUP_RE.sub("", text[:index]).strip(" \u201e\"(")
    after = _MARKUP_RE.sub("", text[index:]).strip(" \u201d\")")
    after = _PLACEHOLDER_RE.sub("", after, count=1).strip()
    if before == "" and after.strip(" .!?\u2026") == "":
        return True
    if before.endswith(",") and (after[:1] in ".,!?\u2026" or after == ""):
        return True
    if before == "" and after.startswith(","):
        return True
    # „Wiesz, 1Hero bawił się…” — po przecinku, a dalej czasownik: to zwrot.
    if before.endswith(",") and after[:1] != "":
        next_word = re.split(r"\s+", after.lstrip(" ,"))[0].strip(_TRIM).lower()
        if _is_verb_like(next_word):
            return True
    return False


def decide_case(text: str, index: int) -> tuple[str | None, str]:
    """Ustal przypadek dla placeholdera na pozycji ``index``.

    Zwraca ``(przypadek, uzasadnienie)``; ``None`` oznacza brak rozstrzygnięcia.
    """
    if _is_vocative(text, index):
        return "voc", "wołacz (forma równa mianownikowi)"
    words = _words_before(text, index)
    if not words:
        return "nom", "brak słowa rządzącego — mianownik"
    governor = words[0]
    if governor in PREPOSITION_CASES:
        case = PREPOSITION_CASES[governor]
        return case, f"przyimek {governor} → {case}"
    if governor in DEFAULT_AMBIGUOUS:
        case = DEFAULT_AMBIGUOUS[governor]
        previous = words[1] if len(words) > 1 else ""
        if governor in {"z", "ze"} and previous in GENITIVE_Z_GOVERNORS:
            return "gen", f"przyimek {governor} + {previous} (źródło) → gen"
        if governor == "o" and previous in ACC_O_GOVERNORS:
            return "acc", f"przyimek o + {previous} → acc"
        return case, f"przyimek {governor} (domyślnie) → {case}"
    if governor in NOUN_GENITIVE_GOVERNORS:
        return "gen", f"rzeczownik {governor} → gen"
    if governor in VERB_CASES:
        case = VERB_CASES[governor]
        return case, f"czasownik {governor} → {case}"
    if _is_verb_like(governor):
        return None, f"czasownik „{governor}” poza tabelą rządu"
    return "nom", f"brak rządu („{governor}”) — mianownik"


def decline_text(text: str) -> tuple[str, list[dict[str, object]]]:
    """Odmień wszystkie wystąpienia ``1Hero`` w tekście.

    Zwraca ``(nowy_tekst, decyzje)``; decyzja zawiera pozycję, przypadek, formę
    i uzasadnienie (albo ``unresolved``, gdy przypadek nie jest rozstrzygnięty).
    """
    decisions: list[dict[str, object]] = []
    pieces: list[str] = []
    last = 0
    for match in _PLACEHOLDER_RE.finditer(text):
        case, reason = decide_case(text, match.start())
        pieces.append(text[last:match.start()])
        if case is None:
            pieces.append(HERO_FORMS["nom"])
            decisions.append({
                "offset": match.start(), "case": None, "form": HERO_FORMS["nom"],
                "resolved": False, "reason": reason,
            })
        else:
            form = HERO_FORMS[case]
            pieces.append(form)
            decisions.append({
                "offset": match.start(), "case": case, "form": form,
                "resolved": True, "reason": reason,
            })
        last = match.end()
    pieces.append(text[last:])
    return "".join(pieces), decisions
