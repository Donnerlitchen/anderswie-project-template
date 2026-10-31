"""Welches Python für Prüfungen und Builds gilt — eine Stelle für die ganze Werkzeugkiste.

**Warum das hier steht:** `python3` im PATH ist nicht immer das Projekt-Python. Auf diesem Rechner
zeigt es zum Beispiel auf die Umgebung eines anderen Werkzeugs; darin fehlen `pytest` und die
Projektabhängigkeiten. Ein Prüfskript scheitert dann an seinen **eigenen** Gates, obwohl der Code in
Ordnung ist — und man sucht den Fehler an der falschen Stelle. Damit das nicht davon abhängt, wie
jemand das Skript aufruft, gilt ab jetzt eine Regel:

1. `.venv/bin/python` im Projektordner, wenn vorhanden und startbar.
2. Sonst `python3` aus dem PATH.

Skripte, die Unterprozesse starten, holen sich das Python über `python_fuer_pruefungen()` und rufen
zu Beginn `mit_projektumgebung_neu_starten()` auf. `scripts/gates.sh` setzt dieselbe Regel in der
Shell um — dort ist kein Import möglich, deshalb steht die kurze Fassung auch dort.

Prüfbar: siehe `tests/test_projektumgebung.py`.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV_PYTHON = ROOT / ".venv" / "bin" / "python"


def python_fuer_pruefungen() -> str:
    """Das Python, mit dem Tests, Kompilierung und Sicherheitsprüfung laufen sollen."""
    if VENV_PYTHON.is_file() and os.access(VENV_PYTHON, os.X_OK):
        return str(VENV_PYTHON)
    return "python3"


def gleiche_umgebung(ziel: str) -> bool:
    """Läuft `ziel` in derselben Umgebung wie das laufende Programm?

    **Nicht die Dateien vergleichen:** `.venv/bin/python` ist ein Verweis auf denselben
    Basis-Interpreter wie jedes andere Venv auf diesem Rechner — beide zeigen auf dieselbe Datei,
    sind aber verschiedene Umgebungen. Ein Dateivergleich sagt deshalb fälschlich „gleich" und der
    Neustart unterbliebe. Verglichen wird darum `sys.prefix`, also die Wurzel der Umgebung.
    """
    try:
        ergebnis = subprocess.run([ziel, "-c", "import sys; print(sys.prefix)"],
                                  capture_output=True, text=True, check=True)
    except (OSError, subprocess.SubprocessError):
        return False
    return ergebnis.stdout.strip() == sys.prefix


def mit_projektumgebung_neu_starten() -> None:
    """Startet das laufende Skript mit dem richtigen Python neu, falls es mit dem falschen läuft.

    Gehört als erste Zeile in `if __name__ == "__main__":`. Danach ist `sys.executable` verlässlich.
    """
    ziel = python_fuer_pruefungen()
    if not gleiche_umgebung(ziel):
        print(f"Hinweis: falsche Umgebung ({sys.prefix}) – Neustart mit {ziel}", file=sys.stderr)
        os.execv(ziel, [ziel, *sys.argv])
