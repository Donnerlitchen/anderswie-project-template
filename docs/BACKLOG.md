# Offene Arbeit

Nur **Offenes**. Jeder Abschnitt datiert; jede Zeile ist eindeutig offen, teilweise fertig oder
fertig. Erledigtes wird **mit Beleg** (Version, Test, Messung) durchgestrichen, nicht gelöscht.

**Stand:** 2026-10-31 · **Verantwortlich:** Ramona

## Offen — Stand 2026-10-31

1. <Vorhaben>: Ursache, Ansatz, was es braucht. *(Platzhalter aus der Vorlage — beim ersten echten
   Vorhaben ersetzen.)*

**Erledigt — Stand 2026-10-31** (durchgestrichen, nicht gelöscht — so bleibt die Entscheidung lesbar)

- ~~`docs/GOVERNANCE.md` ist überwiegend **englisch** — das widerspricht der Sprachregel in `AGENTS.md`.
  Übersetzen in einem eigenen Schritt; es ist ein langer Fachtext, kein Häppchen.~~
  **Entschieden am 2026-10-31 (Ramona): die englischen Fachabschnitte bleiben englisch.** Die
  Sprachregel gilt für die **eigenen** Texte eines Projekts; diese beiden Dokumente sind gewachsene
  Verfahrenstexte in ihrer Originalsprache, und kein Projekt muss sie mitführen. Beleg:
  [`CHANGELOG.md`](../CHANGELOG.md), Abschnitt „Entschieden (2026-10-31)".

- **Neu (2026-10-31): `VERSIONING.md` verlangt annotierte Tags `v<version>` auf einem Release-Commit,
  dessen Betreff mit `release: <version>` beginnt — dieses Repository hat für 1.0.0, 1.1.0, 1.2.0 und
  1.3.0 keinen einzigen Tag.** Entweder gilt die Tag-Regel auch hier — dann fehlen vier Tags **und** je
  Fassung ein Commit mit dem Betreff `release: <version>` — oder die Regel gehört auf Projekte mit
  Artefakt eingegrenzt (dieses Repository baut nichts). **Nicht** nachträglich getaggt: ein Tag auf
  einen Commit mit anderem Betreff würde genau die Prüfung verletzen, die die Regel verlangt. Die
  Entscheidung liegt bei Ramona.
