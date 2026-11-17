"""GLB verkleinern: alle Teile gleicher Farbe zu einem Mesh zusammenfassen.
Aufruf: python merge_glb.py ein.glb aus.glb [--ohne R,G,B ...]
  --ohne R,G,B  Teile dieser Farbe weglassen (z. B. Stiftleisten, die man nicht einlötet)
Gibt außerdem Maße und Farben aus.
"""
import sys, collections
import numpy as np
import trimesh

src, dst = sys.argv[1], sys.argv[2]
ohne = {tuple(int(v) for v in a.split(',')) for a in sys.argv[3:] if a != '--ohne'}
scene = trimesh.load(src)
groups = collections.defaultdict(list)
for node in scene.graph.nodes_geometry:
    T, gname = scene.graph[node]
    g = scene.geometry[gname].copy()
    g.apply_transform(T)
    mat = getattr(g.visual, 'material', None)
    if mat is not None and getattr(mat, 'baseColorFactor', None) is not None:
        col = tuple(int(v) for v in mat.baseColorFactor[:4])
    elif hasattr(g.visual, 'face_colors'):
        col = tuple(int(v) for v in g.visual.face_colors[0])
    else:
        col = (200, 200, 200, 255)
    if col[:3] in ohne:
        continue
    groups[col].append(g)

out = trimesh.Scene()
for i, (col, meshes) in enumerate(sorted(groups.items(), key=lambda kv: -sum(len(m.faces) for m in kv[1]))):
    m = trimesh.util.concatenate([trimesh.Trimesh(mm.vertices, mm.faces, process=False) for mm in meshes])
    m.merge_vertices()
    m.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        name=f"farbe_{i}", baseColorFactor=np.array(col, dtype=np.uint8),
        metallicFactor=0.0, roughnessFactor=0.6))
    out.add_geometry(m, geom_name=f"farbe_{i}")
    print(f"farbe_{i}: rgba{col}  {len(m.faces)} Dreiecke")
out.export(dst)
print("Maße (mm):", out.extents.round(2), "Ursprung:", out.bounds[0].round(2))
