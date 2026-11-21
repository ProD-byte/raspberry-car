# Gehäuse und Druckteile

Alle Druckteile entstehen aus Python-Skripten mit [build123d](https://github.com/gumyr/build123d). Oben in jedem Skript stehen die Maße als Parameter – ändern, Skript neu starten, fertig. Jedes Skript erzeugt **STL** (zum Drucken) und **STEP** (für jedes CAD-Programm).

```
pip install build123d
python ebene1_fahrwerk.py
```

Koordinaten in mm, Mitte des Autos = 0, x nach vorne, z nach links, y nach oben (wie im 3D-Modell).

## Bauweise

- **Ebene für Ebene:** Ebene 1 ist eine Wanne, das Elektronik-Deck (Ebene 2) ist zugleich ihr Deckel. Darüber kommt ein Gehäuse-Ring, dann Ebene 3 usw.
- **Außenform aller Ebenen gleich:** 205 × 130 mm, vorne bis x = +85, hinten bis x = −120. Die **Räder sitzen an den Ecken** (Achsen bei x = +55 und −90, Radstand 145 mm), vorne und hinten je 30 mm Überhang.
- **Nur M3-Zylinderkopfschrauben (ISO 4762).** In Kunststoff schneiden sie ihr Gewinde selbst: Kernloch **2,6 mm**, Dom Ø 10 mm, mindestens 10 mm tief. Durch ein Teil hindurch: **3,4 mm**.
- **Von außen sichtbare Köpfe liegen bündig** in einer Senkung Ø 6,5 × 3,1 mm (Kopf Ø 5,5 × 3 mm). Innen dürfen die Köpfe aufliegen. Ausnahme: die Motorschrauben in der Seitenwand – die Wand ist dort nur 3 mm dick, die Köpfe sitzen hinter dem Rad. Wer sie bündig will: M3 mit flachem Kopf (DIN 7984, 2 mm hoch).
- **Material um jedes Kernloch mindestens 3,5 mm** – sonst kann der Kunststoff beim Eindrehen reißen. Alle Druckteile haben überall **3,7 mm** (nachgemessen am fertigen STL mit Messstrahlen von jeder Lochachse aus: `werkzeug/fleisch.py`, braucht `pip install trimesh rtree`).
- **Keine gekauften Halter:** Die Motoren werden direkt an die Wanne geschraubt, Module ohne Löcher sitzen in Einklick-Taschen.
- **Gut an die Kabel kommen:** Die Wanne hängt mit 4 langen Schrauben von unten am Elektronik-Deck. Zum Arbeiten an Motoren, Akku und Stromversorgung: Auto umdrehen, 4 × M3 × 45 lösen, Wanne abnehmen – alles darüber bleibt zusammengebaut.

## Ebene 1 – Fahrwerk & Energie (`ebene1_fahrwerk.py` → `ebene1/`)

In der Wanne liegt alles, was schwer ist oder mit dem Akku zu tun hat: 4 Motoren, Akku und die **komplette Stromversorgung**. Schwerpunkt ganz unten, und die dicken Akkukabel bleiben kurz.

| Datei | Anzahl | Maße | Druckrichtung | Hinweise |
|---|---|---|---|---|
| `ebene1/wanne.stl` | 1 | 205 × 130 × 42 mm | Boden unten | Ohne Stützen (geprüft): Kufen mit scharfem 45°-Knick, Sensorfenster mit 45°-Ecken, Senkungen im Boden mit Brücken-Trick, Rastnasen als Keil. Passt auf ein 220er-Druckbett. |
| `ebene1/motorbuegel.stl` | **4** | 51 × 16 × 10 mm | flach auf die große Seite | Ohne Stützen. |

**Druckeinstellungen:** PETG empfohlen (verträgt die Wärme von Motoren und Akku besser), PLA geht auch. **4 Wände/Perimeter** (damit die Schrauben gut greifen), 25 % Füllung, 0,2 mm Schichthöhe. Die Empfehlung für jedes einzelne Druckteil (Filament, Temperaturen, Wände, Füllung, Druckrichtung, Download) steht auch in den 3D-Ansichten: Druckteil antippen.

**Druckbar ohne Stützen – geprüft:** `python werkzeug/ueberhang.py` prüft alle Druckteile in ihrer Druckrichtung. Erlaubt sind nur Flächen, die mindestens 45° steil sind, kurze Brücken (waagerecht, an zwei Seiten aufliegend, höchstens 15 mm – z. B. die Decke eines Schlitzes) und die Oberseite kleiner runder Löcher in senkrechten Wänden bis Ø 10 mm (Wellenlöcher, Schraub-Langlöcher, Schalterloch) – die schafft jeder Drucker. Ergebnis: alle Teile „ohne Stützen druckbar“. Nach jeder Änderung an einem Druckteil neu laufen lassen.

**Was wo ist** (von oben gesehen, vorne = Kamera)
- **Motoren** liegen in 2 Sätteln, die Getriebe-Stirnseite innen an der Seitenwand. **Encoder-Stecker zeigen nach oben** – zwischen Stecker und Deck bleiben ca. 9 mm.
- **Akku** (2 × Keystone 1047) in der Mitte auf 4 Sockeln.
- **4 Aufnahmekerben für den Prüfstand** unten im Boden unter dem Akku (wie bei einer Hebebühne). Innen ist der Boden dort 2,5 mm dicker – der Platz unter den Akkuhaltern ist sowieso frei.
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
| `ebene2/platte.stl` | 1 | 205 × 130 × 12 mm (mit Taschen und Domen) | Unterseite aufs Bett | **Ohne Stützen** – alles sitzt auf der Oberseite. Die 4 Kernlöcher für die Wanne kommen von unten. |
| `ebene2/ring_oben.stl` | 1 | 205 × 130 × 23 mm | **umgedreht** (Oberkante aufs Bett) | Ohne Stützen – so stehen die Röhren auf dem Bett. Seitenwand zwischen Elektronik-Deck und Ebene 3, hinten mit Loch für den Hauptschalter und Ausschnitt für die USB-C-Buchse. |

**Aufteilung in Zonen** – alles gut erreichbar, nichts liegt kreuz und quer:

| Zone | Wo | Was |
|---|---|---|
| Motorzone vorne | über der Vorderachse | Griffloch über den beiden Motorsteckern, **DRV8833 vorne** (treibt beide Vordermotoren), **3,3-V-Verteiler vorne** (Encoder der Vordermotoren) |
| Motorzone hinten | über der Hinterachse | genauso: Griffloch, **DRV8833 hinten**, **3,3-V-Verteiler hinten** (Encoder der Hintermotoren, BNO085, INA226) |
| Steuerung | Mitte | **Pico 2 W auf dem Freenove-Board** (Klemmen-Reihen zeigen zu den Seiten) und davor der **Kompass BNO085** (um 90° gedreht) |
| Strom und Laden | Rand | hinten links das **Ladeboard**, rechts neben dem Pico der **MP1584** und der Strom-Durchbruch **C** |

**Gut erreichbar – Ebene 3 als Klappdeckel:** Die beiden hinteren Dome (x = −112,6, z = ±24) tragen das Scharnier von Ebene 3 (M3-Schraube als Achse), vorne hält eine Schraube. Schraube lösen, Deckel hochklappen – dann liegen alle Klemmen und Stecker von Ebene 2 offen. (Ebene 3 selbst wird noch entworfen.)

**Erreichbarkeit – vom Skript geprüft:** `ebene2_elektronik.py` prüft bei jedem Lauf nicht nur, ob sich etwas überschneidet, sondern auch, ob man herankommt (Ausgabe „Erreichbarkeit – Probleme: 0“):

| Was | verlangt frei | Hindernis zählt ab |
|---|---|---|
| vor jeder Freenove-Klemmen-Reihe (Kabel mit Aderendhülse) | 13 mm | 6 mm Höhe (die Kabel gehen ca. 9 mm über dem Deck hinein) |
| vor der Kabelseite jedes WAGO | 15 mm | 2 mm Höhe |
| vor jeder STEMMA-QT-Buchse des Kompasses | 12 mm | 2 mm Höhe |
| rund um jedes Griffloch (Finger) | 4 mm + Rand | 6 mm Höhe |
| unter dem Hauptschalter (ragt 25 mm nach innen) | ganze Länge | 6,5 mm Höhe |

Module mit Lötanschlüssen (DRV8833, MP1584, Ladeboard) klickt man zum Löten heraus – ihre Kabel bekommen dafür ein paar Zentimeter Reserve.

**Was darauf sitzt**
- **Freenove-Board mit Pico 2 W** in der Mitte, die Klemmen-Reihen zeigen zu den Seiten (dort sind mindestens 23 mm frei für Kabel mit Aderendhülse), auf 4 gedruckten Domen (4 mm hoch, Platz für die Lötstellen), 4 × **M3 × 8** durch die Löcher des Boards – schneiden sich das Gewinde selbst (greifen 6,4 mm).
- **Einklick-Taschen** für alle Module ohne Löcher: 2 × DRV8833, MP1584, BNO085, 2 × WAGO 221-415 (3,3-V-Verteiler vorne/hinten) und das Ladeboard. Passgenauer Rahmen (0,3 mm Luft), je 2 Rastnasen (0,6 mm), eine Kerbe zum Heraushebeln mit einem kleinen Schraubendreher.
- **Grifflöcher** (28 × 22 mm, mit 2 mm hohem Rand eingefasst, rundum mindestens 6 mm nichts Hohes – Platz für zwei Finger) genau über den beiden Motorsteckern jeder Achse: Deckel auf, durchgreifen, Stecker **direkt am Motor** einstecken oder abziehen – keine Zwischenstecker. Das Motorkabel geht durch dasselbe Loch gerade nach oben. **Wanne abnehmen:** Deckel auf, die 4 Motorstecker abziehen, 4 × M3 × 45 unten lösen.
- **DRV8833** je Achse direkt neben dem Griffloch, die Motor-Reihe (OUT1–OUT4) zeigt zum Loch. OUT1/OUT2 = linker Motor, OUT3/OUT4 = rechter Motor dieser Achse.
- **WAGO-Taschen (3,3 V):** auf der anderen Seite des Grifflochs, die **Kabelseite ist offen und zeigt nach außen** (davor mindestens 19 mm frei), die Rückwand ist nur 4 mm hoch (Hebel klappen frei auf), die Rastnasen sitzen an den kurzen Enden.
- **BNO085 (Kompass)** vor dem Pico, um 90° gedreht – die STEMMA-QT-Buchsen zeigen zu den Seiten, davor sind mindestens 18 mm frei (ca. 5 cm zum vorderen, 10 cm zum hinteren Motor). Motormagnete, Spulen und Leitungen mit viel Strom stören den Kompass – deshalb ist rund um ihn alles frei, und am Sensor keine Stahlschrauben (er wird nur eingeklickt). Die Tasche hat an beiden kurzen Seiten eine 16 mm breite Aussparung für die STEMMA-QT-Stecker.
- **MP1584** rechts neben dem Freenove-Board, direkt am Strom-Durchbruch C (ca. 7 cm vom Kompass – seine Spule macht ein Magnetfeld). Er ist niedrig, die Kabel zu den Freenove-Klemmen gehen darüber.

  **Kabellängen vom Motorstecker** (gerechnet aus dem 3D-Modell, mit Reserve) – alles kurz, die üblichen 20-cm-Motorkabel reichen:

  | Ader | vorne links | vorne rechts | hinten links | hinten rechts |
  |---|---|---|---|---|
  | M1, M2 → DRV8833 der Achse | 6 cm | 7 cm | 6 cm | 7 cm |
  | VCC → 3,3-V-Verteiler der Achse | 7 cm | 6 cm | 7 cm | 6 cm |
  | GND, A, B → Freenove-Klemmen | 12 cm | 18 cm | 13 cm | 7 cm |

  Längere Kabel ordentlich aufrollen und mit einem Kabelbinder sichern. Nach der Lieferung nachmessen.
- **Kabelwege nach unten in die Wanne:** die beiden Grifflöcher (Motorkabel, XSHUT der Nahsensoren), hinten links und rechts je ein Schlitz (Daten vom INA226, Schalter-Rückleitung), seitlich A/B, **C am rechten Rand** (Plus und Minus von den Verteilern – immer paarweise nebeneinander, dann heben sich ihre Magnetfelder auf). Leitungen mit viel Strom laufen am Rand, nie quer durch die Mitte.
- **Ladeboard DDTCCRUB 2S** hinten links: Die Platine liegt **bündig an der Innenseite der Rückwand**, die USB-C-Buchse steckt im Ausschnitt der Wand und sitzt nur 1 mm hinter der Außenseite – der Stecker ist gut zu erreichen und rastet voll ein. Dafür ist die innere Ecke des Rings hinten links enger gerundet (R 4 statt 7,6; die Wand ist dort an der dünnsten Stelle 0,9 mm). Der Ausschnitt ist 13,5 × 8 mm (außen angefast), im Deck darunter eine flache Mulde. Die Seitenwände der Tasche stehen nur im vorderen Teil, hinten sitzen der Dom der Wannenschraube und die Ecke des Rings. BAT und GND gehen durch Durchbruch B hinunter zum BMS.
- **Rückwand des Gehäuse-Rings:** links (von hinten gesehen) der **Hauptschalter** – runder Taster, rastend, **Ø 12 mm** (Loch Ø 12,2 mm, Frontring Ø 13,9 mm liegt außen auf, Mutter innen; ragt 19 mm nach innen, darunter bleibt frei) –, rechts die **USB-C-Buchse** des Ladeboards. Beide sitzen außen, nicht über den Grifflöchern. Die Wand ist 2,4 mm dick, das passt für die Mutter. Reihenfolge beim Zusammenbau: erst das Ladeboard einklicken, dann den Ring aufsetzen.

- Im 3D-Modell: `modell/ebene2-oben.html` (Werkstatt-Ansicht nur für Ebene 2).

**Befestigung**
- Unten: 4 Dome (Kernloch von unten, 10 mm tief) über den Säulen der Wanne – dort greifen die 4 × M3 × 45 der Wanne von unten (Kernloch 11 mm tief, oben geschlossen).
- Oben: der **Gehäuse-Ring** schließt die Seiten bis Ebene 3. Seine Röhren sind **Hülsen** (Ø 13 mm) über 4 Domen des Decks (8 mm hoch, Kernloch 11 mm tief) bei x = 73,5 / z = ±57,6 (vorne, in der Ecke an Seiten- und Vorderwand) und x = −112,6 / z = ±23,3 (hinten an der Rückwand = Scharnier des Klappdeckels Ebene 3). Jede Hülse geht von unten bis oben, umschließt den Dom ganz (0,3 mm Luft) und ist in voller Breite mit der Außenwand verbunden – von außen eine durchgehende Säule ohne Fuge, und der Ring sitzt formschlüssig auf dem Deck.

Alle Kernlöcher haben **3,7 mm Material** rundum (nachgemessen mit `werkzeug/fleisch.py`). Die Lage aller Taschen, Dome und Durchbrüche prüfen beide Skripte selbst auf Überschneidungen (Ausgabe „Überschneidungen: 0“).

**Schrauben für Ebene 2:** 4 × M3 × 8 (Freenove-Board). Die Schrauben zur Wanne zählen bei Ebene 1.

## Ebene 3 – Gehirn, Klappdeckel (`ebene3_gehirn.py` → `ebene3/`)

Ein Druckteil: **Boden von Ebene 3 und Seitenwände bis Ebene 4 in einem Stück** (215,5 × 130 × 48 mm mit Scharnier-Lappen). Der ganze obere Teil klappt nach hinten auf wie eine Motorhaube – dann liegt Ebene 2 offen.

- **Scharniere hinten:** zwei Scharniere außen an der Trennfuge. Die Achse liegt 5,5 mm hinter der Rückwand und 5 mm über der Fuge. Je Scharnier sitzen zwei Lappen am Deckel und einer am Ring von Ebene 2. Die Achse ist eine **M3 × 16**, ihr Gewinde schneidet sich in den äußeren Lappen. Das Skript prüft in 10°-Schritten bis 100°, dass beim Aufklappen nichts anstößt.
- **Vorne zwei M3 × 12** waagerecht durch die Vorderwand, die Köpfe sitzen bündig. Sie greifen in zwei Laschen, die vom Ring von Ebene 2 durch Schlitze im Boden nach oben ragen. Schrauben raus, Deckel hoch.
- **Raspberry Pi 5** mit Active Cooler und AI HAT+: 4 Dome (5 mm hoch).
  - **M2,5** von unten durch Boden, Dom und Pi in die 16-mm-Abstandshalter des AI HAT+ (liegen bei).
  - Ausnahme von „nur M3“, weil die Löcher des Pi nur 2,7 mm groß sind.
  - Die Köpfe sind unten versenkt, mit Brücken-Trick.
  - USB und Ethernet zeigen nach hinten.
- **Pololu D36V50F5** vorne rechts in einer Einklick-Tasche, nah an der USB-C-Buchse des Pi.
- **4G-Modul Waveshare SIM7600G-H 4G DONGLE:** Es wird nur die Platine eingebaut (82,3 × 40,2 mm, ohne Löcher), die Kunststoffhülle ist zu groß.
  - Die Platine steht **senkrecht links neben dem Pi**. Sie wird von oben in zwei Säulen mit Nut an ihren Enden geschoben und steht auf dem Boden.
  - Der USB-A-Stecker zeigt nach hinten. Ein kurzes Winkel-Kabel führt zum Pi.
  - Die SMA-Buchse (MAIN) zeigt nach vorne, die zwei u.FL-Buchsen (AUX, GNSS) liegen daneben.
- **Kamera Modul 3 Wide** vorne: von oben in zwei Nuten geschoben. Das Objektiv schaut durch ein rundes Fenster mit flacher Oberkante, außen angefast.
- **Lüftung:** senkrechte Schlitze in beiden Seitenwänden. Der AI HAT+ darf nicht ohne Luft eingebaut werden.
- **Ebene 4:** 4 Röhren in den Ecken, Kernloch von oben (11 mm tief, 3,7 mm Material rundum).
- **Kabel nach unten:** Durchbruch hinten Mitte, nah am Scharnier. Dort laufen USB Pico → Pi und Akku-Plus/Minus zum Pololu. So knicken die Kabel beim Aufklappen kaum.
- **Ring von Ebene 2:** wird **aufrecht** gedruckt (Scharnier-Lappen und Laschen mit 45°-Schrägen). Er ist mit **4 × M3 × 20 von oben** am Deck verschraubt; die Köpfe liegen unter dem Deckel.

Im 3D-Modell: `modell/ebene3-gehirn.html` (Werkstatt-Ansicht mit Regler zum Aufklappen).

**Schrauben für Ebene 3:** 2 × M3 × 16 (Scharniere), 2 × M3 × 12 (vorne), 4 × M2,5 × 6 (Pi, plus die beiliegenden Abstandshalter des AI HAT+). Am Ring von Ebene 2 dazu 4 × M3 × 20.

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
