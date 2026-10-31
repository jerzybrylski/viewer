# Fragmenty Czytanki z wstawkami wideo (TGO1–TGO12)

Fragmenty dostarczone przez właściciela projektu leżą na Google Drive
w `TGO/dostawy/` (folder `1OzLwZyMo4ygfNFI6U_g9HGvU9Xnwh7WF`). Są to autorskie
cięcia dużego skryptu `reading/v1/chronological_script_PL.md`: kolejne odcinki
czytania, w których właściciel zostawił tylko kwestie dialogowe, a nagłówki
`## ...` wskazują, z którego epizodu pliku matki pochodzi dany blok.

Ten katalog zawiera:

| Ścieżka | Zawartość |
|---|---|
| `source/` | pliki dokładnie w postaci dostarczonej (12 plików `.txt`, bez zmian) |
| `v1/` | te same pliki z wstawionymi znacznikami `> **🎬 Wstawka wideo:** ...` |
| `../../translation/reports/tgo_reading_fragments_video_v1.json` | raport przebiegu: bloki, dopasowania, wstawki, kwestie spoza pliku matki |

Nazwy plików zachowano 1:1 z dostawą — dlatego obok `TGO1.txt`…`TGO6.txt`
i `TGO10.txt`…`TGO12.txt` leżą `TG7.txt`, `TG8.txt`, `TG9.txt`. Kolejność
czytania wynika z numeru w nazwie, nie z nazwy prefiksu.

## Co zostało zrobione

`tools/annotate_reading_fragments.py` dopasowuje każdy blok fragmentu do epizodu
pliku matki i wstawia w te same miejsca znaczniki wstawek wideo w konwencji
pliku matki (`> **🎬 Wstawka wideo:** \`plik.mp4\`` z dopiskiem `(zapętlone)`,
gdy klip jest zapętlony).

Zasady, które narzędzie stosuje:

- **Nagłówek to kotwica.** `## Mapa 033 — Wschodnie skrzydło / event 18 / strona 1`
  wskazuje epizod o tej samej nazwie w pliku matce (wszystkie 92 nagłówki z 12
  plików występują tam dokładnie raz).
- **Kwestie porównywane są po normalizacji** (białe znaki, cudzysłowy, myślniki,
  wielokropek) przez `difflib.SequenceMatcher`; kolejność kwestii musi się zgadzać.
- **Znacznik trafia tylko tam, gdzie stoi w pliku matce** — między dwiema
  dopasowanymi kwestiami albo między nagłówkiem epizodu a pierwszą kwestią.
  W tej dostawie **każda z 72 wstawek** stoi między dwiema *sąsiednimi* kwestiami
  pliku matki (żadna nie przeskakuje pominiętych linii).
- **Treść użytkownika jest nietykalna.** Kwestie, których nie ma w pliku matce
  (własne redakcje, opcje wyboru, linie pisane ręcznie), zostają bez zmian i są
  wypisane w raporcie. Nie są zgadywane ani „poprawiane”.
- **Format pliku bez zmian:** styl zakończeń linii (wszystkie 12 plików to CRLF),
  kolejność i treść linii. Dodawane są wyłącznie linie znaczników wraz z pustymi
  liniami, których wymaga Markdown (blok cytatu musi być osobnym akapitem).

## Wynik

12 plików, 105 bloków (93 z nagłówkiem + 12 preambuł), 1 829 kwestii
(1 765 dopasowanych), **72 wstawki wideo**, 64 kwestie spoza pliku matki:
27 w ogóle nie występuje w matce (własne redakcje i opcje wyboru), a 37
występuje w *innych* epizodach — to linie NPC/„gadki” przeniesione przez
redakcję do sceny. Sprawdzono każdą z nich: tylko jedna („Co się stało?” w scenie
Judy) powtarza się także w epizodach ze wstawkami, ale w tym kontekście nie ma
wideo — żaden znacznik nie został przez to pominięty.

| plik | bloki | kwestie | dopasowane | wstawki | kwestie spoza matki |
|---|---:|---:|---:|---:|---:|
| `TGO1.txt` | 7 | 68 | 68 | 1 | 0 |
| `TGO2.txt` | 10 | 212 | 196 | 3 | 16 |
| `TGO3.txt` | 5 | 65 | 64 | 4 | 1 |
| `TGO4.txt` | 6 | 78 | 76 | 5 | 2 |
| `TGO5.txt` | 5 | 83 | 83 | 3 | 0 |
| `TGO6.txt` | 8 | 107 | 102 | 4 | 5 |
| `TG7.txt` | 13 | 320 | 316 | 3 | 4 |
| `TG8.txt` | 10 | 177 | 157 | 2 | 20 |
| `TG9.txt` | 10 | 190 | 188 | 16 | 2 |
| `TGO10.txt` | 7 | 176 | 173 | 15 | 3 |
| `TGO11.txt` | 13 | 263 | 258 | 16 | 5 |
| `TGO12.txt` | 11 | 90 | 84 | 0 | 6 |

`TGO12.txt` jest bajt w bajt identyczny ze źródłem — **żaden z 10 epizodów tego
fragmentu nie ma w pliku matce wstawki wideo** (sprawdzone w matce, nie założone).

Kontrola jakości: dla bloków w pełni pokrywających epizod plik matki i plik
wynikowy są zgodne w 90–100% (mediana podobieństwa 0,94 dla wszystkich 93
bloków); rozbieżności to wyłącznie redakcje właściciela (np. „Jak zawsze piękny.”
w miejscu matczynego „piękna.”).

## Regeneracja

```bash
python3 games/the-genesis-order/tools/annotate_reading_fragments.py \
  --master games/the-genesis-order/reading/v1/chronological_script_PL.md \
  --fragments games/the-genesis-order/reading/fragments/source \
  --out /tmp/fragments-v1 \
  --report /tmp/tgo_reading_fragments_video_v1.json
```

Narzędzie odmawia pracy, gdy katalog wyjściowy albo raport już istnieją
(ochrona przed nadpisaniem), i nigdy nie modyfikuje plików wejściowych.

## Ograniczenia

- Dopasowanie jest statyczne — nie ocenia warunków w grze ani nie odtwarza
  kolejności runtime. Wstawki w scenach, których fragment nie zawiera, nie
  pojawiają się (nie ma czego oznaczać).
- Jeśli właściciel celowo pominął kwestię, a wstawka stała w pliku matce między
  dwiema pozostawionymi kwestiami, znacznik **zostaje** — wstawka wydarzyła się
  w tym miejscu historii. W tej dostawie taki przypadek nie występuje.
- Znaczniki spoza pliku matki nie są tworzone: żadna nazwa pliku wideo nie jest
  dopisywana „z pamięci”.
