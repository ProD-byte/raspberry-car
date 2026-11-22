"""Setzt Ebene 2 (Deck, Ring, Bauteile) und Ebene 3 (Klapphaube mit allen Bauteilen am Dach, LiDAR oben) in die
Fahrsimulation – die Bauteile sind eine Kopie aus raspberry-car-3d.html.
Kann mehrfach laufen: ersetzt den Block zwischen den Markierungen. Nach Änderungen an Ebene 2 oder 3 im großen Modell
neu laufen lassen (siehe CLAUDE.md)."""
import re
from pathlib import Path

M = Path(__file__).resolve().parent.parent   # Ordner modell/
sim = (M / "fahrsimulation.html").read_text(encoding="utf-8")
gz = (M / "raspberry-car-3d.html").read_text(encoding="utf-8").split("\n")


def finde(lst, text, ab=0):
    for i in range(ab, len(lst)):
        if text in lst[i]:
            return i
    raise SystemExit("nicht gefunden: " + text)


def ohne_nur_im_auto(zeilen):
    zeilen = [z for z in zeilen if "nurImAuto = true" not in z or "m3Schraube" in z]
    return [z.replace(").userData.nurImAuto = true));", ")));") for z in zeilen]


# Ebene 2: vom Hauptschalter bis zum letzten 3,3-V-Verteiler
b0 = finde(gz, "(function sw() {")
b1 = finde(gz, "wago(L1, 'W3H'")
teile2 = ohne_nur_im_auto([z.replace("part(L1,", "part(E2,").replace("wago(L1,", "wago(E2,") for z in gz[b0:b1 + 1]])
# Ebene 3: Pi … 4G-Modul, dazu alles auf/unter dem Dach (LiDAR, GPS, LTE-Antennen, LEDs, Display)
c0 = finde(gz, "    const PI = { x: -8, y: TOP[2] + 5, z: 0 };")
c1 = finde(gz, "// EBENE 4 – Dach") - 1
d0 = finde(gz, "const L3 = makeLayer(3);") + 1
d1 = finde(gz, "// VERDRAHTUNG – jede Leitung") - 1
teile3 = [z.replace("part(L2,", "part(E3,").replace("ribbon(L2,", "ribbon(E3,").replace("part(L3,", "part(E3,")
           for z in gz[c0:c1] + gz[d0:d1]]   # alles übernehmen (auch „nur im Auto“: in der Simulation ist das ganze Auto zu sehen)
r0 = finde(gz, "    function ribbon(p, pts, width, color) {")
r1 = finde(gz, "    }", r0)
ribbon = gz[r0:r1 + 1]
pin = next(z for z in gz if "const PIN = {" in z).strip()

ANF, END = "    // >>> EBENE 2 (automatisch eingefügt, sim_ebene2.py)", "    // <<< EBENE 2"
block = [ANF,
         "    // Ebene 2 (Elektronik-Deck mit Ring) und Ebene 3 (Klapphaube mit Dach) – dieselben Bauteile wie in raspberry-car-3d.html.",
         "    // Ändert sich dort etwas an Ebene 2 oder 3, sim_ebene2.py neu laufen lassen (siehe CLAUDE.md).",
         "    const E2 = new THREE.Group(); auto.add(E2);",
         "    const E3 = new THREE.Group(); auto.add(E3);",
         "    const LEVEL = [50.25, 58, 84, 118];   // wie im großen Modell: [3] = Unterseite des Dachs der Haube",
         "    const TOP = [0, 61, 87, 121];",
         "    " + pin,
         ] + ribbon + [
         "    const deckFarbe = (mat) => { mat.color.set(0xd85a30).convertSRGBToLinear(); mat.roughness = 0.8; };",
         "    const ringFarbe = (mat) => { mat.color.set(0x575d63).convertSRGBToLinear(); mat.roughness = 0.8; };",
         "    const haubeFarbe = (mat) => { mat.color.set(0x6a7178).convertSRGBToLinear(); mat.roughness = 0.8; };",
         "    [['e2_platte_vorne', 'Elektronik-Deck Ebene 2, vordere Hälfte (Druckteil)', 'deck'], ['e2_platte_hinten', 'Elektronik-Deck Ebene 2, hintere Hälfte (Druckteil)', 'deck'],",
         "     ['e2_ring_vorne', 'Gehäuse-Ring oben, vordere Hälfte (Druckteil)', 'ring'], ['e2_ring_hinten', 'Gehäuse-Ring oben, hintere Hälfte (Druckteil)', 'ring']].forEach(([datei, name, art]) => {",
         "      const d = part(E2, name, 'Teil von Ebene 2 (Elektronik-Deck mit Ring). Einzelheiten: Werkstatt Ebene 2.', 0, 0, 0);",
         "      d.userData.druckteil = art; cadTeil(datei, d, new THREE.Group(), (m) => m, art === 'ring' ? ringFarbe : deckFarbe);",
         "    });",
         '    // Schutzbleche: 4 × dasselbe Druckteil (vorne links modelliert; rechts um 180° gedreht), am Ring von Ebene 2 verschraubt',
         '    [[0, false], [-160, false], [160, true], [0, true]].forEach(([dx, rechts]) => {',
         "      const w = part(E2, 'Schutzblech (4 × Druckteil)', 'Kotflügel über dem Rad (gehaeuse/schutzblech.py): eckiger Bogen (flaches Dach, schräge Schultern, steile Flanken) mit mindestens 4,5 mm Luft zum Reifen, außen ein nach innen gezogener Rand. Der 6 mm dicke Flansch liegt am Gehäuse-Ring von Ebene 2 an und wird mit 2 × M3 × 10 von außen in zwei Schraubsäulen des Rings geschraubt (Köpfe bündig) – nicht an der Wanne, die bleibt nach unten abnehmbar. Die Schrauben sitzen so weit außen, dass der Schraubendreher am Rad vorbeikommt. Viermal dasselbe Teil (rechts um 180° gedreht). Flansch-Rückseite aufs Bett, ohne Stützen. Datei: gehaeuse/schutzbleche/schutzblech.stl', dx, 0, 0);",
         "      w.userData.druckteil = 'ring'; if (rechts) w.rotation.y = Math.PI;",
         "      cadTeil('schutzblech', w, new THREE.Group(), (m) => m, (mat) => { mat.color.set(0xd85a30).convertSRGBToLinear(); mat.roughness = 0.6; mat.metalness = 0; });",
         '    });',
         "    // Haube: eigene Gruppe, damit sie sich durchsichtig schalten lässt (die Bauteile am Dach bleiben normal)",
         "    const haube = new THREE.Group(); E3.add(haube);",
         "    let haubeDurchsichtig = true;",
         "    function haubeGlas() {   // nach dem Laden jedes Teils und beim Umschalten",
         "      setTimeout(() => haube.traverse((o) => { if (!o.isMesh) return; (Array.isArray(o.material) ? o.material : [o.material]).forEach((m) => {",
         "        m.transparent = haubeDurchsichtig; m.opacity = haubeDurchsichtig ? 0.22 : 1; m.depthWrite = !haubeDurchsichtig; m.needsUpdate = true; }); }), 0);",
         "    }",
         "    [['e3_haube_vorne', 'Klapphaube Ebene 3, vordere Hälfte (Druckteil)'], ['e3_haube_hinten', 'Klapphaube Ebene 3, hintere Hälfte (Druckteil)']].forEach(([datei, name]) => {",
         "      const h = part(haube, name, 'Teil von Ebene 3 (Klapphaube mit Dach). Einzelheiten: Werkstatt Ebene 3.', 0, 0, 0);",
         "      h.userData.druckteil = 'haube'; cadTeil(datei, h, new THREE.Group(), (m) => { haubeGlas(); return m; }, haubeFarbe);",
         "    });",
         ] + teile2 + teile3 + [
         "    if (sweep) sweep.visible = false;   // den Strahl des LiDAR zeigt die Simulation selbst",
         END]

if ANF in sim:
    i = sim.index(ANF); j = sim.index(END) + len(END)
    sim = sim[:i] + "\n".join(block) + sim[j:]
else:
    marke = "      PARTS[`Nahsensor VL53L1X (${n})`].rotation.set(0, ry, 5 * Math.PI / 180);\n    });\n"
    assert sim.count(marke) == 1
    sim = sim.replace(marke, marke + "\n" + "\n".join(block) + "\n")

# Haken: Ebene 2, Ebene 3, Haube durchsichtig
HAKEN = ('        <label class="check"><input id="ebene2" type="checkbox" checked> Ebene 2</label>\n'
         '        <label class="check"><input id="ebene3" type="checkbox" checked> Ebene 3</label>\n'
         '        <label class="check"><input id="glas3" type="checkbox" checked> Haube durchsichtig</label>\n')
sim, n = re.subn(r'        <label class="check"><input id="ebene2"[^\n]*\n(        <label class="check"><input id="ebene3"[^\n]*\n)?(        <label class="check"><input id="glas3"[^\n]*\n)?', HAKEN, sim, count=1)
if not n:
    a = '      <div class="controls">\n        <label class="range" for="tempo">'
    assert sim.count(a) == 1
    sim = sim.replace(a, '      <div class="controls">\n' + HAKEN + '        <label class="range" for="tempo">')
HOERER = ("    document.getElementById('ebene2').addEventListener('change', (e) => { E2.visible = e.target.checked; });\n"
          "    document.getElementById('ebene3').addEventListener('change', (e) => { E3.visible = e.target.checked; });\n"
          "    document.getElementById('glas3').addEventListener('change', (e) => { haubeDurchsichtig = e.target.checked; haubeGlas(); });\n")
sim, n = re.subn(r"    document\.getElementById\('ebene2'\)\.addEventListener\('change'[^\n]*\n(    document\.getElementById\('ebene3'\)[^\n]*\n)?(    document\.getElementById\('glas3'\)[^\n]*\n)?", HOERER, sim, count=1)
if not n:
    a = "    // ===================================================================\n    // FAHRZEUG-DATEN (mm, kg, s)"
    assert sim.count(a) == 1
    sim = sim.replace(a, HOERER + "\n" + a)
sim = sim.replace("<h1>So fährt das Fahrwerk im Gelände</h1>", "<h1>So fährt das Auto im Gelände</h1>")
sim = sim.replace("Ebene 2 und 3 lassen sich ausblenden.", "Ebene 2 und 3 lassen sich ausblenden, die Haube lässt sich durchsichtig schalten.")
(M / "fahrsimulation.html").write_text(sim, encoding="utf-8")
print("ok", len(teile2), "Zeilen Ebene 2,", len(teile3), "Zeilen Ebene 3")
