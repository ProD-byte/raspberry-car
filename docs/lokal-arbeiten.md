# Lokal mit Claude Code weiterarbeiten

1. Repository auf GitHub anlegen (z. B. `raspberry-car`, öffentlich, **ohne** README – die ist schon hier drin).
2. Diesen Ordner entpacken und im Terminal darin:
   ```
   git init -b main
   git add .
   git commit -m "Projektstart: Plan, Stückliste, Verdrahtung, 3D-Modell"
   git remote add origin https://github.com/ProD-byte/raspberry-car.git
   git push -u origin main
   ```
3. Im Ordner `claude` starten (Terminal) oder den Ordner in der Claude-Desktop-App bzw. in VS Code öffnen.
   Claude liest `CLAUDE.md` automatisch und kennt damit alle Entscheidungen.
4. Erste Aufgabe, wenn der Pico da ist: „Hilf mir, MicroPython auf den Pico 2 W zu spielen und einen LED-Test zu machen.“
