# Verdrahtungsplan

Verbindlicher Plan: Jede Leitung von Anschluss zu Anschluss. Das 3D-Modell (`modell/raspberry-car-3d.html`) ist aus derselben Liste erzeugt – tippe dort auf ein Kabel, um es zu sehen.
Die Pinbelegung als Code steht in `pico/pins.py`. **Bei Änderungen alle drei Stellen gemeinsam ändern.**

Hinweise:
- Jedes Kabel in einer Schraubklemme bekommt eine Aderendhülse, zwei Kabel in einem Punkt eine Zwillings-Aderendhülse.
- Zwischen MP1584 OUT+ und Pico VSYS sitzt eine Schottky-Diode 1N5819 (Ring zur Pico-Seite).
- Encoder-Kabelfarben unterscheiden sich je nach Händler – vor dem Anschließen mit dem Datenblatt des Motors vergleichen.
- Kabel zwischen den Ebenen laufen durch die Durchbrüche A (rechts), B (links), C (hinten) in den Platten.
- Pi 5: `usb_max_current_enable=1` in `config.txt`.
- **DRV8833-Modul** (MakerMind, roboter-bausatz.de RBS12954, schwarz, 16 × 18,5 mm): Die Beschriftung steht auf der **Unterseite**. Reihe zum Pico: IN4, IN3, GND, VCC, IN2, IN1 – gegenüber Reihe zu den Motoren: EEP, OUT1, OUT2, OUT3, OUT4, ULT. **ULT** ist der Schlaf-Eingang (LOW = Motoren aus) → daran hängt der Not-Stopp. **EEP** ist nur ein Fehler-Ausgang und bleibt frei. Die Lötbrücke **J1 („en/sleep“) offen lassen**, sonst ist ULT fest auf VCC und der Not-Stopp wirkt nicht. Das Modul hat keine Befestigungslöcher: mit doppelseitigem Schaumklebeband auf die Platte, Kabel direkt in die Lötaugen löten (keine Stiftleiste).

### Akku & Schutz

| Farbe | Von | Nach | Zweck |
|---|---|---|---|
| schwarz | Akku Gruppe 1 Minus | BMS B− | Minus des Akkus |
| rot | Akku Gruppe 1 Plus | Akku Gruppe 2 Minus | Reihenverbindung der beiden Zellengruppen |
| gelb | Akku Gruppe 2 Minus | BMS BM | Mittelabgriff, damit das BMS jede Gruppe einzeln überwacht |
| rot | Akku Gruppe 2 Plus | BMS B+ | Plus des Akkus |
| schwarz | BMS P− | Ladeboard GND | Ladestrom Minus |
| rot | BMS P+ | Ladeboard BAT | Ladestrom Plus |
| rot | BMS P+ | Sicherung Eingang | Plus zur Sicherung |
| rot | Sicherung Ausgang | Hauptschalter Anschluss 1 | Plus zum Hauptschalter |
| rot | Hauptschalter Anschluss 2 | INA226 VIN+ | Geschaltetes Plus durch den Strommesser |
| rot | INA226 VIN− | Verteiler Plus Platz 1 | Plus in den Verteiler |
| schwarz | BMS P− | Verteiler Minus Platz 1 | Masse in den Verteiler |
| rot | INA226 VBS | INA226 VIN− | Spannungsmessung des INA226 |

### Stromverteilung

| Farbe | Von | Nach | Zweck |
|---|---|---|---|
| rot | Verteiler Plus Platz 2 | DRV8833 vorne VCC | Motorstrom Treiber vorne |
| schwarz | Verteiler Minus Platz 2 | DRV8833 vorne GND | Masse Treiber vorne |
| rot | Verteiler Plus Platz 3 | DRV8833 hinten VCC | Motorstrom Treiber hinten |
| schwarz | Verteiler Minus Platz 3 | DRV8833 hinten GND | Masse Treiber hinten |
| rot | Verteiler Plus Platz 4 | MP1584 IN+ | Eingang 5-V-Wandler für den Pico |
| schwarz | Verteiler Minus Platz 4 | MP1584 IN− | Masse 5-V-Wandler |
| rot | MP1584 OUT+ | Pico VSYS (Pin 39) | 5 V an VSYS – mit Schottky-Diode 1N5819 in der Leitung (Ring zur Pico-Seite) |
| schwarz | MP1584 OUT− | Pico GND (Pin 38) | Masse Pico |
| rot | Verteiler Plus Platz 5 | Pololu VIN | Eingang 5-V-Wandler für den Pi |
| schwarz | Verteiler Minus Platz 5 | Pololu GND | Masse Pololu |
| rot | Pololu VOUT | Pi 5 USB-C (Strom) | 5 V in den Pi (USB-C-Stecker zum Anlöten) |
| schwarz | Pololu GND | Pi 5 USB-C (Strom) | Masse in den Pi |

### Motor vorne links

| Farbe | Von | Nach | Zweck |
|---|---|---|---|
| rot | Motor vorne links M1 | DRV8833 vorne OUT1 | Motorstrom |
| weiß | Motor vorne links M2 | DRV8833 vorne OUT2 | Motorstrom |
| schwarz | Motor vorne links GND | Pico GND (Pin 8) | Encoder Masse |
| blau | Motor vorne links VCC | 3,3-V-Verteiler vorne Platz 2 | Encoder 3,3 V |
| gelb | Motor vorne links A | Pico GP6 (Pin 9) | Encoder Kanal A |
| grün | Motor vorne links B | Pico GP7 (Pin 10) | Encoder Kanal B |

### Motor hinten links

| Farbe | Von | Nach | Zweck |
|---|---|---|---|
| rot | Motor hinten links M1 | DRV8833 hinten OUT1 | Motorstrom |
| weiß | Motor hinten links M2 | DRV8833 hinten OUT2 | Motorstrom |
| schwarz | Motor hinten links GND | Pico GND (Pin 3) | Encoder Masse |
| blau | Motor hinten links VCC | 3,3-V-Verteiler hinten Platz 2 | Encoder 3,3 V |
| gelb | Motor hinten links A | Pico GP8 (Pin 11) | Encoder Kanal A |
| grün | Motor hinten links B | Pico GP9 (Pin 12) | Encoder Kanal B |

### Motor vorne rechts

| Farbe | Von | Nach | Zweck |
|---|---|---|---|
| rot | Motor vorne rechts M1 | DRV8833 vorne OUT3 | Motorstrom |
| weiß | Motor vorne rechts M2 | DRV8833 vorne OUT4 | Motorstrom |
| schwarz | Motor vorne rechts GND | Pico GND (Pin 28) | Encoder Masse |
| blau | Motor vorne rechts VCC | 3,3-V-Verteiler vorne Platz 3 | Encoder 3,3 V |
| gelb | Motor vorne rechts A | Pico GP20 (Pin 26) | Encoder Kanal A |
| grün | Motor vorne rechts B | Pico GP21 (Pin 27) | Encoder Kanal B |

### Motor hinten rechts

| Farbe | Von | Nach | Zweck |
|---|---|---|---|
| rot | Motor hinten rechts M1 | DRV8833 hinten OUT3 | Motorstrom |
| weiß | Motor hinten rechts M2 | DRV8833 hinten OUT4 | Motorstrom |
| schwarz | Motor hinten rechts GND | Pico GND (Pin 33) | Encoder Masse |
| blau | Motor hinten rechts VCC | 3,3-V-Verteiler hinten Platz 3 | Encoder 3,3 V |
| gelb | Motor hinten rechts A | Pico GP26 (Pin 31) | Encoder Kanal A |
| grün | Motor hinten rechts B | Pico GP27 (Pin 32) | Encoder Kanal B |

### Steuerleitungen Motortreiber

Jeder Motor braucht ein **eigenes PWM-Paar** des Pico: Je zwei GPIOs teilen sich einen PWM-Ausgang (GP2 und GP18 sind beide Kanal 1A, GP3 und GP19 beide 1B usw.). Deshalb hängt der Motor hinten rechts an GP14/GP15 (Kanal 7) und nicht an GP18/GP19 – sonst liefen vorne links und hinten rechts immer gleich schnell.

| Farbe | Von | Nach | Zweck |
|---|---|---|---|
| orange | Pico GP2 (Pin 4) | DRV8833 vorne IN1 | PWM IN1 Treiber vorne (Motor vorne links) |
| gelb | Pico GP3 (Pin 5) | DRV8833 vorne IN2 | PWM IN2 Treiber vorne (Motor vorne links) |
| orange | Pico GP4 (Pin 6) | DRV8833 hinten IN1 | PWM IN1 Treiber hinten (Motor hinten links) |
| gelb | Pico GP5 (Pin 7) | DRV8833 hinten IN2 | PWM IN2 Treiber hinten (Motor hinten links) |
| grün | Pico GP16 (Pin 21) | DRV8833 vorne IN3 | PWM IN3 Treiber vorne (Motor vorne rechts) |
| blau | Pico GP17 (Pin 22) | DRV8833 vorne IN4 | PWM IN4 Treiber vorne (Motor vorne rechts) |
| grün | Pico GP14 (Pin 19) | DRV8833 hinten IN3 | PWM IN3 Treiber hinten (Motor hinten rechts) |
| blau | Pico GP15 (Pin 20) | DRV8833 hinten IN4 | PWM IN4 Treiber hinten (Motor hinten rechts) |
| violett | Pico GP22 (Pin 29) | DRV8833 vorne ULT | Treiber an/aus (Not-Stopp), ULT = Schlaf-Eingang |
| violett | DRV8833 vorne ULT | DRV8833 hinten ULT | Treiber an/aus, weiter zum hinteren Treiber |

### 3,3 V für Sensoren

| Farbe | Von | Nach | Zweck |
|---|---|---|---|
| orange | Pico 3V3 (Pin 36) | 3,3-V-Verteiler vorne Platz 1 | 3,3 V vom Pico in Verteiler vorne |
| orange | 3,3-V-Verteiler vorne Platz 5 | 3,3-V-Verteiler hinten Platz 1 | Brücke zu Verteiler hinten |
| orange | 3,3-V-Verteiler hinten Platz 4 | BNO085 VIN | Versorgung BNO085 |
| orange | 3,3-V-Verteiler hinten Platz 5 | INA226 VCC | Versorgung INA226 |

### Sensorbus I²C

| Farbe | Von | Nach | Zweck |
|---|---|---|---|
| blau | Pico GP10 (Pin 14) | BNO085 SDA | I²C SDA (GP10) |
| gelb | Pico GP11 (Pin 15) | BNO085 SCL | I²C SCL (GP11) |
| schwarz | Pico GND (Pin 18) | BNO085 GND | Masse Sensoren |
| blau | BNO085 SDA | INA226 SDA | I²C SDA weiter zum INA226 |
| gelb | BNO085 SCL | INA226 SCL | I²C SCL weiter zum INA226 |
| schwarz | Pico GND (Pin 23) | INA226 GND | Masse INA226 |
| orange | INA226 VCC | VL53L1X hinten VIN | 3,3 V zum hinteren Nahsensor (angelötet) |
| schwarz | INA226 GND | VL53L1X hinten GND | Masse zum hinteren Nahsensor (angelötet) |
| blau | INA226 SDA | VL53L1X hinten SDA | I²C SDA zum hinteren Nahsensor (angelötet) |
| gelb | INA226 SCL | VL53L1X hinten SCL | I²C SCL zum hinteren Nahsensor (angelötet) |
| orange | VL53L1X hinten VIN | VL53L1X vorne VIN | 3,3 V weiter zum vorderen Nahsensor (angelötet) |
| schwarz | VL53L1X hinten GND | VL53L1X vorne GND | Masse weiter zum vorderen Nahsensor (angelötet) |
| blau | VL53L1X hinten SDA | VL53L1X vorne SDA | I²C SDA weiter zum vorderen Nahsensor (angelötet) |
| gelb | VL53L1X hinten SCL | VL53L1X vorne SCL | I²C SCL weiter zum vorderen Nahsensor (angelötet) |
| violett | Pico GP13 (Pin 17) | VL53L1X vorne XSHUT | XSHUT: schaltet den Sensor beim Start einzeln an, damit jeder eine eigene Adresse bekommt |
| violett | Pico GP12 (Pin 16) | VL53L1X hinten XSHUT | XSHUT: schaltet den Sensor beim Start einzeln an, damit jeder eine eigene Adresse bekommt |

### Front- und Rücklicht

Zwei WS2812B-Leisten mit je 8 LEDs unten in der Vorder- und Rückwand der Haube, eine Kette an GP28 (Nummern 0–7 vorne,
8–15 hinten). Status-LEDs gibt es nicht mehr – den Zustand zeigt das runde Display. Alle Leitungen angelötet, vom Deck durch
Durchbruch A nach oben und entlang des Dachs mit Klebesockeln geführt. Zusammen bis ca. 1 A bei voll Weiß – die Software begrenzt die Helligkeit (`LED_HELL_MAX` in `pico/pins.py`).

| Farbe | Von | Nach | Zweck |
|---|---|---|---|
| grün | Pico GP28 (Pin 34) | Frontlicht DIN | Daten (GP28) |
| rot | MP1584 OUT+ | Frontlicht 5V | 5 V für die Lichter |
| schwarz | Pico GND (Pin 13) | Frontlicht GND | Masse Lichter |
| grün | Frontlicht DOUT | Rücklicht DIN | Daten weiter zum Rücklicht |
| rot | Frontlicht 5V (Ende) | Rücklicht 5V | 5 V weiter |
| schwarz | Frontlicht GND (Ende) | Rücklicht GND | Masse weiter |

### USB & Antennen

Alle vier USB-Buchsen des Pi 5 sind belegt. Über USB gibt der Pi zusammen nur **0,6 A** ab, solange er nicht weiß, dass sein Netzteil 5 A kann – beim angelöteten USB-C-Stecker vom Pololu weiß er das nicht. Deshalb in Stufe 3 einstellen: `usb_max_current_enable=1` in `/boot/firmware/config.txt` und `PSU_MAX_CURRENT=5000` im EEPROM (`sudo rpi-eeprom-config -e`). Danach einmal den Gesamtstrom am Pololu messen (Pi, AI HAT+, 4G, LiDAR und Display zusammen).

| Farbe | Von | Nach | Zweck |
|---|---|---|---|
| grau | Pico Micro-USB | Pi 5 USB 2.0 unten | Pico ↔ Pi: Befehle und Messwerte |
| schwarz (STEMMA-QT) | LiDAR-Anschluss | LiDAR-Adapter Eingang | LiDAR-Daten (4-polig) |
| grau | LiDAR-Adapter USB | Pi 5 USB 2.0 oben | LiDAR-Daten zum Pi |
| grau | 4G-Modul USB | Pi 5 USB 3.0 unten | Mobilfunk und GPS zum Pi |
| grau | Status-Display USB-C | Pi 5 USB 3.0 oben | Status-Display: Strom, Touch, Mikrofon und Lautsprecher (USB-C auf USB-A) |
| schwarz (STEMMA-QT) | GPS-Antenne | 4G-Modul GNSS | Antennenkabel GPS |
| schwarz (STEMMA-QT) | LTE-Antenne links | 4G-Modul MAIN | Antennenkabel LTE Haupt |
| schwarz (STEMMA-QT) | LTE-Antenne rechts | 4G-Modul AUX | Antennenkabel LTE Neben |

### Flachbandkabel

| Art | Von | Nach | Zweck |
|---|---|---|---|
| Flachband 22→15 Pin | Camera Module 3 | Pi 5 CAM/DISP 0 | Kamerabild |
| Flachband (liegt bei) | AI HAT+ PCIe | Pi 5 PCIe | KI-Beschleuniger |

## Belegung am Pico (Klemmen auf dem Freenove-Board)

| Pin | Name | Angeschlossen an |
|---|---|---|
| 3 | GND | Motor hinten links GND |
| 4 | GP2 | DRV8833 vorne IN1 |
| 5 | GP3 | DRV8833 vorne IN2 |
| 6 | GP4 | DRV8833 hinten IN1 |
| 7 | GP5 | DRV8833 hinten IN2 |
| 8 | GND | Motor vorne links GND |
| 9 | GP6 | Motor vorne links A |
| 10 | GP7 | Motor vorne links B |
| 11 | GP8 | Motor hinten links A |
| 12 | GP9 | Motor hinten links B |
| 13 | GND | Frontlicht GND |
| 14 | GP10 | BNO085 SDA |
| 15 | GP11 | BNO085 SCL |
| 16 | GP12 | VL53L1X hinten XSHUT |
| 17 | GP13 | VL53L1X vorne XSHUT |
| 18 | GND | BNO085 GND |
| 19 | GP14 | DRV8833 hinten IN3 |
| 20 | GP15 | DRV8833 hinten IN4 |
| 21 | GP16 | DRV8833 vorne IN3 |
| 22 | GP17 | DRV8833 vorne IN4 |
| 23 | GND | INA226 GND |
| 24 | GP18 | frei (teilt PWM-Kanal mit GP2) |
| 25 | GP19 | frei (teilt PWM-Kanal mit GP3) |
| 26 | GP20 | Motor vorne rechts A |
| 27 | GP21 | Motor vorne rechts B |
| 28 | GND | Motor vorne rechts GND |
| 29 | GP22 | DRV8833 vorne ULT |
| 31 | GP26 | Motor hinten rechts A |
| 32 | GP27 | Motor hinten rechts B |
| 33 | GND | Motor hinten rechts GND |
| 34 | GP28 | Frontlicht DIN |
| 36 | 3V3 | 3,3-V-Verteiler vorne Platz 1 |
| 38 | GND | MP1584 OUT− |
| 39 | VSYS | MP1584 OUT+ |