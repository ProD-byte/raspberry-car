# Test: Encoder zählen, ohne dass die Motoren laufen.
#
# Die Motoren bleiben aus. Drehe die Räder von Hand – die Zahlen müssen sich ändern.
# Vorwärts drehen (so, wie das Auto nach vorne fahren würde) muss die Zahl größer machen.
#
# Impulse je Radumdrehung messen: Rad mit einem Strich markieren, genau 10 Umdrehungen
# vorwärts drehen, Zahl durch 10 teilen und in einstellungen.py bei IMPULSE_PRO_UMDREHUNG eintragen.
#
# Beenden: Stopp-Knopf in Thonny (oder Strg+C).

import time
from encoder import alle_encoder

encoder = alle_encoder()
namen = ("vorne_links", "vorne_rechts", "hinten_links", "hinten_rechts")
print("  ".join("%13s" % n for n in namen))
while True:
    print("  ".join("%13d" % encoder[n].stand() for n in namen), end="\r")
    time.sleep_ms(200)
