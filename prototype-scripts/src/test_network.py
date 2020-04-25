"""
Dieses Script laded ein vortrainiertes Neural Netzwerk, und testet es mit
Echtzeit Bildern von der Kamera. Die Ergebnisse der Erkennung werden in der Konsole ausgegeben.
Die Kamera Frames werden mittels matplotlib visualisiert und können in PyCharm angesehen werden.
ACHTUNG: Dateipfade sind hardcoded!
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

DATADIR = "/home/pi/one-man-rps/data/model_backups"

camera = PiCamera()
camera.vflip = True
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

for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
    image = frame.array
    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY) / 255
    input = image.reshape(1, IMG_NET_SIZE[0], IMG_NET_SIZE[1], 1)

    prediction = model.predict([input])

    fig = plt.figure(frameon=False, facecolor="white", figsize=(2, 2))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(input[0].reshape(IMG_NET_SIZE[0], IMG_NET_SIZE[1]), cmap="gray")
    plt.show()

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

    # print(highest)
    rawCapture.truncate(0)
