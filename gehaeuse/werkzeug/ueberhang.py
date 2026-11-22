"""Druckbar ohne Stützen? Prüft alle Druckteile in ihrer Druckrichtung.

Gesucht werden Flächen, die nach unten zeigen und flacher als 45° sind (über dem Druckbett).
Erlaubt sind kurze Brücken (waagerechte Stellen, die an zwei Seiten aufliegen und höchstens BRUECKE_MAX mm
überspannen, z. B. die Decke eines Schlitzes) und die Oberseite kleiner runder Löcher in senkrechten Wänden
(bis LOCH_MAX mm – die schafft jeder Drucker). Alles andere bräuchte Stützen.

Aufruf (einmalig: pip install trimesh):
    python werkzeug/ueberhang.py            # alle Teile
    python werkzeug/ueberhang.py ebene2/platte.stl none
Drehung: none (so wie modelliert), flip (umgedreht), +y / -y (auf die Seite gelegt).
"""
import collections
import sys
from pathlib import Path

import numpy as np
import trimesh

ORDNER = Path(__file__).resolve().parent.parent
# Datei, Druckrichtung – wie in gehaeuse/README.md
TEILE = [("ebene1/wanne_vorne.stl", "none"), ("ebene1/wanne_hinten.stl", "none"), ("ebene1/motorbuegel.stl", "+y"),
         ("ebene2/platte_vorne.stl", "none"), ("ebene2/platte_hinten.stl", "none"), ("ebene2/ring_vorne.stl", "none"), ("ebene2/ring_hinten.stl", "none"), ("ebene3/haube_vorne.stl", "flip"), ("ebene3/haube_hinten.stl", "flip"),
         ("pruefstand/pruefstand.stl", "none")]
STEIL = -0.74          # Flächen mit Normalen-z kleiner als das sind flacher als ca. 45° (nach unten)
BRUECKE_MAX = 15.0     # längste erlaubte Brücke (mm)
LOCH_MAX = 10.0        # runde Löcher in senkrechten Wänden bis zu diesem Durchmesser druckt jeder Drucker ohne Stützen


def pruefe(datei, dreh):
    m = trimesh.load(ORDNER / datei)
    modell = m.copy()
    if dreh == "flip":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    elif dreh == "+y":
        m.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]))
    elif dreh == "-y":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    bett = m.bounds[0][2]
    n, tri = m.face_normals, m.triangles
    schlecht = (n[:, 2] < STEIL) & (tri[:, :, 2].min(axis=1) > bett + 0.25)
    nach = collections.defaultdict(list)
    for a, b in m.face_adjacency[schlecht[m.face_adjacency[:, 0]] & schlecht[m.face_adjacency[:, 1]]]:
        nach[a].append(b); nach[b].append(a)
    gesehen, probleme, bruecken, loecher = set(), [], 0, 0
    for f in np.nonzero(schlecht)[0]:
        if f in gesehen:
            continue
        st, g = [f], []
        gesehen.add(f)
        while st:
            x = st.pop(); g.append(x)
            for y in nach[x]:
                if y not in gesehen:
                    gesehen.add(y); st.append(y)
        if m.area_faces[g].sum() < 0.5:
            continue
        pts = tri[g].reshape(-1, 3)
        dx, dy = np.ptp(pts[:, 0]), np.ptp(pts[:, 1])
        flach = (n[g, 2] < -0.99).all()
        if flach and min(dx, dy) <= BRUECKE_MAX:
            bruecken += 1
            continue
        if not flach and max(dx, dy) <= LOCH_MAX:
            loecher += 1
            continue
        mp = modell.triangles[g].reshape(-1, 3)
        probleme.append(f"    braucht Stütze: {dx:.1f} × {dy:.1f} mm, {pts[:, 2].min() - bett:.1f} mm über dem Bett "
                        f"(Auto x={mp[:, 0].mean():.1f} y={mp[:, 2].mean():.1f} z={-mp[:, 1].mean():.1f})")
    print(f"  {datei:28s} ({dreh:4s}): {'ohne Stützen druckbar' if not probleme else 'NICHT ohne Stützen'}"
          f" – {bruecken} kurze Brücken (≤ {BRUECKE_MAX:.0f} mm), {loecher} kleine runde Löcher (≤ Ø {LOCH_MAX:.0f} mm)")
    for z in probleme:
        print(z)
    return len(probleme)


if __name__ == "__main__":
    liste = [(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "none")] if len(sys.argv) > 1 else TEILE
    print("Druckbar ohne Stützen?")
    fehler = sum(pruefe(d, r) for d, r in liste)
    print("Probleme:", fehler)
