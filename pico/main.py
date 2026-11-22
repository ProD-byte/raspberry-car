# Raspberry Car – Stufe 1: Fahren per Handy-Joystick
#
# Startet automatisch, wenn der Pico Strom bekommt:
#   1. Der Pico macht ein eigenes WLAN auf (Name und Passwort in geheim.py).
#   2. Handy mit diesem WLAN verbinden und im Browser http://192.168.4.1 öffnen.
#   3. Joystick nach oben ziehen = vorwärts, zur Seite = lenken.
#
# Sicherheit:
#   * Kommt 0,5 s lang kein Befehl (Handy weg, WLAN weg, Seite zu), hält das Auto an.
#   * Der Knopf STOPP legt die Motortreiber schlafen, bis man WEITER tippt.
#   * Die Laser-Nahsensoren vorne und hinten bremsen vor Hindernissen (wenn eingebaut).
#   * Bei einem Fehler im Programm werden die Treiber immer ausgeschaltet.

import asyncio
import json
import time
import network
from machine import Pin

import einstellungen as E
from motoren import Antrieb, joystick_zu_raedern
from encoder import alle_encoder
from nahsensoren import Nahsensoren, begrenzen

try:
    import geheim
except ImportError:
    raise SystemExit("geheim.py fehlt – geheim_beispiel.py kopieren, umbenennen und Passwort eintragen")

led = Pin("LED", Pin.OUT)
antrieb = Antrieb()
encoder = alle_encoder()
nah = Nahsensoren()

letzter_befehl = time.ticks_ms()
gesperrt = False                 # STOPP-Knopf gedrückt
wunsch_l = wunsch_r = 0.0        # was der Joystick möchte
hindernis = False                # gerade wegen eines Hindernisses gesperrt


def strecke(seite):
    """Mittlere Strecke der beiden Räder einer Seite in mm."""
    return (encoder["vorne_" + seite].strecke_mm() + encoder["hinten_" + seite].strecke_mm()) / 2


def wlan_starten():
    ap = network.WLAN(network.AP_IF)
    ap.config(ssid=geheim.WLAN_NAME, key=geheim.WLAN_PASSWORT)
    ap.active(True)
    while not ap.active():
        time.sleep_ms(100)
    print("WLAN:", geheim.WLAN_NAME, "– Adresse http://%s" % ap.ifconfig()[0])


def werte(qs):
    """'x=0.5&y=-0.2' → {'x': '0.5', 'y': '-0.2'}"""
    d = {}
    for teil in qs.split("&"):
        if "=" in teil:
            k, v = teil.split("=", 1)
            d[k] = v
    return d


def status():
    return {
        "l": antrieb.ist_l, "r": antrieb.ist_r,
        "sl": strecke("links"), "sr": strecke("rechts"),
        "vorne": nah.abstand["vorne"], "hinten": nah.abstand["hinten"],
        "fehlt": nah.fehlt, "hindernis": hindernis, "gesperrt": gesperrt,
    }


async def antworten(schreiber, code, art, inhalt):
    kopf = "HTTP/1.1 %s\r\nContent-Type: %s\r\nCache-Control: no-store\r\nConnection: close\r\n\r\n" % (code, art)
    schreiber.write(kopf.encode())
    schreiber.write(inhalt)
    await schreiber.drain()


async def anfrage(leser, schreiber):
    global letzter_befehl, gesperrt, wunsch_l, wunsch_r
    try:
        zeile = (await leser.readline()).decode()
        while (await leser.readline()) not in (b"\r\n", b""):   # Kopfzeilen überspringen
            pass
        teile = zeile.split(" ")
        pfad = teile[1] if len(teile) > 1 else "/"
        weg, _, qs = pfad.partition("?")

        if weg == "/fahren":
            letzter_befehl = time.ticks_ms()
            led.toggle()
            w = werte(qs)
            wunsch_l, wunsch_r = joystick_zu_raedern(float(w.get("x", 0)), float(w.get("y", 0)))
            await antworten(schreiber, "200 OK", "application/json", json.dumps(status()).encode())
        elif weg == "/stopp":
            gesperrt = True
            antrieb.ausschalten()
            await antworten(schreiber, "200 OK", "text/plain", b"gestoppt")
        elif weg == "/start":
            gesperrt = False
            await antworten(schreiber, "200 OK", "text/plain", b"weiter")
        elif weg == "/":
            with open("joystick.html", "rb") as f:
                await antworten(schreiber, "200 OK", "text/html; charset=utf-8", f.read())
        else:
            await antworten(schreiber, "404 Not Found", "text/plain", b"nicht gefunden")
    except Exception as fehler:
        print("Fehler bei Anfrage:", fehler)
    finally:
        schreiber.close()
        await schreiber.wait_closed()


async def regelung():
    """Alle 20 ms: Abstände messen, Not-Stopp prüfen, Tempo begrenzen, Motoren nachführen."""
    global wunsch_l, wunsch_r, hindernis
    vorher = time.ticks_ms()
    while True:
        jetzt = time.ticks_ms()
        dt = time.ticks_diff(jetzt, vorher) / 1000
        vorher = jetzt
        a = nah.messen()

        if time.ticks_diff(jetzt, letzter_befehl) > E.BEFEHL_TIMEOUT_MS:
            wunsch_l = wunsch_r = 0.0          # Handy schweigt → anhalten

        if gesperrt:
            pass                               # STOPP gedrückt: Treiber bleiben aus
        elif wunsch_l == 0 and wunsch_r == 0 and antrieb.ist_l == 0 and antrieb.ist_r == 0:
            antrieb.ausschalten()              # steht und soll stehen → Treiber schlafen legen
            hindernis = False
        else:
            links, rechts, hindernis = begrenzen(wunsch_l, wunsch_r, a["vorne"], a["hinten"])
            antrieb.einschalten()
            antrieb.fahren(links, rechts)
            # Notbremse: fährt das Auto noch auf das Hindernis zu, sofort anhalten statt über die Rampe
            fahrt = (antrieb.ist_l + antrieb.ist_r) / 2
            ziel = (links + rechts) / 2
            if hindernis and abs(fahrt) > abs(ziel):
                antrieb.sofort()
        antrieb.aktualisieren(dt)
        await asyncio.sleep_ms(20)


async def haupt():
    wlan_starten()
    await asyncio.start_server(anfrage, "0.0.0.0", 80)
    print("Bereit. Handy ins WLAN, dann http://192.168.4.1 öffnen.")
    if nah.fehlt:
        print("Ohne Nahsensor:", ", ".join(nah.fehlt), "– dort kein Hindernis-Stopp!")
    await regelung()


try:
    asyncio.run(haupt())
finally:
    antrieb.ausschalten()
    led.value(0)
    print("Motoren aus.")
