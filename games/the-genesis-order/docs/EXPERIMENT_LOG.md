# Dziennik eksperymentów — The Genesis Order

## 2026-10-28 — pierwszy pakiet inwentaryzacyjny

- **Cel:** zebrać lokalny spis plików i rozmiary bez założenia silnika ani ścieżki instalacji.
- **Pakiet wejściowy:** `TGO_INVENTORY_REQUEST.zip`, SHA-256 `17305fbf058383f5c9f38472ff60640916de8a684e303096a5052d078ad0478f`; Drive file ID `1Tl3Pmu8PHb5aQXpA5Ah2OKvL0qO96TBe`.
- **Zawartość pakietu:** `URUCHOM.bat`, `COLLECT_TGO.ps1`, `INSTRUKCJA.txt`.
- **Walidacja sandbox pakietu wejściowego:** ZIP poprawny (CRC), ma trzy oczekiwane pliki; statyczne kontrole potwierdziły generator raportu i brak polecenia usuwania. Nie uruchamiano go przez PowerShell w sandboxie.

## 2026-10-28 — pierwszy wynik z Windowsa

- **Raport:** `TGO_DIAGNOSTIC_20261028_191643.zip`, Drive file ID `1gwWlg0ywzYY8k0gjWDi77iTNGl70zmaL`, rozmiar 263 365 B, SHA-256 `9d4a4d129ae1af3208bd7f14fdfdeda72d211c5849e1df1a709e3b9215af2d12`.
- ZIP zawiera pięć raportów tekstowo-strukturalnych: dwa CSV, JSON, podsumowanie TXT i transcript TXT; łączny rozmiar po rozpakowaniu 3 080 183 B. Nie zawiera plików gry.
- Zweryfikowano strukturę ZIP i odczytano CSV/JSON/TXT bez uruchamiania kodu. Raport podaje 17 694 pliki, 19 169 362 931 B, `possibleTextResourceCount=17625` oraz zero ostrzeżeń skanowania.
- Struktura ścieżek i rozszerzeń (`www/js/rpg_core.js`, `www/data/Map###.json`, `.rpgmvp`, `.rpgmvo`, `nw.dll`, `node.dll`) mocno wskazuje na RPG Maker MV + NW.js; wersji i builda nie potwierdzono.
- Pole „possible text resources” obejmuje także media (.mp4/.rpgmvp/.rpgmvo), więc nie mierzy rzeczywistego zakresu tekstu.
- W `_Redist` znajduje się wpis `fitgirl.md5`, co sugeruje repack FitGirl. To sygnał do wyjaśnienia, nie samodzielny dowód statusu prawnego. Transcript raportu zawiera nazwę konta i komputera; tych danych osobowych nie kopiujemy do repo.
- **Nie** otwierano zawartości JSON/JS z instalacji, nie uruchamiano gry, nie ekstraktowano assetów, nie modyfikowano plików ani nie budowano patcha.
- Użytkownik wyjaśnił, że wpis `fitgirl.md5` to jego zdaniem pozostałość niezwiązana z projektem. Pochodzenie/sklep kopii pozostaje niepotwierdzone; próbkowy skrypt instruuje używanie wyłącznie kopii z autoryzowanym dostępem.
- **Pakiet 2:** `TGO_STAGE2_REQUEST_v1.0.0.zip`, Drive file ID `1TNI-ZixJyXj9FP7RXwOE969GqwOOcv4-`, rozmiar 3 495 B, SHA-256 `e563a3e1d5f46cbe2dfb466895b8b214c28b13f785080211b10d36d3b8ecf216`. Zawiera wyłącznie BAT, PowerShell i instrukcję (bez assetów gry).
- Skrypt etapu 2 statycznie przejrzano: jawna allowlista, bez rekursywnego kopiowania, bez wykonywania kodu z gry i bez zapisu do katalogu gry. Sandbox nie ma Windows PowerShell 5.1, więc skrypt nie był tam uruchomiony.
- Użytkownik wybrał bezpośrednie przesłanie danych tekstowych zamiast uruchamiania pakietu 2. Pakiet nadal istnieje na Drive, lecz nie jest potrzebny do bieżącej analizy.

## 2026-10-28 — bezpośredni upload danych/JS

- Folder `www` na Drive: ID `1b1TmOhXx-a8P-pqUS8g6o18HzHVe_fsb`; podfolder `data`: ID `1dY4OpAedbcLSuh2GERf9k8HTbGY4iqLn`; `js`: ID `1A0uM6qPAmTrIoTnaXBIzBn7Gvy-W9Wo8`.
- Drive zawiera 306 elementów w `www/data` (305 JSON + `Credits.txt`) oraz katalog `www/js` z kodem silnika, `plugins.js`, `plugins/` i `libs/`. Główny `package.json` ma ID `1J32h3HCPuwB3HGPWb4oM4FI72y4er1bK` (243 B). Folderów z obrazami, audio i filmami nie pobierano.
- Lokalnie pobrano wybraną próbkę; reszta danych nadal pozostaje na Drive. Poniżej ID i SHA-256 plików pobranych do statycznej analizy:

| Plik | Drive file ID | Bytes | SHA-256 |
|---|---|---:|---|
| `package.json` | `1J32h3HCPuwB3HGPWb4oM4FI72y4er1bK` | 243 | `47e91b54ea4c934dac5ecbb4a99b72c8a40ef16e677bee8ff07ae1419ab81bf` |
| `www/data/System.json` | `11NvNtv8bkMwYCEU4KZJx2cYapzrb3fAe` | 67 244 | `a2e0e6b55dd7cbaa0688feac218e2bf461cb2edd84987a86a092e157ba861732` |
| `www/data/MapInfos.json` | `1FR_FVURDGPzZaQkUBBj2xuu_-50VSg2A` | 29 895 | `becc8069b275a296e9ea9ec393435b719d36f98982fc268ccc044d19e9fbbb52` |
| `www/data/CommonEvents.json` | `1TWpjge4k6q1X5rshp_WlUt0mIJaEQ7lK` | 8 370 942 | `37321ff8693412e5e4488eb736a63b43fcbd142410008b73f5bcb317c27e3ca9` |
| `www/data/Map001.json` | `12qtfTT7QaTOQZU3UsQagYqWkBqMcZ433` | 5 994 | `ebe917a8a2b1a81be34366ef0eb71a042667e1926045bc3f34bd9c30bd81de11` |
| `www/data/Map002.json` | `1XSRqkz2KMvHEw-XcpEhD9pPQ37XHy_CH` | 73 239 | `0858ff180c910e0516ab8df19a776443517f828ee500e9028099f6274f3d9097` |
| `www/data/Map003.json` | `1ayMPasthCixecuVUFYab0ZNt8dTmoKEt` | 569 635 | `e08f416d6d2ec4d4ed67bf67439de36ffb60a831d641c54decb2a806cc9dc86c` |
| `www/data/Map038.json` | `1nFp5cWSs6e_sC0A_GanDYKufKxFyErOQ` | 6 860 | `33489ba187a0a080a6c7de0636ded7540b1e81ec898a0dc316235f195e2c0195` |
| `www/js/plugins.js` | `1fG4EGgUKXtIE3KbNfFc9uWyn_Awjxunk` | 18 042 | `4ba4294032bcd187262d91a70df64ba1905986768d2f7e1d420b5a2fe2249521` |
| `www/js/rpg_core.js` | `1ujkl12ckVUkpyLvZMrNiFDjeHbHfcY1e` | 244 685 | `9020b78d4984b61d58565fcc1d2f4d2071fd80f5fb3b83d4de633b01e4af7c5b` |
| `www/js/rpg_managers.js` | `1EuRJwBhrTeWvm3FN_fPtrl3x8BElu29t` | 84 678 | `791082a4d5768d4a661c071dac828805119952a32d33dabfb440c2d18f0bbed7` |
| `www/js/plugins/Choices.js` | `17QjkMf1XtyP8HY9cTk36wbBrp1q3pEKA` | 1 862 | `e62d24fbedcaec26d558d9154834c59be87fd9fffed6d7e1cff08f4e4e160985` |
| `www/js/plugins/Eli_FontManager.js` | `1OU1QxkxHYdKoWJh9K-wbOkHeYuffrxse` | 15 804 | `776773de5a4fd851fed3aa2f0e9047c6d50c558ce4673f386862923232aa6d99` |
| `www/js/plugins/RS_MessageAlign.js` | `1UDFrqW3xBELlk7fOsvwzm8l3OyxQLXV5` | 14 614 | `12bb247ca2ae4acb01203277aa836f5b697c1b3c57830a60fd9b33c22d074a23` |
| `www/js/plugins/TSR_TextColorAddOn.js` | `1DixovspJYu9ULTHc_BDJd_fK91ttCnmD` | 32 600 | `afb3dea3de09cfadd9d0862e6cc99ac76cd3260206c8051bdeab5b68a70e5aa5` |
| `www/js/plugins/YEP_CoreEngine.js` | `1qPU11DY-ymw_yQ1z2Tq14luJb5s0JiUt` | 95 463 | `6cc5ca5d9213f4f471a09a12cde51310e395688260d687df398f0e54ba98ef32` |
| `www/js/plugins/YEP_LoadCustomFonts.js` | `1zK7fAsd14Kc4oaotYHOh61fAyvjPrKOW` | 4 249 | `c41839917bcdcbce8f41394d4c214cbdd5e2879ee6418cb65fc5e362f0eb1bb9` |
| `www/js/plugins/YEP_MessageCore.js` | `16FQvfsda_MJtl-iLHV_TbZvszHjMQEif` | 50 284 | `4003fc9300924845ef968c4e39a48c228879fc730b50821094f81d1ce620db36` |
| `www/js/plugins/YEP_X_MessageSpeedOpt.js` | `1PoEFRlhK0j3GTmSzoXgePjeSW3Osa8BP` | 11 807 | `91871e6308621b90d852dea3765b854494e7c8fd41464f256e5e5ab45c7f5cac` |

- Statyczne parsowanie potwierdziło 56 plugin entries / 53 enabled, silnik MV 1.6.1, 291 map, mapę startową 38 i 500 Common Events. Zliczenia pól tekstowych i ograniczenia próbek są w `TECHNICAL_FINDINGS.md`; nie wypisywano zawartości dialogów do repo.
- Nie uruchamiano JS, gry ani runtime; JSON parsowano statycznie. Nie skopiowano żadnego assetu do Git.

## 2026-10-28 — fonty i pytanie o zakres przed tłumaczeniem

- Użytkownik przesłał folder `www/fonts/`, Drive folder ID `1PL1rfnA0p6RNgJdJ_kT_zY06Lz3KPS5H`. Zawiera 11 fontów `.ttf`/`.otf` oraz `gamefont.css` (łącznie 12 plików).
- Pobrano wszystkie; identyfikatory Drive, rozmiary i hashe:

| Plik | Drive file ID | Bytes | SHA-256 |
|---|---|---:|---|
| `Akong_agi.ttf` | `1OmtKhPfZgLCCu4spjwh-TwHSFhVi7vhF` | 56 552 | `c6c67bd26b3f556947dbbce6fb6c5aacb8db98f5c65e1b9373e6a9a1691fb877` |
| `Chapbook-Regular.otf` | `1AO_V6SEskOTSng-ShBl88k4UZXACkaV7` | 172 628 | `c1a8b72c565d9ce04eeac6c5b4a18d4006052ad9a0aa84f70c9fe6165e6e7e25` |
| `Cinzel-Black.ttf` | `19cVu_2Bm7QoU4714nfLZQXdJH5Wpcg9t` | 58 616 | `2cce1b54893150f460214b19644f4be9c4eafb32fc221f1a14b856dc1f99e52b` |
| `Cinzel-Regular.ttf` | `16ywK5y9P8kw-9GmJQcb9YENfZWKZ52IZ` | 56 228 | `a73369ecaad30447f72e12d4c80f98dee5aa0e029b841d5a04a28ccd131cb0c4` |
| `gamefont.css` | `19N3d7d8TMIV4jcv4WTRgq5xr6ECYRWR6` | 254 | `b2d96e6d941ad1be97aca81aae9a5427ce8fc17770498ed0a45b40203e9b097a` |
| `JosefinSans-Regular.ttf` | `1aLZEAnTVSw8goZdbk693u0GxT2dnt_Ee` | 33 008 | `e07aa47f7e6dd461342c147d280f094b9f62a0adb52555fb3ec0e899afcf0a06` |
| `JosefinSans-SemiBold.ttf` | `1FANmh8xwp4q6xey_d27vhEBqSdXlDqAB` | 33 004 | `bce2ed51da316e20fc108befa1ba152850eca29cfc2b26f278a8d74957a677fb` |
| `mplus-1m-regular.ttf` | `1wK7ci2KL7DQjkXlPZvW7ABXGEzqZBTI3` | 1 541 768 | `7f2096495dab49c7150cd0609f2f8d6b03ebf2fa7561ea34b3cca1e09eb0bae5` |
| `SpecialElite.ttf` | `1Jd5jCmVa9SBVAZPM6Wo0EHEzing3wHjz` | 166 224 | `9ebacf4e85df65a89db88a3ec38576969490f418890fc6478fb00c2fcbdb4f4c` |
| `texgyreadventor-regular.otf` | `1fbSDpmenUpGxALifLP85H0FgTX1vPBVj` | 124 680 | `f146708de32a3ee8ec1b627004a08f31dd137cc6bc6459ef0ecfc51fef170819` |
| `UglyTypist.ttf` | `1gvWhvOGyXmIlJ-J1zMcstxhOVgJ46OG9` | 79 272 | `12c8cc0dbe28a947c527c44cb59d0a36b7890011a392be7489b3ae484342a94a` |
| `underworld.ttf` | `1eMpmbOE-fWIv2rN5CW5zXnbjbIhC6sMs` | 212 196 | `8a546cf7ce429b35292c843908f0dcc98a46d10cf436d2bed01966df048b4be1` |

- FontTools 4.68.0 cmap dla 18 polskich liter: 7/11 fontów mają pełne pokrycie, 3/11 tylko `óÓ`, a UglyTypist 0/18. `gamefont.css` przypisuje domyślny `GameFont` do JosefinSans-SemiBold (2/18); brak runtime testu fallbacku.
- Użytkownik pyta o wiarygodny przedtłumaczeniowy licznik dialogów/wyborów oraz Czytanki dla obu tytułów. Potwierdzono, że to wykonalne jako osobny etap. Obecne liczniki są częściowe; pełna wycena wymaga przetworzenia wszystkich zasobów tekstowych obu wersji.
- Czytanka powinna zachować scenę/label/mapę, mówiącego, wybory i warunki. Ponieważ obie gry mają rozgałęzienia i teksty dynamiczne, kompletna Czytanka będzie branch-aware, a nie jedną liniową „kanoniczną” trasą.
- **Następny krok:** pełny, walidowany census obu korpusów (dialogi, continuations, opcje, UI/bazy danych i teksty skryptowe osobno), a potem próbny fragment Czytanki do akceptacji formatu. Tłumaczenia jeszcze nie rozpoczęto.

## 2026-10-28 — lista map i ograniczenie eksportu przed pełnym pakietem

- Paginowana lista plików Drive potwierdza mapy `Map001.json`–`Map291.json`. Lokalnie dostępne tekstowe próbki nadal obejmują tylko `Map001`–`Map003`, `Map038` oraz `CommonEvents.json`; pełny zbiór map nie został pobrany ani policzony.
- Połączenie Drive w tej sesji pozwala odczytywać/ściągać pojedyncze pliki, ale nie eksportuje folderu z setkami JSON-ów bezpośrednio do lokalnego parsera. Nie zastępowałem brakujących danych estymacją ani liczeniem samych rozmiarów.
- Żeby dokończyć uzgodniony bezpośredni upload bez mediów i bez uruchamiania BAT/PS1, potrzebny jest jeden ZIP wyłącznie z `Map001.json`–`Map291.json` i `CommonEvents.json` (opcjonalnie `MapInfos.json`). Do tego czasu liczba 611 wierszy dialogu i 816 opcji dotyczy wyłącznie `CommonEvents.json` i nie jest pełnym wynikiem TGO.

## 2026-10-28 — pełny pakiet `www/data/` i census dialogów/wyborów

- Użytkownik przesłał `data.zip` (Drive file ID `1jvwrMJKqQDq28q2EVLb_B4jO7w6po_Sw`), 3 299 615 B, SHA-256 `c9deca5c733cbbc92306e41a8afa0157e38758283a9c7662960349f9b9fd5842`. Archiwum ma 306 elementów: 305 JSON + `Credits.txt`; CRC poprawny, brak niebezpiecznych ścieżek.
- Zweryfikowano poprawność wszystkich 305 JSON-ów, komplet `Map001`–`Map291` i 500 common events. Wszystkie pliki JSON pozostały w ignorowanym `google_drive/`; nic nie dodano do Git poza licznikami i dokumentacją bez tekstów gry.
- Pierwszy licznik event commands `401`/`102` ze wszystkich map i common events: 1 521 niepustych wierszy `401` (766 różnych surowych tekstów), 695 grup wyboru i 2 110 tekstowych opcji (376 różnych). Wówczas wiersze `401` błędnie opisano jako pełny dialog; audyt z tego samego dnia wykazał customowy kanał CE60, opisany w sekcji korekty poniżej.
- Zebrano także osobne pola systemowe/bazodanowe oraz metryki per mapa i common event; skryptowe/plugin commands pozostawiono poza dialogiem, jako potencjalnie dynamiczny zakres do oddzielnej inspekcji.
- Wygenerowano `docs/COUNT_REPORT.md`, `docs/COUNT_BY_MAP.csv` i `docs/COUNT_BY_COMMON_EVENT.csv`. Nie uruchamiano gry, nie uruchamiano żadnego kodu z danych ani nie rozpoczęto tłumaczenia.

## 2026-10-28 — korekta: customowy kanał dialogu i UI

- Użytkownik słusznie zakwestionował 1 521 jako pełny dialog. Analiza statyczna wykazała, że Common Event 60 `MESSAGE` pobiera tekst ze skryptowej `V[21]` po pierwszej kropce, zapisuje treść do `V[25]` i wyświetla ją przez `401`. Zachowując zapisane gałęzie, wykryto **38 638** wpisów i **29 647** różnych payloadów (27 602 wpisy na mapach, 11 036 w common events).
- Śledzenie najbliższego wywołania Common Eventu przed nadpisaniem zmiennej rozdzieliło 39 355 literałów `V[21]`: 38 638 do CE60, 705 do CE222 (`SHOW ARIANNA HINT`), a 12 wyłączono jako niepotwierdzone wiadomości (10 nadpisanych przed wywołaniem, po jednym skierowanym do CE61 i CE53). Nie wszystkie skryptowe stringi uznano za dialog.
- Osobno potwierdzono 17 literalnych tekstów telefonu przez CE53 (10 różnych), 649 etykiet UI znalezionych przedmiotów przez CE223 (334 różne) oraz 67 wywołań CE224. Dalszy statyczny trace wykazał, że CE224 preładuje bitmapy przez `Galv.CACHE.load`; nie jest to tekstowy payload. Dwa natywne wiersze CE224 zachowano jako `needs_review`. Natywne liczniki `401`/`102` pozostały oddzielone.
- Natywne 1 521 wierszy `401` zawierają 6 potwierdzonych rendererów/szablonów dla CE53/60/222/223; dwa wiersze CE224 zachowano jako `needs_review`. Z pozostałych 1 515 wierszy 378 należy do jawnej listy UI telefonu CE17, 13 do natywnego kanału telefonu CE54, a pozostałe 1 124 nadal nie są wszystkie sklasyfikowane. Wybory liczą 695 bloków / 2 110 opcji; w sześciu nazwanych menu/UI wspólnych zdarzeń potwierdzono podzbiór 44 bloków / 180 opcji.
- Dodano `tools/count_custom_text.py` i kolumny per mapa/common event; skrypt parsuje wyłącznie dane statycznie, nie wypisuje treści i nie uruchamia gry ani jej kodu. Zaktualizowano raporty oraz skorygowano wcześniejsze sformułowania o „pełnym censusie”.

## 2026-10-28 — rozstrzygnięcie kolejki JS (lokalne 5 plików)

- Zreprodukowano statyczny skan aktualnie dostępnych 5 plików JS: 327 kandydatur (216 literalnych kandydatur przy API wyświetlania, 111 parametrów pluginów). Każdy ID otrzymał jawny, content-free wynik: 27 potwierdzonych powierzchni UI, 300 technicznych/konfiguracyjnych/markupowych/sterujących pozycji poza zakresem przekładu w tym locatorze, 0 nieocenionych i 0 odroczonych. Decyzje nie zawierają źródłowych tekstów.
- Promocje potwierdzono statycznym przepływem do widocznych etykiet menu/opcji/ekranu tytułowego i rendererów UI; dodatkowe źródła pluginów sprawdzono tylko do odczytu. Wśród wykluczeń oddzielono klucze sterujące, asset/path/font/ustawienia, identyfikatory grup, placeholdery formatowania, markup, ASCII-keyboard i enumy logiki. Dynamiczny wynik API typu połączenia pozostaje osobną luką runtime, nie bezpiecznym literalnym celem.
- Wcześniejszy inwentarz 78 plików miał 554 kandydatury; po rozstrzygnięciu obecnego podzbioru pozostaje **227** z plików nieobecnych w bieżącej lokalnej kopii. Nie uznaje się pełnego pokrycia JS ani gotowości translator ZIP.
- Rozszerzono kurator i manifest o wyniki `confirmed / excluded / deferred / unreviewed`, kontrolę hashy wszystkich kandydatów oraz test syntetyczny. Zaktualizowano prywatny eksport do 44 827 rekordów i szkic Markdown do 495 dokumentów / 44 827 rekordów; pełny `--check` bez zapisu, testy `unittest` 20/20.


## 2026-10-29 — odtworzenie i rozstrzygnięcie pełnego skanu JS

- Przywrócono do ignorowanego `google_drive/the-genesis-order/www/js/` pełną hierarchię z Drive: 78 plików (8 root, 63 pluginy, 7 bibliotek). Hashy kandydatów w nowym skanie zweryfikowano z przywróconymi źródłami; JS nie był uruchamiany.
- Statyczny skan odtworzył dokładnie 554 kandydatury. Dodatkowe 227 zostały ocenione, a curation połączono z wcześniejszym podzbiorem: **554 total; 30 confirmed UI; 524 excluded; 0 deferred; 0 unreviewed**. UI: 4 `ui.engine_static`, 17 `ui.plugin_static`, 9 `ui.plugin_parameter`.
- Dwie nowe etykiety (`Error`/`UnknownError`) w silniku i jeden `UnknownError` w aktywnym YEP_CoreEngine są przekazywane do `Graphics.printError`, więc potwierdzono je jako widoczne UI ekranu błędu, nie dialog fabularny. Pozostałe nowe wartości to klucze TextManager/komend, alignments/formaty, kody markup, kontrolki pluginów, źródła nieaktywne lub niezaładowane oraz diagnostyka błędnego użycia statycznej klasy.
- Znaczenie poprzednich 300 wykluczeń: nie były to 300 wiadomości. Były to kandydatury kodu/ustawień/identyfikatorów/formatów bez dowodu widocznego UI w konkretnym locatorze; nie należy opisywać ich jako „300 technicznych wiadomości”.
- Prywatny eksport v1 odświeżono do **44 830 rekordów** (44 800 data + 30 JS UI); szkic Markdown ma **497 dokumentów / 44 830 rekordów**. `apply_translation.py --check` i pełny zestaw testów pozostają bramką końcową; ZIP nadal wstrzymany do audytu pozostałych dynamicznych i skryptowych powierzchni.

## 2026-10-29 — domknięcie statycznych powierzchni i aktualizacja kanonicznego eksportu

- Rozszerzono eksporter o statyczne wyrażenia stringowe z komendy 122, jeśli ich zmienne są jawnie użyte przez `\\V[...]` w komendzie widocznej wiadomości, tekstu przewijanego lub wyboru. Wykryto 394 literalne przypisania; 262 niepuste wartości weszły do kategorii `ui.variable_value`, a 132 whitespace-only wartości są placeholderami layoutu i zostały pominięte. 61 cen oraz 67 markerów otrzymało `keep_source_value`; brak nieliteralnych wyrażeń w dopasowanym zbiorze.
- Statyczny audit JS zakończono na 78 plikach / 563 kandydaturach: 35 UI (`ui.engine_static` 4, `ui.plugin_parameter` 9, `ui.plugin_static` 22), 528 wykluczeń z jawnym content-free powodem, 0 odroczonych i 0 nierozstrzygniętych. Źródłowe JS pozostały poza Gitem i żaden kod gry nie był wykonywany.
- Audyt listy 1 570 plugin commands: AnimationCurve 1 321, MessageWidth 156, MessageRows 42, Play2ndBGS 17, Fadeout2ndBGS 4, steamworks 30 — kontrola/parametry/asset/API, nie bezpośrednie statyczne UI stringi. 34 pola Items.note sprawdzono statycznie; zawierają wyłącznie tagi/metadane, bez prozy.
- Zaktualizowano bezpieczny write-back `event_script_expression`: tylko statyczny literał JS w operandzie komendy 122 może być zmieniony w staging copy. Hash/locator/source value są ponownie weryfikowane; dynamiczny expression nie jest eksportowany. Test syntetyczny potwierdza zmianę kopii i niezmienność wejścia.
- `export_translation.py` odtworzył kanoniczny, śledzony bundle w `games/the-genesis-order/translation/export-v1/`: **45 229 rekordów, 25 JSONL + manifest**, wszystkie coverage checks true, stabilne ID unikalne. Składniki kontroli obejmują 262 wartości zmiennych, 35 statycznych UI JS, 2 110 opcji, 1 122 ogólne wiersze 401, 8 rendererów pominiętych.
- `apply_translation.py --check`: 45 229 rekordów, 0 tłumaczeń, 238 source files zweryfikowanych, 0 plików zmienionych; `markdown_translation.py build --replace`: 497 dokumentów / 45 229 rekordów / 238 źródeł w ignorowanym google_drive. Markdown import `--check`: 45 229 kanonicznych rekordów, 0 tłumaczeń, 0 braków.
- Pełny zestaw `python3 -m unittest discover -s games/the-genesis-order/tests -v`: **27/27 passed**, w tym kontrola importu Markdown dla chronionych wartości; `git diff --check` bez błędów. Oryginalne assety pozostają poza Gitem; dokumentacja, narzędzia, decyzje kuratorskie oraz wyodrębnione JSONL są przeznaczone do śledzenia w repo zgodnie z najnowszą decyzją właściciela.
- Nie przygotowano ZIP-a, nie uruchamiano gry i nie rozpoczęto tłumaczenia.

## 2026-10-29 — źródłowy pakiet tłumaczeniowy v1

- Na prośbę właściciela przygotowano statyczny source ZIP v1. W późniejszej, wiążącej decyzji właściciel zatwierdził wszystkie 1 122 nie-rendererowe wiersze `401` i 1 930 opcji jako pełnoprawny tekst do tłumaczenia; obecny eksport i paczka używają neutralnych kategorii `native_message` oraz `choice_option`.
- Dodano `tools/build_translation_package.py`. Skrypt wymaga `coverage_checks_passed=true`, zgodności liczby rekordów między JSONL i Markdown, unikalnych ID, bezpiecznych ścieżek, zapisuje ZIP tylko pod `google_drive/`, sprawdza CRC ZIP-a i generuje sidecar SHA-256. Do archiwum trafiają wyłącznie eksport JSONL, Markdown, README/manifest pakietu oraz dokumenty tekstowe; bez assetów i kodu gry.
- Walidacja po dodaniu skryptu: `py_compile` OK; pełne `unittest` **27/27 passed**; Markdown import-check **45 229 rekordów / 0 braków**; builder zweryfikował `coverage_checks_passed=true`, **45 229 rekordów, 497 dokumentów, 131 chronionych wartości, 531 wpisów ZIP**. Końcowy SHA-256 i rozmiar zapisuje builder w `TGO_source_translation_package_v1.zip.sha256`.
- Ponowione `apply_translation.py --check` nie mogło wystartować, bo bieżące środowisko nie zawiera ignorowanego `google_drive/the-genesis-order/data/CommonEvents.json`. Wcześniejszy check 45 229 rekordów / 238 źródeł przeszedł; nie zmieniano eksportu JSONL.
- Nie uruchamiano gry/kodu gry. Nie wygenerowano tłumaczenia ani patcha.

## 2026-10-29 — zatwierdzony zakres tekstów i source ZIP w Git/Drive

- Właściciel zatwierdził wszystkie **1 513** nie-rendererowych wierszy `401` i wszystkie **2 110** opcji `102` jako pełnoprawny, widoczny dla gracza tekst do tłumaczenia. W eksporcie kategorie mają neutralne nazwy `native_message` i `choice_option`; usunięto podtypy sugerujące nierozstrzygnięty zakres, zachowując wydane ID.
- Potwierdzono, że tekst wtopiony w obrazy i wideo nie jest tłumaczony. Oryginalne media i kod gry pozostają poza zakresem/pakietem.
- Zaktualizowano manifest, generator eksportu, testy, format rekordów, raporty, zasady i handoff. Markdown odtworzony: 497 dokumentów / 45 229 rekordów; import-check: 0 braków.
- Pełne `unittest`: **27/27 passed**; `py_compile` i `git diff --check` przechodzą. Builder wymaga poprawnych liczników 1 513/2 110, sprawdza coverage i integralność ZIP-a.
- Source ZIP v1: `games/the-genesis-order/translation/packages/TGO_source_translation_package_v1.zip`, **8 499 321 B**, 531 wpisów, 45 229 rekordów, 497 Markdown, 131 chronionych wartości; SHA-256 `b2215cf29c33ad0f42e22852f3179985b829338be019887b13e5b8818217e2b6`.
- ZIP i sidecar `.sha256` są śledzone w Git. Identyczny artefakt i checksum przesłano na Google Drive: `TGO/translation/packages/` ([ZIP](https://drive.google.com/file/d/1G7T1-bKW9AFHR2tiwXK6xGBJCSSm2IWS/view?usp=drivesdk), [SHA-256](https://drive.google.com/file/d/1oiT5PIqOP2qqyoON2Xz1JQ0cKod0tNip/view?usp=drivesdk)).
- Nie uruchamiano gry ani kodu gry; nie ma jeszcze tłumaczenia ani patcha.
