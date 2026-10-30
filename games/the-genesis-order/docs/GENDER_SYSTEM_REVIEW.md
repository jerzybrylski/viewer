# Systemowy przegląd rodzaju — partie kontekstowe

## Cel i ograniczenia

Audyt nie jest ukończony. Celem jest przegląd większymi, możliwymi do wznowienia partiami, nie automatyczne „naprawianie” końcówek. Narzędzie nie tłumaczy i niczego nie zmienia w korpusie. Nie używa MT, nie uruchamia kodu gry i nie wymaga dodatkowych bibliotek.

Nowy `tools/prepare_gender_review_batches.py`:

1. Czyta inwentarz oparty na walidowanym scaleniu wszystkich draftów z eksportem, z aktualnymi statusami z rejestru.
2. Oznacza heurystyczne sygnały m.in. form rozdzielnych, pierwszej osoby, adresata, liczby mnogiej, orzeczników, wcześniejszych automatycznych edycji i znanych scen opętania. To **priorytety przeglądu**, nie orzeczenia o błędach.
3. Grupuje powtarzające się dokładne źródło, przekład, kategorię i nagłówek; każde wystąpienie ma nadal **własny ID, warunki i kontekst**. Ta sama treść może odnosić się do różnych osób — nie kopiować decyzji bez odczytania każdego wystąpienia.
4. Dodaje po kilka sąsiednich rekordów z tej samej mapy/eventu/strony lub common eventu. Jawnie sprzeczne ramiona tej samej instrukcji warunkowej lub opcji są odrzucane, lecz **pozostałe sąsiedztwo nie gwarantuje wspólnej ścieżki**: warunki mogą być niepełne, instrukcje nie będące tekstem pominięte, a kolejność w grze dynamiczna.
5. Dodaje hash aktualnego fragmentu z sąsiadami (`context_snapshot_sha256`) do późniejszego porównania. Istniejący rejestr decyzji **nie sprawdza jeszcze automatycznie tego hasha**: sprawdza tekst i kontekst samego rekordu, a zmiana sąsiadów wymaga ponownej oceny ręcznej.

Mówca pokazany w wynikach to tylko wskazówka z nagłówka: w opętaniu może on wskazywać ciało, nie rzeczywistą tożsamość. Nie wiadomo automatycznie, kto jest adresatem; nie zakładać tego z samej obsady. Wartości niemożliwe do ustalenia odłożyć z powodem, a nie zmieniać na wyczucie.

## Odtwarzalny przebieg

```bash
python3 games/the-genesis-order/tools/inventory_gender_review.py --output /tmp/tgo-inventory.jsonl
python3 games/the-genesis-order/tools/prepare_gender_review_batches.py \
  --input /tmp/tgo-inventory.jsonl --output /tmp/tgo-review-000.jsonl \
  --max-groups 100 --context 3
# Kolejna strona na TYM SAMYM niezmienionym inwentarzu:
python3 games/the-genesis-order/tools/prepare_gender_review_batches.py \
  --input /tmp/tgo-inventory.jsonl --output /tmp/tgo-review-100.jsonl \
  --offset 100 --max-groups 100 --context 3
```

Polecenia nie nadpisują istniejącego pliku wyjściowego. Inwentarz i partie są odtwarzalne i nie są śledzone w Git. Po zmianie draftów lub rejestru trzeba utworzyć **nowy inwentarz** i zacząć od początku jego kolejki: `offset` odnosi się do jednego konkretnego snapshotu i nie jest stabilnym kursorem pomiędzy snapshotami. Jednoznaczne zmiany wprowadzać ręcznie w draftach z zachowaniem ID/source/tokenów i walidować; każde rozstrzygnięcie zapisać osobno w `translation/reports/gender_review_decisions.jsonl`, w tym powód, a niepewne oznaczyć `deferred`. Po zmianach zsynchronizować Czytankę, przebudować patch i sidecary, wykonać testy oraz wpisać wyniki do dziennika.

## Pomiar na stanie repozytorium z 2026-10-30 (po przeglądzie wąskiej kolejki)

- 39 917 przetłumaczonych rekordów, **850** decyzji w rejestrze (702 `confirmed`, 133 `corrected`, 15 `deferred`); 39 530 rekordów kwalifikuje się do ponownego / pierwszego przeglądu.
- 14 158 rekordów z co najmniej jednym sygnałem, zgrupowanych w 13 280 grup; **28 409** bez sygnału nadal wymaga przeglądu. Liczby są przybliżeniem nakładu selekcji, nie liczbą błędów. Priorytety są heurystyczne, duża liczba trafień jest poprawna.
- Wąskie sito po przeglądzie zwraca **1** pozycję (odłożona kwestia Kimberly, `eb528be8f3a7a510c15d`). To nie jest miara kompletności: sito obejmuje wybrane wzorce i nie widzi większości rekordów bez sygnału.
- Kontrolny test na 34 historycznych poprawionych rekordach z rejestru wykrywa sygnał dla 34/34 dawnych tekstów bez korzystania ze znacznika wcześniejszej edycji. To zbiór celowo dobranych znanych błędów użytych w projektowaniu; wynik **nie jest miarą skuteczności na reszcie gry**, nie potwierdza jakości kontekstu ani nie obejmuje fałszywie dodatnich wyników.
- Testy jednostkowe sprawdzają znane przykłady, brak automatycznych zmian, grupowanie z oddzielnymi ID, filtrowanie jawnie sprzecznych gałęzi, brak fikcyjnej sceny oraz zmiany hasha przy zmianie sąsiedniej kwestii. Pełną zgodność w grze należy potwierdzić osobno.

## Sygnały o wysokiej precyzji — nie wymagają dalszego przeglądu pojedynczo

Trzy „mówcowe” rodziny sprawdzono w całości (362 hipotezy): `winien/winna` (43), forma po `bym/żebym/gdybym` (181) i `powinienem/powinnam` (138). Wynik: **355 potwierdzeń, 7 odłożeń, 0 korekt**. Rodzina adresacka (`byś/żebyś`, 94 hipotezy) dała jednak **3 korekty** przy 91 potwierdzeniach — adresata nie koduje nagłówek, więc te kwestie trzeba czytać scenami. Wszystkie odłożenia to postaci bez mapowanej płci (systemowy NPC z CE25, „Ochrona”). Te sygnały nadają się więc wyłącznie jako kontrola, a nie jako kolejka robocza — masę błędów trzeba szukać w `inna_forma_rodzajowa`, `orzecznik_do_przegladu`, `mozliwy_przymiotnik_lub_rzeczownik` oraz w rekordach bez sygnału.

## Podgląd sceny (narzędzie tylko do odczytu)

Do decyzji potrzebna jest cała scena, nie trzy sąsiednie linijki. `tools/show_gender_scene.py` czyta inwentarz i wypisuje kwestie jednej mapy/eventu/strony albo jednego Common Eventu w kolejności poleceń: znacznik `>>`, indeks polecenia, nagłówek z rozpoznanym mówcą i płcią, tekst źródłowy i przekład. Narzędzie **nic nie zapisuje** (pilnuje tego `tests/test_show_gender_scene.py`) i nie ocenia tłumaczenia.

```bash
python3 games/the-genesis-order/tools/inventory_gender_review.py --output /tmp/tgo-inventory.jsonl
python3 games/the-genesis-order/tools/show_gender_scene.py \
  --inventory /tmp/tgo-inventory.jsonl --id tgo:custom_dialogue:0523d4464428d26ef567 --window 40
python3 games/the-genesis-order/tools/show_gender_scene.py \
  --inventory /tmp/tgo-inventory.jsonl --locator map:144:40:3 --only-scene
```

## Następny etap

Przeglądać partie według priorytetu, stosując glosariusz i źródło, z kontekstem całej sceny tam, gdzie kilka linijek nie wystarcza. Sygnały są wyłącznie filtrem: obejmują również formy poprawne i nie wyłapują wszystkich problemów. Potrzebny jest dalszy przegląd rekordów bez sygnału (28 409) oraz testy runtime; nigdy nie deklarować kompletnego audytu na podstawie pustej kolejki kandydatów.

## Węższa kolejka sprzeczności (2026-10-30)

Na prośbę o kolejkę znacznie mniejszą niż 14 tys. dodano `tools/focus_gender_candidates.py`. Nie ucina wyników do ustalonej liczby i nie zmienia tłumaczenia. Wykrywa wybrane sprzeczności form pierwszej osoby z przypisanym nagłówkiem, drugiej osoby z hipotetycznym rozmówcą oraz ograniczony zestaw orzeczników i `sam/sama`. Jeżeli najbliżsi różni mówcy po obu stronach wskazują różne osoby, nie wybiera adresata. Wynik podaje ID, tekst i uzasadnienie, ale ID sąsiadów trzeba odnaleźć w inwentarzu lub szerszej kolejce; przed decyzją trzeba przeczytać rzeczywistą scenę.

```bash
python3 games/the-genesis-order/tools/inventory_gender_review.py --output /tmp/tgo-focus-inventory.jsonl
python3 games/the-genesis-order/tools/focus_gender_candidates.py --input /tmp/tgo-focus-inventory.jsonl --output /tmp/tgo-focus.jsonl
```

Po przeglądzie całej tej kolejki (2026-10-30, 70 korekt, 31 potwierdzeń, 1 odłożenie) sito zwraca **1** hipotezę — odłożoną kwestię Kimberly. Wcześniejszy pomiar opisany niżej dotyczy stanu przed tym przeglądem.

Na ówczesnym inwentarzu: **126 rekordów** (74 z hipotezą adresata, 32 pierwsza osoba, 11 orzecznik, 9 `sam/sama`; kategorie mogą się pokrywać). To nie liczba potwierdzonych błędów ani oszacowanie liczby wszystkich błędów. Przegląd kilku wyników wykazał fałszywe alarmy, np. „Erica! Zabrałaś duszę Eriki!?” z hipotetycznym adresatem Drab oraz „Sam nie zwiotczeje” przypisane mówiącej. Nagłówek może wskazywać ciało w scenie opętania; także nazwa sąsiada nie dowodzi adresata ani ścieżki. Precyzji nie zmierzono na reprezentatywnej próbie.

Kontrola czułości: w pamięci przywrócono pole `before` każdego z 34 wpisów `corrected` rejestru, nadano im status `unreviewed`, pozostawiono bieżące sąsiedztwo, po czym uruchomiono `focus()` dla całego inwentarza. Sito wskazało **19 z 34**. To nie jest reprezentatywna próba ani szacunek rzeczywistej czułości: przykłady były znane podczas projektowania, a rejestr obejmuje także cofniętą własną korektę opętania (`fc45...`), więc nie wszystkie pola `before` są błędami. Pozostałe 15 nie dostało sygnału. W szczególności samo wąskie sito nie wystarcza do pełnego audytu; należy zachować szerszą kolejkę i badać również rekordy bez sygnału. Wyniki wymagają indywidualnego rozstrzygnięcia, nigdy masowej korekty.
