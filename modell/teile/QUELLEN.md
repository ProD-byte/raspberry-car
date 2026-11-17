# Echte CAD-Modelle für das 3D-Modell

Die `.glb`-Dateien sind aus den STEP-Dateien der Hersteller umgewandelt (Maße 1:1 in mm, Farben aus der STEP-Datei).
`teile.js` enthält dieselben Dateien als Base64, damit `raspberry-car-3d.html` auch per Doppelklick (ohne Webserver) die echten Modelle zeigt.
Fehlt `teile.js` oder ist man offline, zeigt das Modell automatisch die einfachen Ersatzteile.

| Datei | Bauteil | Quelle | Lizenz / Hinweis |
|---|---|---|---|
| `pico2w.glb` | Raspberry Pi Pico 2 W | STEP-Datei „Pico W“ von Raspberry Pi: https://pip.raspberrypi.com/documents/RP-008318-DS (Stand 11.08.2023) | Raspberry Pi bietet für den Pico 2 W keine eigene STEP-Datei an. Pico 2 W und Pico W haben dieselbe Platine und dieselben Maße, nur der Hauptchip ist anders (RP2350 statt RP2040). Die Datei hat keine eigene Lizenzdatei. Die STEP-Datei des Pico 2 (RP-009061-CA) steht unter MIT. |

## Nur lokal: GrabCAD-Modelle (`lokal/`, nicht im Git)

GrabCAD-Modelle dürfen für eigene Projekte genutzt werden. Eine Weitergabe der (umgewandelten) Dateien in einem öffentlichen Repository erlauben die GrabCAD-Nutzungsbedingungen aber nicht ausdrücklich.
Deshalb liegen sie in `modell/teile/lokal/` (steht in `.gitignore`). Wer das Projekt klont, sieht an ihrer Stelle die nachgebauten Ersatzteile (Maße nach Datenblatt/Fotos) – oder lädt die Dateien selbst von GrabCAD und wandelt sie wie unten um.

| Datei | Bauteil | Quelle | Hinweise |
|---|---|---|---|
| `lokal/ddtccrub.glb` | Ladeboard DDTCCRUB 2S (Walfront, Amazon B08LVN7FLH) | GrabCAD, Aleksey Zablotskiy: https://grabcad.com/library/2s-3s-4s-boost-lipo-liion-charger-ddtccrub-1 – Datei `DDTCCRUB CN330X.STEP` | Vom Autor als vereinfachtes Modell bezeichnet. 18 × 37 mm Platine (mit USB-C 38,4 mm). Die grüne Farbe wird im Skript an die Fotos angepasst. |
| `lokal/drv8833.glb` | DRV8833-Modul, schwarz (MakerMind, roboter-bausatz.de RBS12954) | GrabCAD, Juan Manuel Dominici: https://grabcad.com/library/drv8833-dual-h-bridge-motor-driver-doble-puente-h-1 – Datei `Modulo_DRV8833_A.stp` | Stiftleisten beim Umwandeln entfernt (`--ohne 4,4,4 134,90,20`), weil die Kabel direkt eingelötet werden. 18,6 × 16,8 mm. |

**Ersatzteile im Skript** (wenn `lokal/` fehlt):
- DRV8833: nach Produktseite (16 × 18,5 mm) und Fotos, Raster 2,54 mm, Reihenabstand 15,24 mm, Pinfolge laut Aufdruck.
- Ladeboard: nach Händlerangaben baugleicher Boards (39 × 18 × 6,3 mm) und Produktfotos.

**Mit den echten Teilen nachmessen**, bevor Platten gedruckt werden.

## Neues Teil hinzufügen

Im Ordner `modell/teile`. Einmalig: `python -m venv venv` und dann `venv\Scripts\pip install cadquery-ocp trimesh numpy`

```
venv\Scripts\python werkzeug\step2glb.py teil.step roh.glb 0.08     # STEP -> GLB (0,08 mm Genauigkeit)
venv\Scripts\python werkzeug\merge_glb.py roh.glb NAME.glb [--ohne R,G,B] # gleiche Farben zusammenfassen = kleiner
python werkzeug\einbetten.py                                        # teile.js und lokal/teile-lokal.js neu erzeugen
```

Im Skript dann `cadTeil('NAME', gruppe, ersatzGruppe, (m) => { …ausrichten… })` aufrufen (Beispiel: Pico im Abschnitt `freenove()`).
