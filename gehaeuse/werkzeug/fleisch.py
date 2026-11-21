"""Misst das Material („Fleisch“) rund um Kernlöcher in einer STL-Datei.
Für jedes Loch: Strahlen von der Lochachse in 24 Richtungen auf mehreren Höhen.
Fleisch = Strecke Kunststoff vom Lochrand bis zur nächsten freien Fläche.
Aufruf: python fleisch.py datei.stl  x,z,y_von,y_bis[,name] ...   (Modell-Koordinaten)
"""
import sys
import numpy as np
import trimesh

m = trimesh.load(sys.argv[1])
# STL ist in CAD-Koordinaten: X = x, Y = -z, Z = y
for arg in sys.argv[2:]:
    teile = arg.split(',')
    x, z, y0, y1 = map(float, teile[:4]); name = teile[4] if len(teile) > 4 else ''
    minimum = 1e9; richtung = None
    for y in np.linspace(y0 + 0.5, y1 - 0.5, 6):
        for a in np.linspace(0, 2 * np.pi, 24, endpoint=False):
            d = np.array([np.cos(a), -np.sin(a), 0.0])
            start = np.array([x, -z, y])
            locs, _, _ = m.ray.intersects_location([start], [d], multiple_hits=True)
            if len(locs) < 2:
                continue
            ab = np.sort(np.linalg.norm(locs - start, axis=1))
            ab = ab[np.r_[True, np.diff(ab) > 0.01]]   # doppelte Treffer (Strahl genau auf einer Dreieckskante) zusammenfassen
            if len(ab) < 2:
                continue
            fleisch = ab[1] - ab[0]          # erster Treffer = Lochwand, zweiter = Ende des Materials
            if fleisch < minimum:
                minimum, richtung = fleisch, (round(np.degrees(a)), round(y, 1))
    print(f"{name:28s} x={x:6.1f} z={z:6.1f}: Fleisch mindestens {minimum:4.1f} mm  (Richtung {richtung[0]}°, Höhe {richtung[1]})")
