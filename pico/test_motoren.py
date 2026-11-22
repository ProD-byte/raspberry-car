# Test: jeden Motor einzeln kurz vorwärts und rückwärts drehen.
#
# VORHER: Auto auf den Prüfstand stellen oder so hinlegen, dass sich kein Rad den Tisch berührt!
# Start in Thonny (Datei öffnen, F5) – die Ausgabe erscheint unten in der Kommandozeile.
#
# Was du prüfst:
#   * Dreht sich der richtige Motor?  (Reihenfolge: vorne links, vorne rechts, hinten links, hinten rechts)
#   * Dreht er bei „vorwärts“ so, dass das Auto nach vorne fahren würde?
#     Wenn nicht: in einstellungen.py bei MOTOR_UMKEHREN den Wert für diesen Motor umdrehen.
#   * Zählt sein Encoder bei „vorwärts“ positiv?
#     Wenn nicht: bei ENCODER_UMKEHREN umdrehen. Zählt er gar nicht (0): Encoder-Kabel prüfen.

import time
from motoren import Antrieb
from encoder import alle_encoder

TEMPO = 0.5       # halbes Tempo reicht zum Prüfen
DAUER_MS = 1500

antrieb = Antrieb()
encoder = alle_encoder()

try:
    antrieb.einschalten()
    for motor in antrieb.alle:
        enc = encoder[motor.name]
        for richtung, wort in ((1, "vorwärts"), (-1, "rückwärts")):
            enc.nullen()
            print("%-14s %-10s …" % (motor.name, wort), end=" ")
            motor.setzen(richtung * TEMPO)
            time.sleep_ms(DAUER_MS)
            motor.setzen(0)
            time.sleep_ms(500)               # ausrollen lassen
            n = enc.stand()
            ok = (n > 0) if richtung > 0 else (n < 0)
            print("Encoder %6d  %s" % (n, "ok" if ok else ("zählt nicht!" if n == 0 else "falsche Richtung!")))
        time.sleep_ms(500)
finally:
    antrieb.ausschalten()
    print("Fertig, Motoren aus.")
