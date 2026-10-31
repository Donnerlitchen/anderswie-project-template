# Contributing

**Gilt für jede Änderung** — von Hand, im Skript oder durch einen KI-Agenten. Eine Regel hat genau
**einen** Ort.

## Wo die Details stehen

| Thema | Datei |
|---|---|
| Fachliche Produktregeln | `rules.md` |
| Sicherheit, Datenschutz, Freigaben | `docs/POLICIES.md` |
| Prüfungen vor einem Commit | `docs/TEST-GATES.md` |
| Versionen, Tags, Changelog | `docs/VERSIONING.md` |
| Builds, Betrieb, Rollback | `docs/RELEASES.md` |
| Aufräumen und Ordnen | `docs/GOVERNANCE.md` |

## 1. Vor jeder Änderung

1. `git status` prüfen und den betroffenen Bereich lesen, bevor etwas geändert wird.
2. Bestehende Datei vorher sichern (`scratch/`, mit Zeitstempel).
3. Eine Sache pro Änderung — keine Sammeländerungen ohne Zwischenkontrolle.

## 2. Arbeitsweise und Commits

4. Kleine Schritte: nach jedem Schritt Diff und Tests prüfen, dann weiter.
5. Fremde Arbeitsstände nie verwerfen und nichts ungefragt committen.
6. Jeder abgenommene Change ist ein **eigener Commit** — nur die zugehörigen Dateien.
7. Keine Historie umschreiben. Kein Push und kein Deployment ohne ausdrückliche Freigabe.
8. Nichts löschen oder überschreiben ohne Zustimmung.
9. Commit-Betreff nach **Conventional Commits**, deutsch, ohne Zugangsdaten und Rohdaten.

## 3. Code-Qualität

10. Eine Verantwortung pro Datei: Import, Erkennung, Validierung und Ausgabe getrennt.
11. Keine Daten im Code — sie liegen in Datenpfaden und Profilen.
12. Abhängigkeiten werden deklariert, nicht vorausgesetzt.
13. Optionale Felder typgeprüft lesen. Fehlende oder `null`-Werte dürfen nie abstürzen.
14. Fehler nennen Schritt und Fehlercode — verständlich, ohne Rohantworten.
15. Keine Zugangsdaten, Token oder vollständigen Rohantworten in Logs, Meldungen oder Anzeige.
16. Zeitlimits, Größenlimits und begrenzte Wiederholungen setzen. Keine Endlosschleifen.
17. Abweisende Dienste (429/503) mit Zurückweichen behandeln und zählen.
18. Unbekanntes bleibt unbekannt: kein stiller Fallback, keine geschätzten Werte als Tatsache.
19. Ein unvollständiger Import darf einen vorhandenen Bestand nie verschlechtern oder verkleinern.
20. Dateien atomar schreiben und vor jeder Mutation sichern.
21. Gleiche Eingabe, gleiches Ergebnis. Zufall nur mit festem Seed.
22. **Eine Regel hat genau einen Ort** — keine Regel in zwei Dateien unterschiedlich formulieren.

## 4. Tests und Nachweis

23. Vor jedem Commit die zutreffenden Gates aus `docs/TEST-GATES.md` ausführen.
24. Ein Health-Check ist kein Funktionsnachweis.
25. Erst messen, dann behaupten: Quelle, Zeitpunkt und Prüfweg nennen.
26. Bei einem Fehler die **Klasse** beheben, nicht nur den Fundort.
27. Jeder gefundene Fehler bekommt einen Test, der ihn künftig verhindert.
28. Keine erfundenen Ergebnisse. Blocker melden statt faken.

**Ein Test zählt erst, wenn er am alten Stand scheitert.** Vor dem Beheben den neuen Test gegen die
**alte** Fassung laufen lassen und den Fehlschlag sehen. Ein Test, der den Fehler durchwinkt, belegt
nichts.

**Testmodus verdeckt die ausgelieferte Strecke.** Läuft die ganze Suite mit einem Schalter
(`TESTING`, Attrappe, Dry-Run), ist der Produktivpfad **ungetestet**. Mindestens ein Test läuft mit
ausgeschaltetem Schalter; danach strukturell prüfen, dass der echte Pfad erreichbar ist.

## 5. Versionierung und Release

29. **Eine** Versionsquelle im Manifest; die zweite Stelle im Code (`__version__`) muss dazu passen.
30. Versionssprung bei jedem abgenommenen Code-Change, im selben Commit. Reine Doku springt nicht.
31. Annotierte Tags `v<version>`. Der Keep-a-Changelog-Block ist die verbindliche Release-Beschreibung.
32. Nach jedem Code-Commit: frischer, commitgebundener Build mit Manifest.
33. Erst offline, dann als laufendes Artefakt prüfen — erst danach ersetzen.
34. Ein fehlgeschlagener Build bleibt sichtbar. „latest" zeigt nie auf ein ungeprüftes Artefakt.

**Falle — Tag und HEAD:** `git add` nie mit `git tag` verketten. Ein abgelehntes `add` bricht die
Kette ab, ein dahinterstehendes `tag` läuft trotzdem und taggt den **alten** HEAD. Nach dem Taggen
zweifach prüfen: `git rev-parse v<version>^{commit}` gleich `git rev-parse HEAD` **und** der Betreff
des getaggten Commits beginnt mit `release: <version>`.

## 6. Kommandos

```bash
bash scripts/gates.sh            # alle Prüfungen auf einmal
python3 scripts/muellabfuhr.py   # Aufräum-Kandidaten ansehen (ändert nichts)
```

Die Regel für das richtige Python steht in `scripts/projektumgebung.py` (`.venv/bin/python`, sonst
`python3`) — Skripte starten sich bei falscher Umgebung selbst neu. Verglichen wird `sys.prefix`,
**nicht** die Datei: `.venv/bin/python` ist ein Verweis auf denselben Basis-Interpreter wie andere Venvs.
