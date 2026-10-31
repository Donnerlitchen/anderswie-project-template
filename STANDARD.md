# Der anderswie-Projektstandard

**Vorlagen-Version:** 1.2.0 · **Stand:** 2026-10-31 · **Verantwortlich:** Ramona

## Übernommene Konventionen (Fassung mitliefern!)

Wir erfinden nichts, was es schon gibt. Jedes Projekt nennt in seinem `README.md`, aus welcher
Vorlagen-Version es stammt.

| Bereich | Konvention | Fassung |
|---|---|---|
| Agenten-Instruktionen | **AGENTS.md** (offener Standard, AAIF-betreut) — Datei im Wurzelverzeichnis, reine Markdown-Anweisung, **unter 100 Zeilen**, Details über „Must-read documents" verweisen | Stand 2026-10 |
| Community-/Repo-Dateien | **GitHub Community Health Files** (`CONTRIBUTING`, `SECURITY`, `SUPPORT`, `CODE_OF_CONDUCT`, Issue-/PR-Vorlagen) | Stand 2026-10 |
| Änderungsverlauf | **Keep a Changelog** | 1.1.0 |
| Versionierung | **SemVer** | 2.0.0 |
| Commit-Betreff | **Conventional Commits** (`feat(bereich):`, `fix(…)`, `docs(…)`, `chore(…)`) | 1.0.0 |
| Entscheidungen (optional) | **ADR** — Architecture Decision Records | Nygard-Format |
| Formatierung | `.editorconfig`, `.gitignore` | — |
| Dokumentenordnung | Kopfzeile mit `Stand` + `Verantwortlich`, Altersfristen, Wegweiser-Prüfung, Aufräum-Bericht — Ideen aus dem Skill **`agent-harness-engineering`** (Herausgeber `yeyitech`, ClawHub) | 0.1.0 (2026-03-08) |

**Übernahmen immer mit Beleg.** Eine fremde Idee wird mit Name, Herausgeber und Fassung genannt —
sonst ist später nicht nachvollziehbar, woher eine Regel stammt. Aus diesem Skill **nicht** übernommen
wurden sein Doku-Schema (`docs/agent/…` — das wäre ein zweiter Doku-Baum neben diesem) und sein
Bootstrap-Skript: es war unvollständig ausgeliefert (die Vorlagen fehlten) und hätte `AGENTS.md` ohne
Rückfrage überschrieben.

**Warum so:** Der Aufbau wird durch **Vorlagen und Werkzeuge** erzwungen, nicht durch guten Willen
(vgl. *Software Engineering Guide*, Kap. 2.14: „Enforce structure with scaffolding and templates,
not with willpower and review comments"). Deshalb ist der Standard ein Repository und kein Notizzettel.

---
# Der Standardsatz für ein anderswie-Projekt

**Zweck:** die kleinste Dateimenge, mit der ein Projekt ab Tag eins prüfbar, versioniert und
nachvollziehbar ist. Jede Zeile „Falle" stammt aus einem real erlebten Fehler.

---

## 1. Wurzel

| Datei | Zweck | Mindestinhalt | Falle |
|---|---|---|---|
| `README.md` | Einstieg | Was das Projekt ist; **Wie man eine neue Sitzung startet** (kurzer Prompt); Verweis auf Index/Source-of-Truth; **keine** Regelwiederholung | Ein Startprompt, der Regeln wiederholt, ist eine zweite Quelle und driftet |
| `AGENTS.md` | Verhalten des Agenten | Rollennotiz, Verweistabelle „Thema → Datei", die Zusatzpflichten (Doku mitziehen, Sitzungswechsel anregen), kurz gehalten | Wird sie voll, ist das ein Zeichen für fehlende Zielorte |
| `CONTRIBUTING.md` | Wie hier gearbeitet wird | Numerierte Regeln: vor der Änderung, Commits, Code-Qualität, Tests und Gegenproben, Versionierung/Release, die Prüfbefehle | Ein **erfundenes** `ENGINEERING.md` ist keine Konvention |
| `CHANGELOG.md` | Änderungsverlauf | Keep-a-Changelog; **jede** Version ein datierter Block; `[Unreleased]` für den Arbeitsstand | Statements, die später falsch wurden, als **datierter Nachtrag** ergänzen — niemals den Release-Block umschreiben |
| `pyproject.toml` / `package.json` | Version, Abhängigkeiten | Die Version als **eine** Quelle; die zweite Stelle im Code (`__version__`) muss dazu passen | Zwei Zahlen, die auseinanderlaufen, fallen erst im Build auf |
| `.gitignore` | Schutz vor Getracktem | `.env`, Daten, `dist/`, `scratch/`, **`.hermes/`**, **`.venv/`** | Nicht ignoriert = Build gesperrt, ohne dass der Grund erkennbar ist. Ein **nicht** ignoriertes `.venv` wandert komplett in die Versionskontrolle — und die README verlangt genau dieses venv |

## 2. `docs/` — die Ordnung selbst

**Kopfzeile für jedes Dokument:** in den ersten Zeilen
`**Stand:** YYYY-MM-DD · **Verantwortlich:** <Name>`. Ein Dokument ohne Namen hat niemanden, der es
aktualisiert. Fristen: Vorgabe 365 Tage, `STATUS.md` und `BACKLOG.md` 90 — maschinell geprüft.

| Datei | Zweck | Mindestinhalt | Falle |
|---|---|---|---|
| `INDEX.md` | Landkarte | Tabelle **„Aktuell und maßgeblich": jede** aktive Datei mit einer Zeile Zweck | Ein neues Dokument ohne Index-Zeile ist unsichtbar — der Wächter-Test erzwingt es |
| `SOT.md` | Wegweiser | „Welche Quelle gilt wofür"; dazu die **Namensordnung**: jede Kennung hat genau eine Bedeutung | „Schritte A–D" und „Phasen A–D" mit anderem Inhalt machen ein Label unauflösbar |
| `POLICIES.md` | Grenzen und Freigaben | Was **ohne Zustimmung** nie passiert; Datenschutz; Wahrheits- und Qualitätsanspruch | Eine Freigabegrenze an zwei Orten ist keine Grenze |
| `STATUS.md` | Überprüfter Ist-Stand | **Datiert**, jüngster Eintrag oben; Zahlen mit Quelle und Zeitpunkt | Veraltete Aussagen („noch nicht gebaut") nach jedem Build/Bump gezielt suchen |
| `BACKLOG.md` | Offene Arbeit | Nur **Offenes**; jeder Abschnitt datiert; je Eintrag Ursache und Ansatz | Ein Abschnitt „historisch", dessen Zeilen wie offene Aufgaben lesen, wird zu Recht entfernt |
| `VERSIONING.md` | Versionen und Tags | Schema; wann gebumpt wird; dass das Tag auf den Release-Commit zeigt | `git add` nie mit `git tag` verketten — ein abgelehntes `add` taggt still den **alten** HEAD |
| `TEST-GATES.md` | Manuelle Nachweise | Die Gates mit Prüfschritt und Akzeptanz; datierte Läufe | Gate-Erfolg heißt geprüfte **Ausgabe**, nicht vorhandenen Code |
| `RELEASES.md` | Bauen, Rollback, Betrieb | Der ausführbare Ablauf; Voraussetzungen; Betriebsfallen; **zwei Versionen** im Kopf (Quellversion **und** laufendes Artefakt) | Ein Kopf, der „läuft" sagt, während das Artefakt mehrere Versionen hinterherhinkt, altert unbemerkt |
| `Spezifikation-<Modul>.md` | Anforderungen je Modul | Eigene ID-Reihe (`VIS`/`KAT`/`SUZ`/`LAB`), ein Punkt je Anforderung | Eine **zitierte** ID, die nirgends definiert ist, sieht wie eine Quelle aus und ist keine |
| `RULE-MODULE-MAP.md` | Regel → Modul → Umsetzung | Je Modul: Spanne, Code, Umsetzungsstand | Kommt eine ID hinzu, ziehen **Spanne und Fließtext** mit |
| `PLAN-<Thema>.md` | Größere Vorhaben | Ziel, Schritte, **was bewusst nicht** getan wird | Ein Plan gehört ins Projekt, **nie** in einen versteckten Agenten-Ordner außerhalb der Versionskontrolle |
| `archive/<thema>/` | Ersetztes und Entwürfe | Banner oben mit Datum und gültigem Nachfolger | Ein Banner, das fehlt, lässt einen Entwurf wie gültig aussehen |

## 3. `scripts/` — die durchsetzbaren Prüfungen

| Datei | Zweck | Mindestinhalt |
|---|---|---|
| `gates.sh` | **Ein** Befehl für alle Prüfungen | Tests, Kompilierung, Whitespace/Diff, Secret-Prüfung, Verhaltenstests der Oberfläche; klares Gesamtergebnis; ändert nichts am Projekt; sagt **vorab**, wenn `pytest` fehlt, statt mit einem Importfehler abzubrechen |
| `projektumgebung.py` | Welches Python gilt | Eine Regel an **einer** Stelle; Skripte starten sich bei falscher Umgebung selbst neu; verglichen wird `sys.prefix`, **nicht** die Datei |
| `check_repo_security.py` | Keine Geheimnisse | Meldet **Pfad und Art** eines Fundes, niemals den Wert; vergleicht zusätzlich mit den Werten einer lokalen `.env`, ohne sie zu drucken; `--history --ref main` prüft die Historie — vor jedem Push Pflicht |
| Dokumentenordnungs-Test (`tests/test_dokumentenordnung.py`) | Die Ordnung erzwingen | Aktive Dokumente datiert **und mit verantwortlicher Person**, Stand innerhalb der Frist, keine Entwürfe im aktiven Ordner, jede aktive Datei im Index, keine toten Links, `AGENTS.md` als kurzer Wegweiser; dazu Namensordnung und Modulkarte |
| `muellabfuhr.py` | Aufräum-Kandidaten **melden** | Überlange Dateien, verdächtige Namen, Arbeitsmarken-Häufungen, Doku ohne Index-Eintrag, Alter der Dokumente; löscht **nie** etwas — Rückgabewert immer 0 |

## 4. Was verdrahtet sein muss, bevor es zählt

Eine Ordnung ohne Prüfung regressiert in der nächsten Sitzung. Diese vier gehören in `gates.sh`:

1. **Dokumentenordnung:** jede aktive Datei datiert **und mit verantwortlicher Person**, im Index
   gelistet, keine Entwurfs-Kennzeichnung, keine toten relativen Links, Stand innerhalb der Frist,
   `AGENTS.md` verweist auf Index und Prüfbefehl und bleibt kurz.
2. **Dokumentationspflicht:** wenn `src/**` (bzw. der Code) geändert wurde, muss der Changelog im
   selben Commit mitgezogen sein. Der Test liest `git status --porcelain`.
3. **Secret-Prüfung** über die Historie.
4. **Verhaltenstests** der Oberfläche, die ohne Browser laufen.

Ein Test kann beweisen, **dass** etwas dokumentiert wurde — nie, dass es **stimmt**. Deshalb steht
Dokumentationspflicht zusätzlich als Regel in der Agenten-Datei, nicht nur als Test.

Der **Aufräum-Bericht** (`scripts/muellabfuhr.py`) gehört bewusst **nicht** in die Gates: er meldet,
er entscheidet nicht. Eine Prüfung, die bei jedem Lauf rot wird, wird abgeschaltet statt gelesen.

## 5. Reihenfolge am ersten Tag

1. `.gitignore` (inkl. `.hermes/`) → 2. `README.md` + `AGENTS.md` → 3. `CONTRIBUTING.md` +
`docs/POLICIES.md` → 4. `docs/INDEX.md` + `docs/SOT.md` → 5. `docs/STATUS.md` + `docs/BACKLOG.md` +
`CHANGELOG.md` → 6. `VERSIONING.md` + `TEST-GATES.md` + `RELEASES.md` → 7. `scripts/gates.sh` +
Dokumentenordnungs-Test → 8. **erst dann** Code.

**Kurz:** Was geprüft wird, steht vor dem, was geprüft werden soll.
