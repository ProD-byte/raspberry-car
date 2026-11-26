# Stromversorgung

## Überblick

```
USB-C-Ladegerät (5 V, mind. 2 A)
        │
   Ladeboard DDTCCRUB (2S, 1A) ── BAT/GND ──┐
                                            │
Akku 2S2P ── B−/BM/B+ ── BMS 2S 20A Balance ─┤ P+/P−
(4× 18650, 7,4 V, 7000 mAh)                 │
                                            P+ ─► Sicherung 10 A ─► Hauptschalter ─► INA226 (VIN+ → VIN−)
                                                                                         │
                                                                                 WAGO Plus / WAGO Minus
                                                                    ┌──────────────┬───────┴──────┬──────────────┐
                                                               DRV8833 vorne  DRV8833 hinten   MP1584 5 V     Pololu 5 V/5,5 A
                                                                (Motoren)       (Motoren)      → Pico VSYS     → Pi 5 (USB-C)
                                                                                               → Front-/Rücklicht, Scheinwerfer
```

## Wichtige Zahlen

| | |
|---|---|
| Akkuspannung | 6,0 V (leer) – 7,4 V (nominal) – 8,4 V (voll) |
| Kapazität | 7000 mAh, ca. 52 Wh |
| Verbrauch | ca. 18 W normal, ca. 65 W Spitze |
| Fahrzeit | ca. 2–2,5 h (alles an), ca. 4–5 h nur mit Pico und Motoren (Stufe 1–2), ca. 3,5 h stehend mit allem an. Schätzung – genau misst es später der INA226 |
| Ladezeit | ca. 10–12 h (über Nacht) mit dem 1-A-Ladeboard: es nimmt 5 V × 1 A auf, am Akku kommen bei 8,4 V nur ca. 0,55 A an → 7000 mAh ÷ 0,55 A ≈ 12–13 h von ganz leer; da der Pico schon bei 6,4 V abschaltet, ist der Akku nie ganz leer |
| Motoren | 6-V-Motoren am 8,4-V-Akku: Software begrenzt PWM auf ca. 70 % |

## Ladeboard einstellen (vor dem ersten Anschließen)

Auf der Rückseite gibt es Lötbrücken:
- Reihe **OUT**: 2S / 3S / 4S → **nur 2S** brücken
- Reihe **IN**: 1A / 2A / 4A → **nur 1A** brücken

Mehr als 1 A bringt über USB mit 5 V nichts (USB liefert max. 15 W) und macht Board und Kabel heiß.

**Test:** Ohne Akku USB-C einstecken, zwischen BAT und GND messen → ca. **8,4 V**. Bei 12,6 V oder 16,8 V stimmt eine Brücke nicht.

## Akku zusammenbauen

1. Alle 4 Zellen auf gleiche Spannung prüfen (max. 0,05 V Unterschied).
2. Gruppe 1 (Halter links) und Gruppe 2 (Halter rechts, umgedreht eingesetzt) je 2 Zellen parallel.
3. Am BMS in dieser Reihenfolge anschließen: **B− → BM → B+**.
4. Erst dann P−/P+ belasten. Bei manchen BMS muss nach dem Anschließen einmal kurz das Ladegerät angesteckt werden, damit der Ausgang freigibt.

## Vor dem ersten Einschalten

- MP1584 vorher ohne Last auf **5,0 V** einstellen/prüfen.
- Pololu-Ausgang ohne Pi messen: 5,0–5,1 V.
- Diode 1N5819 zwischen MP1584 OUT+ und Pico VSYS: **Ring zur Pico-Seite**.
- Sicherung erst einsetzen, wenn alles verdrahtet und geprüft ist.
- Pi 5: in `config.txt` die Zeile `usb_max_current_enable=1` eintragen.

## Später: schneller laden

Über eine Docking-Station mit 12-V-Netzteil und passendem Lademodul (2 A und mehr). Kontakte im Gehäuse werden mit eingeplant.
