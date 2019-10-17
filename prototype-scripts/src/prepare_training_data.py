"""
Dieses Script nimmt die transformierten Bilder und bereitet die Daten für
Tensorflow auf. Diese Daten werden genutzt um das Neurale Netzwerk zu trainieren.
"""


import numpy as np
import os
import cv2
from tqdm import tqdm
import random
import pickle
import sys
import matplotlib.pyplot as plt

DATADIR = "E:/Thomas/one-man-rps/data"
CATEGORIES = ["rock", "paper", "scissors", "empty"]
SIZE = (140, 140)

dataset = []

print("Working in: ", DATADIR)

for category in CATEGORIES:
    print("Loading images for", category)

    path = os.path.join(DATADIR, "images", category)
    for file in tqdm(iterable=os.listdir(path), file=sys.stdout):
        img = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, SIZE)
        # output = [0, 0, 0]
        # output[CATEGORIES.index(category)] = 1
        dataset.append([img.reshape(SIZE[0], SIZE[1], 1), CATEGORIES.index(category)])
        # plt.imshow(img, cmap='gray')
        # plt.show()

random.shuffle(dataset)

X = []
y = []

for features, label in dataset:
    X.append(features)
    y.append(label)

X = np.array(X)
y = np.array(y)

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
