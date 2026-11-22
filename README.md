# Raspberry Car

Ein kleines Roboterauto zum Nachbauen – gedacht wie eine DJI-Drohne, nur auf vier Rädern:
Live-Video aufs Handy, Hinderniserkennung, Karte der Umgebung per LiDAR (auch als Grundriss),
„Folge mir“ per KI und „Nach Hause fahren“ per GPS.

Gebaut wird nur aus Standardmodulen, verbunden mit Schraubklemmen, Lötstellen und verriegelnden Steckern – keine Jumperkabel.

## Aufbau: Sandwich in Ebenen

> **Umbau läuft (seit 22.11.2026):** Das Auto wird breiter und flacher – **3 Ebenen mit 250 × 180 mm** statt 4 mit 205 × 130 mm, jede Ebene aus zwei verschraubten Hälften (siehe `docs/entscheidungen.md`). Alle drei Ebenen sind neu; Ebene 3 ist eine Klapphaube mit integriertem Dach. Jede Ebene ist 250 × 180 mm und aus zwei verschraubten Hälften gedruckt.

| Ebene | Inhalt | Warum dort |
|---|---|---|
| 3 · Gehirn mit Dach (Klapphaube) | Raspberry Pi 5 + Active Cooler + AI HAT+, Kamera Modul 3 Wide, Pololu 5 V/5,5 A, 4G/GPS-Modul, GPS-Antenne, Status-LEDs, rundes Status-Display (Touch, Mikrofon, Lautsprecher) – alles hängt am Dach; oben der 360°-LiDAR LD19 | Rechenleistung, Belüftung, Kamera vorne, Rundumsicht; klappt hinten auf, dann liegt Ebene 2 offen |
| 2 · Antrieb | Pico 2 W auf Freenove-Board, 2× DRV8833, MP1584, BNO085, 2× 3,3-V-Verteiler, Ladeboard, Hauptschalter | Echtzeit-Steuerung, kurze Wege, vier Grifflöcher über den Motorsteckern |
| 1 · Fahrwerk & Energie | 4× JGA25-370 mit Encoder + Räder (außen, Radstand 160 mm), Akku 2S2P und die Stromversorgung in der Wanne: BMS, INA226, Sicherung und Verteiler; 2× VL53L1X innen hinter Fenstern vorne und hinten | Schwerpunkt ganz unten |

Maße ca. 25 × 24 × 15,5 cm (mit Rädern und LiDAR). 3D-Modell: [`modell/raspberry-car-3d.html`](modell/raspberry-car-3d.html) im Browser öffnen. Nur den unteren Teil, an dem wir gerade bauen (ohne Kabel), zeigt [`modell/ebene1-unten.html`](modell/ebene1-unten.html). Wie das Fahrwerk im Gelände fährt und sich dreht, zeigt die [Fahrsimulation](modell/fahrsimulation.html). Es startet mit der Ansicht **„Vorhandene Teile“** (nur was schon da ist, auf einer Matte mit 1-cm-Raster); „Ganzes Auto“ zeigt den kompletten Plan.

## Stufenplan

Jede Stufe funktioniert für sich. Wer nur Stufe 1 baut, hat schon ein fahrendes Auto.

| Stufe | Teile | Ergebnis | Stand |
|---|---|---|---|
| 1 | Pico 2 W, Freenove-Board, 4 Motoren mit Rädern, 2× DRV8833 | fährt per Handy-Joystick (WLAN vom Pico) | Pico und 2× DRV8833 da, Board bestellt |
| 2 | 4× 18650, BMS, Ladeboard, INA226, Sicherung, Schalter, WAGO-Verteiler, MP1584 | Akku mit USB-C-Ladung, Akkuanzeige | Ladeboard da |
| 3 | Pi 5, Pololu 5 V, Kamera Modul 3 Wide, rundes Status-Display mit Mikrofon und Lautsprecher | Live-Video, Status auf dem Dach, Sprachbefehle | Pi 5 (8 GB) da |
| 4 | LiDAR LD19, BNO085, 2× VL53L1X | Karte, Grundriss, Hindernisse, selbst navigieren | 2× VL53L1X bestellt |
| 5 | AI HAT+ 13 TOPS | Personen erkennen, Folge mir | offen |
| 6 | 4G/GPS-Modul + Antennen | Steuerung von überall, draußen navigieren | offen |

## Dokumente

- [Stückliste](docs/stueckliste.md)
- [Verdrahtungsplan](docs/verdrahtung.md)
- [Stromversorgung](docs/stromversorgung.md)
- [Entscheidungen](docs/entscheidungen.md)

## Lizenz

MIT – siehe [LICENSE](LICENSE).
