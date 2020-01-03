"""
Dieses Script nimmt laded ein vortrainiertes Neural Netzwerk, und testet es mit
Echzeit Bildern von der Kamera.
"""

from tensorflow.keras.models import model_from_json, load_model
import os
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
import matplotlib.pyplot as plt
from utils import *
import numpy as np
import tkinter
import PIL.Image
import PIL.ImageTk

DATADIR = "/home/pi"

camera = PiCamera()
camera.resolution = IMG_NET_SIZE
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=IMG_NET_SIZE)
time.sleep(0.5)

path = os.path.join(DATADIR, "model_architecture.json")
with open(path, "r") as f:
    model = model_from_json(f.read())
path = os.path.join(DATADIR, "model_weights.h5")
model.load_weights(path)
print("Loaded model!")

# Window created with tkinter
window = tkinter.Tk()
# Loading pic with cv
# cv.COLOR_BGR2RGB declares the correct color format
cv_img = cv.cvtColor(cv.imread("blank.png"), cv.COLOR_BGR2RGB)
# Creating canvas with correct scaling
height, width, no_channels = cv_img.shape
canvas = tkinter.Canvas(window, width = width * 2, height = height)
canvas.pack()

for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
    # print("Captured .. ", end='')
    image = frame.array
    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY) / 255

    input = image.reshape(1, IMG_NET_SIZE[0], IMG_NET_SIZE[1], 1)

    prediction = model.predict([input])

    # print("predicted")

    # plt.imshow(input[0].reshape(IMG_NET_SIZE[0], IMG_NET_SIZE[1]), cmap="gray")
    # plt.show()

    # print("{:02d} {:02d} {:02d}".format(int(prediction[0][0] * 100),
    #                                    int(prediction[0][1] * 100),
    #                                    int(prediction[0][2] * 100)))

    print("-", end="\t")

    THRESHOLD = 0.6
    prediction = prediction[0]

    print(int(prediction[0] * 100),
          int(prediction[1] * 100),
          int(prediction[2] * 100),
          int(prediction[3] * 100), end="\t")

    highest = -1

    if prediction[0] < THRESHOLD and prediction[1] < THRESHOLD and prediction[2] < THRESHOLD and prediction[3] < THRESHOLD:
        print("--")
    else:
        CATEGORIES = ["EMPTY", "PAPER", "ROCK", "SCISSORS"]
        out = np.argmax(prediction)

        if isinstance(out, list):
            print(CATEGORIES[out[0]])
            highest = out[0]
        else:
            print(CATEGORIES[out])
            highest = out

    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image * 255))
    canvas.create_image(100, 50, image=photo, anchor=tkinter.E)

    if highest == 0:
        cv_img = cv.cvtColor(cv.imread("blank.png"), cv.COLOR_BGR2RGB)
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

    if highest == 1:
        cv_img = cv.cvtColor(cv.imread("scissors.png"), cv.COLOR_BGR2RGB)
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

    if highest == 2:
        cv_img = cv.cvtColor(cv.imread("paper.png"), cv.COLOR_BGR2RGB)
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

    if highest == 3:
        cv_img = cv.cvtColor(cv.imread("rock.png"), cv.COLOR_BGR2RGB)
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

    rawCapture.truncate(0)
    window.update()
