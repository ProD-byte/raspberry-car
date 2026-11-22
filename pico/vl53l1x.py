# Treiber für den Laser-Abstandssensor VL53L1X (bis ca. 4 m).
#
# Nachgebaut nach dem offiziellen „Ultra Lite Driver“ (ULD) von ST: dieselben Register und
# dieselbe Start-Einstellung (91 Bytes ab Register 0x2D). Der Sensor misst danach von selbst
# immer wieder; wir fragen nur nach, ob ein neuer Messwert da ist, und holen ihn ab.
#
# Der Sensor hat 16-Bit-Registeradressen, deshalb überall addrsize=16.

import time

STANDARD_ADRESSE = 0x29     # nach dem Einschalten hat jeder VL53L1X diese Adresse
KENNUNG = 0xEACC            # steht in Register 0x010F – so erkennen wir einen echten VL53L1X

# Start-Einstellung aus dem ULD von ST (Register 0x2D … 0x87): Langstrecken-Modus,
# Messzeit ca. 50 ms, Interrupt „neuer Messwert“, Messung noch aus.
_START = bytes((
    0x00, 0x00, 0x00, 0x01, 0x02, 0x00, 0x02, 0x08, 0x00, 0x08, 0x10, 0x01, 0x01, 0x00, 0x00, 0x00,  # 0x2D
    0x00, 0xFF, 0x00, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x0B, 0x00, 0x00, 0x02, 0x0A, 0x21,  # 0x3D
    0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0xC8, 0x00, 0x00, 0x38, 0xFF, 0x01, 0x00, 0x08, 0x00,  # 0x4D
    0x00, 0x01, 0xCC, 0x0F, 0x01, 0xF1, 0x0D, 0x01, 0x68, 0x00, 0x80, 0x08, 0xB8, 0x00, 0x00, 0x00,  # 0x5D
    0x00, 0x0F, 0x89, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x0F, 0x0D, 0x0E, 0x0E, 0x00,  # 0x6D
    0x00, 0x02, 0xC7, 0xFF, 0x9B, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00,                                # 0x7D … 0x87
))

# Messstatus des Sensors → 0 bedeutet „gültig“ (Tabelle aus dem ULD)
_STATUS = (255, 255, 255, 5, 2, 4, 1, 7, 3, 0, 255, 255, 9, 13, 255, 255, 255, 255, 10, 6, 255, 255, 11, 12)

# Register
_ADRESSE = 0x0001
_VHV_TIMEOUT = 0x0008
_VHV_START = 0x000B
_SYSTEM_STATUS = 0x00E5
_KENNUNG = 0x010F
_GPIO_HV_MUX = 0x0030
_GPIO_STATUS = 0x0031
_INTERRUPT_LOESCHEN = 0x0086
_MESSUNG = 0x0087
_MESSABSTAND = 0x006C
_TAKT = 0x00DE
_ERGEBNIS_STATUS = 0x0089
_ERGEBNIS_MM = 0x0096


class VL53L1X:
    def __init__(self, i2c, adresse=STANDARD_ADRESSE):
        self.i2c = i2c
        self.adr = adresse

    # --- Register lesen und schreiben ---
    def _w8(self, reg, wert):
        self.i2c.writeto_mem(self.adr, reg, bytes((wert & 0xFF,)), addrsize=16)

    def _w32(self, reg, wert):
        self.i2c.writeto_mem(self.adr, reg, wert.to_bytes(4, "big"), addrsize=16)

    def _r8(self, reg):
        return self.i2c.readfrom_mem(self.adr, reg, 1, addrsize=16)[0]

    def _r16(self, reg):
        b = self.i2c.readfrom_mem(self.adr, reg, 2, addrsize=16)
        return (b[0] << 8) | b[1]

    # --- Einrichten ---
    def warten_bis_wach(self, zeit_ms=500):
        """Nach dem Einschalten (XSHUT an) braucht der Sensor einen Moment."""
        ende = time.ticks_add(time.ticks_ms(), zeit_ms)
        while time.ticks_diff(ende, time.ticks_ms()) > 0:
            try:
                if self._r8(_SYSTEM_STATUS) & 0x01:
                    return
            except OSError:
                pass                       # antwortet noch nicht
            time.sleep_ms(2)
        raise OSError("VL53L1X an 0x%02X wacht nicht auf" % self.adr)

    def adresse_setzen(self, neu):
        """Eigene I²C-Adresse geben (gilt, bis der Sensor wieder ausgeschaltet wird)."""
        self._w8(_ADRESSE, neu & 0x7F)
        self.adr = neu

    def starten(self, messabstand_ms=60):
        """Sensor einrichten und Dauermessung starten. Ein neuer Wert alle messabstand_ms."""
        if self._r16(_KENNUNG) != KENNUNG:
            raise OSError("an 0x%02X ist kein VL53L1X (vielleicht ein VL53L0X?)" % self.adr)
        self.i2c.writeto_mem(self.adr, 0x2D, _START, addrsize=16)
        # Eine erste Messung machen und verwerfen (so steht es im ULD)
        self._w8(_MESSUNG, 0x40)
        ende = time.ticks_add(time.ticks_ms(), 500)
        while not self.daten_bereit():
            if time.ticks_diff(ende, time.ticks_ms()) <= 0:
                raise OSError("VL53L1X an 0x%02X misst nicht" % self.adr)
            time.sleep_ms(2)
        self._w8(_INTERRUPT_LOESCHEN, 0x01)
        self._w8(_MESSUNG, 0x00)
        self._w8(_VHV_TIMEOUT, 0x09)
        self._w8(_VHV_START, 0x00)
        # Abstand zwischen zwei Messungen (der Sensor rechnet in eigenen Takten)
        takt = self._r16(_TAKT) & 0x3FF
        self._w32(_MESSABSTAND, int(takt * messabstand_ms * 1.075))
        self._w8(_MESSUNG, 0x40)       # Dauermessung an

    def stoppen(self):
        self._w8(_MESSUNG, 0x00)

    # --- Messen ---
    def daten_bereit(self):
        aktiv_high = not (self._r8(_GPIO_HV_MUX) & 0x10)
        return (self._r8(_GPIO_STATUS) & 0x01) == (1 if aktiv_high else 0)

    def lesen(self):
        """Abstand in mm, oder None, wenn nichts Gültiges gemessen wurde (z. B. nichts in Reichweite)."""
        status = self._r8(_ERGEBNIS_STATUS) & 0x1F
        mm = self._r16(_ERGEBNIS_MM)
        self._w8(_INTERRUPT_LOESCHEN, 0x01)       # bereit für den nächsten Wert
        if status < len(_STATUS) and _STATUS[status] == 0:
            return mm
        return None
