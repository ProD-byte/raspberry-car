# Pinbelegung des Pico 2 W im Raspberry Car
# Muss zu docs/verdrahtung.md und zum 3D-Modell passen – bei Änderungen alle drei anpassen.
# Angaben: GPIO-Nummer (GPn), in Klammern die Pin-Nummer am Pico / auf dem Freenove-Board.

# --- Motortreiber DRV8833 vorne (Motorzone vorne): OUT1/OUT2 = Motor vorne links, OUT3/OUT4 = vorne rechts ---
DRV_V_IN1 = 2   # GP2  (Pin 4)  -> Motor vorne links
DRV_V_IN2 = 3   # GP3  (Pin 5)  -> Motor vorne links
DRV_V_IN3 = 16  # GP16 (Pin 21) -> Motor vorne rechts
DRV_V_IN4 = 17  # GP17 (Pin 22) -> Motor vorne rechts

# --- Motortreiber DRV8833 hinten (Motorzone hinten): OUT1/OUT2 = Motor hinten links, OUT3/OUT4 = hinten rechts ---
DRV_H_IN1 = 4   # GP4  (Pin 6)  -> Motor hinten links
DRV_H_IN2 = 5   # GP5  (Pin 7)  -> Motor hinten links
DRV_H_IN3 = 14  # GP14 (Pin 19) -> Motor hinten rechts
DRV_H_IN4 = 15  # GP15 (Pin 20) -> Motor hinten rechts
# Wichtig: Je zwei GPIOs teilen sich einen PWM-Ausgang (GP2 und GP18 = Kanal 1A, GP3 und GP19 = 1B …).
# Jeder Motor hat deshalb ein eigenes PWM-Paar: Kanal 1 (GP2/3), 2 (GP4/5), 0 (GP16/17), 7 (GP14/15).

# Beide Treiber an/aus: Anschluss ULT am Modul (= nSLEEP des DRV8833). LOW = Motoren aus = Not-Stopp.
# Nicht EEP – das ist auf diesem Modul nur der Fehler-Ausgang. Lötbrücke J1 offen lassen.
DRV_ENABLE = 22  # GP22 (Pin 29)

# --- Encoder (Kanal A, Kanal B) – A und B liegen immer direkt nebeneinander (für PIO) ---
ENC_VORNE_LINKS = (6, 7)     # GP6/GP7   (Pin 9/10)
ENC_HINTEN_LINKS = (8, 9)    # GP8/GP9   (Pin 11/12)
ENC_VORNE_RECHTS = (20, 21)  # GP20/GP21 (Pin 26/27)
ENC_HINTEN_RECHTS = (26, 27) # GP26/GP27 (Pin 31/32)

# --- I²C-Sensorbus (I2C1): BNO085, INA226, 2× VL53L1X ---
I2C_ID = 1
I2C_SDA = 10  # GP10 (Pin 14)
I2C_SCL = 11  # GP11 (Pin 15)

# XSHUT der Nahsensoren: beim Start einzeln einschalten, damit jeder eine eigene Adresse bekommt
TOF_XSHUT = {
    "vorne": 13,         # GP13 (Pin 17)
    "hinten": 12,        # GP12 (Pin 16)
}
TOF_ADRESSEN = {"vorne": 0x31, "hinten": 0x33}
# GP18 (Pin 24) und GP19 (Pin 25) sind frei – nicht für PWM nutzen, sie teilen sich den Kanal mit GP2/GP3

# Feste I²C-Adressen
ADR_INA226 = 0x40
ADR_BNO085 = 0x4A

# --- LEDs WS2812B: eine Kette an GP28 ---
# Frontlicht (Leiste mit 8 LEDs vorne) -> Rücklicht (Leiste mit 8 LEDs hinten). Den Status zeigt das runde Display.
LED_DATA = 28  # GP28 (Pin 34)
LED_ANZAHL = 16
LED_FRONT = range(0, 8)      # Nummern in der Kette
LED_HECK = range(8, 16)
LED_HELL_MAX = 0.35  # alle 16 LEDs voll weiß ziehen ca. 1 A aus dem MP1584 – in der Software begrenzen

# --- Grenzwerte ---
# 6-V-Motoren am 2S-Akku (bis 8,4 V): PWM begrenzen, damit die Motoren nicht überlastet werden
MOTOR_PWM_MAX = 0.70
PWM_FREQ = 20_000  # 20 kHz, nicht hörbar

# Akku (2S): unter diesen Spannungen warnen bzw. abschalten
AKKU_WARNUNG_V = 6.8
AKKU_AUS_V = 6.4
