// Einzelansicht: ein Bauteil allein als 3D-Modell anschauen (Doppelklick auf ein Bauteil oder Knopf „Als Modell ansehen“).
// Wird von allen 3D-Ansichten geladen (großes Modell, Werkstatt-Seiten, Fahrsimulation). Braucht THREE und THREE.OrbitControls.
// Das Bauteil wird kopiert (Formen geteilt, Farben eigene Kopie) – an der großen Ansicht ändert sich nichts.
(function () {
  let ov = null, renderer = null, scene = null, camera = null, controls = null, halter = null, laeuft = false, vorherFokus = null;

  function css(name, ersatz) {
    const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v || ersatz;
  }

  function aufbauen() {
    ov = document.createElement('div');
    ov.setAttribute('role', 'dialog');
    ov.setAttribute('aria-modal', 'true');
    ov.setAttribute('aria-label', 'Bauteil als Modell');
    ov.style.cssText = 'position:fixed;inset:0;z-index:1000;display:none;align-items:center;justify-content:center;padding:16px;background:rgba(10,14,18,.55);';
    const box = document.createElement('div');
    box.style.cssText = 'position:relative;width:min(900px,100%);height:min(680px,100%);display:flex;flex-direction:column;border-radius:14px;overflow:hidden;' +
      'background:' + css('--surface', '#ffffff') + ';color:' + css('--fg', '#14181c') + ';border:1px solid ' + css('--line', '#d5dbe0') + ';box-shadow:0 20px 60px rgba(0,0,0,.35);';
    const kopf = document.createElement('div');
    kopf.style.cssText = 'display:flex;gap:12px;align-items:flex-start;padding:12px 14px 8px;';
    const texte = document.createElement('div');
    texte.style.cssText = 'flex:1;min-width:0;';
    const titel = document.createElement('b'); titel.className = 'ea-titel';
    titel.style.cssText = 'display:block;font-size:16px;line-height:1.3;';
    const mass = document.createElement('span'); mass.className = 'ea-mass';
    mass.style.cssText = 'display:block;font-size:12px;opacity:.7;margin-top:2px;font-family:ui-monospace,Menlo,Consolas,monospace;';
    texte.append(titel, mass);
    const zu = document.createElement('button');
    zu.type = 'button'; zu.textContent = '✕'; zu.setAttribute('aria-label', 'Schließen');
    zu.style.cssText = 'flex:none;width:36px;height:36px;border-radius:9px;border:1px solid ' + css('--line', '#d5dbe0') + ';background:transparent;color:inherit;font-size:16px;cursor:pointer;';
    zu.addEventListener('click', schliessen);
    kopf.append(texte, zu);
    const buehne = document.createElement('div'); buehne.className = 'ea-buehne';
    buehne.style.cssText = 'position:relative;flex:1;min-height:0;background:' + css('--scene', '#dfe6ea') + ';';
    const hinweis = document.createElement('div');
    hinweis.textContent = 'Ziehen = drehen · Mausrad / zwei Finger = zoomen · Esc = schließen';
    hinweis.style.cssText = 'position:absolute;left:10px;bottom:8px;font-size:12px;opacity:.65;pointer-events:none;';
    buehne.append(hinweis);
    const text = document.createElement('div'); text.className = 'ea-text';
    text.style.cssText = 'max-height:22%;overflow:auto;padding:8px 14px 12px;font-size:13px;line-height:1.45;opacity:.85;';
    box.append(kopf, buehne, text);
    ov.append(box);
    document.body.append(ov);
    ov.addEventListener('click', (e) => { if (e.target === ov) schliessen(); });
    document.addEventListener('keydown', (e) => { if (ov.style.display !== 'none' && e.key === 'Escape') { e.preventDefault(); schliessen(); } }, true);

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setClearColor(0x000000, 0);   // durchsichtig: der Hintergrund der Bühne (Farbe der Seite) scheint durch
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.outputEncoding = THREE.sRGBEncoding;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.domElement.style.cssText = 'display:block;width:100%;height:100%;touch-action:none;';
    buehne.prepend(renderer.domElement);
    scene = new THREE.Scene();
    if (THREE.RoomEnvironment) scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new THREE.RoomEnvironment(), 0.04).texture;
    scene.add(new THREE.HemisphereLight(0xffffff, 0x7d8a96, scene.environment ? 0.35 : 0.8));
    const sonne = new THREE.DirectionalLight(0xffffff, scene.environment ? 0.8 : 1.0); sonne.position.set(1, 2, 1.5); scene.add(sonne);
    const gegen = new THREE.DirectionalLight(0xdfe8ff, 0.4); gegen.position.set(-1.5, 0.8, -1); scene.add(gegen);
    camera = new THREE.PerspectiveCamera(35, 1, 0.1, 10000);
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    new ResizeObserver(groesse).observe(buehne);
  }

  function groesse() {
    if (!renderer) return;
    const b = renderer.domElement.parentElement, w = b.clientWidth, h = b.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  }

  function aufraeumen() {
    if (!halter) return;
    halter.traverse((o) => { if (o.isMesh) (Array.isArray(o.material) ? o.material : [o.material]).forEach((m) => m.dispose()); });
    scene.remove(halter); halter = null;
  }

  function schliessen() {
    if (!ov) return;
    ov.style.display = 'none'; laeuft = false; aufraeumen();
    if (vorherFokus && vorherFokus.focus) vorherFokus.focus();
  }

  function schleife() {
    if (!laeuft) return;
    controls.update(); renderer.render(scene, camera);
    requestAnimationFrame(schleife);
  }

  // obj: die Gruppe des Bauteils (userData.part = { name, desc }); bezug: Gruppe, deren Ausrichtung als „gerade“ gilt (z. B. das Auto in der Simulation)
  window.rcEinzelansicht = function (obj, bezug) {
    if (!obj || !window.THREE || !THREE.OrbitControls) return;
    if (!ov) aufbauen();
    aufraeumen();
    vorherFokus = document.activeElement;
    obj.updateWorldMatrix(true, true);
    const kopie = obj.clone(true);
    // Unsichtbares (z. B. Laserstrahl, ausgeblendete Ersatzteile) und Effekte nicht mitnehmen – sonst stimmen auch die Maße nicht
    const weg = [];
    kopie.traverse((o) => { if (o !== kopie && (!o.visible || (o.userData && (o.userData.fx || o.userData.noPick)) || o.isSprite || o.isLine || o.isPoints)) weg.push(o); });
    weg.forEach((o) => o.parent && o.parent.remove(o));
    kopie.traverse((o) => {
      if (!o.isMesh) return;
      const neu = (m) => { const c = m.clone(); const voll = (m.userData && m.userData.base) ?? 1; c.opacity = voll; c.transparent = voll < 1; c.depthWrite = true; return c; };
      o.material = Array.isArray(o.material) ? o.material.map(neu) : neu(o.material);
    });
    // Lage: so gedreht wie im Auto (bzw. wie im Bezug), Größe 1:1, Mitte in den Ursprung
    const q = new THREE.Quaternion(), p = new THREE.Vector3(), s = new THREE.Vector3();
    obj.matrixWorld.decompose(p, q, s);
    if (bezug) { const qb = new THREE.Quaternion(); bezug.updateWorldMatrix(true, false); bezug.matrixWorld.decompose(new THREE.Vector3(), qb, new THREE.Vector3()); q.premultiply(qb.invert()); }
    kopie.position.set(0, 0, 0); kopie.quaternion.copy(q); kopie.scale.copy(s);
    kopie.visible = true;
    halter = new THREE.Group(); halter.add(kopie); scene.add(halter);
    const bb = new THREE.Box3().setFromObject(halter);
    if (bb.isEmpty()) { aufraeumen(); return; }
    const mitte = bb.getCenter(new THREE.Vector3()), dim = bb.getSize(new THREE.Vector3());
    kopie.position.sub(mitte);
    const r = Math.max(dim.length() / 2, 1);
    camera.near = r / 100; camera.far = r * 100; camera.updateProjectionMatrix();
    camera.position.set(r * 1.6, r * 1.15, r * 1.9);
    controls.target.set(0, 0, 0); controls.minDistance = r * 0.6; controls.maxDistance = r * 12; controls.update();
    const teil = obj.userData.part || {};
    ov.querySelector('.ea-titel').textContent = teil.name || 'Bauteil';
    const f = (v) => v.toLocaleString('de-DE', { maximumFractionDigits: v < 10 ? 1 : 0 });
    ov.querySelector('.ea-mass').textContent = `ca. ${f(dim.x)} × ${f(dim.z)} × ${f(dim.y)} mm (Länge × Breite × Höhe, wie im Auto eingebaut)`;
    ov.querySelector('.ea-text').textContent = teil.desc || '';
    ov.style.display = 'flex';
    groesse();
    ov.querySelector('button').focus();
    if (!laeuft) { laeuft = true; schleife(); }
  };

  // Knopf für die Info-Karte (für Touch-Geräte, die keinen Doppelklick kennen)
  window.rcModellKnopf = function (obj, bezug) {
    const b = document.createElement('button');
    b.type = 'button'; b.textContent = 'Als Modell ansehen';
    b.title = 'Oder: Doppelklick auf das Bauteil';
    b.style.cssText = 'margin-top:6px;justify-self:start;pointer-events:auto;padding:5px 10px;border-radius:8px;border:1px solid ' + css('--line', '#d5dbe0') + ';background:transparent;color:inherit;font:inherit;font-size:13px;cursor:pointer;';
    b.addEventListener('click', (e) => { e.stopPropagation(); window.rcEinzelansicht(obj, bezug); });
    return b;
  };
})();
