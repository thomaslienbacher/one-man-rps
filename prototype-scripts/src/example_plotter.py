"""
Dieses Script wird genutzt um die Beispiel Abbildungen für die schriftliche Arbeit zu generieren.
ACHTUNG: Dateipfade sind hardcoded!
"""

import cv2 as cv
import matplotlib
import matplotlib.pyplot as plt
import os
import random
from utils import *
from pprint import pprint

matplotlib.rcParams['figure.titlesize'] = 'large'
matplotlib.rcParams['font.size'] = 20

DATADIR = "E:/Thomas/one-man-rps/data"
CATEGORIES = ["scissors", "rock", "paper", "empty"]
KATEGORIEN = ["Schere", "Stein", "Papier", "Leer"]
SIZE = (450, 450)


def all_classes_color_bw():
    fig, axes = plt.subplots(2, 4, figsize=(14, 7))
    axes = axes.flatten()
    images = []

    for category in CATEGORIES:
        dir = os.path.join(DATADIR, "images/videostreaming", category)
        files = list(map(lambda f: os.path.join(dir, f), os.listdir(dir)))
        random.shuffle(files)
        img = cv.cvtColor(cv.imread(files[0]), cv.COLOR_BGR2RGB)
        images.append(cv.resize(img, SIZE))

    for img, ax in zip(images, axes[4:]):
        ax.imshow(img)
        ax.axis('off')

    for category, img, ax in zip(KATEGORIEN, images, axes[:4]):
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        ax.imshow(img, cmap="gray")
        ax.axis('off')
        ax.set_title(category)

    plt.tight_layout()
    path = os.path.join(DATADIR, "example_plotter_ac_" + time_escaped() + ".png")
    plt.savefig(path)
    plt.show()


def single_bw():
    images = []

    for category in CATEGORIES:
        dir = os.path.join(DATADIR, "images/all", category)
        files = list(map(lambda f: os.path.join(dir, f), os.listdir(dir)))
        random.shuffle(files)
        img = cv.cvtColor(cv.imread(files[0]), cv.COLOR_BGR2RGB)
        images.append(cv.resize(img, SIZE))

    for img, category in zip(images, CATEGORIES):
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        fig, axes = plt.subplots(1, 1, figsize=(5, 5))
        axes.imshow(img, cmap="gray")
        axes.axis('off')
        plt.tight_layout()
        path = os.path.join(DATADIR, "example_plotter_sb_" + category[:4] + "_" + time_escaped() + ".png")
        plt.savefig(path)
        plt.show()


def otsu_binarization():
    images = []

    for category in CATEGORIES:
        dir = os.path.join(DATADIR, "images/videostreaming", category)
        files = list(map(lambda f: os.path.join(dir, f), os.listdir(dir)))
        random.shuffle(files)
        img = cv.cvtColor(cv.imread(files[0]), cv.COLOR_BGR2RGB)
        images.append(cv.resize(img, (128, 128)))

    for img, category in zip(images, CATEGORIES):
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        ret1, th1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
        ret2, th2 = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        blur = cv.GaussianBlur(img, (5, 5), 0)
        ret3, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        transformed = [img, 0, th1,
                       img, 0, th2,
                       blur, 0, th3]
        titles = ['Original', 'Histogram', 'Global Thresholding (c = 127)',
                  'Original', 'Histogram', "Otsu's Thresholding",
                  'Gaussian Filter', 'Histogram', "Otsu's Thresholding"]

        fig, axes = plt.subplots(3, 3, figsize=(17, 16), gridspec_kw={'width_ratios': [4, 5, 4]})
        axes = axes.flatten()

        for i in range(3):
            axes[i * 3].imshow(transformed[i * 3], cmap="gray")
            axes[i * 3].axis('off')
            axes[i * 3].set_title(titles[i * 3])
            axes[i * 3].set_anchor('S')

            axes[i * 3 + 1].hist(transformed[i * 3].ravel(), bins=32)
            axes[i * 3 + 1].set_title(titles[i * 3 + 1])
            axes[i * 3 + 1].set_anchor('S')

            axes[i * 3 + 2].imshow(transformed[i * 3 + 2], cmap="gray")
            axes[i * 3 + 2].axis('off')
            axes[i * 3 + 2].set_title(titles[i * 3 + 2])
            axes[i * 3 + 2].set_anchor('S')

        plt.tight_layout()
        path = os.path.join(DATADIR, "example_plotter_ob_" + category[:4] + "_" + time_escaped() + ".png")
        plt.savefig(path)
        plt.show()


for _ in range(4):
    otsu_binarization()
