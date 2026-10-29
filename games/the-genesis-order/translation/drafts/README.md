# Robocze tłumaczenia TGO

Stan na 2026-10-29. Wszystkie pliki w tym katalogu są **roboczymi zwrotkami** po stabilnych ID. Wymagają redakcji i kontroli terminologii; nie są zatwierdzonym przekładem, patchem ani dystrybucją gry. Kanoniczny eksport `../export-v1/` i source ZIP v1 pozostają niezmienione.

## Aktualny scalony stan

Najnowsze pełne scalenie znajduje się poza Git, w ignorowanym katalogu `google_drive/the-genesis-order/translation/merged-tgo-12692-reviewed-2026-10-29.jsonl`. Narzędzie `games/the-genesis-order/tools/merge_translation_batches.py` zweryfikowało **45 229 rekordów**: **12 692 niepuste tłumaczenia**, **131 rekordów chronionych** oraz **32 406 tłumaczalnych pól oczekujących**. Scalenie można odtworzyć z aktualnych partii poniżej. Nie jest to eksport kanoniczny.

## Aktualnie używane partie

| Zakres | Plik(i) | Rekordy z niepustym tłumaczeniem |
|---|---|---:|
| UI | `ui-01/` | 127 (130 rekordów, w tym chronione/niezmienione wartości) |
| Wskazówki Arianny | `hints/draft-hints-01.jsonl`–`draft-hints-09.jsonl` | 705 |
| Wybory | `choice-ui-01.jsonl` | 1 583 z 2 110 |
| Powtarzalny dialog | `custom-dialogue-repeated-01.jsonl`–`-06.jsonl` | 6 498 |
| Wybrane sceny common events | wszystkie `custom-dialogue-scene-*-01.jsonl` (13 plików) | 1 088 |
| Nazwy/etykiety | `inventory-names-02.jsonl` | 1 479; zawiera tłumaczenia etykiet map — nie dodawaj osobno `map-labels-01.jsonl` |
| Wiadomości natywne | `native-messages-03.jsonl` | 692 |
| UI kontaktów telefonu | `phone-contact-ui-02.jsonl` | 351 |
| Teksty telefonu i wartości zmiennych | `phone-and-vars-01.jsonl` | 133 |
| Typy systemowe | `system-types-01.jsonl` | 34 |
| Napisy końcowe | `credits-01.jsonl` | 2 |
| **Łącznie w aktualnym scaleniu** |  | **12 692** |

Wcześniejsze wersje partii pozostają dla historii, ale nie należy ich scalać razem z nowszymi zamiennikami: używaj `inventory-names-02`, `native-messages-03` i `phone-contact-ui-02`, nie ich wcześniejszych wariantów. Batch `map-labels-01.jsonl` został już uwzględniony w `inventory-names-02.jsonl`.

## Walidacja i zasady

Scalaj po ID, nie po treści, np. przez `python3 games/the-genesis-order/tools/merge_translation_batches.py` z aktualnymi partiami. Walidator sprawdza zgodność wszystkich pól źródłowych z eksportem, ID, tokeny, chronione wartości i konflikty; nie nadpisuje istniejącego wyniku. Nie zmieniaj ID, locatorów, hashy źródłowych, `source_text` ani struktury. Zachowuj wszystkie `keep_source_value` dokładnie.

Partie są wersją roboczą do redakcji. Potrzebne są kontrole kontekstu, terminologii, długości UI, polskich glifów i zachowania w grze. Żadna gra ani kod gry nie były uruchamiane; nie wykonano testu Windows/runtime. Nie modyfikuj `export-v1/` ani source ZIP v1.
