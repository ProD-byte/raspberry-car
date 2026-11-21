# Pico 2 W – Software

MicroPython auf dem Raspberry Pi Pico 2 W.

## Aufgaben
- Motoren über die beiden DRV8833 steuern (PWM)
- Encoder zählen (Geschwindigkeit, Strecke)
- Sensoren lesen: INA226 (Akku), BNO085 (Lage), 2× VL53L1X (Nahbereich vorne und hinten)
- Joystick-Webseite per WLAN (ab Stufe 1, bevor der Pi da ist)
- Später: Befehle vom Pi über USB annehmen und Messwerte zurückschicken
- Not-Stopp: Motoren aus, wenn keine Befehle mehr kommen

## Stand
- `pins.py` – Pinbelegung (fertig, passt zu `docs/verdrahtung.md`)
- Als Nächstes: MicroPython aufspielen, LED-Test, WLAN-Test, dann Motortest mit einem Motor

## MicroPython aufspielen
1. Aktuelle MicroPython-Firmware für **Pico 2 W** (RP2350) von micropython.org laden (`.uf2`).
2. BOOTSEL-Taste gedrückt halten, Pico per USB anstecken – er erscheint als Laufwerk.
3. Die `.uf2`-Datei auf das Laufwerk ziehen. Der Pico startet neu.
4. Dateien mit Thonny oder `mpremote` übertragen.
