# Raspberry Pi 5 – Software

Kommt in Stufe 3: Live-Video (Kamera Modul 3), Web-App, später LiDAR-Karte (SLAM), Navigation, KI (AI HAT+), 4G/GPS.

Verbindungen: Pico per USB (USB 2.0 unten), LiDAR-Adapter (USB 2.0 oben), 4G-Modul (USB 3.0 unten), Kamera an CAM/DISP 0, AI HAT+ per PCIe.

Wichtig in `config.txt`: `usb_max_current_enable=1` (Strom kommt über USB-C vom Pololu ohne Netzteil-Erkennung).
