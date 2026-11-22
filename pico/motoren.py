# Motoren über die beiden Motortreiber DRV8833 steuern.
#
# So funktioniert der DRV8833: Jeder Motor hat zwei Eingänge (IN1, IN2).
#   IN1 = an,  IN2 = PWM  → vorwärts   (je kürzer IN2 an ist, desto schneller)
#   IN1 = PWM, IN2 = an   → rückwärts
#   beide aus             → Motor rollt aus
# Diese Art heißt „langsames Abklingen“ (slow decay): Das Tempo ist gleichmäßiger als bei
# der einfachen Art, besonders bei langsamer Fahrt.
#
# ULT (= nSLEEP) schaltet beide Treiber ein oder aus. Aus = Not-Stopp, egal was die PWM macht.

from machine import Pin, PWM
import pins
import einstellungen as E

VOLL = 65535  # größter PWM-Wert (immer an)


class Motor:
    def __init__(self, name, pin_in1, pin_in2, umkehren=False):
        self.name = name
        self.umkehren = umkehren
        self.in1 = PWM(Pin(pin_in1), freq=pins.PWM_FREQ, duty_u16=0)
        self.in2 = PWM(Pin(pin_in2), freq=pins.PWM_FREQ, duty_u16=0)
        self.tempo = 0.0

    def setzen(self, tempo):
        """tempo von −1 (voll rückwärts) bis +1 (voll vorwärts). Wird auf TEMPO_MAX begrenzt."""
        tempo = max(-1.0, min(1.0, tempo))
        self.tempo = tempo
        if self.umkehren:
            tempo = -tempo
        anteil = abs(tempo) * E.TEMPO_MAX              # wirklich ausgegebener PWM-Anteil
        if abs(tempo) < E.TEMPO_MIN:
            self.in1.duty_u16(0)                       # ausrollen
            self.in2.duty_u16(0)
        elif tempo > 0:
            self.in1.duty_u16(VOLL)
            self.in2.duty_u16(int(VOLL * (1 - anteil)))
        else:
            self.in1.duty_u16(int(VOLL * (1 - anteil)))
            self.in2.duty_u16(VOLL)

    def bremsen(self):
        """Beide Eingänge an: der Motor wird kurzgeschlossen und bremst hart."""
        self.tempo = 0.0
        self.in1.duty_u16(VOLL)
        self.in2.duty_u16(VOLL)


class Antrieb:
    """Alle vier Motoren. Links und rechts bekommen je ein Tempo (Panzerlenkung)."""

    def __init__(self):
        self.ein = Pin(pins.DRV_ENABLE, Pin.OUT, value=0)   # Treiber erst einmal aus
        u = E.MOTOR_UMKEHREN
        self.vl = Motor("vorne_links", pins.DRV_V_IN1, pins.DRV_V_IN2, u["vorne_links"])
        self.vr = Motor("vorne_rechts", pins.DRV_V_IN3, pins.DRV_V_IN4, u["vorne_rechts"])
        self.hl = Motor("hinten_links", pins.DRV_H_IN1, pins.DRV_H_IN2, u["hinten_links"])
        self.hr = Motor("hinten_rechts", pins.DRV_H_IN3, pins.DRV_H_IN4, u["hinten_rechts"])
        self.alle = (self.vl, self.vr, self.hl, self.hr)
        self.ziel_l = self.ziel_r = 0.0      # gewünschtes Tempo
        self.ist_l = self.ist_r = 0.0        # Tempo nach der Rampe

    def einschalten(self):
        self.ein.value(1)

    def ausschalten(self):
        """Not-Stopp: Treiber schlafen legen und alles auf 0."""
        self.ein.value(0)
        self.ziel_l = self.ziel_r = self.ist_l = self.ist_r = 0.0
        for m in self.alle:
            m.setzen(0)

    def fahren(self, links, rechts):
        """Ziel-Tempo setzen (−1 … +1). Die Motoren folgen über die Rampe in aktualisieren()."""
        self.ziel_l = max(-1.0, min(1.0, links))
        self.ziel_r = max(-1.0, min(1.0, rechts))

    def stopp(self):
        self.fahren(0, 0)

    def sofort(self):
        """Ohne Rampe aufs Ziel springen – für die Notbremse vor einem Hindernis."""
        self.ist_l, self.ist_r = self.ziel_l, self.ziel_r

    def aktualisieren(self, dt_s):
        """Regelmäßig aufrufen (z. B. alle 20 ms): bringt das Tempo langsam zum Ziel."""
        schritt = E.RAMPE_PRO_S * dt_s
        self.ist_l = _hin(self.ist_l, self.ziel_l, schritt)
        self.ist_r = _hin(self.ist_r, self.ziel_r, schritt)
        self.vl.setzen(self.ist_l)
        self.hl.setzen(self.ist_l)
        self.vr.setzen(self.ist_r)
        self.hr.setzen(self.ist_r)


def _hin(ist, ziel, schritt):
    if ziel > ist:
        return min(ziel, ist + schritt)
    return max(ziel, ist - schritt)


def joystick_zu_raedern(x, y):
    """Joystick (x = rechts positiv, y = vorwärts positiv, je −1 … +1) → Tempo links und rechts."""
    links = y + x
    rechts = y - x
    groesster = max(1.0, abs(links), abs(rechts))   # nie über 1, Verhältnis bleibt gleich
    return links / groesster, rechts / groesster
