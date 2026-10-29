# TGO PL — lokalny patch, proof of concept

Paczka stosuje tłumaczenia TGO do **lokalnej kopii gry użytkownika**. Nie zawiera oryginalnych ani przebudowanych plików gry. Nie jest finalnym wydaniem: nie została przetestowana w Windows ani w uruchomionej grze, a teksty nadal wymagają redakcji i QA. Audyt pokrycia tłumaczeń dołączono jako `payload\translation_coverage.json`.

## Wymagania i instalacja

- Windows 10 lub nowszy oraz Python **3.10+** dostępny jako `py -3` albo `python` (patcher używa wyłącznie biblioteki standardowej; okna dialogowe to `tkinter`, dołączany do instalatora Pythona z python.org).
- Rozpakuj ZIP do osobnego folderu. Zamknij grę.
- Uruchom `APPLY.bat` — **nie trzeba wpisywać żadnej ścieżki**. Patcher sam znajdzie instalację, a jeśli znajdzie
  więcej niż jedną, pokaże listę do wyboru. Gdy automat nie ma pewności, otworzy okno wyboru folderu
  (ten, w którym jest `www\index.html`).
- Wybrana instalacja jest **zapamiętywana** raz na zawsze: następne uruchomienia `APPLY.bat` i `COFNIJ.bat`
  nie pytają już o folder, tylko pokazują, której instalacji użyją. Ścieżkę do innej instalacji można podać
  argumentem (przeciągnięcie folderu na `APPLY.bat`) albo wyczyścić pamięć: `patcher.py --forget`.
- Patcher weryfikuje SHA-256 **238 plików źródłowych** przed stagingiem. Pakiet wspiera wyłącznie dokładny fingerprint eksportu źródłowego v1, a nie dowolną wersję produktu. Wykryta różnica, modyfikacja lub brak pliku kończy pracę bez zmian w grze.
- Najpierw wszystkie zmienione pliki są przygotowywane i weryfikowane w stagingu. Przed pierwszą podmianą tworzony jest backup każdego pliku. Gra nie jest uruchamiana.

## Jak patcher znajduje grę

Kolejność jest stała i nic nie jest modyfikowane na tym etapie:

1. argument (przeciągnięty folder) albo `--game ŚCIEŻKA`,
2. zapamiętana ścieżka z poprzedniego uruchomienia,
3. automatyczne przeszukanie: biblioteki Steam z `libraryfolders.vdf`, typowe foldery gier na wszystkich
   dyskach (`Games`, `GOG Games`, `SteamLibrary\steamapps\common`, `Epic Games`), foldery z nazwą zawierającą
   „genesis”, a także Pulpit, Pobrane, Dokumenty i katalog, z którego uruchomiono patcher,
4. okno wyboru folderu — ostatnia deska ratunku, nigdy obowiązkowe.

Katalog gry jest rozpoznawany po obecności `www\index.html` i `www\data\System.json`. Przeszukiwanie ma limit
głębokości, czasu i liczby wyników, więc nie zamienia się w skan całego dysku. Pamięć ścieżki leży
w `%APPDATA%\TGO_PL_patch\config.json` i zawiera wyłącznie ścieżkę oraz wersję patcha — nic więcej.

## Cofanie / przerwana instalacja

Uruchom `COFNIJ.bat` — użyje zapamiętanej instalacji (albo znajdzie ją sam / zapyta oknem wyboru). Cofnięcie sprawdza aktualny hash pliku i hash kopii zapasowej; jeśli plik zmienił się po instalacji, patcher odmawia nadpisania. Backupy zostają w `.tgo-pl-originals\0.1.1-poc\` w folderze gry. Stan transakcji jest w `.tgo-pl-patch-state.json`. Zachowaj oba zasoby.

Po instalacji uruchom grę i sprawdź wybrane dialogi, menu, polskie znaki, łamanie wierszy oraz wybory. Jeśli pojawi się problem, zamknij grę, uruchom `COFNIJ.bat` i zachowaj raport błędu.

## Zakres

Paczka zawiera scalone tłumaczenia, manifesty weryfikacji źródeł i raport audytu pokrycia. Wartości chronione, nazwy własne, kwoty, symbole, kody rendererów i inne niejęzykowe wartości są zachowane zgodnie z raportem; tekst wtopiony w grafikę/wideo pozostaje poza zakresem. Nie są dołączane assety, save'y ani kod gry. Zgodność produktowego numeru wydania nie została potwierdzona — decydującą ochroną jest ścisła kontrola hashy. Szczegóły zakresu znajdują się w dołączonym `payload\patch_manifest.json`.
