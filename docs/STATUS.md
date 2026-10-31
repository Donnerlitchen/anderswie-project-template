# Projektstatus

**Stand:** 2026-10-31 · **Verantwortlich:** Ramona. Der jüngste Stand steht **oben**; ältere Abschnitte sind datierte
Momentaufnahmen und bleiben als Verlauf stehen — sie werden **nicht** umgeschrieben. Maßgeblich bei
Abweichungen sind Code und Tests.

## 2026-10-31 · Vorlage 1.1.0 — die Ordnung wird erzwungen

- **Kopfzeile** (Stand + Verantwortlich) in allen elf Dokumenten; drei neue Prüfungen im Ordnungs-Test:
  verantwortliche Person, Altersfristen, Wegweiser.
- **Neu:** `scripts/muellabfuhr.py` — meldet Aufräum-Kandidaten, löscht nie etwas (bewusst kein Gate).
- **Behoben:** `.gitignore` ignorierte `.venv` nicht (die README verlangt genau dieses venv);
  `gates.sh` brach bei fehlendem `pytest` mit einer kryptischen Meldung ab.
- **Nachweis:** 13 Ordnungs-Tests grün; `bash scripts/gates.sh` alle Schritte bestanden.
- **Offen:** `scripts/check_repo_security.py` fehlt noch — die Secret-Prüfung läuft deshalb nicht mit.

## 2026-10-31 — Projekt startet

- Aufgesetzt aus `anderswie-project-template` Version 1.0.0.
- **Offen:** <was als Nächstes>
