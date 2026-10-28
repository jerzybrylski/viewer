# The Genesis Order — projekt spolszczenia

Projekt rozpoczęty od **bezpiecznej inwentaryzacji lokalnej kopii użytkownika**. Pierwszy raport już otrzymaliśmy; układ plików mocno wskazuje na RPG Maker MV + NW.js. Wersja/build i pochodzenie kopii wymagają jeszcze potwierdzenia.

## Stan

**Inwentaryzacja zakończona; kolejny etap czeka na potwierdzenie źródła kopii.** Raport `TGO_DIAGNOSTIC_20261028_191643.zip` został przesłany na Drive, ID `1gwWlg0ywzYY8k0gjWDi77iTNGl70zmaL`. Zawiera wyłącznie spis ścieżek i metadane, nie pliki gry.

Raport wykazuje ścieżkę `_Redist\fitgirl.md5`, co może oznaczać repack FitGirl. Zanim przygotujemy kolejny pakiet zawierający pliki gry, prosimy o potwierdzenie, że dalsza analiza będzie dotyczyła autoryzowanej kopii ze sklepu. To pozwoli uniknąć analizy zmodyfikowanego lub niezweryfikowanego wydania.

Szczegóły: [status](docs/STATUS.md), [ustalenia techniczne](docs/TECHNICAL_FINDINGS.md), [dziennik eksperymentów](docs/EXPERIMENT_LOG.md), [środowisko](ENVIRONMENT.md), [instrukcje agentów](AGENTS.md).

## Kolejność prac

1. Potwierdzić oficjalne źródło/licencję kopii i jeśli trzeba wykonać tylko inwentarz na legalnej instalacji sklepowej.
2. Przygotować drugi BAT/PS1 do skopiowania minimalnego zestawu dokładnie wskazanych plików JS/JSON potrzebnych do identyfikacji wersji i formatu tekstu.
3. Po otrzymaniu próbki ustalić język źródłowy, ekstrakcję, identyfikatory tekstu, kontekst scen/wyborów, kodowanie i ograniczenia renderowania.
4. Dopiero potem projektować workflow tłumaczenia, testów i patcha.

Nie przesyłaj całego katalogu gry ani multimediów. Nie modyfikujemy oryginałów ani zapisów podczas rozpoznania.
