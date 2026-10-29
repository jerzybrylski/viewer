# Robocze tłumaczenia TGO

Stan na 2026-10-29. Wszystkie pliki w tym katalogu są **roboczymi zwrotkami** po stabilnych ID. Wymagają redakcji i kontroli terminologii; nie są zatwierdzonym przekładem, patchem ani dystrybucją gry. Kanoniczny eksport `../export-v1/` i source ZIP v1 pozostają niezmienione.

## Aktualny scalony stan

Pełny, odtwarzalny audyt wszystkich **424 plików** w `drafts/` wykonał `tools/merge_translation_batches.py` na kanonicznym eksporcie: **45 229 rekordów**, **39 820 unikalnych niepustych tłumaczeń**, **131 rekordów chronionych** oraz **5 278 pustych pól niechronionych**. Warianty z 40 etykiet map w starszym `inventory-names-01.jsonl` uzgodniono z nowszym `inventory-names-02.jsonl` (te same wartości co w `map-labels-01.jsonl`); pełne scalenie nie wykrywa już konfliktów niepustych tłumaczeń. 468 przypadków pustej zwrotki obok wypełnionej to nakładające się wersje batchy, nie konflikt. Wiersze `map-labels-01.jsonl` są zduplikowanym podzbiorem `inventory-names-02.jsonl`, więc nie należy łączyć ich ponownie. Poprzednia projekcja **39 931** zawyżała pełny wynik o **111 ID** z powodu nakładających się wpisów; właściwa liczba po scaleniu po ID to **39 820**. Wśród pustych pól jest **3 742** rozpoznanych slash-prefixed komend w `custom_dialogue`; pozostałe **1 536** to tylko górny pułap rekordów do ręcznej oceny, nie gwarantowana liczba tłumaczalnych tekstów. Potwierdzono co najmniej 94 niewypełnione wiersze UI craftingu na Map 46 — po 47 razy „Craft this item?” i „You have items missing from this recipe.” Wykonane uzgodnienie nie zmienia eksportu kanonicznego ani source ZIP.

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

To zestawienie batchy jest historyczne. Pełny audyt wszystkich 424 plików, z deduplikacją stabilnych ID i kontrolą źródeł/tokenów, wykazał 39 820 niepustych tłumaczeń; wcześniejsza projekcja 39 931 zawyżała wynik o 111 powtórzonych ID. Nie ma już konfliktów między niepustymi wersjami. Wszystkie 792 zinwentaryzowane naturalne wiersze Common Events są opracowane. Pozostałe puste rekordy trzeba klasyfikować po kategorii: nie uznawać ich automatycznie za tekst gracza.

### Kolejne partie — Map 6, 41, 44, 96, 51, 60, 200 i 202 (1 008 draftów)

| Zakres | Plik | Drafty |
|---|---|---:|
| Map 6 — church, 16 eventów | `custom-dialogue-map6-church-followups-02.jsonl` | 137 |
| Map 41 — farm/barn, 15 eventów | `custom-dialogue-map41-followups-02.jsonl` | 130 |
| Map 44 — mansion, 22 eventy | `custom-dialogue-map44-mansion-followups-02.jsonl` | 125 |
| Map 96 — farm/cottage, 10 eventów | `custom-dialogue-map96-followups-01.jsonl` | 126 |
| Map 51 — cam/stream, 8 eventów | `custom-dialogue-map51-followups-01.jsonl` | 119 |
| Map 60 — police/gym, 12 eventów | `custom-dialogue-map60-followups-01.jsonl` | 119 |
| Map 200 — hell/portal, 15 eventów | `custom-dialogue-map200-followups-01.jsonl` | 129 |
| Map 202 — Hell temple, 8 eventów | `custom-dialogue-map202-followups-01.jsonl` | 123 |
| Map 55 — church, 14 eventów | `custom-dialogue-map55-followups-02.jsonl` | 118 |
| Map 121 — chapel/police, 18 eventów | `custom-dialogue-map121-followups-01.jsonl` | 118 |
| Map 57 — mansion, 8 eventów | `custom-dialogue-map57-followups-01.jsonl` | 116 |
| Map 104 — hideout, 3 eventy | `custom-dialogue-map104-followups-01.jsonl` | 117 |
| Map 108 — mansion kitchen, 6 eventów | `custom-dialogue-map108-followups-01.jsonl` | 116 |
| Map 81 — Channel 4, 12 eventów | `custom-dialogue-map81-followups-01.jsonl` | 106 |
| Map 85 — Channel 4, 11 eventów | `custom-dialogue-map85-followups-01.jsonl` | 102 |
| Map 24 — farm, 9 eventów | `custom-dialogue-map24-followups-01.jsonl` | 101 |
| Map 115 — mansion, 4 eventy | `custom-dialogue-map115-followups-01.jsonl` | 101 |
| Map 17 — police station, 12+ eventów | `custom-dialogue-map17-followups-01.jsonl` | 100 |
| Map 35 — interrogation, 12 eventów | `custom-dialogue-map35-followups-01.jsonl` | 100 |
| Map 79 — commissioner house | `custom-dialogue-map79-followups-01.jsonl` | 100 |
| Map 5 — mansion interior | `custom-dialogue-map5-followups-01.jsonl` | 97 |
| Map 56 — church, 12 eventów | `custom-dialogue-map56-followups-01.jsonl` | 95 |
| Map 100 — attic/safe, 14 eventów | `custom-dialogue-map100-followups-01.jsonl` | 95 |
| Map 63 — cave, 11 eventów | `custom-dialogue-map63-followups-01.jsonl` | 92 |
| Map 83 — Channel 4, 11 eventów | `custom-dialogue-map83-followups-01.jsonl` | 90 |
| Map 98 — forest/bugs, 10 eventów | `custom-dialogue-map98-followups-01.jsonl` | 88 |
| Map 128 — station aftermath, 9 eventów | `custom-dialogue-map128-followups-01.jsonl` | 85 |
| Map 158 — Duncan hideout, 10 eventów | `custom-dialogue-map158-followups-01.jsonl` | 85 |
| Map 183 — Hell/Lilith, 10 eventów | `custom-dialogue-map183-followups-01.jsonl` | 85 |
| Map 42 — mansion maids, 11 eventów | `custom-dialogue-map42-followups-01.jsonl` | 83 |
| Map 70 — church forest, 10 eventów | `custom-dialogue-map70-followups-01.jsonl` | 83 |
| Map 18 — commissioner dinner, 10 eventów | `custom-dialogue-map18-followups-01.jsonl` | 82 |
| Map 53 — waterfall, 10 eventów | `custom-dialogue-map53-followups-01.jsonl` | 82 |
| Map 120 — secret painting, 10 eventów | `custom-dialogue-map120-followups-01.jsonl` | 81 |
| Map 73 — church bathroom, 10 eventów | `custom-dialogue-map73-followups-01.jsonl` | 79 |
| Map 137 — dungeon, 10 eventów | `custom-dialogue-map137-followups-01.jsonl` | 79 |
| Map 257 — court/Carol farm, 10 eventów | `custom-dialogue-map257-followups-01.jsonl` | 77 |
| Map 59 — gym interrogation, 10 eventów | `custom-dialogue-map59-followups-01.jsonl` | 75 |
| Map 102 — cave/bunker, 10 eventów | `custom-dialogue-map102-followups-01.jsonl` | 75 |
| Map 43 — Lillian amulets, 10 eventów | `custom-dialogue-map43-followups-01.jsonl` | 74 |
| Map 48 — Carol farm continuation, 10 eventów | `custom-dialogue-map48-followups-01.jsonl` | 73 |
| Map 77 — mansion party, 10 eventów | `custom-dialogue-map77-followups-01.jsonl` | 68 |
| Map 47 — Carol/Hannah church, 10 eventów | `custom-dialogue-map47-followups-01.jsonl` | 67 |
| Map 124 — warehouse/Jon, 10 eventów | `custom-dialogue-map124-followups-01.jsonl` | 67 |
| Map 72 — forest/Judy, 10 eventów | `custom-dialogue-map72-followups-01.jsonl` | 66 |
| Map 240 — Heather car/ECU, 10 eventów | `custom-dialogue-map240-followups-01.jsonl` | 66 |
| Map 140 — swamp alligator, 10 eventów | `custom-dialogue-map140-followups-01.jsonl` | 61 |
| Map 116 — rift/Lilith, 10 eventów | `custom-dialogue-map116-followups-01.jsonl` | 60 |
| Map 153 — alligator Hannah/Alia, 10 eventów | `custom-dialogue-map153-followups-01.jsonl` | 58 |
| Map 190 — mansion chests, 10 eventów | `custom-dialogue-map190-followups-01.jsonl` | 57 |
| Map 245 — Tikpak treasure, 10 eventów | `custom-dialogue-map245-followups-01.jsonl` | 54 |
| Map 109 — sewer grates, 10 eventów | `custom-dialogue-map109-followups-01.jsonl` | 51 |
| Map 86 — Diana/Henry, 10 eventów | `custom-dialogue-map86-followups-01.jsonl` | 49 |
| Map 99 — chapel/Daemalius, 10 eventów | `custom-dialogue-map99-followups-01.jsonl` | 49 |
| Map 204 — Andrea crypto, 10 eventów | `custom-dialogue-map204-followups-01.jsonl` | 48 |
| Map 159 — spies/Ella, 10 eventów | `custom-dialogue-map159-followups-01.jsonl` | 47 |
| Map 22 — church Judy, 10 eventów | `custom-dialogue-map22-followups-01.jsonl` | 46 |
| Map 217 — Casula temple trap, 10 eventów | `custom-dialogue-map217-followups-01.jsonl` | 46 |
| Map 119 — Hannah apartment, 10 eventów | `custom-dialogue-map119-followups-01.jsonl` | 45 |
| Map 145 — interrogation, 10 eventów | `custom-dialogue-map145-followups-01.jsonl` | 45 |
| Map 105 — cave Hannah, 10 eventów | `custom-dialogue-map105-followups-01.jsonl` | 44 |
| Map 291 — lotion quest, 10 eventów | `custom-dialogue-map291-followups-01.jsonl` | 43 |
| Map 206 — Chloe apartment, 10 eventów | `custom-dialogue-map206-followups-01.jsonl` | 42 |
| Map 7 — Melissa cat, 10 eventów | `custom-dialogue-map7-followups-01.jsonl` | 41 |
| Map 149 — Madalyn capture, 10 eventów | `custom-dialogue-map149-followups-01.jsonl` | 41 |
| Map 160 — shooting range, 10 eventów | `custom-dialogue-map160-followups-01.jsonl` | 40 |
| Map 132 — ransacked Ella, 10 eventów | `custom-dialogue-map132-followups-01.jsonl` | 39 |
| Map 58 — Charles office, 10 eventów | `custom-dialogue-map58-followups-01.jsonl` | 38 |
| Map 162 — Casula ruin puzzle, 10 eventów | `custom-dialogue-map162-followups-01.jsonl` | 38 |
| Map 267 — Judy rat trap, 10 eventów | `custom-dialogue-map267-followups-01.jsonl` | 38 |
| Map 97 — West Creek skinny, 10 eventów | `custom-dialogue-map97-followups-01.jsonl` | 37 |
| Map 106 — cave Nellie, 10 eventów | `custom-dialogue-map106-followups-01.jsonl` | 37 |
| Map 64 — Carol swimsuit, 10 eventów | `custom-dialogue-map64-followups-01.jsonl` | 36 |
| Map 147 — feast cornbread, 10 eventów | `custom-dialogue-map147-followups-01.jsonl` | 35 |
| Map 84 — TV transmitter, 10 eventów | `custom-dialogue-map84-followups-01.jsonl` | 33 |
| Map 127 — commissioner wallet, 10 eventów | `custom-dialogue-map127-followups-01.jsonl` | 33 |
| Map 65 — Hannah baloney pony, 10 eventów | `custom-dialogue-map65-followups-01.jsonl` | 32 |
| Map 166 — security room Buddy, 10 eventów | `custom-dialogue-map166-followups-01.jsonl` | 32 |
| Map 107 — Ella spy, 10 eventów | `custom-dialogue-map107-followups-01.jsonl` | 31 |
| Map 134 — cat locked, 10 eventów | `custom-dialogue-map134-followups-01.jsonl` | 30 |
| Map 69 — baby goat Gatorzilla, 10 eventów | `custom-dialogue-map69-followups-01.jsonl` | 28 |
| Map 95 — Nellie shower, 10 eventów | `custom-dialogue-map95-followups-01.jsonl` | 26 |
| Map 246 — church porn, 10 eventów | `custom-dialogue-map246-followups-01.jsonl` | 26 |
| Map 45 — locker phone, 10 eventów | `custom-dialogue-map45-followups-01.jsonl` | 24 |
| Map 122 — church surrounded, 10 eventów | `custom-dialogue-map122-followups-01.jsonl` | 24 |
| Map 10 — Tasha friends path, 10 eventów | `custom-dialogue-map10-followups-01.jsonl` | 23 |
| Map 168 — Andrea house noise, 10 eventów | `custom-dialogue-map168-followups-01.jsonl` | 23 |
| Map 179 — temple bells, 10 eventów | `custom-dialogue-map179-followups-01.jsonl` | 23 |
| Map 129 — Andrea hot tub, 10 eventów | `custom-dialogue-map129-followups-01.jsonl` | 22 |
| Map 150 — Tasha rescue, 10 eventów | `custom-dialogue-map150-followups-01.jsonl` | 21 |
| Map 185 — mansion Daemalius, 10 eventów | `custom-dialogue-map185-followups-01.jsonl` | 20 |
| Map 230 — shooting range bet, 10 eventów | `custom-dialogue-map230-followups-01.jsonl` | 20 |
| Map 14 — sunburn aloe, 10 eventów | `custom-dialogue-map14-followups-01.jsonl` | 19 |
| Map 103 — Guild bunker, 10 eventów | `custom-dialogue-map103-followups-01.jsonl` | 18 |
| Map 142 — backstabber, 10 eventów | `custom-dialogue-map142-followups-01.jsonl` | 17 |
| Map 252 — attacked boxes, 10 eventów | `custom-dialogue-map252-followups-01.jsonl` | 17 |
| Map 126 — rift Mother, 10 eventów | `custom-dialogue-map126-followups-01.jsonl` | 16 |
| Map 130 — hot tub, 10 eventów | `custom-dialogue-map130-followups-01.jsonl` | 16 |
| Map 277 — relic trap Lillian, 10 eventów | `custom-dialogue-map277-followups-01.jsonl` | 16 |
| Map 139 — swim cave, 10 eventów | `custom-dialogue-map139-followups-01.jsonl` | 15 |
| Map 143 — TV studio, 10 eventów | `custom-dialogue-map143-followups-01.jsonl` | 15 |
| Map 67 — escape route, 10 eventów | `custom-dialogue-map67-followups-01.jsonl` | 14 |
| Map 172 — bunker walls, 10 eventów | `custom-dialogue-map172-followups-01.jsonl` | 14 |
| Map 275 — raccoon cat, 10 eventów | `custom-dialogue-map275-followups-01.jsonl` | 14 |
| Map 276 — Lillian goodbye, 10 eventów | `custom-dialogue-map276-followups-01.jsonl` | 14 |
| Map 131 — safe katana, 10 eventów | `custom-dialogue-map131-followups-01.jsonl` | 13 |
| Map 135 — bunker button, 10 eventów | `custom-dialogue-map135-followups-01.jsonl` | 12 |
| Map 146 — mansion jealous, 10 eventów | `custom-dialogue-map146-followups-01.jsonl` | 11 |
| Map 136 — chapel trap, 10 eventów | `custom-dialogue-map136-followups-01.jsonl` | 10 |
| Map 174 — Judy rift, 10 eventów | `custom-dialogue-map174-followups-01.jsonl` | 10 |
| Map 215 — rapids stones, 10 eventów | `custom-dialogue-map215-followups-01.jsonl` | 10 |
| Map 24 — Heather farm dinner, 10 eventów | `custom-dialogue-map24-followups-05.jsonl` | 111 |
| Map 66 — statue throw, 10 eventów | `custom-dialogue-map66-followups-01.jsonl` | 9 |
| Map 186 — toilet hair, 10 eventów | `custom-dialogue-map186-followups-01.jsonl` | 9 |
| Map 282 — laptop gone, 10 eventów | `custom-dialogue-map282-followups-01.jsonl` | 9 |
| Map 29 — suit shopping, 10 eventów | `custom-dialogue-map29-followups-01.jsonl` | 8 |
| Map 113 — wrench valve, 10 eventów | `custom-dialogue-map113-followups-01.jsonl` | 8 |
| Map 68 — cave Lillian, 10 eventów | `custom-dialogue-map68-followups-01.jsonl` | 7 |
| Map 155 — rift objects, 10 eventów | `custom-dialogue-map155-followups-01.jsonl` | 7 |
| Map 167 — Heather forty, 10 eventów | `custom-dialogue-map167-followups-01.jsonl` | 7 |
| Map 181 — dead end Tesla, 10 eventów | `custom-dialogue-map181-followups-01.jsonl` | 7 |
| Map 274 — mint cat, 10 eventów | `custom-dialogue-map274-followups-01.jsonl` | 7 |
| Map 154 — beaver dam, 10 eventów | `custom-dialogue-map154-followups-01.jsonl` | 6 |
| Map 169 — kitchen siphon, 10 eventów | `custom-dialogue-map169-followups-01.jsonl` | 6 |
| Map 176 — lunch glue, 10 eventów | `custom-dialogue-map176-followups-01.jsonl` | 5 |
| Map 117 — gas barrel puzzle, 10 eventów | `custom-dialogue-map117-followups-01.jsonl` | 4 |
| Map 156 — too heavy, 10 eventów | `custom-dialogue-map156-followups-01.jsonl` | 4 |
| Map 165 — homeless clothes, 10 eventów | `custom-dialogue-map165-followups-01.jsonl` | 4 |
| Map 170 — keypad prints, 10 eventów | `custom-dialogue-map170-followups-01.jsonl` | 4 |
| Map 133 — Erica mess, 10 eventów | `custom-dialogue-map133-followups-01.jsonl` | 3 |
| Map 152 — spiders, 10 eventów | `custom-dialogue-map152-followups-01.jsonl` | 3 |
| Map 182 — generator pulley, 10 eventów | `custom-dialogue-map182-followups-01.jsonl` | 3 |
| Map 199 — Judy early, 10 eventów | `custom-dialogue-map199-followups-01.jsonl` | 3 |
| Map 205 — Henry father, 10 eventów | `custom-dialogue-map205-followups-01.jsonl` | 3 |
| Map 74 — offering plate, 10 eventów | `custom-dialogue-map74-followups-01.jsonl` | 2 |
| Map 118 — tree item, 10 eventów | `custom-dialogue-map118-followups-01.jsonl` | 2 |
| Map 148 — secret passage, 10 eventów | `custom-dialogue-map148-followups-01.jsonl` | 2 |
| Map 180 — we're in, 10 eventów | `custom-dialogue-map180-followups-01.jsonl` | 2 |
| Map 193 — amulet coin, 10 eventów | `custom-dialogue-map193-followups-01.jsonl` | 2 |
| Map 214 — get bearings, 10 eventów | `custom-dialogue-map214-followups-01.jsonl` | 2 |
| Map 216 — cave, 10 eventów | `custom-dialogue-map216-followups-01.jsonl` | 2 |
| Map 218 — dark, 10 eventów | `custom-dialogue-map218-followups-01.jsonl` | 2 |
| Map 258 — view judge, 10 eventów | `custom-dialogue-map258-followups-01.jsonl` | 2 |
| Map 39 — church time, 10 eventów | `custom-dialogue-map39-followups-01.jsonl` | 1 |
| Map 112 — shelf item, 10 eventów | `custom-dialogue-map112-followups-01.jsonl` | 1 |
| Map 123 — Dick's talk, 10 eventów | `custom-dialogue-map123-followups-01.jsonl` | 1 |
| Map 161 — where from, 10 eventów | `custom-dialogue-map161-followups-01.jsonl` | 1 |
| Map 164 — Andrea collection, 10 eventów | `custom-dialogue-map164-followups-01.jsonl` | 1 |
| Map 188 — outside sound, 10 eventów | `custom-dialogue-map188-followups-01.jsonl` | 1 |
| **Suma nowych partii** | **149 plików** | **6 660** |

Nowe 6 660 ID (885 + 123 + 236 + 349 + 106 + 102 + 202 + 397 + 95 + 95 + 270 + 338 + 83 + 245 + 158 + 152 + 222 + 202 + 253 + 169 + 197 + 184 + 174 + 161 + 151 + 174 + 153 + 146 + 125 + 100 + 86 + 66 + 111 + 50 + 28 + 29 + 43) przeszły audyt zgodności z kanonicznym eksportem, kompletności, tokenów i braku overlapu; buildery odmawiają nadpisania i przechodzą `py_compile`. Późniejszy pełny audyt skorygował projekcję tych partii do 39 820 niepustych tłumaczeń po ID. Tłumaczenia Map 202/55/121/57/104/108/81/85/24/115/17/35/79/5/56/100/63/83/98/128/158/183/42/70/18/53/120/73/137/257/59/102/43/48/77/47/124/72/240/140/116/153/190/245/109/86/99/204/159/22/217/119/145/105/291/206/7/149/160/132/58/162/267/97/106/64/147/84/127/65/166/107/134/69/95/246/45/122/10/168/179/129/150/185/230/14/103/142/252/126/130/277/139/143/67/172/275/276/131/135/146/136/174/215/24/66/186/282/29/113/68/155/167/181/274/154/169/176/117/156/165/170/133/152/182/199/205/74/118/148/180/193/214/216/218/258/39/112/123/161/164/188 wykonane w pełni LLM-owo w kontekście, z korektą tonu i terminologii, bez automatów.

Wcześniejsze wersje partii pozostają dla historii, ale nie należy ich scalać razem z nowszymi zamiennikami: używaj `inventory-names-02`, `native-messages-03` i `phone-contact-ui-02`, nie ich wcześniejszych wariantów. Batch `map-labels-01.jsonl` został już uwzględniony w `inventory-names-02.jsonl`. Sceny obejmują 13 wcześniejszych i 7 kolejnych plików; aktualny zestaw zawiera Common Event 25, 15 scen Common Events ze step10 oraz 50 follow-upów Common Events ze step11 (2 730 wierszy), a także dialog Map 20/31, eventy Map 3 (22, 31, 37, 39, 41, 45, 47, 56; sensowny dialog Map 3 jest pokryty) i follow-upy Map 23/24/9/116, pierwsze partie Map 41/55/44/82/54/6/26 i 57 Common Events oraz 21 nowszych partii map wyszczególnionych powyżej. Wszystkie partie pozostają do redakcji; znaczniki komend/statusów nie są tłumaczone na ślepo.

## Walidacja i zasady

Scalaj po ID, nie po treści, np. przez `python3 games/the-genesis-order/tools/merge_translation_batches.py` z aktualnymi partiami. Walidator sprawdza zgodność wszystkich pól źródłowych z eksportem, ID, tokeny, chronione wartości i konflikty; nie nadpisuje istniejącego wyniku. Nie zmieniaj ID, locatorów, hashy źródłowych, `source_text` ani struktury. Zachowuj wszystkie `keep_source_value` dokładnie.

Partie są wersją roboczą do redakcji. Potrzebne są kontrole kontekstu, terminologii, długości UI, polskich glifów i zachowania w grze. Żadna gra ani kod gry nie były uruchamiane; nie wykonano testu Windows/runtime. Nie modyfikuj `export-v1/` ani source ZIP v1.
