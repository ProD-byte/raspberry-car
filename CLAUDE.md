# Raspberry Car – Hinweise für Claude

Dieses Projekt ist ein **Nachbau-Projekt**: ein kleines, vierrädriges Roboterauto, das sich wie eine DJI-Drohne anfühlen soll (Live-Video, Karte, „Folge mir“, „Nach Hause fahren“). Andere sollen es mit gekauften Standardmodulen nachbauen können.

## Zusammenarbeit
- **Arbeitsort: `C:\Projekte\raspberry-car`** (lokal). HiDrive ist seit 22.11.2026 per WebDAV als Laufwerk H: verbunden und **nur Sicherung**: `H:\users\tank-1841\Kreativ und Basteln\Elektronik\raspberry-car` – dort nicht arbeiten, keine Terminals mit H: als Arbeitsordner starten, keine Passwörter oder Schlüssel auf H: ablegen. Sichern mit `robocopy "C:\Projekte\raspberry-car" "H:\users\tank-1841\Kreativ und Basteln\Elektronik\raspberry-car" /E /R:10 /W:5 /XD __pycache__` (Exit-Code 1–3 = Erfolg; nichts auf H: löschen ohne Rückfrage).
- Sprache: **Deutsch**, einfach und verständlich erklären. Der Bauherr kann löten (auch SMD), programmiert aber nicht beruflich.
- Eingekauft wird **Stück für Stück, jeden Monat etwas** (Budget pro Monat oft ~50 €). Immer sagen, was jetzt nötig ist und was warten kann.
- Vor dem Bestellen Screenshots der gewählten Variante prüfen (Spannung, Encoder, 2S/3S usw.).
- Nichts anschließen lassen, bevor es einen Verdrahtungsplan gibt.

## Feste Entscheidungen (nicht ohne Rückfrage ändern)
Siehe `docs/entscheidungen.md`. Kurz:
- **Keine Jumperkabel, keine Steckbretter.** Verbindungen über Schraubklemmen (mit Aderendhülsen), Lötstellen, WAGO-Hebelklemmen oder verriegelnde Stecker (STEMMA QT, JST).
- **Nur Standardmodule**, keine eigene Platine – damit es nachbaubar bleibt.
- **Motoren 6 V: JGA25-370 mit Encoder, 130 U/min** (Getriebe 1:46,8), **Räder 85 mm** (seit 22.11.2026 – vorher 280 U/min mit 65 mm: für das 1,9 kg schwere, breite Auto zu schwach zum Drehen auf Teppich). Später für den Garten 100-mm-Geländeräder auf dieselben Motoren.
- **Akku: 2S2P aus 4× Samsung INR18650-35E** (kein LiPo), mit **BMS 2S 20 A Balance** und **Ladeboard DDTCCRUB 2S** (Lötbrücken 2S und 1A).
- **Motoren und Pi haben getrennte Stromwege** (DRV8833 direkt am Akku, Pi über eigenen Pololu-Wandler), damit Motorspitzen den Pi nicht zum Absturz bringen. Deshalb **kein** Waveshare UPS HAT.
- **Pico 2 W** (auf Freenove Breakout Board) = Echtzeit: Motoren, Encoder, Sensoren, Not-Stopp. **Pi 5** = Gehirn: Kamera, LiDAR-Karte, Navigation, Web-App, KI.
- **Vorne/hinten:** Hinten = Seite mit Ladebuchse (USB-C) und Hauptschalter, vorne = Nahsensor und Kamera. In allen Skripten zeigt x nach vorne.
- **Aufbau als Sandwich in 3 Ebenen** (gedruckte Ebenen **250 × 180 mm**, Radstand 160 mm, Räder 85 mm außen; Wanne unten mit der kompletten Stromversorgung, Ebene 2 Antrieb, Ebene 3 Gehirn mit Dach als Klappdeckel; Säulen mitgedruckt, nur M3-Zylinderkopfschrauben ISO 4762). Möglichst flach bauen – kein Turm. **Jede Ebene aus zwei Druckteilen** (vordere / hintere Hälfte, quer geteilt, überlappende Laschen + M3), Fugen je Ebene versetzt. Drucker: Bambu A1 (256 × 256 mm).
- **Umbau auf 250 × 180 (22.11.2026) fertig:** Ebene 1–3, großes 3D-Modell, Werkstatt-Ansichten (mit Kabelwegen) und Fahrsimulation sind auf dem neuen Stand.
- **Schrauben müssen erreichbar sein:** Jedes Ebenen-Skript prüft „Schraubendreher-Zugang“ (gedachter Schraubendreher Ø 6 × 60 mm ab jedem Kopf der Fugen-Schrauben darf weder Druckteile noch Bauteile treffen). Neue Schrauben dort mit eintragen; Ergebnis muss „Probleme: 0“ sein.

## Wo was liegt
| Pfad | Inhalt |
|---|---|
| `README.md` | Überblick, Stufenplan, Stand |
| `docs/stueckliste.md` | Alle Teile je Stufe mit Status (bestellt / offen) |
| `docs/verdrahtung.md` | **Verbindlicher Verdrahtungsplan** – jede Leitung von Anschluss zu Anschluss, Pico-Pinbelegung |
| `docs/stromversorgung.md` | Akku, BMS, Laden, Sicherung, Verteilung, Tests vor dem ersten Anschließen |
| `docs/entscheidungen.md` | Warum etwas so gewählt wurde |
| `modell/raspberry-car-3d.html` | 3D-Modell (im Browser öffnen). Die Kabel im Modell sind aus derselben Tabelle wie `docs/verdrahtung.md` erzeugt (`WIRES` im Skript). |
| (Ansicht) | Das 3D-Modell startet mit „Vorhandene Teile“. Kommt ein Teil an: in der Liste `VORHANDEN` im Skript eine Zeile ergänzen und in der Stückliste auf 📦 setzen. |
| `modell/ebene1-unten.html` | **Werkstatt-Ansicht**: nur der Bereich, an dem gerade gebaut wird (zurzeit Ebene 1), ohne Kabel. Bauteile und Positionen wie im großen Modell – ändert sich dort etwas an Ebene 1, hier mit ändern. |
| `modell/ebene2-oben.html` | **Werkstatt-Ansicht Ebene 2**: nur das Elektronik-Deck mit Ring und Bauteilen, ohne Kabel; Haken für Kompass-Freiraum, Höhe von Ebene 3 und die Wanne darunter. Die Bauteile werden aus `raspberry-car-3d.html` kopiert: nach Änderungen an Ebene 2 dort `python modell/werkzeug/mach_ebene2.py` laufen lassen (erzeugt die Seite neu). |
| `modell/ebene3-gehirn.html` | **Werkstatt-Ansicht Ebene 3**: Klapphaube (Dach integriert, unten offen) mit allem, was am Dach hängt (Pi, AI HAT+, Kamera, Pololu, 4G, GPS, LEDs, Display) und dem LiDAR oben, Regler zum Aufklappen, Ebene 2 darunter. Wird erzeugt: nach Änderungen an Ebene 3 im großen Modell `python modell/werkzeug/mach_ebene3.py` laufen lassen. Deckel-Druckteil: `gehaeuse/ebene3_gehirn.py` (prüft das Aufklappen bis 100°). |
| `gehaeuse/pruefstand.py` | Prüfstand (Druckteil) wie eine Hebebühne: 4 Zapfen rasten in 4 Kerben unten in der Wanne (`PRUEF_PUNKTE` in `ebene1_fahrwerk.py` – bei Änderung in beiden Skripten gleich halten), Räder hängen frei – zum Testen von Motoren und Software. In der Werkstatt-Ansicht per Haken „Auf dem Prüfstand“. Die Werkstatt-Ansicht zeigt per Haken „Verkabelung“ auch die ordentlich verlegten Kabel in der Wanne (Wege von Hand festgelegt, Anschlüsse wie in `docs/verdrahtung.md` – bei Änderungen dort auch hier nachziehen). |
| `modell/fahrsimulation.html` | **Fahrsimulation**: das Fahrwerk (Ebene 1) auf Gelände (Wohnzimmer, Garten, Testparcours) – Panzerlenkung mit Schlupf, Auflage auf 3/4 Rädern, Bodenfreiheit, Stufen, Steigung, Kippen, Stromschätzung. Enthält eine Kopie der Ebene-1-Bauteile aus `ebene1-unten.html` – bei Änderungen an Fahrwerk-Maßen (Radstand, Spur, Bodenfreiheit) die Werte oben im Simulationsteil mit ändern. Ebene 2 und Ebene 3 sind mit allen Bauteilen aufgesetzt (Haken „Ebene 2“, „Ebene 3“, „Haube durchsichtig“ – anfangs durchsichtig, damit man die Bauteile sieht): nach Änderungen an Ebene 2 oder 3 im großen Modell `python modell/werkzeug/sim_ebene2.py` laufen lassen. Fahrzeugdaten (Radstand 160, Spur 224, Räder Ø 85, Masse ca. 1,9 kg geschätzt, Schwerpunkt ca. 66 mm) stehen oben im Simulationsteil; Labyrinth-Felder 50 cm. |
| `modell/teile/druckteile.js` | Druck-Infos je Druckteil (Filament, Temperaturen, Einstellungen, Druckrichtung, Download-Link). Erscheinen in allen 3D-Ansichten beim Antippen eines Druckteils – bei neuen Druckteilen hier eintragen. |
| `gehaeuse/werkzeug/ueberhang.py` | Prüft, ob alle Druckteile **ohne Stützen** druckbar sind (Liste `TEILE` mit Druckrichtung). Nach jeder Änderung an Druckteilen laufen lassen; neue Druckteile dort ergänzen. |
| `modell/teile/` | Echte CAD-Modelle (.glb, aus STEP umgewandelt) + `teile.js` (eingebettet, damit es per Doppelklick läuft). GrabCAD-Modelle liegen in `modell/teile/lokal/` und sind **nicht im Git** (Lizenz). Quellen und Werkzeuge: `modell/teile/QUELLEN.md` |
| `pico/` | MicroPython für den Pico 2 W. `pins.py` ist die Pinbelegung als Code. |
| `pi/` | Software für den Pi 5 (kommt in Stufe 3) |
| `gehaeuse/` | 3D-Druckdateien (kommen, wenn die Teile vermessen sind) |

## Regeln für Änderungen
- Wenn sich eine Verbindung ändert: **`docs/verdrahtung.md`, `pico/pins.py` und die `WIRES`-Liste im 3D-Modell gemeinsam ändern**, sonst passen sie nicht mehr zusammen.
- Maße im 3D-Modell sind grob. Echte Maße erst nach dem Nachmessen der gelieferten Teile eintragen.
- Encoder-Kabelfarben sind händlerabhängig – vor dem Anschließen mit dem Datenblatt abgleichen.
- Code für den Pico in MicroPython, einfach und kommentiert (Deutsch).
- Lizenz MIT, Projekt ist öffentlich gedacht.
