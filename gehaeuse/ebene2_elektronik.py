"""Raspberry Car – Ebene 2: Elektronik-Deck (Antrieb)

Eine gedruckte Platte für Pico 2 W (auf dem Freenove-Board), 2 × DRV8833, MP1584,
BNO085, 2 × WAGO 221-415 und das Ladeboard DDTCCRUB 2S (hinten links, USB-C durch den Ring). Alle Maße in mm. Erzeugt STL und STEP in gehaeuse/ebene2/.

Aufteilung in Zonen (gut erreichbar, ordentlich):
  * Motorzone vorne und Motorzone hinten, beide gleich: je ein Griffloch genau über jedem Motorstecker
    (von oben einstecken/abziehen, mit Rand eingefasst), dazwischen der Motortreiber DRV8833 für diese Achse,
    rechts außen der 3,3-V-Verteiler für deren Encoder. Kurze Motorkabel.
  * Mitte: Steuerung – vorne der Pico auf dem Freenove-Board, hinten der Kompass BNO085 (weit weg von der
    Stromversorgung, die vorne in der Wanne liegt).
  * Rand: hinten links Laden (Ladeboard, USB-C durch den Ring), hinten rechts der Hauptschalter, vorne rechts
    Strom (Durchbruch C über den Verteilern, MP1584).
  * Zwei Druckteile je Teil: das Deck ist bei x = DECK_FUGE geteilt (zwei aufrechte Stege, quer verschraubt),
    der Ring bei x = RING_FUGE. Jede Ring-Hälfte ist für sich auf das Deck geschraubt – so überbrückt der Ring
    die Fuge des Decks und das Deck die Fuge des Rings.
  * Ebene 3 wird ein Klappdeckel: die beiden hinteren Dome tragen das Scharnier (M3 als Achse),
    vorne hält eine Schraube. Deckel auf → die ganze Ebene 2 liegt offen.

Kompass: rund um den BNO085 kein Magnet, keine Spule und keine Leitung mit viel Strom.

Aufruf (einmalig: pip install build123d):
    python ebene2_elektronik.py

Koordinaten wie im 3D-Modell: Mitte des Autos = 0, x nach vorne, z nach links,
y nach oben. Im CAD (Z oben): X = x, Y = −z, Z = y.

Aufbau:
  * Platte 250 × 180 × 3 mm in derselben Form wie die Wanne. Sie ist der Deckel der
    Wanne (liegt auf dem Rand bei 58 mm). Die Wanne wird von unten mit 4 × M3 × 45
    an 4 Dome dieser Platte geschraubt (Kernloch von unten, 11 mm tief, oben geschlossen).
  * Gehäuse-Ring oben (23 mm): Seitenwand bis Ebene 3, Röhren über den Domen
    für Ebene 3. Umgedreht drucken (Oberkante aufs Bett), ohne Stützen.
    In seiner Rückwand: Hauptschalter (Taster Ø 12 mm) und ein Ausschnitt (13,5 × 8 mm, angefast) für
    die USB-C-Buchse des Ladeboards, das direkt dahinter auf dem Deck sitzt.
  * Freenove-Board: 4 Schraubdome, M3 schneidet sich das Gewinde selbst.
  * Module ohne Befestigungslöcher sitzen in Einklick-Taschen: passgenauer
    Rahmen (0,3 mm Luft) mit Rastnasen an den langen Seiten und einer Kerbe zum
    Heraushebeln.
  * Dome für den Ring (8 mm hoch, Kernloch 11 mm): vorne in den Ecken, hinten an der Rückwand (= Scharnier) und
    je zwei an den Seiten bei der Fuge des Rings.
  * 4 Grifflöcher (über den Motorsteckern), Durchbrüche D (Daten), S (Schalter), B (Laden), C (Strom).
"""
from pathlib import Path
from build123d import (Box, Cylinder, Rot, Rectangle, RectangleRounded, Pos, Plane, Polygon, extrude, chamfer, Axis,
                       export_stl, export_step)

# ------------------------------------------------------------------ Parameter
X_VORNE, X_HINTEN = 125.0, -125.0       # gleiche Außenform wie die Wanne
L = X_VORNE - X_HINTEN                   # 250 mm
XM = (X_VORNE + X_HINTEN) / 2            # 0
B, R_ECKE = 180.0, 12.0
UNTEN = 58.0                             # liegt direkt auf dem Wannenrand (Deckel der Wanne, LEVEL[1] im Modell)
DICKE = 3.0
OBEN = UNTEN + DICKE                     # Oberkante Platte (TOP[1] im Modell)

from loecher import PILOT_HOCH, PILOT_QUER, DURCH_HOCH, DURCH_QUER, M25_PILOT_HOCH   # M3-Löcher je Filament und Druckrichtung (loecher.py)
KOPF_D, KOPF_H = 6.5, 3.1                # Senkung: Zylinderkopf schließt bündig ab
DOM_D = 10.0                             # Schraubdom: (10 − 2,6)/2 = 3,7 mm Material

WANNE_DOME = [(X_VORNE - 7.5, 35), (X_VORNE - 7.5, -35), (X_HINTEN + 7.5, 35), (X_HINTEN + 7.5, -35)]   # über den Säulen der Wanne: M3 × 45 von unten
NACH_OBEN = [(X_VORNE - 11.5, B / 2 - 7.4), (X_VORNE - 11.5, -(B / 2 - 7.4)), (X_HINTEN + 7.4, 23.3), (X_HINTEN + 7.4, -23.3)]   # Ring ↔ Deck in den Ecken; hinten = Scharnier
RING_FUGE = -16.5                        # der Ring ist hier geteilt (vordere / hintere Hälfte)
HALTE = [(RING_FUGE + 12, B / 2 - 7.4), (RING_FUGE + 12, -(B / 2 - 7.4)), (RING_FUGE - 12, B / 2 - 7.4), (RING_FUGE - 12, -(B / 2 - 7.4))]   # zusätzlich: jede Ring-Hälfte an der Fuge ans Deck
RING_DOME = NACH_OBEN + HALTE
ROHR_R = DOM_D / 2 + 0.3 + 1.2         # Röhre im Ring als Hülse über den Dom der Platte: 0,3 mm Luft + 1,2 mm Wand (Ø 13)

FREENOVE = (20.0, 0.0)                   # Mitte des Freenove-Boards, NICHT gedreht: die Klemmen-Reihen zeigen zu den Seiten, dort ist Platz für die Kabel
FREENOVE_LOCH = (29.0, 26.0)             # Lochabstand 58 × 52 (x, z)
FREENOVE_HALB = (31.5, 28.5)             # halbe Plattengröße (x, z)
FREENOVE_DOM_H = 4.0                     # Platz für Lötstellen unter dem Board

# Einklick-Taschen: (Name, Mitte x, Mitte z, Innenmaß x, Innenmaß z, Höhe Rastnase über Boden, Wandhöhe, offene Seite)
# offene Seite (+z / −z): dort keine Wand – bei den WAGO-Klemmen die Kabelseite.
# "-x": hinten keine Wand, dort ist die Rückwand des Gehäuse-Rings der Anschlag (Ladeboard: USB-C geht durch den Ring). Die Rückwand ist dann nur 4 mm hoch
# (Hebel klappen frei auf), die Rastnasen sitzen an den kurzen Enden.
LUFT = 0.3
TASCHEN = [
    # Motorzone vorne (Achse x = 80): Treiber mittig zwischen den beiden Grifflöchern, 3,3-V-Verteiler rechts außen (Kabelseite nach außen)
    ("DRV8833 vorne",   80.0,   0.0, 16.8, 18.6, 1.6, 3.2, None),
    ("WAGO 3,3 V vorne", 80.0, -60.0, 29.7, 18.4, 8.1, 8.8, -1),
    # Motorzone hinten (Achse x = −80): genauso
    ("DRV8833 hinten", -80.0,   0.0, 16.8, 18.6, 1.6, 3.2, None),
    ("WAGO 3,3 V hinten", -80.0, -60.0, 29.7, 18.4, 8.1, 8.8, -1),
    # Steuerung: Kompass hinter dem Freenove-Board, um 90° gedreht (STEMMA-QT-Buchsen zeigen zu den Seiten, dort ist frei)
    ("BNO085",        -35.0,   0.0, 22.9, 25.4, 1.6, 3.2, None),
    # Strom und Laden
    ("MP1584",        -24.0, -62.0, 22.1, 16.8, 1.6, 3.2, None),   # rechts hinter dem Freenove-Board (nicht vor der Schraube an der Fuge), ca. 6 cm vom Kompass
    ("Ladeboard",  X_HINTEN + 20.3, 60.0, 38.4, 18.0, 1.6, 3.2, "-x"),  # hinten links: Platine liegt bündig an der Innenseite der Rückwand, die USB-C-Buchse steckt in der Wand (1 mm hinter der Außenseite)
]
WAND = 1.6
NASE = 0.6
# Aussparungen in den kurzen Wänden (Breite in mm), z. B. für STEMMA-QT-Stecker, die waagerecht eingesteckt werden
AUSSPARUNG = {"BNO085": 16.0}                               # wie weit die Rastnase über die Platine greift

# Durchbrüche (x, z, Länge in x, Breite in z)
GRIFFLOECHER = 4                         # die ersten 4 Einträge sind Grifflöcher (mit Rand)
SCHLITZE = [
    (80, 30, 28, 20), (80, -30, 28, 20),     # Grifflöcher vorne: je eines über einem Motorstecker der Vorderachse (Platz für zwei Finger)
    (-80, 30, 28, 20), (-80, -30, 28, 20),   # Grifflöcher hinten: genauso für die Hinterachse (auch XSHUT vorne/hinten)
    (0, 50, 20, 10),                         # D: Daten vom INA226 (Wanne vorne links) zum Pico
    (-50, -76, 14, 9),                       # S: Leitungen zum Hauptschalter (hinten rechts)
    (-70, 62, 14, 9),                        # B: BMS → Ladeboard (hinten links)
    (40, -68, 14, 9),                        # C: Plus/Minus von den Verteilern – über ihnen, vorne rechts, weit weg vom Kompass
]
# Teilung des Decks: zwei aufrechte Stege an der Fuge, quer (in x) verschraubt
DECK_FUGE = 58.0                          # zwischen Freenove-Board und vorderer Motorzone
DECK_SPALT = 0.1
STEG_H = 10.0                             # Stege 10 mm hoch über dem Deck
STEG_VORNE, STEG_HINTEN = 5.0, 6.0        # Dicke (x) des vorderen (Gewinde) und hinteren Stegs (Kopf)
STEG_Z = [(-80.0, -49.0), (48.0, 80.0)]   # zwei Stücke außen (innen sind die Grifflöcher und das Freenove-Board)
STEG_SCHRAUBEN = [-54.0, 64.0]            # z der Schrauben M3 × 10 (Kopf hinten, Gewinde im vorderen Steg). Hinter jedem Kopf
                                          # ist 60 mm Platz für den Schraubendreher (rechts zwischen Durchbruch C und dem Freenove-Board)
STEG_SCHRAUBE_Y = 5.0                     # Höhe der Schrauben über dem Deck
GRIFFLOCH_RAND = (1.6, 2.0)              # Rand um die beiden Grifflöcher: Breite, Höhe – sieht sauber aus, Kabel scheuern nicht

AUS = Path(__file__).resolve().parent / "ebene2"


def P(x, y, z):
    return Pos(x, -z, y)


def zyl_z(r, x, y, z0, z1):
    return P(x, y, (z0 + z1) / 2) * Rot(90, 0, 0) * Cylinder(r, abs(z1 - z0))


def zyl_x(r, y, z, x0, x1):
    return P((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, abs(x1 - x0))


def zyl_y(r, x, z, y0, y1):
    return P(x, (y0 + y1) / 2, z) * Cylinder(r, y1 - y0)


def quader(x0, x1, y0, y1, z0, z1):
    """Quader zwischen zwei Ecken (Reihenfolge egal)."""
    return P((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(z1 - z0), abs(y1 - y0))


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


def platte():
    teil = Pos(XM, 0, UNTEN) * extrude(RectangleRounded(L, B, R_ECKE), DICKE)
    teil = chamfer(teil.edges().group_by(Axis.Z)[-1], 1.0)          # obere Kante leicht angefast

    # Dome über den Säulen der Wanne: Kernloch von unten, 11 mm tief und oben geschlossen (die M3 × 45 kommt von unten durch die Wanne)
    for (x, z) in WANNE_DOME:
        teil += zyl_y(DOM_D / 2, x, z, OBEN - 0.1, OBEN + 9)
        teil -= zyl_y(PILOT_HOCH / 2, x, z, UNTEN - 0.1, UNTEN + 11)

    # Dome für den Ring: Dom auf der Platte, Kernloch 11 mm tief
    for (x, z) in RING_DOME:
        teil += zyl_y(DOM_D / 2, x, z, OBEN - 0.1, OBEN + 8)
        teil -= zyl_y(PILOT_HOCH / 2, x, z, UNTEN + 0.1, OBEN + 8.1)

    # Freenove-Board: 4 Dome oben (Platz für Lötstellen), Kernloch M2,5 6,5 mm tief (M2,5 × 8 greift 6,4 mm)
    fx, fz = FREENOVE
    for sx in (1, -1):
        for sz in (1, -1):
            x, z = fx + sx * FREENOVE_LOCH[0], fz + sz * FREENOVE_LOCH[1]
            teil += zyl_y(DOM_D / 2, x, z, OBEN - 0.1, OBEN + FREENOVE_DOM_H)
            teil -= zyl_y(M25_PILOT_HOCH / 2, x, z, UNTEN + 0.5, OBEN + FREENOVE_DOM_H + 0.1)

    # Einklick-Taschen
    for (name, x, z, ix, iz, nase_h, wand_h, offen) in TASCHEN:
        ax, az = ix / 2 + LUFT, iz / 2 + LUFT
        rahmen = quader(x - ax - WAND, x + ax + WAND, OBEN - 0.1, OBEN + wand_h, z - az - WAND, z + az + WAND)
        rahmen -= quader(x - ax, x + ax, OBEN - 0.2, OBEN + wand_h + 0.1, z - az, z + az)
        if offen == "-x":      # hintere Wand weg, sonst wie eine normale Tasche
            rahmen -= quader(x - ax - WAND - 0.2, x - ax + 0.1, OBEN - 0.2, OBEN + wand_h + 0.2, z - az - WAND - 0.2, z + az + WAND + 0.2)
            # Seitenwände nur im vorderen Teil: hinten sitzen der Dom der Wannenschraube und die Ecke des Rings
            rahmen -= quader(x - ax - WAND - 0.2, X_HINTEN + 14.0, OBEN - 0.2, OBEN + wand_h + 0.2, z - az - WAND - 0.2, z - az + 0.1)
            rahmen -= quader(x - ax - WAND - 0.2, X_HINTEN + 8.0, OBEN - 0.2, OBEN + wand_h + 0.2, z + az - 0.1, z + az + WAND + 0.2)
            offen = None
        # Kerbe in einer kurzen Seite zum Heraushebeln
        kurz_x = ix <= iz
        if offen:
            pass
        elif kurz_x:
            rahmen -= quader(x - 3, x + 3, OBEN + 0.8, OBEN + wand_h + 0.1, z + az - 0.1, z + az + WAND + 0.1)
        else:
            rahmen -= quader(x + ax - 0.1, x + ax + WAND + 0.1, OBEN + 0.8, OBEN + wand_h + 0.1, z - 3, z + 3)
        y0, y1 = OBEN + nase_h - 0.1, OBEN + nase_h + 0.9      # Keil: 1 mm hoch, Unterseite schräg
        if offen:
            # Kabelseite ganz offen, Rückwand nur 4 mm hoch, Rastnasen an den kurzen Enden (x-Wände)
            rahmen -= quader(x - ax - WAND - 0.1, x + ax + WAND + 0.1, OBEN, OBEN + wand_h + 0.2, z + offen * az - offen * 0.1, z + offen * (az + WAND + 0.2))
            rahmen -= quader(x - ax, x + ax, OBEN + 4, OBEN + wand_h + 0.2, z - offen * az + offen * 0.1, z - offen * (az + WAND + 0.2))
            teil += rahmen
            for s in (1, -1):
                teil += nase_keil("x", x + s * ax, x + s * (ax - NASE), y0, y1, z, 4)
            continue
        if name in AUSSPARUNG:
            a = AUSSPARUNG[name] / 2
            if ix >= iz:
                for s in (1, -1):
                    rahmen -= quader(x + s * ax - s * 0.1, x + s * (ax + WAND + 0.1), OBEN, OBEN + wand_h + 0.2, z - a, z + a)
            else:
                for s in (1, -1):
                    rahmen -= quader(x - a, x + a, OBEN, OBEN + wand_h + 0.2, z + s * az - s * 0.1, z + s * (az + WAND + 0.1))
        teil += rahmen
        # Rastnasen an den beiden langen Seiten (je 6 mm lang), knapp über der Platine
        if ix >= iz:   # lange Seiten liegen entlang x → Nasen an z-Wänden
            for s in (1, -1):
                teil += nase_keil("z", z + s * az, z + s * (az - NASE), y0, y1, x, 3)
        else:
            for s in (1, -1):
                teil += nase_keil("x", x + s * ax, x + s * (ax - NASE), y0, y1, z, 3)

    # Flache Mulde unter dem USB-C-Ausschnitt des Rings: Platz für dicke Stecker-Griffe
    for (seite, m, breite, hoch) in RING_OBEN_AUSSCHNITTE:
        if seite == "hinten":
            teil -= quader(X_HINTEN - 1, X_HINTEN + RING_WAND + 2.0, OBEN - USB_SENKE, OBEN + 1, m - breite / 2, m + breite / 2)

    # Rand um die Grifflöcher (die ersten beiden Durchbrüche)
    rb, rh = GRIFFLOCH_RAND
    for (x, z, lx, bz) in SCHLITZE[:GRIFFLOECHER]:
        r = min(lx, bz) / 2 - 0.01
        teil += P(x, OBEN - 0.1, z) * extrude(RectangleRounded(lx + 2 * rb, bz + 2 * rb, r + rb), rh + 0.1)
    # Durchbrüche
    for (x, z, lx, bz) in SCHLITZE:
        teil -= P(x, UNTEN + DICKE / 2, z) * extrude(RectangleRounded(lx, bz, min(lx, bz) / 2 - 0.01), DICKE + 2, both=True)
    return teil


# ------------------------------------------------------------------ Gehäuse-Ringe
RING_WAND = 2.4                          # Wandstärke der Ringe
EBENE3_UNTEN = 84.0                      # Unterkante Ebene 3 (LEVEL[2] im Modell)
# Ausschnitte von der Unterkante aus: (Seite, Mitte, Breite, Höhe) – Seite "hinten"/"vorne"/"links"/"rechts"
RING_OBEN_AUSSCHNITTE = [("hinten", 60.0, 13.5, 8.0)]   # USB-C des Ladeboards: so groß, dass der Stecker-Griff (bis 13,5 × 8 mm) hineinpasst und voll einrastet
USB_FASE = 1.0                                          # außen 45° angefast – der Stecker findet leichter hinein
USB_SENKE = 1.5                                         # im Deck darunter eine flache Mulde, damit auch dicke Stecker-Griffe Platz haben
# Löcher in der Rückwand des Rings (x = −120): (Name, z, y-Mitte, Breite, Höhe, rund?)
RING_Y_MITTE = (OBEN + EBENE3_UNTEN) / 2
# ---- Klappdeckel (Ebene 3): Scharniere hinten, Laschen vorne – der Deckel selbst ist in ebene3_gehirn.py
# Scharnier hinten (Achse in z-Richtung)
SCH_X, SCH_Y = X_HINTEN - 5.5, EBENE3_UNTEN + 5.0       # Achse hinter der Rückwand und über der Trennfuge: beim Aufklappen stößt nichts an
SCH_R = 5.0
SCH_Z = (33.0, -33.0)
SCH_RING_B, SCH_LAPPEN_B, SCH_SPALT = 8.0, 5.0, 0.3
# Vorne: Laschen vom Ring Ebene 2 (bei z = ±46), Schraube waagerecht bei y = 92
VORNE_Z = (46.0, -46.0)
LASCHE_B, LASCHE_X0, LASCHE_X1, LASCHE_OBEN = 9.6, X_VORNE - 15.0, X_VORNE - 7.5, 97.0
VORNE_Y = 92.0

# Schutzbleche (schutzblech.py): je Rad 2 × M3 × 10 von außen durch den Flansch in eine Schraubsäule innen am Ring
import schutzblech as SB
BLECH_SAEULE = (4.9, 82.0)               # halbe Breite der Säule (x, ≥ 3,5 mm um das Kernloch) und wie weit sie nach innen reicht (|z|)

RING_RUECKWAND = [
    ("Druckschalter Ø 12 mm", -55.0, 74.0, 12.2, 12.2, True),   # 12-mm-Taster (GrabCAD „Push button 12mm“): Frontring Ø 13,9 außen, Körper Ø 11,8 × 19 mm innen, Mutter ca. Ø 16,5
]


def rohr_bohrung(x, z, y0, y1, r0):
    """Alles, was aus einer Röhre des Rings herausgeschnitten wird: Durchgangsloch, Senkung oben, unten Platz für den Dom."""
    t = zyl_y(DURCH_HOCH / 2, x, z, y0 - 1, y1 + 1)
    t += zyl_y(KOPF_D / 2, x, z, y1 - KOPF_H, y1 + 1)   # oben: M3 × 20 in den Dom des Decks, Kopf bündig (Deckel liegt darüber)
    if r0 > y0:   # innen unten: Platz für den Dom der Platte (0,3 mm Luft rundum, 0,2 mm oben)
        t += zyl_y(DOM_D / 2 + 0.3, x, z, y0 - 1, r0 + 0.2)
        # Brücken-Trick: der Ring wird aufrecht gedruckt, die Decke der Aussparung hat ein Loch
        t += quader(x - DOM_D / 2 - 0.3, x + DOM_D / 2 + 0.3, r0 + 0.19, r0 + 0.5, z - DURCH_HOCH / 2, z + DURCH_HOCH / 2)
        t += quader(x - DURCH_HOCH / 2, x + DURCH_HOCH / 2, r0 + 0.49, r0 + 0.8, z - DURCH_HOCH / 2, z + DURCH_HOCH / 2)
    return t


def ring(y0, y1, rohre, ausschnitte, rohr_ab=None):
    """Seitenwand mit der Außenform der Platten. rohre: Röhren mit Durchgangsloch M3, mit der Außenwand verbunden.
    rohr_ab: Höhe, bis zu der unten ein Dom der Platte in die Röhre ragt. Röhre und Verbindung gehen trotzdem bis
    ganz unten – nur eine passende Aussparung für den Dom bleibt frei (keine Luft darunter, druckt einfacher)."""
    h = y1 - y0
    wand = Pos(XM, 0, y0) * extrude(RectangleRounded(L, B, R_ECKE), h)
    wand -= Pos(XM, 0, y0 - 1) * extrude(RectangleRounded(L - 2 * RING_WAND, B - 2 * RING_WAND, R_ECKE - RING_WAND), h + 2)
    r0 = rohr_ab if rohr_ab is not None else y0
    aussenform = Pos(XM, 0, y0 - 1) * extrude(RectangleRounded(L, B, R_ECKE), h + 2)
    for (x, z) in rohre:
        # Röhre als Hülse: geht von unten bis oben und umschließt den Dom der Platte ganz – von außen eine
        # durchgehende Säule ohne Fuge. In voller Breite mit der Außenwand verbunden (in Ecken mit beiden Wänden).
        saeule = zyl_y(ROHR_R, x, z, y0, y1)
        bis_seite = B / 2 - abs(z)
        bis_ende = (X_VORNE - x) if x > XM else (x - X_HINTEN)
        sz = 1 if z > 0 else -1
        xw = X_VORNE - RING_WAND / 2 if x > XM else X_HINTEN + RING_WAND / 2
        b = ROHR_R - 0.05                      # 0,05 mm innerhalb der Röhre: eindeutige CAD-Berechnung
        if bis_seite <= bis_ende or bis_seite < 15:
            saeule += quader(x - b, x + b, y0, y1, z, sz * (B / 2 - RING_WAND / 2))
        if bis_ende < bis_seite or bis_ende < 15:
            saeule += quader(x, xw, y0, y1, z - b, z + b)
        wand += saeule & aussenform            # nichts ragt außen aus dem Ring heraus
        wand -= rohr_bohrung(x, z, y0, y1, r0)
    for (seite, m, breite, hoch) in ausschnitte:
        if seite in ("hinten", "vorne"):
            xs = X_HINTEN if seite == "hinten" else X_VORNE
            wand -= quader(xs - 1, xs + (RING_WAND + 4) * (1 if seite == "hinten" else -1), y0 - 1, y0 + hoch, m - breite / 2, m + breite / 2)
            ri = 1 if seite == "hinten" else -1
            wand -= P(xs - ri * 0.01, y0, m) * Rot(0, 90 * ri, 0) * extrude(Rectangle(2 * (hoch + USB_FASE), breite + 2 * USB_FASE), USB_FASE + 0.01, taper=45)
        else:
            zs = B / 2 if seite == "links" else -B / 2
            wand -= quader(m - breite / 2, m + breite / 2, y0 - 1, y0 + hoch, zs + 1 * (1 if seite == "links" else -1), zs - (RING_WAND + 4) * (1 if seite == "links" else -1))
    return wand


def ring_klappdeckel():
    """Was der Ring von Ebene 2 für den Klappdeckel braucht (der Deckel selbst: ebene3_gehirn.py):
    Scharnier-Lappen hinten (mit 45°-Stütze darunter) und die zwei Laschen vorne."""
    t = None
    for zc in SCH_Z:
        lappen = zyl_z(SCH_R, SCH_X, SCH_Y, zc - SCH_RING_B / 2, zc + SCH_RING_B / 2)
        # Halter: unten 45° aus der Rückwand heraus (druckt ohne Stützen), über der Trennfuge 0,3 mm Abstand zum Deckel
        keil = Plane.XZ * Polygon((X_HINTEN + 0.5, EBENE3_UNTEN - 11.5), (X_HINTEN + 0.5, EBENE3_UNTEN), (X_HINTEN - 0.3, EBENE3_UNTEN),
                                  (X_HINTEN - 0.3, SCH_Y), (SCH_X, SCH_Y), (SCH_X - SCH_R, EBENE3_UNTEN - 0.5), align=None)
        lappen += Pos(0, -zc, 0) * extrude(keil.face(), SCH_RING_B / 2, both=True)
        lappen -= zyl_z(DURCH_QUER / 2, SCH_X, SCH_Y, zc - SCH_RING_B, zc + SCH_RING_B)
        t = lappen if t is None else t + lappen
    xi = X_VORNE - RING_WAND
    for zc in VORNE_Z:
        b = LASCHE_B / 2
        prof = Plane.XZ * Polygon((xi + 0.5, EBENE3_UNTEN - 23.0), (xi + 0.5, EBENE3_UNTEN), (LASCHE_X1, EBENE3_UNTEN), (LASCHE_X1, LASCHE_OBEN),
                                  (LASCHE_X0, LASCHE_OBEN), (LASCHE_X0, EBENE3_UNTEN - 10.0), align=None)
        lasche = Pos(0, -zc, 0) * extrude(prof.face(), b, both=True)
        lasche -= zyl_x(PILOT_QUER / 2, VORNE_Y, zc, LASCHE_X0 - 1, LASCHE_X1 + 1)
        t += lasche
    return t



def ring_oben():
    """Zwischen Elektronik-Deck und Ebene 3. Röhren über den Domen für Ebene 3.
    In der Rückwand: Hauptschalter und Ausschnitt für die USB-C-Buchse des Ladeboards."""
    wand = ring(OBEN, EBENE3_UNTEN, RING_DOME, RING_OBEN_AUSSCHNITTE, rohr_ab=OBEN + 8)
    wand += ring_klappdeckel()
    # Schraubsäulen für die Schutzbleche: vom Deck bis oben, mit der Seitenwand verbunden, Kernloch waagerecht durch Wand und Säule
    bx, bz = BLECH_SAEULE
    for (x, y, s) in SB.SCHRAUBEN:
        wand += quader(x - bx, x + bx, OBEN, EBENE3_UNTEN, s * bz, s * (B / 2 - RING_WAND / 2))
        wand -= zyl_z(PILOT_QUER / 2, x, y, s * (bz - 1), s * (B / 2 + 1))
    # Die Säulen vorne (x = 107) reichen bis an die Eck-Röhren: deren Senkung und Dom-Aussparung noch einmal frei schneiden
    for (x, z) in RING_DOME:
        wand -= rohr_bohrung(x, z, OBEN, EBENE3_UNTEN, OBEN + 8)
    xr = X_HINTEN
    for (name, z, y, br, h, rund) in RING_RUECKWAND:
        if rund:
            r = br / 2       # rund mit flacher Oberkante (Ring wird aufrecht gedruckt) – der Frontring des Tasters deckt sie ab
            import math
            pts = [(-z + r * math.cos(math.radians(d)), y - r * math.sin(math.radians(d))) for d in range(-45, 226, 5)]
            wand -= Pos(xr + RING_WAND / 2, 0, 0) * extrude((Plane.YZ * Polygon(*pts, align=None)).face(), RING_WAND / 2 + 2, both=True)
        else:
            wand -= P(xr + RING_WAND / 2, y, z) * Rot(0, 90, 0) * extrude(RectangleRounded(h, br, min(br, h) / 2 - 0.01), RING_WAND / 2 + 2, both=True)
    return wand



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


# ------------------------------------------------------------------ Teilung in zwei Hälften
def teilen_deck(teil):
    """Deck → (vordere, hintere Hälfte). An der Fuge auf jeder Seite ein aufrechter Steg, beide quer verschraubt:
    Kopf hinten, Gewinde im vorderen Steg. Die Stege wachsen beim Druck aus der Platte nach oben (ohne Stützen)."""
    gross = 400.0
    vorne = teil & quader(DECK_FUGE + DECK_SPALT, gross, -gross, gross, -gross, gross)
    hinten = teil & quader(-gross, DECK_FUGE - DECK_SPALT, -gross, gross, -gross, gross)
    for (z0, z1) in STEG_Z:
        vorne += quader(DECK_FUGE + DECK_SPALT, DECK_FUGE + STEG_VORNE, OBEN - 0.1, OBEN + STEG_H, z0, z1)
        hinten += quader(DECK_FUGE - STEG_HINTEN, DECK_FUGE - DECK_SPALT, OBEN - 0.1, OBEN + STEG_H, z0, z1)
    ys = OBEN + STEG_SCHRAUBE_Y
    for z in STEG_SCHRAUBEN:
        hinten -= zyl_x(DURCH_QUER / 2, ys, z, DECK_FUGE - STEG_HINTEN - 1, DECK_FUGE + 1)
        vorne -= zyl_x(PILOT_QUER / 2, ys, z, DECK_FUGE - 1, DECK_FUGE + STEG_VORNE + 1)
    return vorne, hinten


RING_FUGE_FASE = 0.6                     # außen an der Fuge je 0,6 mm × 45° – eine saubere Linie statt einer Lücke
RING_LASCHE = (5.0, 1.6)                 # innen an der vorderen Hälfte: Streifen 5 mm über die Fuge, 1,6 mm dick – man sieht nicht durch


def teilen_ring(teil):
    """Ring → (vordere, hintere Hälfte), stumpf gestoßen (ohne Spalt). Jede Hälfte ist mit eigenen Röhren ans Deck geschraubt.
    Innen hat die vordere Hälfte an beiden Seitenwänden einen Streifen, der hinter die hintere Hälfte greift."""
    gross = 400.0
    vorne = teil & quader(RING_FUGE, gross, -gross, gross, -gross, gross)
    hinten = teil & quader(-gross, RING_FUGE, -gross, gross, -gross, gross)
    lb, ld = RING_LASCHE
    zi = B / 2 - RING_WAND
    for s in (1, -1):
        vorne += quader(RING_FUGE - lb, RING_FUGE + 0.5, OBEN, EBENE3_UNTEN - 1.0, s * (zi - ld), s * zi)
        fase = Pos(RING_FUGE, 0, s * B / 2) * Rot(0, 45, 0) * Box(RING_FUGE_FASE * 1.414, 400, RING_FUGE_FASE * 1.414)
        vorne -= fase; hinten -= fase
    return vorne, hinten


def ueberlappungen():
    """Prüft grob, ob Taschen, Dome, Freenove-Board und Durchbrüche sich überschneiden (Draufsicht)."""
    rechtecke = []
    for (name, x, z, ix, iz, _n, _w, offen) in TASCHEN:
        x0 = x - ix / 2 - LUFT - (0 if offen == "-x" else WAND)
        w = 0 if offen == "-x" else WAND      # Ladeboard: Seitenwände nur vorne (dort ist Platz)
        rechtecke.append((name, x0, x + ix / 2 + LUFT + WAND, z - iz / 2 - LUFT - w, z + iz / 2 + LUFT + w))
    fx, fz = FREENOVE
    hx, hz = FREENOVE_HALB
    rechtecke.append(("Freenove-Board", fx - hx, fx + hx, fz - hz, fz + hz))
    for (x, z) in WANNE_DOME:
        rechtecke.append((f"Dom {x},{z}", x - 5, x + 5, z - 5, z + 5))
    for (x, z) in RING_DOME:
        rechtecke.append((f"Röhre/Dom {x},{z}", x - ROHR_R, x + ROHR_R, z - ROHR_R, z + ROHR_R))
    for (x, z, lx, bz) in SCHLITZE:
        rechtecke.append((f"Durchbruch {x},{z}", x - lx / 2, x + lx / 2, z - bz / 2, z + bz / 2))
    for (z0, z1) in STEG_Z:
        rechtecke.append((f"Steg an der Fuge {z0:+.0f}", DECK_FUGE - STEG_HINTEN - 3.5, DECK_FUGE + STEG_VORNE, z0, z1))   # 3,5 mm hinten: Schraubenkopf
    fehler = 0
    for i in range(len(rechtecke)):
        for j in range(i + 1, len(rechtecke)):
            a, b = rechtecke[i], rechtecke[j]
            # Rechtecke (Name, x0, x1, z0, z1) überlappen, wenn sie sich in x UND in z überschneiden
            if a[1] < b[2] - 0.01 and b[1] < a[2] - 0.01 and a[3] < b[4] - 0.01 and b[3] < a[4] - 0.01:
                print("  Überschneidung:", a[0], "↔", b[0]); fehler += 1
    for (name, x0, x1, z0, z1) in rechtecke:
        if name.startswith("Röhre") or name == "Ladeboard":
            continue        # Hülsen des Rings gehen in die Ringwand über; das Ladeboard liegt absichtlich bündig an der Wand
        if x0 < X_HINTEN + 1 or x1 > X_VORNE - 1 or z0 < -B / 2 + 1 or z1 > B / 2 - 1:
            print("  Zu nah am Rand:", name); fehler += 1
    # Nichts (außer den Stegen) liegt über der Fuge des Decks
    for (name, x0, x1, z0, z1) in rechtecke:
        if not name.startswith("Steg") and x0 < DECK_FUGE + 0.6 and x1 > DECK_FUGE - 0.6:
            print("  liegt über der Fuge des Decks:", name); fehler += 1
    print("Überschneidungen:", fehler)
    # Abstand des Kompasses zu allem, was ein Magnetfeld macht (Motoren: Mitte der Motoren in der Wanne)
    bx, bz = next((x, z) for (n, x, z, *_r) in TASCHEN if n == "BNO085")
    mx, mz = next((x, z) for (n, x, z, *_r) in TASCHEN if n == "MP1584")
    cx, cz = next((x, z) for (x, z, lx, bz) in SCHLITZE if (x, z) == (40, -68))
    for (name, x, z) in [("Motor vorne", 80, 30), ("Motor hinten", -80, 30), ("MP1584 (Spule)", mx, mz), ("Durchbruch C (Strom)", cx, cz),
                         ("Verteiler in der Wanne (Strom)", 47, 17), ("Akku in der Wanne", -33, 12)]:
        print(f"  Kompass – {name}: {((x - bx) ** 2 + (z - bz) ** 2) ** 0.5:.0f} mm")


# ------------------------------------------------------------------ Erreichbarkeit
# Nicht nur „überschneidet sich nichts“, sondern: kommt man mit Kabel, Fingern und Schraubendreher heran?
# Geprüft wird in der Draufsicht. Jedes Hindernis hat eine Höhe über dem Deck (mm) – ein Kabel, das in
# 8 mm Höhe in eine Klemme geht, stört eine 3 mm hohe Tasche nicht, ein 9 mm hoher WAGO aber schon.
# Module mit Lötanschlüssen (DRV8833, MP1584, Ladeboard) klickt man zum Löten heraus – dafür bekommen
# ihre Kabel ein paar Zentimeter Reserve, sie brauchen hier keinen Freiraum.
ZUGANG_KLEMME = 13.0      # vor jeder Schraubklemmen-Reihe frei (Aderendhülse 8 mm + Finger/Biegung)
ZUGANG_WAGO = 15.0        # vor der Kabelseite eines WAGO frei
ZUGANG_STEMMA = 12.0      # vor jeder STEMMA-QT-Buchse frei (Stecker waagerecht einstecken)
ZUGANG_FINGER = 4.0       # um jedes Griffloch herum nichts Hohes (Finger greifen schräg hinein)
HOEHE = {"WAGO": 9.0, "Ladeboard": 6.5, "MP1584": 5.5, "DRV8833": 4.5, "BNO085": 5.0}


def hindernisse():
    """Alles auf dem Deck als (Name, x0, x1, z0, z1, Höhe über dem Deck)."""
    h = []
    for (name, x, z, ix, iz, _n, _w, offen) in TASCHEN:
        x0 = x - ix / 2 - LUFT - (0 if offen == "-x" else WAND)
        hoehe = next((v for k, v in HOEHE.items() if k in name), 5.0)
        h.append((name, x0, x + ix / 2 + LUFT + WAND, z - iz / 2 - LUFT - WAND, z + iz / 2 + LUFT + WAND, hoehe))
    fx, fz = FREENOVE
    hx, hz = FREENOVE_HALB
    h.append(("Freenove-Board", fx - hx, fx + hx, fz - hz, fz + hz, 19.0))
    for (x, z) in WANNE_DOME:
        h.append((f"Dom {x},{z}", x - 5, x + 5, z - 5, z + 5, 9.0))
    for (x, z) in RING_DOME:
        h.append((f"Röhre/Dom {x},{z}", x - ROHR_R, x + ROHR_R, z - ROHR_R, z + ROHR_R, 23.0))   # Hülse des Rings über dem Dom
    for (x, y, s) in SB.SCHRAUBEN:
        h.append((f"Schraubsäule Schutzblech {x:+.0f}/{s:+d}", x - BLECH_SAEULE[0], x + BLECH_SAEULE[0], min(s * BLECH_SAEULE[1], s * B / 2), max(s * BLECH_SAEULE[1], s * B / 2), 23.0))
    for (z0, z1) in STEG_Z:
        h.append((f"Steg {z0:+.0f}", DECK_FUGE - STEG_HINTEN - 3.5, DECK_FUGE + STEG_VORNE, z0, z1, STEG_H))
    return h


def erreichbarkeit():
    zonen = []   # (Beschreibung, x0, x1, z0, z1, ab welcher Höhe ein Hindernis stört, wem die Zone gehört)
    fx, fz = FREENOVE
    hx, hz = FREENOVE_HALB
    k = 25.4     # die Klemmen-Reihe ist 2 × 10 × 2,54 mm lang
    if hx < hz:  # gedreht: Klemmen-Reihen zeigen nach vorne/hinten
        zonen += [("Freenove-Klemmen vorne", fx + hx, fx + hx + ZUGANG_KLEMME, fz - k, fz + k, 6.0, "Freenove"),
                  ("Freenove-Klemmen hinten", fx - hx - ZUGANG_KLEMME, fx - hx, fz - k, fz + k, 6.0, "Freenove")]
    else:        # Klemmen-Reihen zeigen zu den Seiten
        zonen += [("Freenove-Klemmen links", fx - k, fx + k, fz + hz, fz + hz + ZUGANG_KLEMME, 6.0, "Freenove"),
                  ("Freenove-Klemmen rechts", fx - k, fx + k, fz - hz - ZUGANG_KLEMME, fz - hz, 6.0, "Freenove")]
    for (name, x, z, ix, iz, _n, _w, offen) in TASCHEN:
        if "WAGO" in name and offen in (1, -1):
            kante = z + offen * (iz / 2 + LUFT)
            zonen.append((f"{name}: Kabelseite", x - 11, x + 11, min(kante, kante + offen * ZUGANG_WAGO), max(kante, kante + offen * ZUGANG_WAGO), 2.0, name))
        if name in AUSSPARUNG:
            a = AUSSPARUNG[name] / 2
            if ix >= iz:
                for sx in (1, -1):
                    kante = x + sx * (ix / 2 + LUFT + WAND)
                    zonen.append((f"{name}: STEMMA-QT {'vorne' if sx > 0 else 'hinten'}", min(kante, kante + sx * ZUGANG_STEMMA), max(kante, kante + sx * ZUGANG_STEMMA), z - a, z + a, 2.0, name))
            else:
                for sz in (1, -1):
                    kante = z + sz * (iz / 2 + LUFT + WAND)
                    zonen.append((f"{name}: STEMMA-QT {'links' if sz > 0 else 'rechts'}", x - a, x + a, min(kante, kante + sz * ZUGANG_STEMMA), max(kante, kante + sz * ZUGANG_STEMMA), 2.0, name))
    for i, (x, z, lx, bz) in enumerate(SCHLITZE[:GRIFFLOECHER]):
        f = ZUGANG_FINGER + GRIFFLOCH_RAND[0]
        wo = ("vorne" if x > 0 else "hinten") + (" links" if z > 0 else " rechts")
        zonen.append((f"Griffloch {wo}: Finger", x - lx / 2 - f, x + lx / 2 + f, z - bz / 2 - f, z + bz / 2 + f, 6.0, "Griffloch"))
    for (name, z, y, br, h, rund) in RING_RUECKWAND:
        # Taster innen: Mutter (ca. Ø 16,5, 3 mm dick) direkt an der Wand, dahinter Körper Ø 12 bis 19 mm, dann Lötfahnen und Kabel
        xi = X_HINTEN + RING_WAND
        zonen.append((f"{name}: Mutter", xi, xi + 3.0, z - 8.25, z + 8.25, y - 8.25 - OBEN, "Schalter"))
        zonen.append((f"{name}: Körper und Kabel", xi + 3.0, xi + 25.5, z - 6.3, z + 6.3, y - 6.3 - OBEN, "Schalter"))
    fehler = 0
    def abstand(r, q):   # kleinster Abstand zweier Rechtecke (0 = berühren/überlappen)
        dx = max(q[0] - r[1], r[0] - q[1], 0); dz = max(q[2] - r[3], r[2] - q[3], 0)
        return (dx * dx + dz * dz) ** 0.5
    for (was, x0, x1, z0, z1, ab, eigner) in zonen:
        rest = [abstand((x0, x1, z0, z1), (a0, a1, b0, b1)) for (name, a0, a1, b0, b1, hoehe) in hindernisse() if eigner not in name and hoehe >= ab]
        print(f"  {was:40s} frei, nächstes Hindernis {min(rest):5.1f} mm daneben")
        if x0 < X_HINTEN + RING_WAND - 0.01 or x1 > X_VORNE - RING_WAND + 0.01 or z0 < -B / 2 + RING_WAND - 0.01 or z1 > B / 2 - RING_WAND + 0.01:
            print(f"  nicht erreichbar: {was} – stößt an den Gehäuse-Ring"); fehler += 1
        for (name, a0, a1, b0, b1, hoehe) in hindernisse():
            if eigner in name or hoehe < ab:
                continue
            if a0 < x1 and x0 < a1 and b0 < z1 and z0 < b1:
                print(f"  nicht erreichbar: {was} – im Weg: {name}"); fehler += 1
    print("Erreichbarkeit – Probleme:", fehler)
    return fehler


if __name__ == "__main__":
    AUS.mkdir(exist_ok=True)
    ueberlappungen()
    erreichbarkeit()
    deck, ring_ganz = platte(), ring_oben()
    dv, dh = teilen_deck(deck)
    rv, rh = teilen_ring(ring_ganz)
    teile = {"platte_vorne": dv, "platte_hinten": dh, "ring_vorne": rv, "ring_hinten": rh}
    for name, t in teile.items():
        print(f"{name}: {len(t.solids())} Körper", "(gut)" if len(t.solids()) == 1 else "– NICHT zusammenhängend!")
    print("Deck-Hälften durchdringen sich:", "nein" if (dv & dh).volume < 0.5 else "JA")
    # Schraubendreher-Zugang zu den Schrauben an der Fuge des Decks (Deckel von Ebene 3 offen): Kopf hinten, Dreher von hinten
    schrauben = [(f"Deck-Fuge z={z:+.0f}", DECK_FUGE - STEG_HINTEN, OBEN + STEG_SCHRAUBE_Y, z, "x", -1) for z in STEG_SCHRAUBEN]
    bauteile = [(n, x0, x1, OBEN, OBEN + hh, z0, z1) for (n, x0, x1, z0, z1, hh) in hindernisse() if not n.startswith(("Röhre", "Steg", "Dom"))]
    bauteile += [(f"Kabel aus Durchbruch {x},{z}", x - lx / 2, x + lx / 2, UNTEN, EBENE3_UNTEN, z - bz / 2, z + bz / 2) for (x, z, lx, bz) in SCHLITZE[GRIFFLOECHER:]]
    zugang_pruefen(schrauben, [("Deck", dv + dh), ("Ring", rv + rh)], bauteile)
    # Schutzbleche: Schrauben von außen (Kopf in der Senkung des Flanschs), Rad und Schutzblech bleiben dran
    blech, rad = SB.schutzblech(), SB.rad()
    bleche = [("Schutzblech", SB.an_rad(blech, ax, s)) for (ax, s) in SB.RAD_ACHSEN]
    raeder = [("Rad", SB.an_rad(rad, ax, s)) for (ax, s) in SB.RAD_ACHSEN]
    kopf_z = SB.WAND_Z + SB.FLANSCH_D - SB.KOPF_H
    schrauben = [(f"Schutzblech x={x:+.0f} {'links' if s > 0 else 'rechts'}", x, y, s * kopf_z, "z", s) for (x, y, s) in SB.SCHRAUBEN]
    zugang_pruefen(schrauben, [("Ring", rv + rh)] + bleche + raeder, [])
    for (x, y, s) in SB.SCHRAUBEN:   # Säule liegt ganz in einer Ring-Hälfte, nicht auf der Fuge
        if abs(x - RING_FUGE) < BLECH_SAEULE[0] + 1:
            print("  Schraubsäule Schutzblech liegt auf der Fuge des Rings:", x)
    # Selbstprüfung: jede Röhre im Ring muss auf ganzer Höhe mit der Außenwand verbunden sein (CAD-Rechenfehler finden)
    from build123d import Vector
    r, luecken = ring_ganz, []
    for (x, z) in RING_DOME:
        sz = 1 if z > 0 else -1
        bis_seite, bis_ende = B / 2 - abs(z), ((X_VORNE - x) if x > XM else (x - X_HINTEN))
        pruef = []
        if bis_seite <= bis_ende or bis_seite < 15:
            pruef += [(x + dx, z + sz * (ROHR_R - 1)) for dx in (-(ROHR_R - 0.5), ROHR_R - 0.5)]
        if bis_ende < bis_seite or bis_ende < 15:
            pruef += [(x + (ROHR_R - 1 if x > XM else -(ROHR_R - 1)), z + dz) for dz in (-(ROHR_R - 0.5), ROHR_R - 0.5)]
        # nur Punkte innerhalb der Außenform zählen (in den gerundeten Ecken liegen manche schon draußen)
        def drin(px, pz):
            cx = min(max(px, X_HINTEN + R_ECKE), X_VORNE - R_ECKE); cz = min(max(pz, -B / 2 + R_ECKE), B / 2 - R_ECKE)
            return (px - cx) ** 2 + (pz - cz) ** 2 < (R_ECKE - 0.3) ** 2
        luecken += [(px, pz, y) for (px, pz) in pruef if drin(px, pz) for y in (OBEN + 10, OBEN + 16, EBENE3_UNTEN - 1) if not r.is_inside(Vector(px, -pz, y))]
        # unten neben der Dom-Aussparung: zwischen Aussparung und Wand muss Material sein
        unten = [(x, z + sz * 5.9)] if (bis_seite <= bis_ende or bis_seite < 15) else []
        unten += [(x + (5.9 if x > XM else -5.9), z)] if (bis_ende < bis_seite or bis_ende < 15) else []
        luecken += [(px, pz, OBEN + 3) for (px, pz) in unten if not r.is_inside(Vector(px, -pz, OBEN + 3))]
    print("Röhren mit der Außenwand verbunden:", "ja" if not luecken else f"NEIN – Lücke bei {luecken}")
    for name, t in teile.items():
        export_stl(t, str(AUS / f"{name}.stl"), tolerance=0.02, angular_tolerance=0.15)
        export_step(t, str(AUS / f"{name}.step"))
        bb = t.bounding_box()
        print("gültig" if t.is_valid else "UNGÜLTIG", f"{name} {bb.size.X:.1f} × {bb.size.Y:.1f} × {bb.size.Z:.1f} mm, Volumen {t.volume / 1000:.1f} cm³")
