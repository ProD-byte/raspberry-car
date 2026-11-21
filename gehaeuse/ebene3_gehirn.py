"""Raspberry Car – Ebene 3: Gehirn (Klappdeckel)

Ein Druckteil: Boden (Ebene 3) und Seitenwände bis Ebene 4 in einem Stück. Der ganze obere Teil des Autos
klappt nach hinten auf wie eine Motorhaube – dann liegt Ebene 2 offen. Alle Maße in mm.
Erzeugt STL und STEP in gehaeuse/ebene3/.

Aufruf (einmalig: pip install build123d):
    python ebene3_gehirn.py

Koordinaten wie im 3D-Modell: x nach vorne (vorne = Kamera, hinten = Ladebuchse und Schalter), z nach links, y nach oben.

Was darauf sitzt:
  * Raspberry Pi 5 mit Active Cooler und AI HAT+: 4 Dome (5 mm), M2,5-Schrauben von unten durch Boden, Dom und Pi
    in die 16-mm-Abstandshalter des AI HAT+ (liegen dem HAT bei). M2,5, weil die Löcher des Pi nur 2,7 mm groß sind.
  * Pololu D36V50F5 (5 V für den Pi) vorne rechts in einer Einklick-Tasche, nah an der USB-C-Buchse des Pi.
  * 4G/GPS-Modul Waveshare SIM7600G-H 4G DONGLE (Platine ohne Kunststoffhülle, 82,3 × 40,2 mm, mit USB-A-Stecker
    und SMA-Buchse 107 mm lang): steht senkrecht links neben dem Pi, von oben in zwei Nut-Säulen eingeschoben
    (die Platine hat keine Befestigungslöcher). USB-Stecker nach hinten, über ein kurzes USB-Kabel zum Pi.
  * Kamera Modul 3 Wide vorne: in zwei Nuten von oben eingeschoben, schaut durch ein Fenster in der Vorderwand.
  * Lüftungsschlitze in beiden Seitenwänden (der AI HAT+ braucht Luft).

Klappdeckel:
  * Hinten zwei Scharniere außen an der Trennfuge (Achse 5 mm hinter der Rückwand, 5 mm über dem Boden). Je Scharnier
    zwei Lappen am Deckel und einer am Ring von Ebene 2, Achse = M3 × 16 (Gewinde schneidet sich in den äußeren Lappen).
    Weil die Achse hinter und über allem liegt, stößt beim Aufklappen nichts an (das Skript prüft das bis 100°).
  * Vorne zwei M3 × 12 waagerecht durch die Vorderwand (Köpfe bündig) in zwei Laschen, die vom Ring von Ebene 2 durch
    Schlitze im Boden nach oben ragen.

Druck: Boden aufs Bett, ohne Stützen.
"""
import math
from pathlib import Path
from build123d import (Box, Cylinder, Rot, Rectangle, RectangleRounded, Pos, Plane, Polygon, Axis, extrude,
                       export_stl, export_step, Vector)

import ebene2_elektronik as e2

# ------------------------------------------------------------------ Parameter
X_VORNE, X_HINTEN, XM, L, B, R_ECKE = e2.X_VORNE, e2.X_HINTEN, e2.XM, e2.L, e2.B, e2.R_ECKE
WAND = e2.RING_WAND
UNTEN = e2.EBENE3_UNTEN                  # 84: liegt auf dem Ring von Ebene 2
DICKE = 3.0
OBEN = UNTEN + DICKE                     # 87
DACH = 132.0                             # Unterkante Ebene 4
PILOT, DURCH, KOPF_D, KOPF_H = e2.PILOT, e2.DURCH, e2.KOPF_D, e2.KOPF_H

# Raspberry Pi 5 (Mitte x = −8, USB/Ethernet nach hinten), Löcher 58 × 49
PI_X = -8.0
PI_LOECHER = [(PI_X - 19, 24.5), (PI_X - 19, -24.5), (PI_X + 39, 24.5), (PI_X + 39, -24.5)]
PI_DOM_D, PI_DOM_H = 6.5, 5.0
M25_DURCH, M25_KOPF_D, M25_KOPF_H = 2.8, 5.0, 2.6

# Einklick-Taschen (wie Ebene 2): Name, x, z, Innenmaß x, Innenmaß z, Höhe Rastnase, Wandhöhe, offene Seite
LUFT, TWAND, NASE = 0.3, 1.6, 0.6
TASCHEN = [
    ("Pololu D36V50F5", 52.0, -36.0, 25.4, 25.4, 1.6, 3.2, None),
]
# 4G-Dongle (Platine senkrecht, Länge entlang x): Platine x = LTE_X0 … LTE_X0 + 82,3, Leiterplatte z = LTE_Z − 1,6 … LTE_Z
LTE_X0, LTE_Z, LTE_LAENGE, LTE_PCB = -59.0, 50.0, 82.3, 1.6
LTE_NUT_UNTEN, LTE_SAEULE_H = 4.5, 13.0     # an den Enden ist die Platine erst ab 5,2 mm über der Unterkante; USB/SMA ab 14 mm
# Durchbrüche im Boden (x, z, Länge x, Breite z)
SCHLITZE = [
    (-111.0, 0.0, 10.0, 20.0),           # hinten Mitte, nah am Scharnier: USB Pico → Pi und Akku-Plus/Minus zum Pololu
]
# Kamera Modul 3 Wide (25 × 24 mm, 1 mm dick): Platine senkrecht, Objektiv nach vorne
KAM_B, KAM_H, KAM_T = 25.0, 24.0, 1.0
KAM_X = 73.6                             # Vorderseite der Platine
KAM_UNTEN = OBEN + 4.0                   # Platz für den Flachbandstecker unten
KAM_OBJ_Y = KAM_UNTEN + 14.5             # Mitte Objektiv
KAM_FENSTER = 18.0                       # Weitwinkel (120°): großes Fenster, außen angefast

SCH_X, SCH_Y, SCH_R, SCH_Z, SCH_RING_B = e2.SCH_X, e2.SCH_Y, e2.SCH_R, e2.SCH_Z, e2.SCH_RING_B
SCH_LAPPEN_B, SCH_SPALT = 5.0, 0.3
VORNE_Z, LASCHE_B, LASCHE_X0, LASCHE_X1, LASCHE_OBEN, VORNE_Y = e2.VORNE_Z, e2.LASCHE_B, e2.LASCHE_X0, e2.LASCHE_X1, e2.LASCHE_OBEN, e2.VORNE_Y
POLSTER_DICKE = 4.6                      # Verdickung der Vorderwand innen an den Schrauben
# Ebene 4: Röhren in den Ecken, Kernloch von oben
DACH_ROHRE = [(72.0, 57.6), (72.0, -57.6), (-110.0, 57.6), (-110.0, -57.6)]
# Lüftung: senkrechte Schlitze in beiden Seitenwänden
LUEFTUNG_X = [-56 + 8 * i for i in range(11)]
LUEFTUNG_Y = (100.0, 120.0)

AUS = Path(__file__).resolve().parent / "ebene3"


def P(x, y, z):
    return Pos(x, -z, y)


def quader(x0, x1, y0, y1, z0, z1):
    return P((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(z1 - z0), abs(y1 - y0))


def zyl_y(r, x, z, y0, y1):
    return P(x, (y0 + y1) / 2, z) * Cylinder(r, y1 - y0)


def zyl_z(r, x, y, z0, z1):
    return P(x, y, (z0 + z1) / 2) * Rot(90, 0, 0) * Cylinder(r, abs(z1 - z0))


def zyl_x(r, y, z, x0, x1):
    return P((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, abs(x1 - x0))


def senkung_unten(x, z, d, h, durch, y_unten):
    """Senkung von unten (beim Druck unten) mit Brücken-Trick: über der Senkung erst ein Schlitz, dann ein Quadrat."""
    t = zyl_y(d / 2, x, z, y_unten - 1, y_unten + h)
    t += quader(x - d / 2, x + d / 2, y_unten + h - 0.01, y_unten + h + 0.3, z - durch / 2, z + durch / 2)
    t += quader(x - durch / 2, x + durch / 2, y_unten + h + 0.29, y_unten + h + 0.6, z - durch / 2, z + durch / 2)
    return t


def tasche(name, x, z, ix, iz, nase_h, wand_h, offen):
    ax, az = ix / 2 + LUFT, iz / 2 + LUFT
    r = quader(x - ax - TWAND, x + ax + TWAND, OBEN - 0.1, OBEN + wand_h, z - az - TWAND, z + az + TWAND)
    r -= quader(x - ax, x + ax, OBEN - 0.2, OBEN + wand_h + 0.1, z - az, z + az)
    if offen == "-x":
        r -= quader(x - ax - TWAND - 0.2, x - ax + 0.1, OBEN - 0.2, OBEN + wand_h + 0.2, z - az - TWAND - 0.2, z + az + TWAND + 0.2)
    # Kerbe zum Heraushebeln an der Vorderseite
    r -= quader(x + ax - 0.1, x + ax + TWAND + 0.1, OBEN + 0.8, OBEN + wand_h + 0.1, z - 3, z + 3)
    # Rastnasen als Keil an den langen Seiten (z-Wände)
    n0, n1 = OBEN + nase_h - 0.1, OBEN + nase_h + 0.9
    for s in (1, -1):
        r += e2.nase_keil("z", z + s * az, z + s * (az - NASE), n0, n1, x, 3)
    return r


def aussenform(y0, y1):
    return Pos(XM, 0, y0) * extrude(RectangleRounded(L, B, R_ECKE), y1 - y0)


def scharnier_lappen():
    """Die beiden Lappen eines Scharniers am Deckel (je Scharnier außen und innen vom Ring-Lappen)."""
    t = None
    for zc in SCH_Z:
        s = 1 if zc > 0 else -1
        for k, aussen in ((1, True), (-1, False)):
            z0 = zc + k * s * (SCH_RING_B / 2 + SCH_SPALT)
            z1 = z0 + k * s * SCH_LAPPEN_B
            lappen = zyl_z(SCH_R, SCH_X, SCH_Y, z0, z1)
            lappen += quader(SCH_X, X_HINTEN + 0.5, UNTEN, SCH_Y + SCH_R, z0, z1)       # Verbindung zur Rückwand
            lappen -= zyl_z((PILOT if aussen else DURCH) / 2, SCH_X, SCH_Y, z0 - 1 * k * s, z1 + 1 * k * s)
            t = lappen if t is None else t + lappen
    return t


def deckel():
    h = DACH - UNTEN
    teil = aussenform(UNTEN, DACH)
    teil -= Pos(XM, 0, OBEN) * extrude(RectangleRounded(L - 2 * WAND, B - 2 * WAND, R_ECKE - WAND), h)

    # Raspberry Pi: Dome, M2,5 von unten (Kopf versenkt, Brücken-Trick)
    for (x, z) in PI_LOECHER:
        teil += zyl_y(PI_DOM_D / 2, x, z, OBEN - 0.1, OBEN + PI_DOM_H)
        teil -= zyl_y(M25_DURCH / 2, x, z, UNTEN - 1, OBEN + PI_DOM_H + 1)
        teil -= senkung_unten(x, z, M25_KOPF_D, M25_KOPF_H, M25_DURCH, UNTEN)

    for t in TASCHEN:
        teil += tasche(*t)

    # 4G-Dongle: zwei Säulen an den Platinen-Enden mit senkrechter Nut (Platine von oben einschieben, steht auf dem Boden)
    zm = LTE_Z - LTE_PCB / 2
    for xe, s in ((LTE_X0, -1), (LTE_X0 + LTE_LAENGE, 1)):
        saeule = quader(xe - s * 1.5, xe + s * 2.3, OBEN - 0.1, OBEN + LTE_SAEULE_H, zm - 3.0, zm + 3.0)
        saeule -= quader(xe - s * 1.6, xe + s * 0.3, OBEN + LTE_NUT_UNTEN, OBEN + LTE_SAEULE_H + 1, zm - 1.0, zm + 1.0)
        teil += saeule

    # Kamera: zwei Pfosten mit Nut an der Vorderwand (Platine von oben einschieben)
    xi = X_VORNE - WAND
    for s in (1, -1):
        z0, z1 = s * (KAM_B / 2 - 1.5), s * (KAM_B / 2 + 3.5)
        pfosten = quader(KAM_X - KAM_T - 3.0, xi + 0.5, OBEN - 0.1, KAM_UNTEN + KAM_H, z0, z1)
        pfosten -= quader(KAM_X - KAM_T - 0.15, KAM_X + 0.15, KAM_UNTEN, KAM_UNTEN + KAM_H + 1, z0 - s * 0.1, s * (KAM_B / 2 + 0.3))
        teil += pfosten
    # Fenster: rund mit flacher Oberkante (druckt ohne Stützen), außen 45° angefast
    r = KAM_FENSTER / 2
    pts = []
    for d in range(-45, 226, 5):           # Kreisbogen von oben-rechts über unten nach oben-links, oben gerade
        a = math.radians(d)
        pts.append((r * math.cos(a), KAM_OBJ_Y - r * math.sin(a)))
    fen = Plane.YZ * Polygon(*pts, align=None)
    teil -= Pos(X_VORNE - WAND / 2, 0, 0) * extrude(fen.face(), WAND, both=True)
    teil -= P(X_VORNE + 0.01, KAM_OBJ_Y, 0) * Rot(0, -90, 0) * extrude(Rectangle(KAM_FENSTER + 3, KAM_FENSTER + 3), 1.5, taper=45)

    # Lüftungsschlitze (senkrecht: oben nur 3 mm Brücke)
    for x in LUEFTUNG_X:
        for s in (1, -1):
            teil -= quader(x - 1.5, x + 1.5, LUEFTUNG_Y[0], LUEFTUNG_Y[1], s * (B / 2 - WAND - 1), s * (B / 2 + 1))

    # Durchbrüche
    for (x, z, lx, bz) in SCHLITZE:
        teil -= P(x, UNTEN + DICKE / 2, z) * extrude(RectangleRounded(lx, bz, min(lx, bz) / 2 - 0.01), DICKE + 2, both=True)

    # Vorne: Schlitze für die Laschen des Rings, Polster an der Vorderwand mit Schraubloch (Kopf bündig)
    for zc in VORNE_Z:
        teil -= quader(LASCHE_X0 - 0.5, LASCHE_X1 + 0.5, UNTEN - 1, OBEN + 1, zc - LASCHE_B / 2 - 0.5, zc + LASCHE_B / 2 + 0.5)
        teil += quader(xi - POLSTER_DICKE, xi + 0.5, OBEN - 0.1, VORNE_Y + 7.0, zc - 7, zc + 7)
        teil -= zyl_x(DURCH / 2, VORNE_Y, zc, LASCHE_X1 - 1, X_VORNE + 1)
        teil -= zyl_x(KOPF_D / 2, VORNE_Y, zc, X_VORNE - KOPF_H, X_VORNE + 1)

    # Röhren für Ebene 4 (mit der Wand verbunden), Kernloch von oben 11 mm
    for (x, z) in DACH_ROHRE:
        sz = 1 if z > 0 else -1
        r_ = zyl_y(5.0, x, z, OBEN - 0.1, DACH) + quader(x - 4.95, x + 4.95, OBEN - 0.1, DACH, z, sz * (B / 2 - WAND / 2))
        teil += r_ & aussenform(UNTEN, DACH)
        teil -= zyl_y(PILOT / 2, x, z, DACH - 11, DACH + 1)

    # Scharnier-Lappen hinten
    teil += scharnier_lappen()
    return teil


def drehen(teil, winkel):
    """Deckel um die Scharnierachse aufklappen (Winkel in Grad, vorne nach oben)."""
    achse = Axis((SCH_X, 0, SCH_Y), (0, 1, 0))      # CAD: Achse entlang Y (= −z), durch (x, y) = (SCH_X, SCH_Y)
    return teil.rotate(achse, -winkel)


def pruefen(deckel_teil, ring_teil):
    fehler = 0
    # Aufklappen: in Schritten bis 100° – berührt der Deckel den Ring von Ebene 2?
    schlimmst = 0.0
    for w in range(0, 101, 10):
        d = drehen(deckel_teil, w)
        v = (d & ring_teil).volume
        schlimmst = max(schlimmst, v)
        if v > 0.5:
            print(f"  Aufklappen {w:3d}°: stößt am Ring an ({v:.1f} mm³)"); fehler += 1
    print(f"Aufklappen 0–100°: {'frei' if not fehler else 'STÖSST AN'} (größte Berührung {schlimmst:.2f} mm³)")
    # Bauteile auf dem Boden: Überschneidungen (Draufsicht)
    rechtecke = [(n, x - ix / 2 - LUFT - TWAND, x + ix / 2 + LUFT + TWAND, z - iz / 2 - LUFT - TWAND, z + iz / 2 + LUFT + TWAND)
                 for (n, x, z, ix, iz, *_r) in TASCHEN]
    rechtecke.append(("Raspberry Pi 5", PI_X - 42.5 - 3, PI_X + 42.5, -28.0, 28.0))   # Platine + USB-Buchsen hinten
    rechtecke += [(f"Lasche {z}", LASCHE_X0 - 0.5, LASCHE_X1 + 0.5, z - LASCHE_B / 2 - 0.5, z + LASCHE_B / 2 + 0.5) for z in VORNE_Z]
    rechtecke += [(f"Röhre {x},{z}", x - 5, x + 5, z - 5, z + 5) for (x, z) in DACH_ROHRE]
    rechtecke += [(f"Durchbruch {x},{z}", x - lx / 2, x + lx / 2, z - bz / 2, z + bz / 2) for (x, z, lx, bz) in SCHLITZE]
    rechtecke.append(("4G-Dongle + USB-Kabel", LTE_X0 - 15.3 - 30, LTE_X0 + LTE_LAENGE + 9.5, LTE_Z - 4, LTE_Z + 4))
    rechtecke.append(("Kamera", KAM_X - KAM_T - 3, X_VORNE - WAND, -KAM_B / 2 - 3.5, KAM_B / 2 + 3.5))
    n = 0
    for i in range(len(rechtecke)):
        for j in range(i + 1, len(rechtecke)):
            a, b = rechtecke[i], rechtecke[j]
            if a[1] < b[2] - 0.01 and b[1] < a[2] - 0.01 and a[3] < b[4] - 0.01 and b[3] < a[4] - 0.01:
                print("  Überschneidung:", a[0], "↔", b[0]); n += 1
    print("Überschneidungen:", n)
    return fehler + n


if __name__ == "__main__":
    AUS.mkdir(exist_ok=True)
    d = deckel()
    ring = e2.ring_oben()
    pruefen(d, ring)
    export_stl(d, str(AUS / "deckel.stl"), tolerance=0.02, angular_tolerance=0.15)
    export_step(d, str(AUS / "deckel.step"))
    bb = d.bounding_box()
    print("gültig" if d.is_valid else "UNGÜLTIG", f"deckel {bb.size.X:.1f} × {bb.size.Y:.1f} × {bb.size.Z:.1f} mm, Volumen {d.volume / 1000:.1f} cm³")
