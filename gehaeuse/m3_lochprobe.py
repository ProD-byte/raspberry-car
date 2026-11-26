"""Raspberry Car – Lochprobe M3 (Werkzeug, kommt nicht ins Auto)

Zum Ausprobieren, welche Lochgröße mit dem eigenen Filament und Drucker am besten passt
(PLA und PETG drucken Löcher unterschiedlich eng). Ein kleiner Block mit zwei Reihen Löchern:

  * oben im Block: Löcher HOCH (senkrecht gedruckt, wie die Schraubdome und Säulen),
  * in der Wand dahinter: Löcher QUER (waagerecht gedruckt, wie die Schutzblech-Säulen),
  Löcher von 2,8 bis 3,2 mm in 0,1-mm-Schritten.
  Die Zahl über bzw. vor jedem Loch ist sein Durchmesser in der CAD-Zeichnung (in mm).

Die Lochmaße der Skripte stehen in loecher.py (je Filament, hoch und quer).
Testen: eine M3-Schraube (ca. 8 mm lang) in jedes Loch drehen. Gutes Kernloch: Schraube geht mit dem
Inbus ohne Gewalt rein und sitzt danach fest (dreht nicht durch). Gutes Durchgangsloch: Schraube fällt
fast durch, wackelt aber nicht viel.

Druck: so wie er liegt, ohne Stützen, gleiches Filament und gleiche Einstellungen wie die echten Teile
(Wände, Düse, Temperatur) – sonst sagt die Probe nichts aus. Ca. 44 × 28 × 24 mm, wenige Minuten.

Aufruf:  python m3_lochprobe.py   → erzeugt lochprobe/m3_lochprobe.stl und .step
"""
from pathlib import Path
from build123d import Box, Cylinder, Text, Pos, Rot, extrude, export_stl, export_step, Plane

LOECHER = [2.8, 2.9, 3.0, 3.1, 3.2]            # Durchmesser der Probelöcher (seit 25.11.2026 nur dieser Bereich)
TEILUNG, RAND = 8.0, 6.0                       # Abstand der Löcher, Rand
BLOCK = (20.0, 12.0)                           # Block vorne: Tiefe (y), Höhe (z) – Löcher HOCH
WAND = (8.0, 24.0)                             # Wand hinten: Dicke (y), Höhe (z) – Löcher QUER
QUER_Z = 17.0                                  # Höhe der waagerechten Löcher (Schraubenkopf geht über den Block)
SCHRIFT, TIEF = 3.2, 0.6                       # Schriftgröße, Tiefe der Gravur

AUS = Path(__file__).resolve().parent / "lochprobe"


def lage(loecher=LOECHER, teilung=TEILUNG, vorne=0.0):
    """x-Positionen und Durchmesser aller Löcher (vorne = Platz für die Kennung links)."""
    pos = [(vorne + RAND + i * teilung, d) for i, d in enumerate(loecher)]
    return pos, vorne + 2 * RAND + (len(loecher) - 1) * teilung


def zahl(d):
    return f"{d:.1f}".replace(".", ",")


def gravur(text, x, y, z, schrift=SCHRIFT, drehen=0):
    """Text auf eine nach oben zeigende Fläche (Höhe z) eingravieren."""
    return Pos(x, y, z - TIEF) * Rot(0, 0, drehen) * extrude(Text(text, schrift), TIEF + 0.1)


def teil(loecher=LOECHER, teilung=TEILUNG, schrift=SCHRIFT, kennung=None):
    """Lochprobe bauen. kennung (z. B. „M2“) wird links groß auf den Block graviert."""
    vorne = 8.0 if kennung else 0.0
    pos, laenge = lage(loecher, teilung, vorne)
    by, bz = BLOCK
    wy, wz = WAND
    t = Pos(laenge / 2, by / 2, bz / 2) * Box(laenge, by, bz)
    t += Pos(laenge / 2, by + wy / 2, wz / 2) * Box(laenge, wy, wz)
    for x, d in pos:
        # HOCH: senkrecht durch den Block
        t -= Pos(x, 7.0, bz / 2) * Cylinder(d / 2, bz + 2)
        t -= gravur(zahl(d), x, 15.5, bz, schrift)
        # QUER: waagerecht durch die Wand
        t -= Pos(x, by + wy / 2, QUER_Z) * Rot(90, 0, 0) * Cylinder(d / 2, wy + 2)
        t -= gravur(zahl(d), x, by + wy / 2, wz, schrift)
    if kennung:   # quer gestellt, damit auch „M2,5“ in den schmalen Streifen passt
        t -= gravur(kennung, RAND - 0.5, by / 2, bz, 4.0, drehen=90)
    return t, laenge


if __name__ == "__main__":
    AUS.mkdir(exist_ok=True)
    t, laenge = teil()
    print(f"Lochprobe M3: {laenge:.0f} × {BLOCK[0] + WAND[0]:.0f} × {WAND[1]:.0f} mm, Volumen {t.volume / 1000:.1f} cm³")
    print("Löcher:", ", ".join(zahl(d) for d in LOECHER))
    export_stl(t, str(AUS / "m3_lochprobe.stl"), tolerance=0.01, angular_tolerance=0.1)
    export_step(t, str(AUS / "m3_lochprobe.step"))
    print("geschrieben:", AUS / "m3_lochprobe.stl")
