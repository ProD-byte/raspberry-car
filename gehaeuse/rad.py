"""Raspberry Car – Rad Ø 85 mm zum Selberdrucken: Felge (PETG) + Reifen (TPU)

4 × dasselbe Rad. Ersetzt das gekaufte 85-mm-Gummirad mit Sechskant-Kupplung.

Felge (PETG, ca. 40 g):
  * Klemmnabe direkt auf der 4-mm-D-Welle des Motors JGA25-370: D-förmige Bohrung, die Nabe ist geschlitzt und wird
    mit 1 × M3 × 16 (ISO 4762) zusammengezogen. Kopf auf der einen Seite, Gewinde schneidet sich in die andere Hälfte.
  * Die Klemmschraube liegt quer, auf der Innenseite des Rads, zwischen Gehäusewand und Reifen. Erreichbar ist sie
    mit einem Inbus 2,5 von vorne bzw. hinten: Rad drehen, bis die Schraube waagerecht nach vorne zeigt.
  * Die Nabe beginnt erst 3,7 mm vor der Wand: dort sitzen die Köpfe der Motorschrauben (bis z = 93).
    Nur ein dünner Kragen (Ø 8,8) geht näher an die Wand, damit die Welle möglichst lang in der Nabe steckt.
  * Außen eine Scheibe mit 6 runden Fenstern, am Rand zwei Lippen, die den Reifen halten,
    und 12 Rippen, damit der Reifen nicht auf der Felge durchrutscht.

Reifen (TPU 95A, ca. 30 g): wird über die äußere Lippe auf die Felge gezogen (etwas eng, das soll so sein).
  Profil mit versetzten Querrillen, innen 12 Nuten für die Rippen der Felge.

Maße wie im Modell: Ø 85 mm, Innenseite bei |z| = 98,5, Außenseite bei 131,9 (33,4 mm breit), Radmitte über der
D-Welle. z ist hier der Abstand von der Wagenmitte nach außen (so wie beim linken Rad).
Druck: beide Teile mit der Außenseite (große Scheibe) nach unten, ohne Stützen. Reifen langsam (20–30 mm/s).

D-Welle laut Datenblatt Ø 4,0 mm, Fläche 0,5 mm tief (3,5 mm über die Fläche gemessen) –
nach der Lieferung nachmessen und WELLE_D / WELLE_FLACH anpassen.

Aufruf:  python rad.py   → rad/felge.stl/.step, rad/reifen.stl/.step
"""
from pathlib import Path
import math
from build123d import Box, Cylinder, Plane, Polygon, Pos, Rot, Axis, revolve, export_stl, export_step
from loecher import PILOT_QUER, DURCH_QUER, DURCH_HOCH

# ------------------------------------------------------------------ Lage am Auto (wie ebene1_fahrwerk / schutzblech)
WAND_Z = 90.0                     # Außenseite der Wannenwand
MOTORSCHRAUBE_Z = 93.0            # Köpfe der Motorschrauben (M3 × 6 von außen) reichen bis hier
MOTORSCHRAUBE_R = 7.7 - 2.75      # … und so nah an die Achse (Langloch ab 7,7, Kopf Ø 5,5)
WELLE_ENDE = 99.5                 # Ende der Motorwelle
Z_INNEN, Z_AUSSEN = 98.5, 131.9   # Innen- und Außenseite des Rads
R_AUSSEN = 42.5                   # Ø 85

# ------------------------------------------------------------------ Welle und Nabe
WELLE_D, WELLE_FLACH = 4.0, 3.5   # D-Welle: Durchmesser, Maß über die Fläche
BOHRUNG = None                    # aus der Wellenprobe (wellenprobe.py) eintragen, z. B. 4.3 – solange None, gilt die Schätzung:
ZUGABE = 0.2 + (DURCH_HOCH - 3.4) / 2 if BOHRUNG is None else BOHRUNG - WELLE_D   # Bohrung steht beim Druck senkrecht
KRAGEN_R, KRAGEN_Z0 = 4.4, 91.0   # dünner Kragen vor den Motorschrauben
NABE_Z0 = 94.0                    # Klemmblock ab hier (Abstand zu den Motorschrauben-Köpfen)
NABE_X, NABE_Y = (-8.5, 8.5), (-8.0, 9.5)   # Klemmblock (quer zur Achse); Schlitz zeigt nach +y
SCHLITZ_B, SCHLITZ_BIS = 1.2, 104.0         # Schlitzbreite, Schlitz reicht bis z = 104 (lange, weiche Backen)
SCHRAUBE_Y, SCHRAUBE_Z = 5.5, 96.5          # Klemmschraube M3 × 16 quer (entlang x)
INBUS_R = 1.25                              # Inbus 2,5

# ------------------------------------------------------------------ Felge und Reifen
FELGE_R, FELGE_RI = 37.5, 35.0    # Felgenbett außen / innen
LIPPE_R, LIPPE_B = 39.0, 1.0      # Lippen an beiden Rändern
SCHEIBE_D = 3.0                   # Scheibe außen
FENSTER_R, FENSTER_LAGE = 7.0, 22.0
RIPPEN, RIPPE_H, RIPPE_B = 12, 1.0, 2.0
REIFEN_RI = 37.3                  # 0,2 mm enger als das Felgenbett: sitzt stramm
PROFIL_N, PROFIL_T, PROFIL_B = 30, 1.5, 2.5

AUS = Path(__file__).resolve().parent / "rad"


def dreh(punkte):
    """Rotationskörper um die Radachse aus einem (r, z)-Profil."""
    return revolve(Plane.XZ * Polygon(*punkte, align=None), Axis.Z)


def quader(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def felge():
    li = Z_INNEN
    t = dreh([(0, Z_AUSSEN), (LIPPE_R, Z_AUSSEN), (LIPPE_R, Z_AUSSEN - LIPPE_B), (FELGE_R, Z_AUSSEN - LIPPE_B),
              (FELGE_R, li + LIPPE_B + (LIPPE_R - FELGE_R)),        # innere Lippe unten 45° (druckt ohne Stützen)
              (LIPPE_R, li + LIPPE_B), (LIPPE_R, li), (FELGE_RI, li),
              (FELGE_RI, Z_AUSSEN - SCHEIBE_D), (0, Z_AUSSEN - SCHEIBE_D)])
    # Rippen gegen Durchrutschen des Reifens
    for i in range(RIPPEN):
        a = 360 * i / RIPPEN
        t += Rot(0, 0, a) * quader(FELGE_R - 0.5, FELGE_R + RIPPE_H, -RIPPE_B / 2, RIPPE_B / 2,
                                   li + LIPPE_B + 2.0, Z_AUSSEN - LIPPE_B + 0.1)
    # Fenster in der Scheibe
    for i in range(6):
        a = math.radians(60 * i + 30)
        t -= Pos(FENSTER_LAGE * math.cos(a), FENSTER_LAGE * math.sin(a), Z_AUSSEN - SCHEIBE_D / 2) * Cylinder(FENSTER_R, SCHEIBE_D + 2)
    # Nabe: Klemmblock von der Scheibe bis vor die Motorschrauben, davor der dünne Kragen
    t += quader(*NABE_X, *NABE_Y, NABE_Z0, Z_AUSSEN)
    t += Pos(0, 0, (KRAGEN_Z0 + NABE_Z0 + 0.1) / 2) * Cylinder(KRAGEN_R, NABE_Z0 + 0.1 - KRAGEN_Z0)
    # D-Bohrung (Fläche zeigt nach −y, gegenüber vom Schlitz)
    rb = (WELLE_D + ZUGABE) / 2
    flach = WELLE_FLACH - WELLE_D / 2 + ZUGABE / 2          # Abstand der Fläche von der Achse
    lang = Z_AUSSEN - KRAGEN_Z0 + 2
    mitte = (KRAGEN_Z0 + Z_AUSSEN) / 2
    t -= (Pos(0, 0, mitte) * Cylinder(rb, lang)) & quader(-rb - 1, rb + 1, -flach, rb + 1, KRAGEN_Z0 - 1, Z_AUSSEN + 1)
    # Schlitz und Klemmschraube (quer, entlang x)
    t -= quader(-SCHLITZ_B / 2, SCHLITZ_B / 2, 0, NABE_Y[1] + 1, KRAGEN_Z0 - 1, SCHLITZ_BIS)
    t -= Pos(NABE_X[1] / 2, SCHRAUBE_Y, SCHRAUBE_Z) * Rot(0, 90, 0) * Cylinder(DURCH_QUER / 2, NABE_X[1] + 1)
    t -= Pos(NABE_X[0] / 2, SCHRAUBE_Y, SCHRAUBE_Z) * Rot(0, 90, 0) * Cylinder(PILOT_QUER / 2, -NABE_X[0] + 1)
    return t


PROFILE = ["quer", "glatt", "pfeil", "stollen"]   # quer = Standard (reifen.stl), die anderen: reifen_<name>.stl


def reifen(profil="quer"):
    li = Z_INNEN + 0.1
    la = Z_AUSSEN - LIPPE_B - 0.1
    t = dreh([(LIPPE_R + 0.2, li), (REIFEN_RI, li + (LIPPE_R + 0.2 - REIFEN_RI)), (REIFEN_RI, la),
              (R_AUSSEN - 1, la), (R_AUSSEN, la - 1), (R_AUSSEN, li + 1), (R_AUSSEN - 1, li)])
    for i in range(RIPPEN):        # Nuten für die Rippen der Felge
        t -= Rot(0, 0, 360 * i / RIPPEN) * quader(REIFEN_RI - 0.5, FELGE_R + RIPPE_H + 0.2, -RIPPE_B / 2 - 0.2, RIPPE_B / 2 + 0.2,
                                                  Z_INNEN + LIPPE_B + 1.8, la + 1)
    return t - profil_rillen(profil, li, la)


def rille_rund(zc, tiefe=PROFIL_T):
    """Umlaufende Rille mit 45°-Flanken (V-Form) – druckt ohne Stützen, auch wenn der Reifen liegt."""
    return dreh([(R_AUSSEN + 1, zc - tiefe - 1), (R_AUSSEN - tiefe, zc), (R_AUSSEN + 1, zc + tiefe + 1)])


def rille_quer(winkel, z0, z1, breite=PROFIL_B, schraeg=0.0):
    """Rille quer über die Lauffläche bei `winkel` (Grad), von z0 bis z1, um `schraeg` Grad gegen die Achse geneigt."""
    r = quader(R_AUSSEN - PROFIL_T, R_AUSSEN + 1, -breite / 2, breite / 2, 0, z1 - z0)
    return Rot(0, 0, winkel) * Pos(0, 0, z0) * Rot(schraeg, 0, 0) * r


def profil_rillen(profil, li, la):
    """Alle Profile drucken ohne Stützen, wenn der Reifen liegt: Rillen quer stehen senkrecht, umlaufende Rillen sind
    V-förmig (45°), schräge Rillen höchstens 30° geneigt."""
    mitte, breit = (li + la) / 2, la - li
    r = None
    def dazu(k):
        nonlocal r
        r = k if r is None else r + k
    if profil == "quer":           # Standard: versetzte Querrillen – Allrounder für drinnen
        for i in range(PROFIL_N):
            z0, z1 = (li - 1, li + 21) if i % 2 else (la - 21, la + 1)
            dazu(rille_quer(360 * i / PROFIL_N, z0, z1))
    elif profil == "glatt":        # 3 umlaufende Rillen – leise, viel Auflage: Fliesen, Parkett, Tisch
        for k in (-1, 0, 1):
            dazu(rille_rund(mitte + k * breit / 4))
    elif profil == "pfeil":        # Pfeil-Profil wie beim Traktor – Gras, Erde (Pfeil zeigt in Fahrtrichtung vorwärts)
        for i in range(20):
            w = 360 * i / 20
            # beide Arme beginnen in der Mitte und laufen schräg zur gleichen Seite nach außen → Pfeil (V)
            arm = quader(R_AUSSEN - PROFIL_T, R_AUSSEN + 1, -1.5, 1.5, 0, la - mitte + 2)
            dazu(Rot(0, 0, w) * Pos(0, 0, mitte) * Rot(30, 0, 0) * arm)
            dazu(Rot(0, 0, w) * Pos(0, 0, mitte) * Rot(180 - 30, 0, 0) * arm)
    elif profil == "stollen":      # Blöcke (Stollen) – Teppich, Kies, Rasen; greift am stärksten
        for i in range(16):
            dazu(rille_quer(360 * i / 16, li - 1, la + 1, 3.5))
        for k in (-1, 1):
            dazu(rille_rund(mitte + k * breit / 6, 2.0))
    else:
        raise ValueError(f"unbekanntes Profil: {profil}")
    return r


def pruefen():
    fehler = 0
    def check(text, ok):
        nonlocal fehler
        print(f"  {text}: {'ja' if ok else 'NEIN'}")
        fehler += 0 if ok else 1
    print("Prüfungen:")
    check("Welle steckt mindestens 8 mm in der Nabe", WELLE_ENDE - KRAGEN_Z0 >= 8)
    check("Kragen bleibt innerhalb der Motorschrauben-Köpfe", KRAGEN_R < MOTORSCHRAUBE_R - 0.4)
    check("Klemmblock und Schraubenkopf bleiben vor den Motorschrauben-Köpfen",
          NABE_Z0 > MOTORSCHRAUBE_Z + 0.5 and SCHRAUBE_Z - 2.75 > MOTORSCHRAUBE_Z + 0.5)
    check("Kragen berührt die Wand nicht", KRAGEN_Z0 > WAND_Z + 0.5)
    check("Inbus 2,5 kommt waagerecht an die Klemmschraube (am Reifen vorbei)", SCHRAUBE_Z + INBUS_R + 0.5 <= Z_INNEN)
    check("Klemmschraube liegt neben der Bohrung", SCHRAUBE_Y - DURCH_QUER / 2 > (WELLE_D + ZUGABE) / 2 + 1.0)
    print("Probleme:", fehler)


if __name__ == "__main__":
    AUS.mkdir(exist_ok=True)
    f, r = felge(), reifen()
    print(f"Felge: {f.volume / 1000:.1f} cm³ (PETG ca. {f.volume / 1000 * 1.27:.0f} g), "
          f"Reifen: {r.volume / 1000:.1f} cm³ (TPU ca. {r.volume / 1000 * 1.21:.0f} g)")
    print(f"D-Bohrung Ø {WELLE_D + ZUGABE:.1f} mm, Fläche {WELLE_FLACH + ZUGABE:.1f} mm; Klemmschraube M3 × 16")
    teile = [(f, "felge"), (r, "reifen")] + [(reifen(p), f"reifen_{p}") for p in PROFILE[1:]]
    for teil, name in teile:
        export_stl(teil, str(AUS / f"{name}.stl"), tolerance=0.02, angular_tolerance=0.1)
        export_step(teil, str(AUS / f"{name}.step"))
    pruefen()
