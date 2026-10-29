# Środowisko projektu

Ten plik opisuje wyłącznie środowisko znane i sprawdzone w chwili jego aktualizacji. Wymagania związane z konkretną grą zapisuj także w jej katalogu.

## Środowisko agenta

- Praca nad repo odbywa się w sandboxie Linux; należy pracować na gałęzi wskazanej dla bieżącej sesji Arena, bez przełączania jej.
- Python 3 jest dostępny w sandboxie, ale repo nie ma jeszcze wspólnego `requirements.txt` ani obowiązkowego toolchainu tłumaczeniowego.
- PowerShell (`pwsh`/`powershell`) nie jest dostępny w sandboxie. Skrypty PowerShell przeznaczone dla Windows należy statycznie sprawdzić tutaj, a ich wykonanie oznaczać jako **niezweryfikowane**, dopóki użytkownik nie uruchomi ich na swoim komputerze i nie zwróci raportu.
- Nie ma lokalnej instalacji The Genesis Order ani innych kopii gier do testów.

## Środowisko użytkownika

- Użytkownik potwierdził, że gra na Windowsie.
- Dokładna wersja/build gry, sklep (Steam/GOG/inny), ścieżka instalacji i konfiguracja systemu nie są jeszcze potwierdzone.
- Pierwszy pakiet TGO zakłada Windows PowerShell 5.1 dostępny w typowym Windows 10/11; korzysta z `Compress-Archive`. Nie wymaga instalacji Pythona.
- Pakiet TGO wyszukuje typowe ścieżki Steam/GOG, a jeśli nie znajdzie gry, prosi o folder instalacyjny lub ścieżkę do EXE. To mechanizm pomocniczy, nie potwierdzenie lokalizacji użytkownika.
- Pakiet i skrypt nie były uruchomione na Windowsie. Ich wykonanie, czas skanowania i zgodność z lokalną polityką systemu pozostają niezweryfikowane.

## Narzędzia

- `tools/folio-viewer/index.html`: samodzielny HTML/CSS/JavaScript bez zależności; historyczne narzędzie projektu, instrukcja w jego README.
- Dla każdego tytułu dobieramy ekstraktory i edytory dopiero po rozpoznaniu zasobów. Wymagania, wersje narzędzi, źródła pobrania i polecenia testowe dopisujemy do `games/<slug>/ENVIRONMENT.md` albo do sekcji jego README.

## Konwencja statusu testów

W dokumentacji rozróżniaj: **przetestowane w sandboxie**, **przetestowane na Windowsie przez użytkownika**, **przetestowane w uruchomionej grze** oraz **niezweryfikowane**. Samo utworzenie ZIP-a lub statyczne sprawdzenie kodu nie dowodzi, że skrypt działa na systemie docelowym.
