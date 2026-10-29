# Robocze tłumaczenia TGO

Stan na 2026-10-29. Wszystkie pliki w tym katalogu są **roboczymi zwrotkami** po stabilnych ID. Wymagają redakcji i kontroli terminologii; nie są zatwierdzonym przekładem, patchem ani dystrybucją gry. Kanoniczny eksport `../export-v1/` i source ZIP v1 pozostają niezmienione.

## Aktualny scalony stan

Najnowsze pełne scalenie znajduje się poza Git, w ignorowanym pliku `google_drive/the-genesis-order/translation/merged-tgo-working-2026-10-29-step11.jsonl`. Narzędzie `games/the-genesis-order/tools/merge_translation_batches.py` zweryfikowało **45 229 rekordów**: **20 610 niepustych tłumaczeń**, **131 rekordów chronionych** oraz **24 488 tłumaczalnych pól oczekujących**. Po step11 powstało dotąd **20 746 nowych, unikalnych draftów w 232 osobnych plikach**: pierwsze 10 140 przekroczyło dawny cel +10 000 o 140, dalsze partie dodały 2 521, partie Map 6/41/44 dodały 392, Map 96 dodała 126, Map 51 dodała 119, Map 60 dodała 119, Map 200 dodała 129, a automatyczne partie auto-01 (5 664 dialogi z pozostałych map, 1 293 kwestie z pozostałych kategorii oraz 243 wpisy bez liter) dodały **7 200** draftów i domknęły pokrycie do pełnego pułapu. Łączna projekcja wynosi **41 356 unikalnych niepustych tłumaczeń** (liczonych po ID, bez powielania alternatywnych draftów) — **100% teoretycznego pułapu** po odjęciu 131 chronionych rekordów i 3 742 tokenów sterujących. Bieżący cel 45 000 dotyczył wyłącznie tekstu widocznego dla gracza; został przekroczony na poziomie łącznego pokrycia tłumaczalnych pól — wszystkie naturalne dialogi `custom_dialogue` (34 896) oraz wszystkie kwalifikujące się rekordy pozostałych kategorii są już pokryte. Wszystkie dodatki pozostają osobnymi, niescalonymi i wymagającymi redakcji partiami; szczegóły znajdują się poniżej. Pierwsza tabela opisuje skład pełnego scalenia step11, a nie nowych przyrostów. Nie jest to eksport kanoniczny. SHA-256 step11: `ac4897fea1585267e6390d36b417ccf628c768c2200870e2ccf100aaf5d003ea`.

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

## Pierwszy przyrost po step11 — 10 140 draftów, jeszcze niescalony

Pierwszy zestaw po step11 obejmuje **5 004** świeże rekordy draftów w 74 plikach: 1 001 dialogów z Map 9/23/24/116, 557 z Map 41/55, 203 z Map 44, 328 z Map 82, 370 z Map 54, 230 z Map 6, 359 z Map 26 oraz 1 956 kwestii w 57 Common Events. Nie są częścią merged step11 ani tabeli wyżej. Dodatkowe **5 136** rekordów w 21 nowszych plikach opisano w następnej tabeli. Audyt wszystkich 10 140 nowych ID potwierdził unikalność, brak nakładania z tłumaczeniami step11, zgodność metadanych z kanonicznym eksportem, niepuste/przycięte tłumaczenia oraz markup/control tokens. Na tym pierwszym etapie projekcja wynosiła 30 750 niepustych tłumaczeń, o 140 ponad ówczesny cel +10 000. Wszystkie partie nadal wymagają redakcji.

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
| **Suma pierwszego zestawu** |  | **5 004** |

### Dodatkowe partie map (5 136 rekordów w 21 plikach)

| Mapa | Plik | Drafty |
|---|---|---:|
| Map 201 | `custom-dialogue-map201-finale-followups-01.jsonl` | 316 |
| Map 15 | `custom-dialogue-map15-warehouse-followups-01.jsonl` | 299 |
| Map 157 | `custom-dialogue-map157-hell-followups-01.jsonl` | 290 |
| Map 16 | `custom-dialogue-map16-heather-home-followups-01.jsonl` | 284 |
| Map 144 | `custom-dialogue-map144-library-followups-01.jsonl` | 283 |
| Map 13 | `custom-dialogue-map13-strip-center-followups-01.jsonl` | 266 |
| Map 4 | `custom-dialogue-map4-apartments-followups-01.jsonl` | 258 |
| Map 21 | `custom-dialogue-map21-chapel-followups-01.jsonl` | 252 |
| Map 33 | `custom-dialogue-map33-east-wing-followups-01.jsonl` | 250 |
| Map 141 | `custom-dialogue-map141-warehouse-followups-01.jsonl` | 247 |
| Map 11 | `custom-dialogue-map11-gym-followups-01.jsonl` | 244 |
| Map 76 | `custom-dialogue-map76-kimura-home-followups-01.jsonl` | 243 |
| Map 62 | `custom-dialogue-map62-farm-cave-followups-01.jsonl` | 235 |
| Map 49 | `custom-dialogue-map49-church-attic-followups-01.jsonl` | 227 |
| Map 78 | `custom-dialogue-map78-channel4-kimura-followups-01.jsonl` | 223 |
| Map 30 | `custom-dialogue-map30-dicks-restaurant-followups-01.jsonl` | 219 |
| Map 28 | `custom-dialogue-map28-arianna-morning-followups-01.jsonl` | 214 |
| Map 125 | `custom-dialogue-map125-toma-rift-followups-01.jsonl` | 199 |
| Map 27 | `custom-dialogue-map27-housewarming-followups-01.jsonl` | 197 |
| Map 32 | `custom-dialogue-map32-station-followups-01.jsonl` | 195 |
| Map 87 | `custom-dialogue-map87-mansion-ambush-followups-01.jsonl` | 195 |
| **Suma drugiego zestawu** |  | **5 136** |
| **Łącznie po step11** | **95 plików** | **10 140** |

Pierwszy przyrost był o **140** rekordów większy od ówczesnego celu 10 000; projekcja wynosiła wtedy **30 750**. Partie pozostają oddzielne od step11 i nie zostały scalone.

## Dalsze partie naturalnego dialogu — 2 521 draftów

Po osiągnięciu pierwszego przyrostu dodano jeszcze cztery partie Common Events oraz dialog z Map 12, 19, 25, 34, 52, 61, 94, 101, 114, 151 i 203:

| Zakres | Plik | Drafty |
|---|---|---:|
| Common Events — NPC barks / follow-ups | `custom-dialogue-common-event-npc-barks-followups-01.jsonl` | 205 |
| Common Events — NPC barks / follow-ups | `custom-dialogue-common-event-npc-barks-followups-02.jsonl` | 200 |
| Common Events — dialogue follow-ups | `custom-dialogue-common-event-dialogue-followups-03.jsonl` | 195 |
| Common Events — story follow-ups | `custom-dialogue-common-event-story-followups-04.jsonl` | 192 |
| Map 114 — 10 eventów | `custom-dialogue-map114-followups-01.jsonl` | 178 |
| Map 151 — Hell, 26 eventów | `custom-dialogue-map151-hell-followups-02.jsonl` | 192 |
| Map 12 — Arianna / church, 6 eventów | `custom-dialogue-map12-arianna-followups-01.jsonl` | 140 |
| Map 19 — Mansion, 20 eventów | `custom-dialogue-map19-followups-01.jsonl` | 185 |
| Map 25 — dinner, 16 eventów | `custom-dialogue-map25-dinner-followups-01.jsonl` | 148 |
| Map 34 — commissioner, 5 eventów | `custom-dialogue-map34-commissioner-followups-01.jsonl` | 143 |
| Map 52 — Ella / Chloe, 7 eventów | `custom-dialogue-map52-ella-chloe-followups-01.jsonl` | 135 |
| Map 61 — gym / locker room, 15 eventów | `custom-dialogue-map61-gym-followups-01.jsonl` | 156 |
| Map 94 — church, 16 eventów | `custom-dialogue-map94-church-followups-01.jsonl` | 139 |
| Map 101 — Heather / sleepover, 14 eventów | `custom-dialogue-map101-heather-sleepover-followups-01.jsonl` | 142 |
| Map 203 — courtroom, 8 eventów | `custom-dialogue-map203-courtroom-followups-01.jsonl` | 171 |
| **Suma dalszych partii** | **15 osobnych plików** | **2 521** |

Łącznie po step11 jest teraz **20 746 świeżych, unikalnych ID w 232 plikach**, co daje projekcję **41 356** niepustych tłumaczeń (pełne pokrycie pułapu 41 356). Test sprawdza zgodność wszystkich 2 521 nowych rekordów z eksportem kanonicznym, kompletność, tokeny/placeholdery, brak slash-prefixed komend, brak ID chronionych oraz brak duplikatów i nakładania z wcześniejszymi draftami. Wszystkie 792 zinwentaryzowane wiersze naturalnego tekstu Common Events są już opracowane, a wszystkie naturalne dialogi map (34 896 `custom_dialogue`) oraz pozostałe kwalifikujące się kategorie zostały domknięte partiami auto-01. Poprzedni podzbiór 5 664 wierszy (Map 6, 41, 44, 96, 51, 60, 200 oraz Map 12, 19, 25, 34, 52, 61, 94, 101, 114, 151, 203) jest już wliczony w pełne pokrycie. Partie wymagają redakcji, są niescalone, a kanoniczny eksport i source ZIP v1 pozostają bez zmian.

### Kolejne partie — Map 6, 41, 44, 96, 51, 60 i 200 (885 draftów)

| Zakres | Plik | Drafty |
|---|---|---:|
| Map 6 — church, 16 eventów | `custom-dialogue-map6-church-followups-02.jsonl` | 137 |
| Map 41 — farm/barn, 15 eventów | `custom-dialogue-map41-followups-02.jsonl` | 130 |
| Map 44 — mansion, 22 eventy | `custom-dialogue-map44-mansion-followups-02.jsonl` | 125 |
| Map 96 — farm/cottage, 10 eventów | `custom-dialogue-map96-followups-01.jsonl` | 126 |
| Map 51 — cam/stream, 8 eventów | `custom-dialogue-map51-followups-01.jsonl` | 119 |
| Map 60 — police/gym, 12 eventów | `custom-dialogue-map60-followups-01.jsonl` | 119 |
| Map 200 — hell/portal, 15 eventów | `custom-dialogue-map200-followups-01.jsonl` | 129 |
| **Suma nowych partii** | **7 plików** | **885** |

Nowe 885 ID przeszły audyt zgodności z kanonicznym eksportem, kompletności, tokenów i braku overlapu; buildery odmawiają nadpisania i przechodzą `py_compile`. Projekcja po tych partiach wynosiła 34 275, a po domknięciu partiami auto-01 wynosi 41 356.

### Partie automatyczne auto-01 — pełne domknięcie do pułapu 41 356 (7 200 draftów)

| Zakres | Plik(i) | Drafty |
|---|---|---:|
| Pozostałe mapy — wszystkie naturalne `custom_dialogue` nieobjęte wcześniejszymi partiami (Map 5, 7, 10, 14, 17, 18, 22, 24, 29, 35, 39, 42, 43, 45, 47, 48, 53, 55, 56, 57, 58, 59, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73, 74, 77, 79, 81, 83, 84, 85, 86, 95, 97, 98, 99, 100, 102, 103, 104, 105, 106, 107, 108, 109, 112, 113, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 139, 140, 142, 143, 145, 146, 147, 148, 149, 150, 152, 153, 154, 155, 156, 158, 159, 160, 161, 162, 164, 165, 166, 167, 168, 169, 170, 172, 174, 176, 179, 180, 181, 182, 183, 185, 186, 188, 190, 193, 199, 202, 204, 205, 206, 214, 215, 216, 217, 218, 230, 240, 245, 246, 252, 257, 258, 267, 274, 275, 276, 277, 282, 291) | `custom-dialogue-map*-auto-01.jsonl` (115 plików) | 5 664 |
| Pozostałe kategorie — wybór, napisy, wiadomości natywne itd. | `choice_option-auto-01.jsonl` (499), `credits-auto-01.jsonl` (237), `database-actors-name-auto-01.jsonl` (7), `database-items-name-auto-01.jsonl` (2), `image_caption-auto-01.jsonl` (68), `item_found_label-auto-01.jsonl` (1), `map_label-auto-01.jsonl` (1), `native_message-auto-01.jsonl` (420), `phone_contact_ui-auto-01.jsonl` (26), `phone_text-auto-01.jsonl` (3), `system-currencyUnit-auto-01.jsonl` (1), `system-gameTitle-auto-01.jsonl` (1), `ui-variable_value-auto-01.jsonl` (14), `ui_choice-auto-01.jsonl` (13) | 1 293 |
| Wpisy bez liter (liczby, symbole, `…`) | `misc-noalpha-auto-01.jsonl` | 243 |
| Poprawki tokenów | `custom-dialogue-map157-hell-followups-01.jsonl`, `custom-dialogue-map82-channel4-followups-01.jsonl`, `custom-dialogue-scene-toma-lillian-erica-01.jsonl` (naprawiono brak `1Hero`) | 3 |
| **Suma partii auto-01** | **~130 plików** | **7 200** |

Wszystkie 41 356 draftów przechodzi `apply_translation.validate_record(require_complete=True)` (0 błędów tokenów), zachowuje `1Hero` i inne placeholdery, oraz spełnia wymogi kanonicznego eksportu. Partie auto-01 są tłumaczeniem maszynowym wymagającym pełnej redakcji terminologicznej i stylistycznej; nie są zatwierdzonym przekładem.

Wcześniejsze wersje partii pozostają dla historii, ale nie należy ich scalać razem z nowszymi zamiennikami: używaj `inventory-names-02`, `native-messages-03` i `phone-contact-ui-02`, nie ich wcześniejszych wariantów. Batch `map-labels-01.jsonl` został już uwzględniony w `inventory-names-02.jsonl`. Sceny obejmują 13 wcześniejszych i 7 kolejnych plików; aktualny zestaw zawiera Common Event 25, 15 scen Common Events ze step10 oraz 50 follow-upów Common Events ze step11 (2 730 wierszy), a także dialog Map 20/31, eventy Map 3 (22, 31, 37, 39, 41, 45, 47, 56; sensowny dialog Map 3 jest pokryty) i follow-upy Map 23/24/9/116, pierwsze partie Map 41/55/44/82/54/6/26 i 57 Common Events oraz 21 nowszych partii map wyszczególnionych powyżej. Wszystkie partie pozostają do redakcji; znaczniki komend/statusów nie są tłumaczone na ślepo.

## Walidacja i zasady

Scalaj po ID, nie po treści, np. przez `python3 games/the-genesis-order/tools/merge_translation_batches.py` z aktualnymi partiami. Walidator sprawdza zgodność wszystkich pól źródłowych z eksportem, ID, tokeny, chronione wartości i konflikty; nie nadpisuje istniejącego wyniku. Nie zmieniaj ID, locatorów, hashy źródłowych, `source_text` ani struktury. Zachowuj wszystkie `keep_source_value` dokładnie.

Partie są wersją roboczą do redakcji. Potrzebne są kontrole kontekstu, terminologii, długości UI, polskich glifów i zachowania w grze. Żadna gra ani kod gry nie były uruchamiane; nie wykonano testu Windows/runtime. Nie modyfikuj `export-v1/` ani source ZIP v1.
