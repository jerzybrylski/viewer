# Glosariusz — The Genesis Order

Decyzje **robocze**, oparte na locatorach i kontekście kanonicznego eksportu v1. Nie są jeszcze zatwierdzeniem właściciela ani wynikiem testu w grze. Formy fabularne i imiona wymagają osobnego przeglądu scen; nie wyciągamy ich z samych nazw.

| Oryginał | Forma polska | Kontekst / źródło decyzji | Status / uwagi |
|---|---|---|---|
| The Genesis Order | The Genesis Order | `system.gameTitle`, tytuł gry | roboczo zachować nazwę własną |
| Level / Lv | Poziom / Poz. | `system.terms`, basic 0–1 | robocze; skrót wymaga testu szerokości |
| Item / Key Item | Przedmiot / Przedmiot kluczowy | `system.terms`, commands 4 / 14 | robocze; nie przesądza nazw konkretnych przedmiotów |
| Skill | Umiejętność | `system.terms`, commands 5 | robocze |
| Save / Continue / New Game | Zapisz / Kontynuuj / Nowa gra | `system.terms`, commands 9 / 19 / 18 | robocze; zachować źródłowe wcięcia |
| Fullscreen / Low Quality Video | Pełny ekran / Niska jakość wideo | `ui.plugin_parameter`, `ui.plugin_static` | robocze, sprawdzić szerokość |
| Connection Type / Connected / Not Connected | Typ połączenia / Połączono / Nie połączono | `ui.plugin_static`, Lovense | robocze; etykieta typu zachowuje końcową spację |
| Lovense Remote / PC / LAN / Web | Lovense Remote / PC / LAN / Web | `ui.plugin_parameter` i `ui.plugin_static` | nazwa własna; trzy ostatnie to chronione operandy, pozostają bez zmian |
| Angelcraft / Angelcrafting | Angelcraft | wskazówki CE23; nazwa funkcji tworzenia | roboczo zachować nazwę; sprawdzić w UI i ekwipunku |
| cable thimble / cable crimps | kausza / zaciski linowe | wskazówki CE23 o naprawie żyrandola | hipoteza terminologiczna, porównać z nazwami przedmiotów i sceną |
| HP / MP / TP / EXP | HP / MP / TP / EXP | `system.terms`, basic 2–9 | roboczo zachować skróty; znaczenia i użycie sprawdzić w grze |

## Konwencja partii UI 01

Dla komunikatów z dynamicznym `%1` stosujemy bezosobowe konstrukcje, żeby nie zgadywać rodzaju ani odmiany nazwy. Kolejność i liczba tokenów pozostają niezmienione. Marki, nazwy plików i widoczne nazwy obcych przycisków pozostają oryginalne. Nie zakładamy limitu szerokości ani dostępności polskich znaków; potrzebny jest test runtime. Teksty są wersją roboczą do redakcji w kontekście.
