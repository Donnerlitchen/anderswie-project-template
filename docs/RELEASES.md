# Builds, Betrieb und Rollback

**Stand:** 2026-10-31.

**Kopf dieses Dokuments nennt zwei Dinge getrennt:** die **Quellversion** (mit Commit) und das
**laufende Artefakt**. Ein Kopf, der „läuft" sagt, während das Artefakt hinterherhinkt, altert
unbemerkt.

## Ablauf

1. Sauberer Arbeitsbaum (`git status --porcelain --untracked-files=normal` **leer**).
2. Build aus genau diesem Commit, mit Version, Commit, Artefakt-ID und Prüfsummen im Manifest.
3. Erst **isoliert** prüfen, dann das laufende Artefakt ersetzen.
4. „latest" **erst nach** der Rückprüfung aktualisieren.
5. Genau **einen** Rückfall behalten; ältere entfernen (samt Abbild, wenn kein Container mehr
   darauf zeigt).

## Betriebsfallen

- **Ein loser, unversionierter Ordner im Baum sperrt jeden commitgebundenen Build** — obwohl er gar
  nicht ins Artefakt könnte. Bei „Build gesperrt" zuerst `git status` prüfen, nicht den Code.
- **Zählen, nicht schätzen.** Bei `podman` zeigt `podman images` nur markierte Abbilder;
  `podman images -a` und `podman system df` zählen Zwischenschichten mit (real: 9 gegen 80). Eine
  Zahl aus einer gekürzten Auflistung ist falsch. „RECLAIMABLE" ist **nicht** der frei werdende
  Plattenplatz — vorher/nachher mit `du`/`df` messen, beide Zahlen getrennt nennen.
- **Nicht ersetzen, solange eine Messung läuft** — der Wechsel schneidet den Lauf ab.
