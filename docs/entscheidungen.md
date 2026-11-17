# Entscheidungen

| Thema | Entscheidung | Warum |
|---|---|---|
| Ziel | Nachbau-Projekt, öffentlich, MIT | Andere sollen es nachbauen können |
| Bauweise | Nur Standardmodule, keine eigene Platine | Nachbaubar; Teile überall erhältlich |
| Verbindungen | Keine Jumperkabel/Steckbretter. Schraubklemmen mit Aderendhülsen, Löten, WAGO 221, STEMMA QT/JST | Steckverbindungen rütteln sich im fahrenden Auto los |
| Einkauf | Stück für Stück, monatlich | Budget; jede Stufe läuft für sich |
| Motorspannung | 6 V statt 12 V | Auto soll klein bleiben |
| Motoren | JGA25-370, 6 V, Encoder, Räder 65 mm (im Set) | Kompakt, kräftig genug, Encoder für Geschwindigkeit/Strecke |
| Räder | Normale Gummiräder (Panzerlenkung) | Im Motor-Set dabei; Mecanum später nachrüstbar |
| Motortreiber | DRV8833 | Günstig, reicht bei 6 V; bis 10,8 V |
| Akku | 2S2P 18650 (Samsung 35E), kein LiPo | Li-Ion im Metallgehäuse ist robuster, darf im Auto geladen werden |
| Akkuschutz | BMS 2S 20 A mit Balance | Pflicht: Überladen, Tiefentladen, Kurzschluss, Ausgleich |
| Laden | DDTCCRUB 2S, Brücken 2S + 1A | Lieferbar, sicher an jedem USB-Ladegerät; über Nacht voll |
| Akkuanzeige | INA226 mit R002 statt Spannungsteiler | Misst auch Strom → Prozent, Verbrauch, Restzeit wie bei DJI |
| Strompfade | Motoren und Pi getrennt (DRV8833 am Akku, Pi über Pololu) | Motorspitzen sollen den Pi nicht abstürzen lassen |
| UPS HAT (E) | Nicht verwendet | Gibt nur 5 V aus, 4S (16,8 V) zu viel für DRV8833, Motoren und Pi auf einer Schiene |
| Echtzeit | Pico 2 W auf Freenove-Board | Motoren/Encoder/Not-Stopp unabhängig vom Pi; WLAN-Joystick schon ab Stufe 1 |
| Gehirn | Raspberry Pi 5 (8 GB) | Kamera, SLAM, Web-App, KI |
| KI | AI HAT+ 13 TOPS (Hailo-8L) | Reicht für Objekterkennung in Echtzeit, bester Preis/Strom |
| Umgebung | 360°-LiDAR LD19 (oder RPLIDAR C1) oben auf dem Dach | Karte, Grundriss (PNG/SVG/DXF), Navigation; ±2–3 cm |
| Nahbereich | 4× VL53L1X mit STEMMA QT | Niedrige Hindernisse, die der LiDAR nicht sieht |
| Mobilfunk/GPS | SIM7600G-H als USB-Modul | Kein zweiter HAT auf dem Stapel |
| Form | Sandwich mit 4 Ebenen | Jede Ebene eigener Zweck, einzeln baubar und testbar |
| Aufbewahrung | Box von Action, innen ≥ 30 × 22 × 14 cm | |
