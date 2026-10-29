# Decyzje redakcyjne — do zatwierdzenia przez właściciela

Ten plik zbiera **wszystkie miejsca, w których dwa źródła w repo mówią co innego** albo gdzie przyjęto wariant bez jednoznacznego rozstrzygnięcia. Nic tu jeszcze nie jest „poprawione” — to lista do decyzji. Każda pozycja ma ID, więc decyzję można zapisać jednym zdaniem („R-03: wariant B”).

**Stan:** 2026-10-29, po odzyskaniu pracy poprzedniego agenta. Liczby: 427 partii, 39 926 tłumaczeń, 0 nierozstrzygniętych.

## Jak czytać

- **POTWIERDZONE** — sprawdzone w plikach, nie wymaga weryfikacji.
- **HIPOTEZA** — wniosek z poszlak, wymaga potwierdzenia (najczęściej testem w grze).
- **NIEZNANE** — brak danych.

---

## R-01 — Tytuł gry: „Zakon Genesis” czy „The Genesis Order”

- **Stan:** w `drafts/visible-name-l10n-01.jsonl` tytuł (`system.gameTitle`) to **„Zakon Genesis”**. Wcześniejszy glosariusz roboczo zakładał zachowanie oryginału jako nazwy marki.
- **Uzasadnienie tłumaczenia:** „the Genesis Order” to w fabule nazwa zakonu (organizacji), nie tylko tytuł produktu — więc tłumaczenie jest merytorycznie obronne.
- **Ryzyko:** tytuł widoczny na oknie gry i w menu; gracze szukają gry po angielskiej nazwie. Część wydawców zostawia tytuł, część tłumaczy.
- **Do decyzji:** A) „Zakon Genesis” (stan obecny), B) „The Genesis Order” bez zmian, C) hybryda „The Genesis Order — Zakon Genesis” (wymaga sprawdzenia, czy pole mieści taki tekst).
- **Koszt zmiany:** jeden rekord + przebudowa patcha i Czytanki (~10 s każda, deterministyczne).

## R-02 — `Channel 4` jako marka

- **Stan:** POTWIERDZONE — nowsze partie zostawiają `Channel 4` bez zmian; starsza wersja miała „Kanał 4”. Uzgodnione na wersji bez tłumaczenia, konfliktów brak.
- **Uzasadnienie:** to w świecie gry nazwa stacji telewizyjnej, prawdopodobnie nawiązanie do realnego kanału; tłumaczenie gubi aluzję.
- **Do decyzji:** potwierdzić `Channel 4` (stan obecny) albo przywrócić „Kanał 4”.
- **Uwaga:** ta sama nazwa może występować w dialogach jako tekst mówiony — wtedy odmiana przez przypadki wymagałaby formy „na Kanale 4” itd. Sprawdzone: w korpusie nie ma odmienionych wystąpień.

## R-03 — 40 etykiet map (`map_label`)

- **Stan:** POTWIERDZONE — `drafts/inventory-names-01.jsonl` zawiera 40 przepisanych etykiet (bajt w bajt zgodnych z PR #5), m.in. `PRE TITLE` → „PRZED EKRANEM TYTUŁOWYM”, `MC Home` → „Dom bohatera”, `Strip Center` → „Centrum handlowe”, `Foyer` → „Hol wejściowy”, `Storage` → „Magazyn”, `Police Station` → „Komisariat policji”.
- **Charakter:** etykiety widać w grze na ekranie mapy/przejść, więc to tekst gracza; ale część z nich to nazwy robocze dewelopera (`PRE TITLE`, `TEST MAP`), których gracz może nigdy nie zobaczyć.
- **Do decyzji:** A) zostawić tłumaczenia wszystkich 40 (stan obecny), B) przywrócić robocze nazwy tam, gdzie mapa jest nieosiągalna, C) punktowo — właściciel wskazuje, które mapy są widoczne.
- **Uwaga:** 70 z 291 map jest nieosiągalnych w statycznym BFS od startu (`reading/v1/README_PL.md`), więc część etykiet może być martwa — ale BFS jest przybliżony, nie dowodem.

## R-04 — „Craft this item?”: „Wytworzyć ten przedmiot?” czy „Wytworzyć przedmiot?”

- **Stan:** w korpusie finalnym **„Wytworzyć ten przedmiot?”** (94 rekordy Map 46, identyczne powtórzenia).
- **Alternatywa:** „Wytworzyć przedmiot?” — krótsze, mniej „urzedowe”; mieści się lepiej w wąskim okienku UI.
- **Do decyzji:** A) „Wytworzyć ten przedmiot?”, B) „Wytworzyć przedmiot?”, C) „Wytworzyć?” (najkrótsze, ale traci dopełnienie).
- **Koszt zmiany:** jeden rekord źródłowy × 47 wystąpień; builder przebudowuje deterministycznie.

## R-05 — „You have items missing from this recipe.”

- **Stan:** „Brakuje ci przedmiotów potrzebnych do tego przepisu.”
- **Alternatywa:** „Brakuje przedmiotów z tej receptury.” — krótsze, ale „receptura” brzmi technicznie.
- **Do decyzji:** A) stan obecny, B) krótszy wariant.
- **Uwaga:** to komunikat błędu widoczny przy każdej nieudanej próbie craftingu, więc długość ma znaczenie dla czytelności.

## R-06 — `He’s going to be` → „Będzie”

- **Stan:** POTWIERDZONE — fragment zdania telefonu, kontynuacja wcześniejszej linii „Wkurzony, kumasz?”; w korpusie „Będzie”.
- **Alternatywa:** „On będzie” (bliżej składni angielskiej, ale w polskim zaimka się nie powtarza).
- **Do decyzji:** A) „Będzie” (stan obecny), B) „On będzie”.
- **Uwaga:** linia jest dzielona między dwa rekordy — przy zmianie trzeba zachować spójność z poprzednim fragmentem.

## R-07 — Placeholdery mapy testowej

- **Stan:** 7 × `Text goes here<br>…` → „Tekst w tym miejscu<br>…”. To jawnie renderowane wypełniacze z TEST MAP.
- **Dylemat:** tłumaczenie placeholdera dewelopera to praca bez wartości gracza; z drugiej strony jeśli mapa jest osiągalna, gracz zobaczy polski tekst.
- **Do decyzji:** A) zostawić tłumaczenie (stan obecny), B) przywrócić angielskie wypełniacze, C) zostawić tylko tam, gdzie mapa jest osiągalna.

## R-08 — `TEXT` → „TEKST” w kanale telefonu

- **Stan:** dosłowny literał kanału telefonu przetłumaczony.
- **Ryzyko (HIPOTEZA):** jeśli ten literał jest kluczem dopasowywanym przez kod gry (a nie tylko etykietą), zmiana może zepsuć logikę. Nie ma lokalnie kodu gry, więc tego nie sprawdzono.
- **Do decyzji:** A) zostawić „TEKST”, B) przywrócić `TEXT` z ostrożności, C) sprawdzić w runtime na kopii gry i wrócić do tematu.

## R-09 — Odmiana imion i nazw własnych

- **Stan:** imiona pozostają w formie bazowej (`Erica`, `Arianna`, `Toma`, `Lilith`, `Daemalius`, `Anachorismos`), zgodnie z glosariuszem.
- **Konsekwencja:** w polskich zdaniach pojawiają się formy nieodmienione („z Erica”, „do Lilith”). To świadomy kompromis — odmiana wymagałaby ręcznej redakcji każdego zdania i rodzi ryzyko niespójności w 39 tysiącach rekordów.
- **Do decyzji:** A) zostawić formy bazowe (stan obecny), B) wprowadzić odmianę w dialogach (duży nakład, ryzyko regresji), C) odmieniać tylko w narracji Czytanki, nie w grze.

## R-10 — `WoNoChurch` → „WoNo — kościół”

- **Stan:** częściowe tłumaczenie: niejasny prefiks `WoNo` zachowany, oczywisty człon przetłumaczony.
- **Alternatywy:** „Kościół WoNo”, „WoNoChurch” bez zmian.
- **Do decyzji:** A) stan obecny, B) „Kościół WoNo”, C) bez zmian.

## R-11 — Fonty i polskie glify (NIEZNANE)

- **Stan:** nie sprawdzono, czy czcionki w grze zawierają ą/ć/ę/ł/ń/ó/ś/ź/ż ani jak łamie się dłuższy polski tekst.
- **Ryzyko:** to najpoważniejsze ryzyko całego projektu — jeśli font nie ma glifów, cała praca jest niewidoczna w grze.
- **Do decyzji:** test na kopii gry (Windows) albo świadome zaakceptowanie ryzyka w POC.

---

## Podsumowanie do szybkiej decyzji

| ID | Temat | Rekomendacja agenta |
|---|---|---|
| R-01 | Tytuł gry | wariant B lub C — tytuł to marka, ale nazwa zakonu jest fabularna |
| R-02 | `Channel 4` | zostawić markę |
| R-03 | 40 etykiet map | zostawić, potem punktowo wyciszyć martwe mapy |
| R-04 | Crafting — pytanie | „Wytworzyć przedmiot?” (krótsze) |
| R-05 | Crafting — błąd | stan obecny |
| R-06 | Telefon | „Będzie” |
| R-07 | Placeholdery | przywrócić angielskie (brak wartości gracza) |
| R-08 | `TEXT`/`TEKST` | sprawdzić w runtime przed zmianą |
| R-09 | Odmiana imion | formy bazowe |
| R-10 | `WoNoChurch` | „Kościół WoNo” |
| R-11 | Fonty | **zbadać przed publikacją** — blokuje sens całości |
