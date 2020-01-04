"""
Diese Script liest die Bilder der Kamera aus und transformiert sie um einfacher
verabeitet werden zu können. Alle 30 Bilder wird eine Diagramm der derzeitigen Verarbeitung
dargestellt.
"""

import os
import cv2 as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import matplotlib.pyplot as plt

# setup
PRE_CONVERT = False  # wether to apply Otsu filtering to images
SIZE = (400, 400)
camera = PiCamera()
camera.resolution = SIZE
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=SIZE)
time.sleep(0.5)
counter = 20000
capturing = "empty"  # eg. scissors, rock, paper, empty

if not os.path.exists("/tmp/images/rock"):
    os.makedirs("/tmp/images/rock")

if not os.path.exists("/tmp/images/paper"):
    os.makedirs("/tmp/images/paper")

if not os.path.exists("/tmp/images/scissors"):
    os.makedirs("/tmp/images/scissors")

if not os.path.exists("/tmp/images/empty"):
    os.makedirs("/tmp/images/empty")

# start and wait until hand is ready to record
for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
    print("Captured:", counter)
    image = frame.array

    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    if PRE_CONVERT:
        ret1, th1 = cv.threshold(image, 127, 255, cv.THRESH_BINARY)
        # Otsu's thresholding
        ret2, th2 = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        # Otsu's thresholding after Gaussian filtering
        blur = cv.GaussianBlur(image, (5, 5), 0)
        ret3, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        print("and transformed!")
        cv.imwrite("/tmp/images/" + capturing + "/image{:04d}.jpg".format(counter), th3)
    else:
        cv.imwrite("/tmp/images/" + capturing + "/image{:04d}.jpg".format(counter), image)

    if counter % 80 == 0:
        if PRE_CONVERT:
            images = [image, 0, th1,
                      image, 0, th2,
                      blur, 0, th3]
            titles = ["Original Noisy Image", "Histogram", "Global Thresholding (v=127)",
                      "Original Noisy Image", "Histogram", "Otsu's Thresholding",
                      "Gaussian filtered Image", "Histogram", "Otsu's Thresholding"]

            for i in range(3):
                plt.subplot(3, 3, i * 3 + 1), plt.imshow(images[i * 3], "gray")
                plt.title(titles[i * 3]), plt.xticks([]), plt.yticks([])
                plt.subplot(3, 3, i * 3 + 2), plt.hist(images[i * 3].ravel(), 256)
                plt.title(titles[i * 3 + 1]), plt.xticks([]), plt.yticks([])
                plt.subplot(3, 3, i * 3 + 3), plt.imshow(images[i * 3 + 2], "gray")
                plt.title(titles[i * 3 + 2]), plt.xticks([]), plt.yticks([])
        else:
            fig = plt.figure(frameon=False, facecolor="white", figsize=(2, 2))
            ax = plt.Axes(fig, [0., 0., 1., 1.])
            ax.set_axis_off()
            fig.add_axes(ax)
            plt.imshow(cv.resize(image, (100, 100)), cmap="gray")
            plt.show()

        plt.show()

    counter += 1

    if counter % 500 == 0:
        print("Sleeping for 20 seconds...")
        time.sleep(20)

    if counter % 22000 == 0:
        print("Sleeping for 300 seconds...")
        time.sleep(300)

    rawCapture.truncate(0)
