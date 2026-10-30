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

## Pomiar na stanie repozytorium z 2026-10-30

- 39 917 przetłumaczonych rekordów, 265 istniejących decyzji (w tym 5 `deferred`); 39 657 rekordów kwalifikuje się do ponownego / pierwszego przeglądu.
- 14 178 rekordów z co najmniej jednym sygnałem, zgrupowanych w 13 297 grup; **25 479** bez sygnału nadal wymaga przeglądu. Liczby są przybliżeniem nakładu selekcji, nie liczbą błędów. Priorytety są heurystyczne, duża liczba trafień jest poprawna.
- Kontrolny test na 34 historycznych poprawionych rekordach z rejestru wykrywa sygnał dla 34/34 dawnych tekstów bez korzystania ze znacznika wcześniejszej edycji. To zbiór celowo dobranych znanych błędów użytych w projektowaniu; wynik **nie jest miarą skuteczności na reszcie gry**, nie potwierdza jakości kontekstu ani nie obejmuje fałszywie dodatnich wyników.
- Testy jednostkowe sprawdzają znane przykłady, brak automatycznych zmian, grupowanie z oddzielnymi ID, filtrowanie jawnie sprzecznych gałęzi, brak fikcyjnej sceny oraz zmiany hasha przy zmianie sąsiedniej kwestii. Pełną zgodność w grze należy potwierdzić osobno.

## Następny etap

Przeglądać partie według priorytetu, stosując glosariusz i źródło, z kontekstem całej sceny tam, gdzie kilka linijek nie wystarcza. Sygnały są wyłącznie filtrem: obejmują również formy poprawne i nie wyłapują wszystkich problemów. Potrzebny jest dalszy przegląd rekordów bez sygnału oraz testy runtime; nigdy nie deklarować kompletnego audytu na podstawie pustej kolejki kandydatów.

## Węższa kolejka sprzeczności (2026-10-30)

Na prośbę o kolejkę znacznie mniejszą niż 14 tys. dodano `tools/focus_gender_candidates.py`. Nie ucina wyników do ustalonej liczby i nie zmienia tłumaczenia. Wykrywa wybrane sprzeczności form pierwszej osoby z przypisanym nagłówkiem, drugiej osoby z hipotetycznym rozmówcą oraz ograniczony zestaw orzeczników i `sam/sama`. Jeżeli najbliżsi różni mówcy po obu stronach wskazują różne osoby, nie wybiera adresata. Wynik podaje ID, tekst i uzasadnienie, ale ID sąsiadów trzeba odnaleźć w inwentarzu lub szerszej kolejce; przed decyzją trzeba przeczytać rzeczywistą scenę.

```bash
python3 games/the-genesis-order/tools/inventory_gender_review.py --output /tmp/tgo-focus-inventory.jsonl
python3 games/the-genesis-order/tools/focus_gender_candidates.py --input /tmp/tgo-focus-inventory.jsonl --output /tmp/tgo-focus.jsonl
```

Na aktualnym inwentarzu: **126 rekordów** (74 z hipotezą adresata, 32 pierwsza osoba, 11 orzecznik, 9 `sam/sama`; kategorie mogą się pokrywać). To nie liczba potwierdzonych błędów ani oszacowanie liczby wszystkich błędów. Przegląd kilku wyników wykazał fałszywe alarmy, np. „Erica! Zabrałaś duszę Eriki!?” z hipotetycznym adresatem Drab oraz „Sam nie zwiotczeje” przypisane mówiącej. Nagłówek może wskazywać ciało w scenie opętania; także nazwa sąsiada nie dowodzi adresata ani ścieżki. Precyzji nie zmierzono na reprezentatywnej próbie.

Kontrola czułości: w pamięci przywrócono pole `before` każdego z 34 wpisów `corrected` rejestru, nadano im status `unreviewed`, pozostawiono bieżące sąsiedztwo, po czym uruchomiono `focus()` dla całego inwentarza. Sito wskazało **19 z 34**. To nie jest reprezentatywna próba ani szacunek rzeczywistej czułości: przykłady były znane podczas projektowania, a rejestr obejmuje także cofniętą własną korektę opętania (`fc45...`), więc nie wszystkie pola `before` są błędami. Pozostałe 15 nie dostało sygnału. W szczególności samo wąskie sito nie wystarcza do pełnego audytu; należy zachować szerszą kolejkę i badać również rekordy bez sygnału. Wyniki wymagają indywidualnego rozstrzygnięcia, nigdy masowej korekty.
