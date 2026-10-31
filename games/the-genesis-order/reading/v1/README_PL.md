# Czytanka TGO PL — wydanie robocze v1

## Jak czytać

- Zacznij od `chronological_script_PL.md` (pełny tekst). Wersje rozdziałów są osobno w `episodes/`, `reading_order.tsv` podaje kolejność i podstawę sortowania, a `index_characters_PL.md` i `index_locations_PL.md` są indeksami mówców i lokacji.
- Każda kwestia ma jawnego mówcę, gdy można go statycznie odczytać z kodu nagłówka; nierozpoznane nagłówki są oznaczone, nie zgadywane.
- **Ścieżka warunkowa** zachowuje wybory i warunki z kontekstu eventu. Wybory są listowane w miejscu polecenia. Mówca, etykiety i dialog pochodzą ze scalonych tłumaczeń; wartości kontrolne i nazwy własne pozostają źródłowe.
- Wartości `\V[n]`, `\N[n]` i `\P[n]` są oznaczane jako zmienna, imię aktora lub członek drużyny; `\I[n]` jako ikona. Niepewne wartości nie są zgadywane.
- **Imię bohatera:** w grze pozostaje placeholder `1Hero` (podstawiane imieniem gracza w runtime), ale w Czytance bohater nazywa się **Mox** i jest odmieniany przez przypadki (`Moxa`, `Moxowi`, `Moxem`, `Moxie`). Odmiana działa na warstwie Czytanki i nie zmienia tekstu gry; reguły i raport decyzji: `tools/hero_declension.py` i `translation/reports/hero_declension_v1.json`.
- **🎬 Wstawka wideo** to znacznik miejsca, w którym scenariusz uruchamia klip z `www/movies` (np. `AdChng1.mp4`). Nazwa pochodzi z polecenia `ysp.VideoPlayer.newVideo(...)` odczytanego statycznie z `www/data`, a rozszerzenie z inwentarza plików instalacji; znacznik nie odtwarza wideo i nie zmienia tekstu. Adnotacje: (zapętlone) dla pętli `setLoopById`, (pliku nie ma w inwentarzu tej kopii), gdy kod wskazuje nazwę bez odpowiadającego pliku. Zestawienie plików jest w `index_movies_PL.md`.

## Ważne ograniczenie chronologii

Kolejność jest **przybliżona i statyczna**, nie kanoniczna: początkowa kolejność map to BFS po bezpośrednich transferach RPG Maker i rozpoznanych wywołaniach Common Events z mapy startowej 38. Warunki, przełączniki, zmienne, wybory oraz runtime nie są wykonywane. **221/291** map ma potencjalną ścieżkę od startu w tym grafie; pozostałe są na końcu w kolejności edytora. Common Events sortujemy po pierwszym znalezionym wywołaniu, a nie po gwarantowanej kolejności rozgrywki. Sceny opcjonalne/ponownie odtwarzane mogą mieć inne miejsce; nie traktuj ich sąsiedztwa jako jednej rozgrywki.

To zachowuje ostrzeżenie z przykładowych skryptów SRW: warunkowe/sytuacyjne kwestie nie tworzą jednej, gwarantowanej osi czasu.

## Statyczne źródła i liczby

- Numeracja rozdziałów i indeks lokacji są dziedziczone z wydania v1: źródła gry nie są przechowywane w repozytorium, więc grafu osiągalności ani nazw map nie przelicza się od zera. Treść kwestii pochodzi w całości z bieżącego korpusu tłumaczeń.
- Korpus: 45,229 kanonicznych rekordów; 39,917 rekordów z tłumaczeniem; nazwy własne, markery, kody i jawnie chronione wartości pozostają bez zmian.
- W tym wydaniu: 4136 rozdziałów map/event/page i 261 rozdziałów Common Events.
- Wstawki wideo: **3812** wywołań w **305** rozdziałach, **3696** plików; inwentarz: `index_movies_PL.md`.
- Gry nie uruchamiano. Nie dołączono assetów, mediów, kodu gry ani zapisów.
- Źródłowe ID w plikach pozwalają wrócić do rekordu JSONL. Pełna lista kolejności znajduje się w `reading_order.tsv`.
