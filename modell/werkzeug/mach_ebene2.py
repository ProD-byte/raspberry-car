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
    <p class="lead">Nur das Elektronik-Deck, an dem wir gerade bauen – aufgeteilt in Zonen: vorne und hinten je eine <strong>Motorzone</strong> (zwei Grifflöcher über den Motorsteckern, Motortreiber, 3,3-V-Verteiler), in der Mitte die <strong>Steuerung</strong> (vorne Pico, hinten Kompass), am Rand <strong>Strom und Laden</strong>. Deck und Ring sind je aus zwei Hälften gedruckt. Ohne Kabel. Ziehen zum Drehen, Mausrad oder zwei Finger zum Zoomen. <strong>Tippe auf ein Bauteil</strong>, dann steht unten, was es ist.</p>
  </header>

  <div class="stage" id="stage">
    <div class="loading" id="loading">3D-Modell wird gebaut …</div>
    <div class="dims">Deck 250 × 180 × 3 mm (2 Hälften) · bis Ebene 3: 23 mm · vorne: Nahsensor · hinten: Ladebuchse und Schalter</div>
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
    <p><strong>Zwei Hälften:</strong> Das Deck ist bei x = 58 geteilt (zwei aufrechte Stege, 2 × M3 × 10 quer), der Ring bei x = −16,5. Jede Ring-Hälfte ist mit eigenen M3 × 20 auf das Deck geschraubt – so überbrückt der Ring die Fuge des Decks und das Deck die Fuge des Rings.</p>
    <p><strong>Kompass:</strong> Der BNO085 sitzt hinten in der Mitte, ca. 12 cm von der Stromversorgung (vorne in der Wanne) und von Durchbruch C entfernt. Der grüne Kreis (Haken „Freiraum um den Kompass“, 5 cm) zeigt, wo kein Magnet, keine Spule und keine Leitung mit viel Strom hin darf. Darunter liegt in der Wanne der Akku (4 cm tiefer) – ob sein Strom den Kompass stört, zeigt erst ein Test mit dem echten Auto.</p>
    <p><strong>Erreichbar:</strong> Ebene 3 ist ein Klappdeckel (Scharnier hinten am Ring, vorne zwei Schrauben). Deckel auf – dann liegen alle Klemmen offen, und durch die vier Grifflöcher steckt man die Motorstecker direkt am Motor ein und aus.</p>
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
          .replace("const HOME = { pos: V(240, 250, 360), target: V(0, 30, 0) };",
                   "const HOME = { pos: V(210, 320, 300), target: V(0, 62, 0) };")
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
    const deckFarbe = (mat) => { mat.color.set(0xd85a30).convertSRGBToLinear(); mat.roughness = 0.8; };
    const ringFarbe = (mat) => { mat.color.set(0x575d63).convertSRGBToLinear(); mat.roughness = 0.8; };
    const ALLE = ' Ist zugleich der Deckel der Wanne: liegt auf dem Wannenrand, die Wanne wird von unten mit 4 × M3 × 45 an 4 Dome des Decks geschraubt. Das Deck ist bei x = 58 geteilt: an der Fuge auf jeder Hälfte ein aufrechter Steg, beide mit 2 × M3 × 10 quer verschraubt. Alles auf der Oberseite – druckt flach ohne Stützen.';
    [['e2_platte_vorne', 'Elektronik-Deck Ebene 2, vordere Hälfte (Druckteil)', 'Motorzone vorne: zwei Grifflöcher mit Rand über den Motorsteckern der Vorderachse, dazwischen der Motortreiber DRV8833, rechts außen der 3,3-V-Verteiler. 67 × 180 mm. Datei: gehaeuse/ebene2/platte_vorne.stl'],
     ['e2_platte_hinten', 'Elektronik-Deck Ebene 2, hintere Hälfte (Druckteil)', 'Vorne der Pico auf dem Freenove-Board (Klemmen zu den Seiten), dahinter der Kompass BNO085, vorne rechts MP1584 und Strom-Durchbruch C, hinten die Motorzone hinten (zwei Grifflöcher, Treiber, 3,3-V-Verteiler), hinten links das Ladeboard. Dome für den Ring (M3 × 20 von oben). 183 × 180 mm. Datei: gehaeuse/ebene2/platte_hinten.stl']].forEach(([datei, name, desc]) => {
      const g = part(L0, name, desc + ALLE, 0, 0, 0);
      g.userData.druckteil = 'deck';
      cadTeil(datei, g, new THREE.Group(), (m) => m, deckFarbe);
    });
    [['e2_ring_vorne', 'Gehäuse-Ring oben, vordere Hälfte (Druckteil)', 'Seitenwand zwischen Elektronik-Deck und Ebene 3, 23 mm hoch. Vorne die zwei Laschen, in die die Schrauben des Klappdeckels greifen. Hülsen über den Domen des Decks: vorne in den Ecken und zwei an der Fuge des Rings. Aufrecht drucken, ohne Stützen. Datei: gehaeuse/ebene2/ring_vorne.stl'],
     ['e2_ring_hinten', 'Gehäuse-Ring oben, hintere Hälfte (Druckteil)', 'Hinten die Scharnier-Lappen des Klappdeckels, in der Rückwand in Fahrtrichtung links der Ausschnitt 13,5 × 8 mm für die USB-C-Buchse des Ladeboards und rechts das Loch Ø 12,2 mm für den 12-mm-Taster. Hülsen über den Domen des Decks (M3 × 20 von oben). Aufrecht drucken, ohne Stützen. Datei: gehaeuse/ebene2/ring_hinten.stl']].forEach(([datei, name, desc]) => {
      const g = part(L0, name, desc, 0, 0, 0);
      g.userData.druckteil = 'ring';
      cadTeil(datei, g, new THREE.Group(), (m) => m, ringFarbe);
    });
    // Schutzbleche: 4 × dasselbe Druckteil (vorne links modelliert; rechts um 180° gedreht), am Ring von Ebene 2 verschraubt
    [[0, false], [-160, false], [160, true], [0, true]].forEach(([dx, rechts]) => {
      const w = part(L0, 'Schutzblech (4 × Druckteil)', 'Kotflügel über dem Rad (gehaeuse/schutzblech.py): eckiger Bogen (flaches Dach, schräge Schultern, steile Flanken) mit mindestens 4,5 mm Luft zum Reifen, außen ein nach innen gezogener Rand. Der 6 mm dicke Flansch liegt am Gehäuse-Ring von Ebene 2 an und wird mit 2 × M3 × 10 von außen in zwei Schraubsäulen des Rings geschraubt (Köpfe bündig) – nicht an der Wanne, die bleibt nach unten abnehmbar. Die Schrauben sitzen so weit außen, dass der Schraubendreher am Rad vorbeikommt. Viermal dasselbe Teil (rechts um 180° gedreht). Flansch-Rückseite aufs Bett, ohne Stützen. Datei: gehaeuse/schutzbleche/schutzblech.stl', dx, 0, 0);
      w.userData.druckteil = 'ring'; if (rechts) w.rotation.y = Math.PI;
      cadTeil('schutzblech', w, new THREE.Group(), (m) => m, (mat) => { mat.color.set(0xd85a30).convertSRGBToLinear(); mat.roughness = 0.6; mat.metalness = 0; });
    });
    // Wanne darunter (nur zur Orientierung, durchsichtig, nicht anklickbar)
    const wanneGrau = new THREE.Group(); wanneGrau.visible = false; scene.add(wanneGrau);
    ['e1_wanne_vorne', 'e1_wanne_hinten'].forEach((n) => cadTeil(n, wanneGrau, new THREE.Group(), (m) => { m.traverse((o) => { o.userData.noPick = true; }); return m; },
      (mat) => { mat.color.set(0x9aa3aa).convertSRGBToLinear(); mat.transparent = true; mat.opacity = 0.22; mat.depthWrite = false; }));
"""
pin = next(z for z in gz if "const PIN = {" in z).strip()[len("const PIN = "):].rstrip(";")
rahmen = rahmen.replace("__PIN__", pin)


def schrauben_block(gz, aufruf):
    """Funktion schraubenDerDruckteile aus dem großen Modell + Aufruf für diese Seite (siehe raspberry-car-3d.html)."""
    a = next(i for i, z in enumerate(gz) if ">>> SCHRAUBEN" in z)
    b = next(i for i, z in enumerate(gz) if "<<< SCHRAUBEN" in z)
    return gz[a:b + 1] + ["    " + aufruf]


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
      ring.rotation.x = -Math.PI / 2; ring.position.set(-35, TOP[1] + 0.3, 0); ring.userData.noPick = true; kompass.add(ring);
      const flaeche = new THREE.Mesh(new THREE.CircleGeometry(48.5, 96), new THREE.MeshBasicMaterial({ color: 0x1d9e75, transparent: true, opacity: 0.12, side: THREE.DoubleSide, depthWrite: false }));
      flaeche.rotation.x = -Math.PI / 2; flaeche.position.set(-35, TOP[1] + 0.25, 0); flaeche.userData.noPick = true; kompass.add(flaeche);
    })();
    // Unterkante von Ebene 3 (84 mm): so hoch darf nichts auf dem Deck werden
    const decke = new THREE.Mesh(new THREE.BoxGeometry(250, 0.6, 180), new THREE.MeshStandardMaterial({ color: 0x3f6db5, transparent: true, opacity: 0.2, depthWrite: false }));
    decke.position.set(0, 84, 0); decke.visible = false; decke.userData.noPick = true; scene.add(decke);
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
    "    document.getElementById('oben').addEventListener('click', () => { controls.autoRotate = false; rot.setAttribute('aria-pressed', 'false'); ansicht(V(0, 470, 1), V(0, 61, 0)); });",
    "    document.getElementById('unten').addEventListener('click', () => { controls.autoRotate = false; rot.setAttribute('aria-pressed', 'false'); ansicht(V(0, -360, 60), V(0, 60, 0)); });",
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

alles = kopf + [html] + skripte + hilfe + rahmen.split("\n") + wago + teile + extra.split("\n") + schrauben_block(gz, "schraubenDerDruckteile(null, L0, null);") + bedienung + schluss
(M / "ebene2-oben.html").write_text("\n".join(alles), encoding="utf-8")
print("geschrieben", len(alles), "Zeilen")
