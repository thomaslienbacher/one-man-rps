"""
Dieses Script nimmt die transformierten Bilder und bereitet die Daten für
Tensorflow auf. Die Daten werden dabei in Arrays konvertiert und in eine Datei gespeichert,
diese Dateien werden dann von train_network.py genutzt, um das Neurale Netzwerk zu trainieren.
Diese Methode ist sehr ineffizient, da bei den großen Datenmengen extrem große Dateien entstehen, die
den gesamten Prozess sehr stark verlangsamen. ACHTUNG: Dateipfade sind hardcoded!
"""

import numpy as np
import os
import cv2
from tqdm import tqdm
import random
import pickle
import sys
import matplotlib.pyplot as plt
from utils import IMG_NET_SIZE

DATADIR = "E:/Thomas/one-man-rps/data"
CATEGORIES = ["rock", "paper", "scissors", "empty"]

dataset = []

print("Working in: ", DATADIR)

for category in CATEGORIES:
    print("Loading images for", category)

    path = os.path.join(DATADIR, "images/all", category)
    for file in tqdm(iterable=os.listdir(path)[:50], file=sys.stdout):
        img = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, IMG_NET_SIZE) / 255
        # img2 = cv2.flip(img, 1)

        dataset.append([img.reshape(IMG_NET_SIZE[0], IMG_NET_SIZE[1], 1), CATEGORIES.index(category)])
        # dataset.append([img2.reshape(IMG_NET_SIZE[0], IMG_NET_SIZE[1], 1), CATEGORIES.index(category)])
        # plt.imshow(img, cmap='gray')
        # plt.show()

random.shuffle(dataset)

X = []
y = []

for features, label in dataset:
    X.append(features)
    y.append(label)

print(type(X), type(y), type(dataset))

X = np.array(X)
y = np.array(y)

print(type(X), type(y))
print("Dumping X and y...")

path = os.path.join(DATADIR, "X.pickle")
pickle_out = open(path, "wb")
pickle.dump(X, pickle_out)
pickle_out.close()

path = os.path.join(DATADIR, "y.pickle")
pickle_out = open(path, "wb")
pickle.dump(y, pickle_out)
pickle_out.close()

print("Finished!")
