# Die beiden Laser-Nahsensoren VL53L1X (vorne und hinten) und der Hindernis-Stopp.
#
# Beide Sensoren haben ab Werk dieselbe I²C-Adresse (0x29). Deshalb schalten wir sie beim Start
# über ihre XSHUT-Leitung nacheinander ein und geben jedem eine eigene Adresse
# (vorne 0x31, hinten 0x33 – steht in pins.py). Fehlt ein Sensor, läuft der Rest trotzdem.

import time
from machine import Pin, I2C
import pins
import einstellungen as E
from vl53l1x import VL53L1X, STANDARD_ADRESSE


def i2c_bus():
    """Der Sensorbus (I2C1 an GP10/GP11). Auch für BNO085 und INA226."""
    return I2C(pins.I2C_ID, sda=Pin(pins.I2C_SDA), scl=Pin(pins.I2C_SCL), freq=400_000)


class Nahsensoren:
    def __init__(self, i2c=None):
        self.i2c = i2c or i2c_bus()
        self.sensoren = {}
        self.abstand = {"vorne": None, "hinten": None}      # mm, None = frei / unbekannt
        self.zeit = {"vorne": 0, "hinten": 0}              # wann zuletzt gemessen
        self.fehlt = []
        xshut = {name: Pin(nr, Pin.OUT, value=0) for name, nr in pins.TOF_XSHUT.items()}
        time.sleep_ms(10)                                   # alle aus
        for name, pin in xshut.items():
            pin.value(1)                                    # nur diesen einschalten
            try:
                s = VL53L1X(self.i2c, STANDARD_ADRESSE)
                s.warten_bis_wach()
                s.adresse_setzen(pins.TOF_ADRESSEN[name])
                s.starten(E.NAH_MESSABSTAND_MS)
                self.sensoren[name] = s
            except OSError as fehler:
                print("Nahsensor", name, "fehlt:", fehler)
                self.fehlt.append(name)
                pin.value(0)                                # aus lassen, damit er den Bus nicht stört

    def messen(self):
        """Neue Werte abholen (oft aufrufen, z. B. alle 20 ms). Gibt {'vorne': mm, 'hinten': mm} zurück."""
        jetzt = time.ticks_ms()
        for name, s in self.sensoren.items():
            try:
                if s.daten_bereit():
                    self.abstand[name] = s.lesen()
                    self.zeit[name] = jetzt
            except OSError:
                self.abstand[name] = None
            # Zu alter Wert (Sensor hängt?) zählt nicht mehr
            if time.ticks_diff(jetzt, self.zeit[name]) > 4 * E.NAH_MESSABSTAND_MS:
                self.abstand[name] = None
        return self.abstand


def faktor(mm):
    """Wie viel vom Tempo in Richtung des Hindernisses erlaubt ist: 1 = alles, 0 = gar nichts."""
    if mm is None or not E.HINDERNIS_STOPP_AN:
        return 1.0
    if mm <= E.HINDERNIS_STOPP_MM:
        return 0.0
    if mm >= E.HINDERNIS_LANGSAM_MM:
        return 1.0
    return (mm - E.HINDERNIS_STOPP_MM) / (E.HINDERNIS_LANGSAM_MM - E.HINDERNIS_STOPP_MM)


def begrenzen(links, rechts, vorne_mm, hinten_mm):
    """Tempo links/rechts so verkleinern, dass das Auto nicht auf ein Hindernis fährt.

    Nur der Anteil „vor“ bzw. „zurück“ wird gebremst – drehen auf der Stelle geht immer,
    damit man vom Hindernis wegdrehen kann. Gibt (links, rechts, gesperrt) zurück;
    gesperrt = True heißt: in diese Richtung geht es gerade gar nicht weiter.
    """
    v = (links + rechts) / 2
    if v > 0:
        f = faktor(vorne_mm)
    elif v < 0:
        f = faktor(hinten_mm)
    else:
        return links, rechts, False
    weg = v * (1 - f)
    return links - weg, rechts - weg, f == 0.0
