# Pinbelegung des Pico 2 W im Raspberry Car
# Muss zu docs/verdrahtung.md und zum 3D-Modell passen – bei Änderungen alle drei anpassen.
# Angaben: GPIO-Nummer (GPn), in Klammern die Pin-Nummer am Pico / auf dem Freenove-Board.

# --- Motortreiber DRV8833 links (Motor vorne links = A, hinten links = B) ---
DRV_L_IN1 = 2   # GP2  (Pin 4)  -> Motor vorne links
DRV_L_IN2 = 3   # GP3  (Pin 5)  -> Motor vorne links
DRV_L_IN3 = 4   # GP4  (Pin 6)  -> Motor hinten links
DRV_L_IN4 = 5   # GP5  (Pin 7)  -> Motor hinten links

# --- Motortreiber DRV8833 rechts (Motor vorne rechts = A, hinten rechts = B) ---
DRV_R_IN1 = 16  # GP16 (Pin 21) -> Motor vorne rechts
DRV_R_IN2 = 17  # GP17 (Pin 22) -> Motor vorne rechts
DRV_R_IN3 = 18  # GP18 (Pin 24) -> Motor hinten rechts
DRV_R_IN4 = 19  # GP19 (Pin 25) -> Motor hinten rechts

# Beide Treiber an/aus: Anschluss ULT am Modul (= nSLEEP des DRV8833). LOW = Motoren aus = Not-Stopp.
# Nicht EEP – das ist auf diesem Modul nur der Fehler-Ausgang. Lötbrücke J1 offen lassen.
DRV_ENABLE = 22  # GP22 (Pin 29)

# --- Encoder (Kanal A, Kanal B) – A und B liegen immer direkt nebeneinander (für PIO) ---
ENC_VORNE_LINKS = (6, 7)     # GP6/GP7   (Pin 9/10)
ENC_HINTEN_LINKS = (8, 9)    # GP8/GP9   (Pin 11/12)
ENC_VORNE_RECHTS = (20, 21)  # GP20/GP21 (Pin 26/27)
ENC_HINTEN_RECHTS = (26, 27) # GP26/GP27 (Pin 31/32)

# --- I²C-Sensorbus (I2C1): BNO085, INA226, 4× VL53L1X ---
I2C_ID = 1
I2C_SDA = 10  # GP10 (Pin 14)
I2C_SCL = 11  # GP11 (Pin 15)

# XSHUT der Nahsensoren: beim Start einzeln einschalten, damit jeder eine eigene Adresse bekommt
TOF_XSHUT = {
    "vorne_links": 12,   # GP12 (Pin 16)
    "vorne": 13,         # GP13 (Pin 17)
    "vorne_rechts": 14,  # GP14 (Pin 19)
    "hinten": 15,        # GP15 (Pin 20)
}
TOF_ADRESSEN = {"vorne_links": 0x30, "vorne": 0x31, "vorne_rechts": 0x32, "hinten": 0x33}

# Feste I²C-Adressen
ADR_INA226 = 0x40
ADR_BNO085 = 0x4A

# --- Status-LEDs WS2812 (4 Stück) ---
LED_DATA = 28  # GP28 (Pin 34)
LED_ANZAHL = 4

# --- Grenzwerte ---
# 6-V-Motoren am 2S-Akku (bis 8,4 V): PWM begrenzen, damit die Motoren nicht überlastet werden
MOTOR_PWM_MAX = 0.70
PWM_FREQ = 20_000  # 20 kHz, nicht hörbar

# Akku (2S): unter diesen Spannungen warnen bzw. abschalten
AKKU_WARNUNG_V = 6.8
AKKU_AUS_V = 6.4
