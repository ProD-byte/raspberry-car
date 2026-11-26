"""Raspberry Car – Wellenprobe für die 4-mm-D-Welle der Motoren (Werkzeug, kommt nicht ins Auto)

Ein kleiner Block mit 7 D-förmigen Löchern in verschiedenen Größen. Damit findest du heraus, welche Bohrung in der
Felge (rad.py) am besten auf die Motorwelle passt. Die Löcher stehen beim Druck senkrecht, genau wie in der Felge.

  * Zahl hinter jedem Loch = Durchmesser in der CAD-Zeichnung (mm). Die flache Seite wächst mit
    (Maß über die Fläche = Zahl − 0,5).
  * Flache Seite der Löcher zeigt zur Beschriftung hin.

Testen: Probe auf die Welle eines Motors stecken (flache Seite der Welle zur Beschriftung).
  Gutes Loch: geht mit leichtem Druck drauf, wackelt nicht und dreht nicht durch.
  Für die Felge darf es eher eine Spur lockerer sein, weil die Klemmschraube die Nabe noch zuzieht.
  Sag dann die Zahl – sie wird in rad.py eingetragen (BOHRUNG).

Druck: so wie es liegt, ohne Stützen, gleiches Filament und gleiche Einstellungen wie die Felge.

Aufruf:  python wellenprobe.py   → lochprobe/wellenprobe.stl und .step
"""
from build123d import Box, Cylinder, Pos, export_stl, export_step
import m3_lochprobe as lp
from rad import WELLE_D, WELLE_FLACH

BOHRUNGEN = [4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6]
TEILUNG, RAND = 9.0, 6.5
TIEFE, HOEHE = 20.0, 10.0          # Block (y), Höhe (z) – die Welle steckt in der Felge 8,5 mm
LOCH_Y, SCHRIFT_Y = 8.0, 16.0


def d_loch(x, d):
    """D-Loch: Kreis mit Fläche zur +y-Seite (zur Beschriftung)."""
    flach = WELLE_FLACH - WELLE_D / 2 + (d - WELLE_D) / 2      # Abstand der Fläche von der Mitte
    kreis = Pos(x, LOCH_Y, HOEHE / 2) * Cylinder(d / 2, HOEHE + 2)
    rest = Pos(x, LOCH_Y + flach - d, HOEHE / 2) * Box(d + 2, 2 * d, HOEHE + 2)   # alles unterhalb der Fläche
    return kreis & rest


def teil():
    laenge = 2 * RAND + (len(BOHRUNGEN) - 1) * TEILUNG
    t = Pos(laenge / 2, TIEFE / 2, HOEHE / 2) * Box(laenge, TIEFE, HOEHE)
    for i, d in enumerate(BOHRUNGEN):
        x = RAND + i * TEILUNG
        t -= d_loch(x, d)
        t -= lp.gravur(lp.zahl(d), x, SCHRIFT_Y, HOEHE)
    return t, laenge


if __name__ == "__main__":
    lp.AUS.mkdir(exist_ok=True)
    t, laenge = teil()
    print(f"Wellenprobe: {laenge:.0f} × {TIEFE:.0f} × {HOEHE:.0f} mm, Volumen {t.volume / 1000:.1f} cm³")
    print("Bohrungen:", ", ".join(f"{lp.zahl(d)} (Fläche {lp.zahl(d - 0.5)})" for d in BOHRUNGEN))
    export_stl(t, str(lp.AUS / "wellenprobe.stl"), tolerance=0.01, angular_tolerance=0.1)
    export_step(t, str(lp.AUS / "wellenprobe.step"))
