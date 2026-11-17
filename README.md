# Raspberry Car

Ein kleines Roboterauto zum Nachbauen – gedacht wie eine DJI-Drohne, nur auf vier Rädern:
Live-Video aufs Handy, Hinderniserkennung, Karte der Umgebung per LiDAR (auch als Grundriss),
„Folge mir“ per KI und „Nach Hause fahren“ per GPS.

Gebaut wird nur aus Standardmodulen, verbunden mit Schraubklemmen, Lötstellen und verriegelnden Steckern – keine Jumperkabel.

## Aufbau: Sandwich in vier Ebenen

| Ebene | Inhalt | Warum dort |
|---|---|---|
| 4 · Dach | 360°-LiDAR LD19, GPS-Antenne, LTE-Antennen, Status-LEDs | Rundumsicht, Sicht zum Himmel |
| 3 · Gehirn | Raspberry Pi 5 + Active Cooler + AI HAT+, Kamera Modul 3 Wide, Pololu 5 V/5,5 A, 4G/GPS-Modul | Rechenleistung, Belüftung, Kamera vorne |
| 2 · Antrieb | Pico 2 W auf Freenove-Board, 2× DRV8833, MP1584, BNO085, 3,3-V-Verteiler | Echtzeit-Steuerung, kurze Wege |
| 1 · Fahrwerk & Energie | 4× JGA25-370 mit Encoder + Räder, Akku 2S2P unter der Platte, BMS, Ladeboard (USB-C hinten), Sicherung, Schalter, INA226, Verteiler, 4× VL53L1X | Schwerpunkt ganz unten |

Maße ca. 18 × 19 × 19 cm (mit Rädern und LiDAR). 3D-Modell: [`modell/raspberry-car-3d.html`](modell/raspberry-car-3d.html) im Browser öffnen.

## Stufenplan

Jede Stufe funktioniert für sich. Wer nur Stufe 1 baut, hat schon ein fahrendes Auto.

| Stufe | Teile | Ergebnis | Stand |
|---|---|---|---|
| 1 | Pico 2 W, Freenove-Board, 4 Motoren mit Rädern, 2× DRV8833 | fährt per Handy-Joystick (WLAN vom Pico) | Pico + Board bestellt |
| 2 | 4× 18650, BMS, Ladeboard, INA226, Sicherung, Schalter, WAGO-Verteiler, MP1584 | Akku mit USB-C-Ladung, Akkuanzeige | Ladeboard ausgesucht |
| 3 | Pi 5, Pololu 5 V, Kamera Modul 3 Wide | Live-Video | offen |
| 4 | LiDAR LD19, BNO085, 4× VL53L1X | Karte, Grundriss, Hindernisse, selbst navigieren | offen |
| 5 | AI HAT+ 13 TOPS | Personen erkennen, Folge mir | offen |
| 6 | 4G/GPS-Modul + Antennen | Steuerung von überall, draußen navigieren | offen |

## Dokumente

- [Stückliste](docs/stueckliste.md)
- [Verdrahtungsplan](docs/verdrahtung.md)
- [Stromversorgung](docs/stromversorgung.md)
- [Entscheidungen](docs/entscheidungen.md)

## Lizenz

MIT – siehe [LICENSE](LICENSE).
