#!/usr/bin/env python3
"""Znajdowanie instalacji The Genesis Order i zapamiętywanie wybranej ścieżki.

Patcher nie powinien wymagać przepisywania ścieżki z ręki. Ten moduł robi trzy
rzeczy, w tej kolejności:

1. **Pamięta** ostatnio użyty katalog gry (plik konfiguracji w profilu
   użytkownika) — kolejne instalacje i cofnięcia startują bez pytania.
2. **Szuka** instalacji sam: biblioteki Steam (`libraryfolders.vdf`), typowe
   katalogi gier na wszystkich dyskach, pulpit/pobrane użytkownika oraz
   katalog, z którego uruchomiono patcher.
3. **Pyta człowieka**, gdy automat nie ma jednoznacznej odpowiedzi: okno
   wyboru folderu (albo lista znalezionych instalacji).

Wszystko jest tylko do odczytu. Ten moduł nigdy nie modyfikuje plików gry —
decyduje wyłącznie o tym, *gdzie* patcher ma pracować.
"""
from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

CONFIG_SCHEMA = "tgo-patch-locator-config-v1"
ENV_CONFIG_PATH = "TGO_PATCH_CONFIG"
INSTALL_MARKERS = (("www", "index.html"), ("www", "data", "System.json"))
# Katalogi, których nie ma sensu przeszukiwać (system, cache, ogromne drzewa).
SKIP_DIR_NAMES = {
    "$recycle.bin", "system volume information", "windows", "winsxs", "appdata",
    "node_modules", "proc", "sys", "dev", "usr", "bin", "etc", "lib", "boot",
    ".git", "__pycache__", "recovery", "temp", "tmp",
}
NAME_HINTS = ("genesis", "tgo")


# --------------------------------------------------------------------------- #
# Rozpoznawanie instalacji
# --------------------------------------------------------------------------- #

def is_install_root(path: Path) -> bool:
    """Czy katalog wygląda na instalację TGO (szybki test, bez hashowania)?"""
    try:
        return all((path.joinpath(*parts)).is_file() for parts in INSTALL_MARKERS)
    except OSError:
        return False


def vdf_library_paths(text: str) -> list[str]:
    """Wyciągnij ścieżki bibliotek Steam z `libraryfolders.vdf` (bez zależności)."""
    import re

    paths = []
    for match in re.finditer(r'"path"\s+"((?:[^"\\]|\\.)*)"', text):
        raw = match.group(1).replace("\\\\", "\\")
        if raw:
            paths.append(raw)
    return paths


def steam_install_roots() -> list[Path]:
    """Biblioteki Steam: rejestr + `libraryfolders.vdf` → katalogi `steamapps/common`."""
    steam_dirs: list[Path] = []
    if sys.platform.startswith("win"):
        try:
            import winreg  # type: ignore[import-not-found]
        except ImportError:
            winreg = None  # type: ignore[assignment]
        if winreg is not None:
            for hive, key, value in (
                (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam", "InstallPath"),
            ):
                try:
                    with winreg.OpenKey(hive, key) as handle:
                        raw, _ = winreg.QueryValueEx(handle, value)
                except OSError:
                    continue
                if isinstance(raw, str) and raw:
                    steam_dirs.append(Path(raw))
    for guess in (Path("C:/Program Files (x86)/Steam"), Path("C:/Program Files/Steam")):
        steam_dirs.append(guess)

    roots: list[Path] = []
    for steam in steam_dirs:
        libraries = [steam]
        vdf = steam / "steamapps" / "libraryfolders.vdf"
        try:
            libraries.extend(Path(entry) for entry in vdf_library_paths(vdf.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            pass
        for library in libraries:
            for common in (library / "steamapps" / "common", library / "SteamApps" / "common"):
                if common.is_dir():
                    roots.append(common)
    return _dedupe(roots)


def guess_roots() -> list[Path]:
    """Typowe miejsca instalacji gier na dyskach + katalogi użytkownika."""
    roots: list[Path] = []
    if sys.platform.startswith("win"):
        for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            drive = Path(f"{letter}:/")
            if not drive.is_dir():
                continue
            for name in ("Games", "GOG Games", "SteamLibrary/steamapps/common",
                         "Program Files/Steam/steamapps/common",
                         "Program Files (x86)/Steam/steamapps/common",
                         "Program Files/Epic Games", "Epic Games"):
                candidate = drive / name
                if candidate.is_dir():
                    roots.append(candidate)
            # Instalacje „portable” często leżą bezpośrednio na dysku, np. D:\The Genesis Order.
            try:
                for child in drive.iterdir():
                    if child.is_dir() and any(hint in child.name.lower() for hint in NAME_HINTS):
                        roots.append(child)
            except OSError:
                continue
    home = Path.home()
    for name in ("Desktop", "Pulpit", "Downloads", "Pobrane", "Documents", "Dokumenty", "Games"):
        candidate = home / name
        if candidate.is_dir():
            roots.append(candidate)
    roots.extend([Path.cwd(), Path(__file__).resolve().parent.parent])
    return _dedupe(roots)


def _dedupe(paths: Iterable[Path]) -> list[Path]:
    seen: set[str] = set()
    unique: list[Path] = []
    for path in paths:
        try:
            key = str(path.resolve())
        except OSError:
            key = str(path)
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique


def find_installations(roots: Sequence[Path], max_depth: int = 4,
                       time_budget: float = 8.0, limit: int = 40) -> list[Path]:
    """Przeszukaj `roots` w głąb (BFS) w poszukiwaniu instalacji TGO.

    Przeszukiwanie jest ograniczone głębokością, czasem i liczbą wyników, żeby
    nigdy nie zamieniło się w skan całego dysku.
    """
    started = time.monotonic()
    found: list[Path] = []
    queue: list[tuple[Path, int]] = [(root, 0) for root in roots]
    visited = 0
    while queue:
        if time.monotonic() - started > time_budget or len(found) >= limit:
            break
        current, depth = queue.pop(0)
        visited += 1
        if visited > 40_000:
            break
        if is_install_root(current):
            found.append(current)
            continue
        if depth >= max_depth:
            continue
        try:
            children = sorted(current.iterdir(), key=lambda item: item.name.lower())
        except OSError:
            continue
        for child in children:
            try:
                if not child.is_dir() or child.is_symlink():
                    continue
            except OSError:
                continue
            if child.name.lower() in SKIP_DIR_NAMES:
                continue
            queue.append((child, depth + 1))
    return _dedupe(found)


# --------------------------------------------------------------------------- #
# Zapamiętana ścieżka
# --------------------------------------------------------------------------- #

def default_config_path() -> Path:
    override = os.environ.get(ENV_CONFIG_PATH)
    if override:
        return Path(override).expanduser()
    if sys.platform.startswith("win"):
        base = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming")
        return base / "TGO_PL_patch" / "config.json"
    base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return base / "tgo-pl-patch" / "config.json"


@dataclass
class Config:
    """Trwała pamięć ostatnio użytego katalogu gry."""

    path: Path = field(default_factory=default_config_path)

    def load(self) -> dict[str, Any]:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        return data if isinstance(data, dict) else {}

    def save(self, game_path: Path, patch_version: str, action: str) -> None:
        data = self.load()
        data.update({
            "schema": CONFIG_SCHEMA,
            "game_path": str(Path(game_path)),
            "last_patch_version": patch_version,
            "last_action": action,
            "saved_at_utc": datetime.now(timezone.utc).isoformat(),
        })
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self.path.with_name(self.path.name + f".{os.getpid()}.tmp")
            temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            os.replace(temporary, self.path)
        except OSError:
            # Brak zapisu konfiguracji nie może blokować instalacji patcha.
            pass

    def remembered(self) -> Path | None:
        raw = self.load().get("game_path")
        if not isinstance(raw, str) or not raw.strip():
            return None
        candidate = Path(raw)
        return candidate if is_install_root(candidate) else None

    def forget(self) -> bool:
        data = self.load()
        if not data:
            self.path.unlink(missing_ok=True)
            return False
        had = "game_path" in data
        data.pop("game_path", None)
        try:
            self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except OSError:
            return False
        return had


# --------------------------------------------------------------------------- #
# Interfejs użytkownika (GUI z fallbackiem konsolowym)
# --------------------------------------------------------------------------- #

class ConsoleGui:
    """Minimalny interfejs tekstowy: działa zawsze, także bez tkinter."""

    def __init__(self, stream=None) -> None:
        self.stream = stream or sys.stdout

    def say(self, message: str) -> None:
        print(message, file=self.stream)

    def ask_yes_no(self, question: str, default: bool = True) -> bool:
        suffix = " [T/n] " if default else " [t/N] "
        try:
            answer = input(question + suffix).strip().lower()
        except EOFError:
            return default
        if not answer:
            return default
        return answer in {"t", "tak", "y", "yes"}

    def pick_folder(self, initial: Path | None) -> Path | None:
        prompt = "Podaj folder The Genesis Order (zawierający www\\index.html)"
        if initial:
            prompt += f" [{initial}]"
        try:
            raw = input(prompt + ": ").strip().strip('"')
        except EOFError:
            return None
        return Path(raw) if raw else None

    def choose(self, candidates: Sequence[Path]) -> Path | None:
        self.say("Znaleziono kilka instalacji The Genesis Order:")
        for index, candidate in enumerate(candidates, 1):
            self.say(f"  {index}. {candidate}")
        try:
            raw = input(f"Wybierz numer (1-{len(candidates)}), Enter = ręcznie: ").strip()
        except EOFError:
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(candidates):
            return candidates[int(raw) - 1]
        return None


class TkGui(ConsoleGui):
    """Okna dialogowe Windows/macOS/Linux; przy braku tkinter wraca do konsoli."""

    def __init__(self) -> None:
        super().__init__()
        try:
            import tkinter  # noqa: F401
        except Exception:  # brak wyświetlacza / brak modułu → konsola
            self.tk = None
        else:
            self.tk = tkinter

    @property
    def available(self) -> bool:
        return self.tk is not None

    def _root(self):
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        return root

    def say(self, message: str) -> None:
        super().say(message)
        if not self.available:
            return
        try:
            from tkinter import messagebox

            root = self._root()
            try:
                messagebox.showinfo("TGO PL — patcher", message)
            finally:
                root.destroy()
        except Exception:
            pass

    def ask_yes_no(self, question: str, default: bool = True) -> bool:
        if not self.available:
            return super().ask_yes_no(question, default)
        try:
            from tkinter import messagebox

            root = self._root()
            try:
                return bool(messagebox.askyesno("TGO PL — patcher", question))
            finally:
                root.destroy()
        except Exception:
            return super().ask_yes_no(question, default)

    def pick_folder(self, initial: Path | None) -> Path | None:
        if not self.available:
            return super().pick_folder(initial)
        try:
            from tkinter import filedialog

            root = self._root()
            try:
                chosen = filedialog.askdirectory(
                    title="Wskaż folder The Genesis Order (ten z www\\index.html)",
                    initialdir=str(initial) if initial and initial.is_dir() else None,
                    mustexist=True,
                )
            finally:
                root.destroy()
        except Exception:
            return super().pick_folder(initial)
        return Path(chosen) if chosen else None

    def choose(self, candidates: Sequence[Path]) -> Path | None:
        if not self.available:
            return super().choose(candidates)
        import tkinter as tk
        from tkinter import ttk

        try:
            root = tk.Tk()
            root.title("TGO PL — wybierz instalację")
            root.attributes("-topmost", True)
            frame = ttk.Frame(root, padding=12)
            frame.pack(fill="both", expand=True)
            ttk.Label(frame, text="Znaleziono więcej niż jedną instalację The Genesis Order:").pack(anchor="w")
            listbox = tk.Listbox(frame, height=min(8, len(candidates)), width=70, exportselection=False)
            for candidate in candidates:
                listbox.insert("end", str(candidate))
            listbox.selection_set(0)
            listbox.pack(fill="both", expand=True, pady=8)
            result: dict[str, Path | None] = {"value": None}

            def accept() -> None:
                selection = listbox.curselection()
                if selection:
                    result["value"] = candidates[selection[0]]
                root.destroy()

            def pick_other() -> None:
                root.destroy()

            buttons = ttk.Frame(frame)
            buttons.pack(fill="x")
            ttk.Button(buttons, text="Użyj tej instalacji", command=accept).pack(side="left")
            ttk.Button(buttons, text="Wskaż inny folder…", command=pick_other).pack(side="left", padx=6)
            ttk.Button(buttons, text="Anuluj", command=root.destroy).pack(side="right")
            listbox.bind("<Double-Button-1>", lambda _event: accept())
            root.mainloop()
            return result["value"]
        except Exception:
            return super().choose(candidates)


# --------------------------------------------------------------------------- #
# Rozwiązywanie ścieżki instalacji
# --------------------------------------------------------------------------- #

def resolve_install(explicit: Path | None = None, *, action: str = "apply",
                    config: Config | None = None, gui: ConsoleGui | None = None,
                    interactive: bool = True, assume_yes: bool = False,
                    extra_roots: Sequence[Path] = (), log: Callable[[str], None] | None = None) -> Path:
    """Zwróć katalog instalacji: z argumentu, z pamięci, z autodetekcji albo od użytkownika.

    Kolejność jest celowa — najpierw to, co pewne i tanie (argument, pamięć),
    potem przeszukanie dysku, a dopiero na końcu pytanie do człowieka.
    """
    gui = gui or ConsoleGui()
    config = config or Config()
    say = log or gui.say

    if explicit is not None:
        candidate = Path(explicit).expanduser()
        if is_install_root(candidate):
            config.save(candidate, patch_version="", action=action)
            return candidate
        if not interactive:
            raise ValueError(f"To nie jest katalog instalacji TGO: {candidate}")
        say(f"Folder {candidate} nie wygląda na instalację TGO (brak www\\index.html).")

    remembered = config.remembered()
    declined: Path | None = None
    if remembered is not None:
        if assume_yes or not interactive:
            say(f"Używam zapamiętanej instalacji: {remembered}")
            config.save(remembered, patch_version="", action=action)
            return remembered
        if gui.ask_yes_no(f"Użyć zapamiętanej instalacji?\n\n{remembered}", default=True):
            config.save(remembered, patch_version="", action=action)
            return remembered
        # Skoro użytkownik odrzucił zapamiętaną instalację, nie proponujemy jej ponownie.
        declined = remembered
        config.forget()
    elif config.load().get("game_path"):
        say("Zapamiętana ścieżka już nie istnieje — szukam instalacji ponownie.")

    roots = list(extra_roots) + guess_roots() + steam_install_roots()
    if remembered is not None:
        roots.insert(0, remembered.parent)
    say("Szukam instalacji The Genesis Order…")
    candidates = [path for path in find_installations(roots) if path != declined]
    if remembered is not None and remembered in candidates:
        candidates.remove(remembered)
        candidates.insert(0, remembered)

    if len(candidates) == 1:
        chosen: Path | None = candidates[0]
        if interactive and not assume_yes:
            if not gui.ask_yes_no(f"Znalazłem instalację:\n\n{chosen}\n\nUżyć jej?", default=True):
                chosen = None
        if chosen is not None:
            say(f"Wybrano: {chosen}")
            config.save(chosen, patch_version="", action=action)
            return chosen
    elif len(candidates) > 1:
        say(f"Znaleziono {len(candidates)} instalacje.")
        chosen = gui.choose(candidates)
        if chosen is not None:
            config.save(chosen, patch_version="", action=action)
            return chosen

    if not interactive:
        raise ValueError(
            "Nie udało się automatycznie znaleźć instalacji The Genesis Order. "
            "Wskaż ją argumentem --game ŚCIEŻKA."
        )
    manual = gui.pick_folder(remembered.parent if remembered else None)
    if manual is None:
        raise ValueError("Anulowano wybór folderu instalacji; niczego nie zmieniono.")
    manual = Path(manual).expanduser()
    if not is_install_root(manual):
        raise ValueError(
            f"Folder {manual} nie zawiera www\\index.html — to nie jest katalog instalacji TGO."
        )
    say(f"Zapamiętam tę instalację: {manual}")
    config.save(manual, patch_version="", action=action)
    return manual
