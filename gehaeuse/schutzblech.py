"""Raspberry Car – Schutzbleche (Kotflügel) über den vier Rädern

Ein Druckteil, viermal drucken: es passt an jedes Rad (vorne/hinten gleich, für die rechte Seite einfach um 180°
gedreht). Alle Maße in mm. Erzeugt STL und STEP in gehaeuse/schutzbleche/.

Aufruf (einmalig: pip install build123d):
    python schutzblech.py

Koordinaten wie im 3D-Modell (x nach vorne, z nach links, y nach oben). Das Teil wird für das Rad vorne links
modelliert: Achse bei x = 80, y = 33,8, Rad Ø 85 × 36 mm, Innenseite bei z = 95,9.

Aufbau:
  * Bogen über dem Rad: Innenradius 47 mm (4,5 mm Luft zum Reifen), 2,4 mm dick, von −60° bis +60° (die Enden
    liegen auf Höhe der Fuge Wanne/Deck), in z von der Gehäusewand (z = 90) bis 4 mm über die Außenseite des Rads.
    Außen ein nach innen gezogener Rand (2 mm, unten 45° schräg) – sieht fertig aus und macht den Bogen steifer.
  * Flansch an der Gehäusewand: 6 mm dick, folgt dem Bogen. Er liegt am Gehäuse-Ring von Ebene 2 an (y 61 … 84)
    und wird mit 2 × M3 × 10 von außen in zwei Schraubsäulen des Rings geschraubt (Kopf bündig im Flansch).
    Nur am Ring – so lässt sich die Wanne weiter nach unten abnehmen, und die Klapphaube (ab y = 84) bleibt frei.
  * Die Schrauben sitzen so weit außen (52,8 mm von der Achse), dass ein Schraubendreher am Rad und am Bogen
    vorbeikommt – Rad und Schutzblech müssen zum Festschrauben nicht ab.

Drucken: Flansch-Rückseite (die an der Wand anliegt) aufs Bett, der Bogen wächst senkrecht nach oben – ohne Stützen.
Schrauben: nur M3-Zylinderkopf (ISO 4762). Rund um jedes Kernloch mindestens 3,5 mm Material.
"""
from pathlib import Path
import math
from build123d import Cylinder, Box, Rot, Pos, Plane, Polygon, extrude, export_stl, export_step, Axis, Cone

# ------------------------------------------------------------------ Parameter
RAD_X, ACHSE = 80.0, 33.8                # Rad vorne links (Achse)
RAD_R, RAD_INNEN, RAD_AUSSEN = 42.5, 95.9, 131.9   # Radius, Innen- und Außenseite (z)
WAND_Z = 90.0                            # Außenseite der Gehäusewand (B/2)

BOGEN_RI = 47.0                          # Innenradius des Bogens (4,5 mm Luft zum Reifen)
BOGEN_D = 2.4                            # Dicke des Bogens
BOGEN_RA = BOGEN_RI + BOGEN_D            # 49,4
BOGEN_WINKEL = 60.0                      # von −60° bis +60° (0° = senkrecht über der Achse)
BOGEN_Z1 = RAD_AUSSEN + 4.0              # außen 4 mm über die Außenseite des Rads
RAND_B = 2.0                             # Rand außen: 2 mm nach innen gezogen

FLANSCH_D = 6.0                          # Flansch an der Wand
FLANSCH_RA = 58.5                        # Außenradius des Flanschs
FLANSCH_Y = (61.2, 83.8)                 # nur am Gehäuse-Ring (Deck-Oberkante 61, Haube ab 84)
FLANSCH_X = 32.0                         # ± um die Achse (vorne endet der Flansch vor der Rundung der Ecke bei x = 113)

PILOT, DURCH = 2.6, 3.4
KOPF_D, KOPF_H = 6.5, 3.1                # Senkung: Zylinderkopf schließt bündig ab
SCHRAUBE_DX = 27.0                       # Schrauben bei Achse ± 27 mm in x …
SCHRAUBE_Y = 79.2                        # … und auf y = 79,2 (52,8 mm von der Achse)
SCHRAUBE_L = 10.0                        # M3 × 10

# Schraubsäulen im Gehäuse-Ring (für ebene2_elektronik.py): an jedem Rad zwei, (x, y, z der Wand-Außenseite mit Vorzeichen)
RAD_ACHSEN = [(80.0, 1), (80.0, -1), (-80.0, 1), (-80.0, -1)]       # (x der Achse, Seite +1 links / −1 rechts)
SCHRAUBEN = [(ax + k * SCHRAUBE_DX, SCHRAUBE_Y, s) for (ax, s) in RAD_ACHSEN for k in (-1, 1)]

AUS = Path(__file__).resolve().parent / "schutzbleche"


def P(x, y, z):
    """Punkt im Modell (x vorne, y oben, z links) → build123d (X = x, Y = −z, Z = y)."""
    return Pos(x, -z, y)


def zyl_z(r, x, y, z0, z1):
    return P(x, y, (z0 + z1) / 2) * Rot(90, 0, 0) * Cylinder(r, abs(z1 - z0))


def quader(x0, x1, y0, y1, z0, z1):
    return P((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(z1 - z0), abs(y1 - y0))


def sektor(r, winkel, z0, z1):
    """Tortenstück um die Radachse (Spitze in der Achse), von −winkel bis +winkel, in z von z0 bis z1."""
    pts = [(RAD_X, ACHSE)] + [(RAD_X + r * math.sin(math.radians(a)), ACHSE + r * math.cos(math.radians(a)))
                              for a in [-winkel + i * 2 * winkel / 48 for i in range(49)]]
    flaeche = Plane.XZ * Polygon(*pts, align=None)            # Plane.XZ: (u, v) = (x, y)
    return Pos(0, -z1, 0) * extrude(flaeche.face(), z1 - z0)   # Extrusion geht in +Y (= −z), daher bei −z1 beginnen


def schutzblech():
    # Bogen: Ring zwischen RI und RA, von der Wand bis außen
    bogen = sektor(BOGEN_RA, BOGEN_WINKEL, WAND_Z, BOGEN_Z1) - zyl_z(BOGEN_RI, RAD_X, ACHSE, WAND_Z - 1, BOGEN_Z1 + 1)
    # Rand außen: nach innen gezogen (außen bleibt der Bogen glatt, dort muss der Schraubendreher vorbei).
    # Liegt ganz außerhalb des Reifens (ab dessen Außenseite), unten 45° schräg – druckt ohne Stützen.
    z_a = BOGEN_Z1 - 2.0
    rand = zyl_z(BOGEN_RI + 0.1, RAD_X, ACHSE, RAD_AUSSEN, BOGEN_Z1)
    rand -= P(RAD_X, ACHSE, RAD_AUSSEN - 0.01) * Rot(90, 0, 0) * Cone(BOGEN_RI + 0.01, BOGEN_RI - RAND_B, z_a - RAD_AUSSEN + 0.02, align=None)
    rand -= zyl_z(BOGEN_RI - RAND_B, RAD_X, ACHSE, z_a, BOGEN_Z1 + 1)
    rand &= sektor(BOGEN_RA, BOGEN_WINKEL, RAD_AUSSEN - 1, BOGEN_Z1 + 1)
    # Flansch an der Wand
    flansch = sektor(FLANSCH_RA, 89.0, WAND_Z, WAND_Z + FLANSCH_D) - zyl_z(BOGEN_RI, RAD_X, ACHSE, WAND_Z - 1, WAND_Z + FLANSCH_D + 1)
    flansch &= quader(RAD_X - FLANSCH_X, RAD_X + FLANSCH_X, FLANSCH_Y[0], FLANSCH_Y[1], WAND_Z - 1, WAND_Z + FLANSCH_D + 1)
    teil = bogen + rand + flansch
    # Bogen oben nicht über die Trennfuge zur Haube
    teil &= quader(RAD_X - 80, RAD_X + 80, 0, FLANSCH_Y[1], WAND_Z - 1, BOGEN_Z1 + 1)
    # Schraubenlöcher mit Senkung (Kopf bündig)
    for k in (-1, 1):
        x = RAD_X + k * SCHRAUBE_DX
        teil -= zyl_z(DURCH / 2, x, SCHRAUBE_Y, WAND_Z - 1, WAND_Z + FLANSCH_D + 1)
        teil -= zyl_z(KOPF_D / 2, x, SCHRAUBE_Y, WAND_Z + FLANSCH_D - KOPF_H, WAND_Z + FLANSCH_D + 1)
    return teil


def rad():
    """Das Rad als einfacher Zylinder (für die Prüfungen)."""
    return zyl_z(RAD_R, RAD_X, ACHSE, RAD_INNEN, RAD_AUSSEN)


def an_rad(teil, ax, s):
    """Teil (modelliert für vorne links) an das Rad mit Achse x = ax, Seite s setzen."""
    if s < 0:
        teil = teil.rotate(Axis((RAD_X, 0, 0), (0, 0, 1)), 180)   # um die senkrechte Achse durch die Radachse drehen
    return Pos(ax - RAD_X, 0, 0) * teil


if __name__ == "__main__":
    AUS.mkdir(exist_ok=True)
    t = schutzblech()
    r = rad()
    # Prüfungen
    luft = min(BOGEN_RI - RAD_R, (FLANSCH_Y[1] - ACHSE) - RAD_R)
    print(f"Luft Reifen ↔ Bogen: {BOGEN_RI - RAD_R:.1f} mm, Oberkante Bogen y = {min(ACHSE + BOGEN_RA, FLANSCH_Y[1]):.1f} (Haube ab 84)")
    print("Schutzblech berührt das Rad:", "JA" if (t & r).volume > 0.01 else "nein")
    rs = math.hypot(SCHRAUBE_DX, SCHRAUBE_Y - ACHSE)
    print(f"Schraube {rs:.1f} mm von der Achse: Kopf-Rand {rs - KOPF_D / 2:.1f} > Bogen außen {BOGEN_RA:.1f}:", "ja" if rs - KOPF_D / 2 > BOGEN_RA else "NEIN")
    for k in (-1, 1):
        x = RAD_X + k * SCHRAUBE_DX
        rand_ = min(x - (RAD_X - FLANSCH_X), (RAD_X + FLANSCH_X) - x, FLANSCH_Y[1] - SCHRAUBE_Y) - DURCH / 2
        print(f"  Schraube x = {x:.0f}: Material bis zum Flanschrand {rand_:.1f} mm")
    print("vorne endet der Flansch bei x =", RAD_X + FLANSCH_X, "(Rundung der Ecke beginnt bei 113)")
    print(f"Schraube M3 × {SCHRAUBE_L:.0f}: greift {SCHRAUBE_L - (FLANSCH_D - KOPF_H):.1f} mm in Ringwand + Säule")
    print(f"{len(t.solids())} Körper", "(gut)" if len(t.solids()) == 1 else "– NICHT zusammenhängend!", "| gültig" if t.is_valid else "| UNGÜLTIG")
    export_stl(t, str(AUS / "schutzblech.stl"), tolerance=0.02, angular_tolerance=0.15)
    export_step(t, str(AUS / "schutzblech.step"))
    bb = t.bounding_box()
    print(f"schutzblech {bb.size.X:.1f} × {bb.size.Y:.1f} × {bb.size.Z:.1f} mm, Volumen {t.volume / 1000:.1f} cm³ (4 Stück drucken)")
