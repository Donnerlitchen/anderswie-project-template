# Versionierung und Releases (SemVer)

**Stand:** 2026-10-31 · **Verantwortlich:** Ramona. Richtlinie: [SemVer 2.0.0](https://semver.org/lang/de/).

| Stufe | Wann |
|---|---|
| MAJOR | Bruch von Ergebnisvertrag, Schema oder öffentlicher API |
| MINOR | neue Fähigkeit, neuer Endpunkt, Umbau der Oberfläche |
| PATCH | Fehlerbehebung ohne Verhaltensänderung |

- **Eine** Versionsquelle (Manifest); die zweite Stelle im Code muss dazu passen — im **selben** Commit.
- Bump gehört zum abgenommenen Code-Change. Reine Doku-Commits bumpen nicht.
- Annotierte Tags `v<version>`; der Tag zeigt auf den **Release-Commit**, dessen Betreff mit
  `release: <version>` beginnt. Zweifach prüfen: `git rev-parse v<version>^{commit}` gleich
  `git rev-parse HEAD` **und** der Betreff.
- Der Keep-a-Changelog-Block ist die verbindliche Release-Beschreibung; die Tag-Nachricht nur die Kurzform.
