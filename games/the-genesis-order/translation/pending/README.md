# Teksty oczekujące na decyzję

Ten katalog **nie jest** częścią `translation/drafts/`. Leżą tu gotowe polskie zwrotki, których nie da się zapisać jako poprawny draft przy obowiązującej sygnaturze markup v1.

## Dlaczego osobno

`apply_translation.validate_record` porównuje listę tokenów źródła i tłumaczenia. Tokenizer v1 (`export_translation.TOKEN_RE`) traktuje `\<słowo>` jako tag razem z opcjonalnym argumentem w nawiasach, więc tag bez argumentu zapisany bezpośrednio przed tekstem — `\fbCraft this item?` — jest zapamiętany jako jeden token `\fbCraft`. Każda polska wersja, np. `\fbWytworzyć przedmiot?`, daje token `\fb` i jest odrzucana jako „Markup/token mismatch”.

Dotknięte są **94 rekordy** kategorii `native_message` na mapie `Crafting` (Map 46): po 47 wystąpień „Craft this item?” i „You have items missing from this recipe.”. W całym eksporcie 45 229 rekordów to jedyne miejsce, w którym sygnatura v1 różni się od proponowanej v2 (`tools/markup_signature.py`).

## Zawartość

| Plik | Rekordy | Stan |
|---|---:|---|
| `crafting-ui-map46-01.jsonl` | 94 | polskie zwrotki autorskie (LLM, kontekst sceny craftingu); walidują się w sygnaturze v2, **odrzucane** przez v1 |

## Warunek przeniesienia do `drafts/`

1. Właściciel zatwierdza ADR 002 (`docs/ADR.md`) — jawna lista tagów bez argumentu, na razie wyłącznie `\fb`.
2. Powstaje sygnatura v2: albo eksport v2 z przeliczonym `markup_tokens` dla tych 94 rekordów, albo udokumentowana reguła walidatora dla tagów bez argumentu.
3. Plik zostaje przeniesiony do `translation/drafts/` i przechodzi pełny `validate_record` oraz testy.

Do tego czasu **nie wolno** wpisywać tych zwrotek do `drafts/` ani rozluźniać walidatora po cichu — test `tests/test_markup_signature.py` celowo sprawdza, że v1 nadal je odrzuca.

## Walidacja

```bash
python3 games/the-genesis-order/tools/markup_signature.py
python3 -m unittest games/the-genesis-order/tests/test_markup_signature.py -v
```
