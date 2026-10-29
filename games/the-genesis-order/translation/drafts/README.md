# Robocze tłumaczenia TGO

Stan na 2026-10-29. Wszystkie pliki w tym katalogu są **roboczymi zwrotkami** po stabilnych ID. Wymagają redakcji i kontroli terminologii; nie są zatwierdzonym przekładem, patchem ani dystrybucją gry. Kanoniczny eksport `../export-v1/` i source ZIP v1 pozostają niezmienione.

## Aktualny scalony stan

Najnowsze pełne scalenie znajduje się poza Git, w ignorowanym pliku `google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl`. Narzędzie `games/the-genesis-order/tools/merge_translation_batches.py` zweryfikowało **45 229 rekordów**: **20 610 niepustych tłumaczeń**, **131 rekordów chronionych** oraz **24 488 tłumaczalnych pól oczekujących**. Zgodnie z najnowszą instrukcją rozpoczęto przyrost 10 000 nowych draftów (cel 30 610 łącznie): po step11 dodano **1 453 nowe, unikalne rekordy**, pozostało 8 547. Te rekordy są opisane osobno poniżej i nie należą do step11. Poniższa tabela opisuje skład ostatniego pełnego scalenia, a nie nowego przyrostu. Nie jest to eksport kanoniczny. SHA-256 step11: `ac4897fea1585267e6390d36b417ccf628c768c2200870e2ccf100aaf5d003ea`.

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

Wszystkie poniższe pliki zawierają łącznie **1 453** świeże rekordy draftów (1 001 dialogów map + 452 kwestie w 10 Common Events). Nie są częścią merged step11 ani tabeli wyżej. Weryfikacja sprawdziła 1 453 unikalne ID, brak ID już przetłumaczonych w step11 oraz zgodność źródeł z kanonicznym eksportem. Po walidacji łączny licznik wyniósłby 22 063; do bieżącego celu 30 610 pozostałoby 8 547.

| Zakres | Plik(i) | Drafty |
|---|---|---:|
| Map 9 | `custom-dialogue-map9-events-82-55-97-17-95-01.jsonl`, `custom-dialogue-map9-events-59-78-8-4-43-01.jsonl`, `custom-dialogue-map9-followups-05.jsonl` | 309 |
| Map 23 | `custom-dialogue-map23-followups-02.jsonl`–`-04.jsonl` | 230 |
| Map 24 | `custom-dialogue-map24-followups-03.jsonl`–`-04.jsonl` | 222 |
| Map 116 | `custom-dialogue-map116-followups-03.jsonl`–`-04.jsonl` | 240 |
| Common Events 325, 328, 351, 401, 403, 411, 426, 443, 445, 451 | po jednym `custom-dialogue-common-event-<ID>-01.jsonl` | 452 |
| **Suma przyrostu** |  | **1 453** |

Wcześniejsze wersje partii pozostają dla historii, ale nie należy ich scalać razem z nowszymi zamiennikami: używaj `inventory-names-02`, `native-messages-03` i `phone-contact-ui-02`, nie ich wcześniejszych wariantów. Batch `map-labels-01.jsonl` został już uwzględniony w `inventory-names-02.jsonl`. Sceny obejmują 13 wcześniejszych i 7 kolejnych plików; aktualny zestaw zawiera Common Event 25, 15 scen Common Events ze step10 oraz 50 nowych follow-upów Common Events ze step11 (2 730 wierszy), a także dialog Map 20/31, eventy Map 3 (22, 31, 37, 39, 41, 45, 47, 56; sensowny dialog Map 3 jest pokryty) i follow-upy Map 23/24/9/116. Wszystkie partie pozostają do redakcji; znaczniki komend/statusów nie są tłumaczone na ślepo.

## Walidacja i zasady

Scalaj po ID, nie po treści, np. przez `python3 games/the-genesis-order/tools/merge_translation_batches.py` z aktualnymi partiami. Walidator sprawdza zgodność wszystkich pól źródłowych z eksportem, ID, tokeny, chronione wartości i konflikty; nie nadpisuje istniejącego wyniku. Nie zmieniaj ID, locatorów, hashy źródłowych, `source_text` ani struktury. Zachowuj wszystkie `keep_source_value` dokładnie.

Partie są wersją roboczą do redakcji. Potrzebne są kontrole kontekstu, terminologii, długości UI, polskich glifów i zachowania w grze. Żadna gra ani kod gry nie były uruchamiane; nie wykonano testu Windows/runtime. Nie modyfikuj `export-v1/` ani source ZIP v1.
