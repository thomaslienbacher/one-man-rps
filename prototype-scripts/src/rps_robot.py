"""
Dieses Script ist der finale Programm für den Schere Stein Papier Roboter. Es liest den Kamerafeed,
erkennt die Geste und stellt das Gegenzeichen grafisch dar. Zusätzlich die Wahrscheinlichkeit der Erkennung
angezeigt. Die vortrainierten Neuralen Netzwerke werden aus dem git Repository geladen. Das UI wird im Fullscreen
Mode angezeigt und die UI Elemente werden anhand der Bildschirmgröße automatisch skaliert.
ACHTUNG: Dateipfade sind hardcoded!
"""

from tensorflow.keras.models import model_from_json
import os
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
from utils import *
import numpy as np
from tkinter import *
from tkinter.ttk import *
import PIL.Image
import PIL.ImageTk

REPODIR = "/home/pi/one-man-rps/"
PADDING = 12
BORDER = 2

camera = PiCamera()
camera.resolution = IMG_NET_SIZE
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=IMG_NET_SIZE)
time.sleep(0.5)

model_backups = os.path.join(REPODIR, "data/model_backups")
path = os.path.join(model_backups, "v6_model_architecture.json")
with open(path, "r") as f:
    model = model_from_json(f.read())
path = os.path.join(model_backups, "v6_model_weights.h5")
model.load_weights(path)
print("Loaded model!")

# Window created with tkinter
window = Tk()
window.attributes("-fullscreen", True)
window.configure(background="white", cursor="none")
window.update()
image_size = int(window.winfo_width() * 0.66) - PADDING * 2 - BORDER * 2

Style().configure("TFrame", background="white")
Style().configure("CustomPanel.TLabel", borderwidth=BORDER, relief="flat", background="black")
Style().configure("CustomLabel.TLabel", background="white", font="jetbrainsmono 32")

# pre loaded images
images = os.path.join(REPODIR, "prototype-scripts/src")
cv_img = cv.cvtColor(cv.imread(os.path.join(images, "rock.png")), cv.COLOR_BGR2RGB)
cv_img = cv.resize(cv_img, (image_size, image_size))
photo_rock = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

cv_img = cv.cvtColor(cv.imread(os.path.join(images, "paper.png")), cv.COLOR_BGR2RGB)
cv_img = cv.resize(cv_img, (image_size, image_size))
photo_paper = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

cv_img = cv.cvtColor(cv.imread(os.path.join(images, "scissors.png")), cv.COLOR_BGR2RGB)
cv_img = cv.resize(cv_img, (image_size, image_size))
photo_scissors = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

cv_img = cv.cvtColor(cv.imread(os.path.join(images, "blank.png")), cv.COLOR_BGR2RGB)
cv_img = cv.resize(cv_img, (image_size, image_size))
photo_empty = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

# tk panels
panel_frame = Frame(window)
label_frame = Frame(window)

panel_gesture = Label(panel_frame, image=photo_empty, style="CustomPanel.TLabel")
panel_gesture.pack(side="bottom", fill="x", expand=False, padx=(PADDING, PADDING), pady=(PADDING, PADDING))
label_title = Label(panel_frame, text="Schere Stein Papier - Roboter", style="CustomLabel.TLabel")
label_title.pack(side="top", fill="y", anchor="n", expand=False, pady=(PADDING, PADDING))
panel_frame.pack(side="top")
panel_frame.update()

label = Label(label_frame, text="", style="CustomLabel.TLabel")
label.pack(side="bottom", fill="y", anchor="n", expand=True)
label_frame.pack(side="bottom", fill="both", anchor="center", expand=True)
label_frame.update()

window.update()

for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
    image = frame.array
    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY) / 255
    input = image.reshape(1, IMG_NET_SIZE[0], IMG_NET_SIZE[1], 1)
    prediction = model.predict([input])

    # print prediction percent
    prediction_text = "_"
    THRESHOLD = 0.6
    prediction = prediction[0]
    highest = -1
    if prediction[0] < THRESHOLD and prediction[1] < THRESHOLD and prediction[2] < THRESHOLD and prediction[3] < THRESHOLD:
        prediction_text = "{:>6} zu {:>5.1f}% erkannt".format("", 0)
        panel_gesture.configure(image=photo_empty)
    else:
        CATEGORIES = ["EMPTY", "PAPER", "ROCK", "SCISSORS"]
        CATEGORIES_DE = ["Leer", "Papier", "Stein", "Schere"]
        out = np.argmax(prediction)

        if isinstance(out, list):
            prediction_text = "{:>6} zu {:>5.1f}% erkannt".format(
                CATEGORIES_DE[out[0]], prediction[out[0]] * 100)
            highest = out[0]
        else:
            prediction_text = "{:>6} zu {:>5.1f}% erkannt".format(
                CATEGORIES_DE[out], prediction[out] * 100)
            highest = out

    label.configure(text=prediction_text)

    if highest == 0:
        panel_gesture.configure(image=photo_empty)

    if highest == 1:
        panel_gesture.configure(image=photo_scissors)

    if highest == 2:
        panel_gesture.configure(image=photo_paper)

    if highest == 3:
        panel_gesture.configure(image=photo_rock)

    rawCapture.truncate(0)
    window.update()
