# anderswie Projekt-Template

Vorlage für neue anderswie-Projekte: **Regeldateien, Dokumentenordnung und Prüfungen ab Tag eins.**

Dies ist ein **Template-Repository** — kein Projekt. Ein neues Projekt entsteht daraus, nicht durch
Abschreiben.

## Neues Projekt starten

```bash
git clone <pfad>/anderswie-project-template <neues-projekt>
cd <neues-projekt>
rm -rf .git && git init          # sauberer Verlauf, kein geerbtes Template-Log
```

Dann `STANDARD.md` lesen und den Platzhalter `<PROJEKT>` ersetzen (das Datum 2026-10-31
durch das Datum deines Projektstarts).

**Umgebung:** eigenes venv anlegen (`.venv`). Die Regel für das *richtige* Python steht an
einer Stelle in `scripts/projektumgebung.py`; `scripts/gates.sh` nutzt `.venv/bin/python`,
sonst `python3`.

**Der erste grüne Lauf ist der Startschuss:** `bash scripts/gates.sh` muss bestanden sein,
**bevor** Code entsteht.

## Was hier drin ist

| Datei | Zweck |
|---|---|
| `STANDARD.md` | **Der Standard:** Dateisatz, Mindestinhalte, Fallen, Vorlagen-Version |
| `AGENTS.md` | Verhalten des KI-Agenten (kurz, verweist nur) |
| `CONTRIBUTING.md` | Wie hier gearbeitet wird |
| `CHANGELOG.md` | Änderungsverlauf (Keep a Changelog) |
| `docs/` | Index, Source of Truth, Policies, Status, Backlog, Versionierung, Gates, Releases, Governance |
| `scripts/gates.sh` | **Ein** Befehl für alle Prüfungen |
| `tests/test_dokumentenordnung.py` | Erzwingt die Ordnung in `docs/` |

## Herkunft

Entstanden aus dem Projekt *anderswie-product-intelligence*, wo diese Struktur mühsam
nachgezogen werden musste. Jede „Falle" in `STANDARD.md` ist dort real passiert.
