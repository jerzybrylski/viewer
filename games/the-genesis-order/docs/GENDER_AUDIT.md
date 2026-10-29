# Audyt rodzaju gramatycznego — PL

Raport generuje `tools/fix_grammatical_gender.py`. Podstawą jest płeć mówcy
(pierwsza osoba) i płeć adresata ustalona z jednorodnej obsady sceny (druga osoba).

- Tłumaczone rekordy: **39 917**.
- Rekordy zmienione: **593**.

## Rodzaje zmian

| Kategoria | Liczba |
|---|---:|
| pierwsza_osoba_czasownik | 450 |
| druga_osoba_czasownik | 107 |
| 1_osoba_orzecznik | 53 |
| 1_osoba_warunkowy | 21 |
| 2_osoba_orzecznik | 9 |
| 2_osoba_warunkowy | 5 |
| zaimek_sam | 1 |

## Czego narzędzie nie rozstrzyga

- Kwestie bez znanego mówcy z pierwszą osobą: **143**.
- Druga osoba bez jednoznacznego adresata: **589**.
- Kwestie z „sam/sama” do ręcznego przeglądu: **130**.
- Zdania z zaimkiem 3. osoby i czasownikiem na „-ł” (próbka): **20**.

Pełne listy są w `translation/reports/gender_fix_v1.json` w sekcji `residual`.

## Zasady

- **Pierwsza osoba** — forma przyjmuje płeć mówcy z `custom_header` (ta sama mapa kodów co w Czytance).
- **Druga osoba** — forma przyjmuje płeć adresata tylko wtedy, gdy wszyscy pozostali mówcy sceny o znanej płci są jednej płci.
- **Tryb warunkowy** — `bym/byś` + czasownik przyjmuje płeć mówcy (1. os.) albo adresata (2. os.); formy 2. osoby nie są nigdy liczone płcią mówcy.
- **Trzecia osoba** — nie ruszana automatycznie: podmiot bywa domyślny, a zgadywanie coreferencji wprowadzałoby błędy. Wymaga przeglądu w grze.
- **„sam/sama”** — tylko w tym samym zdaniu, w którym zmieniono czasownik mówcy; samodzielnie rodzaj zależy od podmiotu, nie od mówcy (`ten sam problem`, `sama pani komisarz`).
- Rzeczowniki w narzędniku (`kościołem`, `ciałem`) i czas teraźniejszy (`działam`) są wyłączone z podmiany.

## Pełny dziennik

Każdą zmianę (przed/po, mówca, adresat, podstawa) zawiera `translation/reports/gender_fix_v1.json`.
