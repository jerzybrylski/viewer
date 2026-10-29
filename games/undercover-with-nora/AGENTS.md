# Instrukcje — Undercover with Nora

## Start

Przeczytaj `../../AGENTS.md`, `../../ENVIRONMENT.md`, `README.md`, `ENVIRONMENT.md`, `docs/STATUS.md`, `docs/TECHNICAL_FINDINGS.md`, `docs/COUNT_REPORT.md` i `docs/EXPERIMENT_LOG.md`.

## Fakty i ograniczenia

- Badana kopia to `Undercover With Nora` v1.0.0, Ren'Py 8.3.3.24111502, z archiwum `game/01001110.rpa` w formacie RPA-3.0.
- W dostarczonym archiwum znaleziono 23 skompilowane skrypty `.rpyc`; wszystkie zdekompilowano próbnie. Pełne liczniki znajdują się w `docs/COUNT_REPORT.md`.
- Nie uruchamiaj gry ani kodu z archiwum. Do analizy używaj kopii w ignorowanym `google_drive/uwn/`; nie commituj archiwów, zdekompilowanych `.rpy`, assetów ani dialogów.
- W raporcie liczone są instrukcje dialogowe `say` z rozpoznanym mówiącym, a opcje z instrukcji `menu` są osobno. Treści UI i teksty tworzone dynamicznie poza tym wzorcem wymagają osobnej inwentaryzacji.
- Uwzględniaj wszystkie gałęzie/warunki źródłowe. Nie spłaszczaj ich do jednej trasy ani nie zakładaj kanonicznych wyborów.
- Użytkownik jeszcze nie wybrał tego tytułu do rozpoczęcia tłumaczenia. Nie twórz tłumaczenia ani patcha bez osobnej decyzji.

## Zasady

- Nie zakładaj, że build v1.0.0 odpowiada innym wydaniom gry; raport dotyczy wyłącznie kopii w folderze UWN na Drive.
- Zachowuj stabilne identyfikatory scen/labeli, nazwy mówiących, warunki, wybory i kolejność. W Czytance pokazuj odgałęzienia jawnie.
- Przed deklaracją pełnego zakresu lokalizacji oddziel dialogi od UI, przycisków, osiągnięć, nazw własnych, tekstów screenów i mediów.
