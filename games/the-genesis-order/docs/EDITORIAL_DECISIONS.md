# Decyzje redakcyjne

Ten plik zbiera **wszystkie miejsca, w których dwa źródła w repo mówią co innego** albo gdzie przyjęto wariant bez jednoznacznego rozstrzygnięcia. Pozycje rozstrzygnięte przez właściciela mają w nagłówku **ROZSTRZYGNIĘTE**, datę decyzji i opis wykonania; pozostałe czekają na decyzję. Każda pozycja ma ID, więc decyzję zapisuje się jednym zdaniem („R-03: wariant B”).

**Stan:** 2026-10-29, po decyzjach właściciela. Liczby: 427 partii, **39 917** tłumaczeń, 131 rekordów chronionych, **5 181** świadomie zachowanych w źródle, 0 nierozstrzygniętych.

**Wszystkie pozycje są rozstrzygnięte.** R-01, R-02, R-07, R-08, R-09 — wykonane (zmiany w korpusie i paczkach). R-03, R-04, R-05, R-06, R-10 — właściciel uznał za nieistotne: **zostaje wariant obecny, bez żadnych zmian**. R-11 (fonty) — **POTWIERDZONE W GRZE** 2026-10-29: polskie znaki, opcje PL i zawijanie tekstu działają. Lista decyzji jest zamknięta.

## Jak czytać

- **POTWIERDZONE** — sprawdzone w plikach, nie wymaga weryfikacji.
- **HIPOTEZA** — wniosek z poszlak, wymaga potwierdzenia (najczęściej testem w grze).
- **NIEZNANE** — brak danych.

---

## R-01 — Tytuł gry: „Zakon Genesis” czy „The Genesis Order” — **ROZSTRZYGNIĘTE: wariant B**

> **Decyzja właściciela (2026-10-29):** tytuł gry zostaje **zawsze po angielsku**. Wykonane: rekord
> `system.gameTitle` usunięty z `drafts/visible-name-l10n-01.jsonl` (partia ma teraz 2 rekordy: `Arianna as Erica`,
> `WoNoChurch`), a bramka pokrycia klasyfikuje ten tytuł z jawnym powodem
> `owner_decision_R01_brand_title_kept_in_english`. Zdanie z „SCN - Ending” już zawierało angielską nazwę, więc jest spójne.

- **Stan:** w `drafts/visible-name-l10n-01.jsonl` tytuł (`system.gameTitle`) to **„Zakon Genesis”**. Wcześniejszy glosariusz roboczo zakładał zachowanie oryginału jako nazwy marki.
- **Uzasadnienie tłumaczenia:** „the Genesis Order” to w fabule nazwa zakonu (organizacji), nie tylko tytuł produktu — więc tłumaczenie jest merytorycznie obronne.
- **Ryzyko:** tytuł widoczny na oknie gry i w menu; gracze szukają gry po angielskiej nazwie. Część wydawców zostawia tytuł, część tłumaczy.
- **Niespójność w korpusie (POTWIERDZONE):** w scenie „SCN - Ending” zdanie `The Genesis Order will continue being updated on the 2nd and 15th…` zostaje z angielską nazwą („The Genesis Order będzie nadal otrzymywać aktualizacje…”). Jeśli zostaje „Zakon Genesis”, ta linia jest jedynym miejscem, gdzie tytuł nadal brzmi po angielsku — trzeba ją zmienić razem z `gameTitle`.
- **Do decyzji:** A) „Zakon Genesis” + poprawka zdania z „SCN - Ending”, B) „The Genesis Order” bez zmian (spójne z tą linią i z decyzją R-02 o marce), C) hybryda „The Genesis Order — Zakon Genesis” (wymaga sprawdzenia, czy pole mieści taki tekst).
- **Koszt zmiany:** 1–2 rekordy + przebudowa patcha i Czytanki (deterministyczna, ~10 s każda przy dostępnych źródłach).

## R-02 — `Channel 4` jako marka — **ROZSTRZYGNIĘTE: zostaje po angielsku**

> **Decyzja właściciela (2026-10-29):** `Channel 4` **bez zmian** (nazwa stacji w świecie gry). Korpus już to spełnia:
> 63/63 wystąpień i etykieta mapy.

- **Stan (POTWIERDZONE, sprawdzone w korpusie):** we **wszystkich** 63 przetłumaczonych wystąpieniach zostaje `Channel 4` (np. „Musisz iść do wieżowca Channel 4.”), a etykieta mapy to dosłownie `Channel 4`. W plikach draftów **nie ma już ani jednego** „Kanał 4” — starszy wariant z `inventory-names-01.jsonl` został zastąpiony podczas uzgodnienia 40 etykiet.
- **Uzasadnienie:** to nazwa stacji telewizyjnej w świecie gry, prawdopodobnie nawiązanie do realnego kanału; tłumaczenie gubi aluzję.
- **Do decyzji:** potwierdzić `Channel 4` (stan obecny) albo przywrócić „Kanał 4” (wtedy trzeba też poprawić 63 zdania, gdzie nazwa pełni funkcję rzeczownika).
- **Uwaga:** nazwa wchodzi do polskich zdań w formie nieodmienionej („w wieżowcu Channel 4”, nie „w wieżowcu Kanale 4”). To spójne z decyzją R-09 o formach bazowych, ale jest odczuwalne stylistycznie.

## R-03 — Etykiety map (wszystkie 291, w tym 40 przepisanych) — **ROZSTRZYGNIĘTE: zostaje stan obecny**

> **Decyzja właściciela (2026-10-29): pozycja nieistotna — nie zmieniać.** Obowiązuje obecny korpus: 291 etykiet, 288 przetłumaczonych, 3 bez zmian (`Channel 4`, `START`, `Test`).

- **Stan (POTWIERDZONE):** `drafts/inventory-names-01.jsonl` zawiera **wszystkie 291** etykiet map: **288** przetłumaczonych, **3** bez zmian (`Channel 4`, `START`, `Test`). W ostatnim uzgodnieniu przepisano **40** etykiet — plik jest bajt w bajt zgodny z wersją z PR #5.
- **Przykłady przepisanych:** `PRE TITLE` → „PRZED EKRANEM TYTUŁOWYM”, `MC Home` → „Dom bohatera”, `Strip Center` → „Centrum handlowe”, `Foyer` → „Hol wejściowy”, `Storage` → „Magazyn”, `Police Station` → „Komisariat policji”.
- **Charakter:** etykiety widać na ekranie mapy/przejść, więc to tekst gracza; ale część z nich to nazwy robocze dewelopera (`PRE TITLE`, `TEST MAP` → „MAPA TESTOWA”), których gracz może nigdy nie zobaczyć.
- **Do decyzji:** A) zostawić wszystkie 288 tłumaczeń (stan obecny), B) przywrócić robocze nazwy tam, gdzie mapa jest nieosiągalna, C) punktowo — właściciel wskazuje mapy widoczne w grze.
- **Uwaga:** 70 z 291 map jest nieosiągalnych w statycznym BFS od startu (`reading/v1/README_PL.md`), więc część etykiet może być martwa — ale BFS jest przybliżony, nie dowodem.

## R-04 — „Craft this item?”: „Wytworzyć ten przedmiot?” czy „Wytworzyć przedmiot?” — **ROZSTRZYGNIĘTE: zostaje stan obecny**

> **Decyzja właściciela (2026-10-29): pozycja nieistotna — nie zmieniać.** Obowiązuje „Wytworzyć ten przedmiot?” (94 rekordy Map 46).

- **Stan:** w korpusie finalnym **„Wytworzyć ten przedmiot?”** (94 rekordy Map 46, identyczne powtórzenia).
- **Alternatywa:** „Wytworzyć przedmiot?” — krótsze, mniej „urzedowe”; mieści się lepiej w wąskim okienku UI.
- **Do decyzji:** A) „Wytworzyć ten przedmiot?”, B) „Wytworzyć przedmiot?”, C) „Wytworzyć?” (najkrótsze, ale traci dopełnienie).
- **Koszt zmiany:** jeden rekord źródłowy × 47 wystąpień; builder przebudowuje deterministycznie.

## R-05 — „You have items missing from this recipe.” — **ROZSTRZYGNIĘTE: zostaje stan obecny**

> **Decyzja właściciela (2026-10-29): pozycja nieistotna — nie zmieniać.** Obowiązuje „Brakuje ci przedmiotów potrzebnych do tego przepisu.” (94 rekordy).

- **Stan:** „Brakuje ci przedmiotów potrzebnych do tego przepisu.”
- **Alternatywa:** „Brakuje przedmiotów z tej receptury.” — krótsze, ale „receptura” brzmi technicznie.
- **Do decyzji:** A) stan obecny, B) krótszy wariant.
- **Uwaga:** to komunikat błędu widoczny przy każdej nieudanej próbie craftingu, więc długość ma znaczenie dla czytelności.

## R-06 — `He’s going to be` → „Będzie” — **ROZSTRZYGNIĘTE: zostaje stan obecny**

> **Decyzja właściciela (2026-10-29): pozycja nieistotna — nie zmieniać.** Obowiązuje „Będzie<br>” (komenda 430) przed „Wkurzony, kumasz?” (431).

- **Stan (POTWIERDZONE, kolejność sprawdzona w evencie):** to **pierwsza** z dwóch linii wiadomości w wątku `M. Deluna` — kolejność komend 430 → 431: „He’s going to be<br>” → **„Będzie<br>”**, a zaraz po niej „pissed, ya know?” → „Wkurzony, kumasz?”. Razem czytają się jako „Będzie wkurzony, kumasz?”.
- **Alternatywa:** „On będzie” (bliżej składni angielskiej, ale w polskim zaimka się nie powtarza).
- **Do decyzji:** A) „Będzie” (stan obecny), B) „On będzie”.
- **Uwaga:** linia jest dzielona między dwa rekordy — przy zmianie trzeba zachować spójność z fragmentem **następnym** w kolejności renderowania („Wkurzony, kumasz?”), bo razem tworzą jedno zdanie. „On będzie” też się wtedy czyta poprawnie; wybór jest stylistyczny.

## R-07 — Placeholdery mapy testowej — **ROZSTRZYGNIĘTE: wariant B (przywrócone angielskie)**

> **Decyzja właściciela (2026-10-29):** przywrócić angielskie `Text goes here<br>` — to wypełniacz dewelopera, bez wartości gracza.
> Wykonane: 7 rekordów `native_message` z TEST MAP usuniętych z `drafts/visible-ui-remaining-01.jsonl`; bramka pokrycia
> klasyfikuje je jako `owner_decision_R07_test_map_placeholder_kept_in_english` (reguła działa **tylko** dla `map_name == "TEST MAP"`).

- **Stan (POTWIERDZONE):** 7 rekordów `native_message` z **TEST MAP, EV001**, każdy `Text goes here<br>` → „Tekst w tym miejscu<br>”. To jawnie renderowane wypełniacze dewelopera.
- **Dylemat:** tłumaczenie placeholdera dewelopera to praca bez wartości gracza; z drugiej strony jeśli mapa jest osiągalna, gracz zobaczy polski tekst.
- **Do decyzji:** A) zostawić tłumaczenie (stan obecny), B) przywrócić angielskie wypełniacze, C) zostawić tylko tam, gdzie mapa jest osiągalna.

## R-08 — `TEXT` → „TEKST” (mapa TEST MAP) — **ROZSTRZYGNIĘTE: wariant B (przywrócony `TEXT`)**

> **Decyzja właściciela (2026-10-29):** przywrócić `TEXT` razem z R-07. Wykonane: rekord `phone_text`
> usunięty z draftów; powód w bramce: `owner_decision_R08_test_map_stub_kept_in_english`.
> **NIEZWERYFIKOWANE:** czy `TEXT` jest kluczem dopasowywanym przez kod gry — kod nie jest dostępny lokalnie.

- **Stan (POTWIERDZONE):** literał `TEXT` to `phone_text` z **TEST MAP, EV021** — czyli stub mapy testowej, nie element produkcyjnego UI. Przetłumaczony na „TEKST”.
- **Ryzyko (HIPOTEZA, niskie):** gdyby ten literał był kluczem dopasowywanym przez kod gry, zmiana mogłaby zepsuć logikę testową. Kod gry nie jest lokalnie dostępny, więc nie sprawdzono; skoro to mapa testowa, skutek byłby ograniczony.
- **Do decyzji:** A) zostawić „TEKST”, B) przywrócić `TEXT` razem z R-07 (oba są stubami TEST MAP), C) sprawdzić w runtime i wrócić do tematu.

## R-09 — Odmiana imion — **ROZSTRZYGNIĘTE: wariant B (ujednolicić odmianę)**

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

> **Decyzja właściciela (2026-10-29): wariant B — ujednolicić odmianę, bez ponownego tłumaczenia.**
> **Wykonanie (POTWIERDZONE):** narzędzie `tools/unify_name_declension.py` odmienia **wyłącznie** formy, których przypadek
> da się ustalić składniowo, i tylko dla imion na `-a` z tabelą form (`Erica, Andrea, Arianna, Melissa, Ella, Toma, Diana, Tasha, Alia`):
> wołacz po przecinku / w całej kwestii / na początku zdania oraz dopełniacz po rzeczowniku lub przyimku („fragment Toma” → „fragment Tomy”).
> Wynik: **383 wystąpienia w 380 rekordach** (148 plików) — `vocative_comma_address` 247, `vocative_whole_utterance` 89,
> `vocative_leading_address` 29, `genitive_governor` 18. **628 wystąpień** w formach, których nie da się rozstrzygnąć
> bez kontekstu (m.in. mianownik po `jest`, „z Chloe”, nazwiska), zostaje bez zmian i jest wypisane w raporcie
> `translation/reports/declension_r09_report.json`. Drugi przebieg daje zero zmian (test idempotencji).
> **Świadome ograniczenie:** to nie jest pełna odmiana wszystkich ~1 400 wystąpień — wolimy 628 form mianownikowych
> niż 200 błędnych form w zdaniach z przyimkami niejednoznacznymi (`z`, `o`, `na`).

## R-10 — `WoNoChurch` → „WoNo — kościół” — **ROZSTRZYGNIĘTE: zostaje stan obecny**

> **Decyzja właściciela (2026-10-29): pozycja nieistotna — nie zmieniać.** Obowiązuje „WoNo — kościół”.

- **Stan:** częściowe tłumaczenie: niejasny prefiks `WoNo` zachowany, oczywisty człon przetłumaczony.
- **Alternatywy:** „Kościół WoNo”, „WoNoChurch” bez zmian.
- **Do decyzji:** A) stan obecny, B) „Kościół WoNo”, C) bez zmian.

## R-11 — Fonty i polskie glify — **POTWIERDZONE W GRZE (2026-10-29)**

- **Stan:** **POTWIERDZONE przez właściciela na jego kopii gry** (2026-10-29, po wgraniu patcha v0.1.1): napisy wyświetlają się **polską czcionką** (ą/ć/ę/ł/ń/ó/ś/ź/ż są widoczne), **opcje są po polsku**, a tekst **dobrze się zawija i łamie**. To zdejmuje największe ryzyko projektu.
- **Co pozostaje NIEZWERYFIKOWANE:** pełne przejście gry (wszystkie mapy i warianty), zachowanie po wczytaniu save’a, długie kwestie w wąskich oknach UI oraz inne buildy produktu niż ten, na którym testowano. To już QA treści, nie ryzyko techniczne.
- **Ryzyko:** to najpoważniejsze ryzyko całego projektu — jeśli font nie ma glifów, cała praca jest niewidoczna w grze.
- **Do decyzji:** test na kopii gry (Windows) albo świadome zaakceptowanie ryzyka w POC.

---

## Podsumowanie do szybkiej decyzji

| ID | Temat | Rekomendacja agenta |
|---|---|---|
| R-01 | Tytuł gry | **rozstrzygnięte: wariant B** (oryginał) — wykonane |
| R-02 | `Channel 4` | **rozstrzygnięte: marka bez zmian** — korpus już spójny |
| R-03 | Etykiety map | **rozstrzygnięte: bez zmian** — 288 przetłumaczonych zostaje |
| R-04 | Crafting — pytanie | **rozstrzygnięte: bez zmian** — „Wytworzyć ten przedmiot?” |
| R-05 | Crafting — błąd | **rozstrzygnięte: bez zmian** |
| R-06 | Telefon | **rozstrzygnięte: bez zmian** — „Będzie” |
| R-07 | Placeholdery | **rozstrzygnięte: przywrócone angielskie** — wykonane |
| R-08 | `TEXT`/`TEKST` (TEST MAP) | **rozstrzygnięte: przywrócony `TEXT`** — wykonane |
| R-09 | Odmiana imion | **rozstrzygnięte: ujednolicić odmianę** — wykonane w 380 rekordach (patrz wyżej) |
| R-10 | `WoNoChurch` | **rozstrzygnięte: bez zmian** — „WoNo — kościół” |
| R-11 | Fonty | **POTWIERDZONE W GRZE** — polskie znaki, opcje PL i zawijanie tekstu działają |

---

## Redakcja stylistyczna 2026-10-29 — klastry fraz (decyzja wykonawcza)

- **Decyzja właściciela:** urozmaicać wyłącznie **klastry** — to samo wyrażenie powtórzone w jednej scenie. Pojedyncze wystąpienia w różnych scenach zostają bez zmian.
- **Zasada nadrzędna:** **identyczne źródło → identyczne tłumaczenie.** Przed zmianą porównuj `source_text`; powtórzenie w źródle nie jest błędem tłumacza. Jedyny taki klaster (CE17, 6×) pozostawiony bez zmian.
- **Wykonanie:** 27 rekordów, warianty leksykalne w granicach znaczenia i rejestru; `do cholery` 344 → 324, `w porządku` 183 → 176.
- **Spójność krótkich źródeł:** 15 przypadków divergentnych → **8**. Odrzucone „poprawki” z uzasadnieniem: `Church` (motywy vs etykiety map), `Equip` (dwa sloty komend), `Hannah?`/`Ellę?` (eliptyczne odpowiedzi), trzy pytania z odmienną płcią mówiącego, `Anal` (opcja vs podpis obrazu).
- **Status:** [POTWIERDZONE] liczby z `translation/reports/editorial_qa_v1.json`; [NIEZWERYFIKOWANE] odbiór stylistyczny w grze — do oceny właściciela przy pełnym przejściu.
