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

DATADIR = "/home/pi"

camera = PiCamera()
camera.resolution = IMG_NET_SIZE
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=IMG_NET_SIZE)
time.sleep(0.5)
counter = 0

path = os.path.join(DATADIR, "model_architecture.json")
with open(path, "r") as f:
    model = model_from_json(f.read())
path = os.path.join(DATADIR, "model_weights.h5")
model.load_weights(path)
print("Loaded model!")

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

    if prediction[0] < THRESHOLD and prediction[1] < THRESHOLD and prediction[2] < THRESHOLD and prediction[3] < THRESHOLD:
        print("--")
    else:
        CATEGORIES = ["ROCK", "PAPER", "SCISSORS", "EMPTY"]
        out = np.argmax(prediction)

        if isinstance(out, list):
            print(CATEGORIES[out[0]])
        else:
            print(CATEGORIES[out])

    rawCapture.truncate(0)
