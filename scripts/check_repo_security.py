#!/usr/bin/env python3
"""Geheimnis-Prüfung: meldet **Pfade und Arten** möglicher Funde — niemals die Werte.

Aufruf aus dem Projektordner:

    python3 scripts/check_repo_security.py                        # getrackte + unversionierte Dateien
    python3 scripts/check_repo_security.py --history --ref main    # zusätzlich die ganze Historie

`--history` gehört **vor jeden Push und jedes Release**: eine Datei aus dem Arbeitsstand zu löschen
entfernt sie **nicht** aus der Historie. Genau dort bleiben alte Schlüssel liegen.

Warum nur Pfade: Eine Prüfung, die einen Wert ausgibt, hat ihn damit in ein Log und in eine
Kommandozeile geschrieben. Verglichen wird deshalb auch mit den Werten aus einer lokalen `.env` —
die bleiben aber im Arbeitsspeicher und werden nie gedruckt.

Rückgabewert: 0 = grün, 1 = Fund, 2 = nicht prüfbar (kein Git). Rechte an Bildern, Rohdaten und
Fremdinhalten sind eine eigene, **manuelle** Freigabe (`docs/POLICIES.md` §1) — das kann kein
Skript entscheiden.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[1]

# Erkannt wird die **Art** des Fundes, nicht der Wert. Reihenfolge ändert nichts, gesammelt wird als Menge.
MUSTER = {
    "privater_schluessel": re.compile(rb"-----BEGIN (?:OPENSSH|RSA|EC|DSA|ENCRYPTED )?PRIVATE KEY-----"),
    "google_schluessel": re.compile(rb"AIza[A-Za-z0-9_-]{30,}"),
    "openai_schluessel": re.compile(rb"sk-[A-Za-z0-9_-]{20,}"),
    "github_token": re.compile(rb"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "aws_zugangsschluessel": re.compile(rb"AKIA[0-9A-Z]{16}"),
}

# Ab dieser Länge wird ein Wert aus der .env überhaupt verglichen — kurze Werte erzeugen Zufallstreffer.
MINDESTLAENGE = 8


def git(*argumente: str) -> bytes:
    return subprocess.run(["git", *argumente], cwd=WURZEL, check=True, capture_output=True).stdout


def lokale_werte() -> dict[str, bytes]:
    """Werte aus der lokalen `.env` — nur im Arbeitsspeicher, nie gedruckt, nie gespeichert."""
    env_datei = WURZEL / ".env"
    if not env_datei.is_file():
        return {}
    werte: dict[str, bytes] = {}
    for zeile in env_datei.read_text(encoding="utf-8").splitlines():
        if "=" not in zeile or zeile.lstrip().startswith("#"):
            continue
        schluessel, wert = zeile.split("=", 1)
        if any(wort in schluessel.upper() for wort in ("KEY", "TOKEN", "PASSWORD", "SECRET")):
            wert = wert.strip().strip("\"'")
            if len(wert) >= MINDESTLAENGE:
                werte[schluessel] = wert.encode("utf-8")
    return werte


def pruefe(inhalt: bytes, werte: dict[str, bytes]) -> list[str]:
    arten = [art for art, muster in MUSTER.items() if muster.search(inhalt)]
    arten += ["entspricht_lokalem_" + name for name, wert in werte.items() if wert in inhalt]
    return sorted(set(arten))


def befunde_im_arbeitsstand(werte: dict[str, bytes]) -> list[tuple[str, str]]:
    befunde = []
    rohe = git("ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0")
    for roh in sorted(filter(None, rohe)):
        name = roh.decode("utf-8", errors="replace")
        datei = WURZEL / name
        if not datei.is_file():
            continue
        if re.search(r"(^|/)\.env(?:\.|$)", name) and name != ".env.example":
            befunde.append((name, "getrackte_env_datei"))
        for art in pruefe(datei.read_bytes(), werte):
            befunde.append((name, art))
    return befunde


def befunde_in_der_historie(ref: str | None, werte: dict[str, bytes]) -> list[tuple[str, str]]:
    befunde = []
    gesehen: set[str] = set()
    zeilen = git("rev-list", "--objects", ref or "--all").decode("utf-8", errors="replace").splitlines()
    for zeile in zeilen:
        objekt, _, name = zeile.partition(" ")
        if objekt in gesehen:
            continue
        if git("cat-file", "-t", objekt).strip() != b"blob":
            continue
        gesehen.add(objekt)
        for art in pruefe(git("cat-file", "blob", objekt), werte):
            befunde.append(("HISTORIE:" + name, art))
    return befunde


def main() -> int:
    zerleger = argparse.ArgumentParser(description="Meldet mögliche Geheimnisse. Gibt niemals Werte aus.")
    zerleger.add_argument("--history", action="store_true", help="zusätzlich alle erreichbaren Git-Blobs prüfen")
    zerleger.add_argument("--ref", help="nur diesen Ref prüfen (z. B. main); erfordert --history")
    args = zerleger.parse_args()
    if args.ref and not args.history:
        zerleger.error("--ref erfordert --history")

    try:
        git("rev-parse", "--git-dir")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("NICHT PRÜFBAR: hier ist kein Git-Repository (oder git fehlt).", file=sys.stderr)
        return 2

    werte = lokale_werte()
    befunde = befunde_im_arbeitsstand(werte)
    if args.history:
        befunde += befunde_in_der_historie(args.ref, werte)

    for name, art in sorted(set(befunde)):
        print(f"BLOCKIERT: {name} [{art}]")
    print(f"Geprüft: Arbeitsstand{'' if not args.history else ' + Historie'}"
          f"{' (Ref ' + args.ref + ')' if args.ref else ''} · {len(werte)} lokale Werte zum Vergleich")
    print("Geheimnis-Prüfung:", "ROT — erst bereinigen, dann weiter" if befunde else "GRÜN")
    return 1 if befunde else 0


if __name__ == "__main__":
    raise SystemExit(main())
