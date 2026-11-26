"""Raspberry Car – Lochmaße für M3-Schrauben, je nach Filament und Druckrichtung.

Alle Gehäuse-Skripte holen ihre M3-Löcher von hier. Zum Umstellen nur FILAMENT ändern und die Teile neu erzeugen.

  HOCH = Loch steht beim Druck senkrecht (Achse nach oben, z. B. Schraubdome, Säulen),
  QUER = Loch liegt beim Druck waagerecht (z. B. Fugen-Laschen, Schutzblech-Säulen).
  PILOT = Kernloch: die Schraube schneidet ihr Gewinde selbst und muss fest sitzen.
  DURCH = Durchgangsloch: die Schraube soll locker durchgehen, ohne zu klemmen.

Werte aus der Lochprobe (gehaeuse/m3_lochprobe.py), Bambu A1, 0,4-mm-Düse:
  * PLA (getestet 25.11.2026): Kernloch hoch 3,1 / quer 2,8.
    Gedruckt mit 6 Wänden (wie die PLA-Teile). Mit 4 Wänden gehen die Schrauben leichter – dann neu testen.
    PLA druckt Löcher enger als PETG und ist härter (gibt beim Gewindeschneiden kaum nach).
    Gegenüber PETG (2,6 / 3,4 hat gepasst) ist das Kernloch hoch +0,5 mm und quer +0,2 mm größer.
    Durchgangsloch daraus abgeleitet: hoch 3,4 + 0,4 = 3,8 mm, quer 3,4 + 0,2 = 3,6 mm
    (hoch etwas weniger als +0,5, weil ein Teil davon die Härte beim Schneiden ist, nicht die Maßabweichung).
  * PETG: 2,6 / 3,4 hat beim ersten Druck gut gepasst – genaue Werte folgen aus der Lochprobe.
"""

FILAMENT = "PLA"          # "PLA" oder "PETG"

WERTE = {
    #        PILOT_HOCH, PILOT_QUER, DURCH_HOCH, DURCH_QUER
    "PLA":  (3.1, 2.8, 3.8, 3.6),
    "PETG": (2.6, 2.6, 3.4, 3.4),
}

PILOT_HOCH, PILOT_QUER, DURCH_HOCH, DURCH_QUER = WERTE[FILAMENT]

# Kleine Schrauben (Ausnahme von „nur M3“, weil die Platinen kleinere Löcher haben):
#   M2,5 – Pi-Stapel (4 × M2,5 × 16 von oben durchs Dach), M2 – später Display und Ladeboard.
# M2,5 PLA getestet 25.11.2026 (lochprobe_klein.py): Kernloch hoch 2,5 / quer 2,3. (6 Wände)
#   Durchgangsloch daraus wie bei M3 (dort Kernloch → Durchgang hoch +0,7, quer +0,8): hoch 3,2 / quer 3,1.
# M2 noch nicht getestet: Grundmaß (PETG-Wert) plus derselbe Zuschlag wie bei M3.
# PETG-Werte vorläufig (Grundmaße), Test steht aus.
KLEIN = {
    #        M25_PILOT_HOCH/QUER, M25_DURCH_HOCH/QUER, M2_PILOT_HOCH/QUER, M2_DURCH_HOCH/QUER
    "PLA":  (2.5, 2.3, 3.2, 3.1, 2.2, 1.9, 2.8, 2.6),
    "PETG": (2.1, 2.1, 2.8, 2.8, 1.7, 1.7, 2.4, 2.4),
}
(M25_PILOT_HOCH, M25_PILOT_QUER, M25_DURCH_HOCH, M25_DURCH_QUER,
 M2_PILOT_HOCH, M2_PILOT_QUER, M2_DURCH_HOCH, M2_DURCH_QUER) = KLEIN[FILAMENT]

if __name__ == "__main__":
    print(f"Filament {FILAMENT}: M3 Kernloch hoch {PILOT_HOCH} / quer {PILOT_QUER} mm, "
          f"Durchgangsloch hoch {DURCH_HOCH} / quer {DURCH_QUER} mm")
    print(f"  M2,5 Kernloch hoch {M25_PILOT_HOCH} / quer {M25_PILOT_QUER} mm, Durchgangsloch hoch {M25_DURCH_HOCH} / quer {M25_DURCH_QUER} mm")
    print(f"  M2 Kernloch hoch {M2_PILOT_HOCH} / quer {M2_PILOT_QUER} mm, Durchgangsloch hoch {M2_DURCH_HOCH} / quer {M2_DURCH_QUER} mm")
