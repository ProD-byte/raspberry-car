"""Erzeugt modell/ebene3-gehirn.html (Werkstatt-Ansicht Ebene 3, Klappdeckel) aus ebene1-unten.html
(Gerüst, Hilfsfunktionen, Bedienung) und raspberry-car-3d.html (Bauteile der Ebene 3).
Nach Änderungen an Ebene 3 im großen Modell neu laufen lassen."""
import re
from pathlib import Path

M = Path(__file__).resolve().parent.parent   # Ordner modell/
e1 = (M / "ebene1-unten.html").read_text(encoding="utf-8").split("\n")
gz = (M / "raspberry-car-3d.html").read_text(encoding="utf-8").split("\n")

SCH_X, SCH_Y = -130.5, 89.0                  # Scharnierachse (wie gehaeuse/ebene2_elektronik.py: X_HINTEN − 5,5)


def zeilen(lst, von, bis):          # 1-basiert, inklusive
    return lst[von - 1:bis]


def finde(lst, text, ab=0):
    for i in range(ab, len(lst)):
        if text in lst[i]:
            return i + 1
    raise SystemExit("nicht gefunden: " + text)


kopf = zeilen(e1, 1, finde(e1, "</head>"))
kopf = [z.replace("border-top: 4px solid var(--l0)", "border-top: 4px solid var(--l2)") for z in kopf]
kopf = [re.sub(r"<title>.*</title>", "<title>Werkstatt Ebene 3</title>", z) for z in kopf]
if not any("--l2:" in z for z in kopf):
    kopf = [z.replace("  --l1: #23897d;", "  --l1: #23897d;\n  --l2: #3f6db5;") for z in kopf]

html = """<body>
<div class="wrap">
  <header>
    <nav class="seiten" aria-label="3D-Ansichten"><a href="ebene1-unten.html">Werkstatt Ebene 1</a><a href="ebene2-oben.html">Werkstatt Ebene 2</a><a href="ebene3-gehirn.html" aria-current="page">Werkstatt Ebene 3</a><a href="fahrsimulation.html">Fahrsimulation</a><a href="raspberry-car-3d.html">Ganzes Auto</a></nav>
    <div class="eyebrow">Raspberry Car · Werkstatt</div>
    <h1>Ebene 3: Gehirn mit Dach (Klapphaube)</h1>
    <p class="lead">Der obere Teil des Autos ist eine <strong>Klapphaube</strong>: Seitenwände und Dach in einem, unten offen, aus zwei Hälften gedruckt. Alles hängt am Dach: Raspberry Pi 5 mit Active Cooler und AI HAT+, die Kamera hinter dem Fenster vorne, Pololu (5 V für den Pi), 4G-Modul, GPS-Antenne, das runde Display und die Lichtleisten vorne und hinten. Oben steht der LiDAR. Hinten zwei Scharniere, vorne zwei Schrauben. Mit dem Regler klappst du die Haube auf. Ohne Kabel.</p>
  </header>

  <div class="stage" id="stage">
    <div class="loading" id="loading">3D-Modell wird gebaut …</div>
    <div class="dims">Haube 250 × 180 × 37 mm (2 Hälften) · vorne: Kamera · hinten: Scharniere, Ladebuchse und Schalter</div>
    <div class="info" id="info"><b>Tippe auf ein Bauteil</b><span>Zum Beispiel auf den Pi, die Kamera oder die Haube.</span></div>
  </div>

  <div class="controls">
    <label class="check"><input id="bauteile" type="checkbox" checked> Bauteile zeigen</label>
    <label class="check"><input id="glas" type="checkbox"> Haube durchsichtig</label>
    <label class="check"><input id="unten2" type="checkbox" checked> Ebene 2 darunter</label>
    <label class="range" for="klappen">Aufklappen <input id="klappen" type="range" min="0" max="100" step="1" value="0"> <span id="klappen-wert" style="font-family:var(--font-mono);font-size:13px">0°</span></label>
    <div class="toggles">
      <button id="rotate" type="button" aria-pressed="true">Drehen</button>
      <button id="oben" type="button">Von oben</button>
      <button id="reset" type="button">Ansicht zurücksetzen</button>
    </div>
  </div>

  <div class="teile" id="teile"></div>

  <div class="notes">
    <p><strong>Druckdateien:</strong> <code>gehaeuse/ebene3/haube_vorne.stl</code> und <code>haube_hinten.stl</code>, erzeugt von <code>gehaeuse/ebene3_gehirn.py</code> – mit dem Dach nach unten drucken, ohne Stützen. Das Skript prüft auch, dass die Haube beim Aufklappen bis 100° nirgends am Ring von Ebene 2 anstößt.</p>
    <p><strong>Klappen:</strong> Hinten zwei Scharniere außen an der Trennfuge (Achse M3 × 16, Gewinde im äußeren Lappen). Vorne zwei M3 × 12 waagerecht durch die Vorderwand (Köpfe bündig) in die Laschen des Rings von Ebene 2. Alle Kabel von Ebene 2 in die Haube laufen hinten beim Scharnier – dort knicken sie beim Aufklappen am wenigsten.</p>
    <p><strong>Pi 5:</strong> Der Stapel aus Pi, Active Cooler und AI HAT+ hängt an 4 Domen unter dem Dach: M2,5 × 16 von oben durch Dach, Dom und AI HAT+ in die 16-mm-Abstandshalter (liegen dem HAT bei), Köpfe bündig im Dach. Unten hält der Pi mit den beiliegenden Schrauben. Bis zu den höchsten Teilen von Ebene 2 bleiben gut 10 mm Luft. <strong>Kamera:</strong> von unten in die zwei Nuten schieben, bis sie einrastet. <strong>Display:</strong> von unten einsetzen, das Glas liegt am Dach an, 3 Schnapphaken halten die Platine.</p>
    <p><strong>Zwei Hälften:</strong> Fuge bei x = 45. Innen hat jede Hälfte an Dach und Seiten einen 10 mm breiten Rand, beide werden mit 6 × M3 × 12 verschraubt (Kopf hinten).</p>
  </div>
</div>
"""

s0 = finde(e1, '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js')
s1 = finde(e1, "<script>", s0)
skripte = zeilen(e1, s0, s1 - 1)
hilfe = zeilen(e1, s1, finde(e1, "// ---------- Ebene 1 ----------") - 1)
hilfe = [z.replace("// Werkstatt-Ansicht: nur Ebene 1.", "// Werkstatt-Ansicht: nur Ebene 3 (Klappdeckel).")
          .replace("const HOME = { pos: V(190, 210, 300), target: V(-17.5, 30, 0) };", "const HOME = { pos: V(300, 330, 380), target: V(-45, 110, 0) };")
         for z in hilfe]
rib = zeilen(gz, finde(gz, "    function ribbon(p, pts, width, color) {"), finde(gz, "    function ribbon(p, pts, width, color) {") + 6)

rahmen = r"""
    // ---------- Ebene 3: Klappdeckel ----------
    // Alles von Ebene 3 hängt an „klapp“, dessen Ursprung auf der Scharnierachse liegt – so dreht der Regler den Deckel.
    const klapp = new THREE.Group(); klapp.position.set(__SX__, __SY__, 0); scene.add(klapp);
    const L0 = new THREE.Group(); L0.position.set(-(__SX__), -(__SY__), 0); klapp.add(L0);
    richtungsSchilder(scene);
    const ANCH = {};
    function anchor(key, g, x, y, z, d, label) { ANCH[key] = { g, p: V(x, y, z), label: label || key }; }
    const LEVEL = [50.25, 58, 84, 118];   // wie im großen Modell: [2] Unterkante Haube, [3] Unterseite des Dachs
    const TOP = [0, 61, 87, 121];        // [3] = Oberseite des Dachs (dort steht der LiDAR)
    let zeigeBauteile = true, glas = false;
    let sel = null;
    function eachMat(o, fn) { if (!o.material) return; (Array.isArray(o.material) ? o.material : [o.material]).forEach(fn); }
    function setOpacity(o, op) {
      eachMat(o, (m) => {
        const tr = op < 0.999;
        if (m.transparent !== tr) { m.transparent = tr; m.needsUpdate = true; }
        m.opacity = op; m.depthWrite = !tr;
      });
    }
    function anwenden() {
      L0.children.forEach((g) => {
        if (!g.userData.part) return;
        const d = g.userData.druckteil;
        g.visible = d ? true : zeigeBauteile;
        if (d === 'e3') g.traverse((o) => { if (o.isMesh) setOpacity(o, glas ? 0.25 : 1); });
      });
    }
    function m3Schraube(p, x, yKopfUnten, z, laenge, nachOben) {
      const s = new THREE.Group(); s.position.set(x, yKopfUnten, z); if (!nachOben) s.rotation.x = Math.PI; p.add(s);
      cylY(s, 2.75, 3, 0, 0, 0, 0x1b1c1e, { metal: 0.6, rough: 0.4, seg: 24 });
      cylY(s, 1.45, 0.3, 0, 2.75, 0, 0x050505, { seg: 6 });
      cylY(s, 1.5, laenge, 0, 3, 0, 0x2a2b2d, { metal: 0.7, rough: 0.35, seg: 16 });
      return s;
    }
__RIBBON__
    const deckelFarbe = (mat) => { mat.color.set(0x6a7178).convertSRGBToLinear(); mat.roughness = 0.8; };
    const HAUBE = ' Klappt hinten an zwei Scharnieren (Achse M3 × 18) nach hinten auf – dann liegt Ebene 2 offen. Vorne zwei M3 × 12 waagerecht durch die Vorderwand (Köpfe bündig) in die Laschen des Rings. Seiten oben schräg nach innen, Dachkanten 45° abgeschrägt. Zwei Hälften, Fuge bei x = 45: innen an Dach und Seiten ein 10 mm breiter Rand, 6 × M3 × 12. Mit dem Dach nach unten drucken, ohne Stützen.';
    [['e3_haube_vorne', 'Klapphaube Ebene 3, vordere Hälfte (Druckteil)', 'Vorne: Kamera in zwei Nuten hinter dem Fenster, Frontlicht unten in der Vorderwand, Pololu, Schraubpolster für die Laschen des Rings, oben steht der LiDAR. 80 × 180 mm. Datei: gehaeuse/ebene3/haube_vorne.stl'],
     ['e3_haube_hinten', 'Klapphaube Ebene 3, hintere Hälfte (Druckteil)', 'Pi 5 mit AI HAT+ hängt an 4 Domen unter dem Dach (M2,5 von oben, Köpfe bündig), 4G-Modul und GPS-Antenne in Taschen, hinten das runde Display im Dach und die Scharnier-Lappen. Lüftungsschlitze in den Seiten. 180 × 180 mm. Datei: gehaeuse/ebene3/haube_hinten.stl']].forEach(([datei, name, desc]) => {
      const g = part(L0, name, desc + HAUBE, 0, 0, 0);
      g.userData.druckteil = 'e3';
      cadTeil(datei, g, new THREE.Group(), (m) => m, deckelFarbe);
    });
    // Ebene 2 darunter (bleibt stehen, wenn der Deckel aufklappt)
    const unten2 = new THREE.Group(); scene.add(unten2);
    const e2Farbe = (mat) => { mat.color.set(0xd85a30).convertSRGBToLinear(); mat.roughness = 0.8; }, ringFarbe2 = (mat) => { mat.color.set(0x575d63).convertSRGBToLinear(); mat.roughness = 0.8; };
    ['e2_platte_vorne', 'e2_platte_hinten', 'e2_ring_vorne', 'e2_ring_hinten'].forEach((n) => cadTeil(n, unten2, new THREE.Group(), (m) => { m.traverse((o) => { o.userData.noPick = true; }); return m; }, n.includes('ring') ? ringFarbe2 : e2Farbe));
""".replace("__SX__", str(SCH_X)).replace("__SY__", str(SCH_Y)).replace("__RIBBON__", "\n".join(rib))

b0 = finde(gz, "    const PI = { x: -8, y: TOP[2] + 5, z: 0 };")
b1 = finde(gz, "// EBENE 4 – Dach") - 2
d0 = finde(gz, "const L3 = makeLayer(3);") + 1
d1 = finde(gz, "// VERDRAHTUNG – jede Leitung") - 2
teile = [z.replace("part(L2,", "part(L0,").replace("ribbon(L2,", "ribbon(L0,").replace("part(L3,", "part(L0,")
         for z in zeilen(gz, b0, b1) + zeilen(gz, d0, d1)]

bedienung = zeilen(e1, finde(e1, "    anwenden();", finde(e1, "PARTS[`Nahsensor VL53L1X")), finde(e1, "document.getElementById('glas').addEventListener"))
bedienung = [z.replace("<span>Zum Beispiel auf die Wanne, einen Motorbügel oder den Akku.</span>", "<span>Zum Beispiel auf den Pi, die Kamera oder die Haube.</span>")
               .replace("ray.intersectObjects([L0, stand], true)", "ray.intersectObjects([L0], true)")
               .replace("// durchsichtige Wanne: durch sie hindurch tippen", "// durchsichtige Haube: durch sie hindurch tippen")
             for z in bedienung]
bedienung = [z for z in bedienung if "getElementById('unten')" not in z and "getElementById('raeder')" not in z]
gi = next(i for i, z in enumerate(bedienung) if "getElementById('glas')" in z)
bedienung[gi] = "    document.getElementById('glas').addEventListener('change', (e) => { glas = e.target.checked; anwenden(); });"
bedienung += [
    "    document.getElementById('oben').addEventListener('click', () => { controls.autoRotate = false; rot.setAttribute('aria-pressed', 'false'); ansicht(V(-17.5, 470, 1), V(-17.5, 87, 0)); });",
    "    document.getElementById('unten2').addEventListener('change', (e) => { unten2.visible = e.target.checked; });",
    "    document.getElementById('klappen').addEventListener('input', (e) => {",
    "      const w = Number(e.target.value); klapp.rotation.z = w * Math.PI / 180;",
    "      document.getElementById('klappen-wert').textContent = w + '°'; if (sel) waehlen(sel);",
    "    });",
    "",
]
schluss = zeilen(e1, finde(e1, "    function applyTheme() {"), len(e1))

alles = kopf + [html] + skripte + hilfe + rahmen.split("\n") + teile + bedienung + schluss
(M / "ebene3-gehirn.html").write_text("\n".join(alles), encoding="utf-8")
print("geschrieben", len(alles), "Zeilen")
