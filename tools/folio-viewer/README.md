# Folio — viewer screenshotów visual novel

Samodzielny viewer w `index.html` (HTML, CSS, vanilla JavaScript). Nie wymaga instalacji ani połączenia z internetem.

## Uruchomienie

1. Otwórz `index.html` lokalnie w Chrome lub Edge.
2. Kliknij **Otwórz folder** i wskaż folder ze screenshotami PNG.
3. Oznaczenia dodajesz ikoną **⚑** na miniaturze; nie trzeba zmieniać nazw ani zawartości plików.

## Sceny i rozgałęzienia

- Globalny przycisk **Pokaż nieoznaczone** jest dostępny niezależnie od bieżącej sceny lub rozgałęzienia. Pokazuje chronologicznie ilustracje od ostatniego oznaczenia **Początek nowej sceny**, **Punkt wyboru** albo **Dalsza część sceny** do końca folderu. Po dodaniu kolejnego takiego oznaczenia zakres przesuwa się do nowej pozycji. **Wróć do oglądania sceny** przywraca wybraną ścieżkę i decyzje gałęzi.
- **Początek nowej sceny** dzieli zrzuty na osobne galerie. Możesz opcjonalnie nadać scenie nazwę.
- **Dalsza część sceny** dołącza ciąg ilustracji do wybranej sceny; otwarte zakończenia zostają połączone z tym ciągiem.
- **Pokaż sieroty** wyświetla ilustracje, do których nie prowadzi żadna osiągalna scena ani gałąź.
- **Punkt wyboru** zatrzymuje ciąg, a **Początek wyboru** tworzy oznaczoną gałąź. Można wskazać również zagnieżdżony wybór.
- **Wróć do wspólnej ścieżki** łączy gałęzie A/B w tym samym miejscu sceny.
- Kliknięcie etykiety A/B zmienia gałąź; ponowne kliknięcie wybranej etykiety cofa do wyboru. Po końcu gałęzi można wskazać następną scenę.
- Bieżąca scena i rozmiar miniaturek są zapamiętywane w `localStorage`.

Kolejność screenshotów wynika z rosnącego numeru na początku nazwy, a dla nazw bez numeru — z daty modyfikacji.

## Tagi

Przytrzymaj **Shift** i klikaj ilustracje, aby zaznaczyć kilka. **Dodaj tag zaznaczonym** dopisze tagi do wszystkich wybranych obrazów. W oknie oznaczania można podać kilka tagów oddzielonych przecinkami. Chmura tagów filtruje ilustracje; **Pokaż sceny** wraca do widoku scen.

## Zapis i podgląd

Sceny, wybory i tagi zapisują się automatycznie w `localStorage`. **Pobierz oznaczenia** eksportuje JSON, a **Wczytaj oznaczenia** przywraca kopię. Kliknięcie miniatury otwiera podgląd; **X**, kliknięcie ilustracji lub strzałki nawigują po nim. Rozmiar miniaturek zmienia suwak lub **Ctrl + kółko myszy**.
