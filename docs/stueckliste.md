# Stückliste

Preise sind grobe Richtwerte (Stand November 2026) und vor dem Kauf zu prüfen.
Status: 📦 da · ✅ bestellt · 🔎 ausgesucht · ⬜ offen

## Stufe 1 – Fahren

| Status | Teil | Variante / worauf achten | Wo | ca. |
|---|---|---|---|---|
| 📦 | Raspberry Pi Pico 2 **W** mit Headern (Waveshare, vorgelötet) | **W** = mit WLAN | Amazon | 15 € |
| ✅ | Freenove Breakout Board für Pico | Schraubklemmen für alle 40 Pins | Amazon | 15 € |
| ⬜ | 4× Getriebemotor JGA25-370 mit Encoder, **mit Rädern und Halterungen** | **6 V**, **mit Encoder**, alle vier **gleiche Drehzahl** (z. B. 280 U/min). Die üblichen 20-cm-Kabel reichen | AliExpress | 30 € |
| 📦 | 2× Motortreiber DRV8833 | 2-Kanal-Modul, schwarz, 16 × 18,5 mm (MakerMind, RBS12954). Not-Stopp an **ULT**, nicht EEP | roboter-bausatz.de | 4 € |
| ⬜ | 2× WAGO 221-415 (3,3-V-Verteiler) | Original WAGO, 5-polig, transparent/orange. Eine 8er-Packung reicht für alle 4 Klemmen im Auto (hier und Stufe 2): [Amazon B09VZYG222](https://www.amazon.de/dp/B09VZYG222) | Amazon | 7 € (8 Stück) |
| ⬜ | Aufbewahrungsbox | innen mind. 30 × 22 × 14 cm, Klickdeckel | Action | 5 € |
| ✔ vorhanden | Litze 0,25–0,5 mm², Aderendhülsen + Crimpzange, Schrumpfschlauch, Lötkolben | | | |

Zum Testen vor dem Akku: Batteriehalter 4× AA (6 V) für die Motoren, Pico über USB.

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

## Stufe 4 – Orientierung und Karte

| Status | Teil | Variante / worauf achten | ca. |
|---|---|---|---|
| ⬜ | LiDAR LDROBOT LD19 (oder RPLIDAR C1) | mit USB-Adapter | 60–90 € |
| ⬜ | BNO085 mit STEMMA QT (z. B. Adafruit) | | 25 € |
| ⬜ | 2× VL53L1X-Modul 25 × 10,7 mm („VL53L1XV2“, z. B. Happysnow, [Amazon B0CNGP7LCR](https://www.amazon.de/dp/B0CNGP7LCR)) | **Wirklich VL53L1X (4 m), nicht VL53L0X (2 m)** – viele günstige Sets sind L0X. Pins VIN, GND, SCL, SDA, GPIO1, XSHUT; Kabel werden angelötet. Sitzen innen hinter Fenstern vorne und hinten in der Wanne | 2 × 11 € |

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

Alle Ebenen in derselben Außenform 205 × 130 mm, Räder an den Ecken (Radstand 145 mm). Druckhinweise und Zusammenbau: `gehaeuse/README.md`.

| Status | Teil | Datei | Anzahl | Hinweis |
|---|---|---|---|---|
| ⬜ | Wanne (Ebene 1) | `gehaeuse/ebene1/wanne.stl` | 1 | 205 × 130 × 42 mm, mit Halter für die 2 Nahsensoren und Kabelbinder-Schlitzen |
| ⬜ | Motorbügel (Ebene 1) | `gehaeuse/ebene1/motorbuegel.stl` | 4 | |
| ⬜ | Elektronik-Deck (Ebene 2) | `gehaeuse/ebene2/platte.stl` | 1 | zugleich Deckel der Wanne |
| ⬜ | Gehäuse-Ring oben (Ebene 2) | `gehaeuse/ebene2/ring_oben.stl` | 1 | mit Loch für den Druckschalter und Ausschnitt für USB-C |
| ⬜ | **Prüfstand** (Werkzeug, kommt nicht ins Auto) | `gehaeuse/pruefstand/pruefstand.stl` | 1 | 112 × 112 mm, ein Teil, ohne Schrauben, ca. 98 cm³. Wie eine Hebebühne: 4 Zapfen rasten in die 4 Kerben unten in der Wanne. Räder hängen frei, zum Testen von Motoren und Software |

Kamerahalter und Ebene 3/4 folgen.
Schrauben: nur **M3-Zylinderkopf ISO 4762** (Innensechskant 2,5). Für Ebene 1: 8 × M3 × 6, 12 × M3 × 8, **4 × M3 × 45**, 4 × Mutter M3. Die Motorhalterungen aus dem Motor-Set werden nicht gebraucht. Für Ebene 2: 4 × M3 × 8. Messing-Abstandsbolzen sind nicht mehr nötig (Säulen werden mitgedruckt).
