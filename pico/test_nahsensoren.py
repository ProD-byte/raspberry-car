# Test: die beiden Laser-Nahsensoren VL53L1X (vorne und hinten).
#
# Geht schon ohne Akku – der Pico bekommt Strom über USB, die Sensoren 3,3 V vom Pico.
# Start in Thonny (Datei öffnen, F5).
#
# Was du prüfst:
#   1. Findet der Pico am I²C-Bus Geräte? Erwartet nach dem Start: 0x31 (vorne) und 0x33 (hinten).
#   2. Hand vor den Sensor halten: die Zahl muss kleiner werden. „frei“ = nichts in Reichweite.
#   3. Hand vor den VORDEREN halten – ändert sich die Zahl bei „hinten“, sind die XSHUT-Leitungen
#      vertauscht (GP13 = vorne, GP12 = hinten, siehe docs/verdrahtung.md).
#
# Beenden: Stopp-Knopf in Thonny (oder Strg+C).

import time
from nahsensoren import Nahsensoren, i2c_bus

bus = i2c_bus()
print("Geräte am Bus vor dem Start:", [hex(a) for a in bus.scan()], "(alle Nahsensoren noch aus)")
nah = Nahsensoren(bus)
print("Geräte am Bus nach dem Start:", [hex(a) for a in bus.scan()])
if nah.fehlt:
    print("Fehlt:", ", ".join(nah.fehlt), "– Lötstellen, 3,3 V, GND, SDA/SCL und XSHUT prüfen")
if not nah.sensoren:
    raise SystemExit("Kein Nahsensor gefunden.")


def text(mm):
    return "   frei" if mm is None else "%4d mm" % mm


while True:
    a = nah.messen()
    print("vorne %s    hinten %s" % (text(a["vorne"]), text(a["hinten"])), end="\r")
    time.sleep_ms(100)
