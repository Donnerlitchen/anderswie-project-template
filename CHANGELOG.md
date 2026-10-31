# Changelog

Alle nennenswerten Änderungen an <PROJEKT>. Format: [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
Versionierung: SemVer. Jede veröffentlichte Version hat einen eigenen datierten Block.

## [Unreleased]

## [1.2.0] - 2026-10-31

### Hinzugefügt
- **`scripts/check_repo_security.py`** aus dem Projekt übernommen und verallgemeinert: meldet Pfad und **Art** eines Fundes, niemals den Wert; `--history --ref main` prüft die Historie. Damit läuft in `gates.sh` **kein Schritt mehr übersprungen**.

### Geändert
- Die bild- und rohspezifische Rechteprüfung des Herkunftsskripts ist entfernt: sie ist eine Projekt-Politik, kein Teil des Standards.

## [1.1.0] - 2026-10-31

### Hinzugefügt
- **Kopfzeile** für jedes Dokument in `docs/`: `**Stand:** … · **Verantwortlich:** …` — maschinell geprüft.
- **Altersfristen** je Dokument (Vorgabe 365 Tage; `STATUS.md` und `BACKLOG.md` 90 Tage). Ein Stand-Datum in der Zukunft fällt auf.
- **Wegweiser-Prüfung für `AGENTS.md`:** er muss auf `docs/INDEX.md` und `scripts/gates.sh` verweisen und kurz bleiben.
- **`scripts/muellabfuhr.py`:** meldet Aufräum-Kandidaten (überlange Dateien, verdächtige Namen, Arbeitsmarken-Häufungen, Doku ohne Index-Eintrag) und löscht nie etwas.
- Ideen übernommen aus dem Skill `agent-harness-engineering` (Herausgeber `yeyitech`, ClawHub, Fassung 0.1.0, 2026-03-08) — mit Beleg in `STANDARD.md`.

### Behoben
- `.gitignore` ignorierte `.venv`/`venv` nicht: die `README.md` verlangt ein eigenes venv, das damit vollständig in die Versionskontrolle gewandert wäre.
- `scripts/gates.sh` bricht nicht mehr mit einem Importfehler ab, wenn `pytest` fehlt, sondern nennt den Befehl zum Anlegen der Umgebung; ein von außen gesetztes `PY` hat Vorrang.
- `STANDARD.md` nannte als Vorlage des Ordnungs-Tests das inzwischen gelöschte Skill `repository-governance`; jetzt steht dort der echte Pfad `tests/test_dokumentenordnung.py`.

## [1.0.0] - 2026-10-31

- Der Standard als Template-Repository: Dateisatz, Dokumentenordnung und eigene Gates.
