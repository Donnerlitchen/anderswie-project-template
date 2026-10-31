# Source of Truth — welche Quelle gilt wofür

**Stand:** 2026-10-31.

| Frage | Antwort steht in |
|---|---|
| Wie arbeite ich hier? | `CONTRIBUTING.md` |
| Was ist fachlich gewollt? | `rules.md`, `docs/Spezifikation-<Modul>.md` |
| Was ist **überprüft** gebaut? | `docs/STATUS.md` (datiert) — Code und Tests sind maßgeblich |
| Was ist als Nächstes zu tun? | `docs/BACKLOG.md` |
| Welche Grenzen brauchen Freigabe? | `docs/POLICIES.md` |
| Wie sieht der Zielaufbau aus? | `architecture.md` (Zielbild, **nicht** Ist-Stand) |

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
