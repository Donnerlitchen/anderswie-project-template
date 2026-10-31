# Changelog

Alle nennenswerten Änderungen an <PROJEKT>. Format: [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
Versionierung: SemVer. Jede veröffentlichte Version hat einen eigenen datierten Block.

## [Unreleased]

## [1.3.0] - 2026-10-31

### Hinzugefügt
- **`tests/test_dokumentationspflicht.py`:** die Prüfung, die `STANDARD.md` §4 Punkt 2 als Gate
  verlangt, fehlte in der Vorlage — `gates.sh` fuhr sie damit nicht. Ohne Quellordner meldet sie
  nichts; sobald `src/` existiert, verlangt sie den Changelog. Sie stammt aus dem Projekt
  *anderswie-product-intelligence*, wo sie diese Lücke geschlossen hat.
- **`pyproject.toml`** als Platzhalter: eine Versionsquelle, `src/`-Layout, `dev`-Extra mit pytest
  (`STANDARD.md` §1).

### Geändert
- `STANDARD.md` §2: **`docs/ACTIVE-MODULES.md` in den Dateisatz aufgenommen** (gilt, sobald es
  Quellcode gibt). Die Modulkarten-Prüfung übersprang bisher still den Fall „es gibt `src/`, aber
  keine Karte" — sie meldete nie einen Fund. Jetzt schlägt sie in diesem Fall fehl.
- `STANDARD.md` §2: **klargestellt, dass `docs/GOVERNANCE.md` und `docs/REGELWERK-UMBAU.md` der
  Vorlage gehören** und kein Pflichtbestandteil eines Projekts sind. Beide standen in keinem
  Dateisatz; wer die Vorlage abschrieb, musste raten — und sie landeten als zweiter Ort für dieselbe
  Regel im Projekt.
- `STANDARD.md` §3: die Dokumentationspflicht-Prüfung als eigene Zeile ergänzt.
- `README.md`: Abschnitt **„Wofür das gut ist"** ergänzt — das Warum in Alltagssprache, mit der Gegenüberstellung Chat ↔ Projekt. Klon-Befehl zeigt jetzt die GitHub-Adresse.
- `README.md` nannte noch **Fassung 1.1.0**, während `STANDARD.md` bereits auf 1.2.0 stand — die Versionsangabe zieht jetzt mit.

### Nachgetragen (Herkunft, Sprache)
- `docs/GOVERNANCE.md` und `docs/REGELWERK-UMBAU.md` kamen mit Fassung 1.0.0 und standen nur pauschal
  im 1.0.0-Block; ihr Ursprung (Projekt *anderswie-product-intelligence*) steht in ihrer eigenen
  Kopfzeile.
- Beide tragen **englische Fachabschnitte**, während sonst „Deutsch, ohne Jargon" gilt. Bewusst
  **nicht** umgeschrieben: eine Übersetzung verwässert gewachsene, praxiserprobte Texte und ist ein
  eigener Vorgang. Offen und benannt, nicht stillschweigend liegen gelassen.

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
