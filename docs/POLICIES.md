# Policies — Grenzen, Freigaben und Ansprüche

**Stand:** 2026-10-31 · **Verantwortlich:** Ramona.

## 1. Freigabevorbehalte

Ohne ausdrückliche Zustimmung passiert **nichts** von Folgendem:

- Push, Veröffentlichung oder Deployment
- Kostenpflichtige API- oder Modellaufrufe
- Löschen oder Überschreiben von Dateien
- Änderungen an Regeln, Architektur oder Datenmodell
- Bau oder Umbau der Oberfläche
- Externer Versand: E-Mail, Posts, Uploads
- Umschreiben bestehender Git-Historie

## 2. Datenschutz und Git

- `.env`, Schlüssel, Passwörter, Uploads und Rohdaten werden **nicht** getrackt.
- `.gitignore` schützt nur Ungetracktes. Vor einer Veröffentlichung zusätzlich Diff, Historie und
  Nutzungsrechte bereits verfolgter Bilder und Daten prüfen.
- Bestehende Historie nicht eigenmächtig umschreiben.

## 3. Wahrheit und Belege

- Keine erfundenen oder abgeschriebenen Ergebnisse, wenn ein Aufruf fehlschlägt.
- Unbeobachtetes bleibt `null`/leer — kein geschätzter Wert als Tatsache.
- Zahlen brauchen Quelle, Zeitpunkt und Prüfweg.

## 4. Abnahme

Regeln, Architektur und Datenmodell brauchen die **inhaltliche Abnahme** durch die Projektleitung.
