# Stückliste

Preise sind grobe Richtwerte (Stand November 2026) und vor dem Kauf zu prüfen.
Status: 📦 da · ✅ bestellt · 🔎 ausgesucht · ⬜ offen

## Stufe 1 – Fahren

| Status | Teil | Variante / worauf achten | Wo | ca. |
|---|---|---|---|---|
| 📦 | Raspberry Pi Pico 2 **W** mit Headern (Waveshare, vorgelötet) | **W** = mit WLAN | Amazon | 15 € |
| ✅ | Freenove Breakout Board für Pico | Schraubklemmen für alle 40 Pins | Amazon | 15 € |
| 🔎 | 4× Getriebemotor **JGA25-370, 6 V, Encoder, 130 U/min** (Getriebe 1:46,8, 4-mm-D-Welle) | **6 V** und **130 U/min** auswählen, alle vier gleich. Halterungen brauchen wir nicht (die Motoren werden direkt an die Wanne geschraubt). Angebote: [AliExpress 1005001279982165](https://de.aliexpress.com/item/1005001279982165.html) (Variante 6V + 130 U/min wählen, ab ca. 6,30 € je Stück – Screenshot der gewählten Variante prüfen) oder [Amazon Rebower B0HJGFC6DV](https://www.amazon.de/dp/B0HJGFC6DV) (14,49 € je Stück, 1:46,8, 4-mm-D-Welle, 72 mm lang). Nach der Lieferung Länge von Getriebe + Motor nachmessen | AliExpress | ca. 26 € (4 Stück) |
| 🔎 | 4× Gummirad **Ø 85 mm** mit Sechskant-Kupplung, **Bohrung 4 mm** | Angebot: [AliExpress 1005013249538060](https://de.aliexpress.com/item/1005013249538060.html) (4 Stück ca. 24 €). Vor dem Bestellen klären/prüfen: ist die Kupplung mit 4-mm-Bohrung dabei, und passt ihr Sechskant in die Nabe? Sonst passende 4-mm-Sechskant-Kupplungen dazu (ca. 1 € je Stück) | AliExpress | ca. 24–28 € |
| 📦 | 2× Motortreiber DRV8833 | 2-Kanal-Modul, schwarz, 16 × 18,5 mm (MakerMind, RBS12954). Not-Stopp an **ULT**, nicht EEP | roboter-bausatz.de | 4 € |
| ⬜ | 2× WAGO 221-415 (3,3-V-Verteiler) | Original WAGO, 5-polig, transparent/orange. Eine 8er-Packung reicht für alle 4 Klemmen im Auto (hier und Stufe 2): [Amazon B09VZYG222](https://www.amazon.de/dp/B09VZYG222) | Amazon | 7 € (8 Stück) |
| ⬜ | Aufbewahrungsbox | innen mind. 30 × 22 × 14 cm, Klickdeckel | Action | 5 € |
| ✔ vorhanden | Litze 0,25–0,5 mm², Aderendhülsen + Crimpzange, Schrumpfschlauch, Lötkolben | | | |

Ohne Akku läuft nur der Pico (über USB): Joystick-Seite und Encoder lassen sich schon testen, die Motoren drehen erst mit dem Akku aus Stufe 2.

## Stufe 2 – Akku

| Status | Teil | Variante / worauf achten | Wo | ca. |
|---|---|---|---|---|
| 📦 | Ladeboard DDTCCRUB 2S (Walfront, B08LVN7FLH) | 39 × 18 mm, 4 Löcher. Lötbrücken **2S** und **1A** setzen, sonst nichts (siehe Stromversorgung) | Amazon | 7,60 € |
| ⬜ | BMS 2S 20 A | **Balance-Version**, nicht Standard (z. B. HW-391) | Amazon | 7 € |
| ⬜ | 4× Samsung INR18650-35E | **Flat-Top** (ohne Lötfahne), alle 4 zusammen kaufen, **nicht** von AliExpress/eBay (Fälschungen). Echte 35E haben eine rosa Hülle | Akkuteile.de / NKON | 20 € |
| 🔎 | 2× Akkuhalter **Keystone 1047** (2 × 18650, Lötfahnen) | Für Zellen **ohne** Schutzschaltung und Flat-Top geeignet, jede Zelle eigene Kontakte, 2 Löcher Ø 3,2 mm für M3. Nicht den MPD BH-18650-W nehmen – der ist für 70-mm-Zellen mit Schutzschaltung, die 35E (65 mm) würde wackeln | DigiKey (36-1047-ND) | 2 × ca. 10,80 € |
| ⬜ | INA226-Modul | Shunt **R002** (20 A), nicht R100. Die beiliegende **Stiftleiste nicht einlöten** – die Leitungen kommen direkt in die Lötaugen, das Modul liegt flach in seiner Tasche | AliExpress | 4 € |
| ⬜ | MP1584-Wandler 5 V | fest 5 V oder vor Einbau auf 5,0 V einstellen | AliExpress | 2 € |
| ⬜ | Schottky-Diode 1N5819 | zwischen MP1584 und Pico VSYS | | 0,20 € |
| ⬜ | Kfz-Flachsicherungshalter + 10-A-Sicherung | Inline-Halter für **Standard-Flachsicherung (ATO/ATC)** mit 16-AWG-Kabel (ca. 1,3 mm², reicht für 9 A), 5 Halter + je eine Sicherung 3/5/7,5/**10**/15/20 A: [Amazon B078X977PK](https://www.amazon.de/dp/B078X977PK). Halter steht rechts neben dem Akku (Platz und 2 Kabelbinder-Schlitze in der Wanne nach dem CAD-Modell eingeplant) – nach der Lieferung kurz nachmessen | Amazon | 7 € |
| ⬜ | Hauptschalter: **runder Taster Ø 12 mm, rastend** (an/aus) – CAD: GrabCAD „Push button 12mm“ (MATOX_3D), Händler-Link dort: [AliExpress 1005006695980453](https://www.aliexpress.com/item/1005006695980453.html) | Kommt hinten in die Rückwand des Gehäuse-Rings (Einbauloch Ø 12,2 mm, Gewinde mit Mutter, Wand 2,4 mm); ragt 19 mm nach innen. **Stromangabe prüfen:** durch ihn fließt der ganze Strom (bis ca. 9 A). Kleine Taster können oft nur 1–3 A – dann einen mit ≥ 10 A nehmen oder damit ein Relais-/MOSFET-Modul schalten (vor dem Bestellen Screenshot der Variante prüfen) | AliExpress | 2–5 € |
| ⬜ | 2× WAGO 221-415 (Plus- und Minus-Verteiler) | aus derselben 8er-Packung wie die 3,3-V-Verteiler (Stufe 1) | – | – |

## Stufe 3 – Gehirn und Video

| Status | Teil | Variante / worauf achten | ca. |
|---|---|---|---|
| 📦 | Raspberry Pi 5, 8 GB | | 85 € |
| ⬜ | Active Cooler (offiziell) | | 6 € |
| ⬜ | microSD 64 GB A2 | | 12 € |
| ⬜ | Pololu D36V50F5 (5 V, 5,5 A) | | 25 € |
| ⬜ | USB-C-Stecker zum Anlöten | Pololu → Pi 5 | 2 € |
| ⬜ | Camera Module 3 Wide | + Kabel **22 auf 15 Pin** (Pi 5) | 40 € |
| ⬜ | 2× USB-Kabel kurz (A auf Micro-USB) | Pico und LiDAR-Adapter | 5 € |
| 🔎 | Status-Display **Waveshare ESP32-S3-Touch-AMOLED-1.75** (rund, Touch, 2 Mikrofone, Lautsprecher) | Die **einfache Platine ohne Gehäuse** nehmen (nicht „-B“ mit Gehäuse, nicht „-G“ mit GPS), z. B. [Amazon B0F99V6FGF](https://www.amazon.de/dp/B0F99V6FGF). Lautsprecher 8 Ω / 2 W liegt laut Händlern bei – beim Kauf prüfen. Befestigung mit 3 × M2 (Abstandshalter sind auf der Platine) | 40 € |
| ⬜ | USB-Kabel kurz, USB-C auf USB-A (gewinkelt) | Status-Display → Pi 5 USB 3.0 oben | 5 € |
| 🔎 | 2× LED-Leiste **WS2812B, 8 LEDs** (Front- und Rücklicht) | Angebot: [Amazon Joycabin B0G648ST2C](https://www.amazon.de/dp/B0G648ST2C) – Größe **„8 Bits (10 Pcs)“** wählen (10 Stück, 8,79 €). Nachbau des Adafruit NeoPixel Stick: 8 LEDs in einer Reihe, Lötpunkte GND/DI/4–7 V/GND und GND/DO/4–7 V/GND an den Enden auf der Rückseite. Achtung: das Maßbild des Händlers nennt 62 × 12 mm, das Original ist 50,8 × 10,2 mm – nach der Lieferung nachmessen und `LICHT_L`/`LICHT_H` in `gehaeuse/ebene3_gehirn.py` anpassen, bevor die Haube gedruckt wird. Original von Adafruit: [B01F7Z7I70](https://www.amazon.de/dp/B01F7Z7I70) (teuer) | ca. 9 € (10 Stück) |

## Stufe 4 – Orientierung und Karte

| Status | Teil | Variante / worauf achten | ca. |
|---|---|---|---|
| ⬜ | LiDAR LDROBOT LD19 (oder RPLIDAR C1) | mit USB-Adapter | 60–90 € |
| ⬜ | BNO085 mit STEMMA QT (z. B. Adafruit) | | 25 € |
| ✅ | 2× VL53L1X-Modul 25 × 10,7 mm („VL53L1XV2“, z. B. Happysnow, [Amazon B0CNGP7LCR](https://www.amazon.de/dp/B0CNGP7LCR)) | **Wirklich VL53L1X (4 m), nicht VL53L0X (2 m)** – viele günstige Sets sind L0X. Pins VIN, GND, SCL, SDA, GPIO1, XSHUT; Kabel werden angelötet. Sitzen innen hinter Fenstern vorne und hinten in der Wanne | 2 × 11 € |

## Stufe 5 – KI

| Status | Teil | ca. |
|---|---|---|
| ⬜ | Raspberry Pi AI HAT+ 13 TOPS (Hailo-8L) mit Stapel-Stiftleiste | 70–80 € |

## Stufe 6 – Mobilfunk und GPS

| Status | Teil | ca. |
|---|---|---|
| ⬜ | 4G/GNSS-Modul **Waveshare SIM7600G-H 4G DONGLE** (Amazon ASIN B08BZKTZDJ, dort ca. 134 €; bei anderen Händlern oft 56–75 €). Genau auf **G-H** achten (nur diese Variante hat GPS und alle Bänder). Eingebaut wird nur die Platine (82,3 × 40,2 mm), die Kunststoffhülle wird abgezogen. Die beiliegende LTE-Antenne mit SMA passt an MAIN. | 56–134 € |
| ⬜ | Kurzes USB-A-Kabel (Buchse auf Stecker, ca. 15 cm, gewinkelt) vom Dongle zum Pi | 5 € |
| ⬜ | GPS-Keramikantenne (u.FL, aktiv) und 1× LTE-Flachantenne (u.FL) für AUX | 10 € |
| ⬜ | SIM-Karte mit Datentarif | |

## Druckteile

Alle Ebenen in derselben Außenform 250 × 180 mm, jede aus zwei Hälften, Räder außen (Radstand 160 mm). Druckhinweise und Zusammenbau: `gehaeuse/README.md`. Alle drei Ebenen sind neu (seit 22.11.2026). **Farben (Rover-Design):** Wanne, Ring und Haube Graphit/Dunkelgrau, Elektronik-Deck und Schutzbleche Orange, Streuscheiben Natur/Weiß.

| Status | Teil | Datei | Anzahl | Hinweis |
|---|---|---|---|---|
| ⬜ | Wanne vordere Hälfte (Ebene 1) | `gehaeuse/ebene1/wanne_vorne.stl` | 1 | 137 × 180 × 42 mm, Stromversorgung, Nahsensor vorne, 3 Laschen zur hinteren Hälfte |
| ⬜ | Wanne hintere Hälfte (Ebene 1) | `gehaeuse/ebene1/wanne_hinten.stl` | 1 | 131 × 180 × 42 mm, Akku, Nahsensor hinten |
| ⬜ | Motorbügel (Ebene 1) | `gehaeuse/ebene1/motorbuegel.stl` | 4 | |
| ⬜ | Elektronik-Deck vordere Hälfte (Ebene 2) | `gehaeuse/ebene2/platte_vorne.stl` | 1 | Motorzone vorne, Steg zur hinteren Hälfte |
| ⬜ | Elektronik-Deck hintere Hälfte (Ebene 2) | `gehaeuse/ebene2/platte_hinten.stl` | 1 | zugleich Deckel der Wanne: Pico, Kompass, Motorzone hinten, Ladeboard |
| ⬜ | Gehäuse-Ring vordere Hälfte (Ebene 2) | `gehaeuse/ebene2/ring_vorne.stl` | 1 | mit den Laschen für die Schrauben der Klapphaube |
| ⬜ | Gehäuse-Ring hintere Hälfte (Ebene 2) | `gehaeuse/ebene2/ring_hinten.stl` | 1 | Scharnier, Loch für den Hauptschalter, Ausschnitt für USB-C |
| ⬜ | Klapphaube vordere Hälfte (Ebene 3) | `gehaeuse/ebene3/haube_vorne.stl` | 1 | Kamera, Frontlicht, Pololu, oben der LiDAR |
| ⬜ | Klapphaube hintere Hälfte (Ebene 3) | `gehaeuse/ebene3/haube_hinten.stl` | 1 | Pi 5 mit AI HAT+, 4G, GPS, rundes Display, Rücklicht, Scharnier |
| ⬜ | Schutzblech | `gehaeuse/schutzbleche/schutzblech.stl` | 4 | Eckig, dasselbe Teil an allen vier Rädern (rechts um 180° gedreht). Je 2 × M3 × 10 von außen in die Schraubsäulen des Gehäuse-Rings. **Orange** |
| ⬜ | Streuscheibe | `gehaeuse/ebene3/streuscheibe.stl` | 2 | Für Front- und Rücklicht, 1 mm dick, **Natur- oder Weiß-PETG** |
| ⬜ | **Prüfstand** (Werkzeug, kommt nicht ins Auto) | `gehaeuse/pruefstand/pruefstand.stl` | 1 | 112 × 112 mm, ein Teil, ohne Schrauben, ca. 98 cm³. Wie eine Hebebühne: 4 Zapfen rasten in die 4 Kerben unten in der Wanne. Räder hängen frei, zum Testen von Motoren und Software |

Kamerahalter und Ebene 3/4 folgen.
Schrauben: nur **M3-Zylinderkopf ISO 4762** (Innensechskant 2,5). Für Ebene 1: 8 × M3 × 6, 12 × M3 × 8, **4 × M3 × 45**, 4 × Mutter M3. Die Motorhalterungen aus dem Motor-Set werden nicht gebraucht. Für Ebene 2: 4 × M3 × 8. Für die Schutzbleche: 8 × M3 × 10. Messing-Abstandsbolzen sind nicht mehr nötig (Säulen werden mitgedruckt).
