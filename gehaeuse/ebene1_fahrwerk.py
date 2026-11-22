"""Raspberry Car – Ebene 1: Fahrwerk & Energie (Wanne, Motorbügel)

Druckteile für die unterste Ebene. Alle Maße in mm. Erzeugt STL (zum Drucken)
und STEP (für jedes CAD-Programm) im Ordner gehaeuse/ebene1/.

Aufruf (einmalig: pip install build123d):
    python ebene1_fahrwerk.py

Koordinaten wie im 3D-Modell: Mitte zwischen den Achsen = 0 = Mitte der Wanne, x nach vorne,
z nach links, y nach oben. Im CAD (Z oben): X = x, Y = −z (rechts), Z = y.

Aufbau:
  * Wanne 250 × 180 mm (vorne bis x = +125, hinten bis x = −125), aus ZWEI Druckteilen:
    vordere und hintere Hälfte, Fuge quer bei x = FUGE. Die vordere Hälfte hat drei Laschen, die in die
    hintere greifen (innen an beiden Seitenwänden und in der Mitte); sie stehen beim Druck auf dem Bett.
    Verschraubt mit 6 × M3: an jeder Seite 2 waagerecht von außen (Kopf bündig, die Wand der hinteren
    Hälfte ist dort innen auf 6 mm verstärkt), in der Mitte 2 von innen durch einen Block.
    Darin liegen
    - die 4 Motoren (JGA25-370): Getriebe-Stirnseite mit 2 × M3 an die Seitenwand
      (waagerechte Langlöcher 15,4–17 mm), Encoder-Stecker oben, Sättel + Motorbügel,
    - der Akku (2 × Keystone 1047, hintereinander quer im Auto) in der hinteren Hälfte,
    - die Stromversorgung in der vorderen Hälfte: BMS links, Sicherungshalter rechts, dazwischen
      INA226 (ohne Stiftleiste, Leitungen direkt angelötet) und die Verteiler Plus/Minus
      (WAGO 221-415, Kabelseite nach hinten, Hebel nach oben). Das Ladeboard sitzt oben auf dem Elektronik-Deck.
  * Räder außen an den Seiten: Achsen bei x = ±80 (Radstand 160 mm), vorne und hinten je 45 mm Überhang.
  * Boden vorne und hinten gleich schräg hochgezogen („Kufen“): je 45° auf den letzten 8,5 mm, Übergang gerundet.
    So gleitet die Wanne über Steine und Kanten zwischen den Rädern, statt hängen zu bleiben.
  * 2 Nahsensoren VL53L1X (Modul 25 × 10,7 mm, z. B. Happysnow) innen hinter Fenstern in der
    Stirnwand vorne und hinten, in der Mitte. Das Modul wird von oben in zwei Nuten geschoben,
    um 5° nach oben gekippt (sieht den Boden nicht, erkennt Rampen besser).
  * Hauptschalter (Taster Ø 12 mm) und die USB-C-Buchse des Ladeboards sitzen
    hinten im Gehäuse-Ring von Ebene 2 (hinter den Hinterrädern ist in der Wanne kein Platz).
  * Oben liegt direkt das Elektronik-Deck (Ebene 2) als Deckel auf. Die Wanne wird
    von unten mit 4 × M3 × 45 an dessen Dome geschraubt (Köpfe versenkt in den Kufen):
    Auto umdrehen, 4 Schrauben lösen, Wanne ab – alles darüber bleibt zusammen.

Schrauben: nur M3-Zylinderkopf (ISO 4762). In Kunststoff schneiden sie ihr
Gewinde selbst (Kernloch PILOT). Rund um jedes Kernloch mindestens 3,5 mm Material.
"""
from pathlib import Path
import math
from build123d import (Box, Cylinder, Rot, Rectangle, RectangleRounded, RegularPolygon, SlotCenterToCenter, Polygon, Plane,
                       Pos, extrude, chamfer, fillet, Axis, export_stl, export_step, Compound)

# ------------------------------------------------------------------ Parameter
X_VORNE, X_HINTEN = 125.0, -125.0       # Außenkante vorne / hinten (je 45 mm vor bzw. hinter der Achse)
L = X_VORNE - X_HINTEN                  # 250 mm
XM = (X_VORNE + X_HINTEN) / 2           # Mitte der Wanne (0)
B, R_ECKE = 180.0, 12.0
BODEN_UNTEN = 16.0                      # Bodenfreiheit
BODEN = 3.0
BODEN_OBEN = BODEN_UNTEN + BODEN
WAND = 3.0
RAND = 58.0                             # Oberkante Wanne = Unterkante Elektronik-Deck (Platz über den Encoder-Steckern)
FASE = 3.0

ACHSE = 33.8                            # Radachse (Rad Ø 67,6 mm)
MOTOREN_X = (80.0, -80.0)               # Achse vorne / hinten: Radstand 160 mm
MOTOR_X = MOTOREN_X[0]                  # für das Einzelteil Motorbügel
STIRN = B / 2 - 3.0                     # Getriebe-Stirnseite an der Wand-Innenseite bei |z| = 87
MOTOR_LANG = 52.0                       # Getriebe + Motor ab der Stirnseite (Encoder-Stecker liegt innen davor)
MOTOR_R = 12.5
LOCH_MIN, LOCH_MAX = 7.7, 8.5           # M3-Gewinde im Getriebe ±7,7 … ±8,5 (waagerecht)
LAGER_D = 8.0

PILOT = 2.6
DURCH = 3.4
KOPF_D, KOPF_H = 6.5, 3.1               # Senkung: Kopf bündig
DOM_D = PILOT + 2 * 3.7                 # 10 mm

BUEGEL_Z = STIRN - 12.0                 # Motorbügel 12 mm innen von der Stirnseite
SATTEL_Z = STIRN - 37.0                 # zweiter Sattel unter dem Motor
BUEGEL_DICKE = 10.0
BUEGEL_LOCH = 20.0
BUEGEL_FUSS = 25.5

# Akku: 2 × Keystone 1047 (77,1 × 39,8 mm, Löcher 55,2 mm längs), hintereinander quer im Auto in der hinteren Hälfte
AKKU_X = -33.0                          # Mitte der Halter (x)
AKKU_Z = 40.0                           # Mitte je Halter bei z = ±40 (Halter liegen längs in z)
AKKU_LOCH = 27.6
AKKU_SOCKEL = 3.0
AKKU_MASS = (39.8, 77.1)                # Halter: Breite (x) × Länge (z)

# Aufnahmepunkte für den Prüfstand (wie bei einer Hebebühne): 4 Kerben unten im Boden, unter dem Akku.
# Innen ist der Boden dort 2,5 mm dicker (unter den Akkuhaltern ist 3 mm Luft), über der Kerbe bleiben 2,5 mm.
PRUEF_MITTE, PRUEF_HX, PRUEF_HZ = 3.5, 36.5, 40.0   # hinten unter dem Akku, vorne unter der Stromversorgung
PRUEF_PUNKTE = [(PRUEF_MITTE + sx * PRUEF_HX, sz * PRUEF_HZ) for sx in (1, -1) for sz in (1, -1)]
PRUEF_KERBE = (8.0, 6.0, 3.0)          # Länge (x) × Breite (z) × Tiefe
PRUEF_VERSTAERKUNG = 2.5

# Säulen für das Elektronik-Deck (Schraube von unten, Kopf bündig im Boden)
# Kufen: Boden vorne/hinten schräg hochgezogen (Unterkante steigt ab KUFE_x zum Ende hin)
KUFE_VORNE = (X_VORNE - 8.5, 45.0)     # 8,5 mm vor dem Ende, 45°
KUFE_HINTEN = (X_HINTEN + 8.5, 45.0)   # genau wie vorne (gleiche Schrauben vorne und hinten)


KUFE_RADIUS = 0.0                      # Übergang flacher Boden → Schräge: scharfer 45°-Knick. Eine Rundung würde flach am Druckbett
                                       # beginnen und bräuchte Stützen; der Knick druckt sauber und gleitet genauso über Kanten.


def unterkante(x):
    """Höhe der Wannen-Unterkante an der Stelle x (Kufen mit gerundetem Übergang)."""
    y = BODEN_UNTEN
    for (x0, winkel), s in ((KUFE_VORNE, 1), (KUFE_HINTEN, -1)):
        tw = math.tan(math.radians(winkel))
        d = s * (x - x0)                                  # Abstand hinter dem Knick (zum Ende hin positiv)
        gerade = BODEN_UNTEN + max(0.0, d) * tw
        # Rundung: Kreis mit KUFE_RADIUS, berührt den flachen Boden und die Schräge
        dm = -KUFE_RADIUS * (math.sqrt(1 + tw * tw) - 1) / tw          # Kreismitte (in d gemessen)
        de = dm + KUFE_RADIUS * math.sin(math.atan(tw))                # Ende der Rundung
        bogen = BODEN_UNTEN + KUFE_RADIUS - math.sqrt(max(0.0, KUFE_RADIUS ** 2 - (d - dm) ** 2)) if dm <= d <= de else -1e9
        y = max(y, gerade, bogen)
    return y


def seitenprofil(dy=0.0, radius=KUFE_RADIUS, oben=RAND + 5):
    """Seitenansicht der Wanne (x/y) mit Kufen, als Fläche. dy: Unterkante um dy (senkrecht zur Fläche) nach oben."""
    xv, av = KUFE_VORNE
    xh, ah = KUFE_HINTEN
    tv, th = math.tan(math.radians(av)), math.tan(math.radians(ah))
    yb = BODEN_UNTEN + dy
    # Knickpunkte so verschieben, dass die Wand überall dy dick bleibt
    kv = xv - (dy / math.cos(math.radians(av)) - dy) / tv
    kh = xh + (dy / math.cos(math.radians(ah)) - dy) / th
    xe_v, xe_h = X_VORNE + 8, X_HINTEN - 8
    punkte = [(xe_h, oben), (xe_h, yb + (kh - xe_h) * th), (kh, yb), (kv, yb), (xe_v, yb + (xe_v - kv) * tv), (xe_v, oben)]
    flaeche = (Plane.XZ * Polygon(*punkte, align=None)).face()
    knicke = [v for v in flaeche.vertices() if abs(v.Z - yb) < 0.01]
    return flaeche.fillet_2d(radius, knicke) if radius > 0 else flaeche


# Nahsensoren VL53L1X (Modul 25 × 10,7 × 1,6 mm, Sensor zeigt zur Wand): (Name, Richtung +1 vorne / −1 hinten)
TOF = [("vorne", 1), ("hinten", -1)]
TOF_L, TOF_H, TOF_PCB = 25.0, 10.5, 1.5     # Länge (quer im Auto), Höhe, Platinendicke (nach GrabCAD-Modell)
TOF_SENSOR_Y = -2.0                         # Sensor sitzt 2 mm unter der Platinenmitte (Lötpunkte oben)
TOF_BAUTEIL = 1.5                           # so hoch steht der Sensor vorne auf der Platine
TOF_UNTEN = 38.0                            # Unterkante der Platine (über dem Bügel-/Sattelbereich, unter dem Deck)
TOF_FENSTER = (13.0, 9.0)                   # Fenster in der Wand (Breite, Höhe), außen mit Rahmen
TOF_NEIGUNG = 5.0                           # Sensor schaut 5° nach oben: sieht den Boden nicht, erkennt Rampen besser


def tof_lage(s):
    """x-Werte für den Sensor an der Stirnwand (s = +1 vorne, −1 hinten)."""
    wand = X_VORNE - WAND if s > 0 else X_HINTEN + WAND          # Wand-Innenseite
    vorn = wand - s * (0.3 + TOF_BAUTEIL)                         # Vorderseite der Platine
    hinten = vorn - s * TOF_PCB
    return wand, vorn, hinten


SAEULEN = [(X_VORNE - 7.5, 35), (X_VORNE - 7.5, -35), (X_HINTEN + 7.5, 35), (X_HINTEN + 7.5, -35)]   # gehen vorne/hinten in die Wand über, dazu eine Rippe (bricht nicht ab)
RIPPE = DOM_D - 0.1                      # Säule in voller Breite mit der Stirnwand verbunden (0,05 mm schmaler als die Säule:
                                         # Kanten genau auf der Säulenoberfläche bringen die CAD-Berechnung durcheinander)
# Kabelbinder-Schlitze im Boden: je 2 Schlitze quer zum Kabel, der Kabelbinder wird von UNTEN eingefädelt
# (Wanne ist zum Arbeiten ohnehin abgeschraubt und umgedreht). Unten eine flache Rille, damit er bündig liegt.
# (x, z) = Mitte zwischen den beiden Schlitzen; die Kabel laufen dort in x-Richtung.
KABELBINDER = [(-8, -58)]                  # hinter dem Sicherungshalter (vorne ist bis zum Motor kein Platz)
                                           # (Motorkabel brauchen keine: sie gehen auf kurzem Weg nach oben ins Deck)
BINDER_SCHLITZ = (4.6, 2.2)                # Schlitz: Länge in Kabelrichtung × Breite (für Kabelbinder bis 3,6 mm)
BINDER_ABSTAND = 9.0                       # Mitte zu Mitte der beiden Schlitze (Kabelbündel bis ca. 6 mm dazwischen)
BINDER_RILLE = 1.3                         # Tiefe der Rille unten (Kabelbinder ca. 1,1 mm dick)

# Taschen auf dem Boden: (Name, x, z, Innenmaß x, Innenmaß z, Rastnase über Boden, Wandhöhe, Art)
#   Art "rund":   Rahmen ringsum mit Rastnasen an den langen Seiten
#   Art "enden":  nur Wände an den beiden Enden in x-Richtung (schmale Streifen neben dem Akku)
#   Art "+x"/"−x": diese Seite offen (WAGO-Kabelseite)
LUFT, TWAND, NASE = 0.3, 1.6, 0.6
TASCHEN = [
    ("BMS",             33.0,   58.0, 48.0, 20.0, 1.6, 3.2, "enden"),
    ("INA226",          18.0,   26.0, 19.0, 21.0, 1.6, 3.2, "enden"),   # ohne Stiftleiste; VIN+/VIN− zeigen nach hinten
    ("WAGO Minus",      47.0,  -17.0, 18.4, 29.7, 8.1, 8.8, "-x"),    # Kabelseite nach hinten, Hebel nach oben
    ("WAGO Plus",       47.0,   17.0, 18.4, 29.7, 8.1, 8.8, "-x"),
]
SICHERUNG = (34.0, -58.0, 54.2, 12.5)   # Inline-Sicherungshalter für Standard-Flachsicherung, stehend (25,5 mm hoch, Deckel oben), mit Kabelansätzen

# Durchbrüche in der Rückwand (x = −120): (Name, z, y-Mitte, Breite, Höhe, rund?)
# Leer: Schalter und USB-C (Ladeboard) sitzen im Gehäuse-Ring von Ebene 2 (gehaeuse/ebene2_elektronik.py).
RUECKWAND = []

# Teilung in zwei Druckteile (vordere / hintere Hälfte)
FUGE = 6.0                               # Stoßstelle quer bei x = 6 (Akku ganz hinten, Stromversorgung ganz vorne)
FUGE_SPALT = 0.1                         # je Seite: 0,2 mm Spalt in der Fuge
LASCHE_BIS = FUGE - 18.0                 # die Laschen der vorderen Hälfte greifen 18 mm in die hintere (bis x = −12)
LASCHE_VOR = FUGE + 8.0                  # … und sind 8 mm weit in der vorderen Hälfte verankert
LASCHE_D = 6.0                           # Seitenlaschen 6 mm dick (Gewinde greift 6 mm)
VERSTAERKUNG = 3.0                       # hintere Hälfte: Seitenwand an der Fuge innen +3 mm (6 mm Wand für die Senkung)
SEITE_Z0 = STIRN - VERSTAERKUNG          # Seitenlasche liegt innen davor: |z| = 78 … 84
SEITE_Y = (27.0, 38.0)                   # Höhen der beiden seitlichen Schrauben (unter den Zierrillen)
MITTE_LASCHE = (8.0, 34.0)               # Mittellasche: Dicke (z) und Oberkante (y)
MITTE_BLOCK = 10.0                       # Block der hinteren Hälfte daneben (z), Schrauben von innen
MITTE_X = (-6.5, 2.0)                    # x der beiden mittleren Schrauben
MITTE_Y = 26.0                           # Höhe der mittleren Schrauben
LASCHE_LUFT = 0.2                        # Luft rund um die Laschen in der hinteren Hälfte

AUS = Path(__file__).resolve().parent / "ebene1"


def P(x, y, z):
    return Pos(x, -z, y)


def zyl_z(r, x, y, z0, z1):
    return P(x, y, (z0 + z1) / 2) * Rot(90, 0, 0) * Cylinder(r, abs(z1 - z0))


def zyl_x(r, y, z, x0, x1):
    return P((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, abs(x1 - x0))


def zyl_y(r, x, z, y0, y1):
    return P(x, (y0 + y1) / 2, z) * Cylinder(r, y1 - y0)


def quader(x0, x1, y0, y1, z0, z1):
    return P((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(z1 - z0), abs(y1 - y0))


def langloch_z(x, y, z0, z1, laenge, breite):
    """Waagerechtes Langloch durch eine Seitenwand (runde Enden). Kleine Löcher bis ca. Ø 10 mm druckt jeder Drucker ohne Stützen."""
    form = extrude(SlotCenterToCenter(laenge, breite), abs(z1 - z0), both=True)
    return P(x, y, (z0 + z1) / 2) * Rot(90, 0, 0) * form


def nase_keil(achse, wand, spitze, n0, n1, mitte, halb):
    """Rastnase als Keil: oben waagerecht, unten 40° schräg – druckt ohne Stützen.
    achse "z": Wand bei z = wand, Spitze bei z = spitze, Mitte der Nase bei x = mitte (halbe Länge halb).
    achse "x": Wand bei x = wand, Spitze bei x = spitze, Mitte bei z = mitte."""
    aus = wand + (0.05 if wand > spitze else -0.05)
    if achse == "z":
        prof = Plane.YZ * Polygon((-aus, n0), (-aus, n1), (-spitze, n1), (-spitze, n1 - 0.2), align=None)
        return Pos(mitte, 0, 0) * extrude(prof.face(), halb, both=True)
    prof = Plane.XZ * Polygon((aus, n0), (aus, n1), (spitze, n1), (spitze, n1 - 0.2), align=None)
    return Pos(0, -mitte, 0) * extrude(prof.face(), halb, both=True)


def senkung_unten(x, z, sitz, y_unten):
    """Senkung für einen Zylinderkopf von unten (beim Druck unten) mit Brücken-Trick: über der Senkung erst ein
    Schlitz, dann ein Quadrat in Lochbreite (je 0,3 mm) – so überbrückt der Drucker die Decke ohne Stützen."""
    t = zyl_y(KOPF_D / 2, x, z, y_unten, sitz)
    t += quader(x - KOPF_D / 2, x + KOPF_D / 2, sitz - 0.01, sitz + 0.3, z - DURCH / 2, z + DURCH / 2)
    t += quader(x - DURCH / 2, x + DURCH / 2, sitz + 0.29, sitz + 0.6, z - DURCH / 2, z + DURCH / 2)
    return t


def tasche(name, x, z, ix, iz, nase_h, wand_h, art):
    """Einklick-Tasche auf dem Wannenboden."""
    ax, az = ix / 2 + LUFT, iz / 2 + LUFT
    y0 = BODEN_OBEN
    r = quader(x - ax - TWAND, x + ax + TWAND, y0 - 0.1, y0 + wand_h, z - az - TWAND, z + az + TWAND)
    r -= quader(x - ax, x + ax, y0 - 0.2, y0 + wand_h + 0.1, z - az, z + az)
    if art == "enden":   # Längsseiten weg
        for s in (1, -1):
            r -= quader(x - ax - 0.01, x + ax + 0.01, y0 - 0.2, y0 + wand_h + 0.2, z + s * (az - 0.1), z + s * (az + TWAND + 0.2))
    if art in ("+x", "-x"):
        s = 1 if art == "+x" else -1
        r -= quader(x + s * (ax - 0.1), x + s * (ax + TWAND + 0.2), y0 - 0.2, y0 + wand_h + 0.2, z - az - TWAND - 0.1, z + az + TWAND + 0.1)
        if wand_h > 5:   # WAGO: Rückwand niedrig, damit die Hebel frei aufklappen
            r -= quader(x - s * (ax - 0.1), x - s * (ax + TWAND + 0.2), y0 + 4, y0 + wand_h + 0.2, z - az - TWAND - 0.1, z + az + TWAND + 0.1)
    # Rastnasen
    n0, n1 = y0 + nase_h - 0.1, y0 + nase_h + 0.9      # Keil: 1 mm hoch, Unterseite schräg
    if art in ("enden",) or (art in ("+x", "-x") and iz > ix):
        # Nasen an den x-Enden (bzw. bei WAGO an den kurzen z-Enden)
        if art == "enden":
            for s in (1, -1):
                r += nase_keil("x", x + s * ax, x + s * (ax - NASE), n0, n1, z, 4)
        else:
            for s in (1, -1):
                r += nase_keil("z", z + s * az, z + s * (az - NASE), n0, n1, x, 4)
    else:
        for s in (1, -1):
            r += nase_keil("z", z + s * az, z + s * (az - NASE), n0, n1, x, 4)
    return r


# ------------------------------------------------------------------ Wanne
def wanne():
    hoehe = RAND - BODEN_UNTEN
    # Außenform = Draufsicht (abgerundetes Rechteck) ∩ Seitenansicht (mit Kufen). Die 45°-Fase unten an den Längsseiten
    # entsteht, indem sich die Seitenansicht in den äußeren FASE mm nach außen hin um 45° verjüngt – so folgt die Fase
    # auch den Kufen, und es gibt nirgends einen Überhang.
    draufsicht = Pos(XM, 0, BODEN_UNTEN - 1) * extrude(RectangleRounded(L, B, R_ECKE), hoehe + 1)
    profil = seitenprofil()
    kern = extrude(profil, B / 2 - FASE, both=True)
    keil = extrude(profil, FASE, taper=45)
    if keil.bounding_box().max.Y < 0.01:          # Richtung der Extrusion vereinheitlichen (nach +Y)
        keil = keil.mirror(Plane.XZ)
    keil = Pos(0, B / 2 - FASE, 0) * keil
    seite = kern + keil + keil.mirror(Plane.XZ)
    aussen = draufsicht & seite
    innen = (Pos(XM, 0, BODEN_UNTEN - 1) * extrude(RectangleRounded(L - 2 * WAND, B - 2 * WAND, R_ECKE - WAND), hoehe + 2)) \
        & extrude(seitenprofil(BODEN, max(0.5, KUFE_RADIUS - BODEN), RAND + 10), B, both=True)
    teil = aussen - innen

    for mx in MOTOREN_X:
        for s in (1, -1):
            zb = s * BUEGEL_Z
            teil += quader(mx - BUEGEL_FUSS, mx + BUEGEL_FUSS, BODEN_OBEN, ACHSE, zb - BUEGEL_DICKE / 2, zb + BUEGEL_DICKE / 2)
            teil += quader(mx - 14, mx + 14, BODEN_OBEN, ACHSE, s * SATTEL_Z - 2, s * SATTEL_Z + 2)
            teil -= zyl_z(MOTOR_R + 0.2, mx, ACHSE, s * (STIRN - MOTOR_LANG), s * STIRN)
            for k in (-BUEGEL_LOCH, BUEGEL_LOCH):
                teil -= zyl_y(PILOT / 2, mx + k, zb, ACHSE - 10, ACHSE + 0.1)
            teil -= zyl_z(LAGER_D / 2, mx, ACHSE, s * (STIRN - 1), s * (STIRN + WAND + 1))
            for k in (-1, 1):
                teil -= langloch_z(mx + k * (LOCH_MIN + LOCH_MAX) / 2, ACHSE, s * (STIRN - 1), s * (STIRN + WAND + 1),
                                   LOCH_MAX - LOCH_MIN, DURCH)

    # Säulen bis zum Rand, Schraube von unten (Kopf bündig im Boden)
    for (x, z) in SAEULEN:
        teil += zyl_y(DOM_D / 2, x, z, BODEN_OBEN - 0.1, RAND)
        # Rippe von der Säule bis in die Stirnwand: volle Höhe, damit die Säule fest mit der Außenwand verbunden ist
        xw = X_VORNE - WAND / 2 if x > XM else X_HINTEN + WAND / 2
        teil += quader(x, xw, BODEN_OBEN - 0.1, RAND, z - RIPPE / 2, z + RIPPE / 2)
        teil -= zyl_y(DURCH / 2, x, z, BODEN_UNTEN - 1, RAND + 1)

    # Akkuhalter: Sockel + Senkung von unten
    akku_loecher = [(AKKU_X, sz * AKKU_Z + k * AKKU_LOCH) for sz in (1, -1) for k in (1, -1)]
    for (x, z) in akku_loecher:
        teil += zyl_y(5.5, x, z, BODEN_OBEN - 0.1, BODEN_OBEN + AKKU_SOCKEL)
        teil -= zyl_y(DURCH / 2, x, z, BODEN_UNTEN - 1, BODEN_OBEN + AKKU_SOCKEL + 1)
        teil -= senkung_unten(x, z, BODEN_UNTEN + KOPF_H, BODEN_UNTEN - 1)

    # Taschen für die Stromversorgung
    for t in TASCHEN:
        teil += tasche(*t)

    # Rückwand: USB-C des Ladeboards und runder Druckschalter
    xr = X_HINTEN
    for (name, z, y, br, h, rund) in RUECKWAND:
        if rund:
            teil -= zyl_x(br / 2, y, z, xr - 1, xr + WAND + 1)
        else:
            teil -= P(xr + WAND / 2, y, z) * Rot(0, 90, 0) * extrude(RectangleRounded(h, br, min(br, h) / 2 - 0.01), WAND + 2, both=True)

    # Kabelbinder-Schlitze im Boden (abgerundet) und eine flache Rille unten, die beide verbindet
    sl, sb = BINDER_SCHLITZ
    for (x, z) in KABELBINDER:
        for s in (1, -1):
            teil -= P(x, BODEN_UNTEN - 1, z + s * BINDER_ABSTAND / 2) * extrude(RectangleRounded(sl, sb, sb / 2 - 0.01), BODEN + 2)
        lang = BINDER_ABSTAND + sb + 1.0
        teil -= P(x, BODEN_UNTEN - 1, z) * extrude(RectangleRounded(sl + 0.6, lang, (sl + 0.6) / 2 - 0.01), 1 + BINDER_RILLE)

    # Lüftungsgitter unter dem Akku
    for i in range(-2, 3):
        for j in range(-8, 9):
            x = AKKU_X + i * 8.6
            z = j * 9.9 + (4.95 if i % 2 else 0)
            if abs(x - AKKU_X) > 16 or abs(z) > 74:
                continue
            if any(abs(x - ax) < 7 and abs(z - az) < 7 for (ax, az) in akku_loecher):
                continue
            if any(abs(x - px) < 8 and abs(z - pz) < 9 for (px, pz) in PRUEF_PUNKTE):
                continue
            teil -= P(x, BODEN_UNTEN - 1, z) * extrude(RegularPolygon(3.4, 6), BODEN + 2)

    # Halter für die Nahsensoren: an jedem Ende der Platine ein Pfosten mit Nut (nach innen offen).
    # Die Platine wird von oben eingeschoben und sitzt unten auf (Nut beginnt erst bei TOF_UNTEN).
    # Der ganze Halter ist um TOF_NEIGUNG gekippt (Drehpunkt = Sensor), die Platine lehnt oben leicht nach innen.
    for (name, s) in TOF:
        wand, vorn, hinten = tof_lage(s)
        oben = TOF_UNTEN + TOF_H + 1.0
        x_innen = hinten - s * 1.8                                  # Rückseite des Pfostens
        ys = TOF_UNTEN + TOF_H / 2 + TOF_SENSOR_Y                   # Höhe des Sensors = Drehpunkt
        for sz in (1, -1):
            z0, z1 = sz * (TOF_L / 2 - 1.5), sz * (TOF_L / 2 + 3.0)
            halter = quader(x_innen, wand + s * 2.0, BODEN_OBEN - 4, oben, z0, z1)
            halter -= quader(hinten - s * 0.15, vorn + s * 0.15, TOF_UNTEN, oben + 1, z0 - sz * 0.1, sz * (TOF_L / 2 + 0.3))
            halter = halter.rotate(Axis((vorn, 0, ys), (0, 1, 0)), -s * TOF_NEIGUNG)
            teil += halter
        # Fenster in der Wand vor dem Sensor, außen mit einem 1,5 mm tiefen Rahmen (Sichtkegel 27° bleibt frei)
        fb, fh = TOF_FENSTER
        ym = TOF_UNTEN + TOF_H / 2 + TOF_SENSOR_Y
        xa = X_VORNE if s > 0 else X_HINTEN
        # Fenster mit 45°-Ecken statt runder Ecken – oben bleibt nur eine gerade Brücke
        e = 2.5
        fen = Plane.YZ * Polygon(*[(-zz, ym + yy) for (zz, yy) in [(-fb / 2 + e, -fh / 2), (fb / 2 - e, -fh / 2), (fb / 2, -fh / 2 + e), (fb / 2, fh / 2 - e),
                                                                      (fb / 2 - e, fh / 2), (-fb / 2 + e, fh / 2), (-fb / 2, fh / 2 - e), (-fb / 2, -fh / 2 + e)]], align=None)
        teil -= Pos((wand + xa) / 2, 0, 0) * extrude(fen.face(), WAND / 2 + 1, both=True)
        # Rahmen als 45°-Fase rund um das Fenster (statt einer Stufe – die würde oben überhängen)
        teil -= P(xa + s * 0.5, ym, 0) * Rot(0, -90 * s, 0) * extrude(RectangleRounded(fh + 4, fb + 4, 4.5), 2.0, taper=45)

    # Nichts darf unten aus der Außenform herausragen (Säulen und Rippen beginnen innen auf Bodenhöhe –
    # in den Kufen liegt die Unterseite höher, dort würden sie sonst herausstehen)
    # Prüfstand-Aufnahmen: innen verstärken
    kl, kb, kt = PRUEF_KERBE
    for (x, z) in PRUEF_PUNKTE:
        teil += quader(x - kl / 2 - 1, x + kl / 2 + 1, BODEN_OBEN - 0.1, BODEN_OBEN + PRUEF_VERSTAERKUNG, z - kb / 2 - 1, z + kb / 2 + 1)

    teil = teil & aussen

    # Prüfstand-Aufnahmen: Kerbe unten (unten 0,6 mm angefast, damit die Stempel leicht hineinfinden)
    for (x, z) in PRUEF_PUNKTE:
        teil -= quader(x - kl / 2, x + kl / 2, BODEN_UNTEN - 1, BODEN_UNTEN + kt, z - kb / 2, z + kb / 2)
        teil -= P(x, BODEN_UNTEN - 0.01, z) * extrude(Rectangle(kl + 1.22, kb + 1.22), 0.61, taper=45)

    # Säulen: Senkung für den Schraubenkopf jetzt in der Schräge – flacher Sitz so hoch, dass der Kopf ganz versenkt ist
    for (x, z) in SAEULEN:
        sitz = max(unterkante(x + d / 10) for d in range(-33, 34)) + KOPF_H
        teil -= senkung_unten(x, z, sitz, BODEN_UNTEN - 10)
        teil -= zyl_y(DURCH / 2, x, z, BODEN_UNTEN - 10, RAND + 1)

    # Zierrillen an den Seiten
    for s in (1, -1):
        for y in (44.0, 48.5):
            # Querschnitt: unten waagerecht, oben 45° schräg – kein Überhang
            zi, za = s * (B / 2 - 0.8), s * (B / 2 + 1)
            prof = Plane.YZ * Polygon((-za, y), (-zi, y), (-zi, y + 0.8), (-za, y + 1.6 + (za - s * B / 2) * s), align=None)
            teil -= Pos(XM, 0, 0) * extrude(prof.face(), 40, both=True)
    return teil


# ------------------------------------------------------------------ Teilung in zwei Hälften
def teilen(teil):
    """Ganze Wanne → (vordere Hälfte, hintere Hälfte) mit Laschen, Verstärkung und Schraubenlöchern."""
    gross = 400.0
    vorne = teil & quader(FUGE + FUGE_SPALT, gross, -gross, gross, -gross, gross)
    hinten = teil & quader(-gross, FUGE - FUGE_SPALT, -gross, gross, -gross, gross)
    aussen_form = Pos(XM, 0, BODEN_UNTEN - 1) * extrude(RectangleRounded(L, B, R_ECKE), RAND - BODEN_UNTEN + 1)
    mt, my = MITTE_LASCHE

    # --- Laschen der vorderen Hälfte: stehen auf dem Bett (Unterkante = Wannenboden unten), daher ohne Stützen
    laschen = None
    for s in (1, -1):
        za, zb = s * (SEITE_Z0 - LASCHE_D), s * SEITE_Z0
        l = quader(LASCHE_BIS, LASCHE_VOR, BODEN_UNTEN, RAND, za, zb)
        l += quader(FUGE + FUGE_SPALT, LASCHE_VOR, BODEN_UNTEN, RAND, zb, s * (STIRN + 0.5))   # in der vorderen Hälfte bis an die Wand
        laschen = l if laschen is None else laschen + l
    laschen += quader(LASCHE_BIS, LASCHE_VOR, BODEN_UNTEN, my, -mt / 2, mt / 2)
    vorne = vorne + (laschen & aussen_form)

    # --- hintere Hälfte: Platz für die Laschen (auch durch den Boden), Seitenwand innen verstärkt, Block in der Mitte
    for s in (1, -1):
        hinten += quader(LASCHE_BIS - 4, FUGE - FUGE_SPALT, BODEN_OBEN - 0.1, RAND, s * SEITE_Z0, s * (STIRN + 0.5))
        za, zb = s * (SEITE_Z0 - LASCHE_D - LASCHE_LUFT), s * (SEITE_Z0 + 0.01)
        hinten -= quader(LASCHE_BIS - LASCHE_LUFT, FUGE + 1, BODEN_UNTEN - 1, RAND + 1, za, zb)
    hinten += quader(LASCHE_BIS - 2, FUGE - FUGE_SPALT, BODEN_OBEN - 0.1, my, mt / 2 + LASCHE_LUFT, mt / 2 + LASCHE_LUFT + MITTE_BLOCK)
    hinten -= quader(LASCHE_BIS - LASCHE_LUFT, FUGE + 1, BODEN_UNTEN - 1, my + 1, -mt / 2 - LASCHE_LUFT, mt / 2 + LASCHE_LUFT)
    hinten = hinten & aussen_form

    # --- Schrauben: Seiten von außen (Senkung in der verstärkten Wand), Mitte von innen durch den Block
    xs = (LASCHE_BIS + FUGE) / 2
    for s in (1, -1):
        for y in SEITE_Y:
            hinten -= zyl_z(DURCH / 2, xs, y, s * (SEITE_Z0 - 1), s * (B / 2 + 1))
            hinten -= zyl_z(KOPF_D / 2, xs, y, s * (B / 2 - KOPF_H), s * (B / 2 + 1))
            vorne -= zyl_z(PILOT / 2, xs, y, s * (SEITE_Z0 - LASCHE_D - 1), s * (SEITE_Z0 + 1))
    zb = mt / 2 + LASCHE_LUFT + MITTE_BLOCK
    for x in MITTE_X:
        hinten -= zyl_z(DURCH / 2, x, MITTE_Y, 0, zb + 1)
        vorne -= zyl_z(PILOT / 2, x, MITTE_Y, -mt / 2 - 1, mt / 2 + 1)
    return vorne, hinten



# ------------------------------------------------------------------ Schraubendreher-Zugang
DREHER_R, DREHER_L = 3.0, 60.0           # gedachter Schraubendreher: Ø 6 mm, 60 mm lang (Schaft + Anfang des Griffs)


def dreher(x, y, z, achse, richtung):
    """Raum, den ein Schraubendreher von einem Schraubenkopf aus braucht (Zylinder entlang der Achse, ab 0,5 mm vor dem Kopf)."""
    a, b = 0.5 * richtung, (0.5 + DREHER_L) * richtung
    if achse == "x":
        return zyl_x(DREHER_R, y, z, x + a, x + b)
    if achse == "z":
        return zyl_z(DREHER_R, x, y, z + a, z + b)
    return zyl_y(DREHER_R, x, z, y + a, y + b)


def zugang_pruefen(schrauben, druckteile, bauteile):
    """schrauben: (Name, x, y, z, Achse, Richtung nach außen); druckteile: Körper; bauteile: (Name, x0, x1, y0, y1, z0, z1)."""
    fehler = 0
    for (name, x, y, z, achse, richtung) in schrauben:
        d = dreher(x, y, z, achse, richtung)
        im_weg = [n for (n, t) in druckteile if (d & t).volume > 0.5]
        im_weg += [n for (n, x0, x1, y0, y1, z0, z1) in bauteile if (d & quader(x0, x1, y0, y1, z0, z1)).volume > 0.5]
        if im_weg:
            print(f"  NICHT erreichbar: {name} – im Weg: {', '.join(im_weg)}"); fehler += 1
        else:
            print(f"  erreichbar: {name}")
    print("Schraubendreher-Zugang – Probleme:", fehler)
    return fehler


# ------------------------------------------------------------------ Motorbügel
def motorbuegel(mx=MOTOR_X, s=1):
    d = BUEGEL_DICKE
    r_i, r_a = MOTOR_R + 0.3, MOTOR_R + 3.3
    zm = s * BUEGEL_Z
    bogen = zyl_z(r_a, mx, ACHSE, zm - d / 2, zm + d / 2) - zyl_z(r_i, mx, ACHSE, zm - d, zm + d)
    bogen -= quader(mx - r_a - 1, mx + r_a + 1, ACHSE - r_a - 1, ACHSE, zm - d, zm + d)
    fuesse = quader(mx - BUEGEL_FUSS, mx + BUEGEL_FUSS, ACHSE, ACHSE + 3, zm - d / 2, zm + d / 2)
    fuesse -= zyl_z(r_i, mx, ACHSE, zm - d, zm + d)
    teil = bogen + fuesse
    for k in (-BUEGEL_LOCH, BUEGEL_LOCH):
        teil -= zyl_y(DURCH / 2, mx + k, zm, ACHSE - 1, ACHSE + 4)
    return teil


# ------------------------------------------------------------------ Prüfung (Draufsicht)
def ueberlappungen():
    belegt = []
    for mx in MOTOREN_X:
        for s in (1, -1):
            sx = 1 if mx > 0 else -1
            z_a, z_b = s * (STIRN - MOTOR_LANG - 9), s * STIRN     # mit Encoder-Stecker innen
            belegt.append((f"Motor {sx},{s}", mx - 12.6, mx + 12.6, min(z_a, z_b), max(z_a, z_b)))
            belegt.append((f"Sattel/Bügel {sx},{s}", mx - BUEGEL_FUSS, mx + BUEGEL_FUSS, s * BUEGEL_Z - 5, s * BUEGEL_Z + 5))
    ax, az = AKKU_MASS
    for sz in (1, -1):
        belegt.append((f"Akkuhalter {sz}", AKKU_X - ax / 2 - 0.5, AKKU_X + ax / 2 + 0.5, sz * AKKU_Z - az / 2, sz * AKKU_Z + az / 2))
    kl, kb, _kt = PRUEF_KERBE
    for (x, z) in PRUEF_PUNKTE:
        if x > FUGE:      # hinten liegen die Kerben unter dem Akku (darüber 3 mm Luft) – vorne muss der Boden frei sein
            belegt.append((f"Prüfstand-Kerbe {x},{z}", x - kl / 2 - 1, x + kl / 2 + 1, z - kb / 2 - 1, z + kb / 2 + 1))
    # Fuge: Laschen der vorderen Hälfte und Block der hinteren Hälfte
    for s in (1, -1):
        za, zb = s * (SEITE_Z0 - LASCHE_D), s * STIRN
        belegt.append((f"Seitenlasche {s}", LASCHE_BIS, LASCHE_VOR, min(za, zb), max(za, zb)))
    mt = MITTE_LASCHE[0] / 2
    belegt.append(("Mittellasche + Block", LASCHE_BIS, LASCHE_VOR, -mt, mt + MITTE_BLOCK))
    for (x, z) in SAEULEN:
        belegt.append((f"Säule {x},{z}", x - 5, x + 5, z - 5, z + 5))
    for (x, z) in KABELBINDER:   # oben muss über den Schlitzen Platz für das Kabel und den Kabelbinder sein
        belegt.append((f"Kabelbinder {x},{z}", x - 3, x + 3, z - BINDER_ABSTAND / 2 - 2, z + BINDER_ABSTAND / 2 + 2))
    for (name, x, z, ix, iz, _n, _w, art) in TASCHEN:
        x0, x1 = x - ix / 2 - LUFT - TWAND, x + ix / 2 + LUFT + TWAND
        if art == "-x":
            x0 += TWAND          # offene Seite hat keine Wand
        if art == "+x":
            x1 -= TWAND
        z0, z1 = z - iz / 2 - LUFT - TWAND, z + iz / 2 + LUFT + TWAND
        if art == "enden":
            z0, z1 = z - iz / 2 - LUFT, z + iz / 2 + LUFT
        belegt.append((f"Tasche {name}", x0, x1, z0, z1))
    for (name, s) in TOF:
        wand, vorn, hinten = tof_lage(s)
        x_innen = hinten - s * 1.8
        belegt.append((f"Nahsensor {name}", min(x_innen, wand), max(x_innen, wand), -(TOF_L / 2 + 3), TOF_L / 2 + 3))
    x, z, lx, bz = SICHERUNG
    belegt.append(("Sicherungshalter", x - lx / 2, x + lx / 2, z - bz / 2, z + bz / 2))
    fehler = 0
    for i in range(len(belegt)):
        for j in range(i + 1, len(belegt)):
            a, b = belegt[i], belegt[j]
            if a[0].startswith(("Motor", "Sattel")) and b[0].startswith(("Motor", "Sattel")):
                continue
            # Rechtecke (Name, x0, x1, z0, z1) überlappen, wenn sie sich in x UND in z überschneiden
            if a[1] < b[2] - 0.01 and b[1] < a[2] - 0.01 and a[3] < b[4] - 0.01 and b[3] < a[4] - 0.01:
                print("  Überschneidung:", a[0], "<->", b[0]); fehler += 1
    for (name, x0, x1, z0, z1) in belegt:
        if x0 < X_HINTEN + WAND - 0.01 or x1 > X_VORNE - WAND + 0.01 or z0 < -B / 2 + WAND - 0.01 or z1 > B / 2 - WAND + 0.01:
            if not name.startswith(("Motor", "Säule")):   # Motoren sitzen an der Wand, hintere Säulen gehen gewollt in die Wand über
                print("  ragt in die Wand:", name); fehler += 1
    # Jede Tasche, jeder Halter liegt ganz in EINER Hälfte (nicht über der Fuge)
    for (name, x0, x1, z0, z1) in belegt:
        if name.startswith(("Seitenlasche", "Mittellasche", "Motor", "Sattel")):
            continue
        if x0 < FUGE + FUGE_SPALT + 0.5 and x1 > FUGE - FUGE_SPALT - 0.5:
            print("  liegt über der Fuge:", name); fehler += 1
    print("Überschneidungen:", fehler)


if __name__ == "__main__":
    AUS.mkdir(exist_ok=True)
    ueberlappungen()
    for (x, z) in SAEULEN:
        sitz = max(unterkante(x + d / 10) for d in range(-33, 34)) + KOPF_H
        laenge = 45 if sitz + 45 <= 68.5 else 40          # Kernloch im Deck reicht von 58 bis 68
        print(f"Säule {x:+6.1f}/{z:+5.1f}: Kopfauflage bei y = {sitz:5.2f} mm → M3 × {laenge}, greift {sitz + laenge - 58:4.1f} mm im Deck")
    w = wanne()
    vorne, hinten = teilen(w)
    teile = {"wanne_vorne": vorne, "wanne_hinten": hinten, "motorbuegel": motorbuegel()}   # die ganze Wanne wird nicht mehr als Datei ausgegeben
    # Selbstprüfung: jede Säule muss auf ganzer Höhe und Breite mit der Stirnwand verbunden sein (CAD-Rechenfehler finden)
    from build123d import Vector
    luecken = [(x, z, y) for (x, z) in SAEULEN for dz in (-4.5, 4.5) for y in (25, 35, 45, 55)
               if not w.is_inside(Vector(x + (4.0 if x > XM else -4.0), -(z + dz), y))]
    print("Säulen mit der Stirnwand verbunden:", "ja" if not luecken else f"NEIN – Lücke bei {luecken}")
    # Selbstprüfung Fuge: die Hälften dürfen sich nicht durchdringen, und die Laschen müssen mit der vorderen Hälfte verbunden sein
    v = (vorne & hinten).volume
    print(f"Hälften durchdringen sich: {'nein' if v < 0.5 else f'JA ({v:.1f} mm³)'}")
    # Schraubendreher-Zugang zu den Schrauben der Fuge: seitlich von außen, in der Mitte von innen (zwischen Akku und INA226)
    mt = MITTE_LASCHE[0] / 2
    xs = (LASCHE_BIS + FUGE) / 2
    schrauben = [(f"Fuge seitlich {'links' if s > 0 else 'rechts'} y={y:.0f}", xs, y, s * B / 2, "z", s) for s in (1, -1) for y in SEITE_Y]
    schrauben += [(f"Fuge Mitte x={x:+.1f}", x, MITTE_Y, mt + LASCHE_LUFT + MITTE_BLOCK, "z", 1) for x in MITTE_X]
    ax, az = AKKU_MASS
    bauteile = [(f"Akkuhalter {sz:+d}", AKKU_X - ax / 2, AKKU_X + ax / 2, BODEN_OBEN + AKKU_SOCKEL, BODEN_OBEN + AKKU_SOCKEL + 18, sz * AKKU_Z - az / 2, sz * AKKU_Z + az / 2) for sz in (1, -1)]
    bauteile += [(f"Tasche {n}", x - ix / 2 - 2, x + ix / 2 + 2, BODEN_OBEN, BODEN_OBEN + wh + 3, z - iz / 2 - 2, z + iz / 2 + 2) for (n, x, z, ix, iz, _nh, wh, _a) in TASCHEN]
    sx_, sz_, slx, sbz = SICHERUNG
    bauteile.append(("Sicherungshalter", sx_ - slx / 2, sx_ + slx / 2, BODEN_OBEN, BODEN_OBEN + 25.5, sz_ - sbz / 2, sz_ + sbz / 2))
    zugang_pruefen(schrauben, [("Wanne", vorne + hinten)], bauteile)
    for name, t in (("vordere Hälfte", vorne), ("hintere Hälfte", hinten)):
        print(f"{name}: {len(t.solids())} Körper", "(gut)" if len(t.solids()) == 1 else "– NICHT zusammenhängend!")
    for name, t in teile.items():
        export_stl(t, str(AUS / f"{name}.stl"), tolerance=0.02, angular_tolerance=0.15)
        export_step(t, str(AUS / f"{name}.step"))
        bb = t.bounding_box()
        print("gültig" if t.is_valid else "UNGÜLTIG", f"{name:12s} {bb.size.X:6.1f} × {bb.size.Y:6.1f} × {bb.size.Z:5.1f} mm  Volumen {t.volume / 1000:6.1f} cm³")
    alle_buegel = Compound([motorbuegel(mx, s) for mx in MOTOREN_X for s in (1, -1)])
    export_step(alle_buegel, str(AUS / "motorbuegel_alle_4.step"))
    print("fertig:", AUS)
