#!/usr/bin/env bash
# gates.sh – führt alle Prüfungen aus CONTRIBUTING.md (Abschnitt 8) nacheinander aus.
#
# Warum: Die Prüfungen sind beschrieben, aber man muss an jede einzeln denken. Dieses
# Skript geht die Liste ab wie eine Startcheckliste und meldet am Ende ein klares
# Ergebnis. Aufruf aus dem Projektordner:
#
#     bash scripts/gates.sh
#
# Es ändert nichts am Projekt. Es liest, prüft und berichtet.

set -u

cd "$(dirname "$0")/.." || {
  echo "FEHLER: Projektordner nicht gefunden." >&2
  exit 2
}

# Python aus der Projektumgebung, sonst das System-Python.
# Eine von außen gesetzte PY hat Vorrang — für CI oder eine Gegenprobe mit anderem Interpreter.
if [ -z "${PY:-}" ]; then
  PY=".venv/bin/python"
  [ -x "$PY" ] || PY="python3"
fi

# Ohne pytest ist der Testschritt nicht ausführbar. Dann fehlt die Umgebung, nicht der Test —
# eine kryptische Importmeldung hilft niemandem.
if ! "$PY" -c "import pytest" >/dev/null 2>&1; then
  echo "FEHLER: $PY hat kein pytest — die Projektumgebung fehlt." >&2
  echo "        Anlegen mit:  python3 -m venv .venv && .venv/bin/pip install pytest" >&2
  exit 2
fi

fehler=0
nummer=0

lauf() {
  nummer=$((nummer + 1))
  name="$1"
  shift
  printf '\n[%d] %s\n' "$nummer" "$name"
  if "$@" > /tmp/gates-ausgabe.txt 2>&1; then
    printf '    ok\n'
    return 0
  else
    printf '    FEHLGESCHLAGEN\n'
    sed 's/^/    | /' /tmp/gates-ausgabe.txt | tail -20
    fehler=$((fehler + 1))
    return 1
  fi
}

echo "Prüfungen für $(basename "$(pwd)")"
echo "Arbeitsordner: $(pwd)"

lauf "Tests"                 "$PY" -m pytest -q
export PY
lauf "Kompilierung"          bash -c 'for d in src tests scripts; do [ -d "$d" ] || continue; "$PY" -m compileall -q "$d" || exit 1; done' 
lauf "Whitespace und Format" git diff --check
if [ -f scripts/check_repo_security.py ]; then
  lauf "Secret-Prüfung"        "$PY" scripts/check_repo_security.py --history --ref main
else
  echo
  echo "[!] Secret-Prüfung übersprungen – scripts/check_repo_security.py fehlt (noch zu übernehmen)."
fi

# Node-Tests der Oberfläche (Verhalten, ohne Browser) – nur wenn node vorhanden.
if command -v node >/dev/null 2>&1; then
  lauf "UI-Tests (Node)" bash -c 'set -e; for f in tests/*.cjs; do [ -e "$f" ] || continue; echo "-- $f"; node "$f"; done'
else
  echo
  echo "[!] UI-Tests (Node) übersprungen – node ist nicht im PATH."
fi

echo
if [ "$fehler" -eq 0 ]; then
  echo "ALLE PRÜFUNGEN BESTANDEN"
  echo "Hinweis: Der Container-Smoke-Test (Image bauen und starten) ist NICHT enthalten –"
  echo "         der gehört zum Build, siehe docs/RELEASES.md."
  rm -f /tmp/gates-ausgabe.txt
  exit 0
else
  echo "$fehler von $nummer Prüfungen FEHLGESCHLAGEN – bitte zuerst reparieren."
  rm -f /tmp/gates-ausgabe.txt
  exit 1
fi
