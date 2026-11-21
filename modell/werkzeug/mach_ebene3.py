"""Erzeugt modell/ebene3-gehirn.html (Werkstatt-Ansicht Ebene 3, Klappdeckel) aus ebene1-unten.html
(Gerüst, Hilfsfunktionen, Bedienung) und raspberry-car-3d.html (Bauteile der Ebene 3).
Nach Änderungen an Ebene 3 im großen Modell neu laufen lassen."""
import re
from pathlib import Path

M = Path(__file__).resolve().parent.parent   # Ordner modell/
e1 = (M / "ebene1-unten.html").read_text(encoding="utf-8").split("\n")
gz = (M / "raspberry-car-3d.html").read_text(encoding="utf-8").split("\n")

SCH_X, SCH_Y = -125.5, 89.0                  # Scharnierachse (wie gehaeuse/ebene2_elektronik.py)


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
    <h1>Ebene 3: Gehirn (Klappdeckel)</h1>
    <p class="lead">Der obere Teil des Autos ist ein <strong>Klappdeckel</strong>: Boden und Seitenwände in einem Druckteil, hinten zwei Scharniere, vorne zwei Schrauben. Darin sitzen Raspberry Pi 5 mit Active Cooler und AI HAT+, die Kamera hinter dem Fenster vorne, der Pololu (5 V für den Pi) und das 4G/GPS-Modul. Mit dem Regler klappst du den Deckel auf. Ohne Kabel.</p>
  </header>

  <div class="stage" id="stage">
    <div class="loading" id="loading">3D-Modell wird gebaut …</div>
    <div class="dims">Deckel 215,5 × 130 × 48 mm · vorne: Kamera · hinten: Scharniere, Ladebuchse und Schalter</div>
    <div class="info" id="info"><b>Tippe auf ein Bauteil</b><span>Zum Beispiel auf den Pi, die Kamera oder den Deckel.</span></div>
  </div>

  <div class="controls">
    <label class="check"><input id="bauteile" type="checkbox" checked> Bauteile zeigen</label>
    <label class="check"><input id="glas" type="checkbox"> Deckel durchsichtig</label>
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
    <p><strong>Druckdatei:</strong> <code>gehaeuse/ebene3/deckel.stl</code>, erzeugt von <code>gehaeuse/ebene3_gehirn.py</code> – ein Teil, Boden aufs Bett, ohne Stützen. Das Skript prüft auch, dass der Deckel beim Aufklappen bis 100° nirgends am Ring von Ebene 2 anstößt.</p>
    <p><strong>Klappdeckel:</strong> Hinten zwei Scharniere außen an der Trennfuge (Achse M3 × 16, Gewinde im äußeren Lappen). Vorne zwei M3 × 12 waagerecht durch die Vorderwand (Köpfe bündig) in die Laschen, die vom Ring von Ebene 2 durch den Boden nach oben ragen. Schrauben raus, Deckel hochklappen – Ebene 2 liegt offen.</p>
    <p><strong>Pi 5:</strong> M2,5 von unten durch Boden und Dom in die 16-mm-Abstandshalter des AI HAT+ (liegen bei). M2,5, weil die Löcher des Pi nur 2,7 mm groß sind. <strong>Kamera:</strong> von oben in die zwei Nuten schieben, das Objektiv sitzt im Fenster. <strong>Luft:</strong> Schlitze in beiden Seitenwänden – der AI HAT+ darf nicht ohne Belüftung eingebaut werden.</p>
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
    const TOP = [0, 61, 87];       // Oberkante Deck Ebene 2 (61) und Boden Ebene 3 (87)
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
    const deckelFarbe = (mat) => { mat.color.set(0x5a7fbf).convertSRGBToLinear(); mat.roughness = 0.8; };
    (function deckel() {
      const g = part(L0, 'Klappdeckel Ebene 3 (Druckteil)', 'Boden von Ebene 3 und Seitenwände bis Ebene 4 in einem Stück. Klappt hinten an zwei Scharnieren (Achse M3 × 16) nach hinten auf – dann liegt Ebene 2 offen. Vorne zwei M3 × 12 waagerecht durch die Vorderwand (Köpfe bündig) in die Laschen des Rings von Ebene 2. Trägt Pi 5 (4 Dome, M2,5 von unten), Pololu und 4G-Modul in Einklick-Taschen, die Kamera in zwei Nuten hinter dem Fenster vorne; Lüftungsschlitze in den Seiten; 4 Röhren für Ebene 4. Druckt mit dem Boden aufs Bett ohne Stützen. 215,5 × 130 × 48 mm. Datei: gehaeuse/ebene3/deckel.stl', 0, 0, 0);
      g.userData.druckteil = 'e3';
      cadTeil('e3_deckel', g, new THREE.Group(), (m) => m, deckelFarbe);
    })();
    // Ebene 2 darunter (bleibt stehen, wenn der Deckel aufklappt)
    const unten2 = new THREE.Group(); scene.add(unten2);
    const e2Farbe = (mat) => { mat.color.set(0x5f9e95).convertSRGBToLinear(); mat.roughness = 0.8; };
    ['e2_platte', 'e2_ring_oben'].forEach((n) => cadTeil(n, unten2, new THREE.Group(), (m) => { m.traverse((o) => { o.userData.noPick = true; }); return m; }, e2Farbe));
""".replace("__SX__", str(SCH_X)).replace("__SY__", str(SCH_Y)).replace("__RIBBON__", "\n".join(rib))

b0 = finde(gz, "    const PI = { x: -8, y: TOP[2] + 5, z: 0 };")
b1 = finde(gz, "// EBENE 4 – Dach") - 2
teile = [z.replace("part(L2,", "part(L0,").replace("ribbon(L2,", "ribbon(L0,") for z in zeilen(gz, b0, b1)]

bedienung = zeilen(e1, finde(e1, "    anwenden();", finde(e1, "PARTS[`Nahsensor VL53L1X")), finde(e1, "document.getElementById('glas').addEventListener"))
bedienung = [z.replace("<span>Zum Beispiel auf die Wanne, einen Motorbügel oder den Akku.</span>", "<span>Zum Beispiel auf den Pi, die Kamera oder den Deckel.</span>")
               .replace("ray.intersectObjects([L0, stand], true)", "ray.intersectObjects([L0], true)")
               .replace("// durchsichtige Wanne: durch sie hindurch tippen", "// durchsichtiger Deckel: durch ihn hindurch tippen")
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
