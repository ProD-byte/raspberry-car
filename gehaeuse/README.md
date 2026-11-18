# Gehäuse und Druckteile

Hier kommen die Druckdateien hin (STL + Quelldateien), sobald die Teile da sind und vermessen wurden:

- 4 Platten, je ca. 170 × 130 × 3 mm, mit Löchern für M3-Bolzen (78/58 mm von der Mitte) und Kabeldurchbrüchen A (x 20, z −50, 30 × 9), B (x 20, z 50, 30 × 9), C (x −74, z 0, 9 × 30); Ebene 1 zusätzlich Loch für die Akkukabel (x −30, z 10, 16 × 7)
- Kamerahalter vorne auf Ebene 3
- Halter für die vier VL53L1X unter Ebene 1
- Motorhalter kommen mit den Motoren

Koordinaten in mm, Mitte des Autos = 0, x nach vorne, z nach links (wie im 3D-Modell).

## Befestigung der Bauteile (Löcher für die Platten)

Lochabstände sind Mitte zu Mitte. Quelle steht dabei – mit dem Messschieber an den echten Teilen prüfen, bevor gedruckt wird.

| Bauteil | Platine | Löcher | Lochabstand | Schraube | Quelle |
|---|---|---|---|---|---|
| Freenove Breakout Board (FNK0081) | 63 × 57 mm | 4 an den Ecken | **58 × 52 mm** | M3 (Messingbolzen) | offizielle mechanische Zeichnung CB8101 v1.1 von Freenove |
| Raspberry Pi 5 (8 GB) | 85 × 56 mm | 4, Ø 2,7 mm | **58 × 49 mm** | M2,5 | offizielle STEP-Datei und mechanische Zeichnung von Raspberry Pi |
| Raspberry Pi Pico 2 W | 51 × 21 mm | 4, Ø 2,1 mm | **47 × 11,4 mm** | – (steckt im Freenove-Board) | STEP-Datei von Raspberry Pi, deckt sich mit dem Datenblatt |
| Ladeboard DDTCCRUB 2S | 18 × 37 mm (mit USB-C 38,4 mm) | 4, Ø 2,4 mm | **14 × 33 mm** | M2 | BAT/GND-Ende aus der GrabCAD-Datei; die 2 Löcher am USB-Ende fehlen dort und sind gespiegelt angenommen → **nachmessen** |
| DRV8833-Modul (schwarz) | 16,8 × 18,6 mm | keine | – | doppelseitiges Schaumklebeband | GrabCAD-Datei und Produktfotos |

