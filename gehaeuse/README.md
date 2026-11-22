# Gehäuse und Druckteile

Alle Druckteile entstehen aus Python-Skripten mit [build123d](https://github.com/gumyr/build123d). Oben in jedem Skript stehen die Maße als Parameter – ändern, Skript neu starten, fertig. Jedes Skript erzeugt **STL** (zum Drucken) und **STEP** (für jedes CAD-Programm).

```
pip install build123d
python ebene1_fahrwerk.py
```

Koordinaten in mm, Mitte des Autos = 0, x nach vorne, z nach links, y nach oben (wie im 3D-Modell).

## Bauweise

- **Ebene für Ebene:** Ebene 1 ist eine Wanne, das Elektronik-Deck (Ebene 2) ist zugleich ihr Deckel. Darüber kommt ein Gehäuse-Ring, dann Ebene 3 usw.
- **Außenform aller Ebenen gleich:** 250 × 180 mm, vorne bis x = +125, hinten bis x = −125. Die **Räder sitzen außen an den Seiten** (Achsen bei x = ±80, Radstand 160 mm), vorne und hinten je 45 mm Überhang.
- **Jede Ebene aus zwei Hälften** (vorne / hinten), quer geteilt: passt locker auf ein 256er-Druckbett (Bambu A1), druckt schneller und verzieht sich weniger. Die vordere Hälfte greift mit Laschen in die hintere, verschraubt mit M3. Die Fugen der Ebenen liegen versetzt.
- **Umbau fertig:** Alle drei Ebenen sind 250 × 180. Offen sind nur noch die Fahrsimulation und die Kabelwege in der Werkstatt-Ansicht Ebene 1.
- **Nur M3-Zylinderkopfschrauben (ISO 4762).** In Kunststoff schneiden sie ihr Gewinde selbst: Kernloch **2,6 mm**, Dom Ø 10 mm, mindestens 10 mm tief. Durch ein Teil hindurch: **3,4 mm**.
- **Von außen sichtbare Köpfe liegen bündig** in einer Senkung Ø 6,5 × 3,1 mm (Kopf Ø 5,5 × 3 mm). Innen dürfen die Köpfe aufliegen. Ausnahme: die Motorschrauben in der Seitenwand – die Wand ist dort nur 3 mm dick, die Köpfe sitzen hinter dem Rad. Wer sie bündig will: M3 mit flachem Kopf (DIN 7984, 2 mm hoch).
- **Material um jedes Kernloch mindestens 3,5 mm** – sonst kann der Kunststoff beim Eindrehen reißen. Alle Druckteile haben überall **3,7 mm** (nachgemessen am fertigen STL mit Messstrahlen von jeder Lochachse aus: `werkzeug/fleisch.py`, braucht `pip install trimesh rtree`).
- **Keine gekauften Halter:** Die Motoren werden direkt an die Wanne geschraubt, Module ohne Löcher sitzen in Einklick-Taschen.
- **Gut an die Kabel kommen:** Die Wanne hängt mit 4 langen Schrauben von unten am Elektronik-Deck. Zum Arbeiten an Motoren, Akku und Stromversorgung: Auto umdrehen, 4 × M3 × 45 lösen, Wanne abnehmen – alles darüber bleibt zusammengebaut.

## Ebene 1 – Fahrwerk & Energie (`ebene1_fahrwerk.py` → `ebene1/`)

In der Wanne liegt alles, was schwer ist oder mit dem Akku zu tun hat: 4 Motoren, Akku und die **komplette Stromversorgung**. Schwerpunkt ganz unten, und die dicken Akkukabel bleiben kurz.

| Datei | Anzahl | Maße | Druckrichtung | Hinweise |
|---|---|---|---|---|
| `ebene1/wanne_vorne.stl` | 1 | 137 × 180 × 42 mm | Boden unten | Ohne Stützen (geprüft): Kufen mit scharfem 45°-Knick, Sensorfenster mit 45°-Ecken, Senkungen im Boden mit Brücken-Trick, Rastnasen als Keil. Die drei Laschen an der Fuge stehen auf dem Bett. |
| `ebene1/wanne_hinten.stl` | 1 | 131 × 180 × 42 mm | Boden unten | Ohne Stützen (geprüft). Innen an der Fuge die verstärkten Seitenwände und der Block für die mittleren Schrauben. |
| `ebene1/motorbuegel.stl` | **4** | 51 × 16 × 10 mm | flach auf die große Seite | Ohne Stützen. |

**Druckeinstellungen:** PETG empfohlen (verträgt die Wärme von Motoren und Akku besser), PLA geht auch. **4 Wände/Perimeter** (damit die Schrauben gut greifen), 25 % Füllung, 0,2 mm Schichthöhe. Die Empfehlung für jedes einzelne Druckteil (Filament, Temperaturen, Wände, Füllung, Druckrichtung, Download) steht auch in den 3D-Ansichten: Druckteil antippen.

**Schrauben erreichbar – geprüft:** Jedes Ebenen-Skript prüft, ob man die Schrauben an den Fugen mit einem Schraubendreher erreicht (gedachter Schraubendreher Ø 6 × 60 mm ab dem Kopf, er darf weder Druckteile noch Bauteile treffen). Wanne: seitlich von außen, in der Mitte von innen durch die Gasse zwischen Akku und INA226. Ausgabe „Schraubendreher-Zugang – Probleme: 0“.

**Druckbar ohne Stützen – geprüft:** `python werkzeug/ueberhang.py` prüft alle Druckteile in ihrer Druckrichtung. Erlaubt sind nur Flächen, die mindestens 45° steil sind, kurze Brücken (waagerecht, an zwei Seiten aufliegend, höchstens 15 mm – z. B. die Decke eines Schlitzes) und die Oberseite kleiner runder Löcher in senkrechten Wänden bis Ø 10 mm (Wellenlöcher, Schraub-Langlöcher, Schalterloch) – die schafft jeder Drucker. Ergebnis: alle Teile „ohne Stützen druckbar“. Nach jeder Änderung an einem Druckteil neu laufen lassen.

**Was wo ist** (von oben gesehen, vorne = Kamera)
- **Motoren** liegen in 2 Sätteln, die Getriebe-Stirnseite innen an der Seitenwand. **Encoder-Stecker zeigen nach oben** – zwischen Stecker und Deck bleiben ca. 9 mm.
- **Fuge** quer bei x = +6: Die vordere Hälfte hat drei Laschen, die 18 mm in die hintere greifen – innen an beiden Seitenwänden (6 mm dick) und in der Mitte (8 mm dick, 18 mm hoch). In der hinteren Hälfte gehen die Laschen durch Schlitze im Boden, deshalb ist der Boden unten bündig. Schrauben: an jeder Seite **2 × M3 × 8** waagerecht von außen (Kopf bündig in der innen auf 6 mm verstärkten Wand), in der Mitte **2 × M3 × 16** von innen durch einen Block. Erst die beiden Hälften verschrauben, dann Motoren und Akku einbauen.
- **Akku** (2 × Keystone 1047) in der hinteren Hälfte: beide Halter hintereinander quer im Auto (z = ±40) auf 4 Sockeln, zwischen Hinterachse und Fuge.
- **4 Aufnahmekerben für den Prüfstand** unten im Boden (wie bei einer Hebebühne): zwei hinten unter dem Akku, zwei vorne unter der Stromversorgung (Mitte bei x = 3,5, Abstand 73 × 80 mm). Innen ist der Boden dort 2,5 mm dicker.
- **Links neben dem Akku:** BMS, dahinter der INA226 – beide in Einklick-Taschen (Rahmen nur an den Enden, damit die Lötpunkte frei bleiben). Der **INA226 wird ohne Stiftleiste eingebaut**: Stiftleiste nicht einlöten (oder ablöten), alle Leitungen direkt in die Lötaugen löten. So liegt er flach in der Tasche. VIN+/VIN− zeigen nach hinten (Platz bis zum Motor), die Reihe VBS…ALE nach vorne zum BMS.
- **Rechts neben dem Akku:** der Inline-Sicherungshalter für eine Standard-Flachsicherung (ca. 25 × 25,5 × 12,5 mm, mit Kabelansätzen 54 mm lang). Er steht aufrecht, der Klappdeckel zeigt nach oben – so lässt sich die Sicherung wechseln, ohne etwas auszubauen. Seine beiden Kabel werden links und rechts davon mit Kabelbindern am Boden festgebunden.
- **Zwischen Akku und Hinterachse:** 2 × WAGO 221-415 (Verteiler Plus und Minus) quer nebeneinander. Die **Kabelseite zeigt nach hinten** und ist offen, bis zum Motor sind 15 mm frei für die Leitungen; die Hebel klappen nach oben frei auf.
- **2 Nahsensoren VL53L1X** (Modul 25 × 10,7 mm) sitzen **innen** an der Stirnwand vorne und hinten, jeweils in der Mitte. Das Modul wird von oben in zwei Nuten geschoben und sitzt unten auf. Die Nuten sind **5° nach hinten geneigt**, der Sensor schaut also leicht nach oben: So sieht er auf ebenem Boden nicht den Boden selbst, und Rampen lassen sich von Wänden unterscheiden. Der Sensor zeigt zur Wand und schaut durch ein Fenster (13 × 9 mm, außen mit Rahmen). Die Lötpunkte zeigen nach oben, die Kabel werden angelötet. Außen steht nichts vor.
- **Ladeboard, Hauptschalter und USB-C zum Laden** sitzen eine Etage höher: das Ladeboard hinten auf dem Elektronik-Deck, Schalter und USB-C in der Rückwand des Gehäuse-Rings (siehe Ebene 2). Hinter den Hinterrädern ist in der Wanne kein Platz.
- **Kufen:** Der Boden ist vorne und hinten gleich schräg hochgezogen: 45° auf den letzten 8,5 mm, der Übergang ist gerundet, und die Fase läuft ringsum durch. Steine und Kanten zwischen den Rädern rutschen so unter die Wanne, statt an einer Kante hängen zu bleiben – und es sieht schnittiger aus. Innen steigt der Boden dort mit an (Platte bleibt 3 mm dick).
- 4 **Säulen** für die Schrauben zum Deck (2 vorne, 2 hinten). Sie stehen nicht frei, sondern gehen in die Stirnwand über und sind in voller Breite (10 mm) über die ganze Höhe mit der Stirnwand verbunden – so können sie nicht abbrechen oder sich biegen.
- 2 Paar **Kabelbinder-Schlitze im Boden** (links und rechts vom Sicherungshalter, für seine beiden Kabel): Den Kabelbinder **von unten** durch einen Schlitz nach oben, um das Kabel herum und durch den zweiten Schlitz wieder nach unten führen. Unten liegt er in einer flachen Rille bündig im Boden, der Kopf bleibt innen. Innen steht nichts im Weg, und von unten kommt man überall gut heran.
- Die Langlöcher in der Wand passen für 15,4 bis 17 mm Lochabstand der Getriebe-Gewinde (je nach Händler).

**Zusammenbau**
1. Motoren von innen in die Sättel legen, Lagerbund in das Ø-8-Loch der Seitenwand, Stecker nach oben.
2. Je Motor 2 × **M3 × 6** von außen durch die Langlöcher in die Getriebe-Stirnseite (Gewinde 3,5 mm tief – **nicht länger als 6 mm!**).
3. Motorbügel auflegen, je 2 × **M3 × 8** – schneiden sich das Gewinde selbst.
4. Akkuhalter auf die 4 Sockel, je 2 × **M3 × 8** von unten durch Boden und Sockel (Kopf bündig), **Mutter M3** innen auf dem Halterboden.
5. BMS, INA226 und WAGOs in ihre Taschen drücken, verdrahten nach `docs/verdrahtung.md`. Die Leitungen zum Hauptschalter und zum Ladeboard (BAT/GND) gehen durch die hintere Öffnung im Deck nach oben.
6. Kabel mit Kabelbindern durch die Bodenschlitze sichern (von unten einfädeln), die Leitungen nach oben durch die Öffnungen im Deck führen.
7. Elektronik-Deck auflegen, Auto umdrehen, 4 × **M3 × 45** von unten durch die Säulen der Wanne in die Dome des Decks. Die Köpfe sitzen versenkt in der Schräge der Kufen.

**Schrauben für Ebene 1:** 8 × M3 × 6, 12 × M3 × 8, 4 × M3 × 45, 4 × Mutter M3.

**Im 3D-Modell ansehen:** `modell/raspberry-car-3d.html` → Knopf **„Druckteile“**. Zeigt nur die Druckteile; Regler „Auseinanderziehen“, der Haken blendet Motoren, Räder, Akku und Stromversorgung zum Prüfen ein.

Halter für die Nahsensoren sind nach dem GrabCAD-Modell eingeplant – nach der Lieferung kurz nachmessen (Platinendicke, Lage des Sensors).

## Prüfstand (`pruefstand.py` → `pruefstand/`)

Zum Testen von Motoren, Encodern und Software, ohne dass das Auto vom Tisch fährt. Funktioniert wie eine **Hebebühne**: Das Auto steht auf 4 Stempeln, die **Räder hängen 19 mm über dem Tisch** und drehen frei.

| Datei | Anzahl | Maße | Druckrichtung | Hinweise |
|---|---|---|---|---|
| `pruefstand/pruefstand.stl` | 1 | 112 × 112 × 37,5 mm | so wie er steht | Ein Teil, ohne Schrauben, ohne Stützen – passt auf jedes Druckbett. Ca. 98 cm³. |

- **Rutscht nicht:** Unten im Wannenboden sind 4 Kerben (8 × 6 mm, 3 mm tief, unter dem Akku bei x = ±32, z = ±35). Auf jedem Stempel sitzt ein angefaster Zapfen (0,3 mm Luft), der in seine Kerbe einrastet. Innen ist der Wannenboden an den 4 Stellen verstärkt, über jeder Kerbe bleiben 2,5 mm Material.
- **Liegt nur auf den Stempeln:** Zwischen den Stempeln bleiben 2 mm Luft zum Wannenboden.
- **Räder frei:** 19 mm Luft unter den Rädern, der Sockel reicht nicht unter die Räder (knapp 15 mm Abstand zur Radinnenseite).
- Sockel mit Fase und Schriftzug („PRÜFSTAND“ / „RASPBERRY CAR“), zwei Querwände mit Fenstern (oben 45°-Dach, druckt ohne Stützen).
- Im 3D-Modell: `modell/ebene1-unten.html` → Haken **„Auf dem Prüfstand“**.

## Ebene 2 – Elektronik-Deck (`ebene2_elektronik.py` → `ebene2/`)

Das Deck ist der **Deckel der Wanne** (liegt auf dem Wannenrand bei 58 mm). Darüber beginnt Ebene 3 bei 84 mm.

| Datei | Anzahl | Maße | Druckrichtung | Hinweise |
|---|---|---|---|---|
| `ebene2/platte_vorne.stl` | 1 | 67 × 180 × 13 mm | Unterseite aufs Bett | Ohne Stützen. Motorzone vorne, an der Fuge der Steg mit den Gewindelöchern. |
| `ebene2/platte_hinten.stl` | 1 | 183 × 180 × 13 mm | Unterseite aufs Bett | Ohne Stützen. Pico, Kompass, MP1584, Motorzone hinten, Ladeboard. |
| `ebene2/ring_vorne.stl` | 1 | 141 × 180 × 36 mm | **aufrecht** (Unterkante aufs Bett) | Ohne Stützen. Vorne die zwei Laschen für die Schrauben des Klappdeckels (unten 45°-Schräge). |
| `ebene2/ring_hinten.stl` | 1 | 119 × 180 × 33 mm | **aufrecht** | Ohne Stützen. Scharnier-Lappen hinten (unten 45°-Schräge), USB-C-Ausschnitt und Loch für den Hauptschalter. |

**Zwei Hälften:** Das **Deck** ist bei x = +58 geteilt (zwischen Freenove-Board und vorderer Motorzone). An der Fuge steht auf jeder Hälfte ein 10 mm hoher Steg (außen, zwischen den Grifflöchern frei); die Stege werden mit **2 × M3 × 10** quer verschraubt (Kopf hinten, Gewinde im vorderen Steg; bei z = −54 und +64, dahinter ist für den Schraubendreher frei). Der **Ring** ist bei x = −16,5 geteilt, also weit weg von der Fuge des Decks. Jede Ring-Hälfte hat eigene Hülsen und ist mit eigenen **M3 × 20** von oben auf das Deck geschraubt (vorne in den Ecken, hinten an der Rückwand und je zwei an der Fuge des Rings). So überbrückt der Ring die Fuge des Decks und das Deck die Fuge des Rings. Die Fuge der Wanne liegt wieder woanders (x = +6).

**Aufteilung in Zonen** – alles gut erreichbar, nichts liegt kreuz und quer:

| Zone | Wo | Was |
|---|---|---|
| Motorzone vorne | über der Vorderachse (x = 80) | **zwei Grifflöcher**, je eines über einem Motorstecker; dazwischen der **DRV8833 vorne** (treibt beide Vordermotoren), rechts außen der **3,3-V-Verteiler vorne** (Encoder der Vordermotoren) |
| Motorzone hinten | über der Hinterachse (x = −80) | genauso: zwei Grifflöcher, **DRV8833 hinten**, **3,3-V-Verteiler hinten** (Encoder der Hintermotoren, BNO085, INA226) |
| Steuerung | Mitte | vorne der **Pico 2 W auf dem Freenove-Board** (Klemmen-Reihen zeigen zu den Seiten), dahinter der **Kompass BNO085** (um 90° gedreht) |
| Strom und Laden | Rand | vorne rechts der **MP1584** am Strom-Durchbruch **C** (über den Verteilern in der Wanne), hinten links das **Ladeboard**, hinten rechts der **Hauptschalter** |

**Gut erreichbar – Ebene 3 als Klappdeckel:** Hinten am Ring sitzen die Scharnier-Lappen, vorne zwei Laschen für die Schrauben des Deckels. Schrauben lösen, Deckel hochklappen – dann liegen alle Klemmen offen, und durch die vier Grifflöcher steckt man die Motorstecker direkt am Motor ein und aus.

**Erreichbarkeit – vom Skript geprüft:** `ebene2_elektronik.py` prüft bei jedem Lauf nicht nur, ob sich etwas überschneidet, sondern auch, ob man herankommt (Ausgabe „Erreichbarkeit – Probleme: 0“):

| Was | verlangt frei | Hindernis zählt ab |
|---|---|---|
| vor jeder Freenove-Klemmen-Reihe (Kabel mit Aderendhülse) | 13 mm | 6 mm Höhe |
| vor der Kabelseite jedes WAGO | 15 mm | 2 mm Höhe |
| vor jeder STEMMA-QT-Buchse des Kompasses | 12 mm | 2 mm Höhe |
| rund um jedes Griffloch (Finger) | 4 mm + Rand | 6 mm Höhe |
| unter dem Hauptschalter (ragt 25 mm nach innen) | ganze Länge | 6,5 mm Höhe |

Außerdem prüft es, dass nichts über der Fuge des Decks liegt (außer den Stegen), und dass man die Schrauben an der Fuge mit einem Schraubendreher erreicht. Module mit Lötanschlüssen (DRV8833, MP1584, Ladeboard) klickt man zum Löten heraus – ihre Kabel bekommen dafür ein paar Zentimeter Reserve.

**Was darauf sitzt**
- **Freenove-Board mit Pico 2 W** vorne in der Mitte (x = 20) auf 4 gedruckten Domen (4 mm hoch), 4 × **M3 × 8**. Die Klemmen-Reihen zeigen zu den Seiten.
- **Einklick-Taschen** für alle Module ohne Löcher: 2 × DRV8833, MP1584, BNO085, 2 × WAGO 221-415 (3,3 V) und das Ladeboard. Passgenauer Rahmen (0,3 mm Luft), Rastnasen als Keil, eine Kerbe zum Heraushebeln.
- **Grifflöcher** (28 × 20 mm, mit 2 mm hohem Rand) genau über jedem Motorstecker – bei der breiten Wanne liegen die beiden Stecker einer Achse 60 mm auseinander, deshalb vier Grifflöcher.
- **DRV8833** je Achse mittig zwischen den beiden Grifflöchern. OUT1/OUT2 = linker Motor, OUT3/OUT4 = rechter Motor dieser Achse.
- **WAGO-Taschen (3,3 V)** rechts außen, die **Kabelseite ist offen und zeigt nach außen**, die Rückwand ist nur 4 mm hoch (Hebel klappen frei auf).
- **BNO085 (Kompass)** hinten in der Mitte (x = −35): ca. 12 cm von Durchbruch C und von den Verteilern in der Wanne, ca. 5 cm vom hinteren Motor. Darunter liegt in der Wanne (4 cm tiefer) der Akku – ob sein Strom stört, zeigt erst ein Test mit dem echten Auto (BNO085 kalibrieren und beim Fahren beobachten).
- **MP1584** rechts hinter dem Freenove-Board (x = −24), ca. 6 cm vom Kompass. Er sitzt bewusst nicht vor der rechten Schraube an der Deck-Fuge, damit dort der Schraubendreher Platz hat.
- **Kabelwege nach unten in die Wanne:** die vier Grifflöcher (Motorkabel, XSHUT der Nahsensoren), **D** links vor dem Pico (Daten vom INA226), **S** hinten rechts (Leitungen zum Hauptschalter), **B** hinten links (BMS → Ladeboard), **C** vorne rechts (x = 40, z = −68: Plus und Minus von den Verteilern – immer paarweise nebeneinander).
- **Ladeboard DDTCCRUB 2S** hinten links (z = 60): Die Platine liegt **bündig an der Innenseite der Rückwand**, die USB-C-Buchse steckt im Ausschnitt der Wand (13,5 × 8 mm, außen angefast) und sitzt nur 1 mm hinter der Außenseite. Die innere Ecke des Rings ist dort enger gerundet.
- **Rückwand des Gehäuse-Rings:** in Fahrtrichtung rechts der **Hauptschalter** (runder Taster Ø 12 mm, Loch Ø 12,2 mm, z = −55), links die **USB-C-Buchse** des Ladeboards (z = +60). Reihenfolge beim Zusammenbau: erst das Ladeboard einklicken, dann den Ring aufsetzen.
- Die Kabellängen vom Motorstecker werden nach dem Neubau neu ausgemessen.

- Im 3D-Modell: `modell/ebene2-oben.html` (Werkstatt-Ansicht nur für Ebene 2).

**Befestigung**
- Unten: 4 Dome (Kernloch von unten, 11 mm tief) über den Säulen der Wanne – dort greifen die 4 × M3 × 45 der Wanne von unten.
- Oben: der **Gehäuse-Ring** schließt die Seiten bis Ebene 3. Seine Röhren sind **Hülsen** (Ø 13 mm) über 8 Domen des Decks (8 mm hoch, Kernloch 11 mm tief): vorne in den Ecken (x = 113,5 / z = ±82,6), hinten an der Rückwand (x = −117,6 / z = ±23,3, beim Scharnier) und an den Seiten bei der Fuge des Rings (x = −4,5 und −28,5 / z = ±82,6). Jede Hülse geht von unten bis oben und ist mit der Außenwand verbunden.

Alle Kernlöcher haben mindestens **3,5 mm Material** rundum. Die Lage aller Taschen, Dome und Durchbrüche prüft das Skript selbst auf Überschneidungen (Ausgabe „Überschneidungen: 0“).

**Schrauben für Ebene 2:** 4 × M3 × 8 (Freenove-Board), 2 × M3 × 10 (Stege an der Fuge des Decks), 8 × M3 × 20 (Ring aufs Deck). Die Schrauben zur Wanne zählen bei Ebene 1.

## Ebene 3 – Gehirn mit Dach, Klapphaube (`ebene3_gehirn.py` → `ebene3/`)

Die oberste Ebene ist eine **Haube**: Seitenwände und Dach in einem, **unten offen**. Eine eigene vierte Ebene gibt es nicht mehr – das Dach der Haube trägt oben den LiDAR. Die Haube klappt hinten nach oben auf, dann liegt Ebene 2 offen.

| Datei | Anzahl | Maße | Druckrichtung | Hinweise |
|---|---|---|---|---|
| `ebene3/haube_vorne.stl` | 1 | 80 × 180 × 37 mm | **Dach nach unten** (aufs Bett) | Ohne Stützen. Kamera, Status-LEDs, Pololu, Schraubpolster vorne. |
| `ebene3/haube_hinten.stl` | 1 | 180 × 180 × 37 mm (mit Scharnier-Lappen) | **Dach nach unten** | Ohne Stützen. Pi-Dome, 4G- und GPS-Tasche, Display, Scharnier-Lappen (mit 45°-Keil). |

- **Form:** Vorder- und Rückwand senkrecht (vorne das Kamerafenster, hinten das Scharnier). Die Seiten sind unten 12 mm senkrecht und laufen dann schräg nach innen (oben je 7 mm schmaler), alle Dachkanten sind 45° abgeschrägt. Höhe 84 → 121 mm, mit LiDAR ca. 155 mm.
- **Alles hängt am Dach** (beim Druck wachsen die Halter vom Bett nach oben – keine Stützen):
  - **Raspberry Pi 5** mit Active Cooler und AI HAT+: Der Stapel hängt an 4 Domen. **M2,5 × 16 von oben** durch Dach, Dom und AI HAT+ in die 16-mm-Abstandshalter (liegen dem HAT bei), Köpfe bündig im Dach (Senkung mit Brücken-Trick). Unten hält der Pi mit den beiliegenden Schrauben. Ausnahme von „nur M3“, weil die Löcher des Pi nur 2,7 mm groß sind.
  - **Kamera Modul 3 Wide** vorne in zwei Nuten, von unten einschieben bis sie über eine kleine Nase schnappt. Fenster Ø 18 mm (gerade Kante unten), außen angefast.
  - **Pololu D36V50F5**, **4G-Modul** (Waveshare SIM7600G-H, nur die Platine, liegt flach; Stirnseiten offen für USB-Stecker und SMA-Buchse) und **GPS-Antenne** in Einklick-Taschen. Die GPS-Antenne empfängt durch das Dach.
  - **Status-LEDs** (WS2812-Streifen) vorne in einer flachen Tasche, sie leuchten durch 4 Löcher Ø 3 mm.
  - **Rundes Display** hinten: Das Glas liegt von innen am Dach an und schaut durch ein Loch Ø 44,4 mm (außen angefast), 3 Schnapphaken halten die Platine.
  - **LiDAR LD19** oben auf dem Dach, Kabel durch ein Loch Ø 10 nach innen. Seine Befestigungslöcher kommen nach dem Nachmessen.
- **Scharniere hinten:** zwei Scharniere außen an der Trennfuge, Achse 5,5 mm hinter der Rückwand und 5 mm über der Fuge. Je Scharnier zwei Lappen an der Haube, einer am Ring von Ebene 2, Achse **M3 × 16** (Gewinde im äußeren Lappen). Das Skript prüft in 10°-Schritten bis 100°, dass beim Aufklappen nichts anstößt.
- **Vorne zwei M3 × 12** waagerecht durch die Vorderwand (Köpfe bündig) in die Laschen des Rings von Ebene 2.
- **Kabel:** Die Haube ist unten offen – alle Kabel von Ebene 2 laufen hinten beim Scharnier nach oben, dort knicken sie beim Aufklappen am wenigsten.
- **Luft:** senkrechte Lüftungsschlitze in beiden Seitenwänden (der AI HAT+ braucht Luft). Unter Pi und Kamera bleiben bis Ebene 2 gut 10 mm frei.
- **Zwei Hälften:** Fuge bei x = +45 (wieder an einer anderen Stelle als Wanne, Deck und Ring). Innen hat jede Hälfte an Dach und Seiten einen 10 mm breiten Rand; beide werden mit **6 × M3 × 12** verschraubt (bei aufgeklappter Haube). Fünf Köpfe sitzen hinten, die Schraube links am Dach von vorne – hinter ihr liegt das 4G-Modul.

Im 3D-Modell: `modell/ebene3-gehirn.html` (Werkstatt-Ansicht mit Regler zum Aufklappen).

**Schrauben für Ebene 3:** 2 × M3 × 16 (Scharniere), 2 × M3 × 12 (vorne), 6 × M3 × 12 (Fuge), 4 × M2,5 × 16 (Pi-Stapel von oben, plus die Abstandshalter des AI HAT+).

## Befestigung der Bauteile (Löcher für die Platten)

Lochabstände sind Mitte zu Mitte. Quelle steht dabei – mit dem Messschieber an den echten Teilen prüfen, bevor gedruckt wird.

| Bauteil | Platine | Löcher | Lochabstand | Schraube | Quelle |
|---|---|---|---|---|---|
| Freenove Breakout Board (FNK0081) | 63 × 57 mm | 4 an den Ecken | **58 × 52 mm** | M3 (Messingbolzen) | offizielle mechanische Zeichnung CB8101 v1.1 von Freenove |
| Raspberry Pi 5 (8 GB) | 85 × 56 mm | 4, Ø 2,7 mm | **58 × 49 mm** | M2,5 | offizielle STEP-Datei und mechanische Zeichnung von Raspberry Pi |
| Raspberry Pi Pico 2 W | 51 × 21 mm | 4, Ø 2,1 mm | **47 × 11,4 mm** | – (steckt im Freenove-Board) | STEP-Datei von Raspberry Pi, deckt sich mit dem Datenblatt |
| Ladeboard DDTCCRUB 2S | 18 × 37 mm (mit USB-C 38,4 mm) | 4, Ø 2,4 mm | **14 × 33 mm** | M2 | BAT/GND-Ende aus der GrabCAD-Datei; die 2 Löcher am USB-Ende fehlen dort und sind gespiegelt angenommen → **nachmessen** |
| Akkuhalter Keystone 1047 (2 Stück) | 77,1 × 39,8 × 18 mm | 2, Ø 3,2 mm im Mittelsteg | **55,2 mm** (längs, mittig) | M3 + Mutter | Keystone-Datenblatt K75p29 |
| DRV8833-Modul (schwarz) | 16,8 × 18,6 mm | keine | – | doppelseitiges Schaumklebeband | GrabCAD-Datei und Produktfotos |
| Waveshare SIM7600G-H 4G DONGLE (nur Platine) | 82,3 × 40,2 × 1,6 mm | keine | – | steht in 2 Nut-Säulen | offizielles 3D-Modell von Waveshare |
| Motorhalterung JGA25-370 (L-Form) | Motorplatte 26 × 26 × 3 mm | Wellenloch Ø 8 mm + 2 × M3 | **15,4 mm** (in die Getriebe-Stirnseite) | M3 | GrabCAD-Modell; die Löcher der oberen Platte sind dort nicht gezeichnet → **am echten Teil messen** |

## Schrauben

Wir verwenden **M3-Zylinderkopfschrauben mit Innensechskant nach ISO 4762 (DIN 912)**. Maße laut Norm:

| Maß | Wert |
|---|---|
| Gewinde | M3 |
| Kopfdurchmesser | 5,5 mm |
| Kopfhöhe | 3 mm |
| Innensechskant | Schlüsselweite 2,5 mm |
| Durchgangsloch in gedruckten Teilen | 3,2–3,4 mm (mittel) |
| Senkung für versenkten Kopf | Ø 6,0–6,5 mm, 3,2 mm tief |

Die Schrauben werden bei der Gehäuseplanung im 3D-Modell genau nach diesen Normmaßen gezeichnet (Längen je nach Stelle).
