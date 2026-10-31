#!/usr/bin/env python3
"""Müllabfuhr — meldet Aufräum-Kandidaten. Ändert nichts, löscht nichts.

Warum: Jede Eilsitzung, jeder Agent und jede Umbenennung hinterlässt Spuren — überlange Dateien,
Namen wie `final-final` oder `Kopie`, TODO-Häufungen, Dokumente ohne Index-Eintrag. Sieht alles
harmlos aus. Ein Bericht findet es, **bevor** es zu stillen Altlasten wird.

Regel (siehe `docs/GOVERNANCE.md`): Dieser Bericht **meldet nur**. Aufräumen ist ein menschlicher
Entscheid; Löschen und Überschreiben brauchen Zustimmung (`docs/POLICIES.md` §1). Deshalb endet
das Skript immer mit Rückgabewert 0 — es ist keine Prüfung, sondern eine Sichtung.

Nicht hier drin: ob ein Dokument zu alt ist. Das prüft `tests/test_dokumentenordnung.py` mit
harten Fristen. Dieser Bericht zeigt das Alter nur als Information.

Aufruf aus dem Projektordner:

    python3 scripts/muellabfuhr.py
    python3 scripts/muellabfuhr.py --wurzel /pfad/zu/anderem/projekt
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

# Schwellen an genau einer Stelle.
GROSSE_DATEI_BYTES = 100_000
TODO_SCHWELLE = 3
ANZEIGE = 8

# Bilder, Video und Ton sind absichtlich groß — sie als „zu groß“ zu melden, wäre Rauschen und
# würde die echten Funde (Archive, Rohdaten, aufgeblähte Quelle) zudecken.
MEDIEN_ENDUNGEN = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".heic",
                   ".mp4", ".mov", ".avi", ".mkv", ".webm", ".mp3", ".wav", ".ogg", ".flac"}

# Ordner, die nie gemeint sind: fremde oder erzeugte Inhalte.
UEBERSPRINGEN = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
                 "dist", "build", ".mypy_cache", ".ruff_cache"}

# Namen, die auf Drift, Kopien oder abgebrochene Fassungen deuten.
VERDAECHTIG = re.compile(
    r"(final|endg(ü|u)ltig|kopie|copy|backup|sicherung|\balt\b|\bneu\b|\bneu2\b|tmp|temp|"
    r"\bwip\b|draft|entwurf|\bv\d\b\Z|\(\d\)|-\d\Z)", re.IGNORECASE)

# Endungen, die als Text gelesen werden dürfen.
TEXT_ENDUNGEN = {".py", ".md", ".sh", ".js", ".cjs", ".mjs", ".html", ".css", ".yaml", ".yml",
                 ".toml", ".json", ".cfg", ".ini", ".txt"}

SUCHWORT = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b")

# Dieses Skript wird beim Zählen übersprungen: seine Suchmuster enthalten genau die Wörter,
# die es sucht — es würde sich sonst immer selbst melden.
SELBST = Path(__file__).resolve()


def alle_dateien(wurzel: Path):
    for pfad in sorted(wurzel.rglob("*")):
        if any(teil in UEBERSPRINGEN for teil in pfad.parts):
            continue
        if pfad.is_file():
            yield pfad


def grosse_dateien(wurzel: Path):
    funde = [(p.stat().st_size, p) for p in alle_dateien(wurzel)
             if p.stat().st_size >= GROSSE_DATEI_BYTES and p.suffix.lower() not in MEDIEN_ENDUNGEN]
    return sorted(funde, reverse=True)


def verdaechtige_namen(wurzel: Path):
    funde = []
    for pfad in alle_dateien(wurzel):
        if "archive" in pfad.parts:  # historische Namen sind dort Absicht
            continue
        if VERDAECHTIG.search(pfad.stem):
            funde.append(pfad)
    return funde


def todo_hotspots(wurzel: Path):
    funde = []
    for pfad in alle_dateien(wurzel):
        if pfad.suffix.lower() not in TEXT_ENDUNGEN or pfad.stat().st_size > 2_000_000:
            continue
        if pfad.resolve() == SELBST:
            continue
        text = pfad.read_text(encoding="utf-8", errors="ignore")
        zahl = len(SUCHWORT.findall(text))
        if zahl >= TODO_SCHWELLE:
            funde.append((zahl, pfad))
    return sorted(funde, reverse=True)


def dokumente_ohne_index(wurzel: Path):
    docs = wurzel / "docs"
    index_datei = docs / "INDEX.md"
    if not index_datei.is_file():
        return []
    index = index_datei.read_text(encoding="utf-8")
    abschnitt = index.split("## Aktuell und maßgeblich", 1)[-1].split("\n## ", 1)[0]
    verlinkt = set(re.findall(r"\]\(([A-Za-z0-9._\-]+\.md)\)", abschnitt))
    return [d.name for d in sorted(docs.glob("*.md")) if d.name not in verlinkt and d.name != "INDEX.md"]


def alter_der_dokumente(wurzel: Path):
    docs = wurzel / "docs"
    if not docs.is_dir():
        return []
    heute = dt.date.today()
    funde = []
    for datei in sorted(docs.glob("*.md")):
        kopf = "\n".join(datei.read_text(encoding="utf-8").splitlines()[:10])
        treffer = re.search(r"20\d\d-\d\d-\d\d", kopf)
        if not treffer:
            funde.append((None, datei.name))
            continue
        tage = (heute - dt.date.fromisoformat(treffer.group(0))).days
        funde.append((tage, datei.name))
    return sorted(funde, key=lambda x: (x[0] is None, -(x[0] or 0)))


def _abschnitt(titel: str, hinweis: str, zeilen: list[str]) -> None:
    print(f"\n## {titel}")
    if not zeilen:
        print("   nichts gefunden")
        return
    print(f"   {hinweis}")
    for zeile in zeilen[:ANZEIGE]:
        print("   - " + zeile)
    if len(zeilen) > ANZEIGE:
        print(f"   … und {len(zeilen) - ANZEIGE} weitere")


def main() -> int:
    zerleger = argparse.ArgumentParser(description="Meldet Aufräum-Kandidaten. Löscht nichts.")
    zerleger.add_argument("--wurzel", default=str(Path(__file__).resolve().parent.parent),
                          help="Projektordner (Vorgabe: der Ordner über diesem Skript)")
    args = zerleger.parse_args()
    wurzel = Path(args.wurzel).expanduser().resolve()
    if not wurzel.is_dir():
        raise SystemExit(f"Ordner nicht gefunden: {wurzel}")

    print(f"Müllabfuhr-Bericht für {wurzel.name}")
    print(f"Stand {dt.date.today().isoformat()} · Ordner: {wurzel}")
    print("Dieser Bericht meldet nur — er ändert und löscht nichts.")

    _abschnitt("Große Dateien",
               f"über {GROSSE_DATEI_BYTES:,} Bytes — Kandidat für Aufteilen:".replace(",", "."),
               [f"{groesse / 1024:.0f} KB  {p.relative_to(wurzel)}" for groesse, p in grosse_dateien(wurzel)])

    _abschnitt("Verdächtige Namen",
               "deuten auf Kopie, Drift oder abgebrochene Fassung — prüfen, ob es das noch braucht:",
               [str(p.relative_to(wurzel)) for p in verdaechtige_namen(wurzel)])

    _abschnitt("Arbeitsmarken-Häufungen",
               f"{TODO_SCHWELLE} oder mehr TODO/FIXME/XXX/HACK in einer Datei:",
               [f"{zahl:>3}×  {p.relative_to(wurzel)}" for zahl, p in todo_hotspots(wurzel)])

    _abschnitt("Dokumente ohne Index-Eintrag",
               "liegen in docs/, sind aber in keiner Übersicht:",
               dokumente_ohne_index(wurzel))

    _abschnitt("Alter der Dokumente",
               "nur Information — die Fristen prüft tests/test_dokumentenordnung.py:",
               [(f"{name}: {tage} Tage" if tage is not None else f"{name}: kein Stand-Datum")
                for tage, name in alter_der_dokumente(wurzel)])

    print("\nVorschlag: Bericht durchsehen, dann einzeln entscheiden — nie in einem Zug aufräumen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
