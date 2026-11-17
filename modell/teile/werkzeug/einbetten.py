"""Packt die .glb-Dateien in JavaScript-Dateien (Base64).
So lädt das 3D-Modell die Teile auch, wenn die HTML-Datei direkt
per Doppelklick (file://) geöffnet wird – dort darf der Browser keine
.glb-Dateien nachladen, Skripte aber schon.

  modell/teile/*.glb        -> modell/teile/teile.js        (kommt ins Git, frei nutzbare Modelle)
  modell/teile/lokal/*.glb  -> modell/teile/lokal/teile-lokal.js  (NICHT im Git, z. B. GrabCAD-Modelle)

Aufruf:  python einbetten.py
"""
import base64, pathlib

teile = pathlib.Path(__file__).resolve().parent.parent


def packen(ordner, ziel):
    zeilen = ["// Automatisch erzeugt von werkzeug/einbetten.py – nicht von Hand ändern.",
              "window.RC_TEILE = window.RC_TEILE || {};"]
    for glb in sorted(ordner.glob("*.glb")):
        b64 = base64.b64encode(glb.read_bytes()).decode("ascii")
        zeilen.append(f'window.RC_TEILE["{glb.stem}"] = "{b64}";')
        print(f"  {glb.name}: {glb.stat().st_size // 1024} KB")
    ziel.write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    print(f"{ziel.relative_to(teile.parent)} geschrieben")


packen(teile, teile / "teile.js")
if (teile / "lokal").is_dir():
    packen(teile / "lokal", teile / "lokal" / "teile-lokal.js")
