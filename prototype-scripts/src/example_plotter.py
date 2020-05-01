"""
Dieses Script wird genutzt, um die Beispiel Abbildungen für die schriftliche Arbeit zu generieren.
ACHTUNG: Dateipfade sind hardcoded!
"""

import cv2 as cv
import matplotlib
import matplotlib.pyplot as plt
import os
import random

from matplotlib import gridspec
from utils import *
import numpy as np
from pprint import pprint
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# matplotlib.rcParams['figure.titlesize'] = 'large'
# matplotlib.rcParams['font.size'] = 20

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
    img = cv.cvtColor(cv.imread(r"E:\Thomas\one-man-rps\data\scissors_8609.png"), cv.COLOR_BGR2RGB)
    images.append(cv.resize(img, (128, 128)))

    for category in CATEGORIES:
        dir = os.path.join(DATADIR, "images/videostreaming", category)
        files = list(map(lambda f: os.path.join(dir, f), os.listdir(dir)))
        random.shuffle(files)
        img = cv.cvtColor(cv.imread(files[0]), cv.COLOR_BGR2RGB)
        # images.append(cv.resize(img, (128, 128)))

    for img, category in zip(images, CATEGORIES):
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        ret1, th1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
        ret2, th2 = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        blur = cv.GaussianBlur(img, (5, 5), 0)
        ret3, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        transformed = [img, 0, th1,
                       img, 0, th2,
                       blur, 0, th3]
        titles = ['Original', 'Histogramm', 'Schwellenwert (c = 127)',
                  'Original', 'Histogramm', "Otsu's Methode",
                  'Gaußsche Unschärfe', 'Histogramm', "Otsu's Methode"]

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

        # fig.suptitle("Beispiel Otsu's Methode", y=0.4)
        plt.tight_layout()
        path = os.path.join(DATADIR, "example_plotter_ob_" + category[:4] + "_" + time_escaped() + ".png")
        plt.savefig(path)
        plt.show()


def perf_trace_2():
    fig, axes = plt.subplots(2, 1, figsize=(12, 14))
    axes = axes.flatten()

    x = np.arange(0, 30, 0.02)  # start,stop,step
    y = np.cos(x / 7) * 40 + 50
    z = np.cos(x / 4) * 40 + 50

    axes[0].plot(x, y)
    axes[0].set_xlabel('Trainingszeit bis 30s')
    axes[0].set_ylabel('prozentuelle Auslastung')
    axes[0].set_title('Auslastung CPU')
    axes[0].set_xlim([0, 30])
    axes[0].set_ylim([0, 100])

    axes[1].plot(x, z)
    axes[1].set_xlabel('Trainingszeit bis 30s')
    axes[1].set_ylabel('prozentuelle Auslastung')
    axes[1].set_title('Auslastung HDD')
    axes[1].set_xlim([0, 30])
    axes[1].set_ylim([0, 100])

    plt.tight_layout()
    path = os.path.join(DATADIR, "example_plotter_pts2_" + time_escaped() + ".png")
    plt.savefig(path)
    plt.show()


def perf_trace_1():
    x = np.arange(0, 30, 0.02)  # start,stop,step
    y = np.cos(x / 7) * 40 + 50
    z = np.cos(x / 4) * 40 + 50

    plt.figure(figsize=(12, 7))
    plt.plot(x, y, x, z)
    plt.xlabel('Trainingszeit bis 35s')
    plt.ylabel('prozentuelle Auslastung')
    plt.title('Auslastung CPU und HDD')
    plt.legend(['CPU', 'HDD'])
    plt.xlim([0, 30])
    plt.ylim([0, 130])

    plt.tight_layout()
    path = os.path.join(DATADIR, "example_plotter_pts1_" + time_escaped() + ".png")
    plt.savefig(path)
    plt.show(bbox_inches='tight', pad_inches=0)


def image_data_generator():
    DATADIR = "E:/Thomas/one-man-rps/data"
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=20,
        width_shift_range=0.18,
        height_shift_range=0.18,
        shear_range=0.18,
        zoom_range=0.20,
        brightness_range=(0.80, 1.20),
    )

    train_generator = train_datagen.flow_from_directory(
        directory=os.path.join(DATADIR, "image_data_generator"),
        target_size=(280, 280),
        color_mode="grayscale",
        batch_size=200,
        class_mode="sparse",
        shuffle=False,
    )

    fig, axes = plt.subplots(6, 4, figsize=(12, 18))
    axes = axes.flatten()

    for i in range(6):
        sample_training_images, _ = next(train_generator)

        for img, a in zip(sample_training_images[:4], range(4)):
            d = [3, 2, 1, 0][a]
            axes[i * 4 + d].imshow(img.reshape(280, 280), cmap="gray")
            axes[i * 4 + d].axis('off')
            if i == 0:
                axes[i * 4 + d].set_title(KATEGORIEN[d])

    plt.tight_layout()
    path = os.path.join(DATADIR, "examples_figure_idg_" + time_escaped() + ".png")
    plt.savefig(path)
    plt.show()


def training_data():
    amount = 6
    fig, axes = plt.subplots(3, amount, figsize=(6 * 5, 3 * 5))
    axes = axes.flatten()
    images = []

    for category in CATEGORIES:
        dir = os.path.join(DATADIR, "images/videostreaming", category)
        files = list(map(lambda f: os.path.join(dir, f), os.listdir(dir)))
        random.shuffle(files)
        for j in range(amount):
            img = cv.cvtColor(cv.imread(files[j]), cv.COLOR_BGR2RGB)
            images.append(cv.resize(img, SIZE))

    random.shuffle(images)

    for img, ax in zip(images, axes):
        ax.imshow(img)
        ax.axis('off')

    plt.tight_layout()
    path = os.path.join(DATADIR, "example_plotter_td_" + time_escaped() + ".png")
    plt.savefig(path)
    plt.show()


def sample_model_statistics():
    epochs = 14
    x = np.arange(0, epochs, 0.1)  # start,stop,step
    y = np.cos(x * 0.4) / 2 + 0.5
    z = np.cos(x * 0.3) / 2 + 0.5

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(x, -y + 1, label="Trainings Accuracy")
    plt.plot(x, -z + 1, label="Validierungs Accuracy")
    plt.legend(loc="lower right")
    plt.title("Trainings und Validierungs Accuracy")
    plt.xlabel('Epochen')

    plt.subplot(1, 2, 2)
    plt.plot(x, y, label="Trainings Loss")
    plt.plot(x, z, label="Validierungs Loss")
    plt.legend(loc="upper right")
    plt.title("Trainings und Validierungs Loss")
    plt.xlabel('Epochen')

    # plt.tight_layout()
    path = os.path.join(DATADIR, "example_plotter_sms_" + time_escaped() + ".png")
    plt.savefig(path)
    # plt.show(bbox_inches='tight', pad_inches=0)
    plt.show()


def three():
    path = os.path.join(DATADIR, "three.png")
    img = cv.cvtColor(cv.imread(path), cv.COLOR_BGR2RGB)
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    plt.figure(figsize=(2, 2))

    plt.imshow(img, cmap='gray', interpolation='nearest')
    plt.xlim([0, 64])
    plt.ylim([64, 0])
    plt.xticks([0, 16, 32, 48, 64])
    plt.yticks([0, 16, 32, 48, 64])

    # plt.xticks([0, 8, 16, 24, 32, 40, 48, 56, 64])
    # plt.yticks([0, 8, 16, 24, 32, 40, 48, 56, 64])

    plt.tight_layout()
    path = os.path.join(DATADIR, "example_plotter_3_" + time_escaped() + ".svg")
    plt.savefig(path)
    plt.show(bbox_inches='tight', pad_inches=0)
    # plt.show()


for _ in range(1):
    three()
