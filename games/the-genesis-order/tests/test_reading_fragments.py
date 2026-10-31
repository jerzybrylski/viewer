"""Testy narzędzia `annotate_reading_fragments.py` (wstawki wideo we fragmentach)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
GAME = REPO / "games" / "the-genesis-order"
TOOL = GAME / "tools" / "annotate_reading_fragments.py"
MASTER = GAME / "reading" / "v1" / "chronological_script_PL.md"
SOURCES = GAME / "reading" / "fragments" / "source"
OUTPUTS = GAME / "reading" / "fragments" / "v1"
REPORT = GAME / "translation" / "reports" / "tgo_reading_fragments_video_v1.json"

MARKER = "> **🎬 Wstawka wideo:**"

sys.path.insert(0, str(TOOL.parent))
import annotate_reading_fragments as arf  # noqa: E402


MASTER_FIXTURE = """# Test

## Common Event 001 — Scena A

> **🎬 Wstawka wideo:** `A1.mp4` (zapętlone)

**Mox:** Pierwsza kwestia.
**Anna:** Druga kwestia.

> **🎬 Wstawka wideo:** `A2.mp4`

**Mox:** Trzecia kwestia.

---

## Mapa 001 — Gdzieś / event 1 / strona 1

**Anna:** Kwestia bez wstawki.
**Mox:** Kolejna kwestia bez wstawki.
**Anna:** Ostatnia kwestia.

---

## Mapa 002 — Gdzieś indziej / event 2 / strona 1

**Mox:** Kwestia tylko w matce.
**Anna:** Nic tu nie ma wideo.

---
"""

FRAGMENT_NO_HEADER = (
    "The Genesis Order\r\n\r\n"
    "## Common Event 001 — Scena A\r\n\r\n"
    "**Mox:** Pierwsza kwestia.  \r\n"
    "**Anna:** Druga kwestia.  \r\n"
    "**Mox:** Trzecia kwestia.  \r\n\r\n"
    "---\r\n\r\n"
    "## Mapa 001 — Gdzieś / event 1 / strona 1\r\n\r\n"
    "**Mox:** Kolejna kwestia bez wstawki.  \r\n"
    "**Anna:** Ostatnia kwestia.  \r\n"
)


class ToolTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.master = self.root / "master.md"
        self.master.write_text(MASTER_FIXTURE, encoding="utf-8")
        self.frags = self.root / "frags"
        self.frags.mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_tool(self, out_name: str = "out", report: bool = True) -> subprocess.CompletedProcess:
        cmd = [
            sys.executable,
            str(TOOL),
            "--master",
            str(self.master),
            "--fragments",
            str(self.frags),
            "--out",
            str(self.root / out_name),
        ]
        if report:
            cmd += ["--report", str(self.root / f"{out_name}.json")]
        return subprocess.run(cmd, capture_output=True, text=True, check=False)


class TestInsertion(ToolTestCase):
    def test_inserts_leading_and_between_markers(self) -> None:
        (self.frags / "TGO1.txt").write_text(FRAGMENT_NO_HEADER, encoding="utf-8")
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, result.stderr)
        out = (self.root / "out" / "TGO1.txt").read_text(encoding="utf-8")
        self.assertIn("`A1.mp4`", out)
        self.assertIn("`A2.mp4`", out)
        # A1 stoi po nagłówku, przed pierwszą kwestią
        self.assertLess(out.index("Common Event 001"), out.index("A1.mp4"))
        self.assertLess(out.index("A1.mp4"), out.index("Pierwsza kwestia"))
        # A2 stoi między drugą a trzecią kwestią
        self.assertLess(out.index("Druga kwestia"), out.index("A2.mp4"))
        self.assertLess(out.index("A2.mp4"), out.index("Trzecia kwestia"))
        # brak wstawek w epizodzie bez wideo
        self.assertNotIn("Mapa 002", out)

    def test_preserves_crlf_and_content(self) -> None:
        (self.frags / "TGO1.txt").write_text(FRAGMENT_NO_HEADER, encoding="utf-8")
        self.assertEqual(self.run_tool().returncode, 0)
        raw = (self.root / "out" / "TGO1.txt").read_bytes()
        self.assertIn(b"\r\n", raw)
        self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))
        original = [l for l in FRAGMENT_NO_HEADER.split("\r\n") if l.strip()]
        produced = [
            l
            for l in raw.decode("utf-8").split("\r\n")
            if l.strip() and not l.startswith(MARKER)
        ]
        self.assertEqual(original, produced)

    def test_keeps_user_lines_and_reports_them(self) -> None:
        (self.frags / "TGO1.txt").write_text(
            "## Common Event 001 — Scena A\n\n"
            "**Mox:** Pierwsza kwestia.\n"
            "**Mox:** Kwestia dopisana przez redakcję.\n"
            "**Anna:** Druga kwestia.\n",
            encoding="utf-8",
        )
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, result.stderr)
        out = (self.root / "out" / "TGO1.txt").read_text(encoding="utf-8")
        self.assertIn("Kwestia dopisana przez redakcję", out)
        report = json.loads((self.root / "out.json").read_text(encoding="utf-8"))
        self.assertEqual(len(report["reports"][0]["unmatched_dialogs"]), 1)
        # A2 stoi po kwestii redakcyjnej (przed pierwszą dopasowaną po niej)
        self.assertEqual(report["reports"][0]["markers_inserted"], 1)

    def test_keeps_marker_from_skipped_dialogue(self) -> None:
        """Kwestia pominięta przez redakcję nie gubi wstawki, jeśli oba sąsiedztwa zostały.

        Wstawka stoi w pliku matce między kwestią drugą a trzecią; fragment
        pomija kwestię drugą, więc znacznik trafia między pierwszą a trzecią.
        """
        (self.frags / "TGO1.txt").write_text(
            "## Common Event 001 — Scena A\n\n"
            "**Mox:** Pierwsza kwestia.\n"
            "**Mox:** Trzecia kwestia.\n",
            encoding="utf-8",
        )
        self.assertEqual(self.run_tool().returncode, 0)
        out = (self.root / "out" / "TGO1.txt").read_text(encoding="utf-8")
        self.assertIn("A1.mp4", out)
        self.assertIn("A2.mp4", out)
        self.assertLess(out.index("Pierwsza kwestia"), out.index("A2.mp4"))
        self.assertLess(out.index("A2.mp4"), out.index("Trzecia kwestia"))

    def test_trailing_marker_when_block_ends_episode(self) -> None:
        self.master.write_text(
            "## Common Event 001 — Scena A\n\n"
            "**Mox:** Jedyna kwestia.\n\n"
            "> **🎬 Wstawka wideo:** `A9.mp4`\n\n---\n",
            encoding="utf-8",
        )
        (self.frags / "TGO1.txt").write_text(
            "## Common Event 001 — Scena A\n\n**Mox:** Jedyna kwestia.\n\n---\n",
            encoding="utf-8",
        )
        self.assertEqual(self.run_tool().returncode, 0)
        out = (self.root / "out" / "TGO1.txt").read_text(encoding="utf-8")
        self.assertIn("A9.mp4", out)
        self.assertLess(out.index("Jedyna kwestia"), out.index("A9.mp4"))
        self.assertLess(out.index("A9.mp4"), out.index("---"))

    def test_unknown_header_is_reported(self) -> None:
        (self.frags / "TGO1.txt").write_text(
            "## Nieistniejący epizod\n\n**Mox:** Cokolwiek.\n", encoding="utf-8"
        )
        self.assertEqual(self.run_tool().returncode, 0)
        report = json.loads((self.root / "out.json").read_text(encoding="utf-8"))
        block = report["reports"][0]["blocks"][0]
        self.assertEqual(block["error"], "nie dopasowano epizodu")
        self.assertEqual(report["markers_total"], 0)


class TestSafety(ToolTestCase):
    def test_refuses_existing_output_dir(self) -> None:
        (self.frags / "TGO1.txt").write_text(FRAGMENT_NO_HEADER, encoding="utf-8")
        (self.root / "out").mkdir()
        result = self.run_tool()
        self.assertEqual(result.returncode, 3)
        self.assertIn("już istnieje", result.stderr)

    def test_refuses_existing_report(self) -> None:
        (self.frags / "TGO1.txt").write_text(FRAGMENT_NO_HEADER, encoding="utf-8")
        (self.root / "out.json").write_text("{}", encoding="utf-8")
        self.assertEqual(self.run_tool().returncode, 3)

    def test_missing_master(self) -> None:
        (self.frags / "TGO1.txt").write_text(FRAGMENT_NO_HEADER, encoding="utf-8")
        self.master.unlink()
        self.assertEqual(self.run_tool().returncode, 2)


@unittest.skipUnless(MASTER.is_file() and SOURCES.is_dir(), "brak danych wejściowych w repo")
class TestRepositoryData(unittest.TestCase):
    """Kontrola rzeczywistych fragmentów TGO1..TGO12 dołączonych do repo."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.master = arf.Master(MASTER.read_bytes().decode("utf-8-sig"))

    def test_every_source_has_output(self) -> None:
        for source in sorted(SOURCES.glob("*.txt")):
            self.assertTrue((OUTPUTS / source.name).is_file(), source.name)

    def test_no_line_lost(self) -> None:
        for source in sorted(SOURCES.glob("*.txt")):
            before = [
                line for line in source.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").split("\n")
                if line.strip()
            ]
            after = [
                line
                for line in (OUTPUTS / source.name).read_text(encoding="utf-8").split("\n")
                if line.strip() and not line.startswith(MARKER)
            ]
            self.assertEqual(before, after, source.name)

    def test_newline_style_preserved(self) -> None:
        for source in sorted(SOURCES.glob("*.txt")):
            produced = (OUTPUTS / source.name).read_bytes()
            self.assertNotIn(b"\n", produced.replace(b"\r\n", b""), source.name)

    def test_markers_come_from_master(self) -> None:
        master_markers = {line.strip() for line in self.master.lines if line.startswith(MARKER)}
        for path in sorted(OUTPUTS.glob("*.txt")):
            for line in path.read_text(encoding="utf-8").split("\n"):
                if line.startswith(MARKER):
                    self.assertIn(line.strip(), master_markers, f"{path.name}: {line}")

    def test_tgo12_has_no_markers_in_master(self) -> None:
        # fakt z pliku matki: żaden z 10 epizodów TGO12 nie ma wstawki wideo
        self.assertEqual(
            (SOURCES / "TGO12.txt").read_bytes(), (OUTPUTS / "TGO12.txt").read_bytes()
        )

    def test_report_summary(self) -> None:
        self.assertTrue(REPORT.is_file())
        report = json.loads(REPORT.read_text(encoding="utf-8"))
        self.assertEqual(report["files"], 12)
        self.assertEqual(report["markers_total"], 72)
        self.assertEqual(
            report["markers_total"],
            sum(len(entry["markers"]) for entry in report["reports"]),
        )
        for entry in report["reports"]:
            produced = sum(
                1
                for line in (OUTPUTS / entry["file"]).read_text(encoding="utf-8").split("\n")
                if line.startswith(MARKER)
            )
            self.assertEqual(produced, entry["markers_inserted"], entry["file"])


if __name__ == "__main__":
    unittest.main()
