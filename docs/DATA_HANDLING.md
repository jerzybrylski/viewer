# Dane, prywatność i repozytorium

## Zasada

Użytkownik pracuje na własnej kopii gry. Agent prosi o metadane, a potem o minimalną próbkę niezbędną do analizy. Nie pobieramy ani nie przechowujemy całych instalacji.

## Nigdy nie commituj

- instalatorów, binariów, pełnych archiwów/assetów gry, ich ekstraktów ani hurtowych zrzutów źródłowego tekstu;
- zapisów gry, prywatnych screenshotów bez zgody, danych konta, kluczy/credentiali;
- pełnego builda zmodyfikowanej gry, patcha zawierającego oryginalne dane lub cudzych materiałów;
- raportu, który ujawnia więcej danych użytkownika niż potrzeba.

## Katalog lokalny

Dane wejściowe, wyjściowe, cache, testowe buildy, ekstrakty źródłowe i zwrotki przechowuj pod `games/<slug>/local/` lub `games/<slug>/build/`. Są ignorowane przez Git. Nie używaj ich do trwałej dokumentacji bez oczyszczenia i sprawdzenia.

Raporty/inwentaryzacje mogą być commitowane tylko wtedy, gdy są ograniczone do potrzebnych metadanych i nie ujawniają prywatnych ścieżek. Zanim utrwalisz hash lub Drive ID, sprawdź, czy dotyczy pliku diagnostycznego/zasobu i czy jest przydatny do odtworzenia ustaleń.

Dane tłumaczeniowe autorstwa projektu można przechowywać w Git, gdy są potrzebne do współpracy i nie zawierają niepotrzebnie dużych fragmentów oryginalnego tekstu ani materiałów referencyjnych objętych prawami. Tabele łączące polski tekst z surowym źródłem, screenami lub assetami pozostają lokalne/prywatne, chyba że właściciel projektu świadomie zdecyduje inaczej.

## Drive

Używaj Drive jako prywatnego kanału wymiany. Zapisuj ID pliku dla kontynuacji; nie ustawiaj publicznego dostępu bez wyraźnej zgody. W pakietach diagnostycznych informuj, że raport może zawierać nazwy folderów, wersje i ścieżki instalacji. Użytkownik powinien przesyłać wyłącznie wskazany ZIP.
