"""Dokumentationspflicht: Code geändert ⇒ `CHANGELOG.md` mitgezogen.

Warum: Die Regel steht in `AGENTS.md` und `CONTRIBUTING.md` §4 — dieser Test setzt den Teil davon
maschinell durch, der sich maschinell durchsetzen lässt: Wer Dateien unter `src/` anfasst, muss
`CHANGELOG.md` mitziehen. Was sich **nicht** prüfen lässt — ob die Beschreibung stimmt — bleibt
Handarbeit und steht deshalb zusätzlich als Regel in `AGENTS.md`.

Ohne Quellordner (`src/`) gibt es nichts zu prüfen: ein frisches Projekt darf diese Datei behalten,
sie meldet dann nichts. Sobald Code entsteht, greift sie.
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUELLORDNER = ROOT / "src"


def geaenderte_dateien() -> set[str]:
    """Dateien, die vom HEAD abweichen — auch noch nicht vorgemerkte."""
    ausgabe = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, check=True,
                             text=True, capture_output=True).stdout
    dateien = set()
    for zeile in ausgabe.splitlines():
        if len(zeile) < 4:
            continue
        pfad = zeile[3:].strip().strip('"')
        if " -> " in pfad:          # Umbenennung: der neue Pfad zählt
            pfad = pfad.split(" -> ", 1)[1].strip().strip('"')
        dateien.add(pfad)
    return dateien


def test_code_aenderung_zieht_changelog_nach_sich():
    if not QUELLORDNER.is_dir():
        return                      # kein Quellordner: nichts zu prüfen
    dateien = geaenderte_dateien()
    if not dateien:
        return                      # sauberer Arbeitsbaum: nichts zu prüfen
    app_code = sorted(d for d in dateien if d.startswith("src/") and d.endswith(".py"))
    if not app_code:
        return                      # nur Doku, Skripte, Tests: Changelog nicht zwingend
    assert "CHANGELOG.md" in dateien, (
        "Code geändert, aber CHANGELOG.md nicht mitgezogen: "
        + ", ".join(app_code[:5])
        + " — Dokumentationspflicht nach jedem größeren Thema (AGENTS.md, Regel 4).")
