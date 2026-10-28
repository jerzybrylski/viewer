# Status — The Genesis Order

**Stan: rozpoczęcie lokalizacji / oczekiwanie na raport inwentaryzacji.** Aktualizacja: 2026-10-28.

## Potwierdzone

- Użytkownik ma Windows i chce etapowy workflow BAT/PowerShell → ZIP → Google Drive.
- Przygotowano pierwszy pakiet inwentaryzacyjny. Jego ZIP zawiera wyłącznie `URUCHOM.bat`, `COLLECT_TGO.ps1` i `INSTRUKCJA.txt`; został przesłany na Drive pod ID `1Tl3Pmu8PHb5aQXpA5Ah2OKvL0qO96TBe`.
- Skrypt ma zbierać inwentarz nazw/rozmiarów i podstawowe metadane, bez kopiowania zawartości gry i bez modyfikacji instalacji.

## Niezweryfikowane / nieznane

- Pakiet nie został jeszcze uruchomiony na Windowsie.
- Wersja, sklep, lokalizacja i kompletność instalacji użytkownika.
- Silnik, format zasobów, lokalizacja tekstu, kodowanie, mechanizm patchowania i ograniczenia wyświetlania.
- Żaden tekst nie został wyekstrahowany ani przetłumaczony; nie ma patcha.

## Następny krok

Odebrać wynikowy `TGO_DIAGNOSTIC_....zip` od użytkownika przez Drive; zweryfikować zawartość, wyciągnąć strukturę zasobów i dopiero wtedy zaprojektować drugi pakiet zbierający minimalną próbkę.
