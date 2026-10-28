# Ustalenia techniczne — Being a DIK

## Potwierdzone z plików Drive

### Wydanie i silnik

- Folder `Game` zawiera `goggame-1181224050.info`: nazwa `Being a DIK - Season 1`, `gameId=1181224050`, `buildId=55720371802277951`, `language=en-US`, primary `BeingADIK.exe`.
- `script_version.txt` = `(7, 4, 10)`.
- Dostarczony `log.txt` zawiera `Ren'Py 7.4.10.2178` i identyfikację `Windows-10-10.0.16299`. Log dokumentuje start silnika, nie test lokalizacji.

### RPA indexy

Każde zbadane archiwum ma `RPA-3.0` i nagłówek `0x42424242`. Indeksy odczytano po sprawdzeniu opcode'ów pickle allowlistą; nie wykonywano kodu gry ani funkcji z archiwów. Dwa pojedyncze `.rpyc` wyekstrahowano do `/tmp` i zdekompilowano osobnym, bezpiecznym loaderem AST (szczegóły w `EXPERIMENT_LOG.md`).

| Archiwum | Rozmiar | Liczba wpisów | Typy w indeksie |
|---|---:|---:|---|
| `scripts.rpa` | 9,526,870 B | 158 | 158 × `.rpyc` |
| `archive.rpa` | 16,645,751 B | 47 | 46 × `.png`, 1 × `.mp3` |
| `gallery.rpa` | 6,605,109 B | 90 | 89 × `.png`, 1 × `.jpg` |
| `patch_v042.rpa` | 14,849,201 B | 2 | 1 × `.webm`, 1 × `.jpg` |

W `scripts.rpa` są m.in. skrypty `script.rpyc`, `update2/3/4.rpyc`, epizody 2–4, freeroam, klasy/testy, sceny, telefony (chaty, Swyper, Rooster, Brawler, kontakty, bios, odpowiedzi), raporty, nagrody i `screens.rpyc`. Lista nazw jest w prywatnym indeksie z Drive; nie kopiować jej do publicznych materiałów z zawartością gry.

### Fonty

Odczyt tabel Unicode cmap w przesłanych fontach (18 wymaganych liter `ąćęłńóśźżĄĆĘŁŃÓŚŹŻ`):

| Font | Pokrycie cmap |
|---|---:|
| `Museo500.otf`, `Redressed.ttf`, `candara.ttf`, `centurygothicregular.ttf`, `centurygothicbold.ttf` | 18/18 każdy |
| `Audrey-Bold.otf`, `bradhitc.ttf` | 4/18 każdy |
| `cabin-regular.ttf`, `symbolfont.ttf` | częściowe |
| `collegiate.ttf` | 0/18 |

To mierzy obecność glifów, a nie to, który krój dany widok faktycznie wybiera ani czy font może być redystrybuowany.

## Niewiadome / testy do wykonania

- Niezależna semantyczna walidacja starszego bytecode’u pozostaje niewykonana. `unrpyc` zgłosił ostrzeżenie Ren’Py 7 dla 133 plików, choć wszystkie 158 AST załadowały się bez błędu.
- Pełny census skryptów znajduje się w `docs/COUNT_REPORT.md`; kompletność UI/etykiet i wszystkich domen telefonu w użytkowej instalacji wymaga osobnego przeglądu.
- Realne font/style mapowanie, łamanie linii i rozmiary okien.
- Zgodność patcha, save migration i osiągnięć; runtime na docelowym Windowsie.
- Czy użytkownik ma Season 2/3 poza przesłanym manifestem Season 1.
