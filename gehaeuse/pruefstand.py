"""Raspberry Car – Prüfstand für das Fahrwerk (Ebene 1)

Das Auto wird wie auf einer Hebebühne auf 4 Stempel gesetzt: Unten im Wannenboden sind 4 Kerben
(8 × 6 mm, 3 mm tief: hinten unter dem Akku, vorne unter der Stromversorgung). Auf jedem Stempel sitzt ein kleiner Zapfen, der in seine
Kerbe einrastet. Die Räder hängen dann 19 mm über dem Tisch und können frei drehen – zum Testen
von Motoren, Encodern, Motortreibern und Software, ohne dass das Auto vom Tisch fährt.

Einteilig, ohne Schrauben. Alle Maße in mm. Erzeugt STL und STEP in gehaeuse/pruefstand/.

Aufruf (einmalig: pip install build123d):
    python pruefstand.py

Koordinaten wie im 3D-Modell (x nach vorne, z nach links, y nach oben), aber y = 0 ist hier die
Tischplatte und x = 0 / z = 0 liegt genau in der Mitte der vier Kerben (in der Wanne bei x = PRUEF_MITTE = 3,5).

Aufbau:
  * Sockelplatte mit Fase und Schriftzug, in der Mitte offen,
  * zwei Querwände (unten breit, oben 12 mm) mit Fenstern,
  * oben auf jeder Wand zwei Stempel mit Zapfen (0,3 mm Luft zur Kerbe, oben angefast).
  Zwischen den Stempeln bleiben 2 mm Luft zum Wannenboden – das Auto liegt nur auf den Stempeln.

Druck: so wie er steht (Unterseite aufs Bett), ohne Stützen. 124 × 124 mm – passt auf jedes
Druckbett. PLA oder PETG, 3 Wände, 15 % Füllung reicht.
"""
from pathlib import Path
from build123d import (Box, Plane, Polygon, Rectangle, RectangleRounded, Text, Pos, Rot,
                       extrude, chamfer, Axis, export_stl, export_step)

# ------------------------------------------------------------------ Maße der Wanne (aus ebene1_fahrwerk.py)
BODEN_UNTEN = 16.0                     # Wannenboden über dem Boden, wenn das Auto auf den Rädern steht
PRUEF_HX, PRUEF_HZ = 36.5, 40.0       # wie in ebene1_fahrwerk.py (PRUEF_HX, PRUEF_HZ) – bei Änderung beide gleich halten
PRUEF_MITTE = 3.5                      # Mitte der Kerben in der Wanne (x)
PRUEF_PUNKTE = [(sx * PRUEF_HX, sz * PRUEF_HZ) for sx in (1, -1) for sz in (1, -1)]
KERBE = (8.0, 6.0, 3.0)                # Länge (x) × Breite (z) × Tiefe der Kerben in der Wanne
RAD_INNEN = 95.85                      # Innenseite der Räder (z)
RAD_X = (80.0 - PRUEF_MITTE, -80.0 - PRUEF_MITTE)   # Radachsen, vom Prüfstand aus gesehen
RAD_R = 32.5

# ------------------------------------------------------------------ Prüfstand
HUB = 19.0                             # so weit hängen die Räder über dem Tisch
AUFLAGE = BODEN_UNTEN + HUB            # Oberkante der Stempel = Wannenboden (35 mm)
LUFT = 0.3                             # Luft zwischen Zapfen und Kerbe (je Seite)
ZAPFEN_H = KERBE[2] - 0.5              # Zapfen 0,5 mm kürzer als die Kerbe tief ist
ZAPFEN_FASE = 0.8
STEMPEL = (12.0, 10.0)                 # Auflagefläche je Stempel (x × z)
SOCKEL = 124.0                         # quadratische Sockelplatte
SOCKEL_H = 4.0
WAND_FUSS, WAND_KOPF = 22.0, 12.0      # Querwand unten / oben (in x)
WAND_Z = 46.0                          # Querwand reicht bis z = ±46
WAND_OBEN = AUFLAGE - 2.0              # zwischen den Stempeln 2 mm Luft zum Wannenboden

AUS = Path(__file__).resolve().parent / "pruefstand"


def P(x, y, z):
    return Pos(x, -z, y)


def quader(x0, x1, y0, y1, z0, z1):
    return P((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(z1 - z0), abs(y1 - y0))


def querwand(xm):
    """Querwand bei x = xm: Trapez (unten breit, oben schmal), mit Fenster und 2 Stempeln."""
    f, k = WAND_FUSS / 2, WAND_KOPF / 2
    profil = Plane.XZ * Polygon((xm - f, SOCKEL_H - 0.1), (xm + f, SOCKEL_H - 0.1), (xm + k, WAND_OBEN),
                                (xm - k, WAND_OBEN), align=None)
    wand = extrude(profil.face(), WAND_Z, both=True)
    # Fenster: senkrechte Seiten, oben 45°-Dach und kurze flache Brücke (10 mm) – ohne Stützen druckbar
    fenster = Plane.YZ * Polygon((-22, 9), (22, 9), (22, 12), (5, 29), (-5, 29), (-22, 12), align=None)   # oben 45° und nur 10 mm flache Brücke
    wand -= Pos(xm, 0, 0) * extrude(fenster.face(), WAND_FUSS, both=True)
    for (x, z) in PRUEF_PUNKTE:
        if abs(x - xm) > 1:
            continue
        sx, sz = STEMPEL
        wand += quader(x - sx / 2, x + sx / 2, WAND_OBEN - 0.1, AUFLAGE, z - sz / 2, z + sz / 2)
        zl, zb = KERBE[0] - 2 * LUFT, KERBE[1] - 2 * LUFT
        wand += quader(x - zl / 2, x + zl / 2, AUFLAGE - 0.1, AUFLAGE + ZAPFEN_H - ZAPFEN_FASE, z - zb / 2, z + zb / 2)
        wand += P(x, AUFLAGE + ZAPFEN_H - ZAPFEN_FASE - 0.01, z) * extrude(Rectangle(zl, zb), ZAPFEN_FASE + 0.01, taper=45)
    return wand


def sockel():
    platte = extrude(RectangleRounded(SOCKEL, SOCKEL, 10), SOCKEL_H)
    platte = chamfer(platte.edges().group_by(Axis.Z)[-1], 1.2)            # obere Außenkante angefast
    platte -= Pos(0, 0, -1) * extrude(RectangleRounded(2 * (PRUEF_HX - WAND_FUSS / 2), 2 * WAND_Z - 12, 6), SOCKEL_H + 2)
    # Schriftzug vorne und hinten auf dem Rand (0,6 mm vertieft)
    for xm, text, r in ((55.0, "PRÜFSTAND", 90), (-55.0, "RASPBERRY CAR", -90)):
        schrift = Pos(xm, 0, SOCKEL_H - 0.6) * Rot(0, 0, r) * extrude(Text(text, 5.5), 1)
        platte -= schrift
    return platte


def pruefstand():
    teil = sockel()
    for xm in (PRUEF_HX, -PRUEF_HX):
        teil += querwand(xm)
    return teil


def pruefen():
    """Abstände prüfen: Räder frei, Sockel nicht unter den Rädern im Weg."""
    fehler = 0
    if SOCKEL / 2 > RAD_INNEN - 5:
        print("  Sockel zu nah an den Rädern"); fehler += 1
    print(f"Luft unter den Rädern: {HUB:.0f} mm (der Sockel liegt nicht unter den Rädern)")
    print(f"Sockel – Radinnenseite: {RAD_INNEN - SOCKEL / 2:.1f} mm")
    print("Probleme:", fehler)


if __name__ == "__main__":
    AUS.mkdir(exist_ok=True)
    pruefen()
    t = pruefstand()
    export_stl(t, str(AUS / "pruefstand.stl"), tolerance=0.02, angular_tolerance=0.15)
    export_step(t, str(AUS / "pruefstand.step"))
    bb = t.bounding_box()
    print("gültig" if t.is_valid else "UNGÜLTIG", f"pruefstand {bb.size.X:.1f} × {bb.size.Y:.1f} × {bb.size.Z:.1f} mm, Volumen {t.volume / 1000:.1f} cm³")
