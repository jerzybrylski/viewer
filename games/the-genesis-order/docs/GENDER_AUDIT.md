# Audyt rodzaju gramatycznego — TGO PL

> Plik generuje `tools/fix_grammatical_gender.py`. Narzędzie nie tłumaczy:
> przywraca zgodność rodzaju z mówcą (pierwsza osoba) i z adresatem (druga osoba),
> a wszystko, czego nie da się rozstrzygnąć bez sceny, odkłada do listy reszty.

## Podsumowanie

- Rekordy zmienione: **618**.
- Zmienione formy: **679**.

## Rodzaje zmian

| Wzorzec | Zmiany |
|---|---:|
| pierwsza osoba — czasownik (przeszły) | 450 |
| druga osoba — czasownik (przeszły) | 107 |
| pierwsza osoba — orzecznik przymiotnikowy | 86 |
| pierwsza osoba — tryb warunkowy (`bym`) | 21 |
| druga osoba — orzecznik przymiotnikowy | 9 |
| druga osoba — tryb warunkowy (`byś`) | 5 |
| zaimek `sam/sama` w zdaniu mówcy | 1 |

## Reszta do przeglądu w grze

| Klasa | Rekordy | Dlaczego nie automatycznie |
|---|---:|---|
| `bez_znanego_mowcy_z_pierwsza_osoba` | 169 | brak mówcy w źródle — nie zgadujemy płci |
| `druga_osoba_bez_jednoznacznego_adresata` | 2122 | adresat nie wynika ze zdania (brak wołacza i 1Hero) |
| `sam_sama_do_recznego_przegladu` | 192 | „sam/sama” odnosi się do podmiotu, nie do mówcy |
| `trzecia_osoba_do_przegladu_w_grze` | 50 | imię kobiety lub „ona” w pobliżu formy męskiej — do oceny w scenie |

## Przykłady

- **Melissa**: „Chciałem zadać pani kilka pytań.” → „Chciałam zadać pani kilka pytań.”
- **Mox**: „Co!? Nie… Rozmawiałam z właścicielką sklepu…” → „Co!? Nie… Rozmawiałem z właścicielką sklepu…”
- **Mox**: „Z tego, co słyszałam, to Madalyn była opętana.” → „Z tego, co słyszałem, to Madalyn była opętana.”
- **Mox**: „Gdybym cię nie znała, pomyślałabym, że próbujesz mi zaimponować.” → „Gdybym cię nie znała, pomyślałbym, że próbujesz mi zaimponować.”
- **Ella**: „Naprawdę? Jesteś taka młoda. Nie masz konta na Lustagramie?” → „Naprawdę? Jesteś taki młody. Nie masz konta na Lustagramie?”
- **Mox**: „Mam uwierzyć, że znalazłeś skradziony artefakt i nie wiedziałeś, że handlujesz trefnym towarem?” → „Mam uwierzyć, że znalazłaś skradziony artefakt i nie wiedziałaś, że handlujesz trefnym towarem?”
- **Mox**: „Gdybym miała zgadywać… a zwykle dobrze mi to wychodzi…” → „Gdybym miał zgadywać… a zwykle dobrze mi to wychodzi…”
- **Hannah**: „Mógłbym się do tego przyzwyczaić, 1Hero.” → „Mógłabym się do tego przyzwyczaić, 1Hero.”

## Zasady

- **Pierwsza osoba** — czasownik i orzecznik przymiotnikowy biorą rodzaj mówcy
  ustalonego z `custom_header` (ta sama mapa kodów co w Czytance).
- **Druga osoba** — tylko z dowodem w zdaniu: wołacz z imieniem albo zwrot do `1Hero`.
  Sama obsada sceny nie wystarcza — mówca może zwracać się do kogoś bez kwestii.
- **Trzecia osoba** — nie ruszana automatycznie; podmiot bywa domyślny, a zgadywanie
  coreferencji wprowadzałoby nowe błędy.
- Orzecznik przymiotnikowy zmieniamy tylko wtedy, gdy żaden rzeczownik nim nie rządzi
  („jestem jedyną osobą” zostaje); lista par przymiotnikowych jest zamknięta i przeglądana.
- Rzeczowniki w narzędniku (`kościołem`, `aniołem`) i orzeczniki rzeczownikowe
  (`komisarzem`, `wrogiem`) zachowują własny rodzaj.

## Pełny dziennik

Każdą zmianę (przed/po, mówca, adresat, podstawa) zawiera
`translation/reports/gender_fix_v1.json`.
