# Projektstatus

**Stand:** 2026-10-31 · **Verantwortlich:** Ramona. Der jüngste Stand steht **oben**; ältere Abschnitte sind datierte
Momentaufnahmen und bleiben als Verlauf stehen — sie werden **nicht** umgeschrieben. Maßgeblich bei
Abweichungen sind Code und Tests.

## 2026-10-31 · Vorlage 1.2.0 — Secret-Prüfung übernommen

- `scripts/check_repo_security.py` aus *anderswie-product-intelligence* übernommen und
  verallgemeinert. Meldet **Pfad und Art**, nie den Wert; `--history --ref main` prüft die Historie.
- **Damit läuft in `gates.sh` kein Schritt mehr übersprungen** — die Vorlage ist vollständig.
- **Nachweis am Wegwerf-Repo** (nicht im Projekt): sauber → GRÜN (0); Fund im Arbeitsstand → ROT (1)
  mit `config.py [aws_zugangsschluessel]`; **gelöschte** Datei → Arbeitsstand GRÜN, Historie **ROT**
  (`HISTORIE:config.py`). Die Historien-Prüfung ist also nicht dekorativ.
- **Offen:** `docs/GOVERNANCE.md` ist überwiegend englisch — steht in `BACKLOG.md`.

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
