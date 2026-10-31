# Test-Gates

**Stand:** 2026-10-31 · **Verantwortlich:** Ramona. Automatisierte Gates laufen über `bash scripts/gates.sh`; dieses Dokument hält
die **manuellen** Nachweise mit Datum. Maßgeblich ist der jüngste Eintrag oben.

| Gate | Prüfschritt | Akzeptanz |
|---|---|---|
| G0 Repository | `git status --short`, `git diff --check`, unversionierte Dateien und Secrets **ohne Werte auszugeben** prüfen | sauberer Stand vor dem Commit |
| G1 Lokal | Tests + Kompilierung | exakte Zahl nennen (bestanden/gesamt) |
| G2 Vertrag | Ergebnis-/Schnittstellenvertrag gegen Schema und Tests | Offline-Tests grün |
| G3 Ende-zu-Ende | echter Durchlauf bis zum Ergebnis | nur mit ausdrücklicher Freigabe für externe Aufrufe |
| G4 Sicherheit/Release | Secret-Prüfung über **alle** Refs | grün; kein Push ohne Freigabe |
| G5 Build | commitgebundenes Artefakt mit Manifest | Inhalt ohne Secrets/Daten, Version und Commit gebunden |

Ein Gate-Erfolg bedeutet **geprüfte Ausgabe**, nicht vorhandenen Code.

## Automatisch geprüft (in `gates.sh` enthalten)

Die **Dokumentenordnung**: Stand-Datum **und** verantwortliche Person in der Kopfzeile, Stand innerhalb
der Frist, Index-Eintrag, keine Entwürfe im aktiven Ordner, keine toten Verweise, `AGENTS.md` als
kurzer Wegweiser auf Index und Prüfbefehl. Einzelheiten in `docs/SOT.md`, Abschnitt Dokumentenordnung.

## Sichtung, kein Gate

    python3 scripts/muellabfuhr.py

Meldet Aufräum-Kandidaten (überlange Dateien, verdächtige Namen, Arbeitsmarken-Häufungen, Doku ohne
Index-Eintrag) und ändert nichts. Monatlich und vor einem Release ansehen; entschieden wird einzeln.
