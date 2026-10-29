# Robocze tłumaczenia TGO

Stan na 2026-10-29. Wszystkie pliki w tym katalogu są **roboczymi zwrotkami** po stabilnych ID. Wymagają redakcji i kontroli terminologii; nie są zatwierdzonym przekładem, patchem ani dystrybucją gry. Kanoniczny eksport `../export-v1/` i source ZIP v1 pozostają niezmienione.

## Aktualny scalony stan

Najnowsze pełne scalenie znajduje się poza Git, w ignorowanym pliku `google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl`. Narzędzie `games/the-genesis-order/tools/merge_translation_batches.py` zweryfikowało **45 229 rekordów**: **20 610 niepustych tłumaczeń**, **131 rekordów chronionych** oraz **24 488 tłumaczalnych pól oczekujących**. Zgodnie z najnowszą instrukcją rozpoczęto przyrost 10 000 nowych draftów (cel 30 610 łącznie): po step11 dodano **5 004 nowe, unikalne rekordy**, pozostało 4 996. Po walidacji łączny licznik draftów wynosi 25 614. Te rekordy są opisane osobno poniżej i nie należą do step11. Poniższa tabela opisuje skład ostatniego pełnego scalenia, a nie nowego przyrostu. Nie jest to eksport kanoniczny. SHA-256 step11: `ac4897fea1585267e6390d36b417ccf628c768c2200870e2ccf100aaf5d003ea`.

## Aktualnie używane partie

| Zakres | Plik(i) | Rekordy z niepustym tłumaczeniem |
|---|---|---:|
| UI | `ui-01/` | 127 (130 rekordów, w tym chronione/niezmienione wartości) |
| Wskazówki Arianny | `hints/draft-hints-01.jsonl`–`draft-hints-09.jsonl` | 705 |
| Wybory | `choice-ui-01.jsonl` | 1 583 z 2 110 |
| Powtarzalny dialog | `custom-dialogue-repeated-01.jsonl`–`-06.jsonl` | 6 498 |
| Wybrane sceny common events | wszystkie `custom-dialogue-scene-*-01.jsonl` (20 plików) | 1 922 |
| Common Event 25 — teksty systemowe | `custom-dialogue-npc-system-01.jsonl` | 304 |
| Dodatkowe sceny Common Events (step10) | `custom-dialogue-common-event-*-01.jsonl` (15 plików) | 1 014 |
| Common Event follow-ups (step11) | 50 plików `custom-dialogue-common-event-*-01.jsonl` | 2 730 |
| Dialog Map 20 (Foyer) | wszystkie `custom-dialogue-map20-*.jsonl` | 985 |
| Dialog Map 31 | wszystkie `custom-dialogue-map31-*.jsonl` | 700 |
| Dialog Map 3 | wszystkie `custom-dialogue-map3-*.jsonl` | 728 |
| Dialog Map 24 | `custom-dialogue-map24-followups-*.jsonl` | 168 |
| Dialog Map 23 | `custom-dialogue-map23-*.jsonl` | 219 |
| Dialog Map 116 | `custom-dialogue-map116-*.jsonl` | 135 |
| Dialog Map 9 | `custom-dialogue-map9-*.jsonl` | 101 |
| Nazwy/etykiety | `inventory-names-02.jsonl` | 1 479; zawiera tłumaczenia etykiet map — nie dodawaj osobno `map-labels-01.jsonl` |
| Wiadomości natywne | `native-messages-03.jsonl` | 692 |
| UI kontaktów telefonu | `phone-contact-ui-02.jsonl` | 351 |
| Teksty telefonu i wartości zmiennych | `phone-and-vars-01.jsonl` | 133 |
| Typy systemowe | `system-types-01.jsonl` | 34 |
| Napisy końcowe | `credits-01.jsonl` | 2 |
| **Łącznie w aktualnym scaleniu** |  | **20 610** |

## Nowy przyrost po step11 — jeszcze niescalony

Wszystkie poniższe pliki zawierają łącznie **5 004** świeże rekordy draftów: 1 001 dialogów z Map 9/23/24/116, 557 z Map 41/55, 203 z Map 44, 328 z Map 82, 370 z Map 54, 230 z Map 6, 359 z Map 26 oraz 1 956 kwestii w 57 Common Events. Nie są częścią merged step11 ani tabeli wyżej. Weryfikacja sprawdziła 5 004 unikalne ID, brak ID już przetłumaczonych w step11, zgodność metadanych z kanonicznym eksportem oraz markup/control tokens. Po walidacji łączny licznik wynosi 25 614; do bieżącego celu 30 610 pozostało 4 996.

| Zakres | Plik(i) | Drafty |
|---|---|---:|
| Map 9 | `custom-dialogue-map9-events-82-55-97-17-95-01.jsonl`, `custom-dialogue-map9-events-59-78-8-4-43-01.jsonl`, `custom-dialogue-map9-followups-05.jsonl` | 309 |
| Map 23 | `custom-dialogue-map23-followups-02.jsonl`–`-04.jsonl` | 230 |
| Map 24 | `custom-dialogue-map24-followups-03.jsonl`–`-04.jsonl` | 222 |
| Map 116 | `custom-dialogue-map116-followups-03.jsonl`–`-04.jsonl` | 240 |
| Map 41 (events 11, 24, 32, 39, 45) | `custom-dialogue-map41-followups-01.jsonl` | 302 |
| Map 55 (events 3, 6, 25, 32) | `custom-dialogue-map55-followups-01.jsonl` | 255 |
| Common Events 257, 305, 307, 317, 324, 325, 327, 328, 330, 331, 332, 335, 350, 351, 365, 388, 393, 394, 398, 401, 403, 409, 411, 415, 416, 419, 421, 426, 439, 442, 443, 445, 451, 459, 464, 465, 467, 475, 483, 490 | po jednym `custom-dialogue-common-event-<ID>-01.jsonl` | 1 539 |
| Map 44 (eventy 27, 102, 93, 24, 25, 51) | `custom-dialogue-map44-mansion-followups-01.jsonl` | 203 |
| Map 82 (eventy 67, 24, 71, 45, 32, 20, 19, 75, 3, 21, 33, 34, 59, 62) | `custom-dialogue-map82-channel4-followups-01.jsonl` | 328 |
| Map 54 (27 eventów) | `custom-dialogue-map54-backyard-followups-01.jsonl` | 370 |
| Map 6 (eventy 5, 17, 28, 38) | `custom-dialogue-map6-church-followups-01.jsonl` | 230 |
| Map 26 (23 eventy) | `custom-dialogue-map26-mansion-followups-01.jsonl` | 359 |
| Common Events 277, 304, 316, 334, 349, 363, 368, 384, 396, 452, 456, 470 | po jednym `custom-dialogue-common-event-<ID>-02.jsonl` | 317 |
| Common Events 122, 340, 354, 359, 440 | po jednym `custom-dialogue-common-event-<ID>-01.jsonl` | 100 |
| **Suma przyrostu** |  | **5 004** |

Wcześniejsze wersje partii pozostają dla historii, ale nie należy ich scalać razem z nowszymi zamiennikami: używaj `inventory-names-02`, `native-messages-03` i `phone-contact-ui-02`, nie ich wcześniejszych wariantów. Batch `map-labels-01.jsonl` został już uwzględniony w `inventory-names-02.jsonl`. Sceny obejmują 13 wcześniejszych i 7 kolejnych plików; aktualny zestaw zawiera Common Event 25, 15 scen Common Events ze step10 oraz 50 follow-upów Common Events ze step11 (2 730 wierszy), a także dialog Map 20/31, eventy Map 3 (22, 31, 37, 39, 41, 45, 47, 56; sensowny dialog Map 3 jest pokryty) i follow-upy Map 23/24/9/116 oraz nowe partie Map 41/55/44/82/54/6/26 i 57 Common Events z bieżącego przyrostu. Wszystkie partie pozostają do redakcji; znaczniki komend/statusów nie są tłumaczone na ślepo.

## Walidacja i zasady

Scalaj po ID, nie po treści, np. przez `python3 games/the-genesis-order/tools/merge_translation_batches.py` z aktualnymi partiami. Walidator sprawdza zgodność wszystkich pól źródłowych z eksportem, ID, tokeny, chronione wartości i konflikty; nie nadpisuje istniejącego wyniku. Nie zmieniaj ID, locatorów, hashy źródłowych, `source_text` ani struktury. Zachowuj wszystkie `keep_source_value` dokładnie.

Partie są wersją roboczą do redakcji. Potrzebne są kontrole kontekstu, terminologii, długości UI, polskich glifów i zachowania w grze. Żadna gra ani kod gry nie były uruchamiane; nie wykonano testu Windows/runtime. Nie modyfikuj `export-v1/` ani source ZIP v1.
