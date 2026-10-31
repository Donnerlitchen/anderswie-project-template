# Test-Gates

**Stand:** 2026-10-31. Automatisierte Gates laufen über `bash scripts/gates.sh`; dieses Dokument hält
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
