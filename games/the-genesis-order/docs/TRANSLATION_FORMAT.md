# Format rekordów tłumaczeniowych — The Genesis Order

## Przechowywanie i zakres

Kanoniczny eksport tekstów źródłowych jest śledzony w Git na jawne polecenie właściciela projektu:

```text
games/the-genesis-order/translation/export-v1/
```

Zawiera **45 229 rekordów** w JSONL oraz `export_manifest.json`. Binarne assety gry pozostają poza Gitem. Tekstowe dane źródłowe, narzędzia oraz wszystkie robocze i gotowe tłumaczenia (w tym JSONL i używane Markdown) śledzimy w Git. Aktualne partie są w `translation/drafts/`; `google_drive/` służy jako dodatkowy warsztat i kopia, nie jedyne miejsce przechowywania.

Eksport zawiera tekst z RPG Maker MV JSON/Credits, potwierdzone statyczne UI JS oraz statyczne wartości zmiennych, dla których istnieje dowód przepływu przez `\\V[...]` do widocznego komunikatu, wyboru lub tekstu przewijanego. Source ZIP v1 jest śledzony w `games/the-genesis-order/translation/packages/` i publikowany na Google Drive; to pakiet źródłowy, nie przetłumaczona gra.

## Rekord v1

Każda linia JSONL ma `schema: tgo-translation-record-v1` i pola:

- `id`: stabilna przestrzeń identyfikatora + skrót SHA-256 kanonicznego locatora. ID zależy od miejsca w źródle, nie od tekstu; zatwierdzone zmiany etykiet kategorii zachowują istniejące ID.
- `category`, `classification`: rodzaj powierzchni i potwierdzenie jej renderowania. Wszystkie wiersze `401` i opcje `102` są pełnoprawnym tekstem do tłumaczenia.
- `source_text`: dokładna wartość źródłowa; `translation` pozostaje pusta.
- `markup_tokens`: kolejność placeholderów/escape’ów, m.in. RPG Maker, HTML i formatów.
- `source`: plik względny wobec oryginalnych assetów, SHA-256 wejścia, locator oraz dozwolony rodzaj write-back.
- `context`: event/page/warunki/gałąź, identyfikatory zmiennych, dowód powierzchni i — gdzie potrzebne — `translation_policy`.
- `structure`: rodzaj źródłowej komendy/literału i metadane konieczne do walidacji bez uruchamiania gry.

### Locatory i write-back

- `json_string_leaf`: wskazany JSON Pointer, w tym standardowe wiadomości, wybory i pola bazy.
- `script_string_literal`: statyczny literał przypisujący tekst do znanych kanałów CE60/CE222/CE53/CE223/CE224.
- `event_script_expression`: wyłącznie literalny string w operandzie skryptowym komendy 122, kiedy ten sam event/page ma widoczny sink zawierający jego `\\V[id]`. Importer waliduje zakres zmiennych, komendę, typ operandu i źródłową wartość; wyrażenia dynamiczne nie są przepuszczane.
- `js_string_literal`: zatwierdzony statyczny literał JS po offsetcie/wierszu; statyczny template literal może zostać zamieniony na zwykły literał, dynamiczny template jest odrzucany.
- `plugin_parameter`: klucz i ścieżka parametru w statycznym JSON `$plugins`; JavaScript nie jest wykonywany.
- `text_file_line`: wskazana linia Credits.

Stabilne ID obowiązuje przy niezmienionym locatorze. Przesunięcie źródła zmienia ID; importer nie dopasowuje po samym tekście.

## Zabezpieczenia

`apply_translation.py` sprawdza schemat, ID↔locator, hash pliku źródłowego, oryginalny tekst, duplikaty i tokeny. `--check` niczego nie zapisuje. Zwykłe `apply` tworzy kopię stagingową w `google_drive/` i nigdy nie nadpisuje źródła ani nie uruchamia gry.

`context.translation_policy=keep_source_value` blokuje zmianę pól, które są kwotami/markerami lub wartościami sterującymi. W bieżącym eksporcie chronione są m.in. kwoty i markery UI oraz Lovense `PC`/`LAN`/`Web`. Ich nie wolno zmieniać w miejscu; naruszenie kończy się błędem walidacji.

## Pokrycie i decyzje zakresowe

- 45 229 rekordów; wszystkie stabilne ID są unikalne, a wszystkie source hashe/locatory przechodzą `--check` dla 238 plików źródłowych.
- Wybory: 2 110 opcji w 695 grupach; każda opcja jest pełnoprawnym tekstem do tłumaczenia. 180 ma precyzyjniejszą kategorię `ui_choice`, pozostałe 1 930 `choice_option`.
- Natywne `401`: 1 513 nie-rendererowych wierszy; wszystkie są pełnoprawnym tekstem do tłumaczenia. Osiem scaffoldingowych wierszy rendererów nie trafia do pakietu.
- JS: skan statyczny 78 plików, 563 kandydatury, 35 potwierdzonych UI, 528 wykluczeń z jawnym powodem, 0 nierozstrzygniętych.
- Zmienna-display: 262 statyczne niepuste stringi docierające do widocznych escape’ów, 132 whitespace-only wartości pominięte, 128 kwot/markerów chronionych.
- Zgodnie z decyzją właściciela nie tłumaczymy tekstu wtopionego w obrazy i wideo. Dynamiczne dane runtime pochodzące z urządzeń/użytkowników są poza statycznym zakresem; oryginalne źródła JS/data i fonty nie są kopiowane do repo.

Eksport można odtworzyć z dostarczonych oryginalnych assetów poleceniem `python3 games/the-genesis-order/tools/export_translation.py`. Oczekuje ono lokalnych, ignorowanych danych w `google_drive/the-genesis-order/` oraz kuratorowanego pliku JS `translation/export-v1/reviewed_js_ui.jsonl`.

## Robocze partie i uzupełniająca walidacja

`tools/merge_translation_batches.py` łączy niepełne zwrotki z całym źródłowym eksportem po ID. Weryfikuje niezmienność wszystkich pozostałych pól, tokeny oraz konflikty, zapisuje tylko nowy plik pod `translation/` lub `google_drive/` i raportuje nieprzetłumaczone rekordy (chronione liczone oddzielnie). Nie czyta oryginalnych assetów i nie zastępuje `apply_translation.py --check`.

### Znane ograniczenie sygnatury v1: tag bez argumentu przed tekstem

`TOKEN_RE` traktuje `\<słowo>` jako tag razem z opcjonalnym argumentem w nawiasach. Tag bez argumentu zapisany bezpośrednio przed treścią — `\fbCraft this item?` — trafia więc do `markup_tokens` jako `\fbCraft`, a polska wersja (`\fbWytworzyć przedmiot?`) daje token `\fb` i jest odrzucana przez `validate_record` („Markup/token mismatch”). Dotyczy to 94 rekordów `native_message` na mapie `Crafting` (Map 46) i niczego więcej w całym eksporcie.

Wariant v2 (`tools/markup_signature.py`, `tokens_v2`) rozdziela jawnie zdefiniowaną listę tagów bez argumentu — obecnie wyłącznie `\fb` — od następnego słowa. Różni się od v1 wyłącznie na tych 94 rekordach. Gotowe zwrotki leżą w [`../pending/`](../pending/README.md) i czekają na decyzję właściciela (ADR 002); do tego czasu walidator pozostaje bez zmian.

Sygnatura `markup_tokens` eksportu v1 pozostaje bez zmian dla zgodności. Import Markdown i `apply_translation.py` dodatkowo porównują RPG Maker escape’y interpunkcyjne oraz parametry pozycyjne `%1`, `%2` itd., których wcześniejsza sygnatura nie uwzględniała. `--require-complete` dopuszcza puste chronione wartości `keep_source_value`, ale działa tylko na dostarczonych rekordach: samo sprawdzenie niepełnej partii nie dowodzi kompletności całego eksportu.
