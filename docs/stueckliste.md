# Stückliste

Preise sind grobe Richtwerte (Stand November 2026) und vor dem Kauf zu prüfen.
Status: 📦 da · ✅ bestellt · 🔎 ausgesucht · ⬜ offen

## Stufe 1 – Fahren

| Status | Teil | Variante / worauf achten | Wo | ca. |
|---|---|---|---|---|
| 📦 | Raspberry Pi Pico 2 **W** mit Headern (Waveshare, vorgelötet) | **W** = mit WLAN | Amazon | 15 € |
| ✅ | Freenove Breakout Board für Pico | Schraubklemmen für alle 40 Pins | Amazon | 15 € |
| ⬜ | 4× Getriebemotor JGA25-370 mit Encoder, **mit Rädern und Halterungen** | **6 V**, **mit Encoder**, alle vier **gleiche Drehzahl** (z. B. 280 U/min) | AliExpress | 30 € |
| 📦 | 2× Motortreiber DRV8833 | 2-Kanal-Modul, schwarz, 16 × 18,5 mm (MakerMind, RBS12954). Not-Stopp an **ULT**, nicht EEP | roboter-bausatz.de | 4 € |
| ⬜ | 2× WAGO 221-415 (3,3-V-Verteiler) | | Baumarkt / Amazon | 3 € |
| ⬜ | Aufbewahrungsbox | innen mind. 30 × 22 × 14 cm, Klickdeckel | Action | 5 € |
| ✔ vorhanden | Litze 0,25–0,5 mm², Aderendhülsen + Crimpzange, Schrumpfschlauch, Lötkolben | | | |

Zum Testen vor dem Akku: Batteriehalter 4× AA (6 V) für die Motoren, Pico über USB.

## Stufe 2 – Akku

| Status | Teil | Variante / worauf achten | Wo | ca. |
|---|---|---|---|---|
| 📦 | Ladeboard DDTCCRUB 2S (Walfront, B08LVN7FLH) | 39 × 18 mm, 4 Löcher. Lötbrücken **2S** und **1A** setzen, sonst nichts (siehe Stromversorgung) | Amazon | 7,60 € |
| ⬜ | BMS 2S 20 A | **Balance-Version**, nicht Standard (z. B. HW-391) | Amazon | 7 € |
| ⬜ | 4× Samsung INR18650-35E | alle 4 zusammen kaufen, **nicht** von AliExpress/eBay (Fälschungen) | Akkuteile.de / NKON | 20 € |
| ⬜ | 2× Halter 2× 18650 **mit einzelnen Kabeln** | | NKON | 4 € |
| ⬜ | INA226-Modul | Shunt **R002** (20 A), nicht R100 | AliExpress | 4 € |
| ⬜ | MP1584-Wandler 5 V | fest 5 V oder vor Einbau auf 5,0 V einstellen | AliExpress | 2 € |
| ⬜ | Schottky-Diode 1N5819 | zwischen MP1584 und Pico VSYS | | 0,20 € |
| ⬜ | Kfz-Flachsicherungshalter + 10-A-Sicherung | | Baumarkt | 3 € |
| ⬜ | Kippschalter ≥ 10 A | | Baumarkt / AliExpress | 2 € |
| ⬜ | 2× WAGO 221-415 (Plus- und Minus-Verteiler) | | Baumarkt / Amazon | 3 € |

## Stufe 3 – Gehirn und Video

| Status | Teil | Variante / worauf achten | ca. |
|---|---|---|---|
| ⬜ | Raspberry Pi 5, 8 GB | | 85 € |
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
| ⬜ | 4× VL53L1X mit STEMMA QT (z. B. Adafruit) | XSHUT-Pin vorhanden | 4 × 15 € |
| ⬜ | STEMMA-QT-Kabel (verschiedene Längen) | | 5 € |

## Stufe 5 – KI

| Status | Teil | ca. |
|---|---|---|
| ⬜ | Raspberry Pi AI HAT+ 13 TOPS (Hailo-8L) mit Stapel-Stiftleiste | 70–80 € |

## Stufe 6 – Mobilfunk und GPS

| Status | Teil | ca. |
|---|---|---|
| ⬜ | 4G/GNSS-Modul SIM7600G-H als USB-Variante | 50–70 € |
| ⬜ | GPS-Keramikantenne, 2× LTE-Flachantenne (u.FL) | 10 € |
| ⬜ | SIM-Karte mit Datentarif | |

## Druckteile

4 Platten à ca. 170 × 130 × 3 mm, Kamerahalter, Sensorhalter. Dateien folgen in `gehaeuse/`, wenn die Teile vermessen sind.
M3-Messing-Abstandsbolzen: 3 × 4 Stück (ca. 25, 25, 45 mm) + Schrauben.
