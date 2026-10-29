#!/usr/bin/env python3
"""Safe local installer/rollback for the TGO Polish proof-of-concept patch.

The game is never bundled. Source fingerprints are checked before any writes,
and every changed file is backed up before the first replacement.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parent
PAYLOAD = ROOT / "payload"
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
from apply_translation import apply_records, read_jsonl_files, validate_record  # noqa: E402

PATCH_MANIFEST = PAYLOAD / "patch_manifest.json"
TRANSLATIONS = PAYLOAD / "translations.jsonl"
FINGERPRINTS = PAYLOAD / "source_fingerprints.json"
STATE_NAME = ".tgo-pl-patch-state.json"
BACKUP_DIR_NAME = ".tgo-pl-originals"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".{os.getpid()}.tmp")
    data = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    with temporary.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def load_package() -> tuple[dict[str, Any], dict[str, str], list[dict[str, Any]]]:
    manifest = json.loads(PATCH_MANIFEST.read_text(encoding="utf-8"))
    fingerprints = json.loads(FINGERPRINTS.read_text(encoding="utf-8"))
    if manifest.get("schema") != "tgo-standalone-patch-v1":
        raise ValueError("Nieobsługiwany format manifestu patcha.")
    if not isinstance(fingerprints, dict) or not fingerprints:
        raise ValueError("Brak manifestu hashy źródłowych.")
    if sha256_file(TRANSLATIONS) != manifest.get("translations_sha256"):
        raise ValueError("Payload tłumaczeń jest uszkodzony lub zmieniony (SHA-256 nie pasuje).")
    if sha256_file(FINGERPRINTS) != manifest.get("fingerprints_sha256"):
        raise ValueError("Manifest hashy jest uszkodzony lub zmieniony (SHA-256 nie pasuje).")
    if manifest.get("source_file_count") != len(fingerprints):
        raise ValueError("Liczba plików w manifeście hashy nie zgadza się.")
    if manifest.get("translated_record_count", 0) < 1:
        raise ValueError("Paczka nie zawiera tłumaczeń.")
    rows = read_jsonl_files([TRANSLATIONS])
    if len(rows) != manifest["translated_record_count"]:
        raise ValueError("Liczba rekordów payloadu nie zgadza się z manifestem.")
    seen: set[str] = set()
    for row in rows:
        if row.get("id") in seen:
            raise ValueError(f"Powtórzone ID w payloadzie: {row.get('id')}")
        seen.add(row.get("id"))
        validate_record(row, require_complete=True)
    return manifest, fingerprints, rows


def game_file(install_root: Path, source_rel: str) -> tuple[Path, str]:
    """Map export paths to a normal RPG Maker MV install's www/ layout."""
    pure = PurePosixPath(source_rel)
    if pure.is_absolute() or ".." in pure.parts or not pure.parts:
        raise ValueError(f"Niebezpieczna ścieżka źródłowa: {source_rel}")
    if pure.parts[0] == "data":
        target_rel = (PurePosixPath("www") / pure).as_posix()
    elif pure.parts[0] == "www":
        target_rel = pure.as_posix()
    else:
        raise ValueError(f"Nieobsługiwana ścieżka źródłowa: {source_rel}")
    target = (install_root / Path(*PurePosixPath(target_rel).parts)).resolve()
    root = install_root.resolve()
    if target != root and root not in target.parents:
        raise ValueError(f"Ścieżka wychodzi poza katalog gry: {source_rel}")
    return target, target_rel


def verify_install(install_root: Path, fingerprints: dict[str, str]) -> dict[str, Path]:
    if not install_root.is_dir():
        raise FileNotFoundError(f"Nie znaleziono folderu gry: {install_root}")
    for marker in (install_root / "www" / "index.html", install_root / "www" / "data" / "System.json"):
        if not marker.is_file():
            raise ValueError(f"To nie wygląda na katalog instalacji TGO — brak {marker.relative_to(install_root)}")
    verified: dict[str, Path] = {}
    mismatches = []
    missing = []
    for source_rel, expected in fingerprints.items():
        if not isinstance(source_rel, str) or not isinstance(expected, str) or len(expected) != 64:
            raise ValueError("Nieprawidłowy wpis w manifeście fingerprintów.")
        path, _ = game_file(install_root, source_rel)
        if not path.is_file():
            missing.append(source_rel)
            continue
        actual = sha256_file(path)
        if actual != expected:
            mismatches.append((source_rel, expected, actual))
        else:
            verified[source_rel] = path
    if missing or mismatches:
        lines = ["Wersja/źródła gry nie pasują do tej paczki; niczego nie zmieniono."]
        if missing:
            lines.append("Brakujące pliki: " + ", ".join(missing[:12]))
        if mismatches:
            lines.append("Niezgodne hashe (plik: oczekiwany / znaleziony):")
            lines.extend(f"  {rel}: {expected} / {actual}" for rel, expected, actual in mismatches[:12])
        if len(missing) + len(mismatches) > 12:
            lines.append("Lista ucięta; sprawdź, czy to nie inny build lub zmodowana instalacja.")
        raise ValueError("\n".join(lines))
    return verified


def _write_backup(backup: Path, source: Path, expected_hash: str) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    if backup.exists():
        if sha256_file(backup) != expected_hash:
            raise ValueError(f"Istniejąca kopia zapasowa ma inny hash; nie nadpisuję: {backup}")
        return
    data = source.read_bytes()
    if sha256_bytes(data) != expected_hash:
        raise ValueError(f"Źródło zmieniło się podczas przygotowania kopii: {source}")
    with backup.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    shutil.copystat(source, backup)


def install(install_path: Path) -> dict[str, Any]:
    manifest, fingerprints, rows = load_package()
    install_root = install_path.expanduser().resolve()
    state_path = install_root / STATE_NAME
    old_state = None
    if state_path.exists():
        old_state = json.loads(state_path.read_text(encoding="utf-8"))
        if old_state.get("patch_version") != manifest["patch_version"]:
            raise ValueError("Znaleziono stan innej wersji patcha; użyj jego narzędzia cofania najpierw.")
        if old_state.get("status") == "installed":
            patched_sources = {entry["source_rel"]: entry["output_sha256"] for entry in old_state.get("files", [])}
            mismatches = []
            for source_rel, source_hash in fingerprints.items():
                target, target_rel = game_file(install_root, source_rel)
                expected = patched_sources.get(source_rel, source_hash)
                actual = sha256_file(target) if target.is_file() else "MISSING"
                if actual != expected:
                    mismatches.append(target_rel)
            if mismatches:
                raise ValueError("Stan mówi, że patch jest zainstalowany, ale pliki uległy zmianie; nie nadpisuję: " + ", ".join(mismatches[:12]))
            return {"status": "already_installed", "files": len(old_state.get("files", []))}
        if old_state.get("status") != "rolled_back":
            raise ValueError("Poprzednia instalacja jest niedokończona. Uruchom COFNIJ.bat albo przywróć backupy ręcznie.")
    verified = verify_install(install_root, fingerprints)

    with tempfile.TemporaryDirectory(prefix=".tgo-pl-stage-", dir=install_root) as temp_name:
        temp_root = Path(temp_name)
        source_shadow = temp_root / "source"
        stage_out = temp_root / "patched"
        source_rels = sorted({row["source"]["file"] for row in rows})
        for rel in source_rels:
            target = verified.get(rel)
            if target is None:
                raise ValueError(f"Fingerprint pliku używanego przez tłumaczenie nie został zweryfikowany: {rel}")
            shadow = source_shadow / Path(*PurePosixPath(rel).parts)
            shadow.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(target, shadow)
        report = apply_records([TRANSLATIONS], source_shadow, stage_out, check_only=False, require_complete=True)
        candidates = []
        output_map = report["changed_files"]
        for rel, details in sorted(output_map.items()):
            if details["source_sha256"] == details["output_sha256"]:
                continue
            source = verified[rel]
            staged = stage_out / Path(*PurePosixPath(rel).parts)
            target, target_rel = game_file(install_root, rel)
            if sha256_file(source) != details["source_sha256"]:
                raise ValueError(f"Plik zmienił się po preflight: {target_rel}")
            candidates.append({
                "source_rel": rel,
                "target_rel": target_rel,
                "source_sha256": details["source_sha256"],
                "output_sha256": details["output_sha256"],
                "staged": staged,
                "target": target,
                "backup": install_root / BACKUP_DIR_NAME / manifest["patch_version"] / Path(*PurePosixPath(target_rel).parts),
            })
        if not candidates:
            return {"status": "no_changes", "files": 0}

        state_files = [
            {key: value for key, value in item.items() if key in {"source_rel", "target_rel", "source_sha256", "output_sha256"}}
            for item in candidates
        ]
        state = {
            "schema": "tgo-patch-state-v1",
            "patch_version": manifest["patch_version"],
            "status": "installing",
            "installed_at_utc": datetime.now(timezone.utc).isoformat(),
            "files": state_files,
        }
        for item in candidates:
            _write_backup(item["backup"], item["target"], item["source_sha256"])
        atomic_json(state_path, state)
        replaced = []
        try:
            for item in candidates:
                target: Path = item["target"]
                if sha256_file(target) != item["source_sha256"]:
                    raise ValueError(f"Plik zmienił się tuż przed zapisem; przerwano: {item['target_rel']}")
                if sha256_file(item["staged"]) != item["output_sha256"]:
                    raise ValueError(f"Hash pliku stagingowego nie zgadza się: {item['target_rel']}")
                os.replace(item["staged"], target)
                replaced.append(item)
            state["status"] = "installed"
            state["installed_at_utc"] = datetime.now(timezone.utc).isoformat()
            atomic_json(state_path, state)
        except Exception:
            restore_errors = []
            for item in reversed(replaced):
                try:
                    backup_data = item["backup"].read_bytes()
                    if sha256_bytes(backup_data) != item["source_sha256"]:
                        raise ValueError("backup SHA-256 mismatch")
                    restore_tmp = item["target"].with_name(item["target"].name + ".tgo-restore.tmp")
                    restore_tmp.write_bytes(backup_data)
                    os.replace(restore_tmp, item["target"])
                except Exception as error:  # retain installing state for recovery
                    restore_errors.append(f"{item['target_rel']}: {error}")
            if restore_errors:
                state["status"] = "repair_required"
                state["restore_errors"] = restore_errors
                atomic_json(state_path, state)
            else:
                state_path.unlink(missing_ok=True)
            raise
    return {"status": "installed", "files": len(candidates), "translations": len(rows), "state": str(state_path)}


def rollback(install_path: Path) -> dict[str, Any]:
    install_root = install_path.expanduser().resolve()
    state_path = install_root / STATE_NAME
    if not state_path.is_file():
        raise FileNotFoundError(f"Nie znaleziono stanu patcha: {state_path}")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if state.get("schema") != "tgo-patch-state-v1":
        raise ValueError("Nieobsługiwany format stanu patcha.")
    if state.get("status") == "rolled_back":
        return {"status": "already_rolled_back", "files": len(state.get("files", []))}
    if state.get("status") not in {"installed", "installing", "repair_required"}:
        raise ValueError("Brak rozpoznanego stanu instalacji; nie wykonuję cofnięcia automatycznego.")

    backup_root = install_root / BACKUP_DIR_NAME / state["patch_version"]
    verified = []
    for entry in state.get("files", []):
        target_rel = entry.get("target_rel", "")
        pure = PurePosixPath(target_rel)
        if pure.is_absolute() or ".." in pure.parts:
            raise ValueError(f"Niebezpieczna ścieżka w stanie patcha: {target_rel}")
        target = (install_root / Path(*pure.parts)).resolve()
        if install_root not in target.parents:
            raise ValueError(f"Ścieżka cofania wychodzi poza instalację: {target_rel}")
        backup = (backup_root / Path(*pure.parts)).resolve()
        if backup_root.resolve() not in backup.parents:
            raise ValueError(f"Ścieżka backupu wychodzi poza katalog backupów: {target_rel}")
        if not target.is_file():
            raise ValueError(f"Bieżący plik zniknął; nie mogę go bezpiecznie cofnąć: {target_rel}")
        current_hash = sha256_file(target)
        if current_hash not in {entry["source_sha256"], entry["output_sha256"]}:
            raise ValueError(f"Bieżący plik zmienił się od instalacji; nie nadpisuję go: {target_rel}")
        if not backup.is_file() or sha256_file(backup) != entry["source_sha256"]:
            raise ValueError(f"Backup jest brakujący lub uszkodzony; nie przywracam: {target_rel}")
        verified.append((target_rel, target, backup, entry["source_sha256"], current_hash == entry["output_sha256"]))

    for target_rel, target, backup, expected_hash, needs_restore in verified:
        if not needs_restore:
            continue
        tmp = target.with_name(target.name + ".tgo-restore.tmp")
        shutil.copyfile(backup, tmp)
        if sha256_file(tmp) != expected_hash:
            raise ValueError(f"Nie udało się zweryfikować przywracanego pliku: {target_rel}")
        os.replace(tmp, target)
    state["status"] = "rolled_back"
    state["rolled_back_at_utc"] = datetime.now(timezone.utc).isoformat()
    atomic_json(state_path, state)
    return {"status": "rolled_back", "files": len(verified), "backups_kept": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("apply", "rollback"))
    parser.add_argument("game_folder", type=Path, help="folder containing www/index.html")
    args = parser.parse_args()
    result = install(args.game_folder) if args.action == "apply" else rollback(args.game_folder)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] == "installed":
        print("Patch zastosowany; kopie oryginałów pozostawiono w .tgo-pl-originals. Zamknij grę przed każdym użyciem patchera.")
    elif result["status"] == "rolled_back":
        print("Oryginały przywrócone i zweryfikowane; kopie zapasowe pozostają na miejscu.")
    else:
        print("Operacja zakończona bez błędów.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"BŁĄD: {error}", file=sys.stderr)
        raise SystemExit(2)
