# TGO PL — lokalny patch, proof of concept

Paczka stosuje tłumaczenia TGO do **lokalnej kopii gry użytkownika**. Nie zawiera oryginalnych ani przebudowanych plików gry. Nie jest finalnym wydaniem: nie została przetestowana w Windows ani w uruchomionej grze, a teksty nadal wymagają redakcji i QA. Audyt pokrycia tłumaczeń dołączono jako `payload\translation_coverage.json`.

## Wymagania i instalacja

- Windows 10 lub nowszy oraz Python **3.10+** dostępny jako `py -3` albo `python` (patcher używa wyłącznie biblioteki standardowej).
- Rozpakuj ZIP do osobnego folderu. Zamknij grę.
- Uruchom `APPLY.bat` i podaj folder instalacyjny TGO — ten, w którym znajduje się `www\index.html`. Można też przeciągnąć ścieżkę folderu na `APPLY.bat`.
- Patcher weryfikuje SHA-256 **238 plików źródłowych** przed stagingiem. Pakiet wspiera wyłącznie dokładny fingerprint eksportu źródłowego v1, a nie dowolną wersję produktu. Wykryta różnica, modyfikacja lub brak pliku kończy pracę bez zmian w grze.
- Najpierw wszystkie zmienione pliki są przygotowywane i weryfikowane w stagingu. Przed pierwszą podmianą tworzony jest backup każdego pliku. Gra nie jest uruchamiana.

## Cofanie / przerwana instalacja

Uruchom `COFNIJ.bat` i wskaż ten sam folder instalacji. Cofnięcie sprawdza aktualny hash pliku i hash kopii zapasowej; jeśli plik zmienił się po instalacji, patcher odmawia nadpisania. Backupy zostają w `.tgo-pl-originals\0.1.1-poc\` w folderze gry. Stan transakcji jest w `.tgo-pl-patch-state.json`. Zachowaj oba zasoby.

Po instalacji uruchom grę i sprawdź wybrane dialogi, menu, polskie znaki, łamanie wierszy oraz wybory. Jeśli pojawi się problem, zamknij grę, uruchom `COFNIJ.bat` i zachowaj raport błędu.

## Zakres

Paczka zawiera scalone tłumaczenia, manifesty weryfikacji źródeł i raport audytu pokrycia. Wartości chronione, nazwy własne, kwoty, symbole, kody rendererów i inne niejęzykowe wartości są zachowane zgodnie z raportem; tekst wtopiony w grafikę/wideo pozostaje poza zakresem. Nie są dołączane assety, save'y ani kod gry. Zgodność produktowego numeru wydania nie została potwierdzona — decydującą ochroną jest ścisła kontrola hashy. Szczegóły zakresu znajdują się w dołączonym `payload\patch_manifest.json`.
