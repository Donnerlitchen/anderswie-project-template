# Agentenregeln – <PROJEKT>

**Rolle dieser Datei:** Sie sagt einem KI-Agenten, wie er sich hier verhält — **kurz**. Alles
Inhaltliche steht in den Fachdateien; diese Datei verweist nur („eine Regel hat genau einen Ort").

## Zuerst lesen

[README.md](README.md) → [docs/INDEX.md](docs/INDEX.md) → [docs/SOT.md](docs/SOT.md) →
[docs/STATUS.md](docs/STATUS.md) → [docs/BACKLOG.md](docs/BACKLOG.md)

## Prüfen

Alle Prüfungen auf einmal: [`bash scripts/gates.sh`](scripts/gates.sh). Der Lauf muss grün sein,
**bevor** etwas als fertig gilt — Prüfschritte und Nachweise stehen in
[docs/TEST-GATES.md](docs/TEST-GATES.md).

## Verbindliche Regelwerke

| Thema | Datei |
|---|---|
| Arbeitsweise, Code-Qualität, Tests, Versionierung, Release | `CONTRIBUTING.md` |
| Grenzen, Freigaben, Datenschutz, Wahrheitsanspruch | `docs/POLICIES.md` |
| Prüfungen vor einem Commit | `docs/TEST-GATES.md` |
| Fachliche Regeln, Modulanforderungen | `rules.md`, `docs/Spezifikation-<Modul>.md` |
| Aufräumen, Ordnen, Regelwerk prüfen | `docs/GOVERNANCE.md` |

## Was der Agent zusätzlich beachtet

1. **Lesen vor ändern.** `git status` und die betroffenen Dateien, bevor etwas passiert.
2. **Bei Unklarheit fragen** statt annehmen — Ziel, Datenquelle oder Erlaubnis.
3. **Nichts ohne Freigabe ändern:** Regeln, Architektur und Datenmodell brauchen die inhaltliche
   Abnahme; Löschen und Überschreiben ebenso (`docs/POLICIES.md` §1).
4. **Dokumentation mitziehen — nach jedem größeren Thema.** Datierter Stand in `docs/STATUS.md`,
   offene Arbeit in `docs/BACKLOG.md`, Änderung in `CHANGELOG.md`. Was nur im Chat steht, ist mit
   der nächsten Sitzung weg.
5. **Keine erfundenen Ergebnisse.** Scheitert ein Aufruf, wird der Blocker gemeldet.
6. **Keine Kennung ohne Beleg** (Regel-IDs, Versionen): erst im besitzenden Dokument nachschlagen.
7. **Projektdateien bleiben im Projekt** — keine Agenten-Notizen im Baum; `.hermes/` ist ignoriert,
   Pläne gehören nach `docs/PLAN-<Thema>.md`.
8. **Sprache:** Deutsch, klar, ohne Jargon. Zahlen mit Quelle und Zeitpunkt.
9. **Eine Sitzung pro Thema.** Ist ein Thema durch, den Wechsel anregen — mit Namensvorschlag und
   Verweis auf den Startprompt in `README.md`.
