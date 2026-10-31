# anderswie Projekt-Template

Vorlage für neue anderswie-Projekte: **Regeldateien, Dokumentenordnung und Prüfungen ab Tag eins.**

Dies ist ein **Template-Repository** — kein Projekt. Ein neues Projekt entsteht daraus, nicht durch
Abschreiben.

## Wofür das gut ist

**Kurz:** Hausordnung und Kontrollzettel für ein neues Projekt — fertig am ersten Tag, statt mühsam
nachgezogen im dritten Monat.

| Der Chat (das Modell) | Das Projekt (dieser Ordner) |
|---|---|
| vergisst — nach ein paar Stunden ist der Anfang weg | hat alles geschrieben, mit Datum und Quelle |
| jedes KI-Werkzeug erinnert sich anders | **eine** Anweisung für alle (`AGENTS.md`) |
| nichts davon kann man später nachschlagen | nachlesbar, versioniert, prüfbar |

**Jetzt** heißt das: ein neues Projekt ist in Minuten startklar, die Regeln gelten in jeder Sitzung,
und die Prüfungen schlagen von selbst an — statt dass jemand daran denken muss.

**Später** heißt das: nach einer Pause, in einer neuen Sitzung, mit einem anderen Modell oder mit einer
zweiten Person kommt der Stand aus dem Ordner, nicht aus einem Gedächtnis. Eine Sitzung, in der niemand
mehr weiß, warum etwas so ist, kostet mehr als diese Vorlage.

**Was es nicht kann:** Es prüft, *dass* etwas geordnet und dokumentiert ist — nie, *ob es stimmt*.
Entscheidungen nimmt es nicht ab. Es ist die Form, in die Arbeit gegossen wird.

Ein Beispiel für die Art Falle, die es verhindert: eine Kennung, die in drei Dateien zitiert wird und
nirgends definiert ist. Sie sieht aus wie eine Quelle und ist keine. Die weiteren Fallen samt Grund
stehen in `STANDARD.md`.

## Neues Projekt starten

```bash
git clone https://github.com/Donnerlitchen/anderswie-project-template <neues-projekt>
cd <neues-projekt>
rm -rf .git && git init          # sauberer Verlauf, kein geerbtes Template-Log
```

Dann `STANDARD.md` lesen und den Platzhalter `<PROJEKT>` ersetzen (das Datum 2026-10-31
durch das Datum deines Projektstarts) und `CHANGELOG.md` samt `docs/STATUS.md` auf deinen
Startpunkt setzen. Diese Vorlage ist **Fassung 1.3.0** — nenne sie in deinem `README.md`.

**Umgebung:** eigenes venv anlegen (`.venv` — ist ignoriert). Die Regel für das *richtige* Python
steht an einer Stelle in `scripts/projektumgebung.py`; `scripts/gates.sh` nutzt `.venv/bin/python`,
sonst `python3`. Fehlt dort `pytest`, sagt `gates.sh` genau, welcher Befehl die Umgebung anlegt.
Möchtest du einen anderen Interpreter prüfen, setze `PY` von außen.

**Der erste grüne Lauf ist der Startschuss:** `bash scripts/gates.sh` muss bestanden sein,
**bevor** Code entsteht.

## Was hier drin ist

| Datei | Zweck |
|---|---|
| `STANDARD.md` | **Der Standard:** Dateisatz, Mindestinhalte, Fallen, Vorlagen-Version |
| `AGENTS.md` | Verhalten des KI-Agenten (kurz, verweist nur) |
| `CONTRIBUTING.md` | Wie hier gearbeitet wird |
| `CHANGELOG.md` | Änderungsverlauf (Keep a Changelog) |
| `pyproject.toml` | Platzhalter: eine Versionsquelle, `dev`-Extra mit pytest |
| `docs/` | Index, Source of Truth, Policies, Status, Backlog, Versionierung, Gates, Releases, Governance |
| `scripts/gates.sh` | **Ein** Befehl für alle Prüfungen |
| `scripts/check_repo_security.py` | Geheimnis-Prüfung über Arbeitsstand **und** Historie — nennt nie Werte |
| `scripts/muellabfuhr.py` | Meldet Aufräum-Kandidaten — löscht nichts |
| `tests/test_dokumentenordnung.py` | Erzwingt die Ordnung in `docs/` (Datum, Verantwortliche Person, Fristen, Index, Verweise, Wegweiser) |
| `tests/test_dokumentationspflicht.py` | Code geändert ⇒ Changelog mitgezogen (ohne Quellordner still) |

## Herkunft

Entstanden aus dem Projekt *anderswie-product-intelligence*, wo diese Struktur mühsam
nachgezogen werden musste. Jede „Falle" in `STANDARD.md` ist dort real passiert.
