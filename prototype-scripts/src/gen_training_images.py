"""
Diese Script liest die Bilder der Kamera aus und transformiert sie um einfacher
verabeitet werden zu können. Alle 30 Bilder wird eine Diagramm der derzeitigen Verarbeitung
dargestellt.
"""


import cv2 as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import matplotlib.pyplot as plt

# setup
SIZE = (64, 64)
camera = PiCamera()
camera.resolution = SIZE
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=SIZE)
time.sleep(0.5)
counter = 0

# start and wait until hand is ready to record
for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
    print("Captured:", counter, end=' ')
    image = frame.array

    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

    ret1, th1 = cv.threshold(image, 127, 255, cv.THRESH_BINARY)
    # Otsu's thresholding
    ret2, th2 = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # Otsu's thresholding after Gaussian filtering
    blur = cv.GaussianBlur(image, (5, 5), 0)
    ret3, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # image = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 21, 0)
    cv.imwrite("/tmp/images/paper/image{:04d}.jpg".format(counter), th3)
    print("and transformed!")

    if counter % 200 == 0:
        images = [image, 0, th1,
                  image, 0, th2,
                  blur, 0, th3]
        titles = ['Original Noisy Image', 'Histogram', 'Global Thresholding (v=127)',
                  'Original Noisy Image', 'Histogram', "Otsu's Thresholding",
                  'Gaussian filtered Image', 'Histogram', "Otsu's Thresholding"]

        for i in range(3):
            plt.subplot(3, 3, i * 3 + 1), plt.imshow(images[i * 3], 'gray')
            plt.title(titles[i * 3]), plt.xticks([]), plt.yticks([])
            plt.subplot(3, 3, i * 3 + 2), plt.hist(images[i * 3].ravel(), 256)
            plt.title(titles[i * 3 + 1]), plt.xticks([]), plt.yticks([])
            plt.subplot(3, 3, i * 3 + 3), plt.imshow(images[i * 3 + 2], 'gray')
            plt.title(titles[i * 3 + 2]), plt.xticks([]), plt.yticks([])

        plt.show()

    counter += 1
    rawCapture.truncate(0)
