# Pico 2 W – Software

MicroPython auf dem Raspberry Pi Pico 2 W. Stufe 1: Das Auto fährt per Handy-Joystick über das eigene WLAN des Pico.

## Dateien

| Datei | Inhalt |
|---|---|
| `pins.py` | Pinbelegung (passt zu `docs/verdrahtung.md` und zum 3D-Modell) |
| `einstellungen.py` | Was man nach dem ersten Test anpasst: Drehrichtungen, Höchsttempo, Rampe, Not-Stopp-Zeit, Impulse je Radumdrehung |
| `motoren.py` | Die vier Motoren über die zwei DRV8833: Tempo −1 … +1, Anfahr-Rampe, Not-Stopp über ULT |
| `encoder.py` | Zählt die Encoder mit der PIO des Pico (kein Impuls geht verloren), Strecke in mm |
| `main.py` | Startet von selbst: WLAN „RaspberryCar“, Joystick-Seite, Not-Stopp nach 0,5 s ohne Befehl |
| `joystick.html` | Die Seite fürs Handy (läuft ohne Internet) |
| `vl53l1x.py` | Treiber für den Laser-Nahsensor VL53L1X (nach dem offiziellen ULD von ST) |
| `nahsensoren.py` | Beide Nahsensoren starten (eigene Adressen über XSHUT), messen, Hindernis-Stopp |
| `test_nahsensoren.py` | Nahsensoren prüfen – geht schon ohne Akku |
| `test_encoder.py` | Encoder prüfen und Impulse je Radumdrehung messen – Motoren bleiben aus |
| `test_motoren.py` | Jeden Motor einzeln vor und zurück, prüft Richtung und Encoder |
| `geheim_beispiel.py` | Vorlage für `geheim.py` (WLAN-Name und Passwort, kommt nicht ins Git) |

## 1. MicroPython aufspielen

1. Die aktuelle MicroPython-Firmware für den **Pico 2 W** (RP2350, nicht Pico W) von micropython.org laden (`.uf2`).
2. BOOTSEL-Taste gedrückt halten, Pico per USB anstecken. Er erscheint als Laufwerk.
3. Die `.uf2`-Datei auf das Laufwerk ziehen. Der Pico startet neu.
4. **Thonny** installieren (thonny.org), unten rechts „MicroPython (Raspberry Pi Pico)“ wählen.

## 2. Dateien übertragen

1. `geheim_beispiel.py` kopieren, die Kopie `geheim.py` nennen und ein eigenes Passwort eintragen (mindestens 8 Zeichen).
2. In Thonny alle Dateien aus diesem Ordner auf den Pico laden: Ansicht → Dateien, Dateien markieren, Rechtsklick → „Hochladen nach /“.

   Mit der Kommandozeile geht es auch:

   ```powershell
   mpremote cp pins.py einstellungen.py motoren.py encoder.py main.py joystick.html geheim.py test_motoren.py test_encoder.py :
   ```

## 3. Was ohne Akku schon geht

Die Motoren brauchen den Akku (Stufe 2). Bis er da ist, bekommt nur der Pico Strom über USB vom PC. Damit lässt sich schon prüfen:

- **Nahsensoren:** an den I²C-Bus und ihre XSHUT-Leitungen anschließen (wie in `docs/verdrahtung.md`), dann `test_nahsensoren.py`.
- **Joystick-Seite und WLAN:** `main.py` läuft auch ohne Motoren. Die Seite zeigt das Tempo, das die Motoren bekommen würden.
- **Encoder:** Motoren mit ihren Encoder-Leitungen anschließen (wie in `docs/verdrahtung.md`), die Encoder bekommen 3,3 V vom Pico. Mit `test_encoder.py` die Räder von Hand drehen.

Die Motorleitungen (OUT1–OUT4) und die Stromversorgung der DRV8833 kommen erst mit dem Akku dazu, genau nach `docs/verdrahtung.md` und `docs/stromversorgung.md` (Tests vor dem ersten Anschließen beachten). Verbindungen über Schraubklemmen, WAGO und Lötstellen – keine Jumperkabel.

## 4. Testen – in dieser Reihenfolge

1. **Nahsensoren** (geht schon ohne Akku): `test_nahsensoren.py` starten. Nach dem Start müssen am Bus 0x31 (vorne) und 0x33 (hinten) auftauchen. Hand davor halten – die Zahl wird kleiner. Hand vor den vorderen halten: ändert sich „hinten“, sind die XSHUT-Leitungen vertauscht.
2. **Encoder** (geht schon ohne Akku): `test_encoder.py` in Thonny öffnen und starten (F5). Räder von Hand drehen – alle vier Zahlen müssen sich ändern, vorwärts größer werden. Danach die Impulse je Radumdrehung messen (steht oben in der Datei).
3. **Motoren** (ab dem Akku): Auto auf den **Prüfstand** (Räder in der Luft). `test_motoren.py` starten. Jeder Motor dreht kurz vor und zurück. Dreht einer falsch herum oder zählt sein Encoder falsch, in `einstellungen.py` den Wert bei `MOTOR_UMKEHREN` bzw. `ENCODER_UMKEHREN` umdrehen – nichts umlöten.
4. **Joystick** (die Seite geht schon ohne Akku, fahren erst mit Akku): Pico neu starten (USB ab und wieder an) – `main.py` startet von selbst. Handy mit dem WLAN „RaspberryCar“ verbinden, im Browser **http://192.168.4.1** öffnen. Erst auf dem Prüfstand ausprobieren, dann auf dem Boden.

## So funktioniert es

- **Lenken wie ein Panzer:** Beide linken Räder bekommen dasselbe Tempo, beide rechten auch. Joystick nach oben = alle vorwärts, zur Seite = eine Seite schneller, ganz zur Seite = auf der Stelle drehen.
- **Rampe:** Das Tempo ändert sich höchstens um 2,5 × „voll“ pro Sekunde. Das schont Getriebe und Akku.
- **Not-Stopp:** Kommt 0,5 s kein Befehl vom Handy (WLAN weg, Seite zu, Handy gesperrt), hält das Auto an und die Treiber gehen schlafen (ULT aus). Der Knopf **STOPP** schaltet die Treiber sofort aus, bis man **WEITER** tippt.
- **Hindernis-Stopp:** Ab 50 cm vor einem Hindernis wird das Tempo in diese Richtung immer kleiner, ab 15 cm geht es gar nicht mehr weiter. Fährt das Auto dann noch, bremst es sofort, ohne Rampe. Wegdrehen auf der Stelle und Wegfahren gehen immer. Die Abstände stehen in `einstellungen.py` und werden auf der Joystick-Seite angezeigt (gelb = nah, rot = zu nah). Fehlt ein Sensor, fährt das Auto trotzdem – dort aber ohne Schutz, das meldet die Seite mit „kein Sensor“.
- **PWM:** 20 kHz (nicht hörbar). Jeder Motor hat ein eigenes PWM-Paar des Pico – deshalb hängt der Motor hinten rechts an GP14/GP15 und nicht an GP18/GP19 (die teilen sich den Kanal mit GP2/GP3).
- **Encoder:** Zählt jede steigende Flanke von Kanal A, Richtung aus Kanal B. Läuft in der PIO (Block 0), unabhängig vom Programm.

## Später
- Sensoren lesen: INA226 (Akku), BNO085 (Lage)
- Akkuspannung: unter 6,8 V warnen, unter 6,4 V abschalten (Werte stehen schon in `pins.py`)
- Status-LEDs WS2812
- Befehle vom Pi 5 über USB annehmen (Stufe 3)
