# Echte CAD-Modelle für das 3D-Modell

Die `.glb`-Dateien sind aus den STEP-Dateien der Hersteller umgewandelt (Maße 1:1 in mm, Farben aus der STEP-Datei).
`teile.js` enthält dieselben Dateien als Base64, damit `raspberry-car-3d.html` auch per Doppelklick (ohne Webserver) die echten Modelle zeigt.
Fehlt `teile.js` oder ist man offline, zeigt das Modell automatisch die einfachen Ersatzteile.

| Datei | Bauteil | Quelle | Lizenz / Hinweis |
|---|---|---|---|
| `neopixel_stick.glb` | WS2812B-Leiste mit 8 LEDs (Front- und Rücklicht) | Adafruit CAD Parts, „1426 8x NeoPixel Stick“: https://github.com/adafruit/Adafruit_CAD_Parts/tree/main/1426%208x%20NeoPixel%20Stick – Datei `1426 8x NeoPixel Stick.step` | MIT (Adafruit Industries). 50,8 × 10,16 × 2,6 mm, ein Körper ohne Farben; im Modell dunkel eingefärbt, die LED-Flächen leuchten darüber. Umgewandelt mit `step2glb.py … 0.05` und `merge_glb.py`. Die günstigen 8-Bit-Leisten (z. B. Joycabin) sind Nachbauten mit gleicher Anordnung. |
| `pi5.glb` | Raspberry Pi 5 | STEP-Datei „rpi-5 3D STEP – No Graphics small file“ von Raspberry Pi: https://pip.raspberrypi.com/categories/892-raspberry-pi-5 (RP-010083-CA) | MIT (Lizenzdatei liegt bei). Umgewandelt mit `step2glb.py … 0.4 0.9` und `merge_glb.py … --min 0.8 --max 15000` (Lötkugeln unter Chips weggelassen, große Teile vereinfacht), damit es im Browser flüssig läuft: 1,3 MB statt 77 MB. |
| `bno085.glb` | Adafruit BNO085 (4754) | Offizielles Adafruit-CAD: https://github.com/adafruit/Adafruit_CAD_Parts (`4754 BNO085 STEMMA QT.step`) | MIT |
| `vl53l1x.glb` | Adafruit VL53L1X (3967) | Offizielles Adafruit-CAD: https://github.com/adafruit/Adafruit_CAD_Parts (`3967 VL5SL1X TOF Sensor.step`) | MIT |
| `pico2w.glb` | Raspberry Pi Pico 2 W | STEP-Datei „Pico W“ von Raspberry Pi: https://pip.raspberrypi.com/documents/RP-008318-DS (Stand 11.08.2023) | Raspberry Pi bietet für den Pico 2 W keine eigene STEP-Datei an. Pico 2 W und Pico W haben dieselbe Platine und dieselben Maße, nur der Hauptchip ist anders (RP2350 statt RP2040). Die Datei hat keine eigene Lizenzdatei. Die STEP-Datei des Pico 2 (RP-009061-CA) steht unter MIT. |

**Freenove Breakout Board (FNK0081):** Freenove stellt keine 3D-Datei bereit, aber eine **offizielle mechanische Zeichnung** (Platine CB8101, v1.1, als PDF und DWG):
https://github.com/Freenove/Freenove_Breakout_Board_for_Raspberry_Pi_Pico (Dateien `CB8101_mechanical-drawing_v1.1_20240326.pdf/.dwg`, Lizenz CC BY-NC-SA 3.0).
Das Board ist danach im Skript nachgebaut: 63 × 57 mm, Löcher 58 × 52 mm, 2 × 20 Schraubklemmen (Raster 2,54 mm), Buchsenleisten für den Pico (17,78 mm Abstand), Stiftleisten außen, GPIO-LEDs, 5 × 74HC04. Die Zeichnung selbst liegt nicht im Projekt, nur die Maße.

**Akkuhalter Keystone 1047 und Zellen Samsung INR18650-35E:** im Skript nach den offiziellen Datenblättern gebaut.
- Keystone 1047 (Datenblatt K75p29, https://www.keyelco.com/userAssets/file/K75p29.pdf): 77,1 × 39,8 × 18 mm, Zellabstand 19,1 mm, Löcher Ø 3,2 mm im Abstand 55,2 mm. Die Keystone-STEP-Datei gibt es nur nach Registrierung (Name, Firma, Beruf) auf https://www.keyelco.com/product.cfm/product_id/14061 – wer sich dort anmeldet, kann sie wie oben umwandeln und einbauen.
- Samsung INR18650-35E: Samsung stellt keine CAD-Datei bereit. Maße aus dem Datenblatt: Ø 18,4 mm (max. 18,55), Länge 65,0 mm (max. 65,25), Flat-Top, rosa Hülle.
- M3-Zylinderkopfschrauben nach ISO 4762 (Kopf Ø 5,5 × 3 mm) und M3-Muttern (SW 5,5 × 2,4 mm) nach Norm im Skript (`m3Schraube`, `m3Mutter`).

## Nur lokal: GrabCAD-Modelle (`lokal/`, nicht im Git)

GrabCAD-Modelle dürfen für eigene Projekte genutzt werden. Eine Weitergabe der (umgewandelten) Dateien in einem öffentlichen Repository erlauben die GrabCAD-Nutzungsbedingungen aber nicht ausdrücklich.
Deshalb liegen sie in `modell/teile/lokal/` (steht in `.gitignore`). Wer das Projekt klont, sieht an ihrer Stelle die nachgebauten Ersatzteile (Maße nach Datenblatt/Fotos) – oder lädt die Dateien selbst von GrabCAD und wandelt sie wie unten um.

| Datei | Bauteil | Quelle | Hinweise |
|---|---|---|---|
| `lokal/ddtccrub.glb` | Ladeboard DDTCCRUB 2S (Walfront, Amazon B08LVN7FLH) | GrabCAD, Aleksey Zablotskiy: https://grabcad.com/library/2s-3s-4s-boost-lipo-liion-charger-ddtccrub-1 – Datei `DDTCCRUB CN330X.STEP` | Vom Autor als vereinfachtes Modell bezeichnet. 18 × 37 mm Platine (mit USB-C 38,4 mm). Die grüne Farbe wird im Skript an die Fotos angepasst. |
| `lokal/motor.glb` | Getriebemotor JGA25-370 mit Encoder (6 V) | GrabCAD, Patrice Pennel: https://grabcad.com/library/dc-motor-jga25-370-family-with-or-without-encoder-1 – Datei `with_encoder/motor_JGA25-370_EN_LR21.step` | Getriebelänge hängt von der Übersetzung ab (17–27 mm, Dateien LR17…LR27). Vorläufig 21 mm – nach dem Kauf die passende Länge nehmen. |
| `lokal/halter.glb` | L-Motorhalterung JGA25-370 | GrabCAD, nvdien: https://grabcad.com/library/jga25-370-motor-bracket-1 | Löcher der oberen Platte nicht gezeichnet. |
| `lokal/rad.glb` | Rad „65 mm“ (Solarbotics-Form) | GrabCAD, Vincent Chan: https://grabcad.com/library/65mm-rubber-wheel-1 – Datei `65mm rubber wheel.stp` | Real Ø 67,6 × 24,3 mm. Ohne Farben geliefert; eingefärbt mit `merge_glb.py … --farbe ab:65=34,34,36 --alle 236,190,40` (Reifen schwarz, Felge gelb). |
| `lokal/pololu.glb` | Pololu D36V50F5 | Offizielles STEP von Pololu: https://www.pololu.com/file/0J1733/d36v50fx-step-down-voltage-regulator.step | Pololu nennt keine Lizenz → nur lokal |
| `lokal/bms.glb` | BMS 2S 20 A HW-391 | GrabCAD: https://grabcad.com/library/hw-391-2s-20a-bms-1 | |
| `lokal/ina226.glb` | INA226-Modul (lila) | GrabCAD, Viktor Bulatov: https://grabcad.com/library/ina226-1 | Mit Stiftleiste unten |
| `lokal/mp1584.glb` | MP1584EN (D-SUN) | GrabCAD: https://grabcad.com/library/detailed-d-sun-mp1584en-dc-dc-step-down-voltage-regulator-1 | |
| `lokal/sicherung.glb` | Inline-Sicherungshalter für Standard-Flachsicherung (ATO/ATC) | GrabCAD, Dawson Dueck: https://grabcad.com/library/in-line-blade-fuse-holder-1 | Sieht aus wie der gekaufte Halter (Amazon B078X977PK); stehend, Deckel oben, 54,2 × 25,5 × 12,5 mm mit Kabelansätzen |
| `lokal/vl53l1x-v2` → `lokal/vl53v2.glb` | VL53L1X-Modul 25 × 10,5 mm („VL53L1XV2“, z. B. Happysnow) | GrabCAD, Mustafa Ali Özgönül: https://grabcad.com/library/vl53l1x-1 | Platine 1,5 mm, Sensor 2 mm unter der Mitte, Löcher an den Enden 20 mm auseinander |
| `lokal/taster.glb` | Hauptschalter: runder Taster Ø 12 mm | GrabCAD, MATOX_3D: https://grabcad.com/library/push-button-12mm-2 – Datei `Push button 12mm.STEP` | Achse entlang y, Taste vorne bei y = 0. Frontring Ø 13,9 mm, Gewindekörper Ø 11,8 mm, 22,3 mm lang. Mutter ist nicht im CAD (im Skript ergänzt). |
| `lokal/wago.glb` | WAGO 221-415 | GrabCAD: https://grabcad.com/library/wago-221-415-1 | Echte Größe 29,7 × 18,4 × 8,1 mm – deutlich größer als vorher gezeichnet; die Verteiler auf dem Deckel von Ebene 1 sind deshalb verschoben |
| `lokal/ld19.glb` | LiDAR LDROBOT LD19 | GrabCAD: https://grabcad.com/library/lidar-ld19-1 (`LD19_v2.step`) | |
| `lokal/kamera3.glb` | Raspberry Pi Camera Module 3 | GrabCAD: https://grabcad.com/library/raspberry-pi-camera-module-3-1 | Raspberry Pi bietet für die Kamera nur eine Zeichnung (PDF), kein STEP |
| `lokal/cooler.glb` | Raspberry Pi 5 Active Cooler | GrabCAD: https://grabcad.com/library/raspberry-pi-5-active-cooler-2 | Raspberry Pi bietet nur eine Zeichnung (PDF) |
| `lokal/aihat.glb` | Raspberry Pi AI HAT+ (13/26 TOPS) mit 16-mm-Abstandshaltern und Schrauben | GrabCAD, Nick Williamson: https://grabcad.com/library/raspberry-pi-ai-hat-2 – Datei `RPi_AI_HAT_Plus.step` (Nov. 2026) | Raspberry Pi bietet kein 3D-Modell, nur die Maßzeichnung im offiziellen Produktdatenblatt (RP-008133-DS-1, https://pip-assets.raspberrypi.com/categories/1081-raspberry-pi-ai-hat/documents/RP-008133-DS-1-raspberry-pi-ai-hat-plus-product-brief.pdf, Seite 4). Das Modell stimmt damit überein: 65 × 56,5 mm, Löcher 58 × 49, KI-Chip 17 × 17, Aussparung 10 × 16. Ersetzt das ältere Modell von Bertalan Pizag. |
| `lokal/sim7600.glb` | Waveshare SIM7600G-H 4G DONGLE (nur Platine, ohne Hülle) | Waveshare Wiki, „3D drawings of PCBA“: https://files.waveshare.com/wiki/SIM7600G-H/3D/SIM7600G-H_4G_DONGLE_PCB_3D.zip – Datei `SIM7600G-H_4G_DONGLE_PCB.stp` (Nov. 2026) | Lizenz nicht angegeben, deshalb nur lokal. Platine 82,3 × 40,2 × 1,6 mm ohne Befestigungslöcher, USB-A-Stecker bei x = −15,3 … 0, SMA (MAIN) bis x = 91,8, zwei u.FL bei x = 79,4. Umgewandelt mit `step2glb.py` und `merge_glb.py`. |
| `lokal/drv8833.glb` | DRV8833-Modul, schwarz (MakerMind, roboter-bausatz.de RBS12954) | GrabCAD, Juan Manuel Dominici: https://grabcad.com/library/drv8833-dual-h-bridge-motor-driver-doble-puente-h-1 – Datei `Modulo_DRV8833_A.stp` | Stiftleisten beim Umwandeln entfernt (`--ohne 4,4,4 134,90,20`), weil die Kabel direkt eingelötet werden. 18,6 × 16,8 mm. |
| `lokal/rad85.glb` | Rad Ø 85 mm (Geländerad, Gummi auf Felge) | GrabCAD, Tanvir Ahmed: https://grabcad.com/library/85mm-anti-skid-shockproof-wheel-general-purpose-design-1 – Datei `Off Road Tyre v3.step` (Juni 2025) | Laut Autor nach keinem bestimmten Kaufprodukt gezeichnet. Die 530 Spikes (einzelne Körper < 10 mm) sind entfernt, der Reifen (vorher Ø 90,9 mm) ist auf Ø 85 mm skaliert → 85 × 36 mm, Achse entlang z, Mitte im Ursprung. |

**Noch ohne CAD:** 4G/GPS-Modul SIM7600G-H (auf GrabCAD nur als Inventor-/SolidWorks-Datei), GPS- und LTE-Antennen, Status-LEDs, USB-Adapter des LiDAR.

**Einpassen:** Die meisten Modelle werden mit `einpassen(name, gruppe)` im Skript automatisch an die Stelle des einfachen Ersatzmodells gesetzt (lange Seite an lange Seite, mittig, gleiche Unterkante). Vorher legt `werkzeug/ausrichten.py` jedes Modell flach hin (Bauteilseite oben, Stiftleisten unten).

**Ersatzteile im Skript** (wenn `lokal/` fehlt):
- DRV8833: nach Produktseite (16 × 18,5 mm) und Fotos, Raster 2,54 mm, Reihenabstand 15,24 mm, Pinfolge laut Aufdruck.
- Ladeboard: nach Händlerangaben baugleicher Boards (39 × 18 × 6,3 mm) und Produktfotos.

**Mit den echten Teilen nachmessen**, bevor Platten gedruckt werden.

## Neues Teil hinzufügen

Im Ordner `modell/teile`. Einmalig: `python -m venv venv` und dann `venv\Scripts\pip install cadquery-ocp trimesh numpy`

```
venv\Scripts\python werkzeug\step2glb.py teil.step roh.glb 0.08     # STEP -> GLB (0,08 mm Genauigkeit)
venv\Scripts\python werkzeug\merge_glb.py roh.glb NAME.glb [--min 0.3] [--max 12000] [--ohne R,G,B] [--scharf]   # gleiche Farben zusammenfassen, verkleinern; --scharf für eigene Druckteile (scharfe Kanten, sonst helle Dreiecke)
venv\Scripts\python werkzeug\ausrichten.py NAME.glb NAME.glb [oben=klein] [ziel=x]   # flach hinlegen, Bauteilseite oben
python werkzeug\einbetten.py                                        # teile.js und lokal/teile-lokal.js neu erzeugen
```

Im Skript dann `einpassen('NAME', gruppe)` aufrufen (setzt das Modell an die Stelle des Ersatzmodells) oder für eine genaue Lage `cadTeil('NAME', gruppe, ersatzGruppe, (m) => { …ausrichten… })` (Beispiel: Pico im Abschnitt `freenove()`).
