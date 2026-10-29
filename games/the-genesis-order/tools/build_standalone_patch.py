#!/usr/bin/env python3
"""Build a standalone, game-free TGO patch ZIP from the reconciled draft corpus."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

from audit_translation_coverage import audit_translation
from merge_translation_batches import merge_batches

ROOT = Path(__file__).resolve().parents[1]
TRANSLATION = ROOT / "translation"
DRAFTS = TRANSLATION / "drafts"
CANONICAL = TRANSLATION / "export-v1"
PACKAGE_SOURCE = ROOT / "patcher"
TOOLS_SOURCE = ROOT / "tools"
DEFAULT_OUTPUT = TRANSLATION / "packages" / "TGO_PL_translation_patch_POC_v0.1.1.zip"
BUNDLED_TOOLS = (
    "apply_translation.py",
    "export_translation.py",
    "build_source_manifest.py",
    "scan_js_text_candidates.py",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_fingerprints() -> dict[str, str]:
    fingerprints: dict[str, str] = {}
    for path in sorted(CANONICAL.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            rel = row["source"]["file"]
            digest = row["source"]["sha256"]
            prior = fingerprints.setdefault(rel, digest)
            if prior != digest:
                raise ValueError(f"Canonical export has conflicting source hashes for {rel}")
    return fingerprints


def build(output: Path) -> dict[str, object]:
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    sha_path = output.with_suffix(output.suffix + ".sha256")
    if output.exists() or sha_path.exists():
        raise FileExistsError(f"Refusing to overwrite package or hash: {output}")
    if not PACKAGE_SOURCE.is_dir():
        raise FileNotFoundError(PACKAGE_SOURCE)
    for name in ("patcher.py", "APPLY.bat", "COFNIJ.bat", "README_PL.md"):
        if not (PACKAGE_SOURCE / name).is_file():
            raise FileNotFoundError(PACKAGE_SOURCE / name)
    for name in BUNDLED_TOOLS:
        if not (TOOLS_SOURCE / name).is_file():
            raise FileNotFoundError(TOOLS_SOURCE / name)

    fingerprints = canonical_fingerprints()
    coverage = audit_translation(CANONICAL, DRAFTS)
    if coverage["status"] != "complete":
        unresolved = coverage["unresolved_records"]
        raise ValueError(f"Translation coverage is incomplete: {len(unresolved)} unresolved records")
    with tempfile.TemporaryDirectory(prefix="tgo-patch-build-", dir=TRANSLATION) as work_name:
        work = Path(work_name)
        merged = work / "merged.jsonl"
        batches = sorted(DRAFTS.rglob("*.jsonl"))
        report = merge_batches(CANONICAL, batches, merged, TRANSLATION)
        translated = []
        with merged.open(encoding="utf-8") as src:
            for line in src:
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("translation", "").strip():
                    translated.append(row)
        if len(translated) != report["with_translation"]:
            raise ValueError("Translated record count does not match merge report")

        stage = work / "package"
        root_name = "TGO_PL_translation_patch_POC_v0.1.1"
        package = stage / root_name
        payload = package / "payload"
        tools = package / "tools"
        payload.mkdir(parents=True)
        tools.mkdir(parents=True)
        for name in ("patcher.py", "APPLY.bat", "COFNIJ.bat", "README_PL.md"):
            shutil.copyfile(PACKAGE_SOURCE / name, package / name)
        for name in BUNDLED_TOOLS:
            shutil.copyfile(TOOLS_SOURCE / name, tools / name)

        translations_path = payload / "translations.jsonl"
        with translations_path.open("w", encoding="utf-8", newline="\n") as stream:
            for row in translated:
                stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        fingerprints_path = payload / "source_fingerprints.json"
        fingerprints_path.write_text(
            json.dumps(fingerprints, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        coverage_path = payload / "translation_coverage.json"
        coverage_path.write_text(
            json.dumps(coverage, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        manifest = {
            "schema": "tgo-standalone-patch-v1",
            "patch_version": "0.1.1-poc",
            "title": "The Genesis Order — Polish translation proof of concept",
            "product_build": "unconfirmed; exact source fingerprints required",
            "engine": "RPG Maker MV / NW.js (engine version 1.6.1 observed; product build not confirmed)",
            "translated_record_count": len(translated),
            "draft_batch_count": len(batches),
            "canonical_record_count": report["records"],
            "protected_record_count": report["protected"],
            "source_preserved_nonlocalized_record_count": coverage["source_preserved_nonlocalized_record_count"],
            "source_preserved_nonlocalized_by_category": coverage["source_preserved_by_category"],
            "protected_records_by_category": coverage["explicitly_protected_by_category"],
            "pending_untranslated_record_count": coverage["unresolved_translatable_record_count"],
            "translation_coverage_status": coverage["status"],
            "source_file_count": len(fingerprints),
            "translations_sha256": sha256_file(translations_path),
            "fingerprints_sha256": sha256_file(fingerprints_path),
            "translation_coverage_sha256": sha256_file(coverage_path),
            "compatibility_policy": "All source files referenced by export-v1 must match their recorded SHA-256; otherwise the patcher refuses to modify the installation.",
            "game_files_included": False,
            "runtime_tested": False,
        }
        (payload / "patch_manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        readme = (package / "README_PL.md").read_text(encoding="utf-8")
        readme = readme.replace(
            "Paczka stosuje tłumaczenia TGO do **lokalnej kopii gry użytkownika**.",
            f"Paczka stosuje **{len(translated):,}** roboczych rekordów tłumaczenia TGO do **lokalnej kopii gry użytkownika**.".replace(",", " "),
        )
        (package / "README_PL.md").write_text(readme, encoding="utf-8", newline="\n")

        with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(package.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(stage).as_posix())
        with zipfile.ZipFile(output) as archive:
            bad = archive.testzip()
            if bad is not None:
                raise ValueError(f"ZIP CRC failure in {bad}")
            names = archive.namelist()
            if any("data.zip" in name or name.endswith("/www/data/System.json") for name in names):
                raise ValueError("Refusing to include game/source data in patch package")
        digest = sha256_file(output)
        sha_path.write_text(f"{digest}  {output.name}\n", encoding="ascii", newline="\n")
        return {
            "output": str(output),
            "sha256": digest,
            "size_bytes": output.stat().st_size,
            "translated_records": len(translated),
            "source_files_fingerprinted": len(fingerprints),
            "draft_batches": len(batches),
            "archive_entries": len(names),
            "game_files_included": False,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(build(args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
