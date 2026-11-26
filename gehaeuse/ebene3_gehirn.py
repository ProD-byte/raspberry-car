"""Raspberry Car – Ebene 3: Gehirn mit Dach (Klapphaube)

Die oberste Ebene ist eine HAUBE: Seitenwände und Dach in einem, unten offen. Alles hängt am Dach
(Raspberry Pi 5 mit AI HAT+, Kamera, Pololu, 4G-Modul, GPS-Antenne, rundes Display, Front- und Rücklicht),
oben auf dem Dach steht der LiDAR. Die Haube klappt hinten an zwei Scharnieren nach hinten auf –
dann liegt Ebene 2 offen. Alle Maße in mm. Erzeugt STL und STEP in gehaeuse/ebene3/.

Aufruf (einmalig: pip install build123d):
    python ebene3_gehirn.py

Koordinaten wie im 3D-Modell: x nach vorne (vorne = Kamera, hinten = Ladebuchse und Schalter), z nach links, y nach oben.

Form (gegen die „Brotdose“):
  * Vorder- und Rückwand senkrecht (vorne das Kamerafenster, hinten das Scharnier).
  * Die Seitenwände sind unten 12 mm senkrecht und laufen dann schräg nach innen (oben je 7 mm schmaler).
  * Alle Kanten des Dachs 45° abgeschrägt.
  * An den 4 oberen Ecken je eine große schräge Dreiecksfläche (Facette) – kantig wie die Schutzbleche.

Was darin hängt (alles am Dach, die Haube wird mit dem Dach nach unten gedruckt – ohne Stützen):
  * Raspberry Pi 5 mit Active Cooler und AI HAT+: Der Stapel hängt an 4 Domen unter dem Dach.
    M2,5 von oben durch Dach, Dom und AI HAT+ in die 16-mm-Abstandshalter (liegen dem HAT bei),
    Köpfe bündig im Dach. Unten hält der Pi mit den beiliegenden Schrauben an den Abstandshaltern.
  * Zwei Kameras vorne nebeneinander in Nuten, jede schaut durch ein eigenes Fenster in der Vorderwand: links die
    Tag-Kamera (Camera Module 3 Wide), rechts die Nachtsicht (Camera Module 3 NoIR Wide).
  * Nachtsicht-Licht: je Seite zwei 5-mm-IR-LEDs (850 nm) zwischen Kamera und Schraubpolster, von innen eingesteckt;
    ein zweiter MOSFET-Treiber unter dem Dach schaltet sie.
  * Pololu D36V50F5 und das 4G-Modul (Waveshare SIM7600G-H, nur die Platine) in Einklick-Taschen unter dem Dach.
  * GPS-Keramikantenne in einer Tasche unter dem Dach (Kunststoff lässt das Signal durch).
  * Front- und Rücklicht: je eine WS2812B-Leiste (8 LEDs) unten in Vorder- und Rückwand, davor ein durchgehender Leuchtschlitz (Lichtband)
    in einer flachen Blende, innen eine Streuscheibe (eigenes Druckteil, Natur-PETG), Leiste von unten zwischen zwei Pfosten geschoben.
  * Rundes Display (ESP32-S3-Touch-AMOLED-1.75) hinten: Das Glas liegt von innen am Dach an und schaut
    durch ein rundes Loch, 3 Schnapphaken halten die Platine.
  * Zwei Scheinwerfer (weiße 1-W-LED auf 20-mm-Stern) vorne links und rechts, von unten in Schlitze geschoben;
    der MOSFET-Treiber (Adafruit 5648), der sie schaltet, in einer Einklick-Tasche unter dem Dach.
  * LiDAR LD19 oben auf dem Dach, Kabel durch ein Loch nach innen (Befestigungslöcher erst nach dem Nachmessen).

Klappen und Verschluss:
  * Hinten zwei Scharniere außen an der Trennfuge, Achse M3 × 18 (Gewinde im äußeren Lappen der Haube, greift 4,4 mm).
  * Vorne zwei M3 × 12 waagerecht durch die Vorderwand (Köpfe bündig) in die Laschen des Rings von Ebene 2.

Zwei Druckteile: vordere und hintere Hälfte, Fuge quer bei x = FUGE. An der Fuge hat jede Hälfte innen einen
10 mm breiten Rand (Flansch) an Dach und Seitenwänden; beide werden mit 6 × M3 × 12 verschraubt.
"""
import math
from pathlib import Path
from build123d import (Box, Cylinder, Cone, Rot, Rectangle, RectangleRounded, Pos, Plane, Polygon, Axis, extrude,
                       export_stl, export_step, Vector, Keep, Sphere)

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
# Facetten an den 4 oberen Ecken (Design „Rover dunkel“): je eine schräge Dreiecksfläche durch drei Punkte (x, y, z) –
# vorne am Dach (z = ±ECKE_DACH_Z), seitlich am Dach (x = ±ECKE_DACH_X) und unten an der Ecke (y = ECKE_UNTEN).
# So steil, dass die Haube (Dach nach unten gedruckt) ohne Stützen druckbar bleibt (Fläche ≥ 45° gegen die Waagerechte).
ECKE_DACH_Z, ECKE_DACH_X, ECKE_UNTEN = 50.0, 85.0, 88.0
KOPF_D, KOPF_H = e2.KOPF_D, e2.KOPF_H
from loecher import PILOT_QUER, DURCH_QUER   # Haube wird mit dem Dach nach unten gedruckt: alle M3-Löcher liegen quer

# Raspberry Pi 5 + AI HAT+ (hängt am Dach), Löcher 58 × 49, USB/Ethernet nach hinten
PI_X = -8.0
PI_LOECHER = [(PI_X - 19, 24.5), (PI_X - 19, -24.5), (PI_X + 39, 24.5), (PI_X + 39, -24.5)]
PI_UNTEN = UNTEN + 3.0 + 5.0             # 92: Unterseite der Pi-Platine (wie im 3D-Modell)
HAT_OBEN = PI_UNTEN + 1.3 + 16.0 + 1.6   # 110,9: Oberseite des AI HAT+
PI_DOM_D = 6.5
M25_KOPF_D, M25_KOPF_H = 5.0, 2.6
from loecher import M25_DURCH_HOCH as M25_DURCH   # M2,5 durchs Dach: steht beim Druck senkrecht (loecher.py)

# Kamera Modul 3 Wide (25 × 24 mm, 1 mm dick): Platine senkrecht, Objektiv nach vorne, von unten in zwei Nuten
KAM_B, KAM_H, KAM_T = 25.0, 24.0, 1.0
KAM_X = X_VORNE - WAND - 9.0             # Vorderseite der Platine (Objektiv ragt 9 mm nach vorne)
KAM_OBEN = DACH_UNTEN - 2.0              # Oberkante der Platine
KAM_UNTEN = KAM_OBEN - KAM_H
KAM_OBJ_Y = KAM_UNTEN + 14.5             # Mitte Objektiv
KAM_FENSTER = 18.0
# Zwei Kameras nebeneinander (gleiche Größe): links die Tag-Kamera (Camera Module 3 Wide), rechts die Nachtsicht
# (Camera Module 3 NoIR Wide, ohne IR-Sperrfilter). Name, Mitte z. Zwischen beiden ein gemeinsamer Pfosten.
KAMERAS = [("Kamera (Tag)", 15.0), ("Nachtsicht-Kamera (NoIR)", -15.0)]
# IR-LEDs für die Nachtsicht: je Seite zwei 5-mm-LEDs (850 nm) übereinander, zwischen Kamera und Schraubpolster.
# Die LED wird von innen durch einen Block in die Wand gesteckt, bis der Kragen anschlägt (Spitze bündig mit der Außenfläche),
# und mit einem Tropfen Heißkleber gesichert.
IR_Z, IR_Y = 35.0, (101.0, 111.0)        # Mitte z (= ±IR_Z), Höhen der beiden LEDs
IR_LOCH, IR_KRAGEN = 5.2, 6.2            # Bohrung für den LED-Körper Ø 5, Senkung für den Kragen Ø 5,8
IR_LAENGE = 7.6                          # Kragen-Vorderseite bis Spitze (5-mm-LED: 8,6 mm hoch, Kragen 1 mm)
IR_BLOCK = (4.5, 8.7)                    # Block: halbe Breite (z), Tiefe ab der Wand-Außenseite (x)

# Einklick-Taschen unter dem Dach: Name, x, z, Innenmaß x, Innenmaß z, Abstand Platine–Dach, Wandhöhe
LUFT, TWAND, NASE = 0.3, 1.6, 0.6
TASCHEN = [
    ("Pololu D36V50F5", 68.0, -45.0, 25.4, 25.4, 0.0, 4.0),
    ("4G-Modul SIM7600G-H", -18.85, 56.1, 82.3, 40.2, 4.0, 7.2, True),   # Platine; Bauteile der Rückseite (3,7 mm) zeigen zum Dach
    ("GPS-Antenne", -80.0, -55.0, 25.0, 25.0, 0.0, 6.0),
    ("MOSFET-Treiber (Scheinwerfer)", 78.0, 60.0, 25.4, 17.78, 0.0, 4.0, True),   # Adafruit 5648: Bauteile nach unten, Stecker/Klemme an den offenen Enden
    ("MOSFET-Treiber (IR-LEDs)", 85.0, 0.0, 25.4, 17.78, 0.0, 4.0, True),        # zweiter Adafruit 5648 für die Nachtsicht-LEDs
]
LTE_USB_X = -18.85 - 41.15 - 15.3        # Ende des USB-A-Steckers (hinten)
# Front- und Rücklicht: je eine WS2812B-Leiste mit 8 LEDs (53 × 10 mm, LEDs zur Wand) unten in der Vorder- und Rückwand.
# Rover-Design (dunkle Haube): vor den LEDs ein durchgehender Schlitz durch die Wand („Lichtband“), innen davor eine 1 mm dünne
# Streuscheibe (eigenes Druckteil aus Natur-/Weiß-PETG), auf die die LEDs drücken. Außen eine flache Blende um das Lichtband.
# Die Leiste wird von unten (Haube offen) zwischen zwei Pfosten geschoben; hinten hält sie eine Lippe, unten eine kleine Nase.
LICHT_L, LICHT_H, LICHT_PCB, LICHT_LED = 53.0, 10.0, 1.6, 1.6
LICHT_OBEN = UNTEN + 11.2                # 95,2: Oberkante der Leiste (Anschlag in den Pfosten)
LICHT_Y = LICHT_OBEN - LICHT_H / 2       # 90,2: Mitte der LED-Reihe
STREU = (1.0, 26.9, 4.4)                 # Streuscheibe (eigenes Druckteil, Natur-/Weiß-PETG): Dicke, halbe Länge, halbe Höhe
STREU_LUFT = 0.2                         # Luft rundum in der Vertiefung
LICHT_SCHLITZ = (25.4, 2.4)              # Lichtband: EIN durchgehender Schlitz vor allen 8 LEDs – halbe Länge (z), Höhe innen (y);
                                         # die Unterkante läuft nach außen 45° schräg nach unten (druckt ohne Stützen, Licht fällt etwas nach unten)
LICHT_TEILUNG = 6.35                     # Abstand der LEDs auf der Leiste
LICHT_MULDE = (0.4, 38.0, 5.0)           # (0,4 tief: neben dem Schlitz bleiben 1,0 mm Wand) außen: flache Blende um das Lichtband – Tiefe, halbe Länge, halbe Höhe (Enden rund), endet vor den Schraubenköpfen
# Scheinwerfer: zwei weiße 1-W-LEDs auf 20-mm-Alu-Stern vorne links/rechts unter den Eck-Facetten (3D-Form: Adafruit 2530).
# Der Stern steckt senkrecht in einem Schlitz (von unten eingeschoben, Haube offen), die LED-Kuppel sitzt direkt hinter einem Loch
# in der Vorderwand, das sich nach außen 60° weitet (wie ein Reflektor; steiler als 45° – druckt ohne Stützen).
# Rückseite und Mitte bleiben offen: Luft an den Stern, Platz für die Lötstellen vorne.
SW_Z, SW_Y = 64.0, 96.0                  # Mitte der LED (z = ±SW_Z); weiter außen stößt der Stern an die Eck-Facette, die Schiene innen geht in das Polster über
SW_STERN = (20.0, 20.63, 1.6)            # Stern: Breite (z), Höhe (y), Dicke (Adafruit-CAD 1,2 mm, echte Sterne meist 1,5–1,6)
SW_LED_H = 5.95                          # LED-Sockel 7 × 8 × 3,2 + Kuppel Ø 5,5: so weit steht sie vor dem Stern
SW_VORNE = X_VORNE - WAND - 0.2 - SW_LED_H   # Vorderseite des Sterns: Kuppel endet 0,2 mm vor der Innenseite der Wand –
                                             # so lässt sich der Stern von unten einschieben, das Licht geht durch das Loch
SW_LOCH = 3.2                            # Lochradius innen (Kuppel Ø 5,5 direkt dahinter)
SW_REFLEKTOR = 60.0                      # Öffnungswinkel des Lochs gegen die Achse
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
FUGE_SPALT = 0.0                         # stumpf, ohne Spalt (mit Spalt sah man durch die Fuge)
FUGE_RILLE = (1.2, 0.6)                  # außen an der Fuge eine Rille: Breite, Tiefe – eine saubere Linie statt einer Lücke
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


def ecken_ebenen(innen=0.0):
    """Die 4 Facetten-Ebenen an den oberen Ecken (als build123d-Plane, Normale nach außen), um innen mm nach innen versetzt."""
    ebenen = []
    for sx in (1, -1):
        for sz in (1, -1):
            a = Vector(sx * X_VORNE, DACH_OBEN, sz * ECKE_DACH_Z)
            b = Vector(sx * ECKE_DACH_X, DACH_OBEN, sz * (B / 2 - EINZUG))
            c = Vector(sx * X_VORNE, ECKE_UNTEN, sz * B / 2)
            n = (b - a).cross(c - a).normalized()
            if n.X * sx < 0:
                n = -n
            o = a - n * innen
            # Modell (x, y, z) → CAD (x, −z, y)
            ebenen.append(Plane(origin=(o.X, -o.Z, o.Y), z_dir=(n.X, -n.Z, n.Y)))
    return ebenen


def form(innen, y0, y1, fase):
    drauf = Pos(XM, 0, y0) * extrude(RectangleRounded(L - 2 * innen, B - 2 * innen, max(1.0, R_ECKE - innen)), y1 - y0)
    quer = extrude(frontprofil(innen, y0, y1, fase), L, both=True)
    laengs = extrude(seitenprofil(innen, y0, y1, fase), B, both=True)
    k = drauf & quer & laengs
    for e in ecken_ebenen(innen):
        k = k.split(e, keep=Keep.BOTTOM)
    return k


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


def licht(s, nur_ausschnitt=False):
    """Halter für eine WS2812B-Leiste an der Vorder- (s = +1) bzw. Rückwand (s = −1). Gibt (Zugabe, Ausschnitt) zurück,
    wenn nur_ausschnitt False ist, wird nur die Zugabe (Pfosten) geliefert – der Ausschnitt kommt über licht_ausschnitt()."""
    xi = s * (X_VORNE - WAND)                      # Wand-Innenseite
    lippe = xi - s * (LICHT_LED + LICHT_PCB + 0.1)   # LEDs drücken auf die Streuscheibe (bündig mit der Wand-Innenseite), + 0,1 Luft
    zugabe = None
    for sz in (1, -1):
        # Pfosten: von unten bis über die Leiste, oben 45° zur Wand (druckt mit dem Dach nach unten ohne Stützen)
        prof = Plane.XZ * Polygon((xi + s * 0.5, UNTEN), (lippe - s * 2.0, UNTEN), (lippe - s * 2.0, LICHT_OBEN + 1.8),
                                  (xi + s * 0.5, LICHT_OBEN + 1.8 + abs(xi + s * 0.5 - (lippe - s * 2.0))), align=None)
        z0, z1 = sz * (LICHT_L / 2 - 2.0), sz * (LICHT_L / 2 + 3.5)
        pf = Pos(0, -(z0 + z1) / 2, 0) * extrude(prof.face(), abs(z1 - z0) / 2, both=True)
        # Platz für die Leiste: von der Lippe bis zur Wand, Ende 0,2 mm Luft, oben Anschlag bei LICHT_OBEN
        pf -= quader(lippe, xi + s * 0.01, UNTEN - 1, LICHT_OBEN, z0 - sz * 0.1, sz * (LICHT_L / 2 + 0.2))
        # … und die Vertiefung der Streuscheibe bleibt frei
        pf -= quader(xi - s * 0.02, xi + s * (STREU[0] + 0.01), LICHT_Y - STREU[2] - STREU_LUFT, LICHT_Y + STREU[2] + STREU_LUFT,
                     z0 - sz * 0.1, sz * (STREU[1] + STREU_LUFT))
        # kleine Nase unten an der Lippe: die Leiste schnappt beim Einschieben darüber
        pf += quader(lippe, lippe + s * 0.4, LICHT_OBEN - LICHT_H - 0.9, LICHT_OBEN - LICHT_H - 0.3, z0, sz * (LICHT_L / 2 + 0.2))
        zugabe = pf if zugabe is None else zugabe + pf
    return zugabe


def licht_ausschnitt(s):
    """Was für ein Licht aus der Haube weg muss: Platz für die Leiste (auch in den Kamera-Pfosten), Tasche in der Wand, Lichtband-Schlitz, Blende außen."""
    xi = s * (X_VORNE - WAND)
    xa = s * X_VORNE
    lippe = xi - s * (LICHT_LED + LICHT_PCB + 0.1)
    sd, sl, sh = STREU
    md, ml, mh = LICHT_MULDE
    bl, bh = LICHT_SCHLITZ
    a = quader(lippe, xi, UNTEN - 1, LICHT_OBEN, -(LICHT_L / 2 + 0.2), LICHT_L / 2 + 0.2)
    # Vertiefung für die Streuscheibe (von innen)
    a += quader(xi - s * 0.01, xi + s * sd, LICHT_Y - sh - STREU_LUFT, LICHT_Y + sh + STREU_LUFT, -sl - STREU_LUFT, sl + STREU_LUFT)
    # Lichtband: ein Schlitz durch den Rest der Wand, Unterkante nach außen 45° abfallend
    x0, x1 = xi + s * (sd - 0.01), xa + s * 1.0
    tief = abs(x1 - x0)
    prof = Plane.XZ * Polygon((x0, LICHT_Y - bh / 2), (x0, LICHT_Y + bh / 2), (x1, LICHT_Y + bh / 2), (x1, LICHT_Y - bh / 2 - tief), align=None)
    a += extrude(prof.face(), bl, both=True)
    a += P(xa + s * 0.01, LICHT_Y, 0) * Rot(0, -90 * s, 0) * extrude(RectangleRounded(2 * mh, 2 * ml, mh - 0.01), md + 0.01, taper=45)   # Rand 45° – druckt sauber
    return a


def scheinwerfer():
    """Halter für die zwei Scheinwerfer-Sterne an der Vorderwand. Gibt (Zugabe, Ausschnitt) zurück."""
    xi = X_VORNE - WAND
    xs = SW_VORNE                            # Vorderseite des Sterns
    xh = xs - SW_STERN[2] - 0.3              # Rückseite des Schlitzes
    xb = xh - 2.0                            # Rückseite des Halters
    hz, hy = SW_STERN[0] / 2 + 0.25, SW_STERN[1] / 2 + 0.25
    rand = 2.5                               # Schiene außen am Stern
    griff = 1.6                              # so weit greifen die Schienen über den Rand des Sterns
    y_oben = SW_Y + hy
    zugabe = ausschnitt = None
    for sz in (1, -1):
        zc = sz * SW_Z
        # Block von unten bis über den Stern, oben 45° zur Wand (druckt mit dem Dach nach unten ohne Stützen)
        prof = Plane.XZ * Polygon((xi + 0.5, UNTEN), (xb, UNTEN), (xb, y_oben + 2.0), (xi + 0.5, y_oben + 2.0 + (xi + 0.5 - xb)), align=None)
        h = Pos(0, -zc, 0) * extrude(prof.face(), hz + rand, both=True)
        h -= quader(xh, xs, UNTEN - 1, y_oben, zc - hz, zc + hz)                                   # Schlitz, unten offen
        h -= quader(xs - 0.01, xi + 0.01, UNTEN - 1, y_oben, zc - hz + griff, zc + hz - griff)        # vorne offen: LED, Lötstellen
        h -= quader(xb - 1, xh + 0.01, UNTEN - 1, y_oben, zc - hz + griff, zc + hz - griff)           # hinten offen: Luft
        for s in (1, -1):                    # kleine Nasen unten an den hinteren Schienen: der Stern schnappt darüber
            z0, z1 = sorted((zc + s * (hz - griff), zc + s * hz))
            h += quader(xh - 0.01, xh + 0.4, SW_Y - SW_STERN[1] / 2 - 0.7, SW_Y - SW_STERN[1] / 2 - 0.1, z0, z1)
        # Loch in der Vorderwand: innen r = SW_LOCH, nach außen um SW_REFLEKTOR° geweitet
        r1 = SW_LOCH + (WAND + 0.2) * math.tan(math.radians(SW_REFLEKTOR))
        loch = P(xi - 0.1 + (WAND + 0.2) / 2, SW_Y, zc) * Rot(0, 90, 0) * Cone(SW_LOCH, r1, WAND + 0.2)
        zugabe = h if zugabe is None else zugabe + h
        ausschnitt = loch if ausschnitt is None else ausschnitt + loch
    return zugabe, ausschnitt


def sternform(zc):
    """Umriss des Alu-Sterns (etwa): Kreis Ø 20,6 geschnitten mit 20 mm Breite – die Ecken des Rechtecks hat der Stern nicht."""
    kreis = P(SW_VORNE - SW_STERN[2] / 2, SW_Y, zc) * Rot(0, 90, 0) * Cylinder(SW_STERN[1] / 2, SW_STERN[2])
    return kreis & quader(SW_VORNE - SW_STERN[2] - 1, SW_VORNE + 1, SW_Y - 20, SW_Y + 20, zc - SW_STERN[0] / 2, zc + SW_STERN[0] / 2)


def streuscheibe():
    """Streuscheibe für ein Licht (2 Stück drucken, Natur- oder Weiß-PETG): liegt innen in der Vertiefung vor dem Lichtband.
    Modelliert an der Vorderwand."""
    sd, sl, sh = STREU
    xi = X_VORNE - WAND
    return quader(xi, xi + sd, LICHT_Y - sh, LICHT_Y + sh, -sl, sl)


def scharnier_lappen():
    """Hinten je Scharnier zwei Lappen an der Haube (außen mit Kernloch, innen mit Durchgangsloch),
    dazwischen der Lappen des Rings. Achse M3 × 18 (mit × 16 griffe das Gewinde nur 2,4 mm)."""
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
            lappen -= zyl_z((PILOT_QUER if aussen_liegend else DURCH_QUER) / 2, SCH_X, SCH_Y, z0 - s, z1 + s)
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

    # Kameras: je zwei Pfosten an der Vorderwand, vom Dach bis unter die Platine, Nut von unten offen
    # (die inneren Pfosten beider Kameras liegen in der Mitte zusammen – jede Kamera hat ihre eigene Nut darin)
    xi = X_VORNE - WAND
    for (_n, zc) in KAMERAS:
        for s in (1, -1):
            z0, z1 = zc + s * (KAM_B / 2 - 1.5), zc + s * (KAM_B / 2 + 3.5)
            pfosten = quader(KAM_X - KAM_T - 3.0, xi + 0.5, KAM_UNTEN - 2.0, DACH_UNTEN + 0.1, z0, z1)
            # kleine Nase unten in der Nut: die Platine schnappt beim Einschieben darüber
            pfosten += quader(KAM_X - KAM_T - 0.15, KAM_X - KAM_T + 0.25, KAM_UNTEN - 1.2, KAM_UNTEN - 0.4, z0 - s * 0.05, zc + s * (KAM_B / 2 + 0.3))
            teil += pfosten
    for (_n, zc) in KAMERAS:        # Nuten erst danach schneiden: der Pfosten der anderen Kamera darf sie nicht füllen
        for s in (1, -1):
            z0 = zc + s * (KAM_B / 2 - 1.5)
            nut = quader(KAM_X - KAM_T - 0.15, KAM_X + 0.15, KAM_UNTEN - 3.0, KAM_OBEN, z0 - s * 0.1, zc + s * (KAM_B / 2 + 0.3))
            teil -= nut - quader(KAM_X - KAM_T - 0.15, KAM_X - KAM_T + 0.25, KAM_UNTEN - 1.2, KAM_UNTEN - 0.4, -100, 100)   # Nasen bleiben
    # Fenster: rund mit gerader Kante unten (beim Druck liegt das Dach auf dem Bett – unten im Auto ist beim Druck oben), außen angefast
    r = KAM_FENSTER / 2
    pts = [(r * math.cos(math.radians(d)), KAM_OBJ_Y + r * math.sin(math.radians(d))) for d in range(-45, 226, 5)]
    fen = Plane.YZ * Polygon(*pts, align=None)
    for (_n, zc) in KAMERAS:
        teil -= Pos(X_VORNE - WAND / 2, -zc, 0) * extrude(fen.face(), WAND, both=True)
        # Fase außen in derselben Form wie das Fenster (rund mit gerader Kante unten), 1,5 mm breit, 45°
        fase = P(X_VORNE + 0.01, KAM_OBJ_Y, zc) * Rot(0, -90, 0) * Cone(r + 1.51, r, 1.51, align=None)   # runde 45°-Fase, nach innen enger
        teil -= fase & quader(X_VORNE - 3, X_VORNE + 1, KAM_OBJ_Y - r * math.sin(math.radians(45)), KAM_OBJ_Y + r + 3, zc - r - 3, zc + r + 3)   # unten bleibt die gerade Kante

    # IR-LEDs (Nachtsicht): Block von der Wand bis unters Dach, darin je LED Bohrung + Senkung für den Kragen
    for sz in (1, -1):
        zc = sz * IR_Z
        hb, tief = IR_BLOCK
        teil += quader(X_VORNE - tief, xi + 0.5, min(IR_Y) - 5.0, DACH_UNTEN + 0.1, zc - hb, zc + hb)
        for y in IR_Y:
            kragen_x = X_VORNE - IR_LAENGE
            teil -= zyl_x(IR_LOCH / 2, y, zc, kragen_x - 0.01, X_VORNE + 1)
            teil -= zyl_x(IR_KRAGEN / 2, y, zc, X_VORNE - tief - 1, kragen_x)
            teil -= P(X_VORNE + 0.01, y, zc) * Rot(0, -90, 0) * Cone(IR_LOCH / 2 + 0.8, IR_LOCH / 2, 0.8, align=None)   # kleine Fase außen

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
        teil -= zyl_x(DURCH_QUER / 2, VORNE_Y, zc, LASCHE_X1 - 1, X_VORNE + 1)
        teil -= zyl_x(KOPF_D / 2, VORNE_Y, zc, X_VORNE - KOPF_H, X_VORNE + 1)

    for s in (1, -1):              # Licht: Platz für die Leiste freihalten (auch in den Kamera-Pfosten), Tasche, Lichtband, Blende
        teil -= licht_ausschnitt(s)
        teil += licht(s) - quader(-200, 200, UNTEN - 5, UNTEN, -100, 100)   # Pfosten wieder dazu (ohne Platz der Leiste)
    sw_zu, sw_weg = scheinwerfer()  # Scheinwerfer: Halter dazu, Loch mit Reflektor-Weitung weg
    teil += sw_zu - quader(-200, 200, UNTEN - 5, UNTEN, -100, 100)
    teil -= sw_weg
    for zc in VORNE_Z:              # Platz für die Laschen des Rings bleibt frei (die innere Schiene grenzt an das Polster)
        teil -= quader(LASCHE_X0 - 0.5, LASCHE_X1 + 0.5, UNTEN - 1, LASCHE_OBEN + 0.5, zc - LASCHE_B / 2 - 0.5, zc + LASCHE_B / 2 + 0.5)
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
    if fl_v.bounding_box().min.X < FUGE - 0.01:
        fl_v = Pos(FUGE + FUGE_SPALT, 0, 0) * extrude(profil, -(FLANSCH_D - FUGE_SPALT))
    fl_h = fl_v.mirror(Plane.YZ.offset(FUGE))
    vorne += fl_v & aussen()
    hinten += fl_h & aussen()
    rb, rt = FUGE_RILLE
    rille = quader(FUGE - rb / 2, FUGE + rb / 2, -gross, gross, -gross, gross) & (aussen() - form(rt, UNTEN - 1, DACH_OBEN - rt, max(0.5, FASE - rt)))
    vorne -= rille
    hinten -= rille
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
            hinten -= zyl_x(DURCH_QUER / 2, y, z, FUGE - FLANSCH_D - 1, FUGE + 0.5)
            vorne -= zyl_x(PILOT_QUER / 2, y, z, FUGE - 0.5, FUGE + FLANSCH_D + 1)
        else:
            vorne -= zyl_x(DURCH_QUER / 2, y, z, FUGE - 0.5, FUGE + FLANSCH_D + 1)
            hinten -= zyl_x(PILOT_QUER / 2, y, z, FUGE - FLANSCH_D - 1, FUGE + 0.5)
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
        v = sum(getattr(d & r, "volume", 0.0) or 0.0 for r in ring_teile)   # leere Schnittmenge kann None sein
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
    for (n, zc) in KAMERAS:    # beide Kameras zusammen mit dem gemeinsamen Pfosten in der Mitte als ein Rechteck je Kamera
        rechtecke.append((n, KAM_X - KAM_T - 3, X_VORNE - WAND - 5.3, zc - KAM_B / 2 - (3.5 if zc < 0 else 0.0), zc + KAM_B / 2 + (3.5 if zc > 0 else 0.0)))
    for sz in (1, -1):
        rechtecke.append((f"IR-LEDs {'links' if sz > 0 else 'rechts'}", X_VORNE - IR_BLOCK[1], X_VORNE - WAND, sz * IR_Z - IR_BLOCK[0] + 1.0, sz * IR_Z + IR_BLOCK[0] - 1.0))   # vorderster Teil der Pfosten: unter der Kamera geht das Frontlicht durch (Höhe geprüft unten)
    dx, dz = DISPLAY
    rr = DISPLAY_PCB / 2 + 2.0
    rechtecke.append(("Display mit Haken", dx - rr, dx + rr, dz - rr, dz + rr))
    kx, kz, kd = LIDAR_KABEL
    rechtecke.append(("LiDAR-Kabelloch", kx - kd / 2, kx + kd / 2, kz - kd / 2, kz + kd / 2))
    for s, nm in ((1, "Frontlicht"), (-1, "Rücklicht")):
        xi = s * (X_VORNE - WAND)
        x0, x1 = sorted((xi, xi - s * 5.3))
        rechtecke.append((f"{nm} (Leiste + Pfosten)", x0, x1, -(LICHT_L / 2 + 3.5), LICHT_L / 2 + 3.5))
    for sz in (1, -1):
        xb = SW_VORNE - SW_STERN[2] - 2.3
        rechtecke.append((f"Scheinwerfer {'links' if sz > 0 else 'rechts'} (Stern im Schlitz)", xb, X_VORNE - WAND, sz * SW_Z - SW_STERN[0] / 2 - 0.25, sz * SW_Z + SW_STERN[0] / 2 + 0.25))
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
               "Display": DISPLAY_PCB_UNTEN - 3.0, "Licht-Leisten": UNTEN + 0.0}
    print(f"  Frontlicht unter der Kamera: Oberkante Leiste {LICHT_OBEN:.1f}, Kamera-Platine ab {KAM_UNTEN:.1f}, Objektiv-Fenster ab {KAM_OBJ_Y - KAM_FENSTER / 2:.1f}")
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
    print("Hälften durchdringen sich:", "nein" if getattr(vorne & hinten, "volume", 0.0) < 0.5 else "JA")
    # Schraubendreher-Zugang zu den Schrauben an der Fuge (Haube aufgeklappt – alles, was am Dach hängt, ist mit im Weg)
    schr = [(f"Fuge y={y:.0f} z={z:+.0f} (Kopf {kopf})", FUGE - FLANSCH_D if kopf == "hinten" else FUGE + FLANSCH_D, y, z, "x", -1 if kopf == "hinten" else 1)
            for (y, z, kopf) in schrauben]
    bauteile = [("Pi 5 + AI HAT+", PI_X - 45.5, PI_X + 42.5, PI_UNTEN - 1.5, HAT_OBEN + 2, -28, 28),
                ("4G-Modul (Tasche)", -18.85 - 43, -18.85 + 43, DACH_UNTEN - 7.2, DACH_UNTEN, 56.1 - 22, 56.1 + 22),
                ("4G-USB-Stecker", LTE_USB_X, -18.85 - 41, DACH_UNTEN - 9, DACH_UNTEN - 2, 46, 66),
                ("Pololu", 68 - 15, 68 + 15, DACH_UNTEN - 10, DACH_UNTEN, -45 - 15, -45 + 15),
                ("GPS-Antenne", -80 - 14, -80 + 14, DACH_UNTEN - 7, DACH_UNTEN, -55 - 14, -55 + 14),
                ("Kameras", KAM_X - KAM_T - 4, X_VORNE - WAND, KAM_UNTEN - 3, DACH_UNTEN, -32, 32),
                ("MOSFET-Treiber IR", 85 - 15, 85 + 15, DACH_UNTEN - 7, DACH_UNTEN, -11, 11),
                ("MOSFET-Treiber", 78 - 15, 78 + 15, DACH_UNTEN - 7, DACH_UNTEN, 60 - 11, 60 + 11),
                ("Display", DISPLAY[0] - 26, DISPLAY[0] + 26, DISPLAY_PCB_UNTEN - 3, DACH_UNTEN, -26, 26)]
    zugang_pruefen(schr, [("Haube", vorne + hinten)], bauteile)
    sc = streuscheibe()
    print("Streuscheibe passt in die Vertiefung (berührt die Haube nicht):", "ja" if getattr(sc & (vorne + hinten), "volume", 0.0) < 0.01 else "NEIN")
    # Scheinwerfer: Stern, LED-Sockel und Kuppel dürfen die Haube nicht berühren
    sw_frei = True
    for sz in (1, -1):
        zc = sz * SW_Z
        stern = sternform(zc)
        sockel = quader(SW_VORNE, SW_VORNE + 3.2, SW_Y - 4.0, SW_Y + 4.0, zc - 3.5, zc + 3.5)
        kuppel = P(SW_VORNE + 3.2, SW_Y, zc) * Sphere(2.75)
        for t in (stern, sockel, kuppel):
            if getattr(t & (vorne + hinten), "volume", 0.0) > 0.01:
                sw_frei = False
        # Einschieben von unten: Stern (ohne die 0,4-mm-Rastnase an der Rückseite), Sockel und Kuppel 0–14 mm tiefer
        weg = (stern - quader(SW_VORNE - SW_STERN[2] - 1, SW_VORNE - SW_STERN[2] + 0.45, 0, 200, -100, 100)) + sockel + kuppel
        for dy in range(0, 15, 2):
            if getattr(Pos(0, 0, -dy) * weg & (vorne + hinten), "volume", 0.0) > 0.01:
                sw_frei = False
                print(f"  Scheinwerfer {'links' if sz > 0 else 'rechts'}: stößt beim Einschieben {dy} mm unter der Endlage an")
    print("Scheinwerfer passen in die Halter und lassen sich von unten einschieben:", "ja" if sw_frei else "NEIN")
    for name, t in (("haube_vorne", vorne), ("haube_hinten", hinten), ("streuscheibe", sc)):
        export_stl(t, str(AUS / f"{name}.stl"), tolerance=0.02, angular_tolerance=0.15)
        export_step(t, str(AUS / f"{name}.step"))
        bb = t.bounding_box()
        print("gültig" if t.is_valid else "UNGÜLTIG", f"{name} {bb.size.X:.1f} × {bb.size.Y:.1f} × {bb.size.Z:.1f} mm, Volumen {t.volume / 1000:.1f} cm³")
