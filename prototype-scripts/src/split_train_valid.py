"""
Dieses Script teilt die Bilder in train und valid Ordner, indem sie kopiert werden.
"""

import os
import random
import shutil
from tqdm import tqdm
import sys

DATADIR = "E:/Thomas/one-man-rps/data"
CATEGORIES = ["rock", "paper", "scissors", "empty"]
VALID_PERCENT = 0.35

print("Working in: ", DATADIR)

for category in CATEGORIES:
    print("Splitting", category)
    dir = os.path.join(DATADIR, "images/all", category)
    files = os.listdir(dir)

    random.shuffle(files)

    dst = os.path.join(DATADIR, "images/valid", category)
    shutil.rmtree(dst)
    if not os.path.exists(dst):
        os.makedirs(dst)

    for file in tqdm(iterable=files[:-int(1. - VALID_PERCENT * len(files))], file=sys.stdout):
        src = os.path.join(dir, file)
        dst = os.path.join(DATADIR, "images/valid", category, file)

        shutil.copyfile(src, dst)

    dst = os.path.join(DATADIR, "images/train", category)
    shutil.rmtree(dst)
    if not os.path.exists(dst):
        os.makedirs(dst)

    for file in tqdm(iterable=files[int(VALID_PERCENT * len(files)):], file=sys.stdout):
        src = os.path.join(dir, file)
        dst = os.path.join(DATADIR, "images/train", category, file)
        shutil.copyfile(src, dst)

print("Finished!")
