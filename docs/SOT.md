# Source of Truth — welche Quelle gilt wofür

**Stand:** 2026-10-31 · **Verantwortlich:** Ramona.

| Frage | Antwort steht in |
|---|---|
| Wie arbeite ich hier? | `CONTRIBUTING.md` |
| Was ist fachlich gewollt? | `rules.md`, `docs/Spezifikation-<Modul>.md` |
| Was ist **überprüft** gebaut? | `docs/STATUS.md` (datiert) — Code und Tests sind maßgeblich |
| Was ist als Nächstes zu tun? | `docs/BACKLOG.md` |
| Welche Grenzen brauchen Freigabe? | `docs/POLICIES.md` |
| Wie sieht der Zielaufbau aus? | `architecture.md` (Zielbild, **nicht** Ist-Stand) |

## Dokumentenordnung

Diese Regeln gelten für **jedes** Dokument in `docs/` — sie sind maschinell geprüft
(`tests/test_dokumentenordnung.py`), nicht nur gemeint.

| Regel | Was gilt |
|---|---|
| Kopfzeile | In den ersten Zeilen: `**Stand:** YYYY-MM-DD · **Verantwortlich:** <Name>` |
| Frist | Vorgabe 365 Tage; `STATUS.md` und `BACKLOG.md` 90 Tage; ein Stand-Datum in der Zukunft ist ein Fehler |
| Wegweiser | `AGENTS.md` **verweist** und wiederholt nicht; er bleibt kurz (Grenze 120 gefüllte Zeilen) |
| Index | Jede aktive Datei steht im `INDEX.md` unter „Aktuell und maßgeblich" |
| Archiv | Ersetztes und Entwürfe nach `docs/archive/`, mit Banner aus Datum und Nachfolger |
| Verweise | Kein relativer Verweis auf etwas, das es nicht gibt |

Der Aufräum-Bericht (`scripts/muellabfuhr.py`) **meldet** Kandidaten; er entscheidet nichts und löscht
nichts. Die Fristen stehen an genau einer Stelle: oben im Prüfskript.

## Namensordnung

**Ein Name hat genau eine Bedeutung.** Diese Tabelle ist die einzige Quelle für Kennungen. Freie
Buchstaben für Schritte sind verboten — zwei Dokumente mit „Schritte A–D" unterschiedlichen Inhalts
machen ein Label unauflösbar.

| Familie | Schema | Beispiel |
|---|---|---|
| Version | SemVer | `1.4.0` |
| Plan-Schritte | `M1…Mn` | `M3` |
| Regel-IDs | `<MODUL>-<nr>` | `VIS-01`, `KAT-12` |
| Abnahmetests | `AT-01…` | `AT-03` |
| Gates | `G0…Gn` | `G1` |
