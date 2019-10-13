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

DATADIR = "/tmp"
SIZE = (64, 64)

camera = PiCamera()
camera.resolution = SIZE
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=SIZE)
time.sleep(0.5)
counter = 0

path = os.path.join(DATADIR, "model_architecture.json")
with open(path, "r") as f:
    model = model_from_json(f.read())
path = os.path.join(DATADIR, "model_weights.h5")
model.load_weights(path)
print("Loaded model!")

for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
    print("Captured .. ", end='')
    image = frame.array
    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    input = image.reshape(1, SIZE[0], SIZE[1], 1)

    prediction = model.predict([input])

    print("predicted")

    # plt.imshow(image, cmap="gray")
    # plt.show()

    print("{:02d} {:02d} {:02d}".format(int(prediction[0][0] * 100),
                                        int(prediction[0][1] * 100),
                                        int(prediction[0][2] * 100)))
    # print("{}".format(prediction))
    rawCapture.truncate(0)
