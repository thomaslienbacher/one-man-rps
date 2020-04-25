"""
Dieses Script teilt alle Bilder in einen train und valid Ordner, die Trennung erfolgt mittels einfachen
Kopierens des Bildes in den Ordner. Die Bilder müssen getrennt werden, da für das Trainingsprogramm Bilder
benötigt werden, um es zu trainieren (train) und andere, um das Netzwerk nach einer Trainingsepoche zu testen
bzw. zu validieren (valid). ACHTUNG: Dateipfade sind hardcoded!
"""

import os
import random
import shutil
from tqdm import tqdm
import sys

DATADIR = "E:/Thomas/one-man-rps/data"
CATEGORIES = ["rock", "paper", "scissors", "empty"]
VALID_PERCENT = 0.2

print("splitting", 1 - VALID_PERCENT, "training +",
      VALID_PERCENT, "validation")
print("Working in: ", DATADIR)

for category in CATEGORIES:
    print("Splitting", category)
    dir = os.path.join(DATADIR, "images/all", category)
    dir2 = os.path.join(DATADIR, "images/videostreaming", category)
    files = list(map(lambda f: os.path.join(dir, f), os.listdir(dir))) + \
            list(map(lambda f: os.path.join(dir2, f), os.listdir(dir2)))
    random.shuffle(files)

    dst = os.path.join(DATADIR, "images/valid_example_3", category)
    # shutil.rmtree(dst)
    if not os.path.exists(dst):
        os.makedirs(dst)

    for file in tqdm(iterable=files[:-int(1. - VALID_PERCENT * len(files))],
                     file=sys.stdout):
        dst = os.path.join(DATADIR, "images/valid_example_3", category,
                           os.path.basename(os.path.normpath(file)))
        shutil.copyfile(file, dst)

    dst = os.path.join(DATADIR, "images/train_example_3", category)
    # shutil.rmtree(dst)
    if not os.path.exists(dst):
        os.makedirs(dst)

    for file in tqdm(iterable=files[int(VALID_PERCENT * len(files)):],
                     file=sys.stdout):
        dst = os.path.join(DATADIR, "images/train_example_3", category,
                           os.path.basename(os.path.normpath(file)))
        shutil.copyfile(file, dst)

print("Finished!")
