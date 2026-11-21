"""GLB verkleinern: alle Teile gleicher Farbe zu einem Mesh zusammenfassen.
Aufruf: python merge_glb.py ein.glb aus.glb [--max N] [--ohne R,G,B ...]
  --min MM      Einzelteile kleiner als MM (größte Kante) weglassen, z. B. Lötkugeln unter Chips
  (Farben bei --farbe/--alle wie im Bildprogramm angeben, also sRGB 0–255)
  --farbe TEXT=R,G,B   Teile, deren Name TEXT enthält, so einfärben (mehrfach möglich);
                       statt TEXT auch ab:MM = alle Teile, deren größte Kante mindestens MM lang ist
  --alle R,G,B  alle übrigen Teile ohne eigene Farbe so einfärben
  --max N       Farbgruppen mit mehr als N Dreiecken vereinfachen (braucht: pip install fast_simplification)
  --scharf      Punkte NICHT zusammenlegen: scharfe Kanten bleiben scharf (für Druckteile – sonst gibt es
                an Kanten falsche Schattierung, einzelne Dreiecke leuchten hell auf)
  --ohne R,G,B  Teile dieser Farbe weglassen (z. B. Stiftleisten, die man nicht einlötet)
Gibt außerdem Maße und Farben aus.
"""
import sys, collections
import numpy as np
import trimesh

src, dst = sys.argv[1], sys.argv[2]
args = sys.argv[3:]
maxtri = None
minmm = 0.0
farben = []
def lin(c):  # Farbe wie im Bildprogramm (sRGB, 0–255) -> glTF erwartet lineare Werte
    return tuple(round(255 * ((v / 255) / 12.92 if v / 255 <= 0.04045 else (((v / 255) + 0.055) / 1.055) ** 2.4)) for v in c)
while '--farbe' in args:
    i = args.index('--farbe'); k, v = args[i + 1].split('='); farben.append((k, lin(int(x) for x in v.split(',')) + (255,))); del args[i:i + 2]
alle = None
if '--alle' in args:
    i = args.index('--alle'); alle = lin(int(x) for x in args[i + 1].split(',')) + (255,); del args[i:i + 2]
scharf = '--scharf' in args
if scharf:
    args.remove('--scharf')
if '--min' in args:
    i = args.index('--min'); minmm = float(args[i + 1]); del args[i:i + 2]
if '--max' in args:
    i = args.index('--max'); maxtri = int(args[i + 1]); del args[i:i + 2]
ohne = {tuple(int(v) for v in a.split(',')) for a in args if a != '--ohne'}
scene = trimesh.load(src)
groups = collections.defaultdict(list)
for node in scene.graph.nodes_geometry:
    T, gname = scene.graph[node]
    g = scene.geometry[gname].copy()
    g.apply_transform(T)
    if minmm and max(g.extents) < minmm:
        continue
    mat = getattr(g.visual, 'material', None)
    if mat is not None and getattr(mat, 'baseColorFactor', None) is not None:
        col = tuple(int(v) for v in mat.baseColorFactor[:4])
    elif hasattr(g.visual, 'face_colors'):
        col = tuple(int(v) for v in g.visual.face_colors[0])
    else:
        col = (200, 200, 200, 255)
    for k, v in farben:
        if (k.startswith('ab:') and max(g.extents) >= float(k[3:])) or (not k.startswith('ab:') and k in node):
            col = v; break
    else:
        if alle:
            col = alle
    if col[:3] in ohne:
        continue
    groups[col].append(g)

out = trimesh.Scene()
for i, (col, meshes) in enumerate(sorted(groups.items(), key=lambda kv: -sum(len(m.faces) for m in kv[1]))):
    m = trimesh.util.concatenate([trimesh.Trimesh(mm.vertices, mm.faces, process=False) for mm in meshes])
    if not scharf:
        m.merge_vertices()
    if maxtri and len(m.faces) > maxtri:
        m = m.simplify_quadric_decimation(face_count=maxtri)
    m.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        name=f"farbe_{i}", baseColorFactor=np.array(col, dtype=np.uint8),
        metallicFactor=0.0, roughnessFactor=0.6))
    out.add_geometry(m, geom_name=f"farbe_{i}")
    print(f"farbe_{i}: rgba{col}  {len(m.faces)} Dreiecke")
out.export(dst)
print("Maße (mm):", out.extents.round(2), "Ursprung:", out.bounds[0].round(2))
