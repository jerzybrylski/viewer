# Zasady lokalizacji — The Genesis Order

## Stan

Eksport źródłowy znajduje się w `games/the-genesis-order/translation/export-v1/`. Wszystkie pola `translation` są puste; **nie rozpoczęto tłumaczenia**. Pakiet źródłowy `TGO_source_translation_package_v1.zip` został zbudowany w ignorowanym `google_drive/the-genesis-order/translation/packages/`; patcher nie został zbudowany.

## Zasady wejściowe

- Tłumaczyć tylko rekordy z kanonicznego JSONL po ich `id`; nie zmieniać ID, `source_text`, hashy, locatorów ani kontekstu.
- Przed tłumaczeniem obejrzeć kategorię, warunki strony, gałąź, sąsiednie wybory i `visibility_evidence`. `confirmed_text_surface` dowodzi, że tekst jest widoczny, ale nie przesądza, czy to dialog, tutorial, komunikat, czy UI.
- Zachować dokładnie wszystkie tokeny w `markup_tokens`, placeholdery RPG Maker, kolejność escape’ów, znaczniki HTML i formaty. Nie dopisywać ani nie usuwać placeholderów bez osobnej reguły/testu.
- Rekordy z `context.translation_policy=keep_source_value` muszą zachować źródło dokładnie. Dotyczy to między innymi cen/markerów i wartości będących operandami runtime; importer odrzuci zmienioną wartość.
- Nazwy, tytuły, ksywki i terminy fabularne wymagają wspólnego glosariusza oraz zatwierdzonej konwencji zapisu. Nie zakładamy odmiany, rodzaju ani relacji bez kontekstu.
- Nie normalizować wielkości liter, interpunkcji, spacji lub apostrofów automatycznie. Puste źródłowe placeholdery layoutowe są pominięte w eksporcie.

## Walidacja i bezpieczeństwo

- JSONL jest kanoniczny. Markdown w `google_drive/the-genesis-order/translation/markdown-draft-v1/` jest widokiem roboczym po stabilnych ID, nie osobnym źródłem prawdy.
- Przed stagingiem uruchomić testy i `apply_translation.py --check`. Import/patch trafia do nowej kopii pod ignorowanym `google_drive/`; nigdy nie nadpisuje assetów wejściowych.
- Nie uruchamiać gry ani JS przez narzędzia ekstrakcji/importu. Test renderingu i polskich fontów wymaga osobnej zgody oraz kopii gry.
- Source ZIP v1 jest wygenerowany na prośbę właściciela i zawiera pełne, zweryfikowane statyczne źródła; nierozstrzygnięte podtypy pozostają jawne. Nie traktować go jako tłumaczenia, patcha ani finalnej dystrybucji. Finalny ZIP z tłumaczeniem/patcherem wymaga osobnej akceptacji.

Nie kopiować tekstów SRW ani założeń o silniku/limitach SRW do TGO. Przenosić można jedynie ogólne rozwiązania organizacyjne i walidacyjne.
