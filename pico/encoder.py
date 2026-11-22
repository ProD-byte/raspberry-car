# Encoder der vier Motoren zählen – mit der PIO des Pico, damit kein Impuls verloren geht.
#
# Jeder Motor hat einen Encoder mit zwei Kanälen A und B. Bei jeder steigenden Flanke von A
# schaut die PIO auf B:
#   B aus → das Rad dreht vorwärts  → Zähler X eins runter
#   B an  → das Rad dreht rückwärts → Zähler Y eins runter
# Beide Zähler zählen nur abwärts (das kann die PIO in einem Schritt). Daraus rechnen wir
# die Stellung: vorwärts gezählt − rückwärts gezählt. Die PIO läuft ganz allein weiter,
# auch wenn MicroPython gerade etwas anderes tut.

import rp2
from machine import Pin
import pins
import einstellungen as E

MASKE = 0xFFFFFFFF


@rp2.asm_pio()
def _flanken_zaehler():
    wrap_target()
    wait(0, pin, 0)            # warten, bis A aus ist …
    wait(1, pin, 0)            # … und wieder an: steigende Flanke
    jmp(pin, "rueck")          # jmp-Pin = B. B an → rückwärts
    jmp(x_dec, "ende")         # vorwärts: X − 1 (springt immer zum selben Ziel)
    label("ende")
    jmp("weiter")
    label("rueck")
    jmp(y_dec, "weiter")       # rückwärts: Y − 1
    label("weiter")
    wrap()


class Encoder:
    def __init__(self, nummer, name, pins_ab, umkehren=False):
        """nummer = State Machine 0 … 3 (PIO-Block 0; das WLAN-Funkmodul nutzt einen anderen Block).
        pins_ab = (A, B)."""
        a, b = pins_ab
        self.name = name
        self.umkehren = umkehren
        # Pull-up: falls der Encoder nur nach Masse schaltet. Schadet sonst nicht.
        pin_a = Pin(a, Pin.IN, Pin.PULL_UP)
        pin_b = Pin(b, Pin.IN, Pin.PULL_UP)
        self.sm = rp2.StateMachine(nummer, _flanken_zaehler, in_base=pin_a, jmp_pin=pin_b)
        self.sm.active(1)
        self.null = self._roh()

    def _lesen(self, register):
        # Der PIO von außen einen Befehl geben: Register in den Eingang schieben und abholen
        self.sm.exec("in_(%s, 32)" % register)
        self.sm.exec("push()")
        return self.sm.get()

    def _roh(self):
        vor = (-self._lesen("x")) & MASKE      # X und Y zählen von 0 abwärts
        rueck = (-self._lesen("y")) & MASKE
        return vor - rueck

    def stand(self):
        """Gezählte Impulse seit dem Start bzw. seit nullen() (vorwärts positiv)."""
        n = self._roh() - self.null
        return -n if self.umkehren else n

    def nullen(self):
        self.null = self._roh()

    def strecke_mm(self):
        return self.stand() * 3.14159 * E.RAD_DURCHMESSER_MM / E.IMPULSE_PRO_UMDREHUNG


def alle_encoder():
    """Die vier Encoder als Wörterbuch, Schlüssel wie in einstellungen.py."""
    u = E.ENCODER_UMKEHREN
    return {
        "vorne_links": Encoder(0, "vorne_links", pins.ENC_VORNE_LINKS, u["vorne_links"]),
        "hinten_links": Encoder(1, "hinten_links", pins.ENC_HINTEN_LINKS, u["hinten_links"]),
        "vorne_rechts": Encoder(2, "vorne_rechts", pins.ENC_VORNE_RECHTS, u["vorne_rechts"]),
        "hinten_rechts": Encoder(3, "hinten_rechts", pins.ENC_HINTEN_RECHTS, u["hinten_rechts"]),
    }
