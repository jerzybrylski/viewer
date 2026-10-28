# Statyczny census tekstu — The Genesis Order

**Stan:** pełny census eventowych dialogów i wyborów z dostarczonego `www/data/`.  
**Data:** 2026-10-28  
**Zakres kopii:** ZIP przesłany przez użytkownika z całym `www/data/`: 305 poprawnych JSON-ów oraz `Credits.txt`. Archiwum zawiera `Map001.json`–`Map291.json`, `MapInfos.json`, `CommonEvents.json` i bazy danych; brak mediów. `System.json` podaje `versionId=96719260` — wewnętrzny identyfikator projektu, nie potwierdzony numer wydania/builda. Pochodzenie i dokładny produktowy build pozostają nieustalone.

## Wynik dialogu i wyborów

| Kategoria | Wystąpienia w źródle | Różne surowe teksty | Uwagi |
|---|---:|---:|---|
| Wiersze dialogu (`401`) | **1 521** | **766** | Wszystkie zachowane strony, eventy i warunki map oraz `CommonEvents`; wiersze puste wyłączono. |
| Grupy wyborów (`102`) | **695** | — | Standardowe RPG Maker MV choice blocks. |
| Teksty opcji | **2 110** | **376** | Wszystkie opcje z każdej grupy; wszystkie policzone opcje są niepuste. |

**Podział źródła:**

| Źródło | Mapy (`Map001`–`Map291`) | `CommonEvents.json` | Razem |
|---|---:|---:|---:|
| Wiersze dialogu | 910 | 611 | **1 521** |
| Różne surowe wiersze dialogu | 303 | 489 | **766** po deduplikacji między źródłami |
| Grupy wyborów | 493 | 202 | **695** |
| Teksty opcji | 1 294 | 816 | **2 110** |
| Różne surowe teksty opcji | 272 | 122 | **376** po deduplikacji między źródłami |
| Polecenia eventowe | 331 349 | 139 144 | **470 493** |

Map-level distribution: z 291 map **84** zawierają co najmniej jeden wiersz dialogu, **37** zawiera co najmniej jedną grupę wyborów, a **99** ma dialog, wybór lub oba.

RPG Maker ma ponadto 1 140 bloków `Show Text` (`101`) i 1 656 komend wierszy `401`; 135 komend `401` ma pustą zawartość i nie weszło do liczby dialogów. Nie znaleziono bloków przewijanego tekstu (`105`/`405`). W `Troops.json` występuje jedna dodatkowa komenda na liście eventowej, bez dialogu ani wyboru. Łącznie listy eventowe map, common events i troop events zawierają 470 494 komendy; liczba ta nie jest liczbą tekstów.

## Dodatkowe tekstowe pola danych — poza dialogiem

Poniższe wartości policzono osobno, aby nie mieszać tekstów baz danych/UI z wierszami dialogu. Nie są dodawane do sumy powyżej.

| Źródło / pole | Wystąpienia | Różne wartości | Interpretacja |
|---|---:|---:|---|
| `System.json`: terms, tytuł/waluta i nazwy elementów/typów ekwipunku | 131 | 117 | Teksty systemowe/UI i słowniki systemowe; nie obejmują całego tekstu pluginów. |
| `Actors.json`: nazwy aktorów | 28 | 17 | Pola `name`; nazwy assetów portretów/postać wyłączone. |
| `Items.json`: nazwy przedmiotów | 477 | 391 | Pola `name`; 481 formuł i 34 pól `note` pozostawiono poza dialogiem. |
| `MapInfos.json`: nazwy map | 291 | 270 | Etykiety danych/edytora, nie sceny dialogowe. |
| `Credits.txt` | 239 niepustych linii | 239 | Napisy końcowe, osobne od dialogu. |

Nazwy animacji, tilesetów, eventów i common events, pliki assetów oraz pozostałe wewnętrzne identyfikatory nie zostały wliczone jako tekst dla gracza.

## Metoda i pokrycie rozgałęzień

- Bezpiecznie sprawdzono CRC i ścieżki ZIP; rozpakowano wyłącznie JSON/TXT do ignorowanego katalogu `google_drive/the-genesis-order/data/`. Nie uruchamiano gry ani kodu z gry.
- Zweryfikowano 305/305 plików JSON. Mapy mają kompletne, ciągłe ID 001–291, a `MapInfos.json` zawiera 291 wpisów. `CommonEvents.json` zawiera 500 zdarzeń.
- Statycznie zliczono komendy `401` oraz teksty tablic wyborów z `102` w listach komend każdej strony mapy, każdego eventu i każdego common eventu. Wszystkie zapisane strony/warunki i odnogi menu zostały uwzględnione; warunków nie ewaluowano, a pliki nie były uruchamiane.
- Liczba wystąpień nie jest liczbą ścieżek rozgrywki. Ten sam napis zapisany wielokrotnie w różnych eventach liczy się wielokrotnie. „Różne teksty” oznaczają identyczność surowych wartości JSON, bez normalizacji escape codes, zmiennych i formatowania.
- Dla dalszego przygotowania Czytanek zapisano osobne liczniki, bez treści dialogów: [`COUNT_BY_MAP.csv`](COUNT_BY_MAP.csv) (291 wierszy) oraz [`COUNT_BY_COMMON_EVENT.csv`](COUNT_BY_COMMON_EVENT.csv) (500 wierszy). Zawierają ID i metryki gałęziowe, nie tekst gry.

## Wyłączenia i ograniczenia

- Teksty skryptowe/pluginowe mogą zawierać dynamicznie budowane wiadomości. W mapach i common events znajduje się **72 623** komend skryptowych `355`/`655` oraz **1 570** komend pluginowych `356`; nie wliczono ich do dialogu ani nie interpretowano. Wymagają osobnego, statycznego przeglądu, jeśli celem będzie pełne pokrycie wszystkich możliwych stringów.
- UI poza wybranymi polami `System.json`, teksty pluginów z `www/js`, wiadomości tworzone w runtime oraz teksty zaszyte w assetach nie wchodzą do sumy dialogowej. Pełny zakres lokalizacji jest więc szerszy niż podany census dialogów/wyborów.
- Nie badano renderowania polskich znaków, fallbacku fontów, łamania wierszy ani długości okien w runtime. Nie zbudowano patcha i nie rozpoczęto tłumaczenia.
- Właściciel nie wskazał jeszcze tytułu do rozpoczęcia tłumaczenia.

## Źródło i powtarzalność

- Oryginalny upload: `data.zip`, 3 299 615 B, SHA-256 `c9deca5c733cbbc92306e41a8afa0157e38758283a9c7662960349f9b9fd5842`.
- Archiwum: 306 elementów — 305 JSON + 1 TXT; zawiera wszystkie 291 map, `CommonEvents.json`, `MapInfos.json` i pozostałe JSON-y `www/data`.
- ZIP oraz wyodrębnione dane są w ignorowanym katalogu `google_drive/`, poza Gitem.
