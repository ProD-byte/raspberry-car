"""STEP -> GLB mit Farben (OpenCascade XCAF + RWGltf_CafWriter).
Aufruf: python step2glb.py eingabe.step ausgabe.glb [ablenkung_mm]
"""
import sys
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString, TCollection_AsciiString
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.collections import Sequence_TDF_Label as TDF_LabelSequence, IndexedDataMap_TCollection_AsciiString_TCollection_AsciiString as InfoMap
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.RWGltf import RWGltf_CafWriter

from OCP.Message import Message_ProgressRange
from OCP.IFSelect import IFSelect_RetDone
from OCP.RWMesh import RWMesh_CoordinateSystem

src, dst = sys.argv[1], sys.argv[2]
defl = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05

doc = TDocStd_Document(TCollection_ExtendedString("doc"))
r = STEPCAFControl_Reader()
r.SetColorMode(True); r.SetNameMode(True); r.SetLayerMode(True)
assert r.ReadFile(src) == IFSelect_RetDone, "STEP nicht lesbar"
r.Transfer(doc)

st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
labels = TDF_LabelSequence(); st.GetFreeShapes(labels)
for i in range(1, labels.Length() + 1):
    shp = st.GetShape_s(labels.Value(i))
    BRepMesh_IncrementalMesh(shp, defl, False, 0.3, True)

w = RWGltf_CafWriter(TCollection_AsciiString(dst), True)  # True = binär (.glb)
# STEP ist in mm, Z oben -> glTF Y oben, Einheit bleibt mm (Skalierung 1)
cs = w.ChangeCoordinateSystemConverter()
cs.SetInputLengthUnit(0.001); cs.SetOutputLengthUnit(0.001)
cs.SetInputCoordinateSystem(RWMesh_CoordinateSystem.RWMesh_CoordinateSystem_Zup)
cs.SetOutputCoordinateSystem(RWMesh_CoordinateSystem.RWMesh_CoordinateSystem_glTF)
ok = w.Perform(doc, InfoMap(), Message_ProgressRange())
print("geschrieben" if ok else "FEHLER", dst)
