"""Raspberry Car – Ebene 3: Gehirn mit Dach (Klapphaube)

Die oberste Ebene ist eine HAUBE: Seitenwände und Dach in einem, unten offen. Alles hängt am Dach
(Raspberry Pi 5 mit AI HAT+, Kamera, Pololu, 4G-Modul, GPS-Antenne, Status-LEDs, rundes Display),
oben auf dem Dach steht der LiDAR. Die Haube klappt hinten an zwei Scharnieren nach hinten auf –
dann liegt Ebene 2 offen. Alle Maße in mm. Erzeugt STL und STEP in gehaeuse/ebene3/.

Aufruf (einmalig: pip install build123d):
    python ebene3_gehirn.py

Koordinaten wie im 3D-Modell: x nach vorne (vorne = Kamera, hinten = Ladebuchse und Schalter), z nach links, y nach oben.

Form (gegen die „Brotdose“):
  * Vorder- und Rückwand senkrecht (vorne das Kamerafenster, hinten das Scharnier).
  * Die Seitenwände sind unten 12 mm senkrecht und laufen dann schräg nach innen (oben je 7 mm schmaler).
  * Alle Kanten des Dachs 45° abgeschrägt.

Was darin hängt (alles am Dach, die Haube wird mit dem Dach nach unten gedruckt – ohne Stützen):
  * Raspberry Pi 5 mit Active Cooler und AI HAT+: Der Stapel hängt an 4 Domen unter dem Dach.
    M2,5 von oben durch Dach, Dom und AI HAT+ in die 16-mm-Abstandshalter (liegen dem HAT bei),
    Köpfe bündig im Dach. Unten hält der Pi mit den beiliegenden Schrauben an den Abstandshaltern.
  * Kamera Modul 3 Wide vorne in zwei Nuten, schaut durch ein Fenster in der Vorderwand.
  * Pololu D36V50F5 und das 4G-Modul (Waveshare SIM7600G-H, nur die Platine) in Einklick-Taschen unter dem Dach.
  * GPS-Keramikantenne in einer Tasche unter dem Dach (Kunststoff lässt das Signal durch).
  * Status-LEDs (WS2812-Streifen) vorne unter dem Dach, sie leuchten durch 4 Löcher.
  * Rundes Display (ESP32-S3-Touch-AMOLED-1.75) hinten: Das Glas liegt von innen am Dach an und schaut
    durch ein rundes Loch, 3 Schnapphaken halten die Platine.
  * LiDAR LD19 oben auf dem Dach, Kabel durch ein Loch nach innen (Befestigungslöcher erst nach dem Nachmessen).

Klappen und Verschluss:
  * Hinten zwei Scharniere außen an der Trennfuge, Achse M3 × 16 (Gewinde im äußeren Lappen der Haube).
  * Vorne zwei M3 × 12 waagerecht durch die Vorderwand (Köpfe bündig) in die Laschen des Rings von Ebene 2.

Zwei Druckteile: vordere und hintere Hälfte, Fuge quer bei x = FUGE. An der Fuge hat jede Hälfte innen einen
10 mm breiten Rand (Flansch) an Dach und Seitenwänden; beide werden mit 6 × M3 × 12 verschraubt.
"""
import math
from pathlib import Path
from build123d import (Box, Cylinder, Cone, Rot, Rectangle, RectangleRounded, Pos, Plane, Polygon, Axis, extrude,
                       export_stl, export_step, Vector)

import ebene2_elektronik as e2

# ------------------------------------------------------------------ Parameter
X_VORNE, X_HINTEN, XM, L, B, R_ECKE = e2.X_VORNE, e2.X_HINTEN, e2.XM, e2.L, e2.B, e2.R_ECKE
WAND = e2.RING_WAND                      # 2,4 mm
UNTEN = e2.EBENE3_UNTEN                  # 84: Haube sitzt auf dem Ring von Ebene 2
DACH_UNTEN = 118.0                       # Unterseite des Dachs
DACH_D = 3.0
DACH_OBEN = DACH_UNTEN + DACH_D          # 121
SENKRECHT_BIS = UNTEN + 12.0             # Seitenwände bis hier senkrecht, dann schräg
EINZUG = 7.0                             # oben je Seite so viel schmaler
FASE = 3.0                               # 45°-Fase an allen Dachkanten
PILOT, DURCH, KOPF_D, KOPF_H = e2.PILOT, e2.DURCH, e2.KOPF_D, e2.KOPF_H

# Raspberry Pi 5 + AI HAT+ (hängt am Dach), Löcher 58 × 49, USB/Ethernet nach hinten
PI_X = -8.0
PI_LOECHER = [(PI_X - 19, 24.5), (PI_X - 19, -24.5), (PI_X + 39, 24.5), (PI_X + 39, -24.5)]
PI_UNTEN = UNTEN + 3.0 + 5.0             # 92: Unterseite der Pi-Platine (wie im 3D-Modell)
HAT_OBEN = PI_UNTEN + 1.3 + 16.0 + 1.6   # 110,9: Oberseite des AI HAT+
PI_DOM_D = 6.5
M25_DURCH, M25_KOPF_D, M25_KOPF_H = 2.8, 5.0, 2.6

# Kamera Modul 3 Wide (25 × 24 mm, 1 mm dick): Platine senkrecht, Objektiv nach vorne, von unten in zwei Nuten
KAM_B, KAM_H, KAM_T = 25.0, 24.0, 1.0
KAM_X = X_VORNE - WAND - 9.0             # Vorderseite der Platine (Objektiv ragt 9 mm nach vorne)
KAM_OBEN = DACH_UNTEN - 2.0              # Oberkante der Platine
KAM_UNTEN = KAM_OBEN - KAM_H
KAM_OBJ_Y = KAM_UNTEN + 14.5             # Mitte Objektiv
KAM_FENSTER = 18.0

# Einklick-Taschen unter dem Dach: Name, x, z, Innenmaß x, Innenmaß z, Abstand Platine–Dach, Wandhöhe
LUFT, TWAND, NASE = 0.3, 1.6, 0.6
TASCHEN = [
    ("Pololu D36V50F5", 68.0, -45.0, 25.4, 25.4, 0.0, 4.0),
    ("4G-Modul SIM7600G-H", -18.85, 56.1, 82.3, 40.2, 4.0, 7.2, True),   # Platine; Bauteile der Rückseite (3,7 mm) zeigen zum Dach
    ("GPS-Antenne", -80.0, -55.0, 25.0, 25.0, 0.0, 6.0),
]
LTE_USB_X = -18.85 - 41.15 - 15.3        # Ende des USB-A-Steckers (hinten)
LED = (101.0, 0.0, 6.0, 34.0)            # WS2812-Streifen (x, z, Breite, Länge), leuchtet durch 4 Löcher im Dach
LED_LOECHER = [-12.0, -4.0, 4.0, 12.0]
DISPLAY = (-92.0, 0.0)                   # Mitte des runden Displays
DISPLAY_SICHT, DISPLAY_GLAS, DISPLAY_PCB = 44.4, 48.96, 46.0
DISPLAY_PCB_UNTEN = DACH_UNTEN - 6.9     # Unterseite der Platine (Zeichnung Waveshare)
LIDAR = (70.0, 0.0, 46.0, 54.0)          # Auflage oben (x, z, Länge, Breite)
LIDAR_KABEL = (56.0, 12.0, 10.0)         # Loch für das LiDAR-Kabel (x, z, Ø)

# Scharnier und Verschluss (Gegenstücke am Ring in ebene2_elektronik.py)
SCH_X, SCH_Y, SCH_R, SCH_Z = e2.SCH_X, e2.SCH_Y, e2.SCH_R, e2.SCH_Z
SCH_RING_B, SCH_LAPPEN_B, SCH_SPALT = e2.SCH_RING_B, 5.0, 0.3
VORNE_Z, LASCHE_B, LASCHE_X0, LASCHE_X1, LASCHE_OBEN, VORNE_Y = e2.VORNE_Z, e2.LASCHE_B, e2.LASCHE_X0, e2.LASCHE_X1, e2.LASCHE_OBEN, e2.VORNE_Y
POLSTER_DICKE = 4.6

# Lüftung: senkrechte Schlitze in beiden Seitenwänden (im senkrechten und im schrägen Teil)
LUEFTUNG_X = [-56 + 8 * i for i in range(11)]
LUEFTUNG_Y = (UNTEN + 3.0, SENKRECHT_BIS + 12.0)

# Teilung in zwei Druckteile
FUGE = 45.0
FUGE_SPALT = 0.1
FLANSCH_D, FLANSCH_TIEFE = 5.9, 10.0     # Dicke (x) je Hälfte, Breite nach innen
FLANSCH_SCHRAUBEN = [("Dach", 40.0, "vorne"), ("Dach", -40.0, "hinten"), ("Seite", 95.0, "hinten"), ("Seite", 108.0, "hinten")]
# Dach: z; Seite: y (je links und rechts). „vorne“/„hinten“ = Seite, auf der der Kopf sitzt: dort muss der Schraubendreher
# frei herankommen (Haube aufgeklappt). Dach links von vorne, weil hinten das 4G-Modul davor liegt.

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


# ------------------------------------------------------------------ Form
def halbbreite(y, innen=0.0):
    """Halbe Breite (z) der Haube in Höhe y (außen bzw. innen um innen mm versetzt)."""
    if y <= SENKRECHT_BIS:
        return B / 2 - innen
    t = min(1.0, (y - SENKRECHT_BIS) / (DACH_OBEN - SENKRECHT_BIS))
    neig = math.atan(EINZUG / (DACH_OBEN - SENKRECHT_BIS))
    return B / 2 - EINZUG * t - innen / math.cos(neig)


def frontprofil(innen, y0, y1, fase):
    """Querschnitt (z/y) als Fläche in der YZ-Ebene, um innen mm nach innen versetzt."""
    zs = halbbreite(SENKRECHT_BIS, innen)
    zo = halbbreite(y1, innen)
    pts = [(-(B / 2 - innen), y0), (B / 2 - innen, y0), (zs, SENKRECHT_BIS), (zo, y1 - fase), (zo - fase, y1),
           (-(zo - fase), y1), (-zo, y1 - fase), (-zs, SENKRECHT_BIS)]
    return (Plane.YZ * Polygon(*[(-z, y) for (z, y) in pts], align=None)).face()


def seitenprofil(innen, y0, y1, fase):
    """Längsschnitt (x/y) mit 45°-Fasen an Vorder- und Hinterkante des Dachs."""
    xv, xh = X_VORNE - innen, X_HINTEN + innen
    pts = [(xh, y0), (xv, y0), (xv, y1 - fase), (xv - fase, y1), (xh + fase, y1), (xh, y1 - fase)]
    return (Plane.XZ * Polygon(*pts, align=None)).face()


def form(innen, y0, y1, fase):
    drauf = Pos(XM, 0, y0) * extrude(RectangleRounded(L - 2 * innen, B - 2 * innen, max(1.0, R_ECKE - innen)), y1 - y0)
    quer = extrude(frontprofil(innen, y0, y1, fase), L, both=True)
    laengs = extrude(seitenprofil(innen, y0, y1, fase), B, both=True)
    return drauf & quer & laengs


def aussen():
    return form(0.0, UNTEN, DACH_OBEN, FASE)


def innen():
    return form(WAND, UNTEN - 1, DACH_UNTEN, max(0.5, FASE - WAND))


# ------------------------------------------------------------------ Teile unter dem Dach
def senkung_oben(x, z, d_kopf, h_kopf, d_loch):
    """Senkung im Dach von oben (beim Druck unten, Dach liegt auf dem Bett) mit Brücken-Trick."""
    t = zyl_y(d_kopf / 2, x, z, DACH_OBEN - h_kopf, DACH_OBEN + 1)
    t += quader(x - d_kopf / 2, x + d_kopf / 2, DACH_OBEN - h_kopf - 0.3, DACH_OBEN - h_kopf + 0.01, z - d_loch / 2, z + d_loch / 2)
    t += quader(x - d_loch / 2, x + d_loch / 2, DACH_OBEN - h_kopf - 0.6, DACH_OBEN - h_kopf - 0.29, z - d_loch / 2, z + d_loch / 2)
    return t


def nase_keil_unten(wand_z, spitze_z, y_kante, mitte_x, halb):
    """Rastnase an einer z-Wand, die vom Dach nach unten hängt: Unterseite waagerecht (hält die Platine),
    Oberseite 45° schräg – beim Druck (Dach unten) ist die Schräge unten, also ohne Stützen."""
    aus = wand_z + (0.05 if wand_z > spitze_z else -0.05)
    tief = abs(spitze_z - wand_z)
    prof = Plane.YZ * Polygon((-aus, y_kante), (-spitze_z, y_kante), (-spitze_z, y_kante + 0.2), (-aus, y_kante + 0.2 + tief + 0.4), align=None)
    return Pos(mitte_x, 0, 0) * extrude(prof.face(), halb, both=True)


def tasche_dach(name, x, z, ix, iz, abstand, wand_h, enden_offen=False):
    """Einklick-Tasche unter dem Dach: Rahmen hängt vom Dach, die Platine liegt im Abstand `abstand` unter dem Dach
    (auf 4 kleinen Klötzen), Rastnasen an den langen Seiten halten sie von unten."""
    ax, az = ix / 2 + LUFT, iz / 2 + LUFT
    y_dach = DACH_UNTEN
    r = quader(x - ax - TWAND, x + ax + TWAND, y_dach - wand_h, y_dach + 0.1, z - az - TWAND, z + az + TWAND)
    r -= quader(x - ax, x + ax, y_dach - wand_h - 0.1, y_dach + 0.2, z - az, z + az)
    if abstand > 0:     # Klötze in den Ecken, auf denen die Platine anliegt
        for sx in (1, -1):
            for sz in (1, -1):
                r += quader(x + sx * (ax - 4), x + sx * ax + sx * 0.05, y_dach - abstand, y_dach + 0.1, z + sz * (az - 4), z + sz * az + sz * 0.05)
    if enden_offen:     # Stirnseiten (x) offen – dort kommen Stecker heraus; die Platine hält an den langen Seiten
        for s in (1, -1):
            r -= quader(x + s * (ax - 0.1), x + s * (ax + TWAND + 0.2), y_dach - wand_h - 0.2, y_dach + 0.2, z - az + 6, z + az - 6)
    else:               # Kerbe zum Heraushebeln
        r -= quader(x + ax - 0.1, x + ax + TWAND + 0.1, y_dach - wand_h - 0.1, y_dach - 1.0, z - 3, z + 3)
    y_platine = y_dach - abstand - 1.6
    lang_x = ix >= iz
    for s in (1, -1):
        if lang_x:
            r += nase_keil_unten(z + s * az, z + s * (az - NASE), y_platine - 0.1, x, 4)
        else:   # quadratische Platine: Nasen an den x-Wänden (kleiner Klotz, 0,9 mm hoch – druckt als kurze Brücke)
            r += quader(x + s * ax - s * NASE, x + s * ax + s * 0.05, y_platine - 1.0, y_platine - 0.1, z - 4, z + 4)
    return r


def scharnier_lappen():
    """Hinten je Scharnier zwei Lappen an der Haube (außen mit Kernloch, innen mit Durchgangsloch),
    dazwischen der Lappen des Rings. Achse M3 × 16."""
    t = None
    for zc in SCH_Z:
        for s in (1, -1):
            z0 = zc + s * (SCH_RING_B / 2 + SCH_SPALT)
            z1 = z0 + s * SCH_LAPPEN_B
            lappen = zyl_z(SCH_R, SCH_X, SCH_Y, z0, z1)
            lappen += quader(SCH_X, X_HINTEN + 0.5, UNTEN, SCH_Y + SCH_R, z0, z1)        # Verbindung zur Rückwand
            # 45°-Keil vom äußersten Punkt des Lappens schräg hoch an die Rückwand: beim Druck (Dach unten) trägt er den Lappen
            lauf = (X_HINTEN + 0.5) - (SCH_X - SCH_R)
            keil = Plane.XZ * Polygon((SCH_X - SCH_R, SCH_Y), (X_HINTEN + 0.5, SCH_Y), (X_HINTEN + 0.5, SCH_Y + lauf), align=None)
            lappen += Pos(0, -(z0 + z1) / 2, 0) * extrude(keil.face(), SCH_LAPPEN_B / 2, both=True)
            aussen_liegend = abs(z1) > abs(z0)
            lappen -= zyl_z((PILOT if aussen_liegend else DURCH) / 2, SCH_X, SCH_Y, z0 - s, z1 + s)
            t = lappen if t is None else t + lappen
    return t


def haube():
    teil = aussen() - innen()

    # Pi-Stapel: 4 Dome vom Dach bis auf den AI HAT+, M2,5 von oben (Kopf bündig im Dach)
    for (x, z) in PI_LOECHER:
        teil += zyl_y(PI_DOM_D / 2, x, z, HAT_OBEN, DACH_UNTEN + 0.1)
        teil -= zyl_y(M25_DURCH / 2, x, z, HAT_OBEN - 1, DACH_OBEN + 1)
        teil -= senkung_oben(x, z, M25_KOPF_D, M25_KOPF_H, M25_DURCH)

    # Taschen
    for t in TASCHEN:
        teil += tasche_dach(*t)

    # Kamera: zwei Pfosten an der Vorderwand, vom Dach bis unter die Platine, Nut von unten offen
    xi = X_VORNE - WAND
    for s in (1, -1):
        z0, z1 = s * (KAM_B / 2 - 1.5), s * (KAM_B / 2 + 3.5)
        pfosten = quader(KAM_X - KAM_T - 3.0, xi + 0.5, KAM_UNTEN - 2.0, DACH_UNTEN + 0.1, z0, z1)
        pfosten -= quader(KAM_X - KAM_T - 0.15, KAM_X + 0.15, KAM_UNTEN - 3.0, KAM_OBEN, z0 - s * 0.1, s * (KAM_B / 2 + 0.3))
        # kleine Nase unten in der Nut: die Platine schnappt beim Einschieben darüber
        pfosten += quader(KAM_X - KAM_T - 0.15, KAM_X - KAM_T + 0.25, KAM_UNTEN - 1.2, KAM_UNTEN - 0.4, z0 - s * 0.05, s * (KAM_B / 2 + 0.3))
        teil += pfosten
    # Fenster: rund mit gerader Kante unten (beim Druck liegt das Dach auf dem Bett – unten im Auto ist beim Druck oben), außen angefast
    r = KAM_FENSTER / 2
    pts = [(r * math.cos(math.radians(d)), KAM_OBJ_Y + r * math.sin(math.radians(d))) for d in range(-45, 226, 5)]
    fen = Plane.YZ * Polygon(*pts, align=None)
    teil -= Pos(X_VORNE - WAND / 2, 0, 0) * extrude(fen.face(), WAND, both=True)
    teil -= P(X_VORNE + 0.01, KAM_OBJ_Y, 0) * Rot(0, -90, 0) * extrude(Rectangle(KAM_FENSTER + 3, KAM_FENSTER + 3), 1.5, taper=45)

    # Status-LEDs: flache Tasche unter dem Dach, 4 Löcher Ø 3 nach oben
    lx, lz, lb, ll = LED
    teil += quader(lx - lb / 2 - TWAND, lx + lb / 2 + TWAND, DACH_UNTEN - 2.5, DACH_UNTEN + 0.1, lz - ll / 2 - TWAND, lz + ll / 2 + TWAND)
    teil -= quader(lx - lb / 2, lx + lb / 2, DACH_UNTEN - 2.6, DACH_UNTEN - 1.0, lz - ll / 2, lz + ll / 2)
    for z in LED_LOECHER:
        teil -= zyl_y(1.5, lx, lz + z, DACH_UNTEN - 1.1, DACH_OBEN + 1)

    # Display: rundes Sichtloch im Dach (außen angefast), 3 Schnapphaken halten die Platine von unten
    dx, dz = DISPLAY
    teil -= zyl_y(DISPLAY_SICHT / 2, dx, dz, DACH_UNTEN - 1, DACH_OBEN + 1)
    teil -= P(dx, DACH_OBEN - 0.74, dz) * Cone(DISPLAY_SICHT / 2, DISPLAY_SICHT / 2 + 1.5, 1.5)   # außen 45° angefast
    for k in range(3):
        a = math.radians(30 + 120 * k)
        hx, hz = dx + (DISPLAY_PCB / 2 + 0.3 + 0.8) * math.cos(a), dz + (DISPLAY_PCB / 2 + 0.3 + 0.8) * math.sin(a)
        haken = quader(hx - 0.8, hx + 0.8, DISPLAY_PCB_UNTEN - 2.5, DACH_UNTEN + 0.1, hz - 4, hz + 4)
        teil += haken.rotate(Axis((hx, -hz, 0), (0, 0, 1)), -math.degrees(a))
        nase = quader(hx - 0.8 - 1.0, hx - 0.7, DISPLAY_PCB_UNTEN - 1.2, DISPLAY_PCB_UNTEN - 0.1, hz - 4, hz + 4)
        teil += nase.rotate(Axis((hx, -hz, 0), (0, 0, 1)), -math.degrees(a))

    # LiDAR: steht direkt auf dem Dach (Befestigungslöcher nach dem Nachmessen), Kabelloch
    kx, kz, kd = LIDAR_KABEL
    teil -= zyl_y(kd / 2, kx, kz, DACH_UNTEN - 1, DACH_OBEN + 3)

    # Lüftungsschlitze in den Seitenwänden
    for x in LUEFTUNG_X:
        for s in (1, -1):
            teil -= quader(x - 1.5, x + 1.5, LUEFTUNG_Y[0], LUEFTUNG_Y[1], s * (B / 2 - 12), s * (B / 2 + 1))

    # Vorne: Polster an der Vorderwand mit Schraubloch (Kopf bündig) für die Laschen des Rings
    for zc in VORNE_Z:
        prof = Plane.XZ * Polygon((xi + 0.5, UNTEN), (xi - POLSTER_DICKE, UNTEN), (xi - POLSTER_DICKE, VORNE_Y + 7.0),
                                  (xi + 0.5, VORNE_Y + 7.0 + POLSTER_DICKE + 0.5), align=None)
        teil += Pos(0, -zc, 0) * extrude(prof.face(), 7, both=True)
        teil -= quader(LASCHE_X0 - 0.5, LASCHE_X1 + 0.5, UNTEN - 1, LASCHE_OBEN + 0.5, zc - LASCHE_B / 2 - 0.5, zc + LASCHE_B / 2 + 0.5)
        teil -= zyl_x(DURCH / 2, VORNE_Y, zc, LASCHE_X1 - 1, X_VORNE + 1)
        teil -= zyl_x(KOPF_D / 2, VORNE_Y, zc, X_VORNE - KOPF_H, X_VORNE + 1)

    teil = teil & aussen()          # nichts ragt aus der Form
    teil += scharnier_lappen()
    return teil


# ------------------------------------------------------------------ Teilung
def flansch_profil(y0, y1):
    """U-förmiger Rand an der Fuge: innen an Seitenwänden und Dach, FLANSCH_TIEFE breit."""
    aussen_f = frontprofil(WAND - 0.05, y0, y1, 0.0)
    innen_f = frontprofil(WAND + FLANSCH_TIEFE, y0 - 5, y1 - FLANSCH_TIEFE, 0.0)
    return aussen_f - innen_f


def teilen(teil):
    gross = 400.0
    vorne = teil & quader(FUGE + FUGE_SPALT, gross, -gross, gross, -gross, gross)
    hinten = teil & quader(-gross, FUGE - FUGE_SPALT, -gross, gross, -gross, gross)
    profil = flansch_profil(UNTEN, DACH_UNTEN + 0.05)
    fl_v = Pos(FUGE + FUGE_SPALT, 0, 0) * extrude(profil, FLANSCH_D - FUGE_SPALT)
    if fl_v.bounding_box().min.X < FUGE:
        fl_v = Pos(FUGE + FUGE_SPALT, 0, 0) * extrude(profil, -(FLANSCH_D - FUGE_SPALT))
    fl_h = fl_v.mirror(Plane.YZ.offset(FUGE))
    vorne += fl_v & aussen()
    hinten += fl_h & aussen()
    # Schrauben quer durch beide Flansche (Kopf hinten, Gewinde vorne)
    pos = []
    for (art, w, kopf) in FLANSCH_SCHRAUBEN:
        if art == "Dach":
            pos.append((DACH_UNTEN - FLANSCH_TIEFE / 2, w, kopf))
        else:
            for s in (1, -1):
                pos.append((w, s * (halbbreite(w, WAND) - FLANSCH_TIEFE / 2), kopf))
    for (y, z, kopf) in pos:
        if kopf == "hinten":     # Kopf am hinteren Flansch, Gewinde im vorderen
            hinten -= zyl_x(DURCH / 2, y, z, FUGE - FLANSCH_D - 1, FUGE + 0.5)
            vorne -= zyl_x(PILOT / 2, y, z, FUGE - 0.5, FUGE + FLANSCH_D + 1)
        else:
            vorne -= zyl_x(DURCH / 2, y, z, FUGE - 0.5, FUGE + FLANSCH_D + 1)
            hinten -= zyl_x(PILOT / 2, y, z, FUGE - FLANSCH_D - 1, FUGE + 0.5)
    return vorne, hinten, pos



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


# ------------------------------------------------------------------ Prüfungen
def drehen(teil, winkel):
    achse = Axis((SCH_X, 0, SCH_Y), (0, 1, 0))
    return teil.rotate(achse, -winkel)


def pruefen(haube_teil, ring_teile):
    fehler = 0
    schlimmst = 0.0
    for w in range(0, 101, 10):
        d = drehen(haube_teil, w)
        v = sum((d & r).volume for r in ring_teile)
        schlimmst = max(schlimmst, v)
        if v > 0.5:
            print(f"  Aufklappen {w:3d}°: stößt am Ring an ({v:.1f} mm³)"); fehler += 1
    print(f"Aufklappen 0–100°: {'frei' if not fehler else 'STÖSST AN'} (größte Berührung {schlimmst:.2f} mm³)")

    # Draufsicht: was am Dach hängt, darf sich nicht überschneiden
    rechtecke = [(n, x - ix / 2 - LUFT - TWAND, x + ix / 2 + LUFT + TWAND, z - iz / 2 - LUFT - TWAND, z + iz / 2 + LUFT + TWAND)
                 for (n, x, z, ix, iz, *_r) in TASCHEN]
    rechtecke.append(("4G: USB-Stecker + Kabel", LTE_USB_X - 20, -18.85 - 41.15 - LUFT - TWAND, 46.0, 66.0))
    rechtecke.append(("4G: SMA-Buchse", -18.85 + 41.15 + LUFT + TWAND, -18.85 + 41.15 + 9.5, 52.0, 60.0))
    rechtecke.append(("Raspberry Pi 5 + AI HAT+", PI_X - 42.5 - 3, PI_X + 42.5, -28.0, 28.0))
    rechtecke.append(("Kamera", KAM_X - KAM_T - 3, X_VORNE - WAND, -KAM_B / 2 - 3.5, KAM_B / 2 + 3.5))
    lx, lz, lb, ll = LED
    rechtecke.append(("Status-LEDs", lx - lb / 2 - TWAND, lx + lb / 2 + TWAND, lz - ll / 2 - TWAND, lz + ll / 2 + TWAND))
    dx, dz = DISPLAY
    rr = DISPLAY_PCB / 2 + 2.0
    rechtecke.append(("Display mit Haken", dx - rr, dx + rr, dz - rr, dz + rr))
    kx, kz, kd = LIDAR_KABEL
    rechtecke.append(("LiDAR-Kabelloch", kx - kd / 2, kx + kd / 2, kz - kd / 2, kz + kd / 2))
    rechtecke += [(f"Lasche/Polster {z}", LASCHE_X0 - 0.5, X_VORNE - WAND, z - 7, z + 7) for z in VORNE_Z]
    rechtecke.append(("Flansch hinten (mit Schraubenköpfen)", FUGE - FLANSCH_D - 3.5, FUGE, -B / 2, B / 2))
    rechtecke.append(("Flansch vorne", FUGE, FUGE + FLANSCH_D, -B / 2, B / 2))
    n = 0
    for i in range(len(rechtecke)):
        for j in range(i + 1, len(rechtecke)):
            a, b = rechtecke[i], rechtecke[j]
            if a[0].startswith("Flansch") and b[0].startswith("Flansch"):
                continue
            if a[1] < b[2] - 0.01 and b[1] < a[2] - 0.01 and a[3] < b[4] - 0.01 and b[3] < a[4] - 0.01:
                # der Flansch liegt nur am Rand (Seitenwände) und oben unter dem Dach – Teile in der Mitte stören nur, wenn sie hoch reichen
                print("  Überschneidung:", a[0], "↔", b[0]); n += 1
    print("Überschneidungen:", n)
    # Höhe: alles, was am Dach hängt, bleibt über Ebene 2 (höchstes Teil dort: Pico auf dem Freenove-Board, ca. 79 mm)
    tiefste = {"Pi-Unterseite (mit Lötstellen)": PI_UNTEN - 1.5, "Kamera": KAM_UNTEN - 2.0, "4G-Modul": DACH_UNTEN - 4.0 - 1.6 - 3.0,
               "Display": DISPLAY_PCB_UNTEN - 3.0}
    for k, y in tiefste.items():
        print(f"  {k}: tiefster Punkt {y:5.1f} mm (Ebene 2 bis ca. 79 mm, Ring bis 84 mm)")
    return fehler + n


if __name__ == "__main__":
    AUS.mkdir(exist_ok=True)
    h = haube()
    vorne, hinten, schrauben = teilen(h)
    ring_teile = [e2.teilen_ring(e2.ring_oben())[1]]          # nur die hintere Ring-Hälfte liegt beim Scharnier
    pruefen(vorne + hinten, ring_teile)
    for name, t in (("haube_vorne", vorne), ("haube_hinten", hinten)):
        print(f"{name}: {len(t.solids())} Körper", "(gut)" if len(t.solids()) == 1 else "– NICHT zusammenhängend!")
    print("Hälften durchdringen sich:", "nein" if (vorne & hinten).volume < 0.5 else "JA")
    # Schraubendreher-Zugang zu den Schrauben an der Fuge (Haube aufgeklappt – alles, was am Dach hängt, ist mit im Weg)
    schr = [(f"Fuge y={y:.0f} z={z:+.0f} (Kopf {kopf})", FUGE - FLANSCH_D if kopf == "hinten" else FUGE + FLANSCH_D, y, z, "x", -1 if kopf == "hinten" else 1)
            for (y, z, kopf) in schrauben]
    bauteile = [("Pi 5 + AI HAT+", PI_X - 45.5, PI_X + 42.5, PI_UNTEN - 1.5, HAT_OBEN + 2, -28, 28),
                ("4G-Modul (Tasche)", -18.85 - 43, -18.85 + 43, DACH_UNTEN - 7.2, DACH_UNTEN, 56.1 - 22, 56.1 + 22),
                ("4G-USB-Stecker", LTE_USB_X, -18.85 - 41, DACH_UNTEN - 9, DACH_UNTEN - 2, 46, 66),
                ("Pololu", 68 - 15, 68 + 15, DACH_UNTEN - 10, DACH_UNTEN, -45 - 15, -45 + 15),
                ("GPS-Antenne", -80 - 14, -80 + 14, DACH_UNTEN - 7, DACH_UNTEN, -55 - 14, -55 + 14),
                ("Kamera", KAM_X - KAM_T - 4, X_VORNE - WAND, KAM_UNTEN - 3, DACH_UNTEN, -17, 17),
                ("Display", DISPLAY[0] - 26, DISPLAY[0] + 26, DISPLAY_PCB_UNTEN - 3, DACH_UNTEN, -26, 26)]
    zugang_pruefen(schr, [("Haube", vorne + hinten)], bauteile)
    for name, t in (("haube_vorne", vorne), ("haube_hinten", hinten)):
        export_stl(t, str(AUS / f"{name}.stl"), tolerance=0.02, angular_tolerance=0.15)
        export_step(t, str(AUS / f"{name}.step"))
        bb = t.bounding_box()
        print("gültig" if t.is_valid else "UNGÜLTIG", f"{name} {bb.size.X:.1f} × {bb.size.Y:.1f} × {bb.size.Z:.1f} mm, Volumen {t.volume / 1000:.1f} cm³")
