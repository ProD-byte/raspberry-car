"""Erzeugt modell/ebene2-oben.html aus ebene1-unten.html (Gerüst, Hilfsfunktionen, Bedienung)
und raspberry-car-3d.html (Bauteile der Ebene 2)."""
import re
from pathlib import Path

M = Path(__file__).resolve().parent.parent   # Ordner modell/
e1 = (M / "ebene1-unten.html").read_text(encoding="utf-8").split("\n")
gz = (M / "raspberry-car-3d.html").read_text(encoding="utf-8").split("\n")


def zeilen(lst, von, bis):          # 1-basiert, inklusive
    return lst[von - 1:bis]


def finde(lst, text, ab=0):
    for i in range(ab, len(lst)):
        if text in lst[i]:
            return i + 1
    raise SystemExit("nicht gefunden: " + text)


# ---------- Kopf / CSS ----------
ende_css = finde(e1, "</head>")
kopf = zeilen(e1, 1, ende_css)
kopf = [z.replace("border-top: 4px solid var(--l0)", "border-top: 4px solid var(--l1)") for z in kopf]
kopf = [re.sub(r"<title>.*</title>", "<title>Werkstatt Ebene 2</title>", z) for z in kopf]

html = """<body>
<div class="wrap">
  <header>
    <nav class="seiten" aria-label="3D-Ansichten"><a href="ebene1-unten.html">Werkstatt Ebene 1</a><a href="ebene2-oben.html" aria-current="page">Werkstatt Ebene 2</a><a href="ebene3-gehirn.html">Werkstatt Ebene 3</a><a href="fahrsimulation.html">Fahrsimulation</a><a href="raspberry-car-3d.html">Ganzes Auto</a></nav>
    <div class="eyebrow">Raspberry Car · Werkstatt</div>
    <h1>Ebene 2: Antrieb</h1>
    <p class="lead">Nur das Elektronik-Deck, an dem wir gerade bauen – aufgeteilt in Zonen: vorne und hinten je eine <strong>Motorzone</strong> (Griffloch über den Motorsteckern, Motortreiber, 3,3-V-Verteiler), in der Mitte die <strong>Steuerung</strong> (Pico und Kompass), am Rand <strong>Strom und Laden</strong>. Ohne Kabel. Ziehen zum Drehen, Mausrad oder zwei Finger zum Zoomen. <strong>Tippe auf ein Bauteil</strong>, dann steht unten, was es ist.</p>
  </header>

  <div class="stage" id="stage">
    <div class="loading" id="loading">3D-Modell wird gebaut …</div>
    <div class="dims">Deck 205 × 130 × 3 mm · bis Ebene 3: 23 mm · vorne: Nahsensor · hinten: Ladebuchse und Schalter</div>
    <div class="info" id="info"><b>Tippe auf ein Bauteil</b><span>Zum Beispiel auf den Pico, den Kompass oder einen Motortreiber.</span></div>
  </div>

  <div class="controls">
    <label class="check"><input id="bauteile" type="checkbox" checked> Bauteile zeigen</label>
    <label class="check"><input id="ring" type="checkbox" checked> Gehäuse-Ring</label>
    <label class="check"><input id="glas" type="checkbox"> Ring durchsichtig</label>
    <label class="check"><input id="kompass" type="checkbox" checked> Freiraum um den Kompass</label>
    <label class="check"><input id="decke" type="checkbox"> Höhe von Ebene 3</label>
    <label class="check"><input id="wanne" type="checkbox"> Wanne darunter</label>
    <div class="toggles">
      <button id="rotate" type="button" aria-pressed="true">Drehen</button>
      <button id="oben" type="button">Von oben</button>
      <button id="unten" type="button">Von unten</button>
      <button id="reset" type="button">Ansicht zurücksetzen</button>
    </div>
  </div>

  <div class="teile" id="teile"></div>

  <div class="notes">
    <p><strong>Druckdateien:</strong> <code>gehaeuse/ebene2/</code>, erzeugt von <code>gehaeuse/ebene2_elektronik.py</code>. Beschreibung und Zusammenbau: <code>gehaeuse/README.md</code>.</p>
    <p><strong>Kompass:</strong> Der BNO085 sitzt vor dem Pico, ca. 5 cm vom vorderen und 10 cm vom hinteren Motor. Der grüne Kreis (Haken „Freiraum um den Kompass“, 5 cm) zeigt, wo kein Magnet, keine Spule und keine Leitung mit viel Strom hin darf. Der Pico darf hinein – er macht kaum ein Magnetfeld. Der MP1584 (Spule) sitzt deshalb rechts neben dem Pico, ca. 7 cm entfernt, Plus und Minus kommen am rechten Rand durch Durchbruch C hoch.</p>
    <p><strong>Erreichbar:</strong> Ebene 3 wird ein Klappdeckel (Scharnier an den beiden hinteren Domen, vorne eine Schraube). Deckel auf – dann liegen alle Klemmen offen, und durch die beiden Grifflöcher steckt man die Motorstecker direkt am Motor ein und aus.</p>
    <p><strong>Erreichbarkeit geprüft:</strong> <code>gehaeuse/ebene2_elektronik.py</code> prüft bei jedem Lauf nicht nur Überschneidungen, sondern auch, ob man herankommt: vor jeder Klemmen-Reihe 13 mm frei für Kabel, vor jeder WAGO-Kabelseite 15 mm, vor jeder STEMMA-QT-Buchse 12 mm, um jedes Griffloch nichts Hohes, unter dem Schalter frei. Ergebnis: 0 Probleme.</p>
    <p><strong>Höhe:</strong> Zwischen Deck und Ebene 3 sind 23 mm Platz (Haken „Höhe von Ebene 3“). Am höchsten ist der Pico auf dem Freenove-Board – die echte Höhe vor dem Druck nachmessen.</p>
    <p><strong>Das ganze Auto</strong> mit allen Ebenen und Kabeln zeigt <code>raspberry-car-3d.html</code>, die Wanne darunter <code>ebene1-unten.html</code>.</p>
  </div>
</div>
"""

# ---------- Skripte laden ----------
s0 = finde(e1, '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js')
s1 = finde(e1, "<script>", s0)
skripte = zeilen(e1, s0, s1 - 1)

# ---------- Gerüst + Hilfsfunktionen (bis vor "// ---------- Ebene 1 ----------") ----------
h0 = s1
h1 = finde(e1, "// ---------- Ebene 1 ----------") - 1
hilfe = zeilen(e1, h0, h1)
hilfe = [z.replace("// Werkstatt-Ansicht: nur Ebene 1. Die Bauteile sind dieselben wie in raspberry-car-3d.html",
                   "// Werkstatt-Ansicht: nur Ebene 2. Die Bauteile sind dieselben wie in raspberry-car-3d.html")
          .replace("// (gleiche Maße und Positionen) – ändert sich dort etwas an Ebene 1, hier mit ändern.",
                   "// (gleiche Maße und Positionen) – ändert sich dort etwas an Ebene 2, hier mit ändern.")
          .replace("const HOME = { pos: V(190, 210, 300), target: V(-17.5, 30, 0) };",
                   "const HOME = { pos: V(170, 270, 260), target: V(-17.5, 62, 0) };")
         for z in hilfe]

# ---------- Ebene 2: Rahmen ----------
rahmen = r"""
    // ---------- Ebene 2 ----------
    const L0 = new THREE.Group(); scene.add(L0);
    richtungsSchilder(scene);
    const ANCH = {};
    function anchor(key, g, x, y, z, d, label) { ANCH[key] = { g, p: V(x, y, z), label: label || key }; }
    const TOP = [0, 61];           // Oberkante des Elektronik-Decks (liegt bei 58 mm auf dem Wannenrand, 3 mm dick)
    const PIN = __PIN__;
    let zeigeBauteile = true, zeigeRing = true, glas = false;
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
        g.visible = d === 'ring' ? zeigeRing : (d ? true : zeigeBauteile);
        if (d === 'ring') g.traverse((o) => { if (o.isMesh) setOpacity(o, glas ? 0.25 : 1); });
      });
    }
    function m3Schraube(p, x, yKopfUnten, z, laenge, nachOben) {
      const s = new THREE.Group(); s.position.set(x, yKopfUnten, z); if (!nachOben) s.rotation.x = Math.PI; p.add(s);
      cylY(s, 2.75, 3, 0, 0, 0, 0x1b1c1e, { metal: 0.6, rough: 0.4, seg: 24 });
      cylY(s, 1.45, 0.3, 0, 2.75, 0, 0x050505, { seg: 6 });
      cylY(s, 1.5, laenge, 0, 3, 0, 0x2a2b2d, { metal: 0.7, rough: 0.35, seg: 16 });
      return s;
    }
    const deckFarbe = (mat) => { mat.color.set(0x5f9e95).convertSRGBToLinear(); mat.roughness = 0.8; };
    (function deck() {
      const g = part(L0, 'Elektronik-Deck Ebene 2 (Druckteil)', 'In Zonen aufgeteilt: vorne und hinten je eine Motorzone (Griffloch mit Rand über den beiden Motorsteckern, DRV8833 und 3,3-V-Verteiler für diese Achse), in der Mitte Pico auf dem Freenove-Board (Klemmen zu den Seiten) und davor der Kompass BNO085, hinten links das Ladeboard, rechts MP1584 und Strom-Durchbruch C. Ist zugleich der Deckel der Wanne: liegt auf dem Wannenrand, die Wanne wird von unten mit 4 × M3 × 45 an 4 Dome dieses Decks geschraubt. 4 Dome mit Kernloch für Ebene 3 – die beiden hinteren tragen das Scharnier des Klappdeckels. Dazu Durchbrüche hinten links/rechts (Daten), A/B an den Seiten und C am rechten Rand (Strom). Alles auf der Oberseite – druckt flach ohne Stützen. 205 × 130 × 3 mm. Datei: gehaeuse/ebene2/platte.stl', 0, 0, 0);
      g.userData.druckteil = 'deck';
      cadTeil('e2_platte', g, new THREE.Group(), (m) => m, deckFarbe);
    })();
    (function ring() {
      const g = part(L0, 'Gehäuse-Ring oben (Druckteil)', 'Seitenwand zwischen Elektronik-Deck und Ebene 3, 23 mm hoch. In der Rückwand: links (von hinten) das Loch Ø 12,2 mm für den 12-mm-Taster, rechts ein Ausschnitt 13,5 × 8 mm (außen angefast) für die USB-C-Buchse des Ladeboards. Röhren über den 4 Domen – dort wird Ebene 3 festgeschraubt. Umgedreht drucken (Oberkante aufs Bett), ohne Stützen. Datei: gehaeuse/ebene2/ring_oben.stl', 0, 0, 0);
      g.userData.druckteil = 'ring';
      cadTeil('e2_ring_oben', g, new THREE.Group(), (m) => m, deckFarbe);
    })();
    // Wanne darunter (nur zur Orientierung, durchsichtig, nicht anklickbar)
    const wanneGrau = new THREE.Group(); wanneGrau.visible = false; scene.add(wanneGrau);
    cadTeil('e1_wanne', wanneGrau, new THREE.Group(), (m) => { m.traverse((o) => { o.userData.noPick = true; }); return m; },
      (mat) => { mat.color.set(0x9aa3aa).convertSRGBToLinear(); mat.transparent = true; mat.opacity = 0.22; mat.depthWrite = false; });
"""
pin = next(z for z in gz if "const PIN = {" in z).strip()[len("const PIN = "):].rstrip(";")
rahmen = rahmen.replace("__PIN__", pin)

# ---------- Ebene 2: Bauteile aus dem großen Modell ----------
b0 = finde(gz, "(function sw() {")
b1 = finde(gz, "wago(L1, 'W3H'")
teile = zeilen(gz, b0, b1)
teile = [z.replace("part(L1,", "part(L0,").replace("wago(L1,", "wago(L0,") for z in teile]
teile = [z for z in teile if "nurImAuto = true" not in z or "m3Schraube" in z]   # Micro-USB-Stecker des Pi-Kabels weglassen
teile = [z.replace(").userData.nurImAuto = true));", ")));") for z in teile]
w0 = finde(e1, "    function wago(parent, key, name, desc, x, y, z, ry = 0) {")
wago = zeilen(e1, w0, w0 + 10)
assert wago[-1].strip() == "}", wago[-1]

extra = r"""
    // Freiraum um den Kompass: 5 cm rund um den BNO085 – kein Magnet, keine Spule, keine Leitung mit viel Strom
    const kompass = new THREE.Group(); scene.add(kompass);
    (function () {
      const ring = new THREE.Mesh(new THREE.RingGeometry(48.5, 50, 96), new THREE.MeshBasicMaterial({ color: 0x1d9e75, transparent: true, opacity: 0.85, side: THREE.DoubleSide, depthWrite: false }));
      ring.rotation.x = -Math.PI / 2; ring.position.set(8, TOP[1] + 0.3, 0); ring.userData.noPick = true; kompass.add(ring);
      const flaeche = new THREE.Mesh(new THREE.CircleGeometry(48.5, 96), new THREE.MeshBasicMaterial({ color: 0x1d9e75, transparent: true, opacity: 0.12, side: THREE.DoubleSide, depthWrite: false }));
      flaeche.rotation.x = -Math.PI / 2; flaeche.position.set(8, TOP[1] + 0.25, 0); flaeche.userData.noPick = true; kompass.add(flaeche);
    })();
    // Unterkante von Ebene 3 (84 mm): so hoch darf nichts auf dem Deck werden
    const decke = new THREE.Mesh(new THREE.BoxGeometry(205, 0.6, 130), new THREE.MeshStandardMaterial({ color: 0x3f6db5, transparent: true, opacity: 0.2, depthWrite: false }));
    decke.position.set(-17.5, 84, 0); decke.visible = false; decke.userData.noPick = true; scene.add(decke);
"""

# ---------- Liste, Auswahl, Bedienung ----------
l0 = finde(e1, "    anwenden();", finde(e1, "PARTS[`Nahsensor VL53L1X"))
l1 = finde(e1, "document.getElementById('glas').addEventListener")
bedienung = zeilen(e1, l0, l1)
bedienung = [z.replace("<span>Zum Beispiel auf die Wanne, einen Motorbügel oder den Akku.</span>", "<span>Zum Beispiel auf den Pico, den Kompass oder einen Motortreiber.</span>")
               .replace("ray.intersectObjects([L0, stand], true)", "ray.intersectObjects([L0], true)")
               .replace("// durchsichtige Wanne: durch sie hindurch tippen", "// durchsichtiger Ring: durch ihn hindurch tippen")
             for z in bedienung]
bedienung = [z for z in bedienung if "getElementById('unten')" not in z and "getElementById('raeder')" not in z]
bedienung += [
    "    document.getElementById('oben').addEventListener('click', () => { controls.autoRotate = false; rot.setAttribute('aria-pressed', 'false'); ansicht(V(-17.5, 430, 1), V(-17.5, 61, 0)); });",
    "    document.getElementById('unten').addEventListener('click', () => { controls.autoRotate = false; rot.setAttribute('aria-pressed', 'false'); ansicht(V(-17.5, -330, 60), V(-17.5, 60, 0)); });",
    "    document.getElementById('ring').addEventListener('change', (e) => { zeigeRing = e.target.checked; anwenden(); if (sel) waehlen(sel); });",
    "    document.getElementById('kompass').addEventListener('change', (e) => { kompass.visible = e.target.checked; });",
    "    document.getElementById('decke').addEventListener('change', (e) => { decke.visible = e.target.checked; });",
    "    document.getElementById('wanne').addEventListener('change', (e) => { wanneGrau.visible = e.target.checked; });",
    "",
]
glas_i = next(i for i, z in enumerate(bedienung) if "getElementById('glas')" in z)
bedienung[glas_i] = "    document.getElementById('glas').addEventListener('change', (e) => { glas = e.target.checked; anwenden(); });"

e0 = finde(e1, "    function applyTheme() {")
schluss = zeilen(e1, e0, len(e1))

alles = kopf + [html] + skripte + hilfe + rahmen.split("\n") + wago + teile + extra.split("\n") + bedienung + schluss
(M / "ebene2-oben.html").write_text("\n".join(alles), encoding="utf-8")
print("geschrieben", len(alles), "Zeilen")
