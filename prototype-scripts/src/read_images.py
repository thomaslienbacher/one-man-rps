"""
Dieses Script streamt das Video der PiCamera und visualisert die einzelnen Frames mittels
matplotlib. Die Plots werden dann innerhalb PyCharm visualisiert werden.
"""

import sys
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import matplotlib.pyplot as plt

# print some general information
print("Python: ", sys.version.replace("\n", " "))
print("OpenCV: ", cv2.__version__)

# initialize the camera and grab a reference to the raw camera capture
SIZE = (64, 64)
camera = PiCamera()
camera.resolution = SIZE
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=SIZE)

# allow the camera to warmup
time.sleep(0.5)

for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # show image
    plt.imshow(image)
    plt.show()

    print("Captured %d x %d" % (image.shape[1], image.shape[0]))

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
