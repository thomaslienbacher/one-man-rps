"""
Dieses Script laded ein vortrainiertes Neural Netzwerk, und testet es mit
Echzeit Bildern von der Kamera. Die Ergebnisse der Erkennung werden in der Konsole ausgegeben und
grafisch Dargestellt. In dem UI wird das Gegenzeichen, das Kamera Frame und die einzelnen Wahrscheinlichkeiten
der Erkennung angezeigt. Das UI wird im Fullscreen Mode angezeigt und die UI Elemente werden anhand der
Bildschirmgröße automatisch skaliert. Diese Script dient zur Entwicklung und kann bei technischen
Demonstrationen genutzt werden wo mehr Informationen angezeigt werden sollten.
ACHTUNG: Dateipfade sind hardcoded!
"""

from tensorflow.keras.models import model_from_json, load_model
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

DATADIR = "/home/pi/one-man-rps/data/model_backups"
PADDING = 12
BORDER = 2

camera = PiCamera()
camera.resolution = IMG_NET_SIZE
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=IMG_NET_SIZE)
time.sleep(0.5)

path = os.path.join(DATADIR, "v7_model_architecture.json")
with open(path, "r") as f:
    model = model_from_json(f.read())
path = os.path.join(DATADIR, "v7_model_weights.h5")
model.load_weights(path)
print("Loaded model!")

# Window created with tkinter
window = Tk()
window.attributes("-fullscreen", True)
window.update()
image_size = window.winfo_width() // 2 - PADDING * 2 - BORDER * 2

Style().configure("TFrame", background="white")
Style().configure("CustomPanel.TLabel", borderwidth=BORDER, relief="flat", background="black")
Style().configure("CustomLabel.TLabel", background="white", font="jetbrainsmono 32")


def key_up(e):
    if e.keysym == 'Escape':
        sys.exit(0)


window.bind('<KeyRelease>', key_up)

# pre loaded images
cv_img = cv.cvtColor(cv.imread("rock.png"), cv.COLOR_BGR2RGB)
cv_img = cv.resize(cv_img, (image_size, image_size))
photo_rock = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

cv_img = cv.cvtColor(cv.imread("paper.png"), cv.COLOR_BGR2RGB)
cv_img = cv.resize(cv_img, (image_size, image_size))
photo_paper = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

cv_img = cv.cvtColor(cv.imread("scissors.png"), cv.COLOR_BGR2RGB)
cv_img = cv.resize(cv_img, (image_size, image_size))
photo_scissors = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

cv_img = cv.cvtColor(cv.imread("blank.png"), cv.COLOR_BGR2RGB)
cv_img = cv.resize(cv_img, (image_size, image_size))
photo_empty = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

cv_img = cv.cvtColor(cv.imread("error.png"), cv.COLOR_BGR2RGB)
cv_img = cv.resize(cv_img, (image_size, image_size))
photo_error = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

# tk panels
panel_frame = Frame(window)
label_frame = Frame(window)

panel_gesture = Label(panel_frame, image=photo_empty, style="CustomPanel.TLabel")
panel_gesture.pack(side="left", fill="x", expand=False, padx=(PADDING, PADDING), pady=(PADDING, PADDING))
panel_cam = Label(panel_frame, image=photo_empty, style="CustomPanel.TLabel")
panel_cam.pack(side="right", fill="x", expand=False, padx=(PADDING, PADDING), pady=(PADDING, PADDING))
panel_frame.pack(side="top")
panel_frame.update()

label = Label(label_frame, text="sandbox-text", style="CustomLabel.TLabel")
label.pack(side="bottom", fill="y", anchor="n", expand=TRUE)
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
        prediction_text = "E: {:>5.1f}  P: {:>5.1f}  R: {:>5.1f}  S: {:>5.1f} {:>8}".format(
            prediction[0] * 100, prediction[1] * 100,
            prediction[2] * 100, prediction[3] * 100, "--")
        panel_gesture.configure(image=photo_error)
    else:
        CATEGORIES = ["EMPTY", "PAPER", "ROCK", "SCISSORS"]
        out = np.argmax(prediction)

        if isinstance(out, list):
            prediction_text = "E: {:>5.1f}  P: {:>5.1f}  R: {:>5.1f}  S: {:>5.1f} {:>8}".format(
                prediction[0] * 100, prediction[1] * 100,
                prediction[2] * 100, prediction[3] * 100, CATEGORIES[out[0]])
            highest = out[0]
        else:
            prediction_text = "E: {:>5.1f}  P: {:>5.1f}  R: {:>5.1f}  S: {:>5.1f} {:>8}".format(
                prediction[0] * 100, prediction[1] * 100,
                prediction[2] * 100, prediction[3] * 100, CATEGORIES[out])
            highest = out

    print(prediction_text)
    label.configure(text=prediction_text)

    if highest == 0:
        panel_gesture.configure(image=photo_empty)

    if highest == 1:
        panel_gesture.configure(image=photo_scissors)

    if highest == 2:
        panel_gesture.configure(image=photo_paper)

    if highest == 3:
        panel_gesture.configure(image=photo_rock)

    cam_photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv.resize(image * 255, (image_size, image_size))))
    panel_cam.configure(image=cam_photo)

    rawCapture.truncate(0)
    window.update()
