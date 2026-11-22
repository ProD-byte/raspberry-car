"""Setzt Ebene 2 (Deck, Ring, Bauteile) in die Fahrsimulation – Bauteile als Kopie aus raspberry-car-3d.html.
Kann mehrfach laufen: ersetzt den Block zwischen den Markierungen."""
from pathlib import Path

M = Path(__file__).resolve().parent.parent   # Ordner modell/
sim = (M / "fahrsimulation.html").read_text(encoding="utf-8")
gz = (M / "raspberry-car-3d.html").read_text(encoding="utf-8").split("\n")


def finde(lst, text):
    for i, z in enumerate(lst):
        if text in z:
            return i
    raise SystemExit("nicht gefunden: " + text)


b0 = finde(gz, "(function sw() {")
b1 = finde(gz, "wago(L1, 'W3H'")
teile = [z.replace("part(L1,", "part(E2,").replace("wago(L1,", "wago(E2,") for z in gz[b0:b1 + 1]]
teile = [z for z in teile if "nurImAuto = true" not in z or "m3Schraube" in z]
teile = [z.replace(").userData.nurImAuto = true));", ")));") for z in teile]
pin = next(z for z in gz if "const PIN = {" in z).strip()

ANF, END = "    // >>> EBENE 2 (automatisch eingefügt, sim_ebene2.py)", "    // <<< EBENE 2"
block = [ANF,
         "    // Ebene 2 (Elektronik-Deck mit Ring und Bauteilen) – dieselben Bauteile wie in raspberry-car-3d.html.",
         "    // Ändert sich dort etwas an Ebene 2, dieses Skript neu laufen lassen (siehe CLAUDE.md).",
         "    const E2 = new THREE.Group(); auto.add(E2);",
         "    const TOP = [0, 61];",
         "    " + pin,
         "    const deckFarbe = (mat) => { mat.color.set(0x5f9e95).convertSRGBToLinear(); mat.roughness = 0.8; };",
         "    (function () {",
         "      [['e2_platte_vorne', 'Elektronik-Deck Ebene 2, vordere Hälfte (Druckteil)', 'deck'], ['e2_platte_hinten', 'Elektronik-Deck Ebene 2, hintere Hälfte (Druckteil)', 'deck'],",
         "       ['e2_ring_vorne', 'Gehäuse-Ring oben, vordere Hälfte (Druckteil)', 'ring'], ['e2_ring_hinten', 'Gehäuse-Ring oben, hintere Hälfte (Druckteil)', 'ring']].forEach(([datei, name, art]) => {",
         "        const d = part(E2, name, 'Teil von Ebene 2 (Elektronik-Deck mit Ring). Einzelheiten: Werkstatt Ebene 2.', 0, 0, 0);",
         "        d.userData.druckteil = art; cadTeil(datei, d, new THREE.Group(), (m) => m, deckFarbe);",
         "      });",
         "      // Ebene 3: die Klapphaube (nur die Druckteile, zur Form und zum Gewicht)",
         "      const E3 = new THREE.Group(); auto.add(E3); window.__E3 = E3;",
         "      const haubeFarbe = (mat) => { mat.color.set(0x5a7fbf).convertSRGBToLinear(); mat.roughness = 0.8; };",
         "      [['e3_haube_vorne', 'Klapphaube Ebene 3, vordere Hälfte (Druckteil)'], ['e3_haube_hinten', 'Klapphaube Ebene 3, hintere Hälfte (Druckteil)']].forEach(([datei, name]) => {",
         "        const h = part(E3, name, 'Teil von Ebene 3 (Klapphaube mit Dach). Einzelheiten: Werkstatt Ebene 3.', 0, 0, 0);",
         "        h.userData.druckteil = 'haube'; cadTeil(datei, h, new THREE.Group(), (m) => m, haubeFarbe);",
         "      });",
         "    })();"] + teile + [END]

if ANF in sim:
    i = sim.index(ANF); j = sim.index(END) + len(END)
    sim = sim[:i] + "\n".join(block) + sim[j:]
else:
    marke = "      PARTS[`Nahsensor VL53L1X (${n})`].rotation.set(0, ry, 5 * Math.PI / 180);\n    });\n"
    assert sim.count(marke) == 1
    sim = sim.replace(marke, marke + "\n" + "\n".join(block) + "\n")

# Schalter "Ebene 2 zeigen" in die Bedienung
if 'id="ebene2"' not in sim:
    a = '      <div class="controls">\n        <label class="range" for="tempo">'
    assert sim.count(a) == 1
    sim = sim.replace(a, '      <div class="controls">\n        <label class="check"><input id="ebene2" type="checkbox" checked> Ebene 2 zeigen</label>\n        <label class="range" for="tempo">')
    a = "    // ===================================================================\n    // FAHRZEUG-DATEN (mm, kg, s)"
    assert sim.count(a) == 1
    sim = sim.replace(a, "    document.getElementById('ebene2').addEventListener('change', (e) => { E2.visible = e.target.checked; });\n\n" + a)
sim = sim.replace("<h1>So fährt das Fahrwerk im Gelände</h1>", "<h1>So fährt das Auto im Gelände</h1>")
sim = sim.replace("Das Fahrwerk aus der Werkstatt (Ebene 1) auf verschiedenem Untergrund.", "Das Fahrwerk (Ebene 1) mit dem Elektronik-Deck (Ebene 2) auf verschiedenem Untergrund – Ebene 2 lässt sich ausblenden.")
(M / "fahrsimulation.html").write_text(sim, encoding="utf-8")
print("ok", len(teile), "Zeilen Bauteile")
