"""GLB eines Moduls „flach hinlegen“: dünnste Achse → nach oben (oder nach vorne),
Bauteilseite nach oben, Mitte auf 0, Unterkante auf 0.
Aufruf: python ausrichten.py ein.glb aus.glb [oben=gross|klein] [ziel=y|x] [achse=x|y|z]
  oben=gross: Bauteilseite ist die Seite, die weiter von der Platine absteht (Standard)
  oben=klein: umgekehrt (z. B. Module mit langen Stiftleisten unten)
  ziel=x:     dünne Achse zeigt nach vorne (+x) statt nach oben (z. B. Kamera, Objektiv nach vorne)
  achse=...:  dünne Achse von Hand vorgeben
"""
import sys
import numpy as np
import trimesh

ein, aus = sys.argv[1], sys.argv[2]
opt = dict(a.split('=') for a in sys.argv[3:])
scene = trimesh.load(ein)
m = scene.to_geometry() if hasattr(scene, 'to_geometry') else scene.dump(concatenate=True)
ext = m.extents
ax = {'x': 0, 'y': 1, 'z': 2}[opt['achse']] if 'achse' in opt else int(np.argmin(ext))
# Platinenebene: größte waagerechte Flaechen entlang der dünnen Achse
n = m.face_normals[:, ax]
flach = np.abs(n) > 0.95
pos = m.triangles_center[flach, ax]
area = m.area_faces[flach]
bins = np.round(pos, 1)
werte, inv = np.unique(bins, return_inverse=True)
summe = np.bincount(inv, weights=area)
top2 = werte[np.argsort(summe)[-2:]]
mitte = top2.mean()
lo, hi = m.bounds[0, ax], m.bounds[1, ax]
ueber, unter = hi - mitte, mitte - lo
gross_oben = ueber >= unter
vorzeichen = 1 if (gross_oben == (opt.get('oben', 'gross') == 'gross')) else -1
ziel = {'y': 1, 'x': 0}[opt.get('ziel', 'y')]

# Rotation: Achse ax (mit Vorzeichen) → Zielachse
quelle = np.zeros(3); quelle[ax] = vorzeichen
zielv = np.zeros(3); zielv[ziel] = 1
R = trimesh.geometry.align_vectors(quelle, zielv)
scene.apply_transform(R)
b = scene.bounds
T = np.eye(4)
mitte_xyz = (b[0] + b[1]) / 2
T[:3, 3] = -mitte_xyz
T[ziel, 3] = -b[0, ziel]
scene.apply_transform(T)
scene.export(aus)
print(f"dünne Achse {'xyz'[ax]}, Platine bei {mitte:.2f}, über {ueber:.2f} / unter {unter:.2f} -> Masse {np.round(scene.extents, 2)}")
