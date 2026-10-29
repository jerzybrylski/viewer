#!/usr/bin/env python3
"""Build a reviewable static-source ZIP from canonical TGO JSONL.

Only canonical JSONL, generated Markdown, and project documentation are packed.
Original game assets and google_drive source dumps are never included.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
EXPORT_ROOT = REPO_ROOT / "games" / "the-genesis-order" / "translation" / "export-v1"
SOURCE_ROOT = REPO_ROOT / "google_drive" / "the-genesis-order"
MARKDOWN_ROOT = REPO_ROOT / "games/the-genesis-order/translation/markdown-draft-v1"
PACKAGE_ROOT = REPO_ROOT / "games" / "the-genesis-order" / "translation" / "packages"
DEFAULT_OUT = PACKAGE_ROOT / "TGO_source_translation_package_v1.zip"
DOCS_ROOT = REPO_ROOT / "games" / "the-genesis-order" / "docs"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return data


def read_records(export_manifest: dict[str, Any]) -> tuple[int, Counter[str], Counter[str], Counter[str], Counter[int]]:
    record_count = 0
    categories: Counter[str] = Counter()
    classifications: Counter[str] = Counter()
    policies: Counter[str] = Counter()
    command_codes: Counter[int] = Counter()
    ids: set[str] = set()
    jsonl_names = export_manifest.get("jsonl_files", [])
    if not isinstance(jsonl_names, list) or not jsonl_names:
        raise ValueError("Export manifest has no JSONL file list")
    for name in jsonl_names:
        if not isinstance(name, str) or Path(name).name != name or not name.endswith(".jsonl"):
            raise ValueError(f"Unsafe JSONL entry in export manifest: {name!r}")
        path = EXPORT_ROOT / name
        if not path.is_file():
            raise FileNotFoundError(path)
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict) or row.get("schema") != "tgo-translation-record-v1":
                raise ValueError(f"Invalid record at {path}:{line_number}")
            row_id = row.get("id")
            if not isinstance(row_id, str) or row_id in ids:
                raise ValueError(f"Missing or duplicate record ID at {path}:{line_number}")
            ids.add(row_id)
            record_count += 1
            categories[row.get("category", "<missing>")] += 1
            classifications[row.get("classification", "<missing>")] += 1
            locator = (row.get("source") or {}).get("locator") or {}
            command_code = locator.get("command_code")
            if isinstance(command_code, int):
                command_codes[command_code] += 1
            policy = (row.get("context") or {}).get("translation_policy")
            if policy:
                policies[policy] += 1
    return record_count, categories, classifications, policies, command_codes


def readme_text(record_count: int, policies: Counter[str]) -> str:
    protected = policies.get("keep_source_value", 0)
    return f'''# The Genesis Order — pakiet źródłowy do tłumaczenia (v1)\n\n## Co zawiera\n\n- Kanoniczne JSONL ze stabilnymi ID, tekstem źródłowym, kontekstem i pustym polem `translation`.\n- Kontekstowy Markdown dla map i Common Events; zachowuje gałęzie i kolejność źródłową.\n- Glosariusz roboczy, zasady workflow oraz raport zakresu.\n\nTo pełny pakiet statycznie wyodrębnionych, potwierdzonych powierzchni tekstu według audytu z 2026-10-29. Nie jest patchem gry i nie zawiera oryginalnych assetów, mediów, zapisów ani kodu gry.\n\n## Jak wprowadzać tłumaczenia\n\n1. W Markdown edytuj wyłącznie wartość po `TGO-TRANSLATION:`. Albo pracuj w JSONL i zmieniaj wyłącznie pole `translation`.\n2. Nie zmieniaj `id`, `source_text`, `source`, hashy, locatorów, `context`, `structure` ani `markup_tokens`.\n3. Zachowaj wszystkie tokeny/escape’y w `markup_tokens` dokładnie i w tej samej kolejności.\n4. Rekordy z `context.translation_policy=keep_source_value` są zablokowane. W pakiecie chronionych jest {protected} wartości; pozostaw tłumaczenie puste lub równe źródłu.\n5. Przekaż z powrotem komplet zmodyfikowanych plików albo JSONL wraz z ich ID. Nie pomijaj żadnych rekordów tekstu gracza.\n\n## Ważne ograniczenia kontekstu\n\n- Pakiet zawiera **{record_count:,} rekordów** wyeksportowanych według jawnych reguł i coverage checks. Odczytuj kategorię oraz kontekst rekordu; nie każdy widoczny tekst jest dialogiem, a niezweryfikowanych literałów nie klasyfikuj jako UI. Źródłowy język nie został formalnie potwierdzony, choć wiele wpisów wygląda na angielskie. Językiem docelowym projektu jest polski.\n- Wszystkie **2 110 opcji** w 695 grupach i **1 513 nie-rendererowych wierszy `401`** są pełnoprawnymi tekstami widocznymi dla gracza i należą do zakresu tłumaczenia (1 122 wiadomości, 378 pozycji UI telefonu, 13 natywnych tekstów telefonu). To zatwierdzona decyzja zakresowa.\n- Markdown jest uporządkowany według źródeł, **nie** według kanonicznej chronologii fabuły. Czytaj warunki i branch path z kontekstu.\n- Zgodnie z decyzją właściciela tekst wtopiony w obrazy i wideo nie jest tłumaczony. Dynamiczne nazwy urządzeń/użytkowników dostarczane przez runtime również nie są statycznymi stringami gry.\n\nSzczegółowe liczniki i coverage checks są w `docs/COUNT_REPORT.md` oraz `translation/export-v1/export_manifest.json`. Nie uruchamiaj gry na podstawie tego pakietu.\n'''


def build(out: Path) -> dict[str, Any]:
    export_manifest_path = EXPORT_ROOT / "export_manifest.json"
    markdown_manifest_path = MARKDOWN_ROOT / "markdown_manifest.json"
    if not export_manifest_path.is_file() or not markdown_manifest_path.is_file():
        raise FileNotFoundError("Run export_translation.py and markdown_translation.py build first")
    export_manifest = load_json(export_manifest_path)
    markdown_manifest = load_json(markdown_manifest_path)
    if export_manifest.get("schema") != "tgo-translation-export-v1":
        raise ValueError("Unsupported TGO export manifest")
    if not export_manifest.get("coverage_checks_passed"):
        raise ValueError("Refusing to package an export with failed coverage checks")
    if markdown_manifest.get("schema") != "tgo-markdown-package-v1":
        raise ValueError("Unsupported TGO Markdown manifest")
    record_count, categories, classifications, policies, command_codes = read_records(export_manifest)
    if record_count != export_manifest.get("records"):
        raise ValueError("JSONL record count does not match export manifest")
    if command_codes.get(401, 0) != 1513 or command_codes.get(102, 0) != 2110:
        raise ValueError("Command 401/102 translation-scope counts do not match the approved export")
    if record_count != markdown_manifest.get("records"):
        raise ValueError("Markdown record count does not match canonical export")

    package_manifest = {
        "schema": "tgo-source-translation-package-v1",
        "package_status": "complete_static_translation_source_bundle_with_owner_approved_scope",
        "generated_on": "2026-10-29",
        "record_count": record_count,
        "jsonl_file_count": len(export_manifest["jsonl_files"]),
        "markdown_document_count": markdown_manifest["documents"],
        "markdown_record_count": markdown_manifest["records"],
        "source_file_count": len(export_manifest["source_file_hashes"]),
        "coverage_checks_passed": export_manifest["coverage_checks_passed"],
        "translation_policy_counts": dict(sorted(policies.items())),
        "category_counts": dict(sorted(categories.items())),
        "classification_counts": dict(sorted(classifications.items())),
        "player_facing_translation_scope": {
            "command_401_message_rows": command_codes.get(401, 0),
            "command_102_choice_options": command_codes.get(102, 0),
            "decision": "all_included_as_full_translatable_player_facing_text",
        },
        "embedded_image_and_video_text": "excluded_per_owner_decision",
        "original_game_assets_included": False,
        "game_code_included_or_executed": False,
    }
    readme = readme_text(record_count, policies)
    out = out.resolve()
    package_root = PACKAGE_ROOT.resolve()
    if out == package_root or package_root not in out.parents or out.suffix.lower() != ".zip":
        raise ValueError(f"Refusing to write package outside tracked package directory: {package_root}")
    out.parent.mkdir(parents=True, exist_ok=True)
    manifest_bytes = (json.dumps(package_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")

    temporary = out.with_name(out.name + ".tmp")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=6, allowZip64=True) as archive:
        archive.writestr("README_PL.md", readme)
        archive.writestr("PACKAGE_MANIFEST.json", manifest_bytes)
        for name in export_manifest["jsonl_files"]:
            archive.write(EXPORT_ROOT / name, f"translation/export-v1/{name}")
        archive.write(export_manifest_path, "translation/export-v1/export_manifest.json")
        generated_files = markdown_manifest.get("generated_files", [])
        if not isinstance(generated_files, list):
            raise ValueError("Invalid generated_files in Markdown manifest")
        for rel in generated_files:
            if not isinstance(rel, str) or Path(rel).is_absolute() or ".." in Path(rel).parts:
                raise ValueError(f"Unsafe Markdown path: {rel!r}")
            path = MARKDOWN_ROOT / rel
            if not path.is_file():
                raise FileNotFoundError(path)
            archive.write(path, (Path("translation/markdown-draft-v1") / rel).as_posix())
        archive.write(markdown_manifest_path, "translation/markdown-draft-v1/markdown_manifest.json")
        for name in ("GLOSSARY.md", "TRANSLATION_POLICY.md", "COUNT_REPORT.md", "STATUS.md"):
            source = DOCS_ROOT / name
            archive.write(source, f"docs/{name}")
        entry_count = len(archive.namelist())

    os.replace(temporary, out)
    with zipfile.ZipFile(out) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"ZIP integrity check failed at {bad}")
    digest = sha256_file(out)
    sidecar = out.with_suffix(out.suffix + ".sha256")
    sidecar.write_text(f"{digest}  {out.name}\n", encoding="ascii")
    return {
        "archive": str(out),
        "bytes": out.stat().st_size,
        "sha256": digest,
        "entries": entry_count,
        "records": record_count,
        "markdown_documents": markdown_manifest["documents"],
        "protected_values": policies.get("keep_source_value", 0),
        "coverage_checks_passed": export_manifest["coverage_checks_passed"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    report = build(args.out)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError, zipfile.BadZipFile) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
