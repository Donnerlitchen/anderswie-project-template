"""Dokumentenordnung: die Repo ist die einzige Wahrheit — Widersprüche dürfen nicht entstehen.

Hintergrund: Alte Entwürfe und ersetzte Fassungen lagen im aktiven `docs/`-Ordner und sahen dort aus
wie gültige Vorgaben. Außerdem waren Backlog-Zeilen mehrdeutig (erledigt? offen?) und Pläne trugen
Statuszeilen, die längst überholt waren. Diese Regeln gelten **für jede Sitzung, jeden Chat und jeden
Agenten** und stehen als verbindlicher Text in `docs/SOT.md` (Abschnitt „Dokumentenordnung").

Geprüft wird hier nur, was maschinell eindeutig ist — die inhaltliche Wahrheit bleibt bei Code,
Tests und `docs/STATUS.md`.
"""
import re
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
DOCS = WURZEL / "docs"
ARCHIV = DOCS / "archive"
DATUM = re.compile(r"20\d\d-\d\d-\d\d")


def _kopf(datei: Path, zeilen: int = 10) -> str:
    return "\n".join(datei.read_text(encoding="utf-8").splitlines()[:zeilen])


def test_jedes_aktive_dokument_ist_datiert():
    """Regel 2: Jedes Dokument im aktiven `docs/`-Ordner nennt oben ein Stand-Datum."""
    ohne = [d.name for d in sorted(DOCS.glob("*.md")) if not DATUM.search(_kopf(d))]
    assert ohne == [], "ohne Stand-Datum: " + ", ".join(ohne)


def test_keine_entwuerfe_im_aktiven_ordner():
    """Regel 1: Entwürfe und ersetzte Fassungen gehören ins Archiv, nicht nach `docs/`."""
    verdaechtig = []
    for datei in sorted(DOCS.glob("*.md")):
        kopf = _kopf(datei).lower()
        if re.search(r"status:?\s*\**\s*entwurf", kopf) or "nicht freigegeben" in kopf:
            verdaechtig.append(datei.name)
    assert verdaechtig == [], (
        "bezeichnen sich selbst als Entwurf/nicht freigegeben und gehören nach docs/archive/: "
        + ", ".join(verdaechtig))


def test_aktive_dokumente_stehen_im_index():
    """Regel 1: Was im aktiven Ordner liegt, ist im Index als maßgeblich geführt.

    Sonst entsteht genau der Zustand, der bereinigt wurde: eine Datei liegt in `docs/`, sieht
    gültig aus und steht in keiner Übersicht.
    """
    index = (DOCS / "INDEX.md").read_text(encoding="utf-8")
    abschnitt = index.split("## Aktuell und maßgeblich", 1)[-1].split("\n## ", 1)[0]
    tatsaechlich_verlinkt = set(re.findall(r"\]\(([A-Za-z0-9._\-]+\.md)\)", abschnitt))
    fehlend = [d.name for d in sorted(DOCS.glob("*.md"))
               if d.name not in tatsaechlich_verlinkt and d.name != "INDEX.md"]
    assert fehlend == [], (
        "liegen in docs/, stehen aber nicht im Index unter „Aktuell und maßgeblich\": "
        + ", ".join(fehlend))


def test_backlog_abschnitte_sind_datiert():
    """Regel 3: Jede Backlog-Überschrift trägt ein Datum — sonst ist ihr Alter nicht ablesbar."""
    ohne = [z.strip() for z in (DOCS / "BACKLOG.md").read_text(encoding="utf-8").splitlines()
            if z.startswith("## ") and not DATUM.search(z)]
    assert ohne == [], "Backlog-Überschriften ohne Datum: " + " | ".join(ohne)


def test_changelog_bloecke_sind_datiert():
    """Regel 4: Jeder Versionsblock im Changelog ist datiert (außer `[Unreleased]`)."""
    ohne = [z.strip() for z in (WURZEL / "CHANGELOG.md").read_text(encoding="utf-8").splitlines()
            if z.startswith("## [") and "unreleased" not in z.lower() and not DATUM.search(z)]
    assert ohne == [], "Changelog-Blöcke ohne Datum: " + " | ".join(ohne)


def test_archivierte_dokumente_sind_gekennzeichnet():
    """Regel 1: Jedes archivierte Dokument trägt oben seine Archiv-Kennzeichnung mit Nachfolger."""
    if not ARCHIV.is_dir():
        return
    dateien = sorted(ARCHIV.rglob("*.md"))
    ohne = [d.name for d in dateien if "Archiviert am" not in _kopf(d, 6)]
    assert ohne == [], "ohne Archiv-Kennzeichnung: " + ", ".join(ohne)


def test_keine_toten_verweise():
    """Regel 5: Ein aktives Dokument verweist nur auf Vorhandenes.

    Ein toter Verweis ist ein Widerspruch in Reinform: die Datei behauptet, es gebe etwas, das es
    nicht gibt. Geprüft werden die aktiven Dokumente; `docs/archive/` und erzeugte Artefakte bleiben
    außen vor, weil dort historische Pfade absichtlich stehen bleiben.
    """
    dateien = sorted(DOCS.glob("*.md")) + [WURZEL / name for name in ("README.md", "AGENTS.md", "CONTRIBUTING.md")]
    tot = []
    for datei in dateien:
        if not datei.exists():
            continue
        for ziel in re.findall(r"\]\(([^)#\s]+)\)", datei.read_text(encoding="utf-8")):
            if ziel.startswith(("http://", "https://", "mailto:")):
                continue
            if not (datei.parent / ziel).resolve().exists():
                tot.append(f"{datei.relative_to(WURZEL)} → {ziel}")
    assert tot == [], "tote Verweise: " + " | ".join(tot)


def test_alle_module_stehen_in_der_modulkarte():
    """Die Modulkarte beschreibt den **aktuellen Code** — jedes Modul muss dort stehen.

    Ein frisches Projekt hat noch keinen Quellordner; dann gibt es nichts zu prüfen.
    """
    quellen = WURZEL / "src"
    karte_datei = DOCS / "ACTIVE-MODULES.md"
    if not quellen.is_dir() or not karte_datei.is_file():
        return
    karte = karte_datei.read_text(encoding="utf-8")
    module = sorted(p.name for p in quellen.rglob("*.py") if p.name != "__init__.py")
    fehlend = [m for m in module if m not in karte]
    assert fehlend == [], "nicht in docs/ACTIVE-MODULES.md genannt: " + ", ".join(fehlend)


def test_schrittnamen_folgen_der_namensordnung():
    """Namensordnung: Schritte tragen keine freien Buchstaben („Phase B", „Etappe D").

    Ein Name hat genau eine Bedeutung (siehe `docs/SOT.md`, Abschnitt Namensordnung). Was in
    Anführungszeichen oder in Code steht, ist ein **Zitat** der Regel selbst und zählt nicht.
    `STATUS.md` ist ein datierter Verlauf: er behält seine damaligen Worte absichtlich.
    """
    verboten = re.compile(r"\b(?:Phase|Etappe|Schritt) [A-D]\b")
    dateien = sorted(DOCS.glob("*.md"))
    treffer = []
    for datei in dateien:
        if datei.name == "STATUS.md":
            continue
        for nummer, zeile in enumerate(datei.read_text(encoding="utf-8").splitlines(), 1):
            ohne_zitat = re.sub(r"`[^`]*`", "", zeile)
            # Beide Schließzeichen zulassen: typografisch `“` und gerade Anführung `"`.
            ohne_zitat = re.sub(r"„[^“\"]*[“\"]", "", ohne_zitat)
            if verboten.search(ohne_zitat):
                treffer.append(f"{datei.name}:{nummer}")
    assert treffer == [], "freie Buchstaben als Schrittname: " + ", ".join(treffer)
