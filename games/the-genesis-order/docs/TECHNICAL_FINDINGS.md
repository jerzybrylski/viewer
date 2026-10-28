# Ustalenia techniczne — The Genesis Order

Daty i źródła szczegółowych testów znajdują się w [`EXPERIMENT_LOG.md`](EXPERIMENT_LOG.md). To zestawienie rozdziela wiedzę od przypuszczeń.

## Potwierdzone w tym projekcie

- Użytkownik pracuje na Windowsie.
- Pierwszy BAT/PS1 został przygotowany jako skrypt inwentaryzacyjny tylko do odczytu. Oczekiwany wynik to raport nazw/rozmiarów, nie pliki gry.
- Automatyczne wykrywanie instalacji w skrypcie obejmuje typowe katalogi Steam/GOG; w razie niepowodzenia skrypt prosi o folder lub ścieżkę EXE.

## Hipotezy / zakres skanowania

- Lista potencjalnych zasobów w raporcie jest filtrem po rozszerzeniach i nazwach katalogów; **nie potwierdza**, że pliki zawierają tekst.
- Nazwy folderów instalacyjnych mogą różnić się od standardowych; fallback użytkownika jest wymagany.

## Nieznane

- Konkretny silnik i format pakowania.
- Wersja, sklep, DLC, kompletność i ścieżka kopii użytkownika.
- Gdzie są teksty, jak zachować sceny/wybory i jakie są limity techniczne.
- Czy istnieje bezpieczna metoda modyfikacji / instalacji spolszczenia.

## Wcześniejsze źródła zewnętrzne — ograniczone wnioski

Wcześniejszy rekonesans wykazał, że oficjalne wykazy języków wymieniają angielski; nie znaleziono wiarygodnego polskiego fanowskiego patcha. To nie dowodzi, że taka kopia nigdy nie istniała, i nie zastępuje analizy wersji użytkownika. Źródła: [Steam app details](https://store.steampowered.com/api/appdetails?appids=2553870&l=english), [Steam Support](https://help.steampowered.com/en/wizard/HelpWithGameTechnicalIssue?appid=2553870), [GOGDB](https://www.gogdb.org/product/1598140349), [PCGamingWiki](https://www.pcgamingwiki.com/wiki/The_Genesis_Order).
