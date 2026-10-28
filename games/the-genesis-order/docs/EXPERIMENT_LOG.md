# Dziennik eksperymentów — The Genesis Order

## 2026-10-28 — pierwszy pakiet inwentaryzacyjny

- **Cel:** zebrać lokalny spis plików i rozmiary bez założenia silnika lub ścieżki instalacji.
- **Pakiet:** `TGO_INVENTORY_REQUEST.zip`, SHA-256 `17305fbf058383f5c9f38472ff60640916de8a684e303096a5052d078ad0478f`; Drive file ID `1Tl3Pmu8PHb5aQXpA5Ah2OKvL0qO96TBe`.
- **Zawartość:** `URUCHOM.bat`, `COLLECT_TGO.ps1`, `INSTRUKCJA.txt`.
- **Zakres raportu:** plik CSV wszystkich ścieżek względnych/rozmiarów/rozszerzeń/czasów modyfikacji, lista potencjalnych zasobów, podsumowanie, metadane EXE i log. Raport nie ma zawierać bajtów plików gry.
- **Walidacja sandbox:** ZIP poprawny (CRC), ma trzy oczekiwane pliki; statyczne kontrole potwierdziły generator raportu i brak polecenia usuwania. Skrypt nie był wykonany przez PowerShell ani na Windowsie.
- **Wynik:** brak wyniku gry do odnotowania. Status pakietu na Windowsie: **niezweryfikowany**.
- **Następny krok:** użytkownik uruchamia `.bat`, zwraca ZIP wynikowy przez Drive; po odbiorze zapisać jego ID, rozmiar i SHA-256, a następnie zaktualizować ustalenia.
