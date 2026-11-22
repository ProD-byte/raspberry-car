# Einstellungen, die man nach dem ersten Test anpasst.
# Die Pinbelegung steht in pins.py – hier nur Richtungen und Fahrverhalten.

# --- Drehrichtung ---
# Nach test_motoren.py eintragen: Dreht ein Rad bei „vorwärts“ rückwärts, hier True setzen
# (statt die Motorkabel umzulöten). Die rechten Motoren sind spiegelverkehrt eingebaut,
# deshalb sind sie am Anfang schon umgedreht – ob das stimmt, zeigt der Test.
MOTOR_UMKEHREN = {
    "vorne_links": False,
    "hinten_links": False,
    "vorne_rechts": True,
    "hinten_rechts": True,
}

# Zählt ein Encoder bei Vorwärtsfahrt rückwärts (negative Zahlen), hier True setzen.
ENCODER_UMKEHREN = {
    "vorne_links": False,
    "hinten_links": False,
    "vorne_rechts": True,
    "hinten_rechts": True,
}

# --- Fahrverhalten ---
# Höchstes Tempo als Anteil (0 … 1). Mit dem 2S-Akku (bis 8,4 V) höchstens 0,70, damit die
# 6-V-Motoren nicht mehr als etwa 6 V abbekommen.
TEMPO_MAX = 0.70

# Anfahr-Rampe: so viel darf sich das Tempo pro Sekunde höchstens ändern (1,0 = 0 auf voll in 1 s).
# Schont Getriebe und Akku und verhindert Stromspitzen.
RAMPE_PRO_S = 2.5

# Unter diesem Anteil vom Höchsttempo bleibt der Motor stehen (sonst brummt er nur)
TEMPO_MIN = 0.12

# Not-Stopp: kommt so lange kein Befehl vom Handy, halten die Motoren an (Millisekunden)
BEFEHL_TIMEOUT_MS = 500

# --- Rad und Encoder (für Strecke und Geschwindigkeit) ---
RAD_DURCHMESSER_MM = 85
# Zählimpulse je Radumdrehung (gezählt wird jede steigende Flanke von Kanal A).
# JGA25-370 mit 130 U/min: 11 Impulse je Motorumdrehung × Getriebe 1:46,8 → ca. 515.
# Mit test_encoder.py nachmessen: Rad genau 10-mal von Hand drehen,
# die Zahl durch 10 teilen und hier eintragen.
IMPULSE_PRO_UMDREHUNG = 515

# --- Nahsensoren und Hindernis-Stopp ---
# Die Laser-Nahsensoren VL53L1X vorne und hinten bremsen das Auto, bevor es anstößt.
# Gemessen wird ab dem Sensor (er sitzt innen an der Stirnwand der Wanne).
HINDERNIS_STOPP_AN = True
HINDERNIS_STOPP_MM = 150       # näher: in diese Richtung geht es nicht weiter (Notbremse)
HINDERNIS_LANGSAM_MM = 500     # ab hier wird es langsam weniger Tempo, bis zum Stopp-Abstand
NAH_MESSABSTAND_MS = 60        # alle 60 ms ein neuer Messwert je Sensor

# --- WLAN des Autos ---
# Der Pico macht ein eigenes WLAN auf. Name und Passwort stehen in geheim.py
# (nicht im Git, Vorlage: geheim_beispiel.py).
