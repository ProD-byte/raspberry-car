# Raspberry Car – Hinweise für Claude

Dieses Projekt ist ein **Nachbau-Projekt**: ein kleines, vierrädriges Roboterauto, das sich wie eine DJI-Drohne anfühlen soll (Live-Video, Karte, „Folge mir“, „Nach Hause fahren“). Andere sollen es mit gekauften Standardmodulen nachbauen können.

## Zusammenarbeit
- Sprache: **Deutsch**, einfach und verständlich erklären. Der Bauherr kann löten (auch SMD), programmiert aber nicht beruflich.
- Eingekauft wird **Stück für Stück, jeden Monat etwas** (Budget pro Monat oft ~50 €). Immer sagen, was jetzt nötig ist und was warten kann.
- Vor dem Bestellen Screenshots der gewählten Variante prüfen (Spannung, Encoder, 2S/3S usw.).
- Nichts anschließen lassen, bevor es einen Verdrahtungsplan gibt.

## Feste Entscheidungen (nicht ohne Rückfrage ändern)
Siehe `docs/entscheidungen.md`. Kurz:
- **Keine Jumperkabel, keine Steckbretter.** Verbindungen über Schraubklemmen (mit Aderendhülsen), Lötstellen, WAGO-Hebelklemmen oder verriegelnde Stecker (STEMMA QT, JST).
- **Nur Standardmodule**, keine eigene Platine – damit es nachbaubar bleibt.
- **Motoren 6 V** (JGA25-370 mit Encoder, Räder 65 mm), Auto möglichst klein.
- **Akku: 2S2P aus 4× Samsung INR18650-35E** (kein LiPo), mit **BMS 2S 20 A Balance** und **Ladeboard DDTCCRUB 2S** (Lötbrücken 2S und 1A).
- **Motoren und Pi haben getrennte Stromwege** (DRV8833 direkt am Akku, Pi über eigenen Pololu-Wandler), damit Motorspitzen den Pi nicht zum Absturz bringen. Deshalb **kein** Waveshare UPS HAT.
- **Pico 2 W** (auf Freenove Breakout Board) = Echtzeit: Motoren, Encoder, Sensoren, Not-Stopp. **Pi 5** = Gehirn: Kamera, LiDAR-Karte, Navigation, Web-App, KI.
- **Aufbau als Sandwich in 4 Ebenen** (gedruckte Platten 170 × 130 × 3 mm, M3-Messingbolzen).

## Wo was liegt
| Pfad | Inhalt |
|---|---|
| `README.md` | Überblick, Stufenplan, Stand |
| `docs/stueckliste.md` | Alle Teile je Stufe mit Status (bestellt / offen) |
| `docs/verdrahtung.md` | **Verbindlicher Verdrahtungsplan** – jede Leitung von Anschluss zu Anschluss, Pico-Pinbelegung |
| `docs/stromversorgung.md` | Akku, BMS, Laden, Sicherung, Verteilung, Tests vor dem ersten Anschließen |
| `docs/entscheidungen.md` | Warum etwas so gewählt wurde |
| `modell/raspberry-car-3d.html` | 3D-Modell (im Browser öffnen). Die Kabel im Modell sind aus derselben Tabelle wie `docs/verdrahtung.md` erzeugt (`WIRES` im Skript). |
| `pico/` | MicroPython für den Pico 2 W. `pins.py` ist die Pinbelegung als Code. |
| `pi/` | Software für den Pi 5 (kommt in Stufe 3) |
| `gehaeuse/` | 3D-Druckdateien (kommen, wenn die Teile vermessen sind) |

## Regeln für Änderungen
- Wenn sich eine Verbindung ändert: **`docs/verdrahtung.md`, `pico/pins.py` und die `WIRES`-Liste im 3D-Modell gemeinsam ändern**, sonst passen sie nicht mehr zusammen.
- Maße im 3D-Modell sind grob. Echte Maße erst nach dem Nachmessen der gelieferten Teile eintragen.
- Encoder-Kabelfarben sind händlerabhängig – vor dem Anschließen mit dem Datenblatt abgleichen.
- Code für den Pico in MicroPython, einfach und kommentiert (Deutsch).
- Lizenz MIT, Projekt ist öffentlich gedacht.
