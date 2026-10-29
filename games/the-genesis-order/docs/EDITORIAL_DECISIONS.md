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
- **Niespójność w korpusie (POTWIERDZONE):** w scenie „SCN - Ending” zdanie `The Genesis Order will continue being updated on the 2nd and 15th…` zostaje z angielską nazwą („The Genesis Order będzie nadal otrzymywać aktualizacje…”). Jeśli zostaje „Zakon Genesis”, ta linia jest jedynym miejscem, gdzie tytuł nadal brzmi po angielsku — trzeba ją zmienić razem z `gameTitle`.
- **Do decyzji:** A) „Zakon Genesis” + poprawka zdania z „SCN - Ending”, B) „The Genesis Order” bez zmian (spójne z tą linią i z decyzją R-02 o marce), C) hybryda „The Genesis Order — Zakon Genesis” (wymaga sprawdzenia, czy pole mieści taki tekst).
- **Koszt zmiany:** 1–2 rekordy + przebudowa patcha i Czytanki (deterministyczna, ~10 s każda przy dostępnych źródłach).

## R-02 — `Channel 4` jako marka

- **Stan (POTWIERDZONE, sprawdzone w korpusie):** we **wszystkich** 63 przetłumaczonych wystąpieniach zostaje `Channel 4` (np. „Musisz iść do wieżowca Channel 4.”), a etykieta mapy to dosłownie `Channel 4`. W plikach draftów **nie ma już ani jednego** „Kanał 4” — starszy wariant z `inventory-names-01.jsonl` został zastąpiony podczas uzgodnienia 40 etykiet.
- **Uzasadnienie:** to nazwa stacji telewizyjnej w świecie gry, prawdopodobnie nawiązanie do realnego kanału; tłumaczenie gubi aluzję.
- **Do decyzji:** potwierdzić `Channel 4` (stan obecny) albo przywrócić „Kanał 4” (wtedy trzeba też poprawić 63 zdania, gdzie nazwa pełni funkcję rzeczownika).
- **Uwaga:** nazwa wchodzi do polskich zdań w formie nieodmienionej („w wieżowcu Channel 4”, nie „w wieżowcu Kanale 4”). To spójne z decyzją R-09 o formach bazowych, ale jest odczuwalne stylistycznie.

## R-03 — Etykiety map (wszystkie 291, w tym 40 przepisanych)

- **Stan (POTWIERDZONE):** `drafts/inventory-names-01.jsonl` zawiera **wszystkie 291** etykiet map: **288** przetłumaczonych, **3** bez zmian (`Channel 4`, `START`, `Test`). W ostatnim uzgodnieniu przepisano **40** etykiet — plik jest bajt w bajt zgodny z wersją z PR #5.
- **Przykłady przepisanych:** `PRE TITLE` → „PRZED EKRANEM TYTUŁOWYM”, `MC Home` → „Dom bohatera”, `Strip Center` → „Centrum handlowe”, `Foyer` → „Hol wejściowy”, `Storage` → „Magazyn”, `Police Station` → „Komisariat policji”.
- **Charakter:** etykiety widać na ekranie mapy/przejść, więc to tekst gracza; ale część z nich to nazwy robocze dewelopera (`PRE TITLE`, `TEST MAP` → „MAPA TESTOWA”), których gracz może nigdy nie zobaczyć.
- **Do decyzji:** A) zostawić wszystkie 288 tłumaczeń (stan obecny), B) przywrócić robocze nazwy tam, gdzie mapa jest nieosiągalna, C) punktowo — właściciel wskazuje mapy widoczne w grze.
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

- **Stan (POTWIERDZONE, kolejność sprawdzona w evencie):** to **pierwsza** z dwóch linii wiadomości w wątku `M. Deluna` — kolejno „He’s going to be<br>” → **„Będzie<br>”** i „pissed, ya know?” → „Wkurzony, kumasz?”. Razem czytają się jako „Będzie wkurzony, kumasz?”.
- **Alternatywa:** „On będzie” (bliżej składni angielskiej, ale w polskim zaimka się nie powtarza).
- **Do decyzji:** A) „Będzie” (stan obecny), B) „On będzie”.
- **Uwaga:** linia jest dzielona między dwa rekordy — przy zmianie trzeba zachować spójność z **następnym** fragmentem („Wkurzony, kumasz?”), bo razem tworzą jedno zdanie.

## R-07 — Placeholdery mapy testowej

- **Stan (POTWIERDZONE):** 7 rekordów `native_message` z **TEST MAP, EV001**, każdy `Text goes here<br>` → „Tekst w tym miejscu<br>”. To jawnie renderowane wypełniacze dewelopera.
- **Dylemat:** tłumaczenie placeholdera dewelopera to praca bez wartości gracza; z drugiej strony jeśli mapa jest osiągalna, gracz zobaczy polski tekst.
- **Do decyzji:** A) zostawić tłumaczenie (stan obecny), B) przywrócić angielskie wypełniacze, C) zostawić tylko tam, gdzie mapa jest osiągalna.

## R-08 — `TEXT` → „TEKST” (mapa TEST MAP)

- **Stan (POTWIERDZONE):** literał `TEXT` to `phone_text` z **TEST MAP, EV021** — czyli stub mapy testowej, nie element produkcyjnego UI. Przetłumaczony na „TEKST”.
- **Ryzyko (HIPOTEZA, niskie):** gdyby ten literał był kluczem dopasowywanym przez kod gry, zmiana mogłaby zepsuć logikę testową. Kod gry nie jest lokalnie dostępny, więc nie sprawdzono; skoro to mapa testowa, skutek byłby ograniczony.
- **Do decyzji:** A) zostawić „TEKST”, B) przywrócić `TEXT` razem z R-07 (oba są stubami TEST MAP), C) sprawdzić w runtime i wrócić do tematu.

## R-09 — Odmiana imion: **korpus jest niespójny** (największy dług redakcyjny)

- **Stan (POTWIERDZONE, policzone w korpusie):** imiona zakończone na `-a` są odmieniane **tylko w części** wystąpień — reszta zostaje w mianowniku. To nie jest decyzja, a skutek pracy w partiach.

| Imię | Wystąpień | Mianownik | Odmienione | % odmienionych |
|---|---:|---:|---:|---:|
| Erica | 318 | 178 | 140 | 44% |
| Andrea | 294 | 186 | 108 | 37% |
| Ella | 263 | 175 | 88 | 33% |
| Melissa | 185 | 139 | 46 | 25% |
| Arianna | 87 | 61 | 26 | 30% |
| Toma | 176 | 88 | 88 | 50% |
| Diana | 53 | 42 | 11 | 21% |

- **Konsekwencja:** w korpusie występują obok siebie „Klucz do głównej sypialni **Andrei**” i „z **Andrea**”, „Zgubiony telefon **Elli**” i „do **Ella**”. Dla gracza to odczuwalna niekonsekwencja.
- **Imiona bez odmiany:** `Chloe`, `Lilith`, `Carol`, `Hannah`, `Judy` — **0** form odmienionych (449/106/325/606/514 wystąpień). Dla żeńskich imion na spółgłoskę to poprawna polszczyzna; dla `Hannah` możliwa jest forma „Hanny”, ale nie jest wymagana.
- **Do decyzji:** A) ujednolicić mianownik wszędzie (mechanicznie, tanio, ale brzmi obco w 30–50% zdań), B) ujednolicić odmianę imion na `-a` (poprawna polszczyzna, wymaga przejrzenia ~1 400 wystąpień), C) zostawić jak jest i potraktować jako znane ograniczenie POC.
- **Rekomendacja agenta:** B. Zakres jest policzalny (tabela wyżej), a to najbardziej rzucająca się w oczy wada istniejącego przekładu — nie wymaga ponownego tłumaczenia, tylko redakcji form.

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
| R-01 | Tytuł gry | wariant B (oryginał) — spójny z R-02 i z linią „SCN - Ending”; jeśli A, to poprawić też tę linię |
| R-02 | `Channel 4` | zostawić markę |
| R-03 | 40 etykiet map | zostawić, potem punktowo wyciszyć martwe mapy |
| R-04 | Crafting — pytanie | „Wytworzyć przedmiot?” (krótsze) |
| R-05 | Crafting — błąd | stan obecny |
| R-06 | Telefon | „Będzie” |
| R-07 | Placeholdery | przywrócić angielskie (brak wartości gracza) |
| R-08 | `TEXT`/`TEKST` (TEST MAP) | przywrócić `TEXT` razem z R-07 — to stuby mapy testowej |
| R-09 | Odmiana imion | **ujednolicić odmianę imion na `-a`** (dziś 21–50% form odmienionych, reszta w mianowniku) |
| R-10 | `WoNoChurch` | „Kościół WoNo” |
| R-11 | Fonty | **zbadać przed publikacją** — blokuje sens całości |
