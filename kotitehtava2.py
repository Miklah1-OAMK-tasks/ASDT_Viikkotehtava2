import tkinter as tk
import random
import pygame
import time

# Pygamen alustus
pygame.mixer.init()

# Pääikkuna
ikkuna = tk.Tk()
ikkuna.geometry("600x500")

# Juoksurata
juoksurata = tk.Canvas(ikkuna, width=500, height=200)
juoksurata.pack()

# Lähtö- ja maaliviivat
lahtoviiva = juoksurata.create_line(50, 100, 50, 200, width=5, fill="green")
maaliviiva = juoksurata.create_line(450, 100, 450, 200, width=5, fill="red")

# Ernestin ja Kernestin paikat
ernesti_pos = juoksurata.create_oval(40, 110, 60, 130, fill="blue", outline="blue", tags="ernesti")
kernesti_pos = juoksurata.create_oval(40, 140, 60, 160, fill="pink", outline="pink", tags="kernesti")

# Äänitiedostojen lataaminen pygame.mixer.Sound -objekteihin
sounds = {
    "start_gun": pygame.mixer.Sound("juoksuaanet/start_gun.wav"),
    "klomps": pygame.mixer.Sound("juoksuaanet/klomps.wav"),
    "kips": pygame.mixer.Sound("juoksuaanet/kips.wav")
}

# Funktio, joka toistaa ääniä
def play_sound(sound_name):
    if sound_name in sounds:
        sounds[sound_name].play()

# Funktio, joka pysäyttää äänen
def stop_sound(sound_name):
    if sound_name in sounds:
        sounds[sound_name].stop()

# Ernestin ja Kernestin aikojen alustaminen
ernesti_time = None
kernesti_time = None

# Funktio, joka havainnollistaa Ernestin juoksua
def ernesti_juoksee(step=0, start_time=None):
    global ernesti_time
    if step == 0:
        juoksurata.coords("ernesti", 40, 110, 60, 130)  # Siirtää Ernestin lähtöviivalle
        if start_time is None:
            start_time = time.time()  # Aloita ajanotto

    if step < 40:  # 40 askelta maaliin
        play_sound("klomps")  # Kumisaappaiden ääni
        juoksurata.move("ernesti", 10, 0)  # Liikuta Ernestiä eteenpäin
        ikkuna.update()
        ikkuna.after(int(random.uniform(500, 1000)), ernesti_juoksee, step + 1, start_time)
    else:
        stop_sound("klomps")  # Pysäytä ääni, kun Ernesti saapuu maaliin
        ernesti_time = round(time.time() - start_time, 2)
        tarkista_voittaja()

# Funktio, joka havainnollistaa Kernestin juoksua
def kernesti_juoksee(step=0, start_time=None):
    global kernesti_time
    if step == 0:
        juoksurata.coords("kernesti", 40, 140, 60, 160)  # Siirtää Kernestin lähtöviivalle
        if start_time is None:
            start_time = time.time()  # Aloita ajanotto

    if step < 40:  # 40 askelta maaliin
        play_sound("kips")  # Korkokenkien ääni
        juoksurata.move("kernesti", 10, 0)  # Liikuta Kernestiä eteenpäin
        ikkuna.update()
        ikkuna.after(int(random.uniform(500, 1000)), kernesti_juoksee, step + 1, start_time)
    else:
        stop_sound("kips")  # Pysäytä ääni, kun Kernesti saapuu maaliin
        kernesti_time = round(time.time() - start_time, 2)
        tarkista_voittaja()

# Funktio, joka tarkistaa voittajan ja ilmoittaa tuloksen
def tarkista_voittaja():
    if ernesti_time is not None and kernesti_time is not None:
        if ernesti_time < kernesti_time:
            voittaja = "Ernesti"
            aika = ernesti_time
        else:
            voittaja = "Kernesti"
            aika = kernesti_time
        tulos_label.config(text=f"{voittaja} voitti ja saapui maaliin ajassa {aika} sekuntia!")

# Yhteislähtö-toiminto, joka ampuu lähtölaukauksen ja käynnistää molemmat kilpailijat
def yhteislahto():
    play_sound("start_gun")  # Lähtölaukauksen ääni
    tulos_label.config(text=f"")
    global ernesti_time, kernesti_time
    ernesti_time = None
    kernesti_time = None
    aika_start = time.time()
    ernesti_juoksee(0, aika_start)
    kernesti_juoksee(0, aika_start)

# Ikkunan osat - painikkeet
painike_ernesti = tk.Button(ikkuna, text="Ernestin juoksu", command=lambda: ernesti_juoksee(0))
painike_ernesti.place(x=10, y=35)

painike_kernesti = tk.Button(ikkuna, text="Kernestin juoksu", command=lambda: kernesti_juoksee(0))
painike_kernesti.place(x=110, y=35)

# Painike yhteislähtöä varten
painike_yhteislahto = tk.Button(ikkuna, text="Yhteislähtö", command=yhteislahto)
painike_yhteislahto.place(x=210, y=35)

# Label, joka näyttää voittajan ja ajat
tulos_label = tk.Label(ikkuna, text="")
tulos_label.pack()

ikkuna.mainloop()