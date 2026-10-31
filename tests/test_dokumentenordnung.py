"""Dokumentenordnung: die Repo ist die einzige Wahrheit — Widersprüche dürfen nicht entstehen.

Hintergrund: Alte Entwürfe und ersetzte Fassungen lagen im aktiven `docs/`-Ordner und sahen dort aus
wie gültige Vorgaben. Außerdem waren Backlog-Zeilen mehrdeutig (erledigt? offen?) und Pläne trugen
Statuszeilen, die längst überholt waren. Diese Regeln gelten **für jede Sitzung, jeden Chat und jeden
Agenten** und stehen als verbindlicher Text in `docs/SOT.md` (Abschnitt „Dokumentenordnung").

Geprüft wird hier nur, was maschinell eindeutig ist — die inhaltliche Wahrheit bleibt bei Code,
Tests und `docs/STATUS.md`.

**Ein Test zählt erst, wenn er am alten Stand scheitert** (`CONTRIBUTING.md` §4). Jede Prüfung hier
lässt sich gegenprüfen: Datei verstümmeln, Fehlschlag ansehen, zurücknehmen.
"""
import re
from datetime import date
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
DOCS = WURZEL / "docs"
ARCHIV = DOCS / "archive"
DATUM = re.compile(r"20\d\d-\d\d-\d\d")

# Kopfzeilen-Fristen: wie lange darf ein Dokument unüberprüft stehen?
# Grundlage: docs/SOT.md, Abschnitt „Dokumentenordnung".
VORGABE_TAGE = 365
FRIST_TAGE = {
    "STATUS.md": 90,   # behauptet einen geprüften Ist-Stand
    "BACKLOG.md": 90,  # offene Arbeit veraltet schnell und wird dann zur Liste von Rätseln
}

# AGENTS.md ist ein Wegweiser, kein Handbuch (STANDARD.md: „unter 100 Zeilen").
AGENTS_MAX_ZEILEN = 120

# Wohin der Wegweiser zeigen muss: Einstieg in die Doku und der Prüfbefehl.
AGENTS_PFLICHTZIELE = ("docs/INDEX.md", "scripts/gates.sh")


def _kopf(datei: Path, zeilen: int = 10) -> str:
    return "\n".join(datei.read_text(encoding="utf-8").splitlines()[:zeilen])


def _stand(datei: Path):
    """Das Stand-Datum aus der Kopfzeile — oder None, wenn keines da ist."""
    treffer = DATUM.search(_kopf(datei))
    return date.fromisoformat(treffer.group(0)) if treffer else None


def test_jedes_aktive_dokument_ist_datiert():
    """Regel 2: Jedes Dokument im aktiven `docs/`-Ordner nennt oben ein Stand-Datum."""
    ohne = [d.name for d in sorted(DOCS.glob("*.md")) if not DATUM.search(_kopf(d))]
    assert ohne == [], "ohne Stand-Datum: " + ", ".join(ohne)


def test_jedes_aktive_dokument_nennt_verantwortliche():
    """Regel 2: Jedes Dokument nennt oben, **wer** es führt.

    Ein Dokument ohne Namen hat niemanden, der es aktualisiert — genau so entstehen Aussagen, die
    drei Monate später noch wie gültige Vorgaben aussehen.
    """
    ohne = [d.name for d in sorted(DOCS.glob("*.md")) if "verantwortlich" not in _kopf(d).lower()]
    assert ohne == [], (
        "ohne Verantwortliche/n in der Kopfzeile (`**Verantwortlich:** <Name>`): " + ", ".join(ohne))


def test_dokumente_sind_nicht_veraltet():
    """Regel 2: Das Stand-Datum liegt innerhalb der Frist — und nicht in der Zukunft.

    Die Fristen sind bewusst je Dokument gesetzt (`FRIST_TAGE`, sonst `VORGABE_TAGE`): ein
    Regelwerk darf lange halten, ein Status nicht. Ein Datum in der Zukunft ist keine Veraltung,
    sondern eine **falsche Angabe** und wird schärfer gemeldet.
    """
    heute = date.today()
    zu_alt, zukunft = [], []
    for datei in sorted(DOCS.glob("*.md")):
        stand = _stand(datei)
        if stand is None:  # fehlt ganz — das meldet der Datums-Test
            continue
        tage = (heute - stand).days
        if tage < 0:
            zukunft.append(f"{datei.name} ({stand}, {abs(tage)} Tage in der Zukunft)")
            continue
        grenze = FRIST_TAGE.get(datei.name, VORGABE_TAGE)
        if tage > grenze:
            zu_alt.append(f"{datei.name}: {tage} Tage (Frist {grenze})")
    assert zukunft == [], ("Stand-Datum in der Zukunft — Datum korrigieren: " + " | ".join(zukunft))
    assert zu_alt == [], (
        "seit der Frist nicht überprüft — Stand prüfen und Kopfzeile aktualisieren: "
        + " | ".join(zu_alt))


def test_agents_md_verweist_auf_einstieg_und_pruefung():
    """Regel 6: `AGENTS.md` ist ein Wegweiser — er zeigt auf den Doku-Einstieg **und** den Prüfbefehl.

    Ein Wegweiser ohne Ziel ist keiner. Geprüft wird ein echter Markdown-Verweis, kein Code-Zitat:
    nur ein Verweis ist anklickbar und bleibt beim Verschieben sichtbar.
    """
    text = (WURZEL / "AGENTS.md").read_text(encoding="utf-8")
    ziele = [z.rstrip("/") for z in re.findall(r"\]\(([^)#\s]+)\)", text)]
    fehlend = [p for p in AGENTS_PFLICHTZIELE if not any(z.endswith(p) for z in ziele)]
    assert fehlend == [], (
        "AGENTS.md verweist nicht auf: " + ", ".join(fehlend)
        + " (als Markdown-Verweis `[Text](Ziel)`)")


def test_agents_md_bleibt_kurz():
    """Regel 6: Wird `AGENTS.md` zum Handbuch, ist das ein Zeichen für fehlende Zielorte.

    Der Inhalt gehört dann in die Fachdatei — hier bleibt der Wegweiser.
    """
    text = (WURZEL / "AGENTS.md").read_text(encoding="utf-8")
    zeilen = len([z for z in text.splitlines() if z.strip()])
    assert zeilen <= AGENTS_MAX_ZEILEN, (
        f"AGENTS.md hat {zeilen} gefüllte Zeilen (Grenze {AGENTS_MAX_ZEILEN}) — "
        "Inhalt in die zuständige Fachdatei verschieben und hier nur verweisen")


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

    Ein frisches Projekt hat noch keinen Quellordner; dann gibt es nichts zu prüfen. Gibt es aber
    Quellcode, **muss** die Karte da sein: eine still übersprungene Prüfung meldet nie einen Fund.
    """
    quellen = WURZEL / "src"
    if not quellen.is_dir():
        return
    karte_datei = DOCS / "ACTIVE-MODULES.md"
    assert karte_datei.is_file(), (
        "es gibt `src/`, aber `docs/ACTIVE-MODULES.md` fehlt — die Modulkarte gehört dazu "
        "(siehe STANDARD.md §2)")
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
