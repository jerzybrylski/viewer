# Statyczny census tekstu — Being a DIK, GOG Season 1

**Stan:** pełny census skompilowanych skryptów `scripts.rpa`; statyczny, bez uruchamiania gry.  
**Data:** 2026-10-28  
**Zakres builda:** GOG *Being a DIK — Season 1*, `en-US`, `buildId=55720371802277951`; kopia zawiera skrypty odczytane z `scripts.rpa` (158 wpisów `.rpyc`). Nie potwierdzono rewizji treści dokładniejszej niż identyfikator builda z manifestu.

## Wynik główny

| Kategoria | Wystąpienia w źródle | Różne teksty / wzorce | Uwagi |
|---|---:|---:|---|
| Instrukcje dialogowe Ren’Py `Say` | **16 669** | **14 650** | Wszystkie zapisane gałęzie/warunki; 16 510 ma jawnego mówiącego, a 159 nie ma jawnego mówiącego (w tym narracja). |
| Opcje standardowych bloków `menu` | **1 266** w 521 menu | **776** | Liczone oddzielnie od dialogu; menu i opcje obejmują wszystkie statycznie zapisane warianty. |
| Wiadomości zapisane w historii aplikacji telefonu / feedzie | **487** | **439** wzorców | 424 literalne wpisy oraz 63 wzorce z podstawieniem; 23 dodatkowe wpisy są dynamicznymi wartościami, a nie stałym tekstem. |
| Odpowiedzi gracza w interaktywnych czatach telefonu | **400** | **386** | Tablice wyborów czatów i Swypera; osobne od standardowych `menu`-bloków. |

**Łącznie:** 17 156 statycznych wystąpień tekstu konwersacyjnego (`Say` + gotowe wiadomości telefonu/feedu), a osobno 1 666 wystąpień opcji wyboru (menu + wybory w telefonie). Kategorie są celowo rozdzielone; nie są to liczby ekranów ani unikalnych ścieżek rozgrywki.

### Rozkład głównych plików `scripts.rpa`

| Moduł | `Say` | Menu | Opcje menu |
|---|---:|---:|---:|
| `script.rpyc` | 2 458 | 92 | 192 |
| `update2.rpyc` | 3 209 | 79 | 159 |
| `update3.rpyc` | 3 710 | 74 | 163 |
| `update4.rpyc` | 2 691 | 43 | 97 |
| `header.rpyc` | 64 | 4 | 9 |
| Pozostałe 153 moduły | 4 537 | 229 | 646 |
| **Razem** | **16 669** | **521** | **1 266** |

## Jak liczyliśmy

- Z `scripts.rpa` wyodrębniono 158 skompilowanych plików `.rpyc`. Każdy plik został statycznie zdekompilowany przez `unrpyc` v2.0.3 (HEAD `3ae8334ed71a05535927dcc559663d3aca51215b`).
- Do dokładnego licznika dialogu i menu odczytano bezpiecznie załadowane węzły AST Ren’Py; zliczono węzły `Say`, menu i każde tekstowe menu-item. Nie obliczano warunków i nie uruchamiano gry, dzięki czemu objęto wszystkie zapisane odnogi, a nie tylko jedną trasę.
- Węzły `Say` zweryfikowano z tekstem źródłowym dekompilacji: potwierdzone 16 510 jawnych wypowiedzi z mówiącym oraz dodatkowe 159 wypowiedzi bez aliasu (m.in. narrator). Wszystkie 16 669 ma niepusty tekst.
- Dla telefonu statycznie przeanalizowano bloki Pythona w dekompilowanych skryptach, bez wykonywania ich. Teksty dopisywane do historii wiadomości i feedu ujęto jako osobną kategorię; teksty w tablicach `*_reply_array` policzono jako odpowiedzi gracza.
- Wystąpienia liczą kolejne zapisy w kodzie, także powtórzone warianty w osobnych warunkach. Deduplikacja jest wyłącznie porównaniem surowych, zakodowanych tekstów/wzorców; nie scala podobnych sformułowań ani stringów z różnymi placeholderami.

### Kontrola kompletności

| Kontrola | Wynik |
|---|---:|
| Pliki `.rpyc` w archiwum / poprawnie załadowane AST | 158 / **158** |
| Błędy odczytu AST | **0** |
| Pliki, przy których dekompilator zgłosił ostrzeżenie o starszym Ren’Py | 133 |
| Standardowe menu / tekstowe opcje | 521 / **1 266** |
| Jawni mówiący / wypowiedzi bez mówiącego | 16 510 / **159** |

Ostrzeżenia dotyczą tego, że narzędzie targetuje Ren’Py 8, a część bytecode’u pochodzi z Ren’Py 7 lub starszego. Nie uniemożliwiły one parsowania żadnego z 158 plików, ale pozostają ograniczeniem niezależnej walidacji semantycznej.

## Zakres i wyłączenia

**Uwzględniono:** skompilowane skrypty z dostarczonego `scripts.rpa`, w tym główne epizody, route/freeroam, testy/sceny, mini-gry, standardowe menu oraz statycznie zapisane teksty rozmów i feedu w aplikacjach telefonu.

**Nie wliczono do powyższych kategorii:** zwykłych etykiet GUI i przycisków, opisów ustawień, nazw plików/assetów, ścieżek obrazów/audio/wideo, kodu i identyfikatorów, tekstów generowanych wyłącznie w runtime bez stałej treści źródłowej ani innych potencjalnych tekstów poza `scripts.rpa`. UI warto zinwentaryzować osobno przed zamknięciem zakresu lokalizacji. Liczby nie obejmują Seasons 2/3 ani niepotwierdzonych dodatków.

## Ograniczenia

- To census tekstu w skryptach dostarczonego builda, nie liczba słów, znaków, ekranów ani rzeczywistych wypowiedzi podczas jednego przejścia. Te same teksty zapisane w różnych stanach liczą się jako osobne wystąpienia.
- Wzorce telefonu mogą zawierać podstawienia nazw lub zmiennych. Raport liczy każde zakodowane wystąpienie wzorca, nie wszystkie kombinacje runtime.
- 23 dynamiczne dopisania do historii telefonu/feedu nie mają własnego stałego tekstu w miejscu dopisania; część może przenosić wybór gracza ujęty już w kategorii opcji.
- Nie badano osobno tytułów kontaktów, opisów profili, podpisów obrazów, etykiet i pozostałego tekstu ekranów telefonu. UI oraz teksty baz danych/ekranów wymagają osobnego przebiegu, zgodnie z zakresem projektu.
- Nie uruchamiano gry, jej skryptów ani patcha. Nie weryfikowano renderowania polskich znaków, stylów, łamania linii, save compatibility ani runtime w Windows.

## Artefakty źródłowe / powtarzalność

- RPA: `scripts.rpa`, 9 526 870 B, SHA-256 `c9ba7ef3801f482df157afc39a662c7c0e0cbf6455e74657ecc8b2f46d24d86f`.
- Wyodrębnione pliki są obecnie w `google_drive/being-a-dik/raw/`; tekstowe dane projektu należy śledzić w Git, binarne assety gry pozostają poza Git.
- Log dekompilacji: `/tmp/badik-unrpyc.log`. Skrypt tymczasowy licznika AST: `/tmp/badik_ast_count.py` (nie jest częścią produktu ani gry).
- Zdekompilowane źródła pozostają materiałem statycznej analizy; nie należy ich kopiować do publicznych materiałów ani traktować jako zgody na redystrybucję treści.

**Decyzja projektowa:** nie rozpoczęto tłumaczenia. Żaden tytuł nie został wybrany przez właściciela.
