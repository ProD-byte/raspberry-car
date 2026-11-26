"""Raspberry Car – Lochproben für die kleinen Schrauben M2 und M2,5 (Werkzeug, kommt nicht ins Auto)

Gleich aufgebaut wie die M3-Lochprobe (m3_lochprobe.py), aber je Schraubengröße ein eigenes Teil. Die Größe steht
links groß auf dem Block („M2“ bzw. „M2,5“), damit man die beiden nicht verwechselt.

  * oben im Block: Löcher HOCH (senkrecht gedruckt), in der Wand dahinter: Löcher QUER (waagerecht gedruckt),
  * links die kleinen Löcher zum Gewindeschneiden (Kernloch), rechts die großen zum Durchstecken (Durchgangsloch).
  * Die Zahl an jedem Loch ist sein Durchmesser in der CAD-Zeichnung (mm).

Wofür gebraucht:  M2,5 – Pi-Stapel (4 × M2,5 × 16 von oben durchs Dach),  M2 – später Display und Ladeboard.
Zurzeit in loecher.py (aus dem M3-Test hochgerechnet):
  PLA: M2,5 Kernloch 2,5 hoch / 2,3 quer (getestet), Durchgang 3,2 / 3,1 · M2 Kernloch 2,2 / 1,9 · M2 Durchgang 2,8 / 2,6

Testen wie bei M3: kurze Schraube (M2 × 6, M2,5 × 6 … 8) in jedes Loch drehen. Gutes Kernloch: geht ohne Gewalt rein
und sitzt fest. Gutes Durchgangsloch: Schraube geht locker durch, ohne zu klemmen, wackelt aber nicht viel.
Druck: so wie es liegt, ohne Stützen, gleiches Filament und gleiche Einstellungen wie die echten Teile.

Aufruf:  python lochprobe_klein.py   → erzeugt lochprobe/m2_lochprobe.stl/.step und lochprobe/m25_lochprobe.stl/.step
"""
from build123d import export_stl, export_step
import m3_lochprobe as lp

PROBEN = {
    #  Datei,  Kennung,  Löcher: Kernlöcher … | Durchgangslöcher …
    "m2_lochprobe":  ("M2",   [1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.5, 2.7, 2.9]),
    "m25_lochprobe": ("M2,5", [2.3, 2.4, 2.5, 2.6, 2.7]),          # seit 25.11.2026 nur dieser Bereich
}
TEILUNG, SCHRIFT = 7.0, 2.8          # etwas enger und kleiner als bei M3

if __name__ == "__main__":
    lp.AUS.mkdir(exist_ok=True)
    for datei, (kennung, loecher) in PROBEN.items():
        t, laenge = lp.teil(loecher, TEILUNG, SCHRIFT, kennung)
        print(f"Lochprobe {kennung}: {laenge:.0f} × {lp.BLOCK[0] + lp.WAND[0]:.0f} × {lp.WAND[1]:.0f} mm, "
              f"Volumen {t.volume / 1000:.1f} cm³ – Löcher {', '.join(lp.zahl(d) for d in loecher)}")
        export_stl(t, str(lp.AUS / f"{datei}.stl"), tolerance=0.01, angular_tolerance=0.1)
        export_step(t, str(lp.AUS / f"{datei}.step"))
