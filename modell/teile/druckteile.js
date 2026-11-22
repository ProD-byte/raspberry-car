// Druck-Infos für alle Druckteile: Filament, Druckeinstellungen, Druckrichtung, Download.
// Wird von allen 3D-Ansichten geladen. Tippt man ein Druckteil an, erscheint dieser Block unter der Beschreibung.
// Pfade relativ zu modell/ – funktioniert per Doppelklick auf die HTML-Datei und auf GitHub Pages.
// Muss zu gehaeuse/README.md passen. Alle Teile sind ohne Stützen druckbar (geprüft mit gehaeuse/werkzeug/ueberhang.py).
(function () {
  const PETG = 'PETG – verträgt die Wärme von Motoren und Akku (bis ca. 75 °C) und ist zäh. PLA geht zum Probieren, wird im Auto aber weich.';
  const PETG_TEMP = 'Düse 235–245 °C, Bett 75–85 °C, Lüfter 30–50 %';
  window.RC_DRUCK = {
    'Fahrwerk-Wanne vordere Hälfte (Druckteil)': {
      datei: 'ebene1/wanne_vorne', anzahl: 1, gramm: 130, filament: PETG, temp: PETG_TEMP,
      einstellungen: 'Düse 0,4 mm · Schicht 0,2 mm · 4 Wände (die Schrauben schneiden ihr Gewinde selbst) · oben/unten je 5 Schichten · 25 % Füllung (Gyroid) · keine Stützen',
      richtung: 'Boden unten aufs Bett. Die drei Laschen an der Fuge stehen mit auf dem Bett. 137 × 180 mm.'
    },
    'Fahrwerk-Wanne hintere Hälfte (Druckteil)': {
      datei: 'ebene1/wanne_hinten', anzahl: 1, gramm: 125, filament: PETG, temp: PETG_TEMP,
      einstellungen: 'Düse 0,4 mm · Schicht 0,2 mm · 4 Wände (die Schrauben schneiden ihr Gewinde selbst) · oben/unten je 5 Schichten · 25 % Füllung (Gyroid) · keine Stützen',
      richtung: 'Boden unten aufs Bett. 131 × 180 mm.'
    },
    'Motorbügel (4 × Druckteil)': {
      datei: 'ebene1/motorbuegel', anzahl: 4, gramm: 3, filament: PETG, temp: PETG_TEMP,
      einstellungen: 'Düse 0,4 mm · Schicht 0,2 mm · 4 Wände · 40 % Füllung · keine Stützen. Alle 4 auf einmal drucken.',
      richtung: 'Flach auf die große Seite legen.'
    },
    'Prüfstand (Druckteil)': {
      datei: 'pruefstand/pruefstand', anzahl: 1, gramm: 125,
      filament: 'PLA reicht – der Prüfstand ist ein Werkzeug und wird nicht warm.', temp: 'Düse 205–215 °C, Bett 55–60 °C, Lüfter 100 %',
      einstellungen: 'Düse 0,4 mm · Schicht 0,2 mm · 3 Wände · 15 % Füllung · keine Stützen',
      richtung: 'So wie er steht (Unterseite aufs Bett). 124 × 124 mm – passt auf jedes Druckbett.'
    },
    'Elektronik-Deck Ebene 2, vordere Hälfte (Druckteil)': {
      datei: 'ebene2/platte_vorne', anzahl: 1, gramm: 50, filament: PETG, temp: PETG_TEMP,
      einstellungen: 'Düse 0,4 mm · Schicht 0,2 mm · 4 Wände (Schraubdome, Steg mit Gewinde) · 20 % Füllung · keine Stützen. Die Rastnasen der Taschen sind keilförmig und drucken sauber.',
      richtung: 'Unterseite aufs Bett, der Steg an der Fuge steht nach oben. 67 × 180 mm.'
    },
    'Elektronik-Deck Ebene 2, hintere Hälfte (Druckteil)': {
      datei: 'ebene2/platte_hinten', anzahl: 1, gramm: 130, filament: PETG, temp: PETG_TEMP,
      einstellungen: 'Düse 0,4 mm · Schicht 0,2 mm · 4 Wände (Schraubdome) · 20 % Füllung · keine Stützen.',
      richtung: 'Unterseite aufs Bett. 183 × 180 mm.'
    },
    'Gehäuse-Ring oben, vordere Hälfte (Druckteil)': {
      datei: 'ebene2/ring_vorne', anzahl: 1, gramm: 50, filament: PETG, temp: PETG_TEMP,
      einstellungen: 'Düse 0,4 mm · Schicht 0,2 mm · 3 Wände · 15 % Füllung · keine Stützen',
      richtung: 'Aufrecht drucken, so wie er im Auto steht (Unterkante aufs Bett). Die Laschen vorne haben unten 45°-Schrägen. 141 × 180 mm.'
    },
    'Gehäuse-Ring oben, hintere Hälfte (Druckteil)': {
      datei: 'ebene2/ring_hinten', anzahl: 1, gramm: 40, filament: PETG, temp: PETG_TEMP,
      einstellungen: 'Düse 0,4 mm · Schicht 0,2 mm · 3 Wände · 15 % Füllung · keine Stützen',
      richtung: 'Aufrecht drucken (Unterkante aufs Bett). Die Scharnier-Lappen hinten haben unten 45°-Schrägen und drucken ohne Stützen. 119 × 180 mm.'
    },
    'Klapphaube Ebene 3, vordere Hälfte (Druckteil)': {
      datei: 'ebene3/haube_vorne', anzahl: 1, gramm: 105, filament: PETG + ' Pi und AI HAT+ werden warm – deshalb hier unbedingt PETG.', temp: PETG_TEMP,
      einstellungen: 'Düse 0,4 mm · Schicht 0,2 mm · 3–4 Wände (Flansch mit Gewinde, Schraubpolster) · 15–20 % Füllung · keine Stützen',
      richtung: 'Dach nach unten aufs Bett (die Haube steht kopfüber). Kamera-Nuten, Taschen und Flansch wachsen vom Dach nach oben. 80 × 180 mm.'
    },
    'Klapphaube Ebene 3, hintere Hälfte (Druckteil)': {
      datei: 'ebene3/haube_hinten', anzahl: 1, gramm: 170, filament: PETG + ' Pi und AI HAT+ werden warm – deshalb hier unbedingt PETG.', temp: PETG_TEMP,
      einstellungen: 'Düse 0,4 mm · Schicht 0,2 mm · 3–4 Wände (Pi-Dome, Scharnier-Lappen) · 15–20 % Füllung · keine Stützen. Die Senkungen der M2,5 im Dach haben den Brücken-Trick.',
      richtung: 'Dach nach unten aufs Bett. Die Scharnier-Lappen werden von einem 45°-Keil getragen. 180 × 180 mm.'
    }
  };

  // Block für die Info-Box: null, wenn das Teil kein Druckteil ist
  window.rcDruckInfo = function (name) {
    const d = window.RC_DRUCK[name];
    if (!d) return null;
    const box = document.createElement('div');
    box.style.cssText = 'display:grid;gap:3px;margin-top:6px;padding-top:6px;border-top:1px solid var(--line, #ccc);font-size:13px;pointer-events:auto';
    const zeile = (titel, text) => {
      const z = document.createElement('div');
      const t = document.createElement('strong'); t.textContent = titel + ': ';
      z.append(t, document.createTextNode(text));
      box.append(z);
    };
    zeile('Filament', d.filament + ' (' + d.temp + ')');
    zeile('Druckeinstellungen', d.einstellungen);
    zeile('Druckrichtung', d.richtung);
    zeile('Menge', (d.anzahl > 1 ? d.anzahl + ' Stück, ' : '') + 'ca. ' + d.gramm + ' g Filament' + (d.anzahl > 1 ? ' je Stück' : ''));
    const dl = document.createElement('div');
    const t = document.createElement('strong'); t.textContent = 'Download: ';
    dl.append(t);
    [['STL', '.stl'], ['STEP', '.step']].forEach(([was, endung], i) => {
      const a = document.createElement('a');
      a.href = '../gehaeuse/' + d.datei + endung; a.download = d.datei.split('/').pop() + endung; a.textContent = was;
      if (i) dl.append(document.createTextNode(' · '));
      dl.append(a);
    });
    dl.append(document.createTextNode(' (gehaeuse/' + d.datei + '.stl)'));
    box.append(dl);
    return box;
  };
})();
